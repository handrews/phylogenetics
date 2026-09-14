# Review: `1994_guensburg_sprinkle` against the paper

Guensburg, T. E., and J. Sprinkle. 1994. Revised phylogeny and functional
interpretation of the Edrioasteroidea based on new taxa from the Early and
Middle Ordovician of western Utah. *Fieldiana: Geology*, n.s., no. 29, pp.
1–43 (published December 30, 1994). Read from the OCR text at
`1994_guensburg_sprinkle.txt` (PDF page indexes 0–63). Compared against
`data/trees/1994_guensburg_sprinkle.yaml` (309 lines, all read) and the
`1994_guensburg_sprinkle` block in `data/sources.yaml`.

**Page mapping.** The title page (index 6/8) carries no page number; numbered
pagination begins at index 12 = printed p. 1 (confirmed by the Table of
Contents at index 10, and by footer digits recurring through the text).
Printed page = PDF index − 11, valid for index 12 through 53 (pp. 1–43).
Indexes 0–5 are library/copyright front matter with no article text; 7 is the
"Information for Contributors" boilerplate; 9 is the copyright/ISSN page; 11
is a caption for the back cover image. Indexes 41, 42, 46, 47, 55, 57–63 are
full-page figures or blank leaves carrying only a page number or nothing (a
genuine absence of a text layer, not an OCR failure — these are plates/blank
versos). Index 34 (p. 23) and 30 (p. 19) are running-head-only footers between
figure pages. None of the sparse-text indexes conceal missed body text; all
are checked against their neighbors.

Proposed audit state for this source: **partial** (classification skeleton
essentially complete and verified; no material, occurrence, diagnosis,
illustration, or full-text content captured, which is consistent with this
tree's scope).

## 1. Whole-paper coverage

| statement kind | captured | evidence |
|---|---|---|
| classification skeleton (order–subfamily ranks, `emended`, `modifier: nomen transl.`) | all, and verified exactly | Revised Classification, pp. 12–13; repeated verbatim as Systematic Paleontology section headers, pp. 13–38 |
| genus-level placements | all genera in the Appendix compilation | Appendix, pp. 42–43, "compilation of edrioasteroid genera... expanded and modified from Bell (1980)" (p. 42) |
| new taxa (`new: true`) | all 5 genera + 5 species | Abstract (p. 1): "Five new edrioasteroid genera"; each genus/species header in Systematic Paleontology, pp. 14, 21–22, 24–25, 28–29, 33–34 |
| type species (`type: true`) | all 5 | "Type Species—" lines under each new genus, same pages |
| re-rankings (`modifier: nomen transl.`) | all 8 | see §4 below |
| emendations (`emended: true`) | 10 of 11 printed instances | see §4, Lebetodiscinae gap |
| synonymy | 1 of 1 informal case | Cyathotheca/Cyathocystis, p. 21 (partial — see §3) |
| diagnoses | 0 | printed for every order/suborder/family/subfamily actually treated (not Camptostromatoida/Stromatocystitida, which get no systematic treatment at all — see below) and for all 5 new genera/species, pp. 13–34 |
| specimens/material | 0 | holotype/paratype numbers, measurements, plate/figure locators for all 5 new species plus 3 unnamed "Edrioasterid Species Indeterminate" occurrence groups, pp. 14–19, 21–37 |
| occurrences | 0 | formation, member, trilobite zone, section, and township/range/section locality for every taxon above, same pages |
| illustrations | 0 | 18 text figures (Figs. 1–18) plus Table 1 (42 characters); none referenced from the tree |
| cladogram(s) | all 4 topologies (as printed terminal sets) | Fig. 2, p. 5 (caption: "A, B, Two preferred trees; C, D, Adams and strict consensus trees, respectively") |
| character data | 0 | Table 1 (42 characters), p. 6; data matrix, Fig. 1, p. 4 |
| earlier classifications compared (not reproduced) | 0 | prose comparison to Bell (1980) and Smith (1985) classifications, p. 12–13 (see §3) |
| declared scope limits | 0 | "Limitations of time prevented a complete literature search, and the list is not exhaustive" (Appendix, p. 42); "we have not erected a new classification scheme to receive them" (p. 12) |

Order Camptostromatoida, Family Camptostromatidae, Order Stromatocystitida,
Family Stromatocystitidae, and Family Totiglobidae receive **no** diagnosis
or discussion anywhere in Systematic Paleontology — they occur only in the
two classification lists (pp. 12–13, 42–43). This is a fact about the paper's
structure, not a gap in the tree: there is nothing to capture beyond
placement for these five taxa.

## 2. Node-by-node check

### 2a. `taxonomies[0]` (Echinozoa → Edrioasteroidea)

This single tree entry is a synthesis of three printed structures that never
appear together as one table: (i) the Subphylum/Class header at the top of
Systematic Paleontology (p. 13, "Subphylum ECHINOZOA Matsumoto, 1929"); (ii)
the rank/authority/`emend.`/`nomen transl.` markers from the Revised
Classification (pp. 12–13), repeated verbatim as section headers through
Systematic Paleontology; and (iii) the genus memberships from the Appendix
compilation (pp. 42–43), which carries no `emend.`/`nomen transl.` markers of
its own. This should be named explicitly if the tree's `notes` or metadata
ever record "which printed table" it represents — currently it represents
none of the three alone.

| node | printed (page) | verdict |
|---|---|---|
| `echinozoa` | "Subphylum ECHINOZOA Matsumoto, 1929" (p. 13) | matches; note "Credited to Matsumoto 1929" correct |
| `edrioasteroidea` | "Class EDRIOASTEROIDEA Billings, 1858" (pp. 12, 13, 42) | matches |
| `camptostromatoida` | "Order CAMPTOSTROMATOIDA Durham, 1966" (pp. 12, 42); no diagnosis anywhere | matches (no flags printed) |
| `camptostromatidae` | "Family CAMPTOSTROMATIDAE Durham, 1968" (pp. 12, 42) | **year not captured by the tree at all** (tree has no `auth`/`year` fields); see §4 — `taxa.yaml` gives 1967, twice-printed form is 1968 |
| `camptostroma` | "Camptostroma Ruedemann, 1933" (Appendix, p. 42) | matches |
| `stromatocystitida` | "Order STROMATOCYSTITIDA Bell, 1980" (pp. 12, 42); no diagnosis | matches |
| `stromatocystitidae` | "Family STROMATOCYSTITIDAE Bassler, 1935" (pp. 12, 42) | matches |
| `stromatocystites` | "Stromatocystites Pompeckj, 1896" (Appendix, p. 42) | matches |
| `openTaxon: edrioasteroidea-order-uncertain` → `openTaxon: edrioasteroidea-family-uncertain` → `cambraster`, `walcottidiscus` | "Order and Family Uncertain / Cambraster ... / Walcottidiscus ..." — **one** heading, no rank distinction printed (Appendix, p. 42) | **mismatch: the tree invents a two-rank nesting for a heading printed as a single undifferentiated placeholder** — see §4 |
| `isorophida` | "Order ISOROPHIDA Bell, 1976" (pp. 12, 13, 42); Systematic Paleontology gives it no diagnosis of its own (goes straight to Family Agelacrinitidae) | matches, no flags printed |
| `openTaxon: isorophida-family-uncertain` → `edriodiscus`, `stromatocystites`(quoted)+`walcotti_schuchert_1919` | "Order ISOROPHIDA Bell, 1976 / Family Uncertain / Edriodiscus Smith, 1985 / "Stromatocystites" walcotti Schuchert, 1919" (Appendix, p. 42) | matches exactly, including the double-quoted genus abbreviation as printed elsewhere ("S." walcotti, "Totiglobus" lloydi) |
| `agelacrinitidae`, `emended: true` | "Family AGELACRINITIDAE Chapman, 1860 (emend.)" (pp. 12, 24) | matches |
| 22 agelacrinitid genera (`agelacrinites` … `ulrichidiscus`) | Appendix list, p. 42 | all 23 present (deltadiscus flagged `new`), none omitted, none extra |
| `deltadiscus`, `new: true` | "Deltadiscus, n. gen." (Appendix, p. 42); "Genus Deltadiscus / Guensburg and Sprinkle, new genus" (p. 25) | matches; but see §4 for the missing `provisional` |
| `superbus_guensburg_sprinkle_1994`, `type: true, new: true` | "Type Species—Deltadiscus superbus Guensburg and Sprinkle, new species" (p. 25) | matches |
| `lebetodiscidae`, `modifier: nomen transl., emended: true` | "Family LEBETODISCIDAE Bell, 1976 (nomen transl., emend.)" (pp. 12, 25) | matches |
| `lebetodiscinae`, `modifier: nomen transl.` (no `emended`) | Revised Classification (p. 12): "(nomen transl.)" — **but** Systematic Paleontology heading (p. 27): "(nomen transl.. emend.)", with discussion text "it is emended to allow for separation of pyrgocystinids" | **mismatch: the tree follows only the p. 12 wording; the paper's own p. 27 heading and prose add `emend.`** — see §4 |
| 10 lebetodiscinid genera | Appendix, p. 42 | all present, none extra |
| `carneyellinae`, `modifier: nomen transl.` (no `emended`) | "(nomen transl.)" both at p. 12 and p. 27; discussion (p. 27) says the subfamily "is again modified to distinguish the pyrgocystinids" without a formal `(emend.)` tag either place | matches (tag consistent both places; the discussion's "modified" is looser prose, not a formal act) |
| `carneyella`, `cryptogoleus` | Appendix, p. 42 | present; see §4 for `carneyella`'s year |
| `pyrgocystinae`, `modifier: nomen transl., emended: true` | "(nomen transl., emend.)" pp. 12, 27 | matches |
| `archaepyrgus`, `new: true`; `anitae_guensburg_sprinkle_1994`, `type: true, new: true` | pp. 28–29 | matches |
| `epipaston`, `pyrgocystis` | Appendix, p. 42 | present |
| `fanulodiscus`, `new: true`; `crystalensis_guensburg_sprinkle_1994`, `type: true, new: true` | pp. 33–34 | matches |
| `edrioasterida`, `emended: true` (no modifier) | "Order EDRIOASTERIDA Bell, 1976 (emend.)" (pp. 12, 13) | matches |
| `edrioasterina`, `modifier: nomen transl., emended: true` | "(nomen transl., emend.)" p. 12, 13 | matches |
| `totiglobidae` (no flags) | "Family TOTIGLOBIDAE Bell and Sprinkle, 1978" (pp. 12, 42) — no diagnosis anywhere | matches |
| `totiglobus` (leaf) and `totiglobus` quoted → `lloydi_sprinkle_1985` | "Totiglobus Bell and Sprinkle, 1978" / '"Totiglobus" lloydi Sprinkle, 1985' (p. 42); discussion (p. 19): '"Totiglobus" lloydi was provisionally assigned to genus at the time of its description because of poor preservation (Sprinkle, 1985)' | matches on `quoted`; **missing `provisional`** and the reason, which is printed explicitly — see §4 |
| `edrioasteridae` (no flags) | "Family EDRIOASTERIDAE Bather, 1898" (pp. 12, 14) | matches |
| `edrioaster`, `edriophus` | Appendix, p. 42 | present |
| `paredriophus`, `new: true`; `elongatus_guensburg_sprinkle_1994`, `type: true, new: true` | pp. 14–17 | matches |
| `edrioblastoidina`, `modifier: nomen transl., emended: true` | "(nomen transl., emend.)" pp. 12, 20 | matches |
| `astrocystitidae`, `emended: true` (no modifier) | "Family ASTROCYSTITIDAE Bassler, 1935 (emend.)" pp. 12, 21 | matches |
| `astrocystites`, `cambroblastus` | Appendix, pp. 42–43 | present |
| `lampteroblastus`, `new: true`; `hintzei_guensburg_sprinkle_1994`, `type: true, new: true` | pp. 21–23 | matches |
| `cyathocystidae`, `emended: true` (no modifier) | "Family CYATHOCYSTIDAE Bather, 1899 (emend.)" pp. 12, 21 | matches |
| `cyathocystinae`, `modifier: nomen transl., emended: true` | "(nomen transl., emend.)" pp. 12, 21 | matches |
| `cyathocystis` + `synonyms: cyathotheca` | "Cyathocystis Schmidt, 1879" (p. 42); "Cyathotheca Jaekel, 1927, is closely related to or more likely a junior synonym of Cyathocystis, differing from the latter only in lacking a basal ring. This apparent difference could be purely preservational (Fig. 17D)." (p. 21) | matches in substance; note paraphrases rather than quotes, and drops the attribution "Jaekel, 1927" and the figure locator — see §3 |
| `rhenopyrginae`, `modifier: nomen transl., emended: true` | "(nomen transl., emend.)" pp. 12, 21 | matches |
| `rhenopyrgus` | "Rhenopyrgus Dehm, 1961" (p. 43) | matches |

### 2b. `phylogenies` (4 cladograms)

Fig. 2 caption (p. 5): "Cladograms generated by the edrioasteroid parsimony
analysis. A, B, Two preferred trees; C, D, Adams and strict consensus trees,
respectively." The tree's four entries — "preferred parsimony A", "preferred
parsimony B", "Adams", "strict consensus" — correctly correspond to Fig. 2A–D
in that order, and the 15-taxon terminal set matches the paper's own count
("Forty-two characters were scored for 15 taxa," Abstract, p. 1) exactly:
Stromatocystites, Cambraster, Edriodiscus, Pyrgocystinae, Lebetodiscinae,
Chatsworthia, Agelacrinitidae, "S." walcotti, Totiglobus, Edrioasteridae,
Astrocystitidae, Rhenopyrgus, Cyathocystis, "T." lloydi, Camptostroma.

The cladogram figure itself is a line drawing; its OCR text layer preserves
the terminal-taxon labels in reading order but not the branching topology
(brace/line characters are lost). **I cannot verify the exact parent–child
topology in each tree against the figure from OCR text alone.** What can be
verified from the surrounding prose (pp. 3–4, 18–20) is consistent with the
tree's shape: Camptostroma as outgroup/basal branch ("we use Camptostroma...
as the outgroup," p. 3); Cambraster as sister to "S." walcotti and Edriodiscus
as sister to that pair (p. 18); Chatsworthia's position relative to
Lebetodiscinae/Agelacrinitidae explicitly called "unresolved by the parsimony
analysis" (p. 19, consistent with it sitting outside the Pyrgocystinae/
Lebetodiscinae clade in all four tree file entries); pyrgocystinids as sister
to lebetodiscinids (p. 19); Totiglobus/edrioasterids/edrioblastoids/
cyathocystids branching as described (pp. 19–20). Fig. 1 (p. 4, "one preferred
tree... combined with the data matrix") is the same topology as one of the
two preferred trees, not a fifth distinct cladogram, and is not separately
represented — correctly, since it would be a duplicate.

One terminal-rank note, not a mismatch: **Chatsworthia is classified as a
genus of Lebetodiscinae** in the Revised Classification/Appendix (p. 42), yet
stands as its own coordinate terminal alongside "Lebetodiscinae" as a whole in
the cladogram (p. 5). Likewise "Agelacrinitidae" (family), "Pyrgocystinae"/
"Lebetodiscinae" (subfamily), and "Chatsworthia" (genus) are sister terminals
of mixed rank in one cladogram. The tree captures this correctly by letting
`taxon:` reference a node at any rank; flagged in §4 as the documented case.

## 3. Not captured

- All specimen/material data: catalogue numbers (fmnh pe-, usnm-prefixed),
  counts, measurements, and plate/figure locators for the 5 new species and 3
  unnamed occurrence groups ("Giza Peak" megaripple group, "Windy Point"
  hardground group, "Giza Peak" mound specimen), pp. 14–19, 21–37.
- All occurrence data: formation/member, trilobite zone, stage, and
  township-range-section locality for the same, same pages.
- All diagnoses (order through species), pp. 13–34.
- Table 1 (42 morphological characters) and the data matrix (Fig. 1), pp. 4,
  6.
- The footnote on p. 25 describing a second Deltadiscus specimen (paratype
  fmnh pe 52719) "discovered by Colin Sumrall while this paper was in press,"
  with its own occurrence — an in-press addendum entirely absent from the
  tree.
- The prose comparison of this paper's classification to Bell (1980)'s and
  Smith (1985)'s (pp. 12–13): "It [Smith's] differs most significantly from
  ours in combining pyrgocystids and cyathocystids as an order, in its
  inclusion of the cyclocystoids as a family within the isorophids, and in
  placing lebetodiscids as a subfamily within the Agelacrinitidae"; and "our
  classification differs from that of Bell (1980) in that the parsimony
  analysis mapped cyathocystids as derived from edrioasterids rather than
  isorophids, and edrioblastoids were specialized edrioasterids rather than
  a separate class." Neither comparison is captured as a note or claim
  anywhere in the tree.
- The declared scope limits on the Appendix itself (p. 42): "The
  agelacrinitids are easily the most diverse of edrioasteroid families;
  several subfamilies are likely present, but these are not treated here,
  pending revision of the group. Limitations of time prevented a complete
  literature search, and the list is not exhaustive." No `listComplete:
  false` or equivalent note on `agelacrinitidae` or on the Appendix-derived
  tree as a whole.
- The attribution "Jaekel, 1927" and figure locator "(Fig. 17D)" on the
  `cyathotheca` synonym entry (its `notes` paraphrase the sentence but carry
  neither).
- The explicit statement that Walcottidiscus was excluded from the parsimony
  analysis despite a prior hypothesis about its relationships: "Walcottidiscus
  from the Middle Cambrian has been presented as the sister group to the
  edrioasterids (Smith & Jell, 1990, p. 771)... The specimens are all poorly
  preserved and lack most data, so we omitted this taxon from the parsimony
  analysis" (p. 19). A secondhand placement claim (B19-type) attached to a
  taxon the tree places only as `openTaxon`.
- Count: at minimum 5 kinds of statement (material, occurrence, diagnosis,
  character/matrix data, classification-comparison prose) are captured 0
  times across the whole paper; 1 in-press addendum and 1 secondhand
  citation are also absent.

## 4. Cases for the data model

- **Re-rankings (B18), all 8, with printed wording and derivation.** All are
  `nom. transl.` acts by this paper, transferring names down in rank; `act:
  [nomTransl]` per B6 once that field exists. Printed forms (Revised
  Classification, pp. 12–13, verbatim again in Systematic Paleontology):
  - "Family LEBETODISCIDAE Bell, 1976 (nomen transl., emend.)" — ex Suborder
    Lebetodiscina Bell, 1976 (per B18's own citation of this source).
  - "Subfamily LEBETODISCINAE Bell, 1976 (nomen transl.)" [p. 12] / "(nomen
    transl.. emend.)" [p. 27] — ex Family Lebetodiscidae Bell, 1976 (stated
    explicitly, p. 27: "equivalent to the Lebetodiscidae Bell, 1976").
  - "Subfamily CARNEYELLINAE Bell, 1976 (nomen transl.)" — ex "the family
    Carneyellidae Bell, 1976" (stated explicitly, p. 27).
  - "Subfamily PYRGOCYSTINAE Kesling, 1967 (nomen transl., emend.)" — ex a
    family- or suborder-rank Pyrgocystinae/Pyrgocystidae Kesling, 1967 (the
    source name is not spelled out on these pages; not verified here).
  - "Suborder EDRIOASTERINA Bather, 1898 (nomen transl., emend.)" — ex
    "Bather's family Edrioasteridae as defined by Bell (1976a, 1980)" (p. 13).
  - "Suborder EDRIOBLASTOIDINA Fay, 1962 (nomen transl., emend.)" — ex a
    class-rank Edrioblastoidea Fay, 1962 (per the Discussion, p. 13: "not a
    separate class" as in Fay's original scheme).
  - "Subfamily CYATHOCYSTINAE Bather, 1899 (nomen transl., emend.)" — ex "the
    family Cyathocystidae of Bather, 1898, and the order Cyathocystida, Bell,
    1975" (p. 21, both cited as equivalents in one sentence — a rare case of
    one `nomen transl.` line pointing at two different rank-and-authority
    predecessors printed together).
  - "Subfamily RHENOPYRGINAE Holloway and Jell, 1983 (nomen transl., emend.)"
    — ex "their family Rhenopyrgidae" (Holloway & Jell, 1983, pp. 1002–1004,
    per p. 21).
  All 8 are already captured with `modifier: nomen transl.` (+ `emended` where
  co-printed); none carry the derivation target or the act's own page. B6's
  planned `act`/`actBy`/`altRankOf` structure is the natural home; this
  source is one of the two the roadmap (B18) already names for it.

- **A single printed heading split into two ranks of `openTaxon`.** "Order and
  Family Uncertain" (Appendix, p. 42) is one undifferentiated heading holding
  Cambraster and Walcottidiscus directly. The tree models it as
  `openTaxon: edrioasteroidea-order-uncertain` containing
  `openTaxon: edrioasteroidea-family-uncertain` containing the two genera —
  an editorial two-rank expansion of a heading that names both ranks as
  jointly uncertain, not as two nested placeholders. Neither `taxa.yaml`
  record for these two keys carries a `notes` field explaining the split, nor
  does the tree mark either node `editorial.inferred: true` (B20), though the
  structure is the editor's, not the paper's.

- **A `provisional` statement not carried onto the flag.** "'Totiglobus'
  lloydi was provisionally assigned to genus at the time of its description
  because of poor preservation (Sprinkle, 1985)" (p. 19). The tree captures
  `quoted: true` (correct, for the doubted generic assignment shown in
  quotes) but not `provisional`, and the reason is not in `notes`.

- **A genus's family placement stated as provisional in prose, unflagged in
  the tree.** Deltadiscus: "The new genus is provisionally assigned to and
  arguably the most primitive taxon of agelacrinitids. Difficulties in
  evaluating this taxon result from the lack of or poor information regarding
  oral cover plate, hydropore, and peripheral rim construction..." (p. 25;
  OCR appears to have dropped a word after "assigned to," most likely "the
  Agelacrinitidae"). The tree places `deltadiscus` as a plain child of
  `agelacrinitidae`, no `provisional`.

- **Two occurrences of one heading with different acts printed on the same
  name.** Subfamily Lebetodiscinae is "(nomen transl.)" in the Revised
  Classification (p. 12) and "(nomen transl.. emend.)" in the Systematic
  Paleontology heading (p. 27), the latter reinforced by prose ("it is
  emended to allow for separation of pyrgocystinids"). One paper, one name,
  two different printed acts at two page locations — the tree can only carry
  one `emended` value per node and has picked the p. 12 reading. This is a
  concrete instance of "every rule... has been broken," worth recording
  because the discrepancy is the *source's own*, not a data-entry error.

- **Cladogram terminals of mixed taxonomic rank in one tree**, already
  correctly modeled (§2b): a family (Agelacrinitidae), two subfamilies
  (Pyrgocystinae, Lebetodiscinae), and a genus that is itself classified
  inside one of those subfamilies (Chatsworthia, inside Lebetodiscinae) are
  coordinate sister terminals. Recorded here as a real instance for the
  roadmap to cite; no fix needed, since flat `taxon:` references already
  handle it.

- **Genus-level attributions printed in this paper that differ from the
  `taxa.yaml` record, uncaptured because this tree has no per-node
  `auth`/`year` fields at all.** Since every attribution lives only on the
  taxon record here, none of these are visible as claims:
  - `camptostromatidae`: printed "Durham, 1968" (twice, pp. 12 and 42);
    record gives `year: 1967`.
  - `isorophus`: printed "Foerste, 1917" (p. 42); record gives `year: 1916`.
  - `carneyella`: printed "Foerste, 1917" (p. 42); record gives `year: 1916`.
    (Same author, same one-year offset as `isorophus` — possibly one
    systematic dating convention issue in the record, not independent typos;
    not established here.)
  - `edriodiscus`: printed "Smith, 1985" (p. 42); record gives `auth: [jell,
    burrett, banks], year: 1985` — a different author entirely, same year.
  - `cambraster`: printed "Cabibel, Termier, and Termier, 1958" (p. 42);
    record gives `auth: [jaekel], year: 1923` — a wholly different name,
    author, and year. Neither "1958_cabibel..." nor "1923_jaekel" nor
    "1969_termier..." (the `cambrasteridae` family record's own authority,
    `Termier, Termier, 1969`) exists as a source key in `sources.yaml`. Three
    different attributions for one genus name, across three records, none
    resolvable in this dataset — this is the A11/A8 pattern (multiple printed
    attributions for one entity) at its worst documented so far, and it
    should not be guessed at.
  None of these are `altSpellingOf`/misprint cases on their face; they read as
  either the record's authority being wrong, this paper's citation being
  wrong, or (for `isorophus`/`carneyella`) a genuine reading vs. issue-date
  question the source pattern (A8) already anticipates. Flagged, not
  resolved.

## 5. Source record check

| field | printed | `sources.yaml` | verdict |
|---|---|---|---|
| title | "Revised Phylogeny and Functional Interpretation of the Edrioasteroidea Based on New Taxa from the Early and Middle Ordovician of Western Utah" (title page, p. [ii]/index 8) | "Revised phylogeny and functional interpretation of the Edrioasteroidea based on new taxa from the Early and Middle Ordovician of western Utah" | matches (case-normalized only) |
| journal/series/number | "FIELDIANA Geology NEW SERIES, NO. 29" | `journal: fieldiana`, `volume: New Series`, `number: 29` | matches |
| pages | "PP. 1^*3" (running head, p. 1; OCR-garbled, almost certainly "1–43" — the Appendix ends on printed p. 43) | not recorded | not captured; cannot fully confirm "43" from OCR alone, but every page number I traversed through the Appendix (p. 42–43) is consistent with a 43-page article |
| publication date | Title page (index 8): "Accepted May 27, 1994" / "Published December 30, 1994" | `pubDate: {year: 1994, month: 12, day: 30}` | matches the printed **published** date exactly; the "1994-05-27" the task points to is the printed **accepted** date, a different fact the record does not need to carry unless the model wants a `processDates.accepted` field alongside `pubDate` (parallel to the `read`/`issued` pattern documented elsewhere for this dataset) |
| authors | "Thomas E. Guensburg", "James Sprinkle" | `[guensburg, sprinkle]` | matches (full-name resolution not checked here) |

## 6. Uncertainties

- Cannot verify the branching topology of any of the four cladograms (Fig.
  2A–D, p. 5) against the tree file's parent/child structure beyond the
  terminal-taxon set and the specific relationships stated in prose (§2b);
  the figure is a line drawing and its OCR text layer does not preserve
  branch structure.
- Cannot verify whether "Cambraster" at p. 20 ("Only three genera of
  edrioblastoids are known: Astrocystites, Cambraster, and Lampteroblastus")
  is printed as written or is an OCR misreading of "Cambroblastus" — the same
  paragraph and the next both correctly use "Cambroblastus" for the Late
  Cambrian astrocystitid genus discussed there, and "Cambraster" is
  elsewhere (p. 42, p. 18) consistently a different, Order-and-Family-
  Uncertain genus with no edrioblastoid affinity claimed anywhere else in the
  paper. Likely OCR corruption, not a printed claim; not acted on here.
- Cannot resolve which of "Cambraster Cabibel, Termier, and Termier, 1958,"
  "Cambraster Jaekel, 1923" (the `taxa.yaml` record), or "Cambrasteridae
  Termier, Termier, 1969" (the family record) is the correct original
  citation, or whether more than one is a genuine homonym/misattribution;
  none of the three source works is in `sources.yaml`.
- Cannot confirm the printed page range as exactly "1–43" from the OCR text
  alone (see §5); the digits are garbled in the one place they are printed
  in running form.
- Did not check `taxa.yaml` attributions for the roughly 40 remaining genus
  and family names beyond the sample tested in §4 (a full pass would need to
  check every printed "Name Author, Year" in the Appendix and Revised
  Classification against its `taxa.yaml` record; only genera and families
  with a plausible discrepancy were sampled).
- Did not verify full names behind the `guensburg`/`sprinkle` author keys or
  any other `taxa.yaml`/`sources.yaml` cross-reference not directly bearing
  on this tree file.
