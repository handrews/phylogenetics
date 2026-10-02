"""Open nomenclature: the `cf`/`aff` link of an open form, `quotedParent`,
`nonMonophyletic`, and a material entry's `uncertain` and `roleUncertain`:
the schema, the loader checks, the claims, and the words the tools say.

Synthetic trees are built on the session's loaded corpus under positions
200 and up (`Tree` keeps class-level registries), and the tool tests read a
`ClaimStore` over a copy of `claims/` whose `1961_dehm` file is replaced by
the claims of one synthetic tree, since no `…-cf-…` record exists in the
data yet.
"""

import collections
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
from phylohist.loader.material import walk_document
from phylohist.loader.taxa import Taxon, Tree
from phylohist.store import CLAIMS_DIR, ClaimStore

SCRIPTS = Path(__file__).parent.parent / 'scripts'
SOURCE = '1961_dehm'
CF_KEY = 'lepidocystis-cf-wanneri_sprinkle_1973'
CF_RECORD = {'name': None, 'rank': 'species', 'auth': ['sprinkle'], 'year': 1973}

# Synthetic records for the checks: a genus, a species, an unnamed species,
# a bin, and a spelling of the species.
RECORDS = {
  'genus-a': {'name': 'Genusa'},
  'species_a': {'name': 'speciesa'},
  'open-sp-a': {'name': None, 'rank': 'species'},
  'open-bin': {'name': None, 'rank': 'Order'},
  'varietya': {'name': 'varietya', 'rank': 'variety'},
  'spelled_a': {'altSpellingOf': 'species_a'},
  'ranked_a': {'name': 'Rankeda', 'rank': 'Family'},
}
LOOKUP = nomenclature.record_lookup(RECORDS)


def _messages(result):
  return [m for _, m in result]


# -- schema -------------------------------------------------------------------


def _valid(document):
  return io.build_schema()[io.TREE_DEF].check(document)


def test_schema_accepts_the_new_node_and_material_fields():
  node = {
    'taxon': 'lepidocystis',
    'nonMonophyletic': True,
    'children': [
      {'openTaxon': 'gogia-sp_robison_1965', 'cf': 'grayae_bather_1915', 'new': True},
      {'openTaxon': 'gogia-sp_robison_1965', 'aff': 'grayae_bather_1915'},
      {
        'taxon': 'grayae_bather_1915',
        'quotedParent': True,
        'nonMonophyletic': 'paraphyletic',
        'material': [{'catalogNumbers': ['USNM 1'], 'role': 'topotype', 'roleUncertain': True}],
      },
      {'taxon': 'sardesoni_bather_1915', 'nonMonophyletic': 'polyphyletic'},
      {'taxon': 'sardesoni_bather_1915', 'material': [{'label': 'A', 'uncertain': True}]},
    ],
  }
  assert _valid({'taxonomies': [node]})


@pytest.mark.parametrize(
  'node',
  [
    {'taxon': 'a', 'nonMonophyletic': 'monophyletic'},
    {'taxon': 'a', 'nonMonophyletic': False},
    {'taxon': 'a', 'quotedParent': 'yes'},
    {'taxon': 'a', 'cf': True},
    {'taxon': 'a', 'material': [{'label': 'A', 'uncertain': 'maybe'}]},
    {'taxon': 'a', 'material': [{'label': 'A', 'roleUncertain': 1}]},
  ],
)
def test_schema_rejects_the_wrong_value_types(node):
  assert not _valid({'taxonomies': [node]})


# -- loader checks ------------------------------------------------------------


def test_record_lookup_computes_the_rank_as_the_loader_does():
  assert LOOKUP('species_a').rank == 'species'
  assert LOOKUP('genus-a').rank == 'genus'
  # A spelling has the rank of the record it spells.
  assert LOOKUP('spelled_a').rank == 'species'
  assert LOOKUP('open-bin').rank == 'Order'
  assert LOOKUP('nowhere') is None
  assert nomenclature.record_lookup({'x': {}})('x').rank is None


def test_record_lookup_agrees_with_the_loaded_taxa(load_records):
  data, _, _ = load_records
  lookup = nomenclature.record_lookup(data['taxa'])
  for key in ('grayae_bather_1915', 'rhenopyrgus', 'gogia-sp_robison_1965', 'cyathocystidae'):
    assert lookup(key).rank == Taxon.get(key).rank
    assert lookup(key).name == Taxon.get(key).name


def test_compared_links_clean_cases():
  assert nomenclature.compared_links({'openTaxon': 'open-sp-a', 'cf': 'species_a'}, LOOKUP) == []
  assert nomenclature.compared_links({'openTaxon': 'open-sp-a', 'aff': 'varietya'}, LOOKUP) == []
  # Neither species-level: a cf. genus compared with a named family-group taxon.
  assert nomenclature.compared_links({'openTaxon': 'open-bin', 'cf': 'ranked_a'}, LOOKUP) == []
  assert nomenclature.compared_links({'openTaxon': 'open-sp-a'}, LOOKUP) == []
  assert nomenclature.compared_links({'taxon': 'species_a'}, LOOKUP) == []


@pytest.mark.parametrize('sign', ['cf', 'aff'])
def test_compared_links_on_a_node_that_is_not_an_open_taxon(sign):
  assert nomenclature.compared_links({'taxon': 'species_a', sign: 'species_a'}, LOOKUP) == [
    ('error', f'`{sign}` on a node that is not an `openTaxon`'),
  ]


def test_compared_links_both_signs_is_an_error():
  node = {'openTaxon': 'open-sp-a', 'cf': 'species_a', 'aff': 'varietya'}
  assert nomenclature.compared_links(node, LOOKUP) == [('error', 'both `cf` and `aff` on one node')]


def test_compared_links_target_without_a_record_or_a_name_is_an_error():
  [missing] = nomenclature.compared_links({'openTaxon': 'open-sp-a', 'cf': 'nowhere'}, LOOKUP)
  assert missing[0] == 'error' and '"nowhere" has no taxon record' in missing[1]
  [unnamed] = nomenclature.compared_links({'openTaxon': 'open-sp-a', 'aff': 'open-sp-a'}, LOOKUP)
  assert unnamed[0] == 'error' and 'is itself a placeholder' in unnamed[1]


def test_compared_links_rank_group_disagreement_is_an_error():
  [message] = _messages(
    nomenclature.compared_links({'openTaxon': 'open-sp-a', 'cf': 'genus-a'}, LOOKUP)
  )
  assert '"genus-a" (genus)' in message and '"open-sp-a" (species)' in message
  assert nomenclature.compared_links({'openTaxon': 'open-bin', 'cf': 'species_a'}, LOOKUP)


def test_compared_links_leaves_a_target_that_is_not_a_key_to_the_schema():
  assert nomenclature.compared_links({'openTaxon': 'open-sp-a', 'cf': None}, LOOKUP) == []


def test_compared_links_skips_the_rank_check_for_a_missing_open_record():
  assert nomenclature.compared_links({'openTaxon': 'not-yet', 'cf': 'genus-a'}, LOOKUP) == []


def test_quoted_parent():
  assert nomenclature.quoted_parent({'taxon': 'species_a', 'quotedParent': True}, LOOKUP) == []
  assert nomenclature.quoted_parent({'taxon': 'varietya', 'quotedParent': True}, LOOKUP) == []
  assert nomenclature.quoted_parent({'openTaxon': 'open-sp-a', 'quotedParent': True}, LOOKUP) == []
  assert nomenclature.quoted_parent({'taxon': 'genus-a', 'quotedParent': False}, LOOKUP) == []
  assert nomenclature.quoted_parent({'taxon': 'nowhere', 'quotedParent': True}, LOOKUP) == []
  assert nomenclature.quoted_parent({'quotedParent': True}, LOOKUP) == []
  assert nomenclature.quoted_parent({'taxon': 'genus-a', 'quotedParent': True}, LOOKUP) == [
    ('error', '`quotedParent` on a node that is not a species-level name'),
  ]


def test_role_uncertain_needs_a_role():
  node = {
    'material': [
      {'label': 'A', 'role': 'topotype', 'roleUncertain': True},
      {'label': 'B', 'roleUncertain': True},
      {'label': 'C'},
    ],
  }
  assert nomenclature.role_uncertain(node) == [
    ('error', 'material entry has `roleUncertain` but no `role`'),
  ]
  assert nomenclature.role_uncertain({'material': None}) == []
  assert nomenclature.role_uncertain({}) == []


def _tree_file(*nodes):
  return {'taxonomies': [{'taxon': 'genus-a', 'children': list(nodes)}]}


def test_compared_link_conflicts_warn_once_for_different_links():
  documents = [
    ('src1', _tree_file({'openTaxon': 'open-sp-a', 'cf': 'species_a'})),
    ('src2', _tree_file({'openTaxon': 'open-sp-a', 'aff': 'species_a'})),
    ('src3', _tree_file({'openTaxon': 'open-sp-a', 'cf': 'varietya'})),
  ]
  [(level, message)] = nomenclature.compared_link_conflicts(documents)
  assert level == 'warning'
  assert 'open form "open-sp-a"' in message
  for link in ('cf species_a (src1 at 0/children/0)', 'aff species_a (src2', 'cf varietya (src3'):
    assert link in message


def test_compared_link_conflicts_leave_agreement_and_unlinked_uses_alone():
  agreeing = [
    ('src1', _tree_file({'openTaxon': 'open-sp-a', 'cf': 'species_a'})),
    ('src2', _tree_file({'openTaxon': 'open-sp-a', 'cf': 'species_a'}, {'openTaxon': 'open-sp-a'})),
  ]
  assert nomenclature.compared_link_conflicts(agreeing) == []
  # Another record, or a node that is not an open form, is no conflict.
  other = [
    ('src1', _tree_file({'openTaxon': 'open-sp-a', 'cf': 'species_a'})),
    ('src2', _tree_file({'openTaxon': 'open-bin', 'cf': 'varietya'}, {'taxon': 'species_a'})),
  ]
  assert nomenclature.compared_link_conflicts(other) == []
  assert nomenclature.compared_link_conflicts([]) == []


def test_load_reports_nomenclature_checks_at_the_right_level(load_records, caplog):
  # Direct call, as for `_report_material`: a synthetic corpus routed
  # through `load()` would leak into the session's registries.
  data = {
    'trees': {
      'src1': {
        'taxonomies': [
          {
            'taxon': 'rhenopyrgus',
            'children': [
              {'openTaxon': 'gogia-sp_robison_1965', 'cf': 'grayae_bather_1915'},
              {'taxon': 'grayae_bather_1915', 'aff': 'sardesoni_bather_1915'},
              {'taxon': 'sardesoni_bather_1915', 'quotedParent': True},
              {'taxon': 'cyathocystidae', 'quotedParent': True},
              {'openTaxon': 'gogia-sp_robison_1965', 'cf': 'rhenopyrgus'},
              {
                'taxon': 'sardesoni_bather_1915',
                'material': [{'label': 'A', 'roleUncertain': True}],
              },
            ],
          },
        ],
      },
      'src2': {
        'taxonomies': [{'openTaxon': 'gogia-sp_robison_1965', 'aff': 'grayae_bather_1915'}],
      },
    },
  }
  with caplog.at_level(logging.WARNING, logger='phylohist'):
    _report_nomenclature(data)
  warnings = [r.getMessage() for r in caplog.records if r.levelno == logging.WARNING]
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert any(
    'src1 at 0/children/1: `aff` on a node that is not an `openTaxon`' in m for m in errors
  )
  assert any('src1 at 0/children/3: `quotedParent` on a node that is not' in m for m in errors)
  assert any('src1 at 0/children/4: `cf` target "rhenopyrgus" (genus)' in m for m in errors)
  assert any('src1 at 0/children/5: material entry has `roleUncertain`' in m for m in errors)
  assert len(errors) == 4
  [conflict] = warnings
  assert 'open form "gogia-sp_robison_1965"' in conflict and 'src2 at 0' in conflict


def test_the_corpus_has_no_nomenclature_messages(load_records):
  # The data does not use the new fields yet; the loader's own logs
  # (`test_no_errors`) carry the rest.
  data, _, _ = load_records
  found = []
  for opinion in data['trees'].values():
    for _, node, _ in walk_document(opinion):
      found += nomenclature.compared_links(node, Taxon.get)
      found += nomenclature.quoted_parent(node, Taxon.get)
      found += nomenclature.role_uncertain(node)
  assert found == []
  assert nomenclature.compared_link_conflicts(data['trees'].items()) == []


# -- scripts/check_draft.py ---------------------------------------------------


def _run_check_draft(path):
  return subprocess.run(
    [sys.executable, str(SCRIPTS / 'check_draft.py'), str(path)],
    capture_output=True,
    text=True,
  )


def _draft(tmp_path, body):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text('taxonomies:\n- taxon: rhenopyrgus\n  children:\n' + body)
  return _run_check_draft(draft)


def test_check_draft_accepts_a_linked_open_form(tmp_path):
  result = _draft(
    tmp_path,
    '  - openTaxon: gogia-sp_robison_1965\n'
    '    cf: grayae_bather_1915\n'
    '  - taxon: sardesoni_bather_1915\n'
    '    quotedParent: true\n'
    '    nonMonophyletic: paraphyletic\n',
  )
  assert result.returncode == 0, result.stdout + result.stderr


def test_check_draft_reports_the_link_checks(tmp_path):
  result = _draft(
    tmp_path,
    '  - taxon: grayae_bather_1915\n'
    '    aff: sardesoni_bather_1915\n'
    '  - openTaxon: gogia-sp_robison_1965\n'
    '    cf: gogia-sp_robison_1965\n',
  )
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'children/0: `aff` on a node that is not an `openTaxon`' in result.stdout
  assert 'children/1: `cf` target "gogia-sp_robison_1965" is itself a placeholder' in result.stdout


def test_check_draft_reports_quoted_parent_and_role_uncertain(tmp_path):
  result = _draft(
    tmp_path,
    '  - taxon: cyathocystidae\n'
    '    quotedParent: true\n'
    '  - taxon: grayae_bather_1915\n'
    '    material:\n'
    '    - label: A\n'
    '      roleUncertain: true\n',
  )
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'children/0: `quotedParent` on a node that is not a species-level name' in result.stdout
  assert 'children/1: material entry has `roleUncertain` but no `role`' in result.stdout


def test_check_draft_warns_of_conflicting_links_without_failing(tmp_path):
  result = _draft(
    tmp_path,
    '  - openTaxon: gogia-sp_robison_1965\n'
    '    cf: grayae_bather_1915\n'
    '  - openTaxon: gogia-sp_robison_1965\n'
    '    aff: grayae_bather_1915\n',
  )
  assert result.returncode == 0, result.stdout + result.stderr
  assert 'warning: open form "gogia-sp_robison_1965" is compared with different taxa' in (
    result.stdout
  )


# -- claims -------------------------------------------------------------------


def _claims(root, position, source=SOURCE):
  return extract(
    {source: [Tree(root, {'source_key': source, 'type': 'taxonomy', 'position': position})]}
  )[source]


def _by_path(claims):
  at = collections.defaultdict(list)
  for claim in claims:
    at[claim['path']].append(claim)
  return at


def _one(claims, kind):
  [claim] = [c for c in claims if c['kind'] == kind]
  return claim


def test_usage_claim_carries_the_compared_link(load_records, caplog):
  root = {
    'taxon': 'rhenopyrgus',
    'children': [
      {'openTaxon': 'gogia-sp_robison_1965', 'cf': 'grayae_bather_1915'},
      {'openTaxon': 'asteriadae-gen-sp_sowerby.g.b_1825', 'aff': 'sardesoni_bather_1915'},
      {'openTaxon': 'gogia-sp-1_sprinkle_1973'},
    ],
  }
  at = _by_path(_claims(root, 200))
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  cf = _one(at['200/children/0'], 'usage')
  assert cf['form'] == 'openTaxon' and 'target' not in cf
  assert cf['compared'] == {'sign': 'cf', 'taxon': 'grayae_bather_1915'}
  aff = _one(at['200/children/1'], 'usage')
  assert aff['compared'] == {'sign': 'aff', 'taxon': 'sardesoni_bather_1915'}
  assert 'compared' not in _one(at['200/children/2'], 'usage')


@pytest.mark.parametrize('field', ['cfTaxon', 'affTaxon'])
def test_the_retired_cf_and_aff_taxon_fields_are_rejected(field):
  assert not _valid({'taxonomies': [{'taxon': 'rhenopyrgus', 'children': [{field: 'x'}]}]})


@pytest.mark.parametrize('field', ['cfTaxon', 'affTaxon'])
def test_the_loader_does_not_read_the_retired_fields_as_a_name(field, load_records, caplog):
  # As for any node with no recognised taxon field: it has no taxon of its
  # own and states no usage; the schema is what rejects it.
  root = {'taxon': 'rhenopyrgus', 'children': [{field: 'grayae_bather_1915'}]}
  at = _by_path(_claims(root, 201))
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  assert not [c for c in at['201/children/0'] if c['kind'] == 'usage']


def test_placement_claim_carries_quoted_parent_and_non_monophyly(load_records):
  root = {
    'taxon': 'cyathocystidae',
    'children': [
      {'taxon': 'rhenopyrgus', 'nonMonophyletic': True},
      {'taxon': 'pyrgocystis', 'nonMonophyletic': 'polyphyletic'},
      {'taxon': 'grayae_bather_1915', 'quotedParent': True},
      {'taxon': 'sardesoni_bather_1915'},
    ],
  }
  at = _by_path(_claims(root, 202))
  assert _one(at['202/children/0'], 'placement')['nonMonophyletic'] is True
  assert _one(at['202/children/1'], 'placement')['nonMonophyletic'] == 'polyphyletic'
  quoted = _one(at['202/children/2'], 'placement')
  assert quoted['quotedParent'] is True and 'nonMonophyletic' not in quoted
  plain = _one(at['202/children/3'], 'placement')
  assert 'quotedParent' not in plain and 'nonMonophyletic' not in plain


def test_acceptance_claim_carries_quoted_parent(load_records):
  root = {
    'taxon': 'grayae_bather_1915',
    'synonyms': [
      {'taxon': 'sardesoni_bather_1915', 'quotedParent': True, 'nonMonophyletic': True},
    ],
  }
  entry = _one(_by_path(_claims(root, 203))['203/synonyms/0'], 'acceptance')
  assert entry['quotedParent'] is True
  assert 'nonMonophyletic' not in entry


def test_specimen_claim_carries_uncertain_and_role_uncertain(load_records):
  root = {
    'taxon': 'grayae_bather_1915',
    'material': [
      {'catalogNumbers': ['USNM 165425'], 'role': 'topotype', 'roleUncertain': True},
      {'catalogNumbers': ['USNM 165426'], 'uncertain': True},
      {'catalogNumbers': ['USNM 165427']},
    ],
  }
  first, second, third = [c for c in _claims(root, 204) if c['kind'] == 'material']
  assert first['roleUncertain'] is True and 'uncertain' not in first
  assert second['uncertain'] is True and 'roleUncertain' not in second
  assert 'uncertain' not in third and 'roleUncertain' not in third


# -- the tools ----------------------------------------------------------------


SYNTHETIC = {
  'taxon': 'cyathocystidae',
  'children': [
    {
      'taxon': 'rhenopyrgus',
      'nonMonophyletic': 'paraphyletic',
      'children': [
        {'taxon': 'grayae_bather_1915', 'quotedParent': True},
        {
          'taxon': 'sardesoni_bather_1915',
          'synonyms': [{'taxon': 'grayae_bather_1915', 'quotedParent': True}],
        },
      ],
    },
    {'taxon': 'pyrgocystis', 'nonMonophyletic': True},
    {
      'taxon': 'lepidocystis',
      'children': [
        {'taxon': 'wanneri_foerste_1938'},
        {'openTaxon': CF_KEY, 'cf': 'wanneri_foerste_1938', 'pages': 5},
      ],
    },
  ],
}


# A second source that only cites the compared form, in a synonymy.
CITING = '1985_jell_burrett_banks'
CITING_TREE = {
  'taxon': 'rhenopyrgus',
  'synonyms': [{'openTaxon': CF_KEY, 'aff': 'wanneri_foerste_1938'}],
}


@pytest.fixture(scope='module')
def synthetic(load_records, tmp_path_factory):
  """A `ClaimStore` over a copy of `claims/` with `SOURCE`'s claims
  replaced by those of `SYNTHETIC`, and the record `CF_KEY` registered."""
  directory = tmp_path_factory.mktemp('claims')
  shutil.copytree(CLAIMS_DIR, directory, dirs_exist_ok=True)
  with pytest.MonkeyPatch.context() as patch:
    patch.setitem(Taxon._taxa, CF_KEY, Taxon(dict(CF_RECORD), CF_KEY))
    written = {SOURCE: _claims(SYNTHETIC, 220), CITING: _claims(CITING_TREE, 221, CITING)}
  for source_key, claims in written.items():
    (directory / f'{source_key}.jsonl').write_text(''.join(json.dumps(c) + '\n' for c in claims))
  names = json.loads((directory / 'names.json').read_text())
  names[CF_KEY] = dict(names['gogia-sp_robison_1965'])
  (directory / 'names.json').write_text(json.dumps(names))
  return ClaimStore(directory)


def test_quoted_parent_quotes_the_genus_of_a_placed_species(synthetic):
  [block] = synthetic.contents(SOURCE, 'rhenopyrgus')
  assert '"Rhenopyrgus" grayae' in block['rendered']
  assert 'Rhenopyrgus sardesoni' in block['rendered']
  assert '"Rhenopyrgus grayae"' not in block['rendered']
  # Only the genus: neither the whole label nor the epithet carries quotes.
  assert synthetic.words.display('grayae_bather_1915', SOURCE, '220/children/0/children/0') == (
    '"Rhenopyrgus" grayae'
  )


def test_quoted_parent_quotes_the_genus_of_a_cited_entry(synthetic):
  [block] = synthetic.contents(SOURCE, 'rhenopyrgus', synonymy=True)
  [line] = [ln for ln in block['rendered'].splitlines() if ln.lstrip().startswith('=')]
  assert '"Rhenopyrgus" grayae' in line
  assert synthetic.words.display(
    'grayae_bather_1915', SOURCE, '220/children/0/children/1/synonyms/0'
  ) == ('"Rhenopyrgus" grayae')


def test_a_quoted_combination_still_resolves_by_its_unquoted_form(synthetic):
  assert [c['key'] for c in synthetic.resolve_name('Rhenopyrgus grayae')] == ['grayae_bather_1915']
  assert [c['key'] for c in synthetic.resolve_name('"Rhenopyrgus" grayae')] == [
    'grayae_bather_1915'
  ]
  history = synthetic.history('grayae_bather_1915', style='text')
  assert history['entries']


def test_non_monophyly_in_a_classification_line_and_a_chain(synthetic):
  [block] = synthetic.contents(SOURCE, 'cyathocystidae')
  lines = block['rendered'].splitlines()
  assert any('Rhenopyrgus (paraphyletic)' in ln for ln in lines)
  assert any('Pyrgocystis (non-monophyletic)' in ln for ln in lines)
  assert not any('Lepidocystis (' in ln for ln in lines)
  chain = synthetic.ancestors(['grayae_bather_1915'])['rendered']
  assert 'Rhenopyrgus (paraphyletic)' in chain


def test_non_monophyly_in_a_placement_sentence(synthetic):
  words = synthetic.words
  assert words.claim_words(
    {'kind': 'placement', 'parent': 'cyathocystidae', 'tree': 'taxonomy', 'nonMonophyletic': True}
  ) == ('places it under Cyathocystidae (non-monophyletic)')
  assert words.claim_words(
    {
      'kind': 'placement',
      'parent': 'cyathocystidae',
      'tree': 'taxonomy',
      'nonMonophyletic': 'paraphyletic',
      'provisional': True,
    }
  ) == ('places it under Cyathocystidae (provisional, paraphyletic)')
  assert words.claim_words(
    {'kind': 'placement', 'parent': 'rhenopyrgus', 'tree': 'taxonomy', 'quotedParent': True}
  ) == ('places it under Rhenopyrgus (genus in quotes)')
  # The placement claim of a synthetic node reads the same way.
  claim = next(
    c
    for c in synthetic.by_subject['rhenopyrgus']
    if c['kind'] == 'placement' and c['source'] == SOURCE
  )
  assert words.claim_words(claim) == 'places it under Cyathocystidae (paraphyletic)'


def test_specimen_words_for_a_queried_role_and_a_doubtful_assignment(synthetic):
  words = synthetic.words
  claim = {
    'kind': 'material',
    'materialKind': 'specimen',
    'role': 'topotype',
    'ids': ['USNM 165425'],
  }
  assert words.claim_words(claim) == 'topotype: USNM 165425'
  assert words.claim_words({**claim, 'roleUncertain': True}) == 'topotype?: USNM 165425'
  assert words.claim_words({**claim, 'uncertain': True}) == (
    'topotype: USNM 165425 (doubtfully assigned)'
  )
  assert words.claim_words(
    {**claim, 'roleUncertain': True, 'uncertain': True, 'figured': False}
  ) == ('topotype?: USNM 165425 (doubtfully assigned) (not figured)')


def test_an_open_form_is_labelled_from_the_words_of_its_key(synthetic):
  [block] = synthetic.contents(SOURCE, 'lepidocystis')
  assert 'Lepidocystis cf. wanneri' in block['rendered']
  assert synthetic.words.display(CF_KEY, SOURCE, '220/children/2/children/1') == (
    'Lepidocystis cf. wanneri'
  )


def test_history_lists_a_compared_form_under_its_own_name(synthetic):
  block = synthetic.history('wanneri_foerste_1938')
  own, compared = [e for e in block['entries'] if e['source'] == SOURCE]
  assert own['record'] == 'wanneri_foerste_1938' and 'compared' not in own
  assert compared['record'] == CF_KEY and compared['compared'] == 'cf'
  assert compared['line'].startswith('Lepidocystis cf. wanneri')
  assert compared['page'] == 5
  assert 'Lepidocystis cf. wanneri' in block['rendered']
  # The heading's measurement is the name's own.
  assert CF_KEY not in block['measurement']['records']


def test_history_lists_a_compared_form_a_source_only_cites_in_a_synonymy(synthetic):
  entries = synthetic.history('wanneri_foerste_1938')['entries']
  [cited] = [e for e in entries if e['source'] == CITING]
  # The node's own link: this source's line says `aff`, the other's `cf`.
  assert cited['record'] == CF_KEY and cited['compared'] == 'aff'


def test_history_leaves_the_compared_form_out_without_related(synthetic):
  block = synthetic.history('wanneri_foerste_1938', include_related=False)
  assert {e['record'] for e in block['entries']} == {'wanneri_foerste_1938'}
  assert CF_KEY not in json.dumps(block)


def test_history_of_the_open_form_itself_is_not_marked_compared(synthetic):
  entries = synthetic.history(CF_KEY)['entries']
  assert entries and {e['record'] for e in entries} == {CF_KEY}
  assert not [e for e in entries if 'compared' in e]


def test_other_tools_do_not_pull_the_compared_form_in(synthetic):
  # A compared form is not the taxon: its claims are its own.
  [open_claim] = [
    c for c in synthetic.by_subject[CF_KEY] if c['kind'] == 'usage' and c['source'] == SOURCE
  ]
  named = synthetic.statements('wanneri_foerste_1938')
  claim_ids = {i for entry in named['entries'] for i in entry.get('claims', ())}
  assert open_claim['id'] not in claim_ids
  assert CF_KEY not in json.dumps(named)
  assert CF_KEY not in synthetic.closure.expand(['wanneri_foerste_1938'], True)
  assert CF_KEY not in synthetic.closure.descendants(['wanneri_foerste_1938'])
  assert CF_KEY not in json.dumps(synthetic.synonymy('wanneri_foerste_1938'))
  assert (
    'Lepidocystis cf. wanneri' not in synthetic.placements(['wanneri_foerste_1938'])['rendered']
  )


def test_resolve_shows_what_an_open_form_is_compared_with(synthetic):
  row = synthetic.resolver._candidate(CF_KEY)
  assert row['compared'] == {
    'sign': 'cf',
    'taxon': 'wanneri_foerste_1938',
    'name': 'Lepidocystis wanneri',
  }
  assert 'compared' not in synthetic.resolver._candidate('wanneri_foerste_1938')
  # The link lives on nodes, not in the names index.
  assert 'compared' not in synthetic.names[CF_KEY]
