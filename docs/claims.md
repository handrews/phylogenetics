# Claims: the vocabulary the extractor implements

A claim is one statement a source prints about one name, carried with its
provenance. The claim table is generated from the tree files by
`scripts/claims.py` (M2), deterministically: the same YAML always yields the
same claims, nothing is merged across sources, and nothing is normalised
beyond resolving keys. This document fixes what a claim is and which tree
fields produce which claims, so that the eval questions in `eval/` can be
written against it before the code exists. Field meanings are the roadmap's
(`semantics-roadmap.md`); item codes below point there.

## The record

Every claim carries:

| field | value |
|---|---|
| `id` | `<source>:<path>:<kind>[:<n>]`. `<path>` is the node's position in its tree file as the loader computes it: the taxonomy or phylogeny index, then each step down (`children/2`, `synonyms/0`, `non/1`, `removed/0`, `parents/0`, `moved`, `corrected`, `or/0`). `<n>` disambiguates several claims of one kind from one node (a node with three `specimens` roles yields three `material` claims). Ids are stable as long as the file is not reordered; the tree keeps printed order, so reordering is a data change. |
| `kind` | one of `usage`, `placement`, `acceptance`, `act`, `material`, `editorial` |
| `source` | the tree file's source key |
| `pages` | the node's `pages` as written. A node without `pages` takes the nearest ancestor's along the `children` axis only, and the claim then carries `pagesInherited: true`. Entries under `synonyms`, `non`, `removed`, `parents`, `altPlacements`, `moved` and `corrected` never inherit: a synonymy line's page is its own or unknown. |
| `subject` | the resolved taxon key the claim is about |
| `printed` | the printed form on that line: `citedAs` verbatim, and `auth`, `year`, `in` as written (A1, A12). Absent `auth` means "as the record"; the claim says so with `printedAttribution: as-record`. |
| `audit` | the source's `audit.state`, and its `coverage` value for the claim's kind (`skeleton` for placement, `synonymy` for acceptance, `newTaxa`/`types` for the matching acts, `material`/`occurrences`/`illustrations` for material) |
| `editorial` | the node's `editorial` block, copied through |
| `notes` | the node's `notes`, copied through verbatim |

A claim whose subject is a placeholder (an `openTaxon` key) carries
`placeholder: uncertain | unnamed | open` from the key's form (C4), so a
bin is never reported as a taxon and an unnamed group is not reported as
a bin.

Attribution appears in trees in two shapes and both produce the same
`printed` fields: the flat form (`auth`, `year`, `in`, `citedAs`) and the
nested form (`authority: {source, pages, illustrations}`), which also
resolves the citation to a source record and carries the cited pages. When
the nested form names a source, the claim adds `citesSource`.

## The kinds

### `usage`

Emitted for every node that cites a name: `taxon`, `openTaxon`, `cfTaxon`,
`affTaxon`, and for every `synonyms`, `non`, `removed`, `parents` and `or`
entry. Fields added:

- `form`: which field carried the name.
- `spelling`: the key used on the line. Spellings are undirected (B28); the
  claim never substitutes the record the key points at.
- `target`: for `cfTaxon` and `affTaxon`, the compared name (C1).
- A `synonyms` or `non` entry with no name field of its own is a usage of
  the node's own name by the cited source (the 2020 tree's stacked
  citations of *grayae* are this shape).

### `placement`

Emitted for every child under its parent in a taxonomy. Fields added:

- `parent`: the parent's key; `position`: index among the siblings, since
  the tree keeps the printed order.
- `rank`: the record's rank today. When the tree carries a printed rank
  word in `citedAs` or `notes`, `rankAsPrinted` holds it; the rule that
  rank belongs to the tree node is G8, not yet in force.
- Flags copied from the node: `provisional`, `questionable`, `quoted`,
  `pars`; from the parent: `listHedged`, `listComplete` (B16);
  `altPlacements` as a list of keys.

A phylogeny's nesting produces placements too, marked
`tree: cladogram | diagram | other` with the phylogeny's `notes`, and a
`bracket` label is a placement whose parent is the bracket's key.

### `acceptance`

Emitted for each `synonyms` entry (the source accepts the cited usage as
this name) and each `non` entry (the source rejects it) (B1). Fields added:

- `stance`: `accepts | rejects`.
- `parents`: the original combination, as the list of keys under the
  entry's `parents` (a genus, or a genus and a subgenus).
- `pars`, `tentative` copied.

### `act`

Something this source does to a name. One claim per flag, `actKind` being:

| tree field | `actKind` |
|---|---|
| `new: true` on a named node | `new` (the protologue; F6 checks it) |
| `new: true` on a placeholder | `placeholder` (the source originates the placeholder; C4) |
| `type: true` | `type` (the fixation method joins when B14 lands) |
| `emended: true` | `emended` |
| `modifier: nomen transl.` (and `act: [nomTransl]` after B6) | `nomTransl`, with `altRankOf` giving the derived-from name |
| `corrected` | `corrected`, with the corrected form |
| `moved` | `moved`, with the group moved from |
| `removed` entry | `removed` (the source takes the name out of the group; B5) |
| `homonym: true` on the record | not a claim: key housekeeping |

### `certainty`

Not a kind of its own. The C-axis markers (`provisional`, `questionable`,
`quoted`, `tentative`, `pars`, `cf.`, `aff.`, `illustration.uncertain`) ride
on the claim they qualify, as fields. No separate table.

### `material`

Emitted for each `specimens` role entry, each `occurrences` entry and each
`illustrations` entry on a node. Fields added: `materialKind: specimen |
occurrence | illustration`, `role` as recorded today (`holotype`,
`paratypes`, `syntypes`, `unknowntypes`, …), `ids`, `repository`, and the
occurrence or illustration fields copied verbatim. The shape follows the
YAML as it stands; when D1 migrates material, only the extractor's
material adapter changes and these claims keep their fields.

### `editorial`

The node's `editorial` block emitted as a claim of its own, so a question
can ask whether a placement is the paper's or the editor's. Fields:
`inferred` (`true`, or the list of inferred fields), `source` (the resolved
source for a citation that cannot resolve as printed), `basis`. The claim
it qualifies carries the same block, so both directions are answerable.

## Derived coverage

Per source, the manifest holds the counts of claims by kind and by
`actKind`, beside the declared `audit.state` and `audit.coverage`. Per
taxon, the sources with any claim about it, in publication-year order.
Coverage is declared by a reviewer and counted by the extractor; they are
cross-checked, never conflated (G1): a source declaring `synonymy: all`
with zero `acceptance` claims, or `material: none` with any `material`
claim, is reported as an inconsistency.

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
  `placement` under `edrioasteroidea-order-uncertain_holloway_jell_1983`,
  whose claims carry `placeholder: uncertain`.
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
species node. The node's `occurrences` and `specimens` yield `material`
claims; the holotype claim has `role: holotype`, `repository: NHMUK`,
`ids: [E23470]`.

### Fay 1962, *ottawaensis* (`data/trees/1962_fay.yaml`)

`act` `type` on `ottawaensis_whiteaves_1897`, carrying `editorial:
{inferred: [type], basis: "Fay never prints \"type species\"; the genus is
monotypic (p. 201)"}`, plus a separate `editorial` claim with the same
block. A question "does Fay fix the type species?" is answered from the
act claim's `editorial.inferred`: the flag is the editor's, and the paper
prints monotypy. The `material` claim has `role: syntypes` and the node's
`notes` quoting "Holotype, 752" beside "labelled a syntype", so both printed
words are returned.
