# Review: Bather 1914 — "Studies in Edrioasteroidea. V. Steganoblastus"

No source record and no tree exist for this paper (`1914_bather` is not in
`sources.yaml`; `data/trees/` has no `1914_bather.yaml`). Per the brief,
this review summarises what the paper prints so the owner can decide
whether to enter it.

Text: `1914_bather.txt` (OCR of *Geological Magazine*, decade VI, vol. I).

## Page mapping

PDF index 258 opens the study and carries no visible top-of-page folio
(the article's own masthead occupies that line), but index 259's top
carries "194", so index 258 = printed **p. 193** and the formula **printed
page = index − 65** holds for the whole study, confirmed again at index 261
("196") and index 267 ("202"). This matches the volume's own back-of-book
Index ("Steganoblastus ottawaensis, 193.") and List of Text-figures
("Steganoblastus ottawaensis … 195, 198, 200, 201"), both consulted
independently (index 226/242 area). The study runs **pp. 193–203**; p. 203
is shared with the next article (D. M. S. Watson's), whose running head
already appears at the top of that page.

## Front matter, as printed

Issue masthead (index 258): "THE GEOLOGICAL MAGAZINE. NEW SERIES. DECADE
VI. VOL. I. No. V.—MAY, 1914." Contents listing (index 254, the issue's
front cover): "I. ORIGINAL ARTICLES. Studies in Edrioasteroidea. V.
Steganoblastus. By Dr. F. A. Bather, M.A., F.R.S., British Museum (N.H.).
(Plate XV and 6 Text-figures.)" Article's own heading (index 258):
"I.—STUDIES IN EDRIOASTEROIDEA. V. STEGANOBLASTUS.¹ By F. A. Bather, M.A.,
D.Sc., F.R.S. Published by permission of the Trustees of the British
Museum. (PLATE XV.)" — footnote ¹: "Study IV appeared in the GEOL. MAG. for
March and April, 1914." A separate photographic plate captioned simply
"STEGANOBLASTUS." (index 257, credited "Herring, photo. London Stereoscopic
Co.") is bound as the volume's frontispiece to this Number; it is Plate XV,
explained in full at the article's end. This matches the task's
expectation (pp. 193–203, Plate XV, May 1914) exactly.

## What it prints for *Steganoblastus* and Steganoblastidae

**This paper does not erect either name.** It opens with a section headed
"Previous History" (pp. 193–194) that narrates, and cites by page, three
prior acts, none of them this paper's own:

1. Whiteaves 1897 (protologue of *Astrocystites ottawaensis*, "*Canad. Rec.
   Sci.*, vol. vii, No. 5, pp. 287–92") — including Bather's own account of
   objecting to the name by letter (quoted and discussed in the
   `review_1897_whiteaves.md` companion review) and Whiteaves' "Postscript"
   substituting *Steganoblastus* ("tom. cit., p. 395, January 7, 1898").
2. **The genus's placement and the family's erection, both already done in
   1900:** "The first results of my examination were summarized in
   Lankester's *Treatise on Zoology*, vol. iii, pp. 209–10, text-fig. vii
   (1900), **where I founded for the reception of this genus the Family
   Steganoblastidæ of the Class Edrioasteroidea**" (p. 194). Later in the
   same paper, restating the same fact as a conclusion: "It has therefore
   been necessary to establish for it the Family Steganoblastidæ (*Treatise*,
   **1900**, p. 209)" (p. 203).
3. Two intervening reprints/citations of the 1900 account: Whiteaves
   himself reprinted "his original description, followed by a complete
   extract from the *Treatise*," in *Palaeozoic Fossils*, vol. iii (pp.
   316–21), Geological Survey of Canada, September 1906; and Delage &
   Hérouard reproduced Bather's *Treatise* drawings "in reduced facsimile"
   in *Traité de Zoologie concrète*, tome iii, "Les Échinodermes" (pp. 415,
   416, Paris, March 30, 1904). Also: "The Family Steganoblastidæ is
   accepted by Dr. F. Springer in the second edition of Eastman's Zittel
   ([printed, OCR] 1913 [read as] 1918)" — see Uncertainties.

So both the taxa.yaml credit (`steganoblastidae` → `authority: {source:
1900_bather}`) and the roadmap/Webby-1968 dating this task asked to check
are **confirmed by the source's own words**: Bather 1914 explicitly and
twice attributes the family's founding to his own 1900 Treatise chapter,
p. 209, and treats it here purely as already established. This 1914 study
is a detailed re-description and re-classification of the type material,
not a nomenclatural act on the family or the genus name.

**The genus name itself is not re-erected or emended here either** — no
"Genus *Steganoblastus*" heading, no diagnosis section, no synonymy list,
and the word "diagnosis" and the phrase "type species" never occur in the
study (checked exhaustively). Its structure is instead: "Previous History"
→ "Material" → "General Description" → "Description of the Specimens" →
"Relations of Steganoblastus" → "Explanation of Plate XV" — a narrative
re-examination, not a systematic-paleontology entry.

**One act does occur here: a type designation from among the syntypes.**
"MATERIAL." (p. 194): "The specimens are the three syntypes of Whiteaves,
and may be distinguished as A, B, and C… A is an almost perfect theca with
two columnals. It is the original of Whiteaves' figs. 1 and 2, and of Pl.
XV, Figs. 1, 3, 4, 6, 7, in the present paper. **It is hereby selected as
the holotype.**" B and C are described immediately after with no type role
word attached to either. Bather uses "holotype" for what is, by his own
preceding sentence, a selection of one of several syntypes as the
name-bearing specimen — the same kind of imprecise-but-clear era usage the
roadmap already tracks under `roleAsPrinted` (D1/D2/D9); in modern terms
this is a lectotype designation.

## Material

Three specimens, all from "the Trenton Limestone at Division Street,
Ottawa" (p. 194):

| label | description (as printed) | collector | repository (as printed) | role (as printed) |
|---|---|---|---|---|
| A | "an almost perfect theca with two columnals" | John Stewart, 1886 | "Victoria Memorial Museum, Ottawa" | "hereby selected as the holotype" |
| B | "a theca crushed in the left anterior interradius and adjoining radii, with portions of three columnals" | John Stewart, 1886 | "Victoria Memorial Museum, Ottawa" | none given |
| C | "a much broken and crushed theca with no columnals" | Walter R. Billings | remains in Billings' "possession" (private) | none given |

Two repository names for the same institutional holding appear within two
pages of each other: "Previous History" (p. 193) says Whiteaves "kindly
lent me the two specimens belonging to the **Geological Survey of
Canada**," while "Material" (p. 194) places the same two specimens in the
**Victoria Memorial Museum, Ottawa** — the same collection under an
institutional rename, not two different holdings (cf. roadmap F2,
repository `formerly` aliases; the Preface 2023 example is "NHMUK (formerly
BMNH)"). No catalogue numbers are given for any of the three specimens in
this paper, matching Whiteaves 1897.

Whiteaves' own words are quoted back: "'All three of these specimens, when
found, were,' says Whiteaves, 'almost completely covered with a very
tenacious shaly limestone.' This had been for the most part skilfully
removed before the specimens were sent to me, but the pores and the
outlines of the plates were still obscured" (p. 194) — an example of one
source's material note being carried into a later source's own account
(cf. roadmap H, "a claim about another work's error"/reused description,
though here it is agreement, not correction).

## Locality and horizon

"All were obtained from the Trenton Limestone at Division Street, Ottawa.
**The precise horizon has nowhere been stated**" (p. 194) — Bather
explicitly flags the same gap this review's companion (`review_1897_
whiteaves.md`) found in the 1897 text; no more specific unit or bed is
supplied here either.

## Classification, as printed

No "Order," "Class," or "Family" heading is set as a formal taxonomic
scaffold anywhere in this study (searched exhaustively) — the placement is
stated entirely in the prose "Relations of Steganoblastus" section (pp.
202–203), as three sequential negative/positive arguments from the newly
described morphology:

> "First, the absence of brachioles, inferred from the lack of
> brachiole-facets and the presence of large cover-plates, proves that
> *Steganoblastus* is not a blastoid, not even one of the Protoblastoidea,
> as was at first supposed. It also proves, if proof be needed, that it is
> not one of the Cystidea Diploporita.
>
> Secondly, the structure of the subvective groove, with its floor-plates
> and cover-plates, and its pores between the floor-plates, is paralleled
> by Edrioasteroidea alone among Pelmatozoa, and in that Class most closely
> by *Edrioaster*, though there are minor differences.
>
> Thirdly, the presence of a stem, and the enhanced pentamerism of the
> thecal structures thereby induced, render it impossible to place
> *Steganoblastus* in the Family Edrioasteridæ. It has therefore been
> necessary to establish for it the Family Steganoblastidæ (*Treatise*,
> 1900, p. 209)." (pp. 202–203)

So the chain as this paper states it: Class Edrioasteroidea → Family
Steganoblastidæ (erected 1900, not here) → *Steganoblastus*, with two
explicit rejections along the way — not Blastoidea/Protoblastoidea (the
placement "at first supposed," i.e. by Bather's own 1899 paper, per the
companion `review_1900_bather.md`'s comparison table), and not Cystidea
Diploporita (Whiteaves' 1897 tentative placement — see
`review_1897_whiteaves.md` §f). Structurally closest, but explicitly
distinct from, genus *Edrioaster* within Family Edrioasteridæ. No order
rank is used at all for this lineage in this paper, consistent with the
1900 Treatise's own Class→Family scaffolding for Edrioasteroidea (already
noted in `review_1900_bather.md`).

## Illustrations

Plate XV, seven photographic figures (all by H. G. Herring, "except Fig. 3,
… enlarged 3 diameters"; explained p. 203): Figs. 1, 3, 4, 6, 7 of specimen
A; Figs. 2, 5 of specimen B. Six text-figures (pencil drawings by G. T.
Gwilliam, pp. 194–201): Figs. 1–2 restored views of the theca (based mainly
on specimen A); Figs. 3–6 structural detail drawings tied to specific
plate-figures in the description ("cf. Text-fig. 3," "Text-fig. 4," "Pl.
XV, Figs. 2, 5; Text-fig. 5," "Pl. XV, Fig. 7; Text-fig. 6"). No specimen C
figure is mentioned anywhere.

## "Steganoblast" outside the study

Grepped the whole volume text for "Steganoblast": all instances are inside
the study itself (pp. 193–203) except three front/back-matter listings, all
of which point back to this same study and add no new information:

- **List of Plates** (front matter, before the study; unpaginated in this
  scan): "Steganoblastus" — the plate title only.
- **List of Text-figures** (same front-matter block): "Steganoblastus
  ottawaensis . . . 195, 198, 200, 201" — four of the study's own
  text-figure page citations (of the six total; the other two fall on pp.
  194 and 201/202 by the figure's own placement in the running text).
- **Volume Index** (back matter, index ~734): "Steganoblastus ottawaensis,
  193." — a single page citation to the study's opening page.

No other mention of *Steganoblastus* or Steganoblastidæ occurs anywhere
else in this bound volume of *Geological Magazine*.

## Uncertainties

- The "(1913)"/"(1918)" citation for the second edition of Eastman's
  *Zittel* (p. 194) — OCR reads "1918," which would postdate this May 1914
  paper and cannot be right; the volume's own book-review section elsewhere
  (line 32964 in the OCR text) cites "the … edition (1913) of the
  Eastman-Zittel Text-…", so 1913 is almost certainly the intended reading,
  but this cannot be confirmed from the digit itself — **cannot verify**.
- The postscript's exact issue month (July?) and the Greek etymology for
  *Steganoblastus* are OCR-illegible here too, as in the companion
  `review_1897_whiteaves.md`; not re-litigated in this file.
- Whether Fay 1962's account of a specimen "lent to Mr. Hudson… [and]
  disappeared" refers to specimen B or C (both undesignated as to role
  here, and both still with their 1914 holders/repositories as far as this
  paper states) — **cannot verify** from this text; the loan and loss must
  postdate 1914, since Bather reports no such event.
- Whether "Family Steganoblastidæ" was printed with -idæ, -idae, or the
  Code-preferred stem-corrected form in the 1900 Treatise itself is outside
  this paper's own text (it is cited, not reproduced) — see the existing
  `review_1900_bather.md` for that source's own spelling.
