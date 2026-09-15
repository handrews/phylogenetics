"""What every test module shares: one load of `data/`, one claim store.

`Taxon` and `Tree` keep class-level registries, so the data must be loaded
once per process; `load_records` returns the loaded data, the log records
the load produced, and the tree roots per source. `store` reads the
committed `claims/` once for every test over the tools, and `closure` is
its closure.
"""

import logging
import os

import pytest

from phylohist.closure import Closure
from phylohist.load import load
from phylohist.tools import ClaimStore


class _CollectingHandler(logging.Handler):
  def __init__(self):
    super().__init__()
    self.records = []

  def emit(self, record):
    self.records.append(record)


@pytest.fixture(scope='session')
def load_records():
  handler = _CollectingHandler()
  logger = logging.getLogger('phylohist')
  logger.addHandler(handler)
  try:
    data, roots = load(drafts=bool(os.getenv('PHYLOHIST_DRAFTS')))
  finally:
    logger.removeHandler(handler)

  return data, handler.records, roots


@pytest.fixture(scope='session')
def store():
  return ClaimStore()


@pytest.fixture(scope='session')
def closure(store):
  return Closure(store)
