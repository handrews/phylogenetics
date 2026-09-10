# Review: 1842_conrad.t.a (Conrad, "Descriptions of new Species of Organic Remains belonging to the Silurian, Devonian, and Carboniferous Systems...")

## Page mapping

The 414-page scan holds the whole *Journal of the Academy of Natural Sciences
of Philadelphia*, Vol. VIII, Part II. This Conrad paper's title ("Descriptions
of new species of Organic Remains belonging to the Silurian, Devonian, and
Carboniferous systems of the United States. By T. A. Conrad.") appears
mid-page at PDF index 266, on printed page **235** — the tail of the preceding
Conrad paper ("Observations on the Silurian and Devonian systems...", printed
pp. 228–234, "Read January 18, 1842") occupies the top of that same page. From
there: **printed page = PDF index − 31**, holding through index 311 (printed
280), where this paper ends mid-page and Audubon & Bachman's "Descriptions of
New Species of Quadrupeds..." begins. Running head throughout this paper's
span (pp. 235–280) is "SILURIAN AND DEVONIAN SYSTEMS, ETC." — unchanged from
the previous article, and not updated to mention Carboniferous. The "Explanation
of Plates, Volume VIII" (covering the whole part, printed as a two-column
table) sits later in the volume at printed pp. 353–354 (index 384–385); it is
not part of this paper's own pagination.

Verified directly against page images in `conrad_png/` (a clean typeset
reprint, not the raw OCR) for pp. 235, 278, 279, 280, confirming every
reading below; the crinoid section (pp. 278–280) was cross-checked
word-for-word against `p53.png`, `p54.png`, `p55.png`.

## 1. Every echinoderm entry

The paper treats echinoderms in one short run under the bare heading
"CRINOIDEA." (p. 278), following the trilobite genera and preceding the end
of the paper. All three genera and species are Conrad's own, presented here
for the first time; none carries an explicit "new genus"/"n. s." marker
(true of the whole paper — no species anywhere in it is so marked; "new" is
carried only by the title).

| Printed page | Heading (as printed) | First sentence of description | Locality/formation | Plate/fig. | Tree node |
|---|---|---|---|---|---|
| 278 | `CRINOIDEA.` (bare group heading, no rank word) | — (heading only) | — | — | `crinoidea-family` (root) |
| 278–279 | `STEPHANOCRINUS, Conrad.` | "This singular fossil may be described as having five sides, each of which is depressed and angulated, the angles profoundly carinated; three of the sides with an oblique carina; three longitudinal articulations only are visible; ambulacra on the upper surface and five in number; from the margin proceed five elevated, angular, spiniform processes; pelvis or base triangular, with a cavity where the column unites with it; canal probably pentangular, and very small." | — (genus, no locality) | — | `stephanocrinus` |
| 279 | `STEPHANOCRINUS angulatus.` | "Surface rugose and tuberculated, ambulacra large, covering the whole summit, which is flattened; coronal processes proceeding from between the ambulacra and carinated on the back." | "Lockport, in Niagara shale. Middle Silurian." | Pl. 15, fig. 18 | `angulatus_conrad.t.a_1842` |
| 279 | `ICTHYOCRINUS, Conrad.` (printed without the second "h" — see §6) | "Column round, smooth; canal small and round; scapulae with the margins of the articulations parallel, and somewhat imbricated." | — (genus, no locality) | — | `ichthyocrinus` |
| 279–280 | `ICTHYOCRINUS lævis.` | No morphological diagnosis is given; the only text after the locality is the etymological remark: "There is much resemblance in the markings of this fossil to the scales of a fish, whence the generic name is derived." | "Lockport, New York, in Niagara shale." | Pl. 15, fig. 16 | `lævis_conrad.t.a_1842` |
| 280 | `NUCLEOCRINUS, Conrad.` | "This genus differs from Pentremites, Say, in having only one perforation at top, which is central." | — (genus, no locality) | — | `nucleocrinus` |
| 280 | `NUCLEOCRINUS elegans.` | No morphological diagnosis; only sentence given is locality/collector: "Found by Mr. Hall in the western part of New York, in Upper Silurian shale." | "the western part of New York, in Upper Silurian shale" | Pl. 15, fig. 17 | `elegans_conrad.t.a_1842` |

All three species figures (16–18) are confirmed present on Plate XV in
`conrad_png/p65.png`, matching the "Explanation of Plates" listing (p. 354)
and matching their printed diagnoses: fig. 16 shows a fan-shaped calyx with
bifurcating radial ribs (matching *Icthyocrinus*'s "costal ridges, bifurcating
three times"); fig. 18 shows a small pointed theca with a jagged, crenulate
crown (matching *Stephanocrinus*'s "coronal processes... carinated"); fig. 17
is a small ribbed oval (consistent with, though not diagnostic of, the small
*Nucleocrinus* theca).

No other echinoderm content (no synonymy, no comparative material beyond the
one-line genus contrasts quoted above, no additional occurrences) appears
anywhere else in the paper; the earlier "Table of systems" (p. 234, in the
*preceding* Conrad paper) lists "Crinoidea" only as a bare faunal-list entry
under "Genera of Crustacea. Shells." with no species named, and belongs to
that other article, not this one.

## 2. Correctness of every tree node

| Tree node | Printed (page) | Verdict |
|---|---|---|
| `crinoidea-family` (root), notes "Rank is a guess" | "CRINOIDEA." (p. 278) — a bare section heading, no rank word ("Class," "Family," "Order," etc.) stated anywhere near it | Correct. The note accurately reflects that Conrad assigns no rank at all; "guess" is the right characterization, not an error to fix. |
| `stephanocrinus`, `new: true` | "STEPHANOCRINUS, Conrad." (p. 278), first description, no prior usage | Correct. Genus and attribution match; `new: true` is the right call even though no "n. g." is printed (see §6). |
| `angulatus_conrad.t.a_1842`, `new: true`, under `stephanocrinus` | "STEPHANOCRINUS angulatus." (p. 279) | Correct. |
| `ichthyocrinus`, `new: true` | "ICTHYOCRINUS, Conrad." (p. 279) | Identity/placement/attribution/year correct. The taxon key and record spelling ("Ichthyocrinus") do not match what Conrad printed ("Icthyocrinus," missing the second h) — see §6, this is a printed-form gap, not a wrong identification. |
| `lævis_conrad.t.a_1842`, `new: true`, under `ichthyocrinus` | "ICTHYOCRINUS lævis." (p. 279–280) | Correct; species epithet spelling with the æ ligature matches the print exactly (confirmed against the page image, not just OCR). |
| `nucleocrinus`, notes "This genus differs from Pentremites, Say, in having only one perforation at top, which is central." | "NUCLEOCRINUS, Conrad." (p. 280): "This genus differs from Pentremites, Say, in having only one perforation at top, which is central." | Correct, quoted verbatim (case-normalized only). |
| `elegans_conrad.t.a_1842`, `new: true`, under `nucleocrinus` | "NUCLEOCRINUS elegans." (p. 280) | Correct. |

No mismatches. Every node's identity, rank (or absence of one), placement,
`new` flag, and quoted note checks out against the printed text; the one
finding worth carrying forward is the `ichthyocrinus` printed-spelling gap
in §6, which is a missing `citedAs`-type fact rather than a wrong node.

## 3. The Vanuxem questions

Checked across the full paper (not just the crinoid section) by searching
for every relevant string ("hallii," "gebhardi," "Encrinite*," "Lepocrinite*"
and their OCR variants); none occurs anywhere in this Conrad paper outside
the crinoid section quoted above.

**(a) Is *Nucleocrinus hallii* named or described anywhere in this paper?**
No. The only species Conrad places in *Nucleocrinus* in this paper is
*elegans* (p. 280). The epithet "hallii" does not appear anywhere in the
paper.

**(b) Is *Lepocrinites gebhardi* here?**
No. Neither "Lepocrinites" nor "gebhardi" appears anywhere in the paper. (A
"John Gebhard, Jr." is thanked as a collector for an unrelated trilobite,
*Calymene camerata*, p. 278 — not connected to any crinoid.)

**(c) Is any *Encrinites lævis* here, as distinct from *Ichthyocrinus
lævis*?** No. The genus name "Encrinites" does not occur anywhere in this
paper. The only "lævis" in the paper is *Icthyocrinus lævis* (p. 279–280).

**(d) How does Conrad head *Nucleocrinus* and which species does he place in
it?** He heads it exactly as "NUCLEOCRINUS, Conrad." (p. 280) — his own new
genus, with no other author cited — and diagnoses it only by contrast with
*Pentremites*, Say (one perforation at top, central). He places exactly one
species in it: *elegans* (p. 280), collected by "Mr. Hall in the western part
of New York, in Upper Silurian shale."

**Plainly stated:** this paper is the place *Nucleocrinus* (genus) and
*Nucleocrinus elegans* (species) are described. It is **not** the place
*Nucleocrinus hallii* is named, and *hallii* is not mentioned in it at all.
If Vanuxem's 1842 "Nucleocrinus hallii" (p. 163, citing "the Reports, etc. of
T. A. Conrad") predates this paper's actual appearance, it would be a nomen
nudum citation of a genus name apparently supplied to Vanuxem by Conrad in
advance of, or independent from, this formal description — but nothing in
this paper itself supports or resolves that; it simply never mentions
*hallii*, Vanuxem, or "the Reports." The `nucleocrinus` taxon record's own
note ("Possibly first published in 1842_vanuxem") is a fair question to have
flagged, not something this paper settles either way — resolving it needs
Vanuxem's actual text and the two works' relative publication dates, which
this review's source materials do not include.

## 4. Source record check

`sources.yaml` `1842_conrad.t.a`: title, journal (JANSP), volume 8, number 2
(printed "VOLUME VIII. PART II."), pages 235–280, year 1842, author
`conrad.t.a` — all confirmed against the scan. One cosmetic note: the title
as given in `sources.yaml` ("Descriptions of new Species of Organic Remains
belonging to the Silurian, Devonian, and Carboniferous Systems of the United
States") matches the capitalization used on the volume's **Contents** page
(index 201) exactly; the article's own drop-in title line (p. 235) instead
reads "Descriptions of new species of Organic Remains belonging to the
Silurian, Devonian, and Carboniferous systems of the United States" (lower-case
"species," "systems"). Both are printed forms of the same title in the same
volume; not a discrepancy to fix, just noting which rendering the record
follows. No month/day of publication is stated anywhere for this Part; the
companion paper immediately before it is dated "Read January 18, 1842," but
this paper carries no read-date of its own.

## 5. Uncertainties

- All OCR-uncertain readings in the crinoid section that mattered ("Lockport"
  vs. raw-OCR "Wockport"; "New York" vs. raw-OCR "DES York"; "lævis" vs.
  raw-OCR "levis") were resolved by checking the clean page-image reprint
  (`conrad_png/p53.png`–`p55.png`) rather than the raw OCR text, and all
  confirmed the readings given above. Nothing in this section remains
  "cannot verify."
- One spelling is now *reported*, not merely OCR noise: the genus is printed
  "ICTHYOCRINUS" (no second h) both in-text (pp. 279–280, twice) and in the
  Explanation of Plates (p. 354) and the volume index (p. 348) — the same
  spelling appears independently in the raw OCR and the clean reprint, so
  this is very unlikely to be a scanning error. Whether Conrad's spelling is
  the original orthography (with "Ichthyocrinus" a later, if long-standard,
  emendation) or a compositor's slip is outside this review's scope to
  adjudicate; it is reported as printed.
- The plate identification of fig. 17 (*Nucleocrinus elegans*) is visually
  plausible but not certain from the low-resolution scan alone; figs. 16 and
  18 match their printed diagnoses closely enough to be confident.

## 6. Note for the data model

- **A genus-name spelling the record doesn't carry.** Conrad prints the
  genus twice in-text and twice more in the back matter as "ICTHYOCRINUS"
  (missing the second h), never as "Ichthyocrinus." `taxa.yaml`'s
  `ichthyocrinus` record carries only the now-standard spelling, with no
  `citedAs`/`altSpellingOf` link to the form Conrad actually printed — the
  one case in this paper where the identity record and the printed page
  diverge in spelling, not just in rank or placement.
- **A bare, unranked group heading.** "CRINOIDEA." (p. 278) carries no rank
  word at all — not even the informal "Genus"/"Order" Conrad uses elsewhere
  in the same paper (e.g. "GENUS VESPERTILIO" two pages later, in the
  Audubon paper). This is the same shape of problem as roadmap G8 (rank
  stated in the tree, not the record); the tree's own "Rank is a guess" note
  on `crinoidea-family` is the right call.
- **Monotypic genera with no species-level diagnosis.** For both
  *Icthyocrinus lævis* and *Nucleocrinus elegans*, the entire morphological
  content sits in the genus paragraph; the species entry supplies only a
  locality (and, for *Icthyocrinus*, an etymological aside) — there is no
  independent species diagnosis to distinguish the species from a
  hypothetical congener, because none is described. `diagnosis` on these two
  species nodes, if ever populated, would have nothing printed to draw on
  beyond the genus paragraph.
- **Coverage is skeleton-only, and that is expected for this source's entry
  date** (roadmap G9): no node carries `pages`, `illustrations` (despite
  every species citing a plate and figure number), `auth`/`year`/`citedAs`,
  or `diagnosis`. This is a gap to fill later, not an error now.
