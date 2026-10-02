"""Every eval question's expected answer must still build from the corpus.

`eval/README.md` promises that a question whose expected answer stops
matching the data is updated or removed, never left stale; this test
makes that mechanical. An expected answer is the blocks it is made of
(a tool and the parameters that matter) and the strings the rendered
answer shows. Each alternative is a plan that `phylohist.plan.execute`
must build in full, every block resting on claims or being a gap or
absence statement; the rendered composition of each alternative
must contain every `shows` string, the question's and its own.

The manifest's inconsistency rows are gated too: a declared coverage
value that the derived claims contradict fails until the declaration or
the tree is corrected (`scripts/claims.py --inconsistencies` explains
each row).
"""

import collections
import logging
import os
import pathlib

import pytest
import yaml

from phylohist import plan
from phylohist.claims import (
  corrected_node,
  derived_coverage,
  extract,
  holotype_conflicts,
  manifest,
  merge_patch,
)
from phylohist.evaluation import alternatives, normalise
from phylohist.loader.taxa import Tree
from phylohist.render import render_composition

QUESTIONS_PATH = pathlib.Path(__file__).parent.parent / 'eval' / 'questions.yaml'

with open(QUESTIONS_PATH) as fd:
  QUESTIONS = yaml.safe_load(fd)

pytestmark = pytest.mark.skipif(
  bool(os.getenv('PHYLOHIST_DRAFTS')),
  reason='the eval set is written against data/ only',
)


@pytest.fixture(scope='session')
def roots(load_records):
  _, _, roots = load_records
  return roots


@pytest.fixture(scope='session')
def claims(roots):
  return extract(roots)


@pytest.mark.parametrize('question', QUESTIONS, ids=[q['id'] for q in QUESTIONS])
def test_question(question):
  expected = question['expected']
  qid = question['id']
  for alternative in alternatives(expected):
    # Each alternative is a plan; it must build in full and show its
    # strings and the question's.
    outcome = plan.execute({'header': '', 'blocks': alternative['blocks']})
    if outcome['errors']:
      pytest.fail(f'{qid}: {outcome["errors"]}')
    for block in outcome['blocks']:
      if block['type'] != 'statement' and not block['claims']:
        pytest.fail(f'{qid}: {block["tool"]} {block["parameters"]} rests on no claim')
    rendered = normalise(render_composition(outcome['composition'], 'text'))
    for text in list(expected.get('shows') or ()) + alternative['shows']:
      if normalise(text) not in rendered:
        pytest.fail(f'{qid}: the expected answer does not show "{text}"')


def test_no_inconsistencies(claims, roots):
  rows = {
    source_key: entry['inconsistencies']
    for source_key, entry in manifest(claims, roots)['sources'].items()
    if entry['inconsistencies']
  }
  if rows:
    listing = '\n'.join(f'{source_key}: {"; ".join(found)}' for source_key, found in rows.items())
    pytest.fail(
      f'{len(rows)} sources declare coverage their claims contradict '
      f'(run scripts/claims.py --inconsistencies):\n{listing}',
    )


def test_merge_patch_follows_rfc_7396():
  target = {'a': 'b', 'c': {'d': 'e', 'f': 'g'}}
  assert merge_patch(target, {'a': 'z', 'c': {'f': None}}) == {'a': 'z', 'c': {'d': 'e'}}
  assert merge_patch({'a': [1, 2]}, {'a': {'x': 1}}) == {'a': {'x': 1}}
  assert merge_patch({'a': 1}, 'text') == 'text'
  assert merge_patch(None, {'a': None, 'b': 2}) == {'b': 2}
  assert target == {'a': 'b', 'c': {'d': 'e', 'f': 'g'}}


def test_corrected_node_applies_the_editorial_corrections():
  data = {
    'taxon': 'isorophida',
    'auth': ['bell.b.m'],
    'year': 1974,
    'citedAs': 'Bell, 1974',
    'editorial': {
      'corrections': {'auth': None, 'year': None, 'authority': {'source': '1976_bell.b.m'}},
      'basis': 'cited before publication',
    },
  }
  assert corrected_node(data) == {
    'taxon': 'isorophida',
    'citedAs': 'Bell, 1974',
    'authority': {'source': '1976_bell.b.m'},
  }
  assert corrected_node({'taxon': 'x', 'editorial': {'inferred': True, 'basis': 'b'}}) is None
  # A null with nothing to put in its place: the printed field is dropped.
  dropped = corrected_node(
    {'taxon': 'x', 'pages': 12, 'editorial': {'corrections': {'pages': None}, 'basis': 'b'}}
  )
  assert dropped == {'taxon': 'x'}


def test_corrections_reach_the_claims(claims):
  # Bell 1975 cites "Bell, 1974" for the paper that appeared in 1976: the
  # usage stays as printed, names its erroneous fields, and carries the
  # attribution the editor reads instead.
  by_id = {c['id']: c for c in claims['1975_bell.b.m']}
  usage = by_id['1975_bell.b.m:0/children/0:usage']
  assert usage['printed'] == {'auth': ['bell.b.m'], 'year': 1974, 'citedAs': 'Bell, 1974'}
  assert usage['printedErrors'] == ['auth', 'year']
  assert usage['corrected'] == {
    'printed': {'citedAs': 'Bell, 1974'},
    'citesSource': '1976_bell.b.m',
  }
  assert 'erroneous' not in usage
  note = by_id['1975_bell.b.m:0/children/0:editorial']
  assert 'errors' not in note and note['corrections']['authority'] == {'source': '1976_bell.b.m'}


def test_manifest_carries_author_surnames(claims, roots):
  authors = manifest(claims, roots)['authors']
  assert authors['bell.b.m'] == 'Bell' and authors['bather'] == 'Bather'


def test_change_node_acts(claims):
  # A `translated` node names the taxon at the earlier rank; the node itself
  # is the earlier state as cited, so it emits its usage on its own axis.
  transl = next(
    c
    for c in claims['1994_guensburg_sprinkle']
    if c.get('actKind') == 'nomTransl' and c['subject'] == 'rhenopyrginae'
  )
  assert transl['translatedFrom'] == 'rhenopyrgidae'
  assert 'modifier' not in transl and 'altRankOf' not in transl
  earlier = next(
    c
    for c in claims['1994_guensburg_sprinkle']
    if c['kind'] == 'usage' and c['path'] == transl['path'] + '/translated'
  )
  assert earlier['axis'] == 'translated' and earlier['subject'] == 'rhenopyrgidae'
  # An act the source follows rather than performs names the work.
  parsley = next(c for c in claims['1982c_parsley'] if c.get('actKind') == 'nomTransl')
  assert parsley['by'] == '1968b_paul.c.r.c' and 'translatedFrom' not in parsley
  # A nomen nudum is an act on the synonymy entry that cites the nude usage.
  nudum = [c for c in claims['2005_frest'] if c.get('actKind') == 'nomNudum']
  assert len(nudum) == 3 and all('/synonyms/' in c['path'] for c in nudum)


@pytest.mark.parametrize('axis', ['translated', 'corrected', 'substituted', 'moved', 'removed'])
def test_earlier_state_entries_are_cited(load_records, caplog, axis):
  # The node under a change is the earlier state of the name as this
  # source cites it: as on a synonymy entry, its pages and illustrations
  # locate that earlier use, never this source's own page or figure.
  illustrations = [{'page': 13, 'figures': ['1']}]
  earlier = {
    'taxon': 'rhenopyrgidae',
    'pages': 12,
    'illustrations': illustrations,
    # The cited work's own material is not this source's: none of the four
    # material fields on a cited entry emits a claim.
    'material': [{'catalogNumbers': ['GSC 1']}],
    'contexts': {'somewhere': {'unit': ['Some Formation']}},
    'ranges': [{'series': 'Ordovician'}],
  }
  child = {'taxon': 'rhenopyrgus', axis: [earlier] if axis == 'removed' else earlier}
  root = Tree(
    {'taxon': 'cyathocystidae', 'pages': 100, 'children': [child]},
    {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 99},
  )
  claims = extract({'1961_dehm': [root]})['1961_dehm']
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  cited = [c for c in claims if f'/{axis}' in c['path']]
  assert cited and not [c for c in cited if c['kind'] == 'material']
  for claim in cited:
    assert 'pages' not in claim
    assert claim['citedPages'] == 12 and claim['citedIllustrations'] == illustrations


def test_lapsus_is_the_slip_not_a_synonym(load_records, caplog):
  # The intended name stands in the tree and the name printed by a slip of
  # the pen hangs under `lapsus`: the intended name's node names the slip,
  # and the slip is used as printed here but neither accepted as a synonym
  # nor claimed as new, though its place is its protologue.
  child = {
    'taxon': 'ottawaensis_whiteaves_1897',
    'lapsus': {'taxon': 'canadensis_billings_1866', 'pages': 13},
  }
  root = Tree(
    {'taxon': 'astrocystites', 'pages': 100, 'children': [child]},
    {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 98},
  )
  claims = extract({'1961_dehm': [root]})['1961_dehm']
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  by_path = collections.defaultdict(list)
  for claim in claims:
    by_path[claim['path']].append(claim)
  act = next(c for c in by_path['98/children/0'] if c['kind'] == 'act')
  assert act['actKind'] == 'lapsus' and act['lapsusAs'] == 'canadensis_billings_1866'
  [slip] = by_path['98/children/0/lapsus']
  assert slip['kind'] == 'usage' and slip['axis'] == 'lapsus'
  # The slip is printed in this source: its pages are the source's own.
  assert slip['pages'] == 13 and 'citedPages' not in slip
  assert '1961_dehm' in Tree._new_index['canadensis_billings_1866']


def test_lapsus_listed_in_a_synonymy(claims):
  # Bather 1914 notes Whiteaves's slip: the entry names the record the
  # slip was printed for, and is accepted under it without being a synonym.
  [entry] = [
    c
    for c in claims['1914c_bather']
    if c['kind'] == 'acceptance' and c['subject'] == 'canadensis_whiteaves_1898'
  ]
  assert entry['lapsusFor'] == 'ottawaensis_whiteaves_1897'
  assert entry['parents'] == ['steganoblastus'] and entry['citedPages'] == 395


def test_lapsus_records_stay_under_lapsus(load_records, caplog):
  # A lapsus record appears under `lapsus`, or as a synonymy entry marked
  # `lapsusFor`; anywhere else, and a `lapsusFor` off a synonymy entry, is
  # an error.
  from phylohist.loader.load import _report_lapsus_records

  slip = {'taxon': 'canadensis_billings_1866'}
  printed = Tree(
    {
      'taxon': 'astrocystites',
      'children': [{'taxon': 'ottawaensis_whiteaves_1897', 'lapsus': slip}],
    },
    {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 97},
  )
  listed = {
    'taxon': 'ottawaensis_whiteaves_1897',
    'synonyms': [dict(slip, lapsusFor={'taxon': 'ottawaensis_whiteaves_1897'})],
  }
  placed = Tree(
    {'taxon': 'astrocystites', 'children': [dict(slip), listed]},
    {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 96},
  )
  caplog.clear()
  _report_lapsus_records({'1961_dehm': [printed, placed]})
  errors = [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]
  assert len(errors) == 1 and '[96]/astrocystites/0/canadensis_billings_1866' in errors[0]

  caplog.clear()
  Tree(
    {'taxon': 'astrocystites', 'lapsusFor': {'taxon': 'ottawaensis_whiteaves_1897'}},
    {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 95},
  )
  errors = [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]
  assert len(errors) == 1 and 'is not a `synonyms` or `non` entry' in errors[0]


def test_recombined_is_the_printed_new_combination(load_records, caplog):
  # "comb. nov.": the act on the species, beside the move out of the genus
  # it leaves; followed from another work, it names that work.
  child = {
    'taxon': 'grayae_bather_1915',
    'recombined': True,
    'moved': {'taxon': 'pyrgocystis'},
  }
  followed = {
    'taxon': 'coronaeformis_rievers_1961',
    'recombined': {'by': {'source': '1983_holloway_jell', 'pages': 12}},
  }
  root = Tree(
    {'taxon': 'rhenopyrgus', 'children': [child, followed]},
    {'source_key': '1985_jell_burrett_banks', 'type': 'taxonomy', 'position': 94},
  )
  claims = extract({'1985_jell_burrett_banks': [root]})['1985_jell_burrett_banks']
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  at = collections.defaultdict(list)
  for claim in claims:
    at[claim['path']].append(claim)
  kinds = {(c['kind'], c.get('actKind')) for c in at['94/children/0']}
  assert {('act', 'combNov'), ('act', 'moved'), ('rejection', None)} <= kinds
  [act] = [c for c in at['94/children/1'] if c.get('actKind') == 'combNov']
  assert act['by'] == '1983_holloway_jell' and act['byPages'] == 12

  caplog.clear()
  Tree(
    {'taxon': 'rhenopyrgus', 'recombined': True},
    {'source_key': '1985_jell_burrett_banks', 'type': 'taxonomy', 'position': 93},
  )
  errors = [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]
  assert len(errors) == 1 and 'is not a species-group name' in errors[0]


def test_material_adapter(load_records, caplog):
  # Contexts, material, illustrations, ranges, in that fixed order, over a
  # node with a file context, a node context, a numbered entry, a range
  # pair, a label-only entry, an explicit repository, a repository resolved
  # through the file's list, a tentative context, tied and untied
  # illustrations, and two ranges.
  file_contexts = {
    'division-st': {'unit': ['Trenton Limestone'], 'location': ['Division Street, Ottawa']},
  }
  node_data = {
    'taxon': 'rhenopyrgus',
    'contexts': {'quarry-x': {'unit': ['Quarry X Beds']}},
    'material': [
      {'catalogNumbers': ['GSC 752'], 'role': 'lectotype', 'context': 'division-st'},
      {'catalogNumbers': [['GSC 100', 'GSC 105']], 'role': 'paratype', 'formerIds': ['G 1']},
      {'label': 'the specimen lent to Hudson', 'role': 'syntype', 'status': 'lost'},
      {'catalogNumbers': ['XYZ 1'], 'repository': 'nhmuk', 'notes': 'lent'},
      {'catalogNumbers': ['PE 7'], 'preparation': 'latex cast', 'castOf': 'GSC 752'},
      {
        'catalogNumbers': ['GSC 900'],
        'context': {'key': 'division-st', 'tentative': True},
        'role': 'hypotype',
      },
      {
        'catalogNumbers': ['GSC 901'],
        'role': 'syntype',
        'editorial': {'inferred': ['role'], 'basis': 'Only "the type" is printed.'},
      },
    ],
    'illustrations': [
      {'textFigures': [3], 'of': 'GSC 752'},
      {
        'plate': 1,
        'figures': [2],
        'of': ['GSC 100', 'the specimen lent to Hudson'],
        'depicts': 'cast',
      },
      {'plate': 2, 'uncertain': True},
    ],
    'ranges': [
      {
        'series': 'Middle Ordovician',
        'regions': ['Ottawa', {'value': 'Quebec', 'tentative': True}],
      },
      {'period': 'Devonian', 'regions': ['Germany']},
    ],
  }
  root = Tree(
    node_data,
    {
      'source_key': '1961_dehm',
      'type': 'taxonomy',
      'position': 90,
      'file_contexts': file_contexts,
      'file_unused': (),
      'file_repositories': ('fmnh',),
    },
  )
  claims = extract({'1961_dehm': [root]})['1961_dehm']
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  material = [c for c in claims if c['kind'] == 'material']

  # The fixed order fixes the ids.
  kinds = [c['materialKind'] for c in material]
  assert kinds == ['occurrence'] * 2 + ['specimen'] * 7 + ['illustration'] * 3 + ['range'] * 2
  assert [c['id'] for c in material] == [f'1961_dehm:90:material:{n}' for n in range(len(material))]
  assert [
    c['id'] for c in extract({'1961_dehm': [root]})['1961_dehm'] if c['kind'] == 'material'
  ] == [c['id'] for c in material]

  # A file context the node refers to and the node's own context, once each.
  file_ctx, node_ctx = material[:2]
  assert file_ctx['contextKey'] == 'division-st' and file_ctx['contextScope'] == 'file'
  assert file_ctx['occurrence'] == file_contexts['division-st']
  assert node_ctx['contextKey'] == 'quarry-x' and node_ctx['contextScope'] == 'node'
  assert node_ctx['occurrence'] == node_data['contexts']['quarry-x']

  numbered, pair, label_only, explicit, file_listed, tentative, inferred = material[2:9]

  assert numbered['role'] == 'lectotype' and numbered['ids'] == ['GSC 752']
  assert numbered['catalogNumbers'] == ['GSC 752'] and numbered['contextKey'] == 'division-st'
  assert 'contextTentative' not in numbered
  assert numbered['repository'] == 'gsc' and numbered['repositoryVia'] == 'prefix'
  assert numbered['joinKeys'] == ['gsc:752'] and 'rangeJoin' not in numbered
  assert 'roleAct' not in numbered  # not a protologue node

  assert pair['ids'] == [['GSC 100', 'GSC 105']] and pair['formerIds'] == ['G 1']
  assert pair['joinKeys'] == ['gsc:100', 'gsc:105'] and pair['rangeJoin'] is True

  assert label_only['label'] == 'the specimen lent to Hudson' and label_only['status'] == 'lost'
  assert label_only['ids'] == [] and label_only['repository'] is None
  assert 'joinKeys' not in label_only and 'repositoryVia' not in label_only

  assert explicit['repository'] == 'nhmuk' and explicit['repositoryVia'] == 'explicit'
  assert explicit['joinKeys'] == ['nhmuk:xyz1'] and explicit['materialNotes'] == 'lent'
  assert 'role' not in explicit

  # `PE` belongs to two registry entries; the file's list settles it.
  assert file_listed['repository'] == 'fmnh' and file_listed['repositoryVia'] == 'file'
  assert file_listed['preparation'] == 'latex cast' and file_listed['castOf'] == 'GSC 752'

  assert tentative['contextKey'] == 'division-st' and tentative['contextTentative'] is True

  # The claim is about the entry: its editorial block, not the node's.
  assert inferred['editorial'] == node_data['material'][6]['editorial']
  assert inferred['inferredFields'] == ['role']

  tied, list_tied, untied = material[9:12]
  assert tied['illustration'] == {'textFigures': [3]} and tied['of'] == 'GSC 752'
  assert tied['ofClaim'] == [numbered['id']]
  assert list_tied['of'] == ['GSC 100', 'the specimen lent to Hudson']
  assert list_tied['depicts'] == 'cast' and 'depicts' not in tied
  assert list_tied['illustration'] == {'plate': 1, 'figures': [2]}
  assert list_tied['ofClaim'] == [pair['id'], label_only['id']]
  assert numbered['illustrationClaims'] == [tied['id']]
  assert numbered['specimenIllustrations'] == [tied['illustration']]
  assert pair['illustrationClaims'] == [list_tied['id']]
  assert untied['illustration'] == {'plate': 2, 'uncertain': True}
  assert 'ofClaim' not in untied and 'illustrationClaims' not in explicit

  first, second = material[12:14]
  assert first['range'] == node_data['ranges'][0] and second['range'] == node_data['ranges'][1]

  # A protologue node: the entry's own `roleAct` wins, else a holotype,
  # paratype, syntype or cotype is this source's designation, and any
  # other role derives none. An open-nomenclature record sidesteps the
  # protologue-source check a named one would need.
  new_node = Tree(
    {
      'openTaxon': 'rhenopyrgus-sp-1_ewin_martin.m_isotalo_zamora_2020',
      'new': True,
      'material': [
        {'count': 5, 'role': 'paratype', 'roleAct': 'reported'},
        {'catalogNumbers': ['GSC 1'], 'role': 'holotype'},
        {'catalogNumbers': ['GSC 2'], 'role': 'cotype'},
        {'catalogNumbers': ['GSC 3'], 'role': 'hypotype'},
        {'catalogNumbers': ['GSC 4']},
      ],
    },
    {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 91},
  )
  new_claims = [
    c for c in extract({'1961_dehm': [new_node]})['1961_dehm'] if c['kind'] == 'material'
  ]
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  assert [c.get('roleAct') for c in new_claims] == [
    'reported',
    'designated',
    'designated',
    None,
    None,
  ]
  assert new_claims[0]['count'] == 5


def _specimen(entry, file_repositories=()):
  root = Tree(
    {'taxon': 'rhenopyrgus', 'material': entry},
    {
      'source_key': '1961_dehm',
      'type': 'taxonomy',
      'position': 90,
      'file_repositories': file_repositories,
    },
  )
  claims = extract({'1961_dehm': [root]})['1961_dehm']
  return [c for c in claims if c.get('materialKind') == 'specimen']


def test_two_printed_forms_of_one_catalog_number_share_a_join_key(load_records):
  first, second = _specimen([{'catalogNumbers': ['F. 5404']}, {'catalogNumbers': ['UQF5404']}])
  assert first['joinKeys'] == second['joinKeys'] == ['uq-f:5404']
  # The printed form stays in `ids`.
  assert (first['ids'], second['ids']) == (['F. 5404'], ['UQF5404'])


def test_a_range_pairs_two_join_keys_are_both_bare(load_records):
  [pair] = _specimen([{'catalogNumbers': [['UQF 5399', 'F. 5403']]}])
  assert pair['joinKeys'] == ['uq-f:5399', 'uq-f:5403'] and pair['rangeJoin'] is True


def test_an_explicit_repository_strips_its_own_prefix_only(load_records):
  own, other = _specimen(
    [
      {'catalogNumbers': ['GSC 752'], 'repository': 'gsc'},
      {'catalogNumbers': ['MCZ 690'], 'repository': 'usnm'},
    ],
  )
  assert own['joinKeys'] == ['gsc:752']
  assert other['joinKeys'] == ['usnm:mcz690']


def test_each_number_of_an_entry_keys_under_its_own_holder(load_records):
  [mixed] = _specimen([{'catalogNumbers': ['UTGD 122233', 'NMVP 107053', ['UQF 1', 'QMF 2']]}])
  assert mixed['repository'] == 'utgd' and mixed['repositoryVia'] == 'prefix'
  assert mixed['joinKeys'] == ['utgd:122233', 'nmv-p:107053', 'uq-f:1', 'qm-f:2']


def test_a_number_that_resolves_to_nothing_keys_under_the_entrys_repository(load_records):
  [mixed] = _specimen([{'catalogNumbers': ['GSC 752', 'ZZZ 5', 'Specimen 9']}])
  assert mixed['joinKeys'] == ['gsc:752', 'gsc:zzz5', 'gsc:specimen9']


def test_an_explicit_collection_keys_a_parent_prefix_under_the_institution(load_records):
  [specimen] = _specimen([{'catalogNumbers': ['USNM 165421'], 'repository': 'usnm-walcott'}])
  assert specimen['repository'] == 'usnm-walcott' and specimen['repositoryVia'] == 'explicit'
  assert specimen['joinKeys'] == ['usnm:165421']


def test_an_explicit_repository_wins_over_the_prefix_of_an_unrelated_holder(load_records):
  [specimen] = _specimen(
    [
      {'catalogNumbers': ['MCZ 690', 'USNM 5', 'UQF 9'], 'repository': 'usnm'},
    ],
  )
  # A sibling collection is not an ancestor: the explicit holder keeps it.
  assert specimen['joinKeys'] == ['usnm:mcz690', 'usnm:5', 'usnm:uqf9']
  [sibling] = _specimen([{'catalogNumbers': ['S 7'], 'repository': 'usnm-walcott'}])
  assert sibling['joinKeys'] == ['usnm-walcott:s7']


def test_a_file_listed_prefix_strips_to_the_bare_number(load_records):
  [specimen] = _specimen([{'catalogNumbers': ['PE-214']}], ('fmnh',))
  assert specimen['repository'] == 'fmnh' and specimen['joinKeys'] == ['fmnh:214']


def _occurrence(context, file_repositories=()):
  root = Tree(
    {'taxon': 'rhenopyrgus', 'contexts': {'x': context}},
    {
      'source_key': '1961_dehm',
      'type': 'taxonomy',
      'position': 90,
      'file_repositories': file_repositories,
    },
  )
  claims = extract({'1961_dehm': [root]})['1961_dehm']
  [claim] = [c for c in claims if c.get('materialKind') == 'occurrence']
  return claim


def test_locality_keys_join_two_printed_forms_of_one_number(load_records):
  claim = _occurrence({'localityNumbers': ['Walcott 35k', 'USNM loc. 35k', 'USGS 5462']})
  assert claim['localityKeys'] == ['usnm-l:35k', 'usgs-l:5462']


def test_locality_keys_use_the_listed_field_code_register(load_records):
  context = {'localityNumbers': ['SH-1', 'USGS 4148 CO', 'unresolvable? 7']}
  assert _occurrence(context, ('sprinkle-l',))['localityKeys'] == [
    'sprinkle-l:sh1',
    'usgs-l:4148co',
    'sprinkle-l:unresolvable?7',
  ]
  # Unlisted, SH-1 resolves to nothing, and a context with none has no field.
  assert _occurrence(context)['localityKeys'] == ['usgs-l:4148co']
  assert 'localityKeys' not in _occurrence({'unit': ['Wheeler Shale']})
  assert 'localityKeys' not in _occurrence({'localityNumbers': ['SH-1']})


def test_a_specimen_is_followed_across_sources_by_its_join_key(claims):
  # Whitehouse 1941's "F. 5404" and Jell & Sprinkle 2021's "UQF5404".
  keys = {}
  for source in ('1941_whitehouse', '2021_jell_sprinkle'):
    [holotype] = [
      c
      for c in claims[source]
      if c['kind'] == 'material'
      and c['materialKind'] == 'specimen'
      and c['subject'] == 'navicula_whitehouse_1941'
      and c.get('role') == 'holotype'
    ]
    keys[source] = holotype['joinKeys']
  assert keys['1941_whitehouse'] == keys['2021_jell_sprinkle'] == ['uq-f:5404']


def test_derived_coverage():
  base = {'source_key': '1961_dehm', 'type': 'taxonomy'}

  def tree(data, position, file_unused=()):
    return Tree(data, {**base, 'position': position, 'file_unused': file_unused})

  def derived(root, kind='material'):
    return derived_coverage({'s': [root]})['s'][kind]

  child = {'taxon': 'grayae_bather_1915'}
  other = {'taxon': 'sardesoni_bather_1915'}
  cases = [
    # `na`: the file lists the field as unused, whatever the nodes say.
    ('na', tree({'taxon': 'rhenopyrgus'}, 0, file_unused=('material',))),
    # A species null and no species lacks the field: `all`. The genus has
    # no `material` and is not counted.
    (
      'all',
      tree(
        {
          'taxon': 'rhenopyrgus',
          'children': [{**child, 'material': [{'label': 'A'}]}, {**other, 'material': None}],
        },
        1,
      ),
    ),
    # A species null and another species lacks it: `partly`.
    (
      'partly',
      tree(
        {
          'taxon': 'rhenopyrgus',
          'children': [{**child, 'material': None}, other],
        },
        2,
      ),
    ),
    # `all` downgraded by an entry that is not list-complete, read from
    # every named node.
    (
      'partly',
      tree(
        {
          'taxon': 'rhenopyrgus',
          'material': [{'label': 'A', 'listComplete': False}],
          'children': [{**child, 'material': None}],
        },
        3,
      ),
    ),
    # Values alone declare nothing: a value says what the source prints,
    # not that the file was audited for the field.
    (None, tree({'taxon': 'rhenopyrgus', 'material': [{'label': 'A'}], 'children': [child]}, 4)),
    (None, tree({'taxon': 'rhenopyrgus'}, 5)),
    # A cited entry never counts, whatever it carries or lacks.
    (
      'all',
      tree(
        {
          'taxon': 'rhenopyrgus',
          'children': [{**child, 'material': None}],
          'synonyms': [other],
        },
        6,
      ),
    ),
    # A null on a genus is not counted: specimens are cited for species.
    (
      None,
      tree(
        {
          'taxon': 'rhenopyrgus',
          'material': None,
          'children': [
            {**child, 'material': [{'label': 'A'}]},
            {**other, 'material': [{'label': 'B'}]},
          ],
        },
        11,
      ),
    ),
  ]
  for expected, root in cases:
    assert derived(root) == expected, (expected, root.data)

  # `occurrences` reads `contexts` or `ranges`; `na` needs both unused.
  occ = tree(
    {
      'taxon': 'rhenopyrgus',
      'ranges': [{'series': 'Ordovician'}],
      'children': [{**child, 'contexts': None}],
    },
    7,
  )
  assert derived(occ, 'occurrences') == 'all'
  only_one = tree({'taxon': 'rhenopyrgus'}, 8, file_unused=('ranges',))
  assert derived(only_one, 'occurrences') is None
  both = tree({'taxon': 'rhenopyrgus'}, 9, file_unused=('ranges', 'contexts'))
  assert derived(both, 'occurrences') == 'na'

  # `illustrations` reads the `illustrations` field.
  ill = tree({'taxon': 'rhenopyrgus', 'children': [{**child, 'illustrations': None}]}, 10)
  assert derived(ill, 'illustrations') == 'all'

  # Like `material`, `illustrations` counts species-level nodes only: a
  # genus without the field is not an uncaptured one, so a species value
  # and a species null are `all`.
  ill_genus = tree(
    {
      'taxon': 'rhenopyrgus',
      'children': [
        {**child, 'illustrations': [{'plate': 1}]},
        {**other, 'illustrations': None},
      ],
    },
    12,
  )
  assert derived(ill_genus, 'illustrations') == 'all'
  # A species lacking the field still makes it `partly`.
  ill_species = tree(
    {'taxon': 'rhenopyrgus', 'children': [{**child, 'illustrations': None}, other]}, 13
  )
  assert derived(ill_species, 'illustrations') == 'partly'
  # A figure on a genus is a value, not a null: it does not declare.
  ill_on_genus = tree({'taxon': 'rhenopyrgus', 'illustrations': [{'plate': 1}]}, 14)
  assert derived(ill_on_genus, 'illustrations') is None

  # `occurrences` is captured through a material entry's `context`: a
  # species with no `contexts`/`ranges` but a linked entry counts as
  # present, beside a species whose `ranges` is null.
  linked = tree(
    {
      'taxon': 'rhenopyrgus',
      'ranges': [{'series': 'Ordovician'}],
      'children': [
        {**child, 'material': [{'label': 'A', 'context': 'x'}]},
        {**other, 'ranges': None},
      ],
    },
    15,
  )
  assert derived(linked, 'occurrences') == 'all'
  # Without the link the same species is an uncaptured field.
  unlinked = tree(
    {
      'taxon': 'rhenopyrgus',
      'ranges': [{'series': 'Ordovician'}],
      'children': [{**child, 'material': [{'label': 'A'}]}, {**other, 'ranges': None}],
    },
    16,
  )
  assert derived(unlinked, 'occurrences') == 'partly'
  # A linked node that also writes a null is present and still declares.
  linked_null = tree(
    {
      'taxon': 'rhenopyrgus',
      'ranges': [{'series': 'Ordovician'}],
      'children': [{**child, 'material': [{'label': 'A', 'context': 'x'}], 'contexts': None}],
    },
    17,
  )
  assert derived(linked_null, 'occurrences') == 'all'
  linked_only = tree(
    {
      'taxon': 'rhenopyrgus',
      'ranges': [{'series': 'Ordovician'}],
      'children': [{**child, 'material': [{'label': 'A', 'context': 'x'}]}],
    },
    18,
  )
  assert derived(linked_only, 'occurrences') is None

  # Only taxonomy trees are counted: a cladogram's nodes print no material,
  # so a root of that type contributes none and cannot make a kind `partly`.
  taxonomy = tree({'taxon': 'rhenopyrgus', 'children': [{**child, 'material': None}]}, 19)
  cladogram = Tree(
    {'taxon': 'rhenopyrgus', 'children': [other]},
    {**base, 'type': 'cladogram', 'position': 20},
  )
  assert derived_coverage({'s': [taxonomy, cladogram]})['s']['material'] == 'all'
  assert derived_coverage({'s': [cladogram]})['s']['material'] is None


def test_derived_synonymy_coverage():
  base = {'source_key': '1961_dehm', 'type': 'taxonomy'}

  def derived(data, position, file_unused=(), tree_type='taxonomy'):
    root = Tree(
      data, {**base, 'type': tree_type, 'position': 100 + position, 'file_unused': file_unused}
    )
    return derived_coverage({'s': [root]})['s']['synonymy']

  child = {'taxon': 'grayae_bather_1915'}
  other = {'taxon': 'sardesoni_bather_1915'}
  syn = [{'taxon': 'sardesoni_bather_1915'}]
  # `unused: [synonyms]` is `na`, whatever the nodes say.
  assert derived({'taxon': 'rhenopyrgus'}, 0, file_unused=('synonyms',)) == 'na'
  # A null and values elsewhere, no node lacking both fields: `all`.
  nulled_root = {'taxon': 'rhenopyrgus', 'synonyms': None, 'children': [{**child, 'synonyms': syn}]}
  assert derived(nulled_root, 1) == 'all'
  # A null and a node lacking both fields: `partly` (every rank counts).
  partly_child = {'taxon': 'rhenopyrgus', 'children': [{**child, 'synonyms': None}, other]}
  assert derived(partly_child, 2) == 'partly'
  assert derived({'taxon': 'rhenopyrgus', 'synonyms': None, 'children': [child]}, 3) == 'partly'
  # `non` alone counts as present.
  non_root = {'taxon': 'rhenopyrgus', 'non': syn, 'children': [{**child, 'synonyms': None}]}
  assert derived(non_root, 4) == 'all'
  # Values alone declare nothing.
  assert derived({'taxon': 'rhenopyrgus', 'synonyms': syn, 'children': [child]}, 5) is None
  assert derived({'taxon': 'rhenopyrgus', 'non': syn}, 6) is None
  # A phylogeny root contributes nothing.
  assert derived({'taxon': 'rhenopyrgus', 'synonyms': None}, 7, tree_type='cladogram') is None
  taxonomy = Tree({'taxon': 'rhenopyrgus', 'synonyms': None}, {**base, 'position': 108})
  cladogram = Tree(
    {'taxon': 'rhenopyrgus', 'children': [other]}, {**base, 'type': 'cladogram', 'position': 109}
  )
  assert derived_coverage({'s': [taxonomy, cladogram]})['s']['synonymy'] == 'all'


def test_manifest_synonymy_keeps_the_count_check_unless_a_null_derives_it(monkeypatch):
  from phylohist.loader.research import Source

  coverage = Source.get('1961_dehm')._data['audit']['coverage']
  # Declared `all`, no null: nothing derived, and no acceptance claims, so
  # the claim-count check fires.
  monkeypatch.setitem(coverage, 'synonymy', 'all')
  values = {
    '1961_dehm': [
      Tree(
        {'taxon': 'pyrgocystis', 'children': [{'taxon': 'grayae_bather_1915'}]},
        {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 30},
      )
    ]
  }
  entry = manifest(extract(values), values)['sources']['1961_dehm']
  assert entry['derivedCoverage']['synonymy'] is None
  assert entry['coverage']['synonymy'] == 'all'
  assert 'synonymy: declared all, no claims derived' in entry['inconsistencies']

  # A null derives the kind: the derived value wins, and the declaration
  # is compared with it instead of with the claim count.
  nulled = {
    '1961_dehm': [
      Tree(
        {'taxon': 'pyrgocystis', 'synonyms': None, 'children': [{'taxon': 'grayae_bather_1915'}]},
        {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 31},
      )
    ]
  }
  entry = manifest(extract(nulled), nulled)['sources']['1961_dehm']
  assert entry['derivedCoverage']['synonymy'] == 'partly'
  assert entry['coverage']['synonymy'] == 'partly'
  assert (
    'synonymy: declared all but derived from the tree (partly); remove the declaration'
  ) in entry['inconsistencies']
  assert not [r for r in entry['inconsistencies'] if r.startswith('synonymy: declared all, no')]


def test_manifest_reports_derived_disagreement(load_records, monkeypatch):
  # A declared value that the file's nulls contradict is an inconsistency
  # row naming both, and the effective map carries the derived label.
  from phylohist.loader.research import Source

  audited = Tree(
    {
      'taxon': 'pyrgocystis',
      'children': [
        {'taxon': 'grayae_bather_1915', 'illustrations': None},
        {'taxon': 'sardesoni_bather_1915'},
      ],
    },
    {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 0},
  )
  synthetic = {'1961_dehm': [audited]}
  assert derived_coverage(synthetic)['1961_dehm']['illustrations'] == 'partly'
  monkeypatch.setitem(Source.get('1961_dehm')._data['audit']['coverage'], 'illustrations', 'none')

  entry = manifest(extract(synthetic), synthetic)['sources']['1961_dehm']
  assert (
    'illustrations: declared none but derived from the tree (partly); remove the declaration'
  ) in entry['inconsistencies']
  assert entry['coverage']['illustrations'] == 'partly'
  assert entry['derivedCoverage']['illustrations'] == 'partly'

  # Agreeing values still draw the row: the tree gives the kind its
  # coverage, so the declaration is redundant.
  monkeypatch.setitem(Source.get('1961_dehm')._data['audit']['coverage'], 'illustrations', 'partly')
  entry = manifest(extract(synthetic), synthetic)['sources']['1961_dehm']
  assert (
    'illustrations: declared partly but derived from the tree (partly); remove the declaration'
  ) in entry['inconsistencies']
  monkeypatch.setitem(Source.get('1961_dehm')._data['audit']['coverage'], 'illustrations', 'none')

  # A value alone derives nothing, so the declaration stands and no row fires.
  values_only = {
    '1961_dehm': [
      Tree(
        {'taxon': 'pyrgocystis', 'illustrations': [{'plate': 1}]},
        {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 1},
      )
    ]
  }
  entry = manifest(extract(values_only), values_only)['sources']['1961_dehm']
  assert entry['derivedCoverage']['illustrations'] is None
  assert entry['coverage']['illustrations'] == 'none'
  assert not [r for r in entry['inconsistencies'] if r.startswith('illustrations')]


# -- absence claims and `figured: False` --------------------------------------

_BASE = {'source_key': '1961_dehm', 'type': 'taxonomy'}
_SPECIES = 'grayae_bather_1915'
_SISTER = 'sardesoni_bather_1915'


def _claims_of(data, position, **metadata):
  root = Tree(data, {**_BASE, 'position': position, **metadata})
  return extract({'1961_dehm': [root]})['1961_dehm']


def _absences(claims):
  return [(c['absenceOf'], c['fields']) for c in claims if c['kind'] == 'absence']


def test_absence_emission_by_kind():
  def absences(node, position, **metadata):
    return _absences(_claims_of({'taxon': _SPECIES, **node}, position, **metadata))

  assert absences({'material': None}, 200) == [('material', ['material'])]
  assert absences({'illustrations': None}, 201) == [('illustrations', ['illustrations'])]
  assert absences({'synonyms': None}, 202) == [('synonymy', ['synonyms'])]
  assert absences({'contexts': None, 'ranges': None}, 203) == [
    ('occurrences', ['contexts', 'ranges'])
  ]
  assert absences({'ranges': None}, 204) == [('occurrences', ['ranges'])]
  # A value for either field, or a material entry linked to a context,
  # says the node has occurrences.
  assert absences({'contexts': None, 'ranges': [{'series': 'Ordovician'}]}, 205) == []
  linked = {'contexts': None, 'material': [{'label': 'A', 'context': 'x'}]}
  assert absences(linked, 206, file_contexts={'x': {'unit': ['a']}}) == []
  # Absent fields and values say nothing.
  assert absences({}, 207) == []
  assert absences({'material': [{'label': 'A'}], 'synonyms': [{'taxon': _SISTER}]}, 208) == []
  # All four, in the fixed order, whatever the order written.
  everything = {
    'synonyms': None,
    'illustrations': None,
    'ranges': None,
    'material': None,
  }
  assert [kind for kind, _ in absences(everything, 209)] == [
    'material',
    'occurrences',
    'illustrations',
    'synonymy',
  ]


def test_absence_is_emitted_at_any_rank_and_never_on_a_cited_entry():
  genus = _claims_of({'taxon': 'rhenopyrgus', 'material': None}, 210)
  assert _absences(genus) == [('material', ['material'])]
  cited = _claims_of(
    {'taxon': _SPECIES, 'synonyms': [{'taxon': _SISTER, 'synonyms': None, 'material': None}]},
    211,
  )
  assert _absences(cited) == []


def test_absence_claim_shape_and_effect_on_ids():
  data = {'taxon': _SPECIES, 'pages': 7, 'notes': 'n', 'material': [{'label': 'A'}]}
  plain = _claims_of(data, 212)
  nulled = _claims_of({**data, 'ranges': None, 'synonyms': None}, 213)
  absences = [c for c in nulled if c['kind'] == 'absence']
  assert [c['id'] for c in absences] == [
    '1961_dehm:213:absence:0',
    '1961_dehm:213:absence:1',
  ]
  first = absences[0]
  assert first['absenceOf'] == 'occurrences' and first['fields'] == ['ranges']
  assert first['pages'] == 7 and first['notes'] == 'n' and first['subject'] == _SPECIES
  # No coverage kind: the claim is not counted under any.
  assert 'coverageKind' not in first['audit']

  def others(claims, position):
    return [c['id'].replace(f':{position}:', ':P:') for c in claims if c['kind'] != 'absence']

  assert others(plain, 212) == others(nulled, 213)
  entry = manifest({'1961_dehm': nulled}, {'1961_dehm': []})['sources']['1961_dehm']
  assert entry['claims']['absence'] == 2
  assert 'absence' not in entry['derived']


def test_unfigured_specimens_are_derived_only_when_illustrations_are_all(monkeypatch):
  from phylohist.loader.research import Source

  figured = {
    'taxon': _SPECIES,
    'material': [{'label': 'A'}, {'label': 'B'}],
    'illustrations': [{'plate': 1, 'of': 'A'}],
  }
  # A sister species whose figures are null makes the kind `all`.
  sister = {'taxon': _SISTER, 'illustrations': None}

  def specimens(species, position, with_sister=True, **metadata):
    children = [species, sister] if with_sister else [species]
    claims = _claims_of({'taxon': 'rhenopyrgus', 'children': children}, position, **metadata)
    return {
      c['label']: c.get('figured')
      for c in claims
      if c['kind'] == 'material' and c['materialKind'] == 'specimen' and c['subject'] == _SPECIES
    }

  assert specimens(figured, 220) == {'A': None, 'B': False}
  # `figured` is never set to True: a figured specimen has illustrationClaims.
  claims = _claims_of({'taxon': 'rhenopyrgus', 'children': [figured, sister]}, 221)
  by_label = {c['label']: c for c in claims if c.get('materialKind') == 'specimen'}
  assert 'illustrationClaims' in by_label['A'] and 'figured' not in by_label['A']

  # Not set when the source's figures are not entered in full.
  monkeypatch.setitem(Source.get('1961_dehm')._data['audit']['coverage'], 'illustrations', 'partly')
  assert specimens(figured, 222, with_sister=False) == {'A': None, 'B': None}
  monkeypatch.undo()

  # Not set with an untied figure on the node: it may show the specimen.
  untied = {**figured, 'illustrations': [{'plate': 1, 'of': 'A'}, {'plate': 2}]}
  assert specimens(untied, 223) == {'A': None, 'B': None}
  # Not set when the node does not carry `illustrations` at all.
  assert specimens({k: v for k, v in figured.items() if k != 'illustrations'}, 224) == {
    'A': None,
    'B': None,
  }
  # A null on the node is a value of the field: every entry is unfigured.
  assert specimens({**figured, 'illustrations': None}, 225) == {'A': False, 'B': False}


def test_a_number_inside_a_run_names_its_entry_for_figured():
  node = {
    'taxon': _SPECIES,
    'material': [{'catalogNumbers': [['GSC 100', 'GSC 105']]}, {'label': 'B'}],
    'illustrations': [{'plate': 1, 'of': 'GSC 103'}],
  }
  sister = {'taxon': _SISTER, 'illustrations': None}
  claims = _claims_of({'taxon': 'rhenopyrgus', 'children': [node, sister]}, 226)
  specimens = [
    c for c in claims if c.get('materialKind') == 'specimen' and c['subject'] == _SPECIES
  ]
  assert [c.get('figured') for c in specimens] == [None, False]


def test_a_figured_role_or_a_figured_cast_is_never_unfigured():
  sister = {'taxon': _SISTER, 'illustrations': None}

  def figured(node, position):
    claims = _claims_of({'taxon': 'rhenopyrgus', 'children': [node, sister]}, position)
    return {
      c['label']: c.get('figured')
      for c in claims
      if c.get('materialKind') == 'specimen' and c['subject'] == _SPECIES
    }

  # The source calls the entry a figured specimen, whatever the figures say.
  node = {
    'taxon': _SPECIES,
    'material': [{'label': 'A', 'role': 'figured'}, {'label': 'B'}],
    'illustrations': [{'plate': 1, 'of': 'B'}],
  }
  assert figured(node, 227) == {'A': None, 'B': None}
  assert figured({**node, 'illustrations': None}, 228) == {'A': None, 'B': False}
  # A figure of a cast shows its original; the cast's own entry is figured by it.
  cast = {
    'taxon': _SPECIES,
    'material': [{'label': 'A'}, {'label': 'B', 'castOf': 'A'}, {'label': 'C'}],
    'illustrations': [{'plate': 1, 'of': 'B'}],
  }
  assert figured(cast, 229) == {'A': None, 'B': None, 'C': False}
  # An unfigured cast leaves its original unfigured, and so does a figure
  # of another entry.
  unfigured_cast = {**cast, 'illustrations': [{'plate': 1, 'of': 'C'}]}
  assert figured(unfigured_cast, 230) == {'A': False, 'B': False, 'C': None}
  # The cast is found by a catalog number or a run as a figure's `of` is.
  numbered = {
    'taxon': _SPECIES,
    'material': [
      {'catalogNumbers': ['GSC 100']},
      {'catalogNumbers': ['GSC 101'], 'castOf': 'GSC 100'},
    ],
    'illustrations': [{'plate': 1, 'of': 'GSC 101'}],
  }
  claims = _claims_of({'taxon': 'rhenopyrgus', 'children': [numbered, sister]}, 231)
  assert [
    c.get('figured')
    for c in claims
    if c.get('materialKind') == 'specimen' and c['subject'] == _SPECIES
  ] == [None, None]


# -- holotype_conflicts (roadmap F5) ---------------------------------------------

_TAXON = 'navicula_whitehouse_1941'


def _claim(source, role='holotype', taxon=_TAXON, **fields):
  return {
    'id': f'{source}:{taxon}:{role}:{len(fields)}',
    'kind': 'material',
    'materialKind': 'specimen',
    'source': source,
    'subject': taxon,
    'role': role,
    **fields,
  }


def _conflicts(*claims):
  by_source = {}
  for claim in claims:
    by_source.setdefault(claim['source'], []).append(claim)
  return holotype_conflicts(by_source)


def test_one_specimen_under_two_printed_forms_is_no_conflict(load_records):
  first = _claim('1941_whitehouse', ids=['F. 5404'], joinKeys=['uq-f:5404'])
  second = _claim('2021_jell_sprinkle', ids=['UQF5404'], joinKeys=['uq-f:5404'])
  assert _conflicts(first, second) == []


def test_two_different_numbers_are_a_conflict_in_year_order(load_records):
  later = _claim('2021_jell_sprinkle', ids=['UQF 9'], joinKeys=['uq-f:9'])
  first = _claim('1941_whitehouse', ids=['F. 5404'], joinKeys=['uq-f:5404'])
  [row] = _conflicts(later, first)
  assert row['taxon'] == _TAXON
  assert row['holotypes'] == [
    {
      'source': '1941_whitehouse',
      'ids': ['F. 5404'],
      'joinKeys': ['uq-f:5404'],
      'claim': first['id'],
    },
    {
      'source': '2021_jell_sprinkle',
      'ids': ['UQF 9'],
      'joinKeys': ['uq-f:9'],
      'claim': later['id'],
    },
  ]


def test_a_later_lectotype_or_neotype_is_no_conflict(load_records):
  holotype = _claim('1941_whitehouse', ids=['F. 5404'], joinKeys=['uq-f:5404'])
  for role in ('lectotype', 'neotype'):
    later = _claim('2021_jell_sprinkle', role=role, ids=['UQF 9'], joinKeys=['uq-f:9'])
    assert _conflicts(holotype, later) == []
  # A source that designates a lectotype leaves the comparison whole, even
  # when it also reports the old holotype entry.
  report = _claim('2021_jell_sprinkle', ids=['UQF 9'], joinKeys=['uq-f:9'])
  assert _conflicts(holotype, later, report) == []


def test_an_uncertain_holotype_is_ignored(load_records):
  holotype = _claim('1941_whitehouse', ids=['F. 5404'], joinKeys=['uq-f:5404'])
  doubtful = _claim('2021_jell_sprinkle', ids=['UQF 9'], joinKeys=['uq-f:9'], uncertain=True)
  assert _conflicts(holotype, doubtful) == []
  # An uncertain lectotype does not excuse a conflict either.
  lectotype = _claim('2021_jell_sprinkle', role='lectotype', ids=['UQF 9'], uncertain=True)
  assert _conflicts(holotype, lectotype) == []


def test_other_roles_and_a_single_source_are_no_conflict(load_records):
  holotype = _claim('1941_whitehouse', ids=['F. 5404'], joinKeys=['uq-f:5404'])
  paratype = _claim('2021_jell_sprinkle', role='paratype', ids=['UQF 9'], joinKeys=['uq-f:9'])
  assert _conflicts(holotype, paratype) == []
  other = _claim('1941_whitehouse', ids=['F. 5405'], joinKeys=['uq-f:5405'], count=1)
  assert _conflicts(holotype, other) == []


def test_unnumbered_holotypes_are_compared_by_label_then_printed_ids(load_records):
  first = _claim('1941_whitehouse', label='the Taf. 2 fossil')
  same = _claim('2021_jell_sprinkle', label='the Taf. 2 fossil')
  assert _conflicts(first, same) == []
  [row] = _conflicts(first, _claim('2021_jell_sprinkle', label='the Taf. 3 fossil'))
  assert row['holotypes'][0]['joinKeys'] == [] and row['holotypes'][0]['label'] == first['label']
  # No join keys and no label: the printed ids, a range pair's endpoints included.
  ids = _claim('1941_whitehouse', ids=[['XX 1', 'XX 2']])
  assert _conflicts(ids, _claim('2021_jell_sprinkle', ids=['XX 2'])) == []
  [row] = _conflicts(ids, _claim('2021_jell_sprinkle', ids=['XX 3']))
  assert row['holotypes'][0]['ids'] == [['XX 1', 'XX 2']]


def test_the_manifest_reports_holotype_conflicts(claims, roots):
  # The real corpus: the function runs and the manifest carries what it returns.
  assert isinstance(holotype_conflicts(claims), list)
  assert manifest(claims, roots)['holotypeConflicts'] == holotype_conflicts(claims)
