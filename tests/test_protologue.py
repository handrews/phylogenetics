"""A taxa record that gives its protologue page agrees with the node marked
`new` for it, on the fields the node declares (`rank`, `pages`,
`illustrations`, `citedAs`, `designation`), and gives nothing its tree file lists as
unused; `citedAs` validates on a record; and a record whose protologue source has a tree that uses
it is flagged `new` there.

The records and trees are synthetic, built on each test's copy of the
loaded test corpus (`records`).
"""

import itertools
import logging

import pytest

from phylohist.loader import io
from phylohist.loader.load import _report_missing_protologues, _report_protologue_mismatches
from phylohist.loader.taxa import Tree
from tests import support

SOURCE = '1758_linnaeus'
FILE = 'data/trees/1758_linnaeus.yaml'
KEY = 'testum_linnaeus_1758'
FIGURE = {'figure': 1}
POSITIONS = itertools.count(400)


def _record(record=None, **base):
  """A record with `pages: 22` in its `authority` block and `record` fields
  on top; a record-side `pages` or `illustrations` goes into the block."""
  record = dict(record or {})
  authority = {'source': SOURCE, 'pages': 22}
  for field in ('pages', 'illustrations'):
    if field in record:
      authority[field] = record.pop(field)
  return {**base, 'authority': authority, **record}


def _check(records, record=None, node=None, unused=(), caplog=None):
  """The messages `_report_protologue_mismatches` logs for a record with
  `record` fields on top of its pages, and a protologue node with `node`."""
  records.add_taxon(_record(record, name='testum', rank='species'), KEY)
  tree = Tree(
    {'taxon': KEY, 'new': True, **(node or {})},
    {
      'source_key': SOURCE,
      'type': 'taxonomy',
      'position': next(POSITIONS),
      'file_unused': tuple(unused),
    },
    corpus=records,
  )
  with caplog.at_level(logging.INFO, logger='phylohist'):
    caplog.clear()
    _report_protologue_mismatches(
      support.with_documents(records, {'trees': {SOURCE: {}}}, {SOURCE: [tree]})
    )
  return [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR], [
    r.getMessage() for r in caplog.records if r.levelno == logging.INFO
  ]


def test_agreeing_fields_say_nothing(records, caplog):
  record = {'rank': 'variety', 'citedAs': 'Afer δ', 'illustrations': [FIGURE]}
  node = {'rank': 'variety', 'pages': 22, 'illustrations': [FIGURE], 'citedAs': 'Afer δ'}
  errors, info = _check(records, record, node, caplog=caplog)
  assert errors == []
  assert info == ['0 disagreements between a taxa record and its protologue node']


def test_a_differing_cited_as_is_named_with_both_values_and_the_file(records, caplog):
  errors, info = _check(records, {'citedAs': 'Afer'}, {'citedAs': 'Afer δ'}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: citedAs "Afer" but its protologue node in {FILE} prints "Afer δ"'
  ]
  assert info == ['1 disagreements between a taxa record and its protologue node']


def test_a_record_cited_as_against_a_node_printing_none(records, caplog):
  errors, _ = _check(records, {'citedAs': 'Afer δ'}, {'citedAs': None}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: citedAs "Afer δ" but its protologue node in {FILE} prints none'
  ]


def test_a_node_citing_a_record_without_cited_as(records, caplog):
  errors, _ = _check(records, None, {'citedAs': 'Afer δ'}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: citedAs none but its protologue node in {FILE} prints "Afer δ"'
  ]


def test_a_differing_rank(records, caplog):
  errors, _ = _check(records, {'rank': 'variety'}, {'rank': 'species'}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: rank "variety" but its protologue node in {FILE} has "species"'
  ]


def test_a_differing_page(records, caplog):
  errors, _ = _check(records, {'pages': 21}, {'pages': 22}, caplog=caplog)
  assert errors == [f'taxa.yaml {KEY}: pages 21 but its protologue node in {FILE} has 22']


def test_differing_illustrations(records, caplog):
  errors, _ = _check(
    records, {'illustrations': [FIGURE]}, {'illustrations': [{'figure': 2}]}, caplog=caplog
  )
  assert errors == [
    f'taxa.yaml {KEY}: illustrations [{{"figure": 1}}] but its protologue node in {FILE} '
    'has [{"figure": 2}]'
  ]


def test_null_illustrations_on_the_node_equal_none_on_the_record(records, caplog):
  assert _check(records, None, {'illustrations': None}, caplog=caplog)[0] == []
  errors, _ = _check(records, {'illustrations': [FIGURE]}, {'illustrations': None}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: illustrations [{{"figure": 1}}] but its protologue node in {FILE} has none'
  ]


def test_an_unranked_node_equals_an_unranked_record(records, caplog):
  assert _check(records, {'rank': 'Unranked'}, {'rank': None}, caplog=caplog)[0] == []
  assert _check(records, {'rank': None}, {'rank': None}, caplog=caplog)[0] == []
  assert records.taxa[KEY].rank == 'Unranked'
  errors, _ = _check(records, {'rank': 'variety'}, {'rank': None}, caplog=caplog)
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
def test_pages_agree_across_forms(records, caplog, record, node):
  assert _check(records, {'pages': record}, {'pages': node}, caplog=caplog)[0] == []


@pytest.mark.parametrize(
  'record, node', [([22, 23], [22, 24]), (22, [22, 23]), ([[22, 23]], [22, 23])]
)
def test_pages_that_differ_in_a_list_are_a_mismatch(records, caplog, record, node):
  errors, _ = _check(records, {'pages': record}, {'pages': node}, caplog=caplog)
  assert len(errors) == 1 and errors[0].startswith(f'taxa.yaml {KEY}: pages ')


def test_a_node_with_null_pages_never_equals_the_records(records, caplog):
  errors, _ = _check(
    records, None, {'pages': None, 'editorial': {'inferred': True, 'basis': 'x'}}, caplog=caplog
  )
  assert errors == [f'taxa.yaml {KEY}: pages 22 but its protologue node in {FILE} has none']


def test_each_differing_field_has_its_own_message(records, caplog):
  errors, info = _check(
    records,
    {'rank': 'variety', 'citedAs': 'Afer'},
    {'rank': 'species', 'pages': 23, 'citedAs': 'Afer δ'},
    caplog=caplog,
  )
  assert [e.split(': ')[1].split(' ')[0] for e in errors] == ['rank', 'pages', 'citedAs']
  assert info == ['3 disagreements between a taxa record and its protologue node']


def test_a_record_without_pages_is_not_checked(records, caplog):
  records.add_taxon({'name': 'testum', 'rank': 'variety', 'authority': {'source': SOURCE}}, KEY)
  tree = Tree(
    {'taxon': KEY, 'new': True, 'rank': 'species', 'citedAs': 'Afer δ'},
    {'source_key': SOURCE, 'type': 'taxonomy', 'position': next(POSITIONS)},
    corpus=records,
  )
  with caplog.at_level(logging.INFO, logger='phylohist'):
    caplog.clear()
    _report_protologue_mismatches(
      support.with_documents(records, {'trees': {SOURCE: {}}}, {SOURCE: [tree]})
    )
  assert [r.levelno for r in caplog.records] == [logging.INFO]


def test_a_node_declaring_none_of_the_fields_says_nothing(records, caplog):
  errors, _ = _check(
    records, {'citedAs': 'Afer δ', 'illustrations': [FIGURE], 'rank': 'species'}, caplog=caplog
  )
  assert errors == []


def test_a_node_not_marked_new_is_not_the_protologue(records, caplog):
  errors, _ = _check(records, None, {'new': False, 'pages': 99}, caplog=caplog)
  assert errors == []


def test_a_cited_use_of_the_record_is_not_the_protologue(records, caplog):
  records.add_taxon(_record(name='testum', rank='species'), KEY)
  tree = Tree(
    {
      'taxon': 'vermes',
      'children': [
        {
          'taxon': KEY,
          'new': True,
          'pages': 22,
          'synonyms': [{'taxon': KEY, 'new': True, 'authority': {'pages': 99}}],
        }
      ],
    },
    {'source_key': SOURCE, 'type': 'taxonomy', 'position': next(POSITIONS)},
    corpus=records,
  )
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    caplog.clear()
    _report_protologue_mismatches(
      support.with_documents(records, {'trees': {SOURCE: {}}}, {SOURCE: [tree]})
    )
  assert [r.getMessage() for r in caplog.records] == []


def test_a_record_cannot_give_a_field_its_file_lists_as_unused(records, caplog):
  errors, info = _check(
    records, {'illustrations': [FIGURE]}, {'pages': 22}, unused=['illustrations'], caplog=caplog
  )
  assert errors == [f'taxa.yaml {KEY}: illustrations given but {FILE} lists it as unused']
  assert info == ['1 disagreements between a taxa record and its protologue node']


def test_an_unused_field_the_record_does_not_give_is_clean(records, caplog):
  assert _check(records, None, unused=['illustrations'], caplog=caplog)[0] == []


def test_a_source_without_a_tree_is_not_checked(records, caplog):
  records.add_taxon(_record(name='testum', rank='variety'), KEY)
  with caplog.at_level(logging.INFO, logger='phylohist'):
    caplog.clear()
    _report_protologue_mismatches(support.with_documents(records, {'trees': {}}))
  assert [r.levelno for r in caplog.records] == [logging.INFO]


def test_schema_accepts_cited_as_on_a_record_and_a_node():
  schema = support.schema()
  record = _record(name='afer', rank='variety')
  assert schema['taxa'].check({'afer_linnaeus_1758': {**record, 'citedAs': 'Afer δ'}})
  assert not schema['taxa'].check({'afer_linnaeus_1758': {**record, 'citedAs': 1}})
  assert not schema['taxa'].check({'afer_linnaeus_1758': {**record, 'printedAs': 'Afer δ'}})
  assert schema[io.TREE_DEF].check({'taxonomies': [{'taxon': 'vermes', 'citedAs': 'Vermes'}]})


def test_a_node_without_a_rank_implies_a_species_or_a_genus(records, caplog):
  # The record spells the rank the node leaves implicit; they must agree.
  assert _check(records, {'rank': 'species'}, caplog=caplog)[0] == []
  errors, _ = _check(records, {'rank': 'variety'}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: rank "variety" but its protologue node in {FILE} implies "species"'
  ]
  errors, _ = _check(records, {'name': 'Testum', 'rank': 'Order'}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: rank "Order" but its protologue node in {FILE} implies "genus"'
  ]
  assert _check(records, {'name': 'Testum', 'rank': 'genus'}, caplog=caplog)[0] == []
  errors, _ = _check(records, {'rank': None}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {KEY}: rank none but its protologue node in {FILE} implies "species"'
  ]


def test_a_record_with_pages_spells_its_rank():
  # The page sits in the `authority` block; the rank the record spells.
  schema = support.schema()
  record = _record(name='afer')
  assert not schema['taxa'].check({'afer_linnaeus_1758': record})
  assert schema['taxa'].check({'afer_linnaeus_1758': {**record, 'rank': 'variety'}})
  assert schema['taxa'].check({'afer_linnaeus_1758': {**record, 'rank': None}})
  assert schema['taxa'].check(
    {'afer_linnaeus_1758': {'name': 'afer', 'authority': {'source': SOURCE}}}
  )


# -- `designation` --------------------------------------------------------------

OPEN_KEY = 'testum-genus-a_linnaeus_1758'


def _check_open(records, record=None, node=None, caplog=None):
  """As `_check`, for an open taxon: a record with a `designation` and a
  protologue `openTaxon` node."""
  records.add_taxon(_record(record, name=None, designation='Genus A', rank='genus'), OPEN_KEY)
  tree = Tree(
    {'openTaxon': OPEN_KEY, 'new': True, **(node or {})},
    {'source_key': SOURCE, 'type': 'taxonomy', 'position': next(POSITIONS)},
    corpus=records,
  )
  with caplog.at_level(logging.INFO, logger='phylohist'):
    caplog.clear()
    _report_protologue_mismatches(
      support.with_documents(records, {'trees': {SOURCE: {}}}, {SOURCE: [tree]})
    )
  return [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]


def test_a_matching_designation_says_nothing(records, caplog):
  assert _check_open(records, None, {'designation': 'Genus A'}, caplog=caplog) == []


def test_a_differing_designation_is_named_with_both_values_and_the_file(records, caplog):
  errors = _check_open(records, None, {'designation': 'Genus B'}, caplog=caplog)
  assert errors == [
    f'taxa.yaml {OPEN_KEY}: designation "Genus A" but its protologue node in {FILE} '
    'prints "Genus B"'
  ]


def test_a_node_declaring_no_designation_says_nothing(records, caplog):
  assert _check_open(records, None, None, caplog=caplog) == []


def test_an_unnamed_record_implies_no_rank_by_its_name(records, caplog):
  # An open form has no name to read a genus or species from; its record
  # spells its rank, which `_report_rank_order` checks against the parent.
  assert _check_open(records, {'rank': 'species'}, caplog=caplog) == []
  assert _check_open(records, {'rank': 'genus'}, caplog=caplog) == []


# -- the protologue flagged `new` ------------------------------------------------


def _flagged(records, *roots, caplog):
  """The errors and info `_report_missing_protologues` logs for a record
  whose authority is `SOURCE`, over one tree per root given: `(tree type,
  fields of the root node)`, the root being the record itself."""
  records.add_taxon({'name': 'testum', 'rank': 'species', 'authority': {'source': SOURCE}}, KEY)
  trees = [
    Tree(
      {'taxon': KEY, **fields},
      {'source_key': SOURCE, 'type': tree_type, 'position': next(POSITIONS)},
      corpus=records,
    )
    for tree_type, fields in roots
  ]
  with caplog.at_level(logging.INFO, logger='phylohist'):
    caplog.clear()
    _report_missing_protologues(
      support.with_documents(records, {'trees': {SOURCE: {}}}, {SOURCE: trees})
    )
  return [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR], [
    r.getMessage() for r in caplog.records if r.levelno == logging.INFO
  ]


def test_a_tree_using_its_own_record_without_new_is_named(records, caplog):
  errors, info = _flagged(records, ('cladogram', {}), caplog=caplog)
  assert errors == [f'Protologue not flagged: {KEY} in {SOURCE}']
  assert info == ['1 taxa with an unflagged protologue']


def test_a_tree_flagging_its_own_record_new_says_nothing(records, caplog):
  errors, info = _flagged(records, ('cladogram', {'new': True}), caplog=caplog)
  assert errors == []
  assert info == ['0 taxa with an unflagged protologue']


def test_a_record_flagged_new_in_one_tree_is_flagged_for_the_source(records, caplog):
  # A cladogram beside the taxonomy that names the record uses it again.
  roots = (('taxonomy', {'new': True}), ('cladogram', {}))
  assert _flagged(records, *roots, caplog=caplog)[0] == []


def test_a_tree_that_does_not_use_the_record_says_nothing(records, caplog):
  # The part of the source we have not recorded is not an error.
  records.add_taxon(
    {'name': 'testorum', 'rank': 'species', 'authority': {'source': SOURCE}}, 'other'
  )
  errors, info = _flagged(records, ('taxonomy', {'new': True}), caplog=caplog)
  assert errors == []
  assert info == ['0 taxa with an unflagged protologue']
