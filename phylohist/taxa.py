import sys
import pathlib
import logging
import collections
from functools import cached_property

import yaml
import jschon

from .research import Author, Source


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
  actual_key,
  expected,
  build_expected_set=None,
  *args,
  **kwargs,
):
  if actual_key == expected:
    return True, {expected}

  if build_expected_set is None or not actual_key.startswith(expected):
    return False, {expected}

  expected_set = build_expected_set(expected, *args, **kwargs)
  if actual_key in expected_set:
    return True, expected_set
  return False, expected_set


def check_extras(taxon, rank, expected_set, expected):
    expected_set.add(f"{expected}-{rank.lower()}")
    if 'originalParent' in taxon:
      expected_set = {
        e + f"_{taxon['originalParent'].lower()}" for e in expected_set
      }
    return expected_set



class Authority:
  def __init__(self, data):
    self._source = None

    if (a := data.get('authority' )):
      self._source = Source.get(a['source'])

      if not self._source:
        raise KeyError(f'Authority source "{source}" not recognized')

      if 'authors' in a:
        self._authors = self._find_authors(a['authors'])
        self._in = self._source.authors
      else:
        self._authors = self._source.authors
        self._in = None

      if self._source.in_preparation:
        self._year = None
      else:
        self._year = self.source.year
        self._disambiguator = self.source.disambiguator

      if 'ex' in a:
        self._ex = Authority({'authority': a['ex']})
      else:
        self._ex = None

    else:
      self._authors = self._find_authors(data['auth'])
      self._year = data.get('year')
      self._in = self._find_authors(data['in']) if 'in' in data else None

      assert 'ex' not in data, "TODO: 'ex' outside of 'authority'"
      self._ex = None

    if self._year:
      for a in self._authors:
        if not a.could_publish_in(self._year):
          raise ValueError(
            f'Source {source_key} year {year} too far outside of '
            f'{author} lifespan!',
          )

  def __str__(self):
    # TODO: Figure out when/how to add disambiguating intitials.
    string = ', '.join([a.family for a in self._authors])
    if self._in:
      string += ' in ' + ', '.join([a.family for a in self._in])
    if self._year:
      string = f'{string} {self._year}'
    return string

  def _find_authors(self, author_strings):
    authors = []
    for author_string in author_strings:
      if author_string == 'et al.':
        continue

      if author_string.lower() != author_string:
        # Currently, we do not have unregistered authors with given names.
        authors.append(Author({'family': author_string}))
      else:
        if not (author := Author.get(author_string)):
          raise KeyError(f'Author for author key {author_string} not found!')
        authors.append(author)
    return tuple(authors)

  @property
  def source(self):
    return self._source

  @property
  def authors(self):
    return self._authors

  @property
  def taxon_suffix(self):
    if self._source:
      return f'{self._source.author_keys_string}_{self._year}'
    return '_'.join([
        (a.key if a.key else a.family.lower())
        for a in self.authors
    ]) + f'_{self._year}'


class Taxon:
  _taxa = {}

  @classmethod
  def add(cls, taxon_data, taxon_key):
    cls._taxa[taxon_key] = Taxon(taxon_data, taxon_key)

  @classmethod
  def get(cls, taxon_key):
    return cls._taxa.get(taxon_key)

  def __init__(self, taxon_data, taxon_key):
    self._data = taxon_data
    self._key = taxon_key
    self._name = self._data.get('name')
    self._rank = self._data.get('rank')

    if not self._rank:
      if self.name is None:
        raise ValueError(f"Unnamed, unranked taxon {taxon_key}!")

      self._rank = 'species' if self._name.islower() else 'genus'

    logger.debug(f'  Processing taxon "{taxon_key}"...')

    if (alt_key := taxon_data.get('altSpellingOf')):
      if not (alt := Taxon.get(alt_key)):
        raise KeyError(f'Taxon {taxon_key} alt spelling of unknown {alt_key}')
      self._alt = alt
      self._rank = alt.rank
      self._authority = alt.authority

    elif (alt_key := taxon_data.get('altRankOf')):
      if not (alt := Taxon.get(alt_key)):
        raise KeyError(f'Taxon {taxon_key} alt rank of unknown {alt_key}')
      self._alt = alt
      self._name = alt.name
      self._authority = alt.authority

    else:
      self._alt = None
      self._authority = Authority(taxon_data)

    if self._name is not None:
      expected = self._name.lower()

      valid, valid_set = check_expectation(
        taxon_key,
        expected,
        self._build_expected_taxon,
      )
      if not valid:
        logger.error(f'"{taxon_key}" not in expected set: {valid_set}')

    logger.debug(f'    ...all authorities for "{taxon_key}" processed')

  def _build_expected_taxon(self, expected):

    if (
      self._data.get('homonym') or
      self._data.get('needsQualification') or
      self.rank in ('species', 'subspecies', 'variety')
    ):
      suffix_expected = expected + '_' + self.authority.taxon_suffix
      expected_set = {suffix_expected}
      if self.authority.source:
        expected_set.add(suffix_expected + self.authority.source.disambiguator)
    else:
      expected_set = {expected}

    expected_set = check_extras(self._data, self.rank, expected_set, expected)
    logger.debug(f'...built {expected_set}')
    return expected_set

  @property
  def key(self):
    return self._key

  @property
  def name(self):
    return self._data['name']

  @cached_property
  def canonical_name(self):
    # The canonical name is:
    # * nomen correct. if one exists, or...
    # * the normalized spelling of the originally defined name
    # If a name is the result of a re-ranking that has been
    # done both with and without translation, the translation is preferred.
    # TODO: Align with ICZN wherever possible.
    if (alt := self._data.get('altSpellingOf')):
      return Taxon.get(alt).name
    return self.name

  @property
  def rank(self):
    # TODO: Handle this properly, it's more complex than it looks
    return self._rank

  @property
  def authority(self):
    return self._authority

def check_taxa(data):
  logger.info(f"Processing {len(data['taxa'])} taxa...")
  deferred = []
  for taxon_key, taxon_data in data['taxa'].items():
    if taxon_data.keys() & {'altRankOf', 'altSpellingOf'}:
      deferred.append((taxon_key, taxon_data))
      continue
    Taxon.add(taxon_data, taxon_key)
  for taxon_key, taxon_data in deferred:
    Taxon.add(taxon_data, taxon_key)

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
    taxon_key = node[taxon_type]
    current = parent + [taxon_key]

    logger.debug(f'checking {current}')
    if not (taxon := data['taxa'].get(taxon_key, {})):
      logger.error(f'Taxon "{taxon_key}" not found!')

    elif (
      taxon_type in NAMED_TAXON_FIELDS and 'altRankOf' not in taxon and
      taxon.get('name') is None
    ):
      logger.error(f'Taxon "{taxon_key}" expected to have a name!')
    elif taxon_type not in NAMED_TAXON_FIELDS and taxon['name'] is not None:
      logger.error(f'Taxon "{taxon_key}" NOT expected to have a name!')

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


def check_trees(data, taxa, args):
  logger.info(f"Processing {len(data['trees'])} opinions...")
  logger.info(f'...searching for taxon "{taxa}"')
  opinions = set()
  tree_index = 0
  tree_lookup = {}
  data['index'] = collections.defaultdict(set)
  for ref_key, opinion in data['trees'].items():
    opinions.add(ref_key)
    logger.debug(f'Processing opinions from "{ref_key}"')
    if ref_key not in data['sources']:
      logger.error(f'Tree citation "{ref_key}" not found!')

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
      check_node(t, data, tree_info=(tree_index, ref_key))
      tree_index += 1
  logger.info(f"...opinions processed.")

  if taxa or args.author:
    print_taxa(taxa, data, tree_lookup, args)

  if (difference := Source.count() - len(opinions)):
    # logger.warn("Missing opinions from:\n    " + '\n    '.join(sorted(difference)))
    logger.warn(f"Missing opinions from {difference} papers!")
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
          data['authors'][a_key] for a_key in paper['authors']
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
  if (taxon_key := node.get('taxon')):
    if not (taxon := data['taxa'].get(taxon_key)):
      raise ValueError(f'No taxon data for id {taxon_key}')
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
    if (taxon_key := node.get('openTaxon')):
      name = f'[{taxon_key}]'
    elif (taxon_key := node.get('cfTaxon')):
      name = f'[cf. {taxon_key}]'
    elif (taxon_key := node.get('affTaxon')):
      name = f'[aff. {taxon_key}]'
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
