#!/usr/bin/env python3
"""Regenerate the claim table and its coverage manifest.

    poetry run python scripts/claims.py                # -> claims/
    poetry run python scripts/claims.py --source 1962_fay 1983_holloway_jell
    poetry run python scripts/claims.py --draft --out /tmp/claims-with-drafts

Writes one `<source>.jsonl` per tree file, one claim per line, and
`manifest.json`; `docs/claims.md` defines both. CI reruns the script and
fails if `claims/` changes, so every data commit regenerates it.
`--draft` also loads `drafts/` and therefore refuses to write into the
committed directory.
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


def main(argv):
  parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
  parser.add_argument('--out', type=pathlib.Path, default=DEFAULT_OUT)
  parser.add_argument('--source', nargs='+', help='only these source keys')
  parser.add_argument(
    '--draft', action='store_true', help='also load the trees in drafts/',
  )
  args = parser.parse_args(argv)

  out = args.out.resolve()
  if args.draft and out == DEFAULT_OUT.resolve():
    parser.error('--draft needs --out pointing outside claims/')

  logging.basicConfig(level=logging.WARNING)
  _, roots = load(drafts=args.draft)
  claims_by_source = extract(roots, sources=set(args.source or ()) or None)
  full = args.source is None
  write(out, claims_by_source, full)

  total = sum(len(c) for c in claims_by_source.values())
  print(f'{total} claims from {len(claims_by_source)} sources -> {out}')
  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
