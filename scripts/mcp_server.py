#!/usr/bin/env python3
"""MCP server exposing the read-only block tools over the claim table.

    poetry run python scripts/mcp_server.py

Speaks MCP over stdio; `.mcp.json` at the repository root registers it for
Claude Code. Every tool reads the committed `claims/` directory and nothing
can write. The descriptions a model sees are `tools.TOOL_DESCRIPTIONS`,
shared with the CLI and the eval runner, and speak of sources, names and
statements, not of files. Block-returning tools carry `rendered`, the
text to reproduce verbatim.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from mcp.server.mcpserver import MCPServer  # noqa: E402

from phylohist import tools  # noqa: E402

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
    'is not a gap in the literature.'
  ),
)

D = tools.TOOL_DESCRIPTIONS


@server.tool(description=D['resolve_name'])
def resolve_name(query: str, rank: str | None = None) -> list[dict]:
  return tools.resolve_name(query, rank=rank)


@server.tool(description=D['contents'])
def contents(
  record: str, source: str | None = None, depth: int | None = None,
  synonymy: bool = False, style: str = 'text',
) -> list[dict]:
  return tools.contents(source, record, depth=depth, synonymy=synonymy, style=style)


@server.tool(description=D['placements'])
def placements(
  records: list[str], sources: list[str] | None = None,
  years: list[int | None] | None = None, include_variants: bool = True,
  include_synonyms: bool = True, trees: list[str] | None = None,
  style: str = 'text',
) -> dict:
  return tools.placements(
    records, sources=sources, years=tuple(years) if years else None,
    include_variants=include_variants, include_synonyms=include_synonyms,
    trees=trees, style=style,
  )


@server.tool(description=D['descendants'])
def descendants(
  records: list[str], include_synonyms: bool = True, include_variants: bool = True,
  trees: list[str] | None = None, years: list[int | None] | None = None,
  style: str = 'text',
) -> dict:
  return tools.descendants(
    records, include_synonyms=include_synonyms, include_variants=include_variants,
    trees=trees, years=tuple(years) if years else None, style=style,
  )


@server.tool(description=D['ancestors'])
def ancestors(
  records: list[str], include_variants: bool = True,
  trees: list[str] | None = None, years: list[int | None] | None = None,
  style: str = 'text',
) -> dict:
  return tools.ancestors(
    records, include_variants=include_variants, trees=trees,
    years=tuple(years) if years else None, style=style,
  )


@server.tool(description=D['history'])
def history(
  record: str, include_related: bool = True, trees: list[str] | None = None,
  years: list[int | None] | None = None, style: str = 'text',
) -> dict:
  return tools.history(
    record, include_related=include_related, trees=trees,
    years=tuple(years) if years else None, style=style,
  )


@server.tool(description=D['synonymy'])
def synonymy(record: str, source: str | None = None, style: str = 'text') -> list[dict]:
  return tools.synonymy(record, source=source, style=style)


@server.tool(description=D['statements'])
def statements(
  record: str, source: str | None = None, kind: str | None = None,
  act_kind: str | None = None, style: str = 'text',
) -> dict:
  return tools.statements(record, source=source, kind=kind, act_kind=act_kind, style=style)


@server.tool(description=D['source_coverage'])
def source_coverage(source_key: str) -> dict:
  return tools.source_coverage(source_key)


@server.tool(description=D['gap'])
def gap(source: str, kind: str, style: str = 'text') -> dict:
  return tools.gap(source, kind, style=style)


@server.tool(description=D['printed_forms'])
def printed_forms(record: str, source: str | None = None, style: str = 'text') -> dict:
  return tools.printed_forms(record, source=source, style=style)


if __name__ == '__main__':
  server.run('stdio')
