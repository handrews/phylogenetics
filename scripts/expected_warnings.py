#!/usr/bin/env python3
"""Keep `tests/expected-warnings.txt` to the warnings the data still produces.

    poetry run python scripts/expected_warnings.py          # drop the stale lines
    poetry run python scripts/expected_warnings.py --add    # and add the new ones

The file lists the WARNING-level messages the load of `data/` is expected
to produce, and `tests/test_load.py` fails on a message that is not in it.
Every line is a resolution owed, so resolving one should cost nothing:
`poetry run regenerate` drops every line the load no longer produces
(`scripts/claims.py` does so from the load it makes for the claim table).
A new warning is allowed only in a commit that adds a check, so a new line
is added only on request, with `--add`, which is what this script is for.
Nothing is written when the load logs an error, and the exit status is then 1.
"""

import argparse
import logging
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from phylohist.loader import LoadError, collecting, load  # noqa: E402
from phylohist.regenerate import EXPECTED_WARNINGS, prune_expected  # noqa: E402

# Under the package logger, whose handler prints the record; __name__ is __main__ here.
logger = logging.getLogger('phylohist.scripts.expected_warnings')


def produced():
  """``(warnings, errors)``: the WARNING messages the load of `data/` logs,
  and how many errors it logs (or raises for)."""
  failure = None
  with collecting() as logged:
    try:
      load(tolerate=True)
    except LoadError as error:
      failure = error
  if failure:
    logger.error(str(failure))
    return set(), 1
  return logged.warnings, len(logged.errors)


def main(argv):
  parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
  parser.add_argument('--add', action='store_true', help='also add the warnings the file lacks')
  parser.add_argument(
    '--file', type=pathlib.Path, default=EXPECTED_WARNINGS, help=argparse.SUPPRESS
  )
  args = parser.parse_args(argv)

  actual, errors = produced()
  if errors:
    logger.error(f'{errors} errors while loading; {args.file.name} is left as it is')
    return 1
  stale, new = prune_expected(actual, args.file, add=args.add)
  print(f'{len(stale)} stale expected warnings removed from {args.file.name}')
  if new:
    print(
      f'{len(new)} new warnings ' + ('added' if args.add else 'not expected; add them with --add')
    )
  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
