import sys
import pathlib
import logging
import collections
import argparse

import yaml
import jschon

from .io import load_files
from .research import Author, Publication, Source
from .taxa import Taxon, check_trees
from .convert import convert

logger = logging.getLogger(__name__)

schema_catalog = jschon.create_catalog('2020-12')
"""The default shared ``jschon`` schema loader and cache"""


def main():
  parser = argparse.ArgumentParser(
    prog='phylohist',
  )
  parser.add_argument('-t', '--type', default='x')
  parser.add_argument('-r', '--root', nargs='+', action='extend', default=[])
  parser.add_argument('-l', '--leaf', nargs='+', action='extend', default=[])
  parser.add_argument('-b', '--branch', nargs='+', action='extend', default=[])
  parser.add_argument('-f', '--find', nargs='+', action='extend', default=[])
  parser.add_argument('-m', '--match', default=False, action='store_true')
  parser.add_argument('-i', '--highest')
  parser.add_argument('-w', '--lowest')
  parser.add_argument('-a', '--author', nargs='+', action='extend', default=[])
  args = parser.parse_args()

  taxa = frozenset(
    args.find if args.find else (
      args.branch if args.branch else (
        args.root if args.root else args.leaf
      )
    )
  )

  data = load_files()

  logger.info(f"Checking {len(data['authors'])} authors...")
  for author_key, author in data['authors'].items():
    Author.add(author, author_key)
  logger.info('...authors checked.')

  for pub_key, publication in data['publications'].items():
    Publication.add(publication, pub_key)

  logger.info(f"Checking {len(data['sources'])} sources...")
  for ref_key, source in data['sources'].items():
    Source.add(source, ref_key)
  logger.info('...sources checked.')

  logger.info(f"Processing {len(data['taxa'])} taxa...")
  deferred = []
  for taxon_key, taxon_data in data['taxa'].items():
    if taxon_data.keys() & {'altRankOf', 'altSpellingOf'}:
      deferred.append((taxon_key, taxon_data))
      continue
    Taxon.add(taxon_data, taxon_key)
  for taxon_key, taxon_data in deferred:
    Taxon.add(taxon_data, taxon_key)
  logger.info(f"...taxa processed.")

  check_trees(data, taxa, args)
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
