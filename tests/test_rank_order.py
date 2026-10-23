"""A child of a genus, subgenus or species node in a taxonomy is at a rank
below its parent's, each node at the rank it sits at (`Tree.rank`): the
word it writes, else its record's. So a record must agree with the tree
where its node gives no rank (an open form under a genus is a species,
whatever its record says, and an error otherwise), and a node that writes
a word is checked by that word. A node written `rank: null` stands outside
the order, and above the genus group a source's scheme is its own, so
nothing is checked there.

The records and trees are synthetic, built on each test's copy of the
loaded test corpus (`records`).
"""

import itertools
import logging

import pytest

from phylohist.loader.load import _report_rank_order
from phylohist.loader.taxa import Tree
from tests import support

SOURCE = '1766_linnaeus'
# The named records' authority, so that their nodes need no `new` flag.
EARLIER = {'authority': {'source': '1758_linnaeus'}}
FAMILY = 'testidae'
GENUS = 'testum'
OTHER_GENUS = 'testorum'
SUBGENUS = 'testulum-subgenus'
SPECIES = 'testa_linnaeus_1758'
OPEN = 'testum-sp_linnaeus_1766'
POSITIONS = itertools.count(500)
INFO = ' taxa placed under a genus or species at no lower rank'


@pytest.fixture
def records(records):
  """The test's copy of the corpus, with the named records the trees place."""
  records.add_taxon({'name': 'Testidae', 'rank': 'Family', **EARLIER}, FAMILY)
  records.add_taxon({'name': 'Testum', 'rank': 'genus', **EARLIER}, GENUS)
  records.add_taxon({'name': 'Testorum', 'rank': 'genus', **EARLIER}, OTHER_GENUS)
  records.add_taxon({'name': 'Testulum', 'rank': 'subgenus', **EARLIER}, SUBGENUS)
  records.add_taxon({'name': 'testa', 'rank': 'species', **EARLIER}, SPECIES)
  return records


def _check(records, tree, rank='species', caplog=None, tree_type='taxonomy'):
  """The errors and info lines `_report_rank_order` logs for `tree`, whose
  `OPEN` record has `rank`, and the root's string form for the messages."""
  records.add_taxon({'name': None, 'rank': rank, 'authority': {'source': SOURCE}}, OPEN)
  root = Tree(
    tree, {'source_key': SOURCE, 'type': tree_type, 'position': next(POSITIONS)}, corpus=records
  )
  with caplog.at_level(logging.INFO, logger='phylohist'):
    caplog.clear()
    _report_rank_order(support.with_documents(records, roots={SOURCE: [root]}))
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  info = [r.getMessage() for r in caplog.records if r.levelno == logging.INFO]
  return errors, info, str(root)


def _open_under(parent, **node):
  return {'taxon': parent, 'children': [{'openTaxon': OPEN, 'new': True, **node}]}


def _misplaced(key, rank, parent, above, where, printed=False):
  opening = f'{key}: printed rank' if printed else f'taxa.yaml {key}: rank'
  return f'{opening} "{rank}" but the tree places it under {parent} ({above}) at {where}'


def test_an_open_species_under_a_genus_says_nothing(records, caplog):
  errors, info, _ = _check(records, _open_under(GENUS), caplog=caplog)
  assert errors == []
  assert info == ['0' + INFO]


def test_a_record_ranked_genus_under_a_genus_is_named_with_both_ranks(records, caplog):
  errors, info, root = _check(records, _open_under(GENUS), rank='genus', caplog=caplog)
  assert errors == [_misplaced(OPEN, 'genus', GENUS, 'genus', f'{root}/0/{OPEN}')]
  assert info == ['1' + INFO]


def test_a_subgenus_under_a_genus_is_below_it_and_a_genus_is_not(records, caplog):
  assert _check(records, _open_under(GENUS), rank='subgenus', caplog=caplog)[0] == []
  tree = {'taxon': GENUS, 'children': [_open_under(SUBGENUS)]}
  errors, _, root = _check(records, tree, rank='genus', caplog=caplog)
  assert errors == [
    _misplaced(OPEN, 'genus', SUBGENUS, 'subgenus', f'{root}/0/{SUBGENUS}/0/{OPEN}')
  ]


def test_a_variety_under_a_species_is_below_it_and_a_species_is_not(records, caplog):
  tree = {'taxon': GENUS, 'children': [_open_under(SPECIES)]}
  assert _check(records, tree, rank='variety', caplog=caplog)[0] == []
  errors, _, root = _check(records, tree, rank='species', caplog=caplog)
  assert errors == [_misplaced(OPEN, 'species', SPECIES, 'species', f'{root}/0/{SPECIES}/0/{OPEN}')]


def test_a_named_child_is_checked_too(records, caplog):
  tree = {'taxon': GENUS, 'children': [{'taxon': OTHER_GENUS}]}
  errors, _, root = _check(records, tree, caplog=caplog)
  assert errors == [_misplaced(OTHER_GENUS, 'genus', GENUS, 'genus', f'{root}/0/{OTHER_GENUS}')]


def test_the_parents_printed_rank_word_is_the_rank_it_sits_at(records, caplog):
  tree = {'taxon': GENUS, 'rank': 'Subgenus', 'children': [{'openTaxon': OPEN, 'new': True}]}
  errors, _, root = _check(records, tree, rank='subgenus', caplog=caplog)
  assert errors == [_misplaced(OPEN, 'subgenus', GENUS, 'Subgenus', f'{root}/0/{OPEN}')]


def test_a_node_printing_its_own_rank_word_is_checked_by_that_word(records, caplog):
  # The source's own rank word is the rank the node sits at, whatever its
  # record says, and the error names the word as printed.
  errors, _, root = _check(records, _open_under(GENUS, rank='Genus'), caplog=caplog)
  assert errors == [_misplaced(OPEN, 'Genus', GENUS, 'genus', f'{root}/0/{OPEN}', printed=True)]
  assert _check(records, _open_under(GENUS, rank='species'), rank='genus', caplog=caplog)[0] == []


def test_a_parent_and_child_at_printed_words(records, caplog):
  tree = {
    'taxon': GENUS,
    'rank': 'Subgenus',
    'children': [{'openTaxon': OPEN, 'new': True, 'rank': 'Subgenus'}],
  }
  errors, _, root = _check(records, tree, caplog=caplog)
  assert errors == [
    _misplaced(OPEN, 'Subgenus', GENUS, 'Subgenus', f'{root}/0/{OPEN}', printed=True)
  ]
  tree['children'][0]['rank'] = 'species'
  assert _check(records, tree, rank='genus', caplog=caplog)[0] == []


def test_a_node_sits_at_the_rank_it_writes_else_at_its_records(records):
  tree = {
    'taxon': GENUS,
    'rank': 'Subgenus',
    'children': [
      {'taxon': SPECIES, 'rank': None},
      {'taxon': SUBGENUS},
      {'notes': 'a bin', 'children': []},
    ],
  }
  metadata = {'source_key': SOURCE, 'type': 'taxonomy', 'position': next(POSITIONS)}
  root = Tree(tree, metadata, corpus=records)
  nodes = {node.pointer: node for node in root.walk()}
  assert root.rank == 'Subgenus'
  assert nodes['/children/0'].rank is None
  assert nodes['/children/1'].rank == 'subgenus'
  assert nodes['/children/2'].rank is None


def test_a_null_rank_stands_outside_the_order(records, caplog):
  # `rank: null` says the source places the taxon with no rank, so any
  # rank may sit above or below it, whatever its record says.
  assert _check(records, _open_under(GENUS, rank=None), rank='genus', caplog=caplog)[0] == []
  tree = {'taxon': GENUS, 'rank': None, 'children': [{'openTaxon': OPEN, 'new': True}]}
  assert _check(records, tree, rank='genus', caplog=caplog)[0] == []


def test_above_the_genus_group_nothing_is_said(records, caplog):
  # Macleay 1821 lists classes under an order: a source's scheme above the
  # genus group is its own.
  assert _check(records, _open_under(FAMILY), rank='Family', caplog=caplog)[0] == []
  assert _check(records, _open_under(FAMILY), rank='Order', caplog=caplog)[0] == []


def test_a_member_by_path_only_is_looked_through(records, caplog):
  tree = {
    'taxon': GENUS,
    'children': [{'notes': 'a bin', 'children': [{'openTaxon': OPEN, 'new': True}]}],
  }
  errors, _, root = _check(records, tree, rank='genus', caplog=caplog)
  assert errors == [_misplaced(OPEN, 'genus', GENUS, 'genus', f'{root}/0/0/{OPEN}')]


def test_a_phylogeny_is_not_checked(records, caplog):
  errors, info, _ = _check(
    records, _open_under(GENUS), rank='genus', caplog=caplog, tree_type='cladogram'
  )
  assert errors == []
  assert info == ['0' + INFO]
