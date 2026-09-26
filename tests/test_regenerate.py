"""`regenerate` rewrites every derived file and reports any step that failed."""

import pathlib
import subprocess
import sys

from phylohist import regenerate


def _fake_run(calls, failing=None):
  def run(command):
    calls.append(command)
    status = 1 if failing and pathlib.Path(command[1]).name == failing else 0
    return subprocess.CompletedProcess(command, status)

  return run


def test_regenerate_runs_both_generators(monkeypatch):
  calls = []
  monkeypatch.setattr(regenerate.subprocess, 'run', _fake_run(calls))
  assert regenerate.main() == 0
  assert [c[0] for c in calls] == [sys.executable, sys.executable]
  assert [pathlib.Path(c[1]).name for c in calls] == ['claims.py', 'schema_audit.py']
  assert calls[1][2:] == ['--markdown', str(regenerate.SCRIPTS / 'schema-usage.md')]


def test_regenerate_runs_every_step_when_one_fails(monkeypatch):
  calls = []
  monkeypatch.setattr(regenerate.subprocess, 'run', _fake_run(calls, failing='claims.py'))
  assert regenerate.main() == 1
  assert len(calls) == 2
