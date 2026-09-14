# Audit: `1985_jell_burrett_banks` against the paper

Jell, P.A., Burrett, C.F. & Banks, M.R. 1985. Cambrian and Ordovician
echinoderms from eastern Australia. *Alcheringa* 9(3): 183–208. Read from the
supplied text layer; page numbers below are the printed ones, derived from the
running heads and the explicit page numbers on pp. 184, 185, 194, 198, 200,
202, 204, 206, 207, 208 (formula: printed page = 182 + PDF page index, for
index 1–26). PDF page index 0 is the journal's unpaginated cover sheet.
Indexes 5, 9, 19, 21 (pp. 187, 191, 201, 203) are plates with no body text, as
expected. Compared against `data/trees/1985_jell_burrett_banks.yaml` (156
lines, all read, all `notes` — this file has none).

Proposed audit state: **partial** (current `sources.yaml` state agrees).

## 1. Whole-paper coverage

| statement kind | captured | evidence |
|---|---|---|
| classification skeleton | 3 of 4 root taxa | Class Edrioasteroidea (p.185), Class Ctenocystoidea (p.197), Class Eocrinoidea (p.199) are all present with correct family/genus nesting. **Class RHOMBIFERA (p.205), with Family Echinoencrinitidae Bather 1899 (p.205) and its content, is entirely absent from the tree** — no root node, no family node, no species node. |
| new taxa (`new: true`) | all named new taxa flagged, plus 6 open/cf. nodes also flagged | *C. tastudorum* (p.185), *Edriodiscus* (p.190), *C. jagoi* (p.197), Ridersiidae, *Ridersia*, *R. watsonae* (all p.199) all correctly `new: true`. Six additional nodes with no "n." in their printed heading are also `new: true` — see §4 |
| type species (`type: true`) | 3 of 4 named, all correctly flagged | *Trochocystites cannati* Miquel 1894 "by original designation" (p.185); *Cyclocystoides primotica* Henderson & Shergold 1971 (p.190); *Ctenocystis utahensis* Robison & Sprinkle 1969 (p.197); *Ridersia watsonae* (p.199, type of its own new genus). **Missing: *Stromatocystites pentangularis* Pompeckj 1896, "by monotypy" (p.192) — no node exists for it under `stromatocystites`** |
| emendations / re-rankings | none printed | none found |
| genus-level synonymy | 0 of 1 | p.185: "the synonymy of *Eikosacystis* Cabibel, Termier & Termier 1958 recognised … by Ubaghs (1971)" — not captured |
| original combinations | 1 of 2 | *primotica*'s original combination *Cyclocystoides primotica* Henderson & Shergold 1971 is captured as a `synonyms`+`parents` entry (p.190). **`cannati`'s original combination, "*Trochocystites cannati* Miquel 1894" (p.185), is not captured** — no `synonyms`/`parents` entry, and `trochocystites` already exists as a taxon key |
| diagnoses | 0 | genus diagnoses for *Cambraster* (p.185) and *Ridersia* (p.199); species diagnoses for *C. tastudorum* (p.186), *C. jagoi* (p.197), *R. watsonae* ("As for genus.", p.199) — none captured, consistent with the corpus norm |
| descriptions / remarks | 0 | full morphological text on every named taxon and every indet. form — none captured, consistent with the corpus norm |
| specimens / material | captured for 8 of 10 systematic entries | see §2; catalogue numbers captured with holotype/paratype/unknowntypes roles for every entry that has a tree node; the two missing nodes (Eocrinoid plates indet., Echinoencrinitid indet.) carry no specimens either, since the nodes don't exist |
| occurrences / localities | 0 | none of the four numbered Museum of Victoria localities (NMVPL58, 92, 1597, 1598, pp.183–184) or the two unnumbered ones (Winkleigh/Beaconsfield, p.204; Lune Sugarloaf, p.205) are recorded anywhere in the tree — no `occurrences` field is used in the file at all |
| illustrations | 0 | 18 figures (Figs 1–18) across the paper, none linked to a node or specimen |
| open nomenclature | 6 of 8 forms | *C.* sp. cf. *C. tastudorum* (p.188), *Cambraster* sp. (p.188), ?*Stromatocystites* sp. (p.192), Stromatocystitid indet. (p.195), Isorophid indet. (p.195), Macrocystellid indet. (p.204) are all present. **Eocrinoid plates indet. (p.205) and Echinoencrinitid indet. (p.205) are missing** |
| repository prefix definitions | 0 | p.184 defines NMVP, UTGD, CPC, TMF, ANU; not scoped in the tree/source record |

## 2. Node-by-node check

| node | printed (page) | verdict |
|---|---|---|
| `edrioasteroidea` | "Class EDRIOASTEROIDEA" (p.185) | matches |
| `stromatocystitidae` | "Family STROMATOCYSTITIDAE … Bassler 1936" (p.185) | matches; auth/year agree with `taxa.yaml` |
| `cambraster` | "CAMBRASTER Cabibel, Termier & Termier 1958" (p.185) | **mismatch**: node carries no `auth`/`year`, so it inherits `taxa.yaml`'s `auth: [jaekel], year: 1923`, which contradicts every attribution this paper (and the genus's actual authorship) prints |
| `cannati_miquel_1894` (type) | "Type species. *Trochocystites cannati* Miquel 1894 … by original designation" (p.185) | **mismatch**: placed directly under `cambraster` with no record of the original genus *Trochocystites*; contrast with `primotica`, which does carry its original combination. Fixation method "by original designation" not captured (no field for it exists yet) |
| `tastudorum_jell_burrett_banks_1985` (new) | "CAMBRASTER TASTUDORUM sp. nov." (p.185); Material (p.186) | matches; holotype UTGD122593 and all 22 paratype numbers (`UTGD122226, 122231, 122233`, `NMVP107053–107057, 107059–107072`) reproduced exactly, fully enumerated rather than range-shorthand |
| `cfTaxon: tastudorum…` (= *Cambraster* sp. cf. *C. tastudorum*) | "CAMBRASTER sp. cf. C. TASTUDORUM sp. nov." (p.188); Material "UTGD122233 and 122234 (part and counterpart)" (p.188) | matches on specimens (including the apparent duplicate use of UTGD122233, see §6); `new: true` has no printed nomenclatural basis — see §4 |
| `openTaxon: cambraster-sp…` (= *Cambraster* sp.) | "CAMBRASTER sp." (p.188); Material "ANU36957 to 36960" (p.188) | matches; `new: true` has no printed nomenclatural basis — see §4 |
| `walcotti_schuchert_1919` (provisional) | "we tentatively include *Stromatocystites walcotti* Schuchert 1919 … to that genus" (p.185); "?C. walcotti" (p.185) | matches; `provisional: true` correctly reflects the "?" before the genus abbreviation |
| `edriodiscus` (new) | "EDRIODISCUS gen. nov." (p.190) | matches |
| `primotica_henderson_shergold_1971` (type) | "Type species. *Cyclocystoides primotica* Henderson & Shergold 1971" (p.190); "EDRIODISCUS PRIMOTICA (Henderson & Shergold 1971)"; Material (p.190) | matches on identity, type flag, and the original-combination `synonyms`/`parents` entry. **Mismatch on specimens**: tree lists `paratypes: [CPCl1396, NMVP107479]`, but the paper only designates CPCl1396 "Paratype" (singular, part of Henderson & Shergold's 1971 type series); NMVP107479 is this paper's own newly examined oral-surface specimen, assigned to the species "based on comparison" — never called a paratype (a 1985 paper cannot add paratypes to a name published in 1971) |
| `stromatocystites` | "STROMATOCYSTITES Pompeckj 1896" (p.192) | matches genus identity; **type species not captured** — see §1 |
| `openTaxon: stromatocystites-sp…` (provisional, new) | "?STROMATOCYSTITES sp." (p.192); Material "NMVP107478" (p.192) | matches on specimen and `provisional` (from the "?"); `new: true` has no printed nomenclatural basis — see §4 |
| `openTaxon: stromatocystitidae-sp…` (= Stromatocystitid indet.) | "Stromatocystitid indet." (p.195); Material "ANU36949 to 36956" (p.195) | matches (range of 8 specimens, recorded here as a two-element batch `[ANU36949, ANU36956]` rather than the full enumeration used for `tastudorum` — an internal inconsistency in representation, not a factual error); `new: true` has no printed nomenclatural basis |
| `isorophida` | "Order ISOROPHIDA Bell 1976" (p.195) | matches identity and rank against `taxa.yaml`; placement under `edrioasteroidea` is not stated on the same line but is contextually certain (no intervening class heading) |
| `openTaxon: isorophida-sp…` (= Isorophid indet.) | "Isorophid indet." (p.195); Material "NMVP107129 and 108990" (p.195) | matches on specimens; `new: true` has no "n." in the heading, but the paper does call this "the oldest isorophid edrioasteroid and the first from the Late Cambrian" (pp.183–184) — see §4. **Not captured**: p.196 Remarks call NMVP107129 "the holotype", despite the taxon being left in open nomenclature; the tree records it as a bare, roleless `unknowntypes` entry |
| `ctenocystoidea` | "Class CTENOCYSTOIDEA Robison & Sprinkle 1969" (p.197) | matches |
| `ctenocystidae` | "Family CTENOCYSTIDAE Sprinkle & Robison 1978" (p.197) | matches |
| `ctenocystis` | "CTENOCYSTIS Robison & Sprinkle 1969" (p.197) | matches |
| `utahensis_robison_sprinkle_1969` (type) | "Type species. *Ctenocystis utahensis* Robison & Sprinkle 1969" (p.197) | matches |
| `jagoi_jell_burrett_banks_1985` (new) | "CTENOCYSTIS JAGOI sp. nov." (p.197); Material "Holotype UTGD122594. Paratypes NMVP107073, 107075, 107076" (p.197) | matches exactly, including the gap at NMVP107074. That number is figured (Fig. 10B, "NMVP107074", p.198) but not listed as a paratype — an inconsistency in the paper itself (see §6), correctly not reproduced in the tree |
| `eocrinoidea` | "Class EOCRINOIDEA" (p.199) | matches |
| `ridersiidae` (new) | "Family RIDERSIIDAE nov." (p.199) | matches |
| `ridersia` (new) | "RIDERSIA gen. nov." (p.199) | matches |
| `watsonae_jell_burrett_banks_1985` (type, new) | "RIDERSIA WATSONAE sp. nov." (p.199); Material "Holotype NMVP107112. Paratypes NMVP107113–107128, NMVP107480–107492 and 108991" (p.199) | matches exactly: 16 + 13 + 1 = 30 paratype numbers, all enumerated correctly |
| `macrocystellidae` | "Family MACROCYSTELLIDAE Bather 1899" (p.204) | matches |
| `openTaxon: macrocystellidae-sp…` (= Macrocystellid indet.) | "Macrocystellid indet." (p.204); Material "TMF8342" (p.204) | matches on specimen; `new: true` corresponds to the paper's claim that this is "the first macrocystellid … specimen[] in Australia" (pp.183–184) rather than to any nomenclatural act — see §4. Locality/age data (Winkleigh, Beaconsfield, Tremadocian, p.204) not captured |
| — (no node) | "Family undetermined / Eocrinoid plates indet." (p.205); Material "ANU36961 to 36964" (p.205) | **not captured**: no node anywhere in the tree |
| — (no node) | "Class RHOMBIFERA" / "Family ECHINOENCRINITIDAE Bather 1899" / "Echinoencrinitid indet." (p.205); Material "UTGD54622" (p.205) | **not captured**: no node anywhere in the tree. `rhombifera` and `echinoencrinitidae` already exist as keys in `taxa.yaml` (used by 14 other tree files), so this is a gap in this tree file, not a missing identity record |

## 3. Not captured — summary

- **A whole class-level clade is missing**: Class Rhombifera > Family
  Echinoencrinitidae > Echinoencrinitid indet. (1 specimen, UTGD54622, p.205),
  stated in the abstract itself ("an equally poorly-preserved rhombiferan of
  Middle Ordovician age from Ida Bay is assigned to the Echinoencrinitidae",
  p.183) and in the paper's own count of firsts ("the first … echinoencrinitid
  specimen[] in Australia", pp.183–184).
- **A second indet. taxon is missing**: Eocrinoidea > Family undetermined >
  Eocrinoid plates indet. (4 specimens, ANU36961–36964, p.205).
- **One type species is missing**: *Stromatocystites pentangularis* Pompeckj
  1896, "by monotypy" (p.192) — no node under `stromatocystites`.
- **One genus-level synonymy is missing**: *Eikosacystis* Cabibel, Termier &
  Termier 1958 = *Cambraster*, per Ubaghs (1971) (p.185).
- **One original combination is missing**: *Trochocystites cannati* Miquel
  1894 (p.185); `primotica`'s equivalent is captured, `cannati`'s is not.
- All diagnoses (at least 5: genus *Cambraster* p.185, species *C. tastudorum*
  p.186, species *C. jagoi* p.197, genus *Ridersia* p.199, species *R.
  watsonae* p.199), all descriptions and all phylogenetic remarks — not
  captured, consistent with the rest of the audited corpus.
- All occurrence data: 4 numbered Museum of Victoria localities (NMVPL58, 92,
  1597, 1598, pp.183–184, each with GR coordinates, formation, age/zone) and 2
  unnumbered ones (Winkleigh/Beaconsfield p.204, Lune Sugarloaf p.205) — 0 of 6
  captured.
- All 18 figures/plates — 0 captured, no specimen-to-illustration links.
- Repository prefix definitions (NMVP, UTGD, CPC, TMF, ANU, p.184) — not
  captured (a registry-level gap, not specific to this tree).
- Type fixation wording ("by original designation" p.185; "by monotypy"
  p.192) — not captured; no field exists for it yet in this corpus.

## 4. Cases for the data model

**The `new` flag on open/cf. nodes has no printed nomenclatural basis, but
tracks a broader, unwritten convention.** The roadmap's only documented
meaning for `new` is "n. gen.", "sp. nov." → protologue (semantics-roadmap.md
table row, and the F6 "protologue consistency" check). Six nodes in this
file carry `new: true` with no "n." in their printed heading at all:
`cfTaxon: tastudorum…` ("CAMBRASTER sp. cf. C. TASTUDORUM sp. nov.", p.188 —
the "sp. nov." belongs to the cited species, not this specimen),
`openTaxon: cambraster-sp…` ("CAMBRASTER sp.", p.188),
`openTaxon: stromatocystites-sp…` ("?STROMATOCYSTITES sp.", p.192),
`openTaxon: stromatocystitidae-sp…` ("Stromatocystitid indet.", p.195),
`openTaxon: isorophida-sp…` ("Isorophid indet.", p.195), and
`openTaxon: macrocystellidae-sp…` ("Macrocystellid indet.", p.204). Every one
of these is, however, newly reported *material* in this paper — as opposed to
`cannati_miquel_1894`, `walcotti_schuchert_1919` and `utahensis_robison_sprinkle_1969`,
which are prior taxa cited for comparison/type-designation only and are
correctly *not* `new`. The paper's own introduction frames several of these
as regional or temporal "firsts" ("the oldest isorophid edrioasteroid and the
first from the Late Cambrian", pp.183–184, for the Isorophid indet.; "the
first … macrocystellid and echinoencrinitid specimens in Australia",
pp.183–184, for the Macrocystellid — and, unflagged, the missing
Echinoencrinitid). So `new` in this file is doing double duty for "protologue"
and "first-reported occurrence of a form new to this fauna/region", and the
roadmap does not currently distinguish the two senses.

**A holotype-like word used on open-nomenclature material.** P.196: "Details
of the oral frame are not clear, particularly on the holotype on the left
hand side …" — said of NMVP107129, part of "Isorophid indet.", a taxon the
paper deliberately leaves unnamed ("we prefer to leave it in open
nomenclature within the order", p.196). There is no species name for this
specimen to be the name-bearing type of. This is the D2 `roleAsPrinted` case
("Illustrated Specimen", "plesiotype") extended to a word that, taken at face
value, cannot be a nomenclatural type at all; the tree currently drops the
word entirely rather than recording it as printed.

**A type species cited in its original genus, with the fixation method
stated, but no home for either fact.** "Type species. *Trochocystites
cannati* Miquel 1894 … by original designation" (p.185). The genus part
(original combination) is the same case as B18/original-combination handling
already applied to `primotica`; the fixation method ("by original
designation") has no field in this corpus yet (the roadmap's `typeFixation`
enum discussion, and D2's parallel `holotypeFixation: monotypy`, are both
species-holotype-scoped, not genus-type-species-scoped). "By monotypy" for
*Stromatocystites pentangularis* (p.192) is the same gap.

**An in-paper contradiction between a Material list and a figure caption.**
*C. jagoi*'s Material (p.197) lists paratypes "NMVP107073, 107075, 107076",
skipping 107074; Fig. 10B's caption (p.198) is captioned "NMVP107074" and
described as "an incomplete specimen showing long suboral, marginal and
lateral ctenoid plates" — material that is clearly part of the type series
but never named a paratype. The tree correctly follows the Material section
and omits it, but the paper's own inconsistency (a figured type-series
specimen absent from the type list) is not the kind of thing any field
currently records; it would need a node-level or specimen-level `notes`.

**A repeated catalogue number across two different taxa.** UTGD122233 is
listed as a paratype of *C. tastudorum* (p.186) and, two pages later, as part
of the material of *C.* sp. cf. *C. tastudorum* ("UTGD122233 and 122234
(part and counterpart)", p.188). The tree reproduces both uses faithfully (as
the ground rules require — "notes is the last-resort escape hatch," not a
place to silently fix the source), but nothing marks that the paper's own
numbering looks internally inconsistent here. See §6.

**A misidentified paratype role carried forward from another source's type
series.** `primotica_henderson_shergold_1971`'s tree entry lists
`paratypes: [CPCl1396, NMVP107479]`; only CPCl1396 is Henderson & Shergold's
1971 paratype (p.190). NMVP107479 is this (1985) paper's own newly examined
material, assigned to the species by inference ("Assignment of the newly
found oral surface to this species is based on comparison…", p.190) — a
referred specimen, not a paratype of a name this paper does not itself
propose. This is the D2 "material cited without a role" case, misapplied.

## 5. Source record check

`sources.yaml`'s `1985_jell_burrett_banks` block matches the paper on every
checked field: title ("Cambrian and Ordovician echinoderms from eastern
Australia"), journal (Alcheringa), volume 9, number 3, pages 183–208, authors
[jell, burrett, banks] in printed order, DOI
10.1080/03115518508618967 (p.183), `processDates.received: 1984-11-22`
("received 22 November 1984", p.183) and `processDates.online: 2008-11-27`
("Published online: 27 Nov 2008", p.183; restated p.183–184).

Two items **cannot verify**:
- The citation header (p.183) prints "JELL, P. A., BURRETT, C. F., & BANKS,
  M. R., 1985:08:26." — an unusual embedded date, "1985:08:26", not present
  anywhere in `sources.yaml`. Its meaning (acceptance date, imprint date, an
  artefact of the citing convention) cannot be determined from the text
  supplied.
- `sources.yaml`'s `audit.notes` retains the legacy pre-migration flags
  ("named=true open=false history=false specimens.basic=false
  specimens.all=false"). Read literally against the tree file, `open=false`
  and `specimens.basic=false` understate what is actually captured: 6 of 8
  open-nomenclature forms are present, and every systematic entry with a tree
  node carries at least catalogue numbers. These are stated to be migrated
  legacy values rather than a current claim, so this is noted, not treated as
  an error to fix.

## 6. Uncertainties

- **CPCl1395 / CPCl1396** (p.190, primotica's holotype/paratype): cannot
  verify whether "CPCl" is the printed prefix or an OCR artefact of "CPC" plus
  a leading "1" misread as "l" in a five-digit number (e.g. "CPC 11395"). The
  tree's spelling matches the supplied text exactly either way.
- **UTGD122233 duplicate use** (pp.186, 188): cannot verify from the text
  alone whether this is a printed error in the original paper (e.g. one of
  the two citations should read a different number) or a real dual role for
  one specimen; the tree reproduces both citations as printed.
- **NMVP107074** (p.198, Fig. 10B) figured but absent from the *C. jagoi*
  paratype list (p.197): cannot verify why; not present in the tree, which is
  consistent with the printed Material section.
- Pages 187, 191, 201, 203 are plates with no OCR text; illustration content
  and any captions confined to those pages cannot be verified beyond what the
  facing-page captions describe.
- Whether "Order ISOROPHIDA Bell 1976" (p.195) is explicitly subordinate to
  "Class EDRIOASTEROIDEA" in the paper's own heading hierarchy cannot be
  fully verified — the two headings are separated by the Stromatocystitidae
  content with no repeated class-level heading in between, so the nesting is
  inferred from continuity of the systematic section rather than from an
  explicit line.
