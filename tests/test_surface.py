"""The tool surface is declared once and every surface agrees with it.

`tools.TOOL_SPECS` is the contract: the tool names and the parameters
each takes. The module-level functions, the `call` table, the CLI's
subcommands and the MCP server's wrappers must all offer exactly those
tools with exactly those parameters (the CLI adds `--style`, which is
the rendering, never a parameter). The MCP server is a script, loaded
here as a module.
"""

import argparse
import inspect
import pathlib

import pytest

from phylohist import blocks, cli, tools
from phylohist.acts import ACT_KINDS
from tests import support

PLANNER_PROMPT = pathlib.Path(__file__).parent.parent / 'eval' / 'planner-prompt.md'
SPECS = {spec['name']: spec for spec in tools.TOOL_SPECS}


@pytest.fixture(scope='module')
def mcp():
  return support.script('mcp_server')


def _parameters(function):
  return set(inspect.signature(function).parameters) - {'style'}


def test_every_surface_offers_the_same_tools(mcp):
  names = set(SPECS)
  assert set(tools.TOOLS) == names
  assert set(cli.SUBCOMMANDS.values()) == names
  assert {n for n in names if callable(getattr(mcp, n, None))} == names
  assert {n for n in names if callable(getattr(tools, n, None))} == names
  assert set(tools.TOOL_DESCRIPTIONS) == names
  subparsers = next(
    a for a in cli.build_parser()._actions if isinstance(a, argparse._SubParsersAction)
  )
  assert set(subparsers.choices) == set(cli.SUBCOMMANDS) | {'plan', 'tools'}


@pytest.mark.parametrize('name', sorted(SPECS))
def test_every_surface_takes_the_specified_parameters(name, mcp):
  expected = set(SPECS[name]['input_schema']['properties'])
  assert _parameters(tools.TOOLS[name]) == expected, 'module function'
  assert _parameters(getattr(mcp, name)) == expected, 'MCP wrapper'
  assert 'style' not in expected


def test_every_act_kind_is_offered(store):
  # The acts the claim table carries and the acts a listing marks are
  # all `ACT_KINDS`, and the planner is offered every one as the tool is.
  assert {c['actKind'] for c in store.by_id.values() if c['kind'] == 'act'} <= set(ACT_KINDS)
  assert set(blocks.ACT_MARKS) <= set(ACT_KINDS)
  assert f'act_kind ({", ".join(ACT_KINDS)})' in PLANNER_PROMPT.read_text()


def test_every_statement_kind_is_offered(store):
  # The kinds `statements` selects by are the claim kinds a record's
  # statements carry plus the material kinds asked for by name; the tool
  # description, the planner prompt and the gap mapping list the same.
  from phylohist.store import _COVERAGE_OF_KIND, _MATERIAL_KINDS, STATEMENT_KINDS

  assert {c['kind'] for c in store.by_id.values()} - {'section'} <= set(STATEMENT_KINDS)
  assert set(_COVERAGE_OF_KIND) == set(STATEMENT_KINDS)
  claim_kinds = [k for k in STATEMENT_KINDS if k not in _MATERIAL_KINDS]
  listed = f'({", ".join(claim_kinds)}; or {", ".join(_MATERIAL_KINDS)} for one kind of material)'
  assert listed in tools.TOOL_DESCRIPTIONS['statements']
  assert listed in PLANNER_PROMPT.read_text()


@pytest.mark.parametrize(
  ('command', 'dest'), [('statements', 'kind'), ('statements', 'act_kind'), ('gap', 'kind')]
)
def test_cli_choices_are_the_specified_enums(command, dest):
  subparsers = next(
    a for a in cli.build_parser()._actions if isinstance(a, argparse._SubParsersAction)
  )
  action = next(a for a in subparsers.choices[command]._actions if a.dest == dest)
  enum = SPECS[command]['input_schema']['properties'][dest]['enum']
  assert list(action.choices) == [v for v in enum if v is not None]


def test_style_is_the_callers_not_a_parameter():
  block = tools.call('history', {'record': 'rhenopyrgidae'}, style='json')
  assert 'rendered' not in block
  assert tools.call('history', {'record': 'rhenopyrgidae'})['rendered'].startswith('Rhenopyrgidae')


def test_years_through_call_filter_as_a_tuple_does():
  by_call = tools.call('history', {'record': 'rhenopyrgidae', 'years': [1990, 2000]}, style='json')
  direct = tools.history('rhenopyrgidae', years=(1990, 2000), style='json')
  assert by_call['blockId'] == direct['blockId']
  assert by_call['parameters'] == direct['parameters']
  assert list(by_call['parameters']['years']) == [1990, 2000]
  assert {e['year'] for e in by_call['entries']} <= set(range(1990, 2001))


@pytest.mark.parametrize(
  'name, arguments',
  [
    ('contents', {'record': 'astrocystitidae', 'source': '1994_guensburg_sprinkle'}),
    ('placements', {'records': ['rhenopyrgidae']}),
    ('descendants', {'records': ['rhenopyrgidae']}),
    ('ancestors', {'records': ['rhenopyrgidae']}),
    ('placed_under', {'record': 'rhenopyrgidae', 'parent': 'cyathocystidae'}),
    ('history', {'record': 'rhenopyrgidae', 'years': [1990, 2020]}),
    ('synonymy', {'record': 'grayae_bather_1915'}),
    ('statements', {'record': 'rhenopyrgidae', 'source': 'Dehm 1961'}),
    ('gap', {'source': 'Dehm 1961', 'kind': 'illustrations'}),
    ('printed_forms', {'record': 'edrioblastoidina'}),
  ],
)
def test_mcp_wrappers_answer_with_rendered_blocks(mcp, name, arguments):
  result = getattr(mcp, name)(**arguments)
  blocks = result if isinstance(result, list) else [result]
  assert blocks and all('rendered' in b and 'blockId' in b for b in blocks)


def test_mcp_lookups_and_gap_kind(mcp):
  assert mcp.resolve_name('Rhenopyrgus')[0]['key'] == 'rhenopyrgus'
  assert mcp.resolve_source('Dehm 1961')[0]['key'] == '1961_dehm'
  assert mcp.source_coverage('Dehm 1961')['known']
  with pytest.raises(ValueError, match='kind must be one of'):
    mcp.gap(source='Dehm 1961', kind='bogus')
  with pytest.raises(ValueError, match='kind must be one of'):
    mcp.statements(record='rhenopyrgidae', source='Dehm 1961', kind='specimen')
  with pytest.raises(ValueError, match=r'years must be \[first, last\]'):
    mcp.history(record='rhenopyrgidae', years=[1990])


def test_mcp_plan_tool(mcp):
  got = mcp.plan(
    'Rhenopyrgidae under Cyathocystidae',
    [
      {
        'tool': 'placed_under',
        'parameters': {'record': 'rhenopyrgidae', 'parent': 'cyathocystidae'},
      }
    ],
  )
  assert got['errors'] == []
  assert got['rendered'].startswith('Rhenopyrgidae under Cyathocystidae\n\n')
  assert 'first Guensburg & Sprinkle 1994' in got['rendered']
  assert [b['tool'] for b in got['blocks']] == ['placed_under']
  assert set(got['blocks'][0]) == {'blockId', 'type', 'tool', 'parameters'}
  bad = mcp.plan('x', [{'tool': 'bogus', 'parameters': {}}])
  assert bad['rendered'] is None and bad['blocks'] == []
  assert bad['errors'][0]['error'] == 'block 1: unknown tool bogus'
  styled = mcp.plan(
    'x', [{'tool': 'history', 'parameters': {'record': 'rhenopyrgidae', 'style': 'json'}}]
  )
  assert 'has no parameter style' in styled['errors'][0]['error']
