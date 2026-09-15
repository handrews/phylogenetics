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

from . import blocks

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

_SPECIES_GROUP_WORDS = ('species', 'subspecies', 'variety')


def node_label(node):
  """A heading as a Systematic Paleontology section prints it: the rank
  word above the species level, the name, the source's mark for a new
  taxon, the acts in the community's abbreviations."""
  name = node.get('label') or (node['name'] if node.get('name') else f"[{node['key']}]")
  if (node.get('flags') or {}).get('quoted'):
    name = f'"{name}"'
  if node.get('or'):
    name += ' or ' + ' or '.join(node['or'])
  rank_word = node.get('rankWord')
  if rank_word and rank_word.lower() not in _SPECIES_GROUP_WORDS and not node.get('placeholder'):
    name = f'{rank_word} {name}'
  if (node.get('flags') or {}).get('new'):
    mark = node.get('newMark') or blocks.new_mark(rank_word)
    # An open-nomenclature name already ends in "sp."; the mark completes it.
    if name.endswith(' sp.') and mark.startswith('sp. '):
      name = name[:-4]
    name += ' ' + mark
  if (node.get('flags') or {}).get('questionable'):
    name += ' ?'
  for act in node.get('acts') or ():
    kind = act.get('act')
    mark = blocks.ACT_MARKS.get(kind)
    if kind in ('moved', 'removed'):
      mark = f"({act.get('words')})"
    if mark:
      name += ' ' + mark + (' (inferred)' if act.get('inferred') else '')
  return name


def _cell_text(cell, sep=' / '):
  values = []
  for v in cell:
    value = v.get('value') if isinstance(v, dict) else v
    if isinstance(value, (list, tuple)):
      value = ', '.join(str(x) for x in value)
    values.append('' if value is None else str(value))
  return sep.join(values)


def pages_text(value):
  """Pages as the community writes them: "p. 118", "pp. 120–122",
  "pp. 242–245, 253"; a phrase such as "cited p. 58" as it is."""
  if value is None:
    return ''
  if isinstance(value, str):
    return value
  items = value if isinstance(value, list) else [value]
  words = []
  for item in items:
    if isinstance(item, list) and len(item) == 2:
      words.append(f'{item[0]}–{item[1]}')
    else:
      words.append(str(item))
  single = len(items) == 1 and not isinstance(items[0], list)
  return ('p. ' if single else 'pp. ') + ', '.join(words)


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
  if entry.get('kind') == 'heading':
    parts.append('(the heading as entered; no verbatim form is recorded)')
  parts.append(entry.get('cite') or entry.get('source') or '')
  if entry.get('page') is not None:
    parts.append(pages_text(entry['page']))
  if entry.get('stance') == 'rejects':
    parts.append('(non)')
  return ' '.join(p for p in parts if p)


def _gap_sentence(f):
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


def _also_sentence(also):
  """The source's other kinds not fully entered, in one sentence: "Its
  synonymy is entered in part; its diagnoses and material have not yet
  been entered."
  """
  def words(items):
    bare = [i['what'][4:] if i['what'].startswith('the ') else i['what'] for i in items]
    joined = bare[0] if len(bare) == 1 else ', '.join(bare[:-1]) + ' and ' + bare[-1]
    plural = len(items) > 1 or items[0].get('plural', False)
    return joined, plural
  clauses = []
  partly = [i for i in also if i['declared'] == 'partly']
  none = [i for i in also if i['declared'] == 'none']
  if partly:
    joined, plural = words(partly)
    clauses.append(f"its {joined} {'are' if plural else 'is'} entered in part")
  if none:
    joined, plural = words(none)
    clauses.append(f"its {joined} {'have' if plural else 'has'} not yet been entered")
  text = '; '.join(clauses)
  return text[0].upper() + text[1:] + '.'


def _statement_text(block):
  kind = block['kind']
  f = block['fields']
  if kind == 'gap':
    text = _gap_sentence(f)
    if f.get('about') and f.get('entered', True):
      text = f"Nothing about {f['about']} is entered from {f['cite']}. " + text
    if f.get('also'):
      text += ' ' + _also_sentence(f['also'])
    return text
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
  # The source above its tree, the tree indented under it, so a list of
  # listings reads source by source.
  lines = []
  if block.get('cite'):
    # The source, with the page the listing starts on when it is recorded.
    head = block['cite']
    root_pages = (block['nodes'][0].get('pages') if block.get('nodes') else None)
    if root_pages is not None:
      head += ', ' + pages_text(root_pages)
    lines.append(head)
  base = '  ' if block.get('cite') else ''
  for node in block['nodes']:
    indent = base + '  ' * node.get('depth', 0)
    if (node.get('flags') or {}).get('provisional') and node.get('depth', 0):
      indent = indent[:-2] + '? '
    lines.append(indent + node_label(node))
    for entry in node.get('synonymy') or ():
      lines.append(indent + '  = ' + _entry_line(entry, node.get('name')))
    if node.get('typeSpecies'):
      lines.append(indent + '  Type species. ' + node['typeSpecies']['label']
                   + (' (editor)' if node['typeSpecies'].get('inferred') else ''))
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


def _statement_line(entry):
  """One statement: year, source, the name as that source uses it when
  it differs from the heading, the sentence, the page."""
  parts = [str(entry.get('year') or ''), entry.get('authors') or entry.get('cite') or '']
  sentence = entry.get('sentence') or ''
  if entry.get('name'):
    sentence = f"{entry['name']}: {sentence}"
  if entry.get('printed') == 'editor':
    sentence += ' (editor)'
  if entry.get('page') is not None:
    sentence += f" ({pages_text(entry['page'])})"
  parts.append(sentence)
  return parts


def _list_title(block):
  heading = block['heading']
  title = heading.get('name') or f"[{heading['key']}]"
  if heading.get('rank'):
    title += f" ({heading['rank']})"
  if block.get('kind') == 'statements':
    title = f'Statements about {title}'
  elif block.get('kind') == 'synonymy':
    # The synonymy is one source's: the listing says whose.
    title = f"Synonymy under {title} in {block['cite']}"
  return title


@style('text', 'list')
def _text_list(block):
  heading = block['heading']
  lines = [_list_title(block)]
  if block.get('kind') == 'statements':
    rows = [_statement_line(e) for e in block['entries']]
    width = max([len(r[1]) for r in rows] + [0])
    for year, authors, sentence in rows:
      lines.append(f'  {year}  {authors.ljust(width)}  {sentence}')
    if not rows:
      lines.append('  (none entered from any source)')
    return '\n'.join(lines)
  for entry in block['entries']:
    lines.append('  ' + _entry_line(entry, heading.get('name')))
  return '\n'.join(lines)


@style('text', 'statement')
def _text_statement(block):
  return _statement_text(block)


def _chain_text(chain):
  parts = []
  for node in chain:
    label = node['label']
    if node.get('provisional'):
      label = '? ' + label
    if node.get('questionable'):
      label += ' ?'
    if node.get('alternatives'):
      label += ' (or ' + ', '.join(node['alternatives']) + ')'
    parts.append(label)
  return ' › '.join(parts)


def _chains_head(block):
  """The title line with the measurement, then the first/last line."""
  deco = block.get('decorations') or {}
  lines = []
  title = block.get('title') or ''
  if deco.get('measure'):
    title = f"{title}: {deco['measure']}" if title else deco['measure']
  if title:
    lines.append(title)
  if deco.get('span'):
    lines.append(deco['span'])
  return lines


@style('text', 'chains')
def _text_chains(block):
  lines = _chains_head(block)
  if lines and block['entries']:
    lines.append('')
  width = max([len(e.get('authors') or e['cite']) for e in block['entries']] + [0])
  for e in block['entries']:
    lines.append(f"{e['year']}  {(e.get('authors') or e['cite']).ljust(width)}  {_chain_text(e['chain'])}")
  if not block['entries']:
    lines.append('(no source places it there)')
  return '\n'.join(lines)


# -- markdown --------------------------------------------------------------

@style('markdown', 'classification')
def _md_classification(block):
  tree = _text_classification(dict(block, cite=None))
  head = f"**{block['cite']}**\n" if block.get('cite') else ''
  return head + '```\n' + tree + '\n```'


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
    # A cell with several values breaks lines; GFM tables allow <br>.
    cells = [_cell_text(cell, '<br>').replace('|', '\\|') for cell in row['cells']]
    lines.append('| ' + ' | '.join(cells) + ' |')
  return '\n'.join(lines)


@style('markdown', 'list')
def _md_list(block):
  heading = block['heading']
  lines = [f'**{_list_title(block)}**', '']
  if block.get('kind') == 'statements':
    for year, authors, sentence in (_statement_line(e) for e in block['entries']):
      lines.append(f'- {year} {authors}: {sentence}')
    if not block['entries']:
      lines.append('(none entered from any source)')
    return '\n'.join(lines)
  for entry in block['entries']:
    lines.append('- ' + _entry_line(entry, heading.get('name')))
  return '\n'.join(lines)


@style('markdown', 'statement')
def _md_statement(block):
  return _statement_text(block)


@style('text', 'timeline')
def _text_timeline(block):
  lines = _chains_head(block)
  deco = block.get('decorations') or {}
  for key in ('ranks', 'positions'):
    if deco.get(key):
      lines.append(deco[key])
  if block['entries']:
    lines.append('')
  width = max([len(e.get('authors') or e['cite']) for e in block['entries']] + [0])
  for e in block['entries']:
    line = e['line']
    if e.get('page') is not None:
      line += f" ({pages_text(e['page'])})"
    lines.append(f"{e['year']}  {(e.get('authors') or e['cite']).ljust(width)}  {line}")
    for s in e.get('synonymy') or ():
      lines.append(' ' * (8 + width) + '= ' + _entry_line(s))
  if not block['entries']:
    lines.append('(no source uses the name)')
  return '\n'.join(lines)


@style('markdown', 'timeline')
def _md_timeline(block):
  head = _chains_head(block)
  deco = block.get('decorations') or {}
  lines = [f'**{head[0]}**'] if head else []
  for key in ('ranks', 'positions'):
    if deco.get(key):
      lines.append(deco[key] + '  ')
  lines.append('')
  for e in block['entries']:
    line = e['line']
    if e.get('page') is not None:
      line += f" ({pages_text(e['page'])})"
    lines.append(f"- {e['year']} {e.get('authors') or e['cite']}: {line}")
    for s in e.get('synonymy') or ():
      lines.append('  - = ' + _entry_line(s))
  if not block['entries']:
    lines.append('(no source uses the name)')
  return '\n'.join(lines)


@style('markdown', 'chains')
def _md_chains(block):
  head = _chains_head(block)
  lines = []
  if head:
    lines.append(f'**{head[0]}**')
    lines += head[1:]
    lines.append('')
  if not block['entries']:
    lines.append('(no source places it there)')
    return '\n'.join(lines)
  lines.append('| year | source | chain |')
  lines.append('|---|---|---|')
  for e in block['entries']:
    lines.append(f"| {e['year']} | {e.get('authors') or e['cite']} | {_chain_text(e['chain']).replace('|', '\\|')} |")
  return '\n'.join(lines)
