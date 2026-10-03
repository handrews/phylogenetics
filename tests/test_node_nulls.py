"""`rank: null`, `pages: null` and `children: null` on a tree node: the
schema, the loader check, the claims, the derived `skeleton` coverage, and
the listing, sentence and table the tools say.

Synthetic trees are built on the session's loaded corpus under positions
330 and up (`Tree` keeps class-level registries); the tool tests read a
`ClaimStore` over a copy of `claims/` whose file for `1766_linnaeus` is
replaced by the claims of those trees, since no data uses the nulls yet.
"""

import json
import logging
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from phylohist.claims import DERIVED_KINDS, derived_coverage, extract, manifest
from phylohist.loader import io, material, nomenclature
from phylohist.loader.load import _report_nomenclature
from phylohist.loader.research import Source
from phylohist.loader.taxa import Taxon, Tree
from phylohist.store import CLAIMS_DIR, ClaimStore
from phylohist.words import ABSENCE_WORDS

# The synthetic trees name real records, so every test needs the corpus loaded.
pytestmark = pytest.mark.usefixtures('load_records')

SCRIPTS = Path(__file__).parent.parent / 'scripts'

SOURCE = '1766_linnaeus'
INFERRED = {'inferred': True, 'basis': 'Carried over from the first part, published 1766.'}


# -- schema -------------------------------------------------------------------


def _valid(document):
  return io.build_schema()[io.TREE_DEF].check(document)


RECORD = {'name': 'Vermes', 'authority': {'source': '1758_linnaeus'}, 'rank': 'Class', 'pages': 5}


def _record_valid(record):
  return io.build_schema()['taxa'].check({'x': record})


def test_schema_accepts_a_null_rank_and_a_null_pages_on_a_node():
  assert _valid(
    {
      'taxonomies': [
        {
          'taxon': 'animalia',
          'rank': 'Kingdom',
          'pages': None,
          'editorial': INFERRED,
          'children': [{'taxon': 'vermes', 'rank': None, 'pages': [1, 2]}],
        },
      ]
    }
  )
  assert _valid({'taxonomies': [{'taxon': 'vermes', 'rank': None, 'synonyms': [{'taxon': 'x'}]}]})


@pytest.mark.parametrize('field', ['rank', 'pages'])
def test_schema_rejects_a_null_on_a_taxon_record(field):
  assert _record_valid(RECORD)
  assert not _record_valid({**RECORD, field: None})


def test_schema_rejects_a_null_authority_pages():
  assert _valid({'taxonomies': [{'taxon': 'vermes', 'authority': {'source': '1758_linnaeus'}}]})
  assert not _valid(
    {
      'taxonomies': [
        {'taxon': 'vermes', 'authority': {'source': '1758_linnaeus', 'pages': None}},
      ]
    }
  )


def test_schema_still_checks_a_node_rank_and_pages():
  assert not _valid({'taxonomies': [{'taxon': 'vermes', 'rank': 'Realm'}]})
  assert not _valid({'taxonomies': [{'taxon': 'vermes', 'pages': {'a': 1}}]})
  assert not _valid({'taxonomies': [{'taxon': 'vermes', 'extra': 1}]})


# -- loader check -------------------------------------------------------------


def test_a_null_pages_on_an_inferred_node_is_clean():
  node = {'taxon': 'animalia', 'pages': None, 'editorial': INFERRED}
  assert nomenclature.inferred_pages(node) == []


@pytest.mark.parametrize(
  'node',
  [
    {'taxon': 'animalia', 'pages': None},
    {'taxon': 'animalia', 'pages': None, 'editorial': {'basis': 'x'}},
    {'taxon': 'animalia', 'pages': None, 'editorial': {'inferred': ['fixation'], 'basis': 'x'}},
    {'taxon': 'animalia', 'pages': None, 'editorial': {'inferred': False, 'basis': 'x'}},
  ],
)
def test_a_null_pages_on_a_printed_node_is_an_error(node):
  assert nomenclature.inferred_pages(node) == [
    ('error', '`pages: null` on a node the source prints; only an inferred node has no page'),
  ]


def test_a_node_with_pages_or_none_says_nothing():
  assert nomenclature.inferred_pages({'taxon': 'animalia'}) == []
  assert nomenclature.inferred_pages({'taxon': 'animalia', 'pages': 5}) == []
  assert nomenclature.inferred_pages({'taxon': 'animalia', 'rank': None}) == []


def test_load_reports_the_null_pages_with_the_nodes_path(caplog):
  data = {
    'trees': {
      'src1': {
        'taxonomies': [
          {
            'taxon': 'animalia',
            'pages': None,
            'editorial': INFERRED,
            'children': [{'taxon': 'vermes', 'pages': None}],
          }
        ],
      },
    },
  }
  with caplog.at_level(logging.WARNING, logger='phylohist'):
    _report_nomenclature(data)
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert len(errors) == 1
  assert errors[0].endswith(
    'src1 at 0/children/0: `pages: null` on a node the source prints; '
    'only an inferred node has no page'
  )


def _check_draft(tmp_path, body):
  draft = tmp_path / '1766_linnaeus.yaml'
  draft.write_text('taxonomies:\n' + body)
  return subprocess.run(
    [sys.executable, str(SCRIPTS / 'check_draft.py'), str(draft)],
    capture_output=True,
    text=True,
  )


def test_check_draft_allows_an_inferred_node_with_null_pages(tmp_path):
  result = _check_draft(
    tmp_path,
    '- taxon: animalia\n'
    '  rank: Kingdom\n'
    '  pages: null\n'
    '  editorial:\n'
    '    inferred: true\n'
    '    basis: Carried over from the first part, published 1766.\n'
    '  children:\n'
    '  - taxon: vermes\n'
    '    rank: null\n',
  )
  assert result.returncode == 0, result.stdout + result.stderr


def test_check_draft_reports_a_null_pages_on_a_printed_node(tmp_path):
  result = _check_draft(
    tmp_path,
    '- taxon: animalia\n  children:\n  - taxon: vermes\n    pages: null\n',
  )
  assert result.returncode == 1, result.stdout + result.stderr
  assert (
    'children/0: `pages: null` on a node the source prints; only an inferred node has no page'
    in result.stdout
  )
  assert 'only an auditor sets nulls' not in result.stdout


# -- claims -------------------------------------------------------------------


def _claims(root, position, source=SOURCE):
  tree = Tree(root, {'source_key': source, 'type': 'taxonomy', 'position': position})
  return extract({source: [tree]})[source]


def _at(claims, path, kind='placement'):
  [claim] = [c for c in claims if c['path'] == path and c['kind'] == kind]
  return claim


def test_a_null_rank_is_a_null_rank_as_printed(load_records):
  root = {
    'taxon': 'animalia',
    'rank': 'Kingdom',
    'children': [{'taxon': 'vermes', 'rank': None}, {'taxon': 'echinodermata'}],
  }
  claims = _claims(root, 330)
  vermes = _at(claims, '330/children/0')
  assert 'rankAsPrinted' in vermes and vermes['rankAsPrinted'] is None
  # The record's rank is unchanged, and a node with no `rank` has no key.
  assert vermes['rank'] == 'Class'
  assert 'rankAsPrinted' not in _at(claims, '330/children/1')
  assert 'rankAsPrinted' not in _at(claims, '330', 'usage')


def test_an_inferred_node_with_null_pages_passes_none_down(load_records):
  root = {
    'taxon': 'animalia',
    'rank': 'Kingdom',
    'pages': None,
    'editorial': INFERRED,
    'children': [
      {'taxon': 'vermes', 'pages': 12, 'children': [{'taxon': 'echinodermata'}]},
      {'taxon': 'mollusca'},
    ],
  }
  claims = _claims(root, 331)
  root_claim = _at(claims, '331', 'usage')
  assert 'pages' not in root_claim and 'pagesInherited' not in root_claim
  assert root_claim['inferred'] is True
  vermes = _at(claims, '331/children/0')
  assert vermes['pages'] == 12 and 'pagesInherited' not in vermes
  assert 'inferred' not in vermes
  # A child with its own pages passes them on, as before; one without,
  # under a root that has none, gets none.
  assert _at(claims, '331/children/0/children/0')['pages'] == 12
  assert _at(claims, '331/children/0/children/0')['pagesInherited'] is True
  assert 'pages' not in _at(claims, '331/children/1')
  assert 'pagesInherited' not in _at(claims, '331/children/1')


def test_null_pages_stops_inheritance_at_the_node(load_records):
  root = {
    'taxon': 'animalia',
    'pages': 5,
    'children': [
      {
        'taxon': 'vermes',
        'pages': None,
        'editorial': INFERRED,
        'children': [{'taxon': 'echinodermata'}],
      }
    ],
  }
  claims = _claims(root, 332)
  assert _at(claims, '332', 'usage')['pages'] == 5
  assert 'pages' not in _at(claims, '332/children/0')
  assert _at(claims, '332/children/0')['inferred'] is True
  assert 'pages' not in _at(claims, '332/children/0/children/0')


# -- the tools ----------------------------------------------------------------

TREE = {
  'taxon': 'animalia',
  'rank': 'Kingdom',
  'pages': None,
  'editorial': INFERRED,
  'children': [
    {'taxon': 'vermes', 'rank': None, 'pages': 12},
    {'taxon': 'echinodermata', 'rank': None, 'new': True, 'pages': 13},
    {'taxon': 'mollusca', 'pages': 14},
  ],
}


@pytest.fixture(scope='module')
def synthetic(load_records, tmp_path_factory):
  """A `ClaimStore` over a copy of `claims/` with the claims of `SOURCE`
  replaced by those of `TREE`."""
  directory = tmp_path_factory.mktemp('claims')
  shutil.copytree(CLAIMS_DIR, directory, dirs_exist_ok=True)
  claims = _claims(TREE, 340)
  (directory / f'{SOURCE}.jsonl').write_text(''.join(json.dumps(c) + '\n' for c in claims))
  return ClaimStore(directory)


def test_contents_prints_an_unranked_node_as_its_name_alone(synthetic):
  [block] = synthetic.contents(SOURCE, 'animalia')
  lines = block['rendered'].splitlines()
  assert lines[1:] == [
    '  Kingdom Animalia',
    '    Vermes',
    '    Echinodermata nov.',
    '    Phylum Mollusca',
  ]
  vermes, echinodermata, mollusca = block['nodes'][1:]
  assert vermes['unranked'] is True and 'rankWord' not in vermes
  assert echinodermata['unranked'] is True and 'rankWord' not in echinodermata
  assert 'unranked' not in mollusca and mollusca['rankWord'] == 'Phylum'
  assert 'pages' not in block['nodes'][0]


def test_the_placement_sentence_says_unranked(synthetic):
  placement = synthetic.at_path[SOURCE]['340/children/0']
  [claim] = [c for c in placement if c['kind'] == 'placement']
  assert synthetic.words.claim_words(claim) == 'places it under Animalia, unranked'
  [ranked] = [c for c in synthetic.at_path[SOURCE]['340/children/2'] if c['kind'] == 'placement']
  assert synthetic.words.claim_words(ranked) == 'places it under Animalia'
  sentences = [e['sentence'] for e in synthetic.statements('vermes', source=SOURCE)['entries']]
  assert 'places it under Animalia, unranked' in sentences


def test_the_placements_table_keeps_the_records_rank(synthetic):
  block = synthetic.placements(['vermes'])
  [row] = [r for r in block['rows'] if r['record'] == 'vermes']
  assert row['cells'][1] == [{'value': 'Class'}]
  [cell] = [c for cells in row['cells'][2:] for c in cells if SOURCE in c['claim']]
  assert cell['value'] == 'Animalia' and cell['rank'] == 'Class'


def test_an_unranked_root_prints_its_name_alone(load_records, tmp_path):
  # A root has no placement claim: its usage carries the null printed rank.
  root = {'taxon': 'vermes', 'rank': None, 'pages': 12, 'children': [{'taxon': 'mollusca'}]}
  claims = _claims(root, 341)
  assert _at(claims, '341', kind='usage')['rankAsPrinted'] is None
  directory = tmp_path / 'claims'
  shutil.copytree(CLAIMS_DIR, directory)
  (directory / f'{SOURCE}.jsonl').write_text(''.join(json.dumps(c) + '\n' for c in claims))
  [block] = ClaimStore(directory).contents(SOURCE, 'vermes')
  assert block['rendered'].splitlines()[1] == '  Vermes'
  assert block['nodes'][0]['unranked'] is True


# -- `children: null` and the derived `skeleton` coverage -----------------------

# The records of the examples: an order (Lithophyta), a class, a family, a
# genus with two species, a `section`, an order that is only a placeholder.
ORDER = 'lithophyta'
CLASS = 'eocrinoidea'
FAMILY = 'edrioasteridae'
GENUS = 'edrioaster'
GENUS_2 = 'cyclaster'
SPECIES = 'bigsbyi_billings_1857'
SPECIES_2 = 'priscus_miller.s.a_gurley_1894'
SECTION = 'anomales'
PLACEHOLDER = 'edrioasteroidea-order-uncertain_bassler_1935'
PHYLUM = 'echinodermata'
DEHM = '1961_dehm'
_BASE = {'source_key': DEHM, 'type': 'taxonomy'}


def test_schema_accepts_a_null_children():
  assert _valid({'taxonomies': [{'taxon': ORDER, 'rank': 'Order', 'pages': 790, 'children': None}]})
  assert _valid(
    {'taxonomies': [{'taxon': PHYLUM, 'children': [{'taxon': ORDER, 'children': None}]}]}
  )
  # A cladogram node shares the schema; the loader refuses the null there.
  assert _valid(
    {'phylogenies': [{'treeType': 'cladogram', 'tree': {'taxon': ORDER, 'children': None}}]}
  )
  assert not _valid({'taxonomies': [{'taxon': ORDER, 'children': 'none'}]})
  assert not _valid({'taxonomies': [{'taxon': ORDER, 'children': {}}]})


def test_schema_has_no_unused_children():
  assert not _valid({'unused': ['children'], 'taxonomies': [{'taxon': ORDER}]})


def _errors(caplog):
  return [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]


def _load(root, position, caplog, tree_type='taxonomy'):
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    return Tree(root, {**_BASE, 'type': tree_type, 'position': position})


def test_children_null_on_an_order_is_clean(caplog):
  tree = _load({'taxon': PHYLUM, 'children': [{'taxon': ORDER, 'children': None}]}, 1100, caplog)
  assert _errors(caplog) == []
  assert [n.taxon.key for n in tree.walk()] == [PHYLUM, ORDER]


@pytest.mark.parametrize(
  'field, taxon',
  [('taxon', t) for t in (SECTION, PHYLUM, CLASS, FAMILY)] + [('openTaxon', PLACEHOLDER)],
)
def test_children_null_is_allowed_above_genus_rank(caplog, field, taxon):
  _load({field: taxon, 'children': None}, 1101, caplog)
  assert _errors(caplog) == []


def test_children_null_on_a_genus_is_an_error(caplog):
  _load({'taxon': FAMILY, 'children': [{'taxon': GENUS_2, 'children': None}]}, 1102, caplog)
  [error] = _errors(caplog)
  assert error.endswith(
    'carries `children: null` but is a genus or species-level name; '
    'only a higher taxon says the tree stops'
  )
  assert GENUS_2 in error


def test_children_null_on_a_subgenus_or_species_is_an_error(caplog):
  for position, taxon in ((1103, 'agelacrinus-subgenus_carneyella'), (1104, SPECIES)):
    caplog.clear()
    _load({'taxon': taxon, 'children': None}, position, caplog)
    [error] = _errors(caplog)
    assert 'carries `children: null` but is a genus or species-level name' in error


def test_children_null_is_compared_lower_cased(monkeypatch, caplog):
  monkeypatch.setattr(Taxon.get(GENUS_2), '_rank', 'Genus')
  _load({'taxon': GENUS_2, 'children': None}, 1105, caplog)
  assert len(_errors(caplog)) == 1


def test_a_genus_with_no_children_says_nothing(caplog):
  _load(
    {'taxon': FAMILY, 'children': [{'taxon': GENUS_2}, {'taxon': GENUS, 'children': []}]},
    1106,
    caplog,
  )
  assert _errors(caplog) == []


def test_children_null_outside_a_taxonomy_is_an_error(caplog):
  root = {'taxon': PHYLUM, 'children': [{'taxon': ORDER, 'children': None}]}
  _load(root, 1107, caplog, tree_type='cladogram')
  [error] = _errors(caplog)
  assert error.endswith('`children: null` outside a taxonomy')
  assert error.startswith('Dehm (1961)[1107]/echinodermata/0/lithophyta')


def test_children_null_on_a_cited_entry_is_an_error():
  assert nomenclature.children_null({'taxon': ORDER, 'children': None}, is_cited=True) == [
    ('error', 'cited entry carries `children: null`'),
  ]
  assert nomenclature.children_null({'taxon': ORDER, 'children': None}, is_cited=False) == []
  assert nomenclature.children_null({'taxon': ORDER, 'children': []}, is_cited=True) == []
  assert nomenclature.children_null({'taxon': ORDER}, is_cited=True) == []


def test_load_reports_a_null_children_on_a_cited_entry_with_the_nodes_path(caplog):
  data = {
    'trees': {
      'src1': {
        'taxonomies': [
          {
            'taxon': PHYLUM,
            'children': [
              {'taxon': ORDER, 'children': None},
              {'taxon': CLASS, 'synonyms': [{'taxon': SECTION, 'children': None}]},
            ],
          }
        ],
      },
    },
  }
  with caplog.at_level(logging.WARNING, logger='phylohist'):
    _report_nomenclature(data)
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert errors == ['src1 at 0/children/1/synonyms/0: cited entry carries `children: null`']


def test_unused_fields_and_null_material_say_nothing_of_children():
  document = {'unused': ['synonyms'], 'taxonomies': [{'taxon': ORDER, 'children': None}]}
  assert material.unused_fields(document) == []
  assert material.null_material({'taxon': ORDER, 'children': None}, is_cited=True) == []


def test_check_draft_rejects_a_null_children(tmp_path):
  result = _check_draft(
    tmp_path, '- taxon: animalia\n  children:\n  - taxon: lithophyta\n    children: null\n'
  )
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'children/0: draft carries `children: null`; only an auditor sets nulls' in result.stdout


def test_check_draft_reports_a_null_children_on_a_cited_entry(tmp_path):
  result = _check_draft(
    tmp_path,
    '- taxon: animalia\n  synonyms:\n  - taxon: lithophyta\n    children: null\n',
  )
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'synonyms/0: cited entry carries `children: null`' in result.stdout


def test_check_draft_allows_an_empty_children_list(tmp_path):
  result = _check_draft(
    tmp_path, '- taxon: animalia\n  children:\n  - taxon: lithophyta\n    children: []\n'
  )
  assert result.returncode == 0, result.stdout + result.stderr


# -- the absence claim --------------------------------------------------------


def test_a_null_children_is_an_absence_claim():
  root = {'taxon': PHYLUM, 'children': [{'taxon': ORDER, 'children': None}]}
  claims = _claims(root, 1110)
  [absence] = [c for c in claims if c['kind'] == 'absence']
  assert absence['absenceOf'] == 'skeleton'
  assert absence['fields'] == ['children']
  assert absence['path'] == '1110/children/0'
  assert absence['subject'] == ORDER
  # The node still has its placement, and the null adds no placement below it.
  assert _at(claims, '1110/children/0')['subject'] == ORDER
  assert len([c for c in claims if c['kind'] == 'placement']) == 1
  assert ABSENCE_WORDS['skeleton'] == 'nothing placed under it'
  # A list, an empty list and an absent `children` are no absence.
  for position, children in ((1111, [{'taxon': GENUS}]), (1112, [])):
    assert not [
      c for c in _claims({'taxon': ORDER, 'children': children}, position) if c['kind'] == 'absence'
    ]
  assert not [c for c in _claims({'taxon': ORDER}, 1113) if c['kind'] == 'absence']


def test_the_skeleton_absence_follows_the_other_absences():
  claims = _claims({'taxon': ORDER, 'synonyms': None, 'type': None, 'children': None}, 1114)
  assert [c['absenceOf'] for c in claims if c['kind'] == 'absence'] == [
    'synonymy',
    'types',
    'skeleton',
  ]


# -- derived `skeleton` coverage ----------------------------------------------


def _skeleton(node, position, file_unused=(), tree_type='taxonomy'):
  root = Tree(node, {**_BASE, 'type': tree_type, 'position': position, 'file_unused': file_unused})
  return derived_coverage({'s': [root]})['s']['skeleton']


def _phylum(*orders):
  return {'taxon': PHYLUM, 'children': list(orders)}


def test_skeleton_coverage_declares_nothing_without_a_null():
  assert _skeleton(_phylum({'taxon': ORDER, 'children': [{'taxon': GENUS}]}), 1120) is None
  assert _skeleton(_phylum({'taxon': ORDER}), 1121) is None
  assert _skeleton(_phylum({'taxon': ORDER, 'children': []}), 1122) is None


def test_skeleton_coverage_all_when_every_node_above_genus_has_a_list_or_a_null():
  tree = {
    'taxon': PHYLUM,
    'children': [
      {'taxon': ORDER, 'children': None},
      {'taxon': CLASS, 'children': [{'taxon': FAMILY, 'children': [{'taxon': GENUS}]}]},
    ],
  }
  assert _skeleton(tree, 1123) == 'all'


def test_skeleton_coverage_partly_when_a_node_above_genus_lacks_children():
  tree = _phylum({'taxon': ORDER, 'children': None}, {'taxon': CLASS})
  assert _skeleton(tree, 1124) == 'partly'
  # A node lower down is counted as well.
  deeper = {'taxon': CLASS, 'children': [{'taxon': ORDER, 'children': None}, {'taxon': FAMILY}]}
  assert _skeleton(_phylum(deeper), 1125) == 'partly'
  assert _skeleton({'taxon': ORDER, 'children': None}, 1126) == 'all'


def test_a_genus_without_children_does_not_count():
  tree = {
    'taxon': PHYLUM,
    'children': [{'taxon': ORDER, 'children': None}, {'taxon': GENUS}, {'taxon': GENUS_2}],
  }
  assert _skeleton(tree, 1127) == 'all'
  tree = {'taxon': ORDER, 'children': [{'taxon': GENUS}, {'taxon': GENUS_2, 'children': []}]}
  assert _skeleton(_phylum(tree, {'taxon': CLASS, 'children': None}), 1128) == 'all'
  tree = {'taxon': ORDER, 'children': [{'taxon': GENUS}, {'taxon': GENUS_2, 'children': []}]}
  assert _skeleton(tree, 1129) is None
  # A species counts for nothing either.
  assert (
    _skeleton(
      {'taxon': ORDER, 'children': [{'taxon': GENUS, 'children': [{'taxon': SPECIES}]}]}, 1130
    )
    is None
  )


def test_a_section_and_an_unranked_node_count(monkeypatch):
  tree = {'taxon': ORDER, 'children': None}
  assert _skeleton(_phylum(tree, {'taxon': SECTION}), 1131) == 'partly'
  assert _skeleton(_phylum(tree, {'taxon': SECTION, 'children': None}), 1132) == 'all'
  monkeypatch.setattr(Taxon.get(SECTION), '_rank', 'Unranked')
  assert _skeleton(_phylum(tree, {'taxon': SECTION}), 1133) == 'partly'
  assert _skeleton(_phylum(tree, {'taxon': SECTION, 'children': None}), 1134) == 'all'


def test_a_placeholder_above_genus_does_not_count():
  tree = _phylum({'taxon': ORDER, 'children': None}, {'openTaxon': PLACEHOLDER})
  assert _skeleton(tree, 1135) == 'all'
  # A placeholder's own null is allowed and writes the null; it is not counted as a node.
  assert _skeleton(_phylum({'openTaxon': PLACEHOLDER, 'children': None}), 1136) is None


def test_skeleton_coverage_is_never_na_and_a_cladogram_contributes_nothing():
  tree = _phylum({'taxon': ORDER, 'children': None})
  assert _skeleton(tree, 1137, file_unused=('children',)) == 'all'
  assert _skeleton(_phylum({'taxon': ORDER}), 1138, file_unused=('children',)) is None
  assert _skeleton(_phylum({'taxon': ORDER}), 1139, file_unused=('synonyms',)) is None
  # The null outside a taxonomy is an error and contributes nothing.
  assert _skeleton(tree, 1140, tree_type='cladogram') is None


def test_skeleton_is_a_derived_kind_with_no_unused_form():
  assert DERIVED_KINDS['skeleton']['unused'] is None
  assert list(DERIVED_KINDS) == [
    'material',
    'occurrences',
    'illustrations',
    'synonymy',
    'types',
    'skeleton',
  ]


def _manifest_entry(values):
  return manifest(extract(values), values)['sources'][DEHM]


def test_manifest_skeleton_declared_beside_a_derived_value_is_inconsistent(monkeypatch):
  coverage = Source.get(DEHM)._data['audit']['coverage']
  monkeypatch.setitem(coverage, 'skeleton', 'all')
  values = {
    DEHM: [
      Tree(
        _phylum({'taxon': ORDER, 'children': None}, {'taxon': CLASS}), {**_BASE, 'position': 1141}
      )
    ]
  }
  entry = _manifest_entry(values)
  assert entry['derivedCoverage']['skeleton'] == 'partly'
  assert entry['coverage']['skeleton'] == 'partly'
  assert (
    'skeleton: declared all but derived from the tree (partly); remove the declaration'
    in entry['inconsistencies']
  )
  assert not [r for r in entry['inconsistencies'] if r.startswith('skeleton: declared all, no')]


def test_manifest_skeleton_keeps_the_claim_count_check_for_a_source_that_derives_nothing(
  monkeypatch,
):
  coverage = Source.get(DEHM)._data['audit']['coverage']
  # Declared `none` beside a tree that places nodes: the claim-count check fires.
  monkeypatch.setitem(coverage, 'skeleton', 'none')
  values = {DEHM: [Tree(_phylum({'taxon': ORDER}), {**_BASE, 'position': 1142})]}
  entry = _manifest_entry(values)
  assert entry['derivedCoverage']['skeleton'] is None
  assert entry['coverage']['skeleton'] == 'none'
  assert any(r.startswith('skeleton: declared none, ') for r in entry['inconsistencies'])
  # Declared `all` with a source that has no tree at all: no claims derived.
  monkeypatch.setitem(coverage, 'skeleton', 'all')
  entry = _manifest_entry({})
  assert 'skeleton: declared all, no claims derived' in entry['inconsistencies']


# -- the tools ----------------------------------------------------------------

# One source with an order that says nothing is placed under it, one that
# lists a class, a family and a genus with species, one that is not entered,
# a section, a genus with no species and a species.
STOPS = {
  'taxon': PHYLUM,
  'children': [
    {'taxon': ORDER, 'children': None},
    {
      'taxon': CLASS,
      'children': [
        {
          'taxon': FAMILY,
          'children': [{'taxon': GENUS, 'children': [{'taxon': SPECIES}, {'taxon': SPECIES_2}]}],
        }
      ],
    },
    {'taxon': 'agelacrinoidea'},
    {'taxon': SECTION, 'children': None},
    {'openTaxon': PLACEHOLDER, 'children': None},
    {'taxon': 'carneyella', 'children': [{'taxon': GENUS_2}]},
  ],
}


@pytest.fixture(scope='module')
def stopped(load_records, tmp_path_factory):
  """A `ClaimStore` over a copy of `claims/` with the claims of 1961 Dehm
  replaced by those of `STOPS`, its `skeleton` coverage `partly`."""
  directory = tmp_path_factory.mktemp('claims_stops')
  shutil.copytree(CLAIMS_DIR, directory, dirs_exist_ok=True)
  claims = _claims(STOPS, 1150, DEHM)
  (directory / f'{DEHM}.jsonl').write_text(''.join(json.dumps(c) + '\n' for c in claims))
  store = ClaimStore(directory)
  store.sources[DEHM]['coverage'] = {**store.sources[DEHM]['coverage'], 'skeleton': 'partly'}
  return store


def _members(block):
  """`[(path, state, basis, count)]` of the members rows of an absence table."""
  return [
    (node['path'], r['state'], r['basis'], r['count'])
    for node in block['content']
    for r in node['rows']
    if r['kind'] == 'members'
  ]


def _table(store, record, source=DEHM):
  return store.statements(record, source=source, kind='absence')


def test_the_members_row_comes_first_and_has_three_states(stopped):
  entered = _table(stopped, CLASS)
  assert [r['kind'] for r in entered['content'][0]['rows']][0] == 'members'
  assert _members(entered) == [('1150/children/1', 'entered', 'claims', 1)]
  [row] = [r for r in entered['rows'] if r['cells'][0][0]['value'] == 'members']
  assert row['cells'][1][0]['value'] == '1 entered'
  assert row['cells'][1][0]['claims'] == ['1961_dehm:1150/children/1/children/0:placement']

  null = _table(stopped, ORDER)
  assert _members(null) == [('1150/children/0', 'none', 'null', None)]
  [row] = [r for r in null['rows'] if r['cells'][0][0]['value'] == 'members']
  assert row['cells'][1][0]['value'] == 'none printed'
  assert row['cells'][1][0]['claims'] == ['1961_dehm:1150/children/0:absence']

  bare = _table(stopped, 'agelacrinoidea')
  assert _members(bare) == [('1150/children/2', 'notEntered', 'coverage', None)]
  [row] = [r for r in bare['rows'] if r['cells'][0][0]['value'] == 'members']
  assert row['cells'][1][0]['value'] == 'not entered' and 'claims' not in row['cells'][1][0]


@pytest.mark.parametrize('declared', ['all', 'na'])
def test_the_members_row_reads_coverage_where_nothing_is_entered(stopped, monkeypatch, declared):
  monkeypatch.setitem(stopped.sources[DEHM]['coverage'], 'skeleton', declared)
  block = _table(stopped, 'agelacrinoidea')
  assert _members(block) == [('1150/children/2', 'none', 'coverage', None)]


def test_the_members_row_counts_the_children_of_a_phylum_and_a_genus(stopped):
  assert _members(_table(stopped, PHYLUM)) == [('1150', 'entered', 'claims', 6)]
  assert _members(_table(stopped, GENUS)) == [
    ('1150/children/1/children/0/children/0', 'entered', 'claims', 2)
  ]
  assert _members(_table(stopped, 'carneyella')) == [('1150/children/5', 'entered', 'claims', 1)]


def test_the_members_row_of_a_section(stopped):
  assert _members(_table(stopped, SECTION)) == [('1150/children/3', 'none', 'null', None)]


def test_the_members_row_of_a_placeholder_appears_only_with_a_statement(stopped):
  assert _members(_table(stopped, PLACEHOLDER)) == [('1150/children/4', 'none', 'null', None)]


def test_no_members_row_for_a_genus_or_species_without_the_absence(stopped):
  for record in (GENUS_2, SPECIES, SPECIES_2):
    block = _table(stopped, record)
    assert 'members' not in [r['kind'] for node in block['content'] for r in node['rows']], record


def test_statements_by_placement_include_the_skeleton_absence(stopped):
  block = stopped.statements(ORDER, source=DEHM, kind='placement')
  assert [e['sentence'] for e in block['entries']][-1] == 'nothing placed under it'
  assert 'absence' in [e['kind'] for e in block['entries']]
  # `absence` selects it, and a node without the null has none.
  block = stopped.statements(ORDER, kind='absence')
  assert [e['sentence'] for e in block['entries']] == ['nothing placed under it']
  block = stopped.statements(CLASS, source=DEHM, kind='placement')
  assert 'nothing placed under it' not in [e['sentence'] for e in block['entries']]
  # Another kind does not select it.
  block = stopped.statements(ORDER, source=DEHM, kind='usage')
  assert 'nothing placed under it' not in [e['sentence'] for e in block['entries']]


def test_contents_prints_no_child_line_under_a_null_children(stopped):
  [block] = stopped.contents(DEHM, ORDER)
  assert block['rendered'].splitlines() == ['Dehm 1961', '  Order Lithophyta']
  assert len(block['nodes']) == 1
  # Beside its siblings the null node is one line, and the next sibling follows it.
  [block] = stopped.contents(DEHM, PHYLUM, depth=1)
  lines = block['rendered'].splitlines()
  index = lines.index('    Order Lithophyta')
  assert lines[index + 1].startswith('    ') and not lines[index + 1].startswith('     ')
