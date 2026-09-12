"""The tools answer from the committed claim table.

`statements` must hold, for every eval question with expected claims, a
claim matching each selector; `source_coverage` must return the declared
value a not-captured question relies on; the resolver must fold the
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

from .selectors import matches

QUESTIONS_PATH = (
  pathlib.Path(__file__).parent.parent / 'eval' / 'questions.yaml'
)
with open(QUESTIONS_PATH) as fd:
  QUESTIONS = yaml.safe_load(fd)

pytestmark = pytest.mark.skipif(
  bool(os.getenv('PHYLOHIST_DRAFTS')),
  reason='the committed claim table covers data/ only',
)

WITH_CLAIMS = [q for q in QUESTIONS if (q.get('expected') or {}).get('claims')]
NOT_CAPTURED = [
  q for q in QUESTIONS
  if (q.get('expected') or {}).get('refusal') == 'not-captured'
]


@pytest.fixture(scope='module')
def store():
  return ClaimStore()


@pytest.mark.parametrize('question', WITH_CLAIMS, ids=[q['id'] for q in WITH_CLAIMS])
def test_statements_answer(question, store):
  for selector in question['expected']['claims']:
    block = store.statements(selector['subject'], source=selector['source'], style='json')
    found = [store.by_id[row['claim']] for row in block['rows']]
    if not any(matches(selector, c) for c in found):
      pytest.fail(f"{question['id']}: statements returned no match for {selector}")


@pytest.mark.parametrize('question', NOT_CAPTURED, ids=[q['id'] for q in NOT_CAPTURED])
def test_source_coverage_backs_refusals(question, store):
  coverage = store.source_coverage(question['scope']['source'])
  assert coverage['known']
  if not coverage['entered']:
    return
  kind = question['expected']['coverageKind']
  declared = (coverage['audit'].get('coverage') or {}).get(kind)
  assert declared in ('none', 'partly'), (question['id'], kind, declared)


def test_unentered_source(store):
  coverage = store.source_coverage('1897_whiteaves')
  assert coverage['known'] and not coverage['entered']
  assert coverage['cite'] == 'Whiteaves 1897'
  assert store.source_coverage('1930_richter.r')['entered'] is False
  assert store.source_coverage('no_such_source') == {
    'source': 'no_such_source', 'known': False,
  }


@pytest.mark.parametrize('query, expected', [
  ('Palæaster', 'palaeaster'),
  ('Palaeaster', 'palaeaster'),
  ('Echino-encrinites', 'echinoencrinites'),
  ('echinoencrinites', 'echinoencrinites'),
  ('Astrocystites', 'astrocystites'),
  ('Rhenopyrgus grayae', 'grayae_bather_1915'),
  ('Edrioaster bigsbyi', 'bigsbyi_billings_1857'),
])
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


def test_history_order_and_measurement(store):
  block = store.history('rhenopyrgus', style='json')
  sources = [row['source'] for row in block['rows']]
  assert sources == [
    '1961_dehm', '1966_regnéll', '1983_holloway_jell',
    '1994_guensburg_sprinkle', '2000_grigo',
    '2013_sumrall_heredia_rodríguez.c.m_mestre',
    '2020_ewin_martin.m_isotalo_zamora',
  ]
  with_clado = store.history('rhenopyrgus', trees=('taxonomy', 'cladogram'), style='json')
  assert '1990_smith.a.b_jell' in [row['source'] for row in with_clado['rows']]
  m = block['measurement']
  assert m['latestRank']['rank'] == 'genus' and m['latestRank']['firstYear'] == 1983
  assert m['ranks'][-1]['lastSource'] == '1966_regnéll'
  header = store.history('rhenopyrgus')['rendered'].splitlines()
  assert header[1].startswith('latest rank: genus: 5 papers 1983–2020, 5 co-author sets')
  alone = store.history('rhenopyrgus', include_related=False, style='json')
  assert '1961_dehm' not in [row['source'] for row in alone['rows']]


def test_contents_of_a_family_in_a_source(store):
  blocks = store.contents('1994_guensburg_sprinkle', 'astrocystitidae', synonymy=True)
  assert len(blocks) == 1
  keys = [n['key'] for n in blocks[0]['nodes']]
  assert keys == ['astrocystitidae', 'astrocystites', 'cambroblastus',
                  'lampteroblastus', 'hintzei_guensburg_sprinkle_1994']
  assert blocks[0]['rendered'] == (
    'Astrocystitidae emend.\n  Astrocystites\n  Cambroblastus\n  Lampteroblastus*\n'
    '    hintzei* [type]'
  )
  every = store.contents(None, 'astrocystitidae')
  assert [b['source'] for b in every][:2] == ['1935_bassler', '1967a_fay']


def test_gap_sentences(store):
  assert store.gap('1983_holloway_jell', 'material')['rendered'] == (
    'The material printed in Holloway & Jell 1983 has not yet been entered '
    '(none of it is entered so far).'
  )
  assert store.gap('1897_whiteaves', 'newTaxa')['rendered'].startswith(
    'Whiteaves 1897 is on record; its content has not yet been entered')
  assert store.gap('1962_fay', 'types')['rendered'] == (
    'Fay 1962 prints no type designations, as reviewed.'
  )
  assert store.gap('1994_guensburg_sprinkle', 'newTaxa')['rendered'] == (
    'The new taxa printed in Guensburg & Sprinkle 1994 are entered in full.'
  )


def test_statements_in_words(store):
  block = store.statements('rhenopyrgidae', kind='act', style='json')
  words = {row['cells'][2][0]['value'] for row in block['rows']}
  assert 'named as new' in words and 'emended' in words
  new = store.statements('rhenopyrgidae', act_kind='new', style='json')
  assert [row['cells'][0][0]['source'] for row in new['rows']] == ['1983_holloway_jell']
  moved = store.statements('rhenopyrgidae', kind='rejection', style='json')
  assert moved['rows'][0]['cells'][2][0]['value'] == 'declines a placement in Cyathocystidae (Family)'
  assert store.statements('no_such_key', style='json')['rows'] == []


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
  claim = store.by_id[transl['rows'][0]['claim']]
  assert claim['rankVariants'] == ['diploporita-order', 'diploporita-suborder']
