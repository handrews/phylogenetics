# Schema audit: work remaining

What is left to do on `schemas/phylogeny.yaml`, and the evidence for each item.
Completed work has been removed — `git log notes/audits/schema-audit.md` has the history
if the reasoning behind a finished change is ever needed.

State as of 2026-09-08, `productize` @ `7518190`.

## How the numbers are produced

`scripts/schema_audit.py` measures usage from the `json-schema-engine` verbose
output tree, which records a schema location and an instance location for every
keyword evaluated and every subschema applied. That is the same per-keyword coverage an Istanbul-style JSON Schema
coverage tool gives, plus instance paths, using the validator the project already
depends on.

```bash
python scripts/schema_audit.py --markdown scripts/schema-usage.md
```

It regenerates [`schema-usage.md`](schema-usage.md) and exits non-zero if either
of its two self-checks fails: an independent raw-YAML walk that must agree with
the result-tree walk, and a cross-reference check that every `sourceId`-typed
value names a real record in `sources.yaml`.

**Corpus.** 218 tree files in `data/trees/` (one per source, since `trees.yaml`
was split), 2,743 taxa, 289 sources, 273 authors. `personal/` is censused
separately. Both `phylohist` and `phylohist --personal` currently exit 0.

## Reading the numbers

Low usage identifies a **candidate**, never a verdict. Zero or near-zero use is
equally consistent with four situations that look identical in the data:

- **abandoned** — superseded by a newer construct
- **rare by nature** — correct and needed, just uncommon (`authority.ex`, which
  encodes pre-Linnaean republication credit, has two uses and is right)
- **not built yet** — an intention that stalled
- **redundant** — another field already does the job

Only domain knowledge separates them. Three habits, each learned by getting it
wrong here:

1. **Read the sibling `notes` before flagging a value.** A page list of
   `[48, 198]` looked like a truncated range; its `notes` said "mentioned on page
   48, and in a footnote on page 198".
2. **Attribute a citation only from the node that owns it.** Walking up to the
   nearest ancestor `authority` misreported a `1972_chauvel` citation as
   `2005_frest`.
3. **Don't reason from consistency between two records** — they may be recording
   different things. A source's own entry lists the full page span discussing a
   taxon; another work's *citation* of it lists only the pages that citation gave.
   Both are correct.

---

## 1. Attribution: 171 taxa to migrate, 791 that stay

Two mechanisms, and the split is mostly legitimate:

| mechanism | taxa |
|---|---|
| `authority: {source: …}` | 1,550 |
| `auth` + `year` | 962 |
| both | 2 |
| neither | 229 |

`auth`+`year` is the **permanent** encoding for a taxon whose naming publication
cannot be cited as a source record — common for pre-1900 works, where often no
consistent formal citation exists. Matching each taxon's `auth` entries and
`year` against the `authors` and `pubDate.year` of every record in
`sources.yaml`:

| | taxa |
|---|---|
| no matching source — correctly on `auth`+`year` | **791** |
| a source exists, never switched over | **171** |

Of the 171, **117 have exactly one candidate** and convert mechanically; 54 match
several sources from the same author and year (`hall` 1858 matches both
`1858a_hall` and `1858b_hall`) and need a human decision.

`taxon.in` has 26 uses, every one on an `auth`+`year` taxon. It records that the
credited authors differ from the publication's authors, and stays on that side —
`authority` expresses the same thing through `attributedTo`.

## 2. The `auth` array mixes references and free text

Items are either an author id (all lower-case) or a free-form name:

| kind | uses | distinct |
|---|---|---|
| author-id references | 673 | all resolve — no dangling ids |
| free-form names | 521 | 220 |

Breaking the free-form half down against `data/authors.yaml`:

| | uses |
|---|---|
| exactly one existing author has that family name — mechanically convertible | **184** |
| several authors share the family name — needs disambiguation | **16** |
| no author record exists — one must be created | **321** |

The ambiguous names are `Miller` (→ `miller.j.s` / `miller.s.a`), `Gray`,
`Sowerby`, `Zhao`, and `Clark` (five candidates). `Hall` appears as a free-form
name while `hall` exists as an id and is referenced elsewhere — the same person
recorded both ways.

**Family-only author records are already schema-legal** — `$defs/person` requires
`anyOf: [family, given]` — but **none of the 273 authors uses that form**, so the
321 unrecorded names would be the first. Many are 18th–19th century figures whose
given names may be genuinely unknown (`Gmelin`, `Pallas`, `Pennant`).

Caution for this pass: an inline `# Lamarck` or `# Klein` on a taxon is *not*
formal attribution — it records the vague sense in which a pre-formalisation
author used the term. Do not sweep those into `auth`.

## 3. Occurrence-level specimens: the schema describes nothing

`basicOccurrence.specimens` and `possibleSpecimens` both put `items` under
`type: object`, where it is inert. **Any value passes today.**

The data has since settled on a consistent three-level shape that the schema does
not describe — role → repository → list of ids, where an id may be a range pair:

```yaml
specimens:
  holotypes: {NHMUK: [EE1659]}
  unknown:   {QMF: [[59647, 59653]]}      # a range of specimen numbers
```

30 occurrence-level specimen blocks use it (14 in `data/`, 16 in `personal/`).
This is now well enough specified to write properly, and it is the clearest
outstanding bug — a whole subtree currently validated by nothing.

Note this is a **fourth** specimen shape, alongside `$defs/specimens` (typed
roles), `$defs/specimen`, and `taxon.holotype`'s ad-hoc nested arrays. Worth
deciding whether they converge.

## 4. Stratigraphy: asymmetric, and cheap to fix while barely used

| | `data/` | `personal/` |
|---|---|---|
| `occurrence` instances | 32 | 32 |
| `basicOccurrence` instances | 33 | 35 |

Structural problems, all unexercised, so changing them costs almost nothing:

- **Rank coverage is lopsided.** `series` and `stage` have `Range`, `Boundary`
  and (for stage) `Modifier` variants; `period`, `era`, `eon` have none.
- **`seriesBoundary` and `seriesRange` are different concepts sharing one
  schema** (`$defs/seriesRange`) — a boundary between two intervals is not a
  range spanning them. Same for stages. All three are unused.
- **`biozone` / `biozones` / `biozoneRange` is a parallel shape** using inline
  arrays rather than the `localX` / `XRange` pattern beside it. `biozone` has 28
  uses, mostly in `personal/`.
- `localPeriod` is a bare string while `localSeries` and `localStage` get defs.
- The personal-tree fix folded `subunit` into `unit` as an array, leaving
  `subunit`, `superunit` and `section` unused. Decide whether they stay.
- Never reached: `eon`, `era`, `seriesRange`, `seriesBoundary`, `stageRange`,
  `localSeriesRange`, `localSeriesBoundary`.

**`eon` and `era` being unused is not a finding.** These enums transcribe
standards-body vocabularies; the corpus is Cambrian–Ordovician echinoderms, so
low coverage is data selection bias. The same goes for `stage` (12 of 100 values
used), `series` (8 of 38) and `period`. **Do not trim them.**

## 5. `$defs/article` and `sources.yaml`

Deliberately excluded from every pass so far, to be handled as a unit:

- `article.pages` uses the **flat alternating** start/end encoding (199 uses) —
  a fourth range notation, distinct from `multiRanges`.
- `article.plates`, `volume`, `number`, `articleNumber`, `chapter` and `series`
  still declare `[integer, string]` inline rather than using
  `$defs/citationNumber`, so that value space is only half-unified.
- `publication.type` is never set, relying entirely on its `default: journal`.

## 6. Dead leaves — ask which of the four kinds each is

Never reached by any data. Each still needs the abandoned / rare / not-built /
redundant question asked before removal:

- `taxon.modifier`, `taxon.reason` — `tree.modifier` has 20 uses; the taxon twins
  have none.
- `tree.categories`, `tree.data`, `tree.plates`
- `person.suffix`, `publication.type`
- `trees.<id>.source` — the map key already is the source id
- `illustration.source`, `illustration.location`, `illustration.collectedFrom`
- `specimens.allotype`, `specimens.neotype`, `specimens.repository` — repository
  prefixes are carried inline in the id strings (`NHMUK EE 1660`)
- **The entire object form of `$defs/specimen`** — `oneOf` branch 1
  (`repository`, `id`, `illustrations`) is unreached; all specimens are bare
  strings
- `taxon.holotype`'s innermost `items/items`

Rare enough to question: `tree.removed` (1 use), `tree.stem` (1), `tree.or` (3),
`tree.non` (4), `tree.mergeInto` (5).

## 7. Schema and code disagree

- **`tree.removed`** is valid in the schema and used once, but `Tree.__init__`
  (`phylohist/loader/taxa.py`) recurses `moved`, `corrected`, `or`, `synonyms`, `non`,
  `parents`, `altPlacements` and `children` — **not `removed`**. That node is
  invisible to every consumer.
- **Occurrences have no consumer at all.** No module in `phylohist/` references
  `occurrence`, `occurrences`, or any stratigraphic field.
- `io.py` initialises `data['personal']` and `data['time']`; nothing ever
  populates either. `data/geology.yaml`, `data/repositories.yaml`,
  `data/time.yaml` and everything in `notes/` are validated by nothing.
- `phylohist/support.py` and `phylohist/source.py` are orphaned and not imported
  anywhere; `support.py` cannot even be imported (it imports a non-existent
  `phylohist.author`) and embeds a stale key allow-set.

## 8. Uncertainty markers: ten overlapping ways to hedge

Plausibly all distinct, but they accreted over eleven months without a unifying
model, and several are rare enough that the distinction may not be load-bearing:
`openTaxon` (230), `provisional` (120), `needsQualification` (28), `quoted` (18),
`pars` (17), `tentative` (16), `affTaxon` (16), `cfTaxon` (15), `questionable`
(12), `illustration.uncertain` (1).

`tentative` defaults to `true` while every sibling boolean defaults to `false` —
worth confirming that inversion is deliberate.

Name-variant markers show the same spread: `altSpellingOf` (160),
`vulgarSpellingOf` (47), `altRankOf` (45), `homonym` (16), `bracket` (13, still
carrying its `### TODO: Replace this property name`), `synonym` (8), `status` (5),
`identifier` (4).

## 9. Dangling references in `personal/`

`personal/` now validates, but four source ids name no record: 
`2015_zamora_lefebvre_hosgör_franzen_nardin_fatka_álvaro` (5 uses),
`2026_andrews.h.h` (2), `2012_hung.d.y`, `2015_zhao.y.l_peng.j_wu.m.y`. The
audit script reports these separately and does not fail on them, since `data/` is
the gate; all 2,157 sourceId values there resolve.
