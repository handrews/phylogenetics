import sys
import pathlib
import logging
import collections

import yaml
import jschon

logger = logging.getLogger(__name__)

NAMED_TAXON_FIELDS = {'taxon', 'cfTaxon', 'affTaxon'}

RANKS = {
  'superphylum': 57,
  'phylum': 55,
  'subphylum': 54,
  'infraphylum': 52,
  'superclass': 47,
  'class': 45,
  'subclass': 43,
  'infraclass': 42,
  'parvclass': 41,
  'superorder': 37,
  'order': 35,
  'suborder': 33,
  'infraorder': 32,
  'parvorder': 31,
  'superfamily': 27,
  'family': 25,
  'subfamily': 23,
  'genus': 15,
  'subgenus': 13,
  'species': 5,
  'subspecies': 3,
  'variety': 5,
}

RANK_GROUPS = {
  'phylum': ('superphylum', 'phylum', 'subphylum', 'infraphylum'),
  'class': ('superclass', 'class', 'subclass', 'infraclass', 'parvclass'),
  'order': ('superorder', 'order', 'suborder', 'infraorder', 'parvorder'),
  'family': ('superfamily', 'family', 'subfamily'),
  'genus': ('genus', 'subgenus'),
  'species': ('species', 'subspecies'),
  'variety': ('variety',),
}


def check_expectation(
  actual_id,
  expected,
  build_expected_set=None,
  *args,
  **kwargs,
):
  if actual_id == expected:
    return True, {expected}

  if build_expected_set is None or not actual_id.startswith(expected):
    return False, {expected}

  expected_set = build_expected_set(expected, *args, **kwargs)
  if actual_id in expected_set:
    return True, expected_set
  return False, expected_set


def check_extras(taxon, rank, expected_set, expected):
    expected_set.add(f"{expected}-{rank.lower()}")
    if 'originalParent' in taxon:
      expected_set = {
        e + f"_{taxon['originalParent'].lower()}" for e in expected_set
      }
    return expected_set


def build_expected_taxon(expected, taxon):
  if not (rank := taxon.get('rank')):
    if taxon['name'] is None:
      logger.error(f"Unnamed, unrakned taxon {expected}!")
      # Let the second check fail normally.
      return {expected}

    rank = 'genus' if taxon['name'][0].isupper() else 'species'

  if (
    taxon.get('homonym') or
    taxon.get('needsQualification') or
    rank in ('species', 'subspecies', 'variety')
  ):
    species_expected = expected
    logger.debug(f'Building species id for {expected}...')
    if 'auth' in taxon:
      for author_id in taxon['auth']:
        species_expected += f"_{author_id.lower()}"
      species_expected += f"_{taxon['year']}"
      expected_set = {species_expected}
    else:
      source_id = taxon['authority']['source']
      idx = source_id.index('_')
      species_expected += f'_{source_id[idx+1:]}_{source_id[:4]}'
      expected_set = {species_expected}
      if idx == 5:
        expected_set.add(species_expected + source_id[idx - 1])

    expected_set = check_extras(taxon, rank, expected_set, expected)
    logger.debug(f'...built {expected_set}')
    return expected_set

  expected_set = check_extras(taxon, rank, {expected}, expected)

  # for author_id in taxon['auth']:
    # logger.debug(f'Adding author "{author_id}" for taxon_id "{taxon}"')
    # alt_expected += f'-{author_id.lower()[0]}'
  # alt_expected += f"-{taxon['year']}"

  return expected_set


def check_taxa(data):
  logger.info(f"Processing {len(data['taxa'])} taxa...")
  for taxon_id, taxon in data['taxa'].items():
    logger.debug(f'  Processing taxon "{taxon_id}"...')

    if 'altSpellingOf' in taxon or 'altRankOf' in taxon:
      if (alt := taxon.get('altSpellingOf')) and alt not in data['taxa']:
        logger.error(f'Taxon {taxon_id} alt spelling of unknown {alt}')
      if (alt := taxon.get('altRankOf')) and alt not in data['taxa']:
        logger.error(f'Taxon {taxon_id} alt rank of unknown {alt}')
      continue

    if taxon['name'] is not None:
      expected = taxon['name'].lower()

      valid, valid_set = check_expectation(
        taxon_id,
        expected,
        build_expected_taxon,
        taxon,
      )
      if not valid:
        logger.error(f'"{taxon_id}" not in expected set: {valid_set}')

    if (authority := taxon.get('authority')):
      if (source := authority['source']) not in data['sources']:
        logger.error(f'Authority source "{source}" not recognized')
    else:
      for author_id in taxon['auth']:
        logger.debug('    Processing authority "{author_id}"')
        # This won't work with multi-token names, but good enough for now
        if author_id != author_id.lower():
          continue

        if not (author := data['authors'].get(author_id)):
          logger.error(
            f'Unrecognized author "{author_id}" in authority for "{taxon_id}"'
          )
          continue

        if (year := taxon.get('year')):
          # 15 pretty arbitrary, no clue if there's a kid genius paleontologist
          if 'birth' in author and year < (author['birth'] + 15):
            birth = author['birth']
            logger.error(f'"{author_id}" born {birth} as authority in {year}?')
          # plus 5 for Barrande 1887
          if (death := author.get('death', 3000)) and  year > (death + 5):
            death = author['death']
            logger.error(f'"{author_id}" died {death} as authority in {year}?')
    logger.debug(f'    ...all authorities for "{taxon_id}" processed')

  logger.info(f"...taxa processed.")


def check_node(node, data, parent=[], tree_info=None):
  if isinstance(node, str):
    logger.error(f"STRING? '{node}'")
    return

  taxon_fields = (NAMED_TAXON_FIELDS | {'openTaxon'}) & node.keys()

  if len(taxon_fields) > 1:
    logger.error(
      f'Found {len(taxon_fields)} taxon fields ({taxon_fields}), expected one!'
    )

  elif len(taxon_fields) == 1:
    taxon_type = taxon_fields.pop()
    taxon_id = node[taxon_type]
    current = parent + [taxon_id]

    logger.debug(f'checking {current}')
    if not (taxon := data['taxa'].get(taxon_id, {})):
      logger.error(f'Taxon "{taxon_id}" not found!')

    elif (
      taxon_type in NAMED_TAXON_FIELDS and 'altRankOf' not in taxon and
      taxon.get('name') is None
    ):
      logger.error(f'Taxon "{taxon_id}" expected to have a name!')
    elif taxon_type not in NAMED_TAXON_FIELDS and taxon['name'] is not None:
      logger.error(f'Taxon "{taxon_id}" NOT expected to have a name!')

    if (
      node.get('new') and
      tree_info is not None and
      (source := taxon.get('authority', {}).get('source')) and
      source != tree_info[1]
    ):
      logger.error(
        f'Expected source {tree_info[1]} for new taxon {taxon}, got source {source}'
      )

    name = taxon.get('name')
    if name and tree_info is not None:
      data['index'][name].add(tree_info)

  else:
    current = parent + ['_anon_']
    logger.debug(f'Descending through {current}')

  if (bracket := node.get('bracket')):
    if bracket not in data['taxa']:
      logger.error(f'Bracket taxa {bracket} not found!')

  for index, synonym in enumerate(node.get('synonyms', [])):
    check_node(synonym, data, current + ['synonym', str(index)])
  for index, non in enumerate(node.get('non', [])):
    check_node(non, data, current + ['non', str(index)])
  for index, parent in enumerate(node.get('parents', [])):
    check_node(parent, data, current + ['parent', str(index)])
  for index, altPlacement in enumerate(node.get('altPlacements', [])):
    check_node(altPlacement, data, current + ['altPlacement', str(index)])
  for index, vel_or in enumerate(node.get('or', [])):
    check_node(vel_or, data, current + ['or', str(index)])
  if (moved := node.get('moved')):
    check_node(moved, data, current + ['moved'])
  if (corrected := node.get('corrected')):
    check_node(corrected, data, current + ['corrected'])
  for child in node.get('children', []):
    check_node(child, data, current, tree_info)


def check_trees(data, sources, taxa, args):
  logger.info(f"Processing {len(data['trees'])} opinions...")
  logger.info(f'...searching for taxon "{taxa}"')
  opinions = set()
  tree_index = 0
  tree_lookup = {}
  data['index'] = collections.defaultdict(set)
  for ref_id, opinion in data['trees'].items():
    opinions.add(ref_id)
    logger.debug(f'Processing opinions from "{ref_id}"')
    if ref_id not in data['sources']:
      logger.error(f'Tree citation "{ref_id}" not found!')

    trees = []
    num_tax = 0
    if args.type == 'x':
      trees.extend([t for t in opinion.get('taxonomies', {})])
      num_tax = len(trees)
      logger.debug(f'Found {num_tax} taxonomic trees')
    if args.type == 'p':
      trees.extend([p['tree'] for p in opinion.get('phylogenies', {})])
      num_phy = len(trees) - num_tax
      logger.debug(f'Found {num_phy} phylogenetic trees')

    for i, t in enumerate(trees):
      tree_lookup[tree_index] = t
      check_node(t, data, tree_info=(tree_index, ref_id))
      tree_index += 1
  logger.info(f"...opinions processed.")

  if taxa or args.author:
    print_taxa(taxa, data, tree_lookup, args)

  if (difference := sources - opinions):
    # logger.warn("Missing opinions from:\n    " + '\n    '.join(sorted(difference)))
    logger.warn(f"Missing opinions from {len(difference)} papers!")
  return data

def print_taxa(taxa, data, tree_lookup, args):
  found_trees = set()
  if taxa:
    for t in taxa:
      found_trees |= set((data['index'].get(t, [])))
  elif args.author:
    for v in data['index'].values():
      found_trees |= v
  logger.info(
    f'Found {len(found_trees)} trees, searching for taxa {taxa}...'
  )

  for tree in sorted(found_trees):
    print_tree(tree_lookup[tree[0]], data, tree, args, first=True)


def print_tree(node, data, tree_info, args, indent='', on=1, buffer='', first=False, header=None):
  root = args.root if args.root else args.branch

  filter_levels = False
  highest = 1000
  if args.highest:
    filter_levels = True
    group = RANK_GROUPS[args.highest.lower()]
    highest = RANKS[group[0]]

  lowest = 1
  if args.lowest:
    filter_levels = True
    group = RANK_GROUPS[args.lowest.lower()]
    lowest = RANKS[group[-1]]

  if first:
    paper = data["sources"][tree_info[1]]
    if args.author and not (set(args.author) & set(paper['authors'])):
      return
    year = tree_info[1][:4] # paper['pubDate']#['year']
    authors = '; '.join(
      [
        f"{a['family']}, {a['given']}" for a in [
          data['authors'][a_id] for a_id in paper['authors']
        ]
      ]
    )
    header = f'\nPAPER: {year} {authors}\n  _{paper["title"]}_'
    if root:
      on = 0

  logger.debug(f'root "{args.root}" leaf "{args.leaf}" branch "{args.branch}"')
  found_name = None
  rank = None
  rank_level = None
  if (taxon_id := node.get('taxon')):
    if not (taxon := data['taxa'].get(taxon_id)):
      raise ValueError(f'No taxon data for id {taxon_id}')
    if not (name := taxon.get('name')):
      if (alt := taxon.get('altRankOf')):
        name = data['taxa'][alt]['name']
      else:
        name = '[** altRank of no taxon ***]'
    else:
      found_name = name
      if (rank := taxon.get('rank')):
        rank_level = RANKS.get(rank.lower(), None)

    if name is not None and taxon.get('rank') == 'subgenus':
      name = f'({name})'
  else:
    if (taxon_id := node.get('openTaxon')):
      name = f'[{taxon_id}]'
    elif (taxon_id := node.get('cfTaxon')):
      name = f'[cf. {taxon_id}]'
    elif (taxon_id := node.get('affTaxon')):
      name = f'[aff. {taxon_id}]'
    else:
      name = '[]'

  if node.get('quoted'):
    name = f'"{name}"'
  if node.get('new'):
    name += '*'
  if node.get('questionable'):
    name += ' ?'

  logger.debug(f'found name "{found_name}"')
  if root and found_name in root:
    on += 1

  new_indent = indent
  if node.get('provisional'):
    indent = indent[:-2] + '?' + ' '

  output = f'{indent}{name}'
  printable_rank = True
  if filter_levels:
    printable_rank = (
      rank_level is not None and
      rank_level <= highest and
      rank_level >= lowest
    )

  if printable_rank:
    if on:
      if header:
        print(header)
        header = None
      if args.branch and found_name in args.branch and buffer:
        # Strip off final newline as print() always adds one.
        print(buffer[:-1])
        buffer = ''
      print(output)
    elif (not filter_levels) or (filter_levels and rank):
      buffer += f'{output}\n'
    new_indent += '  '

  old_on = on
  if args.leaf and found_name in args.leaf:
    on = 0

  for child in node.get('children', []):
    print_tree(child, data, tree_info, args, indent=new_indent, on=on, buffer=buffer, header=header)

  if args.leaf and found_name in args.leaf:
    on = old_on
  if root and found_name in root:
    on -= 1

  # TODO: Figure out the times when we need to print the header separately.
  #       This is not correct.
  # if first and buffer:
  #   print(header)
  #   print(buffer[:-1])
