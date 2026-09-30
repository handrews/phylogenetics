"""`compact_material` in scripts/migrate_material.py, on plain lists and
dicts (the script's ruamel import is optional for these)."""

import importlib.util
import pathlib

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / 'scripts' / 'migrate_material.py'
_spec = importlib.util.spec_from_file_location('migrate_material', SCRIPT)
migrate_material = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(migrate_material)
compact_material = migrate_material.compact_material


def test_consecutive_entries_with_one_role_merge_in_order():
  material = [
    {'catalogNumbers': ['MCZ 632'], 'role': 'paratype'},
    {'catalogNumbers': ['MCZ 633', 'MCZ 634'], 'role': 'paratype'},
    {'catalogNumbers': ['MCZ 635'], 'role': 'paratype'},
  ]
  assert compact_material(material) == 2
  assert material == [
    {'catalogNumbers': ['MCZ 632', 'MCZ 633', 'MCZ 634', 'MCZ 635'], 'role': 'paratype'},
  ]


def test_no_role_merges_with_no_role_but_not_with_a_role():
  material = [
    {'catalogNumbers': ['A 1']},
    {'catalogNumbers': ['A 2']},
    {'catalogNumbers': ['A 3'], 'role': 'holotype'},
  ]
  assert compact_material(material) == 1
  assert material == [
    {'catalogNumbers': ['A 1', 'A 2']},
    {'catalogNumbers': ['A 3'], 'role': 'holotype'},
  ]


def test_context_must_match_or_both_be_absent():
  material = [
    {'catalogNumbers': ['A 1'], 'context': 'x'},
    {'catalogNumbers': ['A 2'], 'context': 'x'},
    {'catalogNumbers': ['A 3'], 'context': 'y'},
    {'catalogNumbers': ['A 4']},
  ]
  assert compact_material(material) == 1
  assert [m['catalogNumbers'] for m in material] == [['A 1', 'A 2'], ['A 3'], ['A 4']]


def test_an_entry_with_any_other_field_breaks_the_run():
  material = [
    {'catalogNumbers': ['A 1'], 'role': 'paratype'},
    {'catalogNumbers': ['A 2'], 'role': 'paratype', 'notes': 'damaged'},
    {'catalogNumbers': ['A 3'], 'role': 'paratype'},
    {'label': 'the Bigsby specimen', 'role': 'paratype'},
    {'catalogNumbers': ['A 4'], 'role': 'paratype'},
    {'catalogNumbers': ['A 5'], 'role': 'paratype'},
  ]
  assert compact_material(material) == 1
  assert [m.get('catalogNumbers') for m in material] == [
    ['A 1'],
    ['A 2'],
    ['A 3'],
    None,
    ['A 4', 'A 5'],
  ]


def test_range_pairs_are_carried_over_as_elements():
  material = [
    {'catalogNumbers': [['MCZ 632', 'MCZ 641']], 'role': 'paratype'},
    {'catalogNumbers': ['MCZ 650'], 'role': 'paratype'},
  ]
  assert compact_material(material) == 1
  assert material == [
    {'catalogNumbers': [['MCZ 632', 'MCZ 641'], 'MCZ 650'], 'role': 'paratype'},
  ]


def test_nothing_to_merge_returns_zero():
  material = [{'catalogNumbers': ['A 1'], 'role': 'holotype'}]
  assert compact_material(material) == 0
  assert compact_material([]) == 0
