# Author
# * id
# * Family name
# * Given name (often initials)
# * altSpellingOf
# * year born
# * year died, or null if confirmed alive
# * possible disambiguations?
# * notes

# Publication
# * id
# * name
# * type (journal, book, book series)
# * editor(s) by reference (if relevant)
# * notes
# ... unclear how much we really want here

# Source
# * id
# * publication by reerence
# * volume, number, pages, article number
# * pub year, optionally month and day
# * process YYYY-MM-DD dates
# * author(s) by reference

# Repositories
# * id (used in specimen ids?)
# * insitution
# * other info?

# Provenance
# * Geologic context (e.g. mountain range)
# * Formation (by reference?)
# * Member (by reference?)
# * Local context (near what landmark, town, province, etc.)
# * Notes (for freeform things like "bought from a sketchy crystal dealer"

# Specimens
# * id
# * instituton by reference (implicit in id?)
# * sub-specimens?  Multiple on slab?
# * part / counterpart?
# * latex cast or other derivation?
# * provenance by reference

# Authority
# * prefer source by reference
# * alternately list of authors by reference
# * falback list of author names
# * year - not always available
# * "in" (same stuff, does year go here instead or in addition?)
# * "ex" (same stuff)
# * emendations?

# Taxon:
# * id
# * name
# * authority
# * altSpellingOf
# * disambituations (e.g. originalParent)
# * notes

# Node:
# * taxon (optional)
# * rank (defaults to "Clade" if null ranks allowed)
# * transl (re-ranked?) from
# * corrected from
# * new combination
# * otherewise moved
# * type flag
# * new flag
# * how to handle informal changes?
# * how to handle informal taxonomies (charts and tables)
# * children
# * specimens






import logging
import copy

from .author import build_author_id

logger = logging.getLogger(__name__)

RANKS = {
  'Domain': 120,
  'Kingdom': 110,
  'Subkingdom': 108,
  'Superphylum': 102,
  'Phylum': 100,
  'Subphylum': 98,
  'Superclass': 92,
  'Class': 90,
  'Subclass': 88,
  'Infraclass': 87,
  'Superorder': 82,
  'Order': 80,
  'Suborder': 78,
  'Infraorder': 77,
  'Superfamily': 72,
  'Family': 70,
  'Subfamily': 68,
  'genus': 60,
  'subgenus': 58,
  'species': 50,
  'subspecies': 48,
  'Branch': 0,
  'Series': 0,
  'Grade': 0,
  'Clade': 0,
  'Plesion': 0,
  'Scion': 0,
}

NEEDS_RANK = {
  'Cincta': ('Class', 'Order'),
  'Soluta': ('Class', 'Order'),
  'Stylophora': ('Superorder'), # Class by default
  'Gogiida': ('Class',), # Order by default
  'Rhombifera': ('Class', 'Order'), # genus by default
  'Glyptocystitida': ('Order', 'Superfamily'),
  'Glyptocystitoida': ('Order', 'Superfamily'),
  'Hemicosmitida': ('Order', 'Superfamily'),
  'Hemicosmitoida': ('Order', 'Superfamily'),
  'Polycosmitida': ('Order', 'Superfamily'),
  'Caryocystitida': ('Order', 'Superfamily'),
  'Diploporita': ('Class', 'Order'),
  'Aristocystitidae': ('Superfamily',), # Family by default
  'Aristocystitida': ('Order', 'Superfamily'),
  'Glyptosphaeritida': ('Order', 'Superfamily'),
  'Sphaeronitida': ('Order', 'Superfamily'),
  'Asteroblastida': ('Order', 'Superfamily'),
}


class PseudoTable():
  @classmethod
  def _registry(cls):
    raise NotImplementedError

  @classmethod
  def get(cls, thing_id, thing_data=None):
    if (
      (registered := cls._registry().get(thing_id)) is None and
      thing_data is not None
    ):
      return cls(thing_data, thing_id)
    return registered

  @classmethod
  def add(cls, thing_id, thing):
    if thing_id in cls._registry() and cls._registry()[thing_id] != thing:
      raise ValueError(
        f'Collision for {cls.__name__} "{thing_id}"\n'
        f'\told:\n{cls._registry()[thing_id]}\n\tnew:\n{thing}'
      )

  def __init__(self, thing_data, thing_id=None):
    self._data = copy.deepcopy(thing_data)
    expected_id = self._build_id()
    if thing_id is not None and thing_id != expected_id:
      raise ValueError(
        f'Expected id "{expected_id}" but got "{thing_id}" '
        f'for {self.__class__.__name__}:\n\t{self._data}'
      )
    self._id = expected_id
    self.add(self)

  @property
  def id(self):
    return self._id


class Publication(PseudoTable):
  _pub_registry = {}

  @classmethod
  def _registry(cls):
    return cls._pub_registry

  @property
  def name(self):
    return self._data['name']

  @property
  def editors(self):
    if self._editors is not None:
      self._editors = [Author.get(e) for e in self._data.get('editors', [])]
      if None in self._editors:
        raise ValueError(
          f"Unrecognized editors in {self._data['editors']} ({self._editors})"
        )
    return self._editors

  def _build_id(self):
    return self.name


class Author(PseudoTable):
  _author_registry = {}

  @classmethod
  def _registry(cls):
    return cls._author_registry

  def _build_id(self):
    return self.build_id_from_name(self.name)

  @classmethod
  def build_id_from_name(cls, name):
    # Notably, this can be used on names that do not correspond
    # to full register-able Author objects.
    logger.debug(f'build: {name}')
    if name.islower() and '.' in name:
      author_id = name
    else:
      components = [c.strip().lower() for c in name.split('.')]
      author_id = '.'.join(components[-1:] + components[:-1])
    logger.debug(f'built: {author_id}')
    return author_id


class Source(PseudoTable):
  _source_registry = {}

  @classmethod
  def _registry(cls):
    return cls._source_registry

  def _build_id(self):
    source_id = f"{(self._data['pubDate']['year'])}_"
    source_id += '_' + '_'.join(
      [Author.build_id_from_name(a) for a in self._data['authors']]
    )
    return source_id


class Authority(PseudoTable):
  _authority_registry = {}

  @classmethod
  def _registry(cls):
    return cls._authority_registry

  def __init__(self, authority_data, authority_id=None):
    self._authors = None
    super().__init__(
      # Filter authority out of taxon
      # TODO: Less of a hack, also, what about the 'notes' field?
      {k: v for k, v in authority_data.items() if k in {
        'authority',
        'auth',
        'year',
        'in',
        'ex',
        'notes',
      }},
      authority_id,
    )

  def _build_id(self):
    if (auth_obj := self._data.get('authority')):
      components = auth_obj['source'].split('_')

      # Strip off any letter suffix, e.g. 1967a
      self._year = int(components[0][:4])
      author_ids = components[1:]
      self._authors = [Author.get(i) for i in author_ids]

    else:
      try:
        self._year = self._data['year']
      except (KeyError, ValueError):
        self._year = None

      self._authors = []
      author_ids = []

      for a in self._data.get('auth', []):
        if (author := Author.get(a)):
          self._authors.append(author)
          author_ids.append(a)
        else:
          # support a mix of Author objects and bare strings
          # until the author set is thoroughly populated.
          self._author.append(a)
          author_ids.append(Author.build_id_from_name(a))

    return '_'.join(author_ids + [str(self._year)])

  @property
  def authors(self):
    if self._authors == None:
      if (authority := self._data.get('authority')):
        components = authority['source'].split('_')
        year = components[0][:4] # cut off any letter, e.g. 1967a
        
        self._authors = [Author(a) for a in self._data['authors']]


class Taxon(PseudoTable):
  _taxon_registry = {}

  _ALWAYS_QUALIFY = ('species', 'subspecies', 'variant')
  _ALWAYS_APPEND_RANK = ('Grade', 'Branch')

  @classmethod
  def _registry(cls):
    return cls._taxon_registry

  def __init__(self, taxon_data, taxon_id=None):
    self._name = taxon_data.get('name')
    self._rank = taxon_data.get('rank')
    if (self._name, self._rank) == (None, None):
      raise ValueError(f'Taxon "{expected}" has neither name nor rank')

    if self._name is None and taxon_id is None:
        raise ValueError(f"Need id for anonymous taxon:\n\t{self._data}")
    self._provided_id = taxon_id

    if self._rank is None:
      self._rank = 'species' if self.name[0].islower() else 'genus'

    self._authority = Authority(taxon_data)

    super().__init__(taxon_data, taxon_id)

  @property
  def id(self):
    return self._id

  @property
  def name(self):
    return self._name

  @property
  def rank(self):
    return self._year

  @property
  def authority(self):
    return self._authority

  @property
  def homonym(self):
    return self._data.get('homonym', False)

  def _build_id(self, expected):
    if self.rank is None:
      if self.name is None:
        raise ValueError(f'Taxon "{expected}" has neither name nor rank')

      self._data['rank'] = 'species' if self.name[0].islower() else 'genus'

    if not self.name:
      if expected is None:
        raise ValueError(
          f"Need expected id for anonymous taxon:\n\t{self._data}"
        )

    self._
    if expected is None:
      expected = self.name.lower()

    if self.homonym or self.rank in ('species', 'subspecies', 'variant'):
      for author in taxon['auth']:
        logger.debug(f'Requesting "{author}" id for taxon')
        expected += '_' + Author.build_id_from_name(author)
      expected += '_' + str(taxon['year'])

    if (year := self._data.get('year')):
      # 15 pretty arbitrary, no clue if there's a kid genius paleontologist
      if 'birth' in author and year < (author['birth'] + 15):
        birth = author['birth']
        logger.error(f'"{author_id}" born {birth} as authority in {year}?')
      # plus 5 for Barrande 1887
      if 'death' in author and year > (author['death'] + 5): 
        death = author['death']
        logger.error(f'"{author_id}" died {death} as authority in {year}?')

    if 'originalParent' in taxon:
      expected += '_' + taxon['originalParent']

    if (
      rank in NEEDS_RANK.get(name, ()) or
      rank in ('subgenus', 'subspecies')
    ):
      return expected + '-' + rank.lower()
    return expected

  def compare_ranks(self, other):
    r1, r2 = RANKS[self.rank], RANKS[other.rank]
    if r1 == r2:
      return 0
    if r1 < r2:
      return -1
    return 1
