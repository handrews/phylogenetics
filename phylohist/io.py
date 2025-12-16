import sys
import pathlib
import logging
import collections

import yaml
import jschon

logger = logging.getLogger(__name__)


FILEDIR = pathlib.Path(__file__).parent / '..' / 'data'
FILES = (
  FILEDIR / 'authors.yaml',
  FILEDIR / 'publications.yaml',
  FILEDIR / 'sources.yaml',
  FILEDIR / 'taxa.yaml',
  FILEDIR / 'trees.yaml',
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


def load_files(*files):
  if files:
    files = [pathlib.Path(f) for f in files]
  else:
    files = FILES

  logger.info("Checking schema...")
  schema_library = jschon.JSONSchema(load_yaml(
    pathlib.Path(__file__).parent / '..' / 'schemas' / 'phylogeny.yaml'
  ))
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
    'publications': {},
    'sources': {},
    'taxa': {},
    'trees': {},
  }
  for filename in files:
    logger.info(f'Checking "{filename}"...')
    name = filename.stem
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
