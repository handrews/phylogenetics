"""Loads all data files in-process and checks the logs they produce.

Fails on any ERROR-level log record. Compares WARNING-level messages against
``tests/expected-warnings.txt``: a new line there is allowed only in a commit
that adds a check, and every line is a resolution owed. Regenerate with
``PHYLOHIST_UPDATE_EXPECTED=1 poetry run pytest``. The load itself is the
session fixture in ``conftest.py``.

``PHYLOHIST_DRAFTS=1`` also loads the unaudited trees under ``drafts/``
(the CLI's ``--draft``). Drafts are expected to produce errors and
warnings until their records exist, so the warning snapshot is not
compared in that mode; the error test still reports what a draft needs.
"""

import logging
import os
import pathlib

import pytest

EXPECTED_WARNINGS_PATH = pathlib.Path(__file__).parent / 'expected-warnings.txt'

EXPECTED_WARNINGS_HEADER = """\
# Expected WARNING-level messages from loading all data files.
# A new line here is allowed only in a commit that adds a check; every line
# is a resolution owed. Regenerate with:
#   PHYLOHIST_UPDATE_EXPECTED=1 poetry run pytest
"""


def test_no_errors(load_records):
  _, records, _ = load_records
  errors = [r for r in records if r.levelno >= logging.ERROR]
  if errors:
    message = '\n'.join(r.getMessage() for r in errors)
    pytest.fail(f'{len(errors)} ERROR-level log records:\n{message}')


def test_data_loaded(load_records):
  data, _, _ = load_records
  assert data['trees'], 'load produced no trees; check for a silent empty load'


def test_expected_warnings(load_records):
  if os.getenv('PHYLOHIST_DRAFTS'):
    pytest.skip('drafts loaded; the warning snapshot covers data/ only')
  _, records, _ = load_records
  actual = sorted({
    r.getMessage() for r in records if r.levelno == logging.WARNING
  })

  if os.getenv('PHYLOHIST_UPDATE_EXPECTED'):
    with open(EXPECTED_WARNINGS_PATH, 'w') as fd:
      fd.write(EXPECTED_WARNINGS_HEADER)
      for message in actual:
        fd.write(f'{message}\n')
    return

  expected = set()
  if EXPECTED_WARNINGS_PATH.exists():
    with open(EXPECTED_WARNINGS_PATH) as fd:
      for line in fd:
        line = line.strip()
        if not line or line.startswith('#'):
          continue
        expected.add(line)

  actual_set = set(actual)
  unexpected = actual_set - expected
  stale = expected - actual_set

  if unexpected or stale:
    parts = []
    if unexpected:
      parts.append(
        'Unexpected warnings (not in tests/expected-warnings.txt):\n' +
        '\n'.join(sorted(unexpected)),
      )
    if stale:
      parts.append(
        'Stale expected warnings (no longer produced):\n' +
        '\n'.join(sorted(stale)),
      )
    pytest.fail('\n\n'.join(parts))
