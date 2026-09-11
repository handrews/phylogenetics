#!/usr/bin/env python3
"""Regenerate the claim table and its coverage manifest.

    poetry run python scripts/claims.py                # -> claims/
    poetry run python scripts/claims.py --source 1962_fay 1983_holloway_jell
    poetry run python scripts/claims.py --draft --out /tmp/claims-with-drafts
    poetry run python scripts/claims.py --inconsistencies

Writes one `<source>.jsonl` per tree file, one claim per line, and
`manifest.json`; `docs/claims.md` defines both. CI reruns the script and
fails if `claims/` changes, so every data commit regenerates it.
`--draft` also loads `drafts/` and therefore refuses to write into the
committed directory. `--inconsistencies` writes nothing: it prints each
source whose declared coverage disagrees with the derived claims, with
the claims behind the disagreement, for the owner to settle either way,
and exits 1 when there are any; `tests/test_claims.py` fails on the same
rows, so CI catches a new one.
"""

import argparse
import json
import logging
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from phylohist.claims import extract, manifest  # noqa: E402
from phylohist.io import load_files  # noqa: E402
from phylohist.main import _basic_load, _load_taxa, _load_trees  # noqa: E402
from phylohist.research import Author, Publication, Source  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / 'claims'


def load(drafts=False):
  data = load_files(drafts=drafts)
  for field, cls in (
    ('authors', Author),
    ('publications', Publication),
    ('sources', Source),
  ):
    _basic_load(data, field, cls)
  _load_taxa(data)
  return data, _load_trees(data)


def write(out, claims_by_source, full):
  out.mkdir(parents=True, exist_ok=True)
  if full:
    for stale in out.glob('*.jsonl'):
      stale.unlink()
  for source_key, claims in claims_by_source.items():
    with open(out / f'{source_key}.jsonl', 'w') as fd:
      for claim in claims:
        fd.write(json.dumps(claim, ensure_ascii=False, sort_keys=True))
        fd.write('\n')
  if full:
    with open(out / 'manifest.json', 'w') as fd:
      json.dump(
        manifest(claims_by_source), fd, ensure_ascii=False, indent=1,
        sort_keys=True,
      )
      fd.write('\n')


# Which tree fields a coverage kind is counted from, for the report.
_KIND_SOURCES = {
  'skeleton': 'taxon/openTaxon/cfTaxon/affTaxon nodes and their children',
  'newTaxa': '`new: true`',
  'types': '`type: true`',
  'synonymy': '`synonyms` and `non` entries',
  'material': '`specimens` (on a node or inside an occurrence)',
  'occurrences': '`occurrences`',
  'illustrations': '`illustrations` on a node (not on a synonymy line)',
  'diagnoses': '`diagnosis`',
  'phylogeny': 'children in a phylogeny',
}


def _describe(claim):
  printed = claim.get('printed') or {}
  detail = printed.get('citedAs') or ' '.join(
    ', '.join(printed[f]) if f == 'auth' else str(printed[f])
    for f in ('auth', 'year') if f in printed
  )
  extra = ''
  if claim['kind'] == 'act':
    extra = f" {claim['actKind']}"
  if claim['kind'] == 'acceptance' and claim.get('parents'):
    extra = f" parents={claim['parents']}"
  if claim['kind'] == 'material':
    extra = f" {claim['materialKind']}"
    if 'role' in claim:
      extra += f" {claim['role']} {claim.get('ids')}"
  return (
    f"{claim['kind']:<11} {claim['subject']}{extra}"
    + (f'  "{detail}"' if detail else '') + f"  @ {claim['path']}"
  )


def report_inconsistencies(claims_by_source):
  """Explain each declared-versus-derived disagreement.

  The declared side is the audit block in data/sources.yaml; the derived
  side is the claims the tree yields, editor-inferred ones excluded. The
  report names both, and lists the inferred claims so that "no claims
  derived" beside an obviously flagged node is not a mystery.
  """
  rows = manifest(claims_by_source)['sources']
  found = 0
  for source_key, entry in rows.items():
    if not entry['inconsistencies']:
      continue
    found += 1
    review = ROOT / 'docs' / 'reviews' / f'review_{source_key}.md'
    print(source_key + (f'  ({review.relative_to(ROOT)})' if review.exists() else ''))
    for row in entry['inconsistencies']:
      kind, _, rest = row.partition(':')
      declared = entry['audit'].get('coverage', {}).get(kind)
      print(f'  {kind}: declared {declared} in data/sources.yaml '
            f'({source_key}.audit.coverage.{kind});{rest.split(",", 1)[1]}')
      counted = [
        c for c in claims_by_source.get(source_key, ())
        if c['audit'].get('coverageKind') == kind and not c.get('inferred')
      ]
      inferred = [
        c for c in claims_by_source.get(source_key, ())
        if c['audit'].get('coverageKind') == kind and c.get('inferred')
      ]
      if counted:
        print(f'    derived from the tree ({_KIND_SOURCES[kind]}):')
        for claim in counted:
          print('      ' + _describe(claim))
      else:
        print(f'    nothing in data/trees/{source_key}.yaml yields a countable '
              f'claim of this kind ({_KIND_SOURCES[kind]})')
      if inferred:
        print('    editor-inferred, so not counted as the paper\'s:')
        for claim in inferred:
          basis = (claim.get('editorial') or {}).get('basis', '')
          print('      ' + _describe(claim) + (f'  basis: {basis.strip()}' if basis else ''))
      if declared in ('all', 'partly') and not counted:
        print(f'    to resolve: enter what the paper prints, or declare '
              f'{"na" if not inferred else "na (the paper prints none; the editor inferred it)"} '
              f'or none')
      elif declared in ('none', 'na') and counted:
        print('    to resolve: declare partly or all, or remove the entries if '
              'they are not what the paper prints')
  print(f'{found} sources with inconsistencies')
  return found


def main(argv):
  parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
  parser.add_argument('--out', type=pathlib.Path, default=DEFAULT_OUT)
  parser.add_argument('--source', nargs='+', help='only these source keys')
  parser.add_argument(
    '--draft', action='store_true', help='also load the trees in drafts/',
  )
  parser.add_argument(
    '--inconsistencies', action='store_true',
    help='print declared-versus-derived coverage disagreements; write nothing',
  )
  args = parser.parse_args(argv)

  out = args.out.resolve()
  if args.draft and out == DEFAULT_OUT.resolve():
    parser.error('--draft needs --out pointing outside claims/')

  logging.basicConfig(level=logging.WARNING)
  _, roots = load(drafts=args.draft)
  claims_by_source = extract(roots, sources=set(args.source or ()) or None)
  if args.inconsistencies:
    return 1 if report_inconsistencies(claims_by_source) else 0
  full = args.source is None
  write(out, claims_by_source, full)

  total = sum(len(c) for c in claims_by_source.values())
  print(f'{total} claims from {len(claims_by_source)} sources -> {out}')
  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
