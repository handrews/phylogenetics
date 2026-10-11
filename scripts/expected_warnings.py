#!/usr/bin/env python3
"""Keep `tests/expected-warnings.txt` to the warnings the data still produces.

    poetry run python scripts/expected_warnings.py          # drop the stale lines
    poetry run python scripts/expected_warnings.py --add    # and add the new ones

The file lists the WARNING-level messages the load of `data/` is expected
to produce, and `tests/test_load.py` fails on a message that is not in it.
Every line is a resolution owed, so resolving one should cost nothing:
`poetry run regenerate` runs this script, which drops every line the load
no longer produces. A new warning is allowed only in a commit that adds a
check, so a new line is added only on request, with `--add`. Nothing is
written when the load logs an error, and the exit status is then 1.
"""

import argparse
import logging
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from phylohist.loader import LoadError, load  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXPECTED_PATH = ROOT / 'tests' / 'expected-warnings.txt'

HEADER = """\
# Expected WARNING-level messages from loading all data files.
# A new line here is allowed only in a commit that adds a check; every line
# is a resolution owed. `poetry run regenerate` drops the lines no longer
# produced; `poetry run python scripts/expected_warnings.py --add` adds new ones.
"""


class _Collecting(logging.Handler):
  """Keeps the WARNING and ERROR records of the load."""

  def __init__(self):
    super().__init__(level=logging.WARNING)
    self.records = []

  def emit(self, record):
    self.records.append(record)


def read_expected(path):
  """The messages the file lists, without its comments and blank lines."""
  if not path.exists():
    return set()
  return {
    line.strip()
    for line in path.read_text().splitlines()
    if line.strip() and not line.startswith('#')
  }


def produced():
  """``(warnings, errors)``: the WARNING messages the load of `data/` logs,
  and how many errors it logs (or raises for)."""
  handler = _Collecting()
  package = logging.getLogger('phylohist')
  package.addHandler(handler)
  try:
    load(tolerate=True)
  except LoadError as error:
    print(f'error: {error}', file=sys.stderr)
    return set(), 1
  finally:
    package.removeHandler(handler)
  warnings = {r.getMessage() for r in handler.records if r.levelno == logging.WARNING}
  errors = sum(1 for r in handler.records if r.levelno >= logging.ERROR)
  return warnings, errors


def write(path, messages):
  path.write_text(HEADER + ''.join(f'{message}\n' for message in sorted(messages)))


def main(argv):
  parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
  parser.add_argument('--add', action='store_true', help='also add the warnings the file lacks')
  parser.add_argument('--file', type=pathlib.Path, default=EXPECTED_PATH, help=argparse.SUPPRESS)
  args = parser.parse_args(argv)

  actual, errors = produced()
  if errors:
    print(f'{errors} errors while loading; {args.file.name} is left as it is', file=sys.stderr)
    return 1
  expected = read_expected(args.file)
  stale = expected - actual
  new = actual - expected
  write(args.file, (expected - stale) | (new if args.add else set()))
  print(f'{len(stale)} stale expected warnings removed from {args.file.name}')
  if new:
    print(
      f'{len(new)} new warnings ' + ('added' if args.add else 'not expected; add them with --add')
    )
  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
