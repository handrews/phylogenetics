"""`rank: null` and `pages: null` on a tree node: the schema, the loader
check, the claims, and the listing and sentence the tools say.

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

from phylohist.claims import extract
from phylohist.loader import io, nomenclature
from phylohist.loader.load import _report_nomenclature
from phylohist.loader.taxa import Tree
from phylohist.store import CLAIMS_DIR, ClaimStore

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


def _claims(root, position):
  tree = Tree(root, {'source_key': SOURCE, 'type': 'taxonomy', 'position': position})
  return extract({SOURCE: [tree]})[SOURCE]


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
