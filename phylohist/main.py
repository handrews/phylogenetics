import sys
import pathlib
import logging
import collections

import yaml
import jschon

from .io import load_files
from .check import check_authors, check_sources, check_taxa, check_trees
from .convert import convert

logger = logging.getLogger(__name__)

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

  # TODO: Obviously this is fragile, fix it!
  handler = logger.parent.handlers[0]
  logged_errors = handler.get_count(logging.ERROR)
  logged_warnings = handler.get_count(logging.WARN)
  if logged_errors:
    logger.error(
      f'Encounterd {logged_errors} errors ({logged_warnings} warnings)!'
    )
    sys.exit(-1)
  elif logged_warnings:
    logger.warn(f'Encountered {logged_warnings} warnings.')
  else:
    logger.info(f'Success!')
