#!/usr/bin/env python3
"""Grade a run of the eval: mechanical checks over compositions, a judge on request.

    poetry run python scripts/eval_grade.py eval/runs/2026-09-12-claude-sonnet-5.jsonl
    poetry run python scripts/eval_grade.py <run> --judge claude-opus-5

An answer is a composition: a header, blocks the tools returned, and
perhaps a question back. The mechanical checks, all on by default:

- a composition exists and every block id in it came from this
  conversation;
- for a question with expected claims, every selector matches a claim
  referenced by a composed block (completeness: retrieval alone does not
  count);
- a not-captured question composes a gap block for the scoped source
  and kind of statement; an absent question composes an absent or
  unentered-source block, and no block about the scoped taxon when no
  source is given;
- the header and any question contain no leak of internals and no
  verdict; the reply that submitted carried no text beside the call
  (text between lookups is noted, not failed);
- when the evidence names a page and a composed block carries it, the
  rendered answer shows it.

With --judge, a judge model scores the header and question only, for
contract (0-2); a re-run keeps the valid scores already in the grades
file and judges only what is missing. Writes `<run>.grades.jsonl` and `<run>.md`, a summary
with per-class pass rates and every failure with the composition the
model chose, for the owner's review.
"""

import argparse
import collections
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import yaml  # noqa: E402

from phylohist.tools import ClaimStore  # noqa: E402
from tests.selectors import matches  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / 'eval' / 'questions.yaml'
README = ROOT / 'eval' / 'README.md'

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


def load_jsonl(path):
  with open(path) as fd:
    return [json.loads(line) for line in fd if line.strip()]


def composed_claims(record):
  comp = record.get('composition') or {}
  return {c for b in comp.get('blocks') or () for c in b.get('claims') or ()}


def composed_blocks(record):
  return (record.get('composition') or {}).get('blocks') or []


def _denial(text):
  for m in DENIAL_WORDS.finditer(text):
    before = text[max(0, m.start() - 70):m.start()]
    if not NEGATED.search(before):
      return m.group(0)
  return None


def mechanical(record, question, store):
  """(failures, notes)."""
  failures, notes = [], []
  expected = question.get('expected') or {}
  scope = question.get('scope') or {}
  comp = record.get('composition')
  if not comp:
    failures.append('no composition (the model answered in prose or not at all)')
    return failures, notes
  if comp.get('invalidIds'):
    failures.append(f"submitted block ids the tools never returned: {comp['invalidIds']}")
  beside, between = [], []
  for entry in comp.get('freeText') or ():
    # The first run recorded free text as bare strings, all beside the submission.
    if not isinstance(entry, dict) or entry.get('withSubmit'):
      beside.append(entry['text'] if isinstance(entry, dict) else entry)
    else:
      between.append(entry['text'])
  if beside:
    failures.append('free text beside the submission: ' + ' | '.join(t[:80] for t in beside))
  if between:
    notes.append('text between lookups: ' + ' | '.join(t[:80] for t in between))
  header = (comp.get('header') or '') + ' ' + (comp.get('question') or '')
  leak = LEAK_WORDS.search(header)
  if leak:
    failures.append(f'header leaks internals: "{leak.group(0)}"')
  verdict = VERDICT_WORDS.search(header)
  if verdict:
    failures.append(f'header passes a verdict: "{verdict.group(0)}"')
  denial = _denial(header)
  if denial:
    failures.append(f'header says the paper lacks it: "{denial}"')

  claims = composed_claims(record)
  got = [store.by_id[c] for c in claims if c in store.by_id]
  selectors = expected.get('claims') or []
  for selector in selectors:
    if not any(matches(selector, c) for c in got):
      failures.append(f'no composed block carries a claim matching {selector}')
  evidence = question.get('evidence') or {}
  if isinstance(evidence, dict):
    page = evidence.get('pages')
    if isinstance(page, int) and str(page) not in (record.get('rendered') or ''):
      source_key = evidence.get('source')
      carried = any(
        c['source'] == (source_key or c['source']) and _has_page(c, page) for c in got
      )
      (failures if carried else notes).append(
        f'page {page} {"not shown" if carried else "not among the composed claims"}'
      )

  blocks = composed_blocks(record)
  refusal = expected.get('refusal')
  if refusal == 'not-captured':
    wanted = (scope.get('source'), expected.get('coverageKind'))
    gaps = [b for b in blocks if b['type'] == 'statement' and
            (b.get('parameters') or {}).get('source') == wanted[0] and
            (b.get('parameters') or {}).get('kind') == wanted[1]]
    if not gaps:
      failures.append(f'no gap block for {wanted[0]} / {wanted[1]}')
  elif refusal == 'absent':
    statements = [b for b in blocks if b['type'] == 'statement']
    if scope.get('source'):
      # The block names the source by key when the corpus has it, or by
      # the citation the model typed when it does not.
      wanted = _source_sig(store, scope['source'])
      ok = any(
        (b.get('parameters') or {}).get('source') == scope['source']
        or _source_sig(store, (b.get('parameters') or {}).get('source')) == wanted
        for b in statements
      )
      if not ok:
        failures.append(f"no block states that {scope['source']} is not entered")
    else:
      if not statements and blocks:
        failures.append('an absent question composed only blocks with content')
      taxon = scope.get('taxon')
      if taxon and any(store.by_id[c]['subject'] == taxon for c in claims if c in store.by_id):
        failures.append(f'a composed block makes statements about {taxon}')
  if record.get('stopReason') == 'max_turns':
    notes.append('composed after the lookup limit was reached')
  return failures, notes


def _source_sig(store, text):
  if not text:
    return None
  sig = store.source_signature(text)
  return (sig['year'], tuple(sig['families'][:1]))


def _has_page(claim, page):
  pages = claim.get('pages')
  if pages is None:
    return False
  for item in (pages if isinstance(pages, list) else [pages]):
    if item == page or (isinstance(item, list) and len(item) == 2 and item[0] <= page <= item[1]):
      return True
  return False


JUDGE_PROMPT = """You are grading the header and question of an answer assembled from blocks of a closed corpus of published taxonomic opinions. The blocks themselves are computed and are not graded here. Score contract 0, 1 or 2: 2 if the header states only the parameters chosen (which records the group is, whether synonyms and rank variants are included, which trees, the year range) in the language of the scientific community, passes no verdict, and the question (if any) asks about a genuinely ambiguous parameter; 1 for one lapse (a summary, a mechanism word, a judgement); 0 for more. Reply with JSON only: {"contract": n, "reason": "..."} with the reason at most 25 words.

Question class: %s
Question: %s
Expected answer:
<expected>
%s
</expected>
Header: %s
Question back: %s
"""


def judge(client, model, record, question):
  comp = record.get('composition') or {}
  expected = question.get('expected') or {}
  prompt = JUDGE_PROMPT % (
    question['class'], question['question'],
    expected.get('answer', '(a refusal: ' + str(expected.get('refusal')) + ')'),
    comp.get('header') or '(none)', comp.get('question') or '(none)',
  )
  # The judge's reasoning counts against max_tokens; a low cap truncates
  # the JSON or leaves no text at all, so the cap is generous and a
  # malformed reply is retried once before it is recorded as an error.
  text = ''
  for _ in range(2):
    response = client.messages.create(model=model, max_tokens=4000,
                                      messages=[{'role': 'user', 'content': prompt}])
    text = ''.join(b.text for b in response.content if b.type == 'text')
    verdict = _parse_verdict(text)
    if verdict is not None:
      return verdict
  return {'error': text}


def _parse_verdict(text):
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


def _previous_judge(path, model):
  """Valid judge entries from an earlier grading of the same run, so a
  re-run judges only what is missing."""
  previous = {}
  if path.exists():
    for grade in load_jsonl(path):
      verdict = grade.get('judge') or {}
      if grade.get('judgeModel') == model and isinstance(verdict.get('contract'), int):
        previous[grade['id']] = verdict
  return previous


def summary(path, grades):
  by_class = collections.defaultdict(lambda: {'n': 0, 'pass': 0})
  for grade in grades:
    row = by_class[grade['class']]
    row['n'] += 1
    if not grade['failures']:
      row['pass'] += 1
  lines = [f'# Grades for `{path.name}`', '']
  lines.append('| class | questions | mechanical pass |')
  lines.append('|---|---|---|')
  for cls, row in sorted(by_class.items()):
    lines.append(f"| {cls} | {row['n']} | {row['pass']} |")
  lines.append('')
  lines.append('## Failures and notes')
  lines.append('')
  for grade in grades:
    if not grade['failures'] and not grade.get('notes'):
      continue
    lines.append(f"### {grade['id']} ({grade['class']})")
    lines.append('')
    lines.append(f"Q: {grade['question']}")
    lines.append('')
    for failure in grade['failures']:
      lines.append(f'- failure: {failure}')
    for note in grade.get('notes') or ():
      lines.append(f'- note: {note}')
    if grade.get('judge'):
      lines.append(f"- judge contract {grade['judge'].get('contract')}: {grade['judge'].get('reason', '')}")
    comp = grade.get('composition') or {}
    lines.append('')
    lines.append(f"Header: {comp.get('header', '')}")
    for b in comp.get('blocks') or ():
      lines.append(f"- {b['type']} {json.dumps(b.get('parameters'), ensure_ascii=False)}")
    if comp.get('question'):
      lines.append(f"Question back: {comp['question']}")
    lines.append('')
    lines.append('> ' + (grade['rendered'] or '').strip().replace('\n', '\n> '))
    lines.append('')
  return '\n'.join(lines) + '\n'


def main(argv):
  parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
  parser.add_argument('run', type=pathlib.Path)
  parser.add_argument('--judge', help='judge model for the header and question')
  args = parser.parse_args(argv)

  with open(QUESTIONS) as fd:
    questions = {q['id']: q for q in yaml.safe_load(fd)}
  store = ClaimStore()
  records = load_jsonl(args.run)

  client = None
  if args.judge:
    import anthropic
    from eval_run import api_key  # noqa: E402
    client = anthropic.Anthropic(api_key=api_key())

  grades_path = args.run.with_suffix('.grades.jsonl')
  previous = _previous_judge(grades_path, args.judge) if args.judge else {}
  grades = []
  for record in records:
    question = questions[record['id']]
    failures, notes = mechanical(record, question, store)
    grade = {
      'id': record['id'], 'class': record['class'], 'question': record['question'],
      'composition': record.get('composition'), 'rendered': record.get('rendered'),
      'failures': failures, 'notes': notes,
    }
    if client is not None:
      grade['judge'] = previous.get(record['id']) or judge(client, args.judge, record, question)
      grade['judgeModel'] = args.judge
    grades.append(grade)
    status = 'ok ' if not failures else 'FAIL'
    print(f"{grade['id']} {status} " + '; '.join(failures))

  with open(grades_path, 'w') as fd:
    for grade in grades:
      fd.write(json.dumps(grade, ensure_ascii=False) + '\n')
  summary_path = args.run.with_suffix('.md')
  summary_path.write_text(summary(args.run, grades))
  print(f'-> {grades_path}\n-> {summary_path}')
  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
