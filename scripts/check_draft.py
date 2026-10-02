"""Check an AI-drafted tree file before a human audit.

    poetry run python scripts/check_draft.py drafts/1891_bell.f.j.yaml

Validates the draft against the tree schema the loader uses, then lists the
taxon keys, author keys and source keys the draft cites that have no record
yet. It then runs the material checks
(`phylohist.loader.material`) over the draft's nodes: a cited entry carrying
`material`/`contexts`/`ranges`, a null `illustrations`, or an `of`/`depicts`
in its `illustrations` (or in an `authority`'s); a null `material`,
`illustrations`, `contexts` or `ranges` on a primary node (only an auditor
sets nulls); a `unused` field still present on a node; an explicit
`repository` that is no registry key; a `prefix` missing from the file's
`prefixes` map, a map entry that is unused, not a registry key or not a known
form of its register, numbers with no prefix, repository or holder, a number
that begins with its register's own prefix, and a locality number with no
register; and a dangling `context`, figure `of` or `castOf`. The
open-nomenclature checks (`phylohist.loader.nomenclature`) add a `cf` or `aff`
off an `openTaxon` node, on both, or aimed at a missing, unnamed or other-rank
taxon; a `quotedParent` above the species level; a `roleUncertain` with no
`role`; a `type` node with no taxon, beside a child marked `isType`, or with
a `fixedBy` its `fixation` cannot explain; and an open form linked to two
different taxa (a warning). The
`sameAs` links (`phylohist.loader.material.same_as_links`) are checked against
the tree files in `data/trees/` that the draft's links name: a source with no
tree, the draft's own source, a later source, or a target that is not exactly
one entry. Each is printed with the node's path. Exit status 1 on a schema failure or any of
those, 0 otherwise; the lists of records without an entry are always printed,
since a draft normally needs new records.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from phylohist.loader import material, nomenclature  # noqa: E402
from phylohist.loader.io import (  # noqa: E402
  DATA_DIR,
  TREE_DEF,
  TREE_DIR,
  build_schema,
  load_yaml,
)

TAXON_FIELDS = ('taxon', 'openTaxon', 'bracket')


def walk(node, taxa, authors, sources):
  if isinstance(node, dict):
    for field in TAXON_FIELDS:
      if isinstance(node.get(field), str):
        taxa.add(node[field])
    for author in node.get('auth') or ():
      # A capitalised author string is the convention for an author with no
      # record; only key-form strings are expected to resolve.
      if isinstance(author, str) and author.lower() == author:
        authors.add(author)
    for field in ('source', 'in'):
      value = node.get(field)
      if isinstance(value, str):
        sources.add(value)
    editorial = node.get('editorial')
    if isinstance(editorial, dict):
      corrected = (editorial.get('corrections') or {}).get('authority') or {}
      if isinstance(corrected.get('source'), str):
        sources.add(corrected['source'])
    for value in node.values():
      walk(value, taxa, authors, sources)
  elif isinstance(node, list):
    for value in node:
      walk(value, taxa, authors, sources)


def draft_nulls(node, is_cited):
  """A draft never emits `null` for a nullable field on a primary node
  (roadmap G11): a model that has not found the content would write a false
  "the source prints none"; only the auditor sets nulls. (On a cited entry
  `null_material` already reports them.)"""
  if is_cited:
    return []
  return [
    ('error', f'draft carries `{field}: null`; only an auditor sets nulls')
    for field in material.ALL_NULLABLE_FIELDS
    if field in node and node[field] is None
  ]


def check_material(draft, repositories, taxa):
  """Every `material.py` and `nomenclature.py` check's `(level, message)`
  over the draft, the per-node ones prefixed with the node's path. `taxa`
  looks a taxon key up (`nomenclature.record_lookup`)."""
  messages = [
    *nomenclature.compared_link_conflicts([('draft', draft)]),
    *((lv, f'repositories: {m}') for lv, m in material.registry_links(repositories)),
    *material.unreferenced_file_contexts(draft),
    *material.unused_fields(draft),
    *material.file_prefixes(draft, repositories),
  ]
  file_prefixes = draft.get('prefixes') or {}
  locality_register = draft.get('localityRegister')

  file_contexts = draft.get('contexts') or {}
  messages.extend(
    material.locality_objects(file_contexts, file_prefixes, locality_register, repositories)
  )
  messages.extend(material.context_tentatives(file_contexts, file_level=True))
  for path, node, is_cited in material.walk_document(draft):
    node_contexts = node.get('contexts') or {}
    for check, args in (
      (material.context_refs, (node, node_contexts, file_contexts)),
      (material.figure_refs, (node, is_cited)),
      (material.number_entries, (node, file_prefixes, repositories)),
      (
        material.locality_objects,
        (node_contexts, file_prefixes, locality_register, repositories),
      ),
      (material.context_tentatives, (node_contexts,)),
      (material.range_tentatives, (node,)),
      (material.cast_refs, (node,)),
      (material.null_material, (node, is_cited)),
      (draft_nulls, (node, is_cited)),
      (nomenclature.compared_links, (node, taxa)),
      (nomenclature.quoted_parent, (node, taxa)),
      (nomenclature.role_uncertain, (node,)),
      (nomenclature.type_node, (node,)),
    ):
      messages.extend((level, f'{path}: {message}') for level, message in check(*args))

  return messages


def check_same_as(key, draft, sources):
  """The `sameAs` links of the draft (the tree file of source `key`), read
  against the tree file `data/trees/<source>.yaml` of each source they name
  when it exists; `sources` is the raw `data/sources.yaml`. Only messages
  about the draft are returned."""
  documents = {key: draft}
  for _, node, _ in material.walk_document(draft):
    for entry in node.get('material') or ():
      link = entry.get('sameAs')
      target = link.get('source') if isinstance(link, dict) else None
      if isinstance(target, str) and target not in documents:
        tree = TREE_DIR / f'{target}.yaml'
        if tree.exists():
          documents[target] = load_yaml(tree)

  def source_year(source_key):
    source = sources.get(source_key)
    if source is None:
      return None
    return 9999 if source.get('inPrep') else (source.get('pubDate') or {}).get('year')

  return [
    (level, message)
    for level, message in material.same_as_links(documents, source_year)
    if message.startswith(f'{key} at ')
  ]


def main(argv):
  if len(argv) != 2:
    print(__doc__)
    return 2
  path = pathlib.Path(argv[1])
  schema = build_schema()
  draft = load_yaml(path)
  # `check` logs the reasons for whatever it rejects.
  if schema[TREE_DEF].check(draft):
    print(f'{path}: valid against the tree schema')
    status = 0
  else:
    print(f'{path}: not valid against the tree schema')
    status = 1

  # The draft's own source is named by its file, and the loader skips a
  # tree whose source has no record.
  taxa, authors, sources = set(), set(), {path.stem}
  walk(draft, taxa, authors, sources)
  records = load_yaml(DATA_DIR / 'taxa.yaml')
  source_records = load_yaml(DATA_DIR / 'sources.yaml')
  known = {
    'taxa': set(records),
    'authors': set(load_yaml(DATA_DIR / 'authors.yaml')),
    'sources': set(source_records),
  }
  for label, cited in (('taxa', taxa), ('authors', authors), ('sources', sources)):
    missing = sorted(cited - known[label])
    print(f'{label}: {len(cited)} cited, {len(missing)} without a record')
    for key in missing:
      print(f'  {key}')

  repositories = load_yaml(DATA_DIR / 'repositories.yaml')
  messages = check_material(draft, repositories, nomenclature.record_lookup(records))
  messages.extend(check_same_as(path.stem, draft, source_records))

  for level, message in messages:
    print(f'{level}: {message}')
    if level == 'error':
      status = 1

  return status


if __name__ == '__main__':
  sys.exit(main(sys.argv))
