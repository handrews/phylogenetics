"""One shape for an attribution (roadmap A4): every printed credit and
every cited work sits in an `authority` block, and a block carries the
locators in the work it names. The schema, the loader, the extractor and
the script that put the data into this shape.

Synthetic records and trees are built on the loaded test corpus (the
registries are restored before each test); the script is exercised over
small texts and over the corpus files, which it must leave as they are.
"""

import logging

import pytest
import yaml

from phylohist.claims import extract, names_index
from phylohist.loader import io
from phylohist.loader.load import _report_material
from phylohist.loader.taxa import Authority, Section, Taxon, Tree
from tests import support

SOURCE = '1758_linnaeus'
LATER = '1766_linnaeus'
PRINTED = {'auth': ['linnaeus'], 'year': 1758}
CREDIT = {'auth': ['linnaeus'], 'year': 1788, 'in': ['gmelin']}


# -- schema -------------------------------------------------------------------


def _tree_valid(node):
  return support.schema()[io.TREE_DEF].check({'taxonomies': [node]})


def _taxon_valid(record):
  return support.schema()['taxa'].check({'testum': record})


def _section_valid(record):
  return support.schema()['sections'].check({'integra': record})


@pytest.mark.parametrize('field', [{'auth': ['linnaeus']}, {'year': 1758}, {'in': ['gmelin']}])
def test_schema_takes_a_printed_credit_only_inside_authority(field):
  block = {'auth': ['linnaeus'], **field}
  assert not _tree_valid({'taxon': 'vermes', **field})
  assert _tree_valid({'taxon': 'vermes', 'authority': block})
  assert not _taxon_valid({'name': 'Testum', **field})
  assert _taxon_valid({'name': 'Testum', 'authority': block})
  assert not _section_valid({'name': 'Integra', **field})
  assert _section_valid({'name': 'Integra', 'authority': block})


@pytest.mark.parametrize(
  'block',
  [CREDIT, PRINTED, {'year': 1850}, {'auth': []}, {'auth': [], 'year': 1850}],
)
def test_schema_accepts_the_printed_forms(block):
  assert _tree_valid({'taxon': 'vermes', 'authority': block})
  assert _taxon_valid({'name': 'Testum', 'authority': block})


@pytest.mark.parametrize(
  'block',
  [
    {'in': ['gmelin'], 'year': 1788},  # `in` qualifies printed authors
    {'auth': [], 'in': ['gmelin']},  # none printed
    {'auctt': True, 'auth': ['linnaeus']},  # "of authors" names no author
    {'auctt': True, 'year': 1758},
    {'source': SOURCE, 'auth': ['linnaeus']},  # a work or a credit, not both
    {'source': SOURCE, 'year': 1758},
    {'auth': ['linnaeus'], 'attributedTo': ['gmelin']},  # with a source only
    {'auth': ['linnaeus'], 'ex': {'source': SOURCE}},
    {'notes': 'nothing named'},
  ],
)
def test_schema_rejects_a_block_that_mixes_or_names_nothing(block):
  assert not _tree_valid({'taxon': 'vermes', 'authority': block})
  assert not _taxon_valid({'name': 'Testum', 'authority': block})


def test_schema_locators_alone_mean_as_the_record():
  # On a node and on a derivative or section record, a block of locators
  # alone is the record's authority at those locators; a record with a
  # name of its own names a work.
  figures = [{'plate': 1, 'figures': [2]}]
  assert _tree_valid({'taxon': 'vermes', 'authority': {'pages': 5}})
  assert _tree_valid({'taxon': 'vermes', 'authority': {'illustrations': figures}})
  spelling = {
    'name': 'testa',
    'altSpellingOf': 'testa',
    'rank': 'species',
    'authority': {'pages': 799},
  }
  assert _taxon_valid(spelling)
  unranked = {key: value for key, value in spelling.items() if key != 'rank'}
  assert not _taxon_valid(unranked)  # a page spells the rank
  assert _section_valid({'name': 'Integra', 'authority': {'pages': 645}})
  assert not _taxon_valid({'name': 'Testum', 'authority': {'pages': 5}})
  assert not _taxon_valid({'name': 'Testum', 'rank': 'genus', 'authority': {'pages': 5}})


def test_schema_puts_a_records_locators_inside_the_block():
  block = {'source': SOURCE, 'pages': 661, 'illustrations': [{'plate': 1}]}
  assert _taxon_valid({'name': 'Testum', 'rank': 'genus', 'authority': block})
  assert _section_valid({'name': 'Integra', 'authority': block})
  for field in ('pages', 'illustrations'):
    record = {
      'name': 'Testum',
      'rank': 'genus',
      'authority': {'source': SOURCE},
      field: block[field],
    }
    assert not _taxon_valid(record)
    assert not _section_valid(
      {'name': 'Integra', 'authority': {'source': SOURCE}, field: block[field]}
    )
  # A record's page spells its rank.
  assert not _taxon_valid({'name': 'Testum', 'authority': {'source': SOURCE, 'pages': 661}})


@pytest.mark.parametrize('work', [PRINTED, {'year': 1900}, {'pages': 12}, {'auth': []}])
def test_schema_cited_works_name_a_work(work):
  # `ex`, `emendedBy`, `restrictedBy`, `by` and `fixedBy` cite a work: a
  # source record or auctt, never a printed credit or locators alone.
  assert not _taxon_valid({'name': 'Testum', 'authority': {'source': SOURCE, 'ex': work}})
  assert not _tree_valid({'taxon': 'vermes', 'emendedBy': [work]})
  assert not _tree_valid({'taxon': 'vermes', 'restrictedBy': [work]})
  assert not _tree_valid({'taxon': 'vermes', 'recombined': {'by': work}})
  assert not _tree_valid({'taxon': 'vermes', 'translated': {'taxon': 'vermes', 'by': work}})
  type_node = {'taxon': 'testa', 'fixation': 'subsequentDesignation', 'fixedBy': work}
  assert not _tree_valid({'taxon': 'vermes', 'type': type_node})
  for cited in ({'source': SOURCE}, {'auctt': True}):
    assert _tree_valid({'taxon': 'vermes', 'emendedBy': [cited]})
    assert _tree_valid({'taxon': 'vermes', 'recombined': {'by': cited}})
    assert _tree_valid({'taxon': 'vermes', 'type': {**type_node, 'fixedBy': cited}})
  assert _taxon_valid({'name': 'Testum', 'authority': {'source': SOURCE, 'ex': {'source': LATER}}})


def test_schema_corrections_follow_the_blocks_shape():
  node = {'taxon': 'isorophida', 'authority': {'auth': ['bell.b.m'], 'year': 1974}}
  nested = {'authority': {'auth': None, 'year': None, 'source': '1976_bell.b.m'}}
  assert _tree_valid({**node, 'editorial': {'corrections': nested, 'basis': 'b'}})
  for flat in ({'auth': None}, {'year': 1976}, {'in': None}, {'auth': None, **nested}):
    assert not _tree_valid({**node, 'editorial': {'corrections': flat, 'basis': 'b'}})
  assert not _tree_valid(
    {**node, 'editorial': {'corrections': {'authority': {'year': 'x'}}, 'basis': 'b'}}
  )


# -- loader -------------------------------------------------------------------


def _errors(caplog):
  return [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]


def _warnings(caplog):
  return [r.getMessage() for r in caplog.records if r.levelno == logging.WARNING]


def test_a_cited_entrys_node_level_locators_end_in_an_error(caplog):
  figures = [{'plate': 1}]
  entries = [
    {'taxon': 'cyathocystidae', 'pages': 5},
    {'taxon': 'cyathocystidae', 'illustrations': figures},
  ]
  trees = {
    '_synthetic_source': {
      'taxonomies': [
        {'taxon': 'cyathocystis', 'synonyms': entries},
        {'taxon': 'cyathocystis', 'authority': {'pages': 5}},
      ]
    }
  }
  with caplog.at_level(logging.WARNING, logger='phylohist'):
    _report_material({'trees': trees})
  errors = _errors(caplog)
  tail = "; the cited work's locators go inside `authority`"
  assert f'_synthetic_source at 0/synonyms/0: cited entry carries `pages`{tail}' in errors
  assert f'_synthetic_source at 0/synonyms/1: cited entry carries `illustrations`{tail}' in errors
  assert (
    "_synthetic_source at 1: primary node's `authority` carries locators alone; "
    'its own page and figures sit on it'
  ) in errors


def test_check_draft_exits_one_on_a_cited_entrys_node_level_illustrations(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'taxonomies:\n'
    '- taxon: cyathocystis\n'
    '  synonyms:\n'
    '  - taxon: cyathocystidae\n'
    '    illustrations:\n'
    '    - plate: 1\n',
  )
  result = support.run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'cited entry carries `illustrations`' in result.stdout


def test_a_year_alone_and_an_empty_auth_name_no_author():
  year_only = Authority({'year': 1850})
  assert str(year_only) == '1850' and year_only.taxon_suffix == 'unknown_1850'
  assert year_only.authors is None and year_only.source is None
  unknown = Authority({'auth': []})
  assert str(unknown) == '' and unknown.taxon_suffix == 'unknown'
  Taxon.add({'name': 'Testum', 'rank': 'genus', 'authority': {'year': 1850}}, 'testum')
  assert str(Taxon.get('testum').authority) == '1850'


def test_in_credits_the_authors_within_the_works_authors():
  authority = Authority(CREDIT)
  assert str(authority) == 'Linnaeus in Gmelin 1788'
  assert [a.key for a in authority.authors] == ['linnaeus']
  assert [a.key for a in authority.source_authors] == ['gmelin']
  assert authority.taxon_suffix == 'linnaeus_1788'


def test_a_derivative_with_locators_alone_borrows_its_targets_authority():
  Taxon.add(
    {'name': 'Testum', 'rank': 'genus', 'authority': {'source': SOURCE, 'pages': 10}}, 'testum'
  )
  Taxon.add({'name': 'Testvm', 'altSpellingOf': 'testum', 'authority': {'pages': 799}}, 'testvm')
  spelling = Taxon.get('testvm')
  assert spelling.authority is Taxon.get('testum').authority
  assert (spelling.pages, spelling.illustrations) == (799, None)
  assert Taxon.get('testum').pages == 10
  # A derivative that names a credit of its own keeps it.
  Taxon.add({'name': 'Testvn', 'altSpellingOf': 'testum', 'authority': PRINTED}, 'testvn')
  assert str(Taxon.get('testvn').authority) == 'Linnaeus 1758'


def test_a_section_with_locators_alone_has_no_authority():
  Section.add({'name': 'Testa', 'authority': {'pages': 645}}, 'testa')
  section = Section.get('testa')
  assert section.authority is None and section.pages == 645
  Section.add({'name': 'Testae', 'authority': {'source': SOURCE, 'pages': 646}}, 'testae')
  assert Section.get('testae').authority.source.key == SOURCE
  assert Section.get('testae').pages == 646


def test_a_capitalised_author_in_a_nodes_block_warns_when_its_key_is_registered(caplog):
  node = {
    'taxon': 'rhenopyrgus',
    'authority': {'auth': ['linnaeus'], 'in': ['Gmelin'], 'year': 1788},
  }
  with caplog.at_level(logging.WARNING, logger='phylohist'):
    Tree(node, {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 940})
  assert [w for w in _warnings(caplog) if 'Unregistered author "Gmelin"' in w and '"gmelin"' in w]


def test_a_capitalised_author_in_a_records_credit_warns_at_the_record(caplog):
  # The warning names the record the credit is on; a bare block has none.
  credit = {'auth': ['Linnaeus'], 'year': 1758}
  with caplog.at_level(logging.WARNING, logger='phylohist'):
    Taxon.add({'name': 'Testum', 'rank': 'genus', 'authority': credit}, 'testum')
    Section.add({'name': 'Testa', 'authority': credit}, 'testa')
    Authority(credit)
  assert _warnings(caplog) == [
    'Unregistered author "Linnaeus" at taxa.yaml testum matches registered key "linnaeus"',
    'Unregistered author "Linnaeus" at sections.yaml testa matches registered key "linnaeus"',
    'Unregistered author "Linnaeus" matches registered key "linnaeus"',
  ]


def test_qualified_keys_add_the_sources_disambiguator():
  keys = Authority({'source': '1760a_linnaeus'}).qualified_keys('testa')
  assert keys == {'testa_linnaeus_1760', 'testa_linnaeus_1760a'}
  assert Authority(PRINTED).qualified_keys('testa') == {'testa_linnaeus_1758'}


# -- extractor ----------------------------------------------------------------


def _usage(root_data, subject, position=941):
  root = Tree(root_data, {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': position})
  claims = extract({'1961_dehm': [root]})['1961_dehm']
  [claim] = [c for c in claims if c['kind'] == 'usage' and c['subject'] == subject]
  return claim


def test_a_cited_entry_prints_its_credit_from_the_block():
  entry = {
    'taxon': 'rhenopyrgidae',
    'citedAs': 'Rhenopyrgidae Linnaeus in Gmelin, 1788',
    'authority': {**CREDIT, 'pages': 12},
  }
  claim = _usage({'taxon': 'rhenopyrgus', 'synonyms': [entry]}, 'rhenopyrgidae')
  assert claim['printed'] == {'citedAs': entry['citedAs'], **CREDIT}
  assert claim['citedPages'] == 12
  for absent in ('citesSource', 'citesAuctt', 'printedAttribution', 'pages'):
    assert absent not in claim


def test_locators_alone_are_the_records_authority_at_those_locators():
  figures = [{'plate': 1, 'figures': [2]}]
  entry = {'taxon': 'rhenopyrgidae', 'authority': {'pages': 12, 'illustrations': figures}}
  claim = _usage({'taxon': 'rhenopyrgus', 'synonyms': [entry]}, 'rhenopyrgidae')
  assert claim['printedAttribution'] == 'as-record'
  assert claim['citedPages'] == 12 and claim['citedIllustrations'] == figures
  assert 'printed' not in claim and 'pages' not in claim and 'citesSource' not in claim


def test_the_nested_correction_names_the_printed_fields_in_error():
  child = {
    'taxon': 'rhenopyrgidae',
    'authority': {'auth': ['bell.b.m'], 'year': 1974},
    'citedAs': 'Bell, 1974',
    'editorial': {
      'corrections': {'authority': {'auth': None, 'year': None, 'source': '1976_bell.b.m'}},
      'basis': 'cited before publication',
    },
  }
  claim = _usage({'taxon': 'rhenopyrgus', 'children': [child]}, 'rhenopyrgidae')
  assert claim['printedErrors'] == ['auth', 'year']
  assert claim['corrected'] == {
    'printed': {'citedAs': 'Bell, 1974'},
    'citesSource': '1976_bell.b.m',
  }


def test_a_patch_over_the_source_is_an_authority_error():
  entry = {
    'taxon': 'rhenopyrgidae',
    'authority': {'source': SOURCE, 'pages': 5},
    'editorial': {'corrections': {'authority': {'source': LATER}}, 'basis': 'the later part'},
  }
  claim = _usage({'taxon': 'rhenopyrgus', 'synonyms': [entry]}, 'rhenopyrgidae')
  assert claim['printedErrors'] == ['authority']
  assert claim['corrected'] == {'citesSource': LATER}
  # So is a block put in place of `authority: null`.
  entry['authority'] = None
  claim = _usage({'taxon': 'rhenopyrgus', 'synonyms': [entry]}, 'rhenopyrgidae', 942)
  assert claim['printedErrors'] == ['authority']


def test_a_patch_that_adds_a_block_corrects_nothing_printed():
  entry = {
    'taxon': 'rhenopyrgidae',
    'citedAs': 'Rhenopyrgidae',
    'editorial': {'corrections': {'authority': {'source': LATER}}, 'basis': 'the work meant'},
  }
  claim = _usage({'taxon': 'rhenopyrgus', 'synonyms': [entry]}, 'rhenopyrgidae')
  assert 'printedErrors' not in claim and 'corrected' not in claim
  assert claim['printed'] == {'citedAs': 'Rhenopyrgidae'} and 'citesSource' not in claim


def test_names_index_rows_for_an_unknown_author_and_a_year_alone():
  Taxon.add({'name': 'Testum', 'rank': 'genus', 'authority': {'year': 1850}}, 'testum')
  rows = names_index()
  assert 'authority' not in rows['hamptonii_unknown']
  assert rows['testum']['authority'] == {'display': '1850'}


# -- the migration script -----------------------------------------------------


TREE_BEFORE = """\
taxonomies:
- taxon: isorophida
  auth: [bell.b.m]
  year: 1974
  citedAs: Bell, 1974
  editorial:
    corrections:
      auth: null
      year: null
      authority:
        source: 1976_bell.b.m
    basis: cited before publication
  synonyms:
  - taxon: agelacrinites
    auth: [barrande]  # as printed
    year: 1887
    pages: [55, 83]
    citedAs: |
      Systeme Silurien
      du centre
  # a reference with no attribution
  - openTaxon: pyrgocystis-sp_x_1999
    pages: 356
  children:
  - taxon: carneyella
    authority: {source: 1758_linnaeus}
    pages: 3
"""

TREE_AFTER = """\
taxonomies:
- taxon: isorophida
  authority:
    auth: [bell.b.m]
    year: 1974
  citedAs: Bell, 1974
  editorial:
    corrections:
      authority:
        auth: null
        year: null
        source: 1976_bell.b.m
    basis: cited before publication
  synonyms:
  - taxon: agelacrinites
    authority:
      auth: [barrande]  # as printed
      year: 1887
      pages: [55, 83]
    citedAs: |
      Systeme Silurien
      du centre
  # a reference with no attribution
  - openTaxon: pyrgocystis-sp_x_1999
    authority:
      pages: 356
  children:
  - taxon: carneyella
    authority: {source: 1758_linnaeus}
    pages: 3
"""

RECORDS_BEFORE = """\
testum_smith_1900:
  name: Testum
  auth: [smith]
  in: [jones]
  year: 1900
# the type
testa_linnaeus_1758:
  name: testa
  rank: species
  pages: 661
  year: 1758
  authority:
    source: 1758_linnaeus
  citedAs: Testa.
testvm:
  altSpellingOf: testum_smith_1900
  pages: 799
hamptonii_unknown:
  name: hamptonii
  auth: []
"""

RECORDS_AFTER = """\
testum_smith_1900:
  name: Testum
  authority:
    auth: [smith]
    year: 1900
    in: [jones]
# the type
testa_linnaeus_1758:
  name: testa
  rank: species
  authority:
    source: 1758_linnaeus
    pages: 661
  citedAs: Testa.
testvm:
  altSpellingOf: testum_smith_1900
  authority:
    pages: 799
hamptonii_unknown:
  name: hamptonii
  authority:
    auth: []
"""

SOURCES = {'1758_linnaeus': {'pubDate': {'year': 1758}}}


def _script():
  return support.script('migrate_authority')


def test_the_script_moves_each_shape_into_a_block():
  script = _script()
  counts = script.Counts()
  text, changed = script.transform(TREE_BEFORE, 'tree', 't', None, counts)
  assert changed and text == TREE_AFTER
  assert dict(counts) == {
    'blocks created': 3,
    'blocks extended': 1,
    'credits moved': 6,
    'locators moved': 2,
    'years dropped': 0,
    'patches rewritten': 1,
  }
  script.check(TREE_BEFORE, TREE_AFTER, 'tree', 't', None)
  counts = script.Counts()
  text, changed = script.transform(RECORDS_BEFORE, 'records', 'r', SOURCES, counts)
  assert changed and text == RECORDS_AFTER
  assert counts['years dropped'] == 1 and counts['credits moved'] == 4
  script.check(RECORDS_BEFORE, RECORDS_AFTER, 'records', 'r', SOURCES)
  assert script.transform(TREE_AFTER, 'tree', 't', None, script.Counts()) == (TREE_AFTER, False)


@pytest.mark.parametrize(
  ('kind', 'text'),
  [
    ('tree', 'taxonomies:\n- taxon: a\n  auth: [b]\n  authority: {source: c}\n'),
    ('tree', 'taxonomies:\n- taxon: a\n  year: 1900\n  authority: {source: c}\n'),
    ('tree', 'taxonomies:\n- taxon: a\n  year: 1900\n  authority: null\n'),
    (
      'tree',
      'taxonomies:\n- taxon: a\n  synonyms:\n'
      '  - taxon: b\n    pages: 1\n    authority: {pages: 2}\n',
    ),
    ('records', 'a:\n  name: A\n  year: 1900\n  authority: {source: 1758_linnaeus}\n'),
  ],
)
def test_the_script_stops_on_a_conflict(kind, text):
  script = _script()
  with pytest.raises(script.Conflict):
    script.transform(text, kind, 'x', SOURCES, script.Counts())


def test_the_corpus_is_a_fixed_point_of_the_script():
  script = _script()
  sources = io.load_yaml(support.CORPUS / 'sources.yaml')
  for path in sorted(support.CORPUS.glob('*.yaml')) + sorted(
    (support.CORPUS / 'trees').glob('*.yaml')
  ):
    if path.name not in ('taxa.yaml', 'sections.yaml') and path.parent == support.CORPUS:
      continue
    kind = 'records' if path.name in ('taxa.yaml', 'sections.yaml') else 'tree'
    text = path.read_text()
    assert script.transform(text, kind, path.name, sources, script.Counts()) == (text, False)
    assert not script.flat_left(yaml.safe_load(text), kind), path.name
