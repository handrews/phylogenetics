"""Wording: the community's words for what the claim table records.

`Words` turns keys and claims into the text the blocks carry: a name as
a source prints it, a heading with its authority, a placeholder in
words, an act or a claim as a sentence, a measurement as a line. The
store holds the indices; the resolver finds keys; this module says
things.
"""

import collections
import re

from . import blocks
from .names import fold, fold_forms, key_stem

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
PLURAL_KINDS = {'newTaxa', 'types', 'occurrences', 'illustrations', 'diagnoses'}


def years_span(first, last):
  """ "1983" for one year, "1983–2020" for a range."""
  return f'{first}' if first == last else f'{first}–{last}'


def short_citation(citation):
  """ "Holloway & Jell 1983", "Sumrall et al. 2013", "Dehm 1961"."""
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


def _flat_words(value):
  """Strings from a value that may be a string, a number, or nested lists."""
  if value is None:
    return []
  if isinstance(value, (list, tuple)):
    return [w for v in value for w in _flat_words(v)]
  return [str(value)]


def _range_words(items):
  """Figures, plates or pages as printed: "2, 4–5"."""
  out = []
  for item in items if isinstance(items, list) else [items]:
    if isinstance(item, list) and len(item) == 2 and not isinstance(item[0], list):
      out.append(f'{item[0]}–{item[1]}')
    else:
      out.append(str(item))
  return ', '.join(out)


def _illustration_words(illustration):
  parts = []
  for field, word in (
    ('plate', 'pl.'),
    ('plates', 'pl.'),
    ('figures', 'fig.'),
    ('figure', 'fig.'),
    ('textFigures', 'text-fig.'),
    ('page', 'p.'),
  ):
    if illustration.get(field) is not None:
      parts.append(f'{word} {_range_words(illustration[field])}')
  for field, value in illustration.items():
    if field not in ('plate', 'plates', 'figures', 'figure', 'textFigures', 'page'):
      parts.append(f'{field} {_range_words(value)}')
  return ', '.join(parts) or 'unspecified'


class Words:
  def __init__(self, store):
    self.store = store

  def label(self, key, source=None, path=None):
    rank = self.store.rank(key)
    name = self.display(key, source, path)
    return f'{name} ({rank})' if rank and rank.lower() not in blocks.SPECIES_GROUP else name

  def combination(self, source_key, path):
    """The name a source uses at a node: for a species-group record the
    nearest genus up the chain, a subgenus between in parentheses, the
    species above a variety, then the epithet; for a subgenus "Genus
    (Subgenus)"; otherwise the record's name. Where the chain gives no
    genus the printed form is used, else the epithet alone."""
    cached = self.store._combinations_at.get((source_key, path))
    if cached is not None:
      return cached
    at = self.store.at_path[source_key].get(path, [])
    placement = self.store.closure.by_path[source_key].get(path)
    usage = next((c for c in at if c['kind'] == 'usage'), None)
    acceptance = next((c for c in at if c['kind'] == 'acceptance'), None)
    base = placement or usage or acceptance
    result = None
    if base is not None:
      key = base['subject']
      rank = self.store._rank_of(key)
      genus = subgenus = species = None
      if placement is not None:
        node = placement
        while node is not None and node.get('parent') and genus is None:
          parent = node['parent']
          parent_rank = self.store._rank_of(parent)
          if (self.store.names.get(parent) or {}).get('placeholder'):
            # A bin above the species is not a genus; the name falls back
            # to the printed form or the epithet.
            break
          if parent_rank == 'subgenus' and subgenus is None:
            subgenus = parent
          elif parent_rank == 'genus':
            genus = parent
          elif parent_rank == 'species' and species is None:
            species = parent
          node = self.store.closure.parent_claim(source_key, node)
      elif acceptance is not None and '/' in path:
        # A cited name: the original combination when the entry gives it,
        # else the genus of the node it sits under.
        parents = acceptance.get('parents') or []
        if parents:
          genus = parents[0]
          subgenus = parents[1] if len(parents) > 1 else None
        else:
          owner = self.combination(source_key, path.rsplit('/', 2)[0])
          genus, subgenus = owner.get('genus'), owner.get('subgenus')
      if rank == 'subgenus':
        genus = genus or self._genus_of_subgenus(key)
        label = (
          f'{self.store.name(genus)} ({self.store.name(key)})' if genus else self.store.name(key)
        )
      elif (
        rank in blocks.SPECIES_GROUP
        and not self.store.names[key].get('name')
        and self.store.names[key].get('designation')
      ):
        # An unnamed species designated as printed ("Rhenopyrgus sp. indet. 1").
        label = self.store.names[key]['designation']
      elif rank in blocks.SPECIES_GROUP:
        parts = []
        if genus:
          parts.append(self.store.name(genus))
          if subgenus:
            parts.append(f'({self.store.name(subgenus)})')
          if species and rank != 'species':
            parts.append(self.store.name(species))
          tail = (
            self._open_tail(key, [genus, subgenus, species])
            if self.store.names[key].get('placeholder')
            else None
          )
          if rank == 'variety' and not (tail and tail.startswith('var.')):
            parts.append('var.')
          parts.append(tail if tail is not None else self.store.name(key))
        else:
          # No genus in the chain: a placeholder in its words, a named
          # species by its epithet; the corpus invents no genus.
          parts.append(
            self.placeholder_words(key, source_key, path)
            if self.store.names[key].get('placeholder')
            else self.store.name(key)
          )
        label = ' '.join(parts)
      else:
        label = self.store.name(key)
      result = {
        'label': label,
        'record': key,
        'genus': genus,
        'subgenus': subgenus,
        'species': species,
        'keys': [k for k in (genus, subgenus, species, key) if k],
      }
    self.store._combinations_at[(source_key, path)] = result or {}
    return result or {}

  def _genus_of_subgenus(self, key):
    """The genus a subgenus sits in, from its own placements, for the
    places a subgenus is cited without its chain."""
    counts = collections.Counter()
    for claim in self.store.closure.placements_of.get(key, ()):
      parent = claim.get('parent')
      if parent and self.store._rank_of(parent) == 'genus':
        counts[parent] += 1
    return counts.most_common(1)[0][0] if counts else None

  def combinations(self, key):
    """A species-group record's distinct combinations across the taxonomy
    trees, each with its sources and years."""
    found = {}
    for claim in self.store.closure.placements_of.get(key, ()):
      if claim['tree'] != 'taxonomy':
        continue
      label = self.combination(claim['source'], claim['path']).get('label')
      if not label:
        continue
      entry = found.setdefault(label, {'label': label, 'sources': set()})
      entry['sources'].add(claim['source'])
    out = []
    for entry in found.values():
      sources = sorted(entry['sources'], key=lambda s: (self.store.source_year(s), s))
      out.append(
        {
          'label': entry['label'],
          'sources': sources,
          'firstYear': self.store.source_year(sources[0]),
          'lastYear': self.store.source_year(sources[-1]),
        }
      )
    out.sort(key=lambda e: (e['firstYear'], e['label']))
    return out

  def display(self, key, source=None, path=None):
    """How a name is shown: the combination at a node when the node is
    known; a species-group record's combinations joined when it is not;
    the name otherwise."""
    if (self.store.names.get(key) or {}).get('placeholder') and self.store._rank_of(
      key
    ) not in blocks.SPECIES_GROUP:
      return self.placeholder_words(key, source, path)
    if source is not None and path is not None:
      label = self.combination(source, path).get('label')
      if label and self.combination(source, path).get('record') == key:
        return label
    if self.store._rank_of(key) in blocks.SPECIES_GROUP:
      combos = self.combinations(key)
      if combos:
        return ' / '.join(c['label'] for c in combos)
      if (self.store.names.get(key) or {}).get('placeholder'):
        return self.placeholder_words(key)
    if self.store._rank_of(key) == 'subgenus':
      genus = self._genus_of_subgenus(key)
      if genus:
        return f'{self.store.name(genus)} ({self.store.name(key)})'
    return self.store.name(key)

  _OPEN_WORDS = {
    'sp': 'sp.',
    'spp': 'spp.',
    'gen': 'gen.',
    'indet': 'indet.',
    'cf': 'cf.',
    'aff': 'aff.',
    'nov': 'nov.',
    'n': 'n.',
    'var': 'var.',
  }

  def placeholder_words(self, key, source=None, path=None):
    """A placeholder in the source's words: a bin by its rank ("Order
    uncertain", "Unnamed family"), an open-nomenclature record by its
    designation, or the words of its key ("Agelacrinites sp.")."""
    row = self.store.names.get(key) or {}
    kind = row.get('placeholder')
    rank = (row.get('rank') or '').lower()
    if kind == 'uncertain':
      return f'{rank.capitalize()} uncertain' if rank else 'Uncertain'
    if kind == 'unnamed':
      return f'Unnamed {rank}' if rank else 'Unnamed'
    if row.get('designation'):
      return row['designation']
    words = [self._OPEN_WORDS.get(w, w) for w in key_stem(key).split('-')]
    return ' '.join(words)[:1].upper() + ' '.join(words)[1:]

  def _open_tail(self, key, chain_keys):
    """The words of an open-nomenclature record's key after the names
    its chain already gives: "sp. a", "var. 1", "sp. indet."."""
    known = {fold(self.store.name(k)) for k in chain_keys if k}
    tokens = key_stem(key).split('-')
    while tokens and fold(tokens[0]) in known:
      tokens.pop(0)
    return ' '.join(self._OPEN_WORDS.get(w, w) for w in tokens)

  def original_combination(self, key):
    """The combination a species-group record was published in, when the
    corpus knows it: its placement in the authority's own paper, the
    original combination a synonymy entry gives, or the parent recorded
    with it. None otherwise."""
    row = self.store.names.get(key) or {}
    auth_source = (row.get('authority') or {}).get('source')
    if auth_source in self.store.sources:
      for c in self.store.by_subject.get(key, ()):
        if c['source'] == auth_source and c['kind'] == 'placement':
          combo = self.combination(auth_source, c['path'])
          if combo.get('genus'):
            return combo['label']
    for c in self.store.by_subject.get(key, ()):
      parents = c.get('parents') if c['kind'] == 'acceptance' else None
      if parents:
        parts = [self.store.name(parents[0])]
        if len(parents) > 1:
          parts.append(f'({self.store.name(parents[1])})')
        return ' '.join(parts + [self.store.name(key)])
    original = row.get('originalParent')
    if original:
      genus = self.store.name(original) if original in self.store.names else original
      return f'{genus} {self.store.name(key)}'
    return None

  def authority_words(self, key):
    """The recorded authority in the corpus's citation form ("Holloway &
    Jell 1983", "Bather in Smith 1900"), or as displayed when the parts
    are not recorded."""
    authority = (self.store.names.get(key) or {}).get('authority') or {}
    if authority.get('authors'):
      words = short_citation({'authors': authority['authors'], 'year': None}).rsplit(' ', 2)[0]
      if authority.get('in'):
        words += (
          ' in ' + short_citation({'authors': authority['in'], 'year': None}).rsplit(' ', 2)[0]
        )
      year = authority.get('year')
      return f'{words} {year}' if year else words
    return authority.get('display')

  def _asked_label(self, key, asked):
    """The combination a query named, in the corpus's spelling."""
    wanted = fold_forms(asked)
    for combo in self.combinations(key):
      label = combo['label']
      bare = re.sub(r' \([^)]*\)', '', label)
      if wanted & (fold_forms(label) | fold_forms(bare)):
        return label
    if wanted & fold_forms(self.store.name(key)):
      return self.store.name(key)
    return asked.strip()

  def heading(self, key, asked=None):
    """A record as a block names it: the combination asked for (else
    the original one, else the latest) with the recorded author, in
    parentheses when the corpus knows the name is a recombination."""
    row = self.store.names.get(key) or {}
    if row.get('placeholder'):
      return self.placeholder_words(key)
    author = self.authority_words(key)
    if self.store._rank_of(key) in blocks.SPECIES_GROUP:
      original = self.original_combination(key)
      if asked:
        shown = self._asked_label(key, asked)
      else:
        combos = self.combinations(key)
        latest = max(combos, key=lambda c: c['lastYear'])['label'] if combos else None
        shown = original or latest or self.store.name(key)
      recombined = bool(
        original and ' ' in shown and fold(shown.split()[0]) != fold(original.split()[0])
      )
      if not author:
        return shown
      return f'{shown} ({author})' if recombined else f'{shown} {author}'
    shown = self.display(key)
    return f'{shown} {author}' if author else shown

  @staticmethod
  def asked(raw, key):
    """The query as typed when it was a printed name rather than a key."""
    if raw is None or raw == key or str(raw).lower() == key:
      return None
    return str(raw)

  def act_words(self, claim):
    kind = claim.get('actKind')
    origin = claim.get('translatedFrom')
    words = {
      'new': 'named as new',
      'placeholder': 'placeholder introduced',
      'type': 'type species',
      'emended': 'emended',
      'nomTransl': 'nomen translatum' + (f' from {self.store.name(origin)}' if origin else ''),
      'nomNudum': 'nomen nudum',
      'corrected': f'corrected from {self.store.name(claim.get("correctedFrom", ""))}',
      'moved': f'moved from {self.store.name(claim.get("movedFrom", ""))}',
      'removed': f'removed from {self.store.name(claim.get("removedFrom", ""))}',
    }.get(kind, kind or '')
    # An act the source follows rather than performs names the work.
    if claim.get('by'):
      words += f' by {self.store.cite(claim["by"])}'
      if claim.get('byPages') is not None:
        words += f', p. {_range_words(claim["byPages"])}'
    if claim.get('inferred'):
      basis = (claim.get('editorial') or {}).get('basis', '').strip()
      words += ' (inferred by the editor' + (f': {basis}' if basis else '') + ')'
    return words

  def claim_words(self, claim):
    kind = claim['kind']
    if kind == 'usage':
      attributed = self.attribution_words(claim.get('printed') or {})
      words = f'cites the name, attributed to {attributed}' if attributed else 'cites the name'
      if claim.get('sensu'):
        words += f' sensu {claim["sensu"]}'
      return words + self.error_words(claim)
    if kind == 'placement':
      parent = claim.get('parent')
      where = self.display(parent) if parent else 'an unnamed group'
      flags = [f for f in ('provisional', 'questionable', 'quoted') if claim.get(f)]
      words = f'places it under {where}'
      if flags:
        words += ' (' + ', '.join(flags) + ')'
      if claim.get('tree') != 'taxonomy':
        words += f' in a {claim["tree"]}'
      return words
    if kind == 'acceptance':
      target = self.display(claim['subject'], claim['source'], claim['path'])
      verb = 'accepts' if claim['stance'] == 'accepts' else 'rejects'
      cited = f' ({self.store.cite(claim["citesSource"])})' if claim.get('citesSource') else ''
      under = ''
      if claim.get('under'):
        under = self.display(claim['under'], claim['source'], claim['path'].rsplit('/', 2)[0])
      return f'{verb} {target}{cited} as {under}' if under else f'{verb} {target}{cited}'
    if kind == 'act':
      return self.act_words(claim)
    if kind == 'rejection':
      return f'declines a placement in {self.display(claim.get("declinedParent", ""))}'
    if kind == 'material':
      mk = claim['materialKind']
      if mk == 'specimen':
        ids = ', '.join(_flat_words(claim.get('ids')))
        repo = f' {claim["repository"]}' if claim.get('repository') else ''
        return f'{claim.get("role", "specimens")}:{repo} {ids}'.strip()
      if mk == 'occurrence':
        occ = claim.get('occurrence') or {}
        parts = [
          ', '.join(_flat_words(occ.get(k)))
          for k in ('stage', 'series', 'unit', 'location')
          if occ.get(k)
        ]
        return 'occurrence: ' + '; '.join(p for p in parts if p) if parts else 'occurrence'
      return 'illustration: ' + _illustration_words(claim.get('illustration') or {})
    if kind == 'diagnosis':
      return 'diagnosis: ' + (claim.get('text') or '').strip().replace('\n', ' ')
    if kind == 'editorial':
      words = "editor's note: " + (claim.get('basis') or '').strip()
      wrong = claim.get('printedErrors')
      if wrong:
        words = f'{", ".join(wrong)} printed in error; ' + words
      return words
    return kind

  def error_words(self, claim):
    """The clause for a printed attribution the editor reads as wrong,
    with the source the corrections resolve it to when they do."""
    errors = claim.get('printedErrors')
    if not errors:
      return ''
    words = f'printed {", ".join(errors)} in error'
    source = (claim.get('corrected') or {}).get('citesSource')
    if source and source in self.store.sources:
      words += f'; read as {self.store.cite(source)}'
    return f' ({words})'

  def scheme_lines(self, schemes):
    lines = []
    for s in schemes:
      parents = ' / '.join(self.display(p['key']) for p in s['parents'])
      span = years_span(s['firstYear'], s['lastYear'])
      lines.append(
        f'{parents}: {s["papers"]} paper{"s" if s["papers"] != 1 else ""} '
        f'({span}), {len(s["coauthorSets"])} co-author set'
        f'{"s" if len(s["coauthorSets"]) != 1 else ""}, last {self.store.cite(s["lastSource"])}'
      )
    return lines

  def variant_words(self, key, base):
    """How a record reached by a variant edge relates to the record it
    is a variant of: a spelling at the same rank, or the name at another
    rank."""
    of = self.store.names[key].get('of') == base or self.store.names[base].get('of') == key
    same_rank = (self.store.rank(key) or '').lower() == (self.store.rank(base) or '').lower()
    if same_rank:
      return f'{"spelling" if of else "same name"} variant of {self.display(base)}'
    return f'same name at another rank as {self.display(base)}'

  def attribution_words(self, printed):
    """A printed attribution by its fields: "Bell, 1974", "Bather in Bell,
    1976", "Hall". Author keys become surnames through the manifest's
    authors map; a string with no record (a capitalised name as printed)
    stays as it is. Empty when nothing is printed."""

    def names(keys):
      return ', '.join(self.store.authors.get(k, k) for k in keys or ())

    words = names(printed.get('auth'))
    if printed.get('in'):
      words = f'{words} in {names(printed["in"])}' if words else f'in {names(printed["in"])}'
    if printed.get('year'):
      words = f'{words}, {printed["year"]}' if words else str(printed['year'])
    return words

  def authors(self, source_key):
    """The short citation without its year, for a line that shows the
    year in its own column."""
    cite = self.store.cite(source_key)
    year = str(self.store.source_year(source_key))
    return cite[: -len(year)].rstrip() if cite.endswith(year) else cite

  def rank_lines(self, m):
    rows = m['ranks']
    if len(rows) < 2:
      return None
    latest = rows[0]
    parts = []
    for r in rows:
      if r is latest and r['lastSource'] == m['sources'][-1]:
        span = f'since {r["firstYear"]}'
      else:
        span = years_span(r['firstYear'], r['lastYear'])
      parts.append(f'{r["rank"]} {span} ({r["papers"]} paper{"s" if r["papers"] != 1 else ""})')
    return ', '.join(parts)

  def position_lines(self, m):
    schemes = m['positions']
    if not schemes:
      return None
    parts = []
    for i, s in enumerate(schemes):
      parents = ' / '.join(self.display(p['key']) for p in s['parents'])
      if i == 0 and s['lastSource'] == m['sources'][-1]:
        span = f'since {s["firstYear"]}'
      else:
        span = years_span(s['firstYear'], s['lastYear'])
      sets = len(s['coauthorSets'])
      parts.append(
        f'in {parents} {span} ({s["papers"]} paper{"s" if s["papers"] != 1 else ""}'
        + (f', {sets} co-author sets' if sets != s['papers'] else '')
        + ')'
      )
    return ', '.join(parts)
