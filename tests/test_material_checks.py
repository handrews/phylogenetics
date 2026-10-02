"""The material checks (`phylohist.loader.material`): context references,
figure references, material entries and the file's `prefixes` map, nulls on
a cited entry, and the file-level `unused` list. Synthetic node dicts and
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


@pytest.fixture
def registers(repositories):
  """`repositories` plus the specimen registers and locality registers the
  real registry has for the cases below."""
  return {
    **repositories,
    'uq-f': _entry('UQF', 'F'),
    'gsc': _entry('GSC', other_names=['Canadian Geological Survey']),
    'usgs-l': {**_entry('USGS'), 'subject': 'localities'},
  }


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


# -- tentative_fields ---------------------------------------------------------


def test_tentative_names_a_field_the_range_does_not_carry():
  rng = {'period': 'Ordovician', 'tentative': ['series']}
  assert material.tentative_fields(rng, 'range') == [
    ('error', '`tentative` names `series`, which the range does not carry'),
  ]
  context = {'unit': ['A Fm.'], 'tentative': ['unit', 'biozone']}
  assert material.tentative_fields(context, 'context') == [
    ('error', '`tentative` names `biozone`, which the context does not carry'),
  ]


def test_tentative_cannot_name_a_key_that_is_no_printed_value():
  rng = {'series': 'Middle Ordovician', 'regions': ['Ottawa'], 'asPrinted': 'x', 'notes': 'y'}
  rng['tentative'] = ['tentative', 'notes', 'asPrinted', 'inferred', 'sources', 'regions']
  messages = material.tentative_fields(rng, 'range')
  assert [level for level, _ in messages] == ['error'] * 6
  assert [m.split('`')[3] for _, m in messages] == rng['tentative']


def test_tentative_true_on_a_file_level_context_is_error():
  context = {'unit': ['A Fm.'], 'tentative': True}
  assert material.tentative_fields(context, 'context', file_level=True) == [
    (
      'error',
      'a file-level context cannot be `tentative: true`; the doubt belongs to the node '
      'or the specimen that uses it',
    ),
  ]


def test_tentative_clean_cases():
  # A list on a range, a list on a node and a file-level context, `true`
  # on a node-level context and on a range, and no `tentative` at all.
  assert material.tentative_fields({'series': 'X', 'tentative': ['series']}, 'range') == []
  assert material.tentative_fields({'series': 'X', 'tentative': True}, 'range') == []
  assert material.tentative_fields({'biozone': 'X', 'tentative': ['biozone']}, 'context') == []
  assert (
    material.tentative_fields({'biozone': 'X', 'tentative': ['biozone']}, 'context', True) == []
  )
  assert material.tentative_fields({'unit': ['A']}, 'context', True) == []
  assert material.tentative_fields(None, 'context') == []
  node = {
    'ranges': [{'series': 'X', 'tentative': ['series']}, {'period': 'Y', 'tentative': True}, None],
    'contexts': {'a': {'biozone': 'X', 'tentative': ['biozone']}, 'b': {'tentative': True}},
  }
  assert material.range_tentatives(node) == []
  assert material.context_tentatives(node['contexts']) == []
  assert material.range_tentatives({'ranges': None}) == []


def test_tentative_checks_name_the_context_and_run_over_the_lists():
  node = {'ranges': [{'period': 'Y', 'tentative': ['series']}]}
  assert material.range_tentatives(node) == [
    ('error', '`tentative` names `series`, which the range does not carry'),
  ]
  contexts = {'a': {'unit': ['A'], 'tentative': True}, 'b': {'tentative': ['biozone']}, 'c': None}
  assert material.context_tentatives(contexts) == [
    ('error', 'context "b": `tentative` names `biozone`, which the context does not carry'),
  ]
  assert [m for _, m in material.context_tentatives(contexts, file_level=True)] == [
    'context "a": a file-level context cannot be `tentative: true`; the doubt belongs to the '
    'node or the specimen that uses it',
    'context "b": `tentative` names `biozone`, which the context does not carry',
  ]


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
  node = {'material': [{'label': 'A'}], 'illustrations': [{'plate': 1, 'of': 'A'}]}
  assert material.figure_refs(node) == []


def test_figure_refs_range_endpoint_matches():
  node = {
    'material': [{'prefix': 'GSC', 'numbers': [[1, 5]]}],
    'illustrations': [{'plate': 1, 'of': 5}],
  }
  assert material.figure_refs(node) == []


def test_figure_refs_no_match_is_error():
  node = {'material': [{'label': 'A'}], 'illustrations': [{'plate': 1, 'of': 'B'}]}
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "B" matches 0 material entries, not 1'),
  ]


def test_figure_refs_several_matches_is_error():
  node = {
    'material': [{'label': 'A'}, {'numbers': ['A']}],
    'illustrations': [{'plate': 1, 'of': 'A'}],
  }
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "A" matches 2 material entries, not 1'),
  ]


def test_figure_refs_list_of_and_no_of_field():
  node = {
    'material': [{'label': 'A'}, {'label': 'B'}],
    'illustrations': [{'plate': 1, 'of': ['A', 'B']}, {'plate': 2}],
  }
  assert material.figure_refs(node) == []


def test_figure_refs_cited_entry_is_not_read():
  node = {'material': [{'label': 'A'}], 'illustrations': [{'plate': 1, 'of': 'B'}]}
  assert material.figure_refs(node, is_cited=True) == []


def test_figure_refs_number_inside_a_run_matches():
  node = {
    'material': [{'prefix': 'MCZ', 'numbers': [[582, 587]]}, {'prefix': 'MCZ', 'numbers': [600]}],
    'illustrations': [{'plate': 1, 'of': [584, '582A', 585]}],
  }
  assert material.figure_refs(node) == []


def test_figure_refs_integer_run_of_five_digits():
  node = {
    'material': [{'prefix': 'GSC', 'numbers': [[25935, 25961]]}],
    'illustrations': [{'plate': 1, 'of': 25940}],
  }
  assert material.figure_refs(node) == []


def test_figure_refs_letter_run_matches_case_sensitively():
  node = {
    'material': [{'prefix': 'GSC', 'numbers': [['10088c', '10088h']]}],
    'illustrations': [{'plate': 1, 'of': '10088d'}, {'plate': 2, 'of': '10088D'}],
  }
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "10088D" matches 0 material entries, not 1'),
  ]


@pytest.mark.parametrize('value', ['581', '588', 'GM 584', '584-5', 'x584', '10088b', '10089d'])
def test_figure_refs_outside_a_run_or_of_another_stem_is_error(value):
  node = {
    'material': [{'prefix': 'MCZ', 'numbers': [[582, 587], ['10088c', '10088h']]}],
    'illustrations': [{'plate': 1, 'of': value}],
  }
  assert material.figure_refs(node) == [
    ('error', f'figure "of" value "{value}" matches 0 material entries, not 1'),
  ]


def test_figure_refs_a_run_with_a_suffixed_endpoint_is_not_an_integer_run():
  node = {
    'material': [{'prefix': 'MCZ', 'numbers': [['582A', 587]]}],
    'illustrations': [{'plate': 1, 'of': 584}],
  }
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "584" matches 0 material entries, not 1'),
  ]


def test_figure_refs_exact_match_beats_a_run_containing_the_number():
  node = {
    'material': [{'prefix': 'MCZ', 'numbers': [[582, 587]]}, {'prefix': 'MCZ', 'numbers': [584]}],
    'illustrations': [{'plate': 1, 'of': 584}],
  }
  assert material.figure_refs(node) == []
  assert [e['numbers'] for e in material.entries_named(node['material'], 584)] == [[584]]


def test_figure_refs_two_runs_containing_the_number_is_error():
  node = {
    'material': [
      {'prefix': 'MCZ', 'numbers': [[582, 587]]},
      {'prefix': 'MCZ', 'numbers': [[584, 590]]},
    ],
    'illustrations': [{'plate': 1, 'of': 585}],
  }
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "585" matches 2 material entries, not 1'),
  ]


# -- cast_refs -------------------------------------------------------------------


def test_cast_refs_matches_a_number_label_or_range_endpoint():
  node = {
    'material': [
      {'prefix': 'MCZ', 'numbers': ['629A'], 'castOf': 199},
      {'prefix': 'PE', 'numbers': [199]},
      {'prefix': 'MCZ', 'numbers': [700], 'castOf': 'the holotype'},
      {'label': 'the holotype'},
      {'prefix': 'MCZ', 'numbers': [800], 'castOf': 205},
      {'prefix': 'PE', 'numbers': [[201, 205]]},
    ],
  }
  assert material.cast_refs(node) == []


def test_cast_refs_number_inside_a_run_matches_and_exact_wins():
  node = {
    'material': [
      {'prefix': 'MCZ', 'numbers': ['629A'], 'castOf': 203},
      {'prefix': 'PE', 'numbers': [[201, 205]]},
      {'prefix': 'MCZ', 'numbers': [800], 'castOf': 204},
      {'prefix': 'PE', 'numbers': [[204, 210]]},
    ],
  }
  assert material.cast_refs(node) == []
  node['material'].append({'prefix': 'PE', 'numbers': [[202, 206]]})
  assert material.cast_refs(node) == [
    ('error', 'castOf "203" matches 2 material entries, not 1'),
  ]


def test_cast_refs_no_match_is_error():
  node = {'material': [{'prefix': 'MCZ', 'numbers': ['629A'], 'castOf': 199}]}
  assert material.cast_refs(node) == [('error', 'castOf "199" matches 0 material entries, not 1')]


def test_cast_refs_several_matches_is_error():
  node = {
    'material': [
      {'prefix': 'MCZ', 'numbers': ['629A'], 'castOf': 199},
      {'prefix': 'PE', 'numbers': [199]},
      {'label': '199'},
    ],
  }
  assert material.cast_refs(node) == [('error', 'castOf "199" matches 2 material entries, not 1')]


def test_cast_refs_own_entry_is_error():
  node = {'material': [{'prefix': 'MCZ', 'numbers': ['629A'], 'castOf': '629A'}]}
  assert material.cast_refs(node) == [('error', 'castOf "629A" names the entry itself')]


def test_cast_refs_absent_castof_and_absent_material_are_quiet():
  assert material.cast_refs({'material': [{'label': 'A'}]}) == []
  assert material.cast_refs({}) == []


# -- null_material --------------------------------------------------------------


@pytest.mark.parametrize('field', ['material', 'contexts', 'ranges'])
def test_null_material_cited_entry_with_any_field_is_error(field):
  node = {field: None}
  assert material.null_material(node, is_cited=True) == [
    ('error', f'cited entry carries `{field}`'),
  ]


def test_null_material_not_cited_is_quiet():
  node = {'material': None, 'illustrations': None, 'contexts': None, 'ranges': None}
  assert material.null_material(node, is_cited=False) == []


def test_null_ranges_is_accepted_on_a_primary_node_and_rejected_on_a_cited_entry():
  node = {'ranges': None}
  assert material.null_material(node, is_cited=False) == []
  assert material.null_material(node, is_cited=True) == [
    ('error', 'cited entry carries `ranges`'),
  ]


def test_null_material_cited_entry_may_carry_locators():
  node = {'illustrations': [{'plate': 15, 'figures': [1, 3, 4], 'uncertain': True}]}
  assert material.null_material(node, is_cited=True) == []


def test_null_material_cited_entry_with_null_illustrations_is_error():
  assert material.null_material({'illustrations': None}, is_cited=True) == [
    ('error', 'cited entry carries `illustrations: null`'),
  ]


def test_null_material_cited_entry_illustration_with_of_is_error():
  node = {'illustrations': [{'plate': 1, 'of': 'A'}, {'plate': 2}]}
  assert material.null_material(node, is_cited=True) == [
    ('error', 'cited entry `illustrations` entry carries `of`'),
  ]


def test_null_material_cited_entry_illustration_with_depicts_is_error():
  node = {'illustrations': [{'plate': 1, 'depicts': 'cast'}]}
  assert material.null_material(node, is_cited=True) == [
    ('error', 'cited entry `illustrations` entry carries `depicts`'),
  ]


def test_null_material_cited_entry_reports_each_offending_entry():
  node = {'illustrations': [{'plate': 1, 'of': 'A', 'depicts': 'cast'}, {'plate': 2, 'of': 'B'}]}
  assert len(material.null_material(node, is_cited=True)) == 3


@pytest.mark.parametrize('is_cited', [False, True])
def test_null_material_authority_illustration_with_of_is_error(is_cited):
  node = {'authority': {'source': 'x', 'illustrations': [{'plate': 1, 'of': 'A'}]}}
  assert material.null_material(node, is_cited=is_cited) == [
    ('error', '`authority.illustrations` entry carries `of`'),
  ]


def test_null_material_authority_illustration_with_depicts_is_error():
  node = {'authority': {'source': 'x', 'illustrations': [{'plate': 1, 'depicts': 'drawing'}]}}
  assert material.null_material(node, is_cited=False) == [
    ('error', '`authority.illustrations` entry carries `depicts`'),
  ]


def test_null_material_authority_locators_without_of_are_quiet():
  node = {'authority': {'source': 'x', 'illustrations': [{'plate': 1, 'figures': 2}]}}
  assert material.null_material(node, is_cited=False) == []


def test_null_material_null_beside_figure_of_is_error():
  node = {'material': None, 'illustrations': [{'plate': 1, 'of': 'A'}]}
  assert material.null_material(node, is_cited=False) == [
    ('error', '`material: null` beside a figure whose `of` names one'),
  ]


def test_null_material_not_null_beside_figure_of_is_quiet():
  node = {'material': [{'label': 'A'}], 'illustrations': [{'plate': 1, 'of': 'A'}]}
  assert material.null_material(node, is_cited=False) == []


def test_null_material_absent_is_quiet():
  assert material.null_material({}, is_cited=False) == []


def test_null_synonyms_on_a_cited_entry_is_error():
  assert material.null_material({'synonyms': None}, is_cited=True) == [
    ('error', 'cited entry carries `synonyms: null`'),
  ]


def test_null_synonyms_beside_a_non_list_is_error():
  node = {'synonyms': None, 'non': [{'taxon': 'a'}]}
  assert material.null_material(node, is_cited=False) == [
    ('error', '`synonyms: null` beside a `non` list'),
  ]


def test_null_synonyms_alone_is_quiet_on_a_primary_node():
  assert material.null_material({'synonyms': None}, is_cited=False) == []
  assert material.null_material({'synonyms': None, 'non': []}, is_cited=False) == []


def test_a_synonyms_list_on_a_cited_entry_is_quiet():
  # A nested synonymy exists; only the null is an error.
  node = {'synonyms': [{'taxon': 'a'}], 'non': [{'taxon': 'b'}]}
  assert material.null_material(node, is_cited=True) == []


# -- unused_fields ---------------------------------------------------------------


def test_unused_fields_none_declared_is_quiet():
  document = {'taxonomies': [{'taxon': 'a', 'ranges': None}]}
  assert material.unused_fields(document) == []


def test_unused_fields_flags_the_node_that_still_carries_it():
  document = {
    'unused': ['ranges'],
    'taxonomies': [
      {'taxon': 'a', 'ranges': None, 'children': [{'taxon': 'b'}]},
    ],
  }
  assert material.unused_fields(document) == [
    ('error', '`ranges` is listed as `unused` but appears at 0'),
  ]


def test_unused_ranges_with_a_node_carrying_ranges_is_error():
  document = {
    'unused': ['ranges'],
    'taxonomies': [{'taxon': 'a', 'ranges': [{'period': 'Ordovician'}]}],
  }
  assert material.unused_fields(document) == [
    ('error', '`ranges` is listed as `unused` but appears at 0'),
  ]


@pytest.mark.parametrize('value', [None, [{'taxon': 'b'}]])
def test_unused_synonyms_with_a_node_carrying_it_is_error(value):
  document = {'unused': ['synonyms'], 'taxonomies': [{'taxon': 'a', 'synonyms': value}]}
  assert material.unused_fields(document) == [
    ('error', '`synonyms` is listed as `unused` but appears at 0'),
  ]


def test_unused_fields_ignores_nodes_without_it():
  document = {'unused': ['ranges'], 'taxonomies': [{'taxon': 'a', 'children': [{'taxon': 'b'}]}]}
  assert material.unused_fields(document) == []


def test_unused_illustrations_tolerates_a_cited_entrys_locators():
  document = {
    'unused': ['illustrations'],
    'taxonomies': [{'taxon': 'a', 'synonyms': [{'taxon': 'b', 'illustrations': [{'plate': 1}]}]}],
  }
  assert material.unused_fields(document) == []


def test_unused_illustrations_flags_a_primary_node_even_with_null():
  document = {
    'unused': ['illustrations'],
    'taxonomies': [
      {
        'taxon': 'a',
        'synonyms': [{'taxon': 'b', 'illustrations': [{'plate': 1}]}],
        'children': [{'taxon': 'c', 'illustrations': None}],
      },
    ],
  }
  assert material.unused_fields(document) == [
    ('error', '`illustrations` is listed as `unused` but appears at 0/children/0'),
  ]


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
    'file_unused': ('ranges',),
  }
  root = Tree({'children': [{}]}, metadata)
  assert root.file_contexts == {'loc': {}}
  assert root.file_unused == ('ranges',)
  child = root.children[0]
  assert child.file_contexts == {'loc': {}}
  assert child.file_unused == ('ranges',)


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
        'unused': ['ranges'],
        'prefixes': {'GM': 'gm'},
        'taxonomies': [
          {
            'taxon': 'cyathocystis',
            'ranges': None,
            'material': [
              {'prefix': 'GM', 'numbers': [1], 'context': 'missing-ctx'},
              {'prefix': 'GM', 'numbers': [3], 'castOf': 2},
              {'numbers': [4], 'repository': 'nowhere'},
            ],
            'illustrations': [{'plate': 1, 'of': 'nope'}],
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
  assert any('`ranges` is listed as `unused`' in m for m in errors)
  assert any('context "missing-ctx" is not defined' in m for m in errors)
  assert any('figure "of" value "nope"' in m for m in errors)
  assert any('cited entry carries `contexts`' in m for m in errors)
  assert any('castOf "2" matches 0' in m for m in errors)
  assert any('repositories: `within` cycles: cyc -> cyc' in m for m in errors)
  assert any(
    '_synthetic_source at 0' in m and 'repository "nowhere" is not a key of the registry' in m
    for m in errors
  )
  assert sum('repository "nowhere"' in m for m in errors) == 1


def test_load_reports_tentative_on_ranges_and_contexts(caplog):
  from phylohist.loader.load import _report_material

  data = {
    'trees': {
      '_synthetic_source': {
        'contexts': {'f': {'biozone': 'X', 'tentative': True}},
        'taxonomies': [
          {
            'taxon': 'a',
            'contexts': {'n': {'tentative': ['biozone']}},
            'ranges': [{'period': 'Y', 'tentative': ['series']}],
          },
        ],
      },
    },
  }
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    _report_material(data)
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert any(m.startswith('_synthetic_source: context "f": a file-level context') for m in errors)
  assert any(
    m.startswith('_synthetic_source at 0: context "n": `tentative` names `biozone`') for m in errors
  )
  assert any(
    m.startswith('_synthetic_source at 0: `tentative` names `series`, which the range')
    for m in errors
  )


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


def test_check_draft_exits_one_on_a_tentative_naming_an_absent_field(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'contexts:\n  f:\n    tentative: true\n'
    'taxonomies:\n- taxon: cyathocystis\n'
    '  ranges:\n  - period: Cambrian\n    tentative: [series]\n',
  )
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'a file-level context cannot be `tentative: true`' in result.stdout
  assert '`tentative` names `series`, which the range does not carry' in result.stdout


def test_check_draft_exits_one_on_illustrations_null_on_a_primary_node(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text('taxonomies:\n- taxon: cyathocystis\n  illustrations: null\n')
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'draft carries `illustrations: null`' in result.stdout


def test_check_draft_exits_one_on_synonyms_null_on_a_primary_node(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text('taxonomies:\n- taxon: cyathocystis\n  synonyms: null\n')
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'draft carries `synonyms: null`' in result.stdout


def test_check_draft_exits_one_on_synonyms_null_on_a_cited_entry(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'taxonomies:\n'
    '- taxon: cyathocystis\n'
    '  synonyms:\n'
    '  - taxon: cyathocystidae\n'
    '    synonyms: null\n',
  )
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'cited entry carries `synonyms: null`' in result.stdout


def test_check_draft_exits_one_on_synonyms_null_beside_non(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'taxonomies:\n- taxon: cyathocystis\n  non:\n  - taxon: cyathocystidae\n  synonyms: null\n',
  )
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert '`synonyms: null` beside a `non` list' in result.stdout


def test_check_draft_exits_one_on_of_in_a_cited_entrys_illustrations(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'taxonomies:\n'
    '- taxon: cyathocystis\n'
    '  synonyms:\n'
    '  - taxon: cyathocystidae\n'
    '    illustrations:\n'
    '    - plate: 1\n'
    '      of: A\n',
  )
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'cited entry `illustrations` entry carries `of`' in result.stdout


def test_check_draft_warns_on_a_locality_number_with_no_register_and_is_quiet_with_one(tmp_path):
  body = (
    'contexts:\n  a:\n    localityNumbers: [{number: SH-1}]\n'
    'taxonomies:\n- taxon: cyathocystis\n  contexts:\n    b:\n'
    '      localityNumbers: [{number: IK-3}]\n'
  )
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(body)
  result = _run_check_draft(draft)
  assert result.stdout.count('has no register') == 2, result.stdout
  assert 'warning: locality number "SH-1"' in result.stdout
  assert 'warning: 0: locality number "IK-3"' in result.stdout

  draft.write_text('localityRegister: sprinkle-l\n' + body)
  result = _run_check_draft(draft)
  assert 'has no register' not in result.stdout, result.stdout


def test_check_draft_exits_one_on_an_explicit_repository_that_is_no_registry_key(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'taxonomies:\n- taxon: cyathocystis\n  material:\n  - {numbers: [1], repository: GSC}\n',
  )
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'repository "GSC" is not a key of the registry' in result.stdout


def test_roles_registry_matches_the_schema_enum():
  # Every role the schema allows is documented, and nothing else is; an
  # `equivalent` names another documented role.
  schema = io.load_yaml(io.SCHEMA_PATH)
  roles = io.load_yaml(io.DATA_DIR / 'roles.yaml')
  assert set(roles) == set(schema['$defs']['role']['enum'])
  for name, entry in roles.items():
    equivalent = entry.get('equivalent')
    assert equivalent is None or (equivalent in roles and equivalent != name), name


# -- the `prefix` + `numbers` shape --------------------------------------------


@pytest.fixture
def numbered(registers):
  """`registers` plus a register that lists its prefix, a collection that
  lists none, and an institution of the same name as one of its series."""
  return {
    **registers,
    'mcz-bare': {'name': 'x', 'type': 'collection', 'within': 'mcz', 'subject': 'specimens'},
    'nhmuk-ee': {
      'name': 'x',
      'type': 'collection',
      'within': 'nhmuk',
      'subject': 'specimens',
      'prefixes': ['EE'],
      'otherNames': ['Reg  E E'],
    },
  }


def _node(*entries, **extra):
  return {'material': list(entries), **extra}


def test_number_entries_prefix_missing_from_the_map_is_error(numbered):
  node = _node({'prefix': 'XX', 'numbers': [1]})
  assert material.number_entries(node, {'MCZ': 'mcz'}, numbered) == [
    ('error', 'prefix "XX" is not in the file\'s `prefixes` map'),
  ]
  assert material.number_entries(node, {'XX': 'mcz'}, numbered) == []
  # No map at all is the same error.
  assert material.number_entries(node, {}, numbered)[0][0] == 'error'


def test_number_entries_numbers_need_a_prefix_a_repository_or_a_holder(numbered):
  assert material.number_entries(_node({'numbers': ['5']}), {}, numbered) == [
    ('error', 'numbers with no prefix, repository or holder'),
  ]
  for entry in (
    {'numbers': ['5'], 'repository': 'gsc'},
    {'numbers': ['5'], 'holder': 'A. R. Palmer'},
    {'numbers': ['5'], 'prefix': 'GSC'},
  ):
    assert material.number_entries(_node(entry), {'GSC': 'gsc'}, numbered) == []


def test_number_entries_a_number_that_begins_with_its_registers_prefix_warns(numbered):
  prefixes = {'EE': 'nhmuk-ee', 'F.': 'uq-f'}
  node = _node(
    {'prefix': 'EE', 'numbers': ['EE16642', 'EE-1', 'EE.2', 'ee 3', 'reg e e 4', ['EE5', 7]]},
    {'prefix': 'F.', 'numbers': ['F. 5404', 'F5405', 'FE 6']},
  )
  assert material.number_entries(node, prefixes, numbered) == [
    ('warning', f'number "{n}" begins with a prefix of its register "{r}"')
    for r, n in (
      ('nhmuk-ee', 'EE16642'),
      ('nhmuk-ee', 'EE-1'),
      ('nhmuk-ee', 'EE.2'),
      ('nhmuk-ee', 'ee 3'),
      ('nhmuk-ee', 'reg e e 4'),
      ('nhmuk-ee', 'EE5'),
      ('uq-f', 'F. 5404'),
      ('uq-f', 'F5405'),
    )
  ]


def test_number_entries_a_clean_number_and_other_cases_are_quiet(numbered):
  prefixes = {'EE': 'nhmuk-ee', 'MCZ': 'mcz-bare'}
  node = _node(
    {'prefix': 'EE', 'numbers': ['16642', 16643, 'EEx1', [10, 12]]},
    # A register that lists no form has nothing to begin with.
    {'prefix': 'MCZ', 'numbers': ['MCZ 1']},
  )
  assert material.number_entries(node, prefixes, numbered) == []
  assert material.number_entries({}, prefixes, numbered) == []


def test_number_entries_reads_the_explicit_repository_register_too(numbered):
  node = _node({'prefix': 'USNM', 'numbers': ['EE 1'], 'repository': 'nhmuk-ee'})
  assert material.number_entries(node, {'USNM': 'usnm'}, numbered) == [
    ('warning', 'number "EE 1" begins with a prefix of its register "nhmuk-ee"'),
  ]


def test_number_entries_an_explicit_repository_is_a_registry_key_reported_once(numbered):
  node = _node(
    {'numbers': ['1'], 'repository': 'nope'},
    # A label entry has no numbers to check, but its repository is still read.
    {'label': 'A', 'repository': 'nowhere'},
    # `GM` is a prefix, not a key: only `gm` is.
    {'prefix': 'GM', 'numbers': [2], 'repository': 'GM'},
    {'count': 1, 'repository': 'gm'},
  )
  assert material.number_entries(node, {'GM': 'gm'}, numbered) == [
    ('error', 'repository "nope" is not a key of the registry'),
    ('error', 'repository "nowhere" is not a key of the registry'),
    ('error', 'repository "GM" is not a key of the registry'),
  ]


def _prefix_document(prefixes, *entries, **extra):
  return {'prefixes': prefixes, 'taxonomies': [{'taxon': 'a', 'material': list(entries)}], **extra}


def test_file_prefixes_clean_file_is_quiet(numbered):
  document = _prefix_document(
    {'MCZ': 'mcz', 'F.': 'uq-f', 'USGS': 'usgs-l', 'EE': 'nhmuk-ee'},
    {'prefix': 'MCZ', 'numbers': [1]},
    {'prefix': 'F.', 'numbers': [2]},
    {'prefix': 'EE', 'numbers': [3]},
    contexts={'a': {'localityNumbers': [{'prefix': 'USGS', 'number': 1}]}},
    localityRegister='usgs-l',
  )
  assert material.file_prefixes(document, numbered) == []
  assert material.file_prefixes({'taxonomies': []}, numbered) == []


def test_file_prefixes_a_value_that_is_no_registry_key_is_error(numbered):
  document = _prefix_document({'MCZ': 'mcz-nowhere'}, {'prefix': 'MCZ', 'numbers': [1]})
  assert material.file_prefixes(document, numbered) == [
    ('error', 'prefix "MCZ" is mapped to "mcz-nowhere", which is not a key of the registry'),
  ]


def test_file_prefixes_a_prefix_nothing_uses_is_error(numbered):
  document = _prefix_document(
    {'MCZ': 'mcz', 'GM': 'gm', 'USGS': 'usgs-l', 'NMV': 'gm'},
    {'prefix': 'MCZ', 'numbers': [1]},
  )
  document['taxonomies'][0]['contexts'] = {
    'b': {'localityNumbers': [{'prefix': 'USGS', 'number': 1}]}
  }
  assert [m for _, m in material.file_prefixes(document, numbered)] == [
    'prefix "GM" in the file\'s `prefixes` map is used by nothing',
    'prefix "NMV" is not a known form of "gm"',
    'prefix "NMV" in the file\'s `prefixes` map is used by nothing',
  ]


def test_file_prefixes_a_prefix_the_register_does_not_list_is_warning(numbered):
  document = _prefix_document(
    {'MCZ': 'gm', 'U.S.N.M.': 'usnm', 'BMNH': 'nhmuk'},
    {'prefix': 'MCZ', 'numbers': [1]},
    {'prefix': 'U.S.N.M.', 'numbers': [2]},
    {'prefix': 'BMNH', 'numbers': [3]},
  )
  assert material.file_prefixes(document, numbered) == [
    ('warning', 'prefix "MCZ" is not a known form of "gm"'),
    ('warning', 'prefix "U.S.N.M." is not a known form of "usnm"'),
  ]


def test_file_prefixes_forms_compare_folded_with_a_trailing_period_ignored(numbered):
  document = _prefix_document(
    {'F.': 'uq-f', 'uqf': 'uq-f', 'Nhm  Uk': 'nhmuk', 'bmnh.': 'nhmuk'},
    *({'prefix': p, 'numbers': [1]} for p in ('F.', 'uqf', 'Nhm  Uk', 'bmnh.')),
  )
  assert material.file_prefixes(document, numbered) == []


def test_file_prefixes_a_register_with_no_forms_is_not_warned_about(numbered):
  # The registers for series a holder numbers separately list no prefix yet.
  document = _prefix_document({'PE': 'mcz-bare'}, {'prefix': 'PE', 'numbers': [1]})
  assert material.file_prefixes(document, numbered) == []


def test_file_prefixes_locality_register_must_be_a_registry_key(numbered):
  assert material.file_prefixes({'localityRegister': 'usgs-l'}, numbered) == []
  assert material.file_prefixes({'localityRegister': 'nope-l'}, numbered) == [
    ('error', 'localityRegister "nope-l" is not a key of the registry'),
  ]


def test_locality_objects(numbered):
  contexts = {
    'a': {
      'localityNumbers': [
        {'number': 'FC-2'},
        {'prefix': 'USGS', 'number': '4148 CO'},
        {'prefix': 'ZZ', 'number': 1},
        {'register': 'usgs-l', 'number': 'D190d CO'},
        {'register': 'nope-l', 'number': 7},
      ]
    },
    'b': None,
  }
  prefixes = {'USGS': 'usgs-l'}
  assert material.locality_objects(contexts, prefixes, None, numbered) == [
    ('warning', 'locality number "FC-2" has no register'),
    ('error', 'prefix "ZZ" is not in the file\'s `prefixes` map'),
    ('error', 'locality register "nope-l" is not a key of the registry'),
  ]
  # A file `localityRegister` gives the bare number its register.
  assert [m for _, m in material.locality_objects(contexts, prefixes, 'sprinkle-l', numbered)] == [
    'prefix "ZZ" is not in the file\'s `prefixes` map',
    'locality register "nope-l" is not a key of the registry',
  ]
  assert material.locality_objects(None, prefixes, None, numbered) == []


# -- entries_named for the `prefix` + `numbers` shape ---------------------------


def test_entries_named_by_label_number_or_integer():
  entries = [
    {'prefix': 'MCZ', 'numbers': ['581A', 582, 'KR-2'], 'label': 'The Type'},
    {'prefix': 'MCZ', 'numbers': [600]},
  ]
  assert material.entries_named(entries, 'The Type') == entries[:1]
  assert material.entries_named(entries, 'the  type') == entries[:1]
  assert material.entries_named(entries, '581A') == entries[:1]
  assert material.entries_named(entries, '581a') == entries[:1]
  assert material.entries_named(entries, 582) == entries[:1]
  assert material.entries_named(entries, '582') == entries[:1]
  assert material.entries_named(entries, 'kr 2') == entries[:1]
  assert material.entries_named(entries, 600) == entries[1:]
  assert material.entries_named(entries, 601) == []
  # The prefix is no part of a number.
  assert material.entries_named(entries, 'MCZ 600') == []


def test_entries_named_inside_a_pair_and_exact_before_in_run():
  entries = [
    {'prefix': 'GSC', 'numbers': [[25935, 25961]]},
    {'prefix': 'GSC', 'numbers': [['A12', 'A20'], 25950]},
    {'prefix': 'GSC', 'numbers': [25940, ['25960', '25970']]},
  ]
  # An end of a pair counts exactly.
  assert material.entries_named(entries, 25935) == entries[:1]
  assert material.entries_named(entries, '25961') == entries[:1]
  # Inside a run only, by the run.
  assert material.entries_named(entries, 25936) == entries[:1]
  assert material.entries_named(entries, 'A15') == entries[1:2]
  assert material.entries_named(entries, 'a15') == []
  # Exact before in-run: 25940 is a number of the third and in the run of the first.
  assert material.entries_named(entries, 25940) == entries[2:]
  assert material.entries_named(entries, 25950) == entries[1:2]
  assert material.entries_named(entries, 25965) == entries[2:]
  assert material.entries_named(entries, 30000) == []


def test_figure_and_cast_refs_read_the_new_shape():
  node = {
    'material': [
      {'prefix': 'MCZ', 'numbers': [581, 'B2']},
      {'prefix': 'MCZ', 'numbers': [[600, 610]], 'castOf': 581},
      {'prefix': 'MCZ', 'numbers': [700], 'castOf': 'no-such'},
    ],
    'illustrations': [
      {'plate': 1, 'of': 581},
      {'plate': 2, 'of': [605, 'B2']},
      {'plate': 3, 'of': 999},
    ],
  }
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "999" matches 0 material entries, not 1'),
  ]
  assert material.cast_refs(node) == [
    ('error', 'castOf "no-such" matches 0 material entries, not 1'),
  ]


# -- the schema ------------------------------------------------------------------


def _schema_accepts(document):
  return io.build_schema()[io.TREE_DEF].check(document)


def _numbers_document(*entries, **extra):
  return {'taxonomies': [{'taxon': 'cyathocystis', 'material': list(entries)}], **extra}


def test_schema_accepts_the_new_shape():
  document = _numbers_document(
    {'prefix': 'MCZ', 'numbers': ['581A', 581, [1, 5], ['A1', 'A5']], 'parts': ['part']},
    {'prefix': 'GSC', 'numbers': [[25935, 25961]], 'asPrinted': 'GSC 25935–25961'},
    {'repository': 'u-cincinnati-caster', 'numbers': ['KR-2']},
    {'holder': 'A. R. Palmer', 'numbers': [[500, 501]]},
    {'prefix': 'USNM', 'repository': 'usnm-walcott', 'numbers': [1], 'castOf': 5, 'fragmentOf': 6},
    prefixes={'MCZ': 'mcz', 'GSC': 'gsc', 'USNM': 'usnm'},
    localityRegister='sprinkle-l',
    contexts={
      'a': {
        'localityNumbers': [
          {'number': 'FC-1'},
          {'prefix': 'USGS', 'number': '4148 CO'},
          {'register': 'usgs-l', 'number': 'D190d CO'},
          {'number': 7},
        ]
      }
    },
  )
  document['taxonomies'][0]['illustrations'] = [
    {'plate': 1, 'of': 581},
    {'plate': 2, 'of': [1, 'a']},
  ]
  assert _schema_accepts(document)


@pytest.mark.parametrize(
  'entry',
  [
    # The old shape is gone.
    {'catalogNumbers': ['MCZ 1']},
    {'catalogNumbers': ['MCZ 1'], 'numbers': [1]},
    {'prefix': 'MCZ', 'numbers': [1], 'catalogNumbersAsPrinted': 'MCZ 1'},
    {'prefix': 'MCZ'},
    {'prefix': '', 'numbers': [1]},
    {'prefix': 'MCZ', 'numbers': []},
    {'prefix': 'MCZ', 'numbers': [[1, 2, 3]]},
    {'prefix': 'MCZ', 'numbers': [[1]]},
    {'prefix': 'MCZ', 'numbers': [1.5]},
    {'prefix': 'MCZ', 'numbers': [[1, [2]]]},
    {'prefix': 'MCZ', 'numbers': [1], 'asPrinted': 3},
  ],
)
def test_schema_rejects_a_malformed_or_mixed_entry(entry):
  assert not _schema_accepts(_numbers_document(entry))


@pytest.mark.parametrize(
  'extra',
  [
    {'prefixes': {'': 'mcz'}},
    {'prefixes': {'MCZ': 'Not A Key'}},
    {'prefixes': {'MCZ': 5}},
    {'prefixes': ['MCZ']},
    {'localityRegister': ['sprinkle-l']},
    {'repositories': ['mcz']},
    {'contexts': {'a': {'localityNumbers': ['USGS 1']}}},
    {'contexts': {'a': {'localityNumbers': [{'prefix': 'A'}]}}},
    {'contexts': {'a': {'localityNumbers': [{'number': 1, 'prefix': 'A', 'register': 'usgs-l'}]}}},
    {'contexts': {'a': {'localityNumbers': [{'number': 1, 'other': 'x'}]}}},
    {'contexts': {'a': {'localityNumbers': [{'number': 1, 'prefix': ''}]}}},
    {'contexts': {'a': {'localityNumbers': [{'number': 1, 'register': 'Not A Key'}]}}},
  ],
)
def test_schema_rejects_a_malformed_prefix_map_or_locality_number(extra):
  assert not _schema_accepts(_numbers_document({'label': 'A'}, **extra))


# -- Tree metadata, the loader and the draft checker ---------------------------


def test_tree_reads_the_prefix_map_and_locality_register_from_root_metadata(load_records):
  metadata = {
    'source_key': '1961_dehm',
    'position': 903,
    'type': 'taxonomy',
    'file_prefixes': {'MCZ': 'mcz'},
    'file_locality_register': 'sprinkle-l',
  }
  root = Tree({'children': [{}]}, metadata)
  child = root.children[0]
  assert (child.file_prefixes, child.file_locality_register) == ({'MCZ': 'mcz'}, 'sprinkle-l')
  bare = Tree({}, {'source_key': '1961_dehm', 'position': 904, 'type': 'taxonomy'})
  assert (bare.file_prefixes, bare.file_locality_register) == ({}, None)


def test_load_reports_the_new_shape_checks(caplog):
  from phylohist.loader.load import _report_material

  data = {
    'repositories': {
      'mcz': _entry('MCZ'),
      'usgs-l': {**_entry('USGS'), 'subject': 'localities'},
    },
    'trees': {
      '_synthetic_source': {
        'prefixes': {'MCZ': 'mcz', 'GM': 'mcz', 'USGS': 'usgs-l'},
        'contexts': {'f': {'localityNumbers': [{'prefix': 'QQ', 'number': 1}]}},
        'taxonomies': [
          {
            'taxon': 'a',
            'material': [
              {'prefix': 'MCZ', 'numbers': ['MCZ 1']},
              {'prefix': 'ZZ', 'numbers': [2]},
              {'numbers': [3]},
            ],
            'contexts': {
              'n': {'localityNumbers': [{'number': 'FC-1'}, {'prefix': 'USGS', 'number': 1}]}
            },
          },
        ],
      },
    },
  }
  with caplog.at_level(logging.WARNING, logger='phylohist'):
    _report_material(data)
  warnings = [r.getMessage() for r in caplog.records if r.levelno == logging.WARNING]
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert '_synthetic_source: prefix "GM" is not a known form of "mcz"' in warnings
  assert (
    '_synthetic_source at 0: number "MCZ 1" begins with a prefix of its register "mcz"' in warnings
  )
  assert '_synthetic_source at 0: locality number "FC-1" has no register' in warnings
  assert '_synthetic_source: prefix "GM" in the file\'s `prefixes` map is used by nothing' in errors
  assert '_synthetic_source at 0: prefix "ZZ" is not in the file\'s `prefixes` map' in errors
  assert '_synthetic_source at 0: numbers with no prefix, repository or holder' in errors
  assert '_synthetic_source: prefix "QQ" is not in the file\'s `prefixes` map' in errors
  # The file's own contexts are read as a file: no `localityRegister`, no prefix.
  assert not any('resolves to no locality register' in m for m in warnings)


def test_check_draft_reports_the_new_shape_checks(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'prefixes:\n  MCZ: mcz\n  XX: usnm\n'
    'localityRegister: sprinkle-l\n'
    'contexts:\n  a:\n    localityNumbers:\n    - {number: FC-1}\n    - {prefix: ZZ, number: 1}\n'
    'taxonomies:\n- taxon: cyathocystis\n  material:\n'
    '  - {prefix: MCZ, numbers: [581A]}\n  - {numbers: [3]}\n  - {prefix: QQ, numbers: [4]}\n'
  )
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  for line in (
    'error: prefix "ZZ" is not in the file\'s `prefixes` map',
    'error: prefix "XX" in the file\'s `prefixes` map is used by nothing',
    'warning: prefix "XX" is not a known form of "usnm"',
    'error: 0: numbers with no prefix, repository or holder',
    'error: 0: prefix "QQ" is not in the file\'s `prefixes` map',
  ):
    assert line in result.stdout, line
  assert 'locality number "FC-1" has no register' not in result.stdout


def test_check_draft_is_quiet_on_a_clean_new_shape_draft(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'prefixes:\n  MCZ: mcz\n  USGS: usgs-l\n'
    'contexts:\n  a:\n    localityNumbers:\n    - {prefix: USGS, number: 4148 CO}\n'
    'taxonomies:\n- taxon: cyathocystis\n  material:\n'
    '  - {prefix: MCZ, numbers: [581A, [1, 5]], context: a}\n'
    '  - {holder: A. R. Palmer, numbers: [500]}\n'
  )
  result = _run_check_draft(draft)
  assert result.returncode == 0, result.stdout + result.stderr
  assert 'warning' not in result.stdout and 'error' not in result.stdout
