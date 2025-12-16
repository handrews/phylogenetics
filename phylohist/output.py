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

def print_taxa(taxa, data, tree_lookup, args):
  found_trees = set()
  for t in taxa:
    found_trees |= set((data['index'].get(t, [])))
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
