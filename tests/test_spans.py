"""A bracket is a span in a tree's reading order, `bracketStart` through
`bracketEnd`: the span rule in the loader, the errors the loader and the
draft checker report, the claims (a `form: bracket` usage at the start
node, a `via: bracket` placement on every named node in the span), the
schema, and the corpus. A section is a span of siblings, `sectionStart`
through `sectionEnd`, with a record in `data/sections.yaml`: the same
for sections (the last part of the file).

Synthetic trees are built on the session's loaded corpus under positions
2000 and up (`Tree` keeps class-level registries); the closure test reads
a `ClaimStore` over a copy of `claims/` whose file for `1766_linnaeus` is
replaced by the claims of one of them.
"""

import json
import logging
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from phylohist.claims import extract, manifest
from phylohist.closure import Closure
from phylohist.loader import io, material
from phylohist.loader.taxa import Section, Tree
from phylohist.store import CLAIMS_DIR, ClaimStore

# The synthetic trees name real records, so every test needs the corpus loaded.
pytestmark = pytest.mark.usefixtures('load_records')

SCRIPTS = Path(__file__).parent.parent / 'scripts'

SOURCE = '1766_linnaeus'

# The shape of `2003_guensburg_sprinkle`'s Camerata: the span starts on a
# named node, runs over an unmarked unnamed node, and ends on an internal
# unnamed node, whose subtree it takes; a one-node span for Disparida sits
# in the unnamed sister.
SPANS = {
  'children': [
    {'taxon': 'cnemecrinus', 'bracketStart': 'camerata'},
    {
      'children': [
        {'taxon': 'adelphicrinus'},
        {'taxon': 'eknomocrinus'},
        {
          'bracketEnd': 'camerata',
          'children': [
            {'taxon': 'habrotecrinus'},
            {'taxon': 'celtocrinus'},
            {'taxon': 'proexenocrinus'},
          ],
        },
        {
          'children': [
            {
              'taxon': 'ramseyocrinus',
              'bracketStart': 'disparida',
              'bracketEnd': 'disparida',
            },
            {'taxon': 'pariocrinus'},
          ],
        },
      ],
    },
    {'taxon': 'glenocrinus'},
  ],
}

POSITIONS = iter(range(2000, 3000))


def _tree(root, tree_type='cladogram'):
  return Tree(
    root,
    {'source_key': SOURCE, 'type': tree_type, 'position': next(POSITIONS)},
  )


def _nodes(tree):
  return list(tree._primary_walk())


def _keys(node):
  return tuple(taxon.key for taxon in node.brackets)


def _claims(tree):
  return extract({SOURCE: [tree]})[SOURCE]


def _bracket_placements(claims, path):
  return [
    c
    for c in claims
    if c['kind'] == 'placement' and c['path'] == path and c.get('via') == 'bracket'
  ]


def _bracket_usages(claims):
  return [c for c in claims if c['kind'] == 'usage' and c.get('form') == 'bracket']


def _errors(caplog):
  return [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]


# -- the span rule ------------------------------------------------------------


def test_an_end_on_an_internal_node_takes_its_subtree():
  tree = _tree(SPANS)
  by_path = {node.pointer: node for node in _nodes(tree)}
  inside = [
    '/children/0',
    '/children/1',
    '/children/1/children/0',
    '/children/1/children/1',
    '/children/1/children/2',
    '/children/1/children/2/children/0',
    '/children/1/children/2/children/1',
    '/children/1/children/2/children/2',
  ]
  for pointer in inside:
    assert _keys(by_path[pointer]) == ('camerata',), pointer
  # Everything else, the root and the nodes after the end node's last
  # descendant included, lies outside Camerata.
  for pointer in set(by_path) - set(inside):
    assert 'camerata' not in _keys(by_path[pointer]), pointer


def test_an_unmarked_unnamed_node_between_start_and_end_is_in_the_span():
  tree = _tree(SPANS)
  unnamed = next(n for n in _nodes(tree) if n.pointer == '/children/1')
  assert unnamed.taxon is None and _keys(unnamed) == ('camerata',)
  claims = _claims(tree)
  assert _bracket_placements(claims, unnamed_path := f'{unnamed.position}{unnamed.pointer}') == []
  # Its named children are placed under Camerata, though the old field
  # was on none of them.
  for index in (0, 1):
    [placement] = _bracket_placements(claims, f'{unnamed_path}/children/{index}')
    assert placement['parent'] == 'camerata'


def test_both_markers_on_one_node_are_a_one_node_span():
  tree = _tree(SPANS)
  by_path = {node.pointer: node for node in _nodes(tree)}
  assert _keys(by_path['/children/1/children/3/children/0']) == ('disparida',)
  assert _keys(by_path['/children/1/children/3/children/1']) == ()
  assert _keys(by_path['/children/1/children/3']) == ()


def test_a_one_node_span_still_takes_the_nodes_own_subtree():
  tree = _tree(
    {
      'children': [
        {
          'taxon': 'cnemecrinus',
          'bracketStart': 'camerata',
          'bracketEnd': 'camerata',
          'children': [{'taxon': 'adelphicrinus'}],
        },
        {'taxon': 'glenocrinus'},
      ]
    }
  )
  assert {node.taxon.key: _keys(node) for node in _nodes(tree) if node.taxon} == {
    'cnemecrinus': ('camerata',),
    'adelphicrinus': ('camerata',),
    'glenocrinus': (),
  }


def test_spans_of_different_taxa_nest_and_a_node_has_one_placement_for_each():
  tree = _tree(
    {
      'children': [
        {
          'taxon': 'crinoidea',
          'bracketStart': 'protocrinoida',
          'children': [
            {'taxon': 'cnemecrinus', 'bracketStart': 'camerata'},
            {'taxon': 'adelphicrinus', 'bracketEnd': 'camerata'},
            {'taxon': 'glenocrinus', 'bracketEnd': 'protocrinoida'},
          ],
        },
        {'taxon': 'pariocrinus'},
      ]
    }
  )
  keys = {node.taxon.key: _keys(node) for node in _nodes(tree) if node.taxon}
  assert keys == {
    'crinoidea': ('protocrinoida',),
    'cnemecrinus': ('protocrinoida', 'camerata'),
    'adelphicrinus': ('protocrinoida', 'camerata'),
    'glenocrinus': ('protocrinoida',),
    'pariocrinus': (),
  }
  claims = _claims(tree)
  p = tree.position
  parents = [c['parent'] for c in _bracket_placements(claims, f'{p}/children/0/children/0')]
  assert parents == ['protocrinoida', 'camerata']
  assert _bracket_placements(claims, f'{p}/children/1') == []


def test_disjoint_spans_of_one_taxon_are_two_usages_and_the_right_placements():
  tree = _tree(
    {
      'children': [
        {'taxon': 'cnemecrinus', 'bracketStart': 'camerata', 'bracketEnd': 'camerata'},
        {'taxon': 'glenocrinus'},
        {'taxon': 'adelphicrinus', 'bracketStart': 'camerata'},
        {'taxon': 'eknomocrinus', 'bracketEnd': 'camerata'},
      ]
    }
  )
  assert [_keys(n) for n in _nodes(tree)[1:]] == [('camerata',), (), ('camerata',), ('camerata',)]
  claims = _claims(tree)
  usages = _bracket_usages(claims)
  assert [(c['path'], c['bracketEnd']) for c in usages] == [
    (f'{tree.position}/children/0', f'{tree.position}/children/0'),
    (f'{tree.position}/children/2', f'{tree.position}/children/3'),
  ]
  placed = [
    c['path']
    for c in claims
    if c['kind'] == 'placement' and c.get('via') == 'bracket' and c['parent'] == 'camerata'
  ]
  assert placed == [f'{tree.position}/children/{i}' for i in (0, 2, 3)]


def test_a_span_ending_the_tree_lets_the_last_end_close_it():
  tree = _tree(
    {
      'children': [
        {'taxon': 'cnemecrinus', 'bracketStart': 'camerata'},
        {
          'taxon': 'adelphicrinus',
          'bracketEnd': 'camerata',
          'children': [{'taxon': 'eknomocrinus'}],
        },
      ]
    }
  )
  assert [_keys(n) for n in _nodes(tree)[1:]] == [('camerata',)] * 3


def test_brackets_are_valid_in_a_taxonomy_too():
  tree = _tree(
    {
      'taxon': 'crinoidea',
      'children': [{'taxon': 'cnemecrinus', 'bracketStart': 'camerata', 'bracketEnd': 'camerata'}],
    },
    tree_type='taxonomy',
  )
  assert [_keys(n) for n in _nodes(tree)] == [(), ('camerata',)]


# -- the loader's errors ------------------------------------------------------


@pytest.mark.parametrize(
  ('root', 'message'),
  [
    (
      {
        'children': [
          {'taxon': 'cnemecrinus', 'bracketStart': 'camerata'},
          {'taxon': 'adelphicrinus', 'bracketStart': 'camerata', 'bracketEnd': 'camerata'},
        ]
      },
      'opens a bracket for camerata that is already open',
    ),
    (
      {'children': [{'taxon': 'cnemecrinus', 'bracketEnd': 'camerata'}]},
      'closes a bracket for camerata that is not open',
    ),
    (
      {
        'children': [
          {'taxon': 'cnemecrinus', 'bracketStart': 'camerata', 'bracketEnd': 'camerata'},
          {'taxon': 'adelphicrinus', 'bracketEnd': 'camerata'},
        ]
      },
      'closes a bracket for camerata that is not open',
    ),
    (
      {
        'children': [{'taxon': 'cnemecrinus', 'bracketStart': 'camerata'}, {'taxon': 'glenocrinus'}]
      },
      'opens a bracket for camerata that the tree never closes',
    ),
  ],
)
def test_the_loader_reports_a_marker_that_does_not_pair(caplog, root, message):
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    tree = _tree(root)
  [error] = _errors(caplog)
  assert error.endswith(message)
  # The message names the offending node.
  assert f'[{tree.position}]/' in error


def test_the_unclosed_error_is_on_the_start_node(caplog):
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    _tree(
      {
        'children': [
          {'taxon': 'glenocrinus'},
          {'taxon': 'cnemecrinus', 'bracketStart': 'camerata'},
          {'taxon': 'adelphicrinus'},
        ]
      }
    )
  [error] = _errors(caplog)
  assert '/cnemecrinus opens a bracket' in error


def test_a_marker_is_checked_as_the_old_field_was(caplog):
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    _tree({'children': [{'taxon': 'cnemecrinus', 'bracketStart': 'no-such-taxon'}]})
  assert any('Unrecognized tree bracketStart no-such-taxon' in e for e in _errors(caplog))
  caplog.clear()
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    _tree(
      {
        'children': [
          {'taxon': 'cnemecrinus', 'bracketEnd': 'crinoidea-genus-a_guensburg_sprinkle_2003'}
        ]
      }
    )
  assert any('expected to be named' in e for e in _errors(caplog))


# -- the draft checker --------------------------------------------------------


def _document(root):
  return {'phylogenies': [{'treeType': 'cladogram', 'tree': root}]}


@pytest.mark.parametrize(
  ('root', 'message'),
  [
    (
      {
        'children': [
          {'taxon': 'cnemecrinus', 'bracketStart': 'camerata'},
          {'taxon': 'adelphicrinus', 'bracketStart': 'camerata', 'bracketEnd': 'camerata'},
        ]
      },
      '0/children/1: opens a bracket for camerata that is already open',
    ),
    (
      {'children': [{'taxon': 'cnemecrinus', 'bracketEnd': 'camerata'}]},
      '0/children/0: closes a bracket for camerata that is not open',
    ),
    (
      {'children': [{'taxon': 'cnemecrinus', 'bracketStart': 'camerata'}]},
      '0/children/0: opens a bracket for camerata that the tree never closes',
    ),
  ],
)
def test_the_raw_pairing_reports_what_the_loader_does(root, message):
  assert material.bracket_errors(_document(root)) == [('error', message)]


def test_the_raw_pairing_passes_a_paired_tree_and_ignores_related_axes():
  assert material.bracket_errors(_document(SPANS)) == []
  # A marker inside a synonym is no part of the reading order.
  synonym = {'taxon': 'adelphicrinus', 'bracketStart': 'camerata'}
  root = {'children': [{'taxon': 'cnemecrinus', 'synonyms': [synonym]}]}
  assert material.bracket_errors(_document(root)) == []


def test_each_tree_of_a_file_pairs_alone():
  document = {
    'taxonomies': [{'children': [{'taxon': 'cnemecrinus', 'bracketStart': 'camerata'}]}],
    'phylogenies': [
      {'treeType': 'cladogram', 'tree': {'taxon': 'cnemecrinus', 'bracketEnd': 'camerata'}}
    ],
  }
  assert material.bracket_errors(document) == [
    ('error', '0/children/0: opens a bracket for camerata that the tree never closes'),
    ('error', '1: closes a bracket for camerata that is not open'),
  ]


def _check_draft(tmp_path, body):
  draft = tmp_path / '1766_linnaeus.yaml'
  draft.write_text('taxonomies:\n' + body)
  return subprocess.run(
    [sys.executable, str(SCRIPTS / 'check_draft.py'), str(draft)],
    capture_output=True,
    text=True,
  )


def test_check_draft_accepts_a_span_and_checks_the_markers_keys(tmp_path):
  body = (
    '- taxon: crinoidea\n'
    '  children:\n'
    '  - taxon: cnemecrinus\n'
    '    bracketStart: camerata\n'
    '  - taxon: adelphicrinus\n'
    '    bracketEnd: camerata\n'
  )
  result = _check_draft(tmp_path, body)
  assert result.returncode == 0, result.stdout + result.stderr
  assert 'camerata' not in result.stdout.split('taxa:')[1].split('authors:')[0]
  result = _check_draft(tmp_path, body.replace('bracketStart: camerata', 'bracketStart: nope-x'))
  assert 'nope-x' in result.stdout


@pytest.mark.parametrize(
  ('body', 'message'),
  [
    (
      '- taxon: crinoidea\n  children:\n  - taxon: cnemecrinus\n    bracketEnd: camerata\n',
      'closes a bracket for camerata that is not open',
    ),
    (
      '- taxon: crinoidea\n  children:\n  - taxon: cnemecrinus\n    bracketStart: camerata\n',
      'opens a bracket for camerata that the tree never closes',
    ),
    (
      '- taxon: crinoidea\n  bracketStart: camerata\n  children:\n'
      '  - taxon: cnemecrinus\n    bracketStart: camerata\n',
      'opens a bracket for camerata that is already open',
    ),
  ],
)
def test_check_draft_reports_a_marker_that_does_not_pair(tmp_path, body, message):
  result = _check_draft(tmp_path, body)
  assert result.returncode == 1, result.stdout + result.stderr
  assert message in result.stdout


# -- the claims ---------------------------------------------------------------


def test_the_usage_is_at_the_start_node_and_names_the_end_nodes_path():
  tree = _tree(SPANS)
  p = tree.position
  usages = _bracket_usages(_claims(tree))
  assert [(c['subject'], c['path'], c['bracketEnd']) for c in usages] == [
    ('camerata', f'{p}/children/0', f'{p}/children/1/children/2'),
    ('disparida', f'{p}/children/1/children/3/children/0', f'{p}/children/1/children/3/children/0'),
  ]
  for usage in usages:
    assert usage['form'] == 'bracket'
    assert usage['spelling'] == usage['subject']
    assert usage['axis'] == 'children'
    assert 'placeholder' not in usage


def test_the_placement_is_under_the_bracket_via_bracket():
  tree = _tree(SPANS)
  claims = _claims(tree)
  p = tree.position
  [placement] = _bracket_placements(claims, f'{p}/children/1/children/2/children/1')
  assert placement['subject'] == 'celtocrinus'
  assert placement['parent'] == 'camerata'
  assert placement['via'] == 'bracket'
  # An unnamed node is no placement, and a node outside every span has none.
  assert _bracket_placements(claims, f'{p}/children/1') == []
  assert _bracket_placements(claims, f'{p}/children/2') == []
  assert [c['path'] for c in claims if c.get('via') == 'bracket'] == [
    f'{p}/children/0',
    f'{p}/children/1/children/0',
    f'{p}/children/1/children/1',
    f'{p}/children/1/children/2/children/0',
    f'{p}/children/1/children/2/children/1',
    f'{p}/children/1/children/2/children/2',
    f'{p}/children/1/children/3/children/0',
  ]


def test_the_nodes_own_placement_wins_by_path(tmp_path):
  tree = _tree(
    {
      'taxon': 'crinoidea',
      'children': [
        {'taxon': 'cnemecrinus', 'bracketStart': 'camerata'},
        {'taxon': 'adelphicrinus', 'bracketEnd': 'camerata'},
      ],
    },
    tree_type='taxonomy',
  )
  claims = _claims(tree)
  directory = tmp_path / 'claims'
  shutil.copytree(CLAIMS_DIR, directory)
  (directory / f'{SOURCE}.jsonl').write_text(''.join(json.dumps(c) + '\n' for c in claims))
  closure = Closure(ClaimStore(directory))
  for index in (0, 1):
    placed = closure.by_path[SOURCE][f'{tree.position}/children/{index}']
    assert placed.get('via') is None
    assert placed['parent'] == 'crinoidea'
    assert placed['position'] == index


def test_the_nodes_own_placement_follows_its_bracket_placements():
  tree = _tree(
    {
      'taxon': 'crinoidea',
      'children': [{'taxon': 'cnemecrinus', 'bracketStart': 'camerata', 'bracketEnd': 'camerata'}],
    },
    tree_type='taxonomy',
  )
  at = [c for c in _claims(tree) if c['kind'] == 'placement' and c['path'].endswith('/children/0')]
  assert [c.get('via') for c in at] == ['bracket', None]


# -- the schema ---------------------------------------------------------------


def _valid(document):
  return io.build_schema()[io.TREE_DEF].check(document)


def test_the_schema_takes_the_markers_on_any_node_and_refuses_the_old_field():
  node = {'taxon': 'cnemecrinus', 'bracketStart': 'camerata', 'bracketEnd': 'camerata'}
  assert _valid({'taxonomies': [{'taxon': 'crinoidea', 'children': [node]}]})
  assert _valid({'phylogenies': [{'treeType': 'cladogram', 'tree': {'children': [node]}}]})
  assert not _valid({'taxonomies': [{'taxon': 'cnemecrinus', 'bracket': 'camerata'}]})
  assert not _valid(
    {'phylogenies': [{'treeType': 'cladogram', 'tree': {'taxon': 'x', 'bracket': 'camerata'}}]}
  )
  assert not _valid({'taxonomies': [{'taxon': 'cnemecrinus', 'bracketStart': 1}]})


def test_the_taxa_schema_keeps_bracket_on_a_record():
  record = {
    'name': 'Edrioasteroidea',
    'authority': {'source': '1858b_billings'},
    'rank': 'Class',
    'bracket': 'Edrioasteroids',
  }
  schema = io.build_schema()['taxa']
  assert schema.check({'x': record})
  assert not schema.check({'x': {**record, 'bracketStart': 'camerata'}})


# -- the corpus ---------------------------------------------------------------

MIGRATED = (
  '1985_smith.a.b',
  '1998_dean.j_smith.a.b',
  '2003_guensburg_sprinkle',
  '2013_nardin_bohatý',
  '2017_nardin_lefebvre_fatka_nohejlová_kašiča_šinágl_szabad',
  '2017_zamora_sumrall_zhu.x.j_lefebvre',
  '2020_guensburg_sprinkle_mooi_lefebvre_david_roux_derstler',
  '2022_zamora_rahman_sumrall_gibson_thompson',
)


def _marked(value, field):
  """Every value of `field` anywhere in a raw document."""
  if isinstance(value, dict):
    for key, item in value.items():
      if key == field:
        yield item
      else:
        yield from _marked(item, field)
  elif isinstance(value, list):
    for item in value:
      yield from _marked(item, field)


@pytest.mark.parametrize('source', MIGRATED)
def test_a_migrated_trees_bracket_placements_are_under_the_taxa_it_brackets(source, store):
  bracketed = set(_marked(io.load_yaml(io.TREE_DIR / f'{source}.yaml'), 'bracketStart'))
  assert bracketed
  assert set(_marked(io.load_yaml(io.TREE_DIR / f'{source}.yaml'), 'bracket')) == set()
  claims = store.by_source[source]
  placements = [c for c in claims if c['kind'] == 'placement' and c.get('via') == 'bracket']
  assert placements
  assert {c['parent'] for c in placements} <= bracketed
  usages = _bracket_usages(claims)
  assert {c['subject'] for c in usages} == bracketed
  assert all(c['bracketEnd'] for c in usages)


def test_the_2003_camerata_and_disparida_placements(store):
  placements = [
    (c['subject'], c['parent'])
    for c in store.by_source['2003_guensburg_sprinkle']
    if c['kind'] == 'placement' and c.get('via') == 'bracket'
  ]
  for genus in ('habrotecrinus', 'celtocrinus', 'proexenocrinus'):
    assert (genus, 'camerata') in placements
  assert ('ramseyocrinus', 'disparida') in placements


# -- sections -----------------------------------------------------------------

INTEGRA = 'integra_linnaeus_1758'
STELLATAE = 'stellatae_linnaeus_1758'
RADIATAE = 'radiatae_linnaeus_1758'
UNNAMED = 'testacea-multivalvia_linnaeus_1758'


@pytest.fixture
def sections(monkeypatch):
  """A synthetic sections registry, in place of the (empty) real one."""
  monkeypatch.setattr(Section, '_sections', {})
  authority = {'source': '1758_linnaeus'}
  Section.add({'name': 'Integra', 'authority': authority, 'citedAs': 'Integra'}, INTEGRA)
  Section.add({'name': 'Stellatae', 'authority': authority}, STELLATAE)
  Section.add({'name': 'Radiatae', 'authority': authority}, RADIATAE)
  Section.add({'name': None, 'designation': 'Multivalvia', 'authority': authority}, UNNAMED)
  return Section._sections


def _start(key, **marker):
  return {'section': key, **marker}


def _taxonomy(children):
  return _tree({'taxon': 'asterias', 'children': children}, tree_type='taxonomy')


def _in(node):
  return tuple(section.key for section in node.sections)


def _listed(tree):
  return [node for node in _nodes(tree) if node.parent is not None]


# *Asterias* as Linnaeus 1758 divides it, in miniature: one sibling in
# "Integra", three in "Stellatae", and three in "Radiatae", one of them
# unnamed and the last with a subtree.
ASTERIAS = [
  {
    'taxon': 'luna_linnaeus_1758',
    'sectionStart': _start(INTEGRA, citedAs='Integra', pages=661),
    'sectionEnd': INTEGRA,
  },
  {'taxon': 'rubens_linnaeus_1758', 'sectionStart': _start(STELLATAE, citedAs='Stellatae')},
  {'taxon': 'glacialis_linnaeus_1758'},
  {'taxon': 'laevigata_linnaeus_1758', 'sectionEnd': STELLATAE},
  {'taxon': 'multiradiata_linnaeus_1758', 'sectionStart': _start(RADIATAE, notes='Rays > 5.')},
  {},
  {
    'taxon': 'ophiura_linnaeus_1758',
    'sectionEnd': RADIATAE,
    'children': [{'taxon': 'pectinata_linnaeus_1758'}],
  },
]


def _section_claims(tree):
  return [c for c in _claims(tree) if c['kind'] == 'section']


# -- the schema ---------------------------------------------------------------


def test_the_sections_schema_takes_a_name_or_a_designation():
  schema = io.build_schema()['sections']
  authority = {'source': '1758_linnaeus'}
  assert schema.check({})
  assert schema.check({INTEGRA: {'name': 'Integra', 'authority': authority, 'citedAs': 'Integra'}})
  assert schema.check(
    {UNNAMED: {'name': None, 'designation': 'Multivalvia', 'authority': authority, 'notes': 'A.'}}
  )
  assert schema.check({INTEGRA: {'name': 'Integra', 'auth': ['linnaeus'], 'year': 1758}})
  assert schema.check({INTEGRA: {'name': 'Integra'}})


@pytest.mark.parametrize(
  'record',
  [
    {'name': None, 'authority': {'source': '1758_linnaeus'}},
    {'designation': 'Multivalvia'},
    {'name': 'Integra', 'rank': 'section'},
    {'name': 'Integra', 'pages': 661},
    {'name': 'Integra', 'authority': {'source': 'nope'}},
    {'name': 'Integra', 'children': []},
  ],
)
def test_the_sections_schema_refuses_what_a_section_is_not(record):
  assert not io.build_schema()['sections'].check({INTEGRA: record})


def test_the_markers_validate_on_a_taxonomy_node():
  node = {'taxon': 'luna_linnaeus_1758', 'sectionStart': _start(INTEGRA), 'sectionEnd': INTEGRA}
  assert _valid({'taxonomies': [{'taxon': 'asterias', 'children': [node]}]})
  full = {**node, 'sectionStart': _start(INTEGRA, citedAs='Integra', pages=[661, 662], notes='x')}
  assert _valid({'taxonomies': [{'taxon': 'asterias', 'children': [full]}]})
  assert _valid({'taxonomies': [{'taxon': 'asterias', 'children': ASTERIAS}]})


@pytest.mark.parametrize(
  'node',
  [
    {'taxon': 'luna_linnaeus_1758', 'sectionStart': {'citedAs': 'Integra'}},
    {'taxon': 'luna_linnaeus_1758', 'sectionStart': INTEGRA},
    {'taxon': 'luna_linnaeus_1758', 'sectionStart': _start(INTEGRA, extra=1)},
    {'taxon': 'luna_linnaeus_1758', 'sectionEnd': {'section': INTEGRA}},
    {'taxon': 'luna_linnaeus_1758', 'sectionEnd': 1},
  ],
)
def test_the_markers_schema_refuses_a_malformed_marker(node):
  assert not _valid({'taxonomies': [{'taxon': 'asterias', 'children': [node]}]})


def test_the_markers_are_valid_in_a_taxonomy_only():
  node = {'taxon': 'luna_linnaeus_1758', 'sectionStart': _start(INTEGRA), 'sectionEnd': INTEGRA}
  assert not _valid(
    {'phylogenies': [{'treeType': 'cladogram', 'tree': {'taxon': 'asterias', 'children': [node]}}]}
  )


# -- the loader ---------------------------------------------------------------


def test_a_clean_sibling_list_with_three_sections(sections):
  tree = _taxonomy(ASTERIAS)
  assert [_in(n) for n in _listed(tree)] == [
    (INTEGRA,),
    (STELLATAE,),
    (STELLATAE,),
    (STELLATAE,),
    (RADIATAE,),
    (RADIATAE,),
    (RADIATAE,),
    # The subtree of the last sibling lies in the section too.
    (RADIATAE,),
  ]
  assert _in(tree) == ()
  luna, rubens, glacialis, laevigata, multiradiata, unnamed, ophiura, pectinata = _listed(tree)
  assert luna.section_end_node is luna
  assert rubens.section_end_node is laevigata
  assert multiradiata.section_end_node is ophiura
  assert glacialis.section_end_node is None
  assert [n.section_start and n.section_start.key for n in _listed(tree)] == [
    INTEGRA,
    STELLATAE,
    None,
    None,
    RADIATAE,
    None,
    None,
    None,
  ]
  assert laevigata.section_end.key == STELLATAE
  assert luna.section_start.name == 'Integra'
  assert luna.section_start_marker == {'section': INTEGRA, 'citedAs': 'Integra', 'pages': 661}


def test_both_markers_on_one_node_are_a_one_node_section(sections):
  tree = _taxonomy(
    [{'taxon': 'luna_linnaeus_1758', **ASTERIAS[0]}, {'taxon': 'rubens_linnaeus_1758'}]
  )
  first, second = _listed(tree)
  assert (_in(first), _in(second)) == ((INTEGRA,), ())
  assert first.section_end_node is first


def test_sections_of_a_list_nest(sections):
  tree = _taxonomy(
    [
      {'taxon': 'luna_linnaeus_1758', 'sectionStart': _start(INTEGRA)},
      {'taxon': 'rubens_linnaeus_1758', 'sectionStart': _start(STELLATAE)},
      {
        'taxon': 'glacialis_linnaeus_1758',
        'sectionEnd': STELLATAE,
        'children': [{'taxon': 'pectinata_linnaeus_1758'}],
      },
      {'taxon': 'laevigata_linnaeus_1758', 'sectionEnd': INTEGRA},
      {'taxon': 'ophiura_linnaeus_1758'},
    ]
  )
  assert [_in(n) for n in _listed(tree)] == [
    (INTEGRA,),
    (INTEGRA, STELLATAE),
    (INTEGRA, STELLATAE),
    (INTEGRA, STELLATAE),
    (INTEGRA,),
    (),
  ]
  assert [n.section_end_node and n.section_end_node.taxon.key for n in _listed(tree)][:2] == [
    'laevigata_linnaeus_1758',
    'glacialis_linnaeus_1758',
  ]


def test_a_subtree_carries_the_sections_of_its_ancestors_below_its_own(sections):
  tree = _taxonomy(
    [
      {
        'taxon': 'luna_linnaeus_1758',
        'sectionStart': _start(INTEGRA),
        'sectionEnd': INTEGRA,
        'children': [
          {'taxon': 'rubens_linnaeus_1758', 'sectionStart': _start(STELLATAE)},
          {'taxon': 'glacialis_linnaeus_1758', 'sectionEnd': STELLATAE},
          {'taxon': 'laevigata_linnaeus_1758'},
        ],
      },
      {'taxon': 'ophiura_linnaeus_1758'},
    ]
  )
  assert [_in(n) for n in _listed(tree)] == [
    (INTEGRA,),
    (INTEGRA, STELLATAE),
    (INTEGRA, STELLATAE),
    (INTEGRA,),
    (),
  ]


def test_sections_of_different_lists_do_not_pair(sections, caplog):
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    _taxonomy(
      [
        {
          'taxon': 'luna_linnaeus_1758',
          'sectionStart': _start(INTEGRA),
          'children': [{'taxon': 'rubens_linnaeus_1758', 'sectionEnd': INTEGRA}],
        },
      ]
    )
  messages = _errors(caplog)
  assert len(messages) == 2
  assert any('closes a section for integra_linnaeus_1758 that is not open' in m for m in messages)
  assert any(
    'opens a section for integra_linnaeus_1758 that its sibling list never closes' in m
    for m in messages
  )


def test_the_section_of_an_unnamed_heading_has_a_designation(sections):
  assert Section.get(UNNAMED).name is None
  assert Section.get(UNNAMED).label == 'Multivalvia'
  assert Section.get(INTEGRA).label == 'Integra'
  assert Section.get(INTEGRA).authority.source.key == '1758_linnaeus'
  assert Section.get(INTEGRA).cited_as == 'Integra'
  assert Section.get('nope') is None


@pytest.mark.parametrize(
  ('children', 'message'),
  [
    (
      [{'taxon': 'luna_linnaeus_1758', 'sectionEnd': INTEGRA}],
      f'closes a section for {INTEGRA} that is not open',
    ),
    (
      [
        {'taxon': 'luna_linnaeus_1758', 'sectionStart': _start(INTEGRA), 'sectionEnd': INTEGRA},
        {'taxon': 'rubens_linnaeus_1758', 'sectionEnd': INTEGRA},
      ],
      f'closes a section for {INTEGRA} that is not open',
    ),
    (
      [
        {'taxon': 'luna_linnaeus_1758', 'sectionStart': _start(INTEGRA)},
        {'taxon': 'rubens_linnaeus_1758'},
      ],
      f'opens a section for {INTEGRA} that its sibling list never closes',
    ),
    (
      [
        {'taxon': 'luna_linnaeus_1758', 'sectionStart': _start(INTEGRA)},
        {'taxon': 'rubens_linnaeus_1758', 'sectionStart': _start(INTEGRA), 'sectionEnd': INTEGRA},
      ],
      f'opens a section for {INTEGRA} that is already open',
    ),
    (
      [
        {'taxon': 'luna_linnaeus_1758', 'sectionStart': _start(INTEGRA)},
        {'taxon': 'rubens_linnaeus_1758', 'sectionStart': _start(STELLATAE)},
        {'taxon': 'glacialis_linnaeus_1758', 'sectionEnd': INTEGRA},
        {'taxon': 'laevigata_linnaeus_1758', 'sectionEnd': STELLATAE},
      ],
      f'closes the section for {INTEGRA} while the section for {STELLATAE}, opened inside it, '
      'is still open',
    ),
    (
      [{'taxon': 'luna_linnaeus_1758', 'sectionStart': _start('no-such-section')}],
      'Unrecognized tree sectionStart no-such-section for',
    ),
    (
      [{'taxon': 'luna_linnaeus_1758', 'sectionEnd': 'no-such-section'}],
      'Unrecognized tree sectionEnd no-such-section for',
    ),
  ],
)
def test_the_loader_reports_a_section_marker_that_does_not_pair(
  sections, caplog, children, message
):
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    tree = _taxonomy(children)
  [error] = _errors(caplog)
  assert message in error
  # The message names the offending node, except where it names the key.
  assert f'[{tree.position}]/asterias' in error


def test_the_unclosed_section_error_is_on_the_start_node(sections, caplog):
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    _taxonomy(
      [
        {'taxon': 'luna_linnaeus_1758'},
        {'taxon': 'rubens_linnaeus_1758', 'sectionStart': _start(INTEGRA)},
        {'taxon': 'glacialis_linnaeus_1758'},
      ]
    )
  [error] = _errors(caplog)
  assert '/rubens_linnaeus_1758 opens a section' in error


@pytest.mark.parametrize('tree_type', ['cladogram', 'diagram', 'other'])
def test_the_loader_reports_a_marker_in_a_tree_that_is_no_taxonomy(sections, caplog, tree_type):
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    tree = _tree(
      {'children': [{'taxon': 'luna_linnaeus_1758', 'sectionStart': _start(INTEGRA)}]},
      tree_type=tree_type,
    )
  [error] = _errors(caplog)
  assert error.endswith(
    f'has `sectionStart` but is in a {tree_type}; sections belong to taxonomies'
  )
  # Nothing is paired, so the node lies in no section.
  assert _in(_listed(tree)[0]) == ()
  assert _listed(tree)[0].section_start is None


def test_the_loader_reports_a_marker_on_a_cited_entry_or_a_root(sections, caplog):
  not_a_child = 'is not a `children` entry; a root or a cited entry cannot start or end a section'
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    _taxonomy(
      [
        {
          'taxon': 'luna_linnaeus_1758',
          'synonyms': [{'taxon': 'rubens_linnaeus_1758', 'sectionEnd': INTEGRA}],
        }
      ]
    )
  [error] = _errors(caplog)
  assert error.endswith(f'has `sectionEnd` but {not_a_child}')
  caplog.clear()
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    _tree(
      {'taxon': 'asterias', 'sectionStart': _start(INTEGRA), 'sectionEnd': INTEGRA},
      tree_type='taxonomy',
    )
  assert [e.partition(' has ')[2] for e in _errors(caplog)] == [
    f'`sectionStart` but {not_a_child}',
    f'`sectionEnd` but {not_a_child}',
  ]


# -- the draft checker --------------------------------------------------------


def _sectioned(root):
  return {'taxonomies': [root]}


@pytest.mark.parametrize(
  ('children', 'message'),
  [
    (
      [{'taxon': 'luna_linnaeus_1758', 'sectionEnd': INTEGRA}],
      f'0/children/0: closes a section for {INTEGRA} that is not open',
    ),
    (
      [{'taxon': 'luna_linnaeus_1758', 'sectionStart': _start(INTEGRA)}],
      f'0/children/0: opens a section for {INTEGRA} that its sibling list never closes',
    ),
    (
      [
        {'taxon': 'luna_linnaeus_1758', 'sectionStart': _start(INTEGRA)},
        {'taxon': 'rubens_linnaeus_1758', 'sectionStart': _start(INTEGRA)},
        {'taxon': 'glacialis_linnaeus_1758', 'sectionEnd': INTEGRA},
      ],
      f'0/children/1: opens a section for {INTEGRA} that is already open',
    ),
    (
      [
        {'taxon': 'luna_linnaeus_1758', 'sectionStart': _start(INTEGRA)},
        {'taxon': 'rubens_linnaeus_1758', 'sectionStart': _start(STELLATAE)},
        {'taxon': 'glacialis_linnaeus_1758', 'sectionEnd': INTEGRA},
        {'taxon': 'laevigata_linnaeus_1758', 'sectionEnd': STELLATAE},
      ],
      f'0/children/2: closes the section for {INTEGRA} while the section for {STELLATAE}, '
      'opened inside it, is still open',
    ),
  ],
)
def test_the_raw_section_pairing_reports_what_the_loader_does(children, message):
  document = _sectioned({'taxon': 'asterias', 'children': children})
  assert material.section_errors(document) == [('error', message)]


def test_the_raw_section_pairing_passes_a_paired_tree_and_pairs_each_list_alone():
  assert material.section_errors(_sectioned({'taxon': 'asterias', 'children': ASTERIAS})) == []
  # The same key in two lists, a nested one included, is no clash.
  document = _sectioned(
    {
      'taxon': 'asterias',
      'children': [
        {
          'taxon': 'luna_linnaeus_1758',
          'sectionStart': _start(INTEGRA),
          'sectionEnd': INTEGRA,
          'children': [
            {
              'taxon': 'rubens_linnaeus_1758',
              'sectionStart': _start(INTEGRA),
              'sectionEnd': INTEGRA,
            }
          ],
        }
      ],
    }
  )
  assert material.section_errors(document) == []
  # A marker inside a synonym is no part of the children lists.
  synonym = {'taxon': 'rubens_linnaeus_1758', 'sectionStart': _start(INTEGRA)}
  root = {'taxon': 'asterias', 'children': [{'taxon': 'luna_linnaeus_1758', 'synonyms': [synonym]}]}
  [(level, message)] = material.section_errors(_sectioned(root))
  assert level == 'error'
  assert message.startswith('0/children/0/synonyms/0: has `sectionStart` but is not a `children`')


def test_the_raw_section_rules_name_a_tree_that_is_no_taxonomy_and_a_root():
  node = {'taxon': 'luna_linnaeus_1758', 'sectionEnd': INTEGRA}
  document = {'phylogenies': [{'treeType': 'cladogram', 'tree': {'children': [node]}}]}
  assert material.section_errors(document) == [
    (
      'error',
      '0/children/0: has `sectionEnd` but is in a cladogram; sections belong to taxonomies',
    )
  ]
  [(_, message)] = material.section_errors(_sectioned({'taxon': 'asterias', **node}))
  assert message.startswith('0: has `sectionEnd` but is not a `children` entry')


def test_check_draft_checks_the_section_keys_and_the_pairing(tmp_path):
  body = (
    '- taxon: asterias\n'
    '  children:\n'
    '  - taxon: luna_linnaeus_1758\n'
    '    sectionStart: {section: no-such-section, citedAs: Integra}\n'
    '  - taxon: rubens_linnaeus_1758\n'
    '    sectionEnd: no-such-section\n'
  )
  result = _check_draft(tmp_path, body)
  assert result.returncode == 0, result.stdout + result.stderr
  assert 'sections: 1 cited, 1 without a record\n  no-such-section' in result.stdout
  result = _check_draft(tmp_path, body.replace('    sectionEnd: no-such-section\n', ''))
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'sections: 1 cited, 1 without a record' in result.stdout
  assert (
    'error: 0/children/0: opens a section for no-such-section that its sibling list never closes'
    in result.stdout
  )
  result = _check_draft(tmp_path, body.replace('{section: no-such-section, citedAs: Integra}', 'x'))
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'not valid against the tree schema' in result.stdout


# -- the claims ---------------------------------------------------------------


def test_the_section_claims_of_asterias(sections):
  tree = _taxonomy(ASTERIAS)
  p = tree.position
  integra, stellatae, radiatae = _section_claims(tree)
  common = {'kind': 'section', 'source': SOURCE, 'tree': 'taxonomy'}
  assert {k: v for k, v in integra.items() if k != 'audit'} == {
    **common,
    'path': f'{p}/children/0',
    'subject': INTEGRA,
    'section': INTEGRA,
    'name': 'Integra',
    'members': ['luna_linnaeus_1758'],
    'memberPaths': [f'{p}/children/0'],
    'endPath': f'{p}/children/0',
    'citedAs': 'Integra',
    'pages': 661,
    'id': f'{SOURCE}:{p}/children/0:section',
  }
  assert {k: v for k, v in stellatae.items() if k != 'audit'} == {
    **common,
    'path': f'{p}/children/1',
    'subject': STELLATAE,
    'section': STELLATAE,
    'name': 'Stellatae',
    'members': ['rubens_linnaeus_1758', 'glacialis_linnaeus_1758', 'laevigata_linnaeus_1758'],
    'memberPaths': [f'{p}/children/{i}' for i in (1, 2, 3)],
    'endPath': f'{p}/children/3',
    'citedAs': 'Stellatae',
    'id': f'{SOURCE}:{p}/children/1:section',
  }
  # The unnamed sibling is a member by path only, and the end node's own
  # subtree is no member.
  assert {k: v for k, v in radiatae.items() if k != 'audit'} == {
    **common,
    'path': f'{p}/children/4',
    'subject': RADIATAE,
    'section': RADIATAE,
    'name': 'Radiatae',
    'members': ['multiradiata_linnaeus_1758', 'ophiura_linnaeus_1758'],
    'memberPaths': [f'{p}/children/{i}' for i in (4, 5, 6)],
    'endPath': f'{p}/children/6',
    'notes': 'Rays > 5.',
    'id': f'{SOURCE}:{p}/children/4:section',
  }
  for claim in (integra, stellatae, radiatae):
    assert claim['audit'] == {'state': 'unaudited'}
    assert 'printedAttribution' not in claim


def test_a_section_claim_names_an_unnamed_section_by_its_designation(sections):
  tree = _taxonomy(
    [{'taxon': 'luna_linnaeus_1758', 'sectionStart': _start(UNNAMED), 'sectionEnd': UNNAMED}]
  )
  [claim] = _section_claims(tree)
  assert claim['name'] == 'Multivalvia'
  assert claim['members'] == ['luna_linnaeus_1758']


def test_a_node_opening_two_sections_has_a_numbered_claim_for_each(sections):
  tree = _taxonomy(
    [
      {
        'taxon': 'luna_linnaeus_1758',
        'sectionStart': _start(INTEGRA),
        'sectionEnd': INTEGRA,
      },
      {'taxon': 'rubens_linnaeus_1758', 'sectionStart': _start(STELLATAE), 'sectionEnd': STELLATAE},
    ]
  )
  assert [c['id'].rpartition(':')[2] for c in _section_claims(tree)] == ['section', 'section']
  tree = _taxonomy(
    [
      {'taxon': 'luna_linnaeus_1758', 'sectionStart': _start(INTEGRA)},
      {'taxon': 'rubens_linnaeus_1758', 'sectionEnd': INTEGRA},
    ]
  )
  [claim] = _section_claims(tree)
  assert claim['members'] == ['luna_linnaeus_1758', 'rubens_linnaeus_1758']


def test_a_section_never_closed_has_no_claim(sections):
  tree = _taxonomy([{'taxon': 'luna_linnaeus_1758', 'sectionStart': _start(INTEGRA)}])
  assert _section_claims(tree) == []


def test_a_section_is_no_placement_or_usage_and_the_nodes_claims_are_unchanged(sections):
  marked = _claims(_taxonomy(ASTERIAS))
  plain = _claims(
    _taxonomy([{k: v for k, v in n.items() if not k.startswith('section')} for n in ASTERIAS])
  )
  strip = lambda claims: [  # noqa: E731
    {k: v for k, v in c.items() if k != 'path' and k != 'id'}
    for c in claims
    if c['kind'] != 'section'
  ]
  assert strip(marked) == strip(plain)


def test_a_claim_store_over_a_section_claim_loads_and_the_tools_run_clean(sections, tmp_path):
  tree = _taxonomy(ASTERIAS)
  claims = _claims(tree)
  roots = {SOURCE: [tree]}
  table = manifest({SOURCE: claims}, roots)
  assert table['sources'][SOURCE]['claims']['section'] == 3
  # A section's subject is no taxon: the per-taxon source lists skip it.
  assert not {INTEGRA, STELLATAE, RADIATAE} & set(table['taxa'])
  assert SOURCE in table['taxa']['luna_linnaeus_1758']

  directory = tmp_path / 'claims'
  shutil.copytree(CLAIMS_DIR, directory)
  (directory / f'{SOURCE}.jsonl').write_text(''.join(json.dumps(c) + '\n' for c in claims))
  store = ClaimStore(directory)
  [claim] = [c for c in store.by_source[SOURCE] if c.get('section') == INTEGRA]
  assert store.by_id[claim['id']] is claim
  assert INTEGRA not in store.by_subject
  assert store.name(INTEGRA) == f'[{INTEGRA}]'
  assert store.at_path[SOURCE][claim['path']]
  # The tools that read a taxon's claims by path are unmoved by it.
  closure = Closure(store)
  assert closure.by_path[SOURCE][claim['path']]['subject'] == 'luna_linnaeus_1758'
  assert store.words.claim_words(claim) == 'section'
