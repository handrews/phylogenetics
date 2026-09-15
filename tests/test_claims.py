"""Every eval question's expected answer must still build from the corpus.

`eval/README.md` promises that a question whose expected answer stops
matching the data is updated or removed, never left stale; this test
makes that mechanical. An expected answer is the blocks it is made of
(a tool and the parameters that matter) and the strings the rendered
answer shows. Each block of each alternative must build through
`phylohist.tools.call` into a block that rests on claims, or a gap or
absence statement; the rendered composition of the first alternative
must contain every `shows` string.

The manifest's inconsistency rows are gated too: a declared coverage
value that the derived claims contradict fails until the declaration or
the tree is corrected (`scripts/claims.py --inconsistencies` explains
each row).
"""

import os
import pathlib

import pytest
import yaml

from phylohist import blocks, tools
from phylohist.claims import extract, manifest
from phylohist.render import render_composition

QUESTIONS_PATH = (
  pathlib.Path(__file__).parent.parent / 'eval' / 'questions.yaml'
)

with open(QUESTIONS_PATH) as fd:
  QUESTIONS = yaml.safe_load(fd)

pytestmark = pytest.mark.skipif(
  bool(os.getenv('PHYLOHIST_DRAFTS')),
  reason='the eval set is written against data/ only',
)


@pytest.fixture(scope='session')
def claims(load_records):
  _, _, roots = load_records
  return extract(roots)


def alternatives(expected):
  """The expected block lists: one, or several under `anyOf`."""
  spec = expected['blocks']
  if isinstance(spec, dict):
    return spec['anyOf']
  return [spec]


def build(block_spec):
  """The blocks a tool call returns for an expected block."""
  result = tools.call(block_spec['tool'], dict(block_spec.get('parameters') or {}, style='json'))
  return result if isinstance(result, list) else [result]


def normalise(text):
  return ' '.join(text.split())


@pytest.mark.parametrize('question', QUESTIONS, ids=[q['id'] for q in QUESTIONS])
def test_question(question):
  expected = question['expected']
  qid = question['id']
  first = None
  for alternative in alternatives(expected):
    built = []
    for spec in alternative:
      got = build(spec)
      if not got:
        pytest.fail(f"{qid}: {spec['tool']} {spec.get('parameters')} returns nothing")
      for block in got:
        if block['type'] != 'statement' and not block['claims']:
          pytest.fail(f"{qid}: {spec['tool']} {spec.get('parameters')} rests on no claim")
      built += got
    if first is None:
      first = built
  rendered = normalise(render_composition(blocks.compose(first, ''), 'text'))
  for text in expected.get('shows') or ():
    if normalise(text) not in rendered:
      pytest.fail(f'{qid}: the expected answer does not show "{text}"')


def test_no_inconsistencies(claims):
  rows = {
    source_key: entry['inconsistencies']
    for source_key, entry in manifest(claims)['sources'].items()
    if entry['inconsistencies']
  }
  if rows:
    listing = '\n'.join(
      f'{source_key}: {"; ".join(found)}' for source_key, found in rows.items()
    )
    pytest.fail(
      f'{len(rows)} sources declare coverage their claims contradict '
      f'(run scripts/claims.py --inconsistencies):\n{listing}',
    )
