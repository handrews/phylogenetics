"""A taxa record that gives its protologue page agrees with the node marked
`new` for it, on the fields the node declares (`rank`, `pages`,
`illustrations`, `citedAs`), and gives nothing its tree file lists as
unused; `citedAs` validates on a record.

The records and trees are synthetic, built on the session's loaded corpus
(`Taxon` and `Tree` keep class-level registries, so each test gets
its own copies, restored afterwards).
"""

import collections
import itertools
import logging

import pytest

from phylohist.loader import io
from phylohist.loader.load import _report_protologue_mismatches
from phylohist.loader.taxa import Taxon, Tree

pytestmark = pytest.mark.usefixtures('load_records')

SOURCE = '1758_linnaeus'
FILE = 'data/trees/1758_linnaeus.yaml'
KEY = 'testum_linnaeus_1758'
FIGURE = {'figure': 1}
POSITIONS = itertools.count(400)


@pytest.fixture(autouse=True)
def registries(monkeypatch):
  """Private copies of the class-level registries a `Tree` writes to."""
  for name in ('_taxon_index', '_new_index', '_author_index'):
    monkeypatch.setattr(Tree, name, collections.defaultdict(set))
  monkeypatch.setattr(Tree, '_type_index', {k: set() for k in Tree._type_index})
  monkeypatch.setattr(Taxon, '_taxa', dict(Taxon._taxa))


def _check(record=None, node=None, unused=(), caplog=None):
  """The messages `_report_protologue_mismatches` logs for a record with
  `record` fields on top of its pages, and a protologue node with `node`."""
  data = {'name': 'testum', 'rank': 'species', 'pages': 22, 'authority': {'source': SOURCE}}
  Taxon.add({**data, **(record or {})}, KEY)
  tree = Tree(
    {'taxon': KEY, 'new': True, **(node or {})},
    {
      'source_key': SOURCE,
      'type': 'taxonomy',
      'position': next(POSITIONS),
      'file_unused': tuple(unused),
    },
  )
  with caplog.at_level(logging.INFO, logger='phylohist'):
    caplog.clear()
    _report_protologue_mismatches({'trees': {SOURCE: {}}}, {SOURCE: [tree]})
  return [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR], [
    r.getMessage() for r in caplog.records if r.levelno == logging.INFO
  ]


def test_agreeing_fields_say_nothing(caplog):
  record = {'rank': 'variety', 'citedAs': 'Afer δ', 'illustrations': [FIGURE]}
  node = {'rank': 'variety', 'pages': 22, 'illustrations': [FIGURE], 'citedAs': 'Afer δ'}
  errors, info = _check(record, node, caplog=caplog)
  assert errors == []
  assert info == ['0 disagreements between a taxa record and its protologue node']


def test_a_differing_cited_as_is_named_with_both_values_and_the_file(caplog):
  errors, info = _check({'citedAs': 'Afer'}, {'citedAs': 'Afer δ'}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: citedAs "Afer" but its protologue node in {FILE} prints "Afer δ"'
  ]
  assert info == ['1 disagreements between a taxa record and its protologue node']


def test_a_record_cited_as_against_a_node_printing_none(caplog):
  errors, _ = _check({'citedAs': 'Afer δ'}, {'citedAs': None}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: citedAs "Afer δ" but its protologue node in {FILE} prints none'
  ]


def test_a_node_citing_a_record_without_cited_as(caplog):
  errors, _ = _check(None, {'citedAs': 'Afer δ'}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: citedAs none but its protologue node in {FILE} prints "Afer δ"'
  ]


def test_a_differing_rank(caplog):
  errors, _ = _check({'rank': 'variety'}, {'rank': 'species'}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: rank "variety" but its protologue node in {FILE} has "species"'
  ]


def test_a_differing_page(caplog):
  errors, _ = _check({'pages': 21}, {'pages': 22}, caplog=caplog)
  assert errors == [f'taxa.yaml {KEY}: pages 21 but its protologue node in {FILE} has 22']


def test_differing_illustrations(caplog):
  errors, _ = _check({'illustrations': [FIGURE]}, {'illustrations': [{'figure': 2}]}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: illustrations [{{"figure": 1}}] but its protologue node in {FILE} '
    'has [{"figure": 2}]'
  ]


def test_null_illustrations_on_the_node_equal_none_on_the_record(caplog):
  assert _check(None, {'illustrations': None}, caplog=caplog)[0] == []
  errors, _ = _check({'illustrations': [FIGURE]}, {'illustrations': None}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: illustrations [{{"figure": 1}}] but its protologue node in {FILE} has none'
  ]


def test_an_unranked_node_equals_an_unranked_record(caplog):
  assert _check({'rank': 'Unranked'}, {'rank': None}, caplog=caplog)[0] == []
  assert _check({'rank': None}, {'rank': None}, caplog=caplog)[0] == []
  assert Taxon.get(KEY).rank == 'Unranked'
  errors, _ = _check({'rank': 'variety'}, {'rank': None}, caplog=caplog)
  assert errors == [f'taxa.yaml {KEY}: rank "variety" but its protologue node in {FILE} has none']


@pytest.mark.parametrize(
  'record, node',
  [
    (22, '22'),
    ('22', 22),
    ([22, 23], [22, '23']),
    ([[22, 23]], [['22', 23]]),
    (22, [22]),
  ],
)
def test_pages_agree_across_forms(caplog, record, node):
  assert _check({'pages': record}, {'pages': node}, caplog=caplog)[0] == []


@pytest.mark.parametrize(
  'record, node', [([22, 23], [22, 24]), (22, [22, 23]), ([[22, 23]], [22, 23])]
)
def test_pages_that_differ_in_a_list_are_a_mismatch(caplog, record, node):
  errors, _ = _check({'pages': record}, {'pages': node}, caplog=caplog)
  assert len(errors) == 1 and errors[0].startswith(f'taxa.yaml {KEY}: pages ')


def test_a_node_with_null_pages_never_equals_the_records(caplog):
  errors, _ = _check(
    None, {'pages': None, 'editorial': {'inferred': True, 'basis': 'x'}}, caplog=caplog
  )
  assert errors == [f'taxa.yaml {KEY}: pages 22 but its protologue node in {FILE} has none']


def test_each_differing_field_has_its_own_message(caplog):
  errors, info = _check(
    {'rank': 'variety', 'citedAs': 'Afer'},
    {'rank': 'species', 'pages': 23, 'citedAs': 'Afer δ'},
    caplog=caplog,
  )
  assert [e.split(': ')[1].split(' ')[0] for e in errors] == ['rank', 'pages', 'citedAs']
  assert info == ['3 disagreements between a taxa record and its protologue node']


def test_a_record_without_pages_is_not_checked(caplog):
  Taxon.add({'name': 'testum', 'rank': 'variety', 'authority': {'source': SOURCE}}, KEY)
  tree = Tree(
    {'taxon': KEY, 'new': True, 'rank': 'species', 'citedAs': 'Afer δ'},
    {'source_key': SOURCE, 'type': 'taxonomy', 'position': next(POSITIONS)},
  )
  with caplog.at_level(logging.INFO, logger='phylohist'):
    caplog.clear()
    _report_protologue_mismatches({'trees': {SOURCE: {}}}, {SOURCE: [tree]})
  assert [r.levelno for r in caplog.records] == [logging.INFO]


def test_a_node_declaring_none_of_the_fields_says_nothing(caplog):
  errors, _ = _check(
    {'citedAs': 'Afer δ', 'illustrations': [FIGURE], 'rank': 'species'}, caplog=caplog
  )
  assert errors == []


def test_a_node_not_marked_new_is_not_the_protologue(caplog):
  errors, _ = _check(None, {'new': False, 'pages': 99}, caplog=caplog)
  assert errors == []


def test_a_cited_use_of_the_record_is_not_the_protologue(caplog):
  Taxon.add(
    {'name': 'testum', 'rank': 'species', 'pages': 22, 'authority': {'source': SOURCE}}, KEY
  )
  tree = Tree(
    {
      'taxon': 'vermes',
      'children': [
        {
          'taxon': KEY,
          'new': True,
          'pages': 22,
          'synonyms': [{'taxon': KEY, 'new': True, 'pages': 99}],
        }
      ],
    },
    {'source_key': SOURCE, 'type': 'taxonomy', 'position': next(POSITIONS)},
  )
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    caplog.clear()
    _report_protologue_mismatches({'trees': {SOURCE: {}}}, {SOURCE: [tree]})
  assert [r.getMessage() for r in caplog.records] == []


def test_a_record_cannot_give_a_field_its_file_lists_as_unused(caplog):
  errors, info = _check(
    {'illustrations': [FIGURE]}, {'pages': 22}, unused=['illustrations'], caplog=caplog
  )
  assert errors == [f'taxa.yaml {KEY}: illustrations given but {FILE} lists it as unused']
  assert info == ['1 disagreements between a taxa record and its protologue node']


def test_an_unused_field_the_record_does_not_give_is_clean(caplog):
  assert _check(None, unused=['illustrations'], caplog=caplog)[0] == []


def test_a_source_without_a_tree_is_not_checked(caplog):
  Taxon.add(
    {'name': 'testum', 'rank': 'variety', 'pages': 22, 'authority': {'source': SOURCE}}, KEY
  )
  with caplog.at_level(logging.INFO, logger='phylohist'):
    caplog.clear()
    _report_protologue_mismatches({'trees': {}}, {})
  assert [r.levelno for r in caplog.records] == [logging.INFO]


def test_schema_accepts_cited_as_on_a_record_and_a_node():
  schema = io.build_schema()
  record = {'name': 'afer', 'rank': 'variety', 'pages': 22, 'authority': {'source': SOURCE}}
  assert schema['taxa'].check({'afer_linnaeus_1758': {**record, 'citedAs': 'Afer δ'}})
  assert not schema['taxa'].check({'afer_linnaeus_1758': {**record, 'citedAs': 1}})
  assert not schema['taxa'].check({'afer_linnaeus_1758': {**record, 'printedAs': 'Afer δ'}})
  assert schema[io.TREE_DEF].check({'taxonomies': [{'taxon': 'vermes', 'citedAs': 'Vermes'}]})


def test_a_node_without_a_rank_implies_a_species_or_a_genus(caplog):
  # The record spells the rank the node leaves implicit; they must agree.
  assert _check({'rank': 'species'}, caplog=caplog)[0] == []
  errors, _ = _check({'rank': 'variety'}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: rank "variety" but its protologue node in {FILE} implies "species"'
  ]
  errors, _ = _check({'name': 'Testum', 'rank': 'Order'}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: rank "Order" but its protologue node in {FILE} implies "genus"'
  ]
  assert _check({'name': 'Testum', 'rank': 'genus'}, caplog=caplog)[0] == []
  errors, _ = _check({'rank': None}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: rank none but its protologue node in {FILE} implies "species"'
  ]


def test_a_record_with_pages_spells_its_rank():
  schema = io.build_schema()
  record = {'name': 'afer', 'pages': 22, 'authority': {'source': SOURCE}}
  assert not schema['taxa'].check({'afer_linnaeus_1758': record})
  assert schema['taxa'].check({'afer_linnaeus_1758': {**record, 'rank': 'variety'}})
  assert schema['taxa'].check({'afer_linnaeus_1758': {**record, 'rank': None}})
  assert schema['taxa'].check(
    {'afer_linnaeus_1758': {'name': 'afer', 'authority': {'source': SOURCE}}}
  )
