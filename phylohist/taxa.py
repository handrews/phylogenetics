import sys
import pathlib
import logging
import collections
from functools import cached_property, reduce

import yaml
import jschon

from .research import Author, Source


logger = logging.getLogger(__name__)

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
      if self._name is None:
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

      valid, valid_set = self._check_expected_taxon(expected)
      if not valid:
        logger.error(f'"{taxon_key}" not in expected set: {valid_set}')

    logger.debug(f'    ...all authorities for "{taxon_key}" processed')

  def _check_expected_taxon(self, expected):
    if self._key == expected:
      return True, {expected}

    if not self._key.startswith(expected):
      return False, {expected}

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

    expected_set.add(f"{expected}-{self.rank.lower()}")
    if (op := self._data.get('originalParent')):
      expected_set = {e + f"_{op.lower()}" for e in expected_set}

    logger.debug(f'...built {expected_set}')

    if self._key in expected_set:
      return True, expected_set
    return False, expected_set

  def __str__(self):
    if self._name:
      string = self._name
      if self._data.get('quoted'):
        string = f'"{string}"'
    else:
      string = f'[{self._key}]'
    return f'{string} ({self._authority})'

  @property
  def key(self):
    return self._key

  @property
  def name(self):
    return self._name

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


class ProxyTaxon(Taxon):
  def __init__(self, taxon, proxy_type, source):
    self._data = {}
    self._name = None
    self._source = source
    self._proxied = taxon
    self._proxy_type = proxy_type
    self._authority = Authority({'authority': {'source': source.key}})

  def __str__(self):
    return f'{self._proxy_type} {self._proxied} ({self._authority})'

  @property
  def key(self):
    return None

  @property
  def rank(self):
    return self._proxied.rank


class Tree:
  _NAMED_FIELDS = {'taxon'}
  _PROXY_FIELDS = {'cfTaxon', 'affTaxon'}
  _UNNAMED_FIELDS = {'openTaxon'}
  _ALL_TAXON_FIELDS = _NAMED_FIELDS | _PROXY_FIELDS | _UNNAMED_FIELDS

  TYPE_TAXONOMY = 'taxonomy'
  TYPE_CLADOGRAM = 'cladogram'
  TYPE_DIAGRAM = 'diagram'
  TYPE_OTHER = 'other'
  TYPES = {
    TYPE_TAXONOMY,
    TYPE_CLADOGRAM,
    TYPE_DIAGRAM,
    TYPE_OTHER,
  }

  RELATED_SINGULAR = (
    'moved',
    'corrected',
  )
  RELATED_LIST = (
    'or',
    'synonyms',
    'non',
    'children',
    'parents',
  )

  _taxon_index = collections.defaultdict(list)
  _type_index = {
    TYPE_TAXONOMY: [],
    TYPE_CLADOGRAM: [],
    TYPE_DIAGRAM: [],
    TYPE_OTHER: [],
  }

  def __init__(
    self,
    tree_data,
    tree_metadata=None,
    parent=None,
    relpath=(),
  ):
    if ((tree_metadata, parent) == (None, None) or
        (tree_metadata is not None and parent is not None)):
      raise ValueError(
        'Tree nodes must have either a parent or metadata, but not both!',
      )
    if parent is not None and relpath == ():
      raise ValueError('Non-root nodes must have a non-root relative path')

    self._data = tree_data
    self._metadata = tree_metadata
    self._parent = parent
    self._taxon = None
    self._relpath = relpath

    self._or = []
    self._synonyms = []
    self._non = []
    self._alt_placements = []
    self._parents = []
    self._children = []

    self._check_metadata()

    self._check_primary_taxon()
    self._bracket = self._check_taxon('bracket')
    self._moved = Tree(self._data['moved'], parent=self, relpath=('moved',)) \
      if 'moved' in self._data else None
    self._corrected = Tree(
      self._data['corrected'], parent=self, relpath=('corrected',)
    ) if 'corrected' in self._data else None

    for index, vel_or in enumerate(self._data.get('or', ())):
      self._or.append(Tree(vel_or, parent=self, relpath=('or', index)))
    for index, syn in enumerate(self._data.get('synonyms', ())):
      self._synonyms.append(Tree(syn, parent=self, relpath=('synonyms', index)))
    for index, non in enumerate(self._data.get('non', ())):
      self._non.append(Tree(non, parent=self, relpath=('non', index)))
    for index, relparent in enumerate(self._data.get('parents', ())):
      self._parents.append(
        Tree(relparent, parent=self, relpath=('parents', index))
      )
    for index, placement in enumerate(self._data.get('altPlacements', ())):
      self._alt_placements.append(
        Tree(placement, parent=self, relpath=('altPlacements', index))
      )
    for index, child in enumerate(self._data.get('children', ())):
      self._children.append(
        Tree(child, parent=self, relpath=('children', index))
      )

    if self._taxon and self._taxon.name:
      Tree._taxon_index[self._taxon.name].append(self.root)

    if self._parent is None:
      Tree._type_index[self._type].append(self)

  def _check_metadata(self):
    if self._metadata:
      self._source = Source.get(self._metadata['source_key'])
      if self._source is None:
        raise KeyError(f'Tree source {source_key} not reognized!')

      self._type = self._metadata['type']
      if self._type not in Tree._type_index:
        raise ValueError(f'Unrecognized tree type {self._type}')

      self._position = self._metadata['position']

    else:
      self._source = self._parent._source
      self._type = self._parent._type
      self._position = self._parent._position

  def _check_taxon(self, field, index=None):
    if index is None:
      taxon_key = self._data.get(field)
    else:
      taxon_key = self._data['field'][index]

    if taxon_key:
      if field in self._PROXY_FIELDS:
        taxon = ProxyTaxon(
          Taxon.get(taxon_key),
          field[:-len('Taxon')] + '.',
          self._source,
        )
      else:
        taxon = Taxon.get(taxon_key)
        if taxon is None:
          # TODO: Is this error message right?
          raise KeyError(f'Unrecognized tree {field} {taxon_key} for {self}')

      unnamed = self._UNNAMED_FIELDS | self._PROXY_FIELDS
      if field not in unnamed and not taxon.name:
        raise ValueError(
          f'Taxon {taxon} at {self}/{field} expected to be named.',
        )
      if field in unnamed and taxon.name:
        raise ValueError(
          f'Taxon {self._taxon} at {self}/{taxon_field} expected '
          'to not be named.',
        )
      return taxon
    return None

  def _check_primary_taxon(self):
    taxon_fields = self._ALL_TAXON_FIELDS & self._data.keys()
    if len(taxon_fields) > 1:
      raise ValueError(
        f'Found {len(taxon_fields)} taxon fields '
        f'({taxon_fields}), expected at most one!',
      )

    if len(taxon_fields) == 1:
      taxon_field = taxon_fields.pop()

      self._taxon = self._check_taxon(taxon_field)

      if (
        self._type == self.TYPE_TAXONOMY and
        self.is_primary and
        taxon_field in self._NAMED_FIELDS and
        self._taxon._authority.source
      ):
        is_new = self._data.get('new')
        tsource = self._taxon._authority.source

        if is_new and self._source != tsource:
          raise ValueError(
            f'Expected source {self._source} for new taxon {self._taxon}, '
            f'got source {tsource}',
          )
        elif not is_new and self._source == tsource:
          raise ValueError(
            f'Taxon {self._taxon} at {self}, field "{taxon_field}", lists '
            f'this source as its authority, but is not marked as new.',
          )

  def __str__(self):
    return f'Tree {self._source}[{self._position}]{self.pointer}'

  @cached_property
  def path(self):
    if self._parent is None:
      return []
    p = self._parent.path
    p.extend(self._relpath)
    return p

  @cached_property
  def is_primary(self):
    return reduce(
      lambda tf, p: tf and (type(p) is int or p == 'children'),
      self.path,
      True,
    )

  @cached_property
  def pointer(self):
    # Field names do not contain '/' or '~', so there
    # is no need to worry about escaping.  Note that
    # this is a plain JSON Pointer, not a URI fragment.
    return '/' + '/'.join([str(p) for p in self.path])

  @cached_property
  def root(self):
    if self._parent is None:
      return self
    return self._parent.root


def check_trees(data, taxa, args):
  logger.info(f"Processing {len(data['trees'])} opinions...")
  logger.info(f'...searching for taxon "{taxa}"')

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
        raise ValueError(f'Unknown tree type {tree_type}')
      metadata['type'] = tree_type

      if 'characteristics' in phy_tree:
        metadata['characteristics'] = phy_tree['characteristics']

      t = Tree(phy_tree['tree'], metadata)
        
  logger.info(f"...opinions processed.")

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
