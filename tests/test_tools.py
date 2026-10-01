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

from phylohist.evaluation import alternatives
from phylohist.render import node_label
from phylohist.store import ClaimStore

QUESTIONS_PATH = pathlib.Path(__file__).parent.parent / 'eval' / 'questions.yaml'
with open(QUESTIONS_PATH) as fd:
  QUESTIONS = yaml.safe_load(fd)

pytestmark = pytest.mark.skipif(
  bool(os.getenv('PHYLOHIST_DRAFTS')),
  reason='the committed claim table covers data/ only',
)

UNCAPTURED = [q for q in QUESTIONS if q['class'] == 'uncaptured']


@pytest.mark.parametrize('question', UNCAPTURED, ids=[q['id'] for q in UNCAPTURED])
def test_source_coverage_backs_refusals(question, store):
  # An uncaptured question expects a gap block; the source must declare
  # that kind none or partly, or have no tree entered.
  gaps = [
    b
    for alt in alternatives(question['expected'])
    for b in alt['blocks']
    if b['tool'] == 'gap' and b['parameters'].get('kind')
  ]
  assert gaps, question['id']
  for gap in gaps:
    coverage = store.source_coverage(gap['parameters']['source'])
    assert coverage['known']
    if not coverage['entered']:
      continue
    declared = coverage['coverage'].get(gap['parameters']['kind'])
    assert declared in ('none', 'partly'), (question['id'], gap['parameters'], declared)


def test_unentered_source(store):
  coverage = store.source_coverage('1898_bather')
  assert coverage['known'] and not coverage['entered']
  assert coverage['cite'] == 'Bather 1898'
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
  spelling = next(c for c in store.resolve_name('Agelacrinidae') if c['key'] == 'agelacrinidae')
  assert spelling['kind'] == 'altSpellingOf' and spelling['of'] == 'agelacrinitidae'


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
  assert store.gap('1898_bather', 'newTaxa')['rendered'].startswith(
    'Bather 1898 is on record; its content has not yet been entered'
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
  # No kind asked: every kind of the source not fully entered is named,
  # since the record's statements may lie in any of them.
  whole = store.statements('octogona_richter.r_1930', source='Holloway & Jell 1983', style='json')
  assert whole['parameters']['also_kinds'] == [
    'synonymy',
    'material',
    'occurrences',
    'illustrations',
  ]
  assert store.statements('octogona_richter.r_1930', source='Holloway & Jell 1983')['rendered'] == (
    'Nothing about Pyrgocystis octogona Richter 1930 is entered from Holloway & Jell 1983. '
    'The classification printed in Holloway & Jell 1983 is entered in full. '
    'Its synonymy is entered in part; its material, occurrences and illustrations '
    'have not yet been entered.'
  )
  lines = store.statements('Rhenopyrgus viviani', kind='material')['rendered'].splitlines()
  assert lines[0] == 'Statements about Rhenopyrgus viviani Ewin et al. 2020'
  assert '  2020  Ewin et al.  holotype: NHMUK EE16642 (pp. 120–122)' in lines
  assert (
    '  2020  Ewin et al.  paratype: NHMUK EE15752–NHMUK EE15755, MPEP 1126.1 (pp. 120–122)' in lines
  )


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


def test_lapsus_listed_but_not_a_synonym(store):
  # Bather 1914 notes Whiteaves's slip "Steganoblastus canadensis": the
  # synonymy shows it, the statements word it, the closure never follows it.
  [block] = store.synonymy('ottawaensis_whiteaves_1897', '1914c_bather')
  assert (
    '1898 Steganoblastus canadensis (in error for ottawaensis) Whiteaves 1898 p. 395'
    in block['rendered']
  )
  said = store.statements('canadensis_whiteaves_1898', source='1914c_bather')['rendered']
  assert 'in error for Steganoblastus ottawaensis' in said
  under = store.descendants(['steganoblastus'], style='json')
  assert 'canadensis_whiteaves_1898' not in {r['record'] for r in under['rows']}
  rows = store.placements(['ottawaensis_whiteaves_1897'], style='json')['rows']
  assert 'canadensis_whiteaves_1898' not in {r.get('record') for r in rows}


def test_corrected_form_is_a_synonym_without_a_synonymy(store):
  # Gill & Caster 1960 correct Placocystidae to Placocystitidae and print
  # no synonymy: the correction alone makes the one a synonym of the other.
  under = store.descendants(['placocystitidae'], style='json')
  row = next(r for r in under['rows'] if r['record'] == 'placocystidae')
  assert [v['value'] for v in row['cells'][2]] == ['Gill & Caster 1960: synonym of Placocystitidae']
  assert row['cells'][2][0]['claim'].endswith('/corrected:usage')
  without = store.descendants(['placocystitidae'], include_synonyms=False, style='json')
  assert 'placocystidae' not in {r['record'] for r in without['rows']}


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
  # The rank's abbreviation; the source's own "Rhenopyrgus nov. subgen." is
  # the printed-forms tool's.
  assert dehm[-3] == '    Subgenus Pyrgocystis (Rhenopyrgus) subgen. nov.'
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
  # A species listed straight under a family keeps its epithet: the corpus
  # invents no genus and shows no printed form there.
  claim = next(
    c
    for c in store.closure.placements_of['angulosus_pander_1830']
    if c['source'] == '1968b_paul.c.r.c'
  )
  assert store.display('angulosus_pander_1830', claim['source'], claim['path']) == 'angulosus'


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


def test_attribution_words_by_field(store):
  words = store.words.attribution_words
  assert words({'auth': ['bell.b.m'], 'year': 1974}) == 'Bell, 1974'
  assert words({'auth': ['bather'], 'in': ['bell.b.m'], 'year': 1976}) == 'Bather in Bell, 1976'
  assert words({'auth': ['Hall']}) == 'Hall'
  assert words({'year': 1899}) == '1899'
  assert words({}) == ''
  # The usage sentence names the printed attribution by field, then the
  # editor's reading of what is wrong with it.
  line = store.statements('isorophida', source='Bell 1975')['rendered'].splitlines()[1]
  assert line.endswith(
    'cites the name, attributed to Bell, 1974 (printed auth, year in error; read as Bell 1976)'
  )


def test_followed_acts_and_sensu_words(store):
  words = store.words
  assert words.act_words({'actKind': 'emended', 'by': '1968b_paul.c.r.c'}) == 'emended by Paul 1968'
  assert (
    words.act_words({'actKind': 'nomTransl', 'translatedFrom': 'rhenopyrgidae', 'byPages': 5})
    == 'nomen translatum from Rhenopyrgidae'
  )
  assert (
    words.act_words({'actKind': 'emended', 'by': '1968b_paul.c.r.c', 'byPages': [[697, 730]]})
    == 'emended by Paul 1968, p. 697–730'
  )
  assert (
    words.act_words({'actKind': 'substituted', 'substitutedFor': 'rhenopyrgidae'})
    == 'substituted for Rhenopyrgidae'
  )
  assert words.act_words({'actKind': 'nomNudum'}) == 'nomen nudum'
  comb = {'actKind': 'combNov', 'by': '1968b_paul.c.r.c'}
  assert words.act_words(comb) == 'new combination by Paul 1968'
  combined = {'key': 'grayae_bather_1915', 'name': 'grayae', 'acts': [{'act': 'combNov'}]}
  assert node_label(combined) == 'grayae comb. nov.'
  lapsus = {'actKind': 'lapsus', 'lapsusAs': 'canadensis_billings_1866'}
  assert words.act_words(lapsus) == 'printed by lapsus calami as canadensis'
  # A listing shows the slip beside the intended name, as it shows a move.
  node = {
    'key': 'ottawaensis_whiteaves_1897',
    'name': 'ottawaensis',
    'acts': [{'act': 'lapsus', 'words': words.act_words(lapsus)}],
  }
  assert node_label(node) == 'ottawaensis (printed by lapsus calami as canadensis)'
  usage = {'kind': 'usage', 'sensu': 'stricto', 'subject': 'crinoidea'}
  assert words.claim_words(usage) == 'cites the name sensu stricto'
  node = {'key': 'crinoidea', 'name': 'Crinoidea', 'rank': 'Class', 'sensu': 'stricto'}
  assert node_label(node).endswith('Crinoidea (s. s.)')


def test_material_words(store):
  claim_words = store.words.claim_words

  def material(kind, **fields):
    return claim_words({'kind': 'material', 'materialKind': kind, **fields})

  assert material('specimen', role='lectotype', ids=['GSC 752']) == 'lectotype: GSC 752'
  assert material('specimen', ids=[['GSC 100', 'GSC 105'], 'GSC 7']) == (
    'specimens: GSC 100–GSC 105, GSC 7'
  )
  assert material('specimen', label='the Bigsby specimen', role='syntype') == (
    'syntype: the Bigsby specimen'
  )
  assert material('specimen', count=5, role='paratype') == 'paratype: 5 specimens'
  assert (
    material(
      'specimen',
      ids=['XYZ 1'],
      repository='nhmuk',
      repositoryVia='explicit',
      preparation='latex cast',
      castOf='XYZ 2',
      contextKey='quarry',
      contextTentative=True,
    )
    == 'specimens: XYZ 1 (latex cast) cast of XYZ 2 [nhmuk] (quarry?)'
  )
  assert material('specimen', ids=['GSC 1'], repository='gsc', repositoryVia='prefix') == (
    'specimens: GSC 1'
  )
  assert (
    material(
      'occurrence',
      contextKey='quarry',
      occurrence={'stage': 'Telychian', 'unit': ['Cybèle Member'], 'localityNumbers': ['SH-1']},
    )
    == 'occurrence quarry: Telychian; Cybèle Member; SH-1'
  )
  assert material('occurrence', contextKey='bare', occurrence={'notes': 'none'}) == (
    'occurrence bare'
  )
  assert (
    material(
      'occurrence',
      contextKey='sh-1',
      occurrence={
        'period': 'Cambrian',
        'localSeries': 'Lower Cambrian',
        'localSeriesModifier': 'upper',
        'stage': 'Wuliuan',
        'stageModifier': 'lower',
        'biozoneRange': ['Olenellus', 'Bonnia'],
      },
    )
    == 'occurrence sh-1: lower Wuliuan; Cambrian; upper Lower Cambrian; Olenellus, Bonnia'
  )
  assert material('occurrence', occurrence={'localStageModifier': 'lower'}) == ('occurrence: lower')
  assert (
    material(
      'illustration',
      illustration={'plate': 2, 'figures': [[1, 4]], 'non': [6]},
      of=['GSC 752', 'GSC 753'],
      depicts='cast',
    )
    == 'illustration: pl. 2, fig. 1–4, non fig. 6 of GSC 752, GSC 753 (cast)'
  )
  assert material('illustration', illustration={'plate': 1, 'uncertain': True}) == (
    'illustration: pl. 1?'
  )
  assert (
    material(
      'range',
      range={'series': 'Ordovician', 'regions': ['Ottawa', {'value': 'Quebec', 'tentative': True}]},
    )
    == 'range: Ordovician; Ottawa, Quebec?'
  )
  assert (
    material('range', range={'stage': 'Wuliuan', 'stageModifier': 'lower', 'regions': ['China']})
    == 'range: lower Wuliuan; China'
  )
  assert material('range', range={}) == 'range'


def _rendered_lines(block):
  return block['rendered'].splitlines()


def test_absence_words_and_not_figured_in_statements(store):
  assert [
    store.words.claim_words({'kind': 'absence', 'absenceOf': k})
    for k in (
      'material',
      'occurrences',
      'illustrations',
      'synonymy',
    )
  ] == [
    'no specimens cited',
    'no locality or range given',
    'not figured',
    'no synonymy given',
  ]
  # A node that nulls its material answers a `specimens` question with the
  # auditor's statement, not with the source's coverage.
  block = store.statements('neglecta_hecker_1940', source='1973_sprinkle', kind='specimens')
  assert block['type'] == 'list'
  [line] = _rendered_lines(block)[1:]
  assert 'no specimens cited' in line and 'p. 127' in line
  [entry] = store.statements(
    'neglecta_hecker_1940', source='1973_sprinkle', kind='specimens', style='json'
  )['entries']
  assert entry['kind'] == 'absence' and entry['page'] == 127
  # The other kinds select their own absences, and `absence` all of them.
  # With no source named, `absence` still lists the claims as statements.
  every = store.statements('neglecta_hecker_1940', kind='absence')
  assert every['type'] == 'list'
  assert [line.rsplit('  ', 1)[-1] for line in _rendered_lines(every)[1:]] == [
    'Bockia neglecta: no specimens cited (p. 127)',
    'Bockia neglecta: no locality or range given (p. 127)',
    'Bockia neglecta: not figured (p. 127)',
  ]
  for kind, words in (
    ('occurrences', 'no locality or range given'),
    ('illustrations', 'not figured'),
    ('material', 'no specimens cited'),
  ):
    rendered = store.statements('neglecta_hecker_1940', source='1973_sprinkle', kind=kind)[
      'rendered'
    ]
    assert words in rendered, kind
  # An unfigured specimen says so; the holotype, which figures name, does not.
  lines = _rendered_lines(
    store.statements('hobbsi_sprinkle_1973', source='1973_sprinkle', kind='specimens')
  )
  assert any('MCZ 642 (not figured)' in line for line in lines)
  assert not [line for line in lines if 'holotype' in line and '(not figured)' in line]
  durhami = _rendered_lines(
    store.statements('durhami_sprinkle_1973', source='1973_sprinkle', kind='specimens')
  )
  assert not [line for line in durhami if 'holotype' in line and '(not figured)' in line]


def _states(block):
  """The rendered rows of a content table, runs of spaces folded."""
  return [' '.join(line.split()) for line in block['rendered'].splitlines()]


def test_absence_with_a_source_is_a_table_of_what_it_gives(store):
  from phylohist import blocks

  block = store.statements('durhami_sprinkle_1973', source='1973_sprinkle', kind='absence')
  assert block['type'] == 'table' and blocks.validate(block, store) == []
  assert _states(block) == [
    'Kinzercystis durhami Sprinkle 1973 in Sprinkle 1973 (p. 70)',
    'kind state',
    '----------- -----------',
    'specimens 3 entered',
    'occurrences 1 entered',
    'figures 12 entered',
    'synonymy not entered',
  ]
  assert block['parameters'] == {
    'record': 'durhami_sprinkle_1973',
    'source': '1973_sprinkle',
    'kind': 'absence',
    'act_kind': None,
  }
  specimens, occurrences, figures, synonymy = (row['cells'][1][0] for row in block['rows'])
  assert len(blocks._claims_of(specimens)) == 3
  assert len(blocks._claims_of(occurrences)) == 1 and len(blocks._claims_of(figures)) == 12
  assert blocks._claims_of(synonymy) == [] and 'claims' not in synonymy
  [node] = block['content']
  assert node['page'] == 70
  assert [(r['kind'], r['state'], r['basis'], r['count']) for r in node['rows']] == [
    ('specimens', 'entered', 'claims', 3),
    ('occurrences', 'entered', 'claims', 1),
    ('figures', 'entered', 'claims', 12),
    ('synonymy', 'notEntered', 'coverage', None),
  ]
  assert block['source'] == '1973_sprinkle' and block['cite'] == 'Sprinkle 1973'
  assert 'group' not in block['rows'][0]
  assert (
    '| specimens | 3 entered |'
    in store.statements(
      'durhami_sprinkle_1973', source='1973_sprinkle', kind='absence', style='markdown'
    )['rendered']
  )


def test_absence_table_rests_on_the_auditors_nulls(store):
  block = store.statements('neglecta_hecker_1940', source='1973_sprinkle', kind='absence')
  assert _states(block)[3:] == [
    'specimens none printed',
    'occurrences none printed',
    'figures none printed',
    'synonymy not entered',
  ]
  rows = block['content'][0]['rows']
  assert [(r['state'], r['basis']) for r in rows] == [
    ('none', 'null'),
    ('none', 'null'),
    ('none', 'null'),
    ('notEntered', 'coverage'),
  ]
  absences = [c['id'] for c in store.by_subject['neglecta_hecker_1940'] if c['kind'] == 'absence']
  assert len(absences) == 3 and block['claims'] == sorted(absences)
  assert [row['cells'][1][0]['claims'] for row in block['rows'][:3]] == [[a] for a in absences]


def test_absence_table_groups_a_record_by_node(store):
  block = store.statements('wanneri_foerste_1938', source='1973_sprinkle', kind='absence')
  assert block['title'] == 'Lepidocystis wanneri Foerste 1938 in Sprinkle 1973'
  assert [row['group'] for row in block['rows']] == ['Lepidocystis wanneri (p. 62)'] * 4 + [
    'Lepidocystis wanneri (p. 66)'
  ] * 4
  assert [len(node['rows']) for node in block['content']] == [4, 4]
  assert [node['page'] for node in block['content']] == [62, 66]
  assert '-- Lepidocystis wanneri (p. 66) --' in block['rendered']


def test_absence_table_leaves_out_species_level_kinds_above_species(store):
  # Specimens and figures are cited for species: a genus with neither gets
  # no row for them, and a genus that is figured keeps its figures row.
  bare = store.statements('lepidocystis', source='1973_sprinkle', kind='absence')
  assert [r['kind'] for r in bare['content'][0]['rows']] == ['occurrences', 'synonymy']
  figured = store.statements('gogia', source='1973_sprinkle', kind='absence')
  assert [(r['kind'], r['state']) for r in figured['content'][0]['rows']] == [
    ('occurrences', 'entered'),
    ('figures', 'entered'),
    ('synonymy', 'notEntered'),
  ]


def test_absence_table_reads_coverage_where_nothing_is_entered(store):
  # Billings 1857 prints no figures and no synonymy (`na`), and enters
  # everything Dehm 1961 prints of a synonymy (`all`): none is printed there.
  for source, record, kinds in (
    ('1857_billings', 'punctatus_billings_1854', {'figures', 'synonymy'}),
    ('1961_dehm', 'octogona_richter.r_1930', {'synonymy'}),
  ):
    block = store.statements(record, source=source, kind='absence')
    rows = {r['kind']: r for r in block['content'][0]['rows']}
    for kind in kinds:
      assert (rows[kind]['state'], rows[kind]['basis']) == ('none', 'coverage'), (source, kind)
    cells = {row['cells'][0][0]['value']: row['cells'][1][0] for row in block['rows']}
    assert all(
      cells[kind]['value'] == 'none printed' and 'claims' not in cells[kind] for kind in kinds
    )
  # A kind the source enters only in part, or has not reviewed, is not entered.
  block = store.statements('punctatus_billings_1854', source='1857_billings', kind='absence')
  assert store.sources['1857_billings']['coverage']['material'] not in ('all', 'na')
  assert block['content'][0]['rows'][0]['state'] == 'notEntered'


def test_absence_table_notes_an_incomplete_specimen_list(store):
  fresh = ClaimStore()
  [path] = fresh._record_paths('1973_sprinkle', 'durhami_sprinkle_1973')
  specimen = next(
    c for c in fresh._node_claims('1973_sprinkle', path) if c.get('materialKind') == 'specimen'
  )
  specimen['listComplete'] = False
  block = fresh.statements('durhami_sprinkle_1973', source='1973_sprinkle', kind='absence')
  assert _states(block)[3] == 'specimens 3 entered (list incomplete)'


def test_absence_with_no_node_in_the_source_is_still_the_gap(store):
  # Nothing about the record is in that source: the gap block, as before.
  block = store.statements('durhami_sprinkle_1973', source='1857_billings', kind='absence')
  assert block['type'] == 'statement' and block['kind'] == 'gap'
  assert block['rendered'].startswith(
    'Nothing about Kinzercystis durhami Sprinkle 1973 is entered from Billings 1857. '
  )


def test_gap_says_of_this_kind_when_the_record_is_in_the_source(store):
  block = store.statements('durhami_sprinkle_1973', source='1973_sprinkle', kind='acceptance')
  assert block['type'] == 'statement' and block['fields']['aboutOther'] is True
  assert block['rendered'] == (
    'Nothing of this kind about Kinzercystis durhami Sprinkle 1973 is entered from '
    'Sprinkle 1973. How much of the synonymy in Sprinkle 1973 is entered has not been reviewed.'
  )
  # A record with no claim in the source keeps the plain sentence.
  plain = store.statements(
    'octogona_richter.r_1930', source='1983_holloway_jell', kind='occurrences'
  )
  assert plain['rendered'].startswith(
    'Nothing about Pyrgocystis octogona Richter 1930 is entered from Holloway & Jell 1983.'
  )
  assert 'aboutOther' not in plain['fields']


def test_synonymy_says_a_source_gives_none(store):
  from phylohist import blocks
  from phylohist.render import render
  from phylohist.store import ClaimStore

  # Nothing nulls a synonymy in the corpus yet, so a store of its own gets
  # the auditor's `absence` claim added at a node that lists no synonymy.
  fresh = ClaimStore()
  [path] = fresh._record_paths('1973_sprinkle', 'neglecta_hecker_1940')
  claim = {
    'kind': 'absence',
    'absenceOf': 'synonymy',
    'fields': ['synonyms'],
    'id': f'1973_sprinkle:{path}:absence:9',
    'source': '1973_sprinkle',
    'path': path,
    'pages': 127,
    'subject': 'neglecta_hecker_1940',
  }
  fresh.at_path['1973_sprinkle'][path].append(claim)
  [block] = fresh.synonymy('neglecta_hecker_1940', source='1973_sprinkle')
  assert block['type'] == 'statement' and block['kind'] == 'none'
  assert block['claims'] == [claim['id']]
  assert block['fields']['what'] == 'synonymy' and block['fields']['page'] == 127
  assert block['rendered'] == 'Sprinkle 1973 gives no synonymy for Bockia neglecta (p. 127).'
  # No source named: as before, only sources with entries are listed.
  assert all(b['type'] == 'list' for b in fresh.synonymy('neglecta_hecker_1940'))
  # And the same statement without a page.
  bare = blocks.statement(
    'none',
    {
      'cite': 'Sprinkle 1973',
      'source': '1973_sprinkle',
      'what': 'synonymy',
      'about': 'X',
      'page': None,
    },
    {},
  )
  assert render(bare, 'text') == 'Sprinkle 1973 gives no synonymy for X.'
  assert store.synonymy('neglecta_hecker_1940', source='1973_sprinkle') == []


# -- open forms as they render from the corpus -------------------------------


def test_compared_form_is_not_marked_as_a_new_taxon(store):
  # A cf. or aff. node carries `new` because the source originates the
  # form; the listing must not print "sp. nov." after it.
  block = store.contents('1975_kolata', 'edrioaster', style='text')[0]
  lines = [line.strip() for line in block['rendered'].splitlines()]
  assert 'Edrioaster cf. bigsbyi' in lines
  block = store.contents('1960_gill_caster', 'victoriacystis', style='text')[0]
  lines = [line.strip() for line in block['rendered'].splitlines()]
  assert 'Victoriacystis aff. wilkinsi a' in lines and 'Victoriacystis aff. wilkinsi b' in lines
  # The named species beside them keeps its mark.
  assert 'Victoriacystis wilkinsi sp. nov.' in lines


def test_cited_open_form_reads_in_its_combination(store):
  # With the original genus given in `parents`, and without it.
  with_parents = store.synonymy('longidactylus_walcott_1886', source='1973_sprinkle', style='text')
  assert '1965 Gogia cf. longidactylus Robison, 1965' in with_parents[0]['rendered']
  without = store.synonymy(
    'flexibilis_parsley_prokop_2004', source='2004_parsley_prokop', style='text'
  )
  assert 'Stromatocystites aff. pentangularis Prokop, 1961' in without[0]['rendered']


def test_cited_combination_quotes_its_genus(store):
  # `quotedParent` on a synonymy entry puts the quotes on the genus the
  # entry's `parents` give; no entry in the corpus carries it yet.
  source, record = '1973_sprinkle', 'longidactylus_walcott_1886'
  path = store._record_paths(source, record)[0]
  entry_path = next(
    p
    for p, claims in store.at_path[source].items()
    if p.startswith(f'{path}/synonyms/')
    and any(c['kind'] == 'acceptance' and c.get('parents') == ['eocystites'] for c in claims)
  )
  acceptance = next(c for c in store.at_path[source][entry_path] if c['kind'] == 'acceptance')
  acceptance['quotedParent'] = True
  try:
    entries = store._synonymy_entries(source, path)
  finally:
    del acceptance['quotedParent']
  assert any(e.get('parents') == ['"Eocystites"'] for e in entries)
