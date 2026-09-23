"""The claim store: the committed claim table in memory, and the blocks
built from it.

`ClaimStore` reads `claims/` (the JSONL per source, `manifest.json`,
`names.json`) into indices, holds the closure over them, and builds
every block a tool returns: the listing a source prints, the matrix,
the descendants and ancestors, the timeline, the statements, the gap
sentence. Name and citation resolution is `resolve.py`; the words the
blocks carry are `words.py`; the tool surface over the store is
`tools.py`.
"""

import collections
import json
import pathlib

from . import blocks
from .closure import TAXONOMY, Closure, in_years
from .render import node_label, render
from .resolve import Resolver
from .words import COVERAGE_WORDS, PLURAL_KINDS, Words, short_citation, years_span

CLAIMS_DIR = pathlib.Path(__file__).parent / '..' / 'claims'

_NODE_FLAGS = ('new', 'provisional', 'questionable', 'quoted')

# The coverage kind a kind of statement is declared under.
_COVERAGE_OF_KIND = {
  'material': 'material',
  'occurrences': 'occurrences',
  'illustrations': 'illustrations',
  'specimens': 'material',
  'diagnosis': 'diagnoses',
  'acceptance': 'synonymy',
  'usage': 'skeleton',
  'placement': 'skeleton',
  'rejection': 'skeleton',
  'act': 'skeleton',
  'editorial': 'skeleton',
}

_RANK_ORDER = (
  'kingdom',
  'phylum',
  'subphylum',
  'superclass',
  'class',
  'subclass',
  'superorder',
  'order',
  'suborder',
  'superfamily',
  'family',
  'subfamily',
  'genus',
  'subgenus',
  'species',
  'subspecies',
)


def _rank_order(rank):
  rank = (rank or '').lower()
  return _RANK_ORDER.index(rank) if rank in _RANK_ORDER else len(_RANK_ORDER)


def _with_style(block, style):
  if style != 'json':
    block['rendered'] = render(block, style)
  return block


class ClaimStore:
  def __init__(self, directory=CLAIMS_DIR):
    directory = pathlib.Path(directory)
    with open(directory / 'manifest.json') as fd:
      self.manifest = json.load(fd)
    with open(directory / 'names.json') as fd:
      self.names = json.load(fd)
    self.sources = self.manifest['sources']
    self.authors = self.manifest.get('authors') or {}

    self.by_source = {}
    self.by_subject = collections.defaultdict(list)
    self.by_id = {}
    self.at_path = collections.defaultdict(lambda: collections.defaultdict(list))
    for path in sorted(directory.glob('*.jsonl')):
      claims = []
      with open(path) as fd:
        for line in fd:
          claim = json.loads(line)
          claims.append(claim)
          self.by_id[claim['id']] = claim
          if claim.get('subject') is not None:
            self.by_subject[claim['subject']].append(claim)
          self.at_path[path.stem][claim['path']].append(claim)
      self.by_source[path.stem] = claims

    self.by_folded = collections.defaultdict(list)
    for key, row in self.names.items():
      for form in row['folded']:
        self.by_folded[form].append(key)
    self._closure = None
    self._combinations_at = {}
    # An `or` entry is the same taxon under another name in that source:
    # the usage claim sits on an `or` axis under the node it belongs to.
    self.or_usages = collections.defaultdict(list)
    self.or_names_at = collections.defaultdict(list)
    for claims in self.by_source.values():
      for claim in claims:
        if claim['kind'] == 'usage' and claim.get('axis') == 'or':
          node_path = claim['path'].rsplit('/or/', 1)[0]
          self.or_usages[claim['subject']].append((claim['source'], node_path, claim))
          self.or_names_at[(claim['source'], node_path)].append(claim['subject'])
    self.resolver = Resolver(self)
    self.words = Words(self)

  @property
  def closure(self):
    if self._closure is None:
      self._closure = Closure(self)
    return self._closure

  def source_year(self, source_key):
    row = self.sources.get(source_key)
    year = (row or {}).get('citation', {}).get('year')
    return year if year is not None else 9999

  def cite(self, source_key):
    row = self.sources.get(source_key)
    if row is None:
      return source_key
    return short_citation(row['citation'])

  def name(self, key):
    """The record's name; an unnamed record's printed designation
    ("Rhenopyrgus sp. indet. 1") when it has one, else its key in
    brackets."""
    row = self.names.get(key) or {}
    return row.get('name') or row.get('designation') or f'[{key}]'

  def rank(self, key):
    return (self.names.get(key) or {}).get('rank')

  def _rank_of(self, key):
    return (self.rank(key) or '').lower()

  def _node_claims(self, source_key, path):
    return self.at_path[source_key].get(path, [])

  def _node(self, source_key, path, depth):
    at = self._node_claims(source_key, path)
    usage = next(
      (c for c in at if c['kind'] == 'usage' and c.get('axis') in ('children', 'root')), None
    )
    placement = next((c for c in at if c['kind'] == 'placement' and not c.get('via')), None)
    acts = [c for c in at if c['kind'] == 'act']
    base = placement or usage
    if base is None:
      return None
    key = base['subject']
    flags = {f: True for f in _NODE_FLAGS if placement and placement.get(f)}
    for act in acts:
      if act['actKind'] in ('new', 'placeholder'):
        flags['new'] = True
    rank_word = (placement or {}).get('rank') or self.rank(key)
    node = {
      'key': key,
      'name': self.names.get(key, {}).get('name'),
      'rank': self.rank(key),
      'depth': depth,
      'flags': flags,
      'claim': base['id'],
      'acts': [
        {'act': a['actKind'], 'words': self.words.act_words(a), 'inferred': bool(a.get('inferred'))}
        for a in acts
      ],
      'actClaims': [a['id'] for a in acts],
    }
    if usage and usage.get('sensu'):
      node['sensu'] = usage['sensu']
    if rank_word:
      node['rankWord'] = rank_word[:1].upper() + rank_word[1:]
    also = self.or_names_at.get((source_key, path))
    if also:
      node['or'] = [self.name(k) for k in also]
    if base.get('placeholder'):
      node['placeholder'] = base['placeholder']
    if flags.get('new'):
      # The rank's abbreviation; the printed heading is the printed_forms tool's.
      node['newMark'] = blocks.new_mark(rank_word)
    label = self.words.display(key, source_key, path)
    if label and label != node['name']:
      node['label'] = label
    printed = (usage or {}).get('printed') or {}
    if printed.get('citedAs'):
      node['printed'] = printed['citedAs']
    if base.get('pages') is not None:
      node['pages'] = base['pages']
    return node

  def _children_paths(self, source_key, path):
    prefix = f'{path}/children/'
    found = []
    for candidate in self.at_path[source_key]:
      if candidate.startswith(prefix) and '/' not in candidate[len(prefix) :]:
        found.append(candidate)
    return sorted(found, key=lambda p: int(p.rsplit('/', 1)[1]))

  def _synonymy_entries(self, source_key, path):
    entries = []
    prefix = f'{path}/synonyms/'
    for candidate, claims in self.at_path[source_key].items():
      if not (candidate.startswith(prefix) and '/' not in candidate[len(prefix) :]):
        continue
      acceptance = next((c for c in claims if c['kind'] == 'acceptance'), None)
      if acceptance is None:
        continue
      cited = acceptance.get('citesSource')
      printed = acceptance.get('printed') or {}
      year = self.source_year(cited) if cited else printed.get('year')
      # A cited work with no record shows its attribution as printed, by field.
      cite = self.cite(cited) if cited else self.words.attribution_words(printed) or None
      entries.append(
        blocks.list_entry(
          source=cited,
          cite=cite,
          year=year if year != 9999 else None,
          claim=acceptance['id'],
          page=acceptance.get('citedPages'),
          stance=acceptance['stance'],
          parents=[self.name(p) for p in acceptance.get('parents') or ()] or None,
          printed=printed.get('citedAs'),
          record=acceptance['subject'] if not acceptance.get('ownName') else None,
          nudum=any(c['kind'] == 'act' and c['actKind'] == 'nomNudum' for c in claims) or None,
          # With an original combination the entry carries the bare epithet
          # (the parents supply the genus); without one, the cited name as the
          # combination the entry falls under; the heading's own name needs
          # neither.
          name=(
            self.name(acceptance['subject'])
            if acceptance.get('parents')
            else None
            if acceptance.get('ownName')
            else self.words.display(acceptance['subject'], source_key, candidate)
          ),
        )
      )
    entries.sort(key=lambda e: (e.get('year') or 0, e.get('cite') or ''))
    return entries

  def _subtree(self, source_key, path, depth, max_depth, synonymy):
    node = self._node(source_key, path, depth)
    if node is None:
      return []
    if synonymy:
      entries = self._synonymy_entries(source_key, path)
      if entries:
        node['synonymy'] = entries
    nodes = [node]
    if max_depth is None or depth < max_depth:
      for child in self._children_paths(source_key, path):
        nodes += self._subtree(source_key, child, depth + 1, max_depth, synonymy)
    # The type species as its own line under the genus, as a Systematic
    # Paleontology section prints it, named as this source combines it.
    for child_path in self._children_paths(source_key, path):
      for claim in self._node_claims(source_key, child_path):
        if claim['kind'] == 'act' and claim.get('actKind') == 'type':
          node['typeSpecies'] = {
            'key': claim['subject'],
            'claim': claim['id'],
            'label': self.words.display(claim['subject'], source_key, child_path),
            'inferred': bool(claim.get('inferred')),
          }
          break
      if node.get('typeSpecies'):
        break
    return nodes

  def _record_paths(self, source_key, record, trees=TAXONOMY):
    paths = []
    for claim in self.by_subject.get(record, ()):
      if claim['source'] != source_key or claim['kind'] != 'usage':
        continue
      if claim.get('axis') not in ('children', 'root') or claim.get('tree') not in trees:
        continue
      paths.append(claim['path'])
    # The node an `or` name belongs to counts as the name's own.
    for source, node_path, claim in self.or_usages.get(record, ()):
      if source == source_key and claim.get('tree') in trees and node_path not in paths:
        paths.append(node_path)
    return paths

  def contents(self, source, record, depth=None, synonymy=False, style='text'):
    """What a source places under a record, as the source prints it."""
    source, record = self.resolver.source_key(source), self.resolver.key(record)
    parameters = {'source': source, 'record': record, 'depth': depth, 'synonymy': synonymy}
    if source is None:
      out = []
      sources = sorted(
        {c['source'] for c in self.by_subject.get(record, ()) if c['kind'] == 'usage'},
        key=lambda s: (self.source_year(s), s),
      )
      for source_key in sources:
        out += self.contents(source_key, record, depth, synonymy, style)
      return out
    result = []
    for path in self._record_paths(source, record):
      nodes = self._subtree(source, path, 0, depth, synonymy)
      if nodes:
        block = blocks.classification(
          nodes,
          {**parameters, 'source': source, 'path': path},
          source=source,
          root=record,
          extra={'cite': self.cite(source), 'year': self.source_year(source)},
        )
        result.append(_with_style(block, style))
    return result

  def placements(
    self,
    records,
    sources=None,
    years=None,
    include_variants=True,
    include_synonyms=True,
    trees=None,
    style='text',
  ):
    """Where each source places each record: rows records, columns sources
    in year order, cells the parent (and its rank)."""
    records = self.resolver.keys(records)
    sources = self.resolver.source_keys(sources) if sources else sources
    trees = tuple(trees) if trees else TAXONOMY
    closure = self.closure
    rows_keys = closure.expand(list(records), include_variants)
    if include_synonyms:
      for key in list(rows_keys):
        for claim in closure.accepted_under.get(key, ()):
          if claim['subject'] not in rows_keys:
            rows_keys.append(claim['subject'])
    cells = collections.defaultdict(lambda: collections.defaultdict(list))
    column_sources = set()
    for key in rows_keys:
      for claim in closure.placements_of.get(key, ()):
        if not closure._wanted(claim, trees, years):
          continue
        if sources and claim['source'] not in sources:
          continue
        parent = claim.get('parent')
        parent_path = claim['path'].rsplit('/children/', 1)[0]
        value = (
          self.words.display(parent, claim['source'], parent_path) if parent else '(unnamed group)'
        )
        if claim.get('provisional'):
          value = '? ' + value
        if claim.get('questionable'):
          value += ' ?'
        # Every claim at the node rides with the cell: the usage, the acts,
        # a rejection, which the cell also shows.
        at = self._node_claims(claim['source'], claim['path'])
        for c in at:
          if c['kind'] == 'rejection' and c.get('declinedParent'):
            value += f'; not {self.words.display(c["declinedParent"])}'
        # A species recombined is a different name: one row per combination.
        row_label = self.words.display(key, claim['source'], claim['path'])
        cells[(key, row_label)][claim['source']].append(
          {
            'value': value,
            'key': parent,
            'claim': claim['id'],
            'claims': sorted({c['id'] for c in at}),
            'rank': claim.get('rank'),
          }
        )
        column_sources.add(claim['source'])
    columns_keys = sorted(column_sources, key=lambda s: (self.source_year(s), s))
    columns = [{'name': 'record', 'kind': 'record'}, {'name': 'rank', 'kind': 'rank'}] + [
      {'name': self.cite(s), 'kind': 'source', 'source': s} for s in columns_keys
    ]
    rows = []
    for key in rows_keys:
      labels = [label for (k, label) in cells if k == key]
      for row_label in sorted(
        labels, key=lambda name: min(self.source_year(s) for s in cells[(key, name)])
      ):
        row_cells = [[{'value': row_label, 'key': key}], [{'value': self.rank(key) or ''}]]
        for s in columns_keys:
          row_cells.append(cells[(key, row_label)].get(s, []))
        rows.append({'cells': row_cells, 'record': key, 'combination': row_label})
    schemes = closure.schemes(list(records), include_variants, trees, years)
    parameters = {
      'records': list(records),
      'sources': sources,
      'years': years,
      'include_variants': include_variants,
      'include_synonyms': include_synonyms,
      'trees': list(trees),
    }
    block = blocks.table(
      columns,
      rows,
      parameters,
      decorations={'schemes': self.words.scheme_lines(schemes)} if schemes else None,
      title='Placements by source',
      extra={'schemes': schemes, 'sourceKeys': columns_keys},
    )
    return _with_style(block, style)

  def descendants(
    self,
    records,
    include_synonyms=True,
    include_variants=True,
    trees=None,
    years=None,
    style='text',
  ):
    records = self.resolver.keys(records)
    trees = tuple(trees) if trees else TAXONOMY
    found = self.closure.descendants(
      list(records), include_synonyms, include_variants, trees, years
    )
    rows = []
    for key in sorted(found, key=lambda k: (_rank_order(self.rank(k)), self.name(k))):
      # One row per combination: a species recombined is a different name.
      by_label = {}
      for via in found[key]:
        claim = self.by_id.get(via.get('claim'))
        if claim is not None and 'parent' in via:
          label = self.words.display(key, claim['source'], claim['path'])
        elif claim is not None and 'synonymOf' in via:
          label = self.words.display(key, claim['source'], claim['path'])
        else:
          label = self.words.display(key)
        by_label.setdefault(label, []).append(via)
      for label, vias in sorted(
        by_label.items(), key=lambda kv: (min((v.get('year', 0) for v in kv[1]), default=0), kv[0])
      ):
        how = []
        for via in vias:
          if 'parent' in via:
            claim = self.by_id[via['claim']]
            parent_path = claim['path'].rsplit('/children/', 1)[0]
            under = self.words.display(via['parent'], via['source'], parent_path)
            how.append(
              {
                'value': f'{self.cite(via["source"])}: under {under}',
                'claim': via['claim'],
                'source': via['source'],
              }
            )
          elif 'synonymOf' in via:
            # The senior name as that source combines it.
            claim = self.by_id[via['claim']]
            senior = self.words.display(
              via['synonymOf'], via['source'], claim['path'].rsplit('/', 2)[0]
            )
            how.append(
              {
                'value': f'{self.cite(via["source"])}: synonym of {senior}',
                'claim': via['claim'],
                'source': via['source'],
              }
            )
          else:
            how.append({'value': self.words.variant_words(key, via['variantOf'])})
        rows.append(
          {
            'cells': [
              [{'value': label, 'key': key}],
              [{'value': self.rank(key) or ''}],
              how,
              [{'value': len({v['source'] for v in vias if 'source' in v})}],
            ],
            'record': key,
            'combination': label,
          }
        )
    parameters = {
      'records': list(records),
      'include_synonyms': include_synonyms,
      'include_variants': include_variants,
      'trees': list(trees),
      'years': years,
    }
    block = blocks.table(
      [
        {'name': 'record', 'kind': 'record'},
        {'name': 'rank', 'kind': 'rank'},
        {'name': 'placed by', 'kind': 'text'},
        {'name': 'sources', 'kind': 'count'},
      ],
      rows,
      parameters,
      title='Placed under ' + ', '.join(self.words.display(r) for r in records),
      extra={'found': found},
    )
    return _with_style(block, style)

  def _chain_entry(self, chain, nodes=None):
    source_key = chain['source']
    nodes = chain['nodes'] if nodes is None else nodes
    shown = []
    for n in nodes:
      shown.append(
        {
          'key': n['key'],
          'label': self.words.display(n['key'], source_key, n['path']),
          'rank': self.rank(n['key']),
          'kind': 'placeholder' if n['placeholder'] else 'placement',
          'alternatives': [self.words.display(a) for a in n['alternatives']],
          'provisional': n['provisional'],
          'questionable': n['questionable'],
        }
      )
    last = chain['nodes'][-1]
    claims = [n['claim'] for n in nodes if n.get('claim')]
    claims += [c['id'] for c in self._node_claims(source_key, last['path'])]
    return {
      'source': source_key,
      'cite': self.cite(source_key),
      'authors': self.words.authors(source_key),
      'year': chain['year'],
      'chain': shown,
      'claims': sorted(set(claims)),
    }

  def _chain_decorations(self, entries, first_last=False):
    sources = sorted({e['source'] for e in entries}, key=lambda s: (self.source_year(s), s))
    if not sources:
      return {}
    sets = {self.closure.coauthor_set(s) for s in sources}
    years = years_span(self.source_year(sources[0]), self.source_year(sources[-1]))
    deco = {
      'measure': (
        f'{len(sources)} paper{"s" if len(sources) != 1 else ""}, '
        f'{len(sets)} co-author set{"s" if len(sets) != 1 else ""}, {years}'
      )
    }
    if first_last:
      deco['span'] = f'first {self.cite(sources[0])}, last {self.cite(sources[-1])}'
    return deco

  def ancestors(self, records, include_variants=True, trees=None, years=None, style='text'):
    """Every source's chain of taxa above the records, one line per
    source, top down."""
    raw = list(records)
    records = self.resolver.keys(records)
    trees = tuple(trees) if trees else TAXONOMY
    closure = self.closure
    entries = []
    for key in closure.expand(list(records), include_variants):
      for chain in closure.chains_of(key, trees, years):
        entries.append(self._chain_entry(chain))
    entries.sort(key=lambda e: (e['year'], e['source']))
    parameters = {
      'records': list(records),
      'include_variants': include_variants,
      'trees': list(trees),
      'years': years,
    }
    title = 'Above ' + ', '.join(
      self.words.heading(k, self.words.asked(r, k)) for r, k in zip(raw, records, strict=True)
    )
    block = blocks.chains(
      entries, parameters, title=title, decorations=self._chain_decorations(entries)
    )
    return _with_style(block, style)

  def placed_under(
    self, record, parent, include_variants=True, trees=None, years=None, style='text'
  ):
    """The sources that place a record under a higher taxon, directly or
    through intermediates, in year order, each with the taxa between;
    first and last stated."""
    raw_record, raw_parent = record, parent
    record, parent = self.resolver.key(record), self.resolver.key(parent)
    trees = tuple(trees) if trees else TAXONOMY
    closure = self.closure
    parents = set(closure.expand([parent], include_variants))
    entries = []
    for key in closure.expand([record], include_variants):
      for chain in closure.chains_of(key, trees, years):
        index = next((i for i, n in enumerate(chain['nodes']) if n['key'] in parents), None)
        if index is None:
          continue
        entries.append(self._chain_entry(chain, chain['nodes'][index + 1 :]))
    entries.sort(key=lambda e: (e['year'], e['source']))
    parameters = {
      'record': record,
      'parent': parent,
      'include_variants': include_variants,
      'trees': list(trees),
      'years': years,
    }
    title = (
      f'{self.words.heading(record, self.words.asked(raw_record, record))} under '
      f'{self.words.heading(parent, self.words.asked(raw_parent, parent))}'
    )
    block = blocks.chains(
      entries,
      parameters,
      title=title,
      decorations=self._chain_decorations(entries, first_last=True),
    )
    return _with_style(block, style)

  def _position_above(self, source_key, path):
    """The taxon a node sits under, above what its combination already
    says: for a species the parent of its genus, for a subgenus the
    parent of the genus, otherwise the parent. None when the source's
    tree stops there."""
    closure = self.closure
    claim = closure.by_path[source_key].get(path)
    if claim is None:
      return None
    inside = set(self.words.combination(source_key, path).get('keys') or ())
    current = claim
    while current is not None and current.get('parent') in inside:
      current = closure.parent_claim(source_key, current)
    if current is None or not current.get('parent'):
      return None
    parent_path = current['path'].rsplit('/children/', 1)[0]
    words = self.words.display(current['parent'], source_key, parent_path)
    if current.get('provisional'):
      words += ' (provisional)'
    if current.get('questionable'):
      words += ' (questionable)'
    return {'key': current['parent'], 'words': words, 'claim': current['id']}

  def history(
    self, record, include_related=True, synonymy=False, trees=None, years=None, style='text'
  ):
    """One line per source in year order: the name as the source uses
    it, its position above what the combination says, the acts in
    words, the page; with synonymy, each source's synonymy entries. The
    measurement is the heading."""
    raw = record
    record = self.resolver.key(record)
    trees = tuple(trees) if trees else TAXONOMY
    closure = self.closure
    keys = closure.expand([record], include_related)
    by_source = collections.defaultdict(list)
    for key in keys:
      for claim in self.by_subject.get(key, ()):
        if claim.get('tree') in trees and in_years(self.source_year(claim['source']), years):
          by_source[claim['source']].append(claim)
    heading = self.words.heading(record, self.words.asked(raw, record))
    entries = []
    for source_key in sorted(by_source, key=lambda s: (self.source_year(s), s)):
      claims = by_source[source_key]
      uses = [c for c in claims if c['kind'] == 'usage' and c.get('axis') in ('children', 'root')]
      # An `or` name is used at the node it belongs to; when the node's own
      # name is also in the history the two share one line.
      node_paths = {c['path'] for c in uses}
      uses += [
        dict(c, path=c['path'].rsplit('/or/', 1)[0])
        for c in claims
        if c['kind'] == 'usage'
        and c.get('axis') == 'or'
        and c['path'].rsplit('/or/', 1)[0] not in node_paths
      ]
      if uses:
        for use in uses:
          path = use['path']
          at = self._node_claims(source_key, path)
          words = self.words.display(use['subject'], source_key, path)
          also = [k for k in self.or_names_at.get((source_key, path), ()) if k != use['subject']]
          if also and use.get('axis') != 'or':
            words += ' or ' + ' or '.join(self.name(k) for k in also)
          position = self._position_above(source_key, path)
          if position:
            words += f', in {position["words"]}'
          acts = [self.words.act_words(c) for c in at if c['kind'] == 'act']
          acts += [self.words.claim_words(c) for c in at if c['kind'] == 'rejection']
          if acts:
            words += '; ' + '; '.join(acts)
          entry = {
            'year': self.source_year(source_key),
            'source': source_key,
            'cite': self.cite(source_key),
            'authors': self.words.authors(source_key),
            'record': use['subject'],
            'line': words,
            'page': use.get('pages'),
            'claims': sorted({c['id'] for c in at}),
          }
          if synonymy:
            found = self._synonymy_entries(source_key, path)
            if found:
              entry['synonymy'] = found
          entries.append(entry)
      else:
        # A source that only cites the name, in a synonymy.
        for c in claims:
          if c['kind'] != 'acceptance':
            continue
          under = c.get('under')
          under_path = c['path'].rsplit('/', 2)[0]
          words = self.words.display(c['subject'], source_key, c['path'])
          if under:
            words += f', cited as a synonym of {self.words.display(under, source_key, under_path)}'
          entries.append(
            {
              'year': self.source_year(source_key),
              'source': source_key,
              'cite': self.cite(source_key),
              'authors': self.words.authors(source_key),
              'record': c['subject'],
              'line': words,
              'page': c.get('citedPages'),
              'claims': [c['id']],
            }
          )
    m = closure.measurement(record, include_related, trees, years)
    deco = {}
    if m['papers']:
      sets = len(m['coauthorSets'])
      years = years_span(self.source_year(m['sources'][0]), self.source_year(m['sources'][-1]))
      deco['measure'] = (
        f'{m["papers"]} paper{"s" if m["papers"] != 1 else ""}, '
        f'{sets} co-author set{"s" if sets != 1 else ""}, {years}'
      )
    ranks = self.words.rank_lines(m)
    if ranks:
      deco['ranks'] = ranks
    positions = self.words.position_lines(m)
    if positions:
      deco['positions'] = positions
    parameters = {
      'record': record,
      'include_related': include_related,
      'synonymy': synonymy,
      'trees': list(trees),
      'years': years,
    }
    block = blocks.timeline(
      entries, parameters, title=heading, decorations=deco, extra={'measurement': m}
    )
    return _with_style(block, style)

  def synonymy(self, record, source=None, style='text'):
    """The synonymy a source gives under a record, as a list; every source
    with one when no source is named."""
    record, source = self.resolver.key(record), self.resolver.source_key(source)
    out = []
    sources = (
      [source]
      if source
      else sorted(
        {c['source'] for c in self.by_subject.get(record, ()) if c['kind'] == 'usage'},
        key=lambda s: (self.source_year(s), s),
      )
    )
    for source_key in sources:
      for path in self._record_paths(source_key, record):
        entries = self._synonymy_entries(source_key, path)
        if not entries:
          continue
        block = blocks.listing(
          {
            'key': record,
            'name': self.words.display(record, source_key, path),
            'rank': None if self._rank_of(record) in blocks.SPECIES_GROUP else self.rank(record),
          },
          entries,
          {'record': record, 'source': source_key, 'path': path},
          kind='synonymy',
          extra={'source': source_key, 'cite': self.cite(source_key)},
        )
        out.append(_with_style(block, style))
    return out

  def statements(self, record, source=None, kind=None, act_kind=None, style='text'):
    """Every statement the corpus holds about one record, in publication
    order, each as a sentence."""
    raw = record
    record, source = self.resolver.key(record), self.resolver.source_key(source)
    claims = self.by_subject.get(record, [])
    if source is not None:
      claims = [c for c in claims if c['source'] == source]
    if kind in ('occurrences', 'illustrations', 'specimens'):
      # Material kinds a reader asks for by name.
      material_kind = {
        'occurrences': 'occurrence',
        'illustrations': 'illustration',
        'specimens': 'specimen',
      }[kind]
      claims = [
        c for c in claims if c['kind'] == 'material' and c.get('materialKind') == material_kind
      ]
    elif kind is not None:
      claims = [c for c in claims if c['kind'] == kind]
    if act_kind is not None:
      claims = [c for c in claims if c.get('actKind') == act_kind]
    claims = sorted(claims, key=lambda c: (self.source_year(c['source']), c['source'], c['path']))
    heading = self.words.heading(record, self.words.asked(raw, record))
    entries = []
    for c in claims:
      page = c.get('pages')
      if page is None and c.get('citedPages') is not None:
        page = f'cited p. {c["citedPages"]}'
      as_used = self.words.display(record, c['source'], c['path'])
      entries.append(
        blocks.list_entry(
          source=c['source'],
          cite=self.cite(c['source']),
          year=self.source_year(c['source']),
          claim=c['id'],
          page=page,
          kind=c['kind'],
          sentence=self.words.claim_words(c),
          # The name as this source uses it, when it is not the heading's.
          name=as_used if not heading.startswith(as_used) else None,
          authors=self.words.authors(c['source']),
          printed='editor' if c.get('inferred') else None,
        )
      )
    parameters = {'record': record, 'source': source, 'kind': kind, 'act_kind': act_kind}
    if not entries and source is not None:
      # Nothing of that kind about the record in that source: the answer
      # is the source's coverage of the kind, the gap block, not an
      # empty list a reader could take for a finished answer.
      coverage_kind = _COVERAGE_OF_KIND.get(kind, 'skeleton')
      if act_kind == 'new' or kind == 'act' and act_kind is None:
        coverage_kind = 'newTaxa'
      gap = self.gap(source, coverage_kind, style='json')
      fields, params = (
        dict(gap['fields']),
        {**parameters, **gap['parameters'], 'statement_kind': kind},
      )
      if gap['kind'] == 'gap':
        fields['about'] = heading
      if gap['kind'] == 'gap' and kind is None and act_kind is None and fields.get('entered'):
        # No kind asked: the record's statements may lie in any kind of the
        # source not yet entered, so the gap names every such kind.
        declared = self.sources[source]['audit'].get('coverage') or {}
        also = [
          {
            'kind': k,
            'what': COVERAGE_WORDS[k],
            'plural': k in PLURAL_KINDS,
            'declared': declared[k],
          }
          for k in COVERAGE_WORDS
          if k != coverage_kind and declared.get(k) in ('none', 'partly')
        ]
        if also:
          fields['also'] = also
          params['also_kinds'] = [a['kind'] for a in also]
      # The gap's own parameters name the coverage kind; the query's ride beside.
      gap = blocks.statement(gap['kind'], fields, params)
      return _with_style(gap, style)
    block = blocks.listing({'key': record, 'name': heading}, entries, parameters, kind='statements')
    return _with_style(block, style)

  def source_coverage(self, source):
    """The raw view of one source: citation, whether entered, declared
    audit, derived counts."""
    source_key = self.resolver.source_key(source)
    row = self.sources.get(source_key)
    if row is None:
      return {'source': source_key, 'known': False}
    return {
      'source': source_key,
      'known': True,
      'citation': row['citation'],
      'cite': short_citation(row['citation']),
      'entered': row['tree'],
      'audit': row['audit'],
      'claims': row['claims'],
      'acts': row['acts'],
      'material': row['material'],
      'derived': row['derived'],
      'inconsistencies': row['inconsistencies'],
    }

  def gap(self, source=None, kind=None, name=None, style='text'):
    """What the corpus says about a source's coverage of one kind of
    statement, as the sentence the contract asks for; or, with a name,
    that no source in the corpus carries it."""
    if name:
      block = blocks.statement('absent', {'name': f'the name {name}'}, {'name': name})
      return _with_style(block, style)
    if not source:
      raise ValueError('gap needs a source, or a name')
    # Without a kind the question is whether the source's classification
    # is entered at all.
    kind = kind or 'skeleton'
    source = self.resolver.source_key(source)
    row = self.sources.get(source)
    what = COVERAGE_WORDS.get(kind, kind)
    if row is None:
      fields = {'source': source, 'known': False, 'what': what, 'kind': kind}
      block = blocks.statement(
        'absent', {'name': f'the source {source}'}, {'source': source, 'kind': kind}
      )
      return _with_style(block, style)
    fields = {
      'source': source,
      'cite': short_citation(row['citation']),
      'kind': kind,
      'what': what,
      'plural': kind in PLURAL_KINDS,
      'entered': row['tree'],
      'declared': (row['audit'].get('coverage') or {}).get(kind),
      'auditState': row['audit'].get('state'),
      'derived': row['derived'].get(kind, 0),
    }
    block = blocks.statement('gap', fields, {'source': source, 'kind': kind})
    return _with_style(block, style)

  def printed_forms(self, record, source=None, style='text'):
    """Each form a source prints for a record, verbatim, with the page."""
    record, source = self.resolver.key(record), self.resolver.source_key(source)
    entries = []
    seen = set()
    for c in self.by_subject.get(record, ()):
      if source and c['source'] != source:
        continue
      printed = c.get('printed') or {}
      if not printed:
        continue
      form = printed.get('citedAs') or ' '.join(
        str(printed[f]) for f in ('auth', 'year', 'in') if f in printed
      )
      if (c['source'], form, json.dumps(c.get('pages'))) in seen:
        continue
      seen.add((c['source'], form, json.dumps(c.get('pages'))))
      entries.append(
        blocks.list_entry(
          source=c['source'],
          cite=self.cite(c['source']),
          year=self.source_year(c['source']),
          claim=c['id'],
          page=c.get('pages'),
          printed=form,
        )
      )
    if not entries and source:
      # No verbatim form from that source: the heading as the source's
      # listing is entered, which is the closest thing the corpus holds.
      for path in self._record_paths(source, record):
        usage = next((c for c in self._node_claims(source, path) if c['kind'] == 'usage'), None)
        if usage is None:
          continue
        node = self._subtree(source, path, 0, 0, False)[0]
        entries.append(
          blocks.list_entry(
            source=source,
            cite=self.cite(source),
            year=self.source_year(source),
            claim=usage['id'],
            page=usage.get('pages'),
            printed=node_label(node),
            kind='heading',
          )
        )
    entries.sort(key=lambda e: (e['year'], e['cite'], e.get('page') is None))
    block = blocks.listing(
      {
        'key': record,
        'name': self.words.display(record),
        'rank': None if self._rank_of(record) in blocks.SPECIES_GROUP else self.rank(record),
      },
      entries,
      {'record': record, 'source': source},
      kind='printedForms',
    )
    return _with_style(block, style)

  # -- the resolver's and the wording's public surface, for callers that hold the store

  def key_of(self, kind, value):
    return self.resolver.key_of(kind, value)

  def resolve_name(self, query, rank=None):
    return self.resolver.resolve_name(query, rank=rank)

  def resolve_source(self, query):
    return self.resolver.resolve_source(query)

  def source_signature(self, text):
    return self.resolver.source_signature(text)

  def related_keys(self, taxon_key):
    return self.resolver.related_keys(taxon_key)

  def heading(self, key, asked=None):
    return self.words.heading(key, asked)

  def display(self, key, source=None, path=None):
    return self.words.display(key, source, path)

  def combination(self, source_key, path):
    return self.words.combination(source_key, path)

  def combinations(self, key):
    return self.words.combinations(key)

  def original_combination(self, key):
    return self.words.original_combination(key)
