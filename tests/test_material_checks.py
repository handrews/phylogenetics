"""The material checks (`phylohist.loader.material`): prefix resolution,
context references, figure references, catalog numbers, nulls on a cited
entry, and the file-level `unused` list. Synthetic node dicts and
documents, one test per rule; a few exercise the loader's own wiring
(`load.py`) and `scripts/check_draft.py` end to end.
"""

import logging
import subprocess
import sys
from pathlib import Path

import pytest

from phylohist.loader import io, material
from phylohist.loader.taxa import Tree

SCRIPTS = Path(__file__).resolve().parent.parent / 'scripts'


@pytest.fixture(scope='module')
def repositories():
  return io.load_yaml(io.DATA_DIR / 'repositories.yaml')


# -- repository_of (4) -------------------------------------------------------


def test_repository_of_exact_key_match(repositories):
  assert material.repository_of('GM 9-5-2 165b', repositories) == ('GM', 'registry')


def test_repository_of_token_boundary_key_match(repositories):
  assert material.repository_of('USNM S-3965', repositories) == ('USNM', 'registry')


def test_repository_of_hyphenated_prefix(repositories):
  assert material.repository_of('PWL 2009/5016sub1-LS', repositories) == ('PWL', 'registry')


def test_repository_of_alias_match(repositories):
  assert material.repository_of('NHM UK EE15373', repositories) == ('NHMUK', 'alias')


def test_repository_of_source_abbreviation_wins(repositories):
  abbreviations = {'E': 'NHMUK'}
  assert material.repository_of('E23470', repositories, abbreviations) == ('NHMUK', 'source')


def test_repository_of_source_abbreviation_wins_other_prefix(repositories):
  abbreviations = {'EE': 'NHMUK'}
  assert material.repository_of('EE15752', repositories, abbreviations) == ('NHMUK', 'source')


def test_repository_of_longest_candidate_wins():
  # A registry where a shorter and a longer key both match at a token
  # boundary: the longer one wins.
  registry = {
    'GM': {'name': 'short', 'kind': 'institution'},
    'GM CO': {'name': 'long', 'kind': 'institution'},
  }
  assert material.repository_of('GM CO 12', registry) == ('GM CO', 'registry')


def test_repository_of_no_prefix(repositories):
  assert material.repository_of('12345', repositories) == (None, None)


def test_repository_of_unresolvable_prefix(repositories):
  assert material.repository_of('ZZZZ 12', repositories) == (None, None)


# -- context_refs -------------------------------------------------------------


def test_context_refs_missing_is_error():
  node = {'material': [{'label': 'A', 'context': 'nowhere'}]}
  assert material.context_refs(node, {}, {}) == [
    ('error', 'context "nowhere" is not defined on the node or the file'),
  ]


def test_context_refs_resolves_from_node_or_file_with_no_message():
  node_only = {'material': [{'label': 'A', 'context': 'here'}]}
  assert material.context_refs(node_only, {'here': {}}, {}) == []
  file_only = {'material': [{'label': 'A', 'context': 'there'}]}
  assert material.context_refs(file_only, {}, {'there': {}}) == []


def test_context_refs_node_key_shadows_file_key_is_warning():
  node = {'material': [{'label': 'A', 'context': 'here'}]}
  messages = material.context_refs(node, {'here': {}}, {'here': {}})
  assert messages == [('warning', 'context "here" on the node shadows a file-level context')]


def test_context_refs_object_form_and_no_context():
  node = {'material': [{'label': 'A', 'context': {'key': 'here', 'tentative': True}}, {'count': 1}]}
  assert material.context_refs(node, {'here': {}}, {}) == []


# -- unreferenced_file_contexts -----------------------------------------------


def test_unreferenced_file_contexts_empty_when_none_declared():
  assert material.unreferenced_file_contexts({'taxonomies': []}) == []


def test_unreferenced_file_contexts_warns_on_the_unused_one():
  document = {
    'contexts': {'used': {}, 'unused-one': {}},
    'taxonomies': [{'taxon': 'a', 'material': [{'label': 'A', 'context': 'used'}]}],
  }
  assert material.unreferenced_file_contexts(document) == [
    ('warning', 'context "unused-one" is defined but referenced by no material entry'),
  ]


def test_unreferenced_file_contexts_all_referenced_is_quiet():
  document = {
    'contexts': {'used': {}},
    'taxonomies': [{'taxon': 'a', 'material': [{'label': 'A', 'context': 'used'}]}],
  }
  assert material.unreferenced_file_contexts(document) == []


# -- figure_refs ---------------------------------------------------------------


def test_figure_refs_label_match_is_quiet():
  node = {'material': [{'label': 'A'}], 'figures': [{'plate': 1, 'of': 'A'}]}
  assert material.figure_refs(node) == []


def test_figure_refs_range_endpoint_matches():
  node = {
    'material': [{'catalogNumbers': [['GSC 1', 'GSC 5']]}],
    'figures': [{'plate': 1, 'of': 'GSC 5'}],
  }
  assert material.figure_refs(node) == []


def test_figure_refs_no_match_is_error():
  node = {'material': [{'label': 'A'}], 'figures': [{'plate': 1, 'of': 'B'}]}
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "B" matches 0 material entries, not 1'),
  ]


def test_figure_refs_several_matches_is_error():
  node = {
    'material': [{'label': 'A'}, {'catalogNumbers': ['A']}],
    'figures': [{'plate': 1, 'of': 'A'}],
  }
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "A" matches 2 material entries, not 1'),
  ]


def test_figure_refs_list_of_and_no_of_field():
  node = {
    'material': [{'label': 'A'}, {'label': 'B'}],
    'figures': [{'plate': 1, 'of': ['A', 'B']}, {'plate': 2}],
  }
  assert material.figure_refs(node) == []


# -- catalog_numbers ------------------------------------------------------------


def test_catalog_numbers_unresolved_is_warning(repositories):
  node = {'material': [{'catalogNumbers': ['ZZZZ 1']}]}
  assert material.catalog_numbers(node, repositories) == [
    ('warning', 'catalog number "ZZZZ 1" has no resolvable repository prefix'),
  ]


def test_catalog_numbers_resolved_is_quiet(repositories):
  node = {'material': [{'catalogNumbers': ['GM 1']}]}
  assert material.catalog_numbers(node, repositories) == []


@pytest.mark.parametrize('ellipsis', ['...', '…'])
def test_catalog_numbers_ellipsis_is_error(repositories, ellipsis):
  node = {'material': [{'catalogNumbers': [f'GM 1{ellipsis}']}]}
  assert material.catalog_numbers(node, repositories) == [
    ('error', f"catalog number 'GM 1{ellipsis}' contains an ellipsis"),
  ]


def test_catalog_numbers_ellipsis_reported_even_with_explicit_repository(repositories):
  node = {'material': [{'catalogNumbers': ['GM 1...'], 'repository': 'GM'}]}
  assert material.catalog_numbers(node, repositories) == [
    ('error', "catalog number 'GM 1...' contains an ellipsis"),
  ]


def test_catalog_numbers_explicit_repository_not_in_registry_is_error(repositories):
  node = {'material': [{'label': 'A', 'repository': 'NOWHERE'}]}
  assert material.catalog_numbers(node, repositories) == [
    ('error', 'repository "NOWHERE" is not a key of the registry'),
  ]


def test_catalog_numbers_explicit_repository_skips_resolution(repositories):
  # No warning for an unresolvable prefix once `repository` is given.
  node = {'material': [{'catalogNumbers': ['ZZZZ 1'], 'repository': 'GM'}]}
  assert material.catalog_numbers(node, repositories) == []


def test_catalog_numbers_range_same_repository_is_quiet(repositories):
  node = {'material': [{'catalogNumbers': [['GM 1', 'GM 2']]}]}
  assert material.catalog_numbers(node, repositories) == []


def test_catalog_numbers_range_different_repositories_is_error(repositories):
  node = {'material': [{'catalogNumbers': [['GM 1', 'USNM 2']]}]}
  assert material.catalog_numbers(node, repositories) == [
    ('error', "catalog number range ['GM 1', 'USNM 2'] resolves to different repositories"),
  ]


def test_catalog_numbers_range_one_endpoint_unresolved_only_warns(repositories):
  node = {'material': [{'catalogNumbers': [['GM 1', 'ZZZZ 2']]}]}
  assert material.catalog_numbers(node, repositories) == [
    ('warning', 'catalog number "ZZZZ 2" has no resolvable repository prefix'),
  ]


def test_unresolved_catalog_numbers_lists_values_by_name(repositories):
  node = {
    'material': [
      {'catalogNumbers': ['GM 1', 'ZZZZ 2...']},
      {'catalogNumbers': [['ZZZZ 3', 'GM 4']]},
      {'catalogNumbers': ['ZZZZ 5'], 'repository': 'GM'},
    ],
  }
  assert material.unresolved_catalog_numbers(node, repositories) == ['ZZZZ 3']


# -- null_material --------------------------------------------------------------


@pytest.mark.parametrize('field', ['material', 'figures', 'contexts', 'range'])
def test_null_material_cited_entry_with_any_field_is_error(field):
  node = {field: None}
  assert material.null_material(node, is_cited=True) == [
    ('error', f'cited entry carries `{field}`'),
  ]


def test_null_material_not_cited_is_quiet():
  node = {'material': None, 'figures': None, 'contexts': None, 'range': None}
  assert material.null_material(node, is_cited=False) == []


def test_null_material_null_beside_figure_of_is_error():
  node = {'material': None, 'figures': [{'plate': 1, 'of': 'A'}]}
  assert material.null_material(node, is_cited=False) == [
    ('error', '`material: null` beside a figure whose `of` names one'),
  ]


def test_null_material_not_null_beside_figure_of_is_quiet():
  node = {'material': [{'label': 'A'}], 'figures': [{'plate': 1, 'of': 'A'}]}
  assert material.null_material(node, is_cited=False) == []


def test_null_material_absent_is_quiet():
  assert material.null_material({}, is_cited=False) == []


# -- unused_fields ---------------------------------------------------------------


def test_unused_fields_none_declared_is_quiet():
  document = {'taxonomies': [{'taxon': 'a', 'range': None}]}
  assert material.unused_fields(document) == []


def test_unused_fields_flags_the_node_that_still_carries_it():
  document = {
    'unused': ['range'],
    'taxonomies': [
      {'taxon': 'a', 'range': None, 'children': [{'taxon': 'b'}]},
    ],
  }
  assert material.unused_fields(document) == [
    ('error', '`range` is listed as `unused` but appears at 0'),
  ]


def test_unused_fields_ignores_nodes_without_it():
  document = {'unused': ['range'], 'taxonomies': [{'taxon': 'a', 'children': [{'taxon': 'b'}]}]}
  assert material.unused_fields(document) == []


# -- walk_document ------------------------------------------------------------


def test_walk_document_paths_and_cited_flags():
  document = {
    'taxonomies': [
      {
        'taxon': 'a',
        'synonyms': [{'taxon': 'b', 'children': [{'taxon': 'c'}]}],
        'children': [{'taxon': 'd'}],
      },
    ],
    'phylogenies': [{'treeType': 'cladogram', 'tree': {'taxon': 'e'}}],
  }
  seen = {
    path: (node.get('taxon'), cited) for path, node, cited in material.walk_document(document)
  }
  assert seen == {
    '0': ('a', False),
    '0/synonyms/0': ('b', True),
    '0/synonyms/0/children/0': ('c', False),
    '0/children/0': ('d', False),
    '1': ('e', False),
  }


def test_walk_document_ignores_non_dict_and_absent_axes():
  assert list(material.walk_document({})) == []
  assert list(material.walk_document({'taxonomies': [None]})) == []


# -- Tree.file_contexts / file_unused / contexts / context_scopes -------------


def test_tree_file_contexts_and_unused_read_from_root_metadata(load_records):
  # No `taxon` field: only a registered source is needed (`Tree` hashes by
  # it), which `load_records` guarantees for real source key '1961_dehm'.
  metadata = {
    'source_key': '1961_dehm',
    'position': 900,
    'type': 'taxonomy',
    'file_contexts': {'loc': {}},
    'file_unused': ('range',),
  }
  root = Tree({'children': [{}]}, metadata)
  assert root.file_contexts == {'loc': {}}
  assert root.file_unused == ('range',)
  child = root.children[0]
  assert child.file_contexts == {'loc': {}}
  assert child.file_unused == ('range',)


def test_tree_contexts_merge_node_over_file_with_scope_map(load_records):
  metadata = {
    'source_key': '1961_dehm',
    'position': 901,
    'type': 'taxonomy',
    'file_contexts': {'loc': {'unit': ['a']}, 'file-only': {}},
  }
  root = Tree({'contexts': {'loc': {'unit': ['b']}}}, metadata)
  assert root.contexts == {'loc': {'unit': ['b']}, 'file-only': {}}
  assert root.context_scopes == {'loc': 'node', 'file-only': 'file'}


def test_tree_file_contexts_defaults_when_absent(load_records):
  metadata = {'source_key': '1961_dehm', 'position': 902, 'type': 'taxonomy'}
  root = Tree({}, metadata)
  assert root.file_contexts == {}
  assert root.file_unused == ()
  assert root.contexts == {}
  assert root.context_scopes == {}


# -- loader wiring (`load.py`'s `_report_material`) ---------------------------


def test_load_reports_material_checks_at_the_right_level(caplog):
  # Direct call, not a full `load()`: `Source`, `Taxon` and `Tree` keep
  # class-level registries shared by the whole session, so a fake corpus
  # routed through `load()` would leak into every other test.
  from phylohist.loader.load import _report_material

  data = {
    'repositories': {'GM': {'name': 'x', 'kind': 'institution'}},
    'trees': {
      '_synthetic_source': {
        'contexts': {'stray': {}},
        'unused': ['range'],
        'taxonomies': [
          {
            'taxon': 'cyathocystis',
            'range': None,
            'material': [{'catalogNumbers': ['ZZZZ 1'], 'context': 'missing-ctx'}],
            'figures': [{'plate': 1, 'of': 'nope'}],
            'synonyms': [{'taxon': 'cyathocystis', 'contexts': None}],
          },
        ],
      },
    },
  }
  with caplog.at_level(logging.WARNING, logger='phylohist'):
    _report_material(data)
  warnings = [r.getMessage() for r in caplog.records if r.levelno == logging.WARNING]
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert any('_synthetic_source' in m and 'context "stray"' in m for m in warnings)
  assert any(
    '_synthetic_source at 0' in m and 'no resolvable repository prefix' in m for m in warnings
  )
  assert any('`range` is listed as `unused`' in m for m in errors)
  assert any('context "missing-ctx" is not defined' in m for m in errors)
  assert any('figure "of" value "nope"' in m for m in errors)
  assert any('cited entry carries `contexts`' in m for m in errors)


# -- scripts/check_draft.py ---------------------------------------------------


def _run_check_draft(path):
  return subprocess.run(
    [sys.executable, str(SCRIPTS / 'check_draft.py'), str(path)],
    capture_output=True,
    text=True,
  )


def test_check_draft_exits_zero_on_a_clean_draft(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text('taxonomies:\n- taxon: cyathocystis\n')
  result = _run_check_draft(draft)
  assert result.returncode == 0, result.stdout + result.stderr


def test_check_draft_exits_one_on_material_null_on_a_cited_entry(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'taxonomies:\n'
    '- taxon: cyathocystis\n'
    '  synonyms:\n'
    '  - taxon: cyathocystidae\n'
    '    material: null\n',
  )
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'cited entry carries `material`' in result.stdout
