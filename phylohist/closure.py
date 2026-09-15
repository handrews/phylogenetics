"""Closures over the claim table: the execution layer a planner hands to.

Everything here is deterministic over a `ClaimStore`: which records any
source places under a set (transitively, through synonyms and through
the records of the same name at other ranks), which higher taxa any
source places a set under, how the sources partition by the placement
they give, and the measurement a trajectory question asks for. Results
are plain structures; `blocks.py` wraps them. Placements come from
taxonomy trees unless `trees` says otherwise, and every hit says which
source, which year and which claim it rests on.
"""

import collections

TAXONOMY = ('taxonomy',)


def in_years(year, years):
  if years is None:
    return True
  first, last = years
  return (first is None or year >= first) and (last is None or year <= last)


class Closure:
  def __init__(self, store):
    self.store = store
    self.names = store.names
    # Placement claims by source, then by path and by parent; acceptances
    # by the record they are accepted under.
    self.by_path = collections.defaultdict(dict)
    self.by_parent = collections.defaultdict(lambda: collections.defaultdict(list))
    self.placements_of = collections.defaultdict(list)
    self.accepted_under = collections.defaultdict(list)
    for source_key, claims in store.by_source.items():
      for claim in claims:
        if claim['kind'] == 'placement':
          self.by_path[source_key][claim['path']] = claim
          if claim.get('parent'):
            self.by_parent[source_key][claim['parent']].append(claim)
          self.placements_of[claim['subject']].append(claim)
        elif claim['kind'] == 'acceptance' and claim['stance'] == 'accepts':
          if claim.get('under') and claim.get('subject') != claim.get('under'):
            self.accepted_under[claim['under']].append(claim)
    # An `or` name is placed wherever its node is.
    for record, uses in store.or_usages.items():
      for source_key, node_path, _ in uses:
        placement = self.by_path[source_key].get(node_path)
        if placement is not None and placement not in self.placements_of[record]:
          self.placements_of[record].append(placement)

  # -- helpers -------------------------------------------------------------

  def year(self, source_key):
    return self.store.source_year(source_key)

  def coauthor_set(self, source_key):
    row = self.store.sources.get(source_key) or {}
    return tuple(sorted(row.get('citation', {}).get('authors') or ()))

  def name(self, key):
    row = self.names.get(key) or {}
    return row.get('name') or f'[{key}]'

  def rank(self, key):
    return (self.names.get(key) or {}).get('rank')

  def variants(self, key):
    """Records of the same name at another rank or spelling."""
    return self.store.related_keys(key)

  def expand(self, records, include_variants):
    keys = list(dict.fromkeys(records))
    if include_variants:
      for key in list(keys):
        for variant in self.variants(key):
          if variant not in keys:
            keys.append(variant)
    return keys

  def parent_claim(self, source_key, claim):
    """The placement claim of the node above, along the children axis."""
    path = claim['path']
    if '/children/' not in path:
      return None
    return self.by_path[source_key].get(path.rsplit('/children/', 1)[0])

  def chains_of(self, record, trees=TAXONOMY, years=None):
    """The chain of taxa above a record in every source that places it,
    top down, one per placement. Each is ``{source, year, nodes}``; a node
    names its key, path, the claim that puts it there (the root's usage
    claim), whether it is a placeholder, the alternative placements the
    source offers at that step, and the provisional and questionable
    flags."""
    out = []
    for claim in self.placements_of.get(record, ()):
      if not self._wanted(claim, trees, years):
        continue
      source_key = claim['source']
      nodes = []
      current = claim
      while current is not None:
        nodes.append(
          {
            'key': current['subject'],
            'path': current['path'],
            'claim': current['id'],
            'placeholder': bool(current.get('placeholder')),
            'alternatives': list(current.get('altPlacements') or ()),
            'provisional': bool(current.get('provisional')),
            'questionable': bool(current.get('questionable')),
          }
        )
        above = self.parent_claim(source_key, current)
        if above is None and current.get('parent'):
          # The root of the tree has a usage claim but no placement.
          path = current['path'].rsplit('/children/', 1)[0]
          usage = next(
            (c for c in self.store.at_path[source_key].get(path, ()) if c['kind'] == 'usage'), None
          )
          nodes.append(
            {
              'key': current['parent'],
              'path': path,
              'claim': usage['id'] if usage else None,
              'placeholder': bool(current.get('parentPlaceholder')),
              'alternatives': [],
              'provisional': False,
              'questionable': False,
            }
          )
        current = above
      nodes.reverse()
      out.append({'source': source_key, 'year': self.year(source_key), 'nodes': nodes})
    out.sort(key=lambda e: (e['year'], e['source'], e['nodes'][-1]['path']))
    return out

  def _wanted(self, claim, trees, years):
    return claim['tree'] in trees and in_years(self.year(claim['source']), years)

  # -- closures ------------------------------------------------------------

  def descendants(
    self,
    records,
    include_synonyms=True,
    include_variants=True,
    trees=TAXONOMY,
    years=None,
  ):
    """Every record any source places under the set, transitively within
    each source. Returns ``{key: [via, ...]}`` where a via names the
    source, its year, the parent (or the name the record is accepted as a
    synonym of, or the record it is a rank or spelling variant of) and
    the claim."""
    start = self.expand(records, include_variants)
    found = {}
    seen = set(start)
    frontier = list(start)
    while frontier:
      nxt = []
      for parent in frontier:
        for source_key, by_parent in self.by_parent.items():
          for claim in by_parent.get(parent, ()):
            if not self._wanted(claim, trees, years):
              continue
            key = claim['subject']
            found.setdefault(key, []).append(
              {
                'source': source_key,
                'year': self.year(source_key),
                'parent': parent,
                'claim': claim['id'],
              }
            )
            if key not in seen:
              seen.add(key)
              nxt.append(key)
        if include_synonyms:
          for claim in self.accepted_under.get(parent, ()):
            if not in_years(self.year(claim['source']), years):
              continue
            key = claim['subject']
            found.setdefault(key, []).append(
              {
                'source': claim['source'],
                'year': self.year(claim['source']),
                'synonymOf': parent,
                'claim': claim['id'],
              }
            )
            if key not in seen:
              seen.add(key)
              nxt.append(key)
        if include_variants:
          for variant in self.variants(parent):
            if variant not in seen:
              seen.add(variant)
              found.setdefault(variant, []).append({'variantOf': parent})
              nxt.append(variant)
      frontier = nxt
    for vias in found.values():
      # Variant edges carry no source; they follow the placements.
      vias.sort(key=lambda v: (v.get('year', 9999), v.get('source', ''), v.get('claim', '')))
    return found

  def ancestors(self, records, include_variants=True, trees=TAXONOMY, years=None):
    """Every higher taxon any source places the set under, with the chain.
    Returns ``{key: [via, ...]}``; a via names the source, year, the
    record whose chain it lies on, the depth above it, the claim, and the
    kind: ``placement`` (on the chain), ``alternative`` (an alternative
    placement the source offers) or ``placeholder`` (a bin, not a
    taxon)."""
    start = self.expand(records, include_variants)
    found = {}
    for key in start:
      for claim in self.placements_of.get(key, ()):
        if not self._wanted(claim, trees, years):
          continue
        source_key = claim['source']
        depth = 0
        current = claim
        while current is not None and current.get('parent'):
          depth += 1
          parent = current['parent']
          kind = 'placeholder' if current.get('parentPlaceholder') else 'placement'
          found.setdefault(parent, []).append(
            {
              'source': source_key,
              'year': self.year(source_key),
              'of': key,
              'depth': depth,
              'claim': current['id'],
              'kind': kind,
            }
          )
          for alt in current.get('altPlacements') or ():
            found.setdefault(alt, []).append(
              {
                'source': source_key,
                'year': self.year(source_key),
                'of': key,
                'depth': depth,
                'claim': current['id'],
                'kind': 'alternative',
              }
            )
          current = self.parent_claim(source_key, current)
    for vias in found.values():
      vias.sort(key=lambda v: (v['year'], v['source'], v['depth']))
    return found

  def schemes(self, records, include_variants=True, trees=TAXONOMY, years=None):
    """The sources partitioned by the placement they give the set: one
    scheme per family of parent names (a parent and its rank variants
    count as one), each with its sources in year order, first and last
    year, the co-author sets, and the last paper."""
    start = self.expand(records, include_variants)
    groups = {}
    for key in start:
      for claim in self.placements_of.get(key, ()):
        if not self._wanted(claim, trees, years) or not claim.get('parent'):
          continue
        parent = claim['parent']
        family = tuple(
          sorted(
            {parent}
            | set(
              v
              for v in self.variants(parent)
              if (self.names.get(v) or {}).get('kind') != 'altSpellingOf'
            )
          )
        )
        group = groups.setdefault(family, {'parents': {}, 'entries': []})
        group['parents'].setdefault(
          parent,
          {
            'key': parent,
            'name': self.name(parent),
            'rank': self.rank(parent),
          },
        )
        group['entries'].append(
          {
            'source': claim['source'],
            'year': self.year(claim['source']),
            'record': key,
            'rank': claim.get('rank'),
            'claim': claim['id'],
            'placeholder': claim.get('parentPlaceholder'),
          }
        )
    schemes = []
    for group in groups.values():
      entries = sorted(group['entries'], key=lambda e: (e['year'], e['source']))
      sources = list(dict.fromkeys(e['source'] for e in entries))
      schemes.append(
        {
          'parents': sorted(group['parents'].values(), key=lambda p: p['key']),
          'entries': entries,
          'sources': sources,
          'papers': len(sources),
          'coauthorSets': sorted({self.coauthor_set(s) for s in sources}),
          'firstYear': entries[0]['year'],
          'lastYear': entries[-1]['year'],
          'lastSource': entries[-1]['source'],
        }
      )
    schemes.sort(key=lambda s: (-s['lastYear'], -s['papers'], s['parents'][0]['key']))
    return schemes

  def measurement(self, record, include_related=True, trees=TAXONOMY, years=None):
    """The trajectory's header: the positions a name has been given
    (parent families) and the ranks it has been used at, each with the
    papers, co-author sets and years; the latest position by year; the
    last paper for each earlier one."""
    schemes = self.schemes([record], include_related, trees, years)
    keys = self.expand([record], include_related)
    # The rank a source uses the name at, counted in the same trees as the
    # positions: taxonomies unless asked otherwise, since the cladograms
    # are entered less consistently and are a later concern.
    ranks = {}
    for key in keys:
      rank = (self.rank(key) or '').lower() or 'unranked'
      for claim in self.store.by_subject.get(key, ()):
        if claim['kind'] != 'usage' or claim.get('axis') not in ('children', 'root'):
          continue
        if not self._wanted(claim, trees, years):
          continue
        entry = ranks.setdefault(rank, {'rank': rank, 'records': set(), 'sources': set()})
        entry['records'].add(key)
        entry['sources'].add(claim['source'])
    rank_rows = []
    for entry in ranks.values():
      sources = sorted(entry['sources'], key=lambda s: (self.year(s), s))
      rank_rows.append(
        {
          'rank': entry['rank'],
          'records': sorted(entry['records']),
          'sources': sources,
          'papers': len(sources),
          'coauthorSets': sorted({self.coauthor_set(s) for s in sources}),
          'firstYear': self.year(sources[0]),
          'lastYear': self.year(sources[-1]),
          'lastSource': sources[-1],
        }
      )
    rank_rows.sort(key=lambda r: (-r['lastYear'], -r['papers'], r['rank']))
    # The papers that use the name at all, at any rank, in any tree.
    all_sources = sorted(
      {s for row in rank_rows for s in row['sources']},
      key=lambda s: (self.year(s), s),
    )
    return {
      'record': record,
      'records': keys,
      'positions': schemes,
      'latestPosition': schemes[0] if schemes else None,
      'ranks': rank_rows,
      'latestRank': rank_rows[0] if rank_rows else None,
      'papers': len(all_sources),
      'coauthorSets': sorted({self.coauthor_set(s) for s in all_sources}),
      'sources': all_sources,
    }
