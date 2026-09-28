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
  derived_material_coverage,
  extract,
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
    # A cited entry locates the cited work's own material (D1): even
    # though these ride on the node, they emit none of the four claims.
    'material': [{'catalogNumbers': ['GSC 1']}],
    'figures': [{'plate': 1, 'figures': [1]}],
    'contexts': {'somewhere': {'unit': ['Some Fm']}},
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
  # D1: contexts, material, figures, range, in that fixed emission order,
  # over a node with a file context, a node context (referenced and not),
  # a numbered entry, a range pair, a label-only entry, an explicit
  # repository, a tentative context and tied/untied figures.
  file_contexts = {
    'division-st': {'unit': ['Trenton Limestone'], 'location': ['Division Street, Ottawa']},
  }
  node_data = {
    'taxon': 'rhenopyrgus',
    'contexts': {'quarry-x': {'unit': ['Quarry X Beds']}},
    'material': [
      {'catalogNumbers': ['GSC 752'], 'role': 'syntype', 'context': 'division-st'},
      {'catalogNumbers': [['GSC 100', 'GSC 105']], 'role': 'paratype'},
      {'label': 'the specimen lent to Hudson', 'role': 'syntype', 'status': 'lost'},
      {'catalogNumbers': ['XYZ 1'], 'repository': 'NHMUK', 'role': 'paratype'},
      {
        'catalogNumbers': ['GSC 900'],
        'context': {'key': 'division-st', 'tentative': True},
        'role': 'hypotype',
      },
    ],
    'figures': [
      {'textFigures': [3], 'of': 'GSC 752'},
      {'plate': 1, 'figures': [2]},
    ],
    'range': {
      'series': 'Middle Ordovician',
      'regions': ['Ottawa', {'value': 'Quebec', 'tentative': True}],
    },
  }
  root = Tree(
    node_data,
    {
      'source_key': '1961_dehm',
      'type': 'taxonomy',
      'position': 90,
      'file_contexts': file_contexts,
      'file_unused': (),
    },
  )
  claims = extract({'1961_dehm': [root]})['1961_dehm']
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  material_claims = [c for c in claims if c['kind'] == 'material']

  # The fixed order fixes the ids: contexts, material, figures, range.
  assert [c['materialKind'] for c in material_claims] == [
    'occurrence',
    'occurrence',
    'specimen',
    'specimen',
    'specimen',
    'specimen',
    'specimen',
    'illustration',
    'illustration',
    'range',
  ]
  assert [c['id'] for c in material_claims] == [
    f'1961_dehm:90:material:{n}' for n in range(len(material_claims))
  ]

  # A file context referenced by the node, and a node's own context, each
  # emitted once, with their scope.
  file_ctx, node_ctx = material_claims[0], material_claims[1]
  assert file_ctx['contextKey'] == 'division-st' and file_ctx['contextScope'] == 'file'
  assert file_ctx['occurrence'] == file_contexts['division-st']
  assert node_ctx['contextKey'] == 'quarry-x' and node_ctx['contextScope'] == 'node'
  assert node_ctx['occurrence'] == node_data['contexts']['quarry-x']

  numbered, range_pair, label_only, explicit_repo, tentative = material_claims[2:7]

  assert numbered['catalogNumbers'] == ['GSC 752']
  assert numbered['contextKey'] == 'division-st' and 'contextTentative' not in numbered
  assert numbered['repository'] == 'GSC' and numbered['repositoryVia'] == 'registry'
  assert numbered['joinKeys'] == ['GSC:gsc752'] and 'rangeJoin' not in numbered

  assert range_pair['catalogNumbers'] == [['GSC 100', 'GSC 105']]
  assert range_pair['repository'] == 'GSC' and range_pair['repositoryVia'] == 'registry'
  assert range_pair['joinKeys'] == ['GSC:gsc100', 'GSC:gsc105']
  assert range_pair['rangeJoin'] is True

  assert label_only['label'] == 'the specimen lent to Hudson'
  assert label_only['status'] == 'lost' and label_only['ids'] == []
  assert 'repository' in label_only and label_only['repository'] is None
  assert 'joinKeys' not in label_only

  assert explicit_repo['repository'] == 'NHMUK' and explicit_repo['repositoryVia'] == 'explicit'
  assert explicit_repo['joinKeys'] == ['NHMUK:xyz1']

  assert tentative['contextKey'] == 'division-st' and tentative['contextTentative'] is True

  # Not a protologue node: no entry derives a `roleAct` (see the separate
  # protologue node below for that derivation).
  no_role_act = (numbered, range_pair, label_only, explicit_repo, tentative)
  assert all('roleAct' not in c for c in no_role_act)

  tied, untied = material_claims[7:9]
  assert tied['illustration'] == {'textFigures': [3]} and tied['of'] == 'GSC 752'
  assert tied['ofClaim'] == numbered['id']
  assert numbered['figureClaims'] == [tied['id']]
  assert 'ofClaim' not in untied and 'specimenIllustrations' not in range_pair

  range_claim = material_claims[9]
  assert range_claim['range'] == node_data['range']

  # Protologue roleAct (D2), on a `new: true` node: a holotype/paratype/
  # syntype entry is this source's designation by definition unless it
  # states its own `roleAct` (the entry's own value wins), and a role
  # outside that set (here, hypotype) gets none. A placeholder taxon
  # (`openTaxon`) sidesteps the protologue-source check `taxon` would need.
  count_node = Tree(
    {
      'openTaxon': 'rhenopyrgus-sp-1_ewin_martin.m_isotalo_zamora_2020',
      'new': True,
      'material': [
        {'count': 5, 'role': 'paratype', 'roleAct': 'reported'},
        {'catalogNumbers': ['GSC 1'], 'role': 'holotype'},
        {'catalogNumbers': ['GSC 2'], 'role': 'hypotype'},
      ],
    },
    {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 91},
  )
  count_claims = [
    c for c in extract({'1961_dehm': [count_node]})['1961_dehm'] if c['kind'] == 'material'
  ]
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  reported, holotype, hypotype = count_claims
  assert reported['count'] == 5 and reported['roleAct'] == 'reported'
  assert holotype['roleAct'] == 'designated'
  assert 'roleAct' not in hypotype


def test_derived_material_coverage():
  base = {'source_key': '1961_dehm', 'type': 'taxonomy'}

  def tree(data, position, file_unused=()):
    return Tree(data, {**base, 'position': position, 'file_unused': file_unused})

  # `na`: the file lists the field(s) as unused, whatever the nodes say.
  na_root = tree({'taxon': 'rhenopyrgus'}, 0, file_unused=('material',))
  assert derived_material_coverage({'s': [na_root]})['s']['material'] == 'na'

  # `all`: no primary, non-cited, named node lacks the field (value or null).
  all_root = tree(
    {
      'taxon': 'rhenopyrgus',
      'material': [{'label': 'A'}],
      'children': [{'taxon': 'grayae_bather_1915', 'material': None}],
    },
    1,
  )
  assert derived_material_coverage({'s': [all_root]})['s']['material'] == 'all'

  # `all` downgraded to `partly` when a material entry is not list-complete.
  partial_list_root = tree(
    {
      'taxon': 'rhenopyrgus',
      'material': [{'label': 'A', 'listComplete': False}],
      'children': [{'taxon': 'grayae_bather_1915', 'material': None}],
    },
    2,
  )
  assert derived_material_coverage({'s': [partial_list_root]})['s']['material'] == 'partly'

  # `partly`: some nodes have it, some do not.
  mixed_root = tree(
    {
      'taxon': 'rhenopyrgus',
      'material': [{'label': 'A'}],
      'children': [{'taxon': 'grayae_bather_1915'}],
    },
    3,
  )
  assert derived_material_coverage({'s': [mixed_root]})['s']['material'] == 'partly'

  # Nothing declared at all (no unused, no node with a value or a null):
  # `None`, so the effective value falls back to the declared coverage.
  none_root = tree({'taxon': 'rhenopyrgus'}, 4)
  assert derived_material_coverage({'s': [none_root]})['s']['material'] is None

  # `occurrences` reads either `contexts` or `range`.
  occ_root = tree(
    {
      'taxon': 'rhenopyrgus',
      'range': {'series': 'Ordovician'},
      'children': [{'taxon': 'grayae_bather_1915', 'contexts': None}],
    },
    5,
  )
  assert derived_material_coverage({'s': [occ_root]})['s']['occurrences'] == 'all'

  # A cited entry (here, a `synonyms` entry) never counts, whatever it carries.
  cited_root = tree(
    {
      'taxon': 'rhenopyrgus',
      'material': None,
      'synonyms': [{'taxon': 'grayae_bather_1915', 'material': [{'label': 'not counted'}]}],
    },
    6,
  )
  assert derived_material_coverage({'s': [cited_root]})['s']['material'] == 'all'


def test_manifest_reports_derived_disagreement(load_records, roots, monkeypatch):
  # A declared value the derived claims contradict (G11) is an
  # inconsistency row naming both, and the effective map still prefers
  # the derived label over the (now wrong) declared one.
  from phylohist.loader.research import Source

  source = Source.get('1961_dehm')
  derived = derived_material_coverage(roots)['1961_dehm']
  assert derived['illustrations'] == 'partly'  # real data, checked once here
  monkeypatch.setitem(source._data['audit']['coverage'], 'illustrations', 'none')

  claims = extract(roots)
  entry = manifest(claims, roots)['sources']['1961_dehm']
  assert 'illustrations: declared none, derived partly' in entry['inconsistencies']
  assert entry['coverage']['illustrations'] == 'partly'
  assert entry['derivedCoverage']['illustrations'] == 'partly'
