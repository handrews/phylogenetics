#!/usr/bin/env python3
"""Grade a run of the eval: mechanical checks, then a judge model.

    poetry run python scripts/eval_grade.py eval/runs/2026-09-11-claude-sonnet-5.jsonl
    poetry run python scripts/eval_grade.py <run> --no-judge
    poetry run python scripts/eval_grade.py <run> --judge claude-opus-5

Mechanical checks per question class:

- with expected claims: the model retrieved, through the tools, a claim
  matching every expected selector, and the answer names each expected
  source's author and year (and the page when `evidence` gives one);
- not-captured: the answer says the material has not yet been entered
  or is not captured, and does not say the paper lacks it;
- absent: the model asked the corpus (a name resolution or a source
  lookup) and the answer names nothing outside it as fact.

The judge scores each answer 0-2 on three axes against the expected
answer and the contract in eval/README.md: grounded (every fact traceable
to the corpus), complete (what the expected answer holds is there), and
contract (refusal language, trajectory structure, no verdict, no leak of
tools or planning). Writes `<run>.grades.jsonl` and `<run>.md`, a summary
with per-class pass rates and every failure, for the owner's review.
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

NOT_CAPTURED_WORDS = re.compile(
  r'not (yet )?been entered|not captured|has not been entered|not yet entered',
  re.I,
)
DENIAL_WORDS = re.compile(
  r'not in the paper|paper (does not|doesn\'t|lacks|never)|'
  r'(does not|doesn\'t) (mention|print|give|provide|designate|report)',
  re.I,
)
LEAK_WORDS = re.compile(
  r'\b(yaml|json|jsonl|claim table|record key|taxon_key|source_key|'
  r'coverage value|gold slice|milestone|MVP|resolve_name|claims_about|'
  r'source_coverage|name_history)\b',
  re.I,
)


def load_jsonl(path):
  with open(path) as fd:
    return [json.loads(line) for line in fd if line.strip()]


def retrieved_ids(record):
  ids = set()
  for call in record['toolCalls']:
    result = call.get('result') or {}
    ids.update(result.get('ids', ()))
  return ids


def asked_corpus(record):
  return any(
    c['name'] in ('resolve_name', 'source_coverage') for c in record['toolCalls']
  )


def _page_seen(got, source_key, page):
  for claim in got:
    if claim['source'] != source_key:
      continue
    pages = claim.get('pages')
    if pages is None:
      continue
    for item in (pages if isinstance(pages, list) else [pages]):
      if item == page or (isinstance(item, list) and len(item) == 2
                          and item[0] <= page <= item[1]):
        return True
  return False


def mechanical(record, question, store):
  """A list of failure strings and a list of notes; no failures means
  every check passed. A trajectory answer that did not retrieve one of
  its expected claims gets a note, since the judge grades its
  completeness; a point answer gets a failure."""
  failures = []
  notes = []
  expected = question.get('expected') or {}
  answer = record['answer'] or ''
  if not answer.strip():
    return ['no answer produced'], notes

  selectors = expected.get('claims') or []
  if selectors:
    ids = retrieved_ids(record)
    got = [c for source_claims in store.by_source.values()
           for c in source_claims if c['id'] in ids]
    cited_sources = set()
    for selector in selectors:
      if not any(matches(selector, c) for c in got):
        message = f'did not retrieve a claim matching {selector}'
        (notes if question['class'] == 'trajectory' else failures).append(message)
      cited_sources.add(selector['source'])
    for source_key in sorted(cited_sources):
      row = store.sources.get(source_key)
      if row is None:
        continue
      citation = row['citation']
      year = str(citation.get('year'))
      family = (citation.get('authors') or [''])[0]
      if year not in answer or family.split('.')[0].lower() not in answer.lower():
        failures.append(f'answer does not cite {store.cite(source_key)}')
    evidence = question.get('evidence') or {}
    pages = evidence.get('pages') if isinstance(evidence, dict) else None
    if isinstance(pages, int) and str(pages) not in answer:
      source_key = evidence.get('source') or next(iter(cited_sources), None)
      if _page_seen(got, source_key, pages):
        failures.append(f'answer does not give page {pages}')
      else:
        notes.append(f'page {pages} was not among the retrieved claims')

  refusal = expected.get('refusal')
  if refusal == 'not-captured':
    if not NOT_CAPTURED_WORDS.search(answer):
      failures.append('refusal does not say the material has not yet been entered')
    if DENIAL_WORDS.search(answer):
      failures.append('refusal says the paper lacks it: ' +
                      DENIAL_WORDS.search(answer).group(0))
  elif refusal == 'absent':
    if not asked_corpus(record):
      failures.append('answered without asking the corpus')
    if DENIAL_WORDS.search(answer) and 'corpus' not in answer.lower():
      failures.append('absence stated as a fact about the paper')

  leak = LEAK_WORDS.search(answer)
  if leak:
    failures.append(f'answer leaks internals: "{leak.group(0)}"')
  return failures, notes


JUDGE_PROMPT = """You are grading one answer from a question-answering system that may use only a closed corpus of published taxonomic opinions. Score the answer on three axes, each 0, 1 or 2, and give a one-sentence reason for each.

grounded: 2 if every fact in the answer could come from the corpus as the expected answer describes it and nothing is added from general knowledge; 1 if one detail is unsupported or embellished; 0 if the answer asserts facts the expected answer contradicts or that the corpus could not hold.

complete: 2 if what the expected answer holds is present (the same sources, positions, counts or refusal); 1 if part is missing; 0 if the substance is missing or wrong.

contract: 2 if the answer follows the contract below for its class (a refusal names the gap as not yet entered, never as the paper lacking it; a trajectory leads with the measured present, then history, then dissent, and passes no verdict; no mention of tools, records, files, fields, storage, or planning; the language of the scientific community); 1 for one lapse; 0 for more.

Reply with JSON only, each reason at most 25 words: {"grounded": n, "complete": n, "contract": n, "reasons": {"grounded": "...", "complete": "...", "contract": "..."}}

The contract (from the eval's README):
<contract>
%s
</contract>

Question class: %s
Question: %s

Expected answer:
<expected>
%s
</expected>

The system's answer:
<answer>
%s
</answer>
"""


def judge(client, model, contract, record, question):
  expected = question.get('expected') or {}
  prompt = JUDGE_PROMPT % (
    contract, question['class'], question['question'],
    expected.get('answer', '(a refusal: ' + str(expected.get('refusal')) + ')'),
    record['answer'],
  )
  messages = [{'role': 'user', 'content': prompt}]
  axes = ('grounded', 'complete', 'contract')
  for attempt in range(2):
    response = client.messages.create(
      model=model, max_tokens=2000, messages=messages,
    )
    text = ''.join(b.text for b in response.content if b.type == 'text')
    match = re.search(r'\{.*\}', text, re.S)
    try:
      verdict = json.loads(match.group(0)) if match else None
    except json.JSONDecodeError:
      verdict = None
    if isinstance(verdict, dict) and all(
      isinstance(verdict.get(axis), int) for axis in axes
    ):
      return verdict
    # The judge sometimes writes a reason for an axis and drops its
    # integer; ask once more for all three.
    missing = [a for a in axes if not isinstance((verdict or {}).get(a), int)]
    messages += [
      {'role': 'assistant', 'content': text or '(empty)'},
      {'role': 'user', 'content': (
        f'Your reply omitted the integer score for: {", ".join(missing)}. '
        'Reply again with the complete JSON: all three integer scores and '
        'the three reasons.'
      )},
    ]
  return {'error': text, 'stopReason': response.stop_reason}


def contract_text():
  text = README.read_text()
  start = text.index('## The answer contract')
  end = text.index('## The entries')
  return text[start:end]


def summary(path, grades):
  by_class = collections.defaultdict(lambda: {'n': 0, 'mechanical': 0, 'judge': 0})
  for grade in grades:
    row = by_class[grade['class']]
    row['n'] += 1
    if not grade['failures']:
      row['mechanical'] += 1
    j = grade.get('judge') or {}
    if all(j.get(axis) == 2 for axis in ('grounded', 'complete', 'contract')):
      row['judge'] += 1
  lines = [f'# Grades for `{path.name}`', '']
  lines.append('| class | questions | mechanical pass | judge 2/2/2 |')
  lines.append('|---|---|---|---|')
  for cls, row in sorted(by_class.items()):
    lines.append(f"| {cls} | {row['n']} | {row['mechanical']} | {row['judge']} |")
  lines.append('')
  lines.append('## Failures and low scores')
  lines.append('')
  for grade in grades:
    j = grade.get('judge') or {}
    low = {a: j[a] for a in ('grounded', 'complete', 'contract') if j.get(a, 2) < 2}
    if not grade['failures'] and not low and not grade.get('notes'):
      continue
    lines.append(f"### {grade['id']} ({grade['class']})")
    lines.append('')
    lines.append(f"Q: {grade['question']}")
    lines.append('')
    for failure in grade['failures']:
      lines.append(f'- mechanical: {failure}')
    for note in grade.get('notes') or ():
      lines.append(f'- note: {note}')
    for axis, score in low.items():
      lines.append(f"- judge {axis} {score}: {j.get('reasons', {}).get(axis, '')}")
    lines.append('')
    lines.append('> ' + (grade['answer'] or '').strip().replace('\n', '\n> '))
    lines.append('')
  return '\n'.join(lines) + '\n'


def main(argv):
  parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
  parser.add_argument('run', type=pathlib.Path)
  parser.add_argument('--judge', default='claude-opus-5')
  parser.add_argument('--no-judge', action='store_true')
  args = parser.parse_args(argv)

  with open(QUESTIONS) as fd:
    questions = {q['id']: q for q in yaml.safe_load(fd)}
  store = ClaimStore()
  records = load_jsonl(args.run)

  client = None
  contract = None
  if not args.no_judge:
    import anthropic
    from eval_run import api_key  # noqa: E402
    client = anthropic.Anthropic(api_key=api_key())
    contract = contract_text()

  grades = []
  for record in records:
    question = questions[record['id']]
    grade = {
      'id': record['id'],
      'class': record['class'],
      'question': record['question'],
      'answer': record['answer'],
    }
    grade['failures'], grade['notes'] = mechanical(record, question, store)
    if client is not None:
      grade['judge'] = judge(client, args.judge, contract, record, question)
      grade['judgeModel'] = args.judge
    grades.append(grade)
    status = 'ok ' if not grade['failures'] else 'FAIL'
    scores = grade.get('judge') or {}
    print(f"{grade['id']} {status} "
          f"{scores.get('grounded', '-')}/{scores.get('complete', '-')}/{scores.get('contract', '-')} "
          + '; '.join(grade['failures']))

  grades_path = args.run.with_suffix('.grades.jsonl')
  with open(grades_path, 'w') as fd:
    for grade in grades:
      fd.write(json.dumps(grade, ensure_ascii=False) + '\n')
  summary_path = args.run.with_suffix('.md')
  summary_path.write_text(summary(args.run, grades))
  print(f'-> {grades_path}\n-> {summary_path}')
  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
