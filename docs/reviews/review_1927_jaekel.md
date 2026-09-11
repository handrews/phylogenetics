# Review: Jaekel 1927 — "Cyathotheca suecica n. g. n. sp., eine Thecoidee des schwedischen Ordoviciums"

No tree and no `sources.yaml` record exist for this item (`grep` of both
turned up nothing for 1927/Jaekel/suecica; only `1899_jaekel` exists, an
unrelated key). `taxa.yaml` already carries `cyathotheca` (auth jaekel, year
1927) and `suecica_jaekel_1927` (auth jaekel, year 1927), both consistent
with the printed heading. Per the brief, parts 2 and 4 are skipped; this
report summarizes what the paper prints, per (a)–(g).

Two files were read: `1927-00-00-p_C.txt` (the article alone, 7 PDF pages,
one word per OCR line) and `1927-00-00-p_A_archive.txt` (the bound Band 19
volume, 736 pages), whose indices 196–201 contain the identical article
text and confirm the citation. Both agree throughout; quotations below are
page/line-checked against both.

## Page mapping

The article is separately paginated (as is normal for *Arkiv för Zoologi*
articles): PDF index 0 (standalone file) = printed p. 1 of the article,
running consecutively through index 4 = printed p. 5, then index 5 = the
unpaginated plate (Tafel 1), matching the BHL metadata line bundled at the
end of the standalone file: "Jaekel, O. 1927. 'Cyathotheca suecica n. g. n.
Sp., eine Thecoidee des schwedischen Ordoviciums.' Arkiv för zoologi 19A(5),
1–5." In the whole-volume archive file, the same five pages sit at indices
196–200, plate at 201 (index 194 is the tail end of the preceding article,
"Bd 19 A. N:o 4"; index 195 is its plate verso). Both files agree the
article is pp. 1–5 + 1 plate, and the article's own footer prints "Arkiv för
zoologi. Bd 19 A. N:o 5." (p. 1) confirming this is Band 19, series A, No. 5.

## (a) Front matter for a source record

| field | value | basis |
|---|---|---|
| journal | Arkiv för Zoologi, utgivet av K. Svenska Vetenskapsakademien (Royal Swedish Academy of Sciences) | archive index 6, 10 |
| Band | 19 (whole Band spans 1927–1928, "MED 40 AVHANDLINGAR OCH 28 TAVLOR") | archive index 6 |
| series/No. | A, N:o 5 | article's own footer, p. 1 |
| Häfte | 2 ("A N:o 4–18, B N:o 2") | archive index 7, see below |
| pages | 1–5, plus Tafel 1 (unpaginated plate) | both files, BHL metadata |
| author as printed | O. Jaekel | title line |
| title as printed | "Cyathotheca suecica n. g. n. sp., eine Thecoidee des schwedischen Ordoviciums" | title line |
| communicated | "Mitgeteilt am 27. Oktober 1926 durch A. Gavelin und T. Odhner" | p. 1, under the title |
| separately printed | "Tryckt den 21 februari 1927" | p. 5, after the plate explanation |
| Häfte issued ("utkom") | "3 nov. 1927" | archive index 7, the Häfte-contents table |
| Häfte's own title-page year | 1927 (Häfte 1's own title page, archive index 10, reads "1927"; no Häfte-2-specific title page was found in the OCR) | archive index 10 |

**Three distinct dates are printed for this one paper** — read 27 October
1926, separately printed 21 February 1927, and collectively issued as part
of Häfte 2 on 3 November 1927 — the same three-date pattern the roadmap's
A11 discusses for other sources (reading vs. separate printing vs. bound
issue date). None of these dates is in conflict; they simply answer
different questions, and the source record's `pubDate` choice (year: 1927
either way) is unaffected, but `processDates` could usefully carry all
three if the schema supports it.

The Häfte/issue table (archive PDF index 7), quoted as read (OCR of a
tabular layout, ditto marks "»" expanded here for clarity):

> "Häfte 1 inneh. A N:o 1–3, B N:o 1, utkom den 19 mars 1927
> Häfte 2 [inneh.] A N:o 4–18, B N:o 2, utkom [den] 3 nov. 1927
> Häfte 3 [inneh.] A N:o 19–24, B N:o 4, utkom [den] 25 jan. 1928
> Häfte 4 [inneh.] A N:o 25–32, B N:o 8, utkom [den] 15 maj 1928"

A:5 (this paper) falls in the A N:o 4–18 range, hence Häfte 2, "utkom den 3
nov. 1927" (issued 3 November 1927) — printed a full 8+ months after the
paper's own separate printing date of 21 February 1927. Digits in this table
read cleanly in the OCR; still, no independent cross-check was possible
here — mark the exact table transcription **cannot fully verify** without
the original page image, though the pattern (separate print date well before
collective Häfte issue) is internally consistent and typical of this
journal's practice.

## (b) Names and acts printed

Both formal markers appear, exactly, in the title: **"Cyathotheca suecica n.
g. n. sp."** No separate "n. g." / "n. sp." abbreviation recurs inside the
body text; the act is stated in prose instead. The genus is erected in the
paper's second paragraph (p. 1):

> "Da sie sich von deren Typus erheblich entfernen, so habe ich sie zum
> Typus einer neuen Familie der **Cyathocystidae** gemacht." [this refers to
> an act in Jaekel's own earlier work — see (f) below, not this paper]

The genus itself is erected by the whole descriptive-comparative discussion
on pp. 2–3 culminating in the explicit diagnosis on p. 4:

> "Die Diagnose unserer neuen Gattung Cyathotheca würde demnach lauten:
> Theca unregelmässig, becherförmig, aufgewachsen. Oben geschlossen durch 5
> interradiale Platten, neben denen abgesondert der After gelegen war."

No separate diagnosis sentence is given for the species *suecica*; the
generic diagnosis and the specimen description (pp. 2–3, monotypic) serve as
both, per the same convention the roadmap already documents at D8 ("Same as
for species" style deferral, here implicit rather than stated).

**Type fixation, printed but not labelled.** No word for "holotype" or
"genotype" (Genotyp) is printed for *Cyathotheca suecica* itself. What is
printed (p. 1) is a monotypy statement:

> "Es liegt nur ein Exemplar vor, auf das Gattung und Art begründet sind,
> und das in den Fig. 1–3 der Taf. abgebildet ist."
> (Only one specimen is at hand, on which the genus and species are
> founded, and which is figured in Fig. 1–3 of the plate.)

This is the same shape as B14's Fay 1962 case: the type is fixed by original
monotypy, but the word is never printed — `editorial.inferred: [type]` would
be needed if entered.

**A secondhand type-fixation statement for a different genus.** In
discussing the prior state of the field (p. 1, footnote 1), Jaekel calls
*Cyathocystis plautinae* the "**Genotyp**" of *Cyathocystis*:

> "Dieselben sind 1889 von Friedr. Schmidt als Cyathocystis Plautinae
> (Genotyp) aus dem Echinosphäritenkalk von Reval … beschrieben worden."

This is Jaekel asserting Schmidt's type species for *Cyathocystis*, third
party to Schmidt's own paper (not in the supplied Schmidt review file
either) — matching the type statement Bockelie & Paul 1983 later print
("Type species — Cyathocystis plautinae Schmidt, by monotypy," per
`docs/source-observations.md`). A case for B15 ("syn. by"/attribution-of-act
style secondhand claims) generalized to type fixation: this source names the
type species of a genus it did not erect, years before the paper that is
usually cited for that statement.

**A recombination without an explicit formula.** *Cyathocystis corallum*
Jaekel (originally named in Jaekel's own 1918 "System der Pelmatozoen," p.
112, not new here) is discussed in the body text still under its original
combination ("die ich als **Cyathocystis** corallum in meinem System der
Pelmatozoen pag. 112 abbildete," p. 3), but the **plate caption** prints it
under the new genus: "**Cyathotheca** corallum Jaekel sp." (Tafelerklärung,
p. 5; OCR "Cyatholheca corallum JAEKEL sp."). No sentence anywhere states
"n. comb." or otherwise flags the transfer; the recombination is visible
only by comparing the plate caption's genus name against the body text's.
This is a case the current field set does not cleanly cover: a placement
change stated only by the combination printed on a plate, with the running
text still using the old combination when citing the earlier reference.

**An apparent family-name inconsistency, printed as-is.** Two different
family names appear for what reads as one act (p. 4):

> "…die ich 1918 noch einer Familie der **Thecocystidae** zurechnete. Es
> waren das Stromatocystis Pompeckj, Thecocystis Jaekel und Cystaster Hall.
> Es wird also nötig, die Familie meiner Thecocystidae zu einer Ordnung zu
> erweitern und deren einzelnen Formenkreise … als Familien aufzufassen…
> Für eine neue Familie der **Cyathothecidae** würde sich nun folgende
> Definition ergeben: Fam. **Thecocystidae**. Theca sackförmig aus einem
> Stück…"

The lead sentence announces a new family "Cyathothecidae" (evidently meant
for *Cyathotheca*, by the -theca- root), but the diagnosis that immediately
follows is headed "Fam. Thecocystidae" (the *narrower*, redefined form of
Jaekel's existing 1918 family, containing *Thecocystis* and *Cystaster*, not
*Cyathotheca*). Both spellings are internally consistent with real, distinct
roots (*Cyathotheca* vs. *Thecocystis*) rather than being one OCR artifact,
but which family — if either — is actually being defined in that paragraph
cannot be resolved from the text alone. **Cannot verify** without checking
the original page image or a secondary source that cites this passage.
This is on top of the *already*-existing family `Cyathocystidae` named
earlier in the very same paper (p. 1, for *Cyathocystis*) — so the paper
prints three similar but distinct family-group names (Cyathocystidae,
Cyathothecidae, Thecocystidae) across four pages, at most one of which
(Thecocystidae) is unambiguously identified with a stated content
(*Stromatocystis*, *Thecocystis*, *Cystaster*).

## (c) Material

| taxon | role/status | number | repository | notes |
|---|---|---|---|---|
| *Cyathotheca suecica* | sole specimen, type by monotypy (unlabelled) | none printed | Riksmuseum, Stockholm ("Orig. Riksmuseum. Stockholm," plate caption) | "Ein genaues Fundort war leider bei diesem Stück nicht angegeben" (no precise locality was recorded for this piece) |
| *Cyathotheca* (as *Cyathocystis*) *corallum* Jaekel | cited comparative material, not new | none printed | Museum Berlin (plate caption) | figured in Jaekel's own 1918 work; refigured here Fig. 4–6 |

No catalogue numbers are printed for either specimen — a D1 "no catalogue
number" case for both, one Swedish and one already in another museum.

## (d) Locality and horizon

- *Cyathotheca suecica*: "aus den roten eisenhaltigen Kalkmergeln im
  südlichen Schweden, vermutlich aus der Gegend von Boda, Dalarna" (p. 2) —
  explicitly hedged ("vermutlich," presumably) and explicitly incomplete
  ("Ein genauer Fundort war leider bei diesem Stück nicht angegeben," p. 2).
  The **plate caption** (p. 5) gives a different, more specific horizon
  term not used in the body text: "roter Leptaenakalk, Boda, Dalarna" (red
  Leptaena limestone). Age, stated separately in the text (p. 5):
  "Geologische Verbreitung im mittleren und vielleicht schon unteren
  Ordovicium" (geological range: Middle, and perhaps already Lower,
  Ordovician).
- *Cyathotheca* ("*Cyathocystis*") *corallum*: "unteres Ordovicium Gegend
  von Petersburg" (plate caption, p. 5) — Lower Ordovician, vicinity of
  [St.] Petersburg.

## (e) Illustrations

One plate (Tafel 1), captioned in full (p. 5):

> "Fig. 1–3. Cyathotheca suecica n. g. n. sp. roter Leptaenakalk, Boda,
> Dalarna: 1 von oben, 2 von der einen, 3 von der anderen Seite. etwa 10:1;
> 3 a natürl. Grösse. Orig. Riksmuseum. Stockholm.
> » 4–6. Cyathotheca corallum Jaekel sp. unteres Ordovicium Gegend von
> Petersburg. 4 von der Seite 9:1, 4 a in natürl. Grösse, 5 Theca von oben,
> 6 untere Ansatzfläche. Museum Berlin."

Figures 1–3 (+3a) depict the type of *suecica* at ~10:1 and natural size;
figures 4–6 (+4a) depict *corallum* at ~9:1 and natural size. No figure
number is tied to a catalogue number for either (none exist).

## (f) Classification as printed, and earlier work cited

Jaekel's own classification, reconstructed from the running text (no single
formal hierarchy block is printed; this is assembled from scattered
statements, a G7-style case):

- Class **Thecoidea** — Jaekel's own class (not defined in this paper, cited
  as pre-existing: "sich ganz dem Typus meiner neuen Klasse der Thecoidea
  einordnen," p. 1).
- Within it, Schmidt's *Cyathocystis* was earlier made "zum Typus einer
  neuen Familie der Cyathocystidae" (p. 1) — an act attributed to Jaekel's
  own prior work (footnote 2, "Stammesgeschichte der Pelmatozoen," Bd. I, p.
  42), not to this paper.
- This paper's new genus *Cyathotheca* is placed alongside *Cyathocystis*
  ("Durch Cyathotheca wird der engere Verwandschaftskreis von Cyathocystis
  zu einem Familienkreis erweitert," p. 4) — expanding that circle to
  family-group rank, though see (b) above on which family name this
  produces.
- A separate, pre-existing family "Thecocystidae" (Jaekel 1918) contained
  *Stromatocystis* Pompeckj, *Thecocystis* Jaekel, and *Cystaster* Hall (p.
  4); this paper proposes raising it to an order and treating its
  "Formenkreise" (form-circles), plus Bather's Pyrgocystidae, as families
  within that order — a classification act stated in prose, not as a formal
  hierarchy list.
- *Cyathocystis* is explicitly linked back to Billings' Edrioasteridae:
  "wie sie ja auch Schmidt schon als nächsten Verwandten der Billing'schen
  Familie der Edrioasteridae aufgefasst hatte" (p. 1) — i.e. Jaekel notes
  that Schmidt himself already regarded *Cyathocystis* as most closely
  related to Billings' Edrioasteridae, a relationship Jaekel's own
  reclassification (into Thecoidea) supersedes.

Earlier works cited by Jaekel for his own prior classificatory acts:
"Stammesgeschichte der Pelmatozoen," Bd. I, p. 42 (footnote 2 — printed
year reads "1889," almost certainly an OCR/compositor misreading of 1899,
the real publication year of that work; not independently verified here,
**cannot verify**) and "Phylogenie und System der Pelmatozoen," Palaeont.
Zeitschr. III, 1918, p. 112 (footnote 3 — this year reads cleanly and
matches the well-known citation).

**On the assignment's specific question** (relation to *Cyathocystis*,
which Bockelie & Paul 1983 and Guensburg & Sprinkle 1994 later treat as a
close relative/senior synonym): Jaekel treats *Cyathotheca* as congeneric in
family rank with *Cyathocystis* but explicitly distinct at genus rank, on
four stated differences (p. 3): the whole oral field of *Cyathotheca* is
only 5 plates ("die wohl den äusseren und nicht den inneren Oralien von
Cyathocystis entsprechen würden"); *Cyathotheca* lacks marginal ("Saum-")
plates including the inner "Oralien"; it lacks the outer ring of marginal
plates present in *Cyathocystis* between the calyx rim and the orals;
and the anus lies outside the oral field (inside it, in *Cyathocystis*).
Jaekel states the phylogenetic relationship between the two genera "ist aus
den erhaltenen Skeletteilen kaum klarzustellen" (can hardly be clarified
from the preserved skeletal parts, p. 4) — an explicit statement of doubt
about their relationship, not a claim of synonymy or close derivation.

## (g) Uncertainties

- **Schmidt's year, as cited here: "1889."** Footnote 1 (p. 1): "Fr.
  Schmidt, Über Cyathocystis Plautinae … Verhdl. d. Mineral. Ges. Petersburg
  1889, [S.?] Nr. 12." Given every other citation of this work gives 1879 or
  1880 (see the companion Schmidt review), "1889" is very likely a
  "7"/"9" OCR or compositor error, but this cannot be confirmed from the
  file. This plausibly explains the existing `taxa.yaml` record
  `rhizophora_schmidt_1889` (year 1889) even though no other source in the
  corpus supports that year independently.
- **Footnote 2's year, "Berlin 1889."** The real "Stammesgeschichte der
  Pelmatozoen" (Bd. I: Thecoidea und Cystoidea) is dated 1899 in the
  literature generally; "1889" here is again most likely an OCR/compositor
  slip, not confirmed against the original page.
- **The Cyathothecidae/Thecocystidae inconsistency** (see (b)) — cannot
  resolve which family, if either, the printed diagnosis on p. 4 actually
  names, without the original page image or a secondary citation of this
  passage.
- **The classifying author's OCR** is otherwise clean in this file (typed
  one-word-per-line, unlike the 1879 Jahrbuch scan), so confidence in the
  transcription generally is high except for the two "1889" instances
  above and minor letter-level noise (ö/ä rendered variously, "Kelech" for
  "Kelch," etc.) that does not affect any name or number.
- **No precise locality** for the type of *suecica* is available even in
  principle — printed as such, not an extraction gap.
