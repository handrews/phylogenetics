import sys
import pathlib
import logging
import collections

import yaml
import jschon

from .io import load_files
from .check import check_authors, check_sources, check_taxa, check_trees
from .convert import convert

from . import logger

schema_catalog = jschon.create_catalog('2020-12')
"""The default shared ``jschon`` schema loader and cache"""


def main():
  if len(sys.argv) > 1 and sys.argv[1] == 'convert':
    return convert()

  data = load_files()
  check_authors(data)
  sources = check_sources(data)
  check_taxa(data)
  check_trees(data, sources)

#   logged_errors = log_counter.get_counts()[logging.ERROR]
#   if logged_errors:
  logged_errors = logger.error_count
  logged_warnings = logger.warn_count
  print()
  if logged_errors:
    logger.error(
      f'Encounterd {logged_errors} errors ({logged_warnings} warnings)!'
    )
    sys.exit(-1)
  elif logged_warnings:
    logger.warn(f'Encountered {logged_warnings} warnings.')
  else:
    logger.info(f'Success!')
