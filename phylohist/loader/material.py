"""Material integrity checks: contexts, catalog numbers, figures, nulls.

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
  """The leading run before the first digit, stripped; `None` if empty."""
  match = _DIGIT_RE.search(number)
  prefix = (number[: match.start()] if match else number).strip()
  return prefix or None


def _is_match(candidate, prefix):
  """Whether `candidate` equals `prefix` or is a token-boundary prefix of it."""
  if candidate == prefix:
    return True
  return prefix.startswith(candidate) and prefix[len(candidate)] == ' '


def repository_of(number, repositories, abbreviations=None):
  """`(registry_key, via)` for a catalog number's repository, resolved from
  its printed prefix; `(None, None)` when nothing matches.

  Candidates are `abbreviations` (the citing source's own map, `via`
  `'source'`), the registry's own keys (`'registry'`), and every
  registry entry's `formerly` alias (`'alias'`); the longest candidate
  that matches wins.
  """
  prefix = _prefix(number)
  if prefix is None:
    return None, None
  folded_prefix = _fold(prefix)

  def candidates():
    for abbreviation, key in (abbreviations or {}).items():
      yield abbreviation, key, 'source'
    for key in repositories:
      yield key, key, 'registry'
    for key, entry in repositories.items():
      for alias in entry.get('formerly') or ():
        yield alias, key, 'alias'

  best = None
  for candidate, key, via in candidates():
    if not _is_match(_fold(candidate), folded_prefix):
      continue
    if best is None or len(candidate) > len(best[0]):
      best = (candidate, key, via)

  return (best[1], best[2]) if best else (None, None)


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


def unresolved_catalog_numbers(node, repositories, abbreviations=None):
  """The printed values of `node`'s catalog numbers whose prefix resolves
  to no repository, among entries with no explicit `repository`."""
  unresolved = []
  for entry in node.get('material') or ():
    if entry.get('repository') is not None:
      continue
    for number in entry.get('catalogNumbers') or ():
      for value in number if isinstance(number, list) else [number]:
        if '...' in value or '…' in value:
          continue
        if repository_of(value, repositories, abbreviations)[0] is None:
          unresolved.append(value)
  return unresolved


def catalog_numbers(node, repositories, abbreviations=None):
  """Catalog-number and repository checks for one node's `material`
  entries (see 4 for prefix resolution): an explicit `repository` not a
  registry key is an error; an ellipsis in a printed number is an error;
  for a number with no explicit `repository`, an unresolved prefix is a
  warning (stage 4 makes it an error) and a range whose endpoints resolve
  to different repositories is an error.
  """
  messages = []
  for entry in node.get('material') or ():
    repository = entry.get('repository')
    if repository is not None and repository not in repositories:
      messages.append(('error', f'repository "{repository}" is not a key of the registry'))
    for number in entry.get('catalogNumbers') or ():
      elements = number if isinstance(number, list) else [number]
      if any('...' in e or '…' in e for e in elements):
        messages.append(('error', f'catalog number {number!r} contains an ellipsis'))
        continue
      if repository is not None:
        continue
      resolved = [repository_of(e, repositories, abbreviations)[0] for e in elements]
      for element, key in zip(elements, resolved, strict=True):
        if key is None:
          messages.append(
            ('warning', f'catalog number "{element}" has no resolvable repository prefix'),
          )
      if len(resolved) == 2 and None not in resolved and resolved[0] != resolved[1]:
        messages.append(
          ('error', f'catalog number range {number!r} resolves to different repositories'),
        )
  return messages


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
