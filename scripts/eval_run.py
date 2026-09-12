#!/usr/bin/env python3
"""Answer the eval questions with a model that composes blocks the tools return.

    poetry run python scripts/eval_run.py --model claude-sonnet-5
    poetry run python scripts/eval_run.py --ids q001 q013 q037
    poetry run python scripts/eval_run.py --resume eval/runs/2026-09-12-claude-sonnet-5.jsonl

One tool-use loop per question over `phylohist.tools`, the system prompt
from `eval/system-prompt.md`, bounded turns. The model sees each block's
id, type and rendered text; it finishes by calling `submit` with a
header, the block ids in order, and optionally a question back. The
runner keeps every block by id, validates the submission against them,
renders the composition, and writes one JSON line per question to
`eval/runs/<date>-<model>.jsonl`: the question, every tool call with a
compact summary of what it returned, the composition (header, blocks
with their types, parameters and claim ids, question, any invalid ids,
any free text, each with its turn and whether that turn called submit),
the rendered answer, token usage and the prompt's hash.
Runs are committed. `--resume` skips ids already in the file.

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

from phylohist import blocks, tools  # noqa: E402
from phylohist.render import render_composition  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / 'eval' / 'questions.yaml'
PROMPT = ROOT / 'eval' / 'system-prompt.md'
RUNS = ROOT / 'eval' / 'runs'

# A tool result larger than this is cut, and the model is told so.
RESULT_LIMIT = 60_000
# Output budget per reply; the model's reasoning counts against it.
MAX_TOKENS = 8192

SUBMIT_SPEC = {
  'name': 'submit',
  'description': (
    'Finish: compose the answer from blocks the tools returned in this '
    'conversation. The header is one line stating the parameters chosen '
    '(which records the group is, whether synonyms and the same name at '
    'other ranks are included, which kinds of tree, the year range); the '
    'blocks are ids in the order they should appear; the question is asked '
    'only when a parameter is genuinely ambiguous. No other text.'
  ),
  'input_schema': {
    'type': 'object',
    'properties': {
      'header': {'type': 'string'},
      'blocks': {'type': 'array', 'items': {'type': 'string'}},
      'question': {'type': ['string', 'null']},
    },
    'required': ['header', 'blocks'],
  },
}


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


def _is_block(value):
  return isinstance(value, dict) and 'blockId' in value


def compact(result):
  """What the model sees of a tool result: for blocks, the id, type,
  title and rendered text; for the resolver and coverage, the dict."""
  if isinstance(result, list) and result and _is_block(result[0]):
    return [compact(b) for b in result]
  if _is_block(result):
    view = {'blockId': result['blockId'], 'type': result['type']}
    if result.get('title'):
      view['title'] = result['title']
    if result.get('cite'):
      view['source'] = result['cite']
    view['rendered'] = result.get('rendered', '')
    return view
  return result


def summarise(name, result):
  """What the run records of a tool result: block ids and types, or keys."""
  if isinstance(result, list) and result and _is_block(result[0]):
    return {'blocks': [{'blockId': b['blockId'], 'type': b['type'], 'claims': len(b['claims'])} for b in result]}
  if _is_block(result):
    return {'blocks': [{'blockId': result['blockId'], 'type': result['type'], 'claims': len(result['claims'])}]}
  if isinstance(result, list):
    return {'count': len(result), 'keys': [c.get('key') for c in result if isinstance(c, dict)]}
  if isinstance(result, dict):
    return {k: result[k] for k in ('source', 'known', 'entered') if k in result}
  return {'value': result}


def _text_of(content):
  return ''.join(b.text for b in content if getattr(b, 'type', None) == 'text')


def run_question(client, model, system, question, max_turns):
  messages = [{'role': 'user', 'content': question['question']}]
  calls = []
  kept = {}
  usage = {'input_tokens': 0, 'output_tokens': 0}
  started = time.time()
  composition = None
  free_text = []
  stop = None
  asked_to_compose = False
  specs = tools.TOOL_SPECS + [SUBMIT_SPEC]

  def create(**extra):
    response = client.messages.create(
      model=model, max_tokens=MAX_TOKENS, system=system, tools=specs,
      messages=messages, **extra,
    )
    usage['input_tokens'] += response.usage.input_tokens
    usage['output_tokens'] += response.usage.output_tokens
    return response

  turn = 0
  while turn < max_turns + 2 and composition is None:
    forced = turn >= max_turns
    if forced:
      messages.append({'role': 'user', 'content': (
        'You have reached the limit of lookups. Compose your answer now '
        'with submit from the blocks already returned.'
      )})
      response = create(tool_choice={'type': 'tool', 'name': 'submit'})
    else:
      response = create()
    stop = response.stop_reason
    messages.append({'role': 'assistant', 'content': response.content})
    text = _text_of(response.content).strip()
    tool_uses = [b for b in response.content if b.type == 'tool_use']
    if text:
      free_text.append({
        'turn': turn, 'text': text,
        'withSubmit': any(b.name == 'submit' for b in tool_uses),
      })

    if not tool_uses:
      if asked_to_compose or forced:
        break
      asked_to_compose = True
      messages.append({'role': 'user', 'content': (
        'Compose your answer with the submit tool: a one-line header and '
        'the ids of the blocks to show, in order.'
      )})
      turn += 1
      continue

    results = []
    for block in tool_uses:
      if block.name == 'submit':
        composition = _submit(dict(block.input), kept)
        calls.append({'turn': turn, 'name': 'submit', 'input': block.input})
        results.append({'type': 'tool_result', 'tool_use_id': block.id, 'content': 'submitted'})
        continue
      try:
        result = tools.call(block.name, dict(block.input))
        error = None
      except Exception as exc:  # the model sees the failure, the run records it
        result, error = None, str(exc)
      if result is not None:
        for b in (result if isinstance(result, list) else [result]):
          if _is_block(b):
            kept[b['blockId']] = b
        text_out = json.dumps(compact(result), ensure_ascii=False)
      else:
        text_out = json.dumps({'error': error})
      cut = len(text_out) > RESULT_LIMIT
      if cut:
        text_out = text_out[:RESULT_LIMIT] + '\n[result cut here; ask more narrowly]'
      call = {
        'turn': turn, 'name': block.name, 'input': block.input,
        'chars': len(text_out),
        'result': summarise(block.name, result) if result is not None else None,
      }
      if error:
        call['error'] = error
      if cut:
        call['cut'] = True
      calls.append(call)
      results.append({'type': 'tool_result', 'tool_use_id': block.id, 'content': text_out})
    if composition is None:
      messages.append({'role': 'user', 'content': results})
    turn += 1

  if composition is not None:
    composition['freeText'] = free_text
    rendered = render_composition(composition['composition'], 'text') if composition['composition'] else ''
  else:
    rendered = ''

  record = {
    'id': question['id'],
    'class': question['class'],
    'question': question['question'],
    'model': model,
    'promptSha': hashlib.sha256(system.encode()).hexdigest()[:12],
    'maxTokens': MAX_TOKENS,
    'maxTurns': max_turns,
    'toolCalls': calls,
    'composition': composition and {
      'header': composition['header'],
      'question': composition['question'],
      'blocks': composition['blocks'],
      'invalidIds': composition['invalidIds'],
      'freeText': composition['freeText'],
      'compositionId': composition['composition']['compositionId'] if composition['composition'] else None,
    },
    'rendered': rendered,
    'answer': rendered if composition else '\n\n'.join(f['text'] for f in free_text),
    'stopReason': 'max_turns' if turn > max_turns else stop,
    'usage': usage,
    'seconds': round(time.time() - started, 1),
  }
  if composition is None:
    record['noComposition'] = True
  return record


def _submit(payload, kept):
  ids = list(payload.get('blocks') or [])
  chosen = [kept[i] for i in ids if i in kept]
  invalid = [i for i in ids if i not in kept]
  composed = blocks.compose(chosen, payload.get('header') or '', payload.get('question')) if chosen or not invalid else None
  return {
    'header': payload.get('header') or '',
    'question': payload.get('question'),
    'blocks': [{
      'blockId': b['blockId'], 'type': b['type'], 'parameters': b.get('parameters'),
      'claims': b['claims'],
    } for b in chosen],
    'invalidIds': invalid,
    'composition': composed,
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
      comp = record.get('composition') or {}
      print(
        f"{record['id']} {record['class']:<12} {len(record['toolCalls'])} calls "
        f"{record['usage']['input_tokens']}+{record['usage']['output_tokens']} tok "
        f"{record['seconds']}s {record['stopReason']} "
        f"{len(comp.get('blocks') or [])} blocks"
        + (' NO COMPOSITION' if record.get('noComposition') else '')
        + (f" invalid={comp['invalidIds']}" if comp.get('invalidIds') else ''),
      )
  print(f'-> {out}')
  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
