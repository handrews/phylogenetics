import sys
import pathlib

import yaml
import jschon

schema_catalog = jschon.create_catalog('2020-12')
"""The default shared ``jschon`` schema loader and cache"""

def printe(data, *args, **kwargs):
  return sys.stderr.write(str(data) + '\n')

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
      printe(f'Loading "{filename}" with duplication prevention...')
      return yaml.load(fd, Loader=UniqueKeyNoDatesLoader)
    else:
      return yaml.safe_load(fd)

if __name__ == '__main__':
  schema_library = jschon.JSONSchema(load_yaml('schemas/phylogeny.yaml'))
  r = schema_library.validate()
  if not r.valid:
    printe("Schema not valid against metaschema!")
    printe(yaml.safe_dump(r.output('detailed')))

  printe("Schema is valid.")
  defs = schema_library['$defs']
  schema = None

  data = {
    'authors': {},
    'sources': {},
    'trees': {},
  }
  for filename in sys.argv[1:]:
    name = pathlib.Path(filename).stem
    data[name] = load_yaml(filename)
    try:
      schema = defs[name]
      r = schema.evaluate(jschon.JSON(data[name]))
      if not r.valid:
        printe(yaml.safe_dump(r.output('detailed')))
      else:
        printe(f'"{filename}" is valid.')
    except KeyError as e:
      printe(repr(e))

  for ref_id, article in data['sources']['articles'].items():
    source_type = 'journal' if 'journal' in article else 'book'
    if article[source_type] not in data['sources']['publications']:
      printe(f"*** ERROR: {source_type} \"{article['publications']}\"")

    expected_id = ''
    for author in article['authors']:
      if author not in data['authors']:
        printe(f'*** ERROR: Author "{author}" not found!')
      if expected_id:
        expected_id += '_'
      expected_id += author.split('_')[0]
    expected_id += f"_{article['pubDate']['year']}"

    if ref_id != expected_id:
      printe(f'*** ERROR: Expected "{expected_id}" but found "{ref_id}"')

    if ref_id not in data['sources']['articles']:
      printe(f'*** ERROR: Source "{ref_id}" not found!')
