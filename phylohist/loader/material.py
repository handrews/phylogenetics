"""Material integrity checks: contexts, material entries, casts, illustrations,
nulls, the repository registry and a tree file's `prefixes` map.

Pure functions over a raw node dict and the file-level maps, so
`scripts/check_draft.py` can run the same checks on an unloaded draft; the
loader (`load.py`) runs them over the corpus's own documents. Each check
returns a list of ``(level, message)`` pairs, ``level`` being ``'error'``
or ``'warning'``; the caller adds the source key and, for a per-node
check, the node path. `context_key`, `flat_numbers`, `entries_named` and
`same_as_matches` are exported for the claims extractor
(`phylohist.claims`), and `in_run` for the store (`phylohist.store`,
`specimen_history`);
`set_repository_registry`/`repository_registry`
hold the loaded `data/repositories.yaml`, set once by `load.py`, so the
extractor can reach it the way it reaches `Source`.
"""

import re

from ..names import fold
from .taxa import (
  BRACKET_ERRORS,
  SECTION_ERRORS,
  SECTION_NOT_CHILD,
  SECTION_NOT_TAXONOMY,
  Tree,
  bracket_spans,
  section_spans,
)

_WHITESPACE_RE = re.compile(r'\s+')


_registry = {}


def set_repository_registry(data):
  """Register `data/repositories.yaml`'s content once (`loader.load.load`),
  so the claim extractor can reach it the way it reaches `Source`."""
  global _registry
  _registry = dict(data or {})


def repository_registry():
  """The registered repositories, keyed by registry key."""
  return _registry


def _fold(text):
  """Case- and whitespace-insensitive comparison form."""
  return _WHITESPACE_RE.sub(' ', text.strip()).casefold()


def _locality_objects(contexts):
  """Every `localityNumbers` value on a `{key: context}` map."""
  for context in (contexts or {}).values():
    yield from (context or {}).get('localityNumbers') or ()


def flat_numbers(entry):
  """Every number of an entry, a range pair's two ends included."""
  for number in entry.get('numbers') or ():
    yield from number if isinstance(number, list) else [number]


def registry_links(repositories):
  """Every `within` names an existing key and following `within` never
  cycles; an error otherwise, a cycle reported once."""
  messages = []
  reported = set()
  for start, entry in repositories.items():
    within = entry.get('within')
    if within is not None and within not in repositories:
      messages.append(('error', f'repository "{start}" is within "{within}", which is not a key'))
    chain = [start]
    while (within := repositories.get(chain[-1], {}).get('within')) in repositories:
      if within in chain:
        cycle = chain[chain.index(within) :]
        if frozenset(cycle) not in reported:
          reported.add(frozenset(cycle))
          messages.append(('error', f'`within` cycles: {" -> ".join([*cycle, within])}'))
        break
      chain.append(within)
  return messages


def context_key(ref):
  """The key a `contextRef` names, whichever of its two shapes it is."""
  return ref if isinstance(ref, str) else ref.get('key')


def context_refs(node, node_contexts, file_contexts):
  """Every `material[*].context` resolves in `node_contexts` first, then
  `file_contexts`; missing from both is an error, and a node key that
  shadows a same-named file key is a warning."""
  messages = []
  for entry in node.get('material') or ():
    ref = entry.get('context')
    if ref is None:
      continue
    key = context_key(ref)
    if key in node_contexts:
      if key in file_contexts:
        messages.append(('warning', f'context "{key}" on the node shadows a file-level context'))
    elif key not in file_contexts:
      messages.append(('error', f'context "{key}" is not defined on the node or the file'))
  return messages


def unreferenced_file_contexts(document):
  """A file-level context referenced by no material entry anywhere in the
  document is a warning."""
  file_contexts = document.get('contexts') or {}
  if not file_contexts:
    return []
  referenced = set()
  for _, node, _ in walk_document(document):
    for entry in node.get('material') or ():
      ref = entry.get('context')
      if ref is not None:
        referenced.add(context_key(ref))
  return [
    ('warning', f'context "{key}" is defined but referenced by no material entry')
    for key in sorted(set(file_contexts) - referenced)
  ]


_NUMBER_RE = re.compile(r'^(.*?)(\d+)([A-Za-z]?)$')


def _split_number(text):
  """`(stem, digits, suffix)` of a catalog number, the stem's whitespace
  runs collapsed, or `None` when it does not end in digits and at most one
  letter."""
  match = _NUMBER_RE.match(text) if isinstance(text, str) else None
  if match is None:
    return None
  stem, digits, suffix = match.groups()
  return _WHITESPACE_RE.sub(' ', stem), digits, suffix


def in_run(value, low, high):
  """Whether `value` lies inside the run `[low, high]`: an integer run
  (same stem, no suffix, `value` of that stem, a letter suffix allowed on
  it) or a letter run (same stem and digits, a one-letter suffix on each,
  the value's letter between the endpoints', case-sensitively)."""
  parts = [_split_number(text) for text in (value, low, high)]
  if None in parts:
    return False
  (v_stem, v_digits, v_suffix), (l_stem, l_digits, l_suffix), (h_stem, h_digits, h_suffix) = parts
  if not v_stem == l_stem == h_stem:
    return False
  if not l_suffix and not h_suffix:
    return int(l_digits) <= int(v_digits) <= int(h_digits)
  if l_suffix and h_suffix and v_suffix and v_digits == l_digits == h_digits:
    return l_suffix <= v_suffix <= h_suffix
  return False


def entry_identifies(entry, value, exact=False):
  """Whether `value` names `entry`: the folded text of `value` (a string or
  an integer) equals its folded `label` or one of its `numbers` (a range
  pair's endpoints count separately); unless `exact`, a value lying in the
  run of one of its range pairs names it too."""
  folded = fold(str(value))
  label = entry.get('label')
  if label is not None and fold(str(label)) == folded:
    return True
  for number in entry.get('numbers') or ():
    elements = number if isinstance(number, list) else [number]
    if any(fold(str(element)) == folded for element in elements):
      return True
    if not exact and len(elements) == 2 and in_run(str(value), *map(str, elements)):
      return True
  return False


def entries_named(entries, value):
  """The entries `value` names: those it names exactly, else those whose
  range-pair run contains it. Callers read "names exactly one entry" from
  the length."""
  exact = [entry for entry in entries if entry_identifies(entry, value, exact=True)]
  return exact or [entry for entry in entries if entry_identifies(entry, value)]


def same_as_matches(entries, link):
  """The entries a `sameAs` link names among `entries` (raw material
  entries or specimen claims, which carry the same `label`, `prefix` and
  `numbers`): those whose folded `label` equals the link's, or, by the
  link's `number`, those it names exactly before those whose range-pair run
  holds it (the rule of `entries_named`, over the numbers alone); with a
  `prefix` on the link, only entries of that prefix. Callers read "names
  exactly one" from the length."""
  if 'label' in link:
    wanted = fold(str(link['label']))
    return [
      entry
      for entry in entries
      if entry.get('label') is not None and fold(str(entry['label'])) == wanted
    ]
  candidates = [
    entry for entry in entries if 'prefix' not in link or entry.get('prefix') == link['prefix']
  ]
  numbered = [({'numbers': entry.get('numbers')}, entry) for entry in candidates]
  value = link.get('number')
  exact = [entry for view, entry in numbered if entry_identifies(view, value, exact=True)]
  return exact or [entry for view, entry in numbered if entry_identifies(view, value)]


def same_as_links(documents, source_year):
  """Every `sameAs` link on a material entry anywhere in `documents`
  (source key to raw tree document) names a source that has a tree, not
  the entry's own, published no later than the entry's (`source_year` maps
  a source key to its year, or `None` when unknown, which is not checked),
  and exactly one material entry in that tree file (`same_as_matches`).
  Each message names the source and the node's path."""
  messages = []
  targets = {}

  def target_entries(key):
    if key not in targets:
      targets[key] = [
        entry
        for _, node, _ in walk_document(documents[key])
        for entry in node.get('material') or ()
      ]
    return targets[key]

  for source_key, document in documents.items():
    for path, node, _ in walk_document(document):
      for entry in node.get('material') or ():
        link = entry.get('sameAs')
        if not isinstance(link, dict):
          continue
        where = f'{source_key} at {path}'
        target = link.get('source')
        if target not in documents:
          messages.append(('error', f'{where}: `sameAs` names "{target}", which has no tree'))
          continue
        if target == source_key:
          messages.append(('error', f'{where}: `sameAs` names its own source'))
          continue
        own, theirs = source_year(source_key), source_year(target)
        if own is not None and theirs is not None and theirs > own:
          messages.append(('error', f'{where}: `sameAs` points at a later source'))
        matches = len(same_as_matches(target_entries(target), link))
        if matches != 1:
          messages.append(
            ('error', f'{where}: `sameAs` matches {matches} entries in "{target}", not 1')
          )
  return messages


def figure_refs(node, is_cited=False):
  """Every `illustrations[*].of` on a primary node names exactly one
  material entry on the node, by a number (either range endpoint) or the
  label, or else by a number inside a range pair's run (an exact match
  takes precedence); no match or several is an error.
  A cited entry's locators name nothing on the node (`null_material`
  rejects an `of` there), so they are not read."""
  if is_cited:
    return []
  messages = []
  entries = node.get('material') or ()
  for figure in node.get('illustrations') or ():
    if not isinstance(figure, dict):
      continue
    of = figure.get('of')
    if of is None:
      continue
    for value in of if isinstance(of, list) else [of]:
      matches = len(entries_named(entries, value))
      if matches != 1:
        messages.append(
          ('error', f'figure "of" value "{value}" matches {matches} material entries, not 1'),
        )
  return messages


def cast_refs(node):
  """Every `castOf` names exactly one material entry on the node, by the
  same rule as figure `of` (a number, a range endpoint included, or a
  `label`, else a number inside a range pair's run); no match or several
  is an error, and an entry naming itself is an error."""
  messages = []
  entries = node.get('material') or ()
  for entry in entries:
    value = entry.get('castOf')
    if value is None:
      continue
    matches = entries_named(entries, value)
    if len(matches) != 1:
      messages.append(
        ('error', f'castOf "{value}" matches {len(matches)} material entries, not 1'),
      )
    elif matches[0] is entry:
      messages.append(('error', f'castOf "{value}" names the entry itself'))
  return messages


def _known_forms(entry):
  """The folded `prefixes` and `otherNames` of a registry entry, each also
  without a trailing period."""
  forms = set()
  for values in (entry.get('prefixes'), entry.get('otherNames')):
    for value in values or ():
      form = _fold(value)
      forms.update({form, form.rstrip('.').rstrip()} - {''})
  return forms


def _begins_with_form(number, entry):
  """Whether `number` begins with a form of `entry` followed by a space,
  hyphen, period or digit."""
  text = _fold(number)
  for form in _known_forms(entry):
    if text.startswith(form) and len(text) > len(form):
      following = text[len(form)]
      if following in ' -.' or following.isdigit():
        return True
  return False


def _prefixes_used(document):
  """Every `prefix` a material entry or a locality number in the
  file uses."""
  used = set()
  all_contexts = [document.get('contexts')]
  for _, node, _ in walk_document(document):
    used.update(e['prefix'] for e in node.get('material') or () if e.get('prefix') is not None)
    all_contexts.append(node.get('contexts'))
  for contexts in all_contexts:
    used.update(n['prefix'] for n in _locality_objects(contexts) if n.get('prefix') is not None)
  return used


def file_prefixes(document, repositories):
  """The tree file's `prefixes` map and `localityRegister`: each value and
  the register must be a registry key (errors); each prefix is used by a
  material entry or a locality number in the file (an error otherwise); and
  the registry entry lists the prefix among its `prefixes` or `otherNames`
  (a warning when it does not, unless the entry lists none at all, as the
  registers for series a holder numbers separately do until their forms are
  entered)."""
  prefixes = document.get('prefixes') or {}
  messages = []
  register = document.get('localityRegister')
  if register is not None and register not in repositories:
    messages.append(('error', f'localityRegister "{register}" is not a key of the registry'))
  if not prefixes:
    return messages
  used = _prefixes_used(document)
  for prefix, key in prefixes.items():
    if key not in repositories:
      messages.append(
        ('error', f'prefix "{prefix}" is mapped to "{key}", which is not a key of the registry')
      )
    elif (forms := _known_forms(repositories[key])) and _fold(prefix).rstrip(
      '.'
    ).rstrip() not in forms:
      messages.append(('warning', f'prefix "{prefix}" is not a known form of "{key}"'))
    if prefix not in used:
      messages.append(
        ('error', f'prefix "{prefix}" in the file\'s `prefixes` map is used by nothing')
      )
  return messages


def number_entries(node, prefixes, repositories):
  """Checks on `node`'s material entries: an explicit `repository` that is
  no registry key is an error; a `prefix` not in the file's `prefixes` map
  is an error; `numbers` with no `prefix`, `repository` or `holder` is an
  error; a string number that begins with a prefix or other name of its own
  register (the one the map gives the prefix, or the entry's `repository`)
  is a warning, the split being probably wrong."""
  messages = []
  for entry in node.get('material') or ():
    repository = entry.get('repository')
    if repository is not None and repository not in repositories:
      messages.append(('error', f'repository "{repository}" is not a key of the registry'))
    if 'numbers' not in entry:
      continue
    prefix = entry.get('prefix')
    if prefix is not None and prefix not in prefixes:
      messages.append(('error', f'prefix "{prefix}" is not in the file\'s `prefixes` map'))
    if prefix is None and repository is None and entry.get('holder') is None:
      messages.append(('error', 'numbers with no prefix, repository or holder'))
    registers = []
    for register in (prefixes.get(prefix), repository):
      if register in repositories and register not in registers:
        registers.append(register)
    for number in flat_numbers(entry):
      if not isinstance(number, str):
        continue
      for register in registers:
        if _begins_with_form(number, repositories[register]):
          messages.append(
            ('warning', f'number "{number}" begins with a prefix of its register "{register}"')
          )
          break
  return messages


def locality_objects(contexts, prefixes, locality_register, repositories):
  """Checks on the object-form locality numbers of a `{key: context}` map:
  a `prefix` not in the file's `prefixes` map is an error, a `register`
  that is no registry key is an error, and a number with neither, in a file
  with no `localityRegister`, is a warning."""
  messages = []
  for number in _locality_objects(contexts):
    prefix, register = number.get('prefix'), number.get('register')
    if prefix is not None and prefix not in prefixes:
      messages.append(('error', f'prefix "{prefix}" is not in the file\'s `prefixes` map'))
    if register is not None and register not in repositories:
      messages.append(('error', f'locality register "{register}" is not a key of the registry'))
    if prefix is None and register is None and locality_register is None:
      messages.append(('warning', f'locality number "{number.get("number")}" has no register'))
  return messages


# What a `tentative` list may not name: the marker itself, and the keys that
# are not printed values (a range's regions carry their own per-element form).
_NOT_QUERIABLE = ('tentative', 'notes', 'asPrinted', 'inferred', 'sources', 'regions')


def tentative_fields(obj, kind, file_level=False):
  """The `tentative` marker of one range or context (`kind` is "range" or
  "context", for the messages): a name in the list that the object does not
  carry is an error, and so is one that is not a printed value
  (`_NOT_QUERIABLE`); `tentative: true` on a file-level context is an error,
  since the doubt belongs to the node or the specimen that uses it."""
  tentative = (obj or {}).get('tentative')
  if tentative is None:
    return []
  if tentative is True:
    if file_level:
      return [
        (
          'error',
          'a file-level context cannot be `tentative: true`; the doubt belongs to the node '
          'or the specimen that uses it',
        )
      ]
    return []
  messages = []
  for name in tentative if isinstance(tentative, list) else ():
    if name in _NOT_QUERIABLE:
      messages.append(('error', f'`tentative` cannot name `{name}`, which is not a printed value'))
    elif name not in obj:
      messages.append(('error', f'`tentative` names `{name}`, which the {kind} does not carry'))
  return messages


def range_tentatives(node):
  """`tentative_fields` over every range on `node`."""
  return [
    message
    for rng in node.get('ranges') or ()
    if isinstance(rng, dict)
    for message in tentative_fields(rng, 'range')
  ]


def context_tentatives(contexts, file_level=False):
  """`tentative_fields` over every context of a `{key: context}` map (a
  node's `contexts` or, with `file_level`, the tree file's), each message
  naming its context."""
  return [
    (level, f'context "{key}": {message}')
    for key, context in (contexts or {}).items()
    if isinstance(context, dict)
    for level, message in tentative_fields(context, 'context', file_level)
  ]


NULLABLE_FIELDS = ('material', 'illustrations', 'contexts', 'ranges')
# Every content field that may be null on a primary node; `synonyms` and
# `type` are the ones that cited entries may carry as a list or a node (a
# nested synonymy, the type of a synonym), so the cited-entry rule above
# reads only `NULLABLE_FIELDS` (`nomenclature.type_node` has `type: null`,
# `nomenclature.children_null` `children: null`).
ALL_NULLABLE_FIELDS = (*NULLABLE_FIELDS, 'synonyms', 'type', 'children')
_PRIMARY_ONLY_KEYS = ('of', 'depicts')


def _locator_errors(locators, where):
  """One error for each `of` or `depicts` on each entry of `locators`, the
  locators of a figure in a cited work, which depict nothing of this
  node's own."""
  return [
    ('error', f'{where} entry carries `{key}`')
    for locator in locators or ()
    if isinstance(locator, dict)
    for key in _PRIMARY_ONLY_KEYS
    if key in locator
  ]


def _authorities(node):
  """`node`'s `authority` and every `ex` authority nested in it."""
  authority = node.get('authority')
  while isinstance(authority, dict):
    yield authority
    authority = authority.get('ex')


def null_material(node, is_cited):
  """A cited entry (a synonymy entry, an earlier state) locates the cited
  work's own material, so it carries none of `material`, `contexts` or
  `ranges`, null or not. It may carry `illustrations`, locators for a
  figure in the cited work, but never null and never with `of` or
  `depicts`; the same ban on `of` and `depicts` holds for
  `authority.illustrations` on any node. A `material: null` node beside an
  illustration that still names one (`of` set) contradicts itself. A
  `synonyms: null` (the source prints no synonymy for the node) is an
  error on a cited entry, which lists synonymy of its own, and beside a
  `non` list, which is a synonymy."""
  messages = []
  if is_cited:
    for field in NULLABLE_FIELDS:
      if field not in node:
        continue
      if field != 'illustrations':
        messages.append(('error', f'cited entry carries `{field}`'))
      elif node[field] is None:
        messages.append(('error', 'cited entry carries `illustrations: null`'))
      else:
        messages.extend(_locator_errors(node[field], 'cited entry `illustrations`'))
  for authority in _authorities(node):
    messages.extend(_locator_errors(authority.get('illustrations'), '`authority.illustrations`'))
  if not is_cited and 'material' in node and node.get('material') is None:
    if any(
      isinstance(f, dict) and f.get('of') is not None for f in node.get('illustrations') or ()
    ):
      messages.append(('error', '`material: null` beside a figure whose `of` names one'))
  if 'synonyms' in node and node['synonyms'] is None:
    if is_cited:
      messages.append(('error', 'cited entry carries `synonyms: null`'))
    if node.get('non'):
      messages.append(('error', '`synonyms: null` beside a `non` list'))
  return messages


def unused_fields(document):
  """A field the file's `unused` lists still appears, even as `null`, on
  some node: an error naming that node's path. `illustrations` counts only
  on a primary node; a cited entry's locators are another use. A node
  marked `isType` is a use of `type` too, the older form of the statement."""
  unused = document.get('unused') or ()
  if not unused:
    return []
  messages = []
  for path, node, is_cited in walk_document(document):
    for field in unused:
      if field in node and not (field == 'illustrations' and is_cited):
        messages.append(('error', f'`{field}` is listed as `unused` but appears at {path}'))
    if 'type' in unused and node.get('isType'):
      messages.append(
        ('error', f'`type` is listed as `unused` but a child at {path} is marked `isType`')
      )
  return messages


def bracket_errors(document):
  """The bracket markers of each tree in a raw tree file that do not pair
  (`taxa.bracket_spans`: a start for a taxon already open, an end with no
  open start, a start the tree never closes), as ``('error', message)``
  pairs naming the node's path; the loader finds the same in each loaded
  `Tree`. Only the `children` axis is read."""
  trees = {}
  for path, node, _ in walk_document(document):
    position, _, pointer = path.partition('/')
    segments = pointer.split('/') if pointer else []
    if all(s == 'children' or s.isdigit() for s in segments):
      marks = (node.get('bracketStart'), node.get('bracketEnd'))
      trees.setdefault(position, []).append(
        (path, len(segments) // 2, *(m if isinstance(m, str) else None for m in marks))
      )
  messages = []
  for entries in trees.values():
    _, errors, _ = bracket_spans(entries)
    messages.extend(
      ('error', f'{path}: {BRACKET_ERRORS[kind].format(key=key)}') for path, kind, key in errors
    )
  return messages


def section_errors(document):
  """The section markers of each taxonomy in a raw tree file that break a
  rule, as ``('error', message)`` pairs naming the node's path: a marker in
  a tree that is no taxonomy or on a node that is no `children` entry, and,
  in each `children` list, the markers that do not pair (`taxa.section_spans`:
  a start for a key already open, an end with no open start, a start the
  list never closes, an interleaving); the loader finds the same in each
  loaded `Tree`. Only the `children` axis is read."""
  taxonomies = len(document.get('taxonomies') or ())
  tree_types = {
    taxonomies + index: str((phylogeny or {}).get('treeType') or '').lower()
    for index, phylogeny in enumerate(document.get('phylogenies') or ())
  }
  messages = []
  lists = {}
  for path, node, _ in walk_document(document):
    position, _, pointer = path.partition('/')
    segments = pointer.split('/') if pointer else []
    marks = {f: node.get(f) for f in ('sectionStart', 'sectionEnd') if node.get(f) is not None}
    start = node.get('sectionStart')
    start = start.get('section') if isinstance(start, dict) else None
    end = node.get('sectionEnd')
    keys = (start if isinstance(start, str) else None, end if isinstance(end, str) else None)
    tree_type = tree_types.get(int(position), 'taxonomy')
    primary = all(s == 'children' or s.isdigit() for s in segments)
    for field in marks:
      if tree_type != 'taxonomy':
        messages.append(
          ('error', f'{path}: ' + SECTION_NOT_TAXONOMY.format(field=field, tree_type=tree_type))
        )
      elif not (primary and segments):
        messages.append(('error', f'{path}: ' + SECTION_NOT_CHILD.format(field=field)))
    if tree_type == 'taxonomy' and primary and segments:
      lists.setdefault((position, tuple(segments[:-2])), []).append((path, *keys))
  for entries in lists.values():
    _, errors, _ = section_spans(entries)
    messages.extend(
      ('error', f'{path}: {SECTION_ERRORS[kind].format(key=key, other=other)}')
      for path, kind, key, other in errors
    )
  return messages


def walk_document(document):
  """Yield `(path, node, is_cited)` for every node of every taxonomy and
  phylogeny in a tree file's raw document: related subtrees before
  children, depth first, mirroring `Tree.walk`/`Tree.is_cited` so the
  loaded corpus and an unloaded draft share one walk. `path` is
  `<position><pointer>`, the same form `claims.py` builds from a `Tree`.
  """
  position = 0
  for tax_tree in document.get('taxonomies') or ():
    yield from _walk_node(tax_tree, position, (), False)
    position += 1
  for phy_tree in document.get('phylogenies') or ():
    yield from _walk_node((phy_tree or {}).get('tree') or {}, position, (), False)
    position += 1


def _walk_node(node, position, relpath, is_cited):
  if not isinstance(node, dict):
    return
  pointer = '/' + '/'.join(str(p) for p in relpath) if relpath else ''
  yield f'{position}{pointer}'.rstrip('/'), node, is_cited

  for axis in Tree.RELATED_AXES:
    value = node.get(axis.name)
    cited = axis.name in Tree.CITED_AXES
    if axis.many:
      for index, item in enumerate(value or ()):
        yield from _walk_node(item, position, (*relpath, axis.name, index), cited)
    elif isinstance(value, dict):
      yield from _walk_node(value, position, (*relpath, axis.name), cited)

  for index, child in enumerate(node.get('children') or ()):
    yield from _walk_node(child, position, (*relpath, 'children', index), False)
