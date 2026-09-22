"""Loads all data files in-process and checks the logs they produce.

Fails on any ERROR-level log record. Compares WARNING-level messages against
``tests/expected-warnings.txt``: a new line there is allowed only in a commit
that adds a check, and every line is a resolution owed. Regenerate with
``PHYLOHIST_UPDATE_EXPECTED=1 poetry run pytest``. The load itself is the
session fixture in ``conftest.py``.

``PHYLOHIST_DRAFTS=1`` also loads the unaudited trees under ``drafts/``
(the CLI's ``--draft``). Drafts are expected to produce errors and
warnings until their records exist, so the warning snapshot is not
compared in that mode; the error test still reports what a draft needs.
"""

import logging
import os
import pathlib

import pytest

EXPECTED_WARNINGS_PATH = pathlib.Path(__file__).parent / 'expected-warnings.txt'

EXPECTED_WARNINGS_HEADER = """\
# Expected WARNING-level messages from loading all data files.
# A new line here is allowed only in a commit that adds a check; every line
# is a resolution owed. Regenerate with:
#   PHYLOHIST_UPDATE_EXPECTED=1 poetry run pytest
"""


def test_no_errors(load_records):
  _, records, _ = load_records
  errors = [r for r in records if r.levelno >= logging.ERROR]
  if errors:
    message = '\n'.join(r.getMessage() for r in errors)
    pytest.fail(f'{len(errors)} ERROR-level log records:\n{message}')


def test_data_loaded(load_records):
  data, _, _ = load_records
  assert data['trees'], 'load produced no trees; check for a silent empty load'


def test_expected_warnings(load_records):
  if os.getenv('PHYLOHIST_DRAFTS'):
    pytest.skip('drafts loaded; the warning snapshot covers data/ only')
  _, records, _ = load_records
  actual = sorted({r.getMessage() for r in records if r.levelno == logging.WARNING})

  if os.getenv('PHYLOHIST_UPDATE_EXPECTED') and not os.getenv('CI'):
    # Regenerate the snapshot; never on CI, where it would hide a regression.
    with open(EXPECTED_WARNINGS_PATH, 'w') as fd:
      fd.write(EXPECTED_WARNINGS_HEADER)
      for message in actual:
        fd.write(f'{message}\n')
    return

  expected = set()
  if EXPECTED_WARNINGS_PATH.exists():
    with open(EXPECTED_WARNINGS_PATH) as fd:
      for line in fd:
        line = line.strip()
        if not line or line.startswith('#'):
          continue
        expected.add(line)

  actual_set = set(actual)
  unexpected = actual_set - expected
  stale = expected - actual_set

  if unexpected or stale:
    parts = []
    if unexpected:
      parts.append(
        'Unexpected warnings (not in tests/expected-warnings.txt):\n'
        + '\n'.join(sorted(unexpected)),
      )
    if stale:
      parts.append(
        'Stale expected warnings (no longer produced):\n' + '\n'.join(sorted(stale)),
      )
    pytest.fail('\n\n'.join(parts))


def test_invalid_tree_raises(tmp_path):
  # A file that fails the schema stops the load with an error the caller
  # can handle, instead of ending the process.
  from phylohist.loader import io

  schema = io.build_schema()
  (tmp_path / 'broken.yaml').write_text('tree:\n  rnak: genus\n')
  with pytest.raises(io.LoadError, match='broken.yaml'):
    io._load_tree_dir(tmp_path, schema['trees'], {})


def test_load_fails_on_logged_errors(monkeypatch):
  # The checks report by logging; the load counts what they logged and
  # refuses to hand over a broken corpus unless asked to.
  import importlib

  from phylohist.loader import LoadError, load

  loading = importlib.import_module('phylohist.loader.load')

  def broken(drafts=False):
    logging.getLogger('phylohist.loader.taxa').error('a check fired')
    return {k: {} for k in ('authors', 'publications', 'sources', 'taxa', 'trees', 'time')}

  monkeypatch.setattr(loading, 'load_files', broken)
  with pytest.raises(LoadError, match='1 integrity error while loading'):
    load()
  data, roots = load(tolerate=True)
  assert data['trees'] == {} and roots == {}


def test_counting_errors_counts_only_errors():
  from phylohist.loader import counting_errors

  with counting_errors() as errors:
    logging.getLogger('phylohist.loader.io').warning('not counted')
    logging.getLogger('phylohist.loader.io').error('counted')
    logging.getLogger('phylohist.loader.research').error('counted too')
  assert errors.count == 2


def test_tree_without_a_source_record_is_skipped(monkeypatch):
  # A draft keyed by a source with no record used to crash the load in
  # the tree's hashing; now it is one logged error and no tree.
  import importlib

  from phylohist.loader import LoadError, load

  loading = importlib.import_module('phylohist.loader.load')

  def orphan(drafts=False):
    data = {k: {} for k in ('authors', 'publications', 'sources', 'taxa', 'time')}
    data['trees'] = {'9999_nobody': {'taxonomies': [{'taxon': 'cyathocystis'}]}}
    return data

  monkeypatch.setattr(loading, 'load_files', orphan)
  with pytest.raises(LoadError, match='1 integrity error'):
    load()
  _, roots = load(tolerate=True)
  assert roots == {}
