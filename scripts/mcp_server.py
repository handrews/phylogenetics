#!/usr/bin/env python3
"""MCP server exposing the read-only block tools over the claim table.

    poetry run python scripts/mcp_server.py

Speaks MCP over stdio; `.mcp.json` at the repository root registers it for
Claude Code. Every tool reads the committed `claims/` directory and nothing
can write. The descriptions a model sees are `tools.TOOL_DESCRIPTIONS`,
shared with the CLI and the eval runner, and speak of sources, names and
statements, not of files. Block-returning tools carry `rendered`, the
text to reproduce verbatim; every call goes through `tools.call`, so the
parameters are the specs' and the rendering is text. The `plan` tool is the other route: the
model states the blocks an answer is made of and code builds them
(`phylohist.plan`), so a chat can answer without reading a block.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from mcp.server.mcpserver import MCPServer  # noqa: E402

from phylohist import plan as plans  # noqa: E402
from phylohist import tools
from phylohist.render import render_composition  # noqa: E402

server = MCPServer(
  'phylohist',
  instructions=(
    'A corpus of published taxonomic opinions on Palaeozoic echinoderms, '
    'recorded source by source exactly as printed. Resolve a name first; '
    'then ask for the contents of a source, the placements of a set of '
    'records, their descendants or ancestors across the corpus, or the '
    'history of a name. Every tool returns a block with a rendered form '
    'to reproduce verbatim; a gap is stated with the gap tool. Every '
    'answer must come from what these tools return; a gap in the corpus '
    'is not a gap in the literature. Or resolve the names and papers the '
    'question mentions and state a plan: the plan tool builds the blocks '
    'and returns the rendered answer to reproduce verbatim.'
  ),
)

D = tools.TOOL_DESCRIPTIONS


def _call(tool, **arguments):
  return tools.call(tool, arguments)


@server.tool(description=D['resolve_name'])
def resolve_name(query: str, rank: str | None = None) -> list[dict]:
  return _call('resolve_name', query=query, rank=rank)


@server.tool(description=D['resolve_source'])
def resolve_source(query: str) -> list[dict]:
  return _call('resolve_source', query=query)


@server.tool(description=D['contents'])
def contents(
  record: str, source: str | None = None, depth: int | None = None, synonymy: bool = False
) -> list[dict]:
  return _call('contents', source=source, record=record, depth=depth, synonymy=synonymy)


@server.tool(description=D['placements'])
def placements(
  records: list[str],
  sources: list[str] | None = None,
  years: list[int | None] | None = None,
  include_variants: bool = True,
  include_synonyms: bool = True,
  trees: list[str] | None = None,
) -> dict:
  return _call(
    'placements',
    records=records,
    sources=sources,
    years=years,
    include_variants=include_variants,
    include_synonyms=include_synonyms,
    trees=trees,
  )


@server.tool(description=D['descendants'])
def descendants(
  records: list[str],
  include_synonyms: bool = True,
  include_variants: bool = True,
  trees: list[str] | None = None,
  years: list[int | None] | None = None,
) -> dict:
  return _call(
    'descendants',
    records=records,
    include_synonyms=include_synonyms,
    include_variants=include_variants,
    trees=trees,
    years=years,
  )


@server.tool(description=D['ancestors'])
def ancestors(
  records: list[str],
  include_variants: bool = True,
  trees: list[str] | None = None,
  years: list[int | None] | None = None,
) -> dict:
  return _call(
    'ancestors', records=records, include_variants=include_variants, trees=trees, years=years
  )


@server.tool(description=D['placed_under'])
def placed_under(
  record: str,
  parent: str,
  include_variants: bool = True,
  trees: list[str] | None = None,
  years: list[int | None] | None = None,
) -> dict:
  return _call(
    'placed_under',
    record=record,
    parent=parent,
    include_variants=include_variants,
    trees=trees,
    years=years,
  )


@server.tool(description=D['history'])
def history(
  record: str,
  include_related: bool = True,
  synonymy: bool = False,
  trees: list[str] | None = None,
  years: list[int | None] | None = None,
) -> dict:
  return _call(
    'history',
    record=record,
    include_related=include_related,
    synonymy=synonymy,
    trees=trees,
    years=years,
  )


@server.tool(description=D['synonymy'])
def synonymy(record: str, source: str | None = None) -> list[dict]:
  return _call('synonymy', record=record, source=source)


@server.tool(description=D['statements'])
def statements(
  record: str, source: str | None = None, kind: str | None = None, act_kind: str | None = None
) -> dict:
  return _call('statements', record=record, source=source, kind=kind, act_kind=act_kind)


@server.tool(description=D['source_coverage'])
def source_coverage(source: str) -> dict:
  return _call('source_coverage', source=source)


@server.tool(description=D['gap'])
def gap(source: str | None = None, kind: str | None = None, name: str | None = None) -> dict:
  if kind is not None and kind not in tools.COVERAGE_WORDS:
    raise ValueError(f'kind must be one of {", ".join(tools.COVERAGE_WORDS)}, not {kind!r}')
  return _call('gap', source=source, kind=kind, name=name)


@server.tool(description=D['printed_forms'])
def printed_forms(record: str, source: str | None = None) -> dict:
  return _call('printed_forms', record=record, source=source)


@server.tool(description=plans.PLAN_SPEC['description'])
def plan(header: str, blocks: list[dict], question: str | None = None) -> dict:
  outcome = plans.execute({'header': header, 'blocks': blocks, 'question': question})
  composition = outcome['composition']
  return {
    'rendered': render_composition(composition, 'text') if composition else None,
    'blocks': [
      {k: b[k] for k in ('blockId', 'type', 'tool', 'parameters')} for b in outcome['blocks']
    ],
    'errors': outcome['errors'],
  }


if __name__ == '__main__':
  server.run('stdio')
