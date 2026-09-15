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
    'Guensburg & Sprinkle 1994\n'
    '  Family Astrocystitidae emend.\n'
    '    Genus Astrocystites\n'
    '    Genus Cambroblastus\n'
    '    Genus Lampteroblastus gen. nov.\n'
    '      Type species. Lampteroblastus hintzei\n'
    '      Lampteroblastus hintzei sp. nov.'
  )
  assert render.render(block, 'markdown').startswith(
    '**Guensburg & Sprinkle 1994**\n```\nFamily Astrocystitidae emend.\n'
  )
  assert 'rendered' not in block


def test_provisional_and_placeholder_marks(store):
  bassler = store.contents('1935_bassler', 'astrocystitidae', style='json')[0]
  assert render.render(bassler, 'text').splitlines()[:2] == [
    'Bassler 1935',
    '  Family Astrocystitidae fam. nov. nom. correct.',
  ]
  holloway = store.contents('1983_holloway_jell', 'edrioasteroidea', depth=1, style='json')[0]
  lines = render.render(holloway, 'text').splitlines()
  assert lines[2] == '    Order uncertain'


def test_table_text_and_markdown(store):
  found = store.descendants(['edrioblastoidea'], style='json')
  text = render.render(found, 'text').splitlines()
  assert text[0] == 'Placed under Edrioblastoidea'
  assert text[1].split() == ['record', 'rank', 'placed', 'by', 'sources']
  md = render.render(found, 'markdown').splitlines()
  assert md[0] == '**Placed under Edrioblastoidea**'
  assert md[2] == '| record | rank | placed by | sources |'
  statements = store.statements('rhenopyrgidae', act_kind='new', style='json')
  assert render.render(statements, 'text').splitlines() == [
    'Statements about Rhenopyrgidae Holloway & Jell 1983',
    '  1983  Holloway & Jell  named as new',
  ]
  assert (
    render.render(statements, 'markdown').splitlines()[2] == '- 1983 Holloway & Jell: named as new'
  )
  casteri = next(
    line for line in render.render(found, 'markdown').splitlines() if 'casteri' in line
  )
  assert '| Bell 1975: under Timeischytes<br>Müller et al. 2013: under Timeischytes |' in casteri
  text = next(line for line in render.render(found, 'text').splitlines() if 'casteri' in line)
  assert 'Bell 1975: under Timeischytes / Müller et al. 2013: under Timeischytes' in text


def test_chains_text_and_markdown(store):
  block = store.placed_under('rhenopyrgus', 'edrioblastoidina', style='json')
  text = render.render(block, 'text').splitlines()
  assert text[3] == '1994  Guensburg & Sprinkle  Cyathocystidae › Rhenopyrginae › Rhenopyrgus'
  md = render.render(block, 'markdown').splitlines()
  assert md[0].startswith('**Rhenopyrgus Dehm 1961 under Edrioblastoidina Fay 1962: 4 papers')
  assert md[3] == '| year | source | chain |'
  assert md[5] == '| 1994 | Guensburg & Sprinkle | Cyathocystidae › Rhenopyrginae › Rhenopyrgus |'
  assert blocks.validate(block, store) == []


def test_list_text(store):
  block = store.synonymy(
    'grayae_bather_1915', source='2020_ewin_martin.m_isotalo_zamora', style='json'
  )[0]
  lines = render.render(block, 'text').splitlines()
  assert lines[0] == 'Synonymy under Rhenopyrgus grayae in Ewin et al. 2020'
  assert lines[1] == '  1915 Pyrgocystis grayae Bather 1915 p. 58'
  assert (
    render.render(block, 'markdown').splitlines()[2]
    == '- 1915 Pyrgocystis grayae Bather 1915 p. 58'
  )


def test_statement_text(store):
  block = store.gap('1983_holloway_jell', 'material', style='json')
  assert render.render(block, 'text') == (
    'The material printed in Holloway & Jell 1983 has not yet been entered '
    '(none of it is entered so far).'
  )
  assert render.render(block, 'markdown') == render.render(block, 'text')
  unknown = store.gap('no_such_source', 'material', style='json')
  assert (
    render.render(unknown, 'text') == 'No source in the corpus mentions the source no_such_source.'
  )


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
  assert text.startswith(
    'Rhenopyrgidae in Holloway & Jell 1983; material coverage.\n\nThe material'
  )
  assert text.endswith(
    'Holloway & Jell 1983\n  Family Rhenopyrgidae fam. nov.\n    Genus Rhenopyrgus\n'
    '      Type species. Rhenopyrgus coronaeformis\n      Rhenopyrgus coronaeformis\n'
    '      Rhenopyrgus grayae\n      Rhenopyrgus whitei sp. nov.'
  )
  assert (
    composition['compositionId'] == blocks.compose([a, b], composition['header'])['compositionId']
  )


def test_a_new_style_registers(store):
  @render.style('count', 'statement')
  def count_statement(block):
    return f'{len(block["fields"])} fields'

  try:
    block = store.gap('1983_holloway_jell', 'material', style='json')
    assert render.render(block, 'count').endswith(' fields')
    assert 'count' in render.styles()
    with pytest.raises(KeyError):
      render.render(store.statements('rhenopyrgus', style='json'), 'count')
  finally:
    del render.STYLES[('statement', 'count')]
