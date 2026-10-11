"""What the test modules share and the fixtures do not hand out: one
compiled schema, the scripts as modules, `scripts/check_draft.py` run in
this process, and the registries copied and restored.

Every module that checked a document against the schema used to build the
schema afresh for each check, and every check of a draft started an
interpreter that parsed `data/` again; the suite spent most of its time
there.
"""

import collections
import contextlib
import functools
import importlib.util
import io as stdio
import logging
import pathlib
import types

from phylohist import claims
from phylohist.loader import io, material
from phylohist.loader.research import Author, Publication, Source
from phylohist.loader.taxa import Section, Taxon, Tree

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


# -- the registries -----------------------------------------------------------

# The class-level registries a load fills and a synthetic tree writes to:
# the record classes' dicts, and the `Tree` indexes of sets.
_RECORDS = (
  (Author, '_authors'),
  (Publication, '_publications'),
  (Source, '_sources'),
  (Taxon, '_taxa'),
  (Section, '_sections'),
)
_INDEXES = ('_taxon_index', '_new_index', '_author_index')


def snapshot():
  """A copy of every registry as it stands: the record dicts, the `Tree`
  indexes with their sets, and the repository registry."""
  return {
    'records': {name: dict(getattr(owner, name)) for owner, name in _RECORDS},
    'indexes': {
      name: {key: set(value) for key, value in getattr(Tree, name).items()} for name in _INDEXES
    },
    'types': {key: set(value) for key, value in Tree._type_index.items()},
    'repositories': dict(material.repository_registry()),
  }


def restore(snap):
  """Rebind every registry to a fresh copy of `snap`, so that what a test
  added (a `Taxon.add`, a `Tree`) is gone before the next one; the rank
  hubs `claims` derives from the taxa are dropped with them."""
  for owner, name in _RECORDS:
    setattr(owner, name, dict(snap['records'][name]))
  for name in _INDEXES:
    index = collections.defaultdict(set)
    for key, value in snap['indexes'][name].items():
      index[key] = set(value)
    setattr(Tree, name, index)
  Tree._type_index = {key: set(value) for key, value in snap['types'].items()}
  material.set_repository_registry(snap['repositories'])
  claims._rank_hubs = None


def reset():
  """Empty every registry, as a process that has loaded nothing has them."""
  restore(
    {
      'records': {name: {} for _, name in _RECORDS},
      'indexes': {name: {} for name in _INDEXES},
      'types': {key: set() for key in Tree._type_index},
      'repositories': {},
    }
  )
