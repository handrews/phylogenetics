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


def _entry(*prefixes, other_names=(), within=None):
  entry = {'name': 'x', 'type': 'institution', 'prefixes': list(prefixes)}
  if other_names:
    entry['otherNames'] = list(other_names)
  if within:
    entry['within'] = within
  return entry


@pytest.fixture
def repositories():
  """A synthetic registry: keys are slugs, and PE, E and UCMP are each
  claimed by two entries."""
  return {
    'fmnh': _entry('FMNH', 'PE', 'FMNH PE'),
    'north-museum-fm': _entry('PE'),
    'nhmuk': _entry('NHMUK', 'E', other_names=['BMNH', 'NHM UK']),
    'uc': _entry('UC'),
    'uc-caster': _entry('E', 'BC', within='uc'),
    'uc-museum': _entry('UCMP', within='uc'),
    'berkeley': _entry('UCMP'),
    'mcz': _entry('MCZ'),
    'gm': _entry('GM'),
    'usnm': _entry('USNM'),
    'usnm-walcott': {'name': 'x', 'type': 'collection', 'within': 'usnm'},
  }


# -- repository_of (D3) --------------------------------------------------------


def test_repository_of_prefix(repositories):
  assert material.repository_of('GM 9-5-2 165b', repositories) == ('gm', 'prefix')


def test_repository_of_key_is_not_a_prefix(repositories):
  # `usnm-walcott` is a slug, not something a catalog number prints.
  assert material.repository_of('usnm-walcott 12', repositories) == (None, None)
  assert material.repository_of('north-museum-fm 12', repositories) == (None, None)


def test_repository_of_other_names(repositories):
  assert material.repository_of('BMNH 12345', repositories) == ('nhmuk', 'otherNames')
  assert material.repository_of('NHM UK EE15373', repositories) == ('nhmuk', 'otherNames')


def test_repository_of_case_and_whitespace_folded(repositories):
  assert material.repository_of('nhm   uk 12', repositories) == ('nhmuk', 'otherNames')
  assert material.repository_of('gm12', repositories) == ('gm', 'prefix')


def test_repository_of_trailing_hyphen_folds_like_a_space(repositories):
  files = ['fmnh']
  assert material.repository_of('PE-214', repositories, files) == ('fmnh', 'file')
  assert material.repository_of('PE 214', repositories, files) == ('fmnh', 'file')


def test_repository_of_trailing_period_folds_like_a_hyphen():
  registry = {'uq-f': _entry('UQF', 'F')}
  for number in ('F. 5404', 'F.5404', 'F 5404', 'F-5404'):
    assert material.repository_of(number, registry) == ('uq-f', 'prefix'), number
  # A period inside the number is past the first digit and untouched.
  assert material.repository_of('UQF 5404.2', registry) == ('uq-f', 'prefix')


def test_repository_of_hyphen_inside_the_number_is_untouched(repositories):
  assert material.repository_of('MCZ 602-D1', repositories) == ('mcz', 'prefix')
  assert material.repository_of('MCZ 602-RO-5', repositories) == ('mcz', 'prefix')


def test_repository_of_token_boundary_prefix(repositories):
  # "USNM S" is the leading run; USNM matches at a token boundary.
  assert material.repository_of('USNM S-3965', repositories) == ('usnm', 'prefix')
  # No boundary after GM, so it is not a match for GMX.
  assert material.repository_of('GMX 12', repositories) == (None, None)


def test_repository_of_longest_candidate_wins(repositories):
  # FMNH PE is longer than FMNH or PE, and only fmnh claims it.
  assert material.repository_of('FMNH PE 12', repositories) == ('fmnh', 'prefix')


def test_repository_of_file_list_settles_pe_for_either_claimant(repositories):
  assert material.repository_of('PE 214', repositories, ['fmnh']) == ('fmnh', 'file')
  assert material.repository_of('PE 214', repositories, ['north-museum-fm']) == (
    'north-museum-fm',
    'file',
  )


def test_repository_of_ambiguous_without_a_list(repositories):
  assert material.repository_of('E23470', repositories) == (
    ('nhmuk', 'uc-caster'),
    material.AMBIGUOUS,
  )


def test_repository_of_ambiguous_when_the_list_names_none_or_both(repositories):
  both = ['nhmuk', 'uc-caster']
  assert material.repository_of('E 1', repositories, both) == (
    ('nhmuk', 'uc-caster'),
    material.AMBIGUOUS,
  )
  assert material.repository_of('E 1', repositories, ['gm']) == (
    ('nhmuk', 'uc-caster'),
    material.AMBIGUOUS,
  )


def test_repository_of_ucmp_with_the_cincinnati_museum_listed(repositories):
  assert material.repository_of('UCMP 12', repositories, ['uc-museum']) == ('uc-museum', 'file')
  assert material.repository_of('UCMP 12', repositories, ['berkeley']) == ('berkeley', 'file')


def test_repository_of_an_entry_claiming_a_candidate_twice_is_one_claim():
  registry = {'a': _entry('AB', other_names=['AB'])}
  assert material.repository_of('AB 1', registry) == ('a', 'prefix')


def test_repository_of_no_prefix(repositories):
  assert material.repository_of('12345', repositories) == (None, None)


def test_repository_of_unresolvable_prefix(repositories):
  assert material.repository_of('ZZZZ 12', repositories) == (None, None)


# -- registry_links -------------------------------------------------------------


def test_registry_links_real_registry_passes():
  assert material.registry_links(io.load_yaml(io.DATA_DIR / 'repositories.yaml')) == []


def test_registry_links_synthetic_registry_passes(repositories):
  assert material.registry_links(repositories) == []


def test_registry_links_within_a_missing_key_is_error():
  registry = {'a': _entry('A', within='nowhere')}
  assert material.registry_links(registry) == [
    ('error', 'repository "a" is within "nowhere", which is not a key'),
  ]


def test_registry_links_within_cycle_is_error_once():
  registry = {
    'a': _entry('A', within='b'),
    'b': _entry('B', within='c'),
    'c': _entry('C', within='a'),
  }
  messages = material.registry_links(registry)
  assert len(messages) == 1
  assert messages[0][0] == 'error'
  assert '`within` cycles' in messages[0][1]


def test_registry_links_self_within_is_a_cycle():
  registry = {'a': _entry('A', within='a')}
  assert material.registry_links(registry) == [('error', '`within` cycles: a -> a')]


def test_registry_links_chain_into_a_cycle_reports_the_cycle():
  registry = {
    'a': _entry('A', within='b'),
    'b': _entry('B', within='c'),
    'c': _entry('C', within='b'),
  }
  assert material.registry_links(registry) == [('error', '`within` cycles: b -> c -> b')]


# -- file_repositories_used ------------------------------------------------------


def _document(*numbers, **extra):
  return {
    'taxonomies': [{'taxon': 'a', 'material': [{'catalogNumbers': list(numbers)}]}],
    **extra,
  }


def test_file_repositories_used_no_list_is_quiet(repositories):
  assert material.file_repositories_used(_document('PE 1'), repositories) == []


def test_file_repositories_used_listed_and_used_is_quiet(repositories):
  document = _document('PE 1', repositories=['fmnh'])
  assert material.file_repositories_used(document, repositories) == []


def test_file_repositories_used_range_endpoint_counts(repositories):
  document = _document(['PE 1', 'PE 5'], repositories=['fmnh'])
  assert material.file_repositories_used(document, repositories) == []


def test_file_repositories_used_explicit_repository_counts(repositories):
  document = {
    'taxonomies': [
      {'taxon': 'a', 'material': [{'catalogNumbers': ['12'], 'repository': 'usnm-walcott'}]}
    ],
    'repositories': ['usnm-walcott'],
  }
  assert material.file_repositories_used(document, repositories) == []


def test_file_repositories_used_missing_key_is_error(repositories):
  document = _document('GM 1', repositories=['nowhere'])
  assert material.file_repositories_used(document, repositories) == [
    ('error', 'listed repository "nowhere" is not a key of the registry'),
  ]


def test_file_repositories_used_listed_but_unused_is_error(repositories):
  document = _document('GM 1', 'PE 2', repositories=['fmnh', 'mcz'])
  assert material.file_repositories_used(document, repositories) == [
    (
      'error',
      'repository "mcz" is listed but no catalog number in the file resolves to it',
    ),
  ]


def test_file_repositories_used_ellipsis_and_ambiguous_do_not_count(repositories):
  # E is ambiguous against this list, and "PE 1..." carries an ellipsis.
  document = _document('E 1', 'PE 1...', repositories=['fmnh'])
  assert material.file_repositories_used(document, repositories) == [
    ('error', 'repository "fmnh" is listed but no catalog number in the file resolves to it'),
  ]


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
  node = {'material': [{'catalogNumbers': ['GM 1...'], 'repository': 'gm'}]}
  assert material.catalog_numbers(node, repositories) == [
    ('error', "catalog number 'GM 1...' contains an ellipsis"),
  ]


def test_catalog_numbers_explicit_repository_not_in_registry_is_error(repositories):
  node = {'material': [{'label': 'A', 'repository': 'nowhere'}]}
  assert material.catalog_numbers(node, repositories) == [
    ('error', 'repository "nowhere" is not a key of the registry'),
  ]


def test_catalog_numbers_explicit_repository_is_a_key_not_a_prefix(repositories):
  # `GM` is a prefix, not a key: only `gm` is.
  node = {'material': [{'catalogNumbers': ['GM 1'], 'repository': 'GM'}]}
  assert material.catalog_numbers(node, repositories) == [
    ('error', 'repository "GM" is not a key of the registry'),
  ]


def test_catalog_numbers_ambiguous_prefix_is_error_naming_the_candidates(repositories):
  node = {'material': [{'catalogNumbers': ['E 23470']}]}
  assert material.catalog_numbers(node, repositories) == [
    ('error', 'catalog number "E 23470" has an ambiguous prefix: nhmuk, uc-caster'),
  ]
  assert material.unresolved_catalog_numbers(node, repositories) == []


def test_catalog_numbers_file_list_settles_an_ambiguous_prefix(repositories):
  node = {'material': [{'catalogNumbers': ['E 23470']}]}
  assert material.catalog_numbers(node, repositories, ['uc-caster']) == []


def test_catalog_numbers_range_endpoints_settled_to_different_entries_is_error(repositories):
  node = {'material': [{'catalogNumbers': [['PE 1', 'FMNH 2']]}]}
  assert material.catalog_numbers(node, repositories, ['north-museum-fm']) == [
    ('error', "catalog number range ['PE 1', 'FMNH 2'] resolves to different repositories"),
  ]


def test_catalog_numbers_explicit_repository_skips_resolution(repositories):
  # No warning for an unresolvable prefix once `repository` is given.
  node = {'material': [{'catalogNumbers': ['ZZZZ 1'], 'repository': 'gm'}]}
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
      {'catalogNumbers': ['ZZZZ 5'], 'repository': 'gm'},
    ],
  }
  assert material.unresolved_catalog_numbers(node, repositories) == ['ZZZZ 3']


# -- cast_refs -------------------------------------------------------------------


def test_cast_refs_matches_a_catalog_number_label_or_range_endpoint():
  node = {
    'material': [
      {'catalogNumbers': ['MCZ 629A'], 'castOf': 'PE 199'},
      {'catalogNumbers': ['PE 199']},
      {'catalogNumbers': ['MCZ 700'], 'castOf': 'the holotype'},
      {'label': 'the holotype'},
      {'catalogNumbers': ['MCZ 800'], 'castOf': 'PE 205'},
      {'catalogNumbers': [['PE 201', 'PE 205']]},
    ],
  }
  assert material.cast_refs(node) == []


def test_cast_refs_no_match_is_error():
  node = {'material': [{'catalogNumbers': ['MCZ 629A'], 'castOf': 'PE 199'}]}
  assert material.cast_refs(node) == [
    ('error', 'castOf "PE 199" matches 0 material entries, not 1')
  ]


def test_cast_refs_several_matches_is_error():
  node = {
    'material': [
      {'catalogNumbers': ['MCZ 629A'], 'castOf': 'PE 199'},
      {'catalogNumbers': ['PE 199']},
      {'label': 'PE 199'},
    ],
  }
  assert material.cast_refs(node) == [
    ('error', 'castOf "PE 199" matches 2 material entries, not 1')
  ]


def test_cast_refs_own_entry_is_error():
  node = {'material': [{'catalogNumbers': ['MCZ 629A'], 'castOf': 'MCZ 629A'}]}
  assert material.cast_refs(node) == [('error', 'castOf "MCZ 629A" names the entry itself')]


def test_cast_refs_absent_castof_and_absent_material_are_quiet():
  assert material.cast_refs({'material': [{'label': 'A'}]}) == []
  assert material.cast_refs({}) == []


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
    'repositories': {'gm': _entry('GM'), 'cyc': _entry('CYC', within='cyc')},
    'trees': {
      '_synthetic_source': {
        'contexts': {'stray': {}},
        'unused': ['range'],
        'repositories': ['gm', 'nowhere'],
        'taxonomies': [
          {
            'taxon': 'cyathocystis',
            'range': None,
            'material': [
              {'catalogNumbers': ['ZZZZ 1'], 'context': 'missing-ctx'},
              {'catalogNumbers': ['MCZ 1'], 'castOf': 'MCZ 2'},
            ],
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
  assert any('castOf "MCZ 2" matches 0' in m for m in errors)
  assert any('repositories: `within` cycles: cyc -> cyc' in m for m in errors)
  assert any('listed repository "nowhere"' in m for m in errors)
  assert any('repository "gm" is listed but no catalog number' in m for m in errors)


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


def test_check_draft_exits_one_on_a_listed_but_unused_repository(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'repositories: [nhmuk]\n'
    'taxonomies:\n'
    '- taxon: cyathocystis\n'
    '  material:\n'
    '  - catalogNumbers: [GSC 1]\n',
  )
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'repository "nhmuk" is listed but no catalog number' in result.stdout


def test_check_draft_exits_one_on_an_ambiguous_prefix_and_zero_once_listed(tmp_path):
  body = '- taxon: cyathocystis\n  material:\n  - catalogNumbers: [E 23470]\n'
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text('taxonomies:\n' + body)
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'ambiguous prefix' in result.stdout

  draft.write_text('repositories: [u-cincinnati-caster]\ntaxonomies:\n' + body)
  result = _run_check_draft(draft)
  assert result.returncode == 0, result.stdout + result.stderr


def test_roles_registry_matches_the_schema_enum():
  # Every role the schema allows is documented, and nothing else is; an
  # `equivalent` names another documented role.
  schema = io.load_yaml(io.SCHEMA_PATH)
  roles = io.load_yaml(io.DATA_DIR / 'roles.yaml')
  assert set(roles) == set(schema['$defs']['role']['enum'])
  for name, entry in roles.items():
    equivalent = entry.get('equivalent')
    assert equivalent is None or (equivalent in roles and equivalent != name), name
