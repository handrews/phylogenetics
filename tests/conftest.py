"""The one in-process load every test module shares.

`Taxon` and `Tree` keep class-level registries, so the data must be loaded
once per process; the fixture returns the loaded data, the log records the
load produced, and the tree roots per source.
"""

import logging
import os

import pytest

from phylohist.load import load


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
