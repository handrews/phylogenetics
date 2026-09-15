# Review: 1895 Haeckel, "Die cambrische Stammgruppe der Echinodermen"

No source record and no tree file exist for this paper (confirmed: `grep -n
"1895_haeckel" data/sources.yaml data/publications.yaml` returns nothing).
Per the brief, this is a "what it prints" summary on the letters given, not
the full coverage/correctness/source-record template.

**Title-page / running-head check.** The scan opens with six unpaginated
leaves (PDF index 0–6): a HathiTrust rights page, a garbled cover-label OCR
("Haekel, 6.- Die cambrische stammgruppe der echinodermen. (1896)."), and a
Harvard MCZ ownership stamp (Alpheus Hyatt Library, accession "18,079",
dated "September 20, 1962"). Index 7 opens the article proper and confirms
it as the assigned work: "E. Haeckel. Die cambrische Stammgruppe der
Echinodermen. Vorläufige Mittheilung von Ernst Haeckel, Jena." Not a
different Haeckel paper.

**Page mapping.** The article carries its own running-head pagination 1–12.
Running heads read cleanly at every page: index 8→"2", index 9→"...3",
index 10→"4", index 11→"...5", index 12→"6", index 13→"...7", index 14→"8",
index 15→"...9", index 16→"10", index 17→"...11", index 18→"12" (this last
one under a shortened running head, "E. Haeckel, Die Stammgruppe der
Echinodermen."). So **printed page = PDF page index − 6**, for indices
7–18 (page 1 itself, index 7, carries no visible running-head numeral —
it is the article's own title/opening page). Indices 19–20 are the back
flyleaf and cover, outside the sequence.

**Reconstruction note.** The source `.txt` tokenizes the scan roughly one
word or mark per line (a PDF-extraction artifact, not the printed layout).
Quotations below are reassembled into continuous prose, rejoining
line-wrap hyphens and keeping only hyphens that form genuine printed
compounds (e.g. "Ambulacral-Felder"). Where a hyphen's status is unclear
this is flagged inline.

## (a) Front matter for a source record

- **Journal**: Jenaische Zeitschrift für Naturwissenschaft — printed on
  index 7 as "Sm Abdruck aus der Jenaischen Zeitschrift für
  Naturwissenschaft." ("Sm Abdruck" is almost certainly an OCR corruption
  of "Separat-Abdruck" or "Sonder-Abdruck", i.e. this scan is an offprint —
  **cannot verify** the exact German word).
- **Volume**: "Bd. XXX. N. F. XXIII." — Band 30, Neue Folge (new series)
  Band 23.
- **Pages**: the article's own running pagination is 1–12. Nothing on the
  scan states whether 1–12 is a separate offprint pagination or the
  article's actual position at the front of the journal volume/fascicle —
  **cannot verify** without the bound volume.
- **Year**: two different, non-identical dates are printed:
  - The article text is dated twice at the end: read/presented "Vorgetragen
    in der Sitzung der Medicinisch-Naturwissenschaftlichen Gesellschaft zu
    Jena am 13. December 1895" (p. 1, under the title), and signed "Jena,
    am 15. December 1895." (p. 11, closing line).
  - The cover-leaf OCR (index 1) and the HathiTrust catalog metadata
    (index 0, "[Jena, 1896].") both give **1896**. The square brackets in
    the catalog line are a library-cataloging convention for a date
    *supplied by the cataloger*, not necessarily printed on the item
    itself — **cannot verify** whether "1896" appears anywhere on the
    physical offprint's own wrapper, or is inferred by the library from the
    journal volume's publication year.
  - Net: the paper is internally dated December 1895 throughout its own
    text; the wrapper/catalog date is 1896. Both should probably be
    recorded (`pubDate` vs. a `read`/presented date), matching this
    project's own key convention that source keys carry publication year,
    not a reading date (roadmap ground rule, A11) — here that convention
    would need a decision about which year the key should reflect, since
    reading and printing straddle the year boundary.
- **Author**: Ernst Haeckel, Jena (title block, p. 1).
- Note also (p. 1): the paper explicitly promises fuller treatment "im
  Jahre 1896" in "den zweiten Theil meiner „Systematischen Phylogenie"" —
  Haeckel's own multi-volume *Systematische Phylogenie* series, not
  necessarily the same 1896 work already reviewed (`1896_haeckel`, the
  Gegenbaur-Festschrift "Amphorideen und Cystoideen" chapter). **Cannot
  verify from this text alone** whether the two are the same publication or
  Haeckel simply delivered the promised material in a different venue.

## (b) The classification printed

Rank words as printed: **Classe** (also once "Stammklasse", p. 2 — see
(h)), **Familie**, **Genus**/**Genera** (also "Gattung"/"Gattungen" in
running prose), and, only in the closing diagram (p. 12), **Cladoma**.
No family is further split into subfamilies in this paper (that begins in
`1896_haeckel`).

- Classe: **Amphoridea** ("Urnensterne") — new here, p. 2
  - Familie: Archaeocystida (oder Protamphorida) — p. 4
    - Genus (hypothetical): Archaeocystis
    - Genus (hypothetical): Pentactaea
    - Genus (hypothetical): Protamphora
    - Genus (hypothetical): Palamphora
    - Genus (hypothetical): Stephanocystis (p. 4) / Stephanamphora (p. 5) — see (h)
  - Familie: Aristocystida (oder Caryocystida) — p. 5
    - Genus: Aristocystis, Deutocystis, Orocystis, Holocystis, Caryocystis, Dendrocystis
  - Familie: Palaeocystida (— oder Echinosphaerida sensu restricto! —) — p. 5
    - Genus: Echinosphaera, Arachnocystis, Palaeocystis, Comarocystis
  - Familie: Anomocystida (oder Pleurocystida) — p. 6
    - Genus: Trochocystis, Mitrocystis, Pleurocystis, Anomocystis, Atelocystis
- Classe: **Cystoidea** ("echte Cystoideen") — six families, p. 7–10
  - Familie: Pomocystida (= Sphaeronitida p. p.) — p. 9 — Genus: Sphaeronites, Pomocystis, Eucystis, Proteocystis
  - Familie: Fungocystida (oder Glyptosphaerida) — p. 9 — Genus: Glyptosphaera, Protocrinus, Fungocystis, Malocystis
  - Familie: Agelacystida (oder Agelacrinida) — p. 9 — Genus: Agelacrinus, Agelacystis, Hemicystis, Gomphocystis, Astroblastus, Mesites
  - Familie: Callocystida (oder Apiocystida) — p. 9 — Genus: Callocystis, Apiocystis, Sphaerocystis, Pseudocrinus, Lepadocrinus
  - Familie: Glyptocystida (oder Caryocrinida p. p.) — p. 10 — Genus: Sycocystis (= Echinencrinus), Pyrocystis, Glyptocystis (= Chirocrinus), Mimocystis, Homocystis
  - Familie: Ascocystida (oder Ascothuria) — p. 10 — Genus: Ascocystis, Thuriocystis, Acanthocystis (Macrocystella?)
- Higher-level scheme, prose (p. 10–11) plus a closing diagram, "Phylogenetische Beziehungen der acht Echinodermen-Classen" (p. 12):
  - I. Cladoma: **Monorchonia** (oder „Anactinogonidiata") — one gonad pair, no Paraxon-Drüse, no genital ring-sinus
    - Classen: Amphoridea, Holothurea, Cystoidea
  - II. Cladoma: **Pentorchonia** (oder „Actinogonidiata") — five gonad pairs, with Paraxon-Drüse and genital ring-sinus
    - IIA. **Orocincta** (= Pelmatozoa) — genital blood-sinus circoral, gonad stems perradial — Classen: Blastoidea, Crinoidea
    - IIB. **Pygocincta** (= Echinozoa) — genital blood-sinus periproctal, gonad stems interradial — Classen: Echinidea, Ophiurea, Asteridea

The p. 12 diagram itself is a figure (a branching tree with the eight
class names at the head and the Cladoma/Orocincta/Pygocincta boxes below),
which the text extraction has flattened into a sequential list with no
lines. The nesting above is reconstructed by matching the diagram's own
numbered list ("1. Amphoridea. 2. Holothurea. 3. Cystoidea. 4. Blastoidea.
5. Crinoidea. 6. Echinidea. 7. Ophiurea. 8. Asteridea.") against the
identical grouping given in prose at p. 10–11 (para. 30–32); the two agree,
so the reconstruction is treated as reliable even though the figure's own
graphical layout cannot be recovered from this scan.

## (c) Names proposed as new

No name in this paper carries a formal "n.", "nov." or "m." tag anywhere —
novelty is marked only by a first-person proposing verb (*vorschlage*,
*könnten … unterscheiden*, *zusammenfassen*) or, for the two Cystoidea-only
higher terms, by bare assertion in prose with no verb at all.

| name | rank | proposing sentence (printed) | page | novelty marker |
|---|---|---|---|---|
| **Amphoridea** | Classe | "…sie sind von diesen letzteren als besondere Classe abzutrennen, für welche ich wegen der urnenähnlichen Gestalt ihrer Panzerkapsel die Bezeichnung Amphoridea vorschlage (,,Urnensterne")." | 2 | verb "vorschlage" ("I propose"); no tag |
| **Archaeocystida, Aristocystida, Palaeocystida, Anomocystida** (as a set) | Familie (4, of Amphoridea) | "Die verschiedenen Genera der Amphorideen lassen sich auf vier Familien vertheilen: 1) Archaeocystida, 2) Aristocystida, 3) Palaeocystida und 4) Anomocystida." | 2 | no verb, no tag — stated as a division |
| **Protamphorida, Caryocystida, Echinosphaerida (sensu restricto), Pleurocystida** | alternate Familie names | given in parentheses at each of the four family headings, "(oder Protamphorida)" p. 4, "(oder Caryocystida)" p. 5, "(— oder Echinosphaerida sensu restricto! —)" p. 5, "(oder Pleurocystida)" p. 6 | 4–6 | no verb, no tag — alternate name offered alongside the primary one |
| **Archaeocystis, Pentactaea, Protamphora, Palamphora, Stephanocystis/Stephanamphora** | Genus (hypothetical, of Archaeocystida) | short form: "Hypothetische Genera: Archaeocystis. Pentactaea. Protamphora. Palamphora. Stephanocystis." (p. 4); elaborated: "Wir könnten als hypothetische Gattungen unterscheiden: Archaeocystis mit 3 Tentakeln (wie Arachnocystis unter den Palaeocystiden); Pentactaea mit 5 Tentakeln; Protamphora mit 15 Tentakeln; Palamphora mit 25 Tentakeln; Stephanamphora mit einem Kranze von zahlreichen Tentakeln (ähnlich Loxosoma oder einem anderen einfachen Bryozoon)." | 4–5 | verb "könnten … unterscheiden" ("we could distinguish"), explicitly hedged as hypothetical; no tag. Note: *Pentactaea* itself is not new here — see (e). |
| **Pomocystida, Fungocystida, Agelacystida, Callocystida, Glyptocystida, Ascocystida** (as a set) | Familie (6, of Cystoidea) | introduced by "…dient uns in erster Linie zur Unterscheidung von sechs Familien der echten Cystoidea" (p. 7), then given individually as formal headings pp. 9–10 | 7, 9–10 | no verb at the individual headings, no tag |
| **Sphaeronitida (p. p.), Glyptosphaerida, Agelacrinida, Apiocystida, Caryocrinida (p. p.), Ascothuria** | alternate Familie names for the six above | given in parentheses at each heading, pp. 9–10 | 9–10 | no verb, no tag |
| **Monorchonia** (oder „Anactinogonidiata") | Classen-group ("Begriff") | "Wir können daher diese drei Classen unter dem Begriffe der Monorchonia zusammenfassen (oder „Anactinogonidiata")." | 11 | verb "zusammenfassen" ("we can group together"); no tag |
| **Pentorchonia** (oder „Actinogonidiata") | Classen-group | "…sie stehen jenen als Pentorchonia gegenüber (oder „Actinogonidiata")." | 11 | no verb — stated in opposition to Monorchonia; no tag |
| **Cladoma**/Cladomen (as a rank word, glossed = Hauptclasse) | rank | "Die Gruppe der Pentorchonien setzt sich nach meiner Ansicht aus zwei verschiedenen Cladomen oder Hauptclassen zusammen…" | 11 | phrase "nach meiner Ansicht" ("in my view"); no tag |
| **Orocincta**, **Pygocincta** | Cladoma-subgroup | "Die Pelmatozoa (Blastoidea und Crinoidea) sind Orocincta; … Die Echinozoa hingegen (Echinidea, Ophiurea und Asteridea) sind Pygocincta;" | 11 | bare assertion, no verb, no tag |

Two names used in this passage — **Pelmatozoa** and **Echinozoa** — are
*not* claimed as new by any verb or marker; they are simply invoked
("den Pelmatozoen und Echinozoen", p. 11) as if already available terms,
so they are treated here as pre-existing rather than proposed (consistent
with Pelmatozoa's known prior currency; **cannot verify** Echinozoa's
status from this text alone, since no citation accompanies either word).

## (d) Names Haeckel 1896 attributes to 1895 — checked against this paper

`review_1896_haeckel.md` §(a)/(b) records six family-rank names (plus the
class Amphoridea) that the 1896 paper cites to this 1895 paper by number
("50, p. n"). All six check out:

| name (1896's citation) | printed here? | page here | spelling here | verdict |
|---|---|---|---|---|
| Amphoridea, "50, p. 2" | yes | 2 | Amphoridea | confirmed, exact page |
| Eocystida's components (Archaeocystida + Protamphorida) | yes | 4 | "Archaeocystida (oder Protamphorida)" | confirmed — both names appear together exactly as 1896 describes the merge |
| Aristocystida, "50, pag. 5" | yes | 5 | Aristocystida | confirmed, exact page |
| Palaeocystida | yes | 5 | Palaeocystida | present (1896 gives no 1895 page for it to check) |
| Pomocystida | yes | 9 | Pomocystida | present |
| Fungocystida | yes | 9 | Fungocystida | present |
| Agelacystida (= Agelacrinida) | yes | 9 | "Agelacystida (oder Agelacrinida)" | present |
| Ascocystida | yes | 10 | Ascocystida | present |
| Glyptocystida | yes | 10 | Glyptocystida | present |

Not cited to 1895 by the 1896 paper, and correctly absent here (checked by
full-text search, 0 hits each): **Callocystida** (1896 credits Bernard
1895, a different author, not this paper), **Anomocystida** (1896 credits
Woodward 1880 priority, though Haeckel notes he used the same spelling
himself in 1895 — and indeed "Anomocystida" is the fourth Amphoridea family
name here, p. 6, so the 1896 synonymy's inclusion of "Anomocystida, E.
HAECKEL, 1895" is confirmed against this paper too), and the three 1896
Anomocystida subfamilies **Placocystida**, **Atelocystida**,
**Pleurocystida** (subfamily rank; "Pleurocystida" here, p. 6, is only the
*alternate name for the family* Anomocystida, not a subfamily — a
different taxon at a different rank sharing the same string).

## (e) Names taken from other authors

This is a short "Vorläufige Mittheilung" (preliminary communication) with
no synonymy apparatus; it contains only one substantive citation to
someone else's work, and it does not name the author in running text:

> "…entspricht nach meiner Überzeugung derjenigen, welche 1888 von dem
> scharfsinnigen Begründer der Pentactaea-Theorie in seiner Abhandlung über
> „Die Entwickelung der Synapta digitata und die Stammesgeschichte der
> Echinodermen" mit Hülfe des biogenetischen Grundgesetzes klar definirt
> worden ist (vergl. Bd. XXII dieser Zeitschrift)." (p. 2)

The cited author is described only by role ("der scharfsinnige Begründer
der Pentactaea-Theorie", "the ingenious founder of the Pentactaea theory")
and by his paper's title and its location (Bd. XXII of the same journal);
his name is never printed in this article. The genus **Pentactaea** itself
(used at p. 4–5 among the "hypothetical genera") is accordingly an existing
name borrowed from that unnamed author's 1888 theory, not new here — the
one clear case of external attribution in the paper, and it is anonymous
on the page. **Cannot verify** the author's identity from this text alone.

No other genus, family or class name in the paper carries an "AUTHOR, year"
citation; all the pre-existing genera used to populate the family lists
(Aristocystis, Deutocystis, Orocystis, Holocystis, Caryocystis, Dendrocystis,
Echinosphaera, Arachnocystis, Palaeocystis, Comarocystis, Trochocystis,
Mitrocystis, Pleurocystis, Anomocystis, Atelocystis, Sphaeronites,
Pomocystis, Eucystis, Proteocystis, Glyptosphaera, Protocrinus, Fungocystis,
Malocystis, Agelacrinus, Agelacystis, Hemicystis, Gomphocystis, Astroblastus,
Mesites, Callocystis, Apiocystis, Sphaerocystis, Pseudocrinus, Lepadocrinus,
Sycocystis, Echinencrinus, Pyrocystis, Glyptocystis, Chirocrinus, Mimocystis,
Homocystis, Ascocystis, Thuriocystis, Acanthocystis, Macrocystella,
Hemicosmites, Glyptosphaera) are simply listed by name with no author
credited on the page.

## (f) Edrioasteroids and the "gold slice" cystoids

No edrioasteroid-specific name occurs anywhere in this paper (checked by
full-text search, 0 hits each): **Edrioaster, Edriocystis, Cyclaster,
Cyclocystoides, Stromatocystites, Thyroidea, Pyrgocystis**. The word
**Metazoen** occurs once, in passing, on p. 1 ("einen abgeschlossenen
selbständigen Stamm der Metazoen") — an existing higher-taxon term used to
place Echinodermata, not proposed here and unrelated to the 1874
`metazoa`/`metazoa-grade` `taxa.yaml` records (see (g)).

The genera that later (in `1896_haeckel`) become the edrioasteroid-relevant
subfamilies Hemicystida/Asterocystida/Edriocystida are already present here,
undivided, as the flat genus list of the third Cystoidea family:

> "26. Dritte Familie: Agelacystida (oder Agelacrinida). Genera:
> Agelacrinus, Agelacystis, Hemicystis, Gomphocystis, Astroblastus,
> Mesites." (p. 9)

No subfamily split, no separate class, and no comment distinguishing these
six genera from the rest of Cystoidea beyond the family's own general
character paragraph. The finer subdivision, and the genus *Edriocystis*
itself, are entirely absent — they are 1896 additions.

## (g) The eight `taxa.yaml` records with `auth: [haeckel]`

`grep -n "haeckel" data/taxa.yaml` (case-sensitive lowercase) returns nine
records; one of them, `collaspidae`, is `altSpellingOf: collaspididae` and
so borrows its authority per this project's own convention (ground rules:
"`altSpellingOf`… = derivative records that borrow authority") rather than
carrying an independent claim — leaving eight primary records. (A tenth
hit, `agelacystis`, has `auth: [Haeckel]` capitalized and `year: 1895`; it
is not one of the eight but is a useful control — see below.)

| key | recorded rank/year | in this 1895 paper? | verdict |
|---|---|---|---|
| `amphorida` (Order, 1896) | name "Amphorida", rank Order, year 1896 | **yes** — but printed here as **Amphoridea** (with the final "-ea"), rank **Classe**, on **p. 2**, in **1895** | this 1895 paper is the true source, not 1896; name, rank and year in the record all disagree with the print. Matches and confirms the B18-style discrepancy the 1896 review already flagged (there working only from Haeckel's 1896 self-citation; now confirmed directly against the primary 1895 text) |
| `collaspididae` (Family, 1889) | 1889 | no — 0 hits for "Collaspid" | not this paper; year already points elsewhere |
| `edriocystis` (1896) | 1896 | no — 0 hits | not this paper; consistent with the 1896 review's finding that it is new in 1896 |
| `hemicystis` (1896) | 1896 | genus name appears, **p. 9**, in the Agelacystida genus list, with no attribution at all (see (e)) | this paper uses the name but claims no authorship of it; per the 1896 review, the name's real author is Hall 1852 — so neither 1895 nor 1896 is the true origin, and the `taxa.yaml` `haeckel` attribution appears to be wrong regardless of which Haeckel paper is meant |
| `metazoa` (Subkingdom, 1874) | 1874 | word "Metazoen" appears once, **p. 1**, as pre-existing usage (see (f)) | not this paper; unrelated to its 1874 coinage elsewhere |
| `metazoa-grade` (Grade, 1874) | 1874 | same single p. 1 usage | not this paper |
| `placocystida` (Suborder, 1896) | 1896 | no — 0 hits for "Placocystid" | not this paper; consistent with the 1896 review (new subfamily there, p. 37) |
| `staurocystis` (1896) | 1896 | no — 0 hits | not this paper; consistent with the 1896 review (new genus there, p. 134) |

Control: `agelacystis` (`auth: [Haeckel]`, `year: 1895`, not one of the
eight) is exactly right against this paper — "Agelacystis" appears at p. 9
in the Agelacystida genus list, and the 1896 review already noted it is
"retained from 1895, not new" there. This is the one Haeckel-genus record
in the corpus whose 1895 attribution is already correct.

**Net: of the eight, only `amphorida` genuinely originates in this 1895
paper — and even that record misstates the name, rank and year.** The other
seven either belong to `1896_haeckel` (five confirmed absent here), belong
to an unrelated 1874 Haeckel work (`metazoa`/`metazoa-grade`), or — for
`hemicystis` — appear to be misattributed to Haeckel at all.

## (h) Uncertainties

- **Typeface/OCR reliability, overall good.** Unlike the heavily
  Fraktur-garbled `1896_haeckel` scan, this article's running prose OCRs
  cleanly and consistently, including umlauts (ü, ö) and ß; genus names,
  the author's own name, and page-running heads all come through without
  the systematic corruption seen in the 1896 scan. This is consistent with
  the body text being set in Antiqua/Roman type rather than Fraktur, though
  this cannot be confirmed without the original page images (**cannot
  verify**).
- **Genuinely garbled patches** (not systematic, isolated to particular
  spots): the offprint notice "Sm Abdruck aus der Jenaischen Zeitschrift"
  (almost certainly "Separat-Abdruck" or "Sonder-Abdruck", p. [front matter]
  — **cannot verify** the exact word); an ownership/dedication block on the
  same leaf ("cllr. Alphear Hyatt (Cambridge) hochoikhysvall") that does
  not resolve into legible German or English — **cannot verify**; one
  Cladoma-diagram OCR ("II . Cladoma : Pentorchonia" with an odd space
  before the colon, and "II B. Pygocincta" with a stray space in "II B"),
  treated as the same headings as "I. Cladoma" and "IIA. Orocincta" since
  the pattern is otherwise consistent.
- **A real printed inconsistency, not obviously OCR**: the fifth
  "hypothetical genus" of Archaeocystida is spelled **Stephanocystis** in
  the short list (p. 4) and **Stephanamphora** in the elaborated sentence
  giving its tentacle count (p. 5) — two visually dissimilar words, unlikely
  to be a simple OCR misread of one for the other. **Cannot verify** which
  (if either) is the compositor's error versus Haeckel's own inconsistency;
  "Stephanamphora" matches the "-amphora" pattern of its family-mates
  Protamphora/Palamphora, which may or may not bear on which is original.
- **c/k spelling of "Classe"/"Klasse".** The rank word is spelled with "C"
  everywhere except one instance, "Stammklasse" (p. 2), against "Classe" /
  "Stammclasse" elsewhere on the same and other pages. **Cannot verify**
  whether this is a genuine period-typical orthographic wobble or an OCR
  misread of "c" as "k".
- **A dropped parenthesis.** The Aristocystida genus line reads "Genera:
  Aristocystis, Deutocystis, Orocystis, Holocystis, Caryocystis,
  Dendrocystis)." — a closing parenthesis with no opening one, the only
  such case among the four Amphoridea family genus-lists (the other three
  have no parentheses at all). **Cannot verify** whether an opening "("
  before "Aristocystis" was dropped by OCR or never printed.
- **The 1896-vs-1895 publication date**, and whether "1896" is printed on
  the physical offprint or supplied by the library catalog — see (a).
  **Cannot verify** from this scan.
- **The anonymous "Begründer der Pentactaea-Theorie"** — his name is never
  printed in this article; identifying him requires the 1888 paper itself
  or an external bibliography, not this text. **Cannot verify** from this
  source alone.
