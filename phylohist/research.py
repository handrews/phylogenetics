import sys
import pathlib
import logging
import collections

import yaml
import jschon

logger = logging.getLogger(__name__)


def build_expected_author(expected, author):
  givens = author['given'].split(' ')
  if len(givens) == 1:
    givens = givens[0].split('-')
  new_expected = f'{expected}.' + '.'.join([name[0].lower() for name in givens])
  return {new_expected}


def check_authors(data):
  logger.info(f"Checking {len(data['authors'])} authors...")
  for author_id, author in data['authors'].items():
    expected = author['family'].lower()
    expected_set = build_expected_author(expected, author)
    expected_set.add(expected)
    if author_id not in expected_set:
      logger.error(f'"{author_id}" not in expected set: {expected_set}')
  logger.info('...authors checked.')


def check_sources(data):
  logger.info(f"Checking {len(data['sources'])} sources...")
  sources = set()
  for pub_id, publication in data['publications'].items():
    for editor in publication.get('editors', ()):
      if editor not in data['authors']:
        logger.error(f'Editor "{editor}" not found for publication {pub_id}!')

  for ref_id, article in data['sources'].items():
    sources.add(ref_id)
    logger.debug(f'Processing article "{ref_id}"')
    source_type = (article.keys() & {'journal', 'book', 'reading'}).pop()
    if article[source_type] not in data['publications']:
      logger.error(f'{source_type} "{article[source_type]}" not found!')

    expected_id = f"{article['pubDate']['year']}"
    if ref_id[4] != '_':
      # There's a disambiguation letter, just assume it is correct.
      expected_id += ref_id[4]

    for author in article['authors']:
      if author not in data['authors']:
        logger.error(f'Author "{author}" not found for source {ref_id}!')
      expected_id += '_' + author.split('_')[0]
    for editor in article.get('editors', ()):
      if editor not in data['authors']:
        logger.error(f'Editor "{editor}" not found for source {ref_id}!')

    if ref_id != expected_id:
      logger.error(f'Expected "{expected_id}" but found "{ref_id}"')

    if ref_id not in data['sources']:
      logger.error(f'Source "{ref_id}" not found!')

    if (
      (trans_of := data['sources'][ref_id].get('translationOf')) and
      trans_of not in data['sources']
    ):
      logger.error(
        f'Translation source "{trans_of}" for "{ref_id}" not found!'
      )
  logger.info('...sources checked.')
  return sources
