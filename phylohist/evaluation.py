"""The eval's pure parts, shared by the runner, the grader and the tests.

The runner (`scripts/eval_run.py`) talks to a model and writes run
files; the grader (`scripts/eval_grade.py`) reads them and writes
grades. What either decides without an API call lives here: where the
key comes from, what a compose-mode submission becomes, what the
expected answer's alternatives are, whether a composition meets one,
and how a judge's reply is read.
"""

import json
import os
import pathlib
import re

from . import blocks
from .tools import RECORD_PARAMETERS, SOURCE_PARAMETERS

ROOT = pathlib.Path(__file__).resolve().parent.parent

# What a header may not say: the corpus's own machinery, a verdict, or
# that the paper lacks something the corpus has not entered.
LEAK_WORDS = re.compile(
  r'\b(yaml|json|jsonl|claim table|record key|taxon_key|source_key|'
  r'coverage value|gold slice|milestone|MVP|resolve_name|claims_about|'
  r'source_coverage|name_history|block id|blockId|tool)\b',
  re.I,
)
VERDICT_WORDS = re.compile(
  r'\b(is a valid|is the correct|correctly|incorrectly|should be|clearly|'
  r'stands unopposed|is a genus|is a subgenus|is a synonym)\b',
  re.I,
)
DENIAL_WORDS = re.compile(
  r'not in the paper|paper (does not|doesn\'t|lacks|never)|'
  r'(does not|doesn\'t) (mention|print|give|provide|designate|report)',
  re.I,
)
NEGATED = re.compile(r'(not evidence that|not that|rather than|never that)[^.]{0,60}$', re.I)


def api_key(environ=None, dotenv=None):
  """The Anthropic key from the environment, else from a `.env` line at the
  repository root (`ANTHROPIC_API_KEY=...`, quotes and a leading `export`
  allowed, `#` lines ignored); None when neither has it. Never logged or
  written anywhere."""
  environ = os.environ if environ is None else environ
  key = environ.get('ANTHROPIC_API_KEY')
  if key:
    return key
  dotenv = ROOT / '.env' if dotenv is None else dotenv
  if dotenv.exists():
    for line in dotenv.read_text().splitlines():
      line = line.strip()
      if not line or line.startswith('#'):
        continue
      if line.startswith('export '):
        line = line[len('export ') :].lstrip()
      name, _, value = line.partition('=')
      value = value.strip().strip('"\'')
      if name.strip() == 'ANTHROPIC_API_KEY' and value:
        return value
  return None


def submit(payload, kept):
  """A compose-mode submission: the blocks the model chose, by id, from
  those the tools returned to it. Ids the tools never returned are
  listed as invalid; a submission naming no block, or only invalid ones,
  composes nothing."""
  ids = list(payload.get('blocks') or [])
  chosen = [kept[i] for i in ids if i in kept]
  invalid = [i for i in ids if i not in kept]
  composed = (
    blocks.compose(chosen, payload.get('header') or '', payload.get('question')) if chosen else None
  )
  return {
    'header': payload.get('header') or '',
    'question': payload.get('question'),
    'blocks': [
      {
        'blockId': b['blockId'],
        'type': b['type'],
        'tool': b.get('tool'),
        'parameters': b.get('parameters'),
        'claims': b['claims'],
      }
      for b in chosen
    ],
    'invalidIds': invalid,
    'composition': composed,
  }


def alternatives(expected):
  """The expected answer's alternatives, each ``{blocks, shows}``: one
  list of blocks, or several under `anyOf`, an alternative being a list
  of blocks or an object with its own shows beside the question's."""
  spec = expected.get('blocks')
  items = spec['anyOf'] if isinstance(spec, dict) else [spec or []]
  return [item if isinstance(item, dict) else {'blocks': item, 'shows': []} for item in items]


def normalise(text):
  return ' '.join(text.split())


def denial(text):
  """The first phrase saying the paper lacks something, unless it is
  negated just before ("not that the paper lacks it")."""
  for m in DENIAL_WORDS.finditer(text):
    before = text[max(0, m.start() - 70) : m.start()]
    if not NEGATED.search(before):
      return m.group(0)
  return None


def composed_blocks(record):
  return (record.get('composition') or {}).get('blocks') or []


def tools_of(record):
  """Which tool produced each block the model saw, for runs that did not
  record it on the composition."""
  found = {}
  for call in record.get('toolCalls') or ():
    for b in (call.get('result') or {}).get('blocks') or ():
      found[b['blockId']] = call['name']
  return found


def mechanical(record, question, store):
  """The mechanical grade of one run record against its question:
  ``(failures, notes)``. A composition must exist and name only blocks
  the tools returned; its header and question must leak nothing, pass
  no verdict and deny nothing; one expected alternative must be met in
  full, its blocks and its shows with the question's, the failures
  reported being the nearest miss. Text the model wrote beside its
  calls is noted, never failed: no reader sees it."""
  failures, notes = [], []
  expected = question.get('expected') or {}
  comp = record.get('composition')
  if not comp:
    failures.append('no composition (the model answered in prose or not at all)')
    return failures, notes
  if comp.get('invalidIds'):
    failures.append(f'submitted block ids the tools never returned: {comp["invalidIds"]}')
  if not comp.get('blocks'):
    failures.append('nothing composed: the submission names no block that could be shown')
  beside, between = [], []
  for entry in comp.get('freeText') or ():
    # The first run recorded free text as bare strings, all beside the submission.
    if not isinstance(entry, dict) or entry.get('withSubmit'):
      beside.append(entry['text'] if isinstance(entry, dict) else entry)
    else:
      between.append(entry['text'])
  if beside:
    notes.append('text beside the submission: ' + ' | '.join(t[:80] for t in beside))
  if between:
    notes.append('text between lookups: ' + ' | '.join(t[:80] for t in between))
  header = (comp.get('header') or '') + ' ' + (comp.get('question') or '')
  leak = LEAK_WORDS.search(header)
  if leak:
    failures.append(f'header leaks internals: "{leak.group(0)}"')
  verdict = VERDICT_WORDS.search(header)
  if verdict:
    failures.append(f'header passes a verdict: "{verdict.group(0)}"')
  denied = denial(header)
  if denied:
    failures.append(f'header says the paper lacks it: "{denied}"')

  tool_of = tools_of(record)
  composed = [
    dict(b, tool=b.get('tool') or tool_of.get(b['blockId'])) for b in composed_blocks(record)
  ]
  rendered = normalise(record.get('rendered') or '')
  nearest = None
  for alternative in alternatives(expected):
    misses = [
      f'no composed block is {spec["tool"]} '
      f'{json.dumps(spec.get("parameters") or {}, ensure_ascii=False)}'
      for spec in alternative['blocks']
      if not any(block_matches(store, spec, b) for b in composed)
    ]
    misses += [
      f'the answer does not show "{text}"'
      for text in list(expected.get('shows') or ()) + alternative['shows']
      if normalise(text) not in rendered
    ]
    if nearest is None or len(misses) < len(nearest):
      nearest = misses
  failures += nearest or []
  if record.get('stopReason') == 'max_turns':
    notes.append('composed after the lookup limit was reached')
  return failures, notes


def snake(name):
  """Parameter names as the specs spell them. Run files before 2026-09-15
  carry the blocks' earlier camelCase names (includeVariants, actKind,
  alsoKinds); newer ones need no change."""
  return re.sub(r'([A-Z])', lambda m: '_' + m.group(1).lower(), name)


def same_value(store, name, expected, actual):
  """A parameter value the expectation names must agree with the composed
  block's: keys and citations after resolution, lists as sets."""
  if isinstance(expected, list):
    if not isinstance(actual, list):
      return False
    return {norm(store, name, v) for v in expected} <= {norm(store, name, v) for v in actual}
  return norm(store, name, expected) == norm(store, name, actual)


def norm(store, name, value):
  if isinstance(value, str):
    if name in RECORD_PARAMETERS:
      try:
        return store.key_of('record', value)
      except ValueError:
        return value
    if name in SOURCE_PARAMETERS:
      try:
        key = store.key_of('source', value)
      except ValueError:
        return value
      if key in store.sources:
        return key
      sig = store.source_signature(value)
      return (sig['year'], tuple(sig['authors'][:1]))
  return value


def block_matches(store, spec, block):
  """Whether a composed block is the expected one: the same tool (or the
  gap block the statements tool answers an empty query with) and
  agreement on every parameter the expectation names."""
  gap_by_statements = (
    spec['tool'] == 'gap' and block.get('tool') == 'statements' and block.get('type') == 'statement'
  )
  if block.get('tool') != spec['tool'] and not gap_by_statements:
    return False
  actual = {snake(k): v for k, v in (block.get('parameters') or {}).items()}
  for name, value in (spec.get('parameters') or {}).items():
    if gap_by_statements and name == 'kind' and value in (actual.get('also_kinds') or ()):
      continue
    if name not in actual or not same_value(store, name, value, actual[name]):
      return False
  return True


def parse_verdict(text):
  """The judge's ``{"contract": n, "reason": ...}`` from its reply: the
  JSON if it parses, else the two fields picked out of the text; None
  when neither is there."""
  match = re.search(r'\{.*\}', text, re.S)
  if match:
    try:
      verdict = json.loads(match.group(0))
      if isinstance(verdict, dict) and isinstance(verdict.get('contract'), int):
        return verdict
    except json.JSONDecodeError:
      pass
  score = re.search(r'"contract"\s*:\s*([012])', text)
  reason = re.search(r'"reason"\s*:\s*"([^"]*)', text)
  if score:
    return {'contract': int(score.group(1)), 'reason': reason.group(1) if reason else ''}
  return None


def previous_judge(grades, model):
  """Valid judge entries from an earlier grading of the same run by the
  same model, so a re-run judges only what is missing."""
  previous = {}
  for grade in grades:
    verdict = grade.get('judge') or {}
    if grade.get('judgeModel') == model and isinstance(verdict.get('contract'), int):
      previous[grade['id']] = verdict
  return previous
