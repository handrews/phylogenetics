#!/usr/bin/env python3
"""Answer the eval questions with a model that can only use the four tools.

    poetry run python scripts/eval_run.py --model claude-sonnet-5
    poetry run python scripts/eval_run.py --ids q001 q013 q037
    poetry run python scripts/eval_run.py --resume eval/runs/2026-09-11-claude-sonnet-5.jsonl

One tool-use loop per question over `phylohist.tools`, the system prompt
from `eval/system-prompt.md`, bounded turns. Writes one JSON line per
question to `eval/runs/<date>-<model>.jsonl`: the question, every tool
call with a compact summary of what it returned, the final answer, token
usage and the prompt's hash. Runs are committed: they are the evidence
the write-up rests on. `--resume` skips ids already in the file.

The API key is read from ANTHROPIC_API_KEY, or from a `.env` line of that
name at the repository root; it is never written anywhere.
"""

import argparse
import datetime
import hashlib
import json
import os
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import yaml  # noqa: E402

from phylohist import tools  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / 'eval' / 'questions.yaml'
PROMPT = ROOT / 'eval' / 'system-prompt.md'
RUNS = ROOT / 'eval' / 'runs'

# A tool result larger than this is cut, and the model is told so; the
# cut is recorded on the call.
RESULT_LIMIT = 60_000

# Output budget per reply. The model's own reasoning counts against it,
# so it is well above the length of any answer; a reply that still hits
# it is recorded with stopReason max_tokens.
MAX_TOKENS = 8192


def api_key():
  key = os.environ.get('ANTHROPIC_API_KEY')
  if key:
    return key
  env = ROOT / '.env'
  if env.exists():
    for line in env.read_text().splitlines():
      name, _, value = line.strip().partition('=')
      if name == 'ANTHROPIC_API_KEY' and value:
        return value.strip().strip('"\'')
  sys.exit('ANTHROPIC_API_KEY is not set (environment or .env)')


def summarise(name, result):
  """What the model saw, compactly: keys or ids, never the whole payload."""
  if isinstance(result, list):
    summary = {'count': len(result)}
    if name == 'resolve_name':
      summary['keys'] = [c['key'] for c in result]
    elif name == 'claims_about':
      summary['ids'] = [c['id'] for c in result]
    elif name == 'name_history':
      summary['sources'] = [h['source'] for h in result]
      summary['ids'] = [
        r['id'] for h in result
        for group in ('placements', 'acts', 'acceptances', 'rejections')
        for r in h[group]
      ]
    return summary
  if isinstance(result, dict):
    return {k: result[k] for k in ('source', 'known', 'entered') if k in result}
  return {'value': result}


def run_question(client, model, system, question, max_turns):
  messages = [{'role': 'user', 'content': question['question']}]
  calls = []
  usage = {'input_tokens': 0, 'output_tokens': 0}
  answer = None
  stop = None
  started = time.time()

  for turn in range(max_turns):
    response = client.messages.create(
      model=model,
      max_tokens=MAX_TOKENS,
      system=system,
      tools=tools.TOOL_SPECS,
      messages=messages,
    )
    usage['input_tokens'] += response.usage.input_tokens
    usage['output_tokens'] += response.usage.output_tokens
    stop = response.stop_reason
    messages.append({'role': 'assistant', 'content': response.content})

    tool_uses = [b for b in response.content if b.type == 'tool_use']
    if not tool_uses:
      answer = ''.join(b.text for b in response.content if b.type == 'text')
      break

    results = []
    for block in tool_uses:
      try:
        result = tools.call(block.name, dict(block.input))
        text = json.dumps(result, ensure_ascii=False)
        error = None
      except Exception as exc:  # the model sees the failure, the run records it
        result, text, error = None, json.dumps({'error': str(exc)}), str(exc)
      cut = len(text) > RESULT_LIMIT
      if cut:
        text = text[:RESULT_LIMIT] + '\n[result cut here; ask more narrowly]'
      call = {
        'turn': turn,
        'name': block.name,
        'input': block.input,
        'chars': len(text),
        'result': summarise(block.name, result) if result is not None else None,
      }
      if error:
        call['error'] = error
      if cut:
        call['cut'] = True
      calls.append(call)
      results.append({
        'type': 'tool_result', 'tool_use_id': block.id, 'content': text,
      })
    messages.append({'role': 'user', 'content': results})
  else:
    # The lookups are exhausted: the model answers from what it has, with
    # no tools offered, and the run records that the limit was reached.
    messages.append({'role': 'user', 'content': (
      'You have reached the limit of lookups. Answer now from what the '
      'tools have already returned.'
    )})
    response = client.messages.create(
      model=model,
      max_tokens=MAX_TOKENS,
      system=system,
      messages=messages,
    )
    usage['input_tokens'] += response.usage.input_tokens
    usage['output_tokens'] += response.usage.output_tokens
    answer = ''.join(b.text for b in response.content if b.type == 'text')
    stop = 'max_turns'

  return {
    'id': question['id'],
    'class': question['class'],
    'question': question['question'],
    'model': model,
    'promptSha': hashlib.sha256(system.encode()).hexdigest()[:12],
    'maxTokens': MAX_TOKENS,
    'maxTurns': max_turns,
    'toolCalls': calls,
    'answer': answer,
    'stopReason': stop,
    'usage': usage,
    'seconds': round(time.time() - started, 1),
  }


def main(argv):
  parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
  parser.add_argument('--model', default='claude-sonnet-5')
  parser.add_argument('--ids', nargs='+', help='only these question ids')
  parser.add_argument('--out', type=pathlib.Path, help='run file to write')
  parser.add_argument('--resume', type=pathlib.Path, help='run file to continue')
  parser.add_argument('--max-turns', type=int, default=12)
  args = parser.parse_args(argv)

  import anthropic
  client = anthropic.Anthropic(api_key=api_key())
  system = PROMPT.read_text()
  with open(QUESTIONS) as fd:
    questions = yaml.safe_load(fd)
  if args.ids:
    questions = [q for q in questions if q['id'] in set(args.ids)]

  out = args.resume or args.out or (
    RUNS / f'{datetime.date.today().isoformat()}-{args.model}.jsonl'
  )
  out.parent.mkdir(parents=True, exist_ok=True)
  done = set()
  if args.resume and out.exists():
    with open(out) as fd:
      done = {json.loads(line)['id'] for line in fd if line.strip()}

  with open(out, 'a') as fd:
    for question in questions:
      if question['id'] in done:
        continue
      record = run_question(client, args.model, system, question, args.max_turns)
      fd.write(json.dumps(record, ensure_ascii=False) + '\n')
      fd.flush()
      print(
        f"{record['id']} {record['class']:<12} {len(record['toolCalls'])} calls "
        f"{record['usage']['input_tokens']}+{record['usage']['output_tokens']} tok "
        f"{record['seconds']}s {record['stopReason']}",
      )
  print(f'-> {out}')
  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
