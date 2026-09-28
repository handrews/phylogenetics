# Drafts

Tree files drafted by an AI pass from a paper's text, awaiting a human
audit before they move to `data/trees/`. The loader reads this directory
only when asked: `phylohist --draft` (`-d`) loads the drafts after the
audited trees, and `PHYLOHIST_DRAFTS=1 poetry run pytest` runs the load
test over them (the warning snapshot is skipped in that mode, since a
draft is expected to warn until its records exist). Each draft opens with
the taxon and author records it would need, and quotes every printed
form it could not map to a field.

Check a draft with:

    poetry run python scripts/check_draft.py drafts/<key>.yaml

It validates the file against the tree schema and lists the taxon, author
and source keys the draft cites that have no record yet.

## What a draft records

The data says who published what systematic information in which paper
(roadmap, Ground rules, "Scope"). A draft therefore carries names, acts,
placements, usages, synonymies, `material` with its repository and
geological `contexts` or `range`, and `figures` (D1), and the page
numbers that locate them. It does not carry diagnoses, descriptions,
figure captions, artists' names, physical descriptions of specimens, or a
narration of the paper's argument. Everything of that kind that a
drafter finds worth recording goes into the review file under
`notes/reviews/`, where quotation with printed page numbers is the
expected form.

Conventions the promotion of the Whiteaves and Bather drafts settled:

- `notes` on a node explains only what would otherwise make the data hard
  to understand or the source hard to locate. A note that quotes the paper
  at length is moved to the review on promotion, so it is better written
  there in the first place.
- `pages` is one page: the page where the name is formally stated, or
  where its prose treatment begins. A range is for exceptional cases.
- A classification the paper adopts by citation is recorded as the
  paper's usage, with the ranks the paper attributes to it, even where the
  paper places nothing under most of it. The genus is not made the top
  node merely because the paper erected nothing above it.
- One specimen, one `material` entry, even when the paper gives no number
  and no type word (then a `label`). Identifiers, a paper's own letters
  (A, B, C) and the repository are kept; descriptions are not.

| draft | paper | open points |
|---|---|---|
| `1897_whiteaves.yaml` | Whiteaves 1897, Canadian Record Sci. 7(5): 287–292 | the protologue of the first edrioblastoid; no higher taxon printed; three specimens without numbers or type words |
| `1898_whiteaves.yaml` | Whiteaves 1898 (postscript), 7(7): 395–396 | the replacement name *Steganoblastus*, recorded as `substituted`; the species' slip "Canadensis" as `lapsus`; check against B6 |
| `1914c_bather.yaml` | Bather 1914, Studies V, Geol. Mag. (6) 1: 193–203 | Steganoblastidae used, not erected; specimen A named holotype among three syntypes |
| `1925_hudson.yaml` | Hudson 1925, J. Geol. 33(6): 642–657 | usage only; "true blastid" affinity in notes; cotypes A and B |
| `1927_hudson.yaml` | Hudson 1927, Rep. Vermont State Geol. 15: 97–110 | usage only; three specimens claimed, two discussed |
| `1879_dames.yaml` | Dames 1879, Referat of Schmidt in Neues Jahrbuch 1879: 1001 | a secondhand account, nothing marked new; *rhizophora* added as printed 1879 against a record dated 1889; the group's author is OCR-illegible |
| `1927_jaekel.yaml` | Jaekel 1927, Arkiv för Zoologi 19A(5): 1–5 | family heading "Thecocystidae" against "Cyathothecidae" in the preceding sentence; type by monotypy marked as the editor's; *C. corallum* recombined only in the plate caption |
| `1891_bell.f.j.yaml` | Bell 1891, Ann. Mag. Nat. Hist. (6) 8: 206–215 | rank words Stage, Sub-branch, Sub-stage absent from the enum; two unnamed sub-stage placeholders; the p. 211 diagram read from the page image (`1891_bell.f.j_p211.png`); `eleutherozoa` record says Subphylum, paper prints "2nd Sub-branch" |
