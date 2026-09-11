import sys
import pathlib
import logging
import collections

import yaml
import jschon

logger = logging.getLogger(__name__)


# Raw string to work around bizarre syntax highlighting bug
FILEDIR = pathlib.Path(__file__).parent / r'..'
DATA_DIR = FILEDIR / 'data'
TREE_DIR = DATA_DIR / 'trees'
DRAFT_DIR = FILEDIR / 'drafts'

# Note: There were once other file sets, but now only this one.
COMMON_FILES = (
  DATA_DIR / 'authors.yaml',
  DATA_DIR / 'publications.yaml',
  DATA_DIR / 'sources.yaml',
  DATA_DIR / 'taxa.yaml',
)

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


def load_files(drafts=False):
  """Load and schema-check every data file.

  With ``drafts`` true, the AI-drafted trees under ``drafts/`` are loaded
  after the audited ones, so that a draft can be run through the same
  integrity checks before it is promoted.
  """
  files = COMMON_FILES

  logger.info("Checking schema...")
  schema_library = jschon.JSONSchema(load_yaml(
    pathlib.Path(__file__).parent / r'..' / 'schemas' / 'phylogeny.yaml'
  ))
  r = schema_library.validate()
  if not r.valid:
    logger.error("Schema not valid against metaschema!")
    log_schema_errors(r)
    sys.exit(-1)

  logger.debug("Schema is valid.")
  defs = schema_library['$defs']

  schema = None
  data = {
    'authors': {},
    'publications': {},
    'sources': {},
    'taxa': {},
    'trees': {},
    'time': {},
  }
  for filename in files:
    if not filename.exists():
      continue

    logger.info(f'Checking "{filename}"...')
    name = filename.stem
    data[name].update(load_yaml(filename))
    try:
      schema = defs[name]
      r = schema.evaluate(jschon.JSON(data[name]))
      if not r.valid:
        logger.error(f'File "{filename}" is not valid.')
        log_schema_errors(r)
        sys.exit(-1)
      else:
        logger.debug(f'"{filename}" is valid.')
    except KeyError as e:
      logger.error(repr(e))

  _load_tree_dir(TREE_DIR, defs['trees'], data['trees'])
  if drafts:
    _load_tree_dir(DRAFT_DIR, defs['trees'], data['trees'])

  return data


def _load_tree_dir(directory, schema, trees):
  for tree_path in sorted(directory.iterdir()):
    if tree_path.suffix != '.yaml':
      continue

    logger.info(f'Checking "{tree_path}"...')
    name = tree_path.stem
    tree_data = {name: load_yaml(tree_path)}
    r = schema.evaluate(jschon.JSON(tree_data))
    if not r.valid:
      logger.error(f'File "{tree_path}" is not valid.')
      log_schema_errors(r)
      sys.exit(-1)
    else:
      logger.debug(f'"{tree_path}" is valid.')
    if name in trees:
      logger.warning(f'File "{tree_path}" overwrites the main tree file.')
    trees.update(tree_data)


def log_error_node(error):
  if isinstance(error, list):
    for e in error:
      log_error_node(e)
  else:
    to_log = error
    if 'errors' in error:
      log_error_node(error['errors'])
      to_log = {k: v for k, v in error.items() if k != 'errors'}
    logger.error('\n' + yaml.safe_dump(to_log))

def log_schema_errors(result):
  for error in result.output('detailed').get('errors', []):
    log_error_node(error)
