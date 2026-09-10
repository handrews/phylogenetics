# Drafts

Tree files drafted by an AI pass from a paper's text, awaiting a human
audit before they move to `data/trees/`. The loader does not read this
directory. Each draft opens with the taxon and author records it would
need, and quotes every printed form it could not map to a field.

Check a draft with:

    poetry run python scripts/check_draft.py drafts/<key>.yaml

It validates the file against the tree schema and lists the taxon, author
and source keys the draft cites that have no record yet.

| draft | paper | open points |
|---|---|---|
| `1891_bell.f.j.yaml` | Bell 1891, Ann. Mag. Nat. Hist. (6) 8: 206–215 | rank words Stage, Sub-branch, Sub-stage absent from the enum; two unnamed sub-stage placeholders; the p. 211 diagram read from the page image (`1891_bell.f.j_p211.png`); `eleutherozoa` record says Subphylum, paper prints "2nd Sub-branch" |
