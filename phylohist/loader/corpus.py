"""The records and trees of one load (`load.load`), handed explicitly to
everything that looks a record up. Each load builds a corpus of its own."""

from ..ranks import TABLE
from .research import Author, Publication, Source, SourceAlias
from .taxa import Section, Taxon


class Corpus:
  """What one load builds: the author, publication, source, taxon and
  section records, each a dict from key to record in the order added; the
  repository registry (`data/repositories.yaml`); the rank table (`ranks`,
  a `ranks.RankTable`: the load's `ranks.yaml`, the repository's own for a
  bare `Corpus()`); the data files as loaded (`data`); and ``{source_key:
  [root Tree]}`` (`roots`). A record is built against the corpus it is
  added to and keeps no reference to it."""

  def __init__(self, repositories=None, ranks=None):
    self.authors = {}
    self.publications = {}
    self.sources = {}
    self.taxa = {}
    self.sections = {}
    self.repositories = dict(repositories or {})
    self.ranks = ranks if ranks is not None else TABLE
    self.data = None
    self.roots = {}

  # Each record is built, then stored: one whose constructor ends the load
  # (`io.fail`) is not stored.
  def add_author(self, data, key):
    self.authors[key] = Author(data, key)

  def add_publication(self, data, key):
    self.publications[key] = Publication(data, key, self)

  def add_source(self, data, key):
    """A source record, or an alias (`aliasOf`); an alias whose target is
    missing or itself an alias has been logged, and is not stored."""
    if 'aliasOf' in data:
      alias = SourceAlias(data, key, self)
      if alias.canonical is not None:
        self.sources[key] = alias
    else:
      self.sources[key] = Source(data, key, self)

  def add_taxon(self, data, key):
    self.taxa[key] = Taxon(data, key, self)

  def add_section(self, data, key):
    self.sections[key] = Section(data, key, self)

  def copy(self):
    """A corpus whose dicts are its own, sharing the records and trees: what
    is added to the copy is not in this one. `data` is copied at its top
    level, `roots` with its lists."""
    other = Corpus(self.repositories, self.ranks)
    other.authors = dict(self.authors)
    other.publications = dict(self.publications)
    other.sources = dict(self.sources)
    other.taxa = dict(self.taxa)
    other.sections = dict(self.sections)
    other.data = None if self.data is None else dict(self.data)
    other.roots = {key: list(trees) for key, trees in self.roots.items()}
    return other

  def protologue_sources(self):
    """``{taxon_key: {source_key}}``: the sources whose trees flag the
    taxon `new`. A slip of the pen is where the name it prints appears, so
    a node under `lapsus` is that name's protologue whether or not the slip
    also claimed it as new."""
    index = {}
    for trees in self.roots.values():
      for root in trees:
        for node in root.walk():
          if node.taxon is not None and (node.data.get('new') or node.axis == 'lapsus'):
            index.setdefault(node.taxon.key, set()).add(node.source.key)
    return index
