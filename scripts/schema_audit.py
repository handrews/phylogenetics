#!/usr/bin/env python3
"""Measure how much of ``schemas/phylogeny.yaml`` the data actually exercises.

Answers three questions the schema alone cannot:

* **Coverage** -- which schema locations are never reached by any data?
* **Frequency** -- for each ``$defs`` entry, how often is each property used?
* **Shape** -- what value types and enum members actually occur?

The measurement reuses the ``verbose`` output of ``json-schema-engine``, a tree
carrying a schema location and an instance location for every keyword evaluated
and every subschema applied.  That is the same per-keyword-location coverage
that Istanbul-style JSON Schema coverage tools produce, but it also carries the
instance paths, and it needs no dependency the project does not already have.

Deliberately does *not* reuse ``phylohist.loader.taxa.Tree``: the census measures
what the schema evaluation reaches, so it works from the raw documents the
schema sees, not from the object model built over them.

Usage::

    python scripts/schema_audit.py                 # census -> stdout summary
    python scripts/schema_audit.py --json out.json # full census as JSON
    python scripts/schema_audit.py --markdown notes/audits/schema-audit.md
"""

import argparse
import collections
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from phylohist.loader.io import (  # noqa: E402
  COMMON_FILES,
  SCHEMA_URI,
  TREE_DIR,
  LoadError,
  build_schema,
  load_yaml,
)

ROOT = pathlib.Path(__file__).parent.parent
SCHEMA_PATH = ROOT / 'schemas' / 'phylogeny.yaml'

# The engine reports absolute locations under the URI the schema is registered
# at; keep only the `phylogeny#/...` part so locations read as the schema file
# is written.  A resource root loses its empty fragment ("phylogeny", not
# "phylogeny#"), which is the form `inventory()` builds independently.
_URI_PREFIX = f'{SCHEMA_URI.rsplit("/", 1)[0]}/'


def location(absolute):
  """Stable, run-independent identifier for a schema location."""
  return absolute.removeprefix(_URI_PREFIX).rstrip('#')


# JSON Schema type name -> the Python type names `type_name()` reports.
JSON_TYPES = {
  'string': {'str'},
  'integer': {'int'},
  'number': {'int', 'float'},
  'boolean': {'bool'},
  'null': {'null'},
  'array': {'list'},
  'object': {'dict'},
}


def type_name(value):
  if isinstance(value, bool):
    return 'bool'
  return {
    int: 'int',
    float: 'float',
    str: 'str',
    list: 'list',
    dict: 'dict',
    type(None): 'null',
  }.get(type(value), type(value).__name__)


def _unescape(token):
  return token.replace('~1', '/').replace('~0', '~')


def instance_value(data, pointer, names):
  """The value a node's instance location names in already-parsed data.

  Output locations cannot point at a property *name*, so a subschema applied
  by ``propertyNames`` reports the location of the property's value.  Under
  ``names`` the instance really is that final token.
  """
  if names:
    return _unescape(pointer.rsplit('/', 1)[-1])
  node = data
  for token in pointer.split('/')[1:]:
    node = node[int(token)] if isinstance(node, list) else node[_unescape(token)]
  return node


class Census:
  """Accumulates usage across every corpus file."""

  def __init__(self):
    # (corpus, schema location) -> set of instance paths that reached it
    self.reached = collections.defaultdict(set)
    # schema location -> value type -> set of instance paths
    self.types = collections.defaultdict(lambda: collections.defaultdict(set))
    # schema location -> raw value -> set of instance paths
    self.enums = collections.defaultdict(lambda: collections.defaultdict(set))
    # schema location -> [sample values]
    self.samples = collections.defaultdict(list)
    # corpus -> property name -> count (independent raw-YAML cross-check)
    self.raw_keys = collections.defaultdict(collections.Counter)
    # corpus -> source id -> count, for every value typed as $defs/sourceId
    self.source_refs = collections.defaultdict(collections.Counter)
    self.invalid = []

  def absorb(self, document, data, corpus, prefix):
    """Walk a ``verbose`` output tree iteratively (the data nests deeply).

    The tree alternates: the root is a schema application, its children are the
    keywords that schema evaluated, an applicator keyword's children are the
    subschemas it applied, and so on.  Tracking which of the two a node is, is
    all it takes to name the subschema a node belongs to -- a keyword node's
    location is its subschema's plus the keyword.  Attributing every node to
    its subschema is what gives a location to property subschemas carrying no
    assertion keyword of their own (e.g. ``taxon.designation``, which is
    description-only).
    """
    stack = [(document, True, False)]
    while stack:
      node, applied, names = stack.pop()
      loc = location(node['absoluteKeywordLocation'])
      keyword = None
      if not applied:
        loc, _, keyword = loc.rpartition('/')
        loc = loc.rstrip('#')
      inst = f'{prefix}{node["instanceLocation"]}'
      self.reached[(corpus, loc)].add(inst)

      if keyword == 'type':
        value = instance_value(data, node['instanceLocation'], names)
        self.types[loc][type_name(value)].add(inst)
        # Only string samples are reported; keeping ints would crowd them out
        # at locations where numbers dominate (e.g. article.pages).
        if isinstance(value, str):
          bucket = self.samples[loc]
          if len(bucket) < 200:
            bucket.append(value)
      elif keyword == 'enum':
        value = instance_value(data, node['instanceLocation'], names)
        self.enums[loc][repr(value)].add(inst)
      elif keyword == 'pattern' and loc == 'phylogeny#/$defs/sourceId':
        # Every value the schema declares to be a source id.  The pattern says
        # it is well-formed; only a cross-reference says it names something.
        self.source_refs[corpus][instance_value(data, node['instanceLocation'], names)] += 1

      children = node.get('annotations') or node.get('errors') or ()
      names = names or keyword == 'propertyNames'
      stack.extend((child, not applied, names) for child in children)


def walk_raw(node, corpus, census):
  """Independent pass over parsed YAML: count property names directly."""
  if isinstance(node, dict):
    for key, value in node.items():
      census.raw_keys[corpus][key] += 1
      walk_raw(value, corpus, census)
  elif isinstance(node, list):
    for item in node:
      walk_raw(item, corpus, census)


def load_schema():
  """The registered schema, or exit if it fails its own metaschema."""
  try:
    return build_schema()
  except LoadError:
    sys.exit('Schema is not valid against the metaschema.')


def corpus_files():
  """(corpus label, def name, path) for everything we can census."""
  items = []
  for path in COMMON_FILES:
    if path.exists():
      items.append(('data', path.stem, path))
  # Since trees.yaml was split, every tree lives in its own file under
  # data/trees/, keyed by the source id its filename stems from.
  for path in sorted(TREE_DIR.iterdir()):
    if path.suffix == '.yaml':
      items.append(('data', 'trees', path))
  return items


def run_census():
  schema = load_schema()
  census = Census()

  for corpus, def_name, path in corpus_files():
    # Must use the debug path: it installs the loader that keeps dates as
    # strings, which is what the schema expects.
    data = load_yaml(path)
    if data is None:
      continue
    # Files under data/trees/ hold a single opinion keyed by the file stem.
    if path.parent == TREE_DIR:
      data = {path.stem: data}
    result = schema.engine.evaluate(schema.uri(def_name), data, output='verbose', annotations=True)
    if not result.valid:
      census.invalid.append(path.name)
    census.absorb(result.output_document, data, corpus, f'{path.name}:')
    walk_raw(data, corpus, census)

  return census


# Keywords whose value is a single subschema, or a map/array of subschemas.
_SUBSCHEMA = (
  'items',
  'additionalProperties',
  'propertyNames',
  'not',
  'if',
  'then',
  'else',
  'unevaluatedProperties',
  'contains',
)
_SUBSCHEMA_MAP = ('properties', 'patternProperties', '$defs')
_SUBSCHEMA_LIST = ('allOf', 'anyOf', 'oneOf', 'prefixItems')


def inventory(node, base='phylogeny#', pointer='', out=None):
  """Every schema location in the file, labelled the way `location()` does."""
  if out is None:
    out = {}
  if not isinstance(node, dict):
    return out
  if '$id' in node and pointer:
    base, pointer = f'{node["$id"]}#', ''
  # A resource root is labelled without the empty fragment ("phylogeny", not
  # "phylogeny#"), so match that or the root looks permanently unreached.
  out[f'{base}{pointer}' if pointer else base.rstrip('#')] = node
  for key in _SUBSCHEMA:
    if isinstance(node.get(key), dict):
      inventory(node[key], base, f'{pointer}/{key}', out)
  for key in _SUBSCHEMA_MAP:
    for name, sub in (node.get(key) or {}).items():
      inventory(sub, base, f'{pointer}/{key}/{name}', out)
  for key in _SUBSCHEMA_LIST:
    for i, sub in enumerate(node.get(key) or []):
      inventory(sub, base, f'{pointer}/{key}/{i}', out)
  return out


def def_of(loc):
  """Which ``$defs`` entry a schema location belongs to."""
  m = re.match(r'phylogeny#/\$defs/([^/]+)', loc)
  return m.group(1) if m else '(root)'


def _label(container, name):
  """Dotted path of a property relative to its `$defs` entry.

  Keeps `tree.citation.source` distinguishable from `tree.source`, which are
  different properties that would otherwise both render as `source`.
  """
  rel = re.sub(r'^(tree|phylogeny#/\$defs/[^/]+)#?', '', container)
  rel = rel.replace('/properties/', '.').lstrip('.')
  return f'{rel}.{name}' if rel else name


def counts(census, loc):
  return len(census.reached.get(('data', loc), ()))


def analyse(census):
  """Turn raw census data into the report's findings."""
  schema_yaml = load_yaml(SCHEMA_PATH)
  locs = inventory(schema_yaml)
  reached = {loc for _, loc in census.reached}

  report = {
    'unreached': [],
    'properties': [],
    'enums': [],
    'types': [],
    'invalid_files': census.invalid,
  }

  # 1. Coverage: schema locations no data ever reached.
  for loc in sorted(locs):
    if loc not in reached:
      report['unreached'].append({'location': loc, 'def': def_of(loc)})

  # 2. Property frequency, with the containing def's instance count as the
  #    denominator so "rare" is readable as a percentage.
  for loc in sorted(locs):
    m = re.match(r'(.*)/properties/([^/]+)$', loc)
    if not m:
      continue
    # A resource root is recorded without its empty fragment ("tree").
    parent, name = m.group(1).rstrip('#') or m.group(1), m.group(2)
    d = counts(census, loc)
    pd = counts(census, parent)
    report['properties'].append(
      {
        'location': loc,
        'def': def_of(loc),
        'container': parent,
        'property': name,
        'label': _label(parent, name),
        'data': d,
        'container_data': pd,
        'pct': round(100.0 * d / pd, 1) if pd else None,
      }
    )

  # 3. Enum members: used vs never used.
  for loc, node in sorted(locs.items()):
    if not isinstance(node.get('enum'), list):
      continue
    used = {k: len(v) for k, v in census.enums.get(loc, {}).items()}
    allowed = {repr(v): v for v in node['enum']}
    report['enums'].append(
      {
        'location': loc,
        'def': def_of(loc),
        'used': sorted(((allowed.get(k, k), n) for k, n in used.items()), key=lambda kv: -kv[1]),
        'unused': [v for k, v in allowed.items() if k not in used],
        'total': len(node['enum']),
      }
    )

  # 4. Value types actually observed where the schema allows a union.
  for loc in sorted(census.types):
    seen = {t: len(v) for t, v in census.types[loc].items()}
    node = locs.get(loc, {})
    declared = node.get('type')
    if isinstance(declared, str):
      declared = [declared]
    report['types'].append(
      {
        'location': loc,
        'def': def_of(loc),
        'declared': declared,
        'observed': dict(sorted(seen.items(), key=lambda kv: -kv[1])),
        'samples': census.samples.get(loc, [])[:200],
      }
    )

  return report


def dangling_sources(census):
  """Source ids that are well-formed but name no record in sources.yaml.

  The `sourceId` pattern cannot catch this: a typo like `1854c_billigns` or a
  stale id matches it perfectly.  Only a lookup against the real keys does.
  """
  known = set(load_yaml(ROOT / 'data' / 'sources.yaml'))
  out = {}
  for corpus, counter in census.source_refs.items():
    missing = {sid: n for sid, n in counter.items() if sid not in known}
    out[corpus] = dict(sorted(missing.items(), key=lambda kv: -kv[1]))
  return out


def cross_check(census, report):
  """Independent verification: raw-YAML key counts vs result-tree counts.

  The two passes share no code.  Compare *distinct instance paths*, not summed
  per-location counts: one instance node legitimately reaches several schema
  locations at once (``modularDate`` declares ``day``/``month`` in its own
  ``properties`` and again inside each ``then/oneOf`` branch), so summing
  locations would show a spurious 4x.

  Raw counts may legitimately exceed schema-attributed ones, because taxon names
  and source ids are themselves map keys and can collide with property names.
  The real error condition is the reverse: schema-attributed paths outnumbering
  raw occurrences would mean the result walk invented nodes.
  """
  paths = collections.defaultdict(set)
  for row in report['properties']:
    paths[row['property']] |= census.reached.get(('data', row['location']), set())
  problems = []
  for name, seen in paths.items():
    raw = census.raw_keys['data'][name]
    if len(seen) > raw:
      problems.append(
        f'{name}: result-tree {len(seen)} distinct paths > raw-YAML {raw} occurrences'
      )
  return sorted(problems)


def _table(header, rows):
  if not rows:
    return ['(none)', '']
  out = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join('---' for _ in header) + '|']
  out += ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]
  out.append('')
  return out


def render(census, report):
  """Render the regenerable census.  Narrative analysis lives elsewhere."""
  L = [
    '# Schema usage census',
    '',
    '**Generated** by `scripts/schema_audit.py` -- do not edit by hand.',
    'Narrative analysis of these numbers is in `notes/audits/schema-audit.md`.',
    '',
    'Counts are *distinct instance locations* that reached a given schema',
    'location, measured from the `json-schema-engine` verbose output tree.',
    '',
  ]

  if report['invalid_files']:
    L += [
      f'> `{"`, `".join(report["invalid_files"])}` do not currently validate. '
      'They are still censused -- presence does not require validity -- so '
      'their columns show what is *used*, not what is correct.',
      '',
    ]

  L += [
    '## 1. Unreached schema locations',
    '',
    'Schema locations no data anywhere reaches. A nested location is listed',
    'even when its parent is also unreached, so read parents first.',
    '',
  ]
  by_def = collections.defaultdict(list)
  for row in report['unreached']:
    if row['location'] == 'phylogeny':
      continue  # never evaluated directly; io.py always enters via $defs/<name>
    by_def[row['def']].append(row['location'])
  L += _table(
    ['`$defs`', 'unreached locations'],
    [(f'`{d}`', '<br>'.join(f'`{x}`' for x in sorted(v))) for d, v in sorted(by_def.items())],
  )

  L += [
    '## 2. Property frequency by `$defs`',
    '',
    "`data %` is the share of that container's instances carrying the",
    'property.',
    '',
  ]
  groups = collections.defaultdict(list)
  for row in report['properties']:
    groups[row['def']].append(row)
  for d in sorted(groups):
    rows = sorted(groups[d], key=lambda r: (-r['data'], r['label']))
    if not any(r['data'] for r in rows):
      continue
    root = 'tree' if d == 'tree' else f'phylogeny#/$defs/{d}'
    total = len(census.reached.get(('data', root), ()))
    L += [f'### `{d}`' + (f' -- {total} instances in `data/`' if total else ''), '']
    L += _table(
      ['property', 'data', 'data %'],
      [(f'`{r["label"]}`', r['data'], '-' if r['pct'] is None else f'{r["pct"]}%') for r in rows],
    )

  L += ['## 3. Enum member usage', '']
  for e in sorted(report['enums'], key=lambda x: x['location']):
    used = sum(n for _, n in e['used'])
    L += [
      f'### `{e["location"]}`',
      '',
      f'{len(e["used"])} of {e["total"]} members used, {used} occurrences.',
      '',
    ]
    if e['used']:
      L += _table(['value', 'count'], [(f'`{v!r}`', n) for v, n in e['used']])
    if e['unused']:
      L += [
        f'**Never used ({len(e["unused"])}):** ' + ', '.join(f'`{v!r}`' for v in e['unused']),
        '',
      ]

  L += [
    '## 4. Observed value types where the schema allows a union',
    '',
    'Tests whether each multi-type declaration is actually needed.',
    '',
  ]
  rows = []
  for t in report['types']:
    if not t['declared'] or len(t['declared']) < 2:
      continue
    unused_types = [d for d in t['declared'] if not (JSON_TYPES.get(d, {d}) & set(t['observed']))]
    obs = ', '.join(f'{k}x{v}' for k, v in t['observed'].items())
    strings = []
    for sample in t['samples']:
      if not isinstance(sample, str):
        continue
      flat = ' '.join(sample.split())
      short = flat[:24] + '...' if len(flat) > 24 else flat
      if short not in strings:
        strings.append(short)
      if len(strings) == 4:
        break
    rows.append(
      (
        f'`{t["location"]}`',
        '/'.join(t['declared']),
        obs or '-',
        ', '.join(f'`{s}`' for s in strings) or '-',
        ', '.join(unused_types) or '-',
      )
    )
  L += _table(
    ['location', 'declared', 'observed', 'string examples', 'declared but unseen'], sorted(rows)
  )
  return '\n'.join(L) + '\n'


def main():
  ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
  ap.add_argument('--json', metavar='PATH', help='write the full census as JSON')
  ap.add_argument('--markdown', metavar='PATH', help='write the census report')
  args = ap.parse_args()

  census = run_census()
  report = analyse(census)

  problems = cross_check(census, report)
  if problems:
    print('CROSS-CHECK FAILED:', file=sys.stderr)
    for p in problems:
      print('  ' + p, file=sys.stderr)
    return 1
  print('cross-check passed: no schema location outnumbers its raw YAML count', file=sys.stderr)

  dangling = dangling_sources(census)
  report['dangling_sources'] = dangling
  for corpus in sorted(dangling):
    bad = dangling[corpus]
    total = sum(census.source_refs[corpus].values())
    if bad:
      print(f'{corpus}: {len(bad)} dangling source id(s) of {total} checked:', file=sys.stderr)
      for sid, n in bad.items():
        print(f'  {n}x {sid}', file=sys.stderr)
    else:
      print(f'{corpus}: all {total} source ids resolve', file=sys.stderr)
  if dangling.get('data'):
    return 1

  if args.json:
    pathlib.Path(args.json).write_text(json.dumps(report, indent=1, default=str))
  if args.markdown:
    pathlib.Path(args.markdown).write_text(render(census, report))
  if not (args.json or args.markdown):
    print(f'{len(report["unreached"])} unreached schema locations')
    print(f'{len(report["properties"])} property locations')
  return 0


if __name__ == '__main__':
  sys.exit(main())
