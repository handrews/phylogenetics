"""The four read-only tools over the committed claim table.

Everything here reads `claims/` (the JSONL per source, `manifest.json`,
`names.json`) and returns plain dicts. Nothing writes, nothing infers, and
an empty result is the closed-world answer: the corpus holds nothing that
matches. The MCP server and the eval runner call these functions directly.
"""

import collections
import json
import pathlib

from .names import fold_forms

CLAIMS_DIR = pathlib.Path(__file__).parent / '..' / 'claims'

_KIND_ORDER = {
  'primary': 0, 'altRankOf': 1, 'altSpellingOf': 2, 'vulgarSpellingOf': 3,
  'placeholder': 4,
}
_PLACEMENT_FLAGS = (
  'provisional', 'questionable', 'quoted', 'pars', 'tentative', 'outgroup',
  'stem', 'altPlacements', 'placeholder', 'parentPlaceholder', 'via',
  'inferred',
)


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
    for path in sorted(directory.glob('*.jsonl')):
      claims = []
      with open(path) as fd:
        for line in fd:
          claim = json.loads(line)
          claims.append(claim)
          if claim.get('subject') is not None:
            self.by_subject[claim['subject']].append(claim)
      self.by_source[path.stem] = claims

    self.by_folded = collections.defaultdict(list)
    for key, row in self.names.items():
      for form in row['folded']:
        self.by_folded[form].append(key)

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

  def _claim_order(self, claim):
    return (self.source_year(claim['source']), claim['source'])

  def _view(self, claim):
    view = dict(claim)
    view['sourceCitation'] = self.cite(claim['source'])
    if 'citesSource' in claim:
      view['citesSourceCitation'] = self.cite(claim['citesSource'])
    return view

  def _candidate(self, key):
    row = self.names[key]
    entry = {
      'key': key,
      'name': row['name'],
      'rank': row['rank'],
      'kind': row['kind'],
      'sources': len({c['source'] for c in self.by_subject.get(key, ())}),
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

  # -- the tools -----------------------------------------------------------

  def resolve_name(self, query, rank=None):
    """Records a printed name can mean, folded for typographical variation.

    A two-word query resolves the epithet and keeps the records some
    source places under a genus whose name matches the first word. The
    empty list means no record in the corpus carries the name.
    """
    query = query.strip()
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
      _KIND_ORDER.get(c['kind'], 9), -c['sources'], c['name'] or '', c['key'],
    ))
    return candidates

  def claims_about(self, taxon_key, source=None, kind=None, act_kind=None):
    """Every statement the corpus holds about one record, in publication
    order, each with its source, page and printed form."""
    claims = self.by_subject.get(taxon_key, [])
    if source is not None:
      claims = [c for c in claims if c['source'] == source]
    if kind is not None:
      claims = [c for c in claims if c['kind'] == kind]
    if act_kind is not None:
      claims = [c for c in claims if c.get('actKind') == act_kind]
    claims = sorted(claims, key=self._claim_order)
    return [self._view(c) for c in claims]

  def source_coverage(self, source_key):
    """What the corpus holds of one source: its citation, whether its
    content has been entered, the declared audit and coverage, and the
    counts of statements by kind."""
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

  def name_history(self, taxon_key, include_related=True):
    """What each source does with a name, in publication order: where it
    is placed, what is done to it, which earlier usages are accepted or
    rejected. With include_related, the records that carry the same name
    at another rank or spelling are included and labelled."""
    keys = [taxon_key]
    if include_related:
      keys += self.related_keys(taxon_key)
    by_source = collections.defaultdict(list)
    for key in keys:
      for claim in self.by_subject.get(key, ()):
        by_source[claim['source']].append(claim)

    history = []
    for source_key in sorted(by_source, key=lambda s: (self.source_year(s), s)):
      entry = {
        'source': source_key,
        'cite': self.cite(source_key),
        'year': self.sources.get(source_key, {}).get('citation', {}).get('year'),
        'placements': [],
        'acts': [],
        'acceptances': [],
        'rejections': [],
      }
      for claim in by_source[source_key]:
        record = {'record': claim['subject'], 'id': claim['id']}
        if claim['subject'] != taxon_key:
          record['recordRank'] = self.names[claim['subject']]['rank']
        if claim.get('pages') is not None:
          record['pages'] = claim['pages']
        if 'printed' in claim:
          record['printed'] = claim['printed']
        if 'notes' in claim:
          record['notes'] = claim['notes']
        if claim['kind'] == 'placement':
          parent = claim.get('parent')
          record.update({
            'parent': parent,
            'parentName': self.names.get(parent, {}).get('name') if parent else None,
            'rank': claim.get('rank'),
            'tree': claim.get('tree'),
          })
          for flag in _PLACEMENT_FLAGS:
            if flag in claim:
              record[flag] = claim[flag]
          entry['placements'].append(record)
        elif claim['kind'] == 'act':
          record['act'] = claim['actKind']
          for field in (
            'movedFrom', 'correctedFrom', 'removedFrom', 'altRankOf',
            'modifier', 'inferred', 'editorial',
          ):
            if field in claim:
              record[field] = claim[field]
          entry['acts'].append(record)
        elif claim['kind'] == 'acceptance':
          record.update({
            'stance': claim['stance'],
            'under': claim.get('under'),
            'parents': claim.get('parents'),
          })
          for field in ('citesSource', 'citedPages', 'pars', 'tentative'):
            if field in claim:
              record[field] = claim[field]
          if 'citesSource' in claim:
            record['citesSourceCitation'] = self.cite(claim['citesSource'])
          entry['acceptances'].append(record)
        elif claim['kind'] == 'rejection':
          record['declinedParent'] = claim.get('declinedParent')
          entry['rejections'].append(record)
      history.append(entry)
    return history


_store = None


def store():
  global _store
  if _store is None:
    _store = ClaimStore()
  return _store


def resolve_name(query, rank=None):
  return store().resolve_name(query, rank=rank)


def claims_about(taxon_key, source=None, kind=None, act_kind=None):
  return store().claims_about(taxon_key, source=source, kind=kind, act_kind=act_kind)


def source_coverage(source_key):
  return store().source_coverage(source_key)


def name_history(taxon_key, include_related=True):
  return store().name_history(taxon_key, include_related=include_related)
