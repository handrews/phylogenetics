"""What every test module shares: the test corpus, its claim table, and
the curated corpus for the checks that are about it.

`tests/corpus/` is a frozen copy of `data/` (its README says from where).
`corpus` loads it once per process and writes its claim table to a
temporary directory, so the tests read the shapes the tools read over
`claims/` without depending on what the curated data says today. `Taxon`
and `Tree` keep class-level registries, so every test starts with them as
that load left them (`support.restore`), whatever the tests before it
added, and with the tools' store over the corpus; `store` and `closure`
are over the corpus too. `production` loads `data/` for the tests marked
`production`, which are about the curated corpus itself. The tests marked
`demo` run the eval questions and the walkthrough over the committed
`claims/`; they hold for the data they were last refreshed against, so
they run only with `--demo`.
"""

import logging
import os
import types

import pytest

from phylohist import tools
from phylohist.claims import extract, manifest
from phylohist.closure import Closure
from phylohist.loader import load
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


class _CollectingHandler(logging.Handler):
  def __init__(self):
    super().__init__()
    self.records = []

  def emit(self, record):
    self.records.append(record)


def _load(**kwargs):
  """``(data, records, roots)``: a tolerated load and the log records it
  produced, for a test to assert on."""
  handler = _CollectingHandler()
  logger = logging.getLogger('phylohist')
  logger.addHandler(handler)
  try:
    data, roots = load(tolerate=True, **kwargs)
  finally:
    logger.removeHandler(handler)
  return data, handler.records, roots


@pytest.fixture(scope='session')
def corpus(tmp_path_factory):
  """The test corpus: its data, log records and roots, its claims by source
  and the directory they are written to, a store over them, and the
  registries as the load left them."""
  support.reset()
  data, records, roots = _load(data_dir=support.CORPUS, fast=True)
  errors = [r.getMessage() for r in records if r.levelno >= logging.ERROR]
  assert not errors, 'tests/corpus does not load cleanly:\n' + '\n'.join(errors)
  claims_by_source = extract(roots)
  claims = tmp_path_factory.mktemp('corpus-claims')
  support.script('claims').write(claims, claims_by_source, roots, full=True)
  return types.SimpleNamespace(
    data=data,
    records=records,
    roots=roots,
    claims_by_source=claims_by_source,
    claims=claims,
    store=ClaimStore(claims),
    registries=support.snapshot(),
  )


@pytest.fixture(autouse=True)
def _isolated(corpus):
  """The registries as the corpus load left them, and the tools' store
  over the corpus, before every test."""
  support.restore(corpus.registries)
  tools._store = corpus.store


@pytest.fixture(scope='session')
def load_records(corpus):
  """``(data, records, roots)`` of the corpus: the older name of the load."""
  return corpus.data, corpus.records, corpus.roots


@pytest.fixture(scope='session')
def store(corpus):
  return corpus.store


@pytest.fixture(scope='session')
def closure(store):
  return Closure(store)


@pytest.fixture(scope='session')
def production(corpus):
  """`data/` loaded (and `drafts/` under `PHYLOHIST_DRAFTS`): its data, the
  log records, and its manifest when the load logged no error. The
  registries are the corpus's again afterwards."""
  support.reset()
  try:
    data, records, roots = _load(drafts=bool(os.getenv('PHYLOHIST_DRAFTS')), fast=True)
    clean = not any(r.levelno >= logging.ERROR for r in records)
    report = manifest(extract(roots), roots) if clean else None
  finally:
    support.restore(corpus.registries)
  return types.SimpleNamespace(data=data, records=records, manifest=report)


@pytest.fixture(scope='session')
def production_store():
  """A store over the committed `claims/`, for the demos."""
  return ClaimStore()


@pytest.fixture
def demo_store(production_store, monkeypatch):
  """The tools over the committed `claims/`, for one test."""
  monkeypatch.setattr(tools, '_store', production_store)
