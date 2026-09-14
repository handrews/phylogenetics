# Review: 1983_holloway_jell

Holloway, D. J. and Jell, P. A. 1983. "Silurian and Devonian Edrioasteroids
from Australia." *Journal of Paleontology* 57(5): 1001–1016, 7 figs.
September 1983.

**Page mapping.** Printed page-foot numbers appear directly in the text
throughout: p. 1001 (running head, ends ~char 5559 of the plain-text file), p.
1002 ends with digit 1002, 1003 (a plate page, almost no OCR text), 1004,
1005, 1006, 1007 (plate page), 1008, 1009, 1010, 1011 (plate page), 1012,
1013 (plate page), 1014, 1015, 1016 (References). Each cited passage below
gives its printed page directly.

## 1. Coverage

The tree (17 lines, 5 species across 3 families plus one indeterminate genus)
captures the full classification skeleton with correct `new` flags, but no
diagnosis, no type-species citation detail, no material, no occurrence, and
no illustration anywhere.

| kind | captured | example |
|---|---|---|
| classification skeleton | all | class > order-uncertain placeholder > family > genus > species (Rhenopyrgidae branch) and class > order > 3 families > genera > species (Isorophida branch), matching the printed "SYSTEMATIC PALEONTOLOGY" hierarchy exactly, including the "gen. et sp. indet." leaf |
| new taxa | all | family Rhenopyrgidae, genus *Epipaston*, and four new species all flagged `new: true` |
| type species | none captured as such | `type: true` flags are present on 4 species, but none records the printed "Type species.—Original designation..." wording or locality (§2–3) |
| synonymy lists | partly | 3 recombination notes captured (bare `parents`, no citation detail, §2); the Isorophidae/Hemicystitidae priority synonymy is captured; the *R. grayae* recombination's supporting argument (pp. 1004–1005) is not |
| material | none | every type-material list (holotype/paratype NMV numbers, 5 times) is absent from the tree |
| occurrences | none | every locality (Kinglake West, Clonbinane, etc.) and horizon (Ludlovian, Dargile Formation, etc.) is absent |
| illustrations | none | none of Figures 1–7 (all captioned with catalogue numbers and magnifications) are recorded |
| diagnoses | none | none of the ~8 printed diagnoses (family, 3 genera, 4 species) are stored, including 2 that are explicitly deferred rather than restated (§3) |
| phylogeny | none | no diagram; the paper's placement argument for Rhenopyrgidae (pp. 1002–1004) is prose only |

In one sentence: the classification skeleton, `new` flags, and `type` flags
are fully and correctly captured; diagnoses, material, occurrences, and
illustrations are not captured for any of the paper's five families.

## 2. Correctness of what is captured

| node | printed (page) | verdict |
|---|---|---|
| `openTaxon: edrioasteroidea-order-uncertain_holloway_jell_1983` | "Class EDRIOASTEROIDEA / Order UNCERTAIN / Family RHENOPYRGIDAE n. fam." (p. 1002) | match — see §3 for a nuance on what kind of uncertainty this is |
| `rhenopyrgidae`, `new: true` | "Family RHENOPYRGIDAE n. fam." (p. 1002) | match |
| `rhenopyrgus` (bare key, genus rank by the dataset's convention) | "Genus RHENOPYRGUS Dehm, 1961" (p. 1002) | match — correctly the genus-rank identity record, in contrast to `1961_dehm.yaml`'s own use of this name (see that review) |
| `coronaeformis_rievers_1961`, `type: true` | "Type species.—Original designation; *Pyrgocystis coronaeformis* Rievers, 1961..." (p. 1002) | match |
| `coronaeformis_rievers_1961` `synonyms: [{taxon: coronaeformis_rievers_1961, parents: [pyrgocystis]}]` | the whole paper's argument is that the species was originally combined in *Pyrgocystis* and is here kept in *Rhenopyrgus*, per Dehm's designation | match in substance, but the entry has no `auth`/`year`/`pages`/`citedAs` — see the general pattern flagged below |
| `grayae_bather_1915` under `rhenopyrgus`, `synonyms: [{parents: [pyrgocystis]}]` | "Other species included.—*Pyrgocystis grayae* Bather, 1915..." (p. 1004) — a new recombination *by this paper*, not merely a repeated one | **partial** — the recombination is real and correctly placed, but it is *this paper's own taxonomic act* (a page and a half of argument, pp. 1004–1005, on whether *grayae*'s ambulacral plates match *Rhenopyrgus*), not a passively-inherited synonym; nothing on the node marks that the recombination itself is new here, and (as above) no citation detail is attached to the `parents` entry |
| `whitei_holloway_jell_1983`, `new: true` | "RHENOPYRGUS WHITEI n. sp." (p. 1004) | match |
| `isorophida` (no `new`/`emended`) | "Order ISOROPHIDA" (p. 1006, no author printed here) | match |
| `lebetodiscidae` (no `new`) | "Family LEBETODISCIDAE Bell, 1976a" (p. 1006) | match |
| `epipaston`, `new: true` | "Genus EPIPASTON n. gen." (p. 1006) | match |
| `ixine_holloway_jell_1983`, `type: true`, `new: true` | "Type species.—*Epipaston ixine* n. gen., n. sp...." (p. 1006) | match |
| `pyrgocystidae` (no `new`) | "Family PYRGOCYSTIDAE Kesling, 1967" (p. 1010) | match |
| `pyrgocystis` > `sardesoni_bather_1915`, `type: true` | "Genus PYRGOCYSTIS Bather, 1915 / Type species.—Original designation; *Pyrgocystis sardesoni* Bather, 1915..." (p. 1010) | match |
| `petalus_holloway_jell_1983`, `provisional: true`, `new: true` | "PYRGOCYSTIS? PETALUS n. sp." (p. 1010) — the "?" sits before the genus, not the species | match — correct use of `provisional` for a "?" before the parent, per the roadmap's C table |
| `hemicystitidae`, `synonyms: [{taxon: isorophidae}]` | "Family HEMICYSTITIDAE Bassler, 1936 / *Isorophidae* BELL, 1976a, p. 147. / Remarks.—If the composition of the Isorophidae proposed by Bell (1976a) is accepted, the name Hemicystitidae clearly has precedence for this family." (p. 1012) | match in substance — a genuine priority synonymy, correctly modeled as a family-level `synonyms` entry, but again with no citation detail (page "147" is printed and lost) |
| `isorophus` > `cincinnatiensis_roemer_1851`, `type: true`, `synonyms: [{parents: [agelacrinus]}]` | "Genus ISOROPHUS Foerste, 1917 / Type species.—Original designation; *Agelacrinus cincinnatiensis* Roemer, 1851..." (p. 1012) | match, including the `agelacrinus` spelling (the source prints "Agelacrinus," matching the `altSpellingOf: agelacrinites` record) |
| `pannosus_holloway_jell_1983`, `new: true` | "ISOROPHUS PANNOSUS n. sp." (p. 1012) | match |
| `openTaxon: isorophida-genus-indeterminate...` > `openTaxon: isorophida-sp...` | "ISOROPHIDA gen. et sp. indet." (p. 1015) | match — correctly modeled as two nested placeholders |

**Recurring gap: `synonyms`/`parents` entries carry no citation.** All three
recombination entries in this tree (`coronaeformis`, `grayae`,
`cincinnatiensis`, plus the family-level `isorophidae` synonym) omit
`auth`/`year`/`pages`/`citedAs`, even though every one of the underlying
citations is fully printed and page-located in the text (e.g., "Bather, 1915"
p. 1004; "Roemer, 1851" p. 1012; "BELL, 1976a, p. 147" p. 1012). This is the
same gap already flagged in the 1961_dehm review, appearing four times in
this file alone — a pattern rather than an isolated slip.

## 3. Cases for the data model

**The family protologue defers its diagnosis to the genus.** Family
Rhenopyrgidae's protologue (p. 1002) reads, in full:

> "Family RHENOPYRGIDAE n. fam. Remarks.—This family, which includes only
> *Rhenopyrgus*, is distinguished by the characters cited in the generic
> diagnosis below. The most significant of these are the very tall,
> columnar theca with a basal sac, the structure of the ambulacra, and the
> lack of any clear distinction between the oral plates and the ambulacral
> coverplates. This combination of features represents a taxonomic
> difference at least comparable with that between other families currently
> recognized within the Edrioasteroidea."

There is no separate "Diagnosis" heading for the family at all — only
"Remarks," which explicitly points to the genus diagnosis instead of
restating it. This is the same deferral pattern documented in the companion
1978 Bell & Sprinkle review (there: genus deferring to species; here: family
deferring to genus), and it recurs a third time later in this same paper
("*Epipaston ixine* n. gen., n. sp. ... Diagnosis.—As for genus," p. 1008).
None of the current fields distinguish "no diagnosis printed" from "diagnosis
deliberately deferred to a named other node," and the tree's `rhenopyrgidae`
node has no `diagnosis` field at all, so this deferral itself is invisible.

**The family's type genus is fixed by explicit monotypy, not by a "type
genus" sentence.** No "Type genus" line is ever printed for Rhenopyrgidae —
the family is simply stated to "include only *Rhenopyrgus*," and *Rhenopyrgus*
is also the name Rhenopyrgidae is formed from, so the type genus is fixed
both by name-formation and by explicit, printed monotypy. Contrast this with
the genus-level type-species fixations in the same paper, which are always
stated formally ("Type species.—Original designation; ..."), four times. The
family-level fixation is real but stated in ordinary prose ("which includes
only Rhenopyrgus") rather than in the formal apparatus the genus level uses
consistently — worth noting since the tree's `rhenopyrgidae` node has no
marker recording the type-genus fact at all (unlike the species-level nodes,
which do get `type: true`).

**Order placement left explicitly unresolved between two named
candidates — not a "bin," not "unnamed."** The heading "Order UNCERTAIN"
(p. 1002) is followed by an extended, two-sided argument (pp. 1002–1004)
weighing whether Rhenopyrgidae belongs in order Isorophida or order
Edrioasterida:

> "The placement of the Rhenopyrgidae within either of the edrioasteroid
> orders recognized by Bell (1976a) is uncertain because little is known
> about the structure of the oral region in *Rhenopyrgus*... However, there
> is a strong resemblance to the genus *Timeischytes* Ehlers and Kesling,
> 1958... Timeischytes was included by Bell (1975) in his suborder
> Cyathocystina of the order Isorophida... Alternatively, the lack of any
> clear distinction between the oral plates and the ambulacral coverplates
> in *Rhenopyrgus* and the presence of the basal sac could be used to argue
> for a relationship with the Edrioasterida." (p. 1002)

This differs from both senses the roadmap's C4 distinguishes: it is not a
"bin" (there is exactly one family here, not a heterogeneous group that need
not form a real taxon), and it is not "unnamed" (the source does not lack a
name for the order — it names two specific candidate orders and cannot
choose between them). The current `openTaxon` placeholder captures the
heading correctly (matching the C5 precedent for "Order and Family
Uncertain"), but the two-candidate argument that gives the uncertainty its
actual content lives only in prose the tree does not reference at all — no
`notes` field anywhere in the file records it.

**A secondhand claim that appears to contradict its own cited source (B19).**
On p. 1004, discussing which other *Pyrgocystis* species might belong in
*Rhenopyrgus*:

> "*P. octogona* Richter, 1930 was assigned to *Rhenopyrgus* by Dehm (1961)
> but the oral and basal features of this species are not known either."

But Dehm's actual 1961 paper (reviewed separately) does the opposite: after
comparing *coronaeformis* and *octogona* at length, Dehm concludes "es
[ist] erforderlich, diese Formen gesondert zu halten" ("it is necessary to
keep these forms separate," p. 16) and defines *Rhenopyrgus* with
*coronaeformis* as its sole type species — *octogona* is discussed as a
close relative, never assigned to the new subgenus. This looks like exactly
the B19 pattern ("Parsley 2021... cites Dzik & Orłowski 1993 for a placement
those authors argued against"), and it sits inside the gold slice's own
cross-citation web (Dehm 1961 → Holloway & Jell 1983), so both works being in
this dataset makes the comparison checkable rather than merely suspected.
Neither tree currently carries a `notes` recording it.

**An explicit rank-elevation argument, contra two named prior authors
(B18).** p. 1004:

> "Although considered to be a subgenus of *Pyrgocystis* by Dehm (1961) and
> Regnell (1966), *Rhenopyrgus* differs from that taxon in the presence of
> the basal sac; the much higher turret... In fact the differences are so
> great that we discount the possibility of an evolutionary relationship
> between these genera, as suggested by Dehm (1961). We consider the
> presence of a columnar theca in both of them to be due to homeomorphy."

This is the printed argument behind the B18 same-name-different-rank split
already present in `taxa.yaml` (`rhenopyrgus` vs. `rhenopyrgus-subgenus`).
The tree correctly uses the bare (genus-rank) key here, but the reasoning
itself — an explicit, named rejection of Dehm's and Regnell's subgenus rank
and of Dehm's proposed evolutionary relationship — is not recorded anywhere,
even as a `notes` quote.

**No acts on edrioblastoids.** Edrioblastoidea and *Astrocystites* are never
mentioned in this paper (checked exhaustively); the "edrioblastoids" prompt
for this review turns up nothing to report.

## 4. Source record check

`sources.yaml`'s `1983_holloway_jell` record matches the printed article in
full, including the manuscript dates: title, journal `jofpaleo`, volume 57,
number 5, pages 1001–1016, `pubDate: {year: 1983, month: 9}`,
`processDates: {received: 1981-11-06, revised: 1982-03-22}` — all confirmed
by the paper's own end-of-article line, "MANUSCRIPT RECEIVED NOVEMBER 6,
1981 / REVISED MANUSCRIPT RECEIVED MARCH 22, 1982" — authors `holloway` +
`jell`, `identifiers.jstor: 1304766` (matches the Stable URL). No
discrepancy.

## 5. Uncertainties

- Pages 1003, 1007, 1011, and 1013 are full-page plates with almost no OCR
  text; nothing bibliographically relevant was expected or found there.
- The Foerste 1916/1917 *Isorophus* date question (flagged in the companion
  1978 Bell & Sprinkle review, where the same taxon appears on the record
  side) recurs here on the printed side: this paper's own heading reads
  "Foerste, 1917," which **cannot be verified** against Foerste's original
  without that source.
- Whether the B19 discrepancy over *P. octogona* (§3) is Holloway & Jell's
  misreading of Dehm, a citation slip, or reflects context from Dehm 1961's
  correspondence with Holloway & Jell (acknowledged on p. 1016: Dehm sent
  them photographs of *Rhenopyrgus coronaeformis*) that is not in the printed
  text, cannot be settled from the two papers alone.
