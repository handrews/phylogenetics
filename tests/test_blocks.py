"""Blocks are data with stable ids; styles render them through a registry.

One golden per block type in each shipped style (short, hand-checked
against the worked examples), the validator rejecting a foreign claim and
a tampered block, ids stable across calls, and a style registered at
test time rendering through the registry like the shipped ones.
"""

import os

import pytest

from phylohist import blocks, render
from phylohist.tools import ClaimStore

pytestmark = pytest.mark.skipif(
  bool(os.getenv('PHYLOHIST_DRAFTS')),
  reason='the committed claim table covers data/ only',
)


@pytest.fixture(scope='module')
def store():
  return ClaimStore()


def test_classification_text_and_markdown(store):
  block = store.contents('1994_guensburg_sprinkle', 'astrocystitidae', style='json')[0]
  assert render.render(block, 'text') == (
    'Astrocystitidae emend.\n  Astrocystites\n  Cambroblastus\n  Lampteroblastus*\n'
    '    Lampteroblastus hintzei* [type]'
  )
  assert render.render(block, 'markdown').startswith('```\nAstrocystitidae emend.\n')
  assert 'rendered' not in block


def test_provisional_and_placeholder_marks(store):
  bassler = store.contents('1935_bassler', 'astrocystitidae', style='json')[0]
  assert render.render(bassler, 'text').splitlines()[0] == 'Astrocystitidae* nom. correct.'
  holloway = store.contents('1983_holloway_jell', 'edrioasteroidea', depth=1, style='json')[0]
  lines = render.render(holloway, 'text').splitlines()
  assert lines[1] == '  [edrioasteroidea-order-uncertain_holloway_jell_1983]'


def test_table_text_and_markdown(store):
  block = store.statements('rhenopyrgidae', act_kind='new', style='json')
  text = render.render(block, 'text').splitlines()
  assert text[0] == 'Statements about Rhenopyrgidae'
  assert text[1].split() == ['source', 'as', 'kind', 'statement', 'page', 'by']
  assert text[3].startswith('Holloway & Jell 1983  Rhenopyrgidae  act   named as new')
  md = render.render(block, 'markdown').splitlines()
  assert md[0] == '**Statements about Rhenopyrgidae**'
  assert md[2] == '| source | as | kind | statement | page | by |'
  assert md[4].startswith('| Holloway & Jell 1983 | Rhenopyrgidae | act | named as new |')


def test_list_text(store):
  block = store.synonymy('grayae_bather_1915', source='2020_ewin_martin.m_isotalo_zamora', style='json')[0]
  lines = render.render(block, 'text').splitlines()
  assert lines[0] == 'Rhenopyrgus grayae'
  assert lines[1] == '  1915 Pyrgocystis grayae Bather 1915 p. 58'
  assert render.render(block, 'markdown').splitlines()[2] == '- 1915 Pyrgocystis grayae Bather 1915 p. 58'


def test_statement_text(store):
  block = store.gap('1983_holloway_jell', 'material', style='json')
  assert render.render(block, 'text') == (
    'The material printed in Holloway & Jell 1983 has not yet been entered '
    '(none of it is entered so far).'
  )
  assert render.render(block, 'markdown') == render.render(block, 'text')
  unknown = store.gap('no_such_source', 'material', style='json')
  assert render.render(unknown, 'text') == 'No source in the corpus mentions the source no_such_source.'


def test_ids_stable_and_validated(store):
  first = store.history('rhenopyrgus', style='json')
  second = store.history('rhenopyrgus', style='json')
  assert first['blockId'] == second['blockId']
  assert blocks.validate(first, store) == []
  tampered = dict(first)
  tampered['claims'] = list(first['claims']) + ['1983_holloway_jell:0:usage:99']
  problems = blocks.validate(tampered, store)
  assert 'blockId does not match content' in problems
  assert any(p.startswith('unknown claim') for p in problems)


def test_composition(store):
  a = store.gap('1983_holloway_jell', 'material', style='json')
  b = store.contents('1983_holloway_jell', 'rhenopyrgidae', style='json')[0]
  composition = blocks.compose([a, b], 'Rhenopyrgidae in Holloway & Jell 1983; material coverage.')
  text = render.render_composition(composition, 'text')
  assert text.startswith('Rhenopyrgidae in Holloway & Jell 1983; material coverage.\n\nThe material')
  assert text.endswith('Rhenopyrgidae*\n  Rhenopyrgus\n    Rhenopyrgus coronaeformis [type]\n'
                       '    Rhenopyrgus grayae\n    Rhenopyrgus whitei*')
  assert composition['compositionId'] == blocks.compose([a, b], composition['header'])['compositionId']


def test_a_new_style_registers(store):
  @render.style('count', 'statement')
  def count_statement(block):
    return f"{len(block['fields'])} fields"
  try:
    block = store.gap('1983_holloway_jell', 'material', style='json')
    assert render.render(block, 'count').endswith(' fields')
    assert 'count' in render.styles()
    with pytest.raises(KeyError):
      render.render(store.statements('rhenopyrgus', style='json'), 'count')
  finally:
    del render.STYLES[('statement', 'count')]
