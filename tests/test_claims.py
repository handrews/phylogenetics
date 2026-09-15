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

import os
import pathlib

import pytest
import yaml

from phylohist import plan
from phylohist.claims import extract, manifest
from phylohist.render import render_composition

QUESTIONS_PATH = pathlib.Path(__file__).parent.parent / 'eval' / 'questions.yaml'

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
  """The alternatives, each ``{blocks, shows}``: one list of blocks, or
  several under `anyOf`, an alternative being a list of blocks or an
  object with its own shows beside the question's."""
  spec = expected['blocks']
  items = spec['anyOf'] if isinstance(spec, dict) else [spec]
  return [item if isinstance(item, dict) else {'blocks': item, 'shows': []} for item in items]


def normalise(text):
  return ' '.join(text.split())


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


def test_no_inconsistencies(claims):
  rows = {
    source_key: entry['inconsistencies']
    for source_key, entry in manifest(claims)['sources'].items()
    if entry['inconsistencies']
  }
  if rows:
    listing = '\n'.join(f'{source_key}: {"; ".join(found)}' for source_key, found in rows.items())
    pytest.fail(
      f'{len(rows)} sources declare coverage their claims contradict '
      f'(run scripts/claims.py --inconsistencies):\n{listing}',
    )
