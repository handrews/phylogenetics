import logging
import pathlib

import yaml
from json_schema_engine.compiler import compile_validator
from json_schema_engine.core import create_engine
from json_schema_engine.core.errors import SchemaValidationError

logger = logging.getLogger(__name__)


FILEDIR = pathlib.Path(__file__).resolve().parent.parent.parent
DATA_DIR = FILEDIR / 'data'
TREE_DIR = DATA_DIR / 'trees'
DRAFT_DIR = FILEDIR / 'drafts'

# The record files, each checked against the `$defs` entry named for its
# stem and loaded under that name.
RECORD_FILES = (
  DATA_DIR / 'authors.yaml',
  DATA_DIR / 'publications.yaml',
  DATA_DIR / 'sources.yaml',
  DATA_DIR / 'taxa.yaml',
  DATA_DIR / 'repositories.yaml',
  DATA_DIR / 'roles.yaml',
)
# Each tree file is one source's trees, keyed by the source id it is named
# for, and checked against this `$defs` entry.
TREE_DEF = 'treeDocument'


class LoadError(ValueError):
  """The schema or a data file failed validation; the errors were logged."""


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
    if 'yaml_implicit_resolvers' not in cls.__dict__:
      cls.yaml_implicit_resolvers = cls.yaml_implicit_resolvers.copy()

    for first_letter, mappings in cls.yaml_implicit_resolvers.items():
      cls.yaml_implicit_resolvers[first_letter] = [
        (tag, regexp) for tag, regexp in mappings if tag != tag_to_remove
      ]

  # from https://gist.github.com/pypt/94d747fe5180851196eb?permalink_comment_id=4653474#gistcomment-4653474
  def construct_mapping(self, node, deep=False):
    mapping = set()
    for key_node, _value_node in node.value:
      if ':merge' in key_node.tag:
        continue
      key = self.construct_object(key_node, deep=deep)
      if key in mapping:
        raise ValueError(f'Duplicate {key!r} key found in YAML.')
      mapping.add(key)
    return super().construct_mapping(node, deep)


UniqueKeyNoDatesLoader.remove_implicit_resolver('tag:yaml.org,2002:timestamp')


def load_yaml(filename):
  """Parse a YAML file, keeping dates as strings and refusing duplicate
  keys."""
  with open(filename) as fd:
    logger.debug(f'Loading "{filename}"...')
    data = yaml.load(fd, Loader=UniqueKeyNoDatesLoader)
    logger.debug(f'...loaded "{filename}"')
    return data


SCHEMA_PATH = FILEDIR / 'schemas' / 'phylogeny.yaml'

# The schema's own ``$id`` is the relative ``phylogeny``; it resolves against
# whatever URI the document is registered under, and nothing ever retrieves it.
SCHEMA_URI = 'https://phylohist.invalid/phylogeny'


class Validator:
  """One ``$defs`` entry, compiled to a Python function.

  The compiled form answers valid/invalid and nothing else, which is all the
  loader needs on the happy path; the interpreter is asked for the reasons
  only when the compiled form rejects something.
  """

  def __init__(self, engine, uri):
    self._engine = engine
    self._uri = uri
    self._validate = compile_validator(engine, uri).validate

  def check(self, instance, where=None):
    """True, or False once the reasons have been logged, each headed by
    `where` (the file the instance came from) when given."""
    if self._validate(instance):
      return True
    result = self._engine.evaluate(self._uri, instance, output='detailed')
    log_schema_errors(result, where)
    return False


class Schema:
  """The registered phylogeny schema, indexed by ``$defs`` entry name.

  Compiling costs more than a single evaluation, so validators are built on
  first use and kept; one ``Schema`` serves a whole load.
  """

  def __init__(self, engine, base, defs):
    self.engine = engine
    self.base = base
    self._defs = defs
    self._validators = {}

  def uri(self, name):
    """The absolute URI of the ``$defs`` entry ``name``."""
    return f'{self.base}#/$defs/{name}'

  def __getitem__(self, name):
    """The validator for ``$defs/<name>``; LoadError if the schema has none."""
    if name not in self._validators:
      if name not in self._defs:
        raise LoadError(f'no schema definition for "{name}"')
      self._validators[name] = Validator(self.engine, self.uri(name))
    return self._validators[name]


def build_schema():
  r"""Load and register the schema, checking it against its metaschema.

  ``regex_dialect='python'`` keeps the patterns reading as they always have.
  Under the ECMA-262 dialect the spec calls for, ``\w`` is ASCII-only, and
  the schema's identifier patterns are written expecting Python's
  Unicode-aware ``\w`` -- source ids such as ``1773_müller.o.f`` depend on it.
  """
  engine = create_engine(validate_schemas=True, regex_dialect='python')
  document = load_yaml(SCHEMA_PATH)
  try:
    base = engine.register_schema(document, SCHEMA_URI)
  except SchemaValidationError as error:
    logger.error(str(error))
    raise LoadError('the schema is not valid against its metaschema') from None
  return Schema(engine, base, document['$defs'])


def tree_files(drafts=False):
  """Every tree file, in load order: `data/trees/`, then `drafts/` when
  asked, so that a draft replaces the audited tree of its source."""
  directories = (TREE_DIR, DRAFT_DIR) if drafts else (TREE_DIR,)
  return [path for directory in directories for path in sorted(directory.glob('*.yaml'))]


def data_files(drafts=False):
  """``(def name, path)`` for every file the loader checks, in load order."""
  return [(path.stem, path) for path in RECORD_FILES] + [
    (TREE_DEF, path) for path in tree_files(drafts)
  ]


def load_checked(path, validator):
  """One data file, checked; LoadError naming the file if it fails."""
  logger.info(f'Checking "{path}"...')
  document = load_yaml(path)
  if not validator.check(document, where=display_path(path)):
    raise LoadError(f'"{path}" is not valid against the schema')
  logger.debug(f'"{path}" is valid.')
  return document


def load_files(drafts=False):
  """Load and schema-check every data file.

  The record files load under their stems, and the tree files under
  ``trees``, each keyed by its source id. With ``drafts`` true, the
  AI-drafted trees under ``drafts/`` are loaded after the audited ones, so
  that a draft can be run through the same integrity checks before it is
  promoted.
  """
  logger.info('Checking schema...')
  schema = build_schema()
  logger.debug('Schema is valid.')

  data = {path.stem: load_checked(path, schema[path.stem]) for path in RECORD_FILES}
  data['trees'] = {}
  for path in tree_files(drafts):
    if path.stem in data['trees']:
      logger.warning(f'File "{path}" overwrites another tree file.')
    data['trees'][path.stem] = load_checked(path, schema[TREE_DEF])
  return data


def display_path(path):
  """A path as the log names it: relative to the repository root when it
  is under it, else as given."""
  try:
    return str(pathlib.Path(path).resolve().relative_to(FILEDIR))
  except ValueError:
    return str(path)


def log_error_node(error, heading=''):
  if isinstance(error, list):
    for e in error:
      log_error_node(e, heading)
  else:
    to_log = error
    if 'errors' in error:
      log_error_node(error['errors'], heading)
      to_log = {k: v for k, v in error.items() if k != 'errors'}
    logger.error(heading + '\n' + yaml.safe_dump(to_log))


def log_schema_errors(result, where=None):
  heading = f'"{where}" is not valid:' if where is not None else ''
  for error in result.output_document.get('errors', []):
    log_error_node(error, heading)
