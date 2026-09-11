"""The four tools answer from the committed claim table.

`claims_about` must return, for every eval question with expected claims,
a claim matching each selector; `source_coverage` must return the declared
value a not-captured question relies on; the resolver must fold the
typographical variation G10 names; `name_history` must order sources by
publication year and label related records. CI proves `claims/` current,
so these tests read the committed files rather than re-extracting.
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
def test_claims_about_answers(question, store):
  for selector in question['expected']['claims']:
    found = store.claims_about(selector['subject'], source=selector['source'])
    if not any(matches(selector, c) for c in found):
      pytest.fail(f"{question['id']}: claims_about returned no match for {selector}")


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
  spelling = next(c for c in store.resolve_name('Palæaster') if c['key'] == 'palæaster')
  assert spelling['kind'] == 'altSpellingOf' and spelling['of'] == 'palaeaster'


def test_resolve_absent_is_empty(store):
  assert store.resolve_name('Rhenoblastus') == []
  assert store.resolve_name('') == []


def test_name_history_order_and_related(store):
  history = store.name_history('rhenopyrgus')
  sources = [h['source'] for h in history]
  assert sources == [
    '1961_dehm', '1966_regnéll', '1983_holloway_jell', '1990_smith.a.b_jell',
    '1994_guensburg_sprinkle', '2000_grigo',
    '2013_sumrall_heredia_rodríguez.c.m_mestre',
    '2020_ewin_martin.m_isotalo_zamora',
  ]
  dehm = history[0]
  assert dehm['cite'] == 'Dehm 1961'
  assert all(p['record'] == 'rhenopyrgus-subgenus' for p in dehm['placements'])
  assert dehm['placements'][0]['recordRank'] == 'subgenus'
  assert any(a['act'] == 'new' for a in dehm['acts'])
  smith = next(h for h in history if h['source'] == '1990_smith.a.b_jell')
  assert smith['placements'][0]['tree'] == 'cladogram'
  alone = store.name_history('rhenopyrgus', include_related=False)
  assert '1961_dehm' not in [h['source'] for h in alone]


def test_claims_about_filters(store):
  acts = store.claims_about('rhenopyrgidae', kind='act')
  assert {a['actKind'] for a in acts} >= {'new', 'emended'}
  new = store.claims_about('rhenopyrgidae', act_kind='new')
  assert [c['source'] for c in new] == ['1983_holloway_jell']
  assert new[0]['sourceCitation'] == 'Holloway & Jell 1983'
  assert store.claims_about('no_such_key') == []
