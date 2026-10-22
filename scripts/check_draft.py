"""Check an AI-drafted tree file before a human audit.

    poetry run python scripts/check_draft.py drafts/1891_bell.f.j.yaml
    poetry run python scripts/check_draft.py --data tests/corpus some-draft.yaml

Validates the draft against the tree schema the loader uses, then lists the
taxon keys, author keys, source keys and section keys the draft cites that
have no record yet. It then runs over the draft every check the loader runs
over a tree file, from the tables of `phylohist.loader.checks` (the material
checks of `phylohist.loader.material` and the open-nomenclature checks of
`phylohist.loader.nomenclature`; each check's docstring says what it
reports), and adds the ones only a draft needs: the pairing of the bracket
and section markers, which the loader does as it builds each tree, and a
`null` on a primary node, which only an auditor sets. The draft's `sameAs`
links are checked against the tree files in `data/trees/` that they name. A
per-node message is printed with the node's path. Exit status 1 on a schema
failure or any error, 0 otherwise (a warning does not fail it); the lists of
records without an entry are always printed, since a draft normally needs
new records. `--data` names another directory shaped like `data/` to check
against.
"""

import argparse
import pathlib
import sys
import types

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from phylohist.loader import checks, material, nomenclature  # noqa: E402
from phylohist.loader.io import (  # noqa: E402
  DATA_DIR,
  TREE_DEF,
  TREE_DIR,
  build_schema,
  load_yaml,
)

TAXON_FIELDS = ('taxon', 'openTaxon', 'mineralTaxon', 'bracketStart', 'bracketEnd')


def walk(node, taxa, authors, sources, sections=None):
  if isinstance(node, dict):
    for field in TAXON_FIELDS:
      if isinstance(node.get(field), str):
        taxa.add(node[field])
    if sections is not None:
      start = node.get('sectionStart')
      if isinstance(start, dict) and isinstance(start.get('section'), str):
        sections.add(start['section'])
      if isinstance(node.get('sectionEnd'), str):
        sections.add(node['sectionEnd'])
    # The credits inside an `authority` block, which the recursion reaches
    # (a correction's too). A capitalised author string is the convention
    # for an author with no record; only key-form strings are expected to
    # resolve.
    for field in ('auth', 'in', 'attributedTo'):
      for author in node.get(field) or ():
        if isinstance(author, str) and author.lower() == author:
          authors.add(author)
    if isinstance(node.get('source'), str):
      sources.add(node['source'])
    for value in node.values():
      walk(value, taxa, authors, sources, sections)
  elif isinstance(node, list):
    for value in node:
      walk(value, taxa, authors, sources, sections)


def check_material(draft, repositories, taxa):
  """Every check the loader runs over a tree file (`phylohist.loader.checks`)
  and the draft-only ones, as `(level, message)` over the draft, the
  per-node ones prefixed with the node's path. `taxa` looks a taxon key up
  (`nomenclature.record_lookup`)."""
  scope = checks.file_scope(draft, repositories, taxa)
  return [
    *nomenclature.compared_link_conflicts([('draft', draft)]),
    *((lv, f'repositories: {m}') for lv, m in material.registry_links(repositories)),
    *checks.file_messages(scope, checks.DRAFT_FILE_CHECKS),
    *((lv, f'{p}: {m}') for p, lv, m in checks.node_messages(scope, checks.DRAFT_NODE_CHECKS)),
  ]


def check_same_as(key, draft, sources, tree_dir=TREE_DIR):
  """The `sameAs` links of the draft (the tree file of source `key`), read
  against the tree file `<tree_dir>/<source>.yaml` of each source they name
  when it exists; `sources` is the raw `sources.yaml`. Only messages
  about the draft are returned."""
  documents = {key: draft}
  for _, node, _ in material.walk_document(draft):
    for entry in node.get('material') or ():
      link = entry.get('sameAs')
      target = link.get('source') if isinstance(link, dict) else None
      if isinstance(target, str) and target not in documents:
        tree = tree_dir / f'{target}.yaml'
        if tree.exists():
          documents[target] = load_yaml(tree)

  # The raw records as `material.source_year` reads a loaded `Source`.
  years = {
    key: material.source_year(
      types.SimpleNamespace(
        in_preparation=source.get('inPrep', False),
        year=(source.get('pubDate') or {}).get('year'),
      )
    )
    for key, source in sources.items()
  }
  return [
    (level, message)
    for level, message in material.same_as_links(documents, years.get)
    if message.startswith(f'{key} at ')
  ]


def main(argv):
  parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
  parser.add_argument('draft', type=pathlib.Path, help='the tree file to check')
  parser.add_argument(
    '--data',
    type=pathlib.Path,
    default=DATA_DIR,
    help='the directory of record files and trees to check against (default: data/)',
  )
  args = parser.parse_args(argv)
  path = args.draft
  data_dir = args.data
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
  taxa, authors, sources, sections = set(), set(), {path.stem}, set()
  walk(draft, taxa, authors, sources, sections)
  records = load_yaml(data_dir / 'taxa.yaml')
  source_records = load_yaml(data_dir / 'sources.yaml')
  known = {
    'taxa': set(records),
    'authors': set(load_yaml(data_dir / 'authors.yaml')),
    'sources': set(source_records),
    'sections': set(load_yaml(data_dir / 'sections.yaml')),
  }
  for label, cited in (
    ('taxa', taxa),
    ('authors', authors),
    ('sources', sources),
    ('sections', sections),
  ):
    missing = sorted(cited - known[label])
    print(f'{label}: {len(cited)} cited, {len(missing)} without a record')
    for key in missing:
      print(f'  {key}')

  repositories = load_yaml(data_dir / 'repositories.yaml')
  messages = check_material(draft, repositories, nomenclature.record_lookup(records))
  messages.extend(check_same_as(path.stem, draft, source_records, data_dir / 'trees'))

  for level, message in messages:
    print(f'{level}: {message}')
    if level == 'error':
      status = 1

  return status


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
