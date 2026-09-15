"""Resolution: what a printed name or a citation means in the corpus.

A `Resolver` holds the store's indices and answers the lookups: the
records a printed name can refer to, the sources a citation can mean,
the key a tool parameter names, and the records related to one by rank
variants and spellings. Nothing here builds a block or a sentence.
"""

import html
import re

from . import blocks
from .names import fold, fold_forms
from .words import short_citation


def _species_group(rank):
  return (rank or '').lower() in blocks.SPECIES_GROUP


_KIND_ORDER = {
  'primary': 0,
  'altRankOf': 1,
  'altSpellingOf': 2,
  'vulgarSpellingOf': 3,
  'placeholder': 4,
}


class Resolver:
  def __init__(self, store):
    self.store = store

  # What a parameter value of each kind is looked up in, and resolved by.
  _KINDS = {
    'record': ('names', 'resolve_name', 'records'),
    'source': ('sources', 'resolve_source', 'sources'),
  }

  def key_of(self, kind, value):
    """The key a parameter value names: a record's or a source's, as given
    when it is a key, lowercased when only that form exists (keys are
    lowercase, printed names are not), or the one record or source the
    printed name or citation resolves to. A value that can mean several
    is refused with the candidates, since a tool cannot choose among
    them; an unknown one passes through, so the answer can say the
    corpus holds nothing that matches."""
    index_name, resolve, plural = self._KINDS[kind]
    index = getattr(self.store, index_name)
    if value is None or value in index:
      return value
    lowered = str(value).lower()
    if lowered in index:
      return lowered
    candidates = getattr(self, resolve)(str(value))
    if len(candidates) == 1:
      return candidates[0]['key']
    if candidates:
      raise ValueError(
        f'"{value}" can mean several {plural}: '
        + ', '.join(c['key'] for c in candidates)
        + '; name one by its key'
      )
    return value

  def key(self, key):
    return self.key_of('record', key)

  def keys(self, keys):
    return [self.key_of('record', k) for k in keys]

  _YEAR_TOKEN = re.compile(r'^(\d{4})([a-z])?$')

  _CITATION_NOISE = {'et', 'al', 'in', 'prep', 'preparation', 'and'}

  def source_signature(self, text):
    """What a citation or a key says about a paper: the year (with a
    key's letter suffix when given), the authors' names folded, and
    whether it is a work in preparation."""
    # A model may write the ampersand as an entity ("Holloway &amp; Jell").
    text = html.unescape((text or '').strip())
    sig = {'year': None, 'suffix': None, 'authors': [], 'inprep': False}
    if not text:
      return sig
    # A key, known or not: year and letter, then authors with initials.
    if re.match(r'^(\d{4}[a-z]?|inprep)_', text.lower()):
      head, _, rest = text.lower().partition('_')
      match = self._YEAR_TOKEN.match(head)
      if match:
        sig['year'], sig['suffix'] = int(match.group(1)), match.group(2)
      else:
        sig['inprep'] = True
      sig['authors'] = [fold(part.split('.')[0]) for part in rest.split('_') if part]
      return sig
    for token in re.split(r'[\s,&;]+', text):
      token = token.strip('().')
      if not token:
        continue
      match = self._YEAR_TOKEN.match(token)
      if match:
        sig['year'], sig['suffix'] = int(match.group(1)), match.group(2)
      elif token.lower() in self._CITATION_NOISE:
        sig['inprep'] = sig['inprep'] or token.lower().startswith('prep')
      else:
        sig['authors'].append(fold(token))
    return sig

  def resolve_source(self, query):
    """The sources a citation can mean: the papers of that year (and
    letter, "Fay 1967a") whose authors begin with the authors named, in
    the order named. "Sumrall et al. 2013" names one author; "Holloway &
    Jell 1983" two. A key is its own answer."""
    query = html.unescape((query or '').strip())
    if not query:
      return []
    if query in self.store.sources or query.lower() in self.store.sources:
      key = query if query in self.store.sources else query.lower()
      return [self._source_candidate(key)]
    sig = self.source_signature(query)
    if sig['year'] is None and not sig['inprep']:
      return []
    found = []
    for key, row in self.store.sources.items():
      citation = row['citation']
      year = citation.get('year')
      if sig['year'] is not None:
        if year != sig['year']:
          continue
        if sig['suffix'] and not key.split('_', 1)[0].endswith(sig['suffix']):
          continue
      elif year is not None:
        continue
      authors = [fold(a) for a in citation.get('authors') or ()]
      if authors[: len(sig['authors'])] != sig['authors']:
        continue
      found.append(self._source_candidate(key))
    found.sort(key=lambda c: (c['year'] or 9999, c['key']))
    return found

  def _source_candidate(self, key):
    row = self.store.sources[key]
    return {
      'key': key,
      'cite': short_citation(row['citation']),
      'year': row['citation'].get('year'),
      'entered': bool(row.get('tree')),
      'authors': list(row['citation'].get('authors') or ()),
    }

  def source_key(self, key):
    return self.key_of('source', key)

  def source_keys(self, keys):
    return [self.key_of('source', k) for k in keys]

  def related_keys(self, taxon_key):
    """Records sharing the name at another rank or spelling, and the
    base or variants a record is linked to. An epithet is not a name on
    its own, so species-group records relate only through explicit
    links: two species called casteri in different genera are different
    names."""
    row = self.store.names.get(taxon_key)
    if row is None:
      return []
    keys = set()
    if not _species_group(row.get('rank')):
      for form in row['folded']:
        keys.update(
          k for k in self.store.by_folded.get(form, ()) if not _species_group(self.store.rank(k))
        )
    if 'of' in row:
      keys.add(row['of'])
    for key, other in self.store.names.items():
      if other.get('of') == taxon_key:
        keys.add(key)
    keys.discard(taxon_key)
    return sorted(keys)

  def _candidate(self, key):
    row = self.store.names[key]
    entry = {
      'key': key,
      'name': row['name'],
      'rank': row['rank'],
      'kind': row['kind'],
      'sourcesWithStatements': len({c['source'] for c in self.store.by_subject.get(key, ())}),
      'variants': self.related_keys(key),
    }
    for field in ('of', 'placeholder', 'homonym', 'originalParent'):
      if field in row:
        entry[field] = row[field]
    if 'authority' in row:
      entry['authority'] = row['authority'].get('display')
      if 'source' in row['authority']:
        entry['authoritySource'] = row['authority']['source']
    if (row['rank'] or '').lower() in blocks.SPECIES_GROUP:
      entry['combinations'] = self.store.words.combinations(key)
    return entry

  def _resolve_combination(self, words):
    """A multi-word query is a combination as the literature writes it:
    "Genus species", "Genus (Subgenus) species", "Genus species
    subspecies", or "Genus (Subgenus)" for the subgenus itself. The
    record is the last name; the rest must be the chain some source
    gives it (the subgenus may be left out of the query)."""
    bare = [w.strip('()') for w in words]
    if len(words) == 2 and words[1].startswith('('):
      genus_forms, sub_forms = fold_forms(bare[0]), fold_forms(bare[1])
      return {
        k
        for form in sub_forms
        for k in self.store.by_folded.get(form, ())
        if self.store._rank_of(k) == 'subgenus'
        and genus_forms & fold_forms(self.store.name(self.store.words._genus_of_subgenus(k) or ''))
      }
    wanted = fold_forms(' '.join(bare))
    epithet_keys = {
      k
      for form in fold_forms(bare[-1])
      for k in self.store.by_folded.get(form, ())
      if self.store._rank_of(k) in blocks.SPECIES_GROUP
    }
    keys = set()
    for k in epithet_keys:
      for combo in self.store.words.combinations(k):
        label = combo['label']
        without_subgenus = re.sub(r' \([^)]*\)', '', label)
        if wanted & (fold_forms(label) | fold_forms(without_subgenus)):
          keys.add(k)
          break
    if not keys:
      # A species no source places under a genus: the chain the first
      # description gives, or the parent recorded with it.
      genus_forms = fold_forms(bare[0])
      keys = {k for k in epithet_keys if self._placed_under(k, genus_forms)}
      if not keys:
        keys = {
          k
          for k in epithet_keys
          if genus_forms & fold_forms(self.store.names[k].get('originalParent') or '')
        }
    return keys

  def _placed_under(self, key, genus_forms):
    for claim in self.store.by_subject.get(key, ()):
      if claim['kind'] != 'placement' or claim.get('parent') is None:
        continue
      parent = self.store.names.get(claim['parent'])
      if parent and genus_forms & set(parent['folded']):
        return True
    return False

  def resolve_name(self, query, rank=None):
    query = (query or '').strip()
    if not query:
      return []
    forms = fold_forms(query)
    keys = {k for form in forms for k in self.store.by_folded.get(form, ())}

    words = query.split()
    if not keys and len(words) >= 2:
      keys = self._resolve_combination(words)

    if not keys and len(words) == 1 and len(query) >= 4:
      prefixes = tuple(forms)
      keys = {
        k for form, ks in self.store.by_folded.items() if form.startswith(prefixes) for k in ks
      }

    if rank is not None:
      wanted = rank.lower()
      keys = {k for k in keys if (self.store.names[k]['rank'] or '').lower() == wanted}

    candidates = [self._candidate(k) for k in keys]
    candidates.sort(
      key=lambda c: (
        _KIND_ORDER.get(c['kind'], 9),
        -c['sourcesWithStatements'],
        c['name'] or '',
        c['key'],
      )
    )
    return candidates
