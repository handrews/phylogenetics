import sys
import pathlib
import logging
import collections

import yaml
import jschon

FUTURE = 2030
FILES = (
  'authors.yaml',
  'sources.yaml',
  'taxa.yaml',
  'trees.yaml',
)

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


class UniqueKeyNoDatesLoader(yaml.SafeLoader):
  # and https://stackoverflow.com/questions/34667108/ignore-dates-and-times-while-parsing-yaml
  @classmethod
  def remove_implicit_resolver(cls, tag_to_remove):
    """
    Remove implicit resolvers for a particular tag

    Takes care not to modify resolvers in super classes.

    We want to load datetimes as strings, not dates, because we
    go on to serialise as json which doesn't have the advanced types
    of yaml, and leads to incompatibilities down the track.
    """
    if not 'yaml_implicit_resolvers' in cls.__dict__:
      cls.yaml_implicit_resolvers = cls.yaml_implicit_resolvers.copy()

    for first_letter, mappings in cls.yaml_implicit_resolvers.items():
      cls.yaml_implicit_resolvers[first_letter] = [(tag, regexp)
                                                   for tag, regexp in mappings
                                                   if tag != tag_to_remove]

  # from https://gist.github.com/pypt/94d747fe5180851196eb?permalink_comment_id=4653474#gistcomment-4653474
  def construct_mapping(self, node, deep=False):
    mapping = set()
    for key_node, value_node in node.value:
      if ':merge' in key_node.tag:
        continue
      key = self.construct_object(key_node, deep=deep)
      if key in mapping:
        raise ValueError(f"Duplicate {key!r} key found in YAML.")
      mapping.add(key)
    return super().construct_mapping(node, deep)


def load_yaml(filename, debug=True):
  UniqueKeyNoDatesLoader.remove_implicit_resolver('tag:yaml.org,2002:timestamp')
  with open(filename) as fd:
    if debug:
      logger.debug(f'Loading "{filename}" with duplication prevention...')
      data = yaml.load(fd, Loader=UniqueKeyNoDatesLoader)
    else:
      logger.debug(f'Loading "{filename}" with safe_load()...')
      data = yaml.safe_load(fd)
    logger.debug(f'...loaded "{filename}"')
    return data


def check_node(n, data, parent=[]):
  if 'taxon' in n:
    current = parent + [n['taxon']]
    logger.debug(f'checking {current}')
    if not (taxon := data['taxa'].get(n['taxon'])):
      logger.error(f"Taxon \"{n['taxon']}\" not found!")
    if n.get('new'):
      # TODO: Figure this out
      pass
  else:
    current = parent + ['_anon_']
    logger.debug(f'Descending through {current}')
  for c in n.get('children', {}):
    check_node(c, data, current)


def load_files():
  logger.info("Checking schema...")
  schema_library = jschon.JSONSchema(load_yaml('schemas/phylogeny.yaml'))
  r = schema_library.validate()
  if not r.valid:
    logger.error("Schema not valid against metaschema!")
    logger.error(yaml.safe_dump(r.output('detailed')))
    sys.exit(-1)

  logger.debug("Schema is valid.")
  defs = schema_library['$defs']

  schema = None
  data = {
    'authors': {},
    'sources': {},
    'taxa': {},
    'trees': {},
  }
  for filename in FILES:
    logger.info(f'Checking "{filename}"...')
    name = pathlib.Path(filename).stem
    data[name] = load_yaml(filename)
    try:
      schema = defs[name]
      r = schema.evaluate(jschon.JSON(data[name]))
      if not r.valid:
        logger.error(f'File "{filename}" is not valid.')
        logger.error(yaml.safe_dump(r.output('detailed')))
        sys.exit(-1)
      else:
        logger.debug(f'"{filename}" is valid.')
    except KeyError as e:
      logger.error(repr(e))
  return data


def build_expected_author(expected, author):
  new_expected = f'{expected}.' + '.'.join(
    [name[0].lower() for name in author['given'].split(' ')]
  )
  return {new_expected}


def build_expected_taxon(expected, taxon):
  if not (rank := taxon.get('rank')):
    rank = 'genus' if taxon['name'][0].isupper() else 'species'

  ranked_expected = expected
  alt_expected = expected
  expected_set = {expected}

  logger.debug(f'Creating alt taxon_id expectations for "{taxon}"')
  ranked_expected += f"-{rank.lower()}"
  for author_id in taxon['auth']:
    logger.debug(f'Adding author "{author_id}" for taxon_id "{taxon}"')
    alt_expected += f'-{author_id.lower()[0]}'
  alt_expected += f"-{taxon['year']}"

  return {ranked_expected, alt_expected}


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


def check_sources(data):
  logger.info("Checking sources...")
  sources = set()
  for ref_id, article in data['sources']['articles'].items():
    sources.add(ref_id)
    logger.debug(f'Processing article "{ref_id}"')
    source_type = 'journal' if 'journal' in article else 'book'
    if article[source_type] not in data['sources']['publications']:
      logger.error(f'{source_type} "{article[source_type]}" not found!')

    expected_id = f"{article['pubDate']['year']}"
    for author in article['authors']:
      if author not in data['authors']:
        logger.error(f'Author "{author}" not found!')
      expected_id += '_' + author.split('_')[0]

    if ref_id != expected_id:
      logger.error(f'Expected "{expected_id}" but found "{ref_id}"')

    if ref_id not in data['sources']['articles']:
      logger.error(f'Source "{ref_id}" not found!')
  return sources


def check_taxa(data):
  logger.info(f"Processing {len(data['taxa'])} taxa...")
  for taxon_id, taxon in data['taxa'].items():
    expected = taxon['name'].lower()
    logger.debug(f'  Processing taxon "{taxon_id}"...')

    valid, valid_set = check_expectation(
      taxon_id,
      expected,
      build_expected_taxon,
      taxon,
    )
    if not valid:
      logger.error(f'"{taxon_id}" not in expected set: {expected_set}')

    for author_id in taxon['auth']:
      logger.debug('    Processing authority "{author_id}"')
      # This won't work with multi-token names, but good enough for now
      if author_id != author_id.lower():
        continue

      if not (author := data['authors'][author_id]):
        logger.error(
          f'Unrecognized author "{author}" in authority for "{taxon_id}"'
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
    logger.warn(f"Missing opinions from {difference}")


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
