import sys
import pathlib
import logging
import collections

import yaml
import jschon

from . import logger

def check_node(node, data, parent=[]):
  taxon_fields = {'taxon', 'cfTaxon', 'openTaxon'} & node.keys()
  if len(taxon_fields) > 1:
    logger.error(
      f'Found {len(taxon_fields)} taxon fields ({taxon_fields}), expected one!'
    )

  elif len(taxon_fields) == 1:
    taxon_type = taxon_fields.pop()

    taxon_id = node[taxon_type]
    current = parent + [taxon_id]
    logger.debug(f'checking {current}')
    if not (taxon := data['taxa'].get(taxon_id)):
      logger.error(f'Taxon "{taxon_id}" not found!')

    elif taxon_type == 'taxon' and taxon['name'] is None:
      logger.error(f'Taxon "{taxon_id}" expected to have a name!')
    elif taxon_type != 'taxon' and taxon['name'] is not None:
      logger.error(f'Taxon "{taxon_id}" NOT expected to have a name!')

    if node.get('new'):
      # TODO: Figure this out
      pass
  else:
    current = parent + ['_anon_']
    logger.debug(f'Descending through {current}')

  for child in node.get('children', {}):
    check_node(child, data, current)


def build_expected_author(expected, author):
  new_expected = f'{expected}.' + '.'.join(
    [name[0].lower() for name in author['given'].split(' ')]
  )
  return {new_expected}


def build_expected_taxon(expected, taxon):
  if not (rank := taxon.get('rank')):
    if taxon['name'] is None:
      logger.error(f"Unnamed, unrakned taxon {expected}!")
      # Let the second check fail normally.
      return {expected}

    rank = 'genus' if taxon['name'][0].isupper() else 'species'

  if rank in ('species', 'subspecies'):
    species_expected = expected
    logger.debug(f'Building species id for {expected}...')
    for author_id in taxon['auth']:
      species_expected += f"_{author_id.lower()}"
    species_expected += f"_{taxon['year']}"
    logger.debug(f'...built {species_expected}')
    return {species_expected}

  ranked_expected = expected
  # alt_expected = expected
  expected_set = {expected}

  logger.debug(f'Creating alt taxon_id expectations for "{taxon}"')
  ranked_expected += f"-{rank.lower()}"
  # for author_id in taxon['auth']:
    # logger.debug(f'Adding author "{author_id}" for taxon_id "{taxon}"')
    # alt_expected += f'-{author_id.lower()[0]}'
  # alt_expected += f"-{taxon['year']}"

  return {ranked_expected} #, alt_expected}


def check_expectation(
  actual_id,
  expected,
  build_expected_set=None,
  *args,
  **kwargs,
):
  if actual_id == expected:
    return True, {expected}

  if build_expected_set is None or not actual_id.startswith(expected):
    return False, {expected}

  expected_set = build_expected_set(expected, *args, **kwargs)
  if actual_id in expected_set:
    return True, expected_set
  return False, expected_set


def check_authors(data):
  logger.info(f"Checking {len(data['authors'])} authors...")
  for author_id, author in data['authors'].items():
    expected = author['family'].lower()
    valid, expected_set = check_expectation(
      author_id,
      expected,
      build_expected_author,
      author,
    )
    if not valid:
      logger.error(f'"{author_id}" not in expected set: {expected_set}')
  logger.info('...authors checked.')


def check_sources(data):
  logger.info(f"Checking {len(data['sources']['articles'])} sources...")
  sources = set()
  for pub_id, publication in data['sources']['publications'].items():
    for editor in publication.get('editors', ()):
      if editor not in data['authors']:
        logger.error(f'Editor "{editor}" not found for publication {pub_id}!')

  for ref_id, article in data['sources']['articles'].items():
    sources.add(ref_id)
    logger.debug(f'Processing article "{ref_id}"')
    source_type = 'journal' if 'journal' in article else 'book'
    if article[source_type] not in data['sources']['publications']:
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

    if ref_id not in data['sources']['articles']:
      logger.error(f'Source "{ref_id}" not found!')

  logger.info('...sources checked.')
  return sources


def check_taxa(data):
  logger.info(f"Processing {len(data['taxa'])} taxa...")
  for taxon_id, taxon in data['taxa'].items():
    if taxon['name'] is not None:
      expected = taxon['name'].lower()
      logger.debug(f'  Processing taxon "{taxon_id}"...')

      valid, valid_set = check_expectation(
        taxon_id,
        expected,
        build_expected_taxon,
        taxon,
      )
      if not valid:
        logger.error(f'"{taxon_id}" not in expected set: {valid_set}')

    for author_id in taxon['auth']:
      logger.debug('    Processing authority "{author_id}"')
      # This won't work with multi-token names, but good enough for now
      if author_id != author_id.lower():
        continue

      if not (author := data['authors'].get(author_id)):
        logger.error(
          f'Unrecognized author "{author_id}" in authority for "{taxon_id}"'
        )
        continue

      if (year := taxon.get('year')):
        # 15 pretty arbitrary, no clue if there's a kid genius paleontologist
        if 'birth' in author and year < (author['birth'] + 15):
          birth = author['birth']
          logger.error(f'"{author_id}" born {birth} as authority in {year}?')
        # plus 5 for Barrande 1887
        if 'death' in author and year > (author['death'] + 5):
          death = author['death']
          logger.error(f'"{author_id}" died {death} as authority in {year}?')
    logger.debug(f'    ...all authorities for "{taxon_id}" processed')

  logger.info(f"...taxa processed.")


def check_trees(data, sources):
  logger.info(f"Processing {len(data['trees'])} opinions...")
  opinions = set()
  for ref_id, opinion in data['trees'].items():
    opinions.add(ref_id)
    logger.debug(f'Processing opinions from "{ref_id}"')
    if ref_id not in data['sources']['articles']:
      logger.error(f'Tree citation "{ref_id}" not found!')

    trees = [t for t in opinion.get('taxonomies', {})]
    num_tax = len(trees)
    logger.debug(f'Found {num_tax} taxonomic trees')
    trees.extend([p['tree'] for p in opinion.get('phylogenies', {})])
    num_phy = len(trees) - num_tax
    logger.debug(f'Found {num_phy} phylogenetic trees')
    for t in trees:
      check_node(t, data)
  logger.info(f"...opinions processed.")

  if (difference := sources - opinions):
    logger.warn("Missing opinions from:\n    " + '\n    '.join(difference))
