#!/usr/bin/env python3
"""Answer the eval questions with a model that composes blocks the tools return.

    poetry run python scripts/eval_run.py --model claude-sonnet-5
    poetry run python scripts/eval_run.py --ids q001 q013 q037
    poetry run python scripts/eval_run.py --resume eval/runs/2026-09-12-claude-sonnet-5.jsonl
    poetry run python scripts/eval_run.py --ask "Who first placed Rhenopyrgus under Edrioblastoidina?"
    poetry run python scripts/eval_run.py --mode planner --model claude-sonnet-5

Two modes. In `compose` mode (the default) the model works one
tool-use loop per question over `phylohist.tools`, with the system
prompt from `eval/system-prompt.md` and bounded turns: it sees each
block's id, type and rendered text and finishes by calling `submit`
with a header, the block ids in order, and optionally a question back.
In `planner` mode (`eval/planner-prompt.md`) it may call only the two
resolvers, then it calls `plan` with the header, the blocks as tool and
parameters, and the question; `phylohist.plan.execute` builds the
composition, and errors (an ambiguous name, a citation the corpus
lacks) go back once for a revised plan. In compose mode the
runner keeps every block by id, validates the submission against them,
renders the composition, and writes one JSON line per question to
`eval/runs/<date>-<model>.jsonl`: the question, every tool call with a
compact summary of what it returned, the composition (header, blocks
with their types, parameters and claim ids, question, any invalid ids,
any free text, each with its turn and whether that turn called submit),
the rendered answer, token usage and the prompt's hash.
Runs are committed. `--resume` skips ids already in the file. `--ask`
answers one question typed on the command line the same way and prints
the rendered answer with the lookups it took; nothing is written.

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

from phylohist import blocks, plan as plans, tools  # noqa: E402
from phylohist.render import render_composition  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / 'eval' / 'questions.yaml'
PROMPT = ROOT / 'eval' / 'system-prompt.md'
PLANNER_PROMPT = ROOT / 'eval' / 'planner-prompt.md'
RESOLVERS = ('resolve_name', 'resolve_source')
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


def run_question(client, model, system, question, max_turns, mode='compose'):
  messages = [{'role': 'user', 'content': question['question']}]
  calls = []
  kept = {}
  usage = {'input_tokens': 0, 'output_tokens': 0}
  started = time.time()
  composition = None
  free_text = []
  stop = None
  asked_to_compose = False
  revised = False
  finish = 'plan' if mode == 'planner' else 'submit'
  if mode == 'planner':
    specs = [s for s in tools.TOOL_SPECS if s['name'] in RESOLVERS] + [plans.PLAN_SPEC]
  else:
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
        'You have reached the limit of lookups. State your plan now.'
        if mode == 'planner' else
        'You have reached the limit of lookups. Compose your answer now '
        'with submit from the blocks already returned.'
      )})
      response = create(tool_choice={'type': 'tool', 'name': finish})
    else:
      response = create()
    stop = response.stop_reason
    messages.append({'role': 'assistant', 'content': response.content})
    text = _text_of(response.content).strip()
    tool_uses = [b for b in response.content if b.type == 'tool_use']
    if text:
      free_text.append({
        'turn': turn, 'text': text,
        'withSubmit': any(b.name == finish for b in tool_uses),
      })

    if not tool_uses:
      if asked_to_compose or forced:
        break
      asked_to_compose = True
      messages.append({'role': 'user', 'content': (
        'State your plan with the plan tool: a one-line header and the '
        'blocks to show, in order.'
        if mode == 'planner' else
        'Compose your answer with the submit tool: a one-line header and '
        'the ids of the blocks to show, in order.'
      )})
      turn += 1
      continue

    results = []
    for block in tool_uses:
      if block.name == 'submit' and mode != 'planner':
        composition = _submit(dict(block.input), kept)
        calls.append({'turn': turn, 'name': 'submit', 'input': block.input})
        results.append({'type': 'tool_result', 'tool_use_id': block.id, 'content': 'submitted'})
        continue
      if block.name == 'plan' and mode == 'planner':
        payload = dict(block.input)
        outcome = plans.execute(payload)
        calls.append({'turn': turn, 'name': 'plan', 'input': payload, 'errors': outcome['errors']})
        if outcome['errors'] and not revised and not forced:
          # The plan comes back once with what could not be built.
          revised = True
          results.append({'type': 'tool_result', 'tool_use_id': block.id, 'content': json.dumps(
            {'errors': outcome['errors'], 'note': 'name what is ambiguous and plan again'},
            ensure_ascii=False)})
          continue
        composition = {
          'header': payload.get('header') or '', 'question': payload.get('question'),
          'blocks': outcome['blocks'], 'invalidIds': [], 'composition': outcome['composition'],
          'plan': payload, 'planErrors': outcome['errors'],
        }
        results.append({'type': 'tool_result', 'tool_use_id': block.id, 'content': 'planned'})
        continue
      if mode == 'planner' and block.name not in RESOLVERS:
        results.append({'type': 'tool_result', 'tool_use_id': block.id,
                        'content': json.dumps({'error': f'{block.name} is not available: put it in the plan'})})
        calls.append({'turn': turn, 'name': block.name, 'input': block.input, 'error': 'not available in planner mode'})
        continue
      try:
        result = tools.call(block.name, dict(block.input))
        error = None
      except Exception as exc:  # the model sees the failure, the run records it
        result, error = None, str(exc)
      if result is not None:
        for b in (result if isinstance(result, list) else [result]):
          if _is_block(b):
            kept[b['blockId']] = dict(b, _tool=block.name)
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
    'mode': mode,
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
      **({'plan': composition['plan'], 'planErrors': composition['planErrors']} if 'plan' in composition else {}),
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
      'blockId': b['blockId'], 'type': b['type'], 'tool': b.get('_tool'),
      'parameters': b.get('parameters'), 'claims': b['claims'],
    } for b in chosen],
    'invalidIds': invalid,
    'composition': composed,
  }


def ask(client, model, system, text, max_turns, mode='compose'):
  """One question from the command line: the answer as the reader would
  see it, then the trail (lookups, the plan in planner mode, header,
  question back, any text the model wrote beside its calls, tokens)."""
  question = {'id': 'ask', 'class': 'ask', 'question': text}
  record = run_question(client, model, system, question, max_turns, mode)
  comp = record.get('composition')
  print(record['rendered'] if comp else '(no composition)')
  print()
  print('--- trail')
  for call in record['toolCalls']:
    if call['name'] == 'submit':
      continue
    if call['name'] == 'plan':
      print(f"  plan {json.dumps(call['input'], ensure_ascii=False)}")
      if call.get('errors'):
        print(f"  plan errors: {json.dumps(call['errors'], ensure_ascii=False)}")
      continue
    result = call.get('result') or {}
    got = (f"{len(result['blocks'])} block(s)" if 'blocks' in result
           else f"{result.get('count', '')} candidate(s)" if 'count' in result
           else 'error: ' + call['error'] if call.get('error') else '')
    print(f"  {call['name']} {json.dumps(call['input'], ensure_ascii=False)} -> {got}")
  if comp:
    print(f"  header: {comp['header']}")
    if comp.get('question'):
      print(f"  question back: {comp['question']}")
    for entry in comp.get('freeText') or ():
      where = 'beside the submission' if entry.get('withSubmit') else 'between lookups'
      print(f"  text {where}: {entry['text']}")
    if comp.get('invalidIds'):
      print(f"  invalid block ids: {comp['invalidIds']}")
  else:
    print('  ' + (record['answer'] or '(nothing)'))
  print(f"  {record['usage']['input_tokens']}+{record['usage']['output_tokens']} tokens, "
        f"{record['seconds']}s, {record['stopReason']}")
  return 0


def main(argv):
  parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
  parser.add_argument('--model', default='claude-sonnet-5')
  parser.add_argument('--ids', nargs='+', help='only these question ids')
  parser.add_argument('--out', type=pathlib.Path, help='run file to write')
  parser.add_argument('--resume', type=pathlib.Path, help='run file to continue')
  parser.add_argument('--max-turns', type=int, default=12)
  parser.add_argument('--ask', metavar='QUESTION', help='answer this one question and print it; write nothing')
  parser.add_argument('--mode', choices=('compose', 'planner'), default='compose',
                      help='compose: the model reads blocks and submits ids; planner: it states a plan')
  args = parser.parse_args(argv)

  import anthropic
  client = anthropic.Anthropic(api_key=api_key())
  system = (PLANNER_PROMPT if args.mode == 'planner' else PROMPT).read_text()
  if args.ask:
    return ask(client, args.model, system, args.ask, args.max_turns, args.mode)
  with open(QUESTIONS) as fd:
    questions = yaml.safe_load(fd)
  if args.ids:
    questions = [q for q in questions if q['id'] in set(args.ids)]

  tag = '-planner' if args.mode == 'planner' else ''
  out = args.resume or args.out or (
    RUNS / f'{datetime.date.today().isoformat()}{tag}-{args.model}.jsonl'
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
      record = run_question(client, args.model, system, question, args.max_turns, args.mode)
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
