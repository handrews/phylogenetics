"""Material integrity checks: contexts, catalog numbers, casts, figures,
nulls, and the repository registry and a tree file's `repositories` list.

Pure functions over a raw node dict and the file-level maps, so
`scripts/check_draft.py` can run the same checks on an unloaded draft; the
loader (`load.py`) runs them over the corpus's own documents. Each check
returns a list of ``(level, message)`` pairs, ``level`` being ``'error'``
or ``'warning'``; the caller adds the source key and, for a per-node
check, the node path. `repository_of` is exported for the claims
extractor (stage 2).
"""

import re

from .taxa import Tree

_DIGIT_RE = re.compile(r'\d')
_WHITESPACE_RE = re.compile(r'\s+')


def _fold(text):
  """Case- and whitespace-insensitive comparison form."""
  return _WHITESPACE_RE.sub(' ', text.strip()).casefold()


def _prefix(number):
  """The leading run before the first digit, stripped, with a trailing
  hyphen dropped ("PE-214" and "PE 214" both give "PE"); `None` if empty.
  A hyphen inside the number ("MCZ 602-D1") is past the first digit and
  untouched."""
  match = _DIGIT_RE.search(number)
  prefix = (number[: match.start()] if match else number).strip()
  prefix = prefix.removesuffix('-').strip()
  return prefix or None


def _is_match(candidate, prefix):
  """Whether `candidate` equals `prefix` or is a token-boundary prefix of it."""
  if candidate == prefix:
    return True
  return prefix.startswith(candidate) and prefix[len(candidate)] == ' '


AMBIGUOUS = 'ambiguous'


def _prefix_index(repositories):
  """`{folded candidate: {key: via}}` over every entry's `prefixes` (via
  `'prefix'`) and `formerly` (via `'formerly'`); a key claiming a candidate
  both ways counts as `'prefix'`. Registry keys are slugs, never
  candidates."""
  index = {}
  for key, entry in repositories.items():
    for via, values in (('formerly', entry.get('formerly')), ('prefix', entry.get('prefixes'))):
      for value in values or ():
        index.setdefault(_fold(value), {})[key] = via
  return index


def repository_of(number, repositories, file_repositories=()):
  """`(key, via)` for a catalog number's repository, resolved from its
  printed prefix (see `_prefix`; compared case-insensitively with
  whitespace collapsed).

  The candidates are every registry entry's `prefixes` and `formerly`; the
  longest one equal to the prefix or a token-boundary prefix of it wins.
  When one entry claims it, `via` is `'prefix'` or `'formerly'`. When
  several claim it, the entries in `file_repositories` (the tree file's
  own list) are preferred: exactly one left gives `(key, 'file')`.

  Returns `(None, None)` when nothing matches, and `(keys, 'ambiguous')`,
  `keys` a sorted tuple of the entries still competing, when the file list
  does not settle it. A caller tests `via == AMBIGUOUS` before using `key`.
  """
  prefix = _prefix(number)
  if prefix is None:
    return None, None
  folded_prefix = _fold(prefix)

  best = None
  for candidate, claims in _prefix_index(repositories).items():
    if _is_match(candidate, folded_prefix) and (best is None or len(candidate) > len(best[0])):
      best = (candidate, claims)
  if best is None:
    return None, None

  claims = best[1]
  if len(claims) == 1:
    ((key, via),) = claims.items()
    return key, via
  listed = [key for key in claims if key in file_repositories]
  if len(listed) == 1:
    return listed[0], 'file'
  return tuple(sorted(listed or claims)), AMBIGUOUS


def _catalog_values(node):
  """`(entry, elements)` for every catalog number on every material entry
  of `node`; `elements` is one printed string or a range pair's two."""
  for entry in node.get('material') or ():
    for number in entry.get('catalogNumbers') or ():
      yield entry, (number if isinstance(number, list) else [number])


def _has_ellipsis(elements):
  return any('...' in e or '…' in e for e in elements)


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


def file_repositories_used(document, repositories):
  """Every key in the tree file's `repositories` list is a registry key
  and is the resolved holder (by prefix, or by an explicit `repository`)
  of at least one catalog number in the file; an error otherwise."""
  listed = document.get('repositories') or ()
  if not listed:
    return []
  messages = [
    ('error', f'listed repository "{key}" is not a key of the registry')
    for key in listed
    if key not in repositories
  ]
  used = set()
  for _, node, _ in walk_document(document):
    for entry, elements in _catalog_values(node):
      if entry.get('repository') is not None:
        used.add(entry['repository'])
        continue
      if _has_ellipsis(elements):
        continue
      for element in elements:
        key, via = repository_of(element, repositories, listed)
        if via not in (None, AMBIGUOUS):
          used.add(key)
  messages.extend(
    ('error', f'repository "{key}" is listed but no catalog number in the file resolves to it')
    for key in listed
    if key in repositories and key not in used
  )
  return messages


def _context_key(ref):
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
    key = _context_key(ref)
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
        referenced.add(_context_key(ref))
  return [
    ('warning', f'context "{key}" is defined but referenced by no material entry')
    for key in sorted(set(file_contexts) - referenced)
  ]


def _entry_identifies(entry, value):
  """Whether `value` names `entry`, by `label` or by any element of a
  `catalogNumbers` entry (a range pair's endpoints count separately)."""
  if entry.get('label') == value:
    return True
  for number in entry.get('catalogNumbers') or ():
    elements = number if isinstance(number, list) else [number]
    if value in elements:
      return True
  return False


def figure_refs(node):
  """Every `figures[*].of` names exactly one material entry on the node,
  by exact string against a catalog number (either range endpoint) or the
  label; no match or several is an error."""
  messages = []
  entries = node.get('material') or ()
  for figure in node.get('figures') or ():
    of = figure.get('of')
    if of is None:
      continue
    for value in of if isinstance(of, list) else [of]:
      matches = sum(1 for entry in entries if _entry_identifies(entry, value))
      if matches != 1:
        messages.append(
          ('error', f'figure "of" value "{value}" matches {matches} material entries, not 1'),
        )
  return messages


def cast_refs(node):
  """Every `castOf` names exactly one material entry on the node, by the
  same rule as figure `of` (exact string against a catalog number, a range
  endpoint included, or a `label`); no match or several is an error, and
  an entry naming itself is an error."""
  messages = []
  entries = node.get('material') or ()
  for entry in entries:
    value = entry.get('castOf')
    if value is None:
      continue
    matches = [other for other in entries if _entry_identifies(other, value)]
    if len(matches) != 1:
      messages.append(
        ('error', f'castOf "{value}" matches {len(matches)} material entries, not 1'),
      )
    elif matches[0] is entry:
      messages.append(('error', f'castOf "{value}" names the entry itself'))
  return messages


def unresolved_catalog_numbers(node, repositories, file_repositories=()):
  """The printed values of `node`'s catalog numbers whose prefix resolves
  to no repository (an ambiguous prefix is not listed: `catalog_numbers`
  reports it), among entries with no explicit `repository`."""
  unresolved = []
  for entry, elements in _catalog_values(node):
    if entry.get('repository') is not None or _has_ellipsis(elements):
      continue
    unresolved.extend(
      e for e in elements if repository_of(e, repositories, file_repositories)[1] is None
    )
  return unresolved


def catalog_numbers(node, repositories, file_repositories=()):
  """Catalog-number and repository checks for one node's `material`
  entries: an explicit `repository` not a registry key is an error; an
  ellipsis in a printed number is an error; for a number with no explicit
  `repository`, an unmatched prefix is a warning (stage 4 makes it an
  error), a prefix still claimed by several entries after
  `file_repositories` is an error naming them, and a range whose
  endpoints resolve to different repositories is an error.
  """
  messages = []
  for entry in node.get('material') or ():
    repository = entry.get('repository')
    if repository is not None and repository not in repositories:
      messages.append(('error', f'repository "{repository}" is not a key of the registry'))
  for entry, elements in _catalog_values(node):
    if _has_ellipsis(elements):
      messages.append(('error', f'catalog number {_shown(elements)!r} contains an ellipsis'))
      continue
    if entry.get('repository') is not None:
      continue
    resolved = []
    for element in elements:
      key, via = repository_of(element, repositories, file_repositories)
      if via is None:
        messages.append(
          ('warning', f'catalog number "{element}" has no resolvable repository prefix'),
        )
      elif via == AMBIGUOUS:
        messages.append(
          ('error', f'catalog number "{element}" has an ambiguous prefix: {", ".join(key)}'),
        )
      else:
        resolved.append(key)
    if len(resolved) == 2 and resolved[0] != resolved[1]:
      messages.append(
        ('error', f'catalog number range {_shown(elements)!r} resolves to different repositories'),
      )
  return messages


def _shown(elements):
  """A catalog number as the messages print it: a string, or a range pair."""
  return elements if len(elements) == 2 else elements[0]


_NULLABLE_FIELDS = ('material', 'figures', 'contexts', 'range')


def null_material(node, is_cited):
  """A cited entry (a synonymy entry, an earlier state) locates the cited
  work's own material, so it carries none of `material`, `figures`,
  `contexts` or `range`, null or not; a `material: null` node beside a
  figure that still names one (`of` set) contradicts itself."""
  messages = []
  if is_cited:
    for field in _NULLABLE_FIELDS:
      if field in node:
        messages.append(('error', f'cited entry carries `{field}`'))
  if 'material' in node and node.get('material') is None:
    if any(isinstance(f, dict) and f.get('of') is not None for f in node.get('figures') or ()):
      messages.append(('error', '`material: null` beside a figure whose `of` names one'))
  return messages


def unused_fields(document):
  """A field the file's `unused` lists still appears, even as `null`, on
  some node: an error naming that node's path."""
  unused = document.get('unused') or ()
  if not unused:
    return []
  messages = []
  for path, node, _ in walk_document(document):
    for field in unused:
      if field in node:
        messages.append(('error', f'`{field}` is listed as `unused` but appears at {path}'))
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
