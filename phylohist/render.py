"""Rendering blocks: a registry of styles, each a function per block type.

`render(block, style)` looks up ``(block type, style)``. Two styles ship:
``text`` (the classification as the old CLI drew it: two-space indent,
``*`` new, ``?`` provisional and questionable, brackets for a
placeholder, ``=`` lines for synonyms; tables as aligned columns; lists
and statements as lines) and ``markdown`` (tables as Markdown, the tree
in a fenced block, lists as bullets). ``json`` is the block itself.

Adding a style is a function and a registration: intended additions are
a modern "Systematic Paleontology" listing for classifications, and a
graph and a timeline for tables (the block keeps sources, years and keys
on every cell, so both can be drawn from the model as it is).
"""

import json

STYLES = {}


def style(name, block_type):
  def register(fn):
    STYLES[(block_type, name)] = fn
    return fn
  return register


def styles():
  return sorted({name for _, name in STYLES} | {'json'})


def render(block, name='text'):
  if name == 'json':
    return json.dumps(block, ensure_ascii=False, indent=1)
  fn = STYLES.get((block['type'], name))
  if fn is None:
    raise KeyError(f'no {name} rendering for a {block["type"]} block')
  return fn(block)


def render_composition(composition, name='text'):
  parts = []
  if composition.get('header'):
    parts.append(composition['header'])
  for block in composition['blocks']:
    parts.append(render(block, name))
  if composition.get('question'):
    parts.append(f'Question: {composition["question"]}')
  return '\n\n'.join(parts)


# -- shared pieces ---------------------------------------------------------

def _node_label(node):
  name = node['name'] if node.get('name') else f"[{node['key']}]"
  if node.get('rank') == 'subgenus':
    name = f'({name})'
  if (node.get('flags') or {}).get('quoted'):
    name = f'"{name}"'
  if (node.get('flags') or {}).get('new'):
    name += '*'
  if (node.get('flags') or {}).get('questionable'):
    name += ' ?'
  return name


def _cell_text(cell):
  values = []
  for v in cell:
    value = v.get('value') if isinstance(v, dict) else v
    if isinstance(value, (list, tuple)):
      value = ', '.join(str(x) for x in value)
    values.append('' if value is None else str(value))
  return ' / '.join(values)


def _entry_line(entry, heading_name=None):
  parts = [str(entry.get('year') or '')]
  name = entry.get('name') or heading_name
  if entry.get('parents') and name:
    parts.append(' '.join(entry['parents']) + ' ' + name)
  elif entry.get('parents'):
    parts.append(' '.join(entry['parents']))
  elif entry.get('name'):
    parts.append(entry['name'])
  if entry.get('printed'):
    parts.append(f'"{entry["printed"]}"')
  parts.append(entry.get('cite') or entry.get('source') or '')
  if entry.get('page') is not None:
    parts.append(f'p. {entry["page"]}')
  if entry.get('stance') == 'rejects':
    parts.append('(non)')
  return ' '.join(p for p in parts if p)


def _statement_text(block):
  kind = block['kind']
  f = block['fields']
  if kind == 'gap':
    what = f.get('what', 'this kind of statement')
    bare = what[4:] if what.startswith('the ') else what
    plural = f.get('plural', False)
    if not f.get('entered', True):
      return (f"{f['cite']} is on record; its content has not yet been "
              f"entered, so nothing it prints about {bare} can be reported yet.")
    declared = f.get('declared')
    if declared in ('none', 'partly'):
      extent = 'none' if declared == 'none' else 'only part'
      return (f"{what[0].upper() + what[1:]} printed in {f['cite']} "
              f"{'have' if plural else 'has'} not yet been entered "
              f"({extent} of {'them' if plural else 'it'} is entered so far).")
    if declared == 'na':
      return f"{f['cite']} prints no {bare}, as reviewed."
    if declared == 'all':
      return (f"{what[0].upper() + what[1:]} printed in {f['cite']} "
              f"{'are' if plural else 'is'} entered in full.")
    return f"How much of {what} in {f['cite']} is entered has not been reviewed."
  if kind == 'printedForm':
    return (f"{f['cite']}{', p. ' + str(f['page']) if f.get('page') is not None else ''}"
            f" prints \"{f['printed']}\"" +
            (f" for {f['name']}" if f.get('name') else '') + '.')
  if kind == 'absent':
    return f"No source in the corpus mentions {f['name']}."
  return json.dumps(f, ensure_ascii=False)


# -- text ------------------------------------------------------------------

@style('text', 'classification')
def _text_classification(block):
  lines = []
  for node in block['nodes']:
    indent = '  ' * node.get('depth', 0)
    if (node.get('flags') or {}).get('provisional') and indent:
      indent = indent[:-2] + '? '
    lines.append(indent + _node_label(node))
    for entry in node.get('synonymy') or ():
      lines.append(indent + '  = ' + _entry_line(entry, node.get('name')))
  return '\n'.join(lines)


@style('text', 'table')
def _text_table(block):
  headers = [c['name'] for c in block['columns']]
  body = [[_cell_text(cell) for cell in row['cells']] for row in block['rows']]
  widths = [
    max([len(h)] + [len(r[i]) for r in body]) for i, h in enumerate(headers)
  ]
  def fmt(values):
    return '  '.join(v.ljust(w) for v, w in zip(values, widths)).rstrip()
  lines = []
  if block.get('title'):
    lines.append(block['title'])
  lines += _decoration_lines(block.get('decorations') or {})
  lines.append(fmt(headers))
  lines.append(fmt(['-' * w for w in widths]))
  current = None
  for row, cells in zip(block['rows'], body):
    if row.get('group') is not None and row['group'] != current:
      current = row['group']
      lines.append(f'-- {current} --')
    lines.append(fmt(cells))
  return '\n'.join(lines)


def _decoration_lines(decorations):
  lines = []
  for key, value in decorations.items():
    if isinstance(value, list):
      value = '; '.join(str(v) for v in value)
    lines.append(f'{key}: {value}')
  return lines


@style('text', 'list')
def _text_list(block):
  heading = block['heading']
  title = heading.get('name') or f"[{heading['key']}]"
  if heading.get('rank'):
    title += f" ({heading['rank']})"
  lines = [title]
  for entry in block['entries']:
    lines.append('  ' + _entry_line(entry, heading.get('name')))
  return '\n'.join(lines)


@style('text', 'statement')
def _text_statement(block):
  return _statement_text(block)


# -- markdown --------------------------------------------------------------

@style('markdown', 'classification')
def _md_classification(block):
  return '```\n' + _text_classification(block) + '\n```'


@style('markdown', 'table')
def _md_table(block):
  headers = [c['name'] for c in block['columns']]
  lines = []
  if block.get('title'):
    lines.append(f"**{block['title']}**")
    lines.append('')
  deco = _decoration_lines(block.get('decorations') or {})
  if deco:
    lines += deco
    lines.append('')
  lines.append('| ' + ' | '.join(headers) + ' |')
  lines.append('|' + '---|' * len(headers))
  current = None
  for row in block['rows']:
    if row.get('group') is not None and row['group'] != current:
      current = row['group']
      lines.append('| ' + f'**{current}**' + ' |' * len(headers))
    cells = [_cell_text(cell).replace('|', '\\|') for cell in row['cells']]
    lines.append('| ' + ' | '.join(cells) + ' |')
  return '\n'.join(lines)


@style('markdown', 'list')
def _md_list(block):
  heading = block['heading']
  title = heading.get('name') or f"[{heading['key']}]"
  if heading.get('rank'):
    title += f" ({heading['rank']})"
  lines = [f'**{title}**', '']
  for entry in block['entries']:
    lines.append('- ' + _entry_line(entry, heading.get('name')))
  return '\n'.join(lines)


@style('markdown', 'statement')
def _md_statement(block):
  return _statement_text(block)
