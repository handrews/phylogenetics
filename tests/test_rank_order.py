"""A child of a genus, subgenus or species node in a taxonomy is at a rank
below its parent's. A node printing no rank word sits where its record's
rank says, so the record must agree with the tree: an open form under a
genus is a species, whatever its record says, and an error otherwise.
Above the genus group a source's scheme is its own (roadmap G8), and
nothing is checked.

The records and trees are synthetic, built on the loaded test corpus
(`Taxon` and `Tree` keep class-level registries, so each test gets its
own copies, restored afterwards).
"""

import collections
import itertools
import logging

import pytest

from phylohist.loader.load import _report_rank_order
from phylohist.loader.taxa import Taxon, Tree

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


@pytest.fixture(autouse=True)
def registries(monkeypatch):
  """Private copies of the class-level registries a `Tree` writes to, with
  the named records the trees place."""
  for name in ('_taxon_index', '_new_index', '_author_index'):
    monkeypatch.setattr(Tree, name, collections.defaultdict(set))
  monkeypatch.setattr(Tree, '_type_index', {k: set() for k in Tree._type_index})
  monkeypatch.setattr(Taxon, '_taxa', dict(Taxon._taxa))
  Taxon.add({'name': 'Testidae', 'rank': 'Family', **EARLIER}, FAMILY)
  Taxon.add({'name': 'Testum', 'rank': 'genus', **EARLIER}, GENUS)
  Taxon.add({'name': 'Testorum', 'rank': 'genus', **EARLIER}, OTHER_GENUS)
  Taxon.add({'name': 'Testulum', 'rank': 'subgenus', **EARLIER}, SUBGENUS)
  Taxon.add({'name': 'testa', 'rank': 'species', **EARLIER}, SPECIES)


def _check(tree, rank='species', caplog=None, tree_type='taxonomy'):
  """The errors and info lines `_report_rank_order` logs for `tree`, whose
  `OPEN` record has `rank`, and the root's string form for the messages."""
  Taxon.add({'name': None, 'rank': rank, 'authority': {'source': SOURCE}}, OPEN)
  root = Tree(tree, {'source_key': SOURCE, 'type': tree_type, 'position': next(POSITIONS)})
  with caplog.at_level(logging.INFO, logger='phylohist'):
    caplog.clear()
    _report_rank_order({SOURCE: [root]})
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  info = [r.getMessage() for r in caplog.records if r.levelno == logging.INFO]
  return errors, info, str(root)


def _open_under(parent, **node):
  return {'taxon': parent, 'children': [{'openTaxon': OPEN, 'new': True, **node}]}


def _misplaced(key, rank, parent, above, where):
  return (
    f'taxa.yaml {key}: rank "{rank}" but the tree places it under {parent} ({above}) at {where}'
  )


def test_an_open_species_under_a_genus_says_nothing(caplog):
  errors, info, _ = _check(_open_under(GENUS), caplog=caplog)
  assert errors == []
  assert info == ['0' + INFO]


def test_a_record_ranked_genus_under_a_genus_is_named_with_both_ranks(caplog):
  errors, info, root = _check(_open_under(GENUS), rank='genus', caplog=caplog)
  assert errors == [_misplaced(OPEN, 'genus', GENUS, 'genus', f'{root}/0/{OPEN}')]
  assert info == ['1' + INFO]


def test_a_subgenus_under_a_genus_is_below_it_and_a_genus_is_not(caplog):
  assert _check(_open_under(GENUS), rank='subgenus', caplog=caplog)[0] == []
  tree = {'taxon': GENUS, 'children': [_open_under(SUBGENUS)]}
  errors, _, root = _check(tree, rank='genus', caplog=caplog)
  assert errors == [
    _misplaced(OPEN, 'genus', SUBGENUS, 'subgenus', f'{root}/0/{SUBGENUS}/0/{OPEN}')
  ]


def test_a_variety_under_a_species_is_below_it_and_a_species_is_not(caplog):
  tree = {'taxon': GENUS, 'children': [_open_under(SPECIES)]}
  assert _check(tree, rank='variety', caplog=caplog)[0] == []
  errors, _, root = _check(tree, rank='species', caplog=caplog)
  assert errors == [_misplaced(OPEN, 'species', SPECIES, 'species', f'{root}/0/{SPECIES}/0/{OPEN}')]


def test_a_named_child_is_checked_too(caplog):
  tree = {'taxon': GENUS, 'children': [{'taxon': OTHER_GENUS}]}
  errors, _, root = _check(tree, caplog=caplog)
  assert errors == [_misplaced(OTHER_GENUS, 'genus', GENUS, 'genus', f'{root}/0/{OTHER_GENUS}')]


def test_the_parents_printed_rank_word_is_the_rank_it_sits_at(caplog):
  tree = {'taxon': GENUS, 'rank': 'Subgenus', 'children': [{'openTaxon': OPEN, 'new': True}]}
  errors, _, root = _check(tree, rank='subgenus', caplog=caplog)
  assert errors == [_misplaced(OPEN, 'subgenus', GENUS, 'Subgenus', f'{root}/0/{OPEN}')]


def test_a_node_printing_its_own_rank_word_is_left_to_the_protologue_check(caplog):
  # The source's own rank word is compared with the record where the node
  # is the protologue; this check reads only a node that prints none, a
  # `rank: null` node among them.
  assert _check(_open_under(GENUS, rank='Genus'), rank='genus', caplog=caplog)[0] == []
  errors, _, root = _check(_open_under(GENUS, rank=None), rank='genus', caplog=caplog)
  assert errors == [_misplaced(OPEN, 'genus', GENUS, 'genus', f'{root}/0/{OPEN}')]


def test_above_the_genus_group_nothing_is_said(caplog):
  # Macleay 1821 lists classes under an order: a source's scheme above the
  # genus group is its own (roadmap G8).
  assert _check(_open_under(FAMILY), rank='Family', caplog=caplog)[0] == []
  assert _check(_open_under(FAMILY), rank='Order', caplog=caplog)[0] == []


def test_a_member_by_path_only_is_looked_through(caplog):
  tree = {
    'taxon': GENUS,
    'children': [{'notes': 'a bin', 'children': [{'openTaxon': OPEN, 'new': True}]}],
  }
  errors, _, root = _check(tree, rank='genus', caplog=caplog)
  assert errors == [_misplaced(OPEN, 'genus', GENUS, 'genus', f'{root}/0/0/{OPEN}')]


def test_a_phylogeny_is_not_checked(caplog):
  errors, info, _ = _check(_open_under(GENUS), rank='genus', caplog=caplog, tree_type='cladogram')
  assert errors == []
  assert info == ['0' + INFO]
