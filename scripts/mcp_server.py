#!/usr/bin/env python3
"""MCP server exposing the four read-only tools over the claim table.

    poetry run python scripts/mcp_server.py

Speaks MCP over stdio; `.mcp.json` at the repository root registers it for
Claude Code. Every tool reads the committed `claims/` directory and nothing
can write. The descriptions a model sees are `tools.TOOL_DESCRIPTIONS`,
shared with the eval runner, and speak of sources, names and statements,
not of files.
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
    'recorded source by source exactly as printed. Resolve a name first, '
    'then ask for its statements or its history. Every answer must come '
    'from what these tools return; a gap in the corpus is not a gap in '
    'the literature.'
  ),
)


@server.tool(description=tools.TOOL_DESCRIPTIONS['resolve_name'])
def resolve_name(query: str, rank: str | None = None) -> list[dict]:
  return tools.resolve_name(query, rank=rank)


@server.tool(description=tools.TOOL_DESCRIPTIONS['claims_about'])
def claims_about(
  taxon_key: str,
  source: str | None = None,
  kind: str | None = None,
  act_kind: str | None = None,
) -> list[dict]:
  return tools.claims_about(taxon_key, source=source, kind=kind, act_kind=act_kind)


@server.tool(description=tools.TOOL_DESCRIPTIONS['source_coverage'])
def source_coverage(source_key: str) -> dict:
  return tools.source_coverage(source_key)


@server.tool(description=tools.TOOL_DESCRIPTIONS['name_history'])
def name_history(taxon_key: str, include_related: bool = True) -> list[dict]:
  return tools.name_history(taxon_key, include_related=include_related)


if __name__ == '__main__':
  server.run('stdio')
