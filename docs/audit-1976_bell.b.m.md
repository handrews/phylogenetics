# Audit sample: `1976_bell.b.m` against the monograph

Bell, B. M. 1976. *A Study of North American Edrioasteroidea*. New York State
Museum Memoir 21. Read from the PDF text layer (OCR; page numbers below are
the printed ones). Compared against `data/trees/1976_bell.b.m.yaml` at
`roadmap` @ `767abd2`.

Scope: the whole monograph at the level of its table of contents, then the
genus *Lebetodiscus* and *L. dicksoni* (pp. 54–65) line by line. The rest of
the systematic section (pp. 65–314) is unaudited.

Proposed audit state for this source: **partial**, with the notes below.

## 1. Whole-monograph coverage

What the tree file captures, by kind of statement:

| statement kind | captured | evidence |
|---|---|---|
| classification skeleton, all ranks | all | every taxon in the contents (pp. vii–ix) is present, in order |
| new taxa (`new: true`) | all | 8 genera and 6 species listed in the abstract (p. 1) all flagged |
| type species (`type: true`) | all named | matches the "Type species" lines in the Diagnostic Summary (pp. 41–48) |
| provisional placements | 3 of 4 | `jasperensis`, `alpenensis`, `saratogensis` flagged; `valcourensis` is "(?)" in the summary (p. 43) but unflagged in the tree — check the heading on p. 129 |
| diagnoses | 12 | Edrioasteroidea through *Streptaster vorticellatus*; none from *Cystaster* (p. 91) onward |
| original combinations (`synonyms` + `parents`) | 13 species | e.g. *vorticellata* under *Agelacrinus*; missing for *dicksoni*, *austini*, *warrenensis*, *granulatus*, *stellatus*, *faberi*, and others |
| genus synonymy lists | 1 of 24 | *Lebetodiscus* only, and only through 1908 (see §2) |
| species synonymy lists | 0 of 46 | |
| material (specimens, roles, measurements) | 0 | every species has a "Specimens" section |
| occurrences | 0 | every species has "Range and occurrence"; family-level ranges on pp. 49–50 |
| illustrations | 0 | text figures and plates are assigned per specimen |
| taxa treated only in range lists | 0 | Stromatocystitidae, Cyathocystidae, Pyrgocystidae placed under Edrioasteroidea as "Others" (p. 50) with their genera in brackets |
| earlier classifications summarized | 0 | Jaekel 1899, Bather 1900, Bassler 1935–36 reproduced in "Previous Investigation" (pp. 4–8) |

The skeleton is complete and correct. What is missing is everything the
monograph says *about* each taxon beyond its placement.

## 2. *Lebetodiscus* Bather, 1908 (p. 54) and *L. dicksoni* (pp. 55–65)

### Genus synonymy, line by line

| printed (p. 54) | tree file | verdict |
|---|---|---|
| 1842 [non] Agelacrinites Vanuxem, p. 158, fig. 80 | `non` entry, 1842_vanuxem, p. 158, fig. 80 | matches |
| 1857 Agelacrinites Vanuxem, Billings, pp. 294–295 | 1857_billings, `citedAs` | matches |
| 1858b Agelacrinites, Billings, dec. 3: 84, pl. 8, fig. 3, 3a, 4, 4a | 1858b_billings, p. 84, pl. 8 figs | matches |
| 1881 Agelacrinites, Grant, pl. 1, fig. 9 | grant 1881, pl. 1 fig. 9 | matches |
| 1887 Agelacrinites, Barrande [partim], 55, 83 | barrande 1887, `pars`, pages [55, 83] | matches |
| 1896b Agelacrinus, Haeckel, pl. 3, fig. 29 | 1896_haeckel, pl. 3 fig. 29 | matches; the printed "b" is not recorded |
| 1899 Agelacrinites, Jaekel [partim], 50, pl. 2, fig. 2 | 1899_jaekel, `pars`, p. 50 | matches |
| 1901 Agelacrinites, Clarke, 191, text fig. 3 | clarke.j.m 1901 | matches |
| 1908 Lebetodiscus Bather, 543–550, pl. 25, fig. 1 | bather **1901**, pages [[543, 550]] | **year wrong**: 1908 printed; `taxa.yaml` also has 1908 |
| 1915 Lebetodiscus, Raymond [partim], 53–56, pl. 1, fig. 6 | — | missing |
| 1921 Lebetodiscus, Raymond [partim], 4–7, pls. 1–3 | — | missing |
| 1935 Lebetodiscus, Bassler, 6 | — | missing |
| 1936 Lebetodiscus, Bassler, 9, pl. 3, fig. 10 | — | missing |
| 1938 Lebetodiscus, Bassler, Fossilium Catalogus, 122 | — | missing |
| 1943 Lebetodiscus, Bassler & Moodey, 206 | — | missing |
| 1946 Lebetodiscus, Wilson, 19; *Lepidoconia* Wilson, ibid.: 21, pl. 4, fig. 2 | — | missing; two names in one line |
| 1966 Lebetodiscus, Regnéll, U165, text fig. 127-4; *Lepidoconia*, idem, U165, text fig. 127-1 | — | missing; two names in one line |

Also on p. 54: "Type species: *Agelacrinites dicksoni* Billings, 1857"
(captured as `type: true` on the species), and "Range and occurrence: Middle
Ordovician through Upper Silurian of eastern North America and Australia" at
family level (not captured).

### Species synonymy (p. 55), none captured

Eighteen lines, 1825–1966. The ones that matter for the model:

- **1825 "A Fossil Belonging to the Class Radiaria", Sowerby** and **1848 "A
  remarkable American fossil", Forbes**: usages with no name at all, cited by
  the descriptive phrase. The data already has the placeholder
  `asteriadae-gen-sp_sowerby.g.b_1825`, and Forbes 1848 already lists it as a
  synonym, so both lines can be recorded as `openTaxon` usages.
- **1857 *Agelacrinites dicksoni* Billings**: the protologue, in the original
  combination. This is the missing `synonyms` + `parents` entry.
- **1908 *Lebetodiscus dicksoni* (Billings), Bather**: the new combination.
- **1915 Raymond**: *L. dicksoni* and, on the same line, *Lebetodiscus
  loriformis* Raymond, ibid.: 56, pl. 1, fig. 6 — a junior synonym erected in
  the same work. `loriformis_raymond_1915` exists in `taxa.yaml`.
- **1946 Wilson**: *Lepidoconia loriformis* (Raymond) — a new genus for the
  synonym. `lepidoconia` exists in `taxa.yaml`.
- **1966 Regnéll** in the Treatise: both names, with text figure numbers.

### Type and material (pp. 60–62)

| specimen | printed status | notes for the model |
|---|---|---|
| GSC 1407-B | "Fragment of the holotype … believed to be a fragment of the holotype … the remainder of the holotype is apparently lost"; "must be considered the holotype by monotypy" (p. 62) | a holotype known only as a fragment; type fixation by monotypy stated explicitly |
| GSC 437 | "Illustrated Specimen of *L. dicksoni* by Grant (1881) and others"; the "Grant specimen" | a role the paper prints as a proper noun; a specimen with a nickname |
| GSC 1414 | "Holotype of *Lepidoconia loriformis* (Raymond) (1915, p. 56)" | holotype of a name this source synonymizes; the type role belongs to the other name |
| GSC 1412 | "Illustrated Specimen … by Raymond (1921, pl. 3, fig. 1)"; the "Fitzpatrick specimen" | |
| ROM 161-t-a | "described by Raymond (1915, 1921) and by Wilson (1946) as 'GSC 1415'"; Wilson "erroneously considered the specimen to be the holotype" (p. 61) | one specimen under two catalogue numbers in two repositories over time; a published error about type status, corrected here |
| ROM 18848-A, ROM 18855 (A–C) | measured, figured | 18855 is three individuals under one number with letter suffixes |
| YPM 28451 (old 2361) | "one of ten specimens labeled *Edrioaster*"; only specimen from outside Ottawa | renumbered; formerly misidentified in the collection |
| the Bigsby specimen | "illustrated and briefly described by Sowerby (1825), mentioned by Forbes (1848), illustrated by Billings (1858), and illustrated and described in detail by Bather (1908)"; "not available for reexamination" (p. 63) | no catalogue number anywhere; identity carried entirely by four works' figures; the first edrioasteroid ever reported (p. 4) |
| Jaekel 1899 specimen (Breslau); Ami 1905 specimen (Dickson collection) | "Three other representatives … have been reported" | reported, not examined; known only from other works |

Each examined specimen carries text-figure and plate assignments (e.g. GSC
437: pl. 1, fig. 9–11; GSC 1414: text fig. 4B–D, pl. 2, fig. 1–6) and two
diameters in millimetres.

### Occurrence (p. 65)

"Trenton Limestones, Middle Ordovician, Ottawa region, Ontario (including
Peterborough, Ontario), and Mercer County, Kentucky." Bracketed: "the
stratigraphic occurrence of all known specimens is 'Cobourg beds' (= the
'Cystid beds, about 180 feet below the top of the Trenton'). The Kentucky
specimen is listed as Lower Trenton." Per specimen, the horizon is given as a
quoted unit name, a group, a series, and a system, e.g. "'Trenton Limestone,'
Trenton Group, Mohawkian Series, Middle Ordovician."

## 3. Repository abbreviations are per publication (p. 2)

Bell defines his own table. Two entries collide with modern usage:

- **UCMP** = Museum of Paleontology, University of Cincinnati. In current
  usage UCMP is the University of California Museum of Paleontology.
- **CFM / CFMP / CFMPE / CFMUC** = Field Museum collections, now cited as FMNH.

So a prefix cannot resolve globally. Resolution has to be scoped to the
source, with `repositories.yaml` holding defaults and each source able to
override.

## 4. Findings to act on

1. **Data error (confirmed, to fix).** In the tree file, the *Lebetodiscus* synonymy entry for
   Bather's own genus (`taxon: lebetodiscus`, `auth: [bather]`) has `year:
   1901`; the paper prints 1908 (p. 54) and `taxa.yaml` has 1908. The 1901
   entry immediately above it, Clarke's *Agelacrinites*, is correct.
2. **Confirmed (to fix: `provisional` under *Carneyella*).** Bell heads the species "( ?) *Carneyella valcourensis*
   Clark, 1920" on p. 129 and writes that "determination of specific and even
   most generic characters is questionable". The tree marks *jasperensis*,
   *alpenensis* and *saratogensis* `provisional` for the same printed form;
   *valcourensis* should match.
3. **Attribution to check.** `taxa.yaml` credits Carneyellinae, Isorophinae
   and Lebetodiscinae to `1976_bell.b.m`, but the monograph's text contains no
   subfamily names of its own (its only "subfamily" mentions quote Jaekel's
   Hemicystida and Asterocystida, p. 7), and the tree file has no subfamily
   nodes. Surfaced by the protologue check added in step 0; either the
   authority is another work or the nodes are missing here.
4. **Capture, in priority order for the gold slice:** the rest of the
   *Lebetodiscus* synonymy; the *L. dicksoni* synonymy and material; the
   "Others" placements on p. 50; then the same for the remaining
   Edrioasteroidea genera.

## 5. What this source shows about the model

Recorded here so the roadmap can cite a real page for each:

- A specimen's identity can change number and repository (ROM 161-t-a was GSC
  1415), be renumbered within a repository (YPM 28451, old 2361), be a fragment
  of a lost original (GSC 1407-B), or have no number at all (the Bigsby
  specimen). Material entries need `formerIds`, `fragmentOf` or a note, and
  the ability to exist without a catalogue number.
- A published statement can be about another work's error (Wilson's holotype
  claim), which is a claim this source makes about that source.
- Role vocabulary is the author's: "Illustrated Specimen" here; "hypotype"
  or "plesiotype" elsewhere. Record the printed word.
- "Holotype by monotypy" is a fixation statement for a species-group name,
  parallel to the genus-level OD/M/SD.
- A synonymy line can carry two names from one work, a descriptive phrase
  instead of a name, or the author's own year-letter ("1858b", "1896b") that
  need not match this dataset's source keys.
- Bell's own attribution is "1976", but he cites the manuscript date
  (submitted January 26, 1973, p. 1) and Bell 1975 cites the work as "Bell,
  1974". The printed attribution and the resolved work are different facts.
