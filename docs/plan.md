# Plan: streams, milestones, and what "MVP" means

Written 2026-09-10 after step 0, two reading rounds (33 papers) and the
semantics roadmap. This is the entry point; `semantics-roadmap.md` is the
detail for the data model, `source-observations.md` the findings per paper.

## Where things stand

- **Data.** 218 tree files, 2,716 taxon records, 289 source records. 24
  sources carry an `audit` block (all `partial`); the rest default to
  `unaudited`. Two reading rounds checked 33 sources against their papers
  and left a corrections table of about 50 rows plus the attribution
  conflicts, none yet applied.
- **Contract.** The roadmap has decided the meaning of every field in use
  (A1–A13, B1–B27, C1–C5, D1–D9, E1–E9, F1–F8, G1–G10). Decided is not
  migrated: the schema and data still carry the old shapes for materials
  (D) and time (E), and the step-1 items are documentation decisions
  waiting for the code that reads them.
- **Integrity.** Loader checks (protologue, `mergeInto`, author keys,
  `removed`), the pytest gate with the expected-warnings file, and CI on
  pushes and PRs.
- **Ingestion.** One AI-drafted tree in `drafts/` awaiting audit; the
  review brief and the 32 per-paper reviews live only in a session
  scratchpad.
- **Product.** Nothing built. The agreed shape lives in conversation only:
  a closed-world Q&A over vetted data, a claim table with provenance, a
  coverage manifest, a few tools behind MCP, an eval set, a write-up.

## Four streams and how they depend on each other

| stream | what it produces | depends on | feeds |
|---|---|---|---|
| S1 Data contract | field meanings fixed, small migrations, integrity checks (roadmap step 1) | nothing | S3 reads it |
| S2 Ingestion | audited sources, corrections applied, source records for unentered papers, AI-drafted trees audited by a human | the contract for what a tree must say | S3's coverage manifest; the eval's ground truth; the write-up's failure modes |
| S3 Product | claim table, coverage manifest, tools, evals, write-up | S1 for the gold slice; S2 for a clean gold slice | the reason S1 and S2 exist |
| S4 Materials | D1–D5 designed, the gold slice migrated, specimen claims | a design decision, then S2 to enter the material | a second demo, and the long-run goal of grounding names in specimens |

The two things called "MVP" are one thing in two phases. The **semantics
MVP** (S1, roadmap step 1) is the data contract the claim table needs: what
name was used, where it was placed, which usages were accepted or rejected,
how sure the source was, and whether the tree was audited. The **product
MVP** (S3) is the code and prompts that read that contract and answer
questions without guessing. Neither is useful alone: the contract without
a reader is documentation, the reader without the contract guesses.

## The recommendation: build the reader to force the contract

Do not finish step 1 as a list and then start the product. Build the claim
extractor over the gold slice first, and let each step-1 item land when the
extractor needs it. The roadmap's decisions are already written; what
remains is making code honour them, and the extractor is that code. Items
the gold slice never exercises move to step 2 without loss. This also puts
the eval first: writing the questions before the extractor says what the
claims must be able to express.

Materials (S4) do not block the product MVP, for two reasons. The claim
table is regenerated from YAML, so the extractor is the only code that
knows the material shape; when D1 migrates the gold slice, one adapter
changes and the claim kinds stay. And the gold slice's material coverage is
thin today (Bell 1976 captures none; the 1961 and 1962 protologues have one
specimen each; only the 2020 tree is rich), so a specimen-grounded demo
needs data entry, which is S2 work, before it needs schema work. Design D
now, in parallel, as a document; migrate after the extractor exists.

## Milestones

**M0. Close the reading rounds** (S2; cheap-model work with a human check)
- Copy the review brief and the 32 review files into `docs/reviews/` so
  the audit trail survives the session. (Done: branch `m0-reviews`.)
- Apply the corrections table, gold slice first (roadmap step 0b), one
  commit per source, gate green after each.
- Give every reviewed source an `audit` block: `state`, and `notes` naming
  its review file. Derived coverage (below) makes further flags
  unnecessary.
- Enter the source records the rounds asked for: Regnéll 1945, Haeckel
  1895 (key year to decide), Zamora et al. 2015, the nine Bather studies
  with the 1915 collection as `printingOf`, Bell 1891 and its author.
- Audit `drafts/1891_bell.f.j.yaml`; promote or reject. Either way, write
  down what the audit took, since that is the measurement for the workflow.

**M1. Eval set v1 and the claim vocabulary** (S3, judgment work)
- Question classes: *answerable* (a claim exists and is cited),
  *uncaptured* (the paper says it, the data does not; ground truth from
  the reviews' coverage lines), *as-published* (the answer must reproduce
  the printed form, e.g. "Bell 1975 cites 'Bell, 1974'"), and *conflict*
  (sources or record and print disagree; the answer reports both with
  sources and does not pick). About 40 questions over the gold slice, each
  with the expected claim ids or the expected refusal.
- Claim kinds, fixed before code: `usage` (name as printed, with
  attribution as printed and the resolved taxon), `placement` (parent,
  rank word, flags), `acceptance` (synonymy or `non`, with `parents`
  for the original combination), `act` (new, emended, nomen transl.,
  corrected, with basis), `certainty` (the C-axis markers, one per
  claim), `material` (specimen cited under a name, role as printed,
  locators), `editorial` (source resolution or inferred placement, with
  basis). Every claim carries source key, page, node path, and the audit
  state of its tree.

**M2. Claim table and coverage manifest** (S3 with S1 interleaved; mostly
cheap-model work behind a spec)
- `scripts/claims.py` walks the gold-slice trees and emits JSONL; the
  output is committed and CI checks it is current, the same pattern as
  `docs/schema-usage.md`.
- Coverage is derived, not declared: per source, counts of each claim
  kind present, plus the audit state. Per taxon, the sources that mention
  it. This replaces what the old `complete` flags tried to say and needs
  no maintenance.
- Step-1 items land as the extractor reaches them, each as its own small
  migration with the gate green.

**M3. Tools, prompts, eval run, write-up** (S3)
- Four tools: resolve a name (rank-aware, folding G10 variation); claims
  about a taxon, filterable by source and kind; a source's coverage and
  audit state; the history of a name across sources in order. All read
  the committed claim table; none can write.
- The closed-world rule in the prompt: answer only from claims, cite them,
  and when the manifest says a kind is absent for a source, say "not
  captured", never "not in the paper".
- Run the eval, keep the failures, and write up the failure modes with the
  reading rounds' catalogue (OCR errors, misattribution, placement slips,
  normalisation of printed forms, gap-filling). That write-up is the
  demonstration.

**M4. Materials** (S4)
- D1–D5 as a design decision, with the specimen cases the reviews
  supplied (D8, D9). Migrate the gold slice; update the extractor's
  material adapter; add the specimen questions to the eval.

**Continuous. Ingestion** (S2)
- Each new paper: extract, review against its tree with the brief, record
  the findings in `source-observations.md`, apply corrections. Each
  unentered paper: an AI draft in `drafts/` with the records it needs
  listed at the top, then a human audit. A draft checker that validates a
  draft against the schema and lists unresolved keys is the one piece of
  code this stream needs; it is small and integrity-strengthening.

## Things to keep straight

- **Derived versus declared.** Coverage is derived from the tree; audit
  state is declared. Do not reintroduce declared coverage flags.
- **The extractor is the seam.** Any schema migration touches the
  extractor once and the tools not at all.
- **Cheap models for the mechanical steps** (corrections, reviews, drafts,
  extractor tests) and the strong model for the design points (claim
  vocabulary, eval questions, D design, write-up).
- **Branches.** `productize` is the mainline and carries everything through
  the second reading round; `step0`, `roadmap`, `editorial-maybe` and
  `bell` are merged or superseded and can go.

## Order for the next sittings

1. M0 in two or three sittings, cheap model, one commit per source.
2. M1 as one sitting with the strong model; the output is a document, not
   code.
3. M2 as several sittings; cheap model against the M1 spec, strong model at
   the points where a step-1 item needs a decision the roadmap left open.
4. M3.
5. M4, with S2 data entry for the gold-slice material in between.
