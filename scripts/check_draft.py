"""Check an AI-drafted tree file before a human audit.

    poetry run python scripts/check_draft.py drafts/1891_bell.f.j.yaml

Validates the draft against the tree schema the loader uses, then lists the
taxon keys, author keys and source keys the draft cites that have no record
yet. Exit status 1 on a schema failure, 0 otherwise; the unresolved lists are
always printed, since a draft normally needs new records.
"""

import pathlib
import sys

import jschon

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from phylohist.io import (  # noqa: E402
  DATA_DIR, FILEDIR, ensure_catalog, load_yaml, log_schema_errors,
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
    if isinstance(editorial, dict) and isinstance(editorial.get('source'), str):
      sources.add(editorial['source'])
    for value in node.values():
      walk(value, taxa, authors, sources)
  elif isinstance(node, list):
    for value in node:
      walk(value, taxa, authors, sources)


def main(argv):
  if len(argv) != 2:
    print(__doc__)
    return 2
  path = pathlib.Path(argv[1])
  ensure_catalog()
  schema = jschon.JSONSchema(load_yaml(FILEDIR / 'schemas' / 'phylogeny.yaml'))
  draft = load_yaml(path)
  result = schema['$defs']['trees'].evaluate(jschon.JSON({path.stem: draft}))
  if not result.valid:
    print(f'{path}: not valid against the tree schema')
    log_schema_errors(result)
    status = 1
  else:
    print(f'{path}: valid against the tree schema')
    status = 0

  taxa, authors, sources = set(), set(), set()
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
  return status


if __name__ == '__main__':
  sys.exit(main(sys.argv))
