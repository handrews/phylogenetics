"""The read-only tools over the committed claim table, returning blocks.

Everything here reads `claims/` (the JSONL per source, `manifest.json`,
`names.json`) and returns blocks (`blocks.py`) rendered in a style
(`render.py`), or plain dicts for the resolver and the coverage view.
Nothing writes, nothing infers, and an empty result is the closed-world
answer: the corpus holds nothing that matches. The CLI, the MCP server
and the eval runner call these functions directly.
"""

import collections
import re
import json
import pathlib

from . import blocks
from .closure import Closure, TAXONOMY, _in_years
from .names import fold, fold_forms, key_stem
from .render import render

CLAIMS_DIR = pathlib.Path(__file__).parent / '..' / 'claims'

_KIND_ORDER = {
  'primary': 0, 'altRankOf': 1, 'altSpellingOf': 2, 'vulgarSpellingOf': 3,
  'placeholder': 4,
}
_NODE_FLAGS = ('new', 'provisional', 'questionable', 'quoted')
_SPECIES_GROUP = ('species', 'subspecies', 'variety')


def _species_group(rank):
  return (rank or '').lower() in _SPECIES_GROUP

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
    self._combinations_at = {}

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
    """The record's name; an unnamed record's printed designation
    ("Rhenopyrgus sp. indet. 1") when it has one, else its key in
    brackets."""
    row = self.names.get(key) or {}
    return row.get('name') or row.get('designation') or f'[{key}]'

  def _key(self, key):
    """A record or source key as given, or lowercased when only that form
    exists (keys are lowercase, printed names are not), or the one record
    a printed name resolves to. A name that can mean several records is
    refused with the candidates, since a tool cannot choose among them."""
    if key is None or key in self.names or key in self.sources:
      return key
    lowered = key.lower()
    if lowered in self.names or lowered in self.sources:
      return lowered
    candidates = self.resolve_name(key)
    if len(candidates) == 1:
      return candidates[0]['key']
    if candidates:
      raise ValueError(
        f'"{key}" can mean several records: ' + ', '.join(c['key'] for c in candidates)
        + '; name one by its key'
      )
    return key

  def _keys(self, keys):
    return [self._key(k) for k in keys]

  def rank(self, key):
    return (self.names.get(key) or {}).get('rank')

  def label(self, key, source=None, path=None):
    rank = self.rank(key)
    name = self.display(key, source, path)
    return f'{name} ({rank})' if rank and rank.lower() not in _SPECIES_GROUP else name

  def _rank_of(self, key):
    return (self.rank(key) or '').lower()

  def combination(self, source_key, path):
    """The name a source uses at a node: for a species-group record the
    nearest genus up the chain, a subgenus between in parentheses, the
    species above a variety, then the epithet; for a subgenus "Genus
    (Subgenus)"; otherwise the record's name. Where the chain gives no
    genus the printed form is used, else the epithet alone."""
    cached = self._combinations_at.get((source_key, path))
    if cached is not None:
      return cached
    at = self.at_path[source_key].get(path, [])
    placement = self.closure.by_path[source_key].get(path)
    usage = next((c for c in at if c['kind'] == 'usage'), None)
    acceptance = next((c for c in at if c['kind'] == 'acceptance'), None)
    base = placement or usage or acceptance
    result = None
    if base is not None:
      key = base['subject']
      rank = self._rank_of(key)
      genus = subgenus = species = None
      if placement is not None:
        node = placement
        while node is not None and node.get('parent') and genus is None:
          parent = node['parent']
          parent_rank = self._rank_of(parent)
          if (self.names.get(parent) or {}).get('placeholder'):
            # A bin above the species is not a genus; the name falls back
            # to the printed form or the epithet.
            break
          if parent_rank == 'subgenus' and subgenus is None:
            subgenus = parent
          elif parent_rank == 'genus':
            genus = parent
          elif parent_rank == 'species' and species is None:
            species = parent
          node = self.closure.parent_claim(source_key, node)
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
        label = f'{self.name(genus)} ({self.name(key)})' if genus else self.name(key)
      elif rank in _SPECIES_GROUP and not self.names[key].get('name') and self.names[key].get('designation'):
        # An unnamed species designated as printed ("Rhenopyrgus sp. indet. 1").
        label = self.names[key]['designation']
      elif rank in _SPECIES_GROUP:
        parts = []
        if genus:
          parts.append(self.name(genus))
          if subgenus:
            parts.append(f'({self.name(subgenus)})')
          if species and rank != 'species':
            parts.append(self.name(species))
          tail = self._open_tail(key, [genus, subgenus, species]) if self.names[key].get('placeholder') else None
          if rank == 'variety' and not (tail and tail.startswith('var.')):
            parts.append('var.')
          parts.append(tail if tail is not None else self.name(key))
        else:
          printed = (usage or {}).get('printed') or {}
          parts.append(printed.get('citedAs') or self.placeholder_words(key, source_key, path)
                       if self.names[key].get('placeholder') else
                       printed.get('citedAs') or self.name(key))
        label = ' '.join(parts)
      else:
        label = self.name(key)
      result = {
        'label': label, 'record': key, 'genus': genus, 'subgenus': subgenus,
        'species': species,
        'keys': [k for k in (genus, subgenus, species, key) if k],
      }
    self._combinations_at[(source_key, path)] = result or {}
    return result or {}

  def _genus_of_subgenus(self, key):
    """The genus a subgenus sits in, from its own placements, for the
    places a subgenus is cited without its chain."""
    counts = collections.Counter()
    for claim in self.closure.placements_of.get(key, ()):
      parent = claim.get('parent')
      if parent and self._rank_of(parent) == 'genus':
        counts[parent] += 1
    return counts.most_common(1)[0][0] if counts else None

  def combinations(self, key):
    """A species-group record's distinct combinations across the taxonomy
    trees, each with its sources and years."""
    found = {}
    for claim in self.closure.placements_of.get(key, ()):
      if claim['tree'] != 'taxonomy':
        continue
      label = self.combination(claim['source'], claim['path']).get('label')
      if not label:
        continue
      entry = found.setdefault(label, {'label': label, 'sources': set()})
      entry['sources'].add(claim['source'])
    out = []
    for entry in found.values():
      sources = sorted(entry['sources'], key=lambda s: (self.source_year(s), s))
      out.append({
        'label': entry['label'], 'sources': sources,
        'firstYear': self.source_year(sources[0]), 'lastYear': self.source_year(sources[-1]),
      })
    out.sort(key=lambda e: (e['firstYear'], e['label']))
    return out

  def display(self, key, source=None, path=None):
    """How a name is shown: the combination at a node when the node is
    known; a species-group record's combinations joined when it is not;
    the name otherwise."""
    if (self.names.get(key) or {}).get('placeholder') and self._rank_of(key) not in _SPECIES_GROUP:
      return self.placeholder_words(key, source, path)
    if source is not None and path is not None:
      label = self.combination(source, path).get('label')
      if label and self.combination(source, path).get('record') == key:
        return label
    if self._rank_of(key) in _SPECIES_GROUP:
      combos = self.combinations(key)
      if combos:
        return ' / '.join(c['label'] for c in combos)
      if (self.names.get(key) or {}).get('placeholder'):
        return self.placeholder_words(key)
    if self._rank_of(key) == 'subgenus':
      genus = self._genus_of_subgenus(key)
      if genus:
        return f'{self.name(genus)} ({self.name(key)})'
    return self.name(key)

  _OPEN_WORDS = {'sp': 'sp.', 'spp': 'spp.', 'gen': 'gen.', 'indet': 'indet.',
                 'cf': 'cf.', 'aff': 'aff.', 'nov': 'nov.', 'n': 'n.', 'var': 'var.'}

  def placeholder_words(self, key, source=None, path=None):
    """A placeholder in the source's words: a bin by its rank ("Order
    uncertain", "Unnamed family"), an open-nomenclature record by its
    designation, the form printed at the node, or the words of its key
    ("Agelacrinites sp.")."""
    row = self.names.get(key) or {}
    kind = row.get('placeholder')
    rank = (row.get('rank') or '').lower()
    if kind == 'uncertain':
      return f'{rank.capitalize()} uncertain' if rank else 'Uncertain'
    if kind == 'unnamed':
      return f'Unnamed {rank}' if rank else 'Unnamed'
    if row.get('designation'):
      return row['designation']
    if source is not None and path is not None:
      for c in self.at_path.get(source, {}).get(path, ()):
        if c['kind'] == 'usage' and (c.get('printed') or {}).get('citedAs'):
          return c['printed']['citedAs']
    words = [self._OPEN_WORDS.get(w, w) for w in key_stem(key).split('-')]
    return ' '.join(words)[:1].upper() + ' '.join(words)[1:]

  def _open_tail(self, key, chain_keys):
    """The words of an open-nomenclature record's key after the names
    its chain already gives: "sp. a", "var. 1", "sp. indet."."""
    known = {fold(self.name(k)) for k in chain_keys if k}
    tokens = key_stem(key).split('-')
    while tokens and fold(tokens[0]) in known:
      tokens.pop(0)
    return ' '.join(self._OPEN_WORDS.get(w, w) for w in tokens)

  def original_combination(self, key):
    """The combination a species-group record was published in, when the
    corpus knows it: its placement in the authority's own paper, the
    original combination a synonymy entry gives, or the parent recorded
    with it. None otherwise."""
    row = self.names.get(key) or {}
    auth_source = (row.get('authority') or {}).get('source')
    if auth_source in self.sources:
      for c in self.by_subject.get(key, ()):
        if c['source'] == auth_source and c['kind'] == 'placement':
          combo = self.combination(auth_source, c['path'])
          if combo.get('genus'):
            return combo['label']
    for c in self.by_subject.get(key, ()):
      parents = c.get('parents') if c['kind'] == 'acceptance' else None
      if parents:
        parts = [self.name(parents[0])]
        if len(parents) > 1:
          parts.append(f'({self.name(parents[1])})')
        return ' '.join(parts + [self.name(key)])
    original = row.get('originalParent')
    if original:
      return f"{self.name(original) if original in self.names else original} {self.name(key)}"
    return None

  def authority_words(self, key):
    """The recorded authority in the corpus's citation form ("Holloway &
    Jell 1983", "Bather in Smith 1900"), or as displayed when the parts
    are not recorded."""
    authority = (self.names.get(key) or {}).get('authority') or {}
    if authority.get('authors'):
      words = short_citation({'authors': authority['authors'], 'year': None}).rsplit(' ', 2)[0]
      if authority.get('in'):
        words += ' in ' + short_citation({'authors': authority['in'], 'year': None}).rsplit(' ', 2)[0]
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
    if wanted & fold_forms(self.name(key)):
      return self.name(key)
    return asked.strip()

  def heading(self, key, asked=None):
    """A record as a block names it: the combination asked for (else
    the original one, else the latest) with the recorded author, in
    parentheses when the corpus knows the name is a recombination."""
    row = self.names.get(key) or {}
    if row.get('placeholder'):
      return self.placeholder_words(key)
    author = self.authority_words(key)
    if self._rank_of(key) in _SPECIES_GROUP:
      original = self.original_combination(key)
      if asked:
        shown = self._asked_label(key, asked)
      else:
        combos = self.combinations(key)
        latest = max(combos, key=lambda c: c['lastYear'])['label'] if combos else None
        shown = original or latest or self.name(key)
      recombined = bool(
        original and ' ' in shown
        and fold(shown.split()[0]) != fold(original.split()[0])
      )
      if not author:
        return shown
      return f'{shown} ({author})' if recombined else f'{shown} {author}'
    shown = self.display(key)
    return f'{shown} {author}' if author else shown

  @staticmethod
  def _asked(raw, key):
    """The query as typed when it was a printed name rather than a key."""
    if raw is None or raw == key or str(raw).lower() == key:
      return None
    return str(raw)

  def related_keys(self, taxon_key):
    """Records sharing the name at another rank or spelling, and the
    base or variants a record is linked to. An epithet is not a name on
    its own, so species-group records relate only through explicit
    links: two species called casteri in different genera are different
    names."""
    row = self.names.get(taxon_key)
    if row is None:
      return []
    keys = set()
    if not _species_group(row.get('rank')):
      for form in row['folded']:
        keys.update(k for k in self.by_folded.get(form, ())
                    if not _species_group(self.rank(k)))
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
    if (row['rank'] or '').lower() in _SPECIES_GROUP:
      entry['combinations'] = self.combinations(key)
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
        k for form in sub_forms for k in self.by_folded.get(form, ())
        if self._rank_of(k) == 'subgenus'
        and genus_forms & fold_forms(self.name(self._genus_of_subgenus(k) or ''))
      }
    wanted = fold_forms(' '.join(bare))
    epithet_keys = {
      k for form in fold_forms(bare[-1]) for k in self.by_folded.get(form, ())
      if self._rank_of(k) in _SPECIES_GROUP
    }
    keys = set()
    for k in epithet_keys:
      for combo in self.combinations(k):
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
          k for k in epithet_keys
          if genus_forms & fold_forms(self.names[k].get('originalParent') or '')
        }
    return keys

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
      where = self.display(parent) if parent else 'an unnamed group'
      flags = [f for f in ('provisional', 'questionable', 'quoted') if claim.get(f)]
      words = f'places it under {where}'
      if flags:
        words += ' (' + ', '.join(flags) + ')'
      if claim.get('tree') != 'taxonomy':
        words += f" in a {claim['tree']}"
      return words
    if kind == 'acceptance':
      target = self.display(claim['subject'], claim['source'], claim['path'])
      verb = 'accepts' if claim['stance'] == 'accepts' else 'rejects'
      cited = f" ({self.cite(claim['citesSource'])})" if claim.get('citesSource') else ''
      under = ''
      if claim.get('under'):
        under = self.display(claim['under'], claim['source'], claim['path'].rsplit('/', 2)[0])
      return f'{verb} {target}{cited} as {under}' if under else f'{verb} {target}{cited}'
    if kind == 'act':
      return self._act_words(claim)
    if kind == 'rejection':
      return f"declines a placement in {self.display(claim.get('declinedParent', ''))}"
    if kind == 'material':
      mk = claim['materialKind']
      if mk == 'specimen':
        ids = ', '.join(_flat_words(claim.get('ids')))
        repo = f" {claim['repository']}" if claim.get('repository') else ''
        return f"{claim.get('role', 'specimens')}:{repo} {ids}".strip()
      if mk == 'occurrence':
        occ = claim.get('occurrence') or {}
        parts = [', '.join(_flat_words(occ.get(k))) for k in ('stage', 'series', 'unit', 'location') if occ.get(k)]
        return 'occurrence: ' + '; '.join(p for p in parts if p) if parts else 'occurrence'
      return 'illustration: ' + _illustration_words(claim.get('illustration') or {})
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
      keys = self._resolve_combination(words)

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
    rank_word = (placement or {}).get('rank') or self.rank(key)
    node = {
      'key': key, 'name': self.names.get(key, {}).get('name'),
      'rank': self.rank(key), 'depth': depth, 'flags': flags,
      'claim': base['id'],
      'acts': [{'act': a['actKind'], 'words': self._act_words(a),
                'inferred': bool(a.get('inferred'))} for a in acts],
      'actClaims': [a['id'] for a in acts],
    }
    if rank_word:
      node['rankWord'] = rank_word[:1].upper() + rank_word[1:]
    if base.get('placeholder'):
      node['placeholder'] = base['placeholder']
    if flags.get('new'):
      # As the source prints it when recorded, else the rank's abbreviation.
      new_act = next((a for a in acts if a['actKind'] in ('new', 'placeholder')), None)
      printed_new = ((new_act or {}).get('printed') or {}).get('citedAs')
      if printed_new and node['name']:
        # The printed form carries the name; the mark is what follows it.
        printed_new = re.sub(re.escape(node['name']), '', printed_new, flags=re.I).strip() or None
      node['newMark'] = printed_new or blocks.new_mark(rank_word)
    label = self.display(key, source_key, path)
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
        # With an original combination the entry carries the bare epithet
        # (the parents supply the genus); without one, the cited name as the
        # combination the entry falls under; the heading's own name needs
        # neither.
        name=(self.name(acceptance['subject']) if acceptance.get('parents')
              else None if acceptance.get('ownName')
              else self.display(acceptance['subject'], source_key, candidate)),
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
    # The type species as its own line under the genus, as a Systematic
    # Paleontology section prints it: the act's printed form when
    # recorded, else the child's name in this source.
    for child_path in self._children_paths(source_key, path):
      for claim in self._node_claims(source_key, child_path):
        if claim['kind'] == 'act' and claim.get('actKind') == 'type':
          printed = (claim.get('printed') or {}).get('citedAs')
          node['typeSpecies'] = {
            'key': claim['subject'], 'claim': claim['id'],
            'label': printed or self.display(claim['subject'], source_key, child_path),
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
    return paths

  def contents(self, source, record, depth=None, synonymy=False, style='text', trees=TAXONOMY):
    """What a source places under a record, as the source prints it."""
    source, record = self._key(source), self._key(record)
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
      parents = ' / '.join(self.display(p['key']) for p in s['parents'])
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
    records = self._keys(records)
    sources = self._keys(sources) if sources else sources
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
        value = self.label(parent, claim['source'], parent_path) if parent else '(unnamed group)'
        if claim.get('parentPlaceholder'):
          value += ' [placeholder]'
        for flag in ('provisional', 'questionable'):
          if claim.get(flag):
            value += f' ({flag})'
        # A species recombined is a different name: one row per combination.
        row_label = self.display(key, claim['source'], claim['path'])
        cells[(key, row_label)][claim['source']].append({
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
      labels = [label for (k, label) in cells if k == key]
      for row_label in sorted(labels, key=lambda l: min(self.source_year(s) for s in cells[(key, l)])):
        rank = self.rank(key)
        shown = f'{row_label} ({rank})' if rank and rank.lower() not in _SPECIES_GROUP else row_label
        row_cells = [[{'value': shown, 'key': key}]]
        for s in columns_keys:
          row_cells.append(cells[(key, row_label)].get(s, []))
        rows.append({'cells': row_cells, 'record': key, 'combination': row_label})
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

  def _variant_words(self, key, base):
    """How a record reached by a variant edge relates to the record it
    is a variant of: a spelling at the same rank, or the name at another
    rank."""
    of = self.names[key].get('of') == base or self.names[base].get('of') == key
    same_rank = (self.rank(key) or '').lower() == (self.rank(base) or '').lower()
    if same_rank:
      return f"{'spelling' if of else 'same name'} variant of {self.display(base)}"
    return f"same name at another rank as {self.display(base)}"

  def descendants(self, records, include_synonyms=True, include_variants=True,
                  trees=None, years=None, style='text'):
    records = self._keys(records)
    trees = tuple(trees) if trees else TAXONOMY
    found = self.closure.descendants(list(records), include_synonyms, include_variants, trees, years)
    rows = []
    for key in sorted(found, key=lambda k: (_rank_order(self.rank(k)), self.name(k))):
      # One row per combination: a species recombined is a different name.
      by_label = {}
      for via in found[key]:
        claim = self.by_id.get(via.get('claim'))
        if claim is not None and 'parent' in via:
          label = self.display(key, claim['source'], claim['path'])
        elif claim is not None and 'synonymOf' in via:
          label = self.display(key, claim['source'], claim['path'])
        else:
          label = self.display(key)
        by_label.setdefault(label, []).append(via)
      for label, vias in sorted(by_label.items(), key=lambda kv: (min((v.get('year', 0) for v in kv[1]), default=0), kv[0])):
        how = []
        for via in vias:
          if 'parent' in via:
            claim = self.by_id[via['claim']]
            parent_path = claim['path'].rsplit('/children/', 1)[0]
            how.append({'value': f"{self.cite(via['source'])}: under {self.display(via['parent'], via['source'], parent_path)}", 'claim': via['claim'], 'source': via['source']})
          elif 'synonymOf' in via:
            # The senior name as that source combines it.
            claim = self.by_id[via['claim']]
            senior = self.display(via['synonymOf'], via['source'], claim['path'].rsplit('/', 2)[0])
            how.append({'value': f"{self.cite(via['source'])}: synonym of {senior}", 'claim': via['claim'], 'source': via['source']})
          else:
            how.append({'value': self._variant_words(key, via['variantOf'])})
        rows.append({'cells': [
          [{'value': label, 'key': key}],
          [{'value': self.rank(key) or ''}],
          how,
          [{'value': len({v['source'] for v in vias if 'source' in v})}],
        ], 'record': key, 'combination': label})
    parameters = {
      'records': list(records), 'includeSynonyms': include_synonyms,
      'includeVariants': include_variants, 'trees': list(trees), 'years': years,
    }
    block = blocks.table([
      {'name': 'record', 'kind': 'record'}, {'name': 'rank', 'kind': 'rank'},
      {'name': 'placed by', 'kind': 'text'}, {'name': 'sources', 'kind': 'count'},
    ], rows, parameters, title='Placed under ' + ', '.join(self.display(r) for r in records),
       extra={'found': found})
    return _with_style(block, style)

  def _authors(self, source_key):
    """The short citation without its year, for a line that shows the
    year in its own column."""
    cite = self.cite(source_key)
    year = str(self.source_year(source_key))
    return cite[:-len(year)].rstrip() if cite.endswith(year) else cite

  def _chain_entry(self, chain, nodes=None):
    source_key = chain['source']
    nodes = chain['nodes'] if nodes is None else nodes
    shown = []
    for n in nodes:
      shown.append({
        'key': n['key'], 'label': self.display(n['key'], source_key, n['path']),
        'rank': self.rank(n['key']),
        'kind': 'placeholder' if n['placeholder'] else 'placement',
        'alternatives': [self.display(a) for a in n['alternatives']],
        'provisional': n['provisional'], 'questionable': n['questionable'],
      })
    last = chain['nodes'][-1]
    claims = [n['claim'] for n in nodes if n.get('claim')]
    claims += [c['id'] for c in self._node_claims(source_key, last['path'])]
    return {
      'source': source_key, 'cite': self.cite(source_key),
      'authors': self._authors(source_key), 'year': chain['year'],
      'chain': shown, 'claims': sorted(set(claims)),
    }

  def _chain_decorations(self, entries, first_last=False):
    sources = sorted({e['source'] for e in entries}, key=lambda s: (self.source_year(s), s))
    if not sources:
      return {}
    sets = {self.closure.coauthor_set(s) for s in sources}
    years = f"{self.source_year(sources[0])}" if len(sources) == 1 else \
      f"{self.source_year(sources[0])}–{self.source_year(sources[-1])}"
    deco = {'measure': (
      f"{len(sources)} paper{'s' if len(sources) != 1 else ''}, "
      f"{len(sets)} co-author set{'s' if len(sets) != 1 else ''}, {years}"
    )}
    if first_last:
      deco['span'] = f'first {self.cite(sources[0])}, last {self.cite(sources[-1])}'
    return deco

  def ancestors(self, records, include_variants=True, trees=None, years=None, style='text'):
    """Every source's chain of taxa above the records, one line per
    source, top down."""
    raw = list(records)
    records = self._keys(records)
    trees = tuple(trees) if trees else TAXONOMY
    closure = self.closure
    entries = []
    for key in closure.expand(list(records), include_variants):
      for chain in closure.chains_of(key, trees, years):
        entries.append(self._chain_entry(chain))
    entries.sort(key=lambda e: (e['year'], e['source']))
    parameters = {
      'records': list(records), 'includeVariants': include_variants,
      'trees': list(trees), 'years': years,
    }
    title = 'Above ' + ', '.join(
      self.heading(k, self._asked(r, k)) for r, k in zip(raw, records))
    block = blocks.chains(entries, parameters, title=title,
                          decorations=self._chain_decorations(entries))
    return _with_style(block, style)

  def placed_under(self, record, parent, include_variants=True, trees=None, years=None,
                   style='text'):
    """The sources that place a record under a higher taxon, directly or
    through intermediates, in year order, each with the taxa between;
    first and last stated."""
    raw_record, raw_parent = record, parent
    record, parent = self._key(record), self._key(parent)
    trees = tuple(trees) if trees else TAXONOMY
    closure = self.closure
    parents = set(closure.expand([parent], include_variants))
    entries = []
    for key in closure.expand([record], include_variants):
      for chain in closure.chains_of(key, trees, years):
        index = next((i for i, n in enumerate(chain['nodes']) if n['key'] in parents), None)
        if index is None:
          continue
        entries.append(self._chain_entry(chain, chain['nodes'][index + 1:]))
    entries.sort(key=lambda e: (e['year'], e['source']))
    parameters = {
      'record': record, 'parent': parent, 'includeVariants': include_variants,
      'trees': list(trees), 'years': years,
    }
    title = (f"{self.heading(record, self._asked(raw_record, record))} under "
             f"{self.heading(parent, self._asked(raw_parent, parent))}")
    block = blocks.chains(entries, parameters, title=title,
                          decorations=self._chain_decorations(entries, first_last=True))
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
    inside = set(self.combination(source_key, path).get('keys') or ())
    current = claim
    while current is not None and current.get('parent') in inside:
      current = closure.parent_claim(source_key, current)
    if current is None or not current.get('parent'):
      return None
    parent_path = current['path'].rsplit('/children/', 1)[0]
    words = self.display(current['parent'], source_key, parent_path)
    if current.get('provisional'):
      words += ' (provisional)'
    if current.get('questionable'):
      words += ' (questionable)'
    return {'key': current['parent'], 'words': words, 'claim': current['id']}

  def _rank_lines(self, m):
    rows = m['ranks']
    if len(rows) < 2:
      return None
    latest = rows[0]
    parts = []
    for r in rows:
      if r is latest and r['lastSource'] == m['sources'][-1]:
        span = f"since {r['firstYear']}"
      elif r['firstYear'] == r['lastYear']:
        span = f"{r['firstYear']}"
      else:
        span = f"{r['firstYear']}–{r['lastYear']}"
      parts.append(f"{r['rank']} {span} ({r['papers']} paper{'s' if r['papers'] != 1 else ''})")
    return ', '.join(parts)

  def _position_lines(self, m):
    schemes = m['positions']
    if not schemes:
      return None
    parts = []
    for i, s in enumerate(schemes):
      parents = ' / '.join(self.display(p['key']) for p in s['parents'])
      if i == 0 and s['lastSource'] == m['sources'][-1]:
        span = f"since {s['firstYear']}"
      elif s['firstYear'] == s['lastYear']:
        span = f"{s['firstYear']}"
      else:
        span = f"{s['firstYear']}–{s['lastYear']}"
      sets = len(s['coauthorSets'])
      parts.append(f"in {parents} {span} ({s['papers']} paper{'s' if s['papers'] != 1 else ''}"
                   + (f", {sets} co-author sets" if sets != s['papers'] else '') + ')')
    return ', '.join(parts)

  def history(self, record, include_related=True, synonymy=False, trees=None, years=None,
              style='text'):
    """One line per source in year order: the name as the source uses
    it, its position above what the combination says, the acts in
    words, the page; with synonymy, each source's synonymy entries. The
    measurement is the heading."""
    raw = record
    record = self._key(record)
    trees = tuple(trees) if trees else TAXONOMY
    closure = self.closure
    keys = closure.expand([record], include_related)
    by_source = collections.defaultdict(list)
    for key in keys:
      for claim in self.by_subject.get(key, ()):
        if claim.get('tree') in trees and _in_years(self.source_year(claim['source']), years):
          by_source[claim['source']].append(claim)
    heading = self.heading(record, self._asked(raw, record))
    entries = []
    for source_key in sorted(by_source, key=lambda s: (self.source_year(s), s)):
      claims = by_source[source_key]
      uses = [c for c in claims if c['kind'] == 'usage' and c.get('axis') in ('children', 'root')]
      if uses:
        for use in uses:
          path = use['path']
          at = self._node_claims(source_key, path)
          words = self.display(use['subject'], source_key, path)
          position = self._position_above(source_key, path)
          if position:
            words += f", in {position['words']}"
          acts = [self._act_words(c) for c in at if c['kind'] == 'act']
          acts += [self._claim_words(c) for c in at if c['kind'] == 'rejection']
          if acts:
            words += '; ' + '; '.join(acts)
          entry = {
            'year': self.source_year(source_key), 'source': source_key,
            'cite': self.cite(source_key), 'authors': self._authors(source_key),
            'record': use['subject'], 'line': words, 'page': use.get('pages'),
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
          words = self.display(c['subject'], source_key, c['path'])
          if under:
            words += f", cited as a synonym of {self.display(under, source_key, under_path)}"
          entries.append({
            'year': self.source_year(source_key), 'source': source_key,
            'cite': self.cite(source_key), 'authors': self._authors(source_key),
            'record': c['subject'], 'line': words, 'page': c.get('citedPages'),
            'claims': [c['id']],
          })
    m = closure.measurement(record, include_related, trees, years)
    deco = {}
    if m['papers']:
      sets = len(m['coauthorSets'])
      years_span = (f"{self.source_year(m['sources'][0])}" if len(m['sources']) == 1 else
                    f"{self.source_year(m['sources'][0])}–{self.source_year(m['sources'][-1])}")
      deco['measure'] = (f"{m['papers']} paper{'s' if m['papers'] != 1 else ''}, "
                         f"{sets} co-author set{'s' if sets != 1 else ''}, {years_span}")
    ranks = self._rank_lines(m)
    if ranks:
      deco['ranks'] = ranks
    positions = self._position_lines(m)
    if positions:
      deco['positions'] = positions
    parameters = {'record': record, 'includeRelated': include_related, 'synonymy': synonymy,
                  'trees': list(trees), 'years': years}
    block = blocks.timeline(entries, parameters, title=heading, decorations=deco,
                            extra={'measurement': m})
    return _with_style(block, style)

  def synonymy(self, record, source=None, style='text'):
    """The synonymy a source gives under a record, as a list; every source
    with one when no source is named."""
    record, source = self._key(record), self._key(source)
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
          {'key': record, 'name': self.display(record, source_key, path),
           'rank': None if self._rank_of(record) in _SPECIES_GROUP else self.rank(record)},
          entries, {'record': record, 'source': source_key, 'path': path},
          extra={'source': source_key, 'cite': self.cite(source_key)},
        )
        out.append(_with_style(block, style))
    return out

  def statements(self, record, source=None, kind=None, act_kind=None, style='text'):
    """Every statement the corpus holds about one record, in publication
    order, each as a sentence."""
    raw = record
    record, source = self._key(record), self._key(source)
    claims = self.by_subject.get(record, [])
    if source is not None:
      claims = [c for c in claims if c['source'] == source]
    if kind is not None:
      claims = [c for c in claims if c['kind'] == kind]
    if act_kind is not None:
      claims = [c for c in claims if c.get('actKind') == act_kind]
    claims = sorted(claims, key=lambda c: (self.source_year(c['source']), c['source'], c['path']))
    heading = self.heading(record, self._asked(raw, record))
    entries = []
    for c in claims:
      page = c.get('pages')
      if page is None and c.get('citedPages') is not None:
        page = f"cited p. {c['citedPages']}"
      as_used = self.display(record, c['source'], c['path'])
      entries.append(blocks.list_entry(
        source=c['source'], cite=self.cite(c['source']), year=self.source_year(c['source']),
        claim=c['id'], page=page, kind=c['kind'], sentence=self._claim_words(c),
        # The name as this source uses it, when it is not the heading's.
        name=as_used if not heading.startswith(as_used) else None,
        authors=self._authors(c['source']),
        printed='editor' if c.get('inferred') else None,
      ))
    parameters = {'record': record, 'source': source, 'kind': kind, 'actKind': act_kind}
    block = blocks.listing({'key': record, 'name': heading}, entries, parameters, kind='statements')
    return _with_style(block, style)

  def source_coverage(self, source_key):
    """The raw view of one source: citation, whether entered, declared
    audit, derived counts."""
    source_key = self._key(source_key)
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
    source = self._key(source)
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
    record, source = self._key(record), self._key(source)
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
      {'key': record, 'name': self.display(record),
       'rank': None if self._rank_of(record) in _SPECIES_GROUP else self.rank(record)},
      entries, {'record': record, 'source': source}, kind='printedForms',
    )
    return _with_style(block, style)


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
  for item in (items if isinstance(items, list) else [items]):
    if isinstance(item, list) and len(item) == 2 and not isinstance(item[0], list):
      out.append(f'{item[0]}–{item[1]}')
    else:
      out.append(str(item))
  return ', '.join(out)


def _illustration_words(illustration):
  parts = []
  for field, word in (('plate', 'pl.'), ('plates', 'pl.'), ('figures', 'fig.'),
                      ('figure', 'fig.'), ('textFigures', 'text-fig.'), ('page', 'p.')):
    if illustration.get(field) is not None:
      parts.append(f'{word} {_range_words(illustration[field])}')
  for field, value in illustration.items():
    if field not in ('plate', 'plates', 'figures', 'figure', 'textFigures', 'page'):
      parts.append(f'{field} {_range_words(value)}')
  return ', '.join(parts) or 'unspecified'


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


def placed_under(record, parent, include_variants=True, trees=None, years=None, style='text'):
  return store().placed_under(record, parent, include_variants, trees, years, style)


def history(record, include_related=True, synonymy=False, trees=None, years=None, style='text'):
  return store().history(record, include_related, synonymy, trees, years, style)


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
    '("sourcesWithStatements", not a count of citations of anything). '
    'Unnamed records (a bin such as "order uncertain", a taxon in open '
    'nomenclature such as "Rhenopyrgus sp. indet. 1") are never found by '
    'name, since the words in their designation name other taxa; reach '
    'them by the key a listing shows. Record and source keys are '
    'lowercase; the other tools accept them in any case, or a printed '
    'name that resolves to one record (a name that can mean several is '
    'refused with the candidates). A combination is written as the '
    'literature writes it: "Rhenopyrgus grayae", "Pyrgocystis '
    '(Rhenopyrgus) coronaeformis", "Pyrgocystis (Rhenopyrgus)". An empty list '
    'means no source in the corpus carries the name; it does not mean the '
    'name does not exist. Optionally restrict by rank word.'
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
    'The chain of taxa above the given records in every source that '
    'places them: one line per source in year order, top down, with a '
    'placeholder such as "Order uncertain" in the source\'s words and an '
    'alternative placement the source offers beside the taxon it applies '
    'to. The heading counts the papers, co-author sets and years.'
  ),
  'placed_under': (
    'The sources that place a record under a higher taxon, directly or '
    'through intermediate taxa: one line per source in year order with '
    'the taxa between, the first and last source stated in the heading. '
    'Answers "who placed X under Y", "who first", "who followed".'
  ),
  'history': (
    'What each source does with a name, one line per source in year '
    'order: the name as that source uses it (a species as its '
    'combination there), its position above what the combination says, '
    'the acts (named as new, emended, nomen translatum, moved, a rejected '
    'placement), the page; the heading measures the papers, co-author '
    'sets and years, the ranks used and the positions given (which is the '
    'trajectory\'s present and history). The same name at other ranks is '
    'included unless include_related is false. With synonymy true each '
    'source\'s synonymy entries follow its line.'
  ),
  'synonymy': (
    'The synonymy a source prints under a record, as a dated list: each '
    'earlier usage accepted or rejected, with the original combination, '
    'the cited work and page, and the printed form. Every source with one '
    'when no source is named.'
  ),
  'statements': (
    'Every statement the corpus holds about one record, in publication '
    'order, each as a sentence with its source, year and page: the name '
    'cited, the placement given, an act (named as new, emended, moved, '
    'type species), a synonymy acceptance, a rejection, material, a '
    'diagnosis. Optionally one source, one kind of statement '
    '(usage, placement, acceptance, act, rejection, material, diagnosis, '
    'editorial) or one act kind (new, type, emended, nomTransl, moved, '
    'removed, corrected). A statement marked "editor" is the '
    'editor\'s inference, not the paper\'s words.'
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

_COMBINATION_NOTE = (
  ' Species-group names are shown as the combination the source uses '
  '(genus, subgenus in parentheses, epithet); a species recombined into '
  'another genus appears once per combination, since each is a name of its own.'
)
for _name in ('contents', 'placements', 'descendants', 'history', 'statements', 'synonymy'):
  TOOL_DESCRIPTIONS[_name] += _COMBINATION_NOTE

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
  _spec('placed_under', {
    'record': {'type': 'string', 'description': 'the record key or printed name'},
    'parent': {'type': 'string', 'description': 'the higher taxon, key or printed name'},
    'include_variants': {'type': 'boolean'}, 'trees': _TREES, 'years': _YEARS,
  }, ['record', 'parent']),
  _spec('history', {
    'record': {'type': 'string', 'description': 'the record key or printed name'},
    'include_related': {'type': 'boolean'}, 'synonymy': {'type': 'boolean'},
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
    'ancestors': ancestors, 'placed_under': placed_under, 'history': history,
    'synonymy': synonymy, 'statements': statements,
    'source_coverage': source_coverage, 'gap': gap, 'printed_forms': printed_forms,
  }
  arguments = dict(arguments)
  if 'years' in arguments and arguments['years'] is not None:
    arguments['years'] = tuple(arguments['years'])
  return functions[name](**arguments)
