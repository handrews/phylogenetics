"""The tools answer from the committed claim table.

`source_coverage` must return the declared value an uncaptured
question's gap block relies on; the resolver must fold the
typographical variation G10 names; `contents`, `history`, `gap` and the
rest must render what the worked examples say. CI proves `claims/`
current, so these tests read the committed files rather than
re-extracting.
"""

import os
import pathlib

import pytest
import yaml

from phylohist.tools import ClaimStore

QUESTIONS_PATH = pathlib.Path(__file__).parent.parent / 'eval' / 'questions.yaml'
with open(QUESTIONS_PATH) as fd:
  QUESTIONS = yaml.safe_load(fd)

pytestmark = pytest.mark.skipif(
  bool(os.getenv('PHYLOHIST_DRAFTS')),
  reason='the committed claim table covers data/ only',
)

UNCAPTURED = [q for q in QUESTIONS if q['class'] == 'uncaptured']


@pytest.fixture(scope='module')
def store():
  return ClaimStore()


@pytest.mark.parametrize('question', UNCAPTURED, ids=[q['id'] for q in UNCAPTURED])
def test_source_coverage_backs_refusals(question, store):
  # An uncaptured question expects a gap block; the source must declare
  # that kind none or partly, or have no tree entered.
  spec = question['expected']['blocks']
  alternatives = spec['anyOf'] if isinstance(spec, dict) else [spec]
  gaps = [
    b for alt in alternatives for b in alt if b['tool'] == 'gap' and b['parameters'].get('kind')
  ]
  assert gaps, question['id']
  for gap in gaps:
    coverage = store.source_coverage(gap['parameters']['source'])
    assert coverage['known']
    if not coverage['entered']:
      continue
    declared = (coverage['audit'].get('coverage') or {}).get(gap['parameters']['kind'])
    assert declared in ('none', 'partly'), (question['id'], gap['parameters'], declared)


def test_unentered_source(store):
  coverage = store.source_coverage('1897_whiteaves')
  assert coverage['known'] and not coverage['entered']
  assert coverage['cite'] == 'Whiteaves 1897'
  assert store.source_coverage('1930_richter.r')['entered'] is False
  assert store.source_coverage('no_such_source') == {
    'source': 'no_such_source',
    'known': False,
  }


@pytest.mark.parametrize(
  'query, expected',
  [
    ('Palæaster', 'palaeaster'),
    ('Palaeaster', 'palaeaster'),
    ('Echino-encrinites', 'echinoencrinites'),
    ('echinoencrinites', 'echinoencrinites'),
    ('Astrocystites', 'astrocystites'),
    ('Rhenopyrgus grayae', 'grayae_bather_1915'),
    ('Edrioaster bigsbyi', 'bigsbyi_billings_1857'),
  ],
)
def test_resolve_folds_variation(store, query, expected):
  keys = [c['key'] for c in store.resolve_name(query)]
  assert expected in keys, (query, keys)


def test_resolve_ranks_and_kinds(store):
  genus = store.resolve_name('Rhenopyrgus', rank='genus')
  subgenus = store.resolve_name('Rhenopyrgus', rank='subgenus')
  assert [c['key'] for c in genus] == ['rhenopyrgus']
  assert [c['key'] for c in subgenus] == ['rhenopyrgus-subgenus']
  both = store.resolve_name('Rhenopyrgus')
  assert both[0]['key'] == 'rhenopyrgus', 'the most cited primary record first'
  assert both[0]['variants'] == ['rhenopyrgus-subgenus']
  assert 'sourcesWithStatements' in both[0] and 'sources' not in both[0]
  spelling = next(c for c in store.resolve_name('Palæaster') if c['key'] == 'palæaster')
  assert spelling['kind'] == 'altSpellingOf' and spelling['of'] == 'palaeaster'


def test_resolve_absent_is_empty(store):
  assert store.resolve_name('Rhenoblastus') == []
  assert store.resolve_name('') == []


def test_unnamed_records_are_not_found_by_name(store):
  # The words in a bin's key or an open-nomenclature designation name
  # other taxa; a prefix query must not sweep them in.
  assert all(c['name'] for c in store.resolve_name('eocrinoid'))
  assert store.resolve_name('Rhenopyrgus sp.') == []
  assert store.names['rhenopyrgus-sp-1_ewin_martin.m_isotalo_zamora_2020']['folded'] == []
  assert (
    store.name('rhenopyrgus-sp-1_ewin_martin.m_isotalo_zamora_2020') == 'Rhenopyrgus sp. indet. 1'
  )
  assert (
    store.name('edrioasteroidea-order-uncertain_holloway_jell_1983')
    == '[edrioasteroidea-order-uncertain_holloway_jell_1983]'
  )


def test_combinations_resolve(store):
  # A multi-word query is a combination as some source writes it; the
  # subgenus may be left out, and the subgenus itself is "Genus (Subgenus)".
  for query in (
    'Rhenopyrgus coronaeformis',
    'Pyrgocystis (Rhenopyrgus) coronaeformis',
    'Pyrgocystis coronaeformis',
    'Rhenopyrgus Coronaeformis',
  ):
    assert [c['key'] for c in store.resolve_name(query)] == ['coronaeformis_rievers_1961'], query
  assert [c['key'] for c in store.resolve_name('Pyrgocystis (Rhenopyrgus)')] == [
    'rhenopyrgus-subgenus'
  ]
  assert store.resolve_name('Astrocystites coronaeformis') == []


def test_names_accepted_where_keys_are(store):
  assert (
    store.history('Astrocystites ottawaensis', style='json')['blockId']
    == store.history('ottawaensis_whiteaves_1897', style='json')['blockId']
  )
  assert (
    store.descendants(['Pyrgocystis (Rhenopyrgus)'], style='json')['blockId']
    == store.descendants(['rhenopyrgus-subgenus'], style='json')['blockId']
  )
  # A bare epithet two species share cannot name one record; a genus name
  # that is itself a key (case aside) is not ambiguous.
  with pytest.raises(ValueError, match='casteri_bell.b.m_1975, casteri_sprinkle_1973'):
    store.history('casteri')
  assert store.history('Rhenopyrgus', style='json')['parameters']['record'] == 'rhenopyrgus'


def test_sources_by_citation(store):
  # A citation as the blocks print it resolves like a key; the year and
  # the authors named, in order, pick the paper.
  for query, key in (
    ('Dehm 1961', '1961_dehm'),
    ('Holloway & Jell 1983', '1983_holloway_jell'),
    ('Sumrall et al. 2013', '2013_sumrall_heredia_rodríguez.c.m_mestre'),
    ('Ewin, Martin, Isotalo & Zamora 2020', '2020_ewin_martin.m_isotalo_zamora'),
    ('Fay 1967a', '1967a_fay'),
    ('1983_holloway_jell', '1983_holloway_jell'),
    ('Sprinkle & Strimple in prep', 'inprep_sprinkle_strimple'),
    ('Holloway &amp; Jell 1983', '1983_holloway_jell'),
  ):
    assert [c['key'] for c in store.resolve_source(query)] == [key], query
  assert store.gap('Holloway & Jell 1983', 'material', style='json') == store.gap(
    '1983_holloway_jell', 'material', style='json'
  )
  assert (
    store.statements('rhenopyrgus', source='Dehm 1961', style='json')['parameters']['source']
    == '1961_dehm'
  )
  assert (
    store.contents('Guensburg & Sprinkle 1994', 'astrocystitidae')[0]['source']
    == '1994_guensburg_sprinkle'
  )
  with pytest.raises(ValueError, match='1816a_lamarck, 1816b_lamarck'):
    store.gap('Lamarck 1816', 'material')
  # A paper the corpus does not have passes through, so the gap can say so.
  assert store.resolve_source('Klug et al. 2008') == []
  assert (
    store.gap('Klug et al. 2008', 'newTaxa')['rendered']
    == 'No source in the corpus mentions the source Klug et al. 2008.'
  )
  assert (
    store.source_signature('2008_klug_krüger_korn_rücklin_schemm-gregory_debaets_mapes')['authors'][
      0
    ]
    == 'klug'
  )


def test_keys_accepted_in_any_case(store):
  assert store.contents('1983_Holloway_Jell', 'Rhenopyrgidae') == store.contents(
    '1983_holloway_jell', 'rhenopyrgidae'
  )
  assert (
    store.history('Rhenopyrgus', style='json')['blockId']
    == store.history('rhenopyrgus', style='json')['blockId']
  )
  assert (
    store.descendants(['Edrioblastoidea'], style='json')['blockId']
    == store.descendants(['edrioblastoidea'], style='json')['blockId']
  )
  assert store.gap('1983_HOLLOWAY_JELL', 'material', style='json') == store.gap(
    '1983_holloway_jell', 'material', style='json'
  )


def test_history_order_and_measurement(store):
  block = store.history('rhenopyrgus', style='json')
  sources = [e['source'] for e in block['entries']]
  assert sources == [
    '1961_dehm',
    '1966_regnéll',
    '1983_holloway_jell',
    '1994_guensburg_sprinkle',
    '2000_grigo',
    '2013_sumrall_heredia_rodríguez.c.m_mestre',
    '2020_ewin_martin.m_isotalo_zamora',
  ]
  with_clado = store.history('rhenopyrgus', trees=('taxonomy', 'cladogram'), style='json')
  assert '1990_smith.a.b_jell' in [e['source'] for e in with_clado['entries']]
  m = block['measurement']
  assert m['latestRank']['rank'] == 'genus' and m['latestRank']['firstYear'] == 1983
  assert m['ranks'][-1]['lastSource'] == '1966_regnéll'
  lines = store.history('rhenopyrgus')['rendered'].splitlines()
  assert lines[0] == 'Rhenopyrgus Dehm 1961: 7 papers, 7 co-author sets, 1961–2020'
  assert lines[1] == 'genus since 1983 (5 papers), subgenus 1961–1966 (2 papers)'
  assert (
    lines[2]
    == 'in Rhenopyrgidae / Rhenopyrginae since 1983 (5 papers), in Pyrgocystis 1961–1966 (2 papers)'
  )
  assert lines[4] == '1961  Dehm                  Pyrgocystis (Rhenopyrgus); named as new (p. 16)'
  alone = store.history('rhenopyrgus', include_related=False, style='json')
  assert '1961_dehm' not in [e['source'] for e in alone['entries']]


def test_contents_of_a_family_in_a_source(store):
  blocks = store.contents('1994_guensburg_sprinkle', 'astrocystitidae', synonymy=True)
  assert len(blocks) == 1
  keys = [n['key'] for n in blocks[0]['nodes']]
  assert keys == [
    'astrocystitidae',
    'astrocystites',
    'cambroblastus',
    'lampteroblastus',
    'hintzei_guensburg_sprinkle_1994',
  ]
  assert blocks[0]['rendered'] == (
    'Guensburg & Sprinkle 1994\n'
    '  Family Astrocystitidae emend.\n'
    '    Genus Astrocystites\n'
    '    Genus Cambroblastus\n'
    '    Genus Lampteroblastus gen. nov.\n'
    '      Type species. Lampteroblastus hintzei\n'
    '      Lampteroblastus hintzei sp. nov.'
  )
  every = store.contents(None, 'astrocystitidae')
  # The heading carries the page the listing starts on when it is recorded.
  assert (
    store.contents('2020_ewin_martin.m_isotalo_zamora', 'rhenopyrgidae')[0][
      'rendered'
    ].splitlines()[0]
    == 'Ewin et al. 2020, p. 118'
  )
  assert [b['source'] for b in every][:2] == ['1935_bassler', '1967a_fay']


def test_gap_sentences(store):
  assert store.gap('1983_holloway_jell', 'material')['rendered'] == (
    'The material printed in Holloway & Jell 1983 has not yet been entered '
    '(none of it is entered so far).'
  )
  assert store.gap('1897_whiteaves', 'newTaxa')['rendered'].startswith(
    'Whiteaves 1897 is on record; its content has not yet been entered'
  )
  assert store.gap('1962_fay', 'types')['rendered'] == (
    'Fay 1962 prints no type designations, as reviewed.'
  )
  assert store.gap('1994_guensburg_sprinkle', 'newTaxa')['rendered'] == (
    'The new taxa printed in Guensburg & Sprinkle 1994 are entered in full.'
  )


def test_statements_in_words(store):
  block = store.statements('rhenopyrgidae', kind='act', style='json')
  words = {e['sentence'] for e in block['entries']}
  assert 'named as new' in words and 'emended' in words
  new = store.statements('rhenopyrgidae', act_kind='new', style='json')
  assert [e['source'] for e in new['entries']] == ['1983_holloway_jell']
  moved = store.statements('rhenopyrgidae', kind='rejection', style='json')
  assert moved['entries'][0]['sentence'] == 'declines a placement in Cyathocystidae'
  assert store.statements('no_such_key', style='json')['entries'] == []
  # Nothing of a kind about a record in a named source: the gap block, so
  # the answer is the source's coverage, not an empty list.
  gap = store.statements(
    'whitei_holloway_jell_1983', source='Holloway & Jell 1983', kind='material', style='json'
  )
  assert gap['type'] == 'statement' and gap['parameters']['kind'] == 'material'
  assert gap['parameters']['source'] == '1983_holloway_jell'
  assert store.statements('rhenopyrgus-subgenus', source='1961_dehm', kind='diagnosis')[
    'rendered'
  ] == (
    'Nothing about Pyrgocystis (Rhenopyrgus) Dehm 1961 is entered from Dehm 1961. '
    'The diagnoses printed in Dehm 1961 have not yet been entered (none of them is entered so far).'
  )
  # No kind asked: every kind of the source not fully entered is named,
  # since the record's statements may lie in any of them.
  whole = store.statements('octogona_richter.r_1930', source='Holloway & Jell 1983', style='json')
  assert whole['parameters']['also_kinds'] == [
    'synonymy',
    'material',
    'occurrences',
    'illustrations',
    'diagnoses',
  ]
  assert store.statements('octogona_richter.r_1930', source='Holloway & Jell 1983')['rendered'] == (
    'Nothing about Pyrgocystis octogona Richter 1930 is entered from Holloway & Jell 1983. '
    'The classification printed in Holloway & Jell 1983 is entered in full. '
    'Its synonymy is entered in part; its material, occurrences, illustrations and diagnoses '
    'have not yet been entered.'
  )
  assert store.statements('whitei_holloway_jell_1983', kind='diagnosis')['rendered'].endswith(
    '(none entered from any source)'
  )
  lines = store.statements('Rhenopyrgus viviani', kind='material')['rendered'].splitlines()
  assert lines[0] == 'Statements about Rhenopyrgus viviani Ewin et al. 2020'
  assert '  2020  Ewin et al.  holotypes: NHMUK EE16642 (pp. 120–122)' in lines
  assert '  2020  Ewin et al.  paratypes: NHMUK EE15752, EE15755 (pp. 120–122)' in lines


def test_rank_variants_linked(store):
  for key, base in (
    ('aristocystitidae-superfamily', 'aristocystitidae'),
    ('glyptocystitida-superfamily', 'glyptocystitidae'),
    ('eumorphocystoidea', 'eumorphocystidae'),
    ('lebetodiscidae', 'lebetodiscina'),
    ('pyrgocystinae', 'pyrgocystidae'),
    ('edrioasterina', 'edrioasteridae'),
    ('cyathocystinae', 'cyathocystidae'),
    ('henicocystinae', 'henicocystidae'),
    ('edrioblastoida', 'edrioblastoidea'),
  ):
    assert store.names[key].get('of') == base, key
  transl = store.statements('diploporita-class', act_kind='nomTransl', style='json')
  claim = store.by_id[transl['entries'][0]['claim']]
  assert claim['rankVariants'] == ['diploporita-order', 'diploporita-suborder']


def test_epithets_do_not_relate_records(store):
  # Two species called casteri in different genera are different names;
  # a gender or spelling variant is linked explicitly.
  assert store.related_keys('casteri_bell.b.m_1975') == []
  assert store.related_keys('asteria_linnaeus_1767') == []
  assert store.related_keys('angulosus_pander_1830') == ['angulosa_pander_1830']
  assert store.related_keys('edrioblastoidea') == ['edrioblastoida', 'edrioblastoidina']
  found = store.descendants(['edrioblastoidea'], style='json')
  assert [r['combination'] for r in found['rows'] if r['record'].startswith('casteri')] == [
    'Timeischytes casteri'
  ]
  above = store.descendants(['edrioasteroidea'], style='json')
  row = next(r for r in above['rows'] if r['record'] == 'septembrachiata_miller.s.a_dyer_1878')
  assert row['cells'][2][-1] == {
    'value': 'spelling variant of ' + store.display('septembrachiatus_miller.s.a_dyer_1878')
  }
  row = next(r for r in above['rows'] if r['record'] == 'edrioasterina')
  assert row['cells'][2][0]['value'].startswith('Guensburg & Sprinkle 1994')
  assert row['cells'][2][-1]['value'] == 'same name at another rank as Edrioasteridae'


def test_senior_synonym_and_designation_shown_as_combinations(store):
  under = store.descendants(['pyrgocystis'], style='json')
  procera = [r for r in under['rows'] if r['record'] == 'procera_aurivillius_1892']
  assert (
    procera[0]['cells'][2][-1]['value'] == 'Ewin et al. 2020: synonym of Rhenopyrgus sp. indet. 1'
  )
  indet = next(
    r for r in under['rows'] if r['record'] == 'rhenopyrgus-sp-1_ewin_martin.m_isotalo_zamora_2020'
  )
  assert indet['combination'] == 'Rhenopyrgus sp. indet. 1'
  listing = store.contents('2020_ewin_martin.m_isotalo_zamora', 'rhenopyrgus')[0]
  assert '    Rhenopyrgus sp. indet. 1\n' in listing['rendered'] + '\n'


def test_ancestors_are_chains_per_source(store):
  block = store.ancestors(['rhenopyrgus'], style='json')
  assert block['type'] == 'chains' and block['title'] == 'Above Rhenopyrgus Dehm 1961'
  assert block['decorations']['measure'] == '7 papers, 7 co-author sets, 1961–2020'
  chains = {e['source']: [n['label'] for n in e['chain']] for e in block['entries']}
  assert chains['1994_guensburg_sprinkle'] == [
    'Echinozoa',
    'Edrioasteroidea',
    'Edrioasterida',
    'Edrioblastoidina',
    'Cyathocystidae',
    'Rhenopyrginae',
    'Rhenopyrgus',
  ]
  assert chains['1961_dehm'] == ['Pyrgocystis', 'Pyrgocystis (Rhenopyrgus)']
  # A placeholder reads in the source's words, never as a key.
  assert chains['1983_holloway_jell'][1] == 'Order uncertain'
  lines = store.ancestors(['rhenopyrgus'])['rendered'].splitlines()
  assert lines[2].startswith('1961  Dehm ') and lines[2].endswith(
    'Pyrgocystis › Pyrgocystis (Rhenopyrgus)'
  )
  assert '[' not in store.ancestors(['rhenopyrgus'])['rendered']


def test_placed_under_states_first_and_last(store):
  block = store.placed_under('rhenopyrgus', 'edrioblastoidina', style='json')
  assert [e['source'] for e in block['entries']] == [
    '1994_guensburg_sprinkle',
    '2000_grigo',
    '2013_sumrall_heredia_rodríguez.c.m_mestre',
    '2020_ewin_martin.m_isotalo_zamora',
  ]
  assert block['decorations'] == {
    'measure': '4 papers, 4 co-author sets, 1994–2020',
    'span': 'first Guensburg & Sprinkle 1994, last Ewin et al. 2020',
  }
  assert [n['label'] for n in block['entries'][0]['chain']] == [
    'Cyathocystidae',
    'Rhenopyrginae',
    'Rhenopyrgus',
  ]
  text = store.placed_under('rhenopyrgus', 'edrioblastoidina')['rendered'].splitlines()
  assert (
    text[0] == 'Rhenopyrgus Dehm 1961 under Edrioblastoidina Fay 1962: '
    '4 papers, 4 co-author sets, 1994–2020'
  )
  assert text[1] == 'first Guensburg & Sprinkle 1994, last Ewin et al. 2020'
  # A recombined species ends each line in the combination that source uses.
  grayae = store.placed_under('Rhenopyrgus grayae', 'Edrioasteroidea', style='json')
  assert grayae['title'] == 'Rhenopyrgus grayae (Bather 1915) under Edrioasteroidea Billings 1858'
  assert [e['chain'][-1]['label'] for e in grayae['entries']] == [
    'Pyrgocystis grayae',
    'Rhenopyrgus grayae',
    'Rhenopyrgus grayae',
  ]
  assert store.placed_under('rhenopyrgus', 'blastoidea', style='json')['entries'] == []


def test_headings_name_the_combination_asked_for(store):
  assert store.heading('grayae_bather_1915') == 'Pyrgocystis grayae Bather 1915'
  assert (
    store.heading('grayae_bather_1915', 'Rhenopyrgus grayae') == 'Rhenopyrgus grayae (Bather 1915)'
  )
  assert store.heading('grayae_bather_1915', 'grayae') == 'grayae Bather 1915'
  assert store.heading('rhenopyrgus-subgenus') == 'Pyrgocystis (Rhenopyrgus) Dehm 1961'
  assert store.heading('edrioasteroidea-order-uncertain_holloway_jell_1983') == 'Order uncertain'
  assert store.original_combination('coronaeformis_rievers_1961') == 'Pyrgocystis coronaeformis'
  assert (
    store.original_combination('viviani_ewin_martin.m_isotalo_zamora_2020') == 'Rhenopyrgus viviani'
  )


def test_combinations_in_a_listing(store):
  dehm = store.contents('1961_dehm', 'pyrgocystis')[0]['rendered'].splitlines()
  assert dehm[0] == 'Dehm 1961'
  assert dehm[1] == '  Genus Pyrgocystis'
  assert dehm[2] == '    Type species. Pyrgocystis sardesoni'
  assert dehm[3] == '    Pyrgocystis sardesoni'
  # The source's own wording for the new subgenus, "Rhenopyrgus nov. subgen.".
  assert dehm[-3] == '    Subgenus Pyrgocystis (Rhenopyrgus) nov. subgen.'
  assert dehm[-2] == '      Type species. Pyrgocystis (Rhenopyrgus) coronaeformis'
  assert dehm[-1] == '      Pyrgocystis (Rhenopyrgus) coronaeformis'


def test_or_names_match_their_node(store):
  # Miller 1821 writes "Pentacrinites or Pentacrinus": the second name
  # matches wherever the node does.
  miller = [b for b in store.contents(None, 'pentacrinus') if b['source'] == '1821_miller.j.s']
  assert len(miller) == 1
  assert miller[0]['rendered'].splitlines()[1] == '  Genus Pentacrinites or Pentacrinus'
  assert '1821_miller.j.s' in store.placements(['pentacrinus'], style='json')['sourceKeys']
  lines = store.history('pentacrinus')['rendered'].splitlines()
  assert sum(1 for line in lines if line.startswith('1821  Miller')) == 1
  assert any(line.endswith('Pentacrinites or Pentacrinus, in Articulata') for line in lines)
  alone = store.history('pentacrinus', include_related=False)['rendered'].splitlines()
  assert any(
    line.startswith('1821  Miller') and 'Pentacrinus, in Articulata' in line for line in alone
  )


def test_recombined_species_are_separate_rows(store):
  block = store.descendants(['pyrgocystis', 'rhenopyrgus'], style='json')
  rows = {row['combination']: row for row in block['rows'] if row['record'] == 'grayae_bather_1915'}
  assert set(rows) == {'Pyrgocystis grayae', 'Rhenopyrgus grayae'}
  sources = {
    label: {v['source'] for v in row['cells'][2] if 'source' in v} for label, row in rows.items()
  }
  assert sources['Pyrgocystis grayae'] and sources['Rhenopyrgus grayae']
  assert not (sources['Pyrgocystis grayae'] & sources['Rhenopyrgus grayae'])
  assert 'Pyrgocystis (Rhenopyrgus) coronaeformis' in {row['combination'] for row in block['rows']}
  placed = store.placements(['grayae_bather_1915'], style='json')
  labels = [row['combination'] for row in placed['rows']]
  assert labels == ['Pyrgocystis grayae', 'Rhenopyrgus grayae']
  filled = [
    {placed['sourceKeys'][i] for i, cell in enumerate(row['cells'][2:]) if cell}
    for row in placed['rows']
  ]
  assert filled[0] and filled[1] and not (filled[0] & filled[1])
  # A cell shows the parent without a rank word, carries every claim at the
  # node, and marks a rejection the source states.
  block = store.placements(['rhenopyrgidae'], style='json')
  sumrall = block['sourceKeys'].index('2013_sumrall_heredia_rodríguez.c.m_mestre')
  cell = block['rows'][0]['cells'][2 + sumrall][0]
  assert cell['value'] == 'Edrioblastoidina; not Cyathocystidae'
  assert any(store.by_id[c]['kind'] == 'rejection' for c in cell['claims'])
  assert block['rows'][0]['cells'][1][0]['value'] == 'Family'
  assert (
    store.gap(name='Rhenoblastus')['rendered']
    == 'No source in the corpus mentions the name Rhenoblastus.'
  )
  assert store.gap('1983_holloway_jell', style='json')['parameters']['kind'] == 'skeleton'
  with pytest.raises(ValueError):
    store.gap()


def test_history_shows_the_name_as_used(store):
  block = store.history('rhenopyrgus-subgenus', include_related=False, style='json')
  assert all(e['line'].startswith('Pyrgocystis (Rhenopyrgus)') for e in block['entries'])
  grayae = store.history('grayae_bather_1915', style='json')
  assert grayae['title'] == 'Pyrgocystis grayae Bather 1915'
  assert (
    store.history('Rhenopyrgus grayae', style='json')['title'] == 'Rhenopyrgus grayae (Bather 1915)'
  )
  lines = [e['line'] for e in grayae['entries']]
  # The binomial states the genus; the position is the level above it.
  assert lines == [
    'Pyrgocystis grayae, in Agelacrinitidae',
    'Pyrgocystis grayae',
    'Rhenopyrgus grayae, in Rhenopyrgidae',
    'Rhenopyrgus grayae, in Rhenopyrgidae',
  ]
  assert (
    grayae['decorations']['positions']
    == 'in Rhenopyrgus since 1983 (2 papers), in Pyrgocystis 1935–1961 (2 papers)'
  )
  with_syn = store.history('grayae_bather_1915', synonymy=True, style='json')
  assert [len(e.get('synonymy') or ()) for e in with_syn['entries']] == [0, 0, 1, 5]


def test_resolver_lists_combinations(store):
  grayae = next(
    c for c in store.resolve_name('Rhenopyrgus grayae') if c['key'] == 'grayae_bather_1915'
  )
  labels = [x['label'] for x in grayae['combinations']]
  assert labels == ['Pyrgocystis grayae', 'Rhenopyrgus grayae']
  assert grayae['combinations'][1]['firstYear'] == 1983
  assert 'combinations' not in store.resolve_name('Rhenopyrgus', rank='genus')[0]


def test_variety_and_no_genus_fallback(store):
  labelled = []
  for key, row in store.names.items():
    if (row['rank'] or '').lower() != 'variety':
      continue
    for c in store.closure.placements_of.get(key, ()):
      if c['tree'] == 'taxonomy' and store.combination(c['source'], c['path']).get('genus'):
        labelled.append(store.display(key, c['source'], c['path']))
  assert labelled and all(' var.' in label for label in labelled)
  # A species listed straight under a family keeps its epithet or printed form.
  claim = next(
    c
    for c in store.closure.placements_of['angulosus_pander_1830']
    if c['source'] == '1968b_paul.c.r.c'
  )
  label = store.display('angulosus_pander_1830', claim['source'], claim['path'])
  printed = (store.by_id[claim['id']].get('printed') or {}).get('citedAs')
  assert label in ('angulosus', printed)


def test_printed_forms_fall_back_to_the_heading(store):
  # No verbatim form recorded in the source: the heading as its listing
  # is entered, marked as such, rather than nothing.
  block = store.printed_forms('rhenopyrginae', source='Guensburg & Sprinkle 1994', style='json')
  assert [e['kind'] for e in block['entries']] == ['heading']
  assert block['entries'][0]['printed'] == 'Subfamily Rhenopyrginae emend. nom. transl.'
  assert block['claims']
  assert (
    '(the heading as entered; no verbatim form is recorded)'
    in store.printed_forms('rhenopyrginae', source='Guensburg & Sprinkle 1994')['rendered']
  )
  verbatim = store.printed_forms('rhenopyrgus-subgenus', source='Dehm 1961', style='json')
  assert all(e.get('kind') != 'heading' for e in verbatim['entries'])


def test_type_species_marks_the_editor(store):
  listing = store.contents('1962_fay', 'astrocystites')[0]
  assert '  Type species. Astrocystites ottawaensis (editor)' in listing['rendered']
  fixed = store.contents('Dehm 1961', 'rhenopyrgus-subgenus')[0]
  assert 'Type species. ' in fixed['rendered'] and '(editor)' not in fixed['rendered']
