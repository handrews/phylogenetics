"""Check an AI-drafted tree file before a human audit.

    poetry run python scripts/check_draft.py drafts/1891_bell.f.j.yaml

Validates the draft against the tree schema the loader uses, then lists the
taxon keys, author keys and source keys the draft cites that have no record
yet, and the catalog numbers whose prefix resolves to no repository (also
reported by name, like a missing record). It then runs the material checks
(`phylohist.loader.material`) over the draft's nodes: a cited entry carrying
`material`/`contexts`/`ranges`, a null `illustrations`, or an `of`/`depicts`
in its `illustrations` (or in an `authority`'s); a null `material`,
`illustrations`, `contexts` or `ranges` on a primary node (only an auditor
sets nulls); a `unused` field still present on a node; an ellipsis or an
ambiguous prefix in a catalog number; a `repositories` list naming a missing
or unused entry; and a dangling `context`, figure `of` or `castOf`. Each is
printed with the node's path. Exit status 1 on a schema failure or any of
those, 0 otherwise; the unresolved lists are always printed, since a draft
normally needs new records.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from phylohist.loader import material  # noqa: E402
from phylohist.loader.io import (  # noqa: E402
  DATA_DIR,
  TREE_DEF,
  build_schema,
  load_yaml,
)

TAXON_FIELDS = ('taxon', 'openTaxon', 'cfTaxon', 'affTaxon', 'bracket')


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


def check_material(draft, repositories):
  """`(messages, prefixes)`: every `material.py` check's `(level, message)`
  over the draft, the per-node ones prefixed with the node's path, and the
  catalog numbers among them with no resolvable repository."""
  messages = [
    *((lv, f'repositories: {m}') for lv, m in material.registry_links(repositories)),
    *material.unreferenced_file_contexts(draft),
    *material.unused_fields(draft),
    *material.file_repositories_used(draft, repositories),
  ]
  prefixes = []
  file_repositories = draft.get('repositories') or ()

  file_contexts = draft.get('contexts') or {}
  for path, node, is_cited in material.walk_document(draft):
    node_contexts = node.get('contexts') or {}
    for check, args in (
      (material.context_refs, (node, node_contexts, file_contexts)),
      (material.figure_refs, (node, is_cited)),
      (material.catalog_numbers, (node, repositories, file_repositories)),
      (material.cast_refs, (node,)),
      (material.null_material, (node, is_cited)),
      (draft_nulls, (node, is_cited)),
    ):
      messages.extend((level, f'{path}: {message}') for level, message in check(*args))
    prefixes.extend(material.unresolved_catalog_numbers(node, repositories, file_repositories))

  return messages, prefixes


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
  known = {
    'taxa': set(load_yaml(DATA_DIR / 'taxa.yaml')),
    'authors': set(load_yaml(DATA_DIR / 'authors.yaml')),
    'sources': set(load_yaml(DATA_DIR / 'sources.yaml')),
  }
  for label, cited in (('taxa', taxa), ('authors', authors), ('sources', sources)):
    missing = sorted(cited - known[label])
    print(f'{label}: {len(cited)} cited, {len(missing)} without a record')
    for key in missing:
      print(f'  {key}')

  repositories = load_yaml(DATA_DIR / 'repositories.yaml')
  messages, prefixes = check_material(draft, repositories)

  unresolved = sorted(set(prefixes))
  print(f'prefixes: {len(unresolved)} without a resolvable repository')
  for value in unresolved:
    print(f'  {value}')

  for level, message in messages:
    print(f'{level}: {message}')
    if level == 'error':
      status = 1

  return status


if __name__ == '__main__':
  sys.exit(main(sys.argv))
