"""What the test modules share and the fixtures do not hand out: one
compiled schema, the scripts as modules, and `scripts/check_draft.py` run
in this process.

Every module that checked a document against the schema used to build the
schema afresh for each check, and every check of a draft started an
interpreter that parsed `data/` again; the suite spent most of its time
there.
"""

import contextlib
import functools
import importlib.util
import io as stdio
import logging
import pathlib
import types

from phylohist.loader import io

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / 'scripts'

_schema = None


def schema():
  """The phylogeny schema, built once for the session (`io.Schema`)."""
  global _schema
  if _schema is None:
    _schema = io.build_schema()
  return _schema


_scripts = {}


def script(name):
  """`scripts/<name>.py` as a module, loaded by path once."""
  if name not in _scripts:
    spec = importlib.util.spec_from_file_location(f'{name}_script', SCRIPTS / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _scripts[name] = module
  return _scripts[name]


def run_check_draft(path, data_dir=io.DATA_DIR):
  """`scripts/check_draft.py <path> --data <data_dir>` run in this process
  with the session's schema and libyaml: the exit status, what it printed,
  and what the loader logged at WARNING or above, named as a subprocess
  result names them (`returncode`, `stdout`, `stderr`)."""
  module = script('check_draft')
  module.build_schema = schema
  module.load_yaml = functools.partial(io.load_yaml, fast=True)
  out, err = stdio.StringIO(), stdio.StringIO()
  handler = logging.StreamHandler(err)
  handler.setLevel(logging.WARNING)
  logger = logging.getLogger('phylohist')
  logger.addHandler(handler)
  try:
    with contextlib.redirect_stdout(out):
      status = module.main([str(path), '--data', str(data_dir)])
  finally:
    logger.removeHandler(handler)
  return types.SimpleNamespace(returncode=status, stdout=out.getvalue(), stderr=err.getvalue())
