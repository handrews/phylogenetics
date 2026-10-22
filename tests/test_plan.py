"""A plan is data; code validates and executes it.

Validation rejects what the tool surface does not have; execution builds
the composition from the corpus, one tool call per block, and reports
what could not be built. Every eval question's expected blocks are a
plan that executes and shows its strings (the claims test covers that).
"""

import pytest

from phylohist import plan, tools
from phylohist.render import render_composition


def test_validate_rejects_what_the_tools_lack():
  bad = {
    'header': 'x',
    'blocks': [
      {'tool': 'bogus', 'parameters': {}},
      {'tool': 'history', 'parameters': {'record': 'rhenopyrgus', 'colour': 'red'}},
      {'tool': 'contents', 'parameters': {'source': '1961_dehm'}},
      {'tool': 'resolve_name', 'parameters': {'query': 'x'}},
      {'tool': 'history', 'parameters': {'record': 'rhenopyrgus', 'years': True}},
    ],
  }
  problems = plan.validate(bad)
  assert problems[:4] == [
    'block 1: unknown tool bogus',
    'block 2: history has no parameter colour',
    'block 3: contents needs record',
    'block 4: resolve_name answers a lookup, not a reader; it is not a block',
  ]
  assert problems[4].startswith(
    'block 5: history years must be a list ([first, last] publication years'
  )
  assert (
    plan.validate(
      {
        'header': 'x',
        'blocks': [
          {'tool': 'history', 'parameters': {'record': 'rhenopyrgus', 'years': [1990, None]}}
        ],
      }
    )
    == []
  )
  assert (
    plan.validate(
      {'header': 'x', 'blocks': [{'tool': 'history', 'parameters': {'record': 'rhenopyrgus'}}]}
    )
    == []
  )


def test_execute_builds_the_blocks_in_order():
  outcome = plan.execute(
    {
      'header': 'Rhenopyrgidae under Cyathocystidae; all years',
      'blocks': [
        {
          'tool': 'placed_under',
          'parameters': {'record': 'Rhenopyrgidae', 'parent': 'Cyathocystidae'},
        },
        {'tool': 'placements', 'parameters': {'records': ['rhenopyrgidae']}},
      ],
    }
  )
  assert outcome['errors'] == []
  assert [b['tool'] for b in outcome['blocks']] == ['placed_under', 'placements']
  assert outcome['blocks'][0]['parameters']['record'] == 'rhenopyrgidae'
  text = render_composition(outcome['composition'], 'text')
  assert text.startswith('Rhenopyrgidae under Cyathocystidae; all years\n\n')
  assert 'first Guensburg & Sprinkle 1994, last Grigo 2000' in text
  assert text.index('first Guensburg') < text.index('Placements by source')


def test_validate_checks_enums_and_list_lengths():
  blocks = [
    {'tool': 'history', 'parameters': {'record': 'rhenopyrgus', 'years': [1990]}},
    {'tool': 'history', 'parameters': {'record': 'rhenopyrgus', 'trees': ['bogus']}},
    {'tool': 'gap', 'parameters': {'source': 'Dehm 1961', 'kind': 'bogus'}},
    {'tool': 'statements', 'parameters': {'record': 'rhenopyrgus', 'kind': 'specimen'}},
    {
      'tool': 'statements',
      'parameters': {'record': 'rhenopyrgus', 'kind': None, 'act_kind': 'type'},
    },
  ]
  problems = plan.validate({'header': 'x', 'blocks': blocks})
  assert [p.split(':')[0] for p in problems] == ['block 1', 'block 2', 'block 3', 'block 4']
  assert problems[0].endswith('not [1990]; leave it out for the default')
  assert problems[1].startswith('block 2: history trees must be a list of taxonomy, cladogram')
  assert problems[2].startswith('block 3: gap kind must be one of skeleton, newTaxa,')
  assert problems[3].startswith('block 4: statements kind must be one of usage, placement,')
  # A plan that fails validation never reaches the tools.
  outcome = plan.execute({'header': 'x', 'blocks': blocks[:1]})
  assert outcome['composition'] is None
  assert [e['block'] for e in outcome['errors']] == [None]


def test_execute_lets_a_bug_through(monkeypatch):
  # Only a ValueError is a block that cannot be built; anything else is a bug.
  def broken(**kwargs):
    raise KeyError('bug')

  monkeypatch.setitem(tools.TOOLS, 'history', broken)
  with pytest.raises(KeyError):
    plan.execute({'header': 'x', 'blocks': [{'tool': 'history', 'parameters': {'record': 'x'}}]})


def test_execute_reports_what_it_cannot_build():
  outcome = plan.execute(
    {
      'header': 'x',
      'blocks': [
        {'tool': 'history', 'parameters': {'record': 'casteri'}},
        {'tool': 'gap', 'parameters': {'source': 'Lamarck 1816', 'kind': 'material'}},
        {'tool': 'gap', 'parameters': {'name': 'Rhenoblastus'}},
      ],
    }
  )
  assert [e['block'] for e in outcome['errors']] == [1, 2]
  assert 'casteri_bell.b.m_1975' in outcome['errors'][0]['error']
  assert '1816a_lamarck' in outcome['errors'][1]['error']
  assert [b['tool'] for b in outcome['blocks']] == ['gap']
  assert outcome['composition']['blocks'][0]['type'] == 'statement'
  assert (
    plan.execute({'header': 'x', 'blocks': [{'tool': 'bogus', 'parameters': {}}]})['composition']
    is None
  )
