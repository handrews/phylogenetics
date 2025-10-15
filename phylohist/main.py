import sys
import pathlib
import logging
import collections

import yaml
import jschon

from .io import load_files
from .check import check_authors, check_sources, check_data, check_trees

FUTURE = 2030

# AI code
class LevelCountHandler(logging.StreamHandler):
  """
  A custom logging handler that counts log messages by level.
  """
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.counts = collections.defaultdict(int)

  def emit(self, record):
    """
    Increments the count for the given log record's level.
    """
    self.counts[record.levelname] += 1

  def get_counts(self):
    """
    Returns a dictionary of log level counts.
    """
    return dict(self.counts)

LEVEL = logging.INFO
log_counter = LevelCountHandler()
log_counter.setLevel(LEVEL)
logger = logging.getLogger(__name__)
logger.setLevel(LEVEL)
logger.addHandler(log_counter)
logger.setLevel(LEVEL)

class L():
  error_count = 0
  warn_count = 0
  def error(self, message):
    self.error_count += 1
    if LEVEL <= logging.ERROR:
      print(f'*** ERROR: {message}')
  def warn(self, message):
    self.warn_count += 1
    if LEVEL <= logging.WARNING:
      print(f'*** WARNING: {message}')
  def info(self, message):
    if LEVEL <= logging.INFO:
      print(f'*** INFO: {message}')
  def debug(self, message):
    if LEVEL <= logging.DEBUG:
      print(f'*** DEBUG: {message}')

logger = L()
schema_catalog = jschon.create_catalog('2020-12')
"""The default shared ``jschon`` schema loader and cache"""


def main():

  data = load_files()
  check_authors(data)
  sources = check_sources(data)
  check_taxa(data)
  check_trees(data, sources)

#   logged_errors = log_counter.get_counts()[logging.ERROR]
#   if logged_errors:
  logged_errors = logger.error_count
  logged_warnings = logger.warn_count
  if logged_errors:
    logger.error(
      f'Encounterd {logged_errors} errors ({logged_warnings} warnings)!'
    )
    sys.exit(-1)
  elif logged_warnings:
    logger.warn(f'Encountered {logged_warnings} warnings.')
  else:
    logger.info(f'Success!')


if __name__ == '__main__':
  main()
