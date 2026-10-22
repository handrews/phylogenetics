"""Loads all data files in-process and checks the logs they produce.

Fails on any ERROR-level log record. Compares WARNING-level messages against
``tests/expected-warnings.txt``: a new line there is allowed only in a commit
that adds a check, and every line is a resolution owed, so a line the load
no longer produces is only a warning here; ``poetry run regenerate`` drops it
(`scripts/expected_warnings.py`). The load itself is the ``production``
fixture in ``conftest.py``; these are the tests about the curated corpus,
marked ``production``.

``PHYLOHIST_DRAFTS=1`` also loads the unaudited trees under ``drafts/``
(the CLI's ``--draft``). Drafts are expected to produce errors and
warnings until their records exist, so the warning snapshot is not
compared in that mode; the error test still reports what a draft needs.
"""

import logging
import os
import pathlib
import warnings

import pytest

from phylohist import regenerate

EXPECTED_WARNINGS_PATH = pathlib.Path(__file__).parent / 'expected-warnings.txt'


@pytest.mark.production
def test_no_errors(production):
  errors = [r for r in production.records if r.levelno >= logging.ERROR]
  if errors:
    message = '\n'.join(r.getMessage() for r in errors)
    pytest.fail(f'{len(errors)} ERROR-level log records:\n{message}')


@pytest.mark.production
def test_data_loaded(production):
  assert production.data['trees'], 'load produced no trees; check for a silent empty load'


@pytest.mark.production
def test_expected_warnings(production):
  if os.getenv('PHYLOHIST_DRAFTS'):
    pytest.skip('drafts loaded; the warning snapshot covers data/ only')
  actual = {r.getMessage() for r in production.records if r.levelno == logging.WARNING}
  expected = regenerate.read_expected(EXPECTED_WARNINGS_PATH)

  stale = expected - actual
  if stale:
    # A resolved warning is progress: `regenerate` drops its line, and CI's
    # diff of the derived files catches a line left behind.
    warnings.warn(
      f'{len(stale)} expected warnings are no longer produced; run `poetry run regenerate`:\n'
      + '\n'.join(sorted(stale)),
      stacklevel=1,
    )
  unexpected = actual - expected
  if unexpected:
    pytest.fail(
      'Unexpected warnings (not in tests/expected-warnings.txt; a new line there is allowed '
      'only in a commit that adds a check):\n' + '\n'.join(sorted(unexpected))
    )


def test_invalid_tree_raises(tmp_path):
  # A file that fails the schema stops the load with an error the caller
  # can handle, instead of ending the process.
  from phylohist.loader import io

  schema = io.build_schema()
  (tmp_path / 'broken.yaml').write_text('tree:\n  rnak: genus\n')
  with pytest.raises(io.LoadError, match='broken.yaml'):
    io.load_checked(tmp_path / 'broken.yaml', schema[io.TREE_DEF])
  # A definition the schema lacks is an error the loader names, too.
  with pytest.raises(io.LoadError, match='no schema definition for "trees"'):
    schema['trees']


def test_schema_error_names_its_file(tmp_path, caplog):
  # The file name was only on the INFO line above the dump.
  from phylohist.loader import io

  schema = io.build_schema()
  broken = tmp_path / 'broken.yaml'
  broken.write_text('tree:\n  rnak: genus\n')
  with caplog.at_level(logging.ERROR, logger='phylohist'), pytest.raises(io.LoadError):
    io.load_checked(broken, schema[io.TREE_DEF])
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert errors and all(m.startswith(f'"{broken}" is not valid:\n') for m in errors)
  # A file under the repository is named by its path from the root.
  assert io.display_path(io.TREE_DIR / '1761_linnaeus.yaml') == 'data/trees/1761_linnaeus.yaml'


def test_data_files_in_load_order(tmp_path, monkeypatch):
  # The record files, then the audited trees, then the drafts: a draft
  # loads last so that it replaces the audited tree of its source.
  from phylohist.loader import io

  data_dir = tmp_path / 'data'
  (data_dir / 'trees').mkdir(parents=True)
  drafts = tmp_path / 'drafts'
  drafts.mkdir()
  audited = [data_dir / 'trees' / f'{key}.yaml' for key in ('1761_linnaeus', '1962_fay')]
  for path in (*audited, drafts / '1962_fay.yaml'):
    path.write_text('')
  monkeypatch.setattr(io, 'DRAFT_DIR', drafts)

  files = io.data_files(drafts=True, data_dir=data_dir)
  assert [name for name, _ in files] == [*io.RECORD_NAMES, *[io.TREE_DEF] * 3]
  assert io.RECORD_NAMES[:3] == ('authors', 'publications', 'sources')
  assert [path for _, path in files] == [
    *io.record_files(data_dir),
    *audited,
    drafts / '1962_fay.yaml',
  ]
  assert [path for _, path in io.data_files(data_dir=data_dir)] == [
    *io.record_files(data_dir),
    *audited,
  ]
  # The defaults are the repository's own data.
  assert io.RECORD_FILES == io.record_files() and io.RECORD_FILES[0] == io.DATA_DIR / 'authors.yaml'


def test_load_fails_on_logged_errors(monkeypatch):
  # The checks report by logging; the load counts what they logged and
  # refuses to hand over a broken corpus unless asked to.
  import importlib

  from phylohist.loader import LoadError, load

  loading = importlib.import_module('phylohist.loader.load')

  def broken(drafts=False, **_):
    logging.getLogger('phylohist.loader.taxa').error('a check fired')
    return {k: {} for k in ('authors', 'publications', 'sources', 'taxa', 'sections', 'trees')}

  monkeypatch.setattr(loading, 'load_files', broken)
  with pytest.raises(LoadError, match='1 integrity error while loading'):
    load()
  data, roots = load(tolerate=True)
  assert data['trees'] == {} and roots == {}


@pytest.mark.parametrize(
  'field, relation',
  [
    ('altSpellingOf', 'alt spelling'),
    ('altGenderOf', 'gender variant'),
    ('latinSpellingOf', 'Latin spelling'),
    ('vulgarSpellingOf', 'vulgar spelling'),
    ('altRankOf', 'alt rank'),
  ],
)
def test_an_unknown_spelling_or_rank_target_is_named(field, relation, caplog):
  # The record a taxon is a spelling or rank of must exist: the error names
  # both keys and ends the load, as a file that fails the schema does.
  from phylohist.loader import LoadError
  from phylohist.loader.taxa import Taxon

  with caplog.at_level(logging.ERROR, logger='phylohist'), pytest.raises(LoadError):
    Taxon.add({'name': 'Testum', field: 'nobody_nowhere'}, 'testum')
  [record] = [r for r in caplog.records if r.levelno == logging.ERROR]
  assert record.getMessage() == f'Taxon testum {relation} of unknown nobody_nowhere'
  # `io.fail` logs on the check's own line.
  assert (record.filename, record.funcName) == ('taxa.py', '_known')
  assert Taxon.get('testum') is None


def test_a_tree_cites_only_sources_with_a_record(caplog):
  # Every source id a tree file carries must name a record: an authority's
  # `source` wherever the authority sits, a `sameAs` link's, and a context's
  # `sources`; an alias counts. The census says the same of the data after
  # the fact; the loader says it beside its other errors, with the path.
  import importlib

  from phylohist.loader.research import Source

  loading = importlib.import_module('phylohist.loader.load')
  Source.add({'aliasOf': '1985_jell_burrett_banks'}, '1985_banks')
  nobody = {'source': '1899_nobody'}
  document = {
    'contexts': {'f': {'sources': ['1961_dehm', '1899_nobody']}},
    'taxonomies': [
      {
        'taxon': 'rhenopyrgus',
        'authority': {'source': '1961_dehm'},
        'emendedBy': [{'source': '1983_holloway_jell'}, {'source': '1975_parsley_mintz'}],
        'type': {'taxon': 'grayae_bather_1915', 'fixedBy': nobody},
        'children': [
          {
            'taxon': 'grayae_bather_1915',
            'authority': nobody,
            'material': [{'label': 'A', 'sameAs': {**nobody, 'label': 'B'}}],
            'editorial': {'corrections': {'authority': nobody}},
            'contexts': {'n': {'sources': ['1985_banks']}},
          },
        ],
      },
    ],
    'phylogenies': [
      {
        'tree': {
          'taxon': 'rhenopyrgus',
          'children': [{'taxon': 'grayae_bather_1915', 'authority': {'source': '1985_banks'}}],
        }
      }
    ],
  }
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    loading._report_cited_sources({'trees': {'1961_dehm': document}})
  errors = sorted(r.getMessage() for r in caplog.records if r.levelno == logging.ERROR)
  tail = ', which has no source record'
  child = '1961_dehm at 0/children/0'
  assert errors == [
    f'{child}: `authority/source` names "1899_nobody"{tail}',
    f'{child}: `editorial/corrections/authority/source` names "1899_nobody"{tail}',
    f'{child}: `material/0/sameAs/source` names "1899_nobody"{tail}',
    f'1961_dehm at 0/type: `fixedBy/source` names "1899_nobody"{tail}',
    f'1961_dehm at 0: `emendedBy/1/source` names "1975_parsley_mintz"{tail}',
    f'1961_dehm: `contexts/f/sources/1` names "1899_nobody"{tail}',
  ]


def test_the_colour_handler_colours_a_copy_of_the_record(caplog):
  # `coloredlog` writes its codes into the record it formats; the package's
  # handler hands it a copy, so a handler after it (caplog here, the
  # expected-warnings collectors in the scripts) sees the message as logged.
  import io as stdio

  import phylohist

  coloured = phylohist.ColourHandler(stream=stdio.StringIO())
  package = logging.getLogger('phylohist')
  package.addHandler(coloured)
  try:
    with caplog.at_level(logging.WARNING, logger='phylohist'):
      logging.getLogger('phylohist.loader.taxa').warning('as logged')
  finally:
    package.removeHandler(coloured)
  [record] = [r for r in caplog.records if r.name == 'phylohist.loader.taxa']
  assert record.getMessage() == 'as logged'
  assert '\x1b[' in coloured.stream.getvalue() and 'as logged' in coloured.stream.getvalue()


def test_counting_errors_counts_only_errors():
  from phylohist.loader import counting_errors

  with counting_errors() as errors:
    logging.getLogger('phylohist.loader.io').warning('not counted')
    logging.getLogger('phylohist.loader.io').error('counted')
    logging.getLogger('phylohist.loader.research').error('counted too')
  assert errors.count == 2


def test_tree_without_a_source_record_is_skipped(monkeypatch):
  # A draft keyed by a source with no record used to crash the load in
  # the tree's hashing; now it is one logged error and no tree.
  import importlib

  from phylohist.loader import LoadError, load

  loading = importlib.import_module('phylohist.loader.load')

  def orphan(drafts=False, **_):
    data = {k: {} for k in ('authors', 'publications', 'sources', 'taxa', 'sections')}
    data['trees'] = {'9999_nobody': {'taxonomies': [{'taxon': 'cyathocystis'}]}}
    return data

  monkeypatch.setattr(loading, 'load_files', orphan)
  with pytest.raises(LoadError, match='1 integrity error'):
    load()
  _, roots = load(tolerate=True)
  assert roots == {}


# -- a record the load cannot continue without ------------------------------
#
# These checks used to log the error and go on to dereference the `None` they
# had reported, so a typo in a key ended the load in an AttributeError. Each
# now ends it in a `LoadError` naming the record (`io.fail`), with whatever
# was logged before it.


def _errors(caplog):
  return [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]


def test_fail_logs_the_detail_on_the_callers_line_and_raises_the_reason(caplog):
  import inspect

  from phylohist.loader import io

  with (
    caplog.at_level(logging.ERROR, logger='phylohist'),
    pytest.raises(io.LoadError, match='^why$'),
  ):
    line = inspect.currentframe().f_lineno + 1
    io.fail('what', 'why')
  [record] = [r for r in caplog.records if r.levelno >= logging.ERROR]
  assert (record.getMessage(), record.filename, record.lineno) == ('what', 'test_load.py', line)


@pytest.mark.parametrize('kind, file', [('Taxon', 'taxa.yaml'), ('Section', 'sections.yaml')])
def test_an_authority_source_with_no_record_ends_the_load(kind, file, caplog):
  # The record's authors and year are the source's, so there is nothing to
  # build without it; the error names the record.
  from phylohist.loader import LoadError, taxa

  cls = getattr(taxa, kind)
  with (
    caplog.at_level(logging.ERROR, logger='phylohist'),
    pytest.raises(LoadError, match='authority source "1899_nobody" has no source record'),
  ):
    cls.add({'name': 'Testum', 'authority': {'source': '1899_nobody'}}, 'testum')
  assert _errors(caplog) == [f'Authority source "1899_nobody" not recognized at {file} testum']
  assert cls.get('testum') is None


def test_an_ex_authority_citing_auctt_ends_the_load(caplog):
  # `ex` names a work (`citedWork`), which admits `auctt`; the loader
  # resolves a source, so "of authors" is an error rather than a KeyError.
  from phylohist.loader import LoadError
  from phylohist.loader.taxa import Taxon

  record = {'name': 'Testum', 'authority': {'source': '1758_linnaeus', 'ex': {'auctt': True}}}
  with (
    caplog.at_level(logging.ERROR, logger='phylohist'),
    pytest.raises(LoadError, match="a record's authority names a work or a printed credit"),
  ):
    Taxon.add(record, 'testum')
  assert _errors(caplog) == ['Authority at taxa.yaml testum cites auctt, which names no work']


@pytest.mark.parametrize(
  'record',
  [
    {'name': 'Testum', 'authority': {'auth': ['nobody'], 'year': 1850}},
    {
      'name': 'testa',
      'rank': 'species',
      'authority': {'source': '1758_linnaeus', 'attributedTo': ['nobody']},
    },
  ],
)
def test_an_author_key_with_no_record_ends_the_load(record, caplog):
  # Whether the key is in `auth` (the lifespan check reads the author) or in
  # `attributedTo` (the key check reads it), the load stops at the lookup.
  from phylohist.loader import LoadError
  from phylohist.loader.taxa import Taxon

  with (
    caplog.at_level(logging.ERROR, logger='phylohist'),
    pytest.raises(LoadError, match='author key "nobody" has no author record'),
  ):
    Taxon.add(record, 'testum')
  assert _errors(caplog) == ['Author for author key nobody not found! at taxa.yaml testum']
  assert Taxon.get('testum') is None


def test_a_source_author_with_no_record_ends_the_load(caplog):
  from phylohist.loader import LoadError
  from phylohist.loader.research import Source

  data = {**Source.get('1758_linnaeus')._data, 'authors': ['nobody']}
  with (
    caplog.at_level(logging.ERROR, logger='phylohist'),
    pytest.raises(LoadError, match='source 1758_nobody names author "nobody", which has no record'),
  ):
    Source.add(data, '1758_nobody')
  assert _errors(caplog) == ['Author "nobody" not found for source_data 1758_nobody!']
  assert Source.get('1758_nobody') is None


def test_an_author_key_is_built_from_the_surname(caplog):
  # `person` allows a surname or a given name alone: without a surname there
  # is no key form, so the load stops; without a given name the key is the
  # bare surname.
  from phylohist.loader import LoadError
  from phylohist.loader.research import Author

  with (
    caplog.at_level(logging.ERROR, logger='phylohist'),
    pytest.raises(LoadError, match='author nobody has no surname'),
  ):
    Author.add({'given': 'Nobody'}, 'nobody')
  assert _errors(caplog) == ['Author "nobody" has no surname!']
  assert Author.get('nobody') is None
  Author.add({'surname': 'Somebody'}, 'somebody')
  assert _errors(caplog) == ['Author "nobody" has no surname!']
  assert Author.get('somebody').surname == 'Somebody'


def test_an_unnamed_record_spells_its_rank(caplog):
  # Without a name there is no genus or species to read a rank from: the
  # schema requires `rank` on a null-name record, and the loader stops on
  # one that slipped through.
  from phylohist.loader import LoadError
  from phylohist.loader.taxa import Taxon
  from tests import support

  check = support.schema()['taxa'].check
  unnamed = {'name': None, 'authority': {'source': '1758_linnaeus'}}
  assert not check({'testum-sp': unnamed})
  assert check({'testum-sp': {**unnamed, 'rank': 'genus'}})
  assert check({'testum-sp': {**unnamed, 'rank': None}})
  with (
    caplog.at_level(logging.ERROR, logger='phylohist'),
    pytest.raises(LoadError, match='taxon testum-sp has neither a name nor a rank'),
  ):
    Taxon.add(unnamed, 'testum-sp')
  assert 'Unnamed, unranked taxon testum-sp!' in _errors(caplog)
  assert Taxon.get('testum-sp') is None


def test_a_record_naming_no_author_loads(caplog):
  # `auth: []` says the author is unknown: the suffix is `unknown`, the
  # authority prints as its year alone, and there is no lifespan to check.
  from phylohist.loader.taxa import Taxon

  with caplog.at_level(logging.ERROR, logger='phylohist'):
    Taxon.add(
      {'name': 'testa', 'rank': 'species', 'authority': {'auth': [], 'year': 1850}},
      'testa_unknown_1850',
    )
  assert _errors(caplog) == []
  authority = Taxon.get('testa_unknown_1850').authority
  assert authority.authors is None
  assert (str(authority), authority.taxon_suffix) == ('1850', 'unknown_1850')
  assert str(Taxon.get('hamptonii_unknown').authority) == ''


def test_a_tree_needs_metadata_or_a_parent():
  # A programming error, not a data error: it raises instead of logging.
  from phylohist.loader.taxa import Tree

  with pytest.raises(TypeError):
    Tree({'taxon': 'rhenopyrgus'})


@pytest.mark.parametrize(
  'metadata, reason',
  [
    (
      {'source_key': '1899_nobody', 'type': 'taxonomy'},
      'tree of "1899_nobody" has no source record',
    ),
    ({'source_key': '1961_dehm', 'type': 'table'}, 'unknown tree type "table"'),
  ],
)
def test_a_root_needs_a_source_record_and_a_known_type(metadata, reason, caplog):
  # Every node hashes by its source, so a root whose metadata names no
  # source record (or a type the loader does not know) cannot be built.
  from phylohist.loader import LoadError
  from phylohist.loader.taxa import Tree

  with caplog.at_level(logging.ERROR, logger='phylohist'), pytest.raises(LoadError, match=reason):
    Tree({'taxon': 'rhenopyrgus'}, {**metadata, 'position': 0, 'file_unused': ()})
  assert len(_errors(caplog)) == 1


def test_a_missing_record_ends_the_load_whatever_tolerate_says(monkeypatch, caplog):
  # The checks before the stop have reported; the stop itself is the reason
  # raised, not the count, and `tolerate` cannot see past it.
  import importlib

  from phylohist.loader import LoadError, load

  loading = importlib.import_module('phylohist.loader.load')

  def broken(drafts=False, **_):
    logging.getLogger('phylohist.loader.taxa').error('a check fired')
    data = {k: {} for k in ('authors', 'publications', 'sources', 'sections', 'trees')}
    data['taxa'] = {'testum': {'name': 'Testum', 'authority': {'source': '1899_nobody'}}}
    return data

  monkeypatch.setattr(loading, 'load_files', broken)
  with (
    caplog.at_level(logging.ERROR, logger='phylohist'),
    pytest.raises(LoadError, match='authority source "1899_nobody" has no source record'),
  ):
    load(tolerate=True)
  assert _errors(caplog) == [
    'a check fired',
    'Authority source "1899_nobody" not recognized at taxa.yaml testum',
  ]


# -- derivative records ------------------------------------------------------
#
# A record derives from another by one of `derivatives.KINDS`; the loader
# builds it from its target by the row's flags, after the target, wherever
# the file puts the two.

SOURCE = {'source': '1758_linnaeus'}


def _taxa(records):
  """`_load_taxa` over synthetic records, returning the errors it logged."""
  import importlib

  loading = importlib.import_module('phylohist.loader.load')
  loading._load_taxa({'taxa': records})


def test_a_chain_loads_in_any_file_order(caplog):
  # A spelling of a rank variant of a base, the base listed last: each is
  # built after its target, and borrows through the chain.
  from phylohist.loader.taxa import Taxon

  with caplog.at_level(logging.ERROR, logger='phylohist'):
    _taxa(
      {
        'testiidae': {'name': 'Testiidae', 'altSpellingOf': 'testidae-order'},
        'testidae-order': {'rank': 'Order', 'altRankOf': 'testidae'},
        'testidae': {'name': 'Testidae', 'rank': 'Family', 'authority': SOURCE},
      }
    )
  assert _errors(caplog) == []
  assert list(Taxon._taxa)[-3:] == ['testidae', 'testidae-order', 'testiidae']
  base, variant, spelling = (Taxon.get(k) for k in ('testidae', 'testidae-order', 'testiidae'))
  assert (variant.name, variant.rank, variant.derivative_kind.field) == (
    'Testidae',
    'Order',
    'altRankOf',
  )
  assert (spelling.name, spelling.rank) == ('Testiidae', 'Order')
  assert spelling.authority is variant.authority is base.authority
  assert spelling.derivative_of is variant and variant.derivative_of is base


@pytest.mark.parametrize(
  'records, message',
  [
    (
      {'loopa': {'name': 'Loopa', 'altSpellingOf': 'loopa'}},
      'Taxon loopa alt spelling of loopa closes a loop: loopa -> loopa',
    ),
    (
      {
        'loopa': {'name': 'Loopa', 'altSpellingOf': 'loopb'},
        'loopb': {'name': 'Loopb', 'altSpellingOf': 'loopa'},
      },
      'Taxon loopb alt spelling of loopa closes a loop: loopa -> loopb -> loopa',
    ),
  ],
)
def test_a_loop_of_derivatives_ends_the_load(records, message, caplog):
  from phylohist.loader import LoadError

  with (
    caplog.at_level(logging.ERROR, logger='phylohist'),
    pytest.raises(LoadError, match='is in a loop of derivative records'),
  ):
    _taxa(records)
  assert _errors(caplog) == [message]


def test_an_unknown_target_at_the_end_of_a_chain_is_named(caplog):
  from phylohist.loader import LoadError

  with (
    caplog.at_level(logging.ERROR, logger='phylohist'),
    pytest.raises(LoadError, match='alt rank of an unknown record'),
  ):
    _taxa(
      {
        'testiidae': {'name': 'Testiidae', 'altSpellingOf': 'testidae-order'},
        'testidae-order': {'rank': 'Order', 'altRankOf': 'nowhere'},
      }
    )
  assert _errors(caplog) == ['Taxon testidae-order alt rank of unknown nowhere']


@pytest.mark.parametrize('field', ['altSpellingOf', 'altGenderOf', 'latinSpellingOf'])
def test_a_spelling_borrows_rank_and_authority_but_not_the_qualifiers(field, caplog):
  # `homonym`, `originalParent` and `needsQualification` tell identically
  # spelled records apart, so each spelling carries its own: the target's
  # `originalParent` is not copied, and the key is checked without it.
  from phylohist.claims import names_index
  from phylohist.loader.taxa import Taxon

  target = 'testa_linnaeus_1758_parentum'
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    Taxon.add(
      {
        'name': 'testa',
        'rank': 'species',
        'originalParent': 'parentum',
        'lang': 'DE',
        'authority': SOURCE,
      },
      target,
    )
    Taxon.add({'name': 'testum', field: target}, 'testum_linnaeus_1758')
  assert _errors(caplog) == []
  taxon = Taxon.get('testum_linnaeus_1758')
  assert (taxon.rank, taxon.derivative_kind.field) == ('species', field)
  assert taxon.authority is Taxon.get(target).authority
  assert 'originalParent' not in taxon._data
  row = names_index()['testum_linnaeus_1758']
  assert (row['kind'], row['of'], row['rank']) == (field, target, 'species')
  assert 'originalParent' not in row


def test_a_vernacular_record_carries_lang(caplog):
  # A vulgar spelling says its language, and so does the vernacular
  # original a Latin spelling points at; the loader reports either missing.
  from phylohist.loader.taxa import Taxon

  with caplog.at_level(logging.ERROR, logger='phylohist'):
    Taxon.add({'name': 'Testen', 'vulgarSpellingOf': 'cyathocystidae'}, 'testen')
    Taxon.add({'name': 'Tester', 'lang': 'DE', 'vulgarSpellingOf': 'cyathocystidae'}, 'tester')
    Taxon.add({'name': 'Testeen', 'rank': None, 'authority': SOURCE}, 'testeen')
    Taxon.add({'name': 'Testidae', 'latinSpellingOf': 'testeen'}, 'testidae')
    Taxon.add({'name': 'Testoen', 'rank': None, 'lang': 'DE', 'authority': SOURCE}, 'testoen')
    Taxon.add({'name': 'Testoidae', 'latinSpellingOf': 'testoen'}, 'testoidae')
  assert _errors(caplog) == [
    'Taxon testen vulgar spelling of cyathocystidae has no `lang`',
    'Taxon testidae Latin spelling of testeen, whose record has no `lang`',
  ]
  assert Taxon.get('testoidae').rank == 'Unranked'


def test_the_schema_knows_every_derivative_kind():
  # Each kind is a `taxonRecord` property and an `oneOf` branch: a record
  # with a name (a rank for a rank variant, a language for a vulgar form)
  # validates, and the field alone does not.
  from phylohist.derivatives import KINDS
  from phylohist.loader import io
  from tests import support

  properties = io.load_yaml(io.SCHEMA_PATH)['$defs']['taxonRecord']['properties']
  check = support.schema()['taxa'].check
  for kind in KINDS:
    assert kind.field in properties
    record = {'name': 'Testa', kind.field: 'testb'}
    if not kind.borrows_rank:
      record['rank'] = 'Family'
    if kind.lang == 'record':
      record['lang'] = 'FR'
    assert check({'testa': record}), kind.field
    assert not check({'testa': {kind.field: 'testb'}}), kind.field
  assert not check({'testen': {'name': 'Testen', 'vulgarSpellingOf': 'testa'}})


def test_the_ranks_are_the_schemas():
  # `phylohist/ranks.py` restates the schema's `rank` enum for both sides
  # of the package; the two must not drift apart.
  from phylohist import ranks
  from phylohist.loader import io

  assert ranks.RANKS == tuple(io.load_yaml(io.SCHEMA_PATH)['$defs']['rank']['enum'])
  assert set(ranks.SPECIES_GROUP + ranks.GENUS_GROUP) <= set(ranks.RANKS)
  assert ranks.rank_order('variety') > ranks.rank_order('species') > ranks.rank_order('Genus')
  assert ranks.rank_order(None) == ranks.rank_order('Stage') == len(ranks.RANKS)
