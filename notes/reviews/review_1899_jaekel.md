# Jaekel 1899, *Stammesgeschichte der Pelmatozoen*, Erster Band — review

No tree file exists for `1899_jaekel`; a source record exists. Per brief, this is a
"what it prints" scoping summary, not a node-by-node audit.

## Page mapping

Printed page = PDF page index − 15. Verified at eight independent anchors spread
across the whole main text: page 10 (idx 25, "Vorbemerkung" close), page 47 (idx 62,
"II. Fam. Agelacrinidae." running head), page 65 (idx 80, "Cystoidea. 65"), page 169
(idx 184, "M. Die phyletische Gliederung. 169"), page 174 (idx 189, Stammbaum), page
178 (idx 193, "I. Ord. Dichoporita." first formal heading), page 328 (idx 343, mid
Echinosphaeridae), page 395 (idx 410, "Fam. Sphaeronidae. 395"), page 439 (idx 454,
"Litteratur-Verzeichniss. 439"), page 442 (idx 457, "Alphabetisches Namen-Register.").
The offset held exactly at every check; it may be off by 1 on unnumbered section-opening
half-title pages (e.g. the "Thecoidea." divider leaf). Front-matter roman numerals
(title, dedication, preface, table of contents) are not covered by this formula and are
cited by their own printed roman numerals where visible.

## (e) Front matter vs. the source record

Title page (PDF idx 6): "STAMMESGESCHICHTE DER PELMATOZOEN VON DR. OTTO JAEKEL. ERSTER
BAND. THECOIDEA UND CYSTOIDEA. MIT 18 TAFELN UND 88 IN DEN TEXT GEDRUCKTEN FIGUREN. …
BERLIN. VERLAG VON JULIUS SPRINGER. 1899." Verso (idx 7): "Buchdruckerei von Gustav
Schade (Otto Francke) in Berlin N." Dedication (idx 8): "Dem Andenken an Johannes
Müller den Begründer der Echinodermen-Forschung." No date beyond the bare year "1899."
is printed anywhere found. Extent: front matter in roman numerals (Vorwort, Inhalt),
main text runs to at least printed page 442 (start of "Alphabetisches Namen-Register"),
followed by "Litteratur-Verzeichniss" (starts 439, so partly interleaved with the
register pagination — TOC gives Litteratur-Verzeichniss its own start page 437 and
Namen-Register 442, consistent with the body check), then 18 unpaginated plates
("Taf. I" … "Taf. XVIII", confirmed by the plate-explanation captions naming each
plate up to "Tafel XVIII" at the very end of the file) with 88 in-text figures.

`data/sources.yaml` record `1899_jaekel` (line 1149): `book: stamm` (→
`Stammesgeschichte der Pelmatozoen` in publications.yaml), `pubDate.year: 1899`,
`authors: [jaekel]`, a Google Books identifier URL. Author, title stem, and year all
match. Two gaps, for the owner to weigh rather than errors as such:
- No field carries the volume-specific subtitle "Erster Band: Thecoidea und
  Cystoidea." The project does use a `title:` field for a part/volume subtitle
  elsewhere on a multi-part work (e.g. `1900_bather`: `title: Part III — The
  Echinoderma` under `book: treatise-zoo`) — the same pattern would fit here if
  Jaekel's later Bände (Blastoidea etc.) are ever entered and need distinguishing.
- No `plates:`/`pages:` fields, but that matches the project's practice for other
  whole-monograph `book:` records (e.g. `1854_müller.j.p`), so likely not a gap.

## (a) Overall classification printed (from the Inhalt, pag. VII–XI, PDF idx 12–15)

Rank words are exactly as printed (abbreviations: Fam. = Familie, Unt. Ord./Unterfam.
= Unterordnung/Unterfamilie, Ord. = Ordnung). Only the two Bände-level classes treated
in this volume are covered; "Pelmatozoa" itself is not subdivided in a single table
anywhere in this book — the two classes are simply the two halves of the volume.

```
Einleitung  (pag. 1-5)

Thecoidea  (pag. 6-51)
  N. Die Systematik (32)
    I. Fam. Thecocystidae (35): Stromatocystis (36), Cyathocystis (42),
       Thecocystis (43), Cystaster (43), Edrioaster (44), Dinocystis (46)
    II. Fam. Agelacrinidae (47): Hemicystites (49), Agelacrinites (49)

Cystoidea  (pag. 53-436)
  N. Die systematische Eintheilung (~174/178)
    I. Ord. Dichoporita (178-345)
      1. Unt. Ord. Regularia (p.65 Uebersicht; "A. Regularia" in body)
        Fam. Chirocrinidae (212): Chirocrinus
        Fam. Cystoblastidae (222): Cystoblastus
        Fam. Pleurocystidae (230): Pleurocystites
        Fam. Scoliocystidae (235): Echinoencrinites, Erinocystis, Glaphyrocystis,
          Scoliocystis, Prunocystites, Schizocystis
        Fam. Callocystidae (266)
          a) Unterfam. Glyptocystinae (274): Glyptocystites
          b) Unterfam. Apiocystinae (277): Meekocystis, Apiocystites
          c) Unterfam. Staurocystinae (282): Pseudocrinites, Staurocystis
          d) Unterfam. Callocystinae (287): Hallicystis, Sphaerocystites,
             Callocystites
      2. Unt. Ord. Irregularia ("B. Irregularia" in body, 291-345)
        Fam. Caryocrinidae (292): Hemicosmites, Corylocrinus, Stribalocystites,
          Caryocrinites
        Fam. Echinosphaeridae (315): Stichocystis, Caryocystites,
          Echinosphaerites, Amorphocystis
        Fam. Tetracystidae (340): Rhombifera, Tiaracrinus, gen. ind. Heterocystites
    II. Ord. Diploporita (346-436)
      Fam. Mesocystidae (372): Mesocystis, Asteroblastus, Blastoidocrinus
      Fam. Sphaeronidae (390): Archegocystis, Sphaeronites, Allocystites,
        Codiacystis, Calix, Lodanella, Eucystis
      Fam. Aristocystidae (398): Aristocystites, Trematocystis
      Fam. Gomphocystidae (404): Pyrocystites, Gomphocystites
      Fam. Glyptosphaeridae (411): Glyptosphaerites
      Fam. Dactylocystidae (414): Protocrinites, Dactylocystis
```

Page numbers below the family level are transcribed from the two-column TOC layout
and cross-checked against a handful of body anchors (Archegocystis 395, Chirocrinidae
212, Agelacrinidae 47, Dichoporita 178 — all confirmed exact); the rest are "cannot
independently verify to the page" but internally consistent.

## (b) Thecoidea in detail

**Definition (page 9-10, PDF idx 24-25):** "Thecoidea sind Pelmatozoen, deren 5 radiäre
Ambulacralstämme keine Seitenzweige oder freie Arme treiben, sondern in ganzer
Ausdehnung an den Körper gebunden sind und durch differenzirte Thecalplatten
geschlossen werden."

**Origin of the name (page 9):** "Der Begriff und Name Thecoidea wurde 1895 (II, 110)
von mir aufgestellt und nach Inhalt und Umfang kurz charakterisirt." — i.e. Jaekel
states explicitly that *he coined Thecoidea in 1895*, not in this 1899 book (matches
`taxa.yaml`'s `thecoidea: auth:[jaekel] year: 1895`, so that name is correctly *not*
among the "credited to 1899" set below).

**Declined name (page 9):** Jaekel quotes Billings 1858 proposing "Edrioasteridae"
for this group ("… it is probable that they will be arranged as a suborder, for which
the name Edrioasteridae would be appropriate …") and explains why he did not adopt it:
"Dass ich den hier vorgeschlagenen Namen Edrioasteridae nicht für den genannten Kreis
… übernommen habe, hat wesentlich darin seinen Grund, dass ich erstens die
vorliegenden Formen nur als Pelmatozoen, nicht als Asteriden betrachten kann, und dass
zweitens die genannte Wortbildung nach den heutigen Regeln der Nomenklatur nur zur
Bezeichnung einer Familie, nicht aber einer Klasse verwendet werden darf." He also
rejects S. A. Miller's 1889 "Agelacrinoidea" as a replacement for Billings' name.

**Genus roll for Thecoidea, as given (page 10), with attribution exactly as printed:**
"Agelacrinus*), VANUXEM, 1842. Haplocystis, F. ROEMER, 1851. Hemicystis, HALL, 1852.
Cyclaster, BILLINGS (non COTTEAU 1856), 1857. Edrioaster, BILLINGS, 1858. Cystaster,
HALL, 1871. Streptaster, HALL (ohne Definition). Lepidodiscus, MEEK & WORTHEN, 1875.
Cyathocystis, F. SCHMIDT, 1879. Echinodiscus, WORTHEN & MÜLLER, 1883. Stromatocystis,
POMPECKJ, 1896. Agelacystis, HAECKEL, 1896. Discocystis, GREGORY, 1897. Thecocystis,
n. g. Dinocystis, n. g." Note "Streptaster, HALL (ohne Definition)" — Jaekel himself
flags it as a nomen nudum.

Of these 15 nominal genera Jaekel recognises only 8 as valid, sunk into two families
(page 35, "N. Die Systematik"): "Ich beschränke mich daher darauf, die Thecoidea in
einige Familien zu gliedern." He gives a key by attachment/shape/skeleton/ambulacrum
character rather than a Latin diagnosis for the split itself.

### I. Fam. Thecocystidae (page 35)

Definition (page 35-36): "Körper pentangular oder sphäroidisch, sack- oder becher-
förmig, frei oder mit einem Theile der Unterfläche angewachsen. Theca lederartig mit
kleinen, z. Th. schwach verkalkten oder dickeren polygonalen, einfach apponirten oder
theilweise verschmolzenen Platten. Ambulacra kurz und gerade oder spiral verlängert,
Saumplättchen oft wenig differenzirt. Cambrium und Untersilur. Europa und Nordamerika."
No "m." (mihi) or "n. fam." marker is used, but the erection is unambiguous — the two
prior sentences state he is dividing Thecoidea into families of his own choosing.

| Genus | Printed attribution | Page | Status |
|---|---|---|---|
| Stromatocystis | Stromatocystites POMPECKJ, 1896 (I, 505) | 36 | pre-existing, redescribed |
| Cyathocystis | Cyathocystis F. SCHMIDT, 1879 (II, 2) | 42 | pre-existing |
| Thecocystis | Thecocystis n. g. | 43 | new genus, Jaekel |
| Cystaster | Cystaster J. HALL, 1871 | 43 | pre-existing |
| Edrioaster | Edrioaster, BILLINGS, 1858 | 44 | pre-existing |
| Dinocystis | Dinocystis n. g. | 46 | new genus, Jaekel — see caveat below |

New species in Thecocystidae:
- **Stromatocystites balticus n. sp.** (page 42): "mittleres Cambrium (Sandstein mit
  Paradoxides Tessini) des baltisch-skandinavischen Silurgebietes. Haut lederartig
  biegsam. Skelet schwach verkalkt, indifferent, undeutlich gegliedert. Saumplatten
  klein." (= `balticus_jaekel_1899` in `taxa.yaml`.)
- **Th. sacculus n. sp.** (page 43, Taf. I fig. 1a, 1b) — a *Thecocystis* species. Not
  present anywhere in `taxa.yaml` (a coverage gap for whenever this source is entered,
  not an error).
- **Dinocystis n. g., diagnosis** (page 46): "Körper oval, mit kleiner, ringförmig
  umgrenzter Fläche aufgewachsen. Theca schwach skeletirt, oben mit kleinen
  polygonalen, unten mit noch kleineren querverlängerten Plättchen getäfelt. Ambulacra
  sehr lang, contrasolar gedreht, schmal, mit wenig differenzirten kleinen
  Saumplättchen. After klein, eine winklige Ausbiegung des Ambulacrum I veranlassend."
  Type species **D. Barroisi n. sp.** (page 46-47): "Untersilur. Condroz, Ardennen. …
  Ich nenne die Art zu Ehren des Herrn CHARLES BARROIS in Lille."

  **Caveat for the data model:** `taxa.yaml`'s `dinocystis` record reads `auth:
  [bather] year: 1898`, but nothing in this book supports that. Jaekel lists
  "Dinocystis, n. g." in his own name at page 10 and again erects it formally
  ("Dinocystis n. g.") at page 46 with no citation to Bather anywhere nearby or
  anywhere else the name occurs in the volume (checked every occurrence). Also
  worth noting: the *species* epithet "barroisi" recurs unrelated in `taxa.yaml` as
  `barroisi_bather_1898` (a different genus/species, not a conflict, just a
  coincidence of epithet). If Bather 1898 (cited in the Litteratur-Verzeichniss as
  "F. A. Bather: Mesites, Ann. u. Mag. Nat. Hist. Ser. 7 Vol. I pag. 102") published
  Dinocystis first as a manuscript name credited to Jaekel, that would explain the
  current attribution, but it cannot be confirmed or denied from this text — flag as
  "cannot verify" and worth checking Bather 1898 directly.

### II. Fam. Agelacrinidae (page 47)

Erection, printed exactly (page 47): **"II. Fam. Agelacrinidae m."** — "m." = *mihi*
("of me"), i.e. Jaekel explicitly claims this family name as his own. Full formal
Definition follows: "Körper mützen- oder hutförmig; Oberseite in der Mitte konvex, am
Rande niedergedrückt, Unterseite eben, mit ganzer Fläche aufgewachsen. Theca, abgesehen
von den Saumplättchen der Ambulacra, aus schuppig übergreifenden Plättchen
zusammengesetzt, die an Grösse nach dem Rande abnehmen und dort fest mit einander
verwachsen sind. Ambulacra gerade oder spiral gedreht, wobei das 5. und auch das 4.
kontrasolar gedreht sein kann. After mit unregelmässig gestellten Plättchen
geschlossen. Saumplatten gross, fingerförmig, Subambulacra vorhanden."

| Genus | Printed attribution | Page |
|---|---|---|
| Hemicystites | Hemicystites HALL 1852 (I, 245); syn. Agelacrinites Beyr. Roem. Barr. non Van., Hemicystis aut. | 49 |
| Agelacrinites | Agelacrinites VANUXEM 1842 (I, 158); syn. Agelacrinus aut., Agelacystis Haeck. | 49 |

The only species-author citation touching "Agelacrinidae" anywhere in the book is a
species, not the family: "H. Billingsi CHAPMAN 1860 (Can. Journ. 5 pag. 358)" (page
49) — Chapman's name **Chapman**, the man usually credited as author of family
Agelacrinidae (1860), is never mentioned in connection with the family name itself;
Jaekel's "m." appears to be made in ignorance of Chapman's prior use, not as a
conscious replacement.

## (c) Names in `data/taxa.yaml` credited to Jaekel 1899

Only one taxon points at the source key directly (`authority: source: 1899_jaekel`):
`dichoporita` (Order). Filtering `auth: [jaekel]` + `year: 1899` finds 16 more. All 17
were checked against the book:

| Key | Printed as | Page | Verdict |
|---|---|---|---|
| dichoporita (Order) | "die Dichoporita und die Diploporita" first named p.169; formal "I. Ord. Dichoporita" heading | 169 / 178 | confirmed |
| thecocystidae (Family) | "I. Fam. Thecocystidae" | 35 | confirmed |
| thecocystis (genus) | "Thecocystis n. g." | 43 | confirmed |
| erinocystis (genus) | "Erinocystis n. g." (Uebersicht p.65; full description p.249, register "Erinocystis 249") | 65/249 | confirmed |
| hallicystis (genus) | "Hallicystis n. g." | 287 (per Uebersicht/register; text at line 19495) | confirmed |
| archegocystis (genus) | "Archegocystis n. g." | 395 | confirmed |
| angelini_jaekel_1899 (sp.) | "Apiocystites Angelini n. sp." (register "Apiocystites Angelini JKL.") | ~277-282 range (Callocystidae/Apiocystinae) | confirmed genus placement Apiocystites |
| atavus_jaekel_1899 (sp.) | "Chirocrinus atavus n. sp." (register "Chirocrinus atavus JKL.") | 193-249 range (Chirocrinidae) | confirmed |
| balticus_jaekel_1899 (sp.) | "Stromatocystites balticus n. sp." | 42 | confirmed, notes field ("Stromatocystites") correct |
| granulatus_jaekel_1899 (sp.) | "Ch. granulatus n. sp." = Chirocrinus granulatus (register "Chirocrinus granulatus JKL.") | Chirocrinidae section | confirmed — **not** the pre-existing "Cystaster granulatus J. HALL, 1872" also mentioned in the Thecoidea section; two different species share the epithet, no conflict |
| interruptus_jaekel_1899 (sp.) | "Ch. interruptus n. sp." = Chirocrinus interruptus | Chirocrinidae section | confirmed |
| reticulatus_jaekel_1899 (sp.) | "E. reticulatus n. sp." = Echinoencrinites reticulatus | Scoliocystidae section | confirmed |
| apiocystitinae (Subfamily) | printed "**Apiocystinae**" (no "tit"), e.g. "b) Unterfam. Apiocystinae" | 277 | **spelling mismatch** — book never spells it "Apiocystitinae" |
| scoliocystinae (Subfamily) | not found | — | **cannot confirm** — "Scoliocystinae" does not appear anywhere in the book; only Fam. **Scoliocystidae** (a family, not a subfamily, with no internal subfamily subdivisions in the TOC or text) exists. Possible conflation with Scoliocystidae. |
| staurocystinae (Subfamily) | "c) Unterfam. Staurocystinae" | 282 | confirmed, spelling matches |
| cheirocrinidae (Family) | printed consistently "**Chirocrinidae**" (no "ei"), e.g. "1. Fam. Chirocrinidae", "Der hier zum Range einer Familie erhobene Formenkreis…" (erection quote, page 212) | 212 | confirmed as new-to-Jaekel, but **spelling mismatch**: book never spells it "Cheirocrinidae" (the genus itself is likewise always "Chirocrinus", never "Cheirocrinus", in this book) |

Erection quote for Chirocrinidae (page 212): "Der hier zum Range einer Familie
erhobene Formenkreis ist so eng geschlossen, dass ich glaube, die hierher gehörigen
Mitglieder desselben in eine Gattung zusammenstellen zu müssen." (He sinks Billings'
Glyptocystites, Eichwald's Chirocrinus, and Barrande's Homocystites all into one genus,
Chirocrinus Eichwald 1856.)

## (d) Regnéll/Bassler attributions to "Jaekel, 1899"

- **"Agelacrinidae Jaekel, 1899"** — the name does print here, with Jaekel explicitly
  self-crediting it ("Fam. Agelacrinidae m.", page 47, quoted above). So Bassler 1935's
  citation is textually accurate as to *what Jaekel printed and claimed*, even though
  standard usage credits the family to Chapman 1860 (whom Jaekel never mentions in that
  connection). `data/taxa.yaml`'s `agelacrinidae` record correctly follows the
  Chapman 1860 priority rather than Jaekel's "m.", so no change indicated there — but
  worth a note if this source is entered, since the printed page genuinely reads "m."
- **"Eocrinoidea"/"Eocrinida"** — **confirmed absent** as a formal taxon name.
  "Eocrinoidea"/"Eocrinida" do not occur anywhere in the file (checked every
  occurrence of "eocrin" case-insensitively). The only related word is the informal
  collective noun "**Eocriniten**"/genus name "**Eocrinites**" (pages 174 and 210),
  used descriptively for primitive pinnule-less forms ancestral to Cladocrinoidea and
  Chirocrinus: "die Macrocystellidae … die man auf Grund des Mangels von Pinnulis zu
  Eocriniten zusammenfassen kann" (page 210) — not capitalised as a Klasse/Ordnung, and
  never given a formal Latin diagnosis. This corroborates Regnéll 1945 p. 14: the
  formal name "Eocrinoidea" is not in Jaekel 1899 (`taxa.yaml`'s own `eocrinoidea`
  record already correctly credits it to `jaekel 1918`, not 1899, so the dataset
  already agrees with Regnéll here).
- **Cyclocystoidea** — appears exactly once (page 9), only as a citation of S. A.
  Miller's 1889 classification ("Palaeocrinoidea, Blastoidea, Cystoidea,
  Lichenocrinoidea, Agelacrinoidea, Cyclocystoidea und Myelodactyloidea"), which Jaekel
  is criticising, not adopting. Not a Jaekel 1899 name; `taxa.yaml` correctly credits
  it to Miller & Gurley 1895 already.
- **Pyrgocystis** — does not appear anywhere in this book (checked). Not covered by
  this volume.

## (f) Uncertainties

- OCR of Fraktur/Antiqua mix is generally clean for German prose but unreliable on
  italicised Latin genus/species names and on author-citation punctuation (commas vs.
  periods, spacing before page numbers in "(I, 505)" style citations); treat any
  Latin name spelling not cross-checked against the printed alphabetic register
  (pages 442+) as unconfirmed.
- Page-number offset (index − 15) is confirmed at 8+ anchors across the whole main
  text but not verified for every individual sub-genus entry in the TOC listing
  (section C.5 above) — those are "cannot independently verify to the page" though
  internally consistent with confirmed anchors on either side.
- The genus/species pages given for `angelini_jaekel_1899`, `atavus_jaekel_1899`,
  `interruptus_jaekel_1899`, and `reticulatus_jaekel_1899` are given as page *ranges*
  for their family/section rather than exact single pages — the "n. sp." line itself
  was located and quoted-attribution-checked via the register (`JKL.` = Jaekel), but
  the precise printed page of each diagnosis was not individually re-derived from the
  offset formula; treat as "cannot verify to the exact page" (rank and genus placement
  are solid; page precision is not).
- Whether `scoliocystinae` in `taxa.yaml` reflects a real subfamily this reviewer
  missed (rather than a conflation with Fam. Scoliocystidae) cannot be fully ruled
  out — grep found no "Scoliocystinae" spelling anywhere in the OCR text, but an OCR
  drop of an entire word is possible, if unlikely given how many other subfamily
  names of similar form (Apiocystinae, Staurocystinae, Callocystinae, Glyptocystinae)
  were found cleanly.
- The Bather 1898 vs. Jaekel 1899 authorship of *Dinocystis* could not be resolved
  from this text alone (see (b) above) — needs a look at Bather 1898 directly.
- Errata leaf (facing page 1, listed in the TOC) lists several author-flagged
  corrections to pages 10, 93, 97, 148, 151, 153, 166, 167, 168 — none intersect the
  Thecoidea section or the taxa checked above, but worth knowing it exists if those
  later pages are ever entered.
