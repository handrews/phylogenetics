# Review: `1985_smith.a.b`

Smith, A. B. 1985. "Cambrian eleutherozoan echinoderms and the early
diversification of edrioasteroids", *Palaeontology* 28(4): 715–756. Compared
against `data/trees/1985_smith.a.b.yaml` (128 lines, all read, including every
`notes`). Printed pages cited below; PDF page index = printed page − 393.

Proposed audit state: **partial**.

## 1. Whole-paper coverage

| statement kind | captured | evidence |
|---|---|---|
| classification skeleton — traditional (Bell 1980) | all | Table 3 left column (p. 734), 20 taxa, reproduced as the first `taxonomies` entry in the same nesting order |
| classification skeleton — revised (this paper) | all | Table 3 right column (p. 734), reproduced as the second `taxonomies` entry |
| classification skeleton — systematic section | all 5 genera, all named species | third `taxonomies` entry ("no higher taxa given") |
| new taxa (`new: true`) | n/a | this paper proposes no new species or genera; none flagged, correctly |
| re-rankings / nom. transl. | 2 of 2 | Isorophina→Isorophinae, Lebetodiscina→Lebetodiscinae, both `modifier: nomen transl.` (p. 736) |
| emendations (`emended: true`) | 1 of at least 2 printed | Cyathocystida flagged; Isorophida printed "(emend.)" in Table 3 (p. 734) and given an emended diagnosis (p. 736) but not flagged — see §2 |
| "sedis mutabilis" | 1 of 3 printed | only on Cyathocystida node; Edrioasterida and Isorophida also print it (p. 734) but the tree has no marker there — see §2 |
| type species | 5 of 5 (flag only) | every genus's "Type species." statement (pp. 736, 746, 748, 749, 753) matches a `type: true` species node; the fixation mechanism itself ("by original monotypy" ×2, "by original designation" ×3) is not captured |
| diagnoses | 0 | 5 genus diagnoses, 2 species diagnoses (others "As for genus"), and 6 emended higher-taxon diagnoses (pp. 734–736) are all prose, none in `notes` |
| synonymy lists | ~1 of 9+ | only the *typicalis*/*magister* synonymy relationship is captured (as a `synonyms` entry); genus- and species-level chronological synonymy lists for all five genera (9–18 lines apiece) are not captured |
| specimens/material | 0 | every species has "Types" and "Material studied/examined" paragraphs with repository numbers (BM(NH), USNM, MCZ, NYSM, CPC); none in the tree |
| occurrences | 0 | every genus/species has a "Stratigraphical age and distribution" paragraph; none in the tree |
| illustrations | 0 | text-figs 1–20 and Plates 87–89 assigned throughout; none in the tree |
| cladogram/phylogeny | 1 entry, scope ambiguous | one `phylogenies` block; the paper prints three distinct cladograms (text-fig. 9, p. 728; text-fig. 10, p. 730; text-fig. 12, p. 735) — see §4 |
| earlier classification reproduced | captured | Table 3's "Traditional classification (based on Bell 1980, but with later additions)" (p. 734) is the tree's first `taxonomies` entry |

## 2. Node-by-node check

Three `taxonomies` entries correspond respectively to: (1) Table 3's
**Traditional classification** column, p. 734; (2) Table 3's **Revised
classification (this paper)** column, p. 734, elaborated by the "Emended
taxonomic definitions" prose, pp. 734–736; (3) the systematic-palaeontology
genus/species headings, pp. 736–753.

### Entry 1 — Traditional classification (p. 734)

| node | printed (p. 734) | verdict |
|---|---|---|
| `edrioasteroidea` (root) | table title only; no explicit rank/name line in this column (contrast entry 2, which prints "Plesion (Class) edrioasteroidea") | matches by editorial necessity; no printed line to check against |
| `stromatocystitida` | "Order **stromatocystitoida** Termier and Termier, 1969" | name as printed differs by one letter from the tree's key/`taxa.yaml` name (`stromatocystitida`); tree's `notes` explains the editor used Bell 1980 as authority instead of the printed citation — see §4 |
| `stromatocystitidae` | "Family stromatocystitidae Bassler, 1936" | matches (`taxa.yaml`: Bassler 1936) |
| `cambrasteridae` | "Family cambrasteridae Termier and Termier, 1969" | matches |
| `edrioasterida` | "Order **edrioasteroida** Bell, 1976" | name as printed differs by one letter from the key; not flagged or noted — cannot verify if genuine variant or OCR (§6) |
| `edrioasteridae` | "Family edrioasteridae Bather, 1898" | matches |
| `totiglobidae` | "Family totiglobidae Bell and Sprinkle, 1978" | matches |
| `isorophida` | "Order isorophida Bell, 1976" | matches |
| `lebetodiscina` | "Suborder lebetodiscina Bell, 1976" | matches |
| `lebetodiscidae` | "Family lebetodiscidae Bell, 1976" | matches |
| `carneyellidae` | "Family carneyellidae Bell, 1976" | matches |
| `isorophina` | "Suborder isorophina Bell, 1976" | matches |
| `hemicystitidae` (+ syn `isorophidae`) | "Family hemicystitidae Bassler, 1936 (= isorophidae' Bell, 1976)" | matches; printed apostrophe after "isorophidae" likely a scan artifact (§6) |
| `agelacrinitidae` | "Family agelacrinitidae Chapman, 1860" | matches |
| `openTaxon: isorophida-uncertain-suborder_bell.b.m_1976` | "Suborder uncertain" | matches in content and child order (pyrgocystidae, lispidecodidae, rhenocystidae); the key attributes the concept to Bell 1976, but this column's own header says "based on Bell 1980" and the family it contains (Rhenocystidae) is dated 1984, postdating even 1980 — cannot verify which Bell work coined "Suborder uncertain" (§6) |
| `pyrgocystidae` | "Family pyrgocystidae Kesling, 1967" | matches |
| `lispidecodidae` | "Family lispidecodidae Kesling, 1967" | matches |
| `rhenocystidae` | "Family rhenocystidae Holloway and Jell, 1984" | matches |
| `cyathocystida` | "Order cyathocystida Bockelie and Paul, 1983" | matches; `notes` on this node ("Credits Bockelie and Paul (1983), but they credit Bell...") makes a claim about Bockelie & Paul's *own* paper that cannot be checked from Smith 1985's text (§6) |
| `cyathocystidae` | "Family cyathocystidae Bather, **1899**" | matches this column, but see entry 2 below — Table 3's revised column prints 1898 for the same family |

### Entry 2 — Revised classification (pp. 734–736)

| node | printed (p. 734, definitions pp. 734–736) | verdict |
|---|---|---|
| `stromatocystites` (top level) | "Genus stromatocystites Pompeckj, 1896" | matches (correctly placed outside the Plesion) |
| `edrioasteroidea` `rank: Plesion` | "Plesion (Class) edrioasteroidea Billings, 1858" | matches; the "(Class)" parenthetical is not captured (no field for a dual/parenthetical rank) |
| `edrioasterida` | "Order edrioasterida Bell, 1976 **(sedis mutabilis)**" | **mismatch**: no `notes` or flag records "sedis mutabilis" on this node, though the trichotomy prose (p. 733) applies equally to all three orders |
| `totiglobidae` | "Family totiglobidae Bell and Sprinkle, 1978" | matches |
| `edrioasteridae` | "Family edrioasteridae Bather, 1898" | matches; paper states elsewhere (p. 733) that this family's diagnosis is expanded to admit *Walcottidiscus*, but no `emended: true` is set — see also §6 (no separate printed emended diagnosis for the family was found) |
| `isorophida` | "Order isorophida Bell, 1976 **(emend.) (sedis mutabilis)**" | **mismatch**: tree has neither `emended: true` nor a "sedis mutabilis" note; an emended diagnosis for "Order isorophida" is printed on p. 736 |
| `cambraster` | "Genus cambraster Cabibel, Termier and Termier, 1958" | matches |
| `edriodiscus` | "Genus **edriodiscus Smith, 1985**" | **misattribution in the source itself** — see §4; not captured either way since the node has no `auth`/`year`/`citedAs` |
| `cyclocystoididae` | "Family cyclocystoididae Miller, 1882" | matches |
| `agelacrinitidae` | "Family agelacrinitidae Chapman, 1860" | matches |
| `isorophinae` `modifier: nomen transl.` | "Subfamily isorophinae Bell, 1976" + emended definition (p. 736); `taxa.yaml` already notes "Explicitly re-ranked from suborder ... in 1985_smith.a.b" | matches |
| `lebetodiscinae` `modifier: nomen transl.` | "Subfamily lebetodiscinae Bell, 1976" + emended definition (p. 736); same `taxa.yaml` note | matches |
| `cyathocystida` `emended: true`, `notes: sedis mutabilis` | "Order cyathocystida Bockelie and Paul, 1983 (emend.) (sedis mutabilis)" | matches — the one order of the three where both flags are captured |
| `pyrgocystidae` | "Family pyrgocystidae Kesling, 1967" | matches |
| `cyathocystidae` | "Family cyathocystidae Bather, **1898**" | matches this column's printed year, but the traditional column (entry 1) and the running prose (p. 730: "placed in their own family Cyathocystidae by Bather (1899)") both say 1899 — internal inconsistency in the paper, tree records neither year (§4) |

### Entry 3 — Systematic palaeontology (pp. 736–753)

| node | printed | verdict |
|---|---|---|
| `stromatocystites` > `pentangularis_pompeckj_1896` `type: true` | "Type species. Stromatocystites pentangularis Pompeckj, 1896, by original monotypy." (p. 736) | matches; fixation mechanism ("by original monotypy") not captured |
| `walcotti_schuchert_1919` | "Other species. S. walcotti Schuchert, 1919." (p. 736), full redescription follows (pp. 741–743) | matches (placement only; redescription content not captured) |
| `balticus_jaekel_1899` `notes: Recommend treating as nomen dubium...` | "I recommend that S. balticus be treated as a nomen dubium" (p. 741, own subsection) | matches (paraphrase, not verbatim, but faithful) |
| `walcottidiscus` > `typicalis_bassler_1935` `type: true`, `synonyms: [magister_bassler_1936]` | "Type species. Walcottidiscus typicalis Bassler, 1935, by original monotypy." (p. 746); "W. magister is treated as a junior synonym of W. typicalis" (p. 743) | matches |
| `totiglobus` > `nimius_bell.b.m_sprinkle_1978` `type: true` | "Type species. Totiglobus nimius Bell and Sprinkle, 1978, by original designation." (p. 748) | matches; fixation mechanism not captured |
| `cambraster` > `cannati_miquel_1894` `type: true` | "Type species. Cambraster cannati (Miquel, 1894), by original designation." (p. 749) | matches; fixation mechanism not captured |
| `tastudorum_jell_burrett_banks_1985` | "Other species. C. tastudorum Jell, Burrett and Banks, 1985." (p. 749); own "Remarks" subsection (pp. 752–753), no full description ("This species has only recently been described by Jell et al. (1985)...") | matches |
| `edriodiscus` > `primotica_henderson_shergold_1971` `type: true` | "Type species. Cyclocystoides primotica Henderson and Shergold, 1971, by original designation." (p. 753) | matches; note the type species is cited in its *original* combination (under *Cyclocystoides*), consistent with the "original combination" ground rule; the recombination synonymy ("1985 Edriodiscus primotica (Henderson and Shergold); Jell, Burrett and Banks, p. 190", p. 753) is not captured (§3) |

### Phylogenies (cladogram)

| node | supporting prose | verdict |
|---|---|---|
| trichotomy of `edrioasterida`/`cyathocystida`/`isorophida` under `bracket: edrioasteroidea` | "the two other monophyletic sister groups... In the cladogram they are therefore placed in a trichotomy" (p. 731); "there are three subgroups forming a trichotomy in the cladogram (text-fig. 12)" (p. 733) | matches the topology described in prose |
| `edrioasteridae` bracket containing `walcottidiscus` alongside `(edriophus, edrioaster)` | "Walcottidiscus is taken as the primitive sister group here rather than Totiglobus since Walcottidiscus and edrioasterids share two advanced characters" (p. 729) | topology matches the prose, but the `bracket: edrioasteridae` label here spans a broader group than Family Edrioasteridae as formally defined (Edrioaster + Edriophus only, per Table 3) — see §4 |
| `isorophida` bracket: `cambraster` sister to a chain `edriodiscus` → `cyclocystoididae` → `agelacrinitidae` (`bracket`+`taxon: savagella`) → (`isorophinae`, `lebetodiscinae`) | "Cambraster, Edriodiscus, and isorophid edrioasteroids belong to the same clade" (p. 730); "cyclocystoids and isorophids are sister groups" (p. 731) | plausible per prose, but **cannot verify against the actual figure** — text-fig. 12 (p. 735) is an image page whose OCR is garbled (§6); see also §4 for the single-child chain encoding and the `savagella` exemplar, which belongs to a different, internal isorophid analysis (text-fig. 10, p. 730) |

## 3. Not captured

- **Genus and species synonymy lists**: 0 of 5 genus-level lists (4–14 lines each) and 0 of 7 species-level lists captured, except the single *typicalis*/*magister* relationship.
- **Diagnoses**: 0 of 5 genus diagnoses, 0 of 2 unique species diagnoses (pentangularis, walcotti — others read "As for genus"), 0 of 6 emended higher-taxon diagnoses (Plesion Edrioasteroidea, Order Edrioasterida, Order Cyathocystida, Order Isorophida, Family Agelacrinitidae, Subfamilies Isorophinae/Lebetodiscinae).
- **Type fixation mechanism**: 0 of 5 — every genus states "by original monotypy" (×2) or "by original designation" (×3); the tree has `type: true` but no fixation field (B14 in the roadmap covers this).
- **Specimens/material**: 0 of ~10 "Types"/"Material studied" paragraphs (repository numbers: BM(NH), USNM, MCZ, NYSM, CPC).
- **Occurrences**: 0 of ~10 "Stratigraphical age and distribution" paragraphs.
- **Illustrations**: 0 of text-figs 1–20 and Plates 87–89 assigned to specimens/nodes.
- **Recombination synonymy for *Edriodiscus primotica***: the transfer from *Cyclocystoides primotica* Henderson & Shergold, 1971 to *Edriodiscus primotica* (Jell, Burrett and Banks, 1985) (p. 753) is not recorded as a `synonyms`/`parents` pair on the systematic-section node.
- **"sedis mutabilis" on Edrioasterida and Isorophida** and **"(emend.)" on Isorophida** in the revised classification (p. 734) — see §2.
- **Attribution fields on classification nodes generally**: none of the ~50 taxon placements in the three `taxonomies` entries carry `auth`/`year`/`citedAs`, even though Table 3 prints a full authority string for every entry. Authority is available only indirectly, through the linked `taxa.yaml` record, which cannot show a printed attribution that disagrees with the record (see §4, the Edriodiscus and Cyathocystidae-year cases).
- **Repositories/abbreviations**: not applicable to this tree file (no material section), but the paper defines BM(NH), CPC, MCZ, NYSM, USNM (p. 753), none referenced.

## 4. Cases for the data model

1. **A source misattributing its own compilation table.** Table 3 (revised
   classification, p. 734) prints "Genus edriodiscus **Smith, 1985**", but the
   genus's own systematic-section heading, four pages later, prints "Genus
   edriodiscus **Jell, Burrett and Banks**, 1985" (p. 753), with the synonymy
   line "1985 Edriodiscus Jell, Burrett and Banks, p. 190." `taxa.yaml`'s
   `edriodiscus` record already sides with Jell, Burrett and Banks (`auth:
   [jell, burrett, banks]`, `year: 1985`), i.e., with the correct authorship.
   Because neither table nor genus-heading attribution is captured as
   `citedAs`/`auth`/`year` on either tree node, the paper's own internal
   contradiction about who erected this genus is invisible in the data. This
   is not quite B19 (a secondhand claim contradicting *its own* citation) — it
   is one source contradicting itself in two places, a variant worth naming.

2. **Two printed years for the same family in the same table.** Table 3 gives
   "Family cyathocystidae Bather, **1899**" in the traditional column and
   "Family cyathocystidae Bather, **1898**" in the revised column (both
   p. 734); the paper's own running prose says "placed in their own family
   Cyathocystidae by Bather (**1899**)" (p. 730). `taxa.yaml`'s `cyathocystidae`
   record uses 1899. This is the H-table case "two years for one cited work"
   (Schmidt 1879/1880) but for a taxon-authority year rather than a source
   year, and it happens within one table.

3. **The `editorial.source` pattern applies but isn't used.** The
   `stromatocystitida` node's authority is resolved to Bell 1980
   (`taxa.yaml`), while Table 3's traditional column prints "Order
   **stromatocystitoida** Termier and Termier, 1969" for the same slot. The
   tree records the reasoning only as free-text `notes` ("Termier and Termier
   1969 instead of Bell 1980, but AFAICT without seeing the full paper, it did
   not erect the formal latin taxon"). This is exactly the first case the
   Ground rules' "The `editorial` block" section describes — "the printed
   citation cannot resolve as printed... and the editor resolves it to this
   source record" — but recorded as prose rather than as a structured
   `editorial: {source: 1980_bell.b.m}` with the printed `citedAs` (Termier
   and Termier, 1969) preserved alongside it.

4. **"sedis mutabilis" applied unevenly.** Table 3 marks all three
   equal-ranked orders under the Edrioasteroidea trichotomy —
   Edrioasterida, Isorophida, Cyathocystida — "(sedis mutabilis)" (p. 734),
   matching the prose that "the three groups identified are best assigned
   equal rank" (p. 733). The tree records the marker as a `notes` string only
   on Cyathocystida. There is no dedicated field for "sedis mutabilis" (it
   currently rides on free-text `notes`, distinct from `provisional`, which
   is about placement doubt, not rank-order doubt among siblings). Given it
   recurs (three instances in this table alone), it may be a candidate for a
   named flag rather than ad hoc `notes` text, per the "a case earns a field
   when it appears in a second source" rule in §H.
   
5. **Cladogram bracket spanning more than the formally named family.** In the
   `phylogenies` cladogram, `bracket: edrioasteridae` contains
   `walcottidiscus` as well as `(edriophus, edrioaster)`, but Table 3's Family
   Edrioasteridae contains only *Edrioaster* and *Edriophus*; *Walcottidiscus*
   is placed directly in Order Edrioasterida, not in the family. The
   cladogram's use of the family name as a clade label for a larger group is
   defensible (the printed prose puts Walcottidiscus as sister to the
   family-level clade) but conflates a clade label with a formal rank name in
   a way the reader could mistake for a classification claim. Compare B18
   ("the same name at different ranks") — here it is the same name used at
   once for a formal family and for an informal, broader clade bracket in one
   tree.

6. **One `phylogenies` entry, apparently drawing on three printed
   cladograms.** The paper prints text-fig. 9 (the five Cambrian genera plus
   *Camptostroma*, p. 728, characters in Table 1), text-fig. 10 (Bell's
   Isorophida, internal relationships, p. 730, characters in Table 2), and
   text-fig. 12 (all edrioasteroid groups, p. 735, characters listed pp.
   734–735). The tree's single `phylogenies` entry has no `notes` identifying
   which figure it represents, and its `savagella` exemplar under
   `agelacrinitidae` (used to illustrate a primitive isorophid retaining a
   Cambraster/Edriodiscus-like marginal ring, p. 731) belongs to the
   text-fig. 10 analysis rather than the all-groups cladogram of text-fig. 12.
   A single merged `phylogenies` node risks conflating two distinct published
   figures without saying so.

7. **Type fixation as a printed, unrecorded fact.** All five "Type species."
   statements name the fixation mechanism explicitly ("by original monotypy"
   ×2, "by original designation" ×3, pp. 736, 746, 748, 749, 753). This is
   exactly B14's `typeFixation` field, not yet applied to this source.

8. **A definition the paper promises but does not print.** The Classification
   section (p. 733) states "it is only necessary to include *Walcottidiscus*
   here and expand the diagnosis for the family Edrioasteridae in
   consequence," implying Family Edrioasteridae is emended. The "Emended
   taxonomic definitions" section (pp. 734–736) prints definitions for the
   Plesion and both other orders/subfamilies but has no separate entry for
   "Family edrioasteridae" — the promised expanded family diagnosis is not
   actually printed anywhere found. Whether this is a gap in the published
   paper or an omission in the extracted text cannot be determined from this
   file alone (§6).

## 5. Source record check

`data/sources.yaml`, block `1985_smith.a.b`:

| field | sources.yaml | printed (p. 715, and receipt lines p. 756) | verdict |
|---|---|---|---|
| title | "Cambrian Eleutherozoan Echinoderms and the Early Diversification of Edrioasteroids" | "CAMBRIAN ELEUTHEROZOAN ECHINODERMS AND THE EARLY DIVERSIFICATION OF EDRIOASTEROIDS" | matches (case only) |
| journal | palaeontology | "Palaeontology, Vol. 28, Part 4, 1985, pp. 715-756, pls. 87-89." | matches |
| volume | 28 | 28 | matches |
| number | 4 | "Part 4" | matches |
| pages | 715–756 | 715–756 | matches; plates 87–89 (unpaginated, interleaved) are not separately recorded — likely out of scope for this field |
| pubDate.year | 1985 | 1985 | matches |
| processDates.received | 1984-10-07 | "Typescript received 7 October 1984" (p. 756) | matches |
| processDates.revised | 1985-03-25 | "Revised typescript received 25 March 1985" (p. 756) | matches |
| authors | smith.a.b | "by ANDREW B. SMITH" (p. 715); address "ANDREW B. SMITH, Department of Palaeontology, British Museum (Natural History)" (p. 756) | matches, single author |

No discrepancies found in the source record.

## 6. Uncertainties

- **Table 3's "Order stromatocystitoida" vs "Order edrioasteroida"** (traditional column, p. 734) each differ by one letter from the taxon keys/names used elsewhere in this paper and in `taxa.yaml` ("stromatocystitida", "edrioasterida"). Cannot verify from the extracted text whether this is a genuine printed variant spelling or an OCR scanno; the surrounding OCR is otherwise reliable for names and dates on this page.
- **The apostrophe after "isorophidae" in "(= isorophidae' Bell, 1976)"** (p. 734) is very likely an OCR artifact (stray quotation mark); cannot confirm without the scan image.
- **Cyathocystidae's year, 1899 vs 1898** (§4, item 2): cannot rule out that "1898" in Table 3's revised column is a digit-OCR error rather than a printed inconsistency, though 1899 is corroborated twice elsewhere in the same paper (traditional column and running prose, p. 730).
- **text-fig. 12 (p. 735)** is an image page; the OCR returns only fragmentary, reordered text ("Plesion (Class) Edrioasteroidea / Order Cyathocystida / Order Edrioasterida / Order Bsorophida..."), not a usable transcription of the figure's actual branching structure. The cladogram's node-by-node topology in §2 is inferred from surrounding prose, not verified against the figure itself.
- Pages with little to no OCR text, consistent with plates: PDF index 344 (Plate 87), 350 (Plate 88), 352 (Plate 89), matching the task's flagged set; PDF index 348 (p. 741, text-fig. 15 caption only) and 361 (p. 754, text-fig. 20 caption only) carry a small amount of caption text but no body prose.
- **The `notes` claims about other papers' content** — Cyathocystida node's note that "Bockelie and Paul (1983)... credit Bell based on establishment of suborder Cyathocystina, which they translated to an order" — describe Bockelie & Paul 1983's own text, not anything printed in Smith 1985. This cannot be verified from the file under review; it is corroborated by `docs/semantics-roadmap.md` B17, which independently documents the same claim about Bockelie & Paul 1983.
- **Whether "Suborder uncertain" is Bell's 1976 or 1980 term** (§2, entry 1): the openTaxon key attributes it to `1976_bell.b.m`, but this column's own header says "based on Bell 1980," and it contains Rhenocystidae (1984), which postdates both. Cannot verify from Smith 1985 alone which of Bell's works actually used the phrase "Suborder uncertain" for this grouping.
- **Whether Family Edrioasteridae actually received a printed emended diagnosis** (§4, item 8): not found in the extracted text of pp. 734–736; cannot confirm this is a true absence in the original publication versus an extraction gap.
