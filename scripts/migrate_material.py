#!/usr/bin/env python3
"""One-shot stage 2 migration of the material shapes (roadmap D5).

Converts the legacy node `specimens`, `occurrences`, node-level
`illustrations` on non-cited nodes, and `taxa.yaml`'s `holotype` to the
`material` / `illustrations` / `contexts` / `ranges` model of
`schemas/phylogeny.yaml`, and adds the `repositories` list to the tree
files whose printed prefixes are claimed by more than one registry entry.
Kept until stage 4, when the legacy shapes are retired.

It needs ruamel.yaml, to round-trip the hand-edited YAML, in a separate
environment: ruamel.yaml is not a project dependency, so do not install it
into the project's own environment.

Usage:
    python scripts/migrate_material.py [--root ROOT] [--write] [--report]
    python scripts/migrate_material.py --compact [--root ROOT] [--write]

    --root ROOT   Repository root containing data/trees, data/taxa.yaml,
                  drafts/ (default: the parent of this script's directory).
    --write       Write the changed files. Without it nothing is written.
    --report      Print the migration report (counts, hoists, TODOs).
    --compact     Instead of migrating, merge consecutive `material` entries
                  that carry nothing but `catalogNumbers`, the same `role`
                  and the same `context` into one entry (see
                  `compact_material`), in every tree file under data/trees
                  and drafts; write only the files it changed.
"""

import argparse
import difflib
import glob
import io
import os
import re
from collections import defaultdict

try:
  from ruamel.yaml import YAML
  from ruamel.yaml.comments import CommentedMap, CommentedSeq
except ImportError:  # only the pure helpers (`compact_material`) work without it
  YAML = CommentedMap = CommentedSeq = None

# --------------------------------------------------------------------------
# YAML I/O tuned to preserve the hand-edited style of these files as far as
# ruamel.yaml's round-trip mode allows.
# --------------------------------------------------------------------------


def _represent_null(representer, data):
  # ruamel's default dumps a bare `null` as an empty scalar; several files
  # (notably taxa.yaml) spell it out explicitly, so preserve that spelling
  # on every dump rather than silently rewriting every untouched `null`.
  return representer.represent_scalar('tag:yaml.org,2002:null', 'null')


def make_yaml():
  y = YAML()
  y.preserve_quotes = True
  y.width = 100000  # never rewrap long lines
  y.indent(mapping=2, sequence=2, offset=0)
  y.representer.add_representer(type(None), _represent_null)
  return y


LEGACY_MARKER_RE = re.compile(r'^\s*(specimens|occurrences|illustrations)\s*:', re.MULTILINE)

# Legacy `specimens` role keys (node level and occurrence level) to the
# singular `$defs/role` term the source printed; `None` is an entry with no
# role. Any key not listed here gets no role and a TODO.
ROLE_SINGULAR = {
  'holotype': 'holotype',
  'holotypes': 'holotype',
  'lectotype': 'lectotype',
  'neotype': 'neotype',
  'syntype': 'syntype',
  'syntypes': 'syntype',
  'paratypes': 'paratype',
  'hypotypes': 'hypotype',
  'plesiotypes': 'plesiotype',
  'topotypes': 'topotype',
  'paralectotypes': 'paralectotype',
  'unknowntypes': None,
  'additional': None,
  'unspecified': None,
  'unknown': None,
}

# Tree files whose printed prefixes several registry entries claim: the
# `repositories` list each gets, placed before `taxonomies`.
FILE_REPOSITORIES = {
  '2020_ewin_martin.m_isotalo_zamora': ['nhmuk'],
  '1973_sprinkle': ['u-cincinnati-caster', 'north-museum-fm'],
  '2020_guensburg_sprinkle_mooi_lefebvre_david_roux_derstler': ['fmnh'],
  '2024_zamora_guensburg_sprinkle': ['fmnh'],
  '1963_durham_caster': ['ucmp'],
  '1967c_durham': ['ucmp'],
}

ELLIPSES = {'...', '…'}

FIGURE_LOCATOR_KEYS = {'plate', 'page', 'figures', 'textFigures', 'notes', 'non'}
FIGURE_ALLOWED_EXTRA = {'uncertain', 'of', 'depicts'}  # 'of'/'depicts' are never set by this script

# Fields a legacy `occurrence` carries that become `context` verbatim, minus
# the ones rule 3 explicitly excludes.
CONTEXT_EXCLUDE = {'specimens', 'possibleSpecimens', 'tentative'}

# `$defs/inferredContext` = timeFields + basis + sources + paleocontinent
# (schema commit 8c9dc3c, "inferredContext takes paleocontinent, as the
# Rievers 1961 tree infers one") -- still NOT localTimeFields and not the
# other plain fields (location, unit...) that a legacy occurrence's own
# nested `inferred: {...}` (a full `basicOccurrence`) could carry.
INFERRED_ALLOWED_KEYS = {
  'eon',
  'era',
  'period',
  'series',
  'seriesBoundary',
  'seriesRange',
  'seriesModifier',
  'stage',
  'stageBoundary',
  'stageRange',
  'stageModifier',
  'basis',
  'sources',
  'paleocontinent',
}

# `$defs/timeFields` and `$defs/localTimeFields`, both of which a `ranges` item and
# `context` support (a range = timeFields + localTimeFields + regions/etc).
TIME_FIELD_KEYS = {
  'eon',
  'era',
  'period',
  'series',
  'seriesBoundary',
  'seriesRange',
  'seriesModifier',
  'stage',
  'stageBoundary',
  'stageRange',
  'stageModifier',
}
LOCAL_TIME_FIELD_KEYS = {
  'localPeriod',
  'localSeries',
  'localSeriesBoundary',
  'localSeriesRange',
  'localSeriesModifier',
  'localStage',
  'localStageBoundary',
  'localStageRange',
  'localStageModifier',
}

# Child-node-bearing keys we recurse into, mirroring
# `phylohist.loader.taxa.Tree.RELATED_AXES`/`CITED_AXES` exactly: a node
# reached through a "cited" axis is a cited entry (a synonymy entry, an
# earlier state this source cites) and never carries `material`/
# `contexts`/`ranges` (`phylohist.loader.material.null_material`), whether or
# not it has its own `authority` sub-object. `children` always resets to
# "not cited", regardless of the current node's own status. `authority`
# itself is never a recursion target: its `illustrations` locate a figure in
# the cited work and are never migrated (D4).
CHILD_LIST_KEYS = [
  ('children', False),
  ('synonyms', True),
  ('non', True),
  ('removed', True),
  ('or', False),
  ('parents', False),
  ('altPlacements', False),
]
CHILD_SINGLE_KEYS = [
  ('moved', True),
  ('corrected', True),
  ('substituted', True),
  ('translated', True),
  ('lapsus', False),
  ('lapsusFor', False),
]


# -- --compact: merge runs of number-only entries ----------------------------

# The only fields a material entry may carry and still be merged into a run.
COMPACTABLE_KEYS = frozenset({'catalogNumbers', 'role', 'context'})


def _has_comment(obj):
  """True when a ruamel node carries a comment of its own (plain Python
  objects never do), which a merge would drop."""
  ca = getattr(obj, 'ca', None)
  return bool(ca and (ca.comment or any(ca.items.values())))


def _run_key(entry):
  """`(role, context)` when `entry` carries nothing but its numbers, a role
  and a context, else `None`: an entry with any other field, no numbers or
  a comment of its own never joins or extends a run."""
  if not isinstance(entry, dict) or not set(entry) <= COMPACTABLE_KEYS:
    return None
  numbers = entry.get('catalogNumbers')
  if not isinstance(numbers, list) or not numbers:
    return None
  if _has_comment(entry) or _has_comment(numbers):
    return None
  return entry.get('role'), entry.get('context')


def compact_material(material):
  """Merge, in place, each run of consecutive entries of one node's
  `material` list that carry only `catalogNumbers`, the same `role` (or
  none) and the same `context` (or none). The first entry of a run keeps
  its place and gains the later entries' `catalogNumbers` in order (a range
  pair `[a, b]` is an element like any other); the later entries are
  deleted. Returns how many entries were removed. Works on plain lists and
  dicts and on ruamel's round-trip types alike."""
  removed = 0
  i = 0
  while i < len(material):
    key = _run_key(material[i])
    if key is None:
      i += 1
      continue
    while i + 1 < len(material) and _run_key(material[i + 1]) == key:
      material[i]['catalogNumbers'].extend(material[i + 1]['catalogNumbers'])
      del material[i + 1]
      removed += 1
    i += 1
  return removed


def fold(s):
  """Case- and space-fold a string for identity comparison."""
  return re.sub(r'\s+', '', s).lower()


def slugify(text):
  s = str(text).strip().lower()
  s = re.sub(r'[^a-z0-9]+', '-', s)
  s = s.strip('-')
  s = re.sub(r'-{2,}', '-', s)
  return s or 'ctx'


SENTENCE_LIKE_RE = re.compile(r'[,;]| the | of | by | from | in |museum|collection|specimen|lent')


def looks_sentence_like(s):
  if len(s) > 30 and s.count(' ') >= 3:
    return True
  if SENTENCE_LIKE_RE.search(s.lower()) and len(s) > 20:
    return True
  return False


def _comment_text(token):
  if token is None:
    return None
  text = getattr(token, 'value', None)
  if text is None:
    return None
  text = text.strip()
  if text.startswith('#'):
    text = text[1:].strip()
  return text or None


def map_value_comment(mapping, key):
  """The trailing end-of-line comment on `key: value` in a CommentedMap,
  if any -- e.g. `holotype: USNM 90773  # two counterparts`."""
  ca = getattr(mapping, 'ca', None)
  if ca is None:
    return None
  item = ca.items.get(key)
  if not item:
    return None
  return _comment_text(item[2])


def seq_item_comment(seq, index):
  """The trailing end-of-line comment on one CommentedSeq item, if any --
  e.g. `- MCZ 591  # ten specimens from SH-1`."""
  ca = getattr(seq, 'ca', None)
  if ca is None:
    return None
  item = ca.items.get(index)
  if not item:
    return None
  return _comment_text(item[0])


def to_str(x):
  if isinstance(x, bool):
    return str(x)
  return str(x)


class Todo:
  __slots__ = ('where', 'message')

  def __init__(self, where, message):
    self.where = where
    self.message = message

  def __str__(self):
    return f'{self.where}: {self.message}'


class FileStats:
  def __init__(self, path):
    self.path = path
    self.entries = 0
    self.contexts = 0
    self.figures = 0
    self.ranges = 0
    self.hoisted = []  # list of hoisted context keys
    self.changed = False
    self.diff_lines = 0


class Migrator:
  def __init__(self, root):
    self.root = root
    self.yaml = make_yaml()
    self.todos = []  # list[Todo]
    self.file_stats = {}  # path -> FileStats
    # source id (tree file stem) -> {'path', 'doc', 'orig_text', 'loaded'}
    self.tree_registry = {}

  # -- generic helpers ---------------------------------------------------

  def add_todo(self, where, message):
    self.todos.append(Todo(where, message))

  def node_label(self, node):
    return (
      node.get('taxon')
      or node.get('openTaxon')
      or node.get('affTaxon')
      or node.get('cfTaxon')
      or '?'
    )

  # -- discovery -----------------------------------------------------

  def discover_tree_files(self):
    paths = []
    paths += sorted(glob.glob(os.path.join(self.root, 'data', 'trees', '*.yaml')))
    paths += sorted(glob.glob(os.path.join(self.root, 'drafts', '*.yaml')))
    return paths

  def stem(self, path):
    return os.path.splitext(os.path.basename(path))[0]

  def load_tree(self, path):
    stem = self.stem(path)
    if stem in self.tree_registry:
      return self.tree_registry[stem]
    with open(path, encoding='utf-8') as f:
      orig_text = f.read()
    doc = self.yaml.load(orig_text)
    entry = {'path': path, 'doc': doc, 'orig_text': orig_text}
    self.tree_registry[stem] = entry
    self.file_stats[path] = FileStats(path)
    return entry

  def get_or_load_by_stem(self, stem):
    if stem in self.tree_registry:
      return self.tree_registry[stem]
    path = os.path.join(self.root, 'data', 'trees', stem + '.yaml')
    if not os.path.exists(path):
      return None
    return self.load_tree(path)

  # -- rule 1: node-level `specimens` -------------------------------------

  def convert_node_specimens(self, specimens, where):
    """Returns (entries list, block_repository or None)."""
    entries = []
    block_repo = specimens.get('repository')
    for role_key, value in specimens.items():
      if role_key == 'repository':
        continue
      role = ROLE_SINGULAR.get(role_key)
      if role_key not in ROLE_SINGULAR:
        self.add_todo(where, f"unrecognised specimens role key '{role_key}'; entry has no role")
      is_list = isinstance(value, list)
      items = value if is_list else [value]
      n = len(items)

      # An ellipsis always sits between two catalog numbers in this
      # corpus (x, ..., y): merge the three into one range-pair entry
      # `catalogNumbers: [[x, y]]`, role kept, no TODO. `merges` maps
      # the ellipsis's own index to the (prev, next) indices it
      # consumes; an ellipsis with no neighbour on either side (not
      # seen in practice) falls back to the old drop-and-TODO path.
      merges = {}
      consumed = set()
      if is_list:
        for idx, item in enumerate(items):
          if isinstance(item, str) and item.strip() in ELLIPSES and 0 < idx < n - 1:
            merges[idx] = (idx - 1, idx + 1)
            consumed.update((idx - 1, idx, idx + 1))

      idx = 0
      while idx < n:
        if idx in merges:
          prev_idx, next_idx = merges[idx]
          x, y = to_str(items[prev_idx]), to_str(items[next_idx])
          comment = seq_item_comment(value, idx)
          entry = {'catalogNumbers': [[x, y]]}
          if role:
            entry['role'] = role
          if comment:
            entry['notes'] = comment
          entries.append(entry)
          if block_repo:
            entry['repository'] = block_repo
          idx = next_idx + 1
          continue
        if idx in consumed:
          idx += 1
          continue
        item = items[idx]
        if is_list:
          comment = seq_item_comment(value, idx)
        else:
          comment = map_value_comment(specimens, role_key)
        entry = self._convert_specimen_item(item, role, where, role_key, comment)
        if entry is not None:
          if block_repo:
            entry['repository'] = block_repo
          entries.append(entry)
        idx += 1
    return entries

  def _convert_specimen_item(self, item, role, where, role_key, comment=None):
    # 2-element list -> range pair
    if isinstance(item, (list, CommentedSeq)) and len(item) == 2:
      a, b = to_str(item[0]), to_str(item[1])
      entry = {'catalogNumbers': [[a, b]]}
    elif isinstance(item, str) and item.strip() in ELLIPSES:
      suffix = f' (comment on the ellipsis: {comment!r})' if comment else ''
      self.add_todo(where, f'ellipsis in {role_key}: needs [from, to] pair and count{suffix}')
      return None
    else:
      s = to_str(item)
      if not any(ch.isdigit() for ch in s):
        entry = {'label': s}
        self.add_todo(
          where, f'{role_key}: free-text item with no catalog number treated as label: {s!r}'
        )
      else:
        entry = {'catalogNumbers': [s]}
        if looks_sentence_like(s):
          self.add_todo(
            where,
            f'{role_key}: catalog number {s!r} looks like free text, not a specimen '
            f'number; consider `label` instead',
          )
    if role:
      entry['role'] = role
    if comment:
      entry['notes'] = comment
    return entry

  # -- rule 2: occurrence-level `specimens` -------------------------------

  def convert_occurrence_specimens(self, specimens, context_key, where):
    entries = []
    for first_key, first_val in specimens.items():
      if first_key in ROLE_SINGULAR:
        role_key = first_key
        role = ROLE_SINGULAR[role_key]
        # role -> REPO -> ids  OR role -> [ids] (no repo)
        if isinstance(first_val, dict):
          for repo, ids in first_val.items():
            entries += self._occ_ids_to_entries(repo, ids, role, role_key, context_key, where)
        elif isinstance(first_val, list):
          entries += self._occ_ids_to_entries('', first_val, role, role_key, context_key, where)
        else:
          entries += self._occ_ids_to_entries('', [first_val], role, role_key, context_key, where)
      else:
        # REPO -> role -> ids
        repo = first_key
        if isinstance(first_val, dict):
          for role_key, ids in first_val.items():
            role = ROLE_SINGULAR.get(role_key)
            if role_key not in ROLE_SINGULAR:
              self.add_todo(
                where, f"unrecognised occurrence specimens role '{role_key}' under repo '{repo}'"
              )
            entries += self._occ_ids_to_entries(repo, ids, role, role_key, context_key, where)
        else:
          entries += self._occ_ids_to_entries(
            repo, first_val, None, 'unspecified', context_key, where
          )
    return entries

  def _occ_ids_to_entries(self, repo, ids, role, role_key, context_key, where):
    if not isinstance(ids, list):
      ids = [ids]
    # Holotypes are singular (D2): combine multiple ids into one entry.
    if role == 'holotype' and len(ids) > 1:
      nums = []
      for i in ids:
        if isinstance(i, (list, CommentedSeq)) and len(i) == 2:
          nums.append([self._occ_num(repo, i[0]), self._occ_num(repo, i[1])])
        else:
          nums.append(self._occ_num(repo, i))
          self._flag_locator_like(nums[-1], role_key, where)
      self.add_todo(
        where, f'holotype has {len(ids)} catalog numbers ({nums}); verify part/counterpart or split'
      )
      entry = {'catalogNumbers': nums, 'role': 'holotype', 'context': context_key}
      return [entry]
    entries = []
    for i in ids:
      if isinstance(i, (list, CommentedSeq)) and len(i) == 2:
        num = [self._occ_num(repo, i[0]), self._occ_num(repo, i[1])]
        entry = {'catalogNumbers': [num], 'context': context_key}
      else:
        num = self._occ_num(repo, i)
        self._flag_locator_like(num, role_key, where)
        entry = {'catalogNumbers': [num], 'context': context_key}
      if role:
        entry['role'] = role
      entries.append(entry)
    return entries

  def _flag_locator_like(self, num, role_key, where):
    if looks_sentence_like(num) or re.search(r'\b(plate|page|fig)', num, re.I):
      self.add_todo(
        where,
        f'{role_key}: catalog number {num!r} looks like a figure locator or free text, '
        f'not a specimen number; consider `label` (+ `holder`) instead (cf. D5 Rievers 1961)',
      )

  def _occ_num(self, repo, i):
    s = to_str(i)
    if repo:
      return f'{repo} {s}'
    return s

  # -- rule 3: occurrences -> contexts / range ----------------------------

  def convert_occurrences(self, node, occurrences, where, used_slugs):
    """Returns (material_entries, node_contexts dict, range_dict_or_None)."""
    material_entries = []
    node_contexts = {}
    range_result = None
    range_count = 0
    for i, occ in enumerate(occurrences):
      occ = dict(occ)  # shallow copy to inspect; original stays for specimens extraction
      has_unit = 'unit' in occ
      location = occ.get('location')
      has_location = bool(location)
      one_location = has_location and (not isinstance(location, list) or len(location) == 1)
      has_specimens = 'specimens' in occ and occ['specimens']
      has_biozone = 'biozone' in occ or 'biozones' in occ
      has_time = any(k in occ for k in TIME_FIELD_KEYS | LOCAL_TIME_FIELD_KEYS)

      # A distribution statement, not specimen provenance (D1): either
      # no unit/location/specimens at all, or a period/series/stage
      # with a location but no unit, specimens or biozone -- the
      # latter is D1's own Dehm 1961 example of why a range's `regions`
      # exists.
      is_plain_range = not has_unit and not has_location and not has_specimens
      is_dated_range = (
        has_time and not has_unit and not has_specimens and not has_biozone and one_location
      )

      if is_plain_range or is_dated_range:
        range_count += 1
        if range_count > 1 or range_result is not None:
          self.add_todo(
            where,
            f'occurrence[{i}] also qualifies as range but node already has one; '
            'converted to context instead',
          )
          ctx_key, ctx = self._occurrence_to_context(occ, i, used_slugs, where)
          node_contexts[ctx_key] = ctx
          continue
        if is_dated_range:
          range_result = self._occurrence_to_dated_range(occ, where)
        else:
          range_result = self._occurrence_to_range(occ)
        continue

      ctx_key, ctx = self._occurrence_to_context(occ, i, used_slugs, where)
      node_contexts[ctx_key] = ctx

      specimens = occ.get('specimens')
      if specimens:
        material_entries += self.convert_occurrence_specimens(specimens, ctx_key, where)

    return material_entries, node_contexts, range_result

  def _occurrence_to_context(self, occ, i, used_slugs, where):
    if occ.get('location'):
      base = occ['location'][0] if isinstance(occ['location'], list) else occ['location']
    elif occ.get('unit'):
      base = occ['unit'][0] if isinstance(occ['unit'], list) else occ['unit']
    else:
      base = f'ctx-{i}'
    slug = slugify(base)
    key = slug
    n = 2
    while key in used_slugs:
      key = f'{slug}-{n}'
      n += 1
    used_slugs.add(key)

    ctx = {}
    for k, v in occ.items():
      if k in CONTEXT_EXCLUDE:
        continue
      if k == 'unit':
        unit = list(v) if isinstance(v, list) else [v]
        if 'subunit' in occ:
          unit = [occ['subunit']] + unit
        if 'superunit' in occ:
          unit = unit + [occ['superunit']]
        ctx['unit'] = unit
      elif k in ('subunit', 'superunit'):
        continue  # folded into unit above
      elif k == 'section':
        pass  # dropped; TODO'd below
      else:
        ctx[k] = v
    if 'unit' not in ctx and ('subunit' in occ or 'superunit' in occ):
      unit = []
      if 'subunit' in occ:
        unit.append(occ['subunit'])
      if 'superunit' in occ:
        unit.append(occ['superunit'])
      ctx['unit'] = unit
    if 'section' in occ:
      self.add_todo(
        where,
        f"context '{key}': occurrence had a 'section' field ({occ['section']!r}); "
        'no target field, needs manual placement',
      )

    if isinstance(ctx.get('inferred'), dict):
      inferred = dict(ctx['inferred'])
      filtered = {k: v for k, v in inferred.items() if k in INFERRED_ALLOWED_KEYS}
      dropped = {k: v for k, v in inferred.items() if k not in INFERRED_ALLOWED_KEYS}
      if dropped:
        for k, v in dropped.items():
          if k not in ctx:
            ctx[k] = v
            self.add_todo(
              where,
              f"context '{key}': 'inferred.{k}' ({v!r}) is not part of inferredContext "
              f"(D1); moved to context.{k} directly, losing the 'this is inferred, not "
              f"printed' marking -- verify by hand",
            )
          else:
            self.add_todo(
              where,
              f"context '{key}': 'inferred.{k}' ({v!r}) is not part of inferredContext "
              f'(D1) and context already has its own {k!r}; dropped, verify by hand',
            )
      if filtered:
        ctx['inferred'] = filtered
      else:
        del ctx['inferred']
    return key, ctx

  def _occurrence_to_range(self, occ):
    rng = {}
    for k, v in occ.items():
      if k in CONTEXT_EXCLUDE:
        continue
      rng[k] = v
    return rng

  def _occurrence_to_dated_range(self, occ, where):
    """A period/series/stage-plus-location occurrence with no unit, no
    specimens and no biozone: a distribution statement, not specimen
    provenance (D1's Dehm 1961 note). Only the time fields, `notes` and
    `location` (as `regions`) travel; anything else present is
    unexpected for this shape and gets a TODO rather than being
    silently dropped."""
    rng = {}
    for k in TIME_FIELD_KEYS | LOCAL_TIME_FIELD_KEYS:
      if k in occ:
        rng[k] = occ[k]
    if 'notes' in occ:
      rng['notes'] = occ['notes']
    location = occ.get('location')
    if location:
      rng['regions'] = list(location) if isinstance(location, list) else [location]
    handled = TIME_FIELD_KEYS | LOCAL_TIME_FIELD_KEYS | {'notes', 'location'} | CONTEXT_EXCLUDE
    leftover = {k: v for k, v in occ.items() if k not in handled}
    if leftover:
      self.add_todo(
        where,
        f"range (from a period/location occurrence, D1's Dehm 1961 note): field(s) "
        f'{sorted(leftover)} have no target here and were dropped; verify by hand',
      )
    return rng

  # -- rule 4: node-level illustrations, normalised in place ---------------

  def convert_illustrations(self, illustrations, where):
    normalised = []
    for ill in illustrations:
      fig = {}
      extra_todo = []
      for k, v in ill.items():
        if k in FIGURE_LOCATOR_KEYS or k in FIGURE_ALLOWED_EXTRA:
          fig[k] = v
        elif k == 'pages':
          extra_todo.append(f"'pages' key inside illustration ({v!r})")
        elif k in ('source', 'location', 'collectedFrom'):
          extra_todo.append(f"'{k}' key inside illustration ({v!r}), dropped (D4: gone)")
        else:
          extra_todo.append(f"unrecognised illustration key '{k}' ({v!r})")
      if extra_todo:
        self.add_todo(where, 'figure conversion: ' + '; '.join(extra_todo))
      normalised.append(fig)
    return normalised

  # -- per-node walk -------------------------------------------------------

  def process_node(self, node, file_label, stats, file_context_registry, is_cited=False):
    if not isinstance(node, dict):
      return
    taxon = self.node_label(node)
    where = f'{file_label}:{taxon}'

    if is_cited:
      # A cited entry (a synonymy entry, an earlier state this source
      # cites) locates the CITED work's own material inside its own
      # `authority`; it never carries `material`/`contexts`/`ranges`
      # itself (phylohist.loader.material.null_material), and its
      # `illustrations` locate a figure in the cited work, so they are left
      # exactly as printed.
      legacy_here = [k for k in ('specimens', 'occurrences', 'illustrations') if k in node]
      if legacy_here:
        if 'specimens' in node or 'occurrences' in node:
          self.add_todo(
            where,
            f'cited entry (synonymy/earlier-state) unexpectedly carries '
            f'{"/".join(legacy_here)}; left untouched, needs manual review',
          )
      for key, cited in CHILD_LIST_KEYS:
        if key in node and isinstance(node[key], list):
          for child in node[key]:
            self.process_node(child, file_label, stats, file_context_registry, cited)
      for key, cited in CHILD_SINGLE_KEYS:
        if key in node and isinstance(node[key], dict):
          self.process_node(node[key], file_label, stats, file_context_registry, cited)
      return

    material_entries = []
    node_contexts = {}
    range_result = None
    changed = False

    # Figure out where the legacy blob sat so the new fields can take
    # roughly its place (rule 6: preserve node order for everything else).
    legacy_keys_present = [k for k in ('specimens', 'occurrences', 'illustrations') if k in node]
    insert_pos = None
    if legacy_keys_present and isinstance(node, CommentedMap):
      keys = list(node.keys())
      insert_pos = min(keys.index(k) for k in legacy_keys_present)

    if 'specimens' in node and isinstance(node['specimens'], dict):
      material_entries += self.convert_node_specimens(node['specimens'], where)
      del node['specimens']
      changed = True

    if 'occurrences' in node and isinstance(node['occurrences'], list):
      used_slugs = set()
      occ_material, occ_contexts, occ_range = self.convert_occurrences(
        node, node['occurrences'], where, used_slugs
      )
      material_entries += occ_material
      node_contexts.update(occ_contexts)
      range_result = occ_range
      del node['occurrences']
      changed = True

    # The node-level list keeps its name and place; only its entries are
    # normalised (a re-run changes nothing).
    if 'illustrations' in node and isinstance(node['illustrations'], list):
      old = node['illustrations']
      normalised = self.convert_illustrations(old, where)
      stats.figures += len(normalised)
      if normalised != list(old):
        node['illustrations'] = normalised
        changed = True

    # Insert the new fields at the old blob's position, in a fixed order,
    # so the rest of the node's keys keep their relative order.
    def set_field(key, value):
      nonlocal pos
      if isinstance(node, CommentedMap):
        node.insert(pos, key, value)
        pos += 1
      else:
        node[key] = value

    pos = insert_pos if insert_pos is not None else len(node)
    if material_entries:
      set_field('material', material_entries)
      stats.entries += len(material_entries)
    if node_contexts:
      set_field('contexts', node_contexts)
      stats.contexts += len(node_contexts)
      file_context_registry.append((node, taxon))
    if range_result is not None:
      set_field('ranges', [range_result])
      stats.ranges += 1

    if changed:
      stats.changed = True

    # recurse
    for key, cited in CHILD_LIST_KEYS:
      if key in node and isinstance(node[key], list):
        for child in node[key]:
          self.process_node(child, file_label, stats, file_context_registry, cited)
    for key, cited in CHILD_SINGLE_KEYS:
      if key in node and isinstance(node[key], dict):
        self.process_node(node[key], file_label, stats, file_context_registry, cited)

  # -- cross-node hoisting within one file --------------------------------

  def hoist_contexts(self, doc, file_context_registry, stats):
    import json

    groups = defaultdict(list)  # content json -> list[(node, local_key)]
    for node, _taxon in file_context_registry:
      for local_key, ctx in list(node.get('contexts', {}).items()):
        content = json.dumps(ctx, sort_keys=True, default=str)
        groups[content].append((node, local_key, ctx))

    file_top_keys = set()
    if isinstance(doc, dict) and doc.get('contexts'):
      file_top_keys.update(doc['contexts'].keys())

    for occurrences in groups.values():
      if len({id(node) for node, _, _ in occurrences}) < 2:
        continue
      canonical_key = occurrences[0][1]
      n = 2
      while canonical_key in file_top_keys:
        canonical_key = f'{occurrences[0][1]}-{n}'
        n += 1
      file_top_keys.add(canonical_key)

      if 'contexts' not in doc or doc.get('contexts') is None:
        self._insert_top_level(doc, 'contexts', {})
      doc['contexts'][canonical_key] = occurrences[0][2]
      stats.hoisted.append(canonical_key)

      for node, local_key, _ctx in occurrences:
        # retarget any material entries on this node using local_key
        for entry in node.get('material', []):
          ref = entry.get('context')
          ref_key = ref['key'] if isinstance(ref, dict) else ref
          if ref_key == local_key:
            if isinstance(ref, dict):
              ref['key'] = canonical_key
            else:
              entry['context'] = canonical_key
        del node['contexts'][local_key]
        if not node['contexts']:
          del node['contexts']

  @staticmethod
  def _insert_top_level(doc, key, value):
    """Put a new top-level `key` after the last tree list (contexts)."""
    pos = len(doc)
    for i, existing in enumerate(doc.keys()):
      if existing in ('taxonomies', 'phylogenies', 'assumptions'):
        pos = i + 1
    doc.insert(pos, key, value)

  # -- repositories list ------------------------------------------------------

  def add_file_repositories(self, path):
    """Write the top-level `repositories` list for a file that needs one,
    before `taxonomies`."""
    stem = self.stem(path)
    wanted = FILE_REPOSITORIES.get(stem)
    if wanted is None:
      return
    entry = self.load_tree(path)
    doc = entry['doc']
    if 'repositories' in doc:
      return
    seq = CommentedSeq(wanted)
    seq.fa.set_flow_style()
    doc.insert(list(doc.keys()).index('taxonomies'), 'repositories', seq)
    self.file_stats[path].changed = True

  # -- driver for one tree file --------------------------------------------

  def process_tree_file(self, path):
    entry = self.load_tree(path)
    doc = entry['doc']
    stats = self.file_stats[path]
    file_label = os.path.relpath(path, self.root)
    file_context_registry = []

    top_lists = []
    if isinstance(doc, dict):
      for key in ('taxonomies', 'assumptions'):
        if key in doc and isinstance(doc[key], list):
          top_lists.append(doc[key])
      for phylogeny in doc.get('phylogenies') or ():
        if isinstance(phylogeny, dict) and isinstance(phylogeny.get('tree'), dict):
          top_lists.append([phylogeny['tree']])

    for lst in top_lists:
      for node in lst:
        self.process_node(node, file_label, stats, file_context_registry)

    if file_context_registry:
      self.hoist_contexts(doc, file_context_registry, stats)

    return stats

  # -- rule 5: taxa.yaml holotype -> protologue node ----------------------

  def process_taxa_holotypes(self, taxa_path, sources_doc):
    with open(taxa_path, encoding='utf-8') as f:
      orig_text = f.read()
    doc = self.yaml.load(orig_text)
    stats = FileStats(taxa_path)
    self.file_stats[taxa_path] = stats

    for key, record in doc.items():
      if not isinstance(record, dict) or 'holotype' not in record:
        continue
      where = f'data/taxa.yaml:{key}'
      holotype = record['holotype']

      pairs = []
      for repo, ids in holotype.items():
        id_list = ids if isinstance(ids, list) else [ids]
        for i in id_list:
          pairs.append((repo, i))

      if len(pairs) != 1:
        self.add_todo(
          where,
          f'holotype has {len(pairs)} repository/id pairs ({dict(holotype)}); '
          'needs manual split, left in place',
        )
        continue
      repo, raw_id = pairs[0]
      num = f'{repo} {raw_id}' if repo else to_str(raw_id)
      num = ' '.join(to_str(num).split())  # normalise internal whitespace only

      source_id, explicit = self.resolve_source_id(record)
      if source_id is None:
        self.add_todo(
          where, 'no authority.source and no auth/year to derive one from; holotype left in place'
        )
        continue

      target = self.get_or_load_by_stem(source_id)
      if target is None:
        self.add_todo(
          where, f"tree file for source '{source_id}' not found; holotype left in place"
        )
        continue
      if sources_doc is not None and source_id not in sources_doc and not explicit:
        self.add_todo(
          where,
          f"derived source id '{source_id}' (from auth/year) not present in sources.yaml; "
          f'used it anyway since {source_id}.yaml exists',
        )

      node = self._find_protologue_node(target['doc'], key)
      if node is None:
        self.add_todo(
          where,
          f'no node with taxon: {key} and new: true in {source_id}.yaml; holotype left in place',
        )
        continue

      target_stats = self.file_stats.setdefault(target['path'], FileStats(target['path']))
      material = node.setdefault('material', [])
      existing_match = None
      possible_dupes = []
      for m in material:
        existing_nums = m.get('catalogNumbers') or []
        for en in existing_nums:
          if not isinstance(en, str):
            continue
          if m.get('role') == 'holotype' and fold(en) == fold(num):
            existing_match = m
          elif self._digit_suffix(en) == self._digit_suffix(num) and self._digit_suffix(num):
            possible_dupes.append((m, en))
      if existing_match is None:
        for m, en in possible_dupes:
          self.add_todo(
            where,
            f'node already has a material entry {en!r} (role={m.get("role")}) whose number '
            f"resembles '{num}' but doesn't match after case/space folding; possible "
            f'duplicate, verify by hand',
          )
      if existing_match is not None:
        del record['holotype']
        target_stats.changed = True
        continue

      material.append({'catalogNumbers': [num], 'role': 'holotype'})
      if not node.get('material'):
        node['material'] = material
      target_stats.entries += 1
      target_stats.changed = True
      del record['holotype']
      stats.changed = True

    return doc, orig_text, stats

  @staticmethod
  def _digit_suffix(s):
    m = re.findall(r'\d+', s)
    return m[-1] if m else ''

  def resolve_source_id(self, record):
    authority = record.get('authority')
    if isinstance(authority, dict) and authority.get('source'):
      return authority['source'], True
    auth = record.get('auth')
    year = record.get('year')
    if auth and year:
      candidate = f'{year}_{"_".join(to_str(a) for a in auth)}'
      return candidate, False
    return None, False

  def _find_protologue_node(self, doc, taxon_key):
    found = [None]

    def walk(node):
      if found[0] is not None:
        return
      if not isinstance(node, dict):
        return
      if node.get('taxon') == taxon_key and node.get('new') is True:
        found[0] = node
        return
      for key, _cited in CHILD_LIST_KEYS:
        if key in node and isinstance(node[key], list):
          for child in node[key]:
            walk(child)
            if found[0] is not None:
              return
      for key, _cited in CHILD_SINGLE_KEYS:
        if key in node and isinstance(node[key], dict):
          walk(node[key])

    top_lists = []
    if isinstance(doc, dict):
      for key in ('taxonomies', 'assumptions'):
        if key in doc and isinstance(doc[key], list):
          top_lists.append(doc[key])
    for lst in top_lists:
      for node in lst:
        walk(node)
        if found[0] is not None:
          break
    return found[0]

  # -- --compact -------------------------------------------------------------

  def compact_node(self, node):
    """`compact_material` over `node` and every node under it; returns the
    number of entries removed and the number seen before."""
    removed = seen = 0
    if not isinstance(node, dict):
      return removed, seen
    material = node.get('material')
    if isinstance(material, list):
      seen += len(material)
      removed += compact_material(material)
    for key, _cited in CHILD_LIST_KEYS:
      if isinstance(node.get(key), list):
        for child in node[key]:
          sub_removed, sub_seen = self.compact_node(child)
          removed += sub_removed
          seen += sub_seen
    for key, _cited in CHILD_SINGLE_KEYS:
      sub_removed, sub_seen = self.compact_node(node.get(key))
      removed += sub_removed
      seen += sub_seen
    return removed, seen

  def compact_tree_file(self, path):
    """Compact every node of one tree file; `(before, after)` counts of
    material entries. The parsed document changes only when it returns
    `before != after`, and only then does the caller write."""
    entry = self.load_tree(path)
    doc = entry['doc']
    top_nodes = []
    if isinstance(doc, dict):
      for key in ('taxonomies', 'assumptions'):
        if isinstance(doc.get(key), list):
          top_nodes += doc[key]
      for phylogeny in doc.get('phylogenies') or ():
        if isinstance(phylogeny, dict):
          top_nodes.append(phylogeny.get('tree'))
    removed = seen = 0
    for node in top_nodes:
      sub_removed, sub_seen = self.compact_node(node)
      removed += sub_removed
      seen += sub_seen
    return seen, seen - removed

  # -- writing --------------------------------------------------------------

  def dump(self, doc):
    buf = io.StringIO()
    self.yaml.dump(doc, buf)
    return buf.getvalue()

  def finalize_and_maybe_write(self, write):
    # tree files
    for entry in self.tree_registry.values():
      path = entry['path']
      stats = self.file_stats[path]
      new_text = self.dump(entry['doc'])
      if new_text == entry['orig_text']:
        stats.changed = False
        continue
      diff = list(
        difflib.unified_diff(entry['orig_text'].splitlines(), new_text.splitlines(), lineterm='')
      )
      stats.diff_lines = len(diff)
      stats.changed = True
      if write:
        with open(path, 'w', encoding='utf-8') as f:
          f.write(new_text)


def run(root, write, report):
  m = Migrator(root)

  sources_path = os.path.join(root, 'data', 'sources.yaml')
  sources_doc = None
  if os.path.exists(sources_path):
    sources_doc = m.yaml.load(open(sources_path, encoding='utf-8').read())

  # Phase 1: convert every tree/draft file that carries a legacy marker.
  for path in m.discover_tree_files():
    with open(path, encoding='utf-8') as f:
      text = f.read()
    if not LEGACY_MARKER_RE.search(text):
      continue
    m.process_tree_file(path)

  # Phase 1b: the `repositories` lists.
  for path in m.discover_tree_files():
    m.add_file_repositories(path)

  # Phase 2: taxa.yaml holotype -> protologue node (may load more tree files).
  taxa_path = os.path.join(root, 'data', 'taxa.yaml')
  taxa_doc, taxa_orig, taxa_stats = m.process_taxa_holotypes(taxa_path, sources_doc)

  # Phase 3: write / diff.
  m.finalize_and_maybe_write(write)

  new_taxa_text = m.dump(taxa_doc)
  if new_taxa_text != taxa_orig:
    diff = list(
      difflib.unified_diff(taxa_orig.splitlines(), new_taxa_text.splitlines(), lineterm='')
    )
    taxa_stats.diff_lines = len(diff)
    taxa_stats.changed = True
    if write:
      with open(taxa_path, 'w', encoding='utf-8') as f:
        f.write(new_taxa_text)
  else:
    taxa_stats.changed = False

  if report:
    print_report(m, root)

  return m


def run_compact(root, write):
  """The `--compact` pass over data/trees and drafts; prints per-file
  entry counts and returns `[(path, before, after)]` for changed files."""
  m = Migrator(root)
  changed = []
  for path in m.discover_tree_files():
    before, after = m.compact_tree_file(path)
    if before == after:
      continue
    changed.append((path, before, after))
    if write:
      with open(path, 'w', encoding='utf-8') as f:
        f.write(m.dump(m.tree_registry[m.stem(path)]['doc']))
  for path, before, after in sorted(changed, key=lambda c: c[1] - c[2], reverse=True):
    print(f'{os.path.relpath(path, root)}: {before} -> {after} entries')
  total_before = sum(c[1] for c in changed)
  total_after = sum(c[2] for c in changed)
  print(f'TOTAL over {len(changed)} changed files: {total_before} -> {total_after} entries')
  return changed


def print_report(m, root):
  print('=' * 78)
  print('MIGRATION REPORT')
  print('=' * 78)
  total_entries = total_contexts = total_figures = total_ranges = 0
  changed_files = 0
  for path in sorted(m.file_stats):
    stats = m.file_stats[path]
    if not (stats.entries or stats.contexts or stats.figures or stats.ranges or stats.changed):
      continue
    rel = os.path.relpath(path, root)
    changed_files += 1 if stats.changed else 0
    print(f'\n{rel}')
    print(
      f'  material entries: {stats.entries}   contexts: {stats.contexts}   '
      f'figures: {stats.figures}   ranges: {stats.ranges}'
    )
    if stats.hoisted:
      print(f'  hoisted to file-level contexts: {", ".join(stats.hoisted)}')
    print(
      f'  changed: {stats.changed}'
      + (f'  (diff: {stats.diff_lines} lines)' if stats.changed else '')
    )
    total_entries += stats.entries
    total_contexts += stats.contexts
    total_figures += stats.figures
    total_ranges += stats.ranges

  print('\n' + '-' * 78)
  print(
    f'TOTALS: {total_entries} material entries, {total_contexts} contexts, '
    f'{total_figures} figures, {total_ranges} ranges, {changed_files} files changed'
  )

  print('\n' + '-' * 78)
  print(f'TODOs ({len(m.todos)}):')
  for t in m.todos:
    print(f'  - {t}')
  print('-' * 78)


def main():
  ap = argparse.ArgumentParser(
    description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
  )
  ap.add_argument(
    '--root',
    default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    help="repository root (default: the parent of this script's directory)",
  )
  ap.add_argument('--write', action='store_true', help='write changed files (default: dry run)')
  ap.add_argument('--report', action='store_true', help='print the migration report')
  ap.add_argument(
    '--compact',
    action='store_true',
    help='merge consecutive number-only material entries instead of migrating',
  )
  args = ap.parse_args()

  if args.compact:
    run_compact(args.root, args.write)
  else:
    run(args.root, args.write, args.report)


if __name__ == '__main__':
  main()
