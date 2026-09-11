# Phylogenetic History Tools

Hand-edited YAML capturing taxonomic opinions as published (`data/`), a
loader with integrity checks (`phylohist/`), and a generated claim table
(`claims/`, one JSONL per source plus a coverage manifest; see
`docs/claims.md`). CI runs the tests, regenerates `docs/schema-usage.md`
and `claims/`, and fails if either is stale:

    poetry run pytest
    poetry run python scripts/schema_audit.py --markdown docs/schema-usage.md
    poetry run python scripts/claims.py
    git diff --exit-code docs/schema-usage.md claims/

The four read-only tools over the claim table (`phylohist/tools.py`) are
served over MCP by `scripts/mcp_server.py`; `.mcp.json` registers the
server for Claude Code, so a session in this directory can resolve a
name, list what the corpus holds about it, check a source's coverage, or
follow a name across sources.

