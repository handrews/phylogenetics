import sys
import pathlib
import logging
import collections
import argparse

import yaml
import jschon

from .io import load_files
from .research import Author, Publication, Source
from .taxa import Taxon, Tree, print_taxa
from .convert import convert

logger = logging.getLogger(__name__)

schema_catalog = jschon.create_catalog('2020-12')
"""The default shared ``jschon`` schema loader and cache"""


def _basic_load(data, field, cls):
  logger.info(f"Loading {len(data[field])} {field}...")
  for item_key, item_data in data[field].items():
    cls.add(item_data, item_key)
  logger.info(f'...{field} loaded.')


def _load_taxa(data):
  logger.info(f"Processing {len(data['taxa'])} taxa...")
  deferred = []
  deferring_fields = frozenset({
    'altRankOf',
    'altSpellingOf',
    'vulgarSpellingOf',
  })
  for taxon_key, taxon_data in data['taxa'].items():
    if taxon_data.keys() & deferring_fields:
      deferred.append((taxon_key, taxon_data))
      continue
    Taxon.add(taxon_data, taxon_key)
  for taxon_key, taxon_data in deferred:
    Taxon.add(taxon_data, taxon_key)
  logger.info(f"...taxa processed.")


def _report_merge_targets(data):
  for ref_key, opinion in data['trees'].items():
    for tax_tree in opinion.get('taxonomies', ()):
      if 'mergeInto' not in tax_tree:
        continue
      src, index = tax_tree['mergeInto']
      if src not in data['trees']:
        logger.error(
          f'{ref_key} has mergeInto target source "{src}", which does '
          'not exist',
        )
      elif index >= len(data['trees'][src].get('taxonomies', [])):
        logger.error(
          f'{ref_key} has mergeInto target "{src}"[{index}], but "{src}" '
          f'only has {len(data["trees"][src].get("taxonomies", []))} '
          'taxonomies',
        )


def _report_missing_protologues(data):
  # A protologue is the source that names a taxon; if that source is one of
  # our trees, the taxon should show up flagged `new` in it.
  missing = 0
  for taxon in Taxon._taxa.values():
    # Open taxa and spelling/rank variants have no protologue to flag.
    if taxon.name is None or taxon.alias_of is not None:
      continue
    source = taxon.authority.source
    if source is None or source.key not in data['trees']:
      continue
    if source.key not in Tree._new_index.get(taxon.key, ()):
      logger.warning(f'Protologue not flagged: {taxon.key} in {source.key}')
      missing += 1
  logger.info(f'{missing} taxa with an unflagged protologue')


def _load_trees(data):
  logger.info(f"Processing {len(data['trees'])} opinions...")

  for ref_key, opinion in data['trees'].items():
    logger.debug(f'Processing opinions from "{ref_key}"')

    position = 0
    for tax_tree in opinion.get('taxonomies', {}):
      metadata = {
        'source_key': ref_key,
        'position': position,
        'type': Tree.TYPE_TAXONOMY,
      }
      position += 1

      t = Tree(tax_tree, metadata)
      logger.debug(f'Processed tree {t}')

    for phy_tree in opinion.get('phylogenies', {}):
      metadata = {
        'source_key': ref_key,
        'position': position,
      }
      position += 1

      if (tree_type := phy_tree.get('treeType', '').lower()) not in Tree.TYPES:
        logger.error(f'Unknown tree type {tree_type}')
      metadata['type'] = tree_type

      if 'characteristics' in phy_tree:
        metadata['characteristics'] = phy_tree['characteristics']

      t = Tree(phy_tree['tree'], metadata)

  logger.info(f"...opinions processed.")

  _report_merge_targets(data)
  _report_missing_protologues(data)

  return data


def main():
  parser = argparse.ArgumentParser(
    prog='phylohist',
  )
  parser.add_argument('-t', '--type', nargs='+', action='extend', default=['x'])
  parser.add_argument('-r', '--root', nargs='+', action='extend', default=[])
  parser.add_argument('-l', '--leaf', nargs='+', action='extend', default=[])
  parser.add_argument('-b', '--branch', nargs='+', action='extend', default=[])
  parser.add_argument('-f', '--find', nargs='+', action='extend', default=[])
  parser.add_argument('-m', '--match', default=False, action='store_true')
  parser.add_argument('-i', '--highest')
  parser.add_argument('-w', '--lowest')
  parser.add_argument('-a', '--author', nargs='+', action='extend', default=[])
  parser.add_argument('-p', '--personal', default=False, action='store_true')
  args = parser.parse_args()

  taxa = frozenset(
    args.find if args.find else (
      args.branch if args.branch else (
        args.root if args.root else args.leaf
      )
    )
  )

  tree_types = set()
  # If 'a' is present, leave set empty to indicate all types.
  if 'a' not in args.type:
    if 'x' in args.type:
      tree_types.add(Tree.TYPE_TAXONOMY)
    if 't' in args.type:
      tree_types.add(Tree.TYPE_TABLE)
    if 'c' in args.type:
      tree_types.add(Tree.TYPE_CLADOGRAM)
    if 'd' in args.type:
      tree_types.add(Tree.TYPE_DIAGRAM)
    if 'o' in args.type:
      tree_types.add(Tree.TYPE_OTHER)

  data = load_files(args.personal)

  for field, cls in (
    ('authors', Author),
    ('publications', Publication),
    ('sources', Source),
  ):
    _basic_load(data, field, cls)

  _load_taxa(data)
  _load_trees(data)

  if taxa or args.author:
    if taxa:
      logger.info(f'...searching for taxon "{taxa}"')
    else:
      logger.info(f'...searching for opinions by "{args.author}"')
    print_taxa(
      taxa=taxa,
      authors=frozenset(args.author),
      tree_types=frozenset(tree_types),
      root=frozenset(args.root if args.root else args.branch),
      leaf=frozenset(args.leaf),
      branch=frozenset(args.branch),
      highest=args.highest,
      lowest=args.lowest,
    )
