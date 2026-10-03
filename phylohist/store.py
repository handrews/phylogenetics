"""The claim store: the committed claim table in memory, and the blocks
built from it.

`ClaimStore` reads `claims/` (the JSONL per source, `manifest.json`,
`names.json`, `repositories.json`) into indices, holds the closure over
them, and builds every block a tool returns: the listing a source prints, the matrix,
the descendants and ancestors, the timeline, the statements, the
history of one specimen, the gap sentence. Name and citation resolution
is `resolve.py`; the words the blocks carry are `words.py`; the tool
surface over the store is `tools.py`.
"""

import collections
import json
import pathlib
import re

from . import blocks
from .claims import specimen_components
from .closure import TAXONOMY, Closure, in_years
from .loader.material import in_run
from .names import fold
from .render import node_label, pages_text, render
from .resolve import Resolver
from .words import COVERAGE_WORDS, PLURAL_KINDS, Words, short_citation, years_span

CLAIMS_DIR = pathlib.Path(__file__).parent / '..' / 'claims'

AMBIGUOUS = 'ambiguous'

_WHITESPACE_RE = re.compile(r'\s+')
_DIGIT_RE = re.compile(r'\d')
_LEADING_SEPARATORS_RE = re.compile(r'(?:[\s.-]|no\.)+', re.IGNORECASE)


def _folded(text):
  """Case- and whitespace-insensitive comparison form."""
  return _WHITESPACE_RE.sub(' ', text.strip()).casefold()


def _typed_prefix(number):
  """The leading run before the first digit, stripped, with a trailing
  hyphen or period dropped ("PE-214", "PE 214" and "F. 5404" give "PE",
  "PE" and "F"); `None` if empty. A hyphen inside the number ("MCZ
  602-D1") is past the first digit and untouched."""
  match = _DIGIT_RE.search(number)
  prefix = (number[: match.start()] if match else number).strip()
  prefix = prefix.rstrip('-.').strip()
  return prefix or None


def _strip_form(number, form):
  """`number` without `form` at its start (matched case-insensitively,
  whitespace runs collapsed) and without the separators after it (spaces,
  hyphens, periods, "No."); `number` unchanged when that leaves nothing or
  `form` is not at its start."""
  tokens = form.split(' ')
  pattern = re.compile(r'\s+'.join(re.escape(token) for token in tokens), re.IGNORECASE)
  text = number.strip()
  match = pattern.match(text)
  if match is None:
    return number
  rest = text[match.end() :]
  separators = _LEADING_SEPARATORS_RE.match(rest)
  rest = rest[separators.end() :] if separators else rest
  return rest or number


def split_typed_number(number, repositories):
  """`(key, via, bare)` for a catalog number as a person types it: the
  registry key of its holder, how that was found, and the number without
  its printed prefix ("F. 5404" and "UQF5404" both give "5404").

  The prefix is the run before the first digit (`_typed_prefix`), compared
  case-insensitively with whitespace collapsed. The known forms are the
  `prefixes` and `otherNames` of every entry of `repositories` that is not a
  locality register; the longest one equal to the prefix or a token-boundary
  prefix of it wins, and only that form's text is removed to make `bare`.
  `via` is `'prefix'` or `'otherNames'` when one entry claims the form (a
  form listed both ways counts as `'prefix'`).

  Returns `(None, None, number)` when no form matches, and `(keys,
  AMBIGUOUS, number)`, `keys` a sorted tuple, when several entries claim
  the form. A caller tests `via == AMBIGUOUS` before using `key`.
  """
  prefix = _typed_prefix(number)
  if prefix is None:
    return None, None, number
  prefix = _folded(prefix)
  claims = {}
  for key, entry in repositories.items():
    if entry.get('subject') == 'localities':
      continue
    for via, values in (('otherNames', entry.get('otherNames')), ('prefix', entry.get('prefixes'))):
      for value in values or ():
        claims.setdefault(_folded(value), {})[key] = via
  forms = [
    form
    for form in claims
    if form == prefix or (prefix.startswith(form) and prefix[len(form)] == ' ')
  ]
  if not forms:
    return None, None, number
  form = max(forms, key=len)
  if len(claims[form]) > 1:
    return tuple(sorted(claims[form])), AMBIGUOUS, number
  ((key, via),) = claims[form].items()
  return key, via, _strip_form(number, form)


_NODE_FLAGS = ('new', 'provisional', 'questionable', 'quoted')

# The coverage kind a kind of statement is declared under.
_COVERAGE_OF_KIND = {
  'material': 'material',
  'occurrences': 'occurrences',
  'illustrations': 'illustrations',
  'specimens': 'material',
  'ranges': 'occurrences',
  'range': 'occurrences',
  'acceptance': 'synonymy',
  'usage': 'skeleton',
  'placement': 'skeleton',
  'rejection': 'skeleton',
  'act': 'skeleton',
  'editorial': 'skeleton',
}

# The `statements` kinds that select material claims, by `materialKind`.
_MATERIAL_KINDS = {
  'occurrences': {'occurrence', 'range'},
  'illustrations': {'illustration'},
  'specimens': {'specimen'},
}

# The `absence` claims (by `absenceOf`) a `statements` kind also selects; an
# explicit `absence` kind selects all of them.
_ABSENCE_OF_KIND = {
  'specimens': ('material',),
  'occurrences': ('occurrences',),
  'illustrations': ('illustrations',),
  'material': ('material', 'occurrences', 'illustrations'),
  'acceptance': ('synonymy',),
  'act': ('types',),
  'placement': ('skeleton',),
}

# The content kinds `statements` tabulates for a node, in order: the label,
# the `materialKind`s that count (None: synonymy entries), the `absenceOf`
# that says none is printed, and the coverage kind the source declares it under.
# `'type'` for the `materialKind`s stands for the node's type statement (its
# `type` node's act claim, else that of a child marked `isType`), `'children'`
# for the placements of the node's children.
_NODE_CONTENT = (
  ('members', 'children', 'skeleton', 'skeleton'),
  ('specimens', {'specimen'}, 'material', 'material'),
  ('occurrences', {'occurrence', 'range'}, 'occurrences', 'occurrences'),
  ('figures', {'illustration'}, 'illustrations', 'illustrations'),
  ('synonymy', None, 'synonymy', 'synonymy'),
  ('type', 'type', 'types', 'types'),
)
# Specimens and figures are cited for species: above that rank a node with
# neither says nothing, as in the derived coverage, and the row is left out.
_SPECIES_LEVEL_CONTENT = frozenset({'specimens', 'figures'})
# A type is stated for a genus or subgenus: at another rank a node with no
# type statement and no `types` absence leaves the row out.
_GENUS_LEVEL_CONTENT = frozenset({'type'})
_GENUS_LEVEL_RANKS = ('genus', 'subgenus')
# The members of a taxon above genus rank are its subtree; at genus or
# species level (a source often lists no species) and for a placeholder the
# row appears only with children entered or the `skeleton` absence.
_ABOVE_GENUS_CONTENT = frozenset({'members'})

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


def _owner_path(path):
  """The node an entry on a related axis hangs off: `…/synonyms/2` and
  `…/corrected` both hang off `…`."""
  head, _, last = path.rpartition('/')
  return head.rpartition('/')[0] if last.isdigit() else head


class ClaimStore:
  def __init__(self, directory=CLAIMS_DIR):
    directory = pathlib.Path(directory)
    with open(directory / 'manifest.json') as fd:
      self.manifest = json.load(fd)
    with open(directory / 'names.json') as fd:
      self.names = json.load(fd)
    with open(directory / 'repositories.json') as fd:
      self.repositories = json.load(fd)
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
    # The open forms compared with a taxon (`cf.`, `aff.`): for an open
    # record its links `{sign, taxon}`, for the taxon the open records
    # compared with it. A compared form is not the taxon, so only `history`
    # reads these.
    self.compared_links = collections.defaultdict(list)
    self.compared_with = collections.defaultdict(list)
    for claims in self.by_source.values():
      for claim in claims:
        if claim['kind'] == 'usage' and claim.get('compared'):
          link = claim['compared']
          if link not in self.compared_links[claim['subject']]:
            self.compared_links[claim['subject']].append(link)
          if claim['subject'] not in self.compared_with[link['taxon']]:
            self.compared_with[link['taxon']].append(claim['subject'])
    # The specimen claims by join key, and the printed runs ("GSC 25935–25961")
    # per holder, each as `(low, high, bare low, bare high, claim)`, so a
    # number inside a run is found beside the claims that cite it by number.
    self.by_join_key = collections.defaultdict(list)
    self.runs = collections.defaultdict(list)
    specimens = []
    for claims in self.by_source.values():
      for claim in claims:
        if claim['kind'] == 'material' and claim.get('materialKind') == 'specimen':
          self._index_specimen(claim)
          specimens.append(claim)
    # Each specimen claim's component (`specimen_components`): the claims
    # linked to it by a shared join key or by `sameAs`, in either direction.
    self.specimen_component = specimen_components(specimens)
    self.resolver = Resolver(self)
    self.words = Words(self)

  def _index_specimen(self, claim):
    """File a specimen claim under each of its join keys and, for each
    range pair it prints, under the holder of the pair's endpoints."""
    for key in claim.get('joinKeys') or ():
      self.by_join_key[key].append(claim)
    if not claim.get('rangeJoin'):
      return
    join_keys = claim.get('joinKeys') or ()
    # The claim's runs carry the numbers as printed, for the words, and
    # folded, to compare.
    position = 0
    for number in claim['numbers']:
      pair = number if isinstance(number, list) else [number]
      holders = join_keys[position : position + len(pair)]
      position += len(pair)
      if len(pair) != 2 or len(holders) != 2:
        continue
      holder = holders[0].split(':', 1)[0]
      pair = [str(end) for end in pair]
      self.runs[holder].append((*pair, *map(fold, pair), claim))

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
    if placement and placement.get('nonMonophyletic'):
      # The one flag that carries its value: `True`, or what the source says.
      flags['nonMonophyletic'] = placement['nonMonophyletic']
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
    if usage and usage.get('compared'):
      # A cf. or aff. form: the source originates the form, not a new taxon.
      node['compared'] = usage['compared']['sign']
    stated = placement or usage or {}
    if 'rankAsPrinted' in stated and stated['rankAsPrinted'] is None:
      # `rank: null`: the source places the taxon with no rank word.
      rank_word = None
      node['unranked'] = True
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
      subject = acceptance['subject']
      parents = acceptance.get('parents') or ()
      parent_names = [self.name(p) for p in parents]
      if parent_names and acceptance.get('quotedParent'):
        parent_names[0] = f'"{parent_names[0]}"'
      # An open form cited in its combination ("Gogia cf. longidactylus"):
      # the words of its key after the genus the parents give.
      row = self.names.get(subject) or {}
      open_form = row.get('placeholder') and not row.get('designation')
      entries.append(
        blocks.list_entry(
          source=cited,
          cite=cite,
          year=year if year != 9999 else None,
          claim=acceptance['id'],
          page=acceptance.get('citedPages'),
          stance=acceptance['stance'],
          parents=parent_names or None,
          printed=printed.get('citedAs'),
          record=subject if not acceptance.get('ownName') else None,
          nudum=any(c['kind'] == 'act' and c['actKind'] == 'nomNudum' for c in claims) or None,
          lapsusFor=self.name(acceptance['lapsusFor']) if acceptance.get('lapsusFor') else None,
          # With an original combination the entry carries the bare epithet
          # (the parents supply the genus); without one, the cited name as the
          # combination the entry falls under; the heading's own name needs
          # neither.
          name=(
            (self.words._open_tail(subject, parents) if open_form else self.name(subject))
            if parents
            else None
            if acceptance.get('ownName')
            else self.words.display(subject, source_key, candidate)
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
    # The type as its own line under the taxon, as a Systematic Paleontology
    # section prints it, named as this source combines it: the taxon's own
    # `type` node first, else a child marked `isType`. It never replaces
    # the child's line.
    for type_path in [f'{path}/type', *self._children_paths(source_key, path)]:
      for claim in self._node_claims(source_key, type_path):
        if claim['kind'] == 'act' and claim.get('actKind') == 'type':
          node['typeSpecies'] = {
            'key': claim['subject'],
            'claim': claim['id'],
            'word': self.words.type_noun(claim['subject']).capitalize(),
            'label': self.words.display(claim['subject'], source_key, type_path),
            'inferred': bool(claim.get('inferred')),
          }
          # How it was fixed, and whether the editor inferred the method.
          if method := self.words.fixation_words(claim, note=False):
            node['typeSpecies']['method'] = method
          if 'fixation' in (claim.get('inferredFields') or ()):
            node['typeSpecies']['methodInferred'] = True
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
        parent_path = closure.parent_path(claim)
        value = (
          self.words.display(parent, claim['source'], parent_path) if parent else '(unnamed group)'
        )
        if claim.get('provisional'):
          value = '? ' + value
        if claim.get('questionable'):
          value += ' ?'
        if claim.get('via') == 'type':
          value += ' ' + self.words.type_mark(key)
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
            parent_path = self.closure.parent_path(claim)
            under = self.words.display(via['parent'], via['source'], parent_path)
            if via.get('via') == 'type':
              under += ' ' + self.words.type_mark(key)
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
            senior = self.words.display(via['synonymOf'], via['source'], _owner_path(claim['path']))
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
          **({'nonMonophyletic': n['nonMonophyletic']} if n.get('nonMonophyletic') else {}),
          **(
            {'via': 'type', 'mark': self.words.type_mark(n['key'])}
            if n.get('via') == 'type'
            else {}
          ),
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

  def _unlisted_type(self, usage):
    """Whether a usage claim is of a `type` node whose record the node it
    types does not also list as a child."""
    return usage.get('axis') == 'type' and any(
      c['kind'] == 'act' and c.get('actKind') == 'type' and c.get('listed') is False
      for c in self._node_claims(usage['source'], usage['path'])
    )

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
    parent_path = closure.parent_path(current)
    words = self.words.display(current['parent'], source_key, parent_path)
    if current.get('provisional'):
      words += ' (provisional)'
    if current.get('questionable'):
      words += ' (questionable)'
    return {'key': current['parent'], 'words': words, 'claim': current['id']}

  @staticmethod
  def _compared_sign(compared, record, at):
    """The sign (`cf`, `aff`) a compared form's line carries: the node's own
    link when it is one of the links the history covers, else the record's
    first."""
    links = compared.get(record)
    if not links:
      return None
    own = next((c['compared'] for c in at if c['kind'] == 'usage' and c.get('compared')), None)
    return (own if own in links else links[0])['sign']

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
    # The open forms compared with the name or its related records are
    # listed under their own names, each line marked with its sign.
    compared = {}
    if include_related:
      for key in keys:
        for open_key in self.compared_with.get(key, ()):
          if open_key not in keys:
            found = [link for link in self.compared_links[open_key] if link['taxon'] == key]
            compared.setdefault(open_key, []).extend(found)
    by_source = collections.defaultdict(list)
    for key in [*keys, *compared]:
      for claim in self.by_subject.get(key, ()):
        if claim.get('tree') in trees and in_years(self.source_year(claim['source']), years):
          by_source[claim['source']].append(claim)
    heading = self.words.heading(record, self.words.asked(raw, record))
    entries = []
    for source_key in sorted(by_source, key=lambda s: (self.source_year(s), s)):
      claims = by_source[source_key]
      uses = [c for c in claims if c['kind'] == 'usage' and c.get('axis') in ('children', 'root')]
      primary = bool(uses)
      # A name the source cites only as a type, in the combination it cites
      # it in, is a use of its own; a type the taxon also lists is the
      # child's use.
      uses += [c for c in claims if c['kind'] == 'usage' and self._unlisted_type(c)]
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
          # A type the taxon also lists: the statement sits on the taxon's
          # `type` node and belongs on the line of the child it names.
          stated = [
            c
            for c in self._node_claims(source_key, f'{Closure.parent_path(use)}/type')
            if c['kind'] == 'act' and c.get('listed') and c['subject'] == use['subject']
          ]
          if use.get('axis') == 'children' and stated:
            acts += [self.words.act_words(c) for c in stated]
            at = [*at, *stated]
          acts += [self.words.claim_words(c) for c in at if c['kind'] == 'rejection']
          if acts:
            words += '; ' + '; '.join(acts)
          if any(c['kind'] == 'placement' and c.get('via') == 'type' for c in at):
            words += ' ' + self.words.type_mark(use['subject'])
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
          if sign := self._compared_sign(compared, use['subject'], at):
            entry['compared'] = sign
          if synonymy:
            found = self._synonymy_entries(source_key, path)
            if found:
              entry['synonymy'] = found
          entries.append(entry)
      if not primary:
        # A source that only cites the name, in a synonymy.
        for c in claims:
          if c['kind'] != 'acceptance':
            continue
          under = c.get('under')
          under_path = c['path'].rsplit('/', 2)[0]
          words = self.words.display(c['subject'], source_key, c['path'])
          if c.get('lapsusFor'):
            intended = self.words.display(c['lapsusFor'], source_key, under_path)
            words += f', cited in error for {intended}'
          elif under:
            words += f', cited as a synonym of {self.words.display(under, source_key, under_path)}'
          entry = {
            'year': self.source_year(source_key),
            'source': source_key,
            'cite': self.cite(source_key),
            'authors': self.words.authors(source_key),
            'record': c['subject'],
            'line': words,
            'page': c.get('citedPages'),
            'claims': [c['id']],
          }
          at = self._node_claims(source_key, c['path'])
          if sign := self._compared_sign(compared, c['subject'], at):
            entry['compared'] = sign
          entries.append(entry)
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
          # A source that was named and printed none, the auditor says so.
          absence = next(
            (
              c
              for c in self.at_path[source_key].get(path, ())
              if c['kind'] == 'absence' and c['absenceOf'] == 'synonymy'
            ),
            None,
          )
          if source and absence is not None:
            block = blocks.statement(
              'none',
              {
                'cite': self.cite(source_key),
                'source': source_key,
                'what': 'synonymy',
                'about': self.words.display(record, source_key, path),
                'page': absence.get('pages'),
              },
              {'record': record, 'source': source_key, 'path': path},
              claims=[absence['id']],
            )
            out.append(_with_style(block, style))
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

  def _node_page(self, source_key, path):
    """The page a node's own usage claim carries, if it has one."""
    for claim in self._node_claims(source_key, path):
      if claim['kind'] == 'usage' and claim.get('axis') in ('children', 'root'):
        return claim.get('pages')
    return None

  def _type_statements(self, source_key, path):
    """The ids of the node's type statement: the act claim of its `type`
    node, else that of a child marked `isType`."""
    at_path = self.at_path[source_key]
    own = [
      c['id']
      for c in at_path.get(f'{path}/type', ())
      if c['kind'] == 'act' and c['actKind'] == 'type'
    ]
    if own:
      return own
    prefix = f'{path}/children/'
    return [
      c['id']
      for candidate, claims in at_path.items()
      if candidate.startswith(prefix) and candidate[len(prefix) :].isdigit()
      for c in claims
      if c['kind'] == 'act' and c['actKind'] == 'type'
    ]

  def _children_placements(self, source_key, path):
    """The ids of the placement claims of the node's `children` nodes."""
    return [
      c['id']
      for child in self._children_paths(source_key, path)
      for c in self._node_claims(source_key, child)
      if c['kind'] == 'placement' and not c.get('via')
    ]

  def _node_content(self, source_key, record, path):
    """What a source gives at one node, per content kind: entered (with the
    count and the claims it rests on), none printed (the auditor's `absence`
    claim, or a source coverage that leaves nothing to enter), or not
    entered. Above species rank the specimens and figures rows appear only
    when the node carries something of the kind, and the type row appears
    for a genus or subgenus, and at any other rank only with a type
    statement or a `types` absence. The members row appears for a named
    node above genus rank, and at any other rank only with children
    entered or a `skeleton` absence."""
    at = self._node_claims(source_key, path)
    coverage = self.sources[source_key].get('coverage') or {}
    species_level = self._rank_of(record) in blocks.SPECIES_GROUP
    # A placeholder (an unnamed or open genus) has no type to state.
    genus_level = self._rank_of(record) in _GENUS_LEVEL_RANKS and not (
      self.names.get(record) or {}
    ).get('placeholder')
    # A placeholder (an unnamed or open taxon) has no members of its own.
    above_genus = self._rank_of(record) not in (
      *_GENUS_LEVEL_RANKS,
      *blocks.SPECIES_GROUP,
    ) and not (self.names.get(record) or {}).get('placeholder')
    rows = []
    for label, material_kinds, absence_of, coverage_kind in _NODE_CONTENT:
      if material_kinds is None:
        ids = [e['claim'] for e in self._synonymy_entries(source_key, path)]
        incomplete = False
      elif material_kinds == 'type':
        ids = self._type_statements(source_key, path)
        incomplete = False
      elif material_kinds == 'children':
        ids = self._children_placements(source_key, path)
        incomplete = False
      else:
        found = [
          c for c in at if c['kind'] == 'material' and c.get('materialKind') in material_kinds
        ]
        ids = [c['id'] for c in found]
        incomplete = label == 'specimens' and any(c.get('listComplete') is False for c in found)
      absence = [c['id'] for c in at if c['kind'] == 'absence' and c['absenceOf'] == absence_of]
      if ids:
        text = f'{len(ids)} entered' + (' (list incomplete)' if incomplete else '')
        row = {'state': 'entered', 'basis': 'claims', 'count': len(ids), 'claims': ids}
      elif absence:
        text = 'none printed'
        row = {'state': 'none', 'basis': 'null', 'count': None, 'claims': absence}
      elif label in _SPECIES_LEVEL_CONTENT and not species_level:
        continue
      elif label in _GENUS_LEVEL_CONTENT and not genus_level:
        continue
      elif label in _ABOVE_GENUS_CONTENT and not above_genus:
        continue
      elif coverage.get(coverage_kind) in ('na', 'all'):
        # The source prints none anywhere, or enters all it prints of the kind.
        text = 'none printed'
        row = {'state': 'none', 'basis': 'coverage', 'count': None, 'claims': []}
      else:
        text = 'not entered'
        row = {'state': 'notEntered', 'basis': 'coverage', 'count': None, 'claims': []}
      rows.append({'kind': label, 'text': text, **row})
    return rows

  def statements(self, record, source=None, kind=None, act_kind=None, style='text'):
    """Every statement the corpus holds about one record, in publication
    order, each as a sentence."""
    raw = record
    record, source = self.resolver.key(record), self.resolver.source_key(source)
    claims = self.by_subject.get(record, [])
    if source is not None:
      claims = [c for c in claims if c['source'] == source]
    if kind is not None:
      if kind in _MATERIAL_KINDS:
        # Material kinds a reader asks for by name; `occurrences` covers a
        # node's contexts and its distribution `ranges` alike.
        material_kinds = _MATERIAL_KINDS[kind]
        claims = [
          c for c in claims if c['kind'] == 'material' and c.get('materialKind') in material_kinds
        ]
      else:
        claims = [c for c in claims if c['kind'] == kind]
      # The auditor's "none printed" for the kinds asked for goes with them.
      claims += [
        c
        for c in self.by_subject.get(record, ())
        if c['kind'] == 'absence'
        and c['absenceOf'] in _ABSENCE_OF_KIND.get(kind, ())
        and (source is None or c['source'] == source)
      ]
    if act_kind is not None:
      # The `types` absence is the statement that no type is printed, so it
      # answers a question about the `type` act.
      claims = [
        c
        for c in claims
        if c.get('actKind') == act_kind
        or act_kind == 'type'
        and c['kind'] == 'absence'
        and c['absenceOf'] == 'types'
      ]
    claims = sorted(claims, key=lambda c: (self.source_year(c['source']), c['source'], c['path']))
    heading = self.words.heading(record, self.words.asked(raw, record))
    parameters = {'record': record, 'source': source, 'kind': kind, 'act_kind': act_kind}
    paths = self._record_paths(source, record) if source is not None and kind == 'absence' else []
    if paths:
      # What the source gives for the record per kind of content: the
      # absences are the auditor's, read beside the counts.
      cite = self.cite(source)
      content, rows = [], []
      for path in paths:
        page = self._node_page(source, path)
        node_rows = self._node_content(source, record, path)
        content.append(
          {
            'path': path,
            'page': page,
            'rows': [{k: r[k] for k in ('kind', 'state', 'basis', 'count')} for r in node_rows],
          }
        )
        group = None
        if len(paths) > 1:
          group = self.words.display(record, source, path)
          group += f' ({pages_text(page)})' if page is not None else ''
        for r in node_rows:
          state = {'value': r['text']}
          if r['claims']:
            state['claims'] = r['claims']
          row = {'cells': [[{'value': r['kind']}], [state]]}
          if group is not None:
            row['group'] = group
          rows.append(row)
      title = f'{heading} in {cite}'
      if len(paths) == 1 and content[0]['page'] is not None:
        title += f' ({pages_text(content[0]["page"])})'
      block = blocks.table(
        [{'name': 'kind', 'kind': 'text'}, {'name': 'state', 'kind': 'text'}],
        rows,
        parameters,
        title=title,
        extra={'source': source, 'cite': cite, 'content': content},
      )
      return _with_style(block, style)
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
        if any(c['source'] == source for c in self.by_subject.get(record, ())):
          # The record is in the source, only not under this kind.
          fields['aboutOther'] = True
      if gap['kind'] == 'gap' and kind is None and act_kind is None and fields.get('entered'):
        # No kind asked: the record's statements may lie in any kind of the
        # source not yet entered, so the gap names every such kind. The
        # effective map says which kinds are worth naming.
        effective = self.sources[source]['coverage']
        also = [
          {
            'kind': k,
            'what': COVERAGE_WORDS[k],
            'plural': k in PLURAL_KINDS,
            'declared': effective[k],
          }
          for k in COVERAGE_WORDS
          if k != coverage_kind and effective.get(k) in ('none', 'partly')
        ]
        if also:
          fields['also'] = also
          params['also_kinds'] = [a['kind'] for a in also]
      # The gap's own parameters name the coverage kind; the query's ride beside.
      gap = blocks.statement(gap['kind'], fields, params)
      return _with_style(gap, style)
    block = blocks.listing({'key': record, 'name': heading}, entries, parameters, kind='statements')
    return _with_style(block, style)

  def _unfound_specimen(self, number, repository, candidates=None):
    """The `absent` statement for a specimen no source mentions (or, with
    `candidates`, whose prefix several repositories claim)."""
    fields = {'name': f'the specimen {number}'}
    if candidates:
      fields['candidates'] = list(candidates)
    return blocks.statement('absent', fields, {'number': number, 'repository': repository})

  def _unfound_label(self, source_key, label):
    """The `absent` statement for a source with no specimen of that label."""
    fields = {'name': f'the specimen "{label}" of {self.cite(source_key)}'}
    return blocks.statement('absent', fields, {'source': source_key, 'label': label})

  def _same_specimen(self, found):
    """`{claim id: carrier}` for every claim in the component of a claim of
    `found`: the carrier is the claim whose `sameAs` link first reached it
    from the claims found directly, `None` for a claim found directly or
    reached through the join key of a one-number entry from one."""
    members = {}
    for claim in found:
      members.update((c['id'], c) for c in self.specimen_component[claim['id']])
    edges = collections.defaultdict(list)
    by_key = collections.defaultdict(list)
    for claim_id, claim in members.items():
      keys = claim.get('joinKeys') or ()
      if len(keys) == 1:
        by_key[keys[0]].append(claim_id)
      target = claim.get('sameAsClaim')
      if target in members:
        edges[claim_id].append((target, claim))
        edges[target].append((claim_id, claim))
    for ids in by_key.values():
      for one in ids:
        edges[one].extend((other, None) for other in ids if other != one)
    carriers = {claim['id']: None for claim in found}
    queue = collections.deque(carriers)
    while queue:
      claim_id = queue.popleft()
      for other, carrier in edges[claim_id]:
        if other not in carriers:
          carriers[other] = carrier or carriers[claim_id]
          queue.append(other)
    return carriers

  def specimen_history(self, number=None, repository=None, source=None, label=None, style='text'):
    """Every citation of one specimen, one line per claim in year order,
    asked for by catalog number or, for a specimen with no number, by
    source and label. The number is split by `split_typed_number` (or, with
    `repository`, as that registry entry's own number) and meets the
    claims' join keys; a number inside a printed run ("GSC 25935–25961") is
    found as well. A source and label meet the labels of that source's
    specimen claims (folded). Either way every claim in the component of a
    claim found is listed too (`specimen_components`: a `sameAs` link in
    either direction, through a chain, or the join key of a one-number
    entry), a line reached only through a link saying on whose authority.
    With a number, `source` and `label` are not read."""
    if number is None:
      if source is None or label is None:
        raise ValueError('give a catalog number, or a source and a label')
      return self._label_history(self.resolver.source_key(source), label, style)
    if repository is not None:
      key = repository
      if key not in self.repositories:
        return _with_style(self._unfound_specimen(number, repository), style)
      _, _, bare = split_typed_number(number, {key: self.repositories[key]})
    else:
      key, via, bare = split_typed_number(number, self.repositories)
      if via == AMBIGUOUS:
        block = self._unfound_specimen(number, repository, candidates=key)
        return _with_style(block, style)
      if via is None:
        return _with_style(self._unfound_specimen(number, repository), style)
    join_key = f'{key}:{fold(bare)}'
    found = {c['id']: c for c in self.by_join_key.get(join_key, ())}
    in_runs = {}
    for low, high, bare_low, bare_high, claim in self.runs.get(key, ()):
      if in_run(fold(bare), bare_low, bare_high):
        found.setdefault(claim['id'], claim)
        in_runs.setdefault(claim['id'], []).append([low, high])
    if not found:
      return _with_style(self._unfound_specimen(number, repository), style)
    entry = self.repositories[key]
    prefixes = entry.get('prefixes')
    printed = f'{prefixes[0] if prefixes else entry["name"]} {bare}'
    block = self._specimen_listing(
      list(found.values()),
      {'key': join_key, 'name': printed, 'rank': None},
      {'number': number, 'repository': repository},
      {'repository': key, 'holder': entry['name'], 'number': bare},
      number,
      join_key,
      in_runs,
    )
    return _with_style(block, style)

  def _label_history(self, source_key, label, style):
    wanted = fold(str(label))
    found = [
      c
      for c in self.by_source.get(source_key, ())
      if c['kind'] == 'material'
      and c.get('materialKind') == 'specimen'
      and c.get('label') is not None
      and fold(str(c['label'])) == wanted
    ]
    if not found:
      return _with_style(self._unfound_label(source_key, label), style)
    name = f'"{label}" of {self.cite(source_key)}'
    block = self._specimen_listing(
      found,
      {'key': f'{source_key}:{wanted}', 'name': name, 'rank': None},
      {'source': source_key, 'label': label},
      {},
      None,
      None,
      {},
    )
    return _with_style(block, style)

  def _specimen_listing(self, found, heading, parameters, extra, number, join_key, in_runs):
    """The list block of the claims `found` and the claims linked to them,
    in year order."""
    carriers = self._same_specimen(found)
    claims = sorted(
      (self.by_id[claim_id] for claim_id in carriers),
      key=lambda c: (self.source_year(c['source']), c['source'], c['path']),
    )
    entries = [
      blocks.list_entry(
        source=c['source'],
        cite=self.cite(c['source']),
        year=self.source_year(c['source']),
        claim=c['id'],
        page=c.get('pages'),
        kind='material',
        authors=self.words.authors(c['source']),
        sentence=self.words.specimen_history_words(
          c, number, join_key, in_runs.get(c['id']), carriers[c['id']]
        ),
      )
      for c in claims
    ]
    return blocks.listing(heading, entries, parameters, kind='specimen', extra=extra)

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
      # Declared coverage, with the three node-state kinds derived where the
      # file says so, and the raw derived labels.
      'coverage': row['coverage'],
      'derivedCoverage': row['derivedCoverage'],
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
      'declared': row['coverage'].get(kind),
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
