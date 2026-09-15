"""Plans: an answer as the blocks it is made of, executed by code.

A plan is what a planner emits instead of an answer: a one-line header
stating the parameters chosen, the blocks in order (each a tool and the
parameters that matter), and a question back when a parameter is
genuinely ambiguous. It is the same form the eval's expected answers
take. `validate` checks a plan against the tool surface without touching
the corpus; `execute` builds the composition from the corpus and reports
what could not be built.
"""

from . import blocks, tools

# Parameters the planner may not set: the rendering is the caller's.
_NOT_PLANNED = {'style'}


def _specs():
  return {spec['name']: spec for spec in tools.TOOL_SPECS}


PLAN_SPEC = {
  'name': 'plan',
  'description': (
    'Answer with a plan: a one-line header stating the parameters chosen '
    '(which records the group is, whether synonyms and the same name at '
    'other ranks are included, which kinds of tree, the year range); the '
    'blocks in the order they should appear, each a tool name and its '
    'parameters; and a question back only when a parameter is genuinely '
    'ambiguous. Code builds the blocks from the corpus; you do not see '
    'them. Name records by key or as the literature prints the name, and '
    'sources by citation ("Dehm 1961").'
  ),
  'input_schema': {
    'type': 'object',
    'properties': {
      'header': {'type': 'string'},
      'blocks': {
        'type': 'array',
        'items': {
          'type': 'object',
          'properties': {
            'tool': {'type': 'string'},
            'parameters': {'type': 'object'},
          },
          'required': ['tool', 'parameters'],
        },
      },
      'question': {'type': ['string', 'null']},
    },
    'required': ['header', 'blocks'],
  },
}


def validate(plan):
  """Problems with a plan's shape: unknown tools, unknown or missing
  parameters, a tool that returns no block. Empty means well formed."""
  problems = []
  specs = _specs()
  if not isinstance(plan, dict):
    return ['a plan is an object with header, blocks and question']
  if not isinstance(plan.get('blocks'), list):
    problems.append('blocks must be a list')
    return problems
  for i, block in enumerate(plan['blocks']):
    where = f'block {i + 1}'
    if not isinstance(block, dict) or 'tool' not in block:
      problems.append(f'{where}: a block names a tool')
      continue
    spec = specs.get(block['tool'])
    if spec is None:
      problems.append(f"{where}: unknown tool {block['tool']}")
      continue
    if block['tool'] in ('resolve_name', 'resolve_source', 'source_coverage'):
      problems.append(f"{where}: {block['tool']} answers a lookup, not a reader; it is not a block")
      continue
    params = block.get('parameters') or {}
    if not isinstance(params, dict):
      problems.append(f'{where}: parameters must be an object')
      continue
    allowed = set(spec['input_schema']['properties']) | _NOT_PLANNED
    for name, value in params.items():
      if name not in allowed:
        problems.append(f"{where}: {block['tool']} has no parameter {name}")
        continue
      schema = spec['input_schema']['properties'].get(name) or {}
      if not _type_ok(value, schema):
        problems.append(
          f"{where}: {block['tool']} {name} must be {_type_words(schema)}, "
          f"not {value!r}; leave it out for the default"
        )
    for name in spec['input_schema'].get('required', ()):
      if name not in params:
        problems.append(f"{where}: {block['tool']} needs {name}")
  return problems


_TYPES = {
  'string': str, 'integer': int, 'number': (int, float), 'boolean': bool,
  'array': list, 'object': dict, 'null': type(None),
}


def _type_ok(value, schema):
  kinds = schema.get('type')
  if kinds is None:
    return True
  kinds = kinds if isinstance(kinds, list) else [kinds]
  for kind in kinds:
    expected = _TYPES.get(kind)
    if expected is None:
      return True
    if isinstance(value, bool) and kind != 'boolean':
      continue
    if isinstance(value, expected):
      if kind == 'array' and schema.get('items'):
        return all(_type_ok(v, schema['items']) for v in value)
      return True
  return False


def _type_words(schema):
  kinds = schema.get('type')
  kinds = kinds if isinstance(kinds, list) else [kinds]
  words = {'string': 'a string', 'integer': 'an integer', 'boolean': 'true or false',
           'array': 'a list', 'object': 'an object', 'null': 'omitted'}
  said = [words.get(k, k) for k in kinds if k != 'null']
  if schema.get('description'):
    return (' or '.join(said) or 'omitted') + f" ({schema['description']})"
  return ' or '.join(said) or 'omitted'


def execute(plan, style='text'):
  """Build a plan's composition from the corpus. Returns ``{composition,
  blocks, errors}``: the composition (None when nothing could be
  built), the blocks in order each carrying the tool and parameters
  that produced it, and one error per block that could not be built
  (an ambiguous name or citation, a bad parameter) with its message."""
  problems = validate(plan)
  if problems:
    return {'composition': None, 'blocks': [], 'errors': [{'block': None, 'error': p} for p in problems]}
  built, errors = [], []
  for i, spec in enumerate(plan['blocks']):
    params = {k: v for k, v in (spec.get('parameters') or {}).items() if k not in _NOT_PLANNED}
    try:
      result = tools.call(spec['tool'], dict(params, style='json'))
    except (ValueError, KeyError, TypeError) as exc:
      errors.append({'block': i + 1, 'tool': spec['tool'], 'parameters': params, 'error': str(exc)})
      continue
    got = result if isinstance(result, list) else [result]
    got = [b for b in got if isinstance(b, dict) and 'blockId' in b]
    if not got:
      errors.append({'block': i + 1, 'tool': spec['tool'], 'parameters': params,
                     'error': 'returned no block; the corpus holds nothing for these parameters'})
      continue
    for b in got:
      built.append(dict(b, _tool=spec['tool']))
  composition = (blocks.compose(built, plan.get('header') or '', plan.get('question'))
                 if built else None)
  return {
    'composition': composition,
    'blocks': [{
      'blockId': b['blockId'], 'type': b['type'], 'tool': b['_tool'],
      'parameters': b.get('parameters'), 'claims': b['claims'],
    } for b in built],
    'errors': errors,
  }
