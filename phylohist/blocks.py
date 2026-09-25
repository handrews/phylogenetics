"""Blocks: the building-block shapes an answer is assembled from.

A block is data, never text: a `type`, a `blockId` (a hash of its
content, so a composition can name it and a validator can confirm it is
the block a tool returned), the `parameters` that produced it, the
`claims` it rests on, and a typed payload that keeps record keys, names,
ranks, source keys, years and claim ids on every node and cell. How a
block looks is `render.py`'s business; a new rendering (a modern
"Systematic Paleontology" listing, a graph, a timeline) is a new style
there and needs nothing here.

Types: `classification` (a tree as a source prints it), `table` (typed
columns, cells that may hold several values), `list` (a synonymy list,
printed forms or statements under a heading), `statement` (a gap, a
printed form, an absence), `chains` (one line per source: the chain of
taxa from a higher taxon down to a record), `timeline` (one line per
source in year order: what it does with a name).
"""

import hashlib
import json

SPECIES_GROUP = ('species', 'subspecies', 'variety')

TYPES = ('classification', 'table', 'list', 'statement', 'chains', 'timeline')

# The marks a listing prints beside a name, in the community's
# abbreviations; shared by the tools that word cells and the renderers.
ACT_MARKS = {
  'emended': 'emend.',
  'nomTransl': 'nom. transl.',
  'nomNudum': 'nom. nud.',
  'corrected': 'nom. correct.',
  'substituted': 'nom. subst.',
}
SENSU_MARKS = {'stricto': '(s. s.)', 'lato': '(s. l.)', 'emendato': '(s. em.)'}
_NEW_MARKS = {
  'superfamily': 'superfam. nov.',
  'family': 'fam. nov.',
  'subfamily': 'subfam. nov.',
  'genus': 'gen. nov.',
  'subgenus': 'subgen. nov.',
  'species': 'sp. nov.',
  'subspecies': 'subsp. nov.',
  'variety': 'var. nov.',
  'order': 'ord. nov.',
  'suborder': 'subord. nov.',
}


def new_mark(rank):
  """How a new taxon is marked when the source's own wording is not
  recorded: the rank's abbreviation, or "nov." for a rank without one."""
  return _NEW_MARKS.get((rank or '').lower(), 'nov.')


def _claims_of(value):
  """The claim ids a cell value or entry carries: one under `claim`,
  several under `claims`."""
  found = []
  if isinstance(value, dict):
    if value.get('claim'):
      found.append(value['claim'])
    found += list(value.get('claims') or ())
  return found


def _canonical(obj):
  return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def block_id(content):
  return hashlib.sha256(_canonical(content).encode()).hexdigest()[:12]


def _make(kind, payload, parameters, claims, extra=None):
  # `extra` is derived data a tool attaches for its callers (a
  # measurement, the closure it drew from); it is part of the content the
  # id covers, since it comes from the same claims.
  if kind not in TYPES:
    raise ValueError(f'unknown block type {kind}')
  content = {'type': kind, 'parameters': parameters, **payload, **(extra or {})}
  content['claims'] = sorted(set(claims))
  content['blockId'] = block_id(content)
  return content


def classification(nodes, parameters, source=None, root=None, extra=None):
  """``nodes`` in document order, each: key, name, rank, depth, flags
  (new, provisional, questionable, quoted), placeholder kind, printed
  form, pages, claim, and optional ``synonymy`` entries as `list_entry`
  makes them."""
  claims = [n['claim'] for n in nodes if n.get('claim')]
  claims += [c for n in nodes for c in n.get('actClaims') or ()]
  claims += [n['typeSpecies']['claim'] for n in nodes if n.get('typeSpecies')]
  claims += [e['claim'] for n in nodes for e in n.get('synonymy') or () if e.get('claim')]
  return _make(
    'classification',
    {
      'source': source,
      'root': root,
      'nodes': nodes,
    },
    parameters,
    claims,
    extra,
  )


def table(columns, rows, parameters, groups=None, decorations=None, title=None, extra=None):
  """``columns``: [{name, kind}] with kind one of record, source, rank,
  text, count, year, list. ``rows``: [{cells: [[{value, claim?}, ...] per
  column], group?: label}]. A cell is a list because one source can place
  a record twice. ``decorations`` carries computed measurements (counts,
  co-author sets, year spans) that a renderer may show as a header."""
  claims = [c for row in rows for cell in row['cells'] for v in cell for c in _claims_of(v)]
  return _make(
    'table',
    {
      'title': title,
      'columns': columns,
      'rows': rows,
      'groups': groups or [],
      'decorations': decorations or {},
    },
    parameters,
    claims,
    extra,
  )


def list_entry(
  source,
  cite,
  year,
  claim,
  page=None,
  stance=None,
  parents=None,
  printed=None,
  record=None,
  name=None,
  kind=None,
  sentence=None,
  claims=None,
  authors=None,
  nudum=None,
):
  """One line of a list: a synonymy entry (parents, name, printed form,
  stance), a printed form, or a statement (kind, sentence)."""
  entry = {'source': source, 'cite': cite, 'year': year, 'claim': claim}
  for field, value in (
    ('page', page),
    ('stance', stance),
    ('parents', parents),
    ('printed', printed),
    ('record', record),
    ('name', name),
    ('kind', kind),
    ('sentence', sentence),
    ('claims', claims),
    ('authors', authors),
    ('nudum', nudum),
  ):
    if value is not None:
      entry[field] = value
  return entry


def listing(heading, entries, parameters, kind='synonymy', extra=None):
  """``heading``: {key, name, rank}; ``entries`` from `list_entry`, in
  year order."""
  return _make(
    'list',
    {
      'kind': kind,
      'heading': heading,
      'entries': entries,
    },
    parameters,
    [c for e in entries for c in _claims_of(e)],
    extra,
  )


def chains(entries, parameters, title=None, decorations=None, extra=None):
  """``entries`` in year order, each: source, cite, year, chain (top
  down, each node key, label, rank, kind: placement, placeholder or
  alternative), claims. ``decorations`` carries the measurement (papers,
  co-author sets, years, first and last)."""
  return _make(
    'chains',
    {
      'title': title,
      'entries': entries,
      'decorations': decorations or {},
    },
    parameters,
    [c for e in entries for c in _claims_of(e)],
    extra,
  )


def timeline(entries, parameters, title=None, decorations=None, extra=None):
  """``entries`` in year order, each: year, source, cite, line (the name
  as the source uses it and its position), acts (words), page, optional
  synonymy entries, claims."""
  return _make(
    'timeline',
    {
      'title': title,
      'entries': entries,
      'decorations': decorations or {},
    },
    parameters,
    [c for e in entries for c in _claims_of(e)]
    + [c for e in entries for s in e.get('synonymy') or () for c in _claims_of(s)],
    extra,
  )


def statement(kind, fields, parameters, claims=()):
  """``kind``: gap (a source's coverage for a kind of statement), absent
  (nothing in the corpus)."""
  return _make('statement', {'kind': kind, 'fields': fields}, parameters, claims)


def compose(blocks, header, question=None):
  """An answer as data: the planner's header (its parameters, one line),
  the blocks in order, and a question back when a parameter was
  ambiguous."""
  content = {
    'header': header,
    'blocks': blocks,
    'question': question,
  }
  content['compositionId'] = block_id(
    {
      'header': header,
      'blocks': [b['blockId'] for b in blocks],
      'question': question,
    }
  )
  return content


def validate(block, store):
  """Every claim id, record key and source key in the block must exist in
  the store, and the block id must match its content. Returns the list
  of problems; empty means valid."""
  problems = []
  content = {k: v for k, v in block.items() if k not in ('blockId', 'rendered', 'tool')}
  if block_id(content) != block.get('blockId'):
    problems.append('blockId does not match content')
  known_claims = {c['id'] for claims in store.by_source.values() for c in claims}
  for claim_id in block.get('claims', ()):
    if claim_id not in known_claims:
      problems.append(f'unknown claim {claim_id}')

  def check_key(key):
    if key is not None and key not in store.names:
      problems.append(f'unknown record {key}')

  def check_source(key):
    if key is not None and key not in store.sources:
      problems.append(f'unknown source {key}')

  kind = block.get('type')
  if kind == 'classification':
    check_source(block.get('source'))
    for node in block.get('nodes', ()):
      check_key(node.get('key'))
      for entry in node.get('synonymy') or ():
        check_source(entry.get('source'))
  elif kind == 'table':
    for column, values in zip(
      block.get('columns', ()),
      zip(*[row['cells'] for row in block.get('rows', ())], strict=False)
      if block.get('rows')
      else (),
      strict=False,
    ):
      for cell in values:
        for v in cell:
          if not isinstance(v, dict):
            continue
          # A cell shows a name; the key or source key rides beside it.
          if column['kind'] == 'record' and 'key' in v:
            check_key(v['key'])
          elif column['kind'] == 'source' and 'source' in v:
            check_source(v['source'])
  elif kind == 'list':
    check_key((block.get('heading') or {}).get('key'))
    for entry in block.get('entries', ()):
      check_source(entry.get('source'))
      check_key(entry.get('record'))
  elif kind == 'statement':
    fields = block.get('fields', {})
    check_source(fields.get('source'))
    check_key(fields.get('record'))
  elif kind == 'chains':
    for entry in block.get('entries', ()):
      check_source(entry.get('source'))
      for node in entry.get('chain', ()):
        check_key(node.get('key'))
  elif kind == 'timeline':
    for entry in block.get('entries', ()):
      check_source(entry.get('source'))
      for s in entry.get('synonymy') or ():
        check_source(s.get('source'))
  else:
    problems.append(f'unknown block type {kind}')
  return problems
