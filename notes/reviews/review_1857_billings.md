# Review: 1857_billings

Source: Geological Survey of Canada, *Report of Progress for the Years 1853-54-55-56*,
"Report of E. Billings, Esq., for the year 1856," pp. 247-346 (this review covers only
the "Descriptions of New Fossils" section, pp. 256-295, and specifically the Asteriadae,
pp. 290-295).

**Page mapping.** Text file `1857-00-00-p.txt`, PDF page index *N* = printed page *N-15*
for the range checked (confirmed: index 305→290, 306→291, 307→292, 308→293, 309→294,
310→295; and index 271→256 for the start of "Descriptions of New Fossils"). Printed page
numbers are cited below, not PDF indexes.

## 1. Coverage

| Kind | Status | Example |
|---|---|---|
| Classification skeleton | all | Order/genus/species hierarchy for Crinoidea, Cystideae, Asteriadae matches the Contents page (p. xii) grouping exactly |
| New taxa (flagged `new`) | all | Every species and genus this report proposes carries `new: true` (e.g. `cyclaster`, `hybocrinus`, `carabocrinus`) |
| Type species | none | No type-species designation is printed anywhere in this report (pre-dates formal fixation practice) and none is captured |
| Synonymy lists | none | Billings cites no prior synonymy for any 1857 taxon in this report; the only "prior citation" style entries are page references to his own 1854 paper for non-new species (e.g. `multiporus_billings_1854`), and those are not modeled as `synonyms` |
| Material/specimens | none | Every species carries a printed "Collector.—" or discovery narrative (e.g. p. 293, Cyclaster found by Dr. Bigsby, redescribed by Billings); none is captured as a `specimens` entry |
| Occurrences | none | Every species carries a printed "Locality and Formation.—" line (e.g. p. 293 "Trenton limestone. City of Ottawa."); none is captured |
| Illustrations | not applicable | This printing of the 1856 report carries no plates for these species; the plates appear only in the 1858 *Figures and Descriptions* reprint (see `1858b_billings` review) |
| Diagnoses | none | Full generic-characters and species "Description.—" paragraphs are printed for every taxon (e.g. p. 292 "Generic characters.—Body sessile, circular, discoid..."); none is captured in a `diagnosis` field |
| Phylogeny | not applicable | Only a taxonomy is printed; no diagram or cladogram |

Beyond the classification skeleton and the `new` flags, nothing else this report prints
(diagnoses, material, occurrences) is captured. This matches the project's early-scope
pattern (roadmap G9): this is one of the earliest sources entered.

## 2. Correctness

70 taxon nodes in the tree. Genus-level placement and the presence/absence of the `new`
flag were checked against the printed headings wherever the OCR was legible; 58 nodes
matched cleanly (all crinoid genera Glyptocrinus, Thysanocrinus/Rhodocrinus, Dendrocrinus,
Heterocrinus, Hybocrinus, Carabocrinus, Cleiocrinus, Lecanocrinus; all cystid genera
Glyptocystites, Pleurocystites, Amygdalocystites; and the Cyclaster/Agelacrinites nodes
below). Mismatches and unverifiable nodes are reported in full below.

### Mismatches

| Node | Printed (page) | Verdict |
|---|---|---|
| `stellata_billings_1857` (under `palæaster`) | "PALŒASTERINA STELLATA" (p. 290) | **Mismatch.** Printed under genus *Palæasterina*, not *Palæaster*. |
| `rigidus_billings_1857` (under `palæaster`) | "PALiEASTERINA RIGIDUS" (p. 291) | **Mismatch.** Printed under *Palæasterina*. |
| `rugosus_billings_1857` (under `palæaster`) | "PALJEASTERINA RUGOSUS" (p. 291) | **Mismatch.** Printed under *Palæasterina*. |
| `pulchellus_billings_1857` (under `palæaster`) | "PALÆASTER PULCHELLUS" (p. 292) | Match — this is the one species actually printed under *Palæaster*. |
| `palæasterina` node, `notes: "Noted from other source, but no new species described."` | pp. 290-291 print three new species (*stellata*, *rigidus*, *rugosus*) directly under this genus heading | **Mismatch.** The note is contradicted by the three species above; they belong here, not under *Palæaster*. |
| `auctidactylus_billings_1857` | OCR reads "D. acutidactylus" / "D. acutidactyTus" (p. 267) | **Cannot verify spelling with confidence** (OCR ambiguity between "au" and "ac"), but the OCR reading and the word's evident etymology (Latin *acutus*, "sharp," matching the description "exceedingly thin and sharp on the back") both point to *acutidactylus*, not *auctidactylus*. Worth checking against the original plate/scan. |

So three placement errors and one contradicted note, all in the same small cluster
(Palæaster/Palæasterina), plus one taxon-key spelling that cannot be confirmed but is
probably wrong.

### Cannot verify

| Node | Issue |
|---|---|
| `gregarius_billings_1857`, `conjugans_billings_1857` | Species headings not locatable in this OCR text; *conjugans* is mentioned only in passing in the *rusticus* description ("like that of D. con/ugans", p. 269), which confirms the name and implies an earlier heading, but that heading itself could not be found. Genus and `new` flag not independently verified. |
| `porocrinus` and `conicus_billings_1857_porocrinus` | Genus listed on the Contents page (p. xii) as one of the nine Crinoidea genera in this section, but no legible heading for it was found in the OCR between pp. 277-290. The "(new genus.)" annotation seen for the other new 1857 genera (Hybocrinus, Carabocrinus, Cleiocrinus) could not be checked for Porocrinus. |
| `priscus_billings_1857` | Heading printed as bare "PRISCUS." (p. 256), i.e. the genus name is not repeated — the "Genus GLYPTOCRINUS" header and generic characters presumably sit on p. 255, outside the range read for this review. Cannot confirm the genus-level heading or its authorship line. |
| `lacunosus_billings_1857` | Named only in a summary paragraph ("I have met with G. !acunosus...", p. 256); no distinct species heading with its own description was located. |
| `comarocystites` node, `notes: "Citation says p. 227 but actually p. 268"` | The printed genus citation reads (OCR) "(Canadian Journal, vol. 2, page 327.)" (p. 288). "327" is plausibly an OCR misreading of "227" (2/3 confusion is common in this scan), which would match the editorial note's "p. 227." The note's corrected page, 268, cannot be checked against the Canadian Journal itself from this text. |

## 3. Cases for the data model

**Subgenus in parentheses, both at genus and species rank.** Page 261: "Genus
THYSANOCRINUS (Hall), RHODOCRINUS (:Miller)" — the genus and its subgenus are given
together, each with its own author in parentheses. Page 263: "THYSANOCRINUS
(RHODOCRINUS) MICROBASALIS" — the species heading itself carries the standard
parenthetical subgenus notation. The tree already nests `rhodocrinus-subgenus` under
`thysanocrinus` with the two species below it, which is the right shape, but nothing
records that the printed species heading actually reads "Thysanocrinus (Rhodocrinus)
microbasalis" with the subgenus name parenthesized between genus and species — the
`citedAs`-style exact-as-printed form (Ground rules, Attribution) isn't captured
anywhere in this tree; none of its ~70 nodes carry `auth`/`year`/`citedAs`.

**Two different printed authority styles for the same set of names, one paper apart.**
This report (1857) never appends an author name to Billings's own new taxa (e.g. "Genus
CYCLASTER." / "CYCLASTER BIGSBYI." with no author at all) but does append "(Author.)"
to genera he is merely using: "Genus HETEROCRINUS, (Hall.)", "HETEROCRINUS SIMPLEX,
(Hall.)", and marks his own new genera "(new genus.)": "Genus HYBOCRINUS, (new
genus.)", "Genus CARABOCRINUS (new genus)." The very same names one paper later
(`1858b_billings`, decade III) are printed with "Billings" appended directly even to
his own new taxa ("Genus EDRIOASTER, Billings.", "VIII. Edrioaster Bigsbyi, Billings.").
Neither tree captures either convention in an `auth`/`citedAs` field. This is a case for
A1/A2 (roadmap section A): the exact printed attribution form differs source to source
for what is otherwise the same nomenclatural act, and the model has a field for exactly
this (`citedAs`) that is unused here.

**A genus-and-species-level "(new genus.)" marker used consistently, unmodeled.**
Every genus this report newly proposes prints its own explicit tag: "(new genus.)"
for Hybocrinus, Carabocrinus, Cleiocrinus. The tree's `new: true` flag captures the
fact correctly, but the printed wording itself ("new genus," not simply asserted by
omission) is a small, recurring, exact phrase that could be preserved in `citedAs` or
`notes` the way other exact-as-printed conventions are meant to be (Ground rules:
"Attribution is written the way the literature writes it").

**Genus *Cyclaster*: no authority at all is printed**, consistent with the paper's
"new: no author needed" convention above — recorded correctly by the tree as `new: true`
with no `auth` field, which is the right absence (nothing to capture).

## 4. Source record check

`sources.yaml` block for `1857_billings`: `book: geo-survey-canada`, `chapter: "Report
of E. Billings, Esq., for the year 1856"`, `pages: [247, 346]`, `pubDate.year: 1857`,
`authors: [billings]`. All of it matches the printed Contents entry exactly: "Report of
E. BILLINGS, Esq., for the year 1856, . . . 247" as the chapter's start page, with the
next chapter ("Report of T. STERRY HUNT, Esq., for the year 1853") beginning at printed
page 347 — i.e. Billings's report runs 247-346, matching the record's page range.

## 5. Uncertainties

- OCR of the æ ligature is unreliable throughout ("PALŒASTERINA" / "PALiEASTERINA" /
  "PALJEASTERINA" all appear for the same word); genus-name spellings quoted above should
  be checked against the original plates where they matter.
- Several species headings (Porocrinus and its species, *gregarius*, *conjugans*, the
  Glyptocrinus genus header itself) could not be located in this scan; see "Cannot
  verify" above. Their absence from this review is a scan-quality gap, not a claim that
  the tree is wrong about them.
- The Comarocystites citation-page discrepancy (327/227/268, above) is noted but not
  resolved; the editorial correction already on the node may well be right, but this
  review cannot independently confirm "268" from the available text.
