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


def test_report_lists_holotypes_that_differ_without_counting_them(load_records, capsys):
  def tree(source, number):
    return Tree(
      {
        'taxon': 'navicula_whitehouse_1941',
        'material': [{'role': 'holotype', 'catalogNumbers': [number]}],
      },
      {'source_key': source, 'type': 'taxonomy', 'position': 0},
    )

  roots = {
    '2021_jell_sprinkle': [tree('2021_jell_sprinkle', 'UQF 9')],
    '1941_whitehouse': [tree('1941_whitehouse', 'F. 5404')],
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


def test_report_prints_no_holotype_section_when_none_differ(load_records, capsys):
  roots = {
    '1941_whitehouse': [
      Tree(
        {
          'taxon': 'navicula_whitehouse_1941',
          'material': [{'role': 'holotype', 'catalogNumbers': ['F. 5404']}],
        },
        {'source_key': '1941_whitehouse', 'type': 'taxonomy', 'position': 0},
      )
    ]
  }
  _, out = _report(capsys, roots)
  assert 'holotypes that differ' not in out


def test_repositories_file_keeps_the_registry_fields_the_store_reads(load_records):
  registry = claims_script._repositories()
  assert list(registry) == sorted(registry)
  assert registry['uq-f']['prefixes'] == ['UQF', 'F']
  assert all(set(entry) <= set(claims_script._REPOSITORY_FIELDS) for entry in registry.values())
