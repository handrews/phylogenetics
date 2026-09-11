"""Every eval question must still match the claim table.

`eval/README.md` promises that a question whose expected answer stops
matching the data is updated or removed, never left stale; this test makes
that mechanical. Each `expected.claims` selector must match at least one
claim of its source (recursive subset match: every selector key present
with an equal value, lists compared element by element); a `not-captured`
refusal needs the source to declare `none` or `partly` for the coverage
kind, or to have no tree; an `absent` refusal needs no tree for the scoped
source, or no claim about the scoped taxon when no source is given.

The manifest's inconsistency rows are gated too: a declared coverage
value that the derived claims contradict fails until the declaration or
the tree is corrected (`scripts/claims.py --inconsistencies` explains
each row).
"""

import os
import pathlib

import pytest
import yaml

from phylohist.claims import extract, manifest
from phylohist.research import Source

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


def matches(selector, value):
  if isinstance(selector, dict):
    return isinstance(value, dict) and all(
      key in value and matches(sub, value[key])
      for key, sub in selector.items()
    )
  if isinstance(selector, list):
    return (
      isinstance(value, list) and len(value) == len(selector) and
      all(matches(a, b) for a, b in zip(selector, value))
    )
  return selector == value


def _derived(claims, source_key, coverage_kind):
  return sum(
    1 for c in claims.get(source_key, ())
    if c['audit'].get('coverageKind') == coverage_kind
    and not c.get('inferred')
  )


@pytest.mark.parametrize('question', QUESTIONS, ids=[q['id'] for q in QUESTIONS])
def test_question(question, claims):
  expected = question['expected']
  scope = question.get('scope') or {}
  qid = question['id']

  for selector in expected.get('claims') or ():
    source_key = selector['source']
    if source_key not in claims:
      pytest.fail(f'{qid}: no tree for {source_key}; selector {selector}')
    if not any(matches(selector, c) for c in claims[source_key]):
      pytest.fail(f'{qid}: no claim of {source_key} matches {selector}')

  refusal = expected.get('refusal')
  if refusal == 'not-captured':
    source_key = scope['source']
    kind = expected['coverageKind']
    if source_key not in claims:
      return
    declared = (Source.get(source_key).audit.get('coverage') or {}).get(kind)
    if declared in ('none', 'partly'):
      return
    derived = _derived(claims, source_key, kind)
    if declared is None and derived == 0:
      return
    pytest.fail(
      f'{qid}: {source_key} declares {kind}: {declared} and derives '
      f'{derived} claims; not-captured needs none or partly',
    )
  elif refusal == 'absent':
    if 'source' in scope:
      if scope['source'] in claims:
        pytest.fail(f'{qid}: {scope["source"]} has a tree; not absent')
    elif 'taxon' in scope:
      mentions = sorted(
        source_key for source_key, source_claims in claims.items()
        if any(c['subject'] == scope['taxon'] for c in source_claims)
      )
      if mentions:
        pytest.fail(f'{qid}: {scope["taxon"]} has claims in {mentions}')
    else:
      pytest.fail(f'{qid}: an absent question needs a scoped taxon or source')


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
