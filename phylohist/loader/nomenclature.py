"""Open-nomenclature integrity checks: the `cf`/`aff` link of an open form,
`quotedParent`, and a queried role.

Pure functions over a raw node dict, in the way of `material.py`: the
loader (`load.py`) runs them over the corpus's own documents and
`scripts/check_draft.py` over an unloaded draft. Each returns a list of
``(level, message)`` pairs, ``level`` being ``'error'`` or ``'warning'``;
the caller adds the source key and, for a per-node check, the node's path.
A check that needs a taxon record takes `taxa`, a callable from a taxon
key to an object with `name` and `rank` (a loaded `Taxon` does), or `None`
for a key with no record; `record_lookup` builds one from the raw
`data/taxa.yaml` for a caller that has not loaded the corpus.
"""

import collections

from .material import walk_document

# The two signs of an open form's link, as the node fields naming the taxon
# it is compared with.
SIGNS = ('cf', 'aff')
_SPECIES_RANKS = ('species', 'subspecies', 'variety')
_OWN_FIELDS = ('taxon', 'openTaxon')

_Record = collections.namedtuple('_Record', 'name rank')


def _raw_rank(records, key, seen=()):
  """The rank `Taxon` would give the raw record: that of the record a
  spelling is of, else its own `rank`, else a species when its name is
  lower-case and a genus otherwise; `None` when it has neither."""
  data = records[key]
  for field in ('altSpellingOf', 'vulgarSpellingOf'):
    target = data.get(field)
    if target in records and target not in seen:
      return _raw_rank(records, target, (*seen, key))
  if data.get('rank'):
    return data['rank']
  name = data.get('name')
  return None if name is None else 'species' if name.islower() else 'genus'


def record_lookup(records):
  """A `taxa` callable over the raw `data/taxa.yaml` mapping."""

  def lookup(key):
    if key not in records:
      return None
    return _Record(records[key].get('name'), _raw_rank(records, key))

  return lookup


def _is_species_level(record):
  return (record.rank or '').lower() in _SPECIES_RANKS


def compared_link(node):
  """`(sign, target)` for an open form's link, or `None` when the node has
  no `openTaxon` or no link (or both, which `compared_links` reports)."""
  signs = [sign for sign in SIGNS if sign in node]
  if 'openTaxon' not in node or len(signs) != 1:
    return None
  return signs[0], node[signs[0]]


def compared_links(node, taxa):
  """A `cf` or `aff` sits only on an `openTaxon` node, never both on one
  node; its target has a record that is named (not itself a placeholder),
  and the open record and the target are both species-level or both not;
  an error otherwise."""
  signs = [sign for sign in SIGNS if sign in node]
  messages = [
    ('error', f'`{sign}` on a node that is not an `openTaxon`')
    for sign in signs
    if 'openTaxon' not in node
  ]
  if len(signs) > 1:
    messages.append(('error', 'both `cf` and `aff` on one node'))
  own = taxa(node['openTaxon']) if isinstance(node.get('openTaxon'), str) else None
  for sign in signs:
    key = node[sign]
    if not isinstance(key, str):
      continue
    target = taxa(key)
    if target is None:
      messages.append(('error', f'`{sign}` target "{key}" has no taxon record'))
    elif not target.name:
      messages.append(
        ('error', f'`{sign}` target "{key}" is itself a placeholder (it has no name)')
      )
    elif own is not None and own.rank and target.rank:
      if _is_species_level(own) != _is_species_level(target):
        messages.append(
          (
            'error',
            f'`{sign}` target "{key}" ({target.rank}) is not at the rank level of the open '
            f'form "{node["openTaxon"]}" ({own.rank})',
          ),
        )
  return messages


def quoted_parent(node, taxa):
  """`quotedParent` quotes a species' genus, so the node's own record is
  species-level; an error otherwise."""
  if not node.get('quotedParent'):
    return []
  key = next((node[f] for f in _OWN_FIELDS if isinstance(node.get(f), str)), None)
  record = taxa(key) if key is not None else None
  if record is None or not record.rank or _is_species_level(record):
    return []
  return [('error', '`quotedParent` on a node that is not a species-level name')]


def role_uncertain(node):
  """`roleUncertain` queries the role word, so the entry has a `role`; an
  error otherwise."""
  return [
    ('error', 'material entry has `roleUncertain` but no `role`')
    for entry in node.get('material') or ()
    if isinstance(entry, dict) and entry.get('roleUncertain') and not entry.get('role')
  ]


def compared_link_conflicts(documents):
  """An open record linked to different `(sign, target)` pairs by nodes
  anywhere in `documents`, an iterable of ``(source key, raw document)``,
  is a warning naming the key and the links with where each is; a node
  that uses the record with no link is not a conflict."""
  seen = collections.defaultdict(dict)
  for source_key, document in documents:
    for path, node, _ in walk_document(document):
      link = compared_link(node)
      if link is not None and isinstance(node['openTaxon'], str):
        seen[node['openTaxon']].setdefault(link, f'{source_key} at {path}')
  return [
    (
      'warning',
      f'open form "{key}" is compared with different taxa: '
      + '; '.join(f'{sign} {target} ({where})' for (sign, target), where in links.items()),
    )
    for key, links in sorted(seen.items())
    if len(links) > 1
  ]
