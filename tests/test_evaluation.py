"""The eval's pure parts, without a model.

`phylohist.evaluation` decides where the key comes from, what a
submission becomes, whether a composition meets an expected answer,
and how a judge's reply is read; each decision is checked here on
small synthetic records over the real store.
"""

import os

import pytest

from phylohist import evaluation as ev

pytestmark = pytest.mark.skipif(
  bool(os.getenv('PHYLOHIST_DRAFTS')),
  reason='the committed claim table covers data/ only',
)


def test_api_key_from_environment_or_dotenv(tmp_path):
  dotenv = tmp_path / '.env'
  assert ev.api_key({'ANTHROPIC_API_KEY': 'from-env'}, dotenv) == 'from-env'
  assert ev.api_key({}, dotenv) is None
  dotenv.write_text('# the key\nexport ANTHROPIC_API_KEY = "from-file"\nOTHER=x\n')
  assert ev.api_key({}, dotenv) == 'from-file'
  dotenv.write_text("ANTHROPIC_API_KEY='quoted'\n")
  assert ev.api_key({}, dotenv) == 'quoted'
  dotenv.write_text('ANTHROPIC_API_KEY=\n')
  assert ev.api_key({}, dotenv) is None


def _kept():
  return {
    'b1': {
      'blockId': 'b1',
      'type': 'chains',
      'parameters': {'record': 'x'},
      'claims': ['c1'],
      'tool': 'ancestors',
    },
    'b2': {
      'blockId': 'b2',
      'type': 'table',
      'parameters': {},
      'claims': ['c2'],
      'tool': 'descendants',
    },
  }


def test_submit_keeps_chosen_blocks_and_reports_the_rest():
  got = ev.submit({'header': 'h', 'blocks': ['b2', 'nope', 'b1']}, _kept())
  assert [b['blockId'] for b in got['blocks']] == ['b2', 'b1']
  assert got['blocks'][0]['tool'] == 'descendants'
  assert got['invalidIds'] == ['nope']
  assert [b['blockId'] for b in got['composition']['blocks']] == ['b2', 'b1']
  # Nothing chosen composes nothing, whether the ids were invalid or absent.
  assert ev.submit({'header': 'h', 'blocks': ['nope']}, _kept())['composition'] is None
  empty = ev.submit({'header': 'h', 'blocks': []}, _kept())
  assert empty['composition'] is None and empty['blocks'] == [] and empty['invalidIds'] == []


def test_alternatives_take_both_forms():
  assert ev.alternatives({'blocks': [{'tool': 'gap'}]}) == [
    {'blocks': [{'tool': 'gap'}], 'shows': []}
  ]
  both = ev.alternatives(
    {'blocks': {'anyOf': [[{'tool': 'gap'}], {'blocks': [{'tool': 'history'}], 'shows': ['x']}]}}
  )
  assert both == [
    {'blocks': [{'tool': 'gap'}], 'shows': []},
    {'blocks': [{'tool': 'history'}], 'shows': ['x']},
  ]
  assert ev.alternatives({}) == [{'blocks': [], 'shows': []}]


def test_denial_unless_negated():
  assert ev.denial('the paper does not mention it') == 'paper does not'
  assert ev.denial('it does not mention the species') == 'does not mention'
  assert ev.denial('not that the paper lacks it; it is not yet entered') is None


def _record(blocks, rendered='', header='Rhenopyrgidae; all years', **extra):
  return {
    'composition': {
      'header': header,
      'question': None,
      'blocks': list(blocks),
      'invalidIds': [],
      'freeText': [],
      'compositionId': 'c' if blocks else None,
    },
    'rendered': rendered,
    **extra,
  }


def _block(tool, kind='chains', **parameters):
  return {
    'blockId': tool[:4],
    'type': kind,
    'tool': tool,
    'parameters': parameters,
    'claims': ['c'],
  }


PLACED = {
  'tool': 'placed_under',
  'parameters': {'record': 'rhenopyrgidae', 'parent': 'cyathocystidae'},
}
GAP = {'tool': 'gap', 'parameters': {'source': '1983_holloway_jell', 'kind': 'synonymy'}}


def test_mechanical_on_the_composition_itself(store):
  question = {'expected': {'blocks': [PLACED]}}
  assert ev.mechanical({'composition': None}, question, store)[0] == [
    'no composition (the model answered in prose or not at all)'
  ]
  record = _record([])
  record['composition']['invalidIds'] = ['zz']
  failures, _ = ev.mechanical(record, question, store)
  assert failures[:2] == [
    "submitted block ids the tools never returned: ['zz']",
    'nothing composed: the submission names no block that could be shown',
  ]


def test_mechanical_reads_the_header(store):
  question = {'expected': {'blocks': []}}
  block = _block('placed_under', record='rhenopyrgidae', parent='cyathocystidae')
  leak = _record([block], header='the record key rhenopyrgidae; all years')
  assert ev.mechanical(leak, question, store)[0] == ['header leaks internals: "record key"']
  verdict = _record([block], header='Rhenopyrgidae is a synonym; all years')
  assert ev.mechanical(verdict, question, store)[0] == ['header passes a verdict: "is a synonym"']
  denial = _record([block], header='the paper does not mention it')
  assert ev.mechanical(denial, question, store)[0] == [
    'header says the paper lacks it: "paper does not"'
  ]
  record = _record([block], stopReason='max_turns')
  record['composition']['freeText'] = [{'turn': 0, 'text': 'thinking', 'withSubmit': True}]
  failures, notes = ev.mechanical(record, question, store)
  assert failures == []
  assert notes == [
    'text beside the submission: thinking',
    'composed after the lookup limit was reached',
  ]


def test_mechanical_matches_shapes_after_resolution(store):
  question = {'expected': {'blocks': [PLACED], 'shows': ['first Guensburg']}}
  # The composed block names the record and parent as printed; the
  # expectation names keys; they agree after resolution.
  block = _block('placed_under', record='Rhenopyrgidae', parent='Cyathocystidae')
  record = _record([block], rendered='first  Guensburg & Sprinkle 1994')
  assert ev.mechanical(record, question, store)[0] == []
  other = _record([_block('placed_under', record='rhenopyrgidae', parent='edrioblastoidina')])
  failures, _ = ev.mechanical(other, question, store)
  assert failures == [
    'no composed block is placed_under {"record": "rhenopyrgidae", "parent": "cyathocystidae"}',
    'the answer does not show "first Guensburg"',
  ]


def test_mechanical_reports_the_nearest_alternative(store):
  question = {
    'expected': {
      'blocks': {
        'anyOf': [
          [PLACED, GAP],
          {
            'blocks': [{'tool': 'history', 'parameters': {'record': 'rhenopyrgidae'}}],
            'shows': ['1983  Holloway'],
          },
        ]
      }
    }
  }
  record = _record([_block('history', kind='timeline', record='rhenopyrgidae')], rendered='nothing')
  failures, _ = ev.mechanical(record, question, store)
  assert failures == ['the answer does not show "1983  Holloway"']
  record['rendered'] = '1983  Holloway & Jell  Rhenopyrgidae'
  assert ev.mechanical(record, question, store)[0] == []


def test_a_statements_gap_meets_an_expected_gap(store):
  question = {'expected': {'blocks': [GAP]}}
  gap = _block('statements', kind='statement')
  gap['parameters'] = {
    'source': 'Holloway & Jell 1983',
    'kind': 'skeleton',
    'also_kinds': ['synonymy'],
  }
  assert ev.mechanical(_record([gap]), question, store)[0] == []
  # A run file from before the rename spells the parameter alsoKinds.
  gap['parameters'] = {
    'source': 'Holloway & Jell 1983',
    'kind': 'skeleton',
    'alsoKinds': ['synonymy'],
  }
  assert ev.mechanical(_record([gap]), question, store)[0] == []
  gap['parameters'] = {'source': 'Holloway & Jell 1983', 'kind': 'skeleton'}
  assert ev.mechanical(_record([gap]), question, store)[0] == [
    'no composed block is gap {"source": "1983_holloway_jell", "kind": "synonymy"}'
  ]


def test_parse_verdict_and_previous_judge():
  assert ev.parse_verdict('{"contract": 2, "reason": "fine"}') == {'contract': 2, 'reason': 'fine'}
  assert ev.parse_verdict('Sure.\n{"contract": 1, "reason": "one lapse"}\nDone.') == {
    'contract': 1,
    'reason': 'one lapse',
  }
  assert ev.parse_verdict('{"contract": 0, "reason": "unterminated') == {
    'contract': 0,
    'reason': 'unterminated',
  }
  assert ev.parse_verdict('no verdict here') is None
  grades = [
    {'id': 'q1', 'judgeModel': 'm', 'judge': {'contract': 2, 'reason': 'x'}},
    {'id': 'q2', 'judgeModel': 'm', 'judge': {'error': 'garbled'}},
    {'id': 'q3', 'judgeModel': 'other', 'judge': {'contract': 1, 'reason': 'y'}},
  ]
  assert ev.previous_judge(grades, 'm') == {'q1': {'contract': 2, 'reason': 'x'}}
