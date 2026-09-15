#!/usr/bin/env python3
"""Grade a run of the eval: mechanical checks over compositions, a judge on request.

    poetry run python scripts/eval_grade.py eval/runs/2026-09-12-claude-sonnet-5.jsonl
    poetry run python scripts/eval_grade.py <run> --judge claude-opus-5

An answer is a composition: a header, blocks the tools returned, and
perhaps a question back. An expected answer is the blocks it is made
of (a tool and the parameters that matter; alternatives under `anyOf`)
and the strings the rendered answer must show. The mechanical checks,
all on by default:

- a composition exists and every block id in it came from this
  conversation;
- text the model wrote beside its calls or its submission is noted,
  never failed: the reader never sees it;
- the header and any question contain no leak of internals and no
  verdict;
- shapes: for one of the expected alternatives, every expected block
  is matched by a composed block of the same tool whose parameters
  agree on every parameter the expectation names (keys and citations
  compared after resolution, lists as sets); extra blocks are not
  failures;
- shows: every expected string appears in the rendered answer, the
  question's and the matched alternative's own.

The checks themselves are `phylohist.evaluation`; this script reads
the run, writes the grades and calls the judge.

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
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import yaml  # noqa: E402

from phylohist.evaluation import mechanical, parse_verdict, previous_judge  # noqa: E402
from phylohist.tools import ClaimStore  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / 'eval' / 'questions.yaml'


def load_jsonl(path):
  with open(path) as fd:
    return [json.loads(line) for line in fd if line.strip()]


JUDGE_PROMPT = (
  'You are grading the header and question of an answer assembled from blocks '
  'of a closed corpus of published taxonomic opinions. The blocks themselves '
  'are computed and are not graded here. Score contract 0, 1 or 2: 2 if the '
  'header states only the parameters chosen (which records the group is, '
  'whether synonyms and rank variants are included, which trees, the year '
  'range) in the language of the scientific community, passes no verdict, and '
  'the question (if any) asks about a genuinely ambiguous parameter; 1 for one '
  'lapse (a summary, a mechanism word, a judgement); 0 for more. Reply with '
  'JSON only: {"contract": n, "reason": "..."} with the reason at most 25 words.'
  """

Question class: %s
Question: %s
Expected answer:
<expected>
%s
</expected>
Header: %s
Question back: %s
"""
)


def judge(client, model, record, question):
  comp = record.get('composition') or {}
  expected = question.get('expected') or {}
  prompt = JUDGE_PROMPT % (
    question['class'],
    question['question'],
    expected.get('answer', '(none written)'),
    comp.get('header') or '(none)',
    comp.get('question') or '(none)',
  )
  # The judge's reasoning counts against max_tokens; a low cap truncates
  # the JSON or leaves no text at all, so the cap is generous and a
  # malformed reply is retried once before it is recorded as an error.
  text = ''
  for _ in range(2):
    response = client.messages.create(
      model=model, max_tokens=4000, messages=[{'role': 'user', 'content': prompt}]
    )
    text = ''.join(b.text for b in response.content if b.type == 'text')
    verdict = parse_verdict(text)
    if verdict is not None:
      return verdict
  return {'error': text}


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
    lines.append(f'| {cls} | {row["n"]} | {row["pass"]} |')
  lines.append('')
  lines.append('## Failures and notes')
  lines.append('')
  for grade in grades:
    if not grade['failures'] and not grade.get('notes'):
      continue
    lines.append(f'### {grade["id"]} ({grade["class"]})')
    lines.append('')
    lines.append(f'Q: {grade["question"]}')
    lines.append('')
    for failure in grade['failures']:
      lines.append(f'- failure: {failure}')
    for note in grade.get('notes') or ():
      lines.append(f'- note: {note}')
    if grade.get('judge'):
      lines.append(
        f'- judge contract {grade["judge"].get("contract")}: {grade["judge"].get("reason", "")}'
      )
    comp = grade.get('composition') or {}
    lines.append('')
    if comp.get('plan'):
      lines.append(f'Plan: {json.dumps(comp["plan"], ensure_ascii=False)}')
      if comp.get('planErrors'):
        lines.append(f'Plan errors: {json.dumps(comp["planErrors"], ensure_ascii=False)}')
    lines.append(f'Header: {comp.get("header", "")}')
    for b in comp.get('blocks') or ():
      lines.append(f'- {b["type"]} {json.dumps(b.get("parameters"), ensure_ascii=False)}')
    if comp.get('question'):
      lines.append(f'Question back: {comp["question"]}')
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

    from phylohist.evaluation import api_key

    key = api_key()
    if not key:
      sys.exit('ANTHROPIC_API_KEY is not set (environment or .env)')
    client = anthropic.Anthropic(api_key=key)

  grades_path = args.run.with_suffix('.grades.jsonl')
  previous = (
    previous_judge(load_jsonl(grades_path), args.judge)
    if args.judge and grades_path.exists()
    else {}
  )
  grades = []
  skipped = [r['id'] for r in records if r['id'] not in questions]
  if skipped:
    print(f'skipped (no longer in the question set): {", ".join(skipped)}')
  for record in records:
    if record['id'] not in questions:
      continue
    question = questions[record['id']]
    failures, notes = mechanical(record, question, store)
    grade = {
      'id': record['id'],
      'class': record['class'],
      'question': record['question'],
      'composition': record.get('composition'),
      'rendered': record.get('rendered'),
      'failures': failures,
      'notes': notes,
    }
    if client is not None:
      grade['judge'] = previous.get(record['id']) or judge(client, args.judge, record, question)
      grade['judgeModel'] = args.judge
    grades.append(grade)
    status = 'ok ' if not failures else 'FAIL'
    print(f'{grade["id"]} {status} ' + '; '.join(failures))

  with open(grades_path, 'w') as fd:
    for grade in grades:
      fd.write(json.dumps(grade, ensure_ascii=False) + '\n')
  summary_path = args.run.with_suffix('.md')
  summary_path.write_text(summary(args.run, grades))
  print(f'-> {grades_path}\n-> {summary_path}')
  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
