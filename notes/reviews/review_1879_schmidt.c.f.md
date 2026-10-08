# Review: 1880_schmidt (draft)

Schmidt, Fr. "Ueber Cyathocystis Plautinae, eine neue Cystideenform aus
Reval." *Verhandlungen der Russisch-Kaiserlichen Mineralogischen
Gesellschaft zu St. Petersburg*, Zweite Serie, Fünfzehnter Band: 1–7, three
woodcuts in the text. Title page dated 1880.

Reviewed from nine PDFs in `example-publications/09-18/` (title page,
contents, seven article pages), each with an OCR text layer. This is the
paper Dames abstracted in `1879_dames` and the draft `drafts/1879_dames.yaml`
records secondhand; the draft `drafts/1880_schmidt.yaml` is written from
the paper itself and is what §1–3 below check.

**Page mapping.** The seven article PDFs are one printed page each, "p 01"
to "p 07" = printed pages 1–7; the printed folios read "- 2", "- 3", "4",
"5", "- -6", "7 -", and p. 1 carries the running foot "XV. 1". The title
page and contents page are unnumbered.

## 1. Coverage of the draft

| kind | captured | example |
|---|---|---|
| classification skeleton | all | the Edrioasteriden group with its four listed members and the new genus with two species; nothing else is placed |
| new taxa | all | *Cyathocystis*, *C. Plautinae*, *C. rhizophora*, all `new: true` |
| type species | partly | `type: true` on *C. Plautinae* rests on "der typischen Art" (p. 7); see §3 |
| synonymy lists | na | none printed |
| material | all that is printed | no numbers, no repository, no type words; the figured pieces and the 1863 Wassalem specimens are listed as `unknowntypes` |
| occurrences | all | both units with their localities and the stratigraphic gloss, quoted |
| illustrations | all | Holzschnitt I–III with captions |
| diagnoses | none | no diagnosis is set apart; the descriptive prose (pp. 2–7) is not captured beyond the two quoted sentences on the genus |
| phylogeny | na | none printed |

## 2. What the paper prints

A single description in prose, no headings. The finds (summer 1878,
Reval, the Plautin family) are assigned to "eine neue Cystideenform aus der
Verwandtschaft von Agelacrinus Van. im weitern Sinn, oder eine neue
Gattung aus der von Billings aufgestellten Gruppe der Edrioasteriden" (pp.
1–2), the group's members being listed as *Agelacrinus* Van., *Edrioaster*
Bill., *Hemicystis* Hall and *Cystaster* Hall, with Billings's view that
the group stands nearer the Asteroids than the Cystids. The genus is named
for its cup form and the species for the Generalin Plautin (p. 2, p. 7).
The lid is described plate by plate (pp. 2–4), with the oral plates
compared to Asterids and to *Glyptosphaerites Leuchtenbergi* Volb., the
marginal plates to Asterids, and the valve pyramid called "die
charakteristische Klappenpyramide der Cystideen" (p. 3); no pores (p. 3).
Hall's figures of "Hemicystites (subgen. Cystaster) granulatus Hall" are
compared (p. 4). The one-piece solid calyx, attached by holdfast roots, is
given as the genus's chief peculiarity (p. 5); twinned calyces are read as
budding (p. 5). The second species, *C. rhizophora* from the Hemicosmites
limestone of Wassalem, has never been found with a lid, has thicker walls
and a stronger root apparatus, and occurs in groups of two and three
calyces sharing a canal at the base (pp. 5–7). All originals were going
to Lovén in Stockholm (p. 4); the 1863 Wassalem material went largely to
the Volborth collection, now the Academy's (p. 7).

Every node of the draft was written from these pages; the quoted wording
is in the draft's notes with the page.

## 3. Cases for the data model

**1879 or 1880.** The title page prints 1880 and the volume's Protocolle
are those of 1879. Dames's Referat, in a Heft whose closing notice is
dated 15 October 1879, cites the paper as "Petersburger Mineralog.
Gesellschaft 1879" (`1879_dames`), so the article was in print by then.
The taxa records date the names 1879 and note that Bassler 1935 and Bell
1975 print 1880 (`cyathocystis`, `plautinae_schmidt_1880`). The source key
should carry the year of publication (roadmap ground rules), which the
paper does not settle: the volume as bound is 1880, the article as issued
is 1879 on Dames's evidence. Cannot verify from these pages alone which is
right; the draft is keyed 1880 after the title page and the header comment
says so.

**"der typischen Art" as a type designation.** The paper never prints
"type species"; p. 7 calls *C. Plautinae* "der typischen Art" in a
comparison of epithecae. The draft sets `type: true` on that phrase rather
than the editor's inference (the Fay 1962 precedent, `inferred: [type]`,
was for a monotypic genus with no phrase at all). Whether a passing
"typical species" is a designation is for the owner; the alternative is
`editorial: {inferred: [type], basis: ...}`.

**One genus, two spellings and two structures in one paper.** On p. 2
*Hemicystis* Hall and *Cystaster* Hall are listed as separate members of
the group; on p. 4 the combination is "Hemicystites (subgen. Cystaster)
granulatus Hall". The draft enters the p. 2 list as nodes (records
`hemicystis` and `cystaster` both exist) and keeps the p. 4 combination in
the `hemicystis` note, since entering it would place *Cystaster* twice, as
a genus and as a subgenus, in one tree. The species has no record
(`granulatus_hall_*` is absent). The parenthetical subgenus notation is the
case the brief asks about: the tree's `taxon: hemicystites-subgenus` /
`cystaster-subgenus` records could carry it if the owner wants the usage
as a node.

**A rankless group with a vernacular plural.** "Gruppe der Edrioasteriden"
is neither a rank word nor a Latin name. The draft resolves it to
`edrioasteroidea` with `citedAs: Edrioasteriden` and `auth: [Billings]`
as printed. The dataset's `vulgarSpellingOf` records (e.g. the German
plurals under `acalephida`) are the other way to say it: a record
`edrioasteriden` with `lang: de`, `vulgarSpellingOf: edrioasteroidea`.
Also, the title calls the form a Cystid while the placement puts it with
a group "den Asteroiden näher als den Cystideen verwandt" (p. 2): both are
kept as printed, the tension is the author's.

**Abbreviated authors on a printed line.** "Agelacrinus Van." and
"Edrioaster Bill." print the authors abbreviated. The draft keeps the
abbreviations in `citedAs` and sets `auth` only where the surname is
printed in full ("Hemicystis Hall", "Cystaster Hall"); `auth: [Van.]`
would be the literal alternative, and the rule "attribution exactly as
printed on that line" does not say which.

**`rhizophora_schmidt_1889`.** This paper is the protologue of
*rhizophora* ("n. sp.", p. 2; "die wir C. rhizophora ... nennen", p. 5).
The record's year 1889 is printed nowhere here; the companion review of
`1879_dames` traced it to Jaekel 1927's citation. The record should carry
the paper's year, whichever of 1879 and 1880 the source key takes.

**Substrate has no field.** "auf Callopora heterosolen Dyb. (Chaetetes
heterosole Keys.) aufgewachsen" (p. 1) and "auf allerhand Korallen und
Bryozoen festsitzt" (p. 5) are host statements the occurrence block cannot
carry except in `notes`, where the draft puts them.

**Specimens with no numbers and a stated destination.** As in
`1897_whiteaves`: figured pieces, a donor, a collection, but no catalogue
numbers and no type words, so `unknowntypes` with descriptive strings.
"Sämmtliche Originalstücke gehn noch zu Prof. Lovén nach Stockholm" (p. 4)
is a statement about where the material was going, not a repository.

**Two woodcut numberings.** The text cites figures as "F. I, 2", "F. II
1", "F. III 3 b"; the woodcuts are unnumbered on the page except by their
own captions. The draft records them as `page` + `textFigures` under the
captioned woodcut, naming the Holzschnitt in `notes`.

## 4. Source record

None exists. From the title and contents pages:

    1880_schmidt:
      title: Ueber Cyathocystis Plautinae, eine neue Cystideenform aus Reval
      journal: verh-min-ges-spb   # new: Verhandlungen der Russisch-Kaiserlichen
                                  # Mineralogischen Gesellschaft zu St. Petersburg
      series: 2
      volume: 15
      pages: [1, 7]
      pubDate: {year: 1880}       # title page; see §3 for 1879
      authors: [schmidt]          # new author record: Schmidt, Friedrich ("Mag. Fr. Schmidt")

The contents page gives article I as beginning on p. 1 and article II on
p. 8. The author's given name is not printed beyond "Fr."; cannot verify
dates from these pages.

## 5. Uncertainties

- OCR is clean enough to read every sentence; artefacts seen and corrected
  from context: "nnd" for "und" (p. 1), "Petrafakten" (p. 1, which may be
  the printed spelling; "Petrefakten" on p. 5), "F. 36" for "F. 3 b"
  (p. 3), "3 6" for "3 b" (p. 7), "ans" for "aus" (p. 7). The species
  names "Callopora heterosolen Dyb." and "Chaetetes heterosole Keys."
  (p. 1) are transcribed as OCR'd; the epithet's ending cannot be verified.
- The stratigraphic labels "(C₁)" and "(B)" (p. 1) are read as printed;
  Dames's Referat gives the second species' bed as "Hemicosmitenbank ...
  (1b)", where this paper prints "Hemicosmitenkalk" and no code.
- Woodcut figure letters ("a", "b") are legible in the captions but not
  reliably in the figures themselves in the OCR; the draft cites captions
  only.
- Nothing in the paper dates itself; the 1879/1880 question (§3) stands.
