"""The MCP server's plan tool answers as `phylohist plan` does.

The server is a script, loaded here as a module; its `plan` wraps
`phylohist.plan.execute` and returns the rendered answer with the
blocks that built it, or the errors when nothing could be built.
"""

import importlib.util
import os
import pathlib

import pytest

pytestmark = pytest.mark.skipif(
  bool(os.getenv('PHYLOHIST_DRAFTS')),
  reason='the committed claim table covers data/ only',
)

SERVER = pathlib.Path(__file__).parent.parent / 'scripts' / 'mcp_server.py'


@pytest.fixture(scope='module')
def server():
  spec = importlib.util.spec_from_file_location('mcp_server', SERVER)
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module


def test_plan_tool_renders_the_composition(server):
  got = server.plan(
    'Rhenopyrgidae under Cyathocystidae',
    [
      {
        'tool': 'placed_under',
        'parameters': {'record': 'rhenopyrgidae', 'parent': 'cyathocystidae'},
      },
    ],
  )
  assert got['errors'] == []
  assert got['rendered'].startswith('Rhenopyrgidae under Cyathocystidae\n\n')
  assert 'first Guensburg & Sprinkle 1994' in got['rendered']
  assert [b['tool'] for b in got['blocks']] == ['placed_under']
  assert set(got['blocks'][0]) == {'blockId', 'type', 'tool', 'parameters'}


def test_plan_tool_reports_what_cannot_be_built(server):
  got = server.plan('x', [{'tool': 'bogus', 'parameters': {}}])
  assert got['rendered'] is None and got['blocks'] == []
  assert got['errors'][0]['error'] == 'block 1: unknown tool bogus'
