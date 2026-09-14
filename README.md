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

The read-only tools over the claim table (`phylohist/tools.py`) return
blocks, rendered in a style; the CLI has one subcommand per tool:

    poetry run phylohist resolve "Palæaster"
    poetry run phylohist contents 1994_guensburg_sprinkle astrocystitidae --synonymy
    poetry run phylohist descendants edrioblastoidea
    poetry run phylohist ancestors astrocystitidae cyathocystidae rhenopyrgidae
    poetry run phylohist history rhenopyrgus --style markdown
    poetry run phylohist history "Rhenopyrgus grayae"
    poetry run phylohist under rhenopyrgus edrioblastoidina
    poetry run phylohist statements "Rhenopyrgus viviani"
    poetry run phylohist gap "Holloway & Jell 1983" material
    poetry run phylohist source "Lamarck 1816"
    poetry run python scripts/eval_run.py --ask "Who first placed Rhenopyrgus under Edrioblastoidina?"

The same tools are served over MCP by `scripts/mcp_server.py`, which
`.mcp.json` registers for Claude Code. `docs/claims.md`, "Reading the
table", describes the blocks and the tools.

