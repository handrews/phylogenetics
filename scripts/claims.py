#!/usr/bin/env python3
"""Regenerate the claim table and its coverage manifest.

    poetry run python scripts/claims.py                # -> claims/
    poetry run python scripts/claims.py --source 1962_fay 1983_holloway_jell
    poetry run python scripts/claims.py --draft --out /tmp/claims-with-drafts
    poetry run python scripts/claims.py --inconsistencies
    poetry run python scripts/claims.py --errors-only

Writes one `<source>.jsonl` per tree file, one claim per line,
`manifest.json`, `names.json` and `repositories.json`; `docs/claims.md`
defines all four. CI reruns the script and
fails if `claims/` changes, so every data commit regenerates it.
`--draft` also loads `drafts/` and therefore refuses to write into the
committed directory. `--inconsistencies` writes nothing: it prints each
source whose declared coverage disagrees with the derived claims, with
the claims behind the disagreement, for the owner to settle either way,
and exits 1 when there are any; `tests/test_claims.py` fails on the same
rows, so CI catches a new one. It then lists the taxa whose holotype is a
different specimen in two sources (roadmap F5), a report that neither
counts towards that exit status nor fails a test. `--errors-only` holds the
load's log until it ends, then shows only its errors when there are any
and its warnings otherwise, so that the errors are not lost among them.
"""

import argparse
import contextlib
import json
import logging
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from phylohist.claims import extract, manifest, names_index  # noqa: E402
from phylohist.loader import LoadError, counting_errors, load  # noqa: E402
from phylohist.loader.material import repository_registry  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / 'claims'


# The registry fields `repositories.json` keeps.
_REPOSITORY_FIELDS = ('name', 'type', 'subject', 'within', 'prefixes', 'otherNames', 'place')


def _repositories():
  """The loaded registry for `claims/repositories.json`: the fields the
  store reads, as present."""
  return {
    key: {field: entry[field] for field in _REPOSITORY_FIELDS if field in entry}
    for key, entry in sorted(repository_registry().items())
  }


def write(out, claims_by_source, roots, full):
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
    for name, content in (
      ('manifest.json', manifest(claims_by_source, roots)),
      ('names.json', names_index()),
      ('repositories.json', _repositories()),
    ):
      with open(out / name, 'w') as fd:
        json.dump(content, fd, ensure_ascii=False, indent=1, sort_keys=True)
        fd.write('\n')


# Which tree fields a coverage kind is counted from, for the report.
_KIND_SOURCES = {
  'skeleton': 'taxon/openTaxon nodes and their children',
  'newTaxa': '`new: true`',
  'types': '`isType: true` or a `type` node',
  'synonymy': '`synonyms` and `non` entries',
  'material': '`material` entries',
  'occurrences': '`contexts` and `ranges`',
  'illustrations': '`illustrations` on a primary node (not on a synonymy line)',
  'phylogeny': 'children in a phylogeny',
}


def _describe(claim):
  printed = claim.get('printed') or {}
  detail = printed.get('citedAs') or ' '.join(
    ', '.join(printed[f]) if f == 'auth' else str(printed[f])
    for f in ('auth', 'year')
    if f in printed
  )
  extra = ''
  if claim['kind'] == 'act':
    extra = f' {claim["actKind"]}'
  if claim['kind'] == 'acceptance' and claim.get('parents'):
    extra = f' parents={claim["parents"]}'
  if claim['kind'] == 'material':
    extra = f' {claim["materialKind"]}'
    if 'role' in claim:
      extra += f' {claim["role"]} {claim.get("ids")}'
  return (
    f'{claim["kind"]:<11} {claim["subject"]}{extra}'
    + (f'  "{detail}"' if detail else '')
    + f'  @ {claim["path"]}'
  )


def _describe_holotype(holotype):
  """A source and the catalog numbers it prints for the holotype (a range
  pair as "a–b"), else its label."""
  numbers = [n if isinstance(n, str) else '–'.join(n) for n in holotype['ids']]
  return f'{holotype["source"]} {", ".join(numbers) or holotype.get("label", "(unnumbered)")}'


def report_inconsistencies(claims_by_source, roots):
  """Explain each declared-versus-derived disagreement.

  The declared side is the audit block in data/sources.yaml; the derived
  side is the claims the tree yields, editor-inferred ones excluded. The
  report names both, and lists the inferred claims so that "no claims
  derived" beside an obviously flagged node is not a mystery.
  """
  report = manifest(claims_by_source, roots)
  rows = report['sources']
  found = 0
  for source_key, entry in rows.items():
    if not entry['inconsistencies']:
      continue
    found += 1
    review = ROOT / 'notes' / 'reviews' / f'review_{source_key}.md'
    print(source_key + (f'  ({review.relative_to(ROOT)})' if review.exists() else ''))
    for row in entry['inconsistencies']:
      kind, _, rest = row.partition(':')
      declared = entry['audit'].get('coverage', {}).get(kind)
      where = f'in data/sources.yaml ({source_key}.audit.coverage.{kind})'
      if ' but derived from the tree' in rest:
        # The tree's nulls derive the kind: the declaration goes, and there
        # are no claim counts to weigh it against.
        print(f'  {kind}: declared {declared} {where} but{rest.split(" but", 1)[1]}')
        continue
      print(f'  {kind}: declared {declared} {where};{rest.split(",", 1)[1]}')
      counted = [
        c
        for c in claims_by_source.get(source_key, ())
        if c['audit'].get('coverageKind') == kind and not c.get('inferred')
      ]
      inferred = [
        c
        for c in claims_by_source.get(source_key, ())
        if c['audit'].get('coverageKind') == kind and c.get('inferred')
      ]
      if counted:
        print(f'    derived from the tree ({_KIND_SOURCES[kind]}):')
        for claim in counted:
          print('      ' + _describe(claim))
      else:
        print(
          f'    nothing in data/trees/{source_key}.yaml yields a countable '
          f'claim of this kind ({_KIND_SOURCES[kind]})'
        )
      if inferred:
        print("    editor-inferred, so not counted as the paper's:")
        for claim in inferred:
          basis = (claim.get('editorial') or {}).get('basis', '')
          print('      ' + _describe(claim) + (f'  basis: {basis.strip()}' if basis else ''))
      if declared in ('all', 'partly') and not counted:
        print(
          f'    to resolve: enter what the paper prints, or declare '
          f'{"na" if not inferred else "na (the paper prints none; the editor inferred it)"} '
          f'or none'
        )
      elif declared in ('none', 'na') and counted:
        print(
          '    to resolve: declare partly or all, or remove the entries if '
          'they are not what the paper prints'
        )
  print(f'{found} sources with inconsistencies')
  if report['holotypeConflicts']:
    print('holotypes that differ between sources:')
    for row in report['holotypeConflicts']:
      print(f'  {row["taxon"]}: ' + '; '.join(_describe_holotype(h) for h in row['holotypes']))
  return found


class _Held(logging.Handler):
  """Keeps the records of WARNING and above instead of letting them print;
  `replay` prints the errors alone when there are any, else every one.
  (Not `release`: `logging.Handler` uses that name for its lock.)"""

  def __init__(self):
    super().__init__(level=logging.WARNING)
    self.records = []

  def emit(self, record):
    self.records.append(record)

  def replay(self, logger):
    errors = [r for r in self.records if r.levelno >= logging.ERROR]
    for record in errors or self.records:
      logger.callHandlers(record)


@contextlib.contextmanager
def _holding(enabled):
  """A block whose log records are shown, on leaving it, as `--errors-only`
  asks. The package logger prints its own records (every INFO line too)
  and passes them to the root; while it holds, only the holder sees them."""
  if not enabled:
    yield
    return
  package = logging.getLogger('phylohist')
  printing = package.handlers[:]
  held = _Held()
  package.handlers[:] = [held]
  package.propagate = False
  try:
    yield
  finally:
    package.handlers[:] = printing
    package.propagate = True
    held.replay(package)


def main(argv):
  parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
  parser.add_argument('--out', type=pathlib.Path, default=DEFAULT_OUT)
  parser.add_argument('--source', nargs='+', help='only these source keys')
  parser.add_argument(
    '--draft',
    action='store_true',
    help='also load the trees in drafts/',
  )
  parser.add_argument(
    '--inconsistencies',
    action='store_true',
    help='print declared-versus-derived coverage disagreements; write nothing',
  )
  parser.add_argument(
    '--tolerate',
    action='store_true',
    help='write the claims even when the load logs integrity errors; the exit status is still 1',
  )
  parser.add_argument(
    '--errors-only',
    action='store_true',
    help='show only the load errors when there are any, else its warnings',
  )
  args = parser.parse_args(argv)

  out = args.out.resolve()
  if args.draft and out == DEFAULT_OUT.resolve():
    parser.error('--draft needs --out pointing outside claims/')

  # The package logger prints its own records (phylohist/__init__.py); a
  # root handler would print each of them a second time.
  failure = None
  with _holding(args.errors_only), counting_errors() as errors:
    try:
      _, roots = load(drafts=args.draft, tolerate=args.tolerate)
    except LoadError as exc:
      failure = exc
  if failure:
    print(f'error: {failure}', file=sys.stderr)
    return 1
  claims_by_source = extract(roots, sources=set(args.source or ()) or None)
  if args.inconsistencies:
    return 1 if report_inconsistencies(claims_by_source, roots) else 0
  full = args.source is None
  write(out, claims_by_source, roots, full)

  total = sum(len(c) for c in claims_by_source.values())
  print(f'{total} claims from {len(claims_by_source)} sources -> {out}')
  if errors.count:
    print(f'{errors.count} integrity errors while loading (tolerated)', file=sys.stderr)
    return 1
  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
