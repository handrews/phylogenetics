"""A plan is data; code validates and executes it.

Validation rejects what the tool surface does not have; execution builds
the composition from the corpus, one tool call per block, and reports
what could not be built. Every eval question's expected blocks are a
plan that executes and shows its strings (the claims test covers that).
"""

import os

import pytest

from phylohist import plan
from phylohist.render import render_composition

pytestmark = pytest.mark.skipif(
  bool(os.getenv('PHYLOHIST_DRAFTS')),
  reason='the committed claim table covers data/ only',
)


def test_validate_rejects_what_the_tools_lack():
  bad = {'header': 'x', 'blocks': [
    {'tool': 'bogus', 'parameters': {}},
    {'tool': 'history', 'parameters': {'record': 'rhenopyrgus', 'colour': 'red'}},
    {'tool': 'contents', 'parameters': {'source': '1961_dehm'}},
    {'tool': 'resolve_name', 'parameters': {'query': 'x'}},
  ]}
  problems = plan.validate(bad)
  assert problems == [
    'block 1: unknown tool bogus',
    'block 2: history has no parameter colour',
    'block 3: contents needs record',
    'block 4: resolve_name answers a lookup, not a reader; it is not a block',
  ]
  assert plan.validate({'header': 'x', 'blocks': [{'tool': 'history', 'parameters': {'record': 'rhenopyrgus'}}]}) == []


def test_execute_builds_the_blocks_in_order():
  outcome = plan.execute({
    'header': 'Rhenopyrgidae under Cyathocystidae; all years',
    'blocks': [
      {'tool': 'placed_under', 'parameters': {'record': 'Rhenopyrgidae', 'parent': 'Cyathocystidae'}},
      {'tool': 'placements', 'parameters': {'records': ['rhenopyrgidae']}},
    ],
  })
  assert outcome['errors'] == []
  assert [b['tool'] for b in outcome['blocks']] == ['placed_under', 'placements']
  assert outcome['blocks'][0]['parameters']['record'] == 'rhenopyrgidae'
  text = render_composition(outcome['composition'], 'text')
  assert text.startswith('Rhenopyrgidae under Cyathocystidae; all years\n\n')
  assert 'first Guensburg & Sprinkle 1994, last Grigo 2000' in text
  assert text.index('first Guensburg') < text.index('Placements by source')


def test_execute_reports_what_it_cannot_build():
  outcome = plan.execute({'header': 'x', 'blocks': [
    {'tool': 'history', 'parameters': {'record': 'casteri'}},
    {'tool': 'gap', 'parameters': {'source': 'Lamarck 1816', 'kind': 'material'}},
    {'tool': 'gap', 'parameters': {'name': 'Rhenoblastus'}},
  ]})
  assert [e['block'] for e in outcome['errors']] == [1, 2]
  assert 'casteri_bell.b.m_1975' in outcome['errors'][0]['error']
  assert '1816a_lamarck' in outcome['errors'][1]['error']
  assert [b['tool'] for b in outcome['blocks']] == ['gap']
  assert outcome['composition']['blocks'][0]['type'] == 'statement'
  assert plan.execute({'header': 'x', 'blocks': [{'tool': 'bogus', 'parameters': {}}]})['composition'] is None
