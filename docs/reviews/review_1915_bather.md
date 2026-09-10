# Review: 1915_bather

`1915_bather` in `sources.yaml` has no tree file. Per the assignment, no node-by-node
check (§2 of the standard review) is attempted. This is a summary of what the volume
prints, for the owner to use in deciding what (if anything) to enter, plus the source
record check (§4), which does apply since a record already exists.

The volume is Bather, *Studies in Edrioasteroidea*, self-published by the author,
October 1915 — "Reprinted, with Additions, from the Geological Magazine for 1898,
1899, 1900, 1908, 1914, and 1915" (title page; OCR renders "1898" as "1808"), each
study kept in its original Geological Magazine pagination.

## (a) The ten items, as printed on their title lines

The volume's own Contents (pp. v-vii) lists **nine** Roman-numbered "Studies," plus
two short unnumbered pieces bound in immediately after Study I. That is eleven printed
items in total, or nine if the two short pieces are not counted as "Studies" in their
own right — the assignment's count of ten does not fall out cleanly from what is
printed; both readings are given below rather than forcing a count.

| # | Title, as printed | Original publication | Date |
|---|---|---|---|
| I | "Dinocystis Barroisi, n.g. et sp., Psammites du Condroz" | Geol. Mag., n.s., Dec. IV, Vol. V, pp. 543-548, Pl. XXI | Dec., 1898 |
| — | "Note on Dinocystis Barroisi" (a letter by G. Dewalque) | Geol. Mag., n.s., Dec. IV, Vol. VI, p. 94 | Feb., 1899 |
| — | "The Horizon of Dinocystis Barroisi" (a letter in reply) | Geol. Mag., n.s., Dec. IV, Vol. VI, pp. 134-136 | March, 1899 |
| II | "Edrioaster Buchianus Forbes sp." | Geol. Mag., n.s., Dec. IV, Vol. VII, pp. 193-204, pls. VIII-X | May, 1900 |
| III | "Lebetodiscus, n.g. for Agelacrinites Dicksoni Billings" | Geol. Mag., n.s., Dec. V, Vol. V, pp. 543-550, pl. XXV | Dec., 1908 |
| IV | "The Edrioasters of the Trenton Limestone" | Geol. Mag., n.s., Dec. VI, Vol. I, pp. 115-125 and 162-171, pls. X-XIV | March and April, 1914 |
| V | "Steganoblastus" | Geol. Mag., n.s., Dec. VI, Vol. I, pp. 193-203, pl. XV | May, 1914 |
| VI | "Pyrgocystis, n.g." | Geol. Mag., n.s., Dec. VI, Vol. II, pp. 5-12 (Pls. II, III) and 49-60 | Jan. and Feb., 1915 |
| VII | "Morphology and Bionomics of the Edrioasteridae" | Geol. Mag., n.s., Dec. VI, Vol. II, pp. 211-215 and 259-266 | May and June, 1915 |
| VIII | "A Comparison with the Structure of Asterozoa" | Geol. Mag., n.s., Dec. VI, Vol. II, pp. 316-322 | July, 1915 |
| IX | "The Genetic Relations to other Echinoderms" | Geol. Mag., n.s., Dec. VI, Vol. II, pp. 393-403 | Sept., 1915 |

Two page ranges in this table were cross-checked between the front-matter Contents and
the in-text citation bracket printed at the head of the actual study, and disagree:
Study VII's second part is "250-266" in the Contents but "259-266" in the study's own
heading; Study IX is "399-408" in the Contents but "393-403" in its own heading. Given
this OCR's general unreliability on digits, both readings are given and neither is
resolved here — **cannot verify** which is the correct printed page range without a
cleaner scan.

This is squarely an A11 "one work, several printings" situation, except the axis is
not printing-vs-printing but original-serial-vs-reprint: nine (or eleven) originally
separate Geological Magazine articles, most already individually paginated and dated,
collected into one 1915 volume that keeps their original pagination and adds a preface
and index. Per the "Printings in `sources.yaml`" discussion (`source-observations.md`),
each of the nine numbered Studies (and arguably the two letters) is a candidate for its
own source record keyed to its true year of first publication (1898, 1899 ×2, 1900,
1908, 1914 ×2, 1915 ×3), with the 1915 volume itself recorded separately (as
`printingOf` or similar) if the "Additions" described below are ever entered.

## (b) Existing source records

`data/sources.yaml` has exactly one record keyed to Bather 1915: `1915_bather`. No
record exists for any of the other years/studies (`1899_bather` and `1900_bather` do
exist but are unrelated Bather works — "A Phylogenetic Classification of the
Pelmatozoa" and the Treatise on Zoology "Part III — The Echinoderma" chapter,
respectively — not part of this collection). See §4 below: `1915_bather` itself does
not cleanly match any one printed item.

## (c) Classification and new names, by study

- **I. *Dinocystis Barroisi*.** New genus and species, from disarticulated plate
  material ("Agelacrinus, n.sp.") purchased from a dealer and traced to the Psammites
  du Condroz (Lower Devonian, Belgium). The two follow-on letters (Dewalque; Bather's
  reply) dispute the horizon, not the taxonomy.
- **II. *Edrioaster Buchianus* Forbes sp.** No new taxon; a full redescription of the
  type species of *Edrioaster* (originally Forbes's *Agelacrinites Buchianus*, 1848,
  the species Billings recombined into his new genus *Edrioaster* in 1858 — see the
  `1858a_billings` review potential/`1858b_billings` review for the genus's own
  protologue), resolving a dispute between Salter's and Etheridge's readings of the
  abactinal membrane.
- **III. *Lebetodiscus*, n.g. for *Agelacrinites Dicksoni* Billings.** New genus
  erected to receive Billings's species — a direct recombination of the species
  reviewed in `1858b_billings` (*Agelacrinites Dicksoni* Billings, 1858) into
  *Lebetodiscus Dicksoni*. `taxa.yaml` already has a `lebetodiscus` record with
  `auth: [bather], year: 1908`, but no `1908_bather` source record exists to back it —
  an existing citation with nothing to resolve to.
- **IV. The Edrioasters of the Trenton Limestone.** A broader revision of the Ottawa
  Trenton Limestone fauna (the same beds and species complex as `1857_billings` and
  `1858b_billings`); at least one new species is named in the running text, "For this
  new species the name *E. laevis* is proposed."
- **V. *Steganoblastus*.** New genus, built on a species Whiteaves originally described
  in 1897 as a new genus and species of Cystidean; Bather's study reclassifies it as an
  edrioasteroid.
- **VI. *Pyrgocystis*, n.g.** New genus with three new species: *P. sardesoni*
  ("genotype," i.e. type species, Lower Ordovician, Minnesota), *P. grayae* (Upper
  Ordovician, Girvan), *P. ansticei* (Middle Silurian, Shropshire). Also refers here
  material from the Middle Silurian of Gotland that C. W. S. Aurivillius had assigned
  in 1892 to seven species of the cirripede genus *Scalpellum*.
- **VII. Morphology and Bionomics of the Edrioasteridae.** Synthetic/comparative; no
  new taxa noted.
- **VIII. A Comparison with the Structure of Asterozoa.** Comparative anatomy against
  Spencer's contemporary Asterozoa monograph; no new taxa.
- **IX. The Genetic Relations to other Echinoderms.** Phylogenetic/classificatory
  synthesis; the volume's own index lists "Edrioasteroidea, value as Class" as a topic
  here, suggesting a formal rank discussion, but this review did not locate or verify
  the exact passage in the running text — **cannot verify** its wording.

## (d) Added material in the 1915 printing

The Preface (pp. v-vii, dated "Kensington, 24 Sept. 1915") states the studies are
"reprinted without textual change and with the original pagination of the Geological
Magazine" but "supplemented by this Preface and by an Index," plus:

- **One stated corrigendum**: "The numbers of the rays in the Text-figure on p. 260 of
  the 1915 volume were inserted in the wrong order (contra-solar instead of solar), and
  that has been set right in this edition" — a correction to Study VII's own figure,
  made in the reprint and separately announced in *Geol. Mag.* for October 1915 (p.
  478, per the Preface; not itself in this text).
- **New horizon information for two of the studies**, given only in the Preface, not
  in the original papers it discusses: for Study I (*Edrioaster buchianus*), a newly
  cited 1885 paper by T. Ruddy placing the species and *Protaster salteri* in specific
  zones; for Study V (*Steganoblastus*), a correspondent's (Walter R. Billings) report
  of the exact bed and associated fauna at the type locality, with an inferred
  correlation to "Dr. P. E. Raymond's Horizon 5."
- **A field-visit note for Study VI**: the Preface reports the author's subsequent
  visit to Coalbrookdale (the *Pyrgocystis ansticei* locality) with a companion, adding
  detail on the exposure without finding new specimens.
- No new plates beyond what each original printing already carried; the Preface notes
  that plates for the 1914 studies were themselves delayed by "official duties," not
  that the 1915 reprint adds plates.

## 4. Source record check

The one existing record does not cleanly match any printed item:

```
1915_bather:
  title: Studies in Edrioasteroidea IV. Pyrgocystis n. g.
  journal: geomag
  number: 5–12
  pages: [49, 90]
  pubDate: {year: 1915, month: 12, day: 6}
```

Comparing against the printed heading of the study this is evidently meant to be
(Study VI, not IV): "VI. PYRGOCYSTIS N.G. [Part I.] [Geol. Mag., N.S., Dec. VI, Vol.
II, pp. 5-12, Pls. II, III; Jan., 1915.]" and Part II's own bracket, "[Geol. Mag., N.S.,
Dec. VI, Vol. II, pp. 49-60; Feb., 1915.]":

- **Roman numeral wrong**: the record's title says "IV," but *Pyrgocystis* is Study
  **VI** on the volume's own Contents page and in both parts' own headings. Study IV is
  a different paper ("The Edrioasters of the Trenton Limestone").
- **Pages wrong**: the record gives `[49, 90]`; the two printed parts together cover
  pp. 5-12 and 49-60 — the record's start page (49) matches only Part II's start, and
  its end page (90) matches neither part.
- **`number: 5–12`** looks like a fragment of Part I's page range, misfiled into the
  `number` field rather than `pages`.
- **Date wrong**: `pubDate: 1915-12-06` does not match either printed date (Jan. and
  Feb., 1915); its origin could not be determined from this text — **cannot verify**
  where "1915-12-06" comes from.

In short: this record appears to be a garbled attempt at Study VI, not Study IV, with
page and date fields that do not match either printed part. It should probably be
retitled/repaged/split (Part I and Part II each have their own citation bracket and
could be two records, per the volume's own practice of double-dating two-part studies)
rather than edited in place, since it is not clear what its numbers were originally
meant to represent.

## 5. Uncertainties

- The "ten" count in the assignment does not match what the volume's own Contents
  prints (nine numbered Studies, or eleven items counting the two 1899 letters); see
  §(a).
- Two page-range disagreements between the front-matter Contents and the in-study
  citation brackets (Study VII's second part, Study IX) are noted but not resolved.
- Study IX's "value as Class" discussion (per the index) was not located and verified
  in the running text.
- This review reflects only the pages read for this task (Contents, Preface, and the
  heading/opening of each Study); it is not a full read of all ~250 pages, so further
  new names or classification statements may exist within the Studies that this review
  did not surface.
