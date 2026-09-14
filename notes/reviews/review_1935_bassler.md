# Review: 1935_bassler — Bassler, "The Classification of the Edrioasteroidea"

**Page mapping.** PDF index *N* = printed page *N* − 1, for N = 2 through 12
(printed pp. 1–11), confirmed by the running heads ("2 SMITHSONIAN
MISCELLANEOUS COLLECTIONS VOL. 93" at PDF index 3; "NO. 8 EDRIOASTEROIDEA
BASSLER 3" at PDF index 4; etc., through "NO. 8 EDRIOASTEROIDEA BASSLER II"
[=11] at PDF index 12). PDF indices 0 and 1 are the unnumbered title leaf and
imprint leaf; index 13 is an unnumbered blank leaf; index 14 is the unnumbered
plate ("Plate 1," captioned "For explanation, see page 10"). All page numbers
below are printed page numbers.

## 1. Coverage

- Classification skeleton: **all**. Class → family → genus → species, plus
  the "Position Uncertain" section, captured completely and in the paper's
  own order (18 genera under Agelacrinitidae, 2 under Edrioasteridae, 2 under
  Cyathocystidae, matching the text exactly).
- New taxa (n. gen. / n. sp. / family "new name"): **mostly all**. All 6 new
  genera the paper announces ("six new generic names are proposed," p. 1:
  *Walcottidiscus*, *Cincinnatidiscus*, *Isorophusella*, *Foerstediscus*,
  *Cooperidiscus*, *Ulrichidiscus*) and all 3 new species ("n. sp.":
  *typicalis*, *cincinnatiensis*, *grandis*) are flagged `new: true`. Of the
  paper's two "new name" families, only one gets `new: true` (see §2).
- Type species (genotype statements): **all**. Every genus with a printed
  "Genotype.—" line has a matching `type: true` species node; none missing,
  none extra.
- Synonymy lists: **partly**. Most bracketed genus/family synonym lists are
  captured in full (e.g. the Class's 5-item list, p. 2; Discocystis's 2-item
  list, p. 8), but two lists are short one entry each, and two "not X"
  homonym citations are folded into the taxon they explicitly exclude rather
  than kept as separate identities (see §2, §3).
- Material (types/specimens): **none**. Holotypes, paratypes and a
  plesiotype are printed for the new species and forms (e.g. "Holotype.—
  U.S.N.M. no. 90754," p. 3; "Plesiotype.—U.S.N.M. no. S.3871," p. 5) but are
  not entered anywhere in the tree.
- Occurrences: **none**. Locality/horizon statements printed for the new taxa
  (e.g. "Burgess shale ... Burgess Pass near Field, B.C.," p. 3) are not
  entered.
- Illustrations: **none**. The plate and its 12-figure "Explanation of Plate"
  (pp. 10–11) are not entered.
- Diagnoses: **none**. The short morphological diagnosis printed for every
  family and genus is not entered; only identity, placement and flags are
  captured.
- Phylogeny: **not applicable**. The paper contains no cladogram or
  phylogenetic diagram.
- Attribution as printed (`auth`/`year`/`citedAs`): **none**. No node in this
  tree carries these fields, so every printed authorship in the paper —
  roughly 40 genus- and family-level citations with author and year — is
  invisible in the tree (recoverable only implicitly from `_author_year`
  suffixes on species keys). This matches the pattern already noted for
  other trees in `source-observations.md` ("nodes ... carry no attribution
  fields at all").

## 2. Correctness

Of the roughly 200 node- and entry-level identity/placement/flag claims in
the file, all genus-level `type: true` flags (≈20), all 6 new-genus flags,
all 3 new-species flags, and the great majority of `synonyms`/`parents`
entries match the printed text exactly. The following do not match, or
cannot be verified from this text.

| node | printed (page) | verdict |
|---|---|---|
| `agelacrinitidae` | "Family AGELAGRINITIDAE, new name" (p. 2) | **Mismatch.** No `new: true` on the node (only `corrected: {taxon: agelacrinidae}` and `synonyms: [thecocystidae]`), although the line is worded identically to Astrocystitidae's (below), which does get `new: true`. See §3 for why. |
| `astrocystitidae` | "Family ASTROCYSTITIDAE, new name" (p. 10) | **Inconsistent with `agelacrinitidae`, above**, not simply wrong: carries `new: true`, `corrected: {taxon: steganoblastidae}`, and `synonyms: [steganoblastidae]` — the same predecessor named twice under two different relations. The node's own `notes` explains the editor's reasoning; `agelacrinitidae`'s otherwise-identical case gets none. |
| `agelacrinites` synonyms | "(Agelacrinus authors; Agelacystis Haeckel, 1895; Haplocystites Roemer, 1852; Haplocystis Bather, 1899)" (p. 7) | **Mismatch.** Tree lists only 3 of 4 (`agelacystis`, `haplocystites`, `haplocystis`). "Agelacrinus authors" is missing, although the `agelacrinus` key exists and is used repeatedly elsewhere in this same tree as an original-combination target. |
| `edrioaster` synonyms | "(Cyclaster Billings, 1857, not Cotteau, 1856; Agelacrinites Forbes, 1848, not Vanuxem; Edriocystis Haeckel, 1896; Aesiocystites Miller and Gurley, 1894; Aesiocystis Bather, 1900)" (p. 9) | **Mismatch.** Tree lists only 4 of 5 (`cyclaster_billings_1857`, `edriocystis`, `aesiocystites`, `aesiocystis`). "Agelacrinites Forbes, 1848, not Vanuxem" is missing entirely. |
| `buchianus_forbes_1848` synonym entry, `parents: [agelacrinites]` | "Agelacrinites buchianus Forbes, 1848" (p. 9), where "Agelacrinites" is Forbes's own homonymous usage, explicitly marked "not Vanuxem" two lines above in the same synonymy | **Mismatch / identity conflation.** `parents` points at the `agelacrinites` key used throughout this tree for Vanuxem's genus (type species `hamiltonensis`), the very genus the printed line says this is *not*. No distinct record exists for Forbes's 1848 usage. |
| `cincinnatidiscus` synonym entry, `taxon: hemicystites` (`pars: true`) | "(Hemicystites of authors not Hall)" (p. 3) | **Mismatch / identity conflation, same pattern as above.** The synonym points at the `hemicystites` key used elsewhere in this tree for Hall's own 1852 genus (type species `parasitica`) — the very usage the printed phrase excludes. `notes` quotes the phrase but the target identity contradicts it. |
| `pilea_hall_1866` synonym entry, `parents: [lepidodiscus-subgenus, agelacrinus]` | "Agelacrinus (Lepidodiscus) pileus Hall, 1866" (p. 4) | **Cannot verify the bracket is a genuine 1866 subgenus.** This paper credits *Lepidodiscus* itself to "Meek and Worthen, 1868" (p. 8) — two years after the cited 1866 combination. `taxa.yaml`'s `lepidodiscus-subgenus` record already flags this ("as a genus its authority is two years later"), but the tree node that makes the combination claim carries no such caveat. |
| `kaskaskiensis_hall_1858` synonym entry, `parents: [agelacrinus-subgenus_discocystis, discocystis]` | "Genotype.—Echinodiscus optatus Worthen and Miller, 1883 = !). (Agelacrinus) kaskaskiensis Hall, 1858." (p. 8) | **Cannot verify.** OCR near this line shows no legible "Discocystis" at all — only "(Agelacrinus) kaskaskiensis Hall, 1858." `Discocystis` itself is Gregory, 1897, thirty-nine years after 1858. `taxa.yaml`'s `agelacrinus-subgenus_discocystis` record already carries "Copied auth/year from genus, unsure if correct." |
| Isorophus species list, "A. faceri Miller, 1894, A. -imrrcnensis James, 1883" (p. 5) | tree key `warrenensis_james_1883` | **Cannot verify spelling.** OCR reads "-imrrcnensis" (leading dash, no legible "w"); "warrenensis" is plausible but not independently confirmed by this text. |
| Class attribution, "Class EDRIOASTEROIDEA Billings, 1854-^8" (p. 2) | not captured on the `edrioasteroidea` node (no tree node carries attribution) | **Cannot verify the year.** OCR is illegible ("1854-^8"); moot for the tree since no node records it, but relevant if attribution is ever added for this source. |

## 3. Cases for the data model

**Parenthetical genus notation means two different things in one paper.** In
the systematic text, "X (Y) species" brackets a subgenus or contemporary
genus grouping, e.g. "Hemicystites (Cystaster) granulatus Hall, 1871" (p. 3,
same-year, unproblematic). In the plate explanation (pp. 10–11) the same
bracket shape is inverted into a "current genus (original genus) species"
cross-reference for readers using older literature: "Fig. 2, 3. Carneyella
(Agelacrinus) pileus Hall, 1866" (p. 10) drops the actual cited subgenus
*Lepidodiscus* that the systematic text uses for the same species ("Agelacrinus
(Lepidodiscus) pileus Hall, 1866," p. 4) and substitutes the plain original
genus. Six of the plate's ten described figures follow this "new(old)"
pattern (Figs. 2–3, 4, 5, 6, 7, 9). Illustrations aren't captured for this
source, so the conflict is latent, but a single bracket-reading rule cannot
serve both parts of this paper.

**A bracketed "subgenus" that postdates its own citation.** "Agelacrinus
(Lepidodiscus) pileus Hall, 1866" (p. 4) brackets *Lepidodiscus*, which this
same paper credits to "Meek and Worthen, 1868" (p. 8) — two years later. The
tree records the bracket as part of the original combination
(`parents: [lepidodiscus-subgenus, agelacrinus]`) with no flag on the node
itself; the caution lives only on the `lepidodiscus-subgenus` taxon record,
invisible to anyone reading the tree alone. The paper does not say whether
Hall himself wrote the bracket in 1866 or whether Bassler is annotating
retrospectively — worth stating as "cannot verify" rather than treating the
bracket as an unproblematic part of the 1866 citation.

**Two "not X" genus-homonym citations, conflated with the record they
exclude.** The paper prints three genus-level "A, author, year, not B, year"
citations: "Cyclaster Billings, 1857, not Cotteau, 1856" (p. 9), "Agelacrinites
Forbes, 1848, not Vanuxem" (p. 9), and "Hemicystites of authors not Hall"
(p. 3). Only the first is modeled with a distinct identity (`cyclaster` for
Cotteau's 1856 usage vs. `cyclaster_billings_1857`, `homonym: true`, for
Billings's). The other two have no distinct record at all: the citation
itself is missing from the tree's synonym lists (Agelacrinites/Forbes) or is
pointed at the very record it excludes (Hemicystites/Hall). This is the same
shape as the *Caryocystites*/*Heliocrinites* misidentification case already
worked out for the roadmap (B10): a name reused by a different author for a
different concept needs an anchor of its own, not a pointer to the name it
was mistaken for or excluded from.

**"New name" at family rank is handled two different ways for one wording.**
"Family AGELAGRINITIDAE, new name" (p. 2) and "Family ASTROCYSTITIDAE, new
name" (p. 10) are worded identically, each with one bracketed predecessor.
The tree's difference in treatment (`corrected`-only vs. `new` + `corrected`
+ `synonyms`) tracks each name's `taxa.yaml` authority choice — Astrocystitidae:
Bassler 1935; Agelacrinidae/Agelacrinitidae: Chapman, 1860 — not anything in
the printed line. The Chapman, 1860 attribution matches nothing in this
paper, which credits the superseded form to "Agelacrinidae Jaekel, 1899"
(p. 2); `taxa.yaml`'s own `thyroidea` record (also "Chapman, 1860") matches
the Class-level synonym printed on the *same page* ("Thyroidea Chapman,
1860"), suggesting the family record's authority may be a copy from the
adjacent entry rather than a reading of Jaekel 1899. Worth checking
independently of this tree, since it is the reason the two "new name" lines
are treated differently here.

**One "Position Uncertain" heading, two different kinds of doubt.**
Astrocystitidae and Cyclocystoididae are printed under one shared heading,
"POSITION UNCERTAIN" (p. 10), with no further subdivision. The tree treats
them differently: Astrocystitidae is a direct child of Edrioasteroidea with
`provisional: true` and `altPlacements: [blastoidea]`, matching the prose
("Regarded by Bather as an edrioasteroid and by Hudson as a blastoid" — doubt
about class membership); Cyclocystoididae is nested inside an
editor-invented placeholder, `edrioasteroidea-order-uncertain_bassler_1935`,
whose `notes` calls the printed "(order uncertain)" qualifier "odd ... because
no orders had been defined." The two families plausibly carry two different
kinds of doubt (class-membership doubt vs. order-placement doubt) bundled
under one heading, which would justify the different treatment — but nothing
in the tree states that reasoning; the placeholder's note reads as
unresolved puzzlement rather than as the rationale for the split.

**A declared new species built on an existing name.** "CARNEYELLA
CINCINNATIENSIS, n. sp." (p. 4) is immediately followed by a synonymy citing
the same epithet already published as "Agelacrinus (Lepidodiscus)
cincinnatiensis Hall (not Roemer)" in 1871 (and 1866 advance sheets) and
1872. This is the renaming case the brief flags: a `new: true` species built
directly on what the source's own synonymy suggests is a recombination of an
existing Hall name. Both `cincinnatiensis_bassler_1935` (tree `notes`:
"Claimed as new sp. but synonymized with the same species name from Hall?")
and the `taxa.yaml` record ("Probably an error of some sort, meaning
cincinnatiensis_hall_1866") already carry the ambiguity honestly rather than
resolving it — a workable precedent if a dedicated field for this shape is
ever added, since right now nothing distinguishes it structurally from an
ordinary new species.

**A rankless variety nested with no rank marker.** "S. walcotti and var.
minor Schuchert, 1919" (p. 2) is captured as `walcotti_schuchert_1919` with
`minor_schuchert_1919` nested as its child — the parent/child placement is
right, but nothing records that Schuchert's own rank for `minor` was "var."
(a rank below species), since the tree has no rank field at this level.

## 4. Source record check

`sources.yaml`'s `1935_bassler` block: title ("The Classification of the
Edrioasteroidea"), journal (`smith-misc`, Smithsonian Miscellaneous
Collections), volume 93, number 8, `pubDate` 1935-04-04, and author
(`bassler`) all match the printed title page ("BY R. S. BASSLER ... APRIL 4,
1935"). The block has **no `pages` field**: the article's printed pagination
is pp. 1–11 (confirmed by running heads) plus one unnumbered plate ("With
One Plate"); this range is absent from the record.

## 5. Uncertainties

- "Class EDRIOASTEROIDEA Billings, 1854-^8" (p. 2): the year is illegible in
  OCR; cannot verify whether it reads 1858 or something else. Not captured
  on the tree's root node regardless.
- "A. -imrrcnensis James, 1883" (p. 5): cannot verify the epithet is
  "warrenensis" from this text alone.
- "Genotype.—Echinodiscus optatus Worthen and Miller, 1883 = !). (Agelacrinus)
  kaskaskiensis Hall, 1858." (p. 8): badly garbled; cannot verify whether a
  bracketed "(Discocystis)" or any other subgenus was printed at all.
- Plate caption "Fig. 5. Streptaster (Agelacrinus) vorticcUaius Hall, 1856"
  (explanation of plate, p. 10) gives 1856 where the main text (p. 5) gives
  "Agelacrinus vorticellatus Hall, 1866" for the same species. Cannot tell
  from this scan whether this is an OCR misread or a printed slip; moot for
  the tree since illustrations aren't entered for this source.
- Minor OCR-affected spellings elsewhere in species lists (e.g. "latinscuius"
  for presumed *latiusculus*, p. 7; "5. halticus" for presumed *S. balticus*,
  p. 2) are plausible from established usage and not flagged individually.
- The plate itself (unnumbered leaf, PDF index 14) was read only as a
  caption; the figured specimens were not independently inspected as images.
