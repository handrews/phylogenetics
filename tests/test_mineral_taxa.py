"""Mineral taxa: a record with `mineral: true` is a mineral formation's name
under which a fossil was once described; it has no rank (`rank: null`), and
a tree names it only through `mineralTaxon`, which names nothing else. The
schema, the loader, the draft checker, the claims, the names index and the
resolver.

Synthetic records and trees are built on the loaded test corpus (`Taxon`
and `Tree` keep class-level registries, so each test gets its own copies,
restored afterwards); the store tests read a copy of the corpus's claim
table with one source's claims replaced.
"""

import collections
import itertools
import json
import logging
import shutil

import pytest

from phylohist import cli
from phylohist.claims import extract, names_index
from phylohist.loader import io, nomenclature
from phylohist.loader.load import (
  _report_nomenclature,
  _report_protologue_mismatches,
  _report_rank_order,
)
from phylohist.loader.taxa import Taxon, Tree
from phylohist.store import ClaimStore
from tests import support

SOURCE = '1766_linnaeus'
# The records' authority, another corpus source, so that their nodes need
# no `new` flag.
EARLIER = {'authority': {'source': '1758_linnaeus'}}
MINERAL = 'mineralum_linnaeus_1758'
SPELLING = 'mineralun_linnaeus_1758'
GENUS = 'testum'
SPECIES = 'testa_linnaeus_1758'
UNRANKED = 'testaceum'
MINERAL_RECORD = {'name': 'mineralum', 'rank': None, 'mineral': True, **EARLIER}
GENUS_RECORD = {'name': 'Testum', 'rank': 'genus', **EARLIER}
RECORDS = {
  MINERAL: MINERAL_RECORD,
  SPELLING: {'name': 'mineralun', 'altSpellingOf': MINERAL},
  GENUS: GENUS_RECORD,
  SPECIES: {'name': 'testa', 'rank': 'species', **EARLIER},
  UNRANKED: {'name': 'Testaceum', 'rank': None, **EARLIER},
}
LOOKUP = nomenclature.record_lookup(RECORDS)
POSITIONS = itertools.count(600)
NOT_MINERAL = '`mineralTaxon` "{}" is not a mineral record (`mineral: true`)'
ONLY_MINERAL_TAXON = '`{}` "{}" is a mineral record, which only `mineralTaxon` names'


@pytest.fixture(autouse=True)
def registries(monkeypatch):
  """Private copies of the class-level registries a `Tree` writes to, with
  the synthetic records loaded."""
  monkeypatch.setattr(Tree, '_new_index', collections.defaultdict(set))
  monkeypatch.setattr(Tree, '_type_index', {k: set() for k in Tree._type_index})
  monkeypatch.setattr(Taxon, '_taxa', dict(Taxon._taxa))
  for key, record in RECORDS.items():
    Taxon.add(dict(record), key)


def _record_valid(record):
  return support.schema()['taxa'].check({'x': record})


def _node_valid(node):
  return support.schema()[io.TREE_DEF].check({'taxonomies': [node]})


def _tree(node):
  return Tree(node, {'source_key': SOURCE, 'type': 'taxonomy', 'position': next(POSITIONS)})


def _logged(caplog, level, build):
  """`build()`'s result and the messages the package logs at `level` and
  above while it runs."""
  with caplog.at_level(level, logger='phylohist'):
    caplog.clear()
    result = build()
  return result, [r.getMessage() for r in caplog.records if r.levelno >= level]


# -- schema -------------------------------------------------------------------


@pytest.mark.parametrize(
  'record',
  [
    MINERAL_RECORD,
    {'name': 'mineralum', 'rank': 'species', 'mineral': False, **EARLIER},
    {'name': 'mineralum', 'mineral': False, **EARLIER},
    {'name': 'mineralum', **EARLIER},
  ],
)
def test_schema_accepts_a_mineral_record_with_a_null_rank(record):
  assert _record_valid(record)


@pytest.mark.parametrize(
  'record',
  [
    {'name': 'mineralum', 'mineral': True, **EARLIER},
    {'name': 'mineralum', 'rank': 'species', 'mineral': True, **EARLIER},
    {'name': 'mineralum', 'rank': 'Unranked', 'mineral': True, **EARLIER},
    {'name': 'mineralum', 'rank': None, 'mineral': 'yes', **EARLIER},
  ],
)
def test_schema_rejects_a_mineral_record_without_a_null_rank(record):
  assert not _record_valid(record)


@pytest.mark.parametrize(
  'node',
  [
    {'taxon': GENUS, 'synonyms': [{'mineralTaxon': MINERAL}]},
    {'taxon': GENUS, 'non': [{'mineralTaxon': MINERAL}]},
    {'taxon': GENUS, 'lapsus': {'mineralTaxon': MINERAL}},
    {'taxon': GENUS, 'children': [{'mineralTaxon': MINERAL, 'new': True}]},
  ],
)
def test_schema_accepts_mineral_taxon_where_taxon_may_appear(node):
  assert _node_valid(node)


def test_schema_rejects_a_mineral_taxon_that_is_no_key():
  assert not _node_valid({'taxon': GENUS, 'synonyms': [{'mineralTaxon': 1}]})


# -- records ------------------------------------------------------------------


def test_a_mineral_reads_as_unranked_and_mineral():
  assert (Taxon.get(MINERAL).rank, Taxon.get(MINERAL).mineral) == ('Unranked', True)
  assert (Taxon.get(GENUS).mineral, Taxon.get(UNRANKED).mineral) == (False, False)


def test_a_spelling_of_a_mineral_is_a_mineral():
  assert Taxon.get(SPELLING).mineral is True
  vulgar = 'mineralen_linnaeus_1758'
  Taxon.add({'name': 'mineralen', 'lang': 'DE', 'vulgarSpellingOf': MINERAL}, vulgar)
  assert Taxon.get(vulgar).mineral is True


def test_a_mineral_key_takes_the_authority_suffix_as_a_species_does(caplog):
  record = {'name': 'lapillus', 'rank': None, 'mineral': True, **EARLIER}
  for key in ('lapillus_linnaeus_1758', 'lapillus'):
    _, errors = _logged(caplog, logging.ERROR, lambda key=key: Taxon.add(dict(record), key))
    assert errors == []
  _, errors = _logged(caplog, logging.ERROR, lambda: Taxon.add(dict(record), 'lapillus-stone'))
  assert len(errors) == 1
  assert errors[0].startswith('"lapillus-stone" not in expected set: ')
  assert 'lapillus_linnaeus_1758' in errors[0]


def test_a_mineral_is_exempt_from_the_rank_suffix_warnings(caplog):
  record = {'name': 'Lapida', 'rank': None, **EARLIER}
  _, warned = _logged(caplog, logging.WARNING, lambda: Taxon.add(dict(record), 'lapida'))
  assert len(warned) == 1 and 'Lapida with suffix "ida"' in warned[0]
  mineral = {**record, 'mineral': True}
  _, warned = _logged(caplog, logging.WARNING, lambda: Taxon.add(mineral, 'lapida_linnaeus_1758'))
  assert warned == []


# -- nodes --------------------------------------------------------------------


def test_mineral_taxon_loads_as_a_named_entry(caplog):
  node = {'taxon': GENUS, 'synonyms': [{'mineralTaxon': MINERAL}]}
  root, errors = _logged(caplog, logging.ERROR, lambda: _tree(node))
  assert errors == []
  [(_, entry)] = list(root.related())
  assert (entry.axis, entry.taxon is Taxon.get(MINERAL)) == ('synonyms', True)


def test_a_primary_mineral_taxon_is_checked_for_its_source_like_a_taxon(caplog):
  own = 'calculus_linnaeus_1766'
  Taxon.add(
    {'name': 'calculus', 'rank': None, 'mineral': True, 'authority': {'source': SOURCE}}, own
  )
  node = {'taxon': GENUS, 'children': [{'mineralTaxon': own}]}
  _, errors = _logged(caplog, logging.ERROR, lambda: _tree(node))
  assert len(errors) == 1
  assert 'lists this source as its authority, but is not marked as new' in errors[0]
  node = {'taxon': GENUS, 'children': [{'mineralTaxon': MINERAL, 'new': True}]}
  _, errors = _logged(caplog, logging.ERROR, lambda: _tree(node))
  assert len(errors) == 1 and errors[0].startswith('Expected source ')
  node = {'taxon': GENUS, 'children': [{'mineralTaxon': own, 'new': True}]}
  _, errors = _logged(caplog, logging.ERROR, lambda: _tree(node))
  assert errors == []


def test_designation_beside_mineral_taxon_is_an_error(caplog):
  node = {'taxon': GENUS, 'synonyms': [{'mineralTaxon': MINERAL, 'designation': 'a stone'}]}
  _, errors = _logged(caplog, logging.ERROR, lambda: _tree(node))
  assert len(errors) == 1
  assert errors[0].endswith('has `designation` but is not an `openTaxon` node')


def test_mineral_taxon_beside_taxon_is_one_field_too_many(caplog):
  node = {'taxon': GENUS, 'synonyms': [{'mineralTaxon': MINERAL, 'taxon': SPECIES}]}
  _, errors = _logged(caplog, logging.ERROR, lambda: _tree(node))
  assert len(errors) == 1 and errors[0].startswith('Found 2 taxon fields')


# -- the pairing check --------------------------------------------------------


def test_record_lookup_carries_mineral_and_reads_an_explicit_null_as_unranked():
  assert LOOKUP(MINERAL) == ('mineralum', 'Unranked', True)
  assert LOOKUP(SPELLING) == ('mineralun', 'Unranked', True)
  assert LOOKUP(GENUS) == ('Testum', 'genus', False)
  assert LOOKUP(UNRANKED) == ('Testaceum', 'Unranked', False)
  assert LOOKUP('nothing') is None


def test_record_lookup_agrees_with_the_loaded_taxa():
  for key in RECORDS:
    loaded = Taxon.get(key)
    assert (LOOKUP(key).rank, LOOKUP(key).mineral) == (loaded.rank, loaded.mineral)


def test_mineral_fields_says_nothing_for_a_right_pairing():
  for node in (
    {'mineralTaxon': MINERAL},
    {'mineralTaxon': SPELLING},
    {'taxon': GENUS, 'bracketStart': GENUS, 'bracketEnd': SPECIES},
    {'mineralTaxon': 'nothing'},
    {'mineralTaxon': 3},
    {},
  ):
    assert nomenclature.mineral_fields(node, LOOKUP) == []


def test_mineral_taxon_naming_no_mineral_is_an_error():
  expected = [('error', NOT_MINERAL.format(GENUS))]
  assert nomenclature.mineral_fields({'mineralTaxon': GENUS}, LOOKUP) == expected
  assert nomenclature.mineral_fields({'mineralTaxon': GENUS}, Taxon.get) == expected


@pytest.mark.parametrize('field', ['taxon', 'openTaxon', 'bracketStart', 'bracketEnd'])
def test_a_mineral_named_by_any_other_field_is_an_error(field):
  for key in (MINERAL, SPELLING):
    expected = [('error', ONLY_MINERAL_TAXON.format(field, key))]
    assert nomenclature.mineral_fields({field: key}, LOOKUP) == expected
    assert nomenclature.mineral_fields({field: key}, Taxon.get) == expected


def test_quoted_parent_and_a_compared_link_are_errors_on_a_mineral_node():
  assert nomenclature.quoted_parent({'mineralTaxon': MINERAL, 'quotedParent': True}, LOOKUP) == [
    ('error', '`quotedParent` on a node that is not a species-level name')
  ]
  assert nomenclature.compared_links({'mineralTaxon': MINERAL, 'cf': GENUS}, LOOKUP) == [
    ('error', '`cf` on a node that is not an `openTaxon`')
  ]


def test_the_load_reports_the_pairing_on_every_axis(caplog):
  document = {
    'taxonomies': [
      {
        'taxon': GENUS,
        'non': [{'taxon': MINERAL}],
        'type': {'taxon': MINERAL},
        'children': [{'mineralTaxon': SPECIES}],
      }
    ]
  }
  _, errors = _logged(
    caplog, logging.ERROR, lambda: _report_nomenclature({'trees': {SOURCE: document}})
  )
  assert sorted(errors) == sorted(
    [
      f'{SOURCE} at 0/non/0: ' + ONLY_MINERAL_TAXON.format('taxon', MINERAL),
      f'{SOURCE} at 0/type: ' + ONLY_MINERAL_TAXON.format('taxon', MINERAL),
      f'{SOURCE} at 0/children/0: ' + NOT_MINERAL.format(SPECIES),
    ]
  )


# -- drafts -------------------------------------------------------------------


@pytest.fixture(scope='module')
def mineral_corpus(tmp_path_factory):
  """A copy of the test corpus whose `taxa.yaml` has the mineral record."""
  directory = tmp_path_factory.mktemp('mineral-corpus')
  shutil.copytree(support.CORPUS, directory, dirs_exist_ok=True)
  with open(directory / 'taxa.yaml', 'a') as fd:
    fd.write(
      f'\n{MINERAL}:\n  name: mineralum\n  rank: null\n  mineral: true\n'
      '  authority:\n    source: 1758_linnaeus\n'
    )
  return directory


def _draft(tmp_path, data_dir, body):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text('taxonomies:\n- taxon: rhenopyrgus\n  children:\n' + body)
  return support.run_check_draft(draft, data_dir=data_dir)


def test_check_draft_accepts_a_mineral_named_by_mineral_taxon(tmp_path, mineral_corpus):
  body = f'  - taxon: sardesoni_bather_1915\n    synonyms:\n    - mineralTaxon: {MINERAL}\n'
  result = _draft(tmp_path, mineral_corpus, body)
  assert result.returncode == 0, result.stdout + result.stderr


def test_check_draft_reports_the_pairing_both_ways(tmp_path, mineral_corpus):
  body = f'  - taxon: {MINERAL}\n  - mineralTaxon: sardesoni_bather_1915\n'
  result = _draft(tmp_path, mineral_corpus, body)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'children/0: ' + ONLY_MINERAL_TAXON.format('taxon', MINERAL) in result.stdout
  assert 'children/1: ' + NOT_MINERAL.format('sardesoni_bather_1915') in result.stdout


def test_check_draft_lists_a_mineral_taxon_key_without_a_record(tmp_path, mineral_corpus):
  result = _draft(tmp_path, mineral_corpus, '  - mineralTaxon: nothing_here\n')
  assert 'nothing_here' in result.stdout


# -- the other loader reports -------------------------------------------------


def test_the_protologue_check_reads_no_rank_off_a_mineral(caplog):
  own = 'calculus_linnaeus_1766'
  record = {'name': 'calculus', 'rank': None, 'authority': {'source': SOURCE, 'pages': 22}}
  Taxon.add({**record, 'mineral': True}, own)
  tree = _tree({'mineralTaxon': own, 'new': True})
  _, errors = _logged(
    caplog,
    logging.ERROR,
    lambda: _report_protologue_mismatches({'trees': {SOURCE: {}}}, {SOURCE: [tree]}),
  )
  assert errors == []
  # The same record as a taxon is read as a species, which its null rank
  # is not.
  Taxon.add(dict(record), 'calculus')
  tree = _tree({'taxon': 'calculus', 'new': True})
  _, errors = _logged(
    caplog,
    logging.ERROR,
    lambda: _report_protologue_mismatches({'trees': {SOURCE: {}}}, {SOURCE: [tree]}),
  )
  assert errors == [
    'taxa.yaml calculus: rank none but its protologue node in '
    'data/trees/1766_linnaeus.yaml implies "species"'
  ]


def test_the_rank_order_check_ignores_a_mineral_under_a_genus(caplog):
  tree = _tree({'taxon': GENUS, 'children': [{'mineralTaxon': MINERAL}]})
  _, errors = _logged(caplog, logging.ERROR, lambda: _report_rank_order({SOURCE: [tree]}))
  assert errors == []


# -- claims and the names index -----------------------------------------------


def test_a_mineral_synonym_yields_a_usage_and_an_acceptance():
  tree = _tree({'taxon': GENUS, 'synonyms': [{'mineralTaxon': MINERAL, 'citedAs': 'Mineralum'}]})
  about = {c['kind']: c for c in extract({SOURCE: [tree]})[SOURCE] if c['subject'] == MINERAL}
  assert set(about) == {'usage', 'acceptance'}
  usage, acceptance = about['usage'], about['acceptance']
  assert (usage['form'], usage['spelling'], usage['axis']) == ('mineralTaxon', MINERAL, 'synonyms')
  assert 'placeholder' not in usage
  assert (acceptance['stance'], acceptance['under']) == ('accepts', GENUS)


def test_the_names_index_marks_a_mineral_and_its_spellings():
  rows = names_index()
  mineral = rows[MINERAL]
  assert (mineral['mineral'], mineral['rank'], mineral['kind']) == (True, 'Unranked', 'primary')
  spelling = rows[SPELLING]
  assert (spelling['mineral'], spelling['kind'], spelling['of']) == (True, 'altSpellingOf', MINERAL)
  assert 'mineral' not in rows[GENUS] and 'mineral' not in rows[UNRANKED]


# -- the store ----------------------------------------------------------------

HOMONYM = 'mineralum'


@pytest.fixture(scope='module')
def synthetic(corpus, tmp_path_factory):
  """A `ClaimStore` over a copy of `claims/` with `SOURCE`'s claims replaced
  by those of a tree citing the mineral in a synonymy, and the names index
  carrying the mineral, its spelling and a genus of the same name."""
  directory = tmp_path_factory.mktemp('claims')
  shutil.copytree(corpus.claims, directory, dirs_exist_ok=True)
  records = (
    (MINERAL, MINERAL_RECORD),
    (SPELLING, RECORDS[SPELLING]),
    (GENUS, GENUS_RECORD),
    (HOMONYM, {'name': 'Mineralum', 'rank': 'genus', **EARLIER}),
  )
  with pytest.MonkeyPatch.context() as patch:
    for key, record in records:
      patch.setitem(Taxon._taxa, key, Taxon(dict(record), key))
    tree = Tree(
      {'taxon': GENUS, 'synonyms': [{'mineralTaxon': MINERAL, 'citedAs': 'Mineralum'}]},
      {'source_key': SOURCE, 'type': 'taxonomy', 'position': 620},
    )
    claims = extract({SOURCE: [tree]})[SOURCE]
    rows = names_index()
  (directory / f'{SOURCE}.jsonl').write_text(''.join(json.dumps(c) + '\n' for c in claims))
  names = json.loads((directory / 'names.json').read_text())
  for key, _ in records:
    names[key] = rows[key]
  (directory / 'names.json').write_text(json.dumps(names))
  return ClaimStore(directory)


def test_resolve_finds_a_mineral_and_keeps_it_apart_from_a_genus_of_the_name(synthetic):
  candidates = {c['key']: c for c in synthetic.resolve_name('mineralum')}
  assert set(candidates) == {MINERAL, HOMONYM}
  mineral = candidates[MINERAL]
  assert (mineral['mineral'], mineral['rank']) == (True, 'Unranked')
  assert mineral['variants'] == [SPELLING]
  assert 'mineral' not in candidates[HOMONYM]
  assert MINERAL not in candidates[HOMONYM]['variants']


def test_the_synonymy_block_lists_the_mineral_entry(synthetic):
  [block] = synthetic.contents(SOURCE, GENUS, synonymy=True)
  assert 'mineralum' in block['rendered']
  blocks = synthetic.synonymy(GENUS, SOURCE)
  assert any('mineralum' in block['rendered'] for block in blocks)


def test_the_cli_prints_mineral_in_place_of_the_rank(capsys):
  candidate = {
    'key': MINERAL,
    'name': 'mineralum',
    'rank': 'Unranked',
    'kind': 'primary',
    'mineral': True,
    'sourcesWithStatements': 1,
    'variants': [],
  }
  cli._print_resolved([candidate], 'text')
  assert capsys.readouterr().out.startswith(f'{MINERAL}  mineralum (mineral, primary); ')
