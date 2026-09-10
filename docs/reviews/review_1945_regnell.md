# Review: Regnéll, G. (1945), *Non-Crinoid Pelmatozoa from the Paleozoic of Sweden*

No `1945_regnell` source record exists in `data/sources.yaml` and no tree file exists in
`data/trees/`. Confirmed by: `grep -n "1945" data/sources.yaml` returns only an incidental
in-text citation "(Bather 1915; Richter 1930; Hecker 1939; Regnéll 1945)" inside another
source's notes, not a top-level block; `ls data/trees/ | grep -i 1945` returns nothing;
`grep -ril regnell data/` returns only `data/taxa.yaml` and two unrelated tree files
(`1982c_parsley.yaml`, `1968b_paul.c.r.c.yaml`) that cite Regnéll 1945 as an *external*
authority for taxa they themselves originate (e.g. `paracrinoidea` class, `lovenicystis`
genus, several species epithets `..._regnéll_1945`). This is scope history (no contradiction):
this paper has simply never been entered as its own source. Proceeding per the "no
tree/no source record" branch — classification, citations, and acts only, no coverage or
correctness tables.

## Page-index → printed-page mapping

Two pagination sequences, no resets within the read ranges:

| PDF index range | Printed pagination | Content |
|---|---|---|
| 2–9 | Roman **I–VIII** (partial; idx4=III, 5=IV, 6=V, 7=VI, 8=VII, 9=VIII) | Title, Contents, Preface |
| 10–264 | Arabic **1–255**, formula `printed = PDF index − 9` | Main text through Explanation of Plates |
| 265–280 | unnumbered | 15 plates of figures |
| 281 | unnumbered | price notice only |

Verified against the printed running heads at every read boundary (e.g. PDF idx 23 header-free
but content = printed "14", matching the Contents entry "Classification of the Pelmatozoa …
14"; PDF idx 206 = printed "197" matching "Class Edrioasteroidea … 197" is not itself in the
Contents but is corroborated by idx205="196" and idx207="198"). All page numbers below are
**printed pages**, formula `printed = PDF index − 9` for indices ≥10.

Ranges actually read: printed pp. III–VIII (Contents/Preface, idx4–9); pp. 1–24 (Historical
Survey + start of Classification chapter, idx10–33, covering the requested 16–31 plus
boundary buffer); pp. 27–31 (Subclass Hydrophoridea/Blastoidea classification, idx36–41,
covering the requested single marker "37"); pp. 41–50 (Class Carpoidea tail, Class
Edrioasteroidea, Incertae sedis: Cyclocystoidea, [Machaeridia], covering the requested
51–58); pp. 59–61 (Orientation of the theca, covering the requested "69"); pp. 196–223
(Class Edrioasteroidea systematic treatment through Cyclocystoides insularis, covering the
requested 206–223, extended to 223 to close a description that runs to its natural end);
pp. 223–239 (Literature, covering the requested 233–238); pp. 235–255 (Literature tail,
Index of Genera and Species, Explanation of Plates, Addendum, covering the requested
244–254, extended to the addendum at p. 255 to close the section).

---

## (a) The paper's own classification

### A1. Overview classification (p. 14, "Classification of the Pelmatozoa")

Printed exactly as a nested list; ranks, names, and authorities as printed (OCR "RATHER"
throughout this text is corrected here to **BATHER** — see Uncertainties):

| Rank | Name | Authority as printed | Page |
|---|---|---|---|
| Subphylum | Pelmatozoa | LEUCKART 1848 | 14 |
| Class | Eocrinoidea | JAEKEL 1918¹ | 14 |
| Class | Paracrinoidea | **nov.** (Regnéll's own new class) | 14 |
| Class | Cystoidea | BUCH 1846, emend. JAEKEL 1918 | 14 |
| — Subclass | Hydrophoridea | ZITTEL 1903 [= Cystoidea auctorum] | 14 |
| — — Order | Rhombifera | ZITTEL 1879, emend. BATHER 1899 [= Dichoporita JAEKEL 1899] | 14 |
| — — Order | Diploporita | J. MÜLLER 1854, emend. BATHER 1906 | 14 |
| — Subclass | Blastoidea | SAY 1825 | 14 |
| — — Order | Parablastoidea | HUDSON 1907 [= Protoblastoidea BATHER 1899, ex parte] | 14 |
| — — Order | Coronata | JAEKEL 1918 | 14 |
| — — Order | Eublastoidea | BATHER 1899 [= Radiolata JAEKEL 1918; Blastoidea auctorum] | 14 |
| Class | Crinoidea | J. S. MILLER 1821 | 14 |
| Class | Carpoidea | JAEKEL 1900, emend. JAEKEL 1918 [= Carpoidea Heterostelea JAEKEL 1900] | 14 |
| Class | Edrioasteroidea | BILLINGS 1858 (1854), emend. BATHER 1899 [= Thecoidea JAEKEL 1895] | 14 |
| Incertae sedis | Cyclocystoidea | MILLER & GURLEY 1895 | 14 |

¹ Footnote on p. 14: "In his paper of 1918 (p. 24) JAEKEL gave 1899 as the year of publication
for the term Eocrinoidea. This is not correct, however, since the term was not defined and
not even mentioned in JAEKEL's memoir of 1899." — Regnéll corrects Jaekel's own self-citation.

No Eocrinoidea family/genus detail falls in the read ranges (the systematic chapter for
Eocrinoidea sits at printed p. 67, PDF idx 76, outside the assignment). The substantive
diagnosis/discussion of the new Class Paracrinoidea sits at printed p. 37 (PDF idx 46), also
outside the assignment — only the classification-list act itself (p. 14) was read.
"Edrioblastoidea" does not appear anywhere in the read ranges; not a term this paper uses.

### A2. Class Edrioasteroidea — classification-chapter treatment (pp. 43–44)

| Rank | Name | Authority as printed | Page |
|---|---|---|---|
| Class | Edrioasteroidea | (as A1) | 43 |
| — (no orders erected) | — | "No attempt has been made … to group the families into orders." | 44 |
| Incertae sedis | Cyclocystoidea | MILLER & GURLEY 1895 | 44 |
| [bracketed, doubtfully Pelmatozoa at all] | [Machaeridia] | WITHERS 1926 | 47–49 |

Range given for the class: "Lower Cambrian–Lower Carboniferous" (p. 44).

### A3. Class Edrioasteroidea — systematic treatment (pp. 197–223)

| Rank | Name | Authority as printed | Page |
|---|---|---|---|
| Class | Edrioasteroidea | BILLINGS 1858 (1854), emend. BATHER 1899 | 197 |
| — (no order-level division) | — | "A dividing into orders was not undertaken by BASSLER 1935 and 1936, nor does the writer think it wise here …" | 198 |
| Family | Stromatocystitidae | BASSLER 1936 | 198 |
| — Genus | *Stromatocystites* | POMPECKJ 1896, emend. SCHUCHERT 1919 | 198 |
| — — Species | *S. balticus* | JAEKEL 1899 (redescribed, not new here) | 198–200 |
| Family | Cyathothecidae | JAEKEL 1927 | 200 |
| — Genus | *Cyathotheca* | JAEKEL 1927 | 200 |
| — — Species | *C. suecica* | JAEKEL 1927 (full redescription, not new here) | 200–203 |
| Family | Hemicystitidae | BASSLER 1936 | 203 |
| — Genus | *Pyrgocystis* | BATHER 1915 [synonym: *Scalpellum* AURIVILLIUS 1892, non LEACH] | 203 |
| — — Species | *P. sulcata* | (AURIVILLIUS 1892) | 205–207 |
| — — Species | *P. procera* | (AURIVILLIUS 1892) | 207–210 |
| — — Species | *P. varia* | (AURIVILLIUS 1892) | 210–212 |
| — — Species | *P. cylindrica* | (AURIVILLIUS 1892) | 212–214 |
| Incertae sedis / Order | Cyclocystoidea | MILLER & GURLEY 1895 | 215 |
| — Family | Cyclocystoididae | S. A. MILLER 1882 | 215 |
| — — Genus | *Cyclocystoides* | SALTER & BILLINGS 1858 | 215 |
| — — — Species | *C. lindströmi* | **n. sp.** (Regnéll) | 216–219 |
| — — — Species | *C. insularis* | **n. sp.** (Regnéll) | 220–223 |

No genus of Family Cyathothecidae besides *Cyathotheca* is treated in the Swedish fauna
(*Cyathocystis* F. SCHMIDT 1879 is named as the family's other included genus, p. 200, but
not itself described — no Swedish material).

---

## (b) Every earlier work cited for edrioasteroid taxa (the main deliverable)

Grouped by cited author/year; page(s) are where Regnéll makes the attribution.

### B1. Status of the Class Edrioasteroidea (historical-opinion citations)

| Author, year | What Regnéll attributes to it | Page(s) |
|---|---|---|
| JAEKEL 1895 (p. 110) | Defined "Thecoidea" as a separate division of the Pelmatozoa — the origin of treating edrioasteroids as class-rank | 43 |
| JAEKEL 1899, 1918 | Classified Edrioasteroidea as a class, under the name Thecoidea | 43 |
| BATHER 1899, 1900, 1929 a | Classified Edrioasteroidea as a class | 43, 197 |
| MACBRIDE 1906 | Classified Edrioasteroidea as a class; also (p. 596) argued Edrioasteroidea became extinct without giving rise to descendants | 43–44 |
| BASSLER 1935, 1936 | Classified Edrioasteroidea as a class | 43 |
| BASSLER 1938 | By contrast, ranked Edrioasteroidea as an *order* of class Cystoidea in his index — inconsistent with his own 1935/1936 usage | 43 |
| ZITTEL-BROILI 1924; SPRINGER 1913 | Also ranked Edrioasteroidea as an order of class Cystoidea (textbook examples) | 43 |
| ABEL 1920 (p. 282) | Made Crinoidea, Cystoidea, Carpoidea, and "Thecoidea" subclasses of class Pelmatozoa; also argued (with MacBride) against edrioasteroid ancestry of Eleutherozoa | 43–44 |
| HAECKEL 1896 | Classified the "Agelacystida" as a family of his class Cystoidea — called by Regnéll "in essential respects very unsuccessful" | 43 |
| MATSUMOTO 1929 (p. 31 for a related point) | New three-subphylum classification of Echinodermata (Crinozoa, Echinozoa, Asterozoa); listed Edrioasteroidea as a class of subphylum Asterozoa | 43 |
| MACBRIDE & SPENCER 1938 (p. 134) | Held out the prospect of an account of "various forms (including the Edrioasteroidea) allied to the cystids" — not yet published as far as Regnéll knew | 43–44 |
| GISLEN 1934 (p. 4) | Opposing view to MacBride/Abel: Eleutherozoa derived from primitive forms with the ambulacral surface already directed upward | 44 |
| BILLINGS 1858 (1854) | Class-name authority. Billings 1854 "only called attention to the great difference" between these forms and typical cystideans (per Springer's account, below); 1858b (p. 85) suggested arranging them as a suborder "Edrioasteridae" | 197–198 |
| SPRINGER 1913 (p. 158) | Reports what Billings actually said in 1854 and 1858, used by Regnéll to correct Bassler's citation (below) | 197–198 |
| HUXLEY 1877 | Named (via a Bather citation Regnéll reproduces) as an early user of the term "Edrioasteroidea" | 198 |
| BASSLER 1935 (p. 2), 1936 (p. 2) | Cited as writing "BILLINGS, 1854–58" for the class-name date — Regnéll states this is **"not correct"**, tracing the error to a misreading of Bather's bracketed reference list | 198 |
| BATHER 1900 (p. 205) | Cited for the class's synonym list | 197 |
| BASSLER 1935 (p. 2) | Cited (with Bather 1900) for the class's synonym list | 197 |
| FOERSTE 1914 (p. 432) | Described branched ambulacra in *Thresherodiscus*, requiring existing diagnoses of the class to be modified to drop the demand for unbranched ambulacra | 198 |
| RICHTER 1943 (pp. 370–371) | On the nomenclatural type concept, cited re: whether a gutta-percha cast can be a holotype (bears on *Stromatocystites balticus*, below) | 198 |
| BASSLER (1935, 1936) [Bibliographic index/Classification of the Edrioasteroidea 1935] | Named directly in the historical survey: "the taxonomist owes a good deal of gratitude to BASSLER for his 'Bibliographic index' (1915) … his 'Classification of the Edrioasteroidea' (1935) …" | 13 |
| BASSLER 1935, 1936 (orientation system) | Adopted Jaekel's radius-lettering system for Edrioasteroidea too, but "used … Arabian figures" instead of Jaekel's Roman numerals | 60 |

### B2. Loven's unpublished plates — earlier attributions reproduced from the plate captions (pp. 7–8)

| Author, year | What is attributed | Page(s) |
|---|---|---|
| FORBES [n.d., pre-1899] | *Edrioaster buchianus* (FORBES) figured on Loven's unpublished Pl. 15, after Museum of Practical Geology, London specimens | 8 |
| F. ROEMER [n.d.] | *Hemicystites bohemicus* (F. ROEMER) figured on Loven's unpublished Pl. 16, after Berlin/Prague specimens, annotated "Lithogr. 1891" | 8 |
| — | Loven's plates listed two genera of Edrioasteroidea overall: *Edrioaster* (Great Britain) and *Hemicystites* (Bohemia) | 8 |

### B3. *Pyrgocystis* — establishment and revision, cited in the historical survey (pp. 9, 203–204)

| Author, year | What Regnéll attributes to it | Page(s) |
|---|---|---|
| AURIVILLIUS 1892 | Published the original Swedish material, as seven species of "cirripeds" under *Scalpellum* | 9, 203 |
| BATHER 1915 a | Removed those seven "Scalpellum" species from the cirripeds and placed them in the new genus *Pyrgocystis* (Edrioasteroidea), established by himself; reduced the species count to three; performed the definitive morphological study (adoral surface material) that first made the genus's organization understood | 9, 203–204 |

### B4. Cyclocystoidea — classification-history citations (pp. 44–47)

| Author, year | What Regnéll attributes to it | Page(s) |
|---|---|---|
| BEGG 1934 (p. 223) | Interpretation: lower plate carries all essential organs, covered by an upper ("dorsal") plate; radial ducts run between the plates from the submarginal canal to a supposed central mouth | 44 |
| RAYMOND 1913 (pp. 30–31) | Stated "no echinoderm is known in which the food groove is not radial … and does not lead directly to the mouth"; offered two alternative interpretations of *Cyclocystoides* (free cystidean/edrioasteroid, or specialized crinoid root comparable to *Lichenocrinus*) | 44, 46 |
| SIEVERTS[-DORECK], HERTHA 1934 (p. 975) | Reviewing Begg: proposed the lower plate's radial rays correspond to ambulacral grooves of the upper face — a proposal Regnéll finds unconfirmed | 44–45, 223 |
| FOERSTE 1924 (p. 81) | Stated conclusively that "no system of arms … was incorporated in the disk as in *Agelacrinus*, and related genera"; redescribed *C. huronensis* without offering an opinion on affinities | 45, 46 |
| HALL 1872 (p. 219, and figure Pl. 6 fig. 16) | Exception among authors: found *Cyclocystoides* to resemble Echinidae more than Crinoidea/Cystidae/Asteridae; his figure of *C. salteri* shows an eccentric opening later reinterpreted by Bather | 45, 217 |
| GISLEN 1934 (p. 14 seq.) | Cited for the general principle of achieving protection for the ambulacral system by different routes in different pelmatozoans | 45 |
| SALTER & BILLINGS 1858 (p. 90) | Erected the genus, inclined to consider it a cystoid with resemblance to *Pseudocrinites* or the Canadian *Amygdalocystites* [Paracrinoidea] | 45, 215 |
| MILLER & DYER 1878; MILLER 1881; FABER 1886; MILLER & FABER 1892; MILLER & GURLEY 1895 | Described several (partly insufficiently defined) American species of *Cyclocystoides*, without clarifying its classification | 45 |
| MILLER & GURLEY 1895 (p. 61) | Established the order Cyclocystoidea | 46, 215 |
| BATHER 1900 (p. 210) | Suggested *Cyclocystoides* might belong to Edrioasteroidea, though to no recognized family; (p. 211) interpreted an eccentric opening as anus and described "a central pyramid of minute plates (mouth?)" | 45–46, 217 |
| SPRINGER 1913 (p. 159) | Shared the view that *Cyclocystoides* may belong to Edrioasteroidea | 46 |
| FOERSTE 1920 b (p. 35) | Same view | 46 |
| ZITTEL-BROILI 1924 (p. 211) | Same view | 46 |
| BASSLER 1935 (p. 10), 1938 (p. 13) | Same view, placing *Cyclocystoides* with Edrioasteroidea | 46 |
| BEGG 1934 (p. 224) | "Cyclocystoides has its affinities with the Cystidea and may even represent a distinct order of that class" — Regnéll judges Begg's "Cystidea" should be read as "Carpoidea" | 46 |
| MAILLIEUX 1926 (p. 94) | Reported a find of *Cyclocystoides* in the Lower Devonian of Belgium; quoted Bather's private opinion "que l'attribution de *Cyclocystoides* aux Edrioastéroïdes ne pourra pas être maintenue" | 47, 219 |
| BASSLER 1936 (p. 23) | Stated family Cyclocystoididae "must be left at present as an uncertain order of Pelmatozoa" — yet (1938) appended it to his order Edrioasteroidea; Regnéll notes the inconsistency and "cannot but agree" with the 1936 caution | 47 |
| BATHER 1913 (§230 seq.), 1926 (p. 6 seq.) | Interpreted slit-like openings in *Cothurnocystis* as subvective — cited in the footnote on rival interpretations of similar structures | 46 |
| JAEKEL 1918 (p. 115) | Suggested the *Cothurnocystis* pores were outlets for sexual products | 46 |
| GISLEN 1930 (p. 206, p. 212) | Found that improbable; proposed a drainage-organ function instead | 46 |
| SPENCER 1938 (p. 299) | Proposed the slits were "respiratory pouches probably without any communication with the alimentary canal" | 46 |

### B5. *Cyclocystoides* — genus/species-level citations, systematic section (pp. 215–223)

| Author, year | What Regnéll attributes to it | Page(s) |
|---|---|---|
| S. A. MILLER 1882 | Established family Cyclocystoididae | 215 |
| SALTER & BILLINGS 1858 | Established genus *Cyclocystoides*; genotype *C. halli* BILLINGS 1858 (in Salter & Billings) | 215 |
| FOERSTE 1920 b (p. 59 seq., pp. 62–63) | Split off new genera *Narrawayella* and *Savagella* for species not matching typical *Cyclocystoides*; Regnéll doubts *Narrawayella*'s validity | 215, 217 |
| SAVAGE 1917 | Described *Cyclocystoides ornatus*, made genotype of *Savagella* by Foerste | 215 |
| LINDSTRÖM 1888 b (p. 20) | Recorded "*Cyclocystoides* sp." in a faunal list from the Silurian of Gotland, without description — the prior record that Regnéll now names *C. lindströmi* | 216 |
| RAYMOND 1913 (p. 26, p. 28, pp. 30–31, Pl. 3) | Noted vertical striations on ossicles indicate flexible cartilaginous/muscular joints; described covering plates over the mamillary-elevation canal; redescribed/figured *C. huronensis*; claimed to have observed a central plate in a specimen of Foerste's *Narrawayella raymondi* | 217, 219, 223 |
| BEGG 1934 (p. 222, pp. 223–224) | Described a "marginal zone of sinuous threads or possibly of imbricating plates" (not confirmed by Regnéll in the Swedish material); rejected on theoretical grounds a ventral anus location; described *C. decussatus* | 217, 219, 221–222 |
| MILLER & DYER 1878 (pp. 32–35, Pl. 2 figs. 8/8a) | Described several Cincinnati-group species (*C. minus*, *C. parvus*, *C. mundulus*, *C. magnus*, *C. bellulus*); observed ducts penetrating vaults radially | 217, 221–223 |
| FOERSTE 1924 (p. 80, p. 81, Pl. 6 fig. 3) | Redescribed/figured *C. huronensis*; stated covering plates over the canal could be moved for water intake/outlet; earlier (1916 b, p. 126) reported *C. huronensis* from the Richmond of W Ontario | 217, 219 |
| BILLINGS 1858 (in SALTER & BILLINGS, p. 86) | Original description of *C. halli*, "one or two inches" in diameter | 219 |
| BILLINGS 1865 | Described *C. huronensis* | 219 |
| SALTER 1858 (in Salter & Billings) | Described *C. davisii*, from the Upper Llandoverian of S. Wales | 219, 221 |
| MAILLIEUX 1926 | Reported (via Bather) an undescribed British Wenlockian *Cyclocystoides* and an undescribed Belgian Lower Devonian species | 219 |
| SIEVERTS[-DORECK], H., 1934 (N. Jb. f. Mineral. Ref. 3, p. 626) | Took over the Belgian Lower Devonian specimen for description after Bather's 1934 death | 219 (footnote) |
| FABER 1886 (Pl. 1 fig. 1) | Described *Cyclocystoides (Narrawayella) nitidus* | 221 |
| MILLER & GURLEY 1895 (p. 61) | Described *C. illinoisensis* as poorly preserved but large, with a distinctive nodose margin | 221–222 |
| MILLER 1881 (p. 70) | Supplied the ossicle-formula data for *C. magnus* | 222 |
| BEGG 1934 | Described *C. decussatus* from Girvan, Ashgillian | 221–222 |
| HALL 1866/1872 (Pl. 6 fig. 6) | Described *C. salteri*; Regnéll finds the figure's arrangement of ossicles "not apparent … maybe not accurately drawn" | 223 |

### B6. Systematic section — *Stromatocystites* (pp. 198–200)

| Author, year | What Regnéll attributes to it | Page(s) |
|---|---|---|
| POMPECKJ 1896 | Established genus *Stromatocystites*; genotype *S. pentangularis* from the Middle Cambrian of Bohemia | 198–199 |
| SCHUCHERT 1919 | Emended the genus; reported new species *S. walcotti* and var. *minor* from the Lower Cambrian of western Newfoundland | 198, 199 |
| JAEKEL 1899 (p. 42, Pl. 2 fig. 7) | Described *S. balticus*, citing a Gottsche specimen as the source; the figured specimen (Breslau collection) is a gutta-percha cast, so — per Richter 1943 — cannot be the holotype | 198–199 |
| JAEKEL 1918 (p. 112, text-fig. 104:A) | Re-figured *S. balticus*, located "Südschweden" | 198–200 |
| MIQUEL 1894 (p. 10) | Referred a French form to "*Trochocystites cannati*" | 199 |
| MIQUEL 1905 (pp. 476, 482) | Recognized that same form as a species of *Stromatocystites* | 199 |
| THORAL 1935 b (p. 35, reporting Stubblefield & Spencer) | *S. cannati* is probably identical with a form Jaekel 1923 named "*Cambraster* n. g." | 199 |
| JAEKEL 1923 (p. 344) | Named "*Cambraster* n. g.", interpreted as an asteroid | 199 |
| JAEKEL 1899 (p. 42) | Proposed that *"Medusites lindströmi"* casts might be internal casts of Stromatocystids | 199 |
| MACBRIDE 1906 (p. 596) | Repeated Jaekel's proposal | 199 |
| LINNARSSON 1871 a (p. 12) | Originally described the fossil as "*Agelacrinus? Lindströmi*"; identification confirmed at the time by Loven | 199 |
| NATHORST 1881 (p. 5) | Showed it is instead a medusa cast (*Medusina eosfata*), a determination Regnéll accepts and confirms from LM specimens | 199 |
| RICHTER 1943 (pp. 370–371) | On the type concept: a gutta-percha cast cannot be considered the holotype | 198 (footnote) |

### B7. Systematic section — *Cyathotheca* (pp. 200–203)

| Author, year | What Regnéll attributes to it | Page(s) |
|---|---|---|
| JAEKEL 1927 b | Established family Cyathothecidae for genera *Cyathotheca* and *Cyathocystis*; established genus *Cyathotheca*, genotype and sole original species *C. suecica*; original diagnosis, quoted/translated by Regnéll ("Transiated from JAEKEL 1927 b (p. 4)") | 200–203 |
| F. SCHMIDT 1879 (in ZITTEL 1879) | Established *Cyathocystis*, the family's other genus | 200 |
| F. SCHMIDT 1880 (p. 5) | Proposed that (the confamiliar) *Cyathocystis plautinae* was parasitic, always found growing on monticuloporids | 202 |
| HECKER 1928 (pp. 74–75) | Observed specimens with no monticuloporid connection; concluded the relationship is epoicy, not parasitism/symbiosis | 202 |
| JAEKEL 1918 | Described *C. corallum*, from the Vaginatum limestone of the Leningrad district | 202 |
| JAEKEL 1927 b (Pl. 1, figs. 4–6) | Re-figured *C. corallum*; recorded affinities/differences between *Cyathotheca* and *Cyathocystis* | 202 |
| BATHER [review of Jaekel 1927 b, Geol. Zbl. 35, 1927, Abstr. 919] | Reported (in a review) having collected *Cyathotheca* specimens from various Siljan-district localities, probably now in the British Museum | 203 |
| THORSLUND [letter to the author] | Suggested a stratigraphic point about *Cyathotheca*'s substrate parallel to one made for *Tormoblastus* | 201 (footnote) |

### B8. Systematic section — *Pyrgocystis* (pp. 203–214)

| Author, year | What Regnéll attributes to it | Page(s) |
|---|---|---|
| BATHER 1915 a | Established genus, genotype *P. sardesoni*; first understood the genus's organization from adoral-surface material; revised all seven Aurivillius "Scalpellum" species down to three (*sulcata*, *procera*, *cylindrica*), described two British and one American species; analytical table draws on his data throughout | 203–214 |
| AURIVILLIUS 1892 | Original author of the seven Swedish "*Scalpellum*" species (*sulcatum*, *procerum*, *granulatum*, *strobiloides*, *fragile*, *varium*, *cylindricum*), described as cirripeds | 203, 205–214 |
| RUEDEMANN 1925 (p. 39) | Further contribution to the genus; described *P. batheri* (North American, Bertie waterlime) as thick-plated, smooth or finely granular | 203–204, 207 |
| RICHTER 1930 | Further contribution; described *P. octogona* (Lower Devonian, Germany) | 203–204 |
| HECKER 1939 (pp. 245–246) | Further contribution; described *P. volborthi*, *P. gracilis*, *P. pulkovi* from the Leningrad Ordovician; claimed the spiral plate arrangement in *P. volborthi* "had never been observed before" | 203–204, 207–208, 211–213 |
| JAEKEL 1927 b (p. 4) | Announced an intended paper on a new, apparently very primitive Norwegian Pyrgocystidae form — never published | 203–204 (footnote) |
| HISINGER 1841 a (p. 4, Pl. 41 fig. 6) | Figured "*Columnae Crinoidis fragmentum*", now referred (inverted figure) to *P. sulcata* | 205–206 |
| HEDE [verbal information; 1921, 1942 publications] | Locality/stratigraphic identifications for several Gotland Pyrgocystis localities | 205–206 (footnotes) |
| **BASSLER (1915 a, p. 51 seq.)** — *see Uncertainties* | As printed, credited with a thorough treatment of the *P. sulcata*/*P. ansticei* interrelations | 207 |
| RUEDEMANN 1925 (p. 39) | Described the North American *P. batheri* as similar to *P. sulcata* but with deeper grooves | 207 |
| HECKER 1939 (pp. 245–246) | *P. volborthi* and *P. gracilis* resemble *P. sulcata* | 207 |
| BATHER 1915 a (pp. 52–53) | Described and analysed the spiral plate arrangement years before Hecker (1939) claimed it as a first observation — a citation Regnéll uses to correct Hecker's priority claim | 208–209 |
| AURIVILLIUS 1892 (pp. 17–19) | Original descriptions synonymized under *P. procera* (*Scalpellum procerum*, *granulatum*, *strobiloides*, *fragile*); noted a "keeled" plate appearance and secondary thickening | 207–210 |
| BATHER 1915 a (p. 59) | Recognized *P. procera* as a separate species from *P. sulcata*, but listed *fragile*, *strobiloides*, *granulatum* (with a query) as synonyms of *P. sulcata* — a synonymy Regnéll revises | 207, 210 |
| HECKER 1939 (p. 246) | *P. pulkovi* closely resembles the Swedish *P. varia* | 212 |
| BATHER 1915 a (p. 54) | Noted no weight can be attached to plate-direction differences at the theca's distal end | 208–209 |

---

## (c) New names and nomenclatural acts printed in this paper (within read ranges)

| Act | Printed wording / location | Page |
|---|---|---|
| New class | "Class Paracrinoidea **nov.**" — classification-list entry only; the diagnosis/discussion (p. 37, PDF idx 46) is outside the assigned read range and was not reviewed | 14 |
| New species | *"Cyclocystoides lindströmi* n. sp." — full description, holotype RM Ec 5028, Visby, Gotland, Lower Wenlock | 216–219 |
| New species | *"Cyclocystoides insularis* n. sp." — full description, holotype RM Ec 5033, Fårö, Lower Wenlock | 220–223 |

Not new acts, though listed without "n." markers that might invite confusion: *Stromatocystites
balticus* (JAEKEL 1899, redescribed), *Cyathotheca suecica* (JAEKEL 1927, redescribed), and
all four *Pyrgocystis* species (all recombinations of AURIVILLIUS 1892 names via BATHER 1915a,
none new to this paper).

Outside the strict edrioasteroid scope but within the assigned page-index range 4–7 (the
Contents pages), four Cystoidea (Hydrophoridea) superfamily-level acts are printed as **"n.
nomen"**, i.e. Regnéll's own new superfamily names substituting for existing groupings —
noted here because the range that shows them was explicitly assigned, but their diagnoses
(pp. 68, 97, 107, 111) lie outside the assignment and were not read:

- "Superfamily Glyptocystitida (BATHER 1913) n. nomen" (Contents, p. IV; text at p. 68)
- "Superfamily Hemicosmitida (JAEKEL 1918) n. nomen" (Contents, p. IV; text at p. 97)
- "Superfamily Polycosmitida (JAEKEL 1918) n. nomen" (Contents, p. V; text at p. 107)
- "Superfamily Caryocystitida (JAEKEL 1918) n. nomen" (Contents, p. V; text at p. 111)

No emendation is performed by Regnéll himself (as opposed to cited) on any edrioasteroid,
Cyclocystoidea, or Machaeridia name within the read ranges.

---

## (d) Bibliographic front matter

| Field | Value | Source |
|---|---|---|
| Series | Meddelanden från Lunds Geologisk-Mineralogiska Institution | Title page, p. [I] |
| Series number | N:r 108 | Title page |
| Author | Gerhard Regnell (printed "GERHARD REGNELL" on the second, corrected title-page scan; the first scan reads "GERHARD REONELL" — OCR error, see Uncertainties) | Title page (both scans) |
| Title | "Non-Crinoid Pelmatozoa from the Paleozoic of Sweden. A Taxonomic Study" | Title page |
| Place / year | Lund, 1945 | Title page |
| Printer | Carl Bloms Boktryckeri | Title page |
| Plate credits (title verso) | "Cliches: A.-B. Almquist & Cöster, Hälsingborg" | p. [II] |
| Pagination, whole work | Prefatory matter pp. I–VIII (roman); main text pp. 1–255 (arabic, single sequence, no reset); 15 unnumbered plates follow; final leaf carries only "Pris kronor 12:-." (price notice) | Contents (p. III–VI) and direct page count |
| Pagination, edrioasteroid-relevant portion | Classification-chapter treatment pp. 43–49 (Class Edrioasteroidea, incl. bracketed Cyclocystoidea/Machaeridia discussion); systematic treatment pp. 197–223 (Class Edrioasteroidea proper + Incertae sedis: Cyclocystoidea); corresponding entries in Literature (pp. 224–239) and Index of Genera and Species (pp. 240–244); corresponding plate explanations within pp. 245–255 (Plates 1–2, figs. 6–8, 10 for Cyathotheca/Bockia/Cheirocrinus/Pyrgocystis; Plate 15 figs. 7–9 for Cyclocystoides) | Contents, direct reading |
| Received/submitted/printed date stamp | **Not found.** No date beyond "Lund 1945" appears on the title page; the Preface (pp. VII–VIII) is undated; no colophon or printing-history statement was seen anywhere in the read ranges (including the closing leaf, PDF idx 281) | Title page, Preface, closing leaf |

---

## Uncertainties

- **OCR "BATHER" → "RATHER"/"HATHER"/"DATHER".** This substitution recurs constantly
  throughout the scan (e.g. "RATHER 1899" in the p. 14 classification list, "HATHER 1900" at
  p. 27, "DATHER Hl13" in the Contents). It is corrected silently to BATHER throughout this
  review wherever context makes the intended name unambiguous (Bather is the only relevant
  echinodermologist whose name it could be). Flagged here as a standing, book-wide OCR
  artifact rather than case-by-case: any transcription of BATHER from this scan should be
  treated as "cannot verify against the actual glyphs" without checking the original.
- **"GERHARD REONELL" (p. [I]).** OCR error on the first title-page scan for "REGNELL",
  confirmed by the correct spelling on the second title-page scan two pages later (p. [I], PDF
  idx 2). Not a printed variant — an OCR artifact only.
- **"BASSLER (1915 a, p. 51 seq.)" at printed p. 207.** The passage concerns a detailed
  comparison of the interrelations between *Pyrgocystis sulcata* and *P. ansticei* — exactly
  the kind of morphological discussion found in BATHER's 1915a "Studies in Edrioasteroidea
  VI. Pyrgocystis n. g." (the paper cited throughout this same section for precisely this
  material), not in Bassler's 1915 *Bibliographic index of American Ordovician and Silurian
  fossils* (a title-and-citation index, not a comparative morphological study). This reads
  as a probable OCR or original-printing confusion of BATHER for BASSLER. **Cannot verify**
  without the source image; flagged rather than silently corrected because, unlike the
  book-wide BATHER/RATHER pattern, this one changes which author gets credited with the
  substantive claim.
- **Umlauts and accents.** "Regnéll", "Lindström", "Muller"/"Müller", "Schuchert" and similar
  render inconsistently across the scan (e.g. "MOLLER" for "MÜLLER" at p. 27, "Lindströ mi"
  with a stray space at p. 10). Rendered here as best the OCR shows; treat any umlaut-bearing
  name as **cannot verify** against the original glyph.
- **Ligature/italic corruption in Latin epithets.** Several genus/species names show clear
  scan artifacts inside the read ranges: "Sce" for "See" (p. 197, synonym note), "seyeral" for
  "several" (p. 216), "eaused" for "caused" (repeated), "narned" for "named" (repeated). These
  are OCR noise in ordinary English words and do not affect any name or citation, but are
  symptomatic of the same unreliability affecting italicized Latin names nearby — treat any
  single-occurrence spelling of a species epithet in this document as unconfirmed against the
  plate/original if it looks anomalous.
- **PDF idx 232 (printed p. 223) sits at the outer edge of the assigned range for the
  233–238 marker but was read as the tail of the Cyclocystoides insularis discussion carried
  over from the 206–223 marker** — no gap, but noting the overlap for transparency.
- **Explanation-of-Plates cross-references** (e.g. "Fig. 10. *Bockia?* sp. … 67") point to
  material and pages outside every read range; these are not verified against the actual
  plate images (images are photographic scans not run through OCR text) and are transcribed
  as printed captions only.
- No claim in this review rests on content outside the stated read ranges except where
  explicitly marked "outside the assigned range" (Class Paracrinoidea's diagnosis at p. 37;
  the four Cystoidea superfamily n. nomen diagnoses at pp. 68/97/107/111; Class Eocrinoidea's
  systematic treatment at p. 67).
