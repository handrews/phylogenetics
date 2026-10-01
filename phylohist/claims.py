"""Claims: one statement a source prints about one name, with provenance.

`docs/claims.md` is the specification. `extract` turns the trees built by
`main._load_trees` into claims deterministically: the same YAML always
yields the same claims in the same order, nothing is merged across sources,
and nothing is normalised beyond resolving keys. `manifest` derives the
per-source coverage counts and cross-checks them against the declared
`audit.coverage`.
"""

import collections

from .acts import RELATED_ACTS
from .loader.material import (
  AMBIGUOUS,
  context_key,
  entry_identifies,
  repository_of,
  repository_registry,
)
from .loader.research import Author, Publication, Source
from .loader.taxa import Taxon
from .names import fold, fold_forms, key_stem

KINDS = (
  'usage',
  'placement',
  'acceptance',
  'act',
  'rejection',
  'material',
  'secondhand',
  'editorial',
)

# The audit.coverage kind each claim is counted under, for the manifest and
# for the `audit.coverage` value carried on the claim.
COVERAGE_KINDS = (
  'skeleton',
  'newTaxa',
  'types',
  'synonymy',
  'material',
  'occurrences',
  'illustrations',
  'phylogeny',
)

_TAXON_FIELDS = ('taxon', 'openTaxon', 'cfTaxon', 'affTaxon')
_PRINTED_FIELDS = ('citedAs', 'auth', 'year', 'in')
# The node fields a correction can touch that bear on attribution.
_ATTRIBUTION_FIELDS = tuple(_PRINTED_FIELDS) + ('authority',)


def merge_patch(target, patch):
  """RFC 7396 JSON Merge Patch: an object patch merges member by member, a
  null member deletes, anything else replaces."""
  if not isinstance(patch, dict):
    return patch
  result = dict(target) if isinstance(target, dict) else {}
  for key, value in patch.items():
    if value is None:
      result.pop(key, None)
    else:
      result[key] = merge_patch(result.get(key), value)
  return result


def corrected_node(data):
  """The node as the editor reads it: its printed fields with the editorial
  `corrections` merged in and the editorial block itself left out. None
  when the block gives no corrections."""
  editorial = data.get('editorial') or {}
  if 'corrections' not in editorial:
    return None
  base = {k: v for k, v in data.items() if k != 'editorial'}
  return merge_patch(base, editorial['corrections'])


_PLACEMENT_FLAGS = (
  'provisional',
  'questionable',
  'quoted',
  'pars',
  'tentative',
  'outgroup',
  'stem',
)
# The synonymy entries: each is a name the source accepts (`synonyms`) or
# rejects (`non`) under the owner's name.
_SYNONYMY_AXES = ('synonyms', 'non')
_ACCEPTANCE_FLAGS = ('pars', 'tentative')

# The roles whose entry on a protologue node (`new: true`) is this source's
# own designation, so the claim derives `roleAct: designated` when the entry
# is silent.
_PROTOLOGUE_ROLES = frozenset({'holotype', 'paratype', 'syntype', 'cotype'})
# The locator fields an illustration claim's `illustration` keeps; `of` and
# `depicts` ride on the claim itself.
_ILLUSTRATION_LOCATOR_FIELDS = (
  'plate',
  'page',
  'figures',
  'textFigures',
  'non',
  'notes',
  'uncertain',
)
# `materialEntry` fields copied onto the claim exactly as written.
_MATERIAL_FIELDS = (
  'catalogNumbers',
  'catalogNumbersAsPrinted',
  'count',
  'label',
  'holder',
  'status',
  'formerIds',
  'fragmentOf',
  'parts',
  'examined',
  'listComplete',
  'preparation',
  'castOf',
  'collectedBy',
  'collectedDate',
)
# The three coverage kinds derived from raw node state rather than a
# reviewer's declaration, and the node fields each reads.
DERIVED_COVERAGE_FIELDS = {
  'material': ('material',),
  'occurrences': ('contexts', 'ranges'),
  'illustrations': ('illustrations',),
}


# The ranks below which specimens are cited; `material` coverage counts
# only nodes at these (phylohist/loader/taxa.py spells the same tuple).
SPECIES_LEVEL_RANKS = ('species', 'subspecies', 'variety')

_rank_hubs = None


def rank_variants(key):
  """The records of the same name at other ranks, in both directions of
  the `altRankOf` link: a spoke sees its hub and the other spokes, a hub
  sees its spokes."""
  global _rank_hubs
  if _rank_hubs is None:
    _rank_hubs = collections.defaultdict(set)
    for k, taxon in Taxon._taxa.items():
      hub = taxon._data.get('altRankOf')
      if hub:
        _rank_hubs[hub].add(k)
  hub = Taxon.get(key)._data.get('altRankOf') if Taxon.get(key) else None
  family = set(_rank_hubs.get(key, ()))
  if hub:
    family |= {hub} | _rank_hubs.get(hub, set())
  family.discard(key)
  return sorted(family)


def placeholder_kind(taxon):
  """C4: a bin (`uncertain`), an unnamed taxon (`unnamed`) or open."""
  if taxon is None or taxon.name is not None:
    return None
  key = taxon.key
  if '-uncertain' in key or '-indeterminate' in key:
    return 'uncertain'
  if '-unnamed' in key:
    return 'unnamed'
  return 'open'


def _effective_pages(node):
  """The node's own `pages`, else the nearest `children`-axis ancestor's."""
  if 'pages' in node.data:
    return node.data['pages'], False
  if node.axis == 'children' and node.parent is not None:
    pages, _ = _effective_pages(node.parent)
    return pages, pages is not None
  return None, False


def _related_key(node, axis):
  """The record named by the node under a single-node axis, if any."""
  related = node.related_node(axis)
  return related.taxon.key if related is not None and related.taxon is not None else None


def _nearest_named_ancestor(node):
  ancestor = node.parent
  while ancestor is not None and ancestor.taxon is None:
    ancestor = ancestor.parent
  return ancestor


def _by(value):
  """The work an act is followed from: `by`'s source and pages, when the
  field's value is an object naming one."""
  by = value.get('by') if isinstance(value, dict) else None
  if not by:
    return {}
  fields = {'by': by['source']}
  if 'pages' in by:
    fields['byPages'] = by['pages']
  return fields


def _coverage_kind(claim):
  kind = claim['kind']
  if kind in ('usage', 'rejection'):
    return 'skeleton'
  if kind == 'placement':
    return 'skeleton' if claim['tree'] == 'taxonomy' else 'phylogeny'
  if kind == 'acceptance':
    return 'synonymy'
  if kind == 'act':
    return {
      'new': 'newTaxa',
      'placeholder': 'newTaxa',
      'type': 'types',
    }.get(claim['actKind'])
  if kind == 'material':
    return {
      'specimen': 'material',
      'occurrence': 'occurrences',
      'illustration': 'illustrations',
      'range': 'occurrences',
    }[claim['materialKind']]
  return None


class _NodeClaims:
  """Builds the claims of one node; the shared fields are computed once."""

  def __init__(self, node, source_key, audit):
    self.node = node
    self.data = node.data
    self.source_key = source_key
    self.audit = audit
    self.path = f'{node.position}{node.pointer}'.rstrip('/')
    self.claims = []

    root = node.root
    self.tree = 'taxonomy' if node.tree_type == 'taxonomy' else node.tree_type
    self.tree_notes = root.tree_notes
    # A cited entry's `pages` and `illustrations` locate the cited usage in
    # the cited work, never the citing source's own page or figure.
    self.cited_entry = node.is_cited
    self.pages, self.pages_inherited = (None, False) if self.cited_entry else _effective_pages(node)
    self.subject = node.taxon.key if node.taxon is not None else None
    self.placeholder = placeholder_kind(node.taxon)

    # The owning node of a related entry (a synonym's accepted name, a
    # removed name's group), for the claims that need it.
    self.owner = node.parent if node.axis != 'children' else None
    self.owner_key = (
      self.owner.taxon.key if self.owner is not None and self.owner.taxon is not None else None
    )

  # -- the shared record ---------------------------------------------------

  def _base(self, kind):
    claim = {
      'kind': kind,
      'source': self.source_key,
      'path': self.path,
      'tree': self.tree,
    }
    if self.tree_notes is not None:
      claim['treeNotes'] = self.tree_notes
    if self.pages is not None:
      claim['pages'] = self.pages
      if self.pages_inherited:
        claim['pagesInherited'] = True
    claim['subject'] = self.subject
    if self.placeholder is not None:
      claim['placeholder'] = self.placeholder
    self._printed(claim)
    if 'editorial' in self.data:
      claim['editorial'] = self.data['editorial']
    if 'notes' in self.data:
      claim['notes'] = self.data['notes']
    return claim

  def _printed(self, claim):
    self._attribution(claim, self.data)
    # The editor's layer: every attribution field the corrections touch is
    # printed in error, and the corrected node gives the attribution the
    # editor reads instead.
    corrections = (self.data.get('editorial') or {}).get('corrections') or {}
    # A key the node prints; a correction that adds a field corrects nothing printed.
    in_error = [f for f in _ATTRIBUTION_FIELDS if f in corrections and f in self.data]
    if in_error:
      claim['printedErrors'] = in_error
    corrected = corrected_node(self.data)
    if in_error and corrected is not None:
      view = {}
      self._attribution(view, corrected)
      changed = {k: v for k, v in view.items() if claim.get(k) != v}
      if changed:
        claim['corrected'] = changed

  def _attribution(self, claim, data):
    printed = {f: data[f] for f in _PRINTED_FIELDS if f in data}
    authority = data.get('authority')
    if printed:
      claim['printed'] = printed
    if authority:
      claim['citesSource'] = authority.get('source')
      for field, name in (
        ('pages', 'citedPages'),
        ('illustrations', 'citedIllustrations'),
        ('attributedTo', 'citedAttributedTo'),
      ):
        if field in authority:
          claim[name] = authority[field]
    if self.cited_entry:
      for field, name in (
        ('pages', 'citedPages'),
        ('illustrations', 'citedIllustrations'),
      ):
        if field in data:
          claim[name] = data[field]
    if not printed and not authority:
      claim['printedAttribution'] = 'as-record'

  def _emit(self, claim, field=None):
    # A claim the editorial block says was inferred is the editor's, not
    # the paper's; it says so, and the manifest does not count it.
    editorial = self.data.get('editorial') or {}
    inferred = editorial.get('inferred')
    if inferred is True or (isinstance(inferred, list) and field is not None and field in inferred):
      claim['inferred'] = True
    # A claim from a field the corrections touch is printed in error; it
    # stays the paper's and says so, and the corrections ride on the claim.
    if field is not None and field in (editorial.get('corrections') or {}) and field in self.data:
      claim['erroneous'] = True
    coverage_kind = _coverage_kind(claim)
    audit = {'state': self.audit.get('state', 'unaudited')}
    if coverage_kind is not None:
      audit['coverageKind'] = coverage_kind
      effective = (self.audit.get('coverage') or {}).get(coverage_kind)
      if effective is not None:
        audit['coverage'] = effective
    claim['audit'] = audit
    self.claims.append(claim)

  # -- the kinds -----------------------------------------------------------

  def build(self):
    node, data = self.node, self.data
    named = self.subject is not None

    if named:
      self._usage()
    elif node.axis in _SYNONYMY_AXES and self.owner_key is not None:
      # An entry with no name of its own cites the owner's name.
      claim = self._base('usage')
      claim['subject'] = self.owner_key
      claim['form'] = node.axis
      claim['axis'] = node.axis
      claim['ownName'] = True
      self._emit(claim, node.axis)

    if node.bracket is not None:
      claim = self._base('usage')
      claim['subject'] = node.bracket.key
      claim['form'] = 'bracket'
      claim['spelling'] = data['bracket']
      claim['axis'] = node.axis
      claim.pop('placeholder', None)
      self._emit(claim, 'bracket')
      if named:
        claim = self._placement_base()
        claim['parent'] = node.bracket.key
        claim['via'] = 'bracket'
        self._emit(claim, 'bracket')

    if named and node.axis == 'children':
      claim = self._placement_base()
      ancestor = _nearest_named_ancestor(node)
      if ancestor is not None:
        claim['parent'] = ancestor.taxon.key
        # A bin is not a taxon (C4): a placement under one says so.
        if (kind := placeholder_kind(ancestor.taxon)) is not None:
          claim['parentPlaceholder'] = kind
        if ancestor is not node.parent:
          claim['parentPath'] = f'{node.parent.position}{node.parent.pointer}'.rstrip('/')
      else:
        claim['parent'] = None
        claim['parentPath'] = f'{node.parent.position}{node.parent.pointer}'.rstrip('/')
      claim['position'] = node.relpath[1]
      self._emit(claim, 'children')

    if node.axis in _SYNONYMY_AXES:
      claim = self._base('acceptance')
      if not named:
        claim['subject'] = self.owner_key
        claim['ownName'] = True
      claim['stance'] = 'accepts' if node.axis == 'synonyms' else 'rejects'
      claim['under'] = self.owner_key
      parents = [p.taxon.key for p in node.related_nodes('parents') if p.taxon is not None]
      if parents:
        claim['parents'] = parents
      # A lapsus listed in the synonymy: the record it was printed for.
      if (intended := _related_key(node, 'lapsusFor')) is not None:
        claim['lapsusFor'] = intended
      for flag in _ACCEPTANCE_FLAGS:
        if data.get(flag):
          claim[flag] = data[flag]
      self._emit(claim, node.axis)

    if named:
      self._acts()

    # A rejection has two printed shapes: the group's side (`removed`
    # under the group) and the taxon's side (`moved` on the taxon).
    if node.axis == 'removed' and named:
      claim = self._base('rejection')
      claim['declinedParent'] = self.owner_key
      self._emit(claim, 'removed')
    if named and (moved := _related_key(node, 'moved')) is not None:
      claim = self._base('rejection')
      claim['declinedParent'] = moved
      self._emit(claim, 'moved')

    if not self.cited_entry:
      self._material()

    if 'editorial' in data:
      claim = self._base('editorial')
      claim.update(
        {k: v for k, v in data['editorial'].items() if k in ('inferred', 'corrections', 'basis')}
      )
      self._emit(claim)

    self._number()
    self._link_illustrations()
    return self.claims

  def _usage(self):
    node, data = self.node, self.data
    field = next(f for f in _TAXON_FIELDS if f in data)
    claim = self._base('usage')
    claim['form'] = field
    claim['spelling'] = data[field]
    claim['axis'] = node.axis
    if field in ('cfTaxon', 'affTaxon'):
      claim['target'] = data[field]
    if 'sensu' in data:
      claim['sensu'] = data['sensu']
    self._emit(claim, field)

  def _placement_base(self):
    node, data = self.node, self.data
    claim = self._base('placement')
    claim['rank'] = node.taxon.rank
    if 'rank' in data:
      claim['rankAsPrinted'] = data['rank']
    for flag in _PLACEMENT_FLAGS:
      if data.get(flag):
        claim[flag] = data[flag]
    alt = [p.taxon.key for p in node.related_nodes('altPlacements') if p.taxon is not None]
    if alt:
      claim['altPlacements'] = alt
    return claim

  def _act(self, act_kind, field, **fields):
    claim = self._base('act')
    claim['actKind'] = act_kind
    claim.update(fields)
    self._emit(claim, field)

  def _acts(self):
    node, data = self.node, self.data
    if data.get('new'):
      self._act('placeholder' if self.placeholder else 'new', 'new')
    if data.get('type'):
      self._act('type', 'type')
    if emended := data.get('emended'):
      self._act('emended', 'emended', **_by(emended))
    if recombined := data.get('recombined'):
      self._act('combNov', 'recombined', **_by(recombined))
    if translated := data.get('translated'):
      fields = _by(translated)
      if (earlier := _related_key(node, 'translated')) is not None:
        fields['translatedFrom'] = earlier
      # The identity link between coordinate names is undirected: the
      # variants are listed whichever record carries the link.
      variants = rank_variants(node.taxon.key)
      if variants:
        fields['rankVariants'] = variants
      self._act('nomTransl', 'translated', **fields)
    if data.get('nudum'):
      self._act('nomNudum', 'nudum')
    for kind, (field, _) in RELATED_ACTS.items():
      if (related := _related_key(node, kind)) is not None:
        self._act(kind, kind, **{field: related})
    if node.axis == 'removed':
      self._act('removed', 'removed', removedFrom=self.owner_key)

  # -- material: contexts, material, illustrations, ranges, in that order,
  # which is what fixes the claim ids ---------------------------------------

  def _material(self):
    self._contexts()
    self._entries()
    self._illustrations()
    self._ranges()

  def _contexts(self):
    """One claim per context the node's material refers to, and per
    context the node defines; a file context once per node that refers
    to it."""
    data = self.data
    wanted = set(data.get('contexts') or ())
    for entry in data.get('material') or ():
      if entry.get('context') is not None:
        wanted.add(context_key(entry['context']))
    scopes = self.node.context_scopes
    for key, context in self.node.contexts.items():
      if key not in wanted:
        continue
      claim = self._base('material')
      claim['materialKind'] = 'occurrence'
      claim['occurrence'] = context
      claim['contextKey'] = key
      claim['contextScope'] = scopes[key]
      self._emit(claim, 'contexts')

  def _repository(self, entry):
    """`(key, via)` for an entry: its explicit `repository`, else what the
    first catalog number's prefix resolves to; `(None, None)` when that is
    absent, unmatched or ambiguous."""
    if 'repository' in entry:
      return entry['repository'], 'explicit'
    numbers = entry.get('catalogNumbers') or ()
    if not numbers:
      return None, None
    first = numbers[0][0] if isinstance(numbers[0], list) else numbers[0]
    key, via = repository_of(first, repository_registry(), self.node.file_repositories)
    return (None, None) if via in (None, AMBIGUOUS) else (key, via)

  def _entries(self):
    """One claim per `material` entry; `self._entry_claims` keeps each
    beside its entry for the illustrations' `of`."""
    data = self.data
    self._entry_claims = []
    for entry in data.get('material') or ():
      claim = self._base('material')
      claim['materialKind'] = 'specimen'
      if 'role' in entry:
        claim['role'] = entry['role']
      for field in _MATERIAL_FIELDS:
        if field in entry:
          claim[field] = entry[field]
      if 'notes' in entry:
        claim['materialNotes'] = entry['notes']
      if 'context' in entry:
        ref = entry['context']
        claim['contextKey'] = context_key(ref)
        if isinstance(ref, dict) and ref.get('tentative'):
          claim['contextTentative'] = True
      # The claim is about the entry, so the entry's editorial block replaces
      # the node's; the claim's own `inferred` stays as `_emit` sets it.
      if 'editorial' in entry:
        claim['editorial'] = entry['editorial']
        inferred = entry['editorial'].get('inferred')
        if isinstance(inferred, list):
          claim['inferredFields'] = inferred
      numbers = entry.get('catalogNumbers') or ()
      claim['ids'] = list(numbers)
      repository, via = self._repository(entry)
      claim['repository'] = repository
      if via is not None:
        claim['repositoryVia'] = via
      role_act = entry.get('roleAct')
      if role_act is None and data.get('new') and entry.get('role') in _PROTOLOGUE_ROLES:
        role_act = 'designated'
      if role_act is not None:
        claim['roleAct'] = role_act
      if repository is not None and numbers:
        claim['joinKeys'] = [
          f'{repository}:{fold(n)}'
          for number in numbers
          for n in (number if isinstance(number, list) else [number])
        ]
      if any(isinstance(number, list) for number in numbers):
        claim['rangeJoin'] = True
      self._emit(claim, 'material')
      self._entry_claims.append((entry, claim))

  def _illustrations(self):
    """One claim per `illustrations` entry on a primary node (this
    source's figures); `self._illustration_links` keeps each beside the
    material claims its `of` names, for the link made once ids exist."""
    self._illustration_links = []
    for figure in self.data.get('illustrations') or ():
      claim = self._base('material')
      claim['materialKind'] = 'illustration'
      claim['illustration'] = {k: v for k, v in figure.items() if k in _ILLUSTRATION_LOCATOR_FIELDS}
      for field in ('of', 'depicts'):
        if field in figure:
          claim[field] = figure[field]
      of = figure.get('of')
      named = []
      for value in of if isinstance(of, list) else [of] if of is not None else ():
        for entry, specimen in self._entry_claims:
          if entry_identifies(entry, value) and specimen not in named:
            named.append(specimen)
      for specimen in named:
        specimen.setdefault('specimenIllustrations', []).append(claim['illustration'])
      self._illustration_links.append((claim, named))
      self._emit(claim, 'illustrations')

  def _ranges(self):
    for value in self.data.get('ranges') or ():
      claim = self._base('material')
      claim['materialKind'] = 'range'
      claim['range'] = value
      self._emit(claim, 'ranges')

  def _link_illustrations(self):
    """`ofClaim` on each illustration claim and `illustrationClaims` on
    each specimen claim it depicts, once every claim has its id."""
    for claim, named in getattr(self, '_illustration_links', ()):
      if named:
        claim['ofClaim'] = [specimen['id'] for specimen in named]
      for specimen in named:
        specimen.setdefault('illustrationClaims', []).append(claim['id'])

  def _number(self):
    # `<source>:<path>:<kind>[:<n>]`; n appears only where the node emits
    # several claims of one kind, so ids stay short and stable.
    per_kind = collections.Counter(c['kind'] for c in self.claims)
    seen = collections.Counter()
    for claim in self.claims:
      kind = claim['kind']
      claim_id = f'{self.source_key}:{self.path}:{kind}'
      if per_kind[kind] > 1:
        claim_id += f':{seen[kind]}'
        seen[kind] += 1
      claim['id'] = claim_id


def _node_writes(data, fields):
  """`(present, null)`: whether the node carries any of `fields`, and
  whether any of those it carries is an explicit null."""
  present = [field for field in fields if field in data]
  return bool(present), any(data[field] is None for field in present)


def derived_material_coverage(roots):
  """Per source, `{kind: value}` for `material`, `occurrences` and
  `illustrations`, from raw node state over primary, non-cited, named
  nodes: `na` when the file lists the kind's fields as `unused`; `None`
  when no node writes a null for them (a value records what the source
  prints, not that the file was audited for it); else `all` when no node
  lacks the fields (`partly` if a material entry has `listComplete:
  false`) and `partly` when some node does. For `material` only the
  species-level nodes are counted, since specimens are cited for species
  and a genus or higher node without `material` is not an uncaptured
  field."""
  out = {}
  for source_key, trees in roots.items():
    unused = set(trees[0].file_unused) if trees else set()
    nodes = [
      node
      for root in trees
      for node in root.walk()
      if node.is_primary and not node.is_cited and node.taxon is not None
    ]
    values = {}
    for kind, fields in DERIVED_COVERAGE_FIELDS.items():
      if set(fields) <= unused:
        values[kind] = 'na'
        continue
      counted = nodes
      if kind == 'material':
        counted = [node for node in nodes if node.taxon.rank in SPECIES_LEVEL_RANKS]
      states = [_node_writes(node.data, fields) for node in counted]
      if not any(null for _, null in states):
        values[kind] = None
      elif not all(present for present, _ in states):
        values[kind] = 'partly'
      elif kind == 'material' and any(
        entry.get('listComplete') is False
        for node in nodes
        for entry in node.data.get('material') or ()
      ):
        values[kind] = 'partly'
      else:
        values[kind] = 'all'
    out[source_key] = values
  return out


def _effective_coverage(declared, derived_row):
  """The declared `audit.coverage`, except that the three kinds derived
  from node state take the derived value when there is one."""
  declared = declared or {}
  derived_row = derived_row or {}
  coverage = {}
  for kind in COVERAGE_KINDS:
    value = derived_row.get(kind) if kind in DERIVED_COVERAGE_FIELDS else None
    coverage[kind] = value if value is not None else declared.get(kind)
  return coverage


def extract(roots, sources=None):
  """Claims per source, in walk order.

  ``roots`` is `main._load_trees`'s result; ``sources`` optionally
  restricts the output to those keys. Each claim's `audit.coverage` is
  the effective value (`_effective_coverage`).
  """
  out = {}
  derived = derived_material_coverage(roots)
  for source_key, trees in roots.items():
    if sources is not None and source_key not in sources:
      continue
    source = Source.get(source_key)
    audit = dict(source.audit) if source is not None else {'state': 'unaudited'}
    audit['coverage'] = _effective_coverage(audit.get('coverage'), derived.get(source_key))
    claims = []
    for root in trees:
      for node in root.walk():
        claims.extend(_NodeClaims(node, source_key, audit).build())
    out[source_key] = claims
  return out


def citation(source):
  """How a reader cites the source: names, year, title, where."""
  data = source._data
  entry = {
    'authors': [a.surname for a in source.authors],
    'year': None if source.in_preparation else source.year,
    'title': data.get('title'),
  }
  for field in ('journal', 'book'):
    if field in data:
      publication = Publication.get(data[field])
      entry['in'] = publication.name if publication is not None else data[field]
  for field in ('series', 'volume', 'number', 'pages', 'plates'):
    if field in data:
      entry[field] = data[field]
  return entry


def names_index():
  """One row per taxon record: what a resolver needs to find it and say
  what it is, with the folded lookup forms precomputed."""
  rows = {}
  for key, taxon in Taxon._taxa.items():
    data = taxon._data
    kind = 'primary'
    for field in ('altSpellingOf', 'altRankOf', 'vulgarSpellingOf'):
      if field in data:
        kind = field
    if taxon.name is None:
      kind = 'placeholder'
    row = {'name': taxon.name, 'rank': taxon.rank, 'kind': kind}
    if data.get('designation'):
      row['designation'] = data['designation']
    if taxon.derivative_of is not None:
      row['of'] = taxon.derivative_of.key
    authority = taxon.authority
    try:
      display = str(authority)
    except TypeError:
      display = None
    if display or authority.source is not None:
      row['authority'] = {'display': display or None}
      # The parts a heading is built from, in the corpus's citation form;
      # a record that names no author has none.
      if authority.authors is not None:
        row['authority']['authors'] = [a.surname for a in authority.authors]
        if authority.attribution_differs_from_source:
          row['authority']['in'] = [a.surname for a in authority.source_authors]
        if authority.year:
          row['authority']['year'] = authority.year
      if authority.source is not None:
        row['authority']['source'] = authority.source.key
    for field in ('homonym', 'originalParent', 'lang', 'status'):
      if field in data:
        row[field] = data[field]
    placeholder = placeholder_kind(taxon)
    if placeholder is not None:
      row['placeholder'] = placeholder
    # An unnamed record (a bin, an open-nomenclature taxon) has no name to
    # look up: the words in its key or designation name other taxa.
    forms = set()
    if taxon.name is not None:
      forms = fold_forms(key_stem(key)) | fold_forms(taxon.name)
    row['folded'] = sorted(forms)
    rows[key] = row
  return dict(sorted(rows.items()))


def _source_order(source_key):
  source = Source.get(source_key)
  year = source.year if source is not None and not source.in_preparation else 9999
  return (year, source_key)


def manifest(claims_by_source, roots):
  """Derived coverage per source and per taxon, cross-checked with the
  declared audit block (`docs/claims.md`, "Derived coverage").

  ``roots`` is what `extract` took; the node-state coverage reads it whole,
  so a ``claims_by_source`` restricted to some sources does not skew it.
  """
  sources = {}
  taxa = collections.defaultdict(set)
  derived_coverage = derived_material_coverage(roots)

  for source_key in Source._sources:
    source = Source.get(source_key)
    entry = {
      'citation': citation(source),
      'tree': source_key in claims_by_source,
      'audit': source.audit,
      'claims': {},
      'acts': {},
      'material': {},
      'inconsistencies': [],
    }
    claims = claims_by_source.get(source_key, [])
    by_kind = collections.Counter(c['kind'] for c in claims)
    entry['claims'] = dict(sorted(by_kind.items()))
    entry['acts'] = dict(
      sorted(collections.Counter(c['actKind'] for c in claims if c['kind'] == 'act').items())
    )
    entry['material'] = dict(
      sorted(
        collections.Counter(c['materialKind'] for c in claims if c['kind'] == 'material').items()
      )
    )

    # Editor-inferred claims are not the paper's, so they do not count
    # towards what the paper's coverage was declared to be.
    claim_counts = collections.Counter(
      c['audit']['coverageKind']
      for c in claims
      if 'coverageKind' in c['audit'] and not c.get('inferred')
    )
    declared = source.audit.get('coverage') or {}
    derived_row = derived_coverage.get(source_key) or {}
    for kind in COVERAGE_KINDS:
      value = declared.get(kind)
      if kind in DERIVED_COVERAGE_FIELDS:
        # Checked only when a declared and a derived value both exist.
        derived_value = derived_row.get(kind)
        if value is not None and derived_value is not None and value != derived_value:
          entry['inconsistencies'].append(f'{kind}: declared {value}, derived {derived_value}')
        continue
      count = claim_counts.get(kind, 0)
      if value in ('all', 'partly') and count == 0:
        entry['inconsistencies'].append(
          f'{kind}: declared {value}, no claims derived',
        )
      elif value in ('none', 'na') and count > 0:
        entry['inconsistencies'].append(
          f'{kind}: declared {value}, {count} claims derived',
        )
    entry['derived'] = {k: claim_counts[k] for k in COVERAGE_KINDS if claim_counts[k]}
    entry['coverage'] = _effective_coverage(declared, derived_row)
    entry['derivedCoverage'] = derived_row
    sources[source_key] = entry

    for claim in claims:
      if claim['subject'] is not None:
        taxa[claim['subject']].add(source_key)

  return {
    # Author keys to surnames, so a printed attribution renders by field.
    'authors': {key: author.surname for key, author in sorted(Author._authors.items())},
    'sources': dict(sorted(sources.items())),
    'taxa': {key: sorted(keys, key=_source_order) for key, keys in sorted(taxa.items())},
  }
