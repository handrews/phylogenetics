# Review: 2011_sumrall_zamora (Sumrall & Zamora 2011, Ordovician edrioasteroids from Morocco)

Page mapping: printed page = PDF page index + 424 (index 1 = p. 425, the
article's first text page; running heads confirm this at every checked
index, e.g. index 10 = p. 434 "Systematic palaeontology" masthead, index 25
= p. 449).

## 1. Coverage

| item | status | example |
|---|---|---|
| classification skeleton | all | both `edrioasteroidea` and `eocrinoidea` roots, all genera/species under Pyrgocystidae and Isorophina/Isorophidae/incertae sedis match pp. 434–450 headers |
| new taxa | all | 3 new genera, 8 new species all flagged `new: true` |
| type species | all | `type: true` correctly on all 4 new-genus type species (*matacarros*, *reboulorum*, *moroccoensis*, *inexpectatus*) |
| synonymy lists | none | Bell (1976b)'s synonymizing of 3 *Streptaster* species (p. 436) and the Chauvel-material review (pp. 425–426, incl. one nomen nudum) are not entered |
| material | none | no holotype/paratype numbers captured for any of the 8 new species (contrast with `2010_zhao...yaml`, entered the same year, which does capture specimens) |
| occurrences | none | Moroccan formation/locality data (pp. 435–451) not in tree |
| illustrations | none | Figs 9–23 not in tree |
| diagnoses | none | none of the printed diagnoses (pp. 435–450) in tree |
| phylogeny | all | Fig. 6 cladogram captured under `phylogenies`, with `treeType`, `methodology`, and internal `notes` on naming/rank discrepancies |

## 2. Correctness of what is captured

Classification (`taxonomies`): both trees' nesting and flags check out
against the Systematic palaeontology section (pp. 434, 445, 449) and
`taxa.yaml` ranks. Two attribution-year issues surface, but only because the
underlying names' printed years happen to be checkable against the paper's
own reference list — the tree itself carries no `auth`/`year` on any node, so
neither is visible as a tree-level "verdict" mismatch; both are reported as
findings for §3 instead. Node count check: 31 taxonomy nodes (`taxon`/`openTaxon` entries under
`taxonomies`), all identity/placement/flag matches bar the one spelling issue
below.

| node | printed (page) | verdict |
|---|---|---|
| `argodiscus` > `epilezorum_sumrall_zamora_2011` | "*Argodiscus **espilezorum*** sp. nov." (p. 440 and 8 further occurrences, pp. 425–437) | **mismatch** — see below |
| all other genus/species nodes | pp. 434–450 | match (30 further nodes checked; identity, `new`/`type`/`provisional` flags, and nesting all consistent with print and with `taxa.yaml`) |
| `chauveli_sumrall_zamora_2011` `provisional: true` | "*Belochthus? chauveli* sp. nov." (p. 437) | match — per the roadmap's own convention table, "?" *before the parent* name means placement-to-parent is tentative, i.e. `provisional`, which is exactly what is flagged (not `questionable`) |
| `hexedriocystis` `provisional: true` | "Eocrinoidea? Jaekel, 1918" heading directly above "Genus Hexedriocystis" (p. 449) | match, same convention: the "?" hedges the genus's assignment to the class, so `provisional` belongs on the child (`hexedriocystis`), which is where it sits |
| cladogram (`phylogenies`) terminal taxa | Fig. 6 caption + text (pp. 431–433): "Twelve ingroup taxa" plus Cambraster and the Kaili-biota edrioasteroid as outgroups | match on taxon sampling — the tree's cladogram has exactly 12 ingroup leaves (edrioaster, streptaster, argodiscus, belochthus, moroccopyrgus, lebetodiscus, carneyella, euryeschatia, isorophus, agelacrinites, anedriophus, isorophusella) plus the 2 outgroups (cambraster, kailidiscus); **internal branching order cannot be verified** — Fig. 6 is a photographic tree diagram, not extractable as text, so only the prose description (pp. 432–433) could be checked, and it is consistent with, but does not fully pin down, the yaml's exact topology |

**`epilezorum` spelling.** The species is printed "espilezorum" nine times
across the paper (abstract p. 425; captions and text pp. 426, 433, 434, 440,
441, twice on p. 441 alone) with no variant spelling anywhere. The tree uses
`taxon: epilezorum_sumrall_zamora_2011` (missing the "s"), and `taxa.yaml`'s
matching record (`epilezorum_sumrall_zamora_2011: name: epilezorum`) carries
the same error — this is a corpus-wide transcription slip, not a
one-off. Every occurrence in the source is unambiguous typeset text with no
ligature or scanning risk.

## 3. Cases for the data model

**Classification-with-partial-ranks *and* a cladogram, modelled separately
(owner's prompt).** The paper prints a classification (the Systematic
palaeontology section, pp. 434–450) that mixes rank words unevenly — "Family
Isorophidae Bell, 1976b" (p. 434) carries the word "Family," but
"Edrioasteroidea Billings, 1858," "Isorophida Bell, 1976b," "Pyrgocystidae
Kesling, 1967," and "Isorophina Bell, 1976b" (pp. 434, 439) do not, and most
(but not all: "Argodiscus Prokop, 1965," p. 439, omits it) genus headers
carry "Genus." It *also* runs a full cladistic analysis with a resulting
strict-consensus cladogram (Fig. 6, pp. 432–433) that is explicitly a
different structure from the classification — the text itself flags that the
figure's "Pyrgocystinae" (a subfamily-rank label used repeatedly describing
Fig. 6, pp. 432–433) is the same clade the classification calls
"Pyrgocystidae" (family rank, p. 433 and the systematic heading, p.
434). The data model keeps these as two separate top-level structures
(`taxonomies` vs. `phylogenies`), which is the right call — conflating them
into one tree would have to arbitrarily pick one rank label or invent a
correspondence the source itself only states informally. The tree's own
`notes: Labeled Pyrgocystinae here, Pyrgocystidae in syst. pal.` on the
cladogram's `pyrgocystinae` node records exactly this, correctly sourced to
the text (paraphrased, not quoted, but the underlying wording is a genuine
match: pp. 432–433 vs. p. 434). A second cladogram `notes` (`Presumably also
Isorophina as it fits nowhere else.`) is the editor's own inference about
where an unlabelled internal node belongs, not a printed statement; it reads
as reasonable but is an editorial judgement riding on a plain `notes` field
rather than the `editorial.inferred` block B20 defines for exactly this kind
of case.

**Two Hall dates for one genus, matching roadmap A11's own Hall case.** The
Systematic section prints "Genus Streptaster Hall, 1872" (p. 435), matching
this paper's own reference list (its only Hall entry: "Hall, J. 1872.
Descriptions of new species of Crinoidea... New York State Museum... Annual
Report, 24, 205–224"). But the same paper elsewhere cites the type species as
"Streptaster vorticellatus Hall, 1866" (Fig. 7 caption, p. 432). This is the
identical multi-printing pattern the roadmap's A11 already documents for
Hall (1866 advance print / 1871 advance print / 1872 Annual Report of the
same material) — this source reproduces it independently, citing the genus
to the 1872 printing and the type species to the 1866 one. Neither year is
captured on the tree's `streptaster` node (no `auth`/`year` fields anywhere
in this tree), so the discrepancy is invisible in the data as it stands, but
it is a ready-made second data point for A11 if that item is revisited.

**A printed year that may not match the record's authority.** "Genus
*Isorophus* Foerste, 1917" (p. 435) is repeated consistently, including in
this paper's own reference list ("Foerste, A. F. 1917. Notes on Cincinnati
fossil types..."). `taxa.yaml`'s `isorophus` record instead carries `year:
1916`. Per A6/A8, if the tree captured printed attribution, this would be a
straightforward claim ("Sumrall & Zamora 2011 credit *Isorophus* to Foerste
1917") sitting beside a record dated 1916 — worth a `citedAs`/`year` entry
plus an `editorial` note if the discrepancy holds up, once attribution
capture is added to this tree.

**A misspelling in the source's own figure captions, separate from the known
PBDB variant.** The type species is "*Hexedriocystis inexpectatus*"
throughout the running text (pp. 425, 428, 449–451, 7 occurrences) but is
printed "*H. inexpectis*" twice, in the captions to Figs 22 and 23 (p.
450–451). `taxa.yaml` already tracks one alternate spelling for this name
(`inexpectans_sumrall_zamora_2011`, noted "PBDB uses this spelling"), but
that is a different string from this paper's own "inexpectis," which is not
recorded anywhere (no record, no tree `notes`).

**An online-first date not captured, matching the H-table's own "online
first" row.** The cover page states "Published online: 03 May 2011," distinct
from "printed 15 September 2011" (both cited on the article itself, pp.
425). `sources.yaml`'s `2011_sumrall_zamora` records `received`, `accepted`
and `printed` but no `online` date, even though `processDates.online` is
noted elsewhere in the roadmap as already existing in the schema for this
exact situation.

## 4. Source record check

`sources.yaml`'s `2011_sumrall_zamora` matches: title verbatim, *Journal of
Systematic Palaeontology* vol. 9, issue 3, Sept. 2011, pp. 425–454, authors
Sumrall/Zamora, received 9 Nov 2009 / accepted 21 May 2010 / printed 15 Sept
2011 (all printed verbatim on p. 425), DOI matches. One gap, not a mismatch:
no `online` date recorded (see §3).

## 5. Uncertainties

The cladogram's exact internal branching order (Fig. 6) cannot be verified
from this text extraction — it is a photographic figure, and only its
caption and the surrounding prose description are available as text; the
prose is consistent with the tree's topology but does not establish every
node independently (flagged in §2). Diacritics throughout the reference list
and author affiliations (e.g. "Guti´errez," "Hünsuruck") are
extraction artefacts of accented characters, not scanning OCR, and do not
touch any name or date used in this review.
