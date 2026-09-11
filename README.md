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

