"""Loads all data files in-process and checks the logs they produce.

Fails on any ERROR-level log record. Compares WARNING-level messages against
``tests/expected-warnings.txt``: a new line there is allowed only in a commit
that adds a check, and every line is a resolution owed, so a line the load
no longer produces is only a warning here; ``poetry run regenerate`` drops it
(`scripts/expected_warnings.py`). The load itself is the ``production``
fixture in ``conftest.py``; these are the tests about the curated corpus,
marked ``production``.

``PHYLOHIST_DRAFTS=1`` also loads the unaudited trees under ``drafts/``
(the CLI's ``--draft``). Drafts are expected to produce errors and
warnings until their records exist, so the warning snapshot is not
compared in that mode; the error test still reports what a draft needs.
"""

import logging
import os
import pathlib
import warnings

import pytest

from tests import support

EXPECTED_WARNINGS_PATH = pathlib.Path(__file__).parent / 'expected-warnings.txt'


@pytest.mark.production
def test_no_errors(production):
  errors = [r for r in production.records if r.levelno >= logging.ERROR]
  if errors:
    message = '\n'.join(r.getMessage() for r in errors)
    pytest.fail(f'{len(errors)} ERROR-level log records:\n{message}')


@pytest.mark.production
def test_data_loaded(production):
  assert production.data['trees'], 'load produced no trees; check for a silent empty load'


@pytest.mark.production
def test_expected_warnings(production):
  if os.getenv('PHYLOHIST_DRAFTS'):
    pytest.skip('drafts loaded; the warning snapshot covers data/ only')
  actual = {r.getMessage() for r in production.records if r.levelno == logging.WARNING}
  expected = support.script('expected_warnings').read_expected(EXPECTED_WARNINGS_PATH)

  stale = expected - actual
  if stale:
    # A resolved warning is progress: `regenerate` drops its line, and CI's
    # diff of the derived files catches a line left behind.
    warnings.warn(
      f'{len(stale)} expected warnings are no longer produced; run `poetry run regenerate`:\n'
      + '\n'.join(sorted(stale)),
      stacklevel=1,
    )
  unexpected = actual - expected
  if unexpected:
    pytest.fail(
      'Unexpected warnings (not in tests/expected-warnings.txt; a new line there is allowed '
      'only in a commit that adds a check):\n' + '\n'.join(sorted(unexpected))
    )


def test_invalid_tree_raises(tmp_path):
  # A file that fails the schema stops the load with an error the caller
  # can handle, instead of ending the process.
  from phylohist.loader import io

  schema = io.build_schema()
  (tmp_path / 'broken.yaml').write_text('tree:\n  rnak: genus\n')
  with pytest.raises(io.LoadError, match='broken.yaml'):
    io.load_checked(tmp_path / 'broken.yaml', schema[io.TREE_DEF])
  # A definition the schema lacks is an error the loader names, too.
  with pytest.raises(io.LoadError, match='no schema definition for "trees"'):
    schema['trees']


def test_schema_error_names_its_file(tmp_path, caplog):
  # The file name was only on the INFO line above the dump.
  from phylohist.loader import io

  schema = io.build_schema()
  broken = tmp_path / 'broken.yaml'
  broken.write_text('tree:\n  rnak: genus\n')
  with caplog.at_level(logging.ERROR, logger='phylohist'), pytest.raises(io.LoadError):
    io.load_checked(broken, schema[io.TREE_DEF])
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert errors and all(m.startswith(f'"{broken}" is not valid:\n') for m in errors)
  # A file under the repository is named by its path from the root.
  assert io.display_path(io.TREE_DIR / '1761_linnaeus.yaml') == 'data/trees/1761_linnaeus.yaml'


def test_data_files_in_load_order():
  # The record files, then the audited trees, then the drafts: a draft
  # loads last so that it replaces the audited tree of its source.
  from phylohist.loader import io

  files = io.data_files(drafts=True)
  names = [name for name, _ in files]
  assert names[: len(io.RECORD_FILES)] == [
    'authors',
    'publications',
    'sources',
    'taxa',
    'sections',
    'repositories',
    'roles',
  ]
  trees = [path for name, path in files if name == io.TREE_DEF]
  assert trees == io.tree_files(drafts=True)
  dirs = [path.parent for path in trees]
  assert dirs == sorted(dirs, key=lambda d: d != io.TREE_DIR) and io.DRAFT_DIR in dirs
  assert [path for _, path in io.data_files()] == [*io.RECORD_FILES, *io.tree_files()]


def test_load_fails_on_logged_errors(monkeypatch):
  # The checks report by logging; the load counts what they logged and
  # refuses to hand over a broken corpus unless asked to.
  import importlib

  from phylohist.loader import LoadError, load

  loading = importlib.import_module('phylohist.loader.load')

  def broken(drafts=False, **_):
    logging.getLogger('phylohist.loader.taxa').error('a check fired')
    return {k: {} for k in ('authors', 'publications', 'sources', 'taxa', 'sections', 'trees')}

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

  def orphan(drafts=False, **_):
    data = {k: {} for k in ('authors', 'publications', 'sources', 'taxa', 'sections')}
    data['trees'] = {'9999_nobody': {'taxonomies': [{'taxon': 'cyathocystis'}]}}
    return data

  monkeypatch.setattr(loading, 'load_files', orphan)
  with pytest.raises(LoadError, match='1 integrity error'):
    load()
  _, roots = load(tolerate=True)
  assert roots == {}
