"""Loading the corpus into the object model.

`load()` reads every data file through `phylohist.loader.io`, registers
authors, publications and sources, builds the taxa, the sections and then every tree,
and returns the raw data with the tree roots per source. The scripts,
the tests and the extractor all come through here. Every integrity
problem is logged where it is found so that one run reports them all;
the load then fails with their count, unless the caller asks for the
data anyway. The exception is a record another record cannot be built
without (an authority's source, an author key): that ends the load where
it is missing (`io.fail`), whatever the caller asked, with what was
logged before it.
"""

import contextlib
import json
import logging

from . import material, nomenclature
from .io import DATA_DIR, TREE_DIR, LoadError, display_path, load_files
from .research import Author, Publication, Source
from .taxa import RANKS, Section, Taxon, Tree

logger = logging.getLogger(__name__)


def _basic_load(data, field, cls):
  logger.info(f'Loading {len(data[field])} {field}...')
  for item_key, item_data in data[field].items():
    cls.add(item_data, item_key)
  logger.info(f'...{field} loaded.')


def _load_sources(data):
  # An alias resolves its target on construction, so aliases load last,
  # wherever they sit in the file.
  logger.info(f'Loading {len(data["sources"])} sources...')
  deferred = []
  for source_key, source_data in data['sources'].items():
    if 'aliasOf' in source_data:
      deferred.append((source_key, source_data))
      continue
    Source.add(source_data, source_key)
  for source_key, source_data in deferred:
    Source.add(source_data, source_key)
  logger.info('...sources loaded.')


def _load_taxa(data):
  logger.info(f'Processing {len(data["taxa"])} taxa...')
  deferred = []
  deferring_fields = frozenset(
    {
      'altRankOf',
      'altSpellingOf',
      'vulgarSpellingOf',
    }
  )
  for taxon_key, taxon_data in data['taxa'].items():
    if taxon_data.keys() & deferring_fields:
      deferred.append((taxon_key, taxon_data))
      continue
    Taxon.add(taxon_data, taxon_key)
  for taxon_key, taxon_data in deferred:
    Taxon.add(taxon_data, taxon_key)
  logger.info('...taxa processed.')


def _report_merge_targets(data):
  for ref_key, opinion in data['trees'].items():
    for tax_tree in opinion.get('taxonomies', ()):
      if 'mergeInto' not in tax_tree:
        continue
      src, index = tax_tree['mergeInto']
      if src not in data['trees']:
        logger.error(
          f'{ref_key} has mergeInto target source "{src}", which does not exist',
        )
      elif index >= len(data['trees'][src].get('taxonomies', [])):
        logger.error(
          f'{ref_key} has mergeInto target "{src}"[{index}], but "{src}" '
          f'only has {len(data["trees"][src].get("taxonomies", []))} '
          'taxonomies',
        )


# A node's own branches, which `material.walk_document` visits as nodes of
# their own; `_source_ids` does not descend into them.
_NODE_BRANCHES = frozenset({'children', *(axis.name for axis in Tree.RELATED_AXES)})


def _source_ids(value, pointer=()):
  """``(pointer, key)`` for every source id under `value`, as the schema
  types them (`$defs/sourceId`): a `source` field, which is an authority's
  (a node's, `fixedBy`, an `emendedBy` or `restrictedBy` entry, a `by`, an
  editorial correction) or a `sameAs` link's, and the `sources` of a context."""
  if isinstance(value, dict):
    for field, item in value.items():
      if not pointer and field in _NODE_BRANCHES:
        continue
      if field == 'source' and isinstance(item, str):
        yield (*pointer, field), item
      elif field == 'sources' and isinstance(item, list):
        for index, key in enumerate(item):
          if isinstance(key, str):
            yield (*pointer, field, index), key
      else:
        yield from _source_ids(item, (*pointer, field))
  elif isinstance(value, list):
    for index, item in enumerate(value):
      yield from _source_ids(item, (*pointer, index))


def _report_cited_sources(data):
  """Every source id a tree file carries names a source record (an alias
  counts). The schema's pattern cannot tell a typo or a stale id from a
  key; only the registry can, and the store indexes these keys directly
  when it renders, so an unknown one is an error here with its path.
  `mergeInto` names a tree and is `_report_merge_targets`'s."""
  for ref_key, opinion in data['trees'].items():
    file_level = {k: v for k, v in opinion.items() if k not in ('taxonomies', 'phylogenies')}
    found = [(None, pointer, key) for pointer, key in _source_ids(file_level)]
    for path, node, _ in material.walk_document(opinion):
      found.extend((path, pointer, key) for pointer, key in _source_ids(node))
    for path, pointer, key in found:
      if Source.get(key) is None:
        where = f'{ref_key} at {path}' if path is not None else ref_key
        field = '/'.join(str(p) for p in pointer)
        logger.error(f'{where}: `{field}` names "{key}", which has no source record')


def _report_missing_protologues(data, roots):
  # A protologue is the source that names a taxon; if that source is one of
  # our trees, the taxon should show up flagged `new` in it. The keys each
  # tree uses come from a walk.
  used = {
    (node.taxon.key, source_key)
    for source_key, trees in roots.items()
    for root in trees
    for node in root.walk()
    if node.taxon is not None
  }
  missing = 0
  for taxon in Taxon._taxa.values():
    # Open taxa and derivative records have no protologue to flag.
    if taxon.name is None or taxon.derivative_of is not None:
      continue
    source = taxon.authority.source
    if source is None or source.canonical.key not in data['trees']:
      continue
    # An authority may cite its protologue's source by an alias.
    source = source.canonical
    if source.key not in Tree._new_index.get(taxon.key, ()):
      if (taxon.key, source.key) in used:
        # We recorded the taxon but did not acknowledge its new-ness.
        logger.error(f'Protologue not flagged: {taxon.key} in {source.key}')
        missing += 1
      else:
        # We have not recorded that part of the tree, which is fine.
        logger.debug(f'Protologue not recorded: {taxon.key} in {source.key}')
  logger.info(f'{missing} taxa with an unflagged protologue')


# The fields a taxa record and its protologue node both give, and the verb the
# message uses for the node's side.
_PROTOLOGUE_FIELDS = (
  ('rank', 'has'),
  ('pages', 'has'),
  ('illustrations', 'has'),
  ('citedAs', 'prints'),
  ('designation', 'prints'),
)


def _page_form(value):
  """`pages` as a comparable value: a number and its digits are one, and a
  bare locator is a one-entry list (the schema says `52` and `[52]` agree)."""
  if not isinstance(value, list):
    value = [value]
  return tuple(
    _page_form(v) if isinstance(v, list) else int(v) if isinstance(v, str) and v.isdigit() else v
    for v in value
  )


def _implicit_rank(node):
  """The rank a node leaves unsaid, as `Taxon` reads a record without one:
  a species when the name is lower-case, else a genus."""
  return 'species' if (node.taxon.name or '').islower() else 'genus'


def _same_protologue_value(field, record_value, node_value):
  if field == 'rank':
    # A node with no rank word is the record's null or `Unranked`.
    return record_value == node_value or (node_value is None and record_value == 'Unranked')
  if field == 'pages':
    # An inferred node's null has no page to agree with the record's.
    return node_value is not None and _page_form(record_value) == _page_form(node_value)
  return record_value == node_value


def _protologue_value(value):
  return 'none' if value is None else json.dumps(value, ensure_ascii=False)


def _report_protologue_mismatches(data, roots):
  # A record that gives its protologue page must agree with the node marked
  # new for it, on the fields that node declares; and it may not give a
  # field its tree file lists as unused.
  mismatches = 0
  for taxon in Taxon._taxa.values():
    if 'pages' not in taxon._data:
      continue
    source = taxon.authority.source
    if source is None or source.canonical.key not in data['trees']:
      continue
    source = source.canonical
    trees = roots.get(source.key, ())
    tree_file = display_path(TREE_DIR / f'{source.key}.yaml')
    where = f'taxa.yaml {taxon.key}'

    for field, _ in _PROTOLOGUE_FIELDS:
      if trees and field in trees[0].file_unused and taxon._data.get(field) is not None:
        logger.error(f'{where}: {field} given but {tree_file} lists it as unused')
        mismatches += 1

    nodes = (
      node
      for root in trees
      for node in root.walk()
      if node.is_primary and not node.is_cited and node.taxon is taxon and node.data.get('new')
    )
    for node in nodes:
      for field, verb in _PROTOLOGUE_FIELDS:
        if field == 'rank' and field not in node.data:
          if taxon.name is None or taxon.mineral:
            # An open form or bin has no name to read a rank from; its
            # record spells one, and `_report_rank_order` checks it
            # against the node's parent. A mineral has no rank at all,
            # and its record says so.
            continue
          # The node leaves a genus or species implicit; the record, which
          # has `pages`, spells its rank, and the two must agree.
          implied = _implicit_rank(node)
          if taxon._data.get('rank') != implied:
            logger.error(
              f'{where}: rank {_protologue_value(taxon._data.get("rank"))} but its '
              f'protologue node in {tree_file} implies "{implied}"'
            )
            mismatches += 1
          continue
        if field not in node.data:
          continue
        record_value, node_value = taxon._data.get(field), node.data[field]
        if _same_protologue_value(field, record_value, node_value):
          continue
        logger.error(
          f'{where}: {field} {_protologue_value(record_value)} but its protologue node '
          f'in {tree_file} {verb} {_protologue_value(node_value)}'
        )
        mismatches += 1
  logger.info(f'{mismatches} disagreements between a taxa record and its protologue node')


# The ranks whose order every source keeps: a genus holds subgenera and
# species, a species its subspecies and varieties. Above the genus group a
# source's scheme is its own (roadmap G8; Macleay 1821 lists classes under
# an order), so a node there says nothing about the ranks of its children.
_ORDERED_GROUPS = frozenset({'genus', 'subgenus', 'species', 'subspecies', 'variety'})


def _placed_rank(node):
  """The rank a node sits at: its printed rank word, or its record's where
  it gives none; `None` for a node written `rank: null`, which the source
  places with no rank, so that any rank may sit above or below it."""
  if 'rank' in node.data:
    return node.data['rank']
  return node.taxon.rank


def _report_rank_order(roots):
  # A child of a genus, subgenus or species in a taxonomy is at a rank
  # below its parent's. A node giving no rank of its own sits where its
  # record's rank says, so the record must agree with the tree: an open
  # form under a genus is a species, whatever its record says. A node
  # with a rank word is the protologue check's, and one written
  # `rank: null` stands outside the order.
  misplaced = 0
  for trees in roots.values():
    for root in trees:
      if root.tree_type != Tree.TYPE_TAXONOMY:
        continue
      for node in root.walk():
        if node.axis != 'children' or node.taxon is None or 'rank' in node.data:
          continue
        parent = node.parent
        while parent is not None and parent.taxon is None:
          parent = parent.parent
        if parent is None:
          continue
        above, own = _placed_rank(parent), node.taxon.rank
        if (above or '').lower() not in _ORDERED_GROUPS or (own or '').lower() not in RANKS:
          continue
        if RANKS[own.lower()] < RANKS[above.lower()]:
          continue
        logger.error(
          f'taxa.yaml {node.taxon.key}: rank {_protologue_value(own)} but the tree places '
          f'it under {parent.taxon.key} ({above}) at {node}'
        )
        misplaced += 1
  logger.info(f'{misplaced} taxa placed under a genus or species at no lower rank')


# The fields a section record and its protologue marker both give.
_SECTION_PROTOLOGUE_FIELDS = (
  ('pages', 'has'),
  ('citedAs', 'prints'),
  ('designation', 'prints'),
)


def _report_section_protologues(data, roots):
  # A section record that gives `pages` must agree with the `sectionStart`
  # marker flagged `new` for it in its authority's trees, on the fields that
  # marker declares.
  mismatches = 0
  for section in Section._sections.values():
    if 'pages' not in section._data:
      continue
    source = section.authority.source if section.authority else None
    if source is None or source.canonical.key not in data['trees']:
      continue
    source = source.canonical
    tree_file = display_path(TREE_DIR / f'{source.key}.yaml')
    where = f'sections.yaml {section.key}'
    markers = [
      node.section_start_marker
      for root in roots.get(source.key, ())
      for node in root.walk()
      if node.section_start is section and node.section_start_marker.get('new')
    ]
    if not markers:
      logger.warning(f'Section protologue not flagged: {section.key} in {source.key}')
      continue
    for marker in markers:
      for field, verb in _SECTION_PROTOLOGUE_FIELDS:
        if field not in marker:
          continue
        record_value, node_value = section._data.get(field), marker[field]
        if _same_protologue_value(field, record_value, node_value):
          continue
        logger.error(
          f'{where}: {field} {_protologue_value(record_value)} but its protologue marker '
          f'in {tree_file} {verb} {_protologue_value(node_value)}'
        )
        mismatches += 1
  logger.info(f'{mismatches} disagreements between a section record and its protologue marker')


def _report_lapsus_records(roots):
  # A record that exists because of a slip of the pen appears under
  # `lapsus`, and elsewhere only as a synonymy entry marked `lapsusFor`.
  nodes = [node for trees in roots.values() for root in trees for node in root.walk()]
  lapsus = {node.taxon.key for node in nodes if node.axis == 'lapsus' and node.taxon}
  for node in nodes:
    if node.taxon is None or node.taxon.key not in lapsus or node.axis == 'lapsus':
      continue
    if 'lapsusFor' not in node.data:
      logger.error(f'Lapsus record {node.taxon.key} at {node} is not under `lapsus` or `lapsusFor`')


def _load_trees(data):
  """Build every tree; return ``{source_key: [roots in position order]}``."""
  logger.info(f'Processing {len(data["trees"])} opinions...')

  roots = {}
  for ref_key, opinion in data['trees'].items():
    logger.debug(f'Processing opinions from "{ref_key}"')
    if Source.get(ref_key) is None:
      # A tree needs its source record: every node hashes by it. Skipped,
      # not built half-way, so a draft without its record fails the load
      # cleanly instead of crashing it.
      logger.error(f'Tree file "{ref_key}" has no source record; its trees are skipped')
      continue
    if Source.get(ref_key).canonical.key != ref_key:
      logger.error(
        f'Tree file "{ref_key}" is named by an alias; name it '
        f'"{Source.get(ref_key).canonical.key}". Its trees are skipped',
      )
      continue
    roots[ref_key] = []
    file_meta = {
      'file_contexts': opinion.get('contexts') or {},
      'file_unused': tuple(opinion.get('unused') or ()),
      'file_prefixes': dict(opinion.get('prefixes') or {}),
      'file_locality_register': opinion.get('localityRegister'),
    }

    position = 0
    for tax_tree in opinion.get('taxonomies', {}):
      metadata = {
        'source_key': ref_key,
        'position': position,
        'type': Tree.TYPE_TAXONOMY,
        **file_meta,
      }
      position += 1

      t = Tree(tax_tree, metadata)
      roots[ref_key].append(t)
      logger.debug(f'Processed tree {t}')

    for phy_tree in opinion.get('phylogenies', {}):
      metadata = {
        'source_key': ref_key,
        'position': position,
        **file_meta,
      }
      position += 1

      metadata['type'] = phy_tree['treeType'].lower()

      if 'characteristics' in phy_tree:
        metadata['characteristics'] = phy_tree['characteristics']
      if 'notes' in phy_tree:
        metadata['notes'] = phy_tree['notes']

      t = Tree(phy_tree['tree'], metadata)
      roots[ref_key].append(t)

  logger.info('...opinions processed.')

  _report_merge_targets(data)
  _report_cited_sources(data)
  _report_missing_protologues(data, roots)
  _report_protologue_mismatches(data, roots)
  _report_rank_order(roots)
  _report_section_protologues(data, roots)
  _report_lapsus_records(roots)
  _report_material(data)
  _report_nomenclature(data)
  return roots


def _log_material(level, message):
  (logger.error if level == 'error' else logger.warning)(message)


def _report_material(data):
  """Run every `material.py` check over the registry, then over every
  opinion and its nodes, logging each at its level with the source key
  and, for a per-node check, the node's path, then the `sameAs` links
  across the whole corpus."""
  repositories = data.get('repositories') or {}
  for level, message in material.registry_links(repositories):
    _log_material(level, f'repositories: {message}')

  for source_key, opinion in data['trees'].items():
    file_prefixes = opinion.get('prefixes') or {}
    locality_register = opinion.get('localityRegister')
    file_contexts = opinion.get('contexts') or {}

    for level, message in material.unreferenced_file_contexts(opinion):
      _log_material(level, f'{source_key}: {message}')
    for level, message in material.unused_fields(opinion):
      _log_material(level, f'{source_key}: {message}')
    for level, message in material.file_prefixes(opinion, repositories):
      _log_material(level, f'{source_key}: {message}')
    for level, message in material.locality_objects(
      file_contexts, file_prefixes, locality_register, repositories
    ):
      _log_material(level, f'{source_key}: {message}')
    for level, message in material.context_tentatives(file_contexts, file_level=True):
      _log_material(level, f'{source_key}: {message}')

    for path, node, is_cited in material.walk_document(opinion):
      where = f'{source_key} at {path}'
      node_contexts = node.get('contexts') or {}
      for level, message in material.context_refs(node, node_contexts, file_contexts):
        _log_material(level, f'{where}: {message}')
      for level, message in material.figure_refs(node, is_cited):
        _log_material(level, f'{where}: {message}')
      for level, message in material.number_entries(node, file_prefixes, repositories):
        _log_material(level, f'{where}: {message}')
      for level, message in material.locality_objects(
        node_contexts, file_prefixes, locality_register, repositories, node.get('material') or ()
      ):
        _log_material(level, f'{where}: {message}')
      for level, message in material.context_tentatives(node_contexts):
        _log_material(level, f'{where}: {message}')
      for level, message in material.range_tentatives(node):
        _log_material(level, f'{where}: {message}')
      for level, message in material.cast_refs(node):
        _log_material(level, f'{where}: {message}')
      for level, message in material.null_material(node, is_cited):
        _log_material(level, f'{where}: {message}')

  for level, message in material.same_as_links(data['trees'], _source_year):
    _log_material(level, message)


def _source_year(source_key):
  """A source's publication year, 9999 for a work in preparation, `None`
  for a key with no source record."""
  source = Source.get(source_key)
  if source is None:
    return None
  return 9999 if source.in_preparation else source.year


def _report_nomenclature(data):
  """Run every `nomenclature.py` check over every opinion's nodes, logging
  each at its level with the source key and the node's path, then the one
  check across the whole corpus."""
  for source_key, opinion in data['trees'].items():
    for path, node, is_cited in material.walk_document(opinion):
      where = f'{source_key} at {path}'
      for check, args in (
        (nomenclature.compared_links, (node, Taxon.get)),
        (nomenclature.quoted_parent, (node, Taxon.get)),
        (nomenclature.mineral_fields, (node, Taxon.get)),
        (nomenclature.role_uncertain, (node,)),
        (nomenclature.type_node, (node, is_cited)),
        (nomenclature.children_null, (node, is_cited)),
        (nomenclature.inferred_pages, (node,)),
      ):
        for level, message in check(*args):
          _log_material(level, f'{where}: {message}')
  for level, message in nomenclature.compared_link_conflicts(data['trees'].items()):
    _log_material(level, message)


class ErrorCount(logging.Handler):
  """Counts the records at ERROR or above that pass through the logger it
  is attached to; the loader's checks report by logging, and this is how
  a caller learns whether any fired."""

  def __init__(self):
    super().__init__(level=logging.ERROR)
    self.count = 0

  def emit(self, record):
    self.count += 1


@contextlib.contextmanager
def counting_errors():
  """A block in which every error the package logs is counted; yields the
  counter. Records propagate to the package logger from every module
  under it, so the counter sits there."""
  counter = ErrorCount()
  package = logging.getLogger(__name__.partition('.')[0])
  package.addHandler(counter)
  try:
    yield counter
  finally:
    package.removeHandler(counter)


def load(drafts=False, tolerate=False, data_dir=DATA_DIR, fast=False):
  """``(data, roots)``: the loaded data files and ``{source: [roots]}``.
  Raises `LoadError` when any integrity check logged an error, with the
  count, so a caller cannot take a broken load for a good one; with
  ``tolerate`` the data comes back regardless, for a caller that wants
  to see everything before stopping. A record the load cannot continue
  without ends it at once, ``tolerate`` or not (`io.fail`). ``data_dir`` and ``fast`` are
  `load_files`'s: another directory shaped like `data/`, and libyaml."""
  with counting_errors() as errors:
    data = load_files(drafts=drafts, data_dir=data_dir, fast=fast)
    material.set_repository_registry(data.get('repositories'))
    for field, cls in (
      ('authors', Author),
      ('publications', Publication),
    ):
      _basic_load(data, field, cls)
    _load_sources(data)
    _load_taxa(data)
    _basic_load(data, 'sections', Section)
    roots = _load_trees(data)
  if errors.count and not tolerate:
    plural = 's' if errors.count != 1 else ''
    raise LoadError(f'{errors.count} integrity error{plural} while loading; see the log')
  return data, roots
