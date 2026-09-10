# Review: 1900_bather — "The Echinoderma", Part III of Lankester's *A Treatise on Zoology*

Tree: `data/trees/1900_bather.yaml` (82 lines, one `taxonomies` tree, no
`phylogenies`).

## Page mapping

OCR text: `1900-00-00-p.txt` (362 "PDF page index" pages). Formula
confirmed at both ends of the examined ranges: **printed page = PDF index −
13** (index 14 carries the printed folio "1", with footnote "By F. A.
Bather, M.A."; index 347 carries "334"; index 90/218/229 carry "77"/"205"/
"216"). Chapter boundaries from the Contents page (index 12) and confirmed
by the running heads: Ch. VIII General Description pp. 1–37; Ch. IX Cystidea
pp. 38–77; Ch. X Blastoidea pp. 78–93; Ch. XI Crinoidea pp. 94–204; **Ch.
XII Edrioasteroidea pp. 205–216**; Ch. XIII Holothurioidea from p. 217. All
citations below are printed-page numbers by this formula.

## Coverage

| kind | coverage | note |
|---|---|---|
| classification skeleton | all | Every rank from Kingdom to Sub-family in the tree matches the book's own scaffolding, checked section by section (below) |
| new taxa | partly | 3 nodes flagged `new: true` (Eocystidae, Tiaracrinidae, Steganoblastidae); one of the three (Tiaracrinidae) is very likely mis-flagged — see Cases |
| type species | none | No genus-rank nodes exist anywhere in the tree |
| synonymy lists | partly | The class-level synonymy of Edrioasteroidea (4 names) is captured as `synonyms`; no attribution is captured for any of them, though the book prints one for each |
| material / specimens | none | — |
| occurrences | none | — |
| illustrations | none | The book has dozens of numbered figures in the sections covered; none are referenced |
| diagnoses | partly | Two `notes` fields carry a diagnostic/explanatory quote (`amphorida`, `blastoidea`); no other node carries diagnosis text, though most families and orders in the covered chapters have one in print |
| phylogeny | none | No `phylogenies` tree exists; the book's own phylogenetic argument (e.g. the Dipleurula-ancestor reasoning, pp. 1–7) is prose, not a diagram, in the sections read |

Per G9, this is scope, not error: the tree captures the classification's
shape cleanly and stops there.

## Correctness of every node

35 of 39 nodes match the print cleanly on identity, rank, placement and
(where present) notes: `animalia`, `protozoa-grade`, `parazoa-branch`,
`enterozoa-branch`, `enterocoela-grade`+`coelentera-grade` (synonym),
`coelomocoela-grade`+`coelomata-grade` (synonym), `echinoderma`,
`pelmatozoa-grade`, `cystidea`, `aristocystidae`, `dendrocystidae`,
`eocystidae`, `anomalocystidae`, `echinosphaeridae`, `comarocystidae`,
`macrocystellidae`, `malocystidae`, `glyptocystidae`, `echinoencrininae`,
`callocystinae`, `glyptocystinae`, `caryocrinidae`, `aporita`,
`cryptocrinidae`, `diploporita-order`, `sphaeronidae`, `glyptosphaeridae`,
`protocrinidae`, `mesocystidae`, `gomphocystidae`, `blastoidea`, `crinoidea`,
`agelacrinidae`, `cyathocystidae`, `edrioasteridae`, `eleutherozoa-grade`,
`holothuroidea`, `stelleroidea`, `echinoidea`. The `blastoidea` node's notes
quote — "Their line of evolution, though in some respects parallel to those
of the Callocystinae and Edrioasteroidea, was independently derived through
the Diploporita from the primitive Amphoridea" — is verified word for word
against pp. 78–79 (it straddles the page break).

Mismatches and cannot-verify rows:

| node | printed (page) | verdict |
|---|---|---|
| `metazoa-grade` | Tabular statement (p. [xii], index 13) shows "GRADE I. PROTOZOA." then a badly garbled line, OCR "MOEPAIGA", then "BRANCH A. BRANCH B. PARAZOA. ENTEROZOA." | **cannot verify** — the garbled line is the only candidate for "GRADE II. METAZOA." between Protozoa and the two branches; plausible but not legible |
| `amphorida` (notes) | "ORDER 1. Amphoridea, Haeckel (1896, pars)." (p. 43) | mismatch — the tree's own `notes` field spells it "Haekel (1896, pars)", missing the second "c"; the same misspelling recurs on the `eocystidae` taxon record's `notes` ("Haekel's Eocystida" vs. printed "Haeckel's Eocystida") |
| `rhombifera-order` | "ORDER 2. Rhombifera, Zittel (1879, emend.)" (p. 52) | mismatch by omission — its sibling orders `aporita` and `diploporita-order` both carry this same attribution pattern as a `notes` field ("Zittel (1879, restr.)" / "Zittel (1879, emend.)"); `rhombifera-order` carries no `notes` at all, though the book credits it identically |
| `tiaracrinidae` (`new: true`) | "Famity 4. TIARACRINIDAE." (p. 57), no attribution or "new" language | **cannot verify the `new` flag** — the family is already in print, equally unattributed, in `1899_bather` a year earlier (see that review); flagging it new to this 1900 source looks wrong unless a still-earlier use is ruled out |
| `edrioasteroidea` | "CLASS IV. EDRIOASTEROIDEA, E. Billings (1854,-58; Huxley, 1877; and Bather, 1899)" (p. 205) | node carries no `auth`/`year`/`citedAs` at all — the printed attribution is a compound, three-author credit that the current single-attribution fields cannot hold cleanly; see Cases |
| `thyroida` (synonym) | "(=Thyroida, Chapman, 1860...)" (p. 205) | attribution not captured (Chapman, 1860) |
| `agelacrinoidea` (synonym) | "AGELACRINOIDEA, S. A. Miller, 1877-83; Worthen, 1883" (p. 205) | attribution not captured; note this synonym is itself credited to **two** authors in print |
| `cystasteroidea` (synonym) | "CYSTASTEROIDEA, Steinmann, 1888; F. Bernard, 1893" (p. 205) | attribution not captured; again credited to two authors |
| `thecoidea` (synonym) | "THECOIDEA, Jaekel, 1895" (p. 205) | attribution not captured |

## Cases for the data model

**A three-author class attribution, and two two-author synonym
attributions, on one heading.** p. 205 prints:

> CLASS IV. EDRIOASTEROIDEA, E. Billings (1854,-58; Huxley, 1877; and
> Bather, 1899) (=Thyroida, Chapman, 1860; Agelacrinoidea, S. A. Miller,
> 1877-83; Worthen, 1883; Cystasteroidea, Steinmann, 1888; F. Bernard, 1893;
> Thecoidea, Jaekel, 1895).

The class name itself is credited to three author-year pairs at once
(Billings for the two dates he described the type genus, Huxley for
independently recognising the separation, and Bather citing his own 1899
paper); two of the four listed synonyms are themselves each credited to two
authors. `taxa.yaml`'s `edrioasteroidea` record picks one authority
(`1858b_billings`) and the tree node carries none of this at all. Existing
roadmap items (A3, A12) assume one attribution per line; this is a genuinely
harder case — a single printed line asserting that a name has **several**
independent authors, all cited together as of equal standing. Worth its own
item: perhaps `auth`/`year`/`citedAs` should accept a list of independently-
credited pairs bracketed together, distinct from `in`/`attributedTo` (which
cover joint or misattributed single acts, not "credited to co-discoverers").

**Rank drift for the same name within one source, and between the two
sources.** The formal classification synopsis at the head of Chapter VIII
prints "GRADE A. PELMATOZOA." (p. 1), and the tree follows this
(`pelmatozoa-grade`, `altRankOf: pelmatozoa`). But the prose discussion 33
pages later gives a different reason and a different rank word for the same
group: "their genetic connection is so evident that it should be recognised
by the establishment of a Sub-phylum, to which we shall continue to apply
the name Pelmatozoa" (p. 33) — almost verbatim the wording of `1899_bather`
p. 917 ("it should be recognised by the retention of them in a sub-phylum
Pelmatozoa"), where the *formal* classification heading also printed
"**Sub-Phylum** Pelmatozoa" (p. 919). So across the two sources, the same
taxon is a **Sub-Phylum** in 1899's formal heading and prose, and a
**Grade** in 1900's formal heading, while 1900's own prose still calls it a
Sub-phylum. This is a clean B18 case (same name at different ranks) with the
added wrinkle that one of the two ranks recurs inconsistently within a
single work.

**Tiaracrinidae's `new` flag is likely wrong.** See Coverage table above;
full argument in the `1899_bather` review.

**A likely internal `taxa.yaml` inconsistency, visible from this node.**
`anomalocystidae` (`altSpellingOf: anomalocystitidae`) carries `auth: [Hall],
year: 1859`, but the record it points to, `anomalocystitidae`, carries
`auth: [bassler], year: 1938`. Neither 1899 nor 1900 prints any attribution
for this family at all (both simply describe it), so this review cannot
settle which is right — only that the two linked records disagree with each
other. The same split exists for `dendrocystidae` (Barrande 1887) vs.
`dendrocystitidae` (Bassler 1938); here the 1900 book credits the *genus*
Dendrocystis to Barrande (1887) (p. 47), which at least matches the
alt-spelling record, not the primary one.

**"Assisted by" credits the source record does not capture.** The title
page reads "Part III / THE ECHINODERMA / BY F. A. BATHER, M.A. ... ASSISTED
BY / J. W. GREGORY, D.Sc. ... AND E. S. GOODRICH, M.A. ...". `sources.yaml`
gives `authors: [bather]`, which correctly reflects the "BY" credit, but the
two "assisted by" names have no field to land in. Not necessarily worth a
new field for one instance, but worth a `notes` line if this record is
touched again.

## Source record check

Title page confirms every field: "A TREATISE ON ZOOLOGY EDITED BY E. RAY
LANKESTER... Part III THE ECHINODERMA BY F. A. BATHER, M.A. ... LONDON ADAM
& CHARLES BLACK 1900." `book: treatise-zoo` in `publications.yaml` gives
"A Treatise on Zoology, editors: [lankester], publisher: Adam & Charles
Black, place: London" — matches exactly. `pubDate.year: 1900` matches the
imprint. `authors: [bather]` matches the "BY" line (Gregory and Goodrich are
"assisted by", a different credit — see Cases). `title: Part III — The
Echinoderma` is a fair transcription of "Part III / THE ECHINODERMA".
`identifiers.url` (archive.org) — **cannot verify**, not fetched.

## Comparing 1899 and 1900

| name | 1899 status | 1900 treatment | 1900's attribution for it |
|---|---|---|---|
| Protoblastoidea (Grade) | introduced, unmarked (p. 918 prose; p. 920 formal) | retained, same rank and placement, under Blastoidea | self-cited **"Bather (1899)"** (p. 79) — matches the paper's own printed year |
| Dinocystis (genus, under Edrioasteridae) | introduced, unmarked (p. 923) | retained, same placement | self-cited **"Bather (1898)"** (p. 209) — the conference year, not the printed year |
| *Steganoblastus* / Steganoblastidae | genus only, tentatively ("[?]") placed in family Asteroblastidae under Grade Protoblastoidea (Class Blastoidea) (p. 921) | **reclassified**: given its own new family, Steganoblastidae, under Class Edrioasteroidea (p. 209–210) | the 1900 book explicitly cites the *old, now-rejected* placement back to itself: "the reference of Steganoblastus to the Protoblastoidea (**Bather, 1899**)" (p. 209) |
| Cyathocystidae (family) | introduced, unmarked (p. 923) | retained unchanged, same class, same rank | no year given for the family in either paper; only the genus *Cyathocystis* is dated, to Schmidt (1880 here, p. 208; the paper itself does not cross-cite its own family) |
| Edrioasteridae (family) | introduced, unmarked (p. 923) | retained unchanged | no year given for the family itself in either paper; the *class* Edrioasteroidea's compound credit line (p. 205) is the closest thing to a Bather self-citation touching this family, and it says "Bather, **1899**" |
| Tiaracrinidae, Comarocystidae, Macrocystellidae, Malocystidae, Glyptocystidae, Protocrinidae, Mesocystidae (families) | all introduced, unmarked, in 1899's Cystidea classification | all retained unchanged, same order, same rank, in 1900 | none re-attributed to Bather by year in either paper |
| Pelmatozoa (Sub-Phylum / Grade) | formal heading: **Sub-Phylum** (p. 919); prose: "sub-phylum Pelmatozoa" (p. 917) | formal heading: **Grade A** (p. 1); prose: "the establishment of a Sub-phylum... Pelmatozoa" (p. 33) | rank word changes between the two papers' formal headings; 1900's own prose does not follow its own formal heading — see Cases |
| Eleutherozoa | informal only, inside a parenthesis in a diagram (p. 917); no rank word given | formalised: "**GRADE B.** ELEUTHEROZOA." (p. 1) | promoted from an unranked, parenthetical grouping to a formal Grade between the two sources |
| Edrioasteroidea (Class) | its separation as a class is credited only vaguely, in running prose, to "Billings, Huxley, Chapman, Worthen, Steinmann, Jaekel, and others" (p. 917) — **Bather is not among the names listed** | formal heading now names three specific credited author-years, and Bather has added **himself**: "E. Billings (1854,-58; Huxley, 1877; and **Bather, 1899**)" (p. 205) | Bather moves from an anonymous "and others" in 1899 to explicitly crediting himself, by name and year, for the same act in 1900 |

Overall: every name that is new in 1899 is simply carried forward unchanged
into 1900's classification with one exception (*Steganoblastus*, promoted
out of Blastoidea into its own new Edrioasteroidea family) and one rank
change at the top of the hierarchy (Pelmatozoa, Sub-Phylum → Grade in the
formal heading, though not in prose). Where Bather cites his own 1899 paper
by year in 1900, he uses "1899" for the paper's own grade-level and generic-
placement acts, and "1898" for a genus described within the same paper —
direct primary-source support for the year problem discussed at length in
the `1899_bather` review, which this source record's own bibliography entry
(p. 216, item 12: "1899... Rep. Brit. Assoc. for 1898, pp. 916-923") also
bears on.

## Uncertainties

- `metazoa-grade`'s printed rank word — OCR garble ("MOEPAIGA") between
  "GRADE I. PROTOZOA." and "BRANCH A./B." on the tabular statement page;
  **cannot verify** it reads "GRADE II. METAZOA." though the position fits.
- Whether "Series Codonoblastida" is printed as a heading in the Blastoidea
  section (relevant to `1899_bather`, not to this tree, which does not cover
  Blastoidea's internal orders/families at all) — not re-checked here.
- Whether any source earlier than 1899 used "Tiaracrinidae" — not checked
  (only these two papers were examined).
- The `identifiers.url` — not fetched, **cannot verify**.
- Coverage of Chapter XI (Crinoidea, pp. 94–204) and the bulk of the
  Cystidea genus-level detail (pp. 44–77) beyond the family/order/subfamily
  headings checked here — not read in full; the tree captures none of it,
  consistent with G9, but this review cannot rule out further node-level
  detail worth capturing beyond what was sampled.
