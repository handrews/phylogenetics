# Claims: the vocabulary the extractor implements

A claim is one statement a source prints about one name, carried with its
provenance. The claim table is generated from the tree files by
`scripts/claims.py` (the logic is `phylohist/claims.py`, over the `Tree`
walk), deterministically: the same YAML always yields the same claims, in
the same order, nothing is merged across sources, and nothing is normalised
beyond resolving keys. The output is committed: `claims/<source>.jsonl`,
one claim per line for every tree file, and `claims/manifest.json`; CI
reruns the script and fails on a stale directory, so every data commit
regenerates it. This document fixes what a claim is and which tree fields
produce which claims; the eval questions in `eval/` are written against
it, and `tests/test_claims.py` checks that they still match. Field
meanings are the roadmap's (`semantics-roadmap.md`); item codes below
point there.

## The record

Every claim carries:

| field | value |
|---|---|
| `id` | `<source>:<path>:<kind>[:<n>]`. `<path>` is the node's position in its tree file as the loader computes it: the taxonomy or phylogeny index, then each step down (`children/2`, `synonyms/0`, `non/1`, `removed/0`, `parents/0`, `moved`, `corrected`, `or/0`). `<n>` disambiguates several claims of one kind from one node (a node with three `specimens` roles yields three `material` claims). Ids are stable as long as the file is not reordered; the tree keeps printed order, so reordering is a data change. |
| `kind` | one of `usage`, `placement`, `acceptance`, `act`, `rejection`, `material`, `diagnosis`, `secondhand`, `editorial` |
| `source` | the tree file's source key |
| `path` | the node's position and pointer, `0/children/0/children/0`, the same string the id carries |
| `tree` | `taxonomy`, or a phylogeny's `treeType`; a phylogeny's `notes` ride along as `treeNotes` |
| `pages` | the node's `pages` as written. A node without `pages` takes the nearest ancestor's along the `children` axis only, and the claim then carries `pagesInherited: true`. Entries under `synonyms`, `non`, `removed`, `parents`, `altPlacements`, `moved` and `corrected` never inherit: a synonymy line's page is its own or unknown. |
| `subject` | the resolved taxon key the claim is about |
| `printed` | the printed form on that line: `citedAs` verbatim, and `auth`, `year`, `in` as written (A1, A12). Absent `auth` means "as the record"; the claim says so with `printedAttribution: as-record`. |
| `audit` | the source's `audit.state`; `coverageKind`, the coverage kind the claim counts under (`skeleton` for usage, rejection and a taxonomy placement, `phylogeny` for a placement in a phylogeny, `synonymy` for acceptance, `newTaxa`/`types` for the matching acts, `material`/`occurrences`/`illustrations` by material kind, `diagnoses`); and `coverage`, the declared value for that kind when the source declares one |
| `editorial` | the node's `editorial` block, copied through |
| `inferred` | `true` when the editorial block says the editor supplied the field this claim comes from (`inferred: true`, or a list naming it). The claim is then the editor's, not the paper's, and the manifest does not count it |
| `notes` | the node's `notes`, copied through verbatim |

A claim whose subject is a placeholder (an `openTaxon` key) carries
`placeholder: uncertain | unnamed | open` from the key's form (C4), so a
bin is never reported as a taxon and an unnamed group is not reported as
a bin. A placement whose parent is a placeholder carries the parent's
kind as `parentPlaceholder`.

Attribution appears in trees in two shapes and both produce the same
`printed` fields: the flat form (`auth`, `year`, `in`, `citedAs`) and the
nested form (`authority: {source, pages, illustrations}`), which also
resolves the citation to a source record and carries the cited pages. When
the nested form names a source, the claim adds `citesSource`, `citedPages`,
`citedIllustrations` and `citedAttributedTo` as present.

## The kinds

### `usage`

Emitted for every node that cites a name: `taxon`, `openTaxon`, `cfTaxon`,
`affTaxon`, and for every `synonyms`, `non`, `removed`, `parents` and `or`
entry. Fields added:

- `form`: which field carried the name; `bracket` for a cladogram's
  bracket label.
- `spelling`: the key used on the line. Spellings are undirected (B28); the
  claim never substitutes the record the key points at.
- `axis`: how the node hangs off its parent (`children`, `synonyms`,
  `removed`, `parents`, …; `root` for a tree's top node).
- `target`: for `cfTaxon` and `affTaxon`, the compared name (C1).
- A `synonyms` or `non` entry with no name field of its own is a usage of
  the node's own name by the cited source (the 2020 tree's stacked
  citations of *grayae* are this shape); it carries `ownName: true`.

### `placement`

Emitted for every child under its parent in a taxonomy. Fields added:

- `parent`: the nearest named ancestor's key; `position`: index among the
  siblings, since the tree keeps the printed order. Under an unnamed clade
  node the parent is null and `parentPath` points at the node; when the
  named ancestor is further up, `parentPath` says so too.
- `rank`: the record's rank today. When the tree carries a printed rank
  word in `citedAs` or `notes`, `rankAsPrinted` holds it; the rule that
  rank belongs to the tree node is G8, not yet in force.
- Flags copied from the node: `provisional`, `questionable`, `quoted`,
  `pars`, `tentative`, `outgroup`, `stem`; `altPlacements` as a list of
  keys. (`listHedged`, `listComplete` (B16) are not in the schema yet.)

A phylogeny's nesting produces placements too, marked
`tree: cladogram | diagram | other` with the phylogeny's `notes`, and a
`bracket` label is a second placement of the node's name whose parent is
the bracket's key, marked `via: bracket`.

A source can also say where a name does *not* belong. Two printed shapes,
one claim: "we are confining the family Cyathocystidae to Cyathocystis and
Cyathotheca" (Bockelie & Paul 1983, the `removed` list, B5) and "we do not
include them within Cyathocystidae Bather, 1899" (Sumrall et al. 2013,
p. 773). The first is written from the group's side and the second from
the taxon's side, and whether anyone had placed the name there before is
the source's business, not the claim's. Both emit a `rejection`: subject,
`declinedParent`, the printed words. `removed` under a group node and a
`rejectedPlacements` list on the taxon node (not yet in the schema) are
the two spellings.

`follows`: the source adopts a placement by citing another work for it
("Edrioasterida sensu Guensburg and Sprinkle (1994)", 2013). A source that
argues a placement from its own evidence is a decider; one that adopts
another's by citation is a follower. The distinction is carried on the
placement claim so that agreement can be counted both ways.

### `acceptance`

Emitted for each `synonyms` entry (the source accepts the cited usage as
this name) and each `non` entry (the source rejects it) (B1). Fields added:

- `stance`: `accepts | rejects`.
- `under`: the node whose name the entry is accepted or rejected under.
- `parents`: the original combination, as the list of keys under the
  entry's `parents` (a genus, or a genus and a subgenus).
- `pars`, `tentative` copied; `ownName: true` when the entry has no name
  of its own.

### `act`

Something this source does to a name. One claim per flag, `actKind` being:

| tree field | `actKind` |
|---|---|
| `new: true` on a named node | `new` (the protologue; F6 checks it) |
| `new: true` on a placeholder | `placeholder` (the source originates the placeholder; C4) |
| `type: true` | `type` (the fixation method joins when B14 lands) |
| `emended: true` | `emended` |
| `modifier: nomen transl.` (and `act: [nomTransl]` after B6) | `nomTransl`, `modifier` verbatim, and `altRankOf` giving the derived-from name when the record carries the link |
| any other `modifier` (nomen nudum, n. comb., (Plesion)) | `modifier`, verbatim, until B6 names them |
| `corrected: {taxon: y}` | `corrected`, `correctedFrom: y`; the node's own name is the corrected form |
| `moved: {taxon: y}` | `moved`, `movedFrom: y` |
| `removed` entry | `removed`, `removedFrom` the group (the source takes the name out of it; B5), beside the `rejection` |
| `homonym: true` on the record | not a claim: key housekeeping |

### `certainty`

Not a kind of its own. The C-axis markers (`provisional`, `questionable`,
`quoted`, `tentative`, `pars`, `cf.`, `aff.`, `illustration.uncertain`) ride
on the claim they qualify, as fields. No separate table.

### `material`

Emitted for each `specimens` role entry, each `occurrences` entry and each
`illustrations` entry on a node. Fields added: `materialKind: specimen |
occurrence | illustration`, `role` as recorded today (`holotype`,
`paratypes`, `syntypes`, `unknowntypes`, and the occurrence blocks'
`holotypes` and `unspecified`), `ids`, `repository`, and the occurrence or
illustration fields copied verbatim (`occurrence`, `illustration`). An
occurrence's own specimens yield specimen claims too, with `inOccurrence`
giving the occurrence's index; those blocks nest role then repository in
most trees and the other way round in two (Vanuxem 1842, Rievers 1961), so
the role word decides which level is which. The shape follows the YAML as
it stands; when D1 migrates material, only the extractor's material
adapter changes and these claims keep their fields.

### `diagnosis`

Emitted for a node's `diagnosis`, `text` verbatim. It is the one tree
field with a coverage kind (`diagnoses`) and, without a claim, no way to
be counted.

### `secondhand`

A source's statement about what another source did, accurate or not: "P.
octogona … was assigned to Rhenopyrgus by Dehm (1961)" (Holloway & Jell
1983 p. 1004). Fields: `about` (the cited source key), `says` (the act or
placement attributed to it), and `matches`, derived by comparing `says`
with the cited source's own claims (B19); here Dehm's tree does not bear
the statement out. Not emitted from any tree field today; reserved so that
"what did later authors say he did" has a home, and so the derived
comparison feeds the citation-error part of the eval.

### `editorial`

The node's `editorial` block emitted as a claim of its own, so a question
can ask whether a placement is the paper's or the editor's. Fields:
`inferred` (`true`, or the list of inferred fields), `source` (the resolved
source for a citation that cannot resolve as printed), `basis`. The claim
it qualifies carries the same block, so both directions are answerable.

## Derived coverage

`claims/manifest.json` holds, per source record (every key in
`sources.yaml`, whether or not a tree exists: `tree: false` is how "the
paper is recorded but not yet entered" is derived), the declared `audit`,
the counts of claims by kind, by `actKind` and by `materialKind`, the
counts by coverage kind (`derived`, editor-inferred claims excluded), and
`inconsistencies`. Per taxon, the sources with any claim about it, in
publication-year order. Coverage is declared by a reviewer and counted by
the extractor; they are cross-checked, never conflated (G1): a source
declaring `all` or `partly` for a kind with no derived claims, or `none`
or `na` with any, is an inconsistency row for the owner to settle either
way.

## What the vocabulary does not do

- No consensus and no "current name": every claim is one source's.
- No merging of spellings (B28): a lookup folds ligatures, diacritics,
  hyphens and spaces (G10) to find records, and the claims keep the key
  as cited.
- No rank inference: the record's rank is a convenience until G8.
- No material redesign: D1 is a later change to one adapter.
- No inference from absence: a kind with no claims for a source means
  "not captured", and only the declared coverage can say whether the paper
  prints any.

## Worked examples

### Holloway & Jell 1983, *Rhenopyrgus* (`data/trees/1983_holloway_jell.yaml`)

The node sits at `taxonomies/0/children/0/children/0/children/0`: class
Edrioasteroidea, placeholder "order uncertain", family Rhenopyrgidae,
genus *Rhenopyrgus*. It yields:

- `placement`: subject `rhenopyrgus`, parent `rhenopyrgidae`, position 0,
  `printedAttribution: as-record`, `pagesInherited: true` if the family
  node has pages (it does not today, so `pages` is absent).
- The parent yields `act` `new` (Rhenopyrgidae is `new: true`) and its own
  `placement` under `edrioasteroidea-order-uncertain_holloway_jell_1983`
  with `parentPlaceholder: uncertain`; the placeholder's own claims carry
  `placeholder: uncertain`.
- Under the genus, *coronaeformis* yields `act` `type`, and its `synonyms`
  entry yields a `usage` and an `acceptance` with `parents: [pyrgocystis]`:
  the original combination *Pyrgocystis coronaeformis*.
- `audit`: state `partial`; coverage `skeleton: all`, `synonymy: partly`,
  `material: none`.

### Ewin et al. 2020, *grayae* (`data/trees/2020_ewin_martin.m_isotalo_zamora.yaml`)

The species node has five `synonyms` entries, none with a name field, so
each is a usage of *grayae* by the cited source, and each is an
`acceptance` with `stance: accepts`, `citesSource` and the cited pages:
`1915b_bather` p. 58 with plate 3 figures 1–2, `1983_holloway_jell`
p. 1004, `1985_smith.a.b` p. 732 with text-figure 11, and two entries for
`2013_sumrall_heredia_rodríguez.c.m_mestre` (figure 1; p. 773). The first
and fourth carry `parents: [pyrgocystis]`. None inherits `pages` from the
species node. The node's `occurrences` yield `material` claims, and the
specimens inside the first occurrence yield more: the holotype claim has
`role: holotypes` (the recorded word), `repository: NHMUK`, `ids:
[E23470]`, `inOccurrence: 0`.

### Fay 1962, *ottawaensis* (`data/trees/1962_fay.yaml`)

`act` `type` on `ottawaensis_whiteaves_1897`, carrying `editorial:
{inferred: [type], basis: "Fay never prints \"type species\"; the genus is
monotypic (p. 201)"}`, plus a separate `editorial` claim with the same
block. A question "does Fay fix the type species?" is answered from the
act claim's `inferred: true`: the flag is the editor's, and the paper
prints monotypy, so the manifest does not count it against the declared
`types: na`. The `material` claim has `role: syntypes` and the node's
`notes` quoting "Holotype, 752" beside "labelled a syntype", so both printed
words are returned.
