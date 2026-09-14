# Review: "Schmidt 1879" — *Cyathocystis* / *Cyathocystis plautinae*

No tree and no `sources.yaml` record exist for this item (checked:
`grep -n "1879\|1927" data/sources.yaml` and `data/trees/` — no hits; no
`1879_schmidt` or similar key). `taxa.yaml` already carries three records
that depend on it: `cyathocystis` (auth Schmidt, year 1879, note "1935_bassler
says 1880 for reasons unclear"), `plautinae_schmidt_1879` / `plautini_schmidt_1880`
(linked by `altSpellingOf`), and `rhizophora_schmidt_1889`. Per the brief, parts
2 and 4 (correctness against a tree, source-record check) are skipped; this
report summarizes what the supplied text prints, per (a)–(g), so the owner can
decide how to enter it.

## Page mapping

`1879-00-00-p_N.txt` is the full Jahrgang 1879 of *Neues Jahrbuch für
Mineralogie, Geologie und Paläontologie* (1112 PDF pages). Printed page
numbers are visible directly on PDF pages in this stretch of the volume:
indices 1040–1048 print 995–1003 in sequence, so **printed page = PDF index
− 45** here, confirmed on nine consecutive pages, not assumed. This offset is
local: at PDF index 700 the printed page is 695 (offset 5), so plates and
unnumbered leaves shift the count elsewhere in the volume and the −45 offset
is not carried beyond the region checked. The owner's index 1046 = printed
p. 1001 is confirmed directly.

## The central finding: this is not the protologue

**The text at printed p. 1001 is a third-party review (*Referat*) by W.
Dames of Schmidt's paper, not Schmidt's own protologue text.** The heading
and byline read, in full (p. 1001):

> "Fr. Schmwr [OCR of Schmidt]: Über Cyathocystis Plautinae, eine neue Cy­stideenform aus Reval. (Petersburger Mineralog. Gesellschaft 1879)."
> … [body, third person] …
> "W. Dames."

Every entry in this section of the Jahrbuch (the abstracts/*Referate*
department) is a summary of a work published elsewhere, signed with the
reviewer's name at the end — the same pattern appears immediately before and
after this entry ("Benecke.", "Steinmann.", "v. Koenen." sign neighbouring
abstracts of other authors' papers). The whole entry narrates in third
person ("*Die hier beschriebene und abgebildete neue Gattung ist…*" = "The
new genus described and figured *here*…", i.e. in Schmidt's paper, not this
one) and closes "W. Dames.", the reviewer, not Schmidt. So a source record
built from this file would misattribute Dames's paraphrase to Schmidt as if
it were his own words, and would record the wrong place of publication for
the genus and species if it cited the Neues Jahrbuch as the protologue venue.

The parenthetical "(Petersburger Mineralog. Gesellschaft 1879)" is Dames's
citation of where Schmidt's paper appeared: the Mineralogical Society of St.
Petersburg. Two other citations of the same external work are on record
elsewhere and disagree on volume, pages and year:

| citing work | citation given | year |
|---|---|---|
| this Referat (p. 1001) | "(Petersburger Mineralog. Gesellschaft 1879)" | 1879 |
| Bell 1975 bibliography (per `notes/audits/source-observations.md`; not independently checked here) | "Verh., ser. 2, vol. 15, pp. 1–5" | 1880 |
| Bockelie & Paul 1983 (per the assignment/roadmap) | pp. "1–7" | 1879 |
| Jaekel 1927 (checked directly, see the companion review) | "Verhdl. d. Mineral. Ges. Petersburg 1889, [S.?] Nr. 12" | "1889" (see below) |

**A plausible resolution, offered as a hypothesis and not a verified fact:**
the Neues Jahrbuch *Referat* (this file) and the actual Verhandlungen der
Mineralogischen Gesellschaft article are two different printings/venues.
If the Jahrbuch volume's own content was substantially complete within 1879
(see below) while the St. Petersburg Verhandlungen volume itself did not
appear until 1880, both "1879" and "1880" could be correct for their
respective venues — the A11/A8 pattern the roadmap already anticipates for
Schmidt. This cannot be confirmed from the files at hand: **cannot verify**
without the St. Petersburg Verhandlungen itself, which is not among the
supplied texts.

## Issue date of the Heft containing p. 1001

No wrapper or "ausgegeben"/"Ausgabe" notice survives in the OCR text for the
specific Heft that contains p. 1001. What the volume's own back matter does
show:

- A "Mittheilung der Redaction" (found near PDF index 829/printed p. ~784)
  apologises for issuing "doppelte und dreifache Hefte" (double and triple
  Hefte) because of backlog — so by the second half of the volume, Heft
  numbers no longer correspond one-to-one with fascicles.
- A "Berichtigung" printed later in the volume refers back to "Heft 3 u. 4
  pg. 242", so Heft 3+4 was already a combined double Heft ending somewhere
  after p. 242.
- The volume's last dated item, right after the paginated content ends
  (~p. 1055 by page count, PDF index ~1098–1100), is the outgoing editors'
  own closing notice announcing changes for 1880, dated and signed
  "Strassburg, Göttingen, Heidelberg, 15. October 1879. E. W. Benecke,
  C. Klein, H. Rosenbusch." A publisher's companion notice is dated
  "Stuttgart, 15. October 1879," and a bound-in price notice a little later
  is dated "November- 1879."

None of these is an explicit issue date for the Heft carrying p. 1001. The
closing items being dated 15 October and November 1879, and following all of
the year's paginated content (of which p. 1001 is only the 91st page from
the end of ~1101), supports the printed volume as a whole being **completed
and current within 1879** — consistent with Bockelie & Paul's "1879"
citation — but the exact month for p. 1001 specifically is **cannot
verify**.

## (a) Front matter for a source record

A source record can be made for the Neues Jahrbuch *Referat* itself (not for
Schmidt's protologue, which is not in these files):

| field | value | basis |
|---|---|---|
| journal | Neues Jahrbuch für Mineralogie, Geologie und Paläontologie | title page, PDF index 6 |
| Jahrgang | 1879 | title page |
| Heft | "Heft 1.2" redigirt von G. Leonhard u. H. B. Geinitz; "Heft 3–9" herausgegeben von E. W. Benecke, C. Klein, H. Rosenbusch (title page); the specific Heft number for p. 1001 is not determinable from the OCR — **cannot verify** |
| page | 1001 (printed); PDF index 1046 | verified directly, see mapping above |
| item type | *Referat* (review/abstract), not an original article | signed "W. Dames." at the end; third-person narration throughout |
| reviewer | W. Dames | signature line |
| author of the reviewed work | Fr. Schmidt (OCR "Schmwr") | heading |
| cited venue of the reviewed work | "(Petersburger Mineralog. Gesellschaft 1879)" | as printed in the heading |
| printed date for this Heft | none found | see above |

The Jahrbuch's own printed title (title page, PDF index 6): "**Neues
Jahrbuch für Mineralogie, Geologie und Paläontologie.** Jahrgang 1879. Heft
1.2 redigirt von G. Leonhard und H. B. Geinitz, Professoren in Heidelberg
und Dresden. Heft 3–9 unter Mitwirkung einer Anzahl von Fachgenossen
herausgegeben von E. W. Benecke, C. Klein und H. Rosenbusch in Strassburg
i. Els., in Göttingen, in Heidelberg. Mit IX Tafeln und mehreren
Holzschnitten. Stuttgart. E. Schweizerbart'sche Verlagshandlung (E. Koch).
1879."

## (b) Names and acts printed

None of the Code-formal markers ("n. g.", "n. sp.") appear anywhere in this
text. The entire passage is prose, third person, and never uses an
abbreviation for a nomenclatural act. What is printed (p. 1001), quoted in
full:

> "Die hier beschriebene und abgebildete neue Gattung ist aufgewachsen mit
> dem stumpf pentagonalen Kelch. Auf diesem aus einem Stück bestehenden
> Kelche ist ein Deckel befindlich, welcher aus fünf Ambulacralstrahlen
> (jeder von diesen aus zwei mit einander alternirenden Plättchenreihen
> bestehend) und aus fünf Interambulacralplatten, welche mit den ersteren
> alternirend gestellt sind und nur aus einem einzigen dreieckigen Stück
> bestehen, zusammengesetzt ist. Im Centrum des Deckels sind fünf
> unregelmässig-pentagonale Plättchen, den Spitzen der Interambulacraltafeln
> aufgesetzt, welche in der Mitte unregelmässig zusammenschliessen. Der Rand
> des Deckels besteht aus einer continuirlichen Reihe von
> Marginalplättchen. Auf einer Interambulacralplatte erhebt sich die wohl
> bekannte fünfplattige Pyramide der Cystideen. Von regelmässigen Poren ist
> nichts wahrnehmbar. Die Oberfläche der einzelnen Plättchen ist fein
> gekörnelt. Auch eine innere Doppelreihe von Plättchen ist wahrscheinlich
> vorhanden."

No genus name is actually printed in this descriptive paragraph — the genus
(*Cyathocystis*) is named only in the heading and in the two species
statements that follow:

> "Es werden zwei Arten unterschieden: 1. Cyathocystis Plautinae aus dem
> Echinosphäritenkalk (= der oberen Abtheilung des Orthocerenkalks nach des
> Autors neuester Eintheilung des Untersilur) von Reval, gesammelt von der
> Generalin Plautin und nach ihr benannt; 2. Cyathocystis rhizophora aus der
> Hemicosmitenbank der Jeweschen Schicht (1b), welche fast stets in mehreren
> zusammengewachsenen Kelchen vorkommt, einen bedeutender entwickelten
> Wurzelhaftapparat und viel dickere Kelchwände besitzt, bisher aber noch nie
> mit Deckel gefunden wurde."

No type-species statement is printed here for the genus (contrast Jaekel
1927, reviewed separately, which does call *plautinae* the "Genotyp"). Since
this is a review of Schmidt's paper rather than the paper itself, whether
Schmidt himself used "n. g." / "n. sp." and fixed a type species in his own
text is **cannot verify** from this file.

## (c) Material

No catalogue numbers, no repository, no specimen count. The only collecting
information printed: *plautinae* "gesammelt von der Generalin Plautin und
nach ihr benannt" (collected by the Generalin [general's wife] Plautin, and
named after her) — an eponym note, not a specimen record.

## (d) Locality and horizon

| species | locality | horizon, as printed |
|---|---|---|
| *plautinae* | Reval | "Echinosphäritenkalk (= der oberen Abtheilung des Orthocerenkalks nach des Autors neuester Eintheilung des Untersilur)" — i.e. equated, in the review's own parenthetical, with the upper division of the Orthocerenkalk under the author's newest subdivision of the Lower Silurian |
| *rhizophora* | not stated beyond the unit name | "Hemicosmitenbank der Jeweschen Schicht (1b)" |

## (e) Illustrations

The review states the genus is "hier beschriebene und **abgebildete**" (also
figured) but names no plate or figure number, and none of the volume's own
plate list entries (Tafel I–IX, per the title page) is tied to this item in
the text supplied. **Cannot verify** whether/where a figure exists in this
Jahrbuch printing; the figures, if any, are more likely in Schmidt's own
St. Petersburg paper.

## (f) Classification as printed, and earlier work cited

> "Die neue Gattung gehört in die S[OCR: "SrıLzına"]'sche Gruppe der
> Edrioasteriden mit Agelacrinus, Edrioaster, Hemicystis und C[OCR:
> "Oystastes"], die mehr Analogieen mit Asteriden als mit Cystideen zeigen."

Translation: "The new genus belongs in [a named author]'s group of the
Edrioasterids, with *Agelacrinus*, *Edrioaster*, *Hemicystis* and
*Cystaster*, which show more analogies with Asterids than with Cystids."

- **Not called a cystid**, despite Schmidt's own paper title (as quoted in
  the heading) calling it "eine neue Cystideenform" (a new cystoid-type
  form). The review's classifying sentence explicitly aligns the genus with
  the Edrioasteroids/Asteroids over the Cystoids. Whether that tension is
  Schmidt's own hedge or Dames's editorial gloss cannot be told from a
  third-person review — **cannot verify**.
- **Group name illegible.** The OCR string "SrıLzına'sche" cannot be
  resolved to a known author's name with confidence (candidates considered
  and rejected on spelling grounds: Stoliczka, who appears two entries later
  in the same section; Zittel; Stur). Quote the OCR reading and mark
  **cannot verify** without the original page image.
- **Compared taxa, as printed:** *Agelacrinus* (not *Agelacrinites*),
  *Edrioaster*, *Hemicystis* (not *Hemicystites*), and OCR "COystastes"
  (almost certainly *Cystaster* Hall). Answering the assignment's direct
  question: yes to *Edrioaster* and (in the spelling-variant sense) to both
  *Agelacrinites* and *Hemicystites*.
- No earlier classificatory work is cited by name in this passage beyond the
  unresolved group author.

## (g) Uncertainties

- **The identity of the text itself.** This is Dames's abstract of Schmidt's
  paper, not the protologue. A source record entered from this file alone
  would misrepresent the place and form of first publication; if the
  dataset wants the actual protologue, it needs the Verhandlungen der
  Mineralogischen Gesellschaft zu St. Petersburg, ser. 2, vol. 15 (per Bell's
  bibliography, itself not independently checked here), which is not among
  the supplied texts.
- **Year.** 1879 (this Referat, and Bockelie & Paul's citation) vs. 1880
  (Bell 1975, Bassler 1935's citations of the Petersburg original) vs. 1889
  (Jaekel 1927's own footnote citation, almost certainly a "7"/"9" OCR or
  compositor slip for 1879, but not independently confirmed — see the
  companion Jaekel review). Existing `taxa.yaml` note on `cyathocystis`
  ("1935_bassler says 1880 for reasons unclear") is now partly explained: at
  minimum, two distinct publications (the St. Petersburg original and this
  Jahrbuch review of it) exist for the same act, so "1879" and "1880" need
  not be an error in either citing work — each may correctly cite a
  different printing. **Cannot verify** without the Petersburg original.
- **The classifying author's name** ("SrıLzına'sche") — OCR-illegible, see
  above.
- **Illustration location** — not stated in the review; cannot verify
  whether the Jahrbuch page itself carries a figure.
- **No material, no repository** is printed here at all; this is scope the
  Jahrbuch review never had, not a gap in extraction.
- **Existing data note `rhizophora_schmidt_1889`** in `taxa.yaml`: this
  review gives no year for *rhizophora* independent of the shared heading
  year (1879 as cited here). The "1889" in the current record likely
  originates from Jaekel 1927's own footnote citation of Schmidt (see the
  companion review), not from this Jahrbuch item.
