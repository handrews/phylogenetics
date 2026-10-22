"""What the test modules share and the fixtures do not hand out: one
compiled schema, the scripts as modules, `scripts/check_draft.py` run in
this process, and a corpus holding a test's own documents.

Every module that checked a document against the schema used to build the
schema afresh for each check, and every check of a draft started an
interpreter that parsed `data/` again; the suite spent most of its time
there.
"""

import contextlib
import functools
import importlib.util
import io as stdio
import pathlib
import types

from phylohist.loader import collecting, io

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / 'scripts'
CORPUS = ROOT / 'tests' / 'corpus'

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


def run_check_draft(path, data_dir=CORPUS):
  """`scripts/check_draft.py <path> --data <data_dir>` run in this process
  with the session's schema and libyaml: the exit status, what it printed,
  and what the loader logged at WARNING or above, named as a subprocess
  result names them (`returncode`, `stdout`, `stderr`)."""
  module = script('check_draft')
  module.build_schema = schema
  module.load_yaml = functools.partial(io.load_yaml, fast=True)
  out = stdio.StringIO()
  with collecting() as logged, contextlib.redirect_stdout(out):
    status = module.main([str(path), '--data', str(data_dir)])
  stderr = ''.join(f'{r.getMessage()}\n' for r in logged.records)
  return types.SimpleNamespace(returncode=status, stdout=out.getvalue(), stderr=stderr)


# -- a corpus over a test's documents -----------------------------------------


def with_documents(corpus, data=None, roots=None):
  """A copy of `corpus` holding the documents `data` and the trees `roots`
  in place of its own (none by default), and only the repositories `data`
  gives: what a loader `_report_*` or `_load_*` reads, run over a few
  synthetic documents. The records are the corpus's, so a tree built
  against it resolves the same objects."""
  view = corpus.copy()
  view.data, view.roots = data or {}, roots or {}
  view.repositories = dict(view.data.get('repositories') or {})
  return view


def footprint(corpus):
  """The size of each registry and the identity of `data` and `roots`: what
  a test must leave as it found it on the session corpus."""
  return (
    len(corpus.authors),
    len(corpus.publications),
    len(corpus.sources),
    len(corpus.taxa),
    len(corpus.sections),
    id(corpus.data),
    id(corpus.roots),
  )
