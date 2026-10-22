#!/usr/bin/env python3
"""Move every attribution into an `authority` block (roadmap A4).

    poetry run python scripts/migrate_authority.py --report
    poetry run python scripts/migrate_authority.py --write
    poetry run python scripts/migrate_authority.py --check-claims

Before this migration an attribution could be written flat (`auth`, `year`,
`in` beside the node or record) or as an `authority` block, and a cited
work's locators (`pages`, `illustrations`) sat at node level on a cited
entry unless a block existed. After it every attribution is an `authority`
block holding `source`, `auctt`, or the printed credit `auth`/`year`/`in`;
a taxon or section record's protologue locators and a cited entry's
locators live inside the block; a cited entry with locators and no
attribution gets a block of locators alone, meaning "as the record"; an
`editorial.corrections` patch follows the node's shape. `citedAs` and a
primary node's own `pages`/`illustrations` stay where they are.

The files are hand-edited YAML with comments, so this rewrites text line by
line: PyYAML locates the structure (`yaml.compose` keeps every line and
column), the script moves lines. Before writing anything it checks every
file: the new text parses to what the old text parses to once the old is
normalised by the same rules (`lift`), the nodes it found are the loader's
(`walk_document`), nothing flat is left, and a second pass changes nothing.
A conflict (a flat credit beside a `source`, a locator both flat and in the
block, anything beside `authority: null`, a patch key written both ways)
stops the run with nothing written, for the owner to resolve by hand.

Kept in the repository until every branch's data has been migrated.
"""

import argparse
import difflib
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import yaml  # noqa: E402

from phylohist.loader.io import UniqueKeyNoDatesLoader, load_yaml  # noqa: E402
from phylohist.loader.material import walk_document  # noqa: E402
from phylohist.loader.taxa import Tree  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent

FLAT = ('auth', 'year', 'in')
LOCATORS = ('pages', 'illustrations')
ATTRIBUTION = ('source', 'auctt', 'auth', 'year')
# The order of a block this script writes.
ORDER = (
  'source',
  'auctt',
  'auth',
  'year',
  'in',
  'attributedTo',
  'ex',
  'pages',
  'illustrations',
  'notes',
)

RECORD, PRIMARY, CITED, PATCH = 'record', 'primary', 'cited', 'patch'
# What each kind of mapping gathers into its block.
GATHERED = {
  RECORD: FLAT + LOCATORS,
  PRIMARY: FLAT,
  CITED: FLAT + LOCATORS,
  PATCH: FLAT,
}


class Conflict(Exception):
  """A mapping the rules cannot rewrite; the owner decides."""


def default_targets(root):
  """The files this migration covers, in load order."""
  files = []
  for data in ('data', 'tests/corpus'):
    files += [root / data / 'taxa.yaml', root / data / 'sections.yaml']
    files += sorted((root / data / 'trees').glob('*.yaml'))
  files += sorted((root / 'drafts').glob('*.yaml'))
  return [f for f in files if f.exists()]


# -- structure --------------------------------------------------------------


def mapping_entries(node):
  """``(key, key node, value node)`` for a composed mapping."""
  return [(k.value, k, v) for k, v in node.value]


def mapping_get(node, key):
  if not isinstance(node, yaml.MappingNode):
    return None
  for k, v in node.value:
    if k.value == key:
      return v
  return None


def seq_items(node):
  return node.value if isinstance(node, yaml.SequenceNode) else ()


def is_null(node):
  return isinstance(node, yaml.ScalarNode) and node.tag == 'tag:yaml.org,2002:null'


def walk_tree(doc):
  """``(mapping node, kind, path)`` for every node of a composed tree
  document, in `walk_document`'s order and with its paths, each node's
  `editorial.corrections` mapping following it as a `PATCH`."""
  position = 0
  for item in seq_items(mapping_get(doc, 'taxonomies')):
    yield from _walk_node(item, position, (), False)
    position += 1
  for phylogeny in seq_items(mapping_get(doc, 'phylogenies')):
    yield from _walk_node(mapping_get(phylogeny, 'tree'), position, (), False)
    position += 1


def _walk_node(node, position, relpath, cited):
  if not isinstance(node, yaml.MappingNode):
    return
  pointer = '/' + '/'.join(str(p) for p in relpath) if relpath else ''
  path = f'{position}{pointer}'.rstrip('/')
  yield node, (CITED if cited else PRIMARY), path
  corrections = mapping_get(mapping_get(node, 'editorial'), 'corrections')
  if isinstance(corrections, yaml.MappingNode):
    yield corrections, PATCH, f'{path} corrections'
  for axis in Tree.RELATED_AXES:
    value = mapping_get(node, axis.name)
    if axis.many:
      for index, item in enumerate(seq_items(value)):
        yield from _walk_node(item, position, (*relpath, axis.name, index), axis.cited)
    elif isinstance(value, yaml.MappingNode):
      yield from _walk_node(value, position, (*relpath, axis.name), axis.cited)
  for index, child in enumerate(seq_items(mapping_get(node, 'children'))):
    yield from _walk_node(child, position, (*relpath, 'children', index), False)


def walk_records(doc):
  for key, value in doc.value:
    if isinstance(value, yaml.MappingNode):
      yield value, RECORD, key.value


def last_line(node):
  """The last line (0-based) a composed node's text occupies."""
  if isinstance(node, yaml.ScalarNode):
    if node.style in ('|', '>') and node.end_mark.column == 0:
      return node.end_mark.line - 1
    return node.end_mark.line
  if node.flow_style or not node.value:
    return node.end_mark.line
  last = node.value[-1][1] if isinstance(node, yaml.MappingNode) else node.value[-1]
  return last_line(last)


def indent_of(line):
  return len(line) - len(line.lstrip(' '))


def is_comment(line):
  return line.lstrip().startswith('#')


def span(lines, key_node, value_node):
  """``(first, last)`` lines of one entry: its key line through its value
  and any comment lines beneath, indented deeper than the key."""
  first = key_node.start_mark.line
  last = max(first, last_line(value_node))
  col = key_node.start_mark.column
  while last + 1 < len(lines) and is_comment(lines[last + 1]) and indent_of(lines[last + 1]) > col:
    last += 1
  return first, last


# -- the rewrite --------------------------------------------------------------


def reindented(lines, first, last, col, new_col):
  """The entry's lines at `new_col`; a `- ` before the first key goes, since
  the block's own line carries it."""
  out = [' ' * new_col + lines[first][col:]]
  delta = new_col - col
  for line in lines[first + 1 : last + 1]:
    if not line.strip():
      out.append(line)
    elif delta >= 0:
      out.append(' ' * delta + line)
    else:
      assert line[:-delta].strip() == '', line
      out.append(line[-delta:])
  return out


def trailing_comment(line):
  """The ` # ...` tail of a key line whose value is a block, if any."""
  head, sep, tail = line.partition(' #')
  return sep + tail if sep and head.rstrip().endswith(':') else ''


def source_year(sources, key):
  record = (sources or {}).get(key) or {}
  return (record.get('pubDate') or {}).get('year')


def rewrite(lines, node, kind, label, sources, counts):
  """The edits ``(first, last, new lines)`` that give one mapping its block,
  or ``[]`` when it has nothing to move; raises `Conflict`."""
  entries = {key: (k, v) for key, k, v in mapping_entries(node)}
  moved = [key for key in GATHERED[kind] if key in entries]
  if not moved:
    return []
  block = entries.get('authority')
  if block is not None and is_null(block[1]):
    raise Conflict(f'{label}: {", ".join(moved)} beside `authority: null`')
  block_keys = [key for key, _, _ in mapping_entries(block[1])] if block else []
  for key in moved:
    if key in block_keys:
      raise Conflict(f'{label}: `{key}` both flat and inside `authority`')
  dropped = []
  if kind != PATCH and set(block_keys) & set(ATTRIBUTION):
    if any(key in ('auth', 'in') for key in moved):
      raise Conflict(f'{label}: a flat credit beside an attribution in `authority`')
    if 'year' in moved:
      year = yaml.safe_load(lines[entries['year'][0].start_mark.line].split(':', 1)[1])
      source = mapping_get(block[1], 'source')
      if kind == RECORD and source is not None and source_year(sources, source.value) == year:
        dropped.append('year')
        moved.remove('year')
      else:
        raise Conflict(f'{label}: a flat `year` beside `source`')

  spans = {key: span(lines, *entries[key]) for key in (*moved, *dropped)}
  if block:
    spans['authority'] = span(lines, *block)
  first_key = min(spans, key=lambda key: spans[key][0])
  first = spans[first_key][0]
  col = entries[first_key][0].start_mark.column
  header = lines[first][:col] + 'authority:'
  if block:
    header += trailing_comment(lines[block[0].start_mark.line])

  children = []
  if block:
    for key, k, v in mapping_entries(block[1]):
      a, b = span(lines, k, v)
      children.append((key, lines[a : b + 1]))
  for key in moved:
    a, b = spans[key]
    children.append((key, reindented(lines, a, b, entries[key][0].start_mark.column, col + 2)))
  if kind == PATCH:
    # The moved keys first, as written; the patch's own `authority` after.
    order = {key: index for index, key in enumerate(moved)}
    children.sort(key=lambda child: order.get(child[0], len(order)))
  else:
    rank = {key: index for index, key in enumerate(ORDER)}
    children.sort(key=lambda child: rank.get(child[0], len(rank)))

  counts['blocks extended' if block else 'blocks created'] += 1
  counts['credits moved'] += sum(1 for key in moved if key in FLAT)
  counts['locators moved'] += sum(1 for key in moved if key in LOCATORS)
  counts['years dropped'] += len(dropped)
  if kind == PATCH:
    counts['patches rewritten'] += 1

  edits = []
  for key, (a, b) in spans.items():
    if key == first_key:
      edits.append((a, b, [header, *(line for _, group in children for line in group)]))
    else:
      edits.append((a, b, []))
  return edits


def transform(text, kind_of_file, label, sources, counts):
  """The migrated text of one file, and whether anything changed."""
  lines = text.split('\n')
  doc = yaml.compose(text, Loader=UniqueKeyNoDatesLoader)
  if doc is None:
    return text, False
  targets = walk_records(doc) if kind_of_file == 'records' else walk_tree(doc)
  edits = []
  conflicts = []
  for node, kind, path in targets:
    try:
      edits += rewrite(lines, node, kind, f'{label} {path}', sources, counts)
    except Conflict as conflict:
      conflicts.append(str(conflict))
  if conflicts:
    raise Conflict('\n'.join(conflicts))
  if not edits:
    return text, False
  edits.sort(key=lambda edit: edit[0], reverse=True)
  for (a, b, _), (c, d, _) in zip(edits, edits[1:], strict=False):
    assert d < a, (label, (c, d), (a, b))
  for a, b, new in edits:
    lines[a : b + 1] = new
  return '\n'.join(lines), True


# -- the checks ---------------------------------------------------------------


def lift_mapping(data, kind, sources):
  """The rules in dict form, applied to a parsed record, node or patch."""
  moved = {key: data.pop(key) for key in GATHERED[kind] if key in data}
  if not moved:
    return
  if 'authority' in data and data['authority'] is None:
    raise Conflict(f'{", ".join(moved)} beside `authority: null`')
  block = dict(data.get('authority') or {})
  if kind == RECORD and 'source' in block and 'year' in moved:
    if source_year(sources, block['source']) == moved['year']:
      del moved['year']
  if kind != PATCH and set(block) & set(ATTRIBUTION) and set(moved) & {'auth', 'in', 'year'}:
    raise Conflict('a flat credit beside an attribution')
  for key in moved:
    if key in block:
      raise Conflict(f'`{key}` both flat and inside `authority`')
  block.update(moved)
  data['authority'] = block


def lift_document(doc, kind_of_file, sources):
  if kind_of_file == 'records':
    for record in doc.values():
      if isinstance(record, dict):
        lift_mapping(record, RECORD, sources)
    return
  for _, node, cited in walk_document(doc):
    lift_mapping(node, CITED if cited else PRIMARY, sources)
    corrections = (node.get('editorial') or {}).get('corrections')
    if isinstance(corrections, dict):
      lift_mapping(corrections, PATCH, sources)


def flat_left(doc, kind_of_file):
  """Where the migrated document still carries a flat field."""
  found = []
  if kind_of_file == 'records':
    for key, record in doc.items():
      if isinstance(record, dict):
        found += [f'{key} {f}' for f in FLAT + LOCATORS if f in record]
    return found
  for path, node, cited in walk_document(doc):
    found += [f'{path} {f}' for f in FLAT if f in node]
    if cited:
      found += [f'{path} {f}' for f in LOCATORS if f in node]
    corrections = (node.get('editorial') or {}).get('corrections')
    if isinstance(corrections, dict):
      found += [f'{path} corrections {f}' for f in FLAT if f in corrections]
  return found


def paths_of(doc, kind_of_file):
  if kind_of_file == 'records':
    return {(key, RECORD) for key, value in doc.value if isinstance(value, yaml.MappingNode)}
  return {(path, kind) for _, kind, path in walk_tree(doc) if kind != PATCH}


def check(text, new_text, kind_of_file, label, sources):
  """Every self-check of one migrated file; raises AssertionError."""
  old_doc = yaml.safe_load(text)
  new_doc = yaml.safe_load(new_text)
  if kind_of_file != 'records':
    loader_paths = {(p, CITED if c else PRIMARY) for p, _, c in walk_document(old_doc)}
    composed = yaml.compose(text, Loader=UniqueKeyNoDatesLoader)
    assert paths_of(composed, kind_of_file) == loader_paths, f'{label}: walk differs'
  lift_document(old_doc, kind_of_file, sources)
  assert new_doc == old_doc, f'{label}: the rewrite does not parse to the lifted original'
  left = flat_left(new_doc, kind_of_file)
  assert not left, f'{label}: flat fields left: {left}'
  comments = sorted(line.strip() for line in text.split('\n') if is_comment(line))
  new_comments = sorted(line.strip() for line in new_text.split('\n') if is_comment(line))
  assert comments == new_comments, f'{label}: comments changed'
  _, changed = transform(new_text, kind_of_file, label, sources, Counts())
  assert not changed, f'{label}: a second pass would change the file'


class Counts(dict):
  def __missing__(self, key):
    return 0


def migrate(files, write, show_diff, report):
  """Transform every file, check each, then write them all or none."""
  results = []
  conflicts = []
  for path in files:
    kind_of_file = 'records' if path.name in ('taxa.yaml', 'sections.yaml') else 'tree'
    sources = load_yaml(path.parent / 'sources.yaml') if kind_of_file == 'records' else None
    text = path.read_text()
    counts = Counts()
    try:
      new_text, changed = transform(text, kind_of_file, path.name, sources, counts)
    except Conflict as conflict:
      conflicts.append(str(conflict))
      continue
    if changed:
      check(text, new_text, kind_of_file, path.name, sources)
    results.append((path, text, new_text, changed, counts))
  if conflicts:
    print('Conflicts; nothing written:', file=sys.stderr)
    for conflict in conflicts:
      print(f'  {conflict}', file=sys.stderr)
    return 1
  total = Counts()
  for path, text, new_text, changed, counts in results:
    for key, value in counts.items():
      total[key] += value
    if report and changed:
      print(
        f'{path.relative_to(ROOT)}: ' + ', '.join(f'{v} {k}' for k, v in sorted(counts.items()))
      )
    if show_diff and changed:
      sys.stdout.writelines(
        difflib.unified_diff(
          text.splitlines(keepends=True),
          new_text.splitlines(keepends=True),
          str(path),
          str(path),
        )
      )
    if write and changed:
      path.write_text(new_text)
  changed_files = sum(1 for r in results if r[3])
  print(
    f'{changed_files} of {len(results)} files {"written" if write else "would change"}: '
    + ', '.join(f'{v} {k}' for k, v in sorted(total.items()))
  )
  return 0


def lift_patch_in_claim(claim):
  """A committed claim's `corrections` payloads in the new shape: the one
  every claim of a corrected node carries, and the editorial claim's own."""
  editorial = claim.get('editorial')
  patches = [editorial.get('corrections')] if isinstance(editorial, dict) else []
  if claim.get('kind') == 'editorial':
    patches.append(claim.get('corrections'))
  for patch in patches:
    if isinstance(patch, dict):
      moved = {key: patch.pop(key) for key in FLAT if key in patch}
      if moved:
        patch['authority'] = {**moved, **(patch.get('authority') or {})}


def check_claims(root):
  """The regenerated claims equal the committed ones once the committed
  patches are lifted; the other generated files are byte-identical."""
  status = 0
  for path in sorted((root / 'claims').glob('*.jsonl')):
    shown = subprocess.run(
      ['git', 'show', f'HEAD:claims/{path.name}'], capture_output=True, text=True, cwd=root
    )
    old = [json.loads(line) for line in shown.stdout.splitlines() if line.strip()]
    new = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    for claim in old:
      lift_patch_in_claim(claim)
    if old != new:
      status = 1
      old_by_id = {c['id']: c for c in old}
      new_by_id = {c['id']: c for c in new}
      differing = [i for i in old_by_id if old_by_id[i] != new_by_id.get(i)]
      differing += [i for i in new_by_id if i not in old_by_id]
      print(f'{path.name}: {len(differing)} claims differ, e.g. {differing[:3]}')
  for name in ('names.json', 'manifest.json', 'repositories.json'):
    shown = subprocess.run(['git', 'show', f'HEAD:claims/{name}'], capture_output=True, cwd=root)
    if shown.stdout != (root / 'claims' / name).read_bytes():
      status = 1
      print(f'{name} differs')
  print('claims unchanged beyond the lifted patches' if status == 0 else 'claims differ')
  return status


def main(argv):
  parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
  parser.add_argument('files', nargs='*', type=pathlib.Path, help='files to migrate (default: all)')
  parser.add_argument('--root', type=pathlib.Path, default=ROOT)
  parser.add_argument('--write', action='store_true', help='write the changed files')
  parser.add_argument('--diff', action='store_true', help='print a unified diff per file')
  parser.add_argument('--report', action='store_true', help='print per-file counts')
  parser.add_argument(
    '--check-claims',
    action='store_true',
    help='compare the regenerated claims/ with the committed ones, patches lifted',
  )
  args = parser.parse_args(argv)
  if args.check_claims:
    return check_claims(args.root.resolve())
  files = [f.resolve() for f in args.files] or default_targets(args.root.resolve())
  return migrate(files, args.write, args.diff, args.report)


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
