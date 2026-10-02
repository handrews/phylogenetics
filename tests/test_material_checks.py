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


# -- resolve_number: the bare number and the register's subject ---------------


@pytest.fixture
def registers(repositories):
  """`repositories` plus the specimen registers and locality registers the
  real registry has for the cases below."""
  return {
    **repositories,
    'uq-f': _entry('UQF', 'F'),
    'gsc': _entry('GSC', other_names=['Canadian Geological Survey']),
    'usgs-l': {**_entry('USGS'), 'subject': 'localities'},
    'usnm-l': {
      **_entry('USNM', 'USNM loc', 'USNM locality', 'Walcott', 'Walcott locality'),
      'subject': 'localities',
    },
    'own-l': {'name': 'x', 'type': 'person', 'subject': 'localities'},
    'other-l': {'name': 'y', 'type': 'person', 'subject': 'localities'},
  }


@pytest.mark.parametrize(
  ('number', 'key', 'bare'),
  [
    ('F. 5404', 'uq-f', '5404'),
    ('UQF5404', 'uq-f', '5404'),
    ('UQF 5404', 'uq-f', '5404'),
    ('UQF No. 5404', 'uq-f', '5404'),
    ('FMNH PE 214', 'fmnh', '214'),
    ('MCZ 602-D1', 'mcz', '602-D1'),
    ('Canadian Geological Survey 752', 'gsc', '752'),
    ('canadian  geological survey 752', 'gsc', '752'),
    ('USNM S-3965', 'usnm', 'S-3965'),
  ],
)
def test_resolve_number_bare_number(registers, number, key, bare):
  assert material.resolve_number(number, registers)[::2] == (key, bare)


def test_resolve_number_bare_number_through_the_file_list(registers):
  assert material.resolve_number('PE-214', registers, ['fmnh']) == ('fmnh', 'file', '214')
  assert material.resolve_number('PE 214', registers, ['north-museum-fm']) == (
    'north-museum-fm',
    'file',
    '214',
  )


def test_resolve_number_strips_only_the_matched_candidate(registers):
  # The prefix is "USGS D", the candidate "USGS": the "D" belongs to the number.
  assert material.resolve_number('USGS D190d CO', registers, localities=True) == (
    'usgs-l',
    'prefix',
    'D190d CO',
  )


def test_resolve_number_unmatched_and_ambiguous_return_the_number_unchanged(registers):
  assert material.resolve_number('ZZZZ 12', registers) == (None, None, 'ZZZZ 12')
  assert material.resolve_number('12345', registers) == (None, None, '12345')
  assert material.resolve_number('E 1', registers) == (
    ('nhmuk', 'uc-caster'),
    material.AMBIGUOUS,
    'E 1',
  )


def test_resolve_number_a_number_that_is_only_its_prefix_stays_whole(registers):
  assert material.resolve_number('UQF', registers) == ('uq-f', 'prefix', 'UQF')


def test_resolve_number_localities_read_the_locality_registers_only(registers):
  assert material.resolve_number('USNM loc. 35k', registers, localities=True) == (
    'usnm-l',
    'prefix',
    '35k',
  )
  assert material.resolve_number('Walcott 35k', registers, localities=True)[::2] == (
    'usnm-l',
    '35k',
  )
  assert material.resolve_number('USNM locality 74e', registers, localities=True)[::2] == (
    'usnm-l',
    '74e',
  )
  assert material.resolve_number('Walcott locality 74e', registers, localities=True)[::2] == (
    'usnm-l',
    '74e',
  )


def test_resolve_number_the_subject_filter_works_both_ways(registers):
  # A locality prefix does not resolve a catalog number ...
  assert material.resolve_number('USGS 4148', registers) == (None, None, 'USGS 4148')
  assert material.resolve_number('Walcott 35k', registers) == (None, None, 'Walcott 35k')
  assert material.repository_of('USNM 35k', registers) == ('usnm', 'prefix')
  # ... and a specimen prefix does not resolve a locality number.
  assert material.resolve_number('GM 12', registers, localities=True) == (None, None, 'GM 12')
  assert material.resolve_number('UQF 12', registers, localities=True) == (None, None, 'UQF 12')


def test_resolve_number_locality_fallback_is_the_one_prefixless_register_listed(registers):
  assert material.resolve_number('SH-1', registers, ['own-l'], localities=True) == (
    'own-l',
    'file',
    'SH-1',
  )
  # A listed register that has prefixes is not the author's own codes.
  assert material.resolve_number('SH-1', registers, ['usgs-l'], localities=True) == (
    None,
    None,
    'SH-1',
  )
  # None listed, two listed, or a specimen register listed: unresolved.
  assert material.resolve_number('SH-1', registers, (), localities=True)[1] is None
  assert (
    material.resolve_number('SH-1', registers, ['own-l', 'other-l'], localities=True)[1] is None
  )
  assert material.resolve_number('SH-1', registers, ['fmnh'], localities=True)[1] is None
  # A prefix that matches wins over the fallback; the fallback is for localities only.
  assert material.resolve_number('USGS 5', registers, ['own-l'], localities=True)[0] == 'usgs-l'
  assert material.resolve_number('SH-1', registers, ['own-l']) == (None, None, 'SH-1')


def test_bare_number_strips_the_named_repositorys_own_prefix_or_name(registers):
  assert material.bare_number('GSC 752', 'gsc', registers) == '752'
  assert material.bare_number('Canadian Geological Survey 752', 'gsc', registers) == '752'
  assert material.bare_number('F. 5404', 'uq-f', registers) == '5404'
  assert material.bare_number('FMNH PE 214', 'fmnh', registers) == '214'
  # Another holder's prefix, no prefix at all, or an unknown repository: unchanged.
  assert material.bare_number('XYZ 1', 'nhmuk', registers) == 'XYZ 1'
  assert material.bare_number('12345', 'gsc', registers) == '12345'
  assert material.bare_number('GSC 752', 'nowhere', registers) == 'GSC 752'
  assert material.bare_number('UQF', 'uq-f', registers) == 'UQF'


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


def test_file_repositories_used_a_locality_number_counts(registers):
  node = {'contexts': {'a': {'localityNumbers': ['SH-1']}}}
  document = {'taxonomies': [{'taxon': 'a', **node}], 'repositories': ['own-l']}
  assert material.file_repositories_used(document, registers) == []
  # A file-level context counts too, and a listed register no number reaches is an error.
  document = {
    'taxonomies': [{'taxon': 'a'}],
    'contexts': {'a': {'localityNumbers': ['USGS 5462', 'Walcott 35k']}},
    'repositories': ['usgs-l', 'usnm-l', 'own-l'],
  }
  assert material.file_repositories_used(document, registers) == [
    ('error', 'repository "own-l" is listed but no catalog number in the file resolves to it'),
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
    'material': [{'catalogNumbers': [['GSC 1', 'GSC 5']]}],
    'illustrations': [{'plate': 1, 'of': 'GSC 5'}],
  }
  assert material.figure_refs(node) == []


def test_figure_refs_no_match_is_error():
  node = {'material': [{'label': 'A'}], 'illustrations': [{'plate': 1, 'of': 'B'}]}
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "B" matches 0 material entries, not 1'),
  ]


def test_figure_refs_several_matches_is_error():
  node = {
    'material': [{'label': 'A'}, {'catalogNumbers': ['A']}],
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
    'material': [{'catalogNumbers': [['MCZ 582', 'MCZ 587']]}, {'catalogNumbers': ['MCZ 600']}],
    'illustrations': [{'plate': 1, 'of': ['MCZ 584', 'MCZ 582A', 'MCZ  585']}],
  }
  assert material.figure_refs(node) == []


def test_figure_refs_integer_run_of_five_digits_and_a_stem():
  node = {
    'material': [{'catalogNumbers': [['GSC 25935', 'GSC 25961']]}],
    'illustrations': [{'plate': 1, 'of': 'GSC 25940'}],
  }
  assert material.figure_refs(node) == []


def test_figure_refs_letter_run_matches_case_sensitively():
  node = {
    'material': [{'catalogNumbers': [['GSC 10088c', 'GSC 10088h']]}],
    'illustrations': [{'plate': 1, 'of': 'GSC 10088d'}, {'plate': 2, 'of': 'GSC 10088D'}],
  }
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "GSC 10088D" matches 0 material entries, not 1'),
  ]


@pytest.mark.parametrize(
  'value',
  ['MCZ 581', 'MCZ 588', 'GM 584', 'MCZ 584-5', 'MCZ584x', 'GSC 10088b', 'GSC 10089d'],
)
def test_figure_refs_outside_a_run_or_of_another_stem_is_error(value):
  node = {
    'material': [{'catalogNumbers': [['MCZ 582', 'MCZ 587'], ['GSC 10088c', 'GSC 10088h']]}],
    'illustrations': [{'plate': 1, 'of': value}],
  }
  assert material.figure_refs(node) == [
    ('error', f'figure "of" value "{value}" matches 0 material entries, not 1'),
  ]


def test_figure_refs_a_run_with_a_suffixed_endpoint_is_not_an_integer_run():
  node = {
    'material': [{'catalogNumbers': [['MCZ 582A', 'MCZ 587']]}],
    'illustrations': [{'plate': 1, 'of': 'MCZ 584'}],
  }
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "MCZ 584" matches 0 material entries, not 1'),
  ]


def test_figure_refs_exact_match_beats_a_run_containing_the_number():
  node = {
    'material': [{'catalogNumbers': [['MCZ 582', 'MCZ 587']]}, {'catalogNumbers': ['MCZ 584']}],
    'illustrations': [{'plate': 1, 'of': 'MCZ 584'}],
  }
  assert material.figure_refs(node) == []
  assert [e['catalogNumbers'] for e in material.entries_named(node['material'], 'MCZ 584')] == [
    ['MCZ 584']
  ]


def test_figure_refs_two_runs_containing_the_number_is_error():
  node = {
    'material': [
      {'catalogNumbers': [['MCZ 582', 'MCZ 587']]},
      {'catalogNumbers': [['MCZ 584', 'MCZ 590']]},
    ],
    'illustrations': [{'plate': 1, 'of': 'MCZ 585'}],
  }
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "MCZ 585" matches 2 material entries, not 1'),
  ]


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


def test_catalog_numbers_holder_needs_no_resolvable_prefix(repositories):
  node = {'material': [{'catalogNumbers': ['ZZZZ 1', [' 5', ' 9']], 'holder': 'a collector'}]}
  assert material.catalog_numbers(node, repositories) == []
  assert material.unresolved_catalog_numbers(node, repositories) == []


def test_catalog_numbers_holder_excuses_neither_an_ellipsis_nor_an_ambiguous_prefix(repositories):
  node = {
    'material': [
      {'catalogNumbers': ['ZZZZ 1...'], 'holder': 'a collector'},
      {'catalogNumbers': ['PE 2'], 'holder': 'a collector'},
    ]
  }
  assert [level for level, _ in material.catalog_numbers(node, repositories)] == ['error', 'error']


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
      {'catalogNumbers': ['ZZZZ 6'], 'holder': 'a collector'},
    ],
  }
  assert material.unresolved_catalog_numbers(node, repositories) == ['ZZZZ 3']


# -- locality_numbers -----------------------------------------------------------


def test_locality_numbers_unresolved_is_warning(registers):
  contexts = {'a': {'localityNumbers': ['USGS 5462', 'SH-1']}}
  assert material.locality_numbers(contexts, registers) == [
    ('warning', 'locality number "SH-1" resolves to no locality register'),
  ]
  assert material.locality_numbers(contexts, registers, ['own-l']) == []


def test_locality_numbers_a_catalog_prefix_is_no_locality_register(registers):
  contexts = {'a': {'localityNumbers': ['GM 12']}}
  assert material.locality_numbers(contexts, registers) == [
    ('warning', 'locality number "GM 12" resolves to no locality register'),
  ]


def test_locality_numbers_ambiguous_is_error_naming_the_entries(registers):
  registers = {**registers, 'usgs-2': {**_entry('USGS'), 'subject': 'localities'}}
  contexts = {'a': {'localityNumbers': ['USGS 1']}}
  assert material.locality_numbers(contexts, registers) == [
    ('error', 'locality number "USGS 1" has an ambiguous prefix: usgs-2, usgs-l'),
  ]
  assert material.locality_numbers(contexts, registers, ['usgs-l']) == []


def test_locality_numbers_no_contexts_or_numbers_is_quiet(registers):
  assert material.locality_numbers(None, registers) == []
  assert material.locality_numbers({'a': {'unit': ['x']}, 'b': None}, registers) == []


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


def test_cast_refs_number_inside_a_run_matches_and_exact_wins():
  node = {
    'material': [
      {'catalogNumbers': ['MCZ 629A'], 'castOf': 'PE 203'},
      {'catalogNumbers': [['PE 201', 'PE 205']]},
      {'catalogNumbers': ['MCZ 800'], 'castOf': 'PE 204'},
      {'catalogNumbers': [['PE 204', 'PE 210']]},
    ],
  }
  assert material.cast_refs(node) == []
  node['material'].append({'catalogNumbers': [['PE 202', 'PE 206']]})
  assert material.cast_refs(node) == [
    ('error', 'castOf "PE 203" matches 2 material entries, not 1'),
  ]


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
        'repositories': ['gm', 'nowhere'],
        'taxonomies': [
          {
            'taxon': 'cyathocystis',
            'ranges': None,
            'material': [
              {'catalogNumbers': ['ZZZZ 1'], 'context': 'missing-ctx'},
              {'catalogNumbers': ['MCZ 1'], 'castOf': 'MCZ 2'},
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
  assert any(
    '_synthetic_source at 0' in m and 'no resolvable repository prefix' in m for m in warnings
  )
  assert any('`ranges` is listed as `unused`' in m for m in errors)
  assert any('context "missing-ctx" is not defined' in m for m in errors)
  assert any('figure "of" value "nope"' in m for m in errors)
  assert any('cited entry carries `contexts`' in m for m in errors)
  assert any('castOf "MCZ 2" matches 0' in m for m in errors)
  assert any('repositories: `within` cycles: cyc -> cyc' in m for m in errors)
  assert any('listed repository "nowhere"' in m for m in errors)
  assert any('repository "gm" is listed but no catalog number' in m for m in errors)


def test_load_reports_locality_numbers_per_node_and_for_the_file(caplog):
  from phylohist.loader.load import _report_material

  data = {
    'repositories': {'usgs-l': {**_entry('USGS'), 'subject': 'localities'}},
    'trees': {
      '_synthetic_source': {
        'contexts': {'f': {'localityNumbers': ['USGS 1', 'ZZ-1']}},
        'taxonomies': [{'taxon': 'a', 'contexts': {'n': {'localityNumbers': ['YY-2']}}}],
      },
    },
  }
  with caplog.at_level(logging.WARNING, logger='phylohist'):
    _report_material(data)
  warnings = [r.getMessage() for r in caplog.records if r.levelno == logging.WARNING]
  assert any(
    m.startswith('_synthetic_source: locality number "ZZ-1" resolves to no') for m in warnings
  )
  assert any(
    m.startswith('_synthetic_source at 0: locality number "YY-2" resolves to no') for m in warnings
  )
  assert not any('"USGS 1"' in m for m in warnings)


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


def test_check_draft_warns_on_an_unresolved_locality_number_and_is_quiet_once_listed(tmp_path):
  body = (
    'contexts:\n  a:\n    localityNumbers: [SH-1]\n'
    'taxonomies:\n- taxon: cyathocystis\n  contexts:\n    b:\n      localityNumbers: [IK-3]\n'
  )
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(body)
  result = _run_check_draft(draft)
  assert result.stdout.count('resolves to no locality register') == 2, result.stdout
  assert 'warning: locality number "SH-1"' in result.stdout
  assert 'warning: 0: locality number "IK-3"' in result.stdout

  draft.write_text('repositories: [sprinkle-l]\n' + body)
  result = _run_check_draft(draft)
  assert 'resolves to no locality register' not in result.stdout, result.stdout


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
    # The old shape is not read.
    {'catalogNumbers': ['EE 1', 'numbers 2']},
  )
  assert material.number_entries(node, prefixes, numbered) == []
  assert material.number_entries({}, prefixes, numbered) == []


def test_number_entries_reads_the_explicit_repository_register_too(numbered):
  node = _node({'prefix': 'USNM', 'numbers': ['EE 1'], 'repository': 'nhmuk-ee'})
  assert material.number_entries(node, {'USNM': 'usnm'}, numbered) == [
    ('warning', 'number "EE 1" begins with a prefix of its register "nhmuk-ee"'),
  ]


def test_catalog_numbers_leaves_the_new_shape_alone_but_checks_its_repository(numbered):
  node = _node({'prefix': 'MCZ', 'numbers': ['ZZZ 1']}, {'numbers': ['1'], 'repository': 'nope'})
  assert material.catalog_numbers(node, numbered) == [
    ('error', 'repository "nope" is not a key of the registry'),
  ]
  assert material.unresolved_catalog_numbers(node, numbered) == []


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
    {'catalogNumbers': ['GM 1']},
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
        'FC-1',
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


def test_locality_numbers_leaves_the_object_form_to_its_own_check(registers):
  contexts = {'a': {'localityNumbers': [{'number': 'SH-1'}, {'prefix': 'USGS', 'number': 1}]}}
  assert material.locality_numbers(contexts, registers) == []
  document = {'repositories': ['own-l'], 'contexts': contexts}
  assert material.file_repositories_used(document, registers) == [
    ('error', 'repository "own-l" is listed but no catalog number in the file resolves to it'),
  ]


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


def test_entries_named_keeps_the_old_rule_for_the_old_shape_beside_the_new():
  old = {'catalogNumbers': [['GSC 1', 'GSC 5']], 'label': 'A'}
  new = {'prefix': 'GSC', 'numbers': [3]}
  entries = [old, new]
  assert material.entries_named(entries, 'GSC 3') == [old]
  assert material.entries_named(entries, 'GSC 5') == [old]
  assert material.entries_named(entries, 3) == [new]
  assert material.entries_named(entries, 'a') == []


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
          'USGS 1',
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
    {'catalogNumbers': ['MCZ 1'], 'numbers': [1]},
    {'prefix': 'MCZ'},
    {'prefix': 'MCZ', 'catalogNumbers': ['MCZ 1']},
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
  # `numbers` is no catalog number: nothing is listed as unresolved.
  assert 'prefixes: 0 without a resolvable repository' in result.stdout


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
