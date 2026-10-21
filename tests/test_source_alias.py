"""A source alias (`aliasOf`) cites a paper by some of its authors, as ICZN
attribution requires ("Banks 1985" for a name Banks alone established in
Jell, Burrett & Banks 1985). Its key's year and letter are the target's, its
authors a strict subset of the target's in their order; everything else is
the target's.

The aliases are synthetic, built on the test corpus; the registries they
write to are restored before every test (`conftest.py`).
"""

import importlib
import logging
import types

import pytest

from phylohist.claims import manifest
from phylohist.loader import LoadError, load
from phylohist.loader.load import _load_sources
from phylohist.loader.research import Source
from phylohist.loader.taxa import Authority, Taxon, Tree
from phylohist.resolve import Resolver

TARGET = '1985_jell_burrett_banks'


def _add(key, target=TARGET, caplog=None):
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    caplog.clear()
    Source.add({'aliasOf': target}, key)
  return [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]


ALIASES = ['1985_jell', '1985_banks', '1985_jell_banks', '1985_burrett_banks']


@pytest.mark.parametrize('key', ALIASES)
def test_an_ordered_strict_subset_is_an_alias(key, caplog):
  assert _add(key, caplog=caplog) == []
  alias = Source.get(key)
  assert alias.canonical is Source.get(TARGET)
  assert alias.alias_of == TARGET
  assert alias.author_keys_string == key.partition('_')[2]
  assert [a.key for a in alias.authors] == key.partition('_')[2].split('_')
  assert (alias.year, alias.disambiguator, alias.title) == (1985, '', Source.get(TARGET).title)


@pytest.mark.parametrize(
  ('key', 'message'),
  [
    ('1984_banks', 'Alias "1984_banks" year "1984" does not match "1985_jell_burrett_banks"'),
    ('1985a_banks', 'Alias "1985a_banks" year "1985a" does not match "1985_jell_burrett_banks"'),
    ('1985_banks_jell', 'authors must be a strict subset'),
    ('1985_banks_burrett_jell', 'authors must be a strict subset'),
    ('1985_sprinkle', 'authors must be a strict subset'),
  ],
)
def test_a_key_that_does_not_fit_its_target_is_an_error(key, message, caplog):
  errors = _add(key, caplog=caplog)
  assert len(errors) == 1 and message in errors[0]


def test_an_author_with_no_record_ends_the_load(caplog):
  # The alias cannot be built without its authors, so the load stops here
  # with a `LoadError` instead of going on to a crash in `Source.__str__`.
  with (
    caplog.at_level(logging.ERROR, logger='phylohist'),
    pytest.raises(LoadError, match='source alias 1985_nobody names author "nobody"'),
  ):
    Source.add({'aliasOf': TARGET}, '1985_nobody')
  assert [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR] == [
    'Author "nobody" not found for source alias 1985_nobody!'
  ]
  assert Source.get('1985_nobody') is None


def test_the_target_must_be_a_source_record(caplog):
  assert _add('1985_banks', caplog=caplog) == []
  errors = _add('1985_jell', target='1985_banks', caplog=caplog)
  assert errors == ['Alias "1985_jell" names "1985_banks", which is itself an alias']
  assert Source.get('1985_jell') is None
  errors = _add('1985_jell', target='1985_nobody', caplog=caplog)
  assert errors == ['Alias "1985_jell" names source "1985_nobody", which does not exist']
  assert Source.get('1985_jell') is None


def test_an_alias_may_precede_its_target(caplog):
  target_data = Source.get(TARGET)._data
  del Source._sources[TARGET]
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    _load_sources({'sources': {'1985_banks': {'aliasOf': TARGET}, TARGET: target_data}})
  assert [r for r in caplog.records if r.levelno >= logging.ERROR] == []
  assert Source.get('1985_banks').canonical is Source.get(TARGET)


def test_an_authority_by_alias_cites_the_alias_authors(caplog):
  _add('1985_banks', caplog=caplog)
  authority = Authority({'authority': {'source': '1985_banks'}})
  assert str(authority) == 'Banks 1985'
  assert authority.taxon_suffix == 'banks_1985'


def _protologue_errors(new, caplog):
  _add('1985_banks', caplog=caplog)
  key = 'testum_banks_1985'
  Taxon.add({'name': 'testum', 'rank': 'species', 'authority': {'source': '1985_banks'}}, key)
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    caplog.clear()
    Tree(
      {'taxon': key, 'new': new},
      {'source_key': TARGET, 'type': 'taxonomy', 'position': 400, 'file_unused': ()},
    )
  return [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]


def test_a_new_taxon_by_alias_is_new_in_the_target_tree(caplog):
  assert _protologue_errors(True, caplog) == []


def test_a_taxon_by_alias_in_the_target_tree_must_be_new(caplog):
  errors = _protologue_errors(False, caplog)
  assert len(errors) == 1 and 'but is not marked as new' in errors[0]


def test_a_tree_file_named_by_an_alias_is_skipped(monkeypatch, caplog):
  loading = importlib.import_module('phylohist.loader.load')

  def aliased(drafts=False, **_):
    data = {k: {} for k in ('authors', 'publications', 'taxa', 'sections')}
    data['sources'] = {'1985_banks': {'aliasOf': TARGET}}
    data['trees'] = {'1985_banks': {'taxonomies': [{'taxon': 'cyathocystis'}]}}
    return data

  monkeypatch.setattr(loading, 'load_files', aliased)
  with pytest.raises(LoadError, match='1 integrity error'):
    load()
  assert f'Tree file "1985_banks" is named by an alias; name it "{TARGET}"' in caplog.text
  _, roots = load(tolerate=True)
  assert roots == {}


def test_the_manifest_row_of_an_alias_is_its_citation_and_target(caplog):
  _add('1985_banks', caplog=caplog)
  rows = manifest({}, {})['sources']
  target = rows[TARGET]['citation']
  assert rows['1985_banks'] == {
    'citation': {**target, 'authors': ['Banks']},
    'aliasOf': TARGET,
  }


def _resolver():
  def row(authors, **extra):
    return {'citation': {'authors': authors, 'year': 1985}, 'tree': True, **extra}

  sources = {
    TARGET: row(['Jell', 'Burrett', 'Banks']),
    '1985_jell': {**row(['Jell']), 'aliasOf': TARGET},
    '1985_banks': {**row(['Banks']), 'aliasOf': TARGET},
    '1985_jell_sprinkle': row(['Jell', 'Sprinkle']),
  }
  return Resolver(types.SimpleNamespace(sources=sources))


def test_a_parameter_naming_an_alias_names_its_target():
  resolver = _resolver()
  assert resolver.source_key('1985_banks') == TARGET
  assert resolver.source_key('1985_Banks') == TARGET
  assert resolver.source_key('Banks 1985') == TARGET
  assert resolver.source_key(TARGET) == TARGET


def test_an_alias_and_its_target_resolve_as_one_paper():
  resolver = _resolver()
  assert [c['key'] for c in resolver.resolve_source('Banks 1985')] == [TARGET]
  assert [c['key'] for c in resolver.resolve_source('1985_banks')] == [TARGET]
  # "Jell 1985" finds the alias and its target, one paper, and another.
  assert [c['key'] for c in resolver.resolve_source('Jell 1985')] == [
    TARGET,
    '1985_jell_sprinkle',
  ]
