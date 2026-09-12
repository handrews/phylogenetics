#!/usr/bin/env python3
"""MCP server exposing the four read-only tools over the claim table.

    poetry run python scripts/mcp_server.py

Speaks MCP over stdio; `.mcp.json` at the repository root registers it for
Claude Code. Every tool reads the committed `claims/` directory and nothing
can write. The docstrings are the tool descriptions a model sees, so they
speak of sources, names and statements, not of files.
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


@server.tool()
def resolve_name(query: str, rank: str | None = None) -> list[dict]:
  """Find the records a printed name can refer to.

  Folds ligatures, diacritics, capitals, hyphens and spaces, so
  "Palæaster", "Echino-encrinites" and "Edrioaster Bigsbyi" all resolve.
  A two-word query is a species: the epithet is resolved and kept where
  some source places it under a genus of that name. Each candidate gives
  the record key to use with the other tools, the rank, whether the
  record is a spelling or rank variant of another (and of which), the
  authority as cited, and how many sources make statements about it. A
  record without a name is a placeholder such as "order uncertain". An
  empty list means no source in the corpus carries the name; it does not
  mean the name does not exist. Optionally restrict by rank word.
  """
  return tools.resolve_name(query, rank=rank)


@server.tool()
def claims_about(
  taxon_key: str,
  source: str | None = None,
  kind: str | None = None,
  act_kind: str | None = None,
) -> list[dict]:
  """Every statement the corpus holds about one record, in publication
  order.

  Each statement carries the source (key and citation), the page when
  recorded, the printed form when it differs from the record, and the
  source's audit state and declared coverage for that kind of statement.
  Kinds: usage (the name is cited), placement (put under a parent, with
  rank and any provisional or questionable marks), acceptance (an earlier
  usage accepted as a synonym or rejected), act (new, type, emended,
  nomTransl, corrected, moved, removed), rejection (the source declines a
  placement), material (specimens, occurrences, illustrations),
  diagnosis, editorial (the editor, not the paper, supplied something).
  A statement marked inferred is the editor's reading, and says so. A
  page inherited from a heading is marked as such. Filter by source key,
  kind, or act kind.
  """
  return tools.claims_about(taxon_key, source=source, kind=kind, act_kind=act_kind)


@server.tool()
def source_coverage(source_key: str) -> dict:
  """What the corpus holds of one publication.

  Its citation; whether its content has been entered at all ("entered"
  false means the paper is on record but not yet entered); the audit
  state and, per kind of statement, whether the reviewer declared all,
  part or none of what the paper prints to be entered; and the counts of
  statements actually derived. When a kind is declared none or partly,
  the right answer to a question about it is that the material has not
  yet been entered, never that the paper lacks it. Unknown key: known
  false.
  """
  return tools.source_coverage(source_key)


@server.tool()
def name_history(taxon_key: str, include_related: bool = True) -> list[dict]:
  """What each source does with a name, in publication order.

  Per source: where the name is placed and at what rank, the acts
  performed on it, the earlier usages accepted or rejected, and
  placements declined. With include_related, records carrying the same
  name at another rank or spelling (a subgenus and the genus it became, a
  nomen translatum, a ligature spelling) are included, each entry naming
  its record, so a trajectory across ranks is visible. The history
  reports; it passes no verdict on which position is right.
  """
  return tools.name_history(taxon_key, include_related=include_related)


if __name__ == '__main__':
  server.run('stdio')
