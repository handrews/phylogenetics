import sys
import pathlib
import logging
import collections

import yaml
import jschon

logger = logging.getLogger(__name__)

NAMED_TAXON_FIELDS = {'taxon', 'cfTaxon', 'affTaxon'}


def print_taxon(taxon, data, tree_lookup, args):
  found_trees = data['index'].get(taxon, [])
  logger.info(
    f'Found {len(found_trees)} trees, searching for taxon {taxon}...'
  )

  for tree in sorted(found_trees):
    print_tree(tree_lookup[tree[0]], data, tree, args)


def print_tree(node, data, tree_info, args, indent='', on=True, buffer=''):
  root = args.root if args.root else args.branch

  if not indent:
    print(f'PAPER: {tree_info[1]}')
    if root is not None:
      on = False

  logger.debug(f'root "{args.root}" leaf "{args.leaf}" branch "{args.branch}"')
  found_name = None
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
  if root is not None and found_name == root:
    on = True

  new_indent = indent
  if node.get('provisional'):
    indent = indent[:-2] + '?' + ' '

  output = f'{indent}{name}'
  if on:
    if args.branch == found_name:
      # Strip off final newline as print() always adds one.
      print(buffer[:-1])
      buffer = ''
    print(output)
  else:
    buffer += f'{output}\n'
  new_indent += '  '

  if args.leaf is not None and found_name == args.leaf:
    on = False

  for child in node.get('children', []):
    print_tree(child, data, tree_info, args, indent=new_indent, on=on, buffer=buffer)

  if args.leaf is not None and found_name == args.leaf:
    on = True
  if root is not None and found_name == root:
    on = False
