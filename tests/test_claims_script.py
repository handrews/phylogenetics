"""`report_inconsistencies` in scripts/claims.py: the explanation it prints
for each kind of manifest inconsistency row, on a synthetic tree."""

import importlib.util
import pathlib

from phylohist.claims import extract
from phylohist.loader.research import Source
from phylohist.loader.taxa import Tree

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / 'scripts' / 'claims.py'
_spec = importlib.util.spec_from_file_location('claims_script', SCRIPT)
claims_script = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(claims_script)

_WHERE = 'in data/sources.yaml (1961_dehm.audit.coverage.{})'


def _report(capsys, roots):
  found = claims_script.report_inconsistencies(extract(roots), roots)
  return found, capsys.readouterr().out


def test_report_explains_both_row_forms(load_records, monkeypatch, capsys):
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
