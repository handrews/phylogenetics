"""The `type` node: a taxon carries its type as a node, cited like a
synonymy entry: the schema, the loader checks, the claims, and the words
and listings the tools say.

Synthetic trees are built on the session's loaded corpus under positions
300 and up (`Tree` keeps class-level registries); the tool tests read a
`ClaimStore` over a copy of `claims/` whose files for the sources named in
`TREES` are replaced by the claims of those trees, since no data uses
`type` yet.
"""

import collections
import json
import logging
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from phylohist.claims import derived_coverage, extract, manifest
from phylohist.loader import io, material, nomenclature
from phylohist.loader.load import _report_nomenclature
from phylohist.loader.material import walk_document
from phylohist.loader.taxa import Tree
from phylohist.store import CLAIMS_DIR, ClaimStore
from phylohist.words import ABSENCE_WORDS

# The synthetic trees name real records, so every test needs the corpus loaded.
pytestmark = pytest.mark.usefixtures('load_records')

SCRIPTS = Path(__file__).parent.parent / 'scripts'

# The records of the examples: a genus (Edrioaster) with two species, the
# genus a species was first described in (Cyclaster Billings 1857) and a
# family above.
GENUS = 'edrioaster'
CYCLASTER = 'cyclaster_billings_1857'
BIGSBYI = 'bigsbyi_billings_1857'
PRIORITY = 'priscus_miller.s.a_gurley_1894'
FAMILY = 'edrioasteridae'

ORIGINAL = {'taxon': BIGSBYI, 'parents': [{'taxon': CYCLASTER}], 'fixation': 'monotypy'}


# -- schema -------------------------------------------------------------------


def _valid(document):
  return io.build_schema()[io.TREE_DEF].check(document)


def _tree(node):
  return {'taxonomies': [{'taxon': GENUS, 'children': [], **node}]}


def test_schema_accepts_the_type_node():
  assert _valid(
    {
      'taxonomies': [
        {
          'taxon': GENUS,
          'synonyms': [{'taxon': CYCLASTER}],
          'type': {
            'taxon': BIGSBYI,
            'parents': [{'taxon': CYCLASTER}],
            'fixation': 'monotypy',
            'authority': {'source': '1857_billings', 'pages': 293},
            'pages': 293,
            'notes': 'Billings names it as the only species.',
            'editorial': {'inferred': ['fixation'], 'basis': 'one species listed'},
          },
          'children': [
            {'taxon': BIGSBYI, 'synonyms': [{'parents': [{'taxon': CYCLASTER}]}]},
            {'taxon': PRIORITY},
          ],
        }
      ]
    }
  )


@pytest.mark.parametrize(
  'fixation',
  [
    'originalDesignation',
    'monotypy',
    'subsequentDesignation',
    'subsequentMonotypy',
    'objectiveSynonymy',
    'tautonymy',
    'typus',
    'iczn',
  ],
)
def test_schema_accepts_each_fixation(fixation):
  assert _valid(_tree({'type': {'taxon': BIGSBYI, 'fixation': fixation}}))


def test_schema_accepts_fixed_by_an_authority():
  node = {
    'taxon': BIGSBYI,
    'fixation': 'subsequentDesignation',
    'fixedBy': {'source': '1899_bather', 'pages': 12},
  }
  assert _valid(_tree({'type': node}))


@pytest.mark.parametrize(
  'node',
  [
    # `fixation` and `fixedBy` belong to the `type` node alone.
    {'taxon': GENUS, 'fixation': 'monotypy'},
    {'taxon': GENUS, 'fixedBy': {'source': '1899_bather'}},
    {'taxon': GENUS, 'children': [{'taxon': BIGSBYI, 'fixation': 'monotypy'}]},
    {'taxon': GENUS, 'synonyms': [{'taxon': CYCLASTER, 'fixation': 'monotypy'}]},
    # The type names a taxon.
    {'taxon': GENUS, 'type': {'fixation': 'monotypy'}},
    {'taxon': GENUS, 'type': {'parents': [{'taxon': CYCLASTER}]}},
    # An unknown fixation, a fixedBy that is not an authority, a flag.
    {'taxon': GENUS, 'type': {'taxon': BIGSBYI, 'fixation': 'designated'}},
    {'taxon': GENUS, 'type': {'taxon': BIGSBYI, 'fixedBy': '1899_bather'}},
    {'taxon': GENUS, 'type': {'taxon': BIGSBYI, 'fixedBy': {'pages': 12}}},
    {'taxon': GENUS, 'type': True},
    {'taxon': GENUS, 'type': [{'taxon': BIGSBYI}]},
  ],
)
def test_schema_rejects_what_is_not_a_type_node(node):
  assert not _valid({'taxonomies': [node]})


# -- loader checks ------------------------------------------------------------


def _messages(result):
  return [m for _, m in result]


def test_type_node_clean_cases():
  assert nomenclature.type_node({'taxon': GENUS}, is_cited=False) == []
  assert nomenclature.type_node({'taxon': GENUS, 'type': {'taxon': BIGSBYI}}, is_cited=False) == []
  assert (
    nomenclature.type_node({'taxon': GENUS, 'children': [{'taxon': BIGSBYI}]}, is_cited=False) == []
  )
  # A child's flag with no `type` is the old form, which is still allowed.
  old = {'taxon': GENUS, 'children': [{'taxon': BIGSBYI, 'isType': True}]}
  assert nomenclature.type_node(old, is_cited=False) == []
  assert (
    nomenclature.type_node(
      {
        'taxon': GENUS,
        'type': {'taxon': BIGSBYI, 'fixation': 'iczn', 'fixedBy': {'source': '1899_bather'}},
        'children': [{'taxon': BIGSBYI, 'isType': False}],
      },
      is_cited=False,
    )
    == []
  )


def test_type_node_without_a_taxon():
  assert nomenclature.type_node(
    {'taxon': GENUS, 'type': {'fixation': 'monotypy'}}, is_cited=False
  ) == [
    ('error', '`type` names no taxon'),
  ]
  assert _messages(nomenclature.type_node({'taxon': GENUS, 'type': {}}, is_cited=False)) == [
    '`type` names no taxon'
  ]
  assert _messages(nomenclature.type_node({'taxon': GENUS, 'type': True}, is_cited=False)) == [
    '`type` names no taxon'
  ]


def test_type_beside_a_child_marked_is_type():
  node = {
    'taxon': GENUS,
    'type': {'taxon': BIGSBYI},
    'children': [{'taxon': PRIORITY}, {'taxon': BIGSBYI, 'isType': True}],
  }
  assert nomenclature.type_node(node, is_cited=False) == [
    ('error', '`type` beside a child marked `isType`: the type is stated twice'),
  ]


@pytest.mark.parametrize('fixation', ['subsequentDesignation', 'subsequentMonotypy', 'iczn'])
def test_fixed_by_goes_with_a_fixation_it_can_explain(fixation):
  type_node = {'taxon': BIGSBYI, 'fixation': fixation, 'fixedBy': {'source': '1899_bather'}}
  assert nomenclature.type_node({'type': type_node}, is_cited=False) == []


@pytest.mark.parametrize('fixation', [None, 'monotypy', 'originalDesignation', 'typus'])
def test_fixed_by_without_such_a_fixation_is_an_error(fixation):
  type_node = {'taxon': BIGSBYI, 'fixedBy': {'source': '1899_bather'}}
  if fixation:
    type_node['fixation'] = fixation
  assert nomenclature.type_node({'type': type_node}, is_cited=False) == [
    (
      'error',
      '`fixedBy` needs a `fixation` of subsequentDesignation, subsequentMonotypy or iczn',
    ),
  ]


def test_the_checks_can_all_fire_on_one_node():
  node = {
    'type': {'fixedBy': {'source': '1899_bather'}},
    'children': [{'taxon': BIGSBYI, 'isType': True}],
  }
  assert len(nomenclature.type_node(node, is_cited=False)) == 3


def test_load_reports_the_type_checks_with_the_nodes_path(load_records, caplog):
  data = {
    'trees': {
      'src1': {
        'taxonomies': [
          {
            'taxon': FAMILY,
            'children': [
              {'taxon': GENUS, 'type': {'fixation': 'monotypy'}},
              {
                'taxon': 'cyclaster',
                'type': {'taxon': BIGSBYI},
                'children': [{'taxon': BIGSBYI, 'isType': True}],
              },
              {
                'taxon': 'carneyella',
                'type': {'taxon': BIGSBYI, 'fixedBy': {'source': '1899_bather'}},
              },
              {'taxon': 'rhenopyrgus', 'type': {'taxon': BIGSBYI, 'fixation': 'monotypy'}},
            ],
          }
        ],
      },
    },
  }
  with caplog.at_level(logging.WARNING, logger='phylohist'):
    _report_nomenclature(data)
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert any('src1 at 0/children/0: `type` names no taxon' in m for m in errors)
  assert any('src1 at 0/children/1: `type` beside a child marked `isType`' in m for m in errors)
  assert any('src1 at 0/children/2: `fixedBy` needs a `fixation` of' in m for m in errors)
  assert len(errors) == 3


def test_the_type_node_is_walked_as_a_cited_entry():
  document = {
    'taxonomies': [
      {'taxon': GENUS, 'type': {'taxon': BIGSBYI, 'parents': [{'taxon': CYCLASTER}]}},
    ],
  }
  walked = {path: (node.get('taxon'), cited) for path, node, cited in walk_document(document)}
  assert walked == {
    '0': (GENUS, False),
    '0/type': (BIGSBYI, True),
    '0/type/parents/0': (CYCLASTER, False),
  }


def test_the_corpus_has_no_type_node_messages(load_records):
  data, _, _ = load_records
  found = []
  for opinion in data['trees'].values():
    for _, node, is_cited in walk_document(opinion):
      found += nomenclature.type_node(node, is_cited)
      assert 'type' not in node
  assert found == []


def test_a_species_level_name_cannot_carry_a_type(load_records, caplog):
  root = {'taxon': BIGSBYI, 'type': {'taxon': PRIORITY}}
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    Tree(root, {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 290})
  [error] = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert 'carries `type` but is a species-level name; its type is a specimen' in error


def test_a_genus_or_family_may_carry_a_type(load_records, caplog):
  root = {'taxon': FAMILY, 'type': {'taxon': GENUS}, 'children': [{'taxon': GENUS}]}
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    Tree(root, {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 291})
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]


# -- scripts/check_draft.py ---------------------------------------------------


def _draft(tmp_path, body):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text('taxonomies:\n- taxon: rhenopyrgus\n  children:\n' + body)
  return subprocess.run(
    [sys.executable, str(SCRIPTS / 'check_draft.py'), str(draft)],
    capture_output=True,
    text=True,
  )


def test_check_draft_accepts_a_type_node(tmp_path):
  result = _draft(
    tmp_path,
    '  - taxon: pyrgocystis\n'
    '    type:\n'
    '      taxon: grayae_bather_1915\n'
    '      fixation: subsequentDesignation\n'
    '      fixedBy:\n'
    '        source: 1899_bather\n'
    '        pages: 12\n',
  )
  assert result.returncode == 0, result.stdout + result.stderr


def test_check_draft_reports_the_type_checks(tmp_path):
  result = _draft(
    tmp_path,
    '  - taxon: pyrgocystis\n'
    '    type:\n'
    '      fixation: monotypy\n'
    '  - taxon: cyclaster\n'
    '    type:\n'
    '      taxon: grayae_bather_1915\n'
    '    children:\n'
    '    - taxon: grayae_bather_1915\n'
    '      isType: true\n'
    '  - taxon: carneyella\n'
    '    type:\n'
    '      taxon: grayae_bather_1915\n'
    '      fixation: monotypy\n'
    '      fixedBy:\n'
    '        source: 1899_bather\n',
  )
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'children/0: `type` names no taxon' in result.stdout
  assert (
    'children/1: `type` beside a child marked `isType`: the type is stated twice' in result.stdout
  )
  assert (
    'children/2: `fixedBy` needs a `fixation` of subsequentDesignation, '
    'subsequentMonotypy or iczn' in result.stdout
  )


# -- claims -------------------------------------------------------------------


def _claims(root, position, source):
  return extract(
    {source: [Tree(root, {'source_key': source, 'type': 'taxonomy', 'position': position})]}
  )[source]


def _by_path(claims):
  at = collections.defaultdict(list)
  for claim in claims:
    at[claim['path']].append(claim)
  return at


def _of_kind(claims, kind):
  return [c for c in claims if c['kind'] == kind]


def _one(claims, kind):
  [claim] = _of_kind(claims, kind)
  return claim


def _act(claims):
  [claim] = [c for c in claims if c['kind'] == 'act' and c['actKind'] == 'type']
  return claim


def _plain(claim):
  """The claim without the fields that vary with the file around it."""
  return {k: v for k, v in claim.items() if k not in ('audit', 'treeNotes')}


def test_a_type_that_is_also_a_child_is_listed_and_places_nothing(load_records):
  root = {
    'taxon': GENUS,
    'type': {**ORIGINAL, 'pages': 12},
    'children': [{'taxon': BIGSBYI}, {'taxon': PRIORITY}],
  }
  at = _by_path(_claims(root, 300, '1961_dehm'))
  claims = at['300/type']
  assert not _of_kind(claims, 'placement')
  assert _one(claims, 'usage')['axis'] == 'type'
  assert _plain(_act(claims)) == {
    'kind': 'act',
    'source': '1961_dehm',
    'path': '300/type',
    'tree': 'taxonomy',
    'subject': BIGSBYI,
    'printedAttribution': 'as-record',
    'citedPages': 12,
    'actKind': 'type',
    'typeOf': GENUS,
    'parents': [CYCLASTER],
    'fixation': 'monotypy',
    'listed': True,
    'id': '1961_dehm:300/type:act',
  }
  # The child's own placement stands, and no second act.
  assert [c['path'] for c in at['300/children/0'] if c['kind'] == 'placement'] == ['300/children/0']
  assert not _of_kind(at['300/children/0'], 'act')


def test_a_type_that_is_no_child_is_a_placement_of_its_own(load_records):
  root = {'taxon': FAMILY, 'children': [{'taxon': GENUS, 'type': ORIGINAL, 'children': []}]}
  at = _by_path(_claims(root, 301, '1985_jell_burrett_banks'))
  claims = at['301/children/0/type']
  assert _act(claims)['listed'] is False
  assert _act(claims)['typeOf'] == GENUS
  placement = _one(claims, 'placement')
  assert placement['parent'] == GENUS
  assert placement['via'] == 'type'
  assert placement['rank'] == 'species'
  assert 'position' not in placement
  assert placement['subject'] == BIGSBYI
  assert placement['id'] == '1985_jell_burrett_banks:301/children/0/type:placement'
  # The genus is a child of the family as before, and has no other placement.
  [genus] = [c for c in at['301/children/0'] if c['kind'] == 'placement']
  assert genus['parent'] == FAMILY and 'via' not in genus


def test_a_type_on_a_root_node_is_placed_under_the_root(load_records):
  root = {'taxon': GENUS, 'type': ORIGINAL, 'children': []}
  claims = _by_path(_claims(root, 302, '1891_bell.f.j'))['302/type']
  placement = _one(claims, 'placement')
  assert placement['parent'] == GENUS and placement['via'] == 'type'


def test_a_type_on_a_cited_entry_places_nothing(load_records):
  root = {
    'taxon': GENUS,
    'synonyms': [{'taxon': CYCLASTER, 'type': {'taxon': BIGSBYI, 'fixation': 'monotypy'}}],
    'children': [{'taxon': BIGSBYI}],
  }
  at = _by_path(_claims(root, 303, '1927_jaekel'))
  claims = at['303/synonyms/0/type']
  assert not _of_kind(claims, 'placement')
  act = _act(claims)
  assert act['typeOf'] == CYCLASTER
  assert act['listed'] is False
  assert act['fixation'] == 'monotypy'
  assert 'parents' not in act
  assert _one(claims, 'usage')['axis'] == 'type'
  # The synonym itself is unchanged: an acceptance and a usage, no act.
  assert not _of_kind(at['303/synonyms/0'], 'act')
  assert _one(at['303/synonyms/0'], 'acceptance')['under'] == GENUS


def test_a_type_under_a_non_taxonomy_places_nothing(load_records):
  root = {'taxon': GENUS, 'type': ORIGINAL, 'children': []}
  claims = extract(
    {
      '1927_jaekel': [
        Tree(root, {'source_key': '1927_jaekel', 'type': 'cladogram', 'position': 304})
      ]
    }
  )['1927_jaekel']
  assert _act(claims)['listed'] is False
  assert not _of_kind(claims, 'placement')


def test_a_type_names_a_record_not_a_rank_variant(load_records):
  # "The same record": a child of another record does not list the type.
  root = {'taxon': GENUS, 'type': ORIGINAL, 'children': [{'taxon': PRIORITY}]}
  assert _act(_by_path(_claims(root, 305, '1927_jaekel'))['305/type'])['listed'] is False


def test_fixed_by_rides_on_the_act_as_a_source_and_pages(load_records):
  node = {
    'taxon': BIGSBYI,
    'fixation': 'subsequentDesignation',
    'fixedBy': {'source': '1899_bather', 'pages': [12, 13]},
  }
  root = {'taxon': GENUS, 'type': node, 'children': []}
  act = _act(_by_path(_claims(root, 306, '1927_jaekel'))['306/type'])
  assert act['fixation'] == 'subsequentDesignation'
  assert act['fixedBy'] == '1899_bather' and act['fixedByPages'] == [12, 13]
  # Without pages there is no `fixedByPages`.
  node['fixedBy'] = {'source': '1899_bather'}
  act = _act(_by_path(_claims({'taxon': GENUS, 'type': node}, 307, '1927_jaekel'))['307/type'])
  assert act['fixedBy'] == '1899_bather' and 'fixedByPages' not in act


def test_an_inferred_type_statement_is_inferred_throughout(load_records):
  node = {**ORIGINAL, 'editorial': {'inferred': True, 'basis': 'one species listed'}}
  root = {'taxon': GENUS, 'type': node, 'children': []}
  claims = _by_path(_claims(root, 308, '1927_jaekel'))['308/type']
  act = _act(claims)
  assert act['inferred'] is True and 'inferredFields' not in act
  assert _one(claims, 'placement')['inferred'] is True


def test_an_inferred_method_is_the_acts_alone(load_records):
  node = {**ORIGINAL, 'editorial': {'inferred': ['fixation'], 'basis': 'one species listed'}}
  root = {'taxon': GENUS, 'type': node, 'children': []}
  claims = _by_path(_claims(root, 309, '1927_jaekel'))['309/type']
  act = _act(claims)
  assert act['inferredFields'] == ['fixation']
  assert 'inferred' not in act
  assert 'inferred' not in _one(claims, 'placement')
  assert 'inferred' not in _one(claims, 'usage')
  # An inferred list that does not name the fixation leaves the act alone.
  node['editorial'] = {'inferred': ['taxon'], 'basis': 'x'}
  claims = _by_path(_claims({'taxon': GENUS, 'type': node}, 310, '1927_jaekel'))['310/type']
  assert 'inferredFields' not in _act(claims)
  assert 'inferred' not in _act(claims)
  assert _one(claims, 'usage')['inferred'] is True


def test_the_type_act_counts_as_a_type_designation(load_records):
  from phylohist.claims import _coverage_kind

  root = {'taxon': GENUS, 'type': ORIGINAL, 'children': [{'taxon': BIGSBYI}]}
  claims = _by_path(_claims(root, 311, '1927_jaekel'))['311/type']
  assert _coverage_kind(_act(claims)) == 'types'
  assert _act(claims)['audit']['coverageKind'] == 'types'


def test_an_is_type_childs_claim_is_what_it_was(load_records):
  root = {
    'taxon': GENUS,
    'children': [{'taxon': BIGSBYI, 'isType': True}, {'taxon': PRIORITY}],
  }
  at = _by_path(_claims(root, 312, '1927_jaekel'))
  act = _act(at['312/children/0'])
  assert _plain(act) == {
    'kind': 'act',
    'source': '1927_jaekel',
    'path': '312/children/0',
    'tree': 'taxonomy',
    'subject': BIGSBYI,
    'printedAttribution': 'as-record',
    'actKind': 'type',
    'id': '1927_jaekel:312/children/0:act',
  }
  [placement] = _of_kind(at['312/children/0'], 'placement')
  assert placement['position'] == 0 and 'via' not in placement


def test_a_type_node_does_not_emit_a_second_act_from_is_type(load_records):
  node = {**ORIGINAL, 'isType': True}
  claims = _by_path(_claims({'taxon': GENUS, 'type': node}, 313, '1927_jaekel'))['313/type']
  assert len([c for c in claims if c['kind'] == 'act']) == 1


def test_a_type_has_no_acceptance_and_no_synonymy(load_records):
  root = {'taxon': GENUS, 'type': ORIGINAL, 'children': []}
  claims = _claims(root, 314, '1927_jaekel')
  assert not _of_kind(claims, 'acceptance')
  assert not _of_kind(claims, 'rejection')


# -- the tools ----------------------------------------------------------------

# A genus with its type listed as a child, and a synonym genus.
LISTED = {
  'taxon': GENUS,
  'synonyms': [{'taxon': CYCLASTER, 'authority': {'source': '1857_billings'}}],
  'type': ORIGINAL,
  'children': [{'taxon': BIGSBYI}, {'taxon': PRIORITY}],
}

# The same, with the type named only there; a family above, with its own
# type genus, a genus listed, and the fixation by a later work.
UNLISTED = {
  'taxon': 'echinodermata',
  'children': [
    {
      'taxon': FAMILY,
      'type': {'taxon': GENUS, 'fixation': 'originalDesignation'},
      'children': [
        {
          'taxon': GENUS,
          'synonyms': [{'taxon': CYCLASTER, 'authority': {'source': '1857_billings'}}],
          'type': ORIGINAL,
          'children': [{'taxon': PRIORITY}],
        },
      ],
    },
  ],
}

# The method fixed by a later work; the whole statement inferred; the method
# alone inferred.
FIXED = {
  'taxon': FAMILY,
  'children': [
    {
      'taxon': GENUS,
      'type': {
        'taxon': BIGSBYI,
        'parents': [{'taxon': CYCLASTER}],
        'fixation': 'subsequentDesignation',
        'fixedBy': {'source': '1899_bather', 'pages': 12},
      },
      'children': [{'taxon': PRIORITY}],
    },
  ],
}
INFERRED = {
  'taxon': FAMILY,
  'children': [
    {
      'taxon': GENUS,
      'type': {**ORIGINAL, 'editorial': {'inferred': True, 'basis': 'the only species listed'}},
      'children': [{'taxon': PRIORITY}],
    },
    {
      'taxon': 'cyclaster',
      'type': {
        'taxon': PRIORITY,
        'parents': [{'taxon': 'cyclaster'}],
        'fixation': 'monotypy',
        'editorial': {'inferred': ['fixation'], 'basis': 'one species'},
      },
    },
  ],
}

# The type's genus from the node it types: under a subgenus, the genus and
# the subgenus; the same type under a genus cited without one.
SUBGENUS = {
  'taxon': 'carneyella',
  'children': [
    {
      'taxon': 'agelacrinus-subgenus_carneyella',
      'type': {'taxon': BIGSBYI},
      'children': [],
    },
  ],
}

# A type named on the root, and one on a synonym genus.
ROOT = {
  'taxon': GENUS,
  'synonyms': [
    {
      'taxon': CYCLASTER,
      'type': {'taxon': PRIORITY, 'fixation': 'subsequentMonotypy'},
    },
    {'taxon': PRIORITY},
  ],
  'type': {'taxon': BIGSBYI, 'fixation': 'typus'},
  'children': [],
}

# The old form, in a family and in a genus.
OLD = {
  'taxon': FAMILY,
  'children': [
    {'taxon': GENUS, 'isType': True, 'children': [{'taxon': BIGSBYI, 'isType': True}]},
    {'taxon': 'cyclaster', 'children': []},
  ],
}

TREES = {
  '1961_dehm': (LISTED, 320),
  '1985_jell_burrett_banks': (UNLISTED, 321),
  '1891_bell.f.j': (FIXED, 322),
  '1899_bather': (INFERRED, 323),
  '1927_jaekel': (SUBGENUS, 324),
  '1935_bassler': (OLD, 325),
  '1936_bassler': (ROOT, 326),
}


@pytest.fixture(scope='module')
def synthetic(load_records, tmp_path_factory):
  """A `ClaimStore` over a copy of `claims/` with the claims of each source
  of `TREES` replaced by those of its tree."""
  directory = tmp_path_factory.mktemp('claims')
  shutil.copytree(CLAIMS_DIR, directory, dirs_exist_ok=True)
  for source_key, (root, position) in TREES.items():
    claims = _claims(root, position, source_key)
    (directory / f'{source_key}.jsonl').write_text(''.join(json.dumps(c) + '\n' for c in claims))
  return ClaimStore(directory)


def _lines(block):
  return block['rendered'].splitlines()


def test_contents_with_the_type_also_a_child(synthetic):
  [block] = synthetic.contents('1961_dehm', GENUS)
  assert _lines(block) == [
    'Dehm 1961',
    '  Genus Edrioaster',
    '    Type species. Cyclaster bigsbyi, by monotypy',
    '    Edrioaster bigsbyi',
    '    Edrioaster priscus',
  ]
  [node] = [n for n in block['nodes'] if n.get('typeSpecies')]
  assert node['typeSpecies']['claim'] == '1961_dehm:320/type:act'
  assert '1961_dehm:320/type:act' in block['claims']


def test_contents_with_the_synonymy_puts_the_type_line_where_it_was(synthetic):
  [block] = synthetic.contents('1961_dehm', GENUS, synonymy=True)
  lines = _lines(block)
  assert lines[1:3] == ['  Genus Edrioaster', '    = 1857 Cyclaster Billings 1857']
  assert lines[3:] == [
    '    Type species. Cyclaster bigsbyi, by monotypy',
    '    Edrioaster bigsbyi',
    '    Edrioaster priscus',
  ]


def test_contents_with_the_type_no_child_node(synthetic):
  [block] = synthetic.contents('1985_jell_burrett_banks', GENUS, synonymy=True)
  assert _lines(block) == [
    'Jell et al. 1985',
    '  Genus Edrioaster',
    '    = 1857 Cyclaster Billings 1857',
    '    Type species. Cyclaster bigsbyi, by monotypy',
    '    Edrioaster priscus',
  ]
  # The type is no child line: the unlisted placement is not a child.
  assert [n['key'] for n in block['nodes']] == [GENUS, PRIORITY]


def test_contents_with_a_type_genus_under_a_family(synthetic):
  [block] = synthetic.contents('1985_jell_burrett_banks', FAMILY)
  assert _lines(block) == [
    'Jell et al. 1985',
    '  Family Edrioasteridae',
    '    Type genus. Edrioaster, by original designation',
    '    Genus Edrioaster',
    '      Type species. Cyclaster bigsbyi, by monotypy',
    '      Edrioaster priscus',
  ]


def test_contents_with_the_old_form_in_both_shapes(synthetic):
  [block] = synthetic.contents('1935_bassler', FAMILY)
  assert _lines(block) == [
    'Bassler 1935',
    '  Family Edrioasteridae',
    '    Type genus. Edrioaster',
    '    Genus Edrioaster',
    '      Type species. Edrioaster bigsbyi',
    '      Edrioaster bigsbyi',
    '    Genus Cyclaster',
  ]


def test_the_type_line_follows_the_types_rank(synthetic):
  words = synthetic.words
  assert words.type_noun(BIGSBYI) == 'type species'
  assert words.type_noun(GENUS) == 'type genus'
  assert words.type_noun('agelacrinus-subgenus_carneyella') == 'type genus'
  assert words.type_noun(FAMILY) == 'type'
  assert words.type_noun('agelacrinitinae') == 'type'


def test_contents_with_the_method_fixed_by_a_later_work(synthetic):
  [block] = synthetic.contents('1891_bell.f.j', GENUS)
  assert _lines(block)[2] == (
    '    Type species. Cyclaster bigsbyi, by subsequent designation (Bather 1899, p. 12)'
  )


def test_contents_marks_an_inferred_statement_or_method(synthetic):
  [whole] = synthetic.contents('1899_bather', GENUS)
  assert _lines(whole)[2] == '    Type species. Cyclaster bigsbyi, by monotypy (editor)'
  [method] = synthetic.contents('1899_bather', 'cyclaster')
  assert _lines(method)[2] == '    Type species. Cyclaster priscus, by monotypy (method: editor)'
  assert method['nodes'][0]['typeSpecies']['methodInferred'] is True
  assert not whole['nodes'][0]['typeSpecies'].get('methodInferred')


def test_the_type_line_reads_the_combination_under_a_subgenus(synthetic):
  [block] = synthetic.contents('1927_jaekel', 'agelacrinus-subgenus_carneyella')
  assert 'Type species. Carneyella (Agelacrinus) bigsbyi' in block['rendered']
  # Cited with no genus of its own the type reads under the genus and the
  # subgenus it types.
  assert (
    synthetic.words.display(BIGSBYI, '1927_jaekel', '324/children/0/type')
    == 'Carneyella (Agelacrinus) bigsbyi'
  )


def test_the_words_of_a_type_act(synthetic):
  def act(source, path):
    return next(
      c for c in synthetic.at_path[source][path] if c['kind'] == 'act' and c['actKind'] == 'type'
    )

  words = synthetic.words
  assert words.act_words(act('1961_dehm', '320/type')) == 'type species of Edrioaster, by monotypy'
  assert words.act_words(act('1891_bell.f.j', '322/children/0/type')) == (
    'type species of Edrioaster, by subsequent designation (Bather 1899, p. 12)'
  )
  assert words.act_words(act('1985_jell_burrett_banks', '321/children/0/type')) == (
    'type genus of Edrioasteridae, by original designation'
  )
  assert words.act_words(act('1899_bather', '323/children/0/type')) == (
    'type species of Edrioaster, by monotypy (inferred by the editor: the only species listed)'
  )
  assert words.act_words(act('1899_bather', '323/children/1/type')) == (
    'type species of Cyclaster, by monotypy (method inferred by the editor)'
  )
  # The old form: no `typeOf`, and the noun follows the rank.
  assert words.act_words(act('1935_bassler', '325/children/0')) == 'type genus'
  assert words.act_words(act('1935_bassler', '325/children/0/children/0')) == 'type species'


def test_each_fixation_has_its_words(synthetic):
  words = synthetic.words
  claim = {'kind': 'act', 'actKind': 'type', 'subject': BIGSBYI, 'typeOf': GENUS}
  claim |= {'source': '1961_dehm', 'path': '320/type'}
  assert {
    fixation: words.act_words({**claim, 'fixation': fixation})
    for fixation in (
      'originalDesignation',
      'monotypy',
      'subsequentDesignation',
      'subsequentMonotypy',
      'objectiveSynonymy',
      'tautonymy',
      'typus',
      'iczn',
    )
  } == {
    'originalDesignation': 'type species of Edrioaster, by original designation',
    'monotypy': 'type species of Edrioaster, by monotypy',
    'subsequentDesignation': 'type species of Edrioaster, by subsequent designation',
    'subsequentMonotypy': 'type species of Edrioaster, by subsequent monotypy',
    'objectiveSynonymy': 'type species of Edrioaster, by objective synonymy',
    'tautonymy': 'type species of Edrioaster, by tautonymy',
    'typus': 'type species of Edrioaster, by its name ("typus" or "typicus")',
    'iczn': 'type species of Edrioaster, by ruling of the ICZN',
  }
  assert words.act_words(claim) == 'type species of Edrioaster'


def test_the_type_marks(synthetic):
  words = synthetic.words
  assert words.type_mark(BIGSBYI) == '(named as the type species; not listed among the species)'
  assert words.type_mark(GENUS) == '(named as the type genus; not listed among the genera)'
  assert words.type_mark(FAMILY) == '(named as the type; not listed)'


def test_combination_at_a_type_node(synthetic):
  combination = synthetic.words.combination
  # The combination the source cites: the genus in `parents`, never the
  # genus the type is placed under.
  assert combination('1961_dehm', '320/type')['label'] == 'Cyclaster bigsbyi'
  assert combination('1985_jell_burrett_banks', '321/children/0/children/0/type')['label'] == (
    'Cyclaster bigsbyi'
  )
  assert combination('1891_bell.f.j', '322/children/0/type')['genus'] == CYCLASTER
  # A type genus prints by its name.
  assert combination('1985_jell_burrett_banks', '321/children/0/type')['label'] == 'Edrioaster'
  # No `parents`: the genus it types.
  assert synthetic.words.display(BIGSBYI, '1927_jaekel', '324/children/0/type') == (
    'Carneyella (Agelacrinus) bigsbyi'
  )
  # The child is under the genus it is placed in.
  assert combination('1961_dehm', '320/children/0')['label'] == 'Edrioaster bigsbyi'


def test_descendants_lists_the_unlisted_type_once_with_the_mark(synthetic):
  block = synthetic.descendants([GENUS], include_synonyms=False, include_variants=False)
  rows = {row['combination']: row for row in block['rows'] if row['record'] == BIGSBYI}
  # The cited combination is a row of its own, apart from the listed one.
  unlisted = rows['Cyclaster bigsbyi']
  vias = [v['value'] for v in unlisted['cells'][2]]
  mark = '(named as the type species; not listed among the species)'
  assert f'Jell et al. 1985: under Edrioaster {mark}' in vias
  # Each source that names it only as the type is marked, once; the paper
  # that cites the genus Cyclaster is not.
  assert [v for v in vias if mark in v] == [
    f'Bell 1891: under Edrioaster {mark}',
    f'Bather 1899: under Edrioaster {mark}',
    f'Jell et al. 1985: under Edrioaster {mark}',
  ]
  # Under the cited combination once. A type cited with no genus reads in
  # the genus it types, as the child would, and only its own line is marked.
  assert [r['combination'] for r in block['rows'] if r['record'] == BIGSBYI].count(
    'Cyclaster bigsbyi'
  ) == 1
  plain = [v['value'] for v in rows['Edrioaster bigsbyi']['cells'][2]]
  assert [v for v in plain if mark in v] == [f'Bassler 1936: under Edrioaster {mark}']
  assert 'Dehm 1961: under Edrioaster' in plain


def test_descendants_lists_the_listed_type_once_without_the_mark(synthetic):
  block = synthetic.descendants([GENUS], include_synonyms=False, include_variants=False)
  [row] = [r for r in block['rows'] if r['combination'] == 'Edrioaster bigsbyi']
  vias = [v['value'] for v in row['cells'][2]]
  assert 'Dehm 1961: under Edrioaster' in vias
  assert 'Bassler 1935: under Edrioaster' in vias
  # The only marked line is the paper that names it only as the type, and
  # cites it with no genus of its own.
  assert [v for v in vias if 'named as the type' in v] == [
    'Bassler 1936: under Edrioaster (named as the type species; not listed among the species)'
  ]
  # The family's type genus, listed as a child, is one row with no mark.
  family = synthetic.descendants([FAMILY], include_synonyms=False, include_variants=False)
  [genus] = [r for r in family['rows'] if r['record'] == GENUS]
  assert not any('named as the type' in v['value'] for v in genus['cells'][2])


def test_closure_descendants_say_which_placement_rests_on_the_type(synthetic):
  found = synthetic.closure.descendants([GENUS], include_synonyms=False, include_variants=False)
  [via] = [v for v in found[BIGSBYI] if v['source'] == '1985_jell_burrett_banks']
  assert via['via'] == 'type' and via['parent'] == GENUS
  assert via['claim'] == '1985_jell_burrett_banks:321/children/0/children/0/type:placement'
  assert not any(v.get('via') for v in found[BIGSBYI] if v['source'] == '1961_dehm')
  assert not any('via' in v for v in found[PRIORITY])


def test_ancestors_of_the_unlisted_type_run_up_through_the_genus_to_the_root(synthetic):
  block = synthetic.ancestors([BIGSBYI], include_variants=False)
  [line] = [e for e in block['entries'] if e['source'] == '1985_jell_burrett_banks']
  assert [n['key'] for n in line['chain']] == [
    'echinodermata',
    FAMILY,
    GENUS,
    BIGSBYI,
  ]
  assert [n['label'] for n in line['chain']] == [
    'Echinodermata',
    'Edrioasteridae',
    'Edrioaster',
    'Cyclaster bigsbyi',
  ]
  assert [n.get('via') for n in line['chain']] == [None, None, None, 'type']
  assert (
    'Edrioasteridae › Edrioaster › Cyclaster bigsbyi (named as the type species;'
    in (block['rendered'])
  )
  # The chain above a listed type carries no mark.
  [listed] = [e for e in block['entries'] if e['source'] == '1961_dehm']
  assert not any(n.get('via') for n in listed['chain'])


def test_closure_chains_and_ancestors_name_the_via(synthetic):
  closure = synthetic.closure
  [chain] = [c for c in closure.chains_of(BIGSBYI) if c['source'] == '1985_jell_burrett_banks']
  assert [(n['key'], n.get('via')) for n in chain['nodes']] == [
    ('echinodermata', None),
    (FAMILY, None),
    (GENUS, None),
    (BIGSBYI, 'type'),
  ]
  above = closure.ancestors([BIGSBYI], include_variants=False)
  [first] = [v for v in above[GENUS] if v['source'] == '1985_jell_burrett_banks']
  assert first['via'] == 'type' and first['depth'] == 1
  [second] = [v for v in above[FAMILY] if v['source'] == '1985_jell_burrett_banks']
  assert 'via' not in second and second['depth'] == 2


def test_a_type_on_the_root_has_the_root_for_its_chain(synthetic):
  # The root has a usage claim and no placement: the chain stops there, at
  # the path without the `/type`.
  closure = synthetic.closure
  [chain] = [c for c in closure.chains_of(BIGSBYI) if c['source'] == '1936_bassler']
  assert [(n['key'], n['path'], n.get('via')) for n in chain['nodes']] == [
    (GENUS, '326', None),
    (BIGSBYI, '326/type', 'type'),
  ]
  assert chain['nodes'][0]['claim'] == '1936_bassler:326:usage'
  placement = synthetic.by_id['1936_bassler:326/type:placement']
  assert closure.parent_path(placement) == '326'
  assert closure.parent_claim('1936_bassler', placement) is None
  assert closure.parent_path({'path': '1/children/2/children/3'}) == '1/children/2'
  assert closure.parent_claim('1936_bassler', {'path': '326'}) is None
  rendered = synthetic.ancestors([BIGSBYI], include_variants=False)['rendered']
  assert (
    '1936  Bassler      Edrioaster › Edrioaster bigsbyi '
    '(named as the type species; not listed among the species)'
  ) in rendered


def test_placed_under_the_family_runs_through_the_genus(synthetic):
  block = synthetic.placed_under(BIGSBYI, FAMILY, include_variants=False)
  [line] = [e for e in block['entries'] if e['source'] == '1985_jell_burrett_banks']
  assert [n['key'] for n in line['chain']] == [GENUS, BIGSBYI]
  assert line['chain'][-1]['mark'] == ('(named as the type species; not listed among the species)')
  assert 'Edrioaster › Cyclaster bigsbyi (named as the type species' in block['rendered']


def test_history_of_the_unlisted_type_shows_the_marked_line(synthetic):
  block = synthetic.history(BIGSBYI, include_related=False)
  [entry] = [e for e in block['entries'] if e['source'] == '1985_jell_burrett_banks']
  assert entry['line'] == (
    'Cyclaster bigsbyi, in Edrioaster; type species of Edrioaster, by monotypy '
    '(named as the type species; not listed among the species)'
  )
  assert '1985_jell_burrett_banks:321/children/0/children/0/type:act' in entry['claims']
  # The listed type is the child's own line, with the statement the genus
  # carries and no mark.
  [listed] = [e for e in block['entries'] if e['source'] == '1961_dehm']
  assert listed['line'] == 'Edrioaster bigsbyi; type species of Edrioaster, by monotypy'
  assert '1961_dehm:320/type:act' in listed['claims']
  assert 'named as the type' in block['rendered']
  # The sources that list the type as a child, or only name its genus,
  # carry no mark.
  assert not any(
    'named as the type' in e['line']
    for e in block['entries']
    if e['source'] in ('1961_dehm', '1935_bassler')
  )


def test_history_shows_a_type_cited_only_under_a_synonym_genus(synthetic):
  # Bassler 1936 cites it as the type of the synonym genus: a use of the
  # name in the combination the entry gives, with nothing to place it by.
  # It also lists the name as a synonym, and that line stays.
  block = synthetic.history(PRIORITY, include_related=False)
  lines = [e['line'] for e in block['entries'] if e['source'] == '1936_bassler']
  assert sorted(lines) == [
    'Cyclaster priscus; type species of Cyclaster, by subsequent monotypy',
    'priscus, cited as a synonym of Edrioaster',
  ]
  claims = _by_path(synthetic.by_source['1936_bassler'])['326/synonyms/0/type']
  assert not _of_kind(claims, 'placement')


def test_placements_of_the_type_show_the_marked_row(synthetic):
  block = synthetic.placements([BIGSBYI], include_variants=False)
  mark = '(named as the type species; not listed among the species)'
  sources = [c.get('source') for c in block['columns']]
  [row] = [r for r in block['rows'] if r['combination'] == 'Cyclaster bigsbyi']
  cells = {s: c for s, c in zip(sources, row['cells'], strict=True) if s}
  # Named only as the type: Edrioaster, marked, resting on the `type` node;
  # the paper that placed it under Cyclaster itself has no mark.
  [value] = cells['1985_jell_burrett_banks']
  assert value['value'] == f'Edrioaster {mark}'
  assert value['claim'] == '1985_jell_burrett_banks:321/children/0/children/0/type:placement'
  assert [v['value'] for v in cells['1857_billings']] == ['Cyclaster']
  assert f'Edrioaster {mark}' in block['rendered']
  # The listed child is a row of its own, and its cells carry no mark except
  # for the paper that names the type only (Bassler 1936, no genus given).
  [listed] = [r for r in block['rows'] if r['combination'] == 'Edrioaster bigsbyi']
  listed_cells = {s: c for s, c in zip(sources, listed['cells'], strict=True) if s}
  assert [v['value'] for v in listed_cells['1961_dehm']] == ['Edrioaster']
  assert [v['value'] for v in listed_cells['1936_bassler']] == [f'Edrioaster {mark}']


def test_the_schemes_and_the_trajectory_carry_the_mark(synthetic):
  mark = '(named as the type species; not listed among the species)'
  schemes = synthetic.closure.schemes([BIGSBYI], include_variants=False)
  entries = {e['source']: e for s in schemes for e in s['entries']}
  assert entries['1985_jell_burrett_banks']['via'] == 'type'
  assert 'via' not in entries['1961_dehm']
  # A scheme that rests on the listed papers too is not marked.
  by_parent = {s['parents'][0]['key']: s for s in schemes}
  assert not any(mark in line for line in synthetic.words.scheme_lines([by_parent[GENUS]]))
  # A scheme every paper of which names the record only as the type is.
  only = {**by_parent[GENUS], 'entries': [e for e in by_parent[GENUS]['entries'] if e.get('via')]}
  assert synthetic.words.scheme_lines([only])[0].endswith(mark)
  assert synthetic.words.position_lines({'positions': [only], 'sources': ['x']}).endswith(mark)
  # The header of `placements` says so for a scheme of the type papers alone.
  lines = synthetic.placements([BIGSBYI])['decorations']['schemes']
  assert [line.endswith(mark) for line in lines] == [False, True, False]
  assert lines[1].startswith('Carneyella (Agelacrinus): 1 paper (1927)')


def test_statements_of_the_type_include_the_act_line(synthetic):
  block = synthetic.statements(BIGSBYI, source='1985_jell_burrett_banks')
  sentences = [e['sentence'] for e in block['entries']]
  assert 'type species of Edrioaster, by monotypy' in sentences
  assert 'places it under Edrioaster' in sentences
  block = synthetic.statements(BIGSBYI, source='1961_dehm', act_kind='type')
  assert [e['sentence'] for e in block['entries']] == ['type species of Edrioaster, by monotypy']
  # The cited name reads in the combination the source cites.
  assert block['entries'][0].get('name') in (None, 'Cyclaster bigsbyi')


def test_printed_forms_of_a_type_does_not_fail(synthetic):
  claims = _claims(
    {
      'taxon': GENUS,
      'type': {
        'taxon': BIGSBYI,
        'parents': [{'taxon': CYCLASTER}],
        'citedAs': 'Cyclaster bigsbyi, Billings, 1857, Canad. Nat.',
        'authority': {'source': '1857_billings', 'pages': 293},
      },
      'children': [],
    },
    332,
    '1927_jaekel',
  )
  assert any(c.get('printed') for c in claims if c['path'] == '332/type')
  block = synthetic.printed_forms(BIGSBYI)
  assert block['rendered']
  block = synthetic.printed_forms(BIGSBYI, source='1985_jell_burrett_banks')
  assert block['kind'] == 'printedForms'


def test_the_original_combination_reads_from_a_type_nodes_parents(synthetic):
  # A type cited with a genus is a combination the corpus knows the name in.
  assert synthetic.words.original_combination(BIGSBYI) == 'Cyclaster bigsbyi'


def test_a_name_the_source_cites_as_a_type_is_not_a_primary_node(synthetic):
  # `contents` finds no node of its own for the type, and the type is no
  # synonym of the genus it types.
  assert synthetic.contents('1985_jell_burrett_banks', BIGSBYI) == []
  [block] = synthetic.synonymy(GENUS, source='1985_jell_burrett_banks')
  assert [e['record'] for e in block['entries']] == [CYCLASTER]
  accepted = synthetic.closure.accepted_under
  assert not any(
    c['source'] == '1985_jell_burrett_banks' and c['subject'] == BIGSBYI
    for c in accepted.get(GENUS, ())
  )
  assert not any(
    c['kind'] == 'acceptance' and c['subject'] == BIGSBYI
    for c in synthetic.by_source['1985_jell_burrett_banks']
  )


def test_combinations_of_the_type_include_the_cited_one_only_when_placed(synthetic):
  labels = {c['label'] for c in synthetic.words.combinations(BIGSBYI)}
  assert {'Edrioaster bigsbyi', 'Cyclaster bigsbyi'} <= labels
  # A cited combination that places nothing (a type of a synonym genus) is
  # no combination of the name.
  assert not [c for c in synthetic.closure.placements_of[PRIORITY] if c['source'] == '1936_bassler']
  assert [c['key'] for c in synthetic.resolve_name('Cyclaster bigsbyi')] == [BIGSBYI]


def test_the_tool_descriptions_name_the_marked_type():
  from phylohist.tools import TOOL_DESCRIPTIONS

  assert 'named only as the type' in TOOL_DESCRIPTIONS['descendants']


# -- the real corpus ----------------------------------------------------------


def test_the_corpus_lines_are_unmarked_and_rank_worded(store):
  checked = 0
  roots = sorted(
    {
      (c['source'], c['subject'])
      for claims in store.by_source.values()
      for c in claims
      if c['kind'] == 'usage' and c['axis'] == 'root' and c['subject']
    }
  )
  for source, record in roots:
    for block in store.contents(source, record):
      assert '(named as the type' not in block['rendered']
      for node in block['nodes']:
        line = node.get('typeSpecies')
        if not line:
          continue
        checked += 1
        rank = store._rank_of(line['key'])
        word = (
          'Type species'
          if rank in ('species', 'subspecies', 'variety')
          else 'Type genus'
          if rank in ('genus', 'subgenus')
          else 'Type'
        )
        assert line['word'] == word
        assert f'{word}. {line["label"]}' + (' (editor)' if line['inferred'] else '') in [
          ln.strip().lstrip('?').strip() for ln in block['rendered'].splitlines()
        ]
        # No data uses the `type` node yet: no method, no placement of its kind.
        assert 'method' not in line
  assert checked > 300
  assert not [c for claims in store.by_source.values() for c in claims if c.get('via') == 'type']


def test_the_corpus_type_genera_now_read_type_genus(store):
  words = {
    (c['source'], c['path']): store.words.type_noun(c['subject'])
    for claims in store.by_source.values()
    for c in claims
    if c['kind'] == 'act' and c['actKind'] == 'type' and '/children/' in c['path']
  }
  assert words[('2010_müller.p_hahn', '0/children/1/children/1')] == 'type'
  assert words[('2010_müller.p_hahn', '0/children/0/children/0')] == 'type genus'
  assert words[('1844_buch', '0/children/1/children/0')] == 'type genus'


def test_a_paper_that_names_the_type_only_counts_among_the_papers(synthetic):
  measured = synthetic.closure.measurement(BIGSBYI, include_related=False)
  assert '1985_jell_burrett_banks' in measured['sources']
  assert '1961_dehm' in measured['sources']


# -- `type: null` and the derived `types` coverage ------------------------------

SUBGENUS_KEY = 'agelacrinus-subgenus_carneyella'
PLACEHOLDER = 'agelacrinitidae-uncertain-genus_bell.b.m_1976'
NULL_TYPE_SOURCE = '1927_jaekel'


def test_schema_accepts_a_null_type_and_unused_type():
  assert _valid(_tree({'type': None}))
  assert _valid({'unused': ['type'], 'taxonomies': [{'taxon': GENUS}]})
  assert not _valid({'unused': ['types'], 'taxonomies': [{'taxon': GENUS}]})


def test_type_null_is_no_error_on_a_primary_node():
  assert nomenclature.type_node({'taxon': GENUS, 'type': None}, is_cited=False) == []
  node = {'taxon': GENUS, 'type': None, 'children': [{'taxon': BIGSBYI, 'isType': False}]}
  assert nomenclature.type_node(node, is_cited=False) == []


def test_type_null_on_a_cited_entry_is_an_error():
  assert nomenclature.type_node({'taxon': CYCLASTER, 'type': None}, is_cited=True) == [
    ('error', 'cited entry carries `type: null`'),
  ]
  # A type node on a cited entry is allowed, as before.
  node = {'taxon': CYCLASTER, 'type': {'taxon': BIGSBYI}}
  assert nomenclature.type_node(node, is_cited=True) == []


def test_type_null_beside_a_child_marked_is_type_is_an_error():
  node = {'taxon': GENUS, 'type': None, 'children': [{'taxon': BIGSBYI, 'isType': True}]}
  assert nomenclature.type_node(node, is_cited=False) == [
    ('error', '`type: null` beside a child marked `isType`'),
  ]
  assert len(nomenclature.type_node(node, is_cited=True)) == 2


def test_load_reports_a_null_type_with_the_nodes_path(load_records, caplog):
  data = {
    'trees': {
      'src1': {
        'taxonomies': [
          {
            'taxon': FAMILY,
            'children': [
              {'taxon': GENUS, 'type': None},
              {
                'taxon': 'cyclaster',
                'type': None,
                'children': [{'taxon': BIGSBYI, 'isType': True}],
              },
              {'taxon': 'carneyella', 'synonyms': [{'taxon': CYCLASTER, 'type': None}]},
            ],
          }
        ],
      },
    },
  }
  with caplog.at_level(logging.WARNING, logger='phylohist'):
    _report_nomenclature(data)
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert any(
    'src1 at 0/children/1: `type: null` beside a child marked `isType`' in m for m in errors
  )
  assert any(
    'src1 at 0/children/2/synonyms/0: cited entry carries `type: null`' in m for m in errors
  )
  assert len(errors) == 2


def test_a_species_level_name_cannot_carry_a_null_type_either(load_records, caplog):
  root = {'taxon': BIGSBYI, 'type': None}
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    Tree(root, {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 950})
  [error] = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert 'carries `type` but is a species-level name; its type is a specimen' in error


def test_a_genus_may_carry_a_null_type_and_places_nothing(load_records, caplog):
  root = {'taxon': FAMILY, 'children': [{'taxon': GENUS, 'type': None}]}
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    tree = Tree(root, {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 951})
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  [node] = [n for n in tree.walk() if n.taxon is not None and n.taxon.key == GENUS]
  assert node.related_node('type') is None


@pytest.mark.parametrize(
  'node',
  [
    {'taxon': GENUS, 'type': {'taxon': BIGSBYI}},
    {'taxon': GENUS, 'type': None},
    {'taxon': GENUS, 'synonyms': [{'taxon': CYCLASTER, 'type': {'taxon': BIGSBYI}}]},
    {'taxon': GENUS, 'synonyms': [{'taxon': CYCLASTER, 'type': None}]},
  ],
)
def test_unused_type_beside_a_type_node_or_a_null_is_an_error(node):
  [(level, message)] = material.unused_fields({'unused': ['type'], 'taxonomies': [node]})
  assert level == 'error'
  assert message.startswith('`type` is listed as `unused` but appears at 0')


def test_unused_type_beside_an_is_type_child_is_an_error():
  document = {
    'unused': ['type'],
    'taxonomies': [
      {'taxon': GENUS, 'children': [{'taxon': PRIORITY}, {'taxon': BIGSBYI, 'isType': True}]}
    ],
  }
  assert material.unused_fields(document) == [
    ('error', '`type` is listed as `unused` but a child at 0/children/1 is marked `isType`'),
  ]
  # Another field's `unused` says nothing of the flag; a clean file is quiet.
  assert material.unused_fields({**document, 'unused': ['synonyms']}) == []
  clean = {'unused': ['type'], 'taxonomies': [{'taxon': GENUS, 'children': [{'taxon': BIGSBYI}]}]}
  assert material.unused_fields(clean) == []


def test_check_draft_rejects_a_null_type(tmp_path):
  result = _draft(tmp_path, '  - taxon: pyrgocystis\n    type: null\n')
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'children/0: draft carries `type: null`; only an auditor sets nulls' in result.stdout


def test_check_draft_reports_a_null_type_on_a_cited_entry(tmp_path):
  result = _draft(
    tmp_path,
    '  - taxon: pyrgocystis\n    synonyms:\n    - taxon: grayae_bather_1915\n      type: null\n',
  )
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'cited entry carries `type: null`' in result.stdout


def test_a_cited_entry_may_still_carry_a_type_node_in_a_draft(tmp_path):
  result = _draft(
    tmp_path,
    '  - taxon: pyrgocystis\n'
    '    synonyms:\n'
    '    - taxon: grayae_bather_1915\n'
    '      type:\n'
    '        taxon: sardesoni_bather_1915\n',
  )
  assert result.returncode == 0, result.stdout + result.stderr


# -- derived `types` coverage ----------------------------------------------------

_BASE = {'source_key': '1961_dehm', 'type': 'taxonomy'}
_TYPE = {'taxon': BIGSBYI}


def _derived(node, position, file_unused=(), tree_type='taxonomy'):
  root = Tree(node, {**_BASE, 'type': tree_type, 'position': position, 'file_unused': file_unused})
  return derived_coverage({'s': [root]})['s']['types']


def _family(*genera):
  return {'taxon': FAMILY, 'children': list(genera)}


def test_types_coverage_declares_nothing_without_a_null():
  assert _derived(_family({'taxon': GENUS, 'type': _TYPE}), 960) is None
  assert _derived(_family({'taxon': GENUS}), 961) is None
  assert _derived(_family({'taxon': GENUS, 'children': [{**_TYPE, 'isType': True}]}), 962) is None


def test_types_coverage_all_when_every_genus_states_a_type_or_a_null():
  family = _family(
    {'taxon': GENUS, 'type': _TYPE},
    {'taxon': 'cyclaster', 'type': None},
    {'taxon': 'carneyella', 'children': [{'taxon': PRIORITY, 'isType': True}]},
  )
  assert _derived(family, 963) == 'all'


def test_types_coverage_partly_when_a_genus_has_none():
  family = _family({'taxon': GENUS, 'type': None}, {'taxon': 'cyclaster', 'children': []})
  assert _derived(family, 964) == 'partly'
  # A child that is not marked `isType` is no statement.
  family = _family(
    {'taxon': GENUS, 'type': None},
    {'taxon': 'cyclaster', 'children': [{'taxon': PRIORITY, 'isType': False}]},
  )
  assert _derived(family, 965) == 'partly'


def test_types_coverage_na_when_unused_lists_type():
  family = _family({'taxon': GENUS, 'type': None})
  assert _derived(family, 966, file_unused=('type',)) == 'na'
  assert _derived(_family({'taxon': GENUS}), 967, file_unused=('type',)) == 'na'
  assert _derived(_family({'taxon': GENUS}), 968, file_unused=('synonyms',)) is None


def test_a_family_without_a_type_is_not_counted():
  genus = {'taxon': GENUS, 'type': None}
  assert _derived({'taxon': FAMILY, 'children': [genus]}, 969) == 'all'
  # A family's own type, a node or a null, is written and not counted.
  assert _derived({'taxon': FAMILY, 'type': {'taxon': GENUS}, 'children': [genus]}, 970) == 'all'
  assert _derived({'taxon': FAMILY, 'type': None, 'children': []}, 971) is None


def test_a_placeholder_genus_is_not_counted():
  family = _family({'taxon': GENUS, 'type': None}, {'taxon': PLACEHOLDER})
  assert _derived(family, 972) == 'all'


def test_a_subgenus_is_counted():
  family = _family(
    {'taxon': 'carneyella', 'type': None, 'children': [{'taxon': SUBGENUS_KEY}]},
  )
  assert _derived(family, 973) == 'partly'
  family = _family(
    {'taxon': 'carneyella', 'type': None, 'children': [{'taxon': SUBGENUS_KEY, 'type': _TYPE}]}
  )
  assert _derived(family, 974) == 'all'


def test_a_species_is_not_counted_and_a_cladogram_contributes_nothing():
  family = _family(
    {'taxon': GENUS, 'type': None, 'children': [{'taxon': BIGSBYI}, {'taxon': PRIORITY}]}
  )
  assert _derived(family, 975) == 'all'
  assert _derived(family, 976, tree_type='cladogram') is None


def test_a_null_type_is_an_absence_claim():
  root = {'taxon': FAMILY, 'children': [{'taxon': GENUS, 'type': None}]}
  claims = _claims(root, 977, '1961_dehm')
  [absence] = _of_kind(claims, 'absence')
  assert absence['absenceOf'] == 'types'
  assert absence['fields'] == ['type']
  assert absence['path'] == '977/children/0'
  assert absence['subject'] == GENUS
  assert not _of_kind(claims, 'act')
  # The words of an absence say what the null says.
  assert ABSENCE_WORDS['types'] == 'no type stated'
  # A type node, or a node with no `type`, is no absence.
  assert not _of_kind(_claims({'taxon': GENUS, 'type': _TYPE}, 978, '1961_dehm'), 'absence')
  assert not _of_kind(_claims({'taxon': GENUS}, 979, '1961_dehm'), 'absence')


def test_a_null_type_is_the_last_of_a_nodes_absences():
  node = {'taxon': BIGSBYI, 'synonyms': None, 'material': None}
  claims = _claims(
    {'taxon': GENUS, **{k: v for k, v in node.items() if k != 'taxon'}}, 980, '1961_dehm'
  )
  assert [c['absenceOf'] for c in _of_kind(claims, 'absence')] == ['material', 'synonymy']
  claims = _claims({'taxon': GENUS, 'synonyms': None, 'type': None}, 981, '1961_dehm')
  assert [c['absenceOf'] for c in _of_kind(claims, 'absence')] == ['synonymy', 'types']


def _manifest_entry(values):
  entry = manifest(extract(values), values)['sources']['1961_dehm']
  return entry


def test_manifest_types_declared_beside_a_derived_value_is_inconsistent(monkeypatch):
  from phylohist.loader.research import Source

  coverage = Source.get('1961_dehm')._data['audit']['coverage']
  monkeypatch.setitem(coverage, 'types', 'all')
  values = {
    '1961_dehm': [
      Tree(
        _family({'taxon': GENUS, 'type': None}, {'taxon': 'cyclaster'}),
        {**_BASE, 'position': 982},
      )
    ]
  }
  entry = _manifest_entry(values)
  assert entry['derivedCoverage']['types'] == 'partly'
  assert entry['coverage']['types'] == 'partly'
  assert (
    'types: declared all but derived from the tree (partly); remove the declaration'
    in (entry['inconsistencies'])
  )
  assert not [r for r in entry['inconsistencies'] if r.startswith('types: declared all, no')]


def test_manifest_types_keeps_the_claim_count_check_for_a_source_that_derives_nothing(
  monkeypatch,
):
  from phylohist.loader.research import Source

  coverage = Source.get('1961_dehm')._data['audit']['coverage']
  # Declared, nothing written and no type claim: the check fires, as for `synonymy`.
  monkeypatch.setitem(coverage, 'types', 'all')
  values = {'1961_dehm': [Tree(_family({'taxon': GENUS}), {**_BASE, 'position': 983})]}
  entry = _manifest_entry(values)
  assert entry['derivedCoverage']['types'] is None
  assert entry['coverage']['types'] == 'all'
  assert 'types: declared all, no claims derived' in entry['inconsistencies']
  # Declared none beside a type node: the other direction.
  monkeypatch.setitem(coverage, 'types', 'none')
  values = {
    '1961_dehm': [Tree(_family({'taxon': GENUS, 'type': _TYPE}), {**_BASE, 'position': 984})]
  }
  entry = _manifest_entry(values)
  assert any(r.startswith('types: declared none, ') for r in entry['inconsistencies'])


# -- the tools -------------------------------------------------------------------

# One source with a genus of each state, the old form, a family with a type
# node, a species, and a type null on a genus and on a subgenus.
NULLS = {
  'taxon': FAMILY,
  'type': {'taxon': GENUS},
  'children': [
    {'taxon': GENUS, 'type': _TYPE, 'children': [{'taxon': BIGSBYI}, {'taxon': PRIORITY}]},
    {'taxon': 'cyclaster', 'type': None, 'children': []},
    {'taxon': 'carneyella', 'children': [{'taxon': PRIORITY, 'isType': True}]},
    {'taxon': 'rhenopyrgus', 'children': [{'taxon': SUBGENUS_KEY, 'type': None}]},
    {'taxon': 'pyrgocystis', 'children': []},
    {'taxon': 'agelacrinitidae', 'children': []},
    {'taxon': 'agelacrinidae', 'type': None, 'children': []},
  ],
}


@pytest.fixture(scope='module')
def nulled(load_records, tmp_path_factory):
  """A `ClaimStore` over a copy of `claims/` with the claims of 1961 Dehm
  replaced by those of `NULLS`, its `types` coverage `partly`."""
  directory = tmp_path_factory.mktemp('claims_nulls')
  shutil.copytree(CLAIMS_DIR, directory, dirs_exist_ok=True)
  claims = _claims(NULLS, 985, '1961_dehm')
  (directory / '1961_dehm.jsonl').write_text(''.join(json.dumps(c) + '\n' for c in claims))
  store = ClaimStore(directory)
  store.sources['1961_dehm']['coverage'] = {
    **store.sources['1961_dehm']['coverage'],
    'types': 'partly',
  }
  return store


def _type_rows(block):
  """`{displayed group or record: (state, basis, count)}` of the type rows."""
  return [
    (
      node['path'],
      [(r['state'], r['basis'], r['count']) for r in node['rows'] if r['kind'] == 'type'],
    )
    for node in block['content']
  ]


def test_the_type_row_in_its_three_states(nulled):
  entered = nulled.statements(GENUS, source='1961_dehm', kind='absence')
  assert _type_rows(entered) == [('985/children/0', [('entered', 'claims', 1)])]
  [row] = [r for r in entered['rows'] if r['cells'][0][0]['value'] == 'type']
  assert row['cells'][1][0]['value'] == '1 entered'
  assert row['cells'][1][0]['claims'] == ['1961_dehm:985/children/0/type:act']

  null = nulled.statements('cyclaster', source='1961_dehm', kind='absence')
  [row] = [r for r in null['rows'] if r['cells'][0][0]['value'] == 'type']
  assert row['cells'][1][0]['value'] == 'none printed'
  assert row['cells'][1][0]['claims'] == ['1961_dehm:985/children/1:absence']
  assert _type_rows(null) == [('985/children/1', [('none', 'null', None)])]

  bare = nulled.statements('pyrgocystis', source='1961_dehm', kind='absence')
  [row] = [r for r in bare['rows'] if r['cells'][0][0]['value'] == 'type']
  assert row['cells'][1][0]['value'] == 'not entered'
  assert 'claims' not in row['cells'][1][0]
  assert _type_rows(bare) == [('985/children/4', [('notEntered', 'coverage', None)])]


@pytest.mark.parametrize('declared', ['all', 'na'])
def test_the_type_row_reads_coverage_where_nothing_is_entered(nulled, monkeypatch, declared):
  monkeypatch.setitem(nulled.sources['1961_dehm']['coverage'], 'types', declared)
  block = nulled.statements('pyrgocystis', source='1961_dehm', kind='absence')
  assert _type_rows(block) == [('985/children/4', [('none', 'coverage', None)])]
  [row] = [r for r in block['rows'] if r['cells'][0][0]['value'] == 'type']
  assert row['cells'][1][0]['value'] == 'none printed' and 'claims' not in row['cells'][1][0]


def test_the_type_row_reads_an_is_type_child_as_entered(nulled):
  block = nulled.statements('carneyella', source='1961_dehm', kind='absence')
  [(_, [(state, basis, count)])] = _type_rows(block)
  assert (state, basis, count) == ('entered', 'claims', 1)
  [row] = [r for r in block['rows'] if r['cells'][0][0]['value'] == 'type']
  [claim] = row['cells'][1][0]['claims']
  assert claim == '1961_dehm:985/children/2/children/0:act'


def test_the_type_row_of_a_subgenus_and_a_family(nulled):
  sub = nulled.statements(SUBGENUS_KEY, source='1961_dehm', kind='absence')
  assert _type_rows(sub) == [('985/children/3/children/0', [('none', 'null', None)])]
  family = nulled.statements(FAMILY, source='1961_dehm', kind='absence')
  assert _type_rows(family) == [('985', [('entered', 'claims', 1)])]


def test_no_type_row_for_a_species(nulled):
  block = nulled.statements(BIGSBYI, source='1961_dehm', kind='absence')
  assert 'type' not in [r['kind'] for node in block['content'] for r in node['rows']]


def test_the_type_row_appears_above_genus_only_when_there_is_something(nulled):
  # A family with neither a type statement nor a `types` absence has no
  # type row (and so no row at all here); a family's null is a row.
  bare = nulled.statements('agelacrinitidae', source='1961_dehm', kind='absence')
  assert 'type' not in [r['kind'] for node in bare['content'] for r in node['rows']]
  null = nulled.statements('agelacrinidae', source='1961_dehm', kind='absence')
  assert _type_rows(null) == [('985/children/6', [('none', 'null', None)])]


def test_statements_by_act_include_the_types_absence(nulled):
  block = nulled.statements('cyclaster', source='1961_dehm', kind='act')
  assert [e['sentence'] for e in block['entries']] == ['no type stated']
  assert block['entries'][0]['kind'] == 'absence'
  block = nulled.statements('cyclaster', source='1961_dehm', act_kind='type')
  assert [e['sentence'] for e in block['entries']] == ['no type stated']
  # Another act kind does not select it, and no kind selects it for a genus with a type.
  block = nulled.statements('cyclaster', source='1961_dehm', kind='act', act_kind='new')
  assert block['type'] == 'statement'
  block = nulled.statements(GENUS, source='1961_dehm', kind='act')
  assert 'no type stated' not in [e['sentence'] for e in block['entries']]
  # `absence` selects it too, and no other kind does.
  block = nulled.statements('cyclaster', kind='absence')
  assert [e['sentence'] for e in block['entries']] == ['no type stated']
  block = nulled.statements('cyclaster', source='1961_dehm', kind='placement')
  assert 'no type stated' not in [e['sentence'] for e in block['entries']]


def test_contents_prints_no_type_line_for_a_null_type(nulled):
  [block] = nulled.contents('1961_dehm', 'cyclaster')
  assert not [line for line in _lines(block) if 'ype' in line]


def test_the_absence_table_has_no_type_row_for_a_placeholder_genus(store):
  record = 'agelacrinitidae-uncertain-genus_bell.b.m_1976'
  block = store.statements(record, '1976_bell.b.m', kind='absence')
  assert [row['kind'] for row in block['content'][0]['rows']] == ['occurrences', 'synonymy']
