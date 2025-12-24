import sys
import pathlib
import logging
import collections
from functools import cached_property
import calendar

import yaml
import jschon

logger = logging.getLogger(__name__)


class Author:
  _authors = {}

  @classmethod
  def add(cls, author_data, author_key):
    cls._authors[author_key] = Author(author_data, author_key)

  @classmethod
  def get(cls, author_key):
    return cls._authors.get(author_key, None)

  def __init__(self, author_data, author_key=None):
    self._data = author_data
    self._key = author_key

    # Unregistered authors can lack a key
    if not self._key:
      return

    family_only = author_data['family'].lower()
    givens = author_data['given'].split(' ')
    if len(givens) == 1:
      givens = givens[0].split('-')
    with_initials = \
      f'{family_only}.' + '.'.join([name[0].lower() for name in givens])

    expected_set = {family_only, with_initials}
    if author_key not in expected_set:
      logger.error(f'"{author_key}" not in expected set: {expected_set}')

  def __str__(self):
    string = f'{family}, {given}'
    if self.birth:
      string += f'({self.birth} – '
      if self.death:
        string += str(self.death)
      string += ')'
    return string

  @property
  def key(self):
    return self._key

  @cached_property
  def family(self):
    return self._data.get('family')

  @cached_property
  def given(self):
    return self._data.get('given')

  @cached_property
  def birth(self):
    return self._data.get('birth')

  @cached_property
  def death(self):
    return self._data.get('death')

  def could_publish_in(self, year):
    # This is a weird heuristic right now, needs improvement.
    if (
      # 15 pretty arbitrary, no clue if there's a kid genius paleontologist
      self.birth and year < (self.birth + 15) or
      # plus 5 for Barrande 1887
      self.death and year > (self.death + 5)
    ):
      return False
    return True


class Publication:
  _publications = {}

  @classmethod
  def add(cls, pub_data, pub_key):
    cls._publications[pub_key] = Publication(pub_data, pub_key)

  @classmethod
  def get(cls, pub_key):
    return cls._publications.get(pub_key)

  def __init__(self, pub_data, pub_key):
    self._data = pub_data
    self._key = pub_key

    for editor in self._data.get('editors', ()):
      if Author.get(editor) is None:
        logger.error(f'Editor "{editor}" not found for publication {pub_key}!')

  @property
  def key(self):
    return self._key


class PublicationDate:
  def __init__(self, pub_date):
    self._year = pub_date['year']
    self._month = pub_date.get('month')
    self._day = pub_date.get('day')

  def __str__(self):
    string = self._year
    if self._month:
      string = f'{calendar.month_name[self._month]} {string}'
      if self._day:
        string = f'{self._day} {string}'
    return string

  @property
  def year(self):
    return self._year

  @property
  def month(self):
    return self._month

  @property
  def day(self):
    return self._day


class Source:
  _sources = {}

  @classmethod
  def add(cls, source_data, source_key):
    cls._sources[source_key] = Source(source_data, source_key)

  @classmethod
  def get(cls, source_key):
    return cls._sources.get(source_key)

  @classmethod
  def count(cls):
    return len(cls._sources)

  def __init__(self, source_data, source_key):
    self._data = source_data
    self._key = source_key

    self._author_keys = tuple(self._data['authors'])
    self._authors = []
    self._editors = []

    if self.in_preparation:
      self._pub_date = None
    else:
      self._pub_date = PublicationDate(self._data['pubDate'])

    logger.debug(f'Processing source "{source_key}"')

    if source_data.get('inPrep'):
      expected_key = 'inprep'
    else:
      source_type = (source_data.keys() & {'journal', 'book', 'reading'}).pop()
      if Publication.get(source_data[source_type]) is None:
        logger.error(f'{source_type} "{source_data[source_type]}" not found!')
      expected_key = f"{source_data['pubDate']['year']}"
      if source_key[4] != '_':
        # There's a disambiguation letter, just assume it is correct.
        # TODO: figure out something better for disambiguation letters.
        expected_key += source_key[4]

    for author_key in self._author_keys:
      if (author := Author.get(author_key)) is None:
        logger.error(
          f'Author "{author_key}" not found for source_data {source_key}!',
        )
      self._authors.append(author)
      expected_key += '_' + author.key
    self._authors = tuple(self._authors)

    for editor_key in source_data.get('editors', ()):
      if (editor := Author.get(editor_key)) is None:
        logger.error(
          f'Editor "{editor_key}" not found for source_data {source_key}!',
        )
      self._editors.append(editor)
    self._editors = tuple(self._editors)

    if source_key != expected_key:
      logger.error(f'Expected "{expected_key}" but found "{source_key}"')

    if (
      (trans_of := source_data.get('translationOf')) and
      Source.get(trans_of) is None
    ):
      logger.error(
        f'Translation source "{trans_of}" for "{source_key}" not found!'
      )

  @property
  def key(self):
    return self._key

  @property
  def publication_date(self):
    return self._pub_date

  @property
  def year(self):
    return self._pub_date.year

  @property
  def disambiguator(self):
    if self._key[4] != '_':
      return self._key[4]
    return ''

  @property
  def authors(self):
    return self._authors

  @property
  def author_keys_string(self):
    return '_'.join(self._author_keys)

  @property
  def in_preparation(self):
    return self._data.get('inPrep', False)
