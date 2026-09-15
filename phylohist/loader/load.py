"""Loading the corpus into the object model.

`load()` reads every data file through `phylohist.loader.io`, registers
authors, publications and sources, builds the taxa and then every tree,
and returns the raw data with the tree roots per source. The scripts,
the tests and the extractor all come through here. Every integrity
problem is logged where it is found so that one run reports them all;
the load then fails with their count, unless the caller asks for the
data anyway.
"""

import contextlib
import logging

from .io import LoadError, load_files
from .research import Author, Publication, Source
from .taxa import Taxon, Tree

logger = logging.getLogger(__name__)


def _basic_load(data, field, cls):
  logger.info(f'Loading {len(data[field])} {field}...')
  for item_key, item_data in data[field].items():
    cls.add(item_data, item_key)
  logger.info(f'...{field} loaded.')


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


def _report_missing_protologues(data):
  # A protologue is the source that names a taxon; if that source is one of
  # our trees, the taxon should show up flagged `new` in it.
  missing = 0
  for taxon in Taxon._taxa.values():
    # Open taxa and derivative records have no protologue to flag.
    if taxon.name is None or taxon.derivative_of is not None:
      continue
    source = taxon.authority.source
    if source is None or source.key not in data['trees']:
      continue
    if source.key not in Tree._new_index.get(taxon.key, ()):
      logger.warning(f'Protologue not flagged: {taxon.key} in {source.key}')
      missing += 1
  logger.info(f'{missing} taxa with an unflagged protologue')


def _load_trees(data):
  """Build every tree; return ``{source_key: [roots in position order]}``."""
  logger.info(f'Processing {len(data["trees"])} opinions...')

  roots = {}
  for ref_key, opinion in data['trees'].items():
    logger.debug(f'Processing opinions from "{ref_key}"')
    roots[ref_key] = []

    position = 0
    for tax_tree in opinion.get('taxonomies', {}):
      metadata = {
        'source_key': ref_key,
        'position': position,
        'type': Tree.TYPE_TAXONOMY,
      }
      position += 1

      t = Tree(tax_tree, metadata)
      roots[ref_key].append(t)
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
      if 'notes' in phy_tree:
        metadata['notes'] = phy_tree['notes']

      t = Tree(phy_tree['tree'], metadata)
      roots[ref_key].append(t)

  logger.info('...opinions processed.')

  _report_merge_targets(data)
  _report_missing_protologues(data)
  return roots


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


def load(drafts=False, tolerate=False):
  """``(data, roots)``: the loaded data files and ``{source: [roots]}``.
  Raises `LoadError` when any integrity check logged an error, with the
  count, so a caller cannot take a broken load for a good one; with
  ``tolerate`` the data comes back regardless, for a caller that wants
  to see everything before stopping."""
  with counting_errors() as errors:
    data = load_files(drafts=drafts)
    for field, cls in (
      ('authors', Author),
      ('publications', Publication),
      ('sources', Source),
    ):
      _basic_load(data, field, cls)
    _load_taxa(data)
    roots = _load_trees(data)
  if errors.count and not tolerate:
    plural = 's' if errors.count != 1 else ''
    raise LoadError(f'{errors.count} integrity error{plural} while loading; see the log')
  return data, roots
