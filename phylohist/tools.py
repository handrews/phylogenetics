"""The read-only tools over the committed claim table, returning blocks.

Everything here reads `claims/` (the JSONL per source, `manifest.json`,
`names.json`) and returns blocks (`blocks.py`) rendered in a style
(`render.py`), or plain dicts for the resolver and the coverage view.
Nothing writes, nothing infers, and an empty result is the closed-world
answer: the corpus holds nothing that matches. The CLI, the MCP server
and the eval runner call these functions directly.
"""

import collections
import json
import pathlib

from . import blocks
from .closure import Closure, TAXONOMY, _in_years
from .names import fold_forms
from .render import render

CLAIMS_DIR = pathlib.Path(__file__).parent / '..' / 'claims'

_KIND_ORDER = {
  'primary': 0, 'altRankOf': 1, 'altSpellingOf': 2, 'vulgarSpellingOf': 3,
  'placeholder': 4,
}
_NODE_FLAGS = ('new', 'provisional', 'questionable', 'quoted')

_PLURAL_KINDS = {'newTaxa', 'types', 'occurrences', 'illustrations', 'diagnoses'}

# The community's words for what the table records.
COVERAGE_WORDS = {
  'skeleton': 'the classification',
  'newTaxa': 'the new taxa',
  'types': 'the type designations',
  'synonymy': 'the synonymy',
  'material': 'the material',
  'occurrences': 'the occurrences',
  'illustrations': 'the illustrations',
  'diagnoses': 'the diagnoses',
  'phylogeny': 'the phylogeny',
}


def short_citation(citation):
  """"Holloway & Jell 1983", "Sumrall et al. 2013", "Dehm 1961"."""
  authors = citation.get('authors') or []
  if len(authors) == 1:
    names = authors[0]
  elif len(authors) == 2:
    names = f'{authors[0]} & {authors[1]}'
  elif authors:
    names = f'{authors[0]} et al.'
  else:
    names = 'anonymous'
  year = citation.get('year')
  return f'{names} {year}' if year else f'{names} (in preparation)'


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

  @property
  def closure(self):
    if self._closure is None:
      self._closure = Closure(self)
    return self._closure

  # -- helpers -------------------------------------------------------------

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
    row = self.names.get(key) or {}
    return row.get('name') or f'[{key}]'

  def rank(self, key):
    return (self.names.get(key) or {}).get('rank')

  def label(self, key):
    rank = self.rank(key)
    return f'{self.name(key)} ({rank})' if rank else self.name(key)

  def related_keys(self, taxon_key):
    """Records sharing the name at another rank or spelling, and the
    base or variants a record is linked to."""
    row = self.names.get(taxon_key)
    if row is None:
      return []
    keys = set()
    for form in row['folded']:
      keys.update(self.by_folded.get(form, ()))
    if 'of' in row:
      keys.add(row['of'])
    for key, other in self.names.items():
      if other.get('of') == taxon_key:
        keys.add(key)
    keys.discard(taxon_key)
    return sorted(keys)

  def _candidate(self, key):
    row = self.names[key]
    entry = {
      'key': key,
      'name': row['name'],
      'rank': row['rank'],
      'kind': row['kind'],
      'sourcesWithStatements': len({c['source'] for c in self.by_subject.get(key, ())}),
      'variants': self.related_keys(key),
    }
    for field in ('of', 'placeholder', 'homonym', 'originalParent'):
      if field in row:
        entry[field] = row[field]
    if 'authority' in row:
      entry['authority'] = row['authority'].get('display')
      if 'source' in row['authority']:
        entry['authoritySource'] = row['authority']['source']
    return entry

  def _placed_under(self, key, genus_forms):
    for claim in self.by_subject.get(key, ()):
      if claim['kind'] != 'placement' or claim.get('parent') is None:
        continue
      parent = self.names.get(claim['parent'])
      if parent and genus_forms & set(parent['folded']):
        return True
    return False

  def _act_words(self, claim):
    kind = claim.get('actKind')
    words = {
      'new': 'named as new',
      'placeholder': 'placeholder introduced',
      'type': 'type species',
      'emended': 'emended',
      'nomTransl': 'nomen translatum'
      + (f" from {self.name(claim['altRankOf'])}" if claim.get('altRankOf') else ''),
      'corrected': f"corrected from {self.name(claim.get('correctedFrom', ''))}",
      'moved': f"moved from {self.name(claim.get('movedFrom', ''))}",
      'removed': f"removed from {self.name(claim.get('removedFrom', ''))}",
      'modifier': claim.get('modifier', ''),
    }.get(kind, kind or '')
    if claim.get('inferred'):
      basis = (claim.get('editorial') or {}).get('basis', '').strip()
      words += ' (inferred by the editor' + (f': {basis}' if basis else '') + ')'
    return words

  def _claim_words(self, claim):
    kind = claim['kind']
    if kind == 'usage':
      printed = (claim.get('printed') or {}).get('citedAs')
      return f'cites the name as "{printed}"' if printed else 'cites the name'
    if kind == 'placement':
      parent = claim.get('parent')
      where = self.label(parent) if parent else 'an unnamed group'
      flags = [f for f in ('provisional', 'questionable', 'quoted') if claim.get(f)]
      words = f'places it under {where}'
      if claim.get('parentPlaceholder'):
        words += f" ({claim['parentPlaceholder']} placeholder)"
      if flags:
        words += ' (' + ', '.join(flags) + ')'
      if claim.get('tree') != 'taxonomy':
        words += f" in a {claim['tree']}"
      return words
    if kind == 'acceptance':
      original = ' '.join(self.name(p) for p in claim.get('parents') or ())
      target = f'{original} {self.name(claim["subject"])}' if original else self.name(claim['subject'])
      verb = 'accepts' if claim['stance'] == 'accepts' else 'rejects'
      cited = f" ({self.cite(claim['citesSource'])})" if claim.get('citesSource') else ''
      under = self.name(claim['under']) if claim.get('under') else ''
      return f'{verb} {target}{cited} as {under}' if under else f'{verb} {target}{cited}'
    if kind == 'act':
      return self._act_words(claim)
    if kind == 'rejection':
      return f"declines a placement in {self.label(claim.get('declinedParent', ''))}"
    if kind == 'material':
      mk = claim['materialKind']
      if mk == 'specimen':
        ids = ', '.join(str(i) for i in claim.get('ids') or ())
        repo = f" {claim['repository']}" if claim.get('repository') else ''
        return f"{claim.get('role', 'specimens')}:{repo} {ids}".strip()
      if mk == 'occurrence':
        occ = claim.get('occurrence') or {}
        parts = [str(occ.get(k)) for k in ('stage', 'series', 'unit', 'location') if occ.get(k)]
        return 'occurrence: ' + '; '.join(p.replace("['", '').replace("']", '') for p in parts)
      return 'illustration: ' + json.dumps(claim.get('illustration'), ensure_ascii=False)
    if kind == 'diagnosis':
      return 'diagnosis: ' + (claim.get('text') or '').strip().replace('\n', ' ')
    if kind == 'editorial':
      return "editor's note: " + (claim.get('basis') or '').strip()
    return kind

  # -- resolver -------------------------------------------------------------

  def resolve_name(self, query, rank=None):
    query = (query or '').strip()
    if not query:
      return []
    forms = fold_forms(query)
    keys = {k for form in forms for k in self.by_folded.get(form, ())}

    words = query.split()
    if not keys and len(words) >= 2:
      genus_forms = fold_forms(words[0])
      epithet_forms = fold_forms(words[-1])
      epithet_keys = {
        k for form in epithet_forms for k in self.by_folded.get(form, ())
      }
      keys = {k for k in epithet_keys if self._placed_under(k, genus_forms)}
      if not keys:
        keys = {
          k for k in epithet_keys
          if genus_forms & fold_forms(self.names[k].get('originalParent') or '')
        }

    if not keys and len(words) == 1 and len(query) >= 4:
      prefixes = tuple(forms)
      keys = {
        k for form, ks in self.by_folded.items()
        if form.startswith(prefixes) for k in ks
      }

    if rank is not None:
      wanted = rank.lower()
      keys = {k for k in keys if (self.names[k]['rank'] or '').lower() == wanted}

    candidates = [self._candidate(k) for k in keys]
    candidates.sort(key=lambda c: (
      _KIND_ORDER.get(c['kind'], 9), -c['sourcesWithStatements'], c['name'] or '', c['key'],
    ))
    return candidates

  # -- block tools ----------------------------------------------------------

  def _node_claims(self, source_key, path):
    return self.at_path[source_key].get(path, [])

  def _node(self, source_key, path, depth):
    at = self._node_claims(source_key, path)
    usage = next((c for c in at if c['kind'] == 'usage' and c.get('axis') in ('children', 'root')), None)
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
    node = {
      'key': key, 'name': self.names.get(key, {}).get('name'),
      'rank': self.rank(key), 'depth': depth, 'flags': flags,
      'claim': base['id'],
      'acts': [{'act': a['actKind'], 'words': self._act_words(a),
                'inferred': bool(a.get('inferred'))} for a in acts],
      'actClaims': [a['id'] for a in acts],
    }
    if base.get('placeholder'):
      node['placeholder'] = base['placeholder']
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
      if candidate.startswith(prefix) and '/' not in candidate[len(prefix):]:
        found.append(candidate)
    return sorted(found, key=lambda p: int(p.rsplit('/', 1)[1]))

  def _synonymy_entries(self, source_key, path):
    entries = []
    prefix = f'{path}/synonyms/'
    for candidate, claims in self.at_path[source_key].items():
      if not (candidate.startswith(prefix) and '/' not in candidate[len(prefix):]):
        continue
      acceptance = next((c for c in claims if c['kind'] == 'acceptance'), None)
      if acceptance is None:
        continue
      cited = acceptance.get('citesSource')
      printed = (acceptance.get('printed') or {})
      year = self.source_year(cited) if cited else printed.get('year')
      cite = self.cite(cited) if cited else ' '.join(
        [', '.join(printed['auth'])] if printed.get('auth') else []
      ) or None
      entries.append(blocks.list_entry(
        source=cited, cite=cite, year=year if year != 9999 else None,
        claim=acceptance['id'], page=acceptance.get('citedPages'),
        stance=acceptance['stance'],
        parents=[self.name(p) for p in acceptance.get('parents') or ()] or None,
        printed=printed.get('citedAs'),
        record=acceptance['subject'] if not acceptance.get('ownName') else None,
        name=self.name(acceptance['subject']) if not acceptance.get('ownName') else None,
      ))
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
    return nodes

  def _record_paths(self, source_key, record, trees=TAXONOMY):
    paths = []
    for claim in self.by_subject.get(record, ()):
      if claim['source'] != source_key or claim['kind'] != 'usage':
        continue
      if claim.get('axis') not in ('children', 'root') or claim.get('tree') not in trees:
        continue
      paths.append(claim['path'])
    return paths

  def contents(self, source, record, depth=None, synonymy=False, style='text', trees=TAXONOMY):
    """What a source places under a record, as the source prints it."""
    parameters = {'source': source, 'record': record, 'depth': depth, 'synonymy': synonymy}
    if source is None:
      out = []
      sources = sorted(
        {c['source'] for c in self.by_subject.get(record, ()) if c['kind'] == 'usage'},
        key=lambda s: (self.source_year(s), s),
      )
      for source_key in sources:
        out += self.contents(source_key, record, depth, synonymy, style, trees)
      return out
    result = []
    for path in self._record_paths(source, record, trees):
      nodes = self._subtree(source, path, 0, depth, synonymy)
      if nodes:
        block = blocks.classification(
          nodes, {**parameters, 'source': source, 'path': path},
          source=source, root=record,
          extra={'cite': self.cite(source), 'year': self.source_year(source)},
        )
        result.append(_with_style(block, style))
    return result

  def _scheme_lines(self, schemes):
    lines = []
    for s in schemes:
      parents = ' / '.join(self.label(p['key']) for p in s['parents'])
      span = f"{s['firstYear']}" if s['firstYear'] == s['lastYear'] else f"{s['firstYear']}–{s['lastYear']}"
      lines.append(
        f"{parents}: {s['papers']} paper{'s' if s['papers'] != 1 else ''} "
        f"({span}), {len(s['coauthorSets'])} co-author set"
        f"{'s' if len(s['coauthorSets']) != 1 else ''}, last {self.cite(s['lastSource'])}"
      )
    return lines

  def placements(self, records, sources=None, years=None, include_variants=True,
                 include_synonyms=True, trees=None, style='text'):
    """Where each source places each record: rows records, columns sources
    in year order, cells the parent (and its rank)."""
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
        value = self.label(parent) if parent else '(unnamed group)'
        if claim.get('parentPlaceholder'):
          value += ' [placeholder]'
        for flag in ('provisional', 'questionable'):
          if claim.get(flag):
            value += f' ({flag})'
        cells[key][claim['source']].append({
          'value': value, 'key': parent, 'claim': claim['id'],
          'rank': claim.get('rank'),
        })
        column_sources.add(claim['source'])
    columns_keys = sorted(column_sources, key=lambda s: (self.source_year(s), s))
    columns = [{'name': 'record', 'kind': 'record'}] + [
      {'name': self.cite(s), 'kind': 'source', 'source': s} for s in columns_keys
    ]
    rows = []
    for key in rows_keys:
      if not cells.get(key):
        continue
      row_cells = [[{'value': self.label(key), 'key': key}]]
      for s in columns_keys:
        row_cells.append(cells[key].get(s, []))
      rows.append({'cells': row_cells, 'record': key})
    schemes = closure.schemes(list(records), include_variants, trees, years)
    parameters = {
      'records': list(records), 'sources': sources, 'years': years,
      'includeVariants': include_variants, 'includeSynonyms': include_synonyms,
      'trees': list(trees),
    }
    block = blocks.table(
      columns, rows, parameters,
      decorations={'schemes': self._scheme_lines(schemes)} if schemes else None,
      title='Placements by source',
      extra={'schemes': schemes, 'sourceKeys': columns_keys},
    )
    return _with_style(block, style)

  def descendants(self, records, include_synonyms=True, include_variants=True,
                  trees=None, years=None, style='text'):
    trees = tuple(trees) if trees else TAXONOMY
    found = self.closure.descendants(list(records), include_synonyms, include_variants, trees, years)
    rows = []
    for key in sorted(found, key=lambda k: (_rank_order(self.rank(k)), self.name(k))):
      vias = found[key]
      how = []
      for via in vias:
        if 'parent' in via:
          how.append({'value': f"{self.cite(via['source'])}: under {self.name(via['parent'])}", 'claim': via['claim'], 'source': via['source']})
        elif 'synonymOf' in via:
          how.append({'value': f"{self.cite(via['source'])}: synonym of {self.name(via['synonymOf'])}", 'claim': via['claim'], 'source': via['source']})
        else:
          how.append({'value': f"same name as {self.name(via['variantOf'])}"})
      rows.append({'cells': [
        [{'value': self.name(key), 'key': key}],
        [{'value': self.rank(key) or ''}],
        how,
        [{'value': len({v['source'] for v in vias if 'source' in v})}],
      ], 'record': key})
    parameters = {
      'records': list(records), 'includeSynonyms': include_synonyms,
      'includeVariants': include_variants, 'trees': list(trees), 'years': years,
    }
    block = blocks.table([
      {'name': 'record', 'kind': 'record'}, {'name': 'rank', 'kind': 'rank'},
      {'name': 'placed by', 'kind': 'text'}, {'name': 'sources', 'kind': 'count'},
    ], rows, parameters, title='Placed under ' + ', '.join(self.name(r) for r in records),
       extra={'found': found})
    return _with_style(block, style)

  def ancestors(self, records, include_variants=True, trees=None, years=None, style='text'):
    trees = tuple(trees) if trees else TAXONOMY
    found = self.closure.ancestors(list(records), include_variants, trees, years)
    rows = []
    for key in sorted(found, key=lambda k: (-len({v['source'] for v in found[k]}), self.name(k))):
      vias = found[key]
      kinds = sorted({v['kind'] for v in vias})
      sources = sorted({v['source'] for v in vias}, key=lambda s: (self.source_year(s), s))
      rows.append({'cells': [
        [{'value': self.name(key), 'key': key}],
        [{'value': self.rank(key) or ''}],
        [{'value': ', '.join(kinds)}],
        [{'value': self.cite(s), 'source': s, 'claim': next(v['claim'] for v in vias if v['source'] == s)} for s in sources],
        [{'value': len(sources)}],
      ], 'record': key})
    parameters = {
      'records': list(records), 'includeVariants': include_variants,
      'trees': list(trees), 'years': years,
    }
    block = blocks.table([
      {'name': 'higher taxon', 'kind': 'record'}, {'name': 'rank', 'kind': 'rank'},
      {'name': 'edge', 'kind': 'text'}, {'name': 'sources', 'kind': 'source'},
      {'name': 'count', 'kind': 'count'},
    ], rows, parameters, title='Placed above ' + ', '.join(self.name(r) for r in records),
       extra={'found': found})
    return _with_style(block, style)

  def history(self, record, include_related=True, trees=None, years=None, style='text'):
    """One row per source in year order: the record used, its rank, the
    position given, the acts, the printed form, the page; the measurement
    as the header."""
    trees = tuple(trees) if trees else TAXONOMY
    closure = self.closure
    keys = closure.expand([record], include_related)
    by_source = collections.defaultdict(list)
    for key in keys:
      for claim in self.by_subject.get(key, ()):
        if _in_years(self.source_year(claim['source']), years):
          by_source[claim['source']].append(claim)
    rows = []
    for source_key in sorted(by_source, key=lambda s: (self.source_year(s), s)):
      claims = by_source[source_key]
      used = sorted({c['subject'] for c in claims if c['kind'] == 'usage' and c.get('axis') in ('children', 'root')})
      positions = []
      for c in claims:
        if c['kind'] == 'placement' and c['tree'] in trees:
          parent = c.get('parent')
          positions.append({'value': (self.label(parent) if parent else '(unnamed group)') + (' [placeholder]' if c.get('parentPlaceholder') else ''), 'key': parent, 'claim': c['id']})
        elif c['kind'] == 'placement':
          positions.append({'value': f"in a {c['tree']}", 'claim': c['id']})
      seen = set()
      positions = [p for p in positions if not (p['value'] in seen or seen.add(p['value']))]
      acts = [{'value': self._act_words(c), 'claim': c['id']} for c in claims if c['kind'] == 'act']
      acts += [{'value': self._claim_words(c), 'claim': c['id']} for c in claims if c['kind'] in ('acceptance', 'rejection')]
      printed = [{'value': c['printed']['citedAs'], 'claim': c['id']} for c in claims if c['kind'] == 'usage' and (c.get('printed') or {}).get('citedAs')]
      pages = sorted({json.dumps(c['pages']) for c in claims if c.get('pages') is not None and c['kind'] == 'usage'})
      rows.append({'cells': [
        [{'value': self.cite(source_key), 'source': source_key}],
        [{'value': self.source_year(source_key)}],
        [{'value': ', '.join(self.rank(k) or '' for k in used)}],
        positions, acts, printed,
        [{'value': p.strip('"') } for p in pages],
      ], 'source': source_key})
    m = closure.measurement(record, include_related, trees, years)
    deco = {}
    if m['latestRank']:
      r = m['latestRank']
      deco['latest rank'] = (
        f"{r['rank']}: {r['papers']} paper{'s' if r['papers'] != 1 else ''} "
        f"{r['firstYear']}–{r['lastYear']}, {len(r['coauthorSets'])} co-author set"
        f"{'s' if len(r['coauthorSets']) != 1 else ''}, last {self.cite(r['lastSource'])}"
      )
      earlier = [x for x in m['ranks'] if x is not r]
      if earlier:
        deco['earlier ranks'] = [
          f"{x['rank']}: {x['papers']} paper{'s' if x['papers'] != 1 else ''} "
          f"{x['firstYear']}–{x['lastYear']}, last {self.cite(x['lastSource'])}" for x in earlier
        ]
    if m['positions']:
      deco['positions'] = self._scheme_lines(m['positions'])
    deco['papers'] = f"{m['papers']}, {len(m['coauthorSets'])} co-author sets"
    parameters = {'record': record, 'includeRelated': include_related, 'trees': list(trees), 'years': years}
    block = blocks.table([
      {'name': 'source', 'kind': 'source'}, {'name': 'year', 'kind': 'year'},
      {'name': 'rank', 'kind': 'rank'}, {'name': 'placed under', 'kind': 'record'},
      {'name': 'acts', 'kind': 'text'}, {'name': 'printed as', 'kind': 'text'},
      {'name': 'pages', 'kind': 'text'},
    ], rows, parameters, decorations=deco, title=f'History of {self.name(record)}',
       extra={'measurement': m})
    return _with_style(block, style)

  def synonymy(self, record, source=None, style='text'):
    """The synonymy a source gives under a record, as a list; every source
    with one when no source is named."""
    out = []
    sources = [source] if source else sorted(
      {c['source'] for c in self.by_subject.get(record, ()) if c['kind'] == 'usage'},
      key=lambda s: (self.source_year(s), s),
    )
    for source_key in sources:
      for path in self._record_paths(source_key, record):
        entries = self._synonymy_entries(source_key, path)
        if not entries:
          continue
        block = blocks.listing(
          {'key': record, 'name': self.name(record), 'rank': self.rank(record)},
          entries, {'record': record, 'source': source_key, 'path': path},
          extra={'source': source_key, 'cite': self.cite(source_key)},
        )
        out.append(_with_style(block, style))
    return out

  def statements(self, record, source=None, kind=None, act_kind=None, style='text'):
    """Every statement the corpus holds about one record, in publication
    order, in words."""
    claims = self.by_subject.get(record, [])
    if source is not None:
      claims = [c for c in claims if c['source'] == source]
    if kind is not None:
      claims = [c for c in claims if c['kind'] == kind]
    if act_kind is not None:
      claims = [c for c in claims if c.get('actKind') == act_kind]
    claims = sorted(claims, key=lambda c: (self.source_year(c['source']), c['source'], c['path']))
    rows = []
    for c in claims:
      page = c.get('pages')
      if page is None and c.get('citedPages') is not None:
        page = f"cited p. {c['citedPages']}"
      rows.append({'cells': [
        [{'value': self.cite(c['source']), 'source': c['source']}],
        [{'value': c['kind']}],
        [{'value': self._claim_words(c), 'claim': c['id']}],
        [{'value': '' if page is None else page}],
        [{'value': 'editor' if c.get('inferred') else 'source'}],
      ], 'claim': c['id']})
    parameters = {'record': record, 'source': source, 'kind': kind, 'actKind': act_kind}
    block = blocks.table([
      {'name': 'source', 'kind': 'source'}, {'name': 'kind', 'kind': 'text'},
      {'name': 'statement', 'kind': 'text'}, {'name': 'page', 'kind': 'text'},
      {'name': 'by', 'kind': 'text'},
    ], rows, parameters, title=f'Statements about {self.name(record)}')
    return _with_style(block, style)

  def source_coverage(self, source_key):
    """The raw view of one source: citation, whether entered, declared
    audit, derived counts."""
    row = self.sources.get(source_key)
    if row is None:
      return {'source': source_key, 'known': False}
    return {
      'source': source_key, 'known': True, 'citation': row['citation'],
      'cite': short_citation(row['citation']), 'entered': row['tree'],
      'audit': row['audit'], 'claims': row['claims'], 'acts': row['acts'],
      'material': row['material'], 'derived': row['derived'],
      'inconsistencies': row['inconsistencies'],
    }

  def gap(self, source, kind, style='text'):
    """What the corpus says about a source's coverage of one kind of
    statement, as the sentence the contract asks for."""
    row = self.sources.get(source)
    what = COVERAGE_WORDS.get(kind, kind)
    if row is None:
      fields = {'source': source, 'known': False, 'what': what, 'kind': kind}
      block = blocks.statement('absent', {'name': f'the source {source}'}, {'source': source, 'kind': kind})
      return _with_style(block, style)
    fields = {
      'source': source, 'cite': short_citation(row['citation']), 'kind': kind,
      'what': what, 'plural': kind in _PLURAL_KINDS, 'entered': row['tree'],
      'declared': (row['audit'].get('coverage') or {}).get(kind),
      'auditState': row['audit'].get('state'),
      'derived': row['derived'].get(kind, 0),
    }
    block = blocks.statement('gap', fields, {'source': source, 'kind': kind})
    return _with_style(block, style)

  def printed_forms(self, record, source=None, style='text'):
    """Each form a source prints for a record, verbatim, with the page."""
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
      entries.append(blocks.list_entry(
        source=c['source'], cite=self.cite(c['source']), year=self.source_year(c['source']),
        claim=c['id'], page=c.get('pages'), printed=form,
      ))
    entries.sort(key=lambda e: (e['year'], e['cite'], e.get('page') is None))
    block = blocks.listing(
      {'key': record, 'name': self.name(record), 'rank': self.rank(record)},
      entries, {'record': record, 'source': source}, kind='printedForms',
    )
    return _with_style(block, style)


def _rank_order(rank):
  order = ['kingdom', 'phylum', 'subphylum', 'superclass', 'class', 'subclass',
           'superorder', 'order', 'suborder', 'superfamily', 'family',
           'subfamily', 'genus', 'subgenus', 'species', 'subspecies']
  rank = (rank or '').lower()
  return order.index(rank) if rank in order else len(order)


# -- module-level surface ---------------------------------------------------

_store = None


def store():
  global _store
  if _store is None:
    _store = ClaimStore()
  return _store


def resolve_name(query, rank=None):
  return store().resolve_name(query, rank=rank)


def contents(source=None, record=None, depth=None, synonymy=False, style='text'):
  return store().contents(source, record, depth=depth, synonymy=synonymy, style=style)


def placements(records, sources=None, years=None, include_variants=True,
               include_synonyms=True, trees=None, style='text'):
  return store().placements(records, sources, years, include_variants, include_synonyms, trees, style)


def descendants(records, include_synonyms=True, include_variants=True, trees=None, years=None, style='text'):
  return store().descendants(records, include_synonyms, include_variants, trees, years, style)


def ancestors(records, include_variants=True, trees=None, years=None, style='text'):
  return store().ancestors(records, include_variants, trees, years, style)


def history(record, include_related=True, trees=None, years=None, style='text'):
  return store().history(record, include_related, trees, years, style)


def synonymy(record, source=None, style='text'):
  return store().synonymy(record, source, style)


def statements(record, source=None, kind=None, act_kind=None, style='text'):
  return store().statements(record, source, kind, act_kind, style)


def source_coverage(source_key):
  return store().source_coverage(source_key)


def gap(source, kind, style='text'):
  return store().gap(source, kind, style)


def printed_forms(record, source=None, style='text'):
  return store().printed_forms(record, source, style)


TOOL_DESCRIPTIONS = {
  'resolve_name': (
    'Find the records a printed name can refer to. Folds ligatures, '
    'diacritics, capitals, hyphens and spaces, so "Palæaster", '
    '"Echino-encrinites" and "Edrioaster Bigsbyi" all resolve. A two-word '
    'query is a species. Each candidate gives the record key to use with '
    'the other tools, the rank, whether the record is a spelling or rank '
    'variant of another (and of which, under "variants": the same name at '
    'other ranks, which together make one group), the authority as cited, '
    'and how many sources make statements about it '
    '("sourcesWithStatements", not a count of citations of anything). A '
    'record without a name is a placeholder such as "order uncertain". An '
    'empty list means no source in the corpus carries the name; it does '
    'not mean the name does not exist. Optionally restrict by rank word.'
  ),
  'contents': (
    'What one source places under a record, as the source prints it: a '
    'classification block (the tree, with new names marked * and '
    'provisional or questionable ones ?), optionally with each name\'s '
    'synonymy. Use it to see the genera a source puts in a family, the '
    'species in a genus, or a whole scheme. With no source, one block per '
    'source that places the record. When a source\'s declared coverage of '
    'new taxa is complete, everything it names sits in this block; look '
    'here before concluding that something has not been entered.'
  ),
  'placements': (
    'Where each source places each record: a table with the records as '
    'rows (the same name at other ranks folded in), the sources as columns '
    'in publication order, and the parent each gives in the cell. The '
    'header measures the schemes: each distinct placement with its papers, '
    'years, co-author sets and last paper. Pass several records to see a '
    'group at once (for example the descendants of a family). Synonyms '
    'accepted as these records are included as rows unless told not to.'
  ),
  'descendants': (
    'Everything any source has ever placed under the given records, '
    'transitively within each source, including names accepted as their '
    'synonyms and the same names at other ranks: a table of records with '
    'rank, which sources place them and under what, and a count. This is '
    'how "what belongs to the edrioblastoids" is answered; feed its '
    'records to placements or ancestors.'
  ),
  'ancestors': (
    'Every higher taxon any source has placed the given records under, up '
    'each source\'s chain: a table with rank, the kind of edge (a '
    'placement on the chain, an alternative placement the source offers, '
    'or a placeholder such as "order uncertain"), the sources, and a '
    'count. Pass the descendants of a group to see everything the group '
    'has ever been put under.'
  ),
  'history': (
    'What each source does with a name, in publication order: one row per '
    'source with the rank used, the position given, the acts (named as '
    'new, type species, emended, nomen translatum, moved from, corrected), '
    'the printed form and the pages. The header is the measurement a '
    'trajectory needs: the latest rank and position with papers, years, '
    'co-author sets and the last paper, and the earlier ones with their '
    'last paper. Records of the same name at other ranks are included and '
    'labelled. The history reports; it passes no verdict.'
  ),
  'synonymy': (
    'The synonymy a source prints under a record, as a dated list: each '
    'earlier usage accepted or rejected, with the original combination, '
    'the cited work and page, and the printed form. Every source with one '
    'when no source is named.'
  ),
  'statements': (
    'Every statement the corpus holds about one record, in publication '
    'order and in words: what each source cites, where it places the '
    'name, what it does to it, what material it gives, whether the '
    'statement is the source\'s or the editor\'s, and the page. Filter by '
    'source, kind (usage, placement, acceptance, act, rejection, '
    'material, diagnosis, editorial) or act kind. The drill-down tool: '
    'use it to see the statement behind a cell.'
  ),
  'source_coverage': (
    'What the corpus holds of one publication: its citation, whether its '
    'content has been entered at all, the audit state and, per kind of '
    'statement, whether the reviewer declared all, part or none of what '
    'the paper prints to be entered, and the counts derived. Consult it '
    'before saying anything has not been entered: when the declared '
    'coverage for a kind is complete, a statement you have not found is '
    'one you have not looked for in the right place.'
  ),
  'gap': (
    'The sentence to give when the corpus does not hold what was asked: '
    'for a source and a kind of statement (skeleton, newTaxa, types, '
    'synonymy, material, occurrences, illustrations, diagnoses, '
    'phylogeny), whether the source is entered and what its declared '
    'coverage says, worded as work not yet done, never as the paper '
    'lacking it. Use this block, not your own words, for a gap.'
  ),
  'printed_forms': (
    'Each form a source prints for a record, verbatim, with the page: '
    'how a name, author or year appears on the page, for questions about '
    'what a paper actually prints. Never corrected.'
  ),
}

_RECORDS = {'type': 'array', 'items': {'type': 'string'}, 'description': 'record keys from resolve_name'}
_STYLE = {'type': 'string', 'enum': ['text', 'markdown', 'json'], 'description': 'rendering style, default text'}
_YEARS = {'type': 'array', 'items': {'type': ['integer', 'null']}, 'minItems': 2, 'maxItems': 2, 'description': '[first, last] publication years, either may be null'}
_TREES = {'type': 'array', 'items': {'type': 'string', 'enum': ['taxonomy', 'cladogram', 'diagram', 'other']}, 'description': 'tree kinds to read placements from; default taxonomy only'}


def _spec(name, properties, required):
  return {
    'name': name, 'description': TOOL_DESCRIPTIONS[name],
    'input_schema': {'type': 'object', 'properties': properties, 'required': required},
  }


TOOL_SPECS = [
  _spec('resolve_name', {
    'query': {'type': 'string', 'description': 'the printed name'},
    'rank': {'type': 'string', 'description': 'optional rank word'},
  }, ['query']),
  _spec('contents', {
    'source': {'type': ['string', 'null'], 'description': 'a source key; omit for every source that places the record'},
    'record': {'type': 'string', 'description': 'a record key'},
    'depth': {'type': ['integer', 'null'], 'description': 'levels below the record; omit for all'},
    'synonymy': {'type': 'boolean', 'description': 'include each name\'s synonymy'},
  }, ['record']),
  _spec('placements', {
    'records': _RECORDS,
    'sources': {'type': 'array', 'items': {'type': 'string'}, 'description': 'restrict to these source keys'},
    'years': _YEARS, 'include_variants': {'type': 'boolean'},
    'include_synonyms': {'type': 'boolean'}, 'trees': _TREES,
  }, ['records']),
  _spec('descendants', {
    'records': _RECORDS, 'include_synonyms': {'type': 'boolean'},
    'include_variants': {'type': 'boolean'}, 'trees': _TREES, 'years': _YEARS,
  }, ['records']),
  _spec('ancestors', {
    'records': _RECORDS, 'include_variants': {'type': 'boolean'},
    'trees': _TREES, 'years': _YEARS,
  }, ['records']),
  _spec('history', {
    'record': {'type': 'string'}, 'include_related': {'type': 'boolean'},
    'trees': _TREES, 'years': _YEARS,
  }, ['record']),
  _spec('synonymy', {
    'record': {'type': 'string'}, 'source': {'type': ['string', 'null']},
  }, ['record']),
  _spec('statements', {
    'record': {'type': 'string'}, 'source': {'type': ['string', 'null']},
    'kind': {'type': ['string', 'null']}, 'act_kind': {'type': ['string', 'null']},
  }, ['record']),
  _spec('source_coverage', {
    'source_key': {'type': 'string'},
  }, ['source_key']),
  _spec('gap', {
    'source': {'type': 'string'},
    'kind': {'type': 'string', 'enum': list(COVERAGE_WORDS)},
  }, ['source', 'kind']),
  _spec('printed_forms', {
    'record': {'type': 'string'}, 'source': {'type': ['string', 'null']},
  }, ['record']),
]


def call(name, arguments):
  """Dispatch a tool call by name with keyword arguments; what the CLI,
  the MCP server and the runner all go through."""
  functions = {
    'resolve_name': resolve_name, 'contents': contents,
    'placements': placements, 'descendants': descendants,
    'ancestors': ancestors, 'history': history, 'synonymy': synonymy,
    'statements': statements, 'source_coverage': source_coverage,
    'gap': gap, 'printed_forms': printed_forms,
  }
  arguments = dict(arguments)
  if 'years' in arguments and arguments['years'] is not None:
    arguments['years'] = tuple(arguments['years'])
  return functions[name](**arguments)
