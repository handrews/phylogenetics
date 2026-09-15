# Review brief (shared by all reviewers in this round)

Read-only task. Do NOT edit any file inside the repository. Write output
only to the review file(s) named in your assignment, in the scratch
directory the assignment gives.

## The dataset

The repository holds hand-edited YAML capturing taxonomic
opinions exactly as each publication printed them, with no normalisation.
- data/trees/<sourceId>.yaml: one file per source. `taxonomies` = one tree per
  printed classification; `phylogenies` = cladograms/diagrams. Node fields:
  `taxon` (key into taxa.yaml), `openTaxon`/`cfTaxon`/`affTaxon` (placeholders
  and open nomenclature), `children`, `synonyms`, `non`, `parents` (original
  placement of a synonym), `removed`, `moved`, `corrected`, flags `new`, `type`,
  `provisional`, `questionable`, `quoted`, `pars`, `emended`, `tentative`,
  `modifier` (e.g. "nomen transl."), `bracket`, `auth`/`year`/`in`/`citedAs`
  (= attribution exactly as printed on that line), `pages`, `illustrations`,
  `specimens`, `occurrences`, `diagnosis`, `notes` (free text: ALWAYS read),
  `editorial` (= the data editor's own inference or resolution, with `basis`).
- data/taxa.yaml: identity records (name + authority). `altSpellingOf`,
  `altRankOf`, `vulgarSpellingOf` = derivative records that borrow authority.
  Species names are entities in their own right; a species node always sits
  under a genus node, so recombination is visible from placement.
- data/sources.yaml: bibliographic records. Keys are by publication year.
- Placeholders: "-uncertain-"/"-indeterminate-" keys mean a bin whose members
  need not form one real taxon; "-unnamed-" keys mean the source believes one
  taxon exists but does not name it. `new: true` on a placeholder means this
  source originates the placeholder, not a nomenclatural act.

Vocabulary and prior findings: read notes/development/semantics-roadmap.md "Ground rules"
(including "The `editorial` block"), items A6, B6, B16–B20, C4, C5, G7, G9 and
the table in section H; and skim notes/audits/source-observations.md for the format.
Look up taxon keys with grep on data/taxa.yaml (do not read the whole file).

## What to deliver per paper

Coverage gaps are scope history, not errors (roadmap G9): early-entered
sources capture less because the project's scope grew. So:

1. **Coverage, one line per kind**: classification skeleton / new taxa / type
   species / synonymy lists / material / occurrences / illustrations /
   diagnoses / phylogeny — each marked all, partly, or none. No item-level
   detail; at most one example per row. If nothing beyond the skeleton is
   captured, say so in one sentence.
2. **Correctness of what IS captured**: check every node in the tree file
   against the printed text: identity, rank, placement, flags, attribution
   as printed, notes. Table: node | printed (page) | verdict. Report only
   mismatches and "cannot verify" rows in full; summarise matches as a count.
3. **Cases for the data model** (the main value): anything the fields cannot
   say cleanly, or that hits a roadmap item. Quote the printed wording with
   the printed page. Pay attention to the specific prompts in your
   assignment (subgenera, parenthetical notation, rankless names, nomina
   nuda, disarticulated plates, renamings, and so on).
4. **Source record check**: title, volume/number/pages, dates, authors
   against the sources.yaml block. One line if it all matches.
5. **Uncertainties**: OCR gaps, plates, anything not verifiable. Never guess;
   write "cannot verify".

For a paper with no tree or no source record, skip 2 and 4, and instead
summarise what it prints (classification, new names, acts) in one short
section so the owner can decide whether to enter it.

## Rules

- Cite printed page numbers, not PDF indexes; work out the mapping from the
  running heads and state it once at the top.
- Quote printed wording exactly, including odd spellings and punctuation.
- Old scans: OCR of italics, ligatures and umlauts is unreliable; when a
  spelling or year matters, say the OCR reading and mark it "cannot verify"
  unless the context settles it.
- Crisp prose, tables where they help, no chatty commentary, no proposals to
  edit YAML beyond naming the discrepancy.
