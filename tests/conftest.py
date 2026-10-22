"""What every test module shares: the test corpus, its claim table, and
the curated corpus for the checks that are about it.

`tests/corpus/` is a frozen copy of `data/` (its README says from where).
`corpus` loads it once per process and writes its claim table to a
temporary directory, so the tests read the shapes the tools read over
`claims/` without depending on what the curated data says today. The
loaded `Corpus` is `corpus.records`; a test that adds records or builds
trees takes `records`, its own copy, so the session's stays as the load
left it (`_isolated` checks), and every test has the tools' store over the
corpus; `store` and `closure` are over the corpus too. `production` loads
`data/` for the tests marked `production`, which are about the curated
corpus itself. The tests marked
`demo` run the eval questions and the walkthrough over the committed
`claims/`; they hold for the data they were last refreshed against, so
they run only with `--demo`.
"""

import os
import types

import pytest

from phylohist import tools
from phylohist.claims import extract, manifest
from phylohist.closure import Closure
from phylohist.loader import collecting, load
from phylohist.tools import ClaimStore
from tests import support


def pytest_addoption(parser):
  parser.addoption(
    '--demo',
    action='store_true',
    help='run the eval questions and the walkthrough over the committed claims/',
  )


def pytest_collection_modifyitems(config, items):
  if config.getoption('--demo'):
    return
  skip = pytest.mark.skip(reason='a demo over the committed claims/; run with --demo')
  for item in items:
    if 'demo' in item.keywords:
      item.add_marker(skip)


def _load(**kwargs):
  """``(records, logged)``: a tolerated load (a fresh `Corpus`) and what it
  logged (the `collecting` collector), for a test to assert on."""
  with collecting() as logged:
    records = load(tolerate=True, **kwargs)
  return records, logged


@pytest.fixture(scope='session')
def corpus(tmp_path_factory):
  """The test corpus: the loaded `Corpus` (`records`), what its load
  logged, its claims by source and the directory they are written to, and
  a store over them."""
  records, logged = _load(data_dir=support.CORPUS, fast=True)
  errors = [r.getMessage() for r in logged.errors]
  assert not errors, 'tests/corpus does not load cleanly:\n' + '\n'.join(errors)
  claims_by_source = extract(records)
  claims = tmp_path_factory.mktemp('corpus-claims')
  support.script('claims').write(claims, records, claims_by_source, full=True)
  return types.SimpleNamespace(
    records=records,
    logged=logged,
    claims_by_source=claims_by_source,
    claims=claims,
    store=ClaimStore(claims),
  )


@pytest.fixture
def records(corpus):
  """The loaded corpus for one test: what the test adds, deletes or builds
  stays in this copy."""
  return corpus.records.copy()


@pytest.fixture(autouse=True)
def _isolated(corpus):
  """The tools' store over the corpus for every test; afterwards, the
  session's corpus as the load left it."""
  tools._store = corpus.store
  before = support.footprint(corpus.records)
  yield
  assert support.footprint(corpus.records) == before, (
    'a test changed the session corpus; use `records`'
  )


@pytest.fixture(scope='session')
def store(corpus):
  return corpus.store


@pytest.fixture(scope='session')
def closure(store):
  return Closure(store)


@pytest.fixture(scope='session')
def production():
  """`data/` loaded (and `drafts/` under `PHYLOHIST_DRAFTS`): its data,
  what the load logged, and its manifest when the load logged no error."""
  records, logged = _load(drafts=bool(os.getenv('PHYLOHIST_DRAFTS')), fast=True)
  report = manifest(records, extract(records)) if not logged.errors else None
  return types.SimpleNamespace(data=records.data, logged=logged, manifest=report)


@pytest.fixture(scope='session')
def production_store():
  """A store over the committed `claims/`, for the demos."""
  return ClaimStore()


@pytest.fixture
def demo_store(production_store, monkeypatch):
  """The tools over the committed `claims/`, for one test."""
  monkeypatch.setattr(tools, '_store', production_store)
