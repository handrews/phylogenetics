"""The suffix lint over the rank table (`data/ranks.yaml`,
`phylohist/ranks.py`): which records it checks, from which year, in which
directions, and the exceptions the table carries.

Synthetic records are added to each test's copy of the loaded test corpus
(`records`); a credit with a year stands for the authority, since the
lint reads the year alone."""

import logging

import pytest
import yaml

from phylohist import ranks
from phylohist.derivatives import KINDS
from phylohist.loader.load import _report_rank_exceptions
from tests import support

SOURCE = {'source': '1758_linnaeus'}
MODERN = {'auth': [], 'year': 1950}
SUFFIX_WORDS = ('expected to end with suffix', 'expected to have one of ranks')


def _warned(caplog, records, data, key):
  with caplog.at_level(logging.WARNING, logger='phylohist'):
    caplog.clear()
    records.add_taxon(data, key)
  return [
    r.getMessage()
    for r in caplog.records
    if r.levelno == logging.WARNING and any(w in r.getMessage() for w in SUFFIX_WORDS)
  ]


def _errors(caplog):
  return [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]


def test_the_lint_checks_names_from_the_cut_year(records, caplog):
  record = {'name': 'Testida', 'rank': 'Class'}
  assert (
    _warned(caplog, records, {**record, 'authority': {'auth': [], 'year': 1899}}, 'testida') == []
  )
  assert _warned(
    caplog, records, {**record, 'authority': {'auth': [], 'year': 1900}}, 'testida'
  ) == ['Testida with suffix "ida" expected to have one of ranks (Order) but has rank Class']
  # No year, no check.
  assert _warned(caplog, records, {**record, 'authority': {'auth': []}}, 'testida') == []


def test_a_rank_expects_its_ending(records, caplog):
  assert _warned(
    caplog, records, {'name': 'Testa', 'rank': 'Family', 'authority': MODERN}, 'testa'
  ) == ['Testa of rank Family expected to end with suffix "idae"']
  assert _warned(
    caplog, records, {'name': 'Testidae', 'rank': 'Subfamily', 'authority': MODERN}, 'testidae'
  ) == [
    'Testidae of rank Subfamily expected to end with suffix "inae"',
    'Testidae with suffix "idae" expected to have one of ranks (Family) but has rank Subfamily',
  ]
  assert _warned(
    caplog, records, {'name': 'Testozoa', 'rank': 'Order', 'authority': MODERN}, 'testozoa'
  ) == [
    'Testozoa with suffix "zoa" expected to have one of ranks '
    '(Class, Subphylum, Phylum, Subkingdom, Kingdom) but has rank Order'
  ]


def test_a_superfamily_ends_in_acea_before_1999_and_oidea_always(records, caplog):
  record = {'name': 'Testacea', 'rank': 'Superfamily'}
  assert (
    _warned(caplog, records, {**record, 'authority': {'auth': [], 'year': 1998}}, 'testacea') == []
  )
  assert _warned(
    caplog, records, {**record, 'authority': {'auth': [], 'year': 1999}}, 'testacea'
  ) == ['Testacea of rank Superfamily expected to end with suffix "oidea"']
  assert _warned(
    caplog, records, {'name': 'Testa', 'rank': 'Superfamily', 'authority': MODERN}, 'testa'
  ) == ['Testa of rank Superfamily expected to end with suffix "oidea" or "acea"']
  # -oidea implies no rank: echinoderm classes end in it.
  assert (
    _warned(
      caplog, records, {'name': 'Testoidea', 'rank': 'Class', 'authority': MODERN}, 'testoidea'
    )
    == []
  )


@pytest.mark.parametrize('rank', ['Grade', 'genus', None])
def test_an_informal_rank_the_genus_group_and_no_rank_are_not_checked(records, caplog, rank):
  assert (
    _warned(caplog, records, {'name': 'Testida', 'rank': rank, 'authority': MODERN}, 'testida')
    == []
  )


@pytest.mark.parametrize('kind', KINDS, ids=[kind.field for kind in KINDS])
def test_a_derivative_is_checked_by_its_kind(records, caplog, kind):
  # A Latin spelling and a rank variant are names in their own right; a
  # spelling, a gender form and a vernacular form are not.
  records.add_taxon(
    {'name': 'Testidae', 'rank': 'Family', 'lang': 'DE', 'authority': MODERN}, 'testidae'
  )
  variant = {'name': 'Testida', kind.field: 'testidae'}
  if kind.field == 'altRankOf':
    variant['rank'] = 'Family'
  if kind.lang == 'record':
    variant['lang'] = 'DE'
  warned = _warned(caplog, records, variant, 'testida')
  assert bool(warned) == kind.suffix_checked
  assert {k.field for k in KINDS if k.suffix_checked} == {'latinSpellingOf', 'altRankOf'}


def test_an_exception_passes_a_name_at_its_rank_only(records, caplog):
  excepted = {
    **ranks.TABLE.document,
    'exceptions': [{'name': 'Testida', 'rank': 'Class', 'note': 'x'}],
  }
  records.ranks = ranks.RankTable(excepted)
  assert (
    _warned(caplog, records, {'name': 'Testida', 'rank': 'Class', 'authority': MODERN}, 'testida')
    == []
  )
  assert (
    _warned(
      caplog, records, {'name': 'Testida', 'rank': 'Subclass', 'authority': MODERN}, 'testida'
    )
    != []
  )


def test_a_stale_exception_is_an_error(records, caplog):
  records.add_taxon({'name': 'Testida', 'rank': 'Class', 'authority': MODERN}, 'testida')
  records.ranks = ranks.RankTable(
    {
      **ranks.TABLE.document,
      'exceptions': [
        {'name': 'Nonesuchida', 'rank': 'Class', 'note': 'x'},
        {'name': 'Testida', 'rank': 'Order', 'note': 'x'},
        {'name': 'Testida', 'rank': 'Class', 'note': 'x'},
      ],
    }
  )
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    _report_rank_exceptions(records)
  assert _errors(caplog) == [
    'ranks.yaml: exception Nonesuchida (Class) names no record',
    'ranks.yaml: exception Testida (Order) names a record at another rank (Class)',
  ]


def test_the_corpora_share_the_vocabulary_and_keep_their_own_exceptions(corpus):
  # The loaded corpus carries no suffix warning and its exceptions all
  # name records; the frozen corpus keeps an exception `data/` has outgrown.
  assert not [w for w in corpus.logged.warnings if any(s in w for s in SUFFIX_WORDS)]
  assert ('Hemicosmitida', 'Superfamily') in corpus.records.ranks.exceptions
  assert ('Hemicosmitida', 'Superfamily') not in ranks.TABLE.exceptions
  live = yaml.safe_load(ranks.TABLE_PATH.read_text())
  frozen = yaml.safe_load((support.CORPUS / 'ranks.yaml').read_text())
  live.pop('exceptions'), frozen.pop('exceptions')
  assert live == frozen


def test_a_null_rank_record_with_a_qualified_key_is_checked_without_a_rank_form(records, caplog):
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    caplog.clear()
    records.add_taxon({'name': 'Testa', 'rank': None, 'authority': SOURCE}, 'testa-x')
  assert _errors(caplog) == ['"testa-x" not in expected set: {\'testa\'}']
