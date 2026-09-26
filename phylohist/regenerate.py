"""Regenerate the files derived from the data: the claim table under
`claims/` and the schema census `scripts/schema-usage.md`.

    poetry run regenerate

CI fails when either is stale, so run this after any change to `data/`
or the schema. Every step runs even when one before it fails, and the
exit status is 1 if any failed.
"""

import subprocess
import sys

from .loader.io import FILEDIR

SCRIPTS = FILEDIR / 'scripts'
STEPS = (
  ('claims.py',),
  ('schema_audit.py', '--markdown', str(SCRIPTS / 'schema-usage.md')),
)


def main():
  statuses = [
    subprocess.run([sys.executable, str(SCRIPTS / script), *args]).returncode
    for script, *args in STEPS
  ]
  return 1 if any(statuses) else 0
