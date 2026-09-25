import collections
import logging
from functools import cached_property, reduce

from .research import Author, Source

logger = logging.getLogger(__name__)

RANKS = {
  'superdomain': 77,
  'domain': 75,
  'subdomain': 74,
  'superkingdom': 67,
  'kingdom': 65,
  'subkingdom': 64,
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

NON_RANKS = {
  'Grade',
  'Branch',
  'Group',
  'Plesion',
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


def _check_unregistered_author(author_string, where=None):
  # A capitalised author string is the convention for an author with no
  # record; when its key form is registered, the record was meant.
  if Author.get(author_string.lower()):
    at = f' at {where}' if where is not None else ''
    logger.warning(
      f'Unregistered author "{author_string}"{at} matches registered key "{author_string.lower()}"',
    )


class Authority:
  def __init__(self, data):
    self._source = None

    if a := data.get('authority'):
      source_key = a['source']
      self._source = Source.get(source_key)
      if not self._source:
        logger.error(f'Authority source "{source_key}" not recognized')

      self._source_authors = self._source.authors
      if 'attributedTo' in a:
        self._authors = self._find_authors(a['attributedTo'])
      else:
        self._authors = None

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
      if not data['auth']:
        self._source_authors = None
        self._authors = None
      else:
        auth_authors = self._find_authors(data['auth'])
        if 'in' in data:
          self._source_authors = self._find_authors(data['in'])
          self._authors = auth_authors
        else:
          self._source_authors = auth_authors
          self._authors = None
        self._year = data.get('year')

        assert 'ex' not in data, "TODO: 'ex' outside of 'authority'"
        self._ex = None

      self._year = data.get('year')

    if self._year:
      for a in self._source_authors:
        if (
          not a.could_publish_in(self._year)
          and not (a.surname == 'Klein' and self._year == 1778)
          and not (a.surname == 'Linnaeus' and self._year == 1790)
          and not (a.surname == 'Forsskål' and self._year == 1775)
        ):
          logger.error(
            f'Source {self} year {self._year} too far outside of {a} lifespan!',
          )

  def __str__(self):
    # TODO: Figure out when/how to add disambiguating intitials.
    string = ', '.join([a.surname for a in self.authors])
    if self.attribution_differs_from_source:
      string += ' in ' + ', '.join([a.surname for a in self.source_authors])
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
        _check_unregistered_author(author_string)
        authors.append(Author({'surname': author_string}))
      else:
        if not (author := Author.get(author_string)):
          logger.error(f'Author for author key {author_string} not found!')
        authors.append(author)
    return tuple(authors)

  @property
  def source(self):
    return self._source

  @property
  def year(self):
    return self._year

  @property
  def authors(self):
    return self._authors if self.attribution_differs_from_source else self._source_authors

  @property
  def source_authors(self):
    return self._source_authors

  @property
  def attribution_differs_from_source(self):
    return self._authors is not None

  @property
  def taxon_suffix(self):
    # TODO: This string-building should not live in two classes, probably.
    if self._source and not self.attribution_differs_from_source:
      string = f'{self._source.author_keys_string}'
    elif self.authors is None:
      string = 'unknown'
    else:
      string = '_'.join([(a.key if a.key else a.surname.lower()) for a in self.authors])
    if self.year:
      return f'{string}_{self._year}'
    return string


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
        logger.error(f'Unnamed, unranked taxon {taxon_key}!')

      self._rank = 'species' if self._name.islower() else 'genus'
      # TODO: Figure out if homonym/originalParent/needsQualification relevant.

    logger.debug(f'  Processing taxon "{taxon_key}"...')

    if alt_key := taxon_data.get('altSpellingOf'):
      if not (alt := Taxon.get(alt_key)):
        raise ValueError(f'Taxon {taxon_key} alt spelling of unknown {alt_key}')
      self._alt = alt
      self._rank = alt.rank
      if 'auth' in self._data or 'authority' in self._data:
        self._authority = Authority(taxon_data)
      else:
        self._authority = alt.authority
      for field in ('homonym', 'originalParent', 'needsQualification'):
        if field in alt._data:
          self._data[field] = alt._data[field]

    elif latin_key := taxon_data.get('vulgarSpellingOf'):
      if not (latin := Taxon.get(latin_key)):
        logger.error(f'Taxon {taxon_key} vulgar spelling of unknown {alt_key}')
      self._alt = latin
      self._rank = latin.rank
      if 'auth' in self._data or 'authority' in self._data:
        self._authority = Authority(taxon_data)
      else:
        self._authority = latin.authority

    elif alt_key := taxon_data.get('altRankOf'):
      if not (alt := Taxon.get(alt_key)):
        logger.error(f'Taxon {taxon_key} alt rank of unknown {alt_key}')
      self._alt = alt
      if 'name' in self._data:
        self._name = self._data['name']
      else:
        self._name = alt.name
      if 'auth' in self._data or 'authority' in self._data:
        self._authority = Authority(taxon_data)
      else:
        self._authority = alt.authority

    else:
      self._alt = None
      self._authority = Authority(taxon_data)

    if self._name is not None:
      expected = self._name.lower()

      valid, valid_set = self._check_expected_taxon(expected)
      if not valid:
        logger.error(f'"{taxon_key}" not in expected set: {valid_set}')

      self._check_rank()

    logger.debug(f'    ...all authorities for "{taxon_key}" processed')

  def _check_expected_taxon(self, expected):
    if self._key == expected:
      return True, {expected}

    if not self._key.startswith(expected):
      return False, {expected}

    if (
      self._data.get('homonym')
      or self._data.get('needsQualification')
      or self.rank in ('species', 'subspecies', 'variety')
    ):
      suffix_expected = expected + '_' + self.authority.taxon_suffix
      expected_set = {suffix_expected}
      if self.authority.source:
        expected_set.add(suffix_expected + self.authority.source.disambiguator)
    else:
      expected_set = {expected}

    expected_set.add(f'{expected}-{self.rank.lower()}')
    if op := self._data.get('originalParent'):
      expected_set = {e + f'_{op.lower()}' for e in expected_set}

    logger.debug(f'...built {expected_set}')

    if self._key in expected_set:
      return True, expected_set
    return False, expected_set

  def _check_rank(self):
    if (
      self.rank in NON_RANKS
      or self.name.lower() == self.name
      or self.key.endswith('-' + self.rank.lower())
    ):
      return

    for suffix, rank, exceptions in (
      ('inae', 'Subfamily', frozenset()),
      (
        'idae',
        'Family',
        frozenset(
          {
            'Crinoiden',
            'Crinoideen',
            'Cystideen',
            'Échinides',
            'Echinides',
            'Stelleridea',
            'Stellérides',
            'Stellerides',
            'Stelleridica',
            'Fistulides',
          }
        ),
      ),
    ):
      if self.name.endswith(suffix) and self.rank != rank:
        logger.warning(
          f'{self.name} with suffix "{suffix}" expected to have rank of {rank}',
        )
      if self.rank == rank and not self.name.endswith(suffix) and self.name not in exceptions:
        if suffix == 'idae' and self.name.endswith('idæ'):
          continue
        logger.warning(
          f'{self.name} of rank {rank} expected to end with suffix "{suffix}"',
        )

    # TODO: Verify that each exception is the expected rank
    ida_classes = frozenset(
      {
        'Acalephida',
        'Arachnida',
        'Caryocystitida',
        'Echinida',
        'Fistulida',
        'Glyptocystitida',
        'Hemicosmitida',
        'Medusida',
        'Stellerida',
        'Zoanthida',
      }
    )
    ida_subclasses = frozenset({'Disparida', 'Helicoplacida', 'Polyplacida'})
    ida_parvclasses = frozenset({'Cladida'})
    ida_suborders = frozenset({'Placocystida'})
    ida_superfamilies = frozenset({'Protocrinitida'})
    ida_exceptions = (
      ida_classes | ida_subclasses | ida_parvclasses | ida_suborders | ida_superfamilies
    )

    ina_exceptions = frozenset(
      {
        'Carallina',
        'Corallina',
        'Craterina',
        'Funiculina',
        'Meandrina',
        'Palasterina',
        'Palaeasterina',
        'Palæasterina',
        'Tellina',
      }
    )

    for suffix, ranks, exceptions in (
      ('acea', ('Superfamily',), frozenset({'Crustacea'})),
      ('ina', ('Suborder',), ina_exceptions),
      ('ida', ('Order',), ida_exceptions),
      (
        'zoa',
        ('Class', 'Subphylum', 'Phylum', 'Subkingdom', 'Kingdom'),
        frozenset({'Lithozoa'}),
      ),
    ):
      if self.name.endswith(suffix) and self.rank not in ranks and self.name not in exceptions:
        logger.warning(
          f'{self.name} with suffix "{suffix}" expected to have one of ranks '
          f'{ranks} but has rank {self.rank}',
        )

    # TODO: More ranks, but they get increasingly inconsistent.

  def __str__(self):
    return f'{self.display_name} ({self._authority})'

  @property
  def key(self):
    return self._key

  @property
  def name(self):
    return self._name

  @cached_property
  def display_name(self):
    if self._name:
      string = self._name
      if self._data.get('quoted'):
        string = f'"{string}"'
      if self.rank == 'subgenus':
        string = f'({string})'
    else:
      string = f'[{self._key}]'
    return string

  @cached_property
  def canonical_name(self):
    # The canonical name is:
    # * nomen correct. if one exists, or...
    # * the normalized spelling of the originally defined name
    # If a name is the result of a re-ranking that has been
    # done both with and without translation, the translation is preferred.
    # TODO: Align with ICZN wherever possible.
    if alt := self._data.get('altSpellingOf'):
      return Taxon.get(alt).name
    return self.name

  @property
  def rank(self):
    # TODO: Handle this properly, it's more complex than it looks
    return self._rank

  @property
  def authority(self):
    return self._authority

  @property
  def derivative_of(self):
    # The record this one derives from (a spelling, vulgar or rank variant),
    # if any; the authority is borrowed from it, so there is no protologue of
    # this record's own.
    return self._alt


class ProxyTaxon(Taxon):
  def __init__(self, taxon, proxy_type, source):
    super().__init__(taxon._data, taxon.key)
    self._name = None
    self._proxy_type = proxy_type
    self._proxied_authority = self._authority
    self._authority = Authority({'authority': {'source': source.key}})

  @property
  def display_name(self):
    return f'{self._proxy_type} ' + super().display_name


class Tree:
  _NAMED_FIELDS = {'taxon'}
  _PROXY_FIELDS = {'cfTaxon', 'affTaxon'}
  _UNNAMED_FIELDS = {'openTaxon'}
  _ALL_TAXON_FIELDS = _NAMED_FIELDS | _PROXY_FIELDS | _UNNAMED_FIELDS

  TYPE_TAXONOMY = 'taxonomy'
  TYPE_TABLE = 'table'
  TYPE_CLADOGRAM = 'cladogram'
  TYPE_DIAGRAM = 'diagram'
  TYPE_OTHER = 'other'
  TYPES = {
    TYPE_TAXONOMY,
    TYPE_CLADOGRAM,
    TYPE_DIAGRAM,
    TYPE_OTHER,
  }

  # The subtrees other than `children`, in walk order: each field and
  # whether it holds a list of nodes rather than a single one.
  RELATED_AXES = (
    ('moved', False),
    ('corrected', False),
    ('substituted', False),
    ('translated', False),
    ('or', True),
    ('synonyms', True),
    ('non', True),
    ('removed', True),
    ('parents', True),
    ('altPlacements', True),
  )

  _taxon_index = collections.defaultdict(set)
  _new_index = collections.defaultdict(set)
  _author_index = collections.defaultdict(set)
  _type_index = {
    TYPE_TAXONOMY: set(),
    TYPE_CLADOGRAM: set(),
    TYPE_DIAGRAM: set(),
    TYPE_OTHER: set(),
  }

  @classmethod
  def find(
    cls,
    taxa=frozenset(),
    authors=frozenset(),
    tree_types=frozenset(),
  ):
    if not taxa and not authors:
      return frozenset()

    trees = set()
    if tree_types:
      for t in cls._type_index.keys() & tree_types:
        trees |= cls._type_index[t]
    else:
      for typed_set in cls._type_index.values():
        trees |= typed_set

    if taxa:
      taxa_trees = set()
      for k in cls._taxon_index.keys() & taxa:
        taxa_trees |= cls._taxon_index[k]
      trees &= taxa_trees

    if authors:
      author_trees = set()
      for k in cls._author_index.keys() & authors:
        author_trees |= cls._author_index[k]
      trees &= author_trees

    return trees

  def __init__(
    self,
    tree_data,
    tree_metadata=None,
    parent=None,
    relpath=(),
  ):
    if (tree_metadata, parent) == (None, None) or (
      tree_metadata is not None and parent is not None
    ):
      logger.error(
        'Tree nodes must have either a parent or metadata, but not both!',
      )
    if parent is not None and relpath == ():
      logger.error('Non-root nodes must have a non-root relative path')

    self._data = tree_data
    self._metadata = tree_metadata
    self._parent = parent
    self._taxon = None
    self._relpath = relpath

    self._related = {}
    self._children = []

    self._check_metadata()
    self._check_primary_taxon()

    self._bracket = self._check_taxon('bracket')
    for axis, many in self.RELATED_AXES:
      value = self._data.get(axis)
      if many:
        self._related[axis] = [
          Tree(item, parent=self, relpath=(axis, index)) for index, item in enumerate(value or ())
        ]
      # `translated: true` states the act without the earlier rank.
      elif isinstance(value, dict):
        self._related[axis] = [Tree(value, parent=self, relpath=(axis,))]
      else:
        self._related[axis] = []

    for index, child in enumerate(self._data.get('children', ())):
      self._children.append(Tree(child, parent=self, relpath=('children', index)))

    if self._taxon:
      if self._taxon.name:
        Tree._taxon_index[self._taxon.name].add(self.root)

      if self._data.get('new'):
        Tree._new_index[self._taxon.key].add(self._source.key)

      for author_string in self._data.get('auth') or ():
        if author_string.lower() != author_string:
          _check_unregistered_author(author_string, where=self)

      # For now, only registered authors are supported in order to use
      # their unique keys.  TODO: Better options.
      if self._taxon.authority.source:
        for author in self._taxon.authority.source.authors:
          Tree._author_index[author.key].add(self.root)

    if self._parent is None:
      Tree._type_index[self._type].add(self)

  def _check_metadata(self):
    if self._metadata:
      self._source = Source.get(self._metadata['source_key'])
      if self._source is None:
        logger.error(f'Tree source {self._metadata["source_key"]} not recognized!')

      self._type = self._metadata['type']
      if self._type not in Tree._type_index:
        logger.error(f'Unrecognized tree type {self._type}')

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
        if proxy_target := Taxon.get(taxon_key):
          taxon = ProxyTaxon(
            proxy_target,
            field[: -len('Taxon')] + '.',
            self._source,
          )
        else:
          raise ValueError(f'Could not get proxy target {taxon_key}')
      else:
        taxon = Taxon.get(taxon_key)
        if taxon is None:
          # TODO: Is this error message right?
          logger.error(f'Unrecognized tree {field} {taxon_key} for {self}')
          return None

      unnamed = self._UNNAMED_FIELDS | self._PROXY_FIELDS
      if field not in unnamed and not taxon.name:
        logger.error(
          f'Taxon {taxon} at {self}/{field} expected to be named.',
        )
      if field in unnamed and taxon.name:
        logger.error(
          f'Taxon {self._taxon} at {self}/{field} expected to not be named.',
        )
      return taxon
    return None

  def _check_primary_taxon(self):
    taxon_fields = self._ALL_TAXON_FIELDS & self._data.keys()
    if len(taxon_fields) > 1:
      logger.error(
        f'Found {len(taxon_fields)} taxon fields ({taxon_fields}), expected at most one!',
      )

    if len(taxon_fields) == 1:
      taxon_field = taxon_fields.pop()

      self._taxon = self._check_taxon(taxon_field)
      if self._taxon is None:
        # TODO: Fix this symptom of weird exception vs logging error handling.
        return

      if (
        self._type == self.TYPE_TAXONOMY
        and self.is_primary
        and taxon_field in self._NAMED_FIELDS
        and self._taxon.authority.source
      ):
        is_new = self._data.get('new')
        tsource = self._taxon._authority.source

        if is_new and self._source != tsource:
          logger.error(
            f'Expected source {self._source} for new taxon {self._taxon}, got source {tsource}',
          )
        elif not is_new and self._source == tsource:
          logger.error(
            f'Taxon {self._taxon} at {self}, field "{taxon_field}", lists '
            f'this source as its authority, but is not marked as new.'
            f'\n{self._data}',
          )

  def _hash_key(self):
    return (self._source.key, self._position, self.path)

  def __str__(self):
    return f'{self._source}[{self._position}]{self.taxon_path}'

  def __repr__(self):
    return repr(self._hash_key())

  def __hash__(self):
    return hash(self._hash_key())

  def __eq__(self, other):
    if not isinstance(other, Tree):
      return False
    return self._hash_key() == other._hash_key()

  def __lt__(self, other):
    return self._hash_key() < other._hash_key()

  def __gt__(self, other):
    return self._hash_key() > other._hash_key()

  @property
  def source(self):
    return self._source

  @property
  def taxon(self):
    return self._taxon

  @property
  def _path_list(self):
    if self._parent is None:
      return []
    p = self._parent._path_list
    p.extend(self._relpath)
    return p

  @cached_property
  def path(self):
    return tuple(self._path_list)

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
  def taxon_path(self):
    path = f'/{self.taxon.key}' if self.taxon else ''
    for segment in self._relpath:
      if segment != 'children':
        path = f'/{segment}{path}'
    if self._parent is not None:
      path = f'{self._parent.taxon_path}{path}'
    return path

  @cached_property
  def root(self):
    if self._parent is None:
      return self
    return self._parent.root

  @property
  def children(self):
    return tuple(self._children)

  # Public view of the node for consumers such as the claim extractor, so
  # that the traversal and its path convention are defined here only.
  @property
  def data(self):
    return self._data

  @property
  def parent(self):
    return self._parent

  @property
  def relpath(self):
    return self._relpath

  @property
  def axis(self):
    # How this node hangs off its parent: 'children', 'synonyms', ...;
    # 'root' for the top of a taxonomy or phylogeny.
    return self._relpath[0] if self._relpath else 'root'

  @property
  def position(self):
    return self._position

  @property
  def tree_type(self):
    return self._type

  @property
  def tree_notes(self):
    return self.root._metadata.get('notes')

  @property
  def bracket(self):
    return self._bracket

  def related_node(self, axis):
    """The node under a single-node axis (``moved``, ``corrected``, ...),
    or None."""
    nodes = self._related[axis]
    return nodes[0] if nodes else None

  def related_nodes(self, axis):
    """The nodes under a list axis (``synonyms``, ``parents``, ...)."""
    return tuple(self._related[axis])

  def related(self):
    """Yield ``(axis, node)`` for every subtree other than ``children``.

    The order is `RELATED_AXES`, so it is the order of every walk.
    """
    for axis, _ in self.RELATED_AXES:
      for node in self._related[axis]:
        yield axis, node

  def walk(self):
    """Yield this node and every descendant, related subtrees before
    children, depth first."""
    yield self
    for _, node in self.related():
      yield from node.walk()
    for child in self._children:
      yield from child.walk()

  @property
  def is_new(self):
    return self._data.get('new', False)
