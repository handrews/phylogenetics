# Review: Webby 1968, "Astrocystites distans sp. nov., an edrioblastoid from the Ordovician of eastern Australia"

Palaeontology 11(4): 513–525, pls. 99–100.

**Page mapping.** Text starts at PDF index 264 (printed p. 513, confirmed by the
footer "[Palaeontology, Vol. 11, Part 4, 1968, pp. 513-25, pis. 99, 100.]") and
ends at index 280 (printed p. 525; index 281 begins Robinson's *Chubbina* paper
at printed p. 526). Offset is not constant because two plates (99, 100) are
tipped in as unnumbered leaves: printed page = index + 249 for indices 264–269
(pp. 513–518), index + 247 for indices 272–273 (pp. 519–520, after Plate 99's
two leaves), and index + 245 for indices 276–280 (pp. 521–525, after Plate
100's two leaves). Indices 270–271 and 274–275 are the plate leaves
themselves (unnumbered recto/verso).

## 1. Coverage by kind

| kind | coverage | note |
|---|---|---|
| classification skeleton | all | Subphylum–Class–Family–Genus header (p. 513) reproduced exactly, rank for rank |
| new taxa | all | the one nomenclatural act (*A. distans* sp. nov.) is captured with `new: true` |
| type species | all | *A. ottawaensis* Whiteaves flagged `type: true`, matching "Type species. *Astrocystites ottawaensis* Whiteaves" (p. 513) |
| synonymy | partly | genus-level synonym (*Steganoblastus*) captured; the family-level synonym *Astrocystitidae* Bassler 1935, argued over at length on p. 514, is not represented anywhere in the tree |
| material | partly | holotype and most paratypes captured, but three paratype catalogue numbers printed in the Material paragraph (USGD 2308, 2313, 2314) are missing from the tree; the "miscellaneous pelmatozoan plates" (six more catalogue numbers, pp. 522–524) are not represented at all |
| occurrences | none | no locality/horizon data anywhere in the tree, though the paper gives grid references, formation names and, for USGD 3303 and 3304, horizons that differ from the rest of the type series |
| illustrations | none | no `illustrations` field anywhere, despite two plates and five text-figures keyed to specific specimens |
| diagnoses | none | the printed diagnosis of *A. distans* (p. 515) is not on the `distans_webby_1968` node |
| phylogeny | na | no cladogram/diagram is printed; the paper's "Discussion of edrioblastoid relationships" (pp. 520–523) is prose argument, not a `phylogenies`-shaped structure |

If the audit block's migrated flags ("specimens.basic=true specimens.all=true")
are read as a claim that all specimens were captured, that claim does not hold
against the printed Material paragraph — see §2 and §3.

## 2. Correctness of every node

7 nodes in the tree. 4 match the printed text cleanly (summarised below); 3
rows need detail.

Matches (no further detail needed): `pelmatozoa` (Subphylum, Leuckart 1848,
p. 513); `edrioblastoidea` (Class, Fay 1962, p. 513); `steganoblastidae`
(Family, Bather 1900, p. 513); `ottawaensis_whiteaves_1897` (`type: true`,
matching "Type species. *Astrocystites ottawaensis* Whiteaves", p. 513, with
no `auth`/`year` printed on that line — correctly left bare per A12).

| node | printed (page) | verdict |
|---|---|---|
| `astrocystites` synonym `steganoblastus` | "(= steganoblastus Whiteaves 1898)" (p. 513); text: "The new generic name was introduced by Whiteaves (1898)" (p. 514); reference list: "whiteaves, j. f. … 1898. Postcript. Ibid. 395" (p. 524) | mismatch — `taxa.yaml`'s `steganoblastus` record carries `year: 1899`, not 1898. Every occurrence of the year in this paper (classification header, prose, and its own reference list) reads 1898. No `1898_whiteaves`/`1899_whiteaves` source record exists to check against independently. |
| `distans_webby_1968.specimens.paratypes` | Material, p. 515 (quoted in full in §3) | mismatch — three catalogue numbers the paper calls paratypes are absent from the tree's list: **USGD 2308, 2313, 2314** (the "plate fragments" group). The tree's nine numbers (2303–2306, 2309–2312, 3303) do match everything else in the Material paragraph. |
| `astrocystites-sp_webby_1968.specimens.unknowntypes` | "The edrioblastoid specimen (USGD 3304) … probably represents a species of *Astrocystites* comparable with *A. distans*, but until more material is found closer comparisons cannot be made." (p. 520) | number correct (USGD 3304, sole specimen); role bucket and hedge undercaptured — see §3 |

## 3. Cases for the data model

**The genus's nomenclatural history has no home but `notes`, and none is
present.** The "Nomenclature and previous work" section (p. 514) is a single
paragraph of exactly the kind the roadmap's `notes` escape hatch exists for,
and none of it is on the tree. Quoted in full:

> "Whiteaves (1897) first described Astrocystites ottawa-ensis from the Trenton
> Limestone of Ottawa. Jn the same year Bather raised objections to
> Whiteaves's generic name on the grounds of possible confusion with
> Asterocystis Haeckel, and suggested that Whiteaves substitute the name
> Steganoblastus. The new generic name was introduced by Whiteaves (1898), and
> the family name Steganoblastidae of the Class Edrioasteroidea added by
> Bather (1900). Whiteaves's original generic name, Astro-cystites, was
> restored by Bassler (1935) on grounds of priority, and he introduced a new
> family name, Astrocystitidae, to replace Steganoblastidae. However, since
> Steganoblastidae, which is based on a junior objective synonym, has priority
> and has been a more widely used name, it would seem desirable that it be
> retained. This view accords with Art. 40 of the International Code of
> Zoological Nomenclature." (p. 514; "Jn" is an OCR misread of "In")

Two placement statements follow immediately:

> "Astrocystites was interpreted as an edrioasteroid by Bather (1914b), and as
> a blastoid by Hudson (1925). Bassler (1935, 1936) also classified the genus
> in the Edrioasteroidea, but observed that, since only a few specimens are
> known and pending further discoveries it might well be assigned to the
> Protoblastoidea. Fay (1962) contended that it did not belong either to the
> edrioasteroids or the blastoids, and raised a new class, the Edrioblastoidea,
> to accommodate it." (p. 514; OCR renders "1914b" as "19146" throughout — the
> reference list confirms "19146. Studies in Edrioasteroidea, Part V.
> Steganoblastus", i.e. 1914b)

This is a compound case, not fully covered by any single roadmap item:

- The *Astrocystitidae* Bassler 1935 / *Steganoblastidae* Bather 1900
  family-group synonymy is exactly the same shape as the genus-level
  `astrocystites`/`steganoblastus` synonymy already modelled on this tree
  (`taxa.yaml` already carries a standalone `astrocystitidae` record, used
  this way in `data/trees/1935_bassler.yaml`), so the fix is mechanical: add
  `astrocystitidae` to `steganoblastidae`'s `synonyms`.
- Webby's own argument for retaining the junior family name under Art. 40 —
  a reversal-of-precedence usage argument, not a nomenclatural act by
  Webby — has no field. It is the kind of thing that belongs in `notes` on
  the `steganoblastidae` node, quoted, per the ground rule that "every rule
  … has been broken … `notes` is the last-resort escape hatch."
- The chain of prior placements (edrioasteroid — Bather 1914b; blastoid —
  Hudson 1925; Edrioasteroidea-with-Protoblastoidea-reservation — Bassler
  1935/1936; new class Edrioblastoidea — Fay 1962) is a case like G7's
  "an earlier classification reproduced": each belongs to those sources' own
  trees, and here at most a `notes` naming that Webby reproduces/summarises
  them, with page.
- Webby's own reservations about Fay's class ("The writer has reservations
  about the need to separate Astrocystites from the Edrioasteroidea and to
  erect a new class, the Edrioblastoidea (Fay 1962)", p. 515) sit alongside a
  classification that nonetheless *follows* Fay's class ("Although Fay's
  classification has been followed …", p. 515) — the tree correctly follows
  the classification used, but the printed disagreement-with-the-classification-
  one-adopts is otherwise invisible; it belongs in `notes` on `edrioblastoidea`
  or `astrocystites`.

**Paratype letters sharing one catalogue number.** Plate 99 fig. 6: "Paratypes
B-D, USGD 2309 … two longitudinal sections (paratype B, top left; paratype C,
centre) and basal plate (paratype D, bottom right)" (p. 518). Three
letter-designated paratypes are cut faces of a single catalogued specimen.
The current `specimens.paratypes` list (a flat array of catalogue numbers)
cannot distinguish "one specimen, three named parts" from "three specimens";
D1's `parts: [part, counterpart]` shape (built for a holotype split across
two numbers) is the nearest existing mechanism but doesn't carry the
generalisation to three named, unnumbered-individually parts under one
paratype. Worth a note if/when this tree is migrated to the `material` list
shape.

**A hedge placement with no marker.** The `astrocystites-sp_webby_1968` node
is placed as a plain child of `astrocystites`, but the paper's own words are
hedged ("probably represents a species of *Astrocystites* … until more
material is found closer comparisons cannot be made", p. 520) and the
placement is never given a formal taxonomic heading — it appears inside the
Remarks on *A. distans*, not under its own "*Astrocystites* sp." heading. This
is the shape of both C ("validity of the taxon" axis: `provisional`) and B20
("placements the editor inferred"): the placement into the tree under
`astrocystites` is a reasonable editorial reading of prose, not a printed
subheading, and nothing currently marks it as either provisional or
editorially inferred.

**Role bucket for non-type material.** `specimens.unknowntypes: [USGD 3304]`
is the D2 "(none)" case exactly: the specimen is never called any kind of
type, it is ordinary referred material in open nomenclature. D2 names
`unknowntypes` as one of the legacy buckets the "(none)" role replaces —
this node is a clean example for that migration.

**Unplaced material entirely outside the tree.** "Miscellaneous pelmatozoan
plates" (pp. 522–524): six more catalogue numbers (USGD 2307, 2315, 2316,
3300, 3301, 3302) explicitly said not to belong to *A. distans* ("In addition
to the thecal plates and fragments which can be positively recognized as
parts of A. distans, there are numerous stem ossicles and a few plates … which
cannot be so confidently determined", p. 522) and never assigned even to
*Astrocystites* sp. — genuinely indeterminate pelmatozoan material with no
taxonomic node to sit under. G9 states plainly that "disarticulated plate
material belongs in scope: the earliest echinoderm records are plates, older
than any articulated fossil," so this is squarely in-scope material with no
current placeholder (an `-indeterminate-` bin under `pelmatozoa` would be the
natural shape, per C4).

**A quote on a taxon record instead of a tree node.** The hedge quote for
`astrocystites-sp_webby_1968` ("[The specimen] probably represents a species
of Astrocystites comparable with A. distans, but until more material is found
closer comparisons cannot be made.") is stored as `notes` on the `taxa.yaml`
identity record rather than on the tree node in `data/trees/1968_webby.yaml`.
Since this placeholder exists only because of this one source, the practical
effect is the same, but it sits on the wrong side of the identity/claim line
the ground rules draw ("notes" as documented is a tree-node field; the
per-source claim belongs with the source's own tree).

**Duplicate catalogue number on two different specimens (probable OCR/print
issue).** Plate 100 explanation lists both fig. 11 ("USGD 2315 … large round
columnal with stellate axial canal") and fig. 16 ("USGD 2315 … small, round
articulated columnals") under the same number, and the running text likewise
describes USGD 2315 twice with two different sizes and forms ("The largest
columnal (USGD 2315) is round, 5 mm. in diameter …", p. 523; "A thinner
articulated specimen (USGD 2315) has round columnals, 1-2 mm. in diameter …",
p. 523). Cannot verify which is a scan/OCR error and which, if either, is a
lot number covering more than one piece; not part of this tree in any case,
noted for completeness given it touches the same catalogue-number series.

## 4. Source record check

Title, journal, volume, number, pages, year and sole author (`webby`) in
`data/sources.yaml`'s `1968_webby` block all match the printed article page
and its citation footer ("Palaeontology, Vol. 11, Part 4, 1968, pp. 513-25,
pis. 99, 100."). One discrepancy worth flagging: the Contents page (PDF index
445) prints the title as "Astrocystites distans, sp. nov., an edrioblastoid
from the Ordovician of **Eastern** Australia" (comma after *distans*, capital
E), while the article's own running head/title block and the citation footer
have no comma after *distans* and (so far as an all-caps line can show)
lowercase "eastern" — a front-matter/running-head typesetting variant, not a
content difference; `sources.yaml`'s title matches the article page, not the
Contents page.

## 5. Uncertainties

- Plate 99's figure captions run 1, 2, 3, 4, 5, 6, **7**, [gap], 9, 10 — fig.
  8's caption is missing from the OCR (text jumps from "7, Paratype, USGD
  2304 …" straight to "9, Paratype, USGD 2313 …"). Cannot verify which
  specimen fig. 8 depicted, or whether it accounts for USGD 2306, 2308 or
  2312 (each cited only in the Material paragraph, with no independent plate
  citation found).
- The 1898 vs. 1899 year for Whiteaves's *Steganoblastus* (§2) cannot be
  independently resolved from this dataset: no `18xx_whiteaves` source record
  exists to check the taxa.yaml `steganoblastus` record against, and the OCR
  of the reference-list entry ("1898. Postcript. Ibid. 395") is otherwise
  clean, not a digit likely to be misread.
- "Bather (19146)" appears repeatedly for what the reference list confirms is
  1914b (OCR misreads the italic/superscript "b" as "6"); read with
  confidence from the reference list, not flagged per-instance above.
- USGD 2315 cited for two different specimens (§3, last item) — cannot verify
  without the plates themselves whether this is a printing error or a shared
  lot number.
