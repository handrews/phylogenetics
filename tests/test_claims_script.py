"""`report_inconsistencies` in scripts/claims.py: the explanation it prints
for each kind of manifest inconsistency row, on a synthetic tree;
`--errors-only`, over a load that logs what the test says, and the lines
the script itself logs when a load fails or errs; and the pruning of the
expected-warnings file from the same load."""

import logging

from phylohist import regenerate
from phylohist.claims import extract
from phylohist.loader import LoadError
from phylohist.loader.research import Source
from phylohist.loader.taxa import Tree
from tests import support

claims_script = support.script('claims')

_WHERE = 'in data/sources.yaml (1961_dehm.audit.coverage.{})'


def _report(capsys, roots):
  found = claims_script.report_inconsistencies(extract(roots), roots)
  return found, capsys.readouterr().out


def test_report_explains_both_row_forms(monkeypatch, capsys):
  coverage = Source.get('1961_dehm')._data['audit']['coverage']
  roots = {
    '1961_dehm': [
      Tree(
        {
          'taxon': 'pyrgocystis',
          'children': [
            {'taxon': 'grayae_bather_1915', 'illustrations': None},
            {'taxon': 'sardesoni_bather_1915'},
          ],
        },
        {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 0},
      )
    ]
  }
  # A kind the tree's nulls derive and the audit block declares as well:
  # the row has no claim count, and the report says to drop the declaration.
  monkeypatch.setitem(coverage, 'illustrations', 'none')
  # A kind only declared, against the claims counted: no synonymy entry in
  # the tree beside a declared `all`.
  monkeypatch.setitem(coverage, 'synonymy', 'all')

  found, out = _report(capsys, roots)
  assert found >= 1
  # The source's review file is named when there is one.
  assert '1961_dehm  (notes/reviews/review_1961_dehm.md)' in out
  assert (
    f'  illustrations: declared none {_WHERE.format("illustrations")} '
    'but derived from the tree (partly); remove the declaration'
  ) in out
  assert f'  synonymy: declared all {_WHERE.format("synonymy")}; no claims derived' in out
  assert 'nothing in data/trees/1961_dehm.yaml yields a countable claim of this kind' in out
  assert 'to resolve: enter what the paper prints, or declare na or none' in out


def test_report_lists_holotypes_that_differ_without_counting_them(capsys):
  def tree(source, prefix, number):
    return Tree(
      {
        'taxon': 'navicula_whitehouse_1941',
        'material': [{'role': 'holotype', 'prefix': prefix, 'numbers': [number]}],
      },
      {
        'source_key': source,
        'type': 'taxonomy',
        'position': 0,
        'file_prefixes': {prefix: 'uq-f'},
      },
    )

  roots = {
    '2021_jell_sprinkle': [tree('2021_jell_sprinkle', 'UQF', 9)],
    '1941_whitehouse': [tree('1941_whitehouse', 'F.', 5404)],
  }
  found, out = _report(capsys, roots)
  # Per-source rows come first and are all that is counted.
  assert out.index(f'{found} sources with inconsistencies') < out.index(
    'holotypes that differ between sources:'
  )
  assert out.endswith(
    'holotypes that differ between sources:\n'
    '  navicula_whitehouse_1941: 1941_whitehouse F. 5404; 2021_jell_sprinkle UQF 9\n'
  )


def test_report_prints_no_holotype_section_when_none_differ(capsys):
  roots = {
    '1941_whitehouse': [
      Tree(
        {
          'taxon': 'navicula_whitehouse_1941',
          'material': [{'role': 'holotype', 'prefix': 'F.', 'numbers': [5404]}],
        },
        {
          'source_key': '1941_whitehouse',
          'type': 'taxonomy',
          'position': 0,
          'file_prefixes': {'F.': 'uq-f'},
        },
      )
    ]
  }
  _, out = _report(capsys, roots)
  assert 'holotypes that differ' not in out


def test_repositories_file_keeps_the_registry_fields_the_store_reads():
  registry = claims_script._repositories()
  assert list(registry) == sorted(registry)
  assert registry['uq-f']['prefixes'] == ['UQF', 'F']
  assert all(set(entry) <= set(claims_script._REPOSITORY_FIELDS) for entry in registry.values())


def _own(caplog):
  """``(level, message)`` for each record the script itself logged."""
  name = claims_script.logger.name
  return [(r.levelno, r.getMessage()) for r in caplog.records if r.name == name]


def _run(monkeypatch, caplog, tmp_path, flag, *, error):
  """Run the script over a load that logs a warning, and an error when
  `error`; the messages that come out, in order."""

  def fake_load(drafts=False, tolerate=False, **_):
    log = logging.getLogger('phylohist.loader.load')
    log.warning('a warning')
    if error:
      log.error('an error')
    log.info('a note')
    return {}, {}

  monkeypatch.setattr(claims_script, 'load', fake_load)
  argv = ['--out', str(tmp_path), *flag]
  with caplog.at_level(logging.WARNING):
    claims_script.main(argv)
  return [r.getMessage() for r in caplog.records if r.name == 'phylohist.loader.load']


def test_errors_only_shows_the_errors_when_there_are_any(monkeypatch, caplog, tmp_path):
  assert _run(monkeypatch, caplog, tmp_path, [], error=True) == ['a warning', 'an error']
  caplog.clear()
  assert _run(monkeypatch, caplog, tmp_path, ['--errors-only'], error=True) == ['an error']
  # The final count is the script's own, logged as an error, and stays.
  assert _own(caplog) == [(logging.ERROR, '1 integrity errors while loading (tolerated)')]


def test_a_failed_load_logs_why(monkeypatch, caplog, tmp_path):
  def failing_load(**_):
    raise LoadError('2 integrity errors while loading; see the log')

  monkeypatch.setattr(claims_script, 'load', failing_load)
  assert claims_script.main(['--out', str(tmp_path)]) == 1
  assert _own(caplog) == [(logging.ERROR, '2 integrity errors while loading; see the log')]


def test_errors_only_shows_the_warnings_when_there_are_no_errors(monkeypatch, caplog, tmp_path):
  assert _run(monkeypatch, caplog, tmp_path, ['--errors-only'], error=False) == ['a warning']


def _prune_run(monkeypatch, tmp_path, *flags, error=False):
  """Run the script over a load that logs 'a warning' (and an error when
  `error`), pruning an expected-warnings file that lists 'a warning' and
  'stale'; the exit status and the file's lines afterwards."""

  def fake_load(drafts=False, tolerate=False, **_):
    log = logging.getLogger('phylohist.loader.load')
    log.warning('a warning')
    if error:
      log.error('an error')
    return {}, {}

  monkeypatch.setattr(claims_script, 'load', fake_load)
  expected = tmp_path / 'expected.txt'
  regenerate.write_expected({'a warning', 'stale'}, expected)
  argv = ['--out', str(tmp_path / 'claims'), '--expected', str(expected), *flags]
  return claims_script.main(argv), regenerate.read_expected(expected)


def test_a_run_drops_the_expected_warnings_the_load_no_longer_produces(
  monkeypatch, tmp_path, capsys
):
  status, lines = _prune_run(monkeypatch, tmp_path)
  assert status == 0 and lines == {'a warning'}
  assert '1 stale expected warnings removed from expected.txt' in capsys.readouterr().out


def test_a_load_with_errors_leaves_the_expected_warnings(monkeypatch, tmp_path, caplog):
  status, lines = _prune_run(monkeypatch, tmp_path, '--tolerate', error=True)
  assert status == 1 and lines == {'a warning', 'stale'}
  assert _own(caplog) == [
    (logging.WARNING, 'expected.txt is left as it is: the load logged errors'),
    (logging.ERROR, '1 integrity errors while loading (tolerated)'),
  ]


def test_a_run_elsewhere_leaves_the_committed_expected_warnings(monkeypatch, caplog, tmp_path):
  # Only the full run into claims/ prunes the committed file by default.
  before = regenerate.EXPECTED_WARNINGS.read_text()
  _run(monkeypatch, caplog, tmp_path, [], error=False)
  assert regenerate.EXPECTED_WARNINGS.read_text() == before
