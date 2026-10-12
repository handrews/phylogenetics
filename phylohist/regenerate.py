"""Regenerate the files derived from the data: the claim table under
`claims/` and the schema census `scripts/schema-usage.md`, and keep
`tests/expected-warnings.txt` to the warnings the load still produces.

    poetry run regenerate

CI fails when any of them is stale, so run this after any change to
`data/` or the schema. Every step runs even when one before it fails, and
the exit status is 1 if any failed. `scripts/claims.py` prunes the
expected warnings from the load it makes for the claim table, so the data
loads once; a new warning is added only with
`scripts/expected_warnings.py --add`, since a new line is allowed only in
a commit that adds a check.
"""

import subprocess
import sys

from .loader.io import FILEDIR

SCRIPTS = FILEDIR / 'scripts'
STEPS = (
  ('claims.py',),
  ('schema_audit.py', '--markdown', str(SCRIPTS / 'schema-usage.md')),
)

EXPECTED_WARNINGS = FILEDIR / 'tests' / 'expected-warnings.txt'

EXPECTED_HEADER = """\
# Expected WARNING-level messages from loading all data files.
# A new line here is allowed only in a commit that adds a check; every line
# is a resolution owed. `poetry run regenerate` drops the lines no longer
# produced; `poetry run python scripts/expected_warnings.py --add` adds new ones.
"""


def read_expected(path=EXPECTED_WARNINGS):
  """The messages the file lists, without its comments and blank lines."""
  if not path.exists():
    return set()
  return {
    line.strip()
    for line in path.read_text().splitlines()
    if line.strip() and not line.startswith('#')
  }


def write_expected(messages, path=EXPECTED_WARNINGS):
  path.write_text(EXPECTED_HEADER + ''.join(f'{message}\n' for message in sorted(messages)))


def prune_expected(produced, path=EXPECTED_WARNINGS, add=False):
  """Rewrite the file to the lines the load still produces, adding the ones
  it did not list only with ``add``; ``(stale, new)``, the lines dropped and
  the warnings the file lacked."""
  expected = read_expected(path)
  stale = expected - produced
  new = produced - expected
  write_expected((expected - stale) | (new if add else set()), path)
  return stale, new


def main():
  statuses = [
    subprocess.run([sys.executable, str(SCRIPTS / script), *args]).returncode
    for script, *args in STEPS
  ]
  return 1 if any(statuses) else 0
