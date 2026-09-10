# Audit: 1852_hall (Hall, Palæontology of New-York, vol. 2)

Tree file: `data/trees/1852_hall.yaml` (221 lines, both `taxonomies` entries read in full).
Source text: whole-volume OCR, `1852-00-00-p.txt`.

## 1. Page-index mapping

**Window A (PDF 255–265).** Printed page = PDF index − 19, confirmed by running heads/page
numbers at every step (PDF255="236" ... PDF265="246") and cross-checked as far as PDF290="271"
(`Atrypa reticularis`, offset still holds: 290−19=271). This window covers Hall's Cystideæ
(*Callocystites* 238–241, *Apiocystites* 242–244, *Hemicystites* 245–246) and the opening of
Asteriadæ (*Palæaster* 247), i.e. only the **tail end** of the tree's second `taxonomies` entry.
The bulk of that entry's crinoid genera (*Homocrinus* through *Calceocrinus*, printed pp.
179–233 per the general index) fall **outside** this window and were not directly read; a few
(*Eucalyptocrinus*, *Melocrinites*, *Myelodactylus brachiatus*, *Glyptaster brachiatus*) were
independently located and read via targeted `grep` because the assignment's specific check-items
required them.

**Window B (PDF 374–380).** Offset is *not* a simple constant here and should not be
extrapolated. PDF374 prints "300" (Additions and Corrections, "NOTE C"), but PDF371 — three
pages *earlier* in the scan — prints "302", and the same page numbers 297/298/300/302/304 recur
**twice** in the file: once (PDF ~283–305) as the main-text Brachiopoda/*Atrypa* treatment, and
again (PDF ~365–374) inside the "Additions and Corrections" section, which reuses that same
page-number range for its own leaves. So pages in the high-200s/low-300s are **not unique**
identifiers in this volume without knowing which pass (main text vs. addenda) is meant. From
PDF375 onward (General Index, then List of Plates) most leaves carry no reliably OCR'd folio at
all — locate content there by the printed genus/page citations inside the index itself (e.g.
"HEMICYSTITES ... 245; parasitica ... 246"), not by PDF-index arithmetic. This is almost
certainly a normal feature of a composite 19th-century monograph (originally issued/assembled in
installments with locally-restarted or plate-interleaved pagination), not a scan defect specific
to this copy.

Title page (PDF index 12): "PALÆONTOLOGY / NEW-YORK. / VOLUME II. ... BY JAMES HALL. / ALBANY: /
PRINTED BY C. VAN BENTHUYSEN. / 1852." — confirms book, volume, year, author (see §5).

## 2. Coverage

| Kind | Extent | Example |
|---|---|---|
| Classification skeleton | Partly | Two disjoint `taxonomies` entries (Clinton / Niagara), each with family→genus→species nesting; ranks above family are guessed (`notes: "rank is a guess"`) |
| New taxa (`new: true`) | All flagged nodes are genuinely printed as "(nov. gen.)"/"(n. sp.)" **except** two outliers — see §4 | *Callocystites* "(nov. gen.)", p.238 |
| Type species | None captured explicitly | no `type` flags present anywhere in file |
| Synonymy lists | Partly | *decorus*/*cælatus* correctly carry `parents: hypanthocrinites`; most Niagara genera carry no synonymy at all (many genuinely have none in Hall) |
| Material/specimens | None captured (no `specimens` fields) | collections are named in running text ("Collection of Col. Jewett") but not transcribed into the tree |
| Occurrences | None captured (no `occurrences` fields) | locality prose ("shale... at Lockport") present in text, absent from tree |
| Illustrations | Partly | *Callocystites jewettii*, *Apiocystites elegans*, *Hemicystites parasitica* all captured with plate+figs; *Palæaster niagarensis* has **none** despite the text giving Pl. LI figs. 21–23 (and even an addenda extension to figs. 21–28 + Pl. LXXXV figs. 8–10) |
| Diagnoses | None captured (no `diagnosis` fields) | Latin/English diagnoses are lengthy in the source; tree relies on `notes` only for the handful of comparative remarks it does capture |
| Phylogeny | None (`phylogenies` key absent/empty) | no cladogram in this source; consistent with a purely descriptive systematic monograph |

Per G9, all of the "None"/"Partly" rows above are scope, not error — this is the first systematic
pass over Hall vol. 2 and material/occurrence/diagnosis capture was evidently out of scope for
this entry.

## 3. Correctness table

Verified rows (direct text quotes) and flagged rows are given in full; clean, taxa.yaml-
consistent rows that fall outside the two windows and were not independently checked are
summarised as a count at the end.

| Node | Printed (page) | Verdict |
|---|---|---|
| `callocystites` | "Genus CALLOCYSTITES (nov. gen.)" p.238 | Match |
| `jewettii_hall_1852` | "1. CALLOCYSTITES JEWETTII (n. sp.)" p.239, "Pl. L. Figs. 1–11" | Match |
| `jewettii-var_hall_1852` (openTaxon, `questionable: true`) | Same plate heading continues: "Figs. 1-11; **and 12-16 var.?**" p.239; described only inside fig.12's caption ("An individual having a slightly different form... in other respects having the same arrangement of parts... with the exception of the arms") — no separate name or diagnosis given | Match — `questionable: true` is directly justified by Hall's own "var.?" hedge; correctly modeled as an unnamed, hedged variant (not a named variety) |
| `apiocystites` | "Genus APIOCYSTITES (Forbes)." p.242 — genus attributed to Forbes, not new | Match (tree correctly omits `new: true` here) |
| `elegans_hall_1852` | "1. APIOCYSTITES ELEGANS (n. sp.)" p.243, Pl. LI figs. 1–17 | Match |
| `hemicystites` | "Genus HEMICYSTITES (nov. gen.)" p.245 | Match — see §4 for the Agelacrinites synonym itself |
| `parasitica_hall_1852` | "HEMICYSTITES PARASITICA." p.246 (no "(n. sp.)" suffix in the heading) | `new: true` is not directly tagged in the printed heading, but is reasonable since it is the sole species under a genus explicitly marked "(nov. gen.)" — weaker than a direct tag but not a mismatch |
| `parasitica_hall_1852` illustrations `[[18,20], "20†"]` | "Figs. 18, 19, 20 and 20†." then individually captioned "Fig. 18.../Fig. 19.../Fig. 20.../Fig. 20†. A still farther enlargement..." p.246 | Match — see §4, the dagger is genuinely printed, not an OCR artifact |
| `palæaster` | "Genus PALÆASTER (nov. gen.)" p.247 | Match |
| `niagarensis_hall_1852_palæaster` | "1. PALÆASTER NIAGARENSIS (n. sp.)" p.247, Pl. LI figs. 21–23 | Match on `new: true`; but tree captures **no** `pages`/`illustrations` at all for this node — coverage gap (see §2) |
| `eucalyptocrinus` (`new: true`) | "Genus EUCALYPTOCRINUS." (no "nov. gen." tag) with printed synonymy "*Eucalyptocrinites*, Goldfuss, 1826." / "*Hypanthocrinites*, Phillips, 1839." — Hall's own text: "there is no sufficient character to separate it from the Genus Hypanthocrinites" | **Mismatch.** Hall presents this as reconciling two pre-existing genera, not originating one; `data/taxa.yaml` already agrees (`eucalyptocrinus: altSpellingOf: eucalyptocrinites`, no `authority.source: 1852_hall`) — the taxa record and the tree's `new: true` flag contradict each other |
| `decorus_phillips.j_1839` | "1. EUCALYPTOCRINUS DECORUS." (no "n. sp."), synonymy "*Hypanthocrinites decorus.* Phillips: Murchison, Sil. System, 1839, pag. 672, pl.17, fig.3. — Hall, Geol. Rep. 4th Dist. N.York, 1843, pag.113, figs.2 and 8." | Match — correctly not `new: true`; `parents: hypanthocrinites` correct |
| `cælatus_hall_1843` | "2. EUCALYPTOCRINUS CÆLATUS." (OCR: "C/ELATUS"), synonymy "*Hypanthocrinites celatus.* Hall, Geol. Rep. 4th Dist. N.York, 1843, pag.113, fig.1." | Match — correctly not `new: true`; `parents: hypanthocrinites` correct |
| `decorus_phillips.j_1839` notes ("Compare f7. celatus. Ip. pag. 113, fig. 1; and pl. 47 ut sup. fig. 4 a.") | Printed line, verbatim in the OCR: "Compare f7. celatus. Ip. pag. 113, fig. 1 ; and pl. 47 ut sup. fig. 4 a." | **OCR artifact, not print** — see §4. Hall almost certainly printed "Compare *E.* cælatus. *Id.* pag. 113, fig. 1..." ("E." = Eucalyptocrinus, "Id." = idem/same author). The tree's note reproduces the OCR misreading rather than the text |
| `papulosus_hall_1852` | "2. EUCALYPTOCRINUS PAPULOSUS (n. sp.)" p.211 | Match on `new: true` |
| `papulosus_hall_1852` notes ("Compare Lucalyptocrinus decorus, ut supra.") | Printed line, verbatim in the OCR: "Compare Lucalyptocrinus decorus, ut supra." | **OCR artifact, not print** — see §4. "Lucalyptocrinus" is an OCR misread of "*E.* [Eucalyptocrinus]"; every other instance of the genus name in this text OCRs correctly as "EUCALYPTOCRINUS" |
| `caryocrinus` (2nd occurrence) notes (Troost's five Tennessee species) | "Prof. Troost has enumerated five species as occurring in Tennessee: these are the Caryocrinus meconideus, C. hexagonus, C. granulatus, C. insculptus, C. globosus..." p.227 | Match — quoted essentially verbatim; correctly kept as prose in `notes`, no taxa/nodes fabricated for Troost's species (consistent with the "material entry notes" pattern rather than `children`) |
| `melocrinites` notes (Goldfuss comparison) | "Genus MELOCRINITES (Goldfuss)." ... "Melocrinites hieroglyphicus, and M. lævis, Goldfuss, Petrefacta Germania, Vol. i, pag. 197, pl. lx, figs. 1 and 2." p.226–227 | Match (OCR shows "levis"; tree correctly restores the "lævis" ligature) |
| `sculptus_hall_1852` (`new: true`) | "1. MELOCRINITES SCULPTUS." p.228 — **no** "(n. sp.)" suffix, unlike every other genuinely-new species heading in this tree | The node's own `notes` already flags this ("Not stated as new but other sources credit this one. Possibly because fragmentary?") — confirmed accurate. This is exactly the situation the roadmap's `editorial.inferred` field is for (existence/status is the editor's judgment, not the source's printed claim), but it is currently only a `notes` string, not marked via `editorial` |
| `glyptaster` sp. `brachiatus_hall_1852_glyptaster` | "1. GLYPTASTER BRACHIATUS (n. sp.)" p.187 | Match |
| `myelodactylus` sp. `brachiatus_hall_1852_myelodactylus` | "2. MYELODACTYLUS BRACHIATUS (n. sp.)" p.232, in a run of "Fragment of..." column/arm descriptions | Match, including the `notes: "Described in section on fragments"` |
| Source record (book/volume/date/authors) | Title page, PDF index 12 | Match — see §5 |

**Clean-match count (taxa.yaml-consistent, `new`/attribution flags internally coherent, not
independently read against primary text because pp. 179–233 for these fall outside both assigned
windows):** `crinoidea-family`×2, `crinoideæ-family` synonym×2, `closterocrinus`,
`elongatus_hall_1852`, `glyptocrinus`, `plumosus_hall_1843` (+synonym), `glyptocrinus-sp_hall_1852`,
`ichthyocrinus`×2, `clintonensis_hall_1852`, `caryocrinus` (1st occurrence), `ornatus_say_1825`×2
(+`loricatus_say_1825` synonym), `homocrinus`, `parvus_hall_1852`, `cylindricus_hall_1852`,
`thysanocrinus`, `liliiformis_hall_1852`, `canaliculatus_hall_1852`, `aculeatus_hall_1852`,
`immaturis_hall_1852`, `myelodactylus`, `convolutus_hall_1852`, `myelodactylus-sp_hall_1852`,
`dendrocrinus`, `longidactylus_hall_1852`, `lævis_conrad.t.a_1842`, `lyriocrinus`,
`dactylus_hall_1843` (+synonym `marsupiocrinites` parent), `lecanocrinus`, `macropetalus_hall_1852`,
`ornatus_hall_1852_lecanocrinus`, `simplex_hall_1852`, `caliculus_hall_1852`, `macrostylocrinus`,
`ornatus_hall_1852_macrostylocrinus`, `saccocrinus`, `speciosus_hall_1852`, `stephanocrinus`,
`angulatus_conrad.t.a_1842`, `gemmiformis_hall_1852`, `heterocystites`, `armatus_hall_1852`,
`calceocrinus`, `cystideæ-family` (+ `cystidea-family` synonym), `echinodermata-order`×2,
`asteriadæ-family` — **45 nodes**. All are internally consistent with `data/taxa.yaml`
authority/altSpellingOf records; none contradicts anything found in the read windows.

## 4. Cases for the data model

### 4.1 Hemicystites / Agelacrinites — genus, not subgenus; synonymy sourced from the addenda, not the main entry

Hall's genus header at p.245 reads exactly:

> "Genus HEMICYSTITES (nov. gen.). [Gr. ἡμι, semi, and κύστις, vesica.]"

This is an unqualified, independent new-genus header — **not** parenthetical subgenus notation
("*Agelacrinites (Hemicystites)*"). Hall never writes the two names paired that way anywhere in
either read window. So the `hemicystites` node is correctly modeled as an ordinary genus, and
B18's parenthetical-subgenus scenario does **not** apply here.

However, the tree's tentative synonym entry (line 199–205) linking `hemicystites` to
`agelacrinites`, annotated "Only Agelacrinites Vanuxem, non Agelacrinites Forbes.", draws on
material printed in **two different, physically separated places**, neither of which is the
Hemicystites genus entry itself:

1. **The identity claim** — printed only in the "Additions and Corrections" addenda (p.300,
   NOTE C), added after the main volume was typeset:
   > "Genus Hemicystites, page 69. This genus is apparently identical with Agelacrinites of
   > Vanuxem, the description and figure of which I had overlooked at the time this volume was
   > written."
   (The addenda's own cross-reference "page 69" does not match either the main-text genus page,
   245, or the General Index's citation of 245/246 for Hemicystites — cannot verify what "page
   69" refers to; likely an error or a reference into a differently-paginated part of the volume.
   `tentative: true` on the synonym is well justified by Hall's own hedge "apparently identical".)
2. **The homonymy caution** — printed nowhere near Hemicystites at all, but in Hall's earlier
   general essay on Cystideæ affinities (p.238, footnote, discussing Forbes's redefinition of the
   name for an unrelated fossil):
   > "* This genus is used as defined by Prof. Forbes, and is not the Agelacrinites of Vanuxem."

So the tree's note is an accurate **synthesis** of two things Hall printed 55 pages apart, not a
transcription of one printed sentence — and the genus-level synonymy itself is only supported by
addenda text that the `hemicystites` node's own `pages: 245` field does not point to. `taxa.yaml`
already keeps the two "Agelacrinites" concepts as separate records (`agelacrinites`, authority
1842_vanuxem; `agelacrinites-sp_forbes_1848`, authority 1848b_forbes), so the synonym correctly
resolves to Vanuxem's record — the modeling is correct, but the locator trail (which page
actually supports the claim) is not currently recoverable from the node's own fields.

### 4.2 The "20†" figure is a real printed dagger, not a data artifact

Plate caption, p.246: "Figs. 18, 19, 20 and 20†." followed by individually numbered captions
"Fig. 18.", "Fig. 19.", "Fig. 20.", and "Fig. 20†. A still farther enlargement of a part of a
specimen..." — Hall genuinely used a dagger to distinguish a second, more-enlarged figure sharing
the base number 20 from the ordinary fig. 20. `illustrations: [[18,20], "20†"]` matches print
exactly.

### 4.3 `jewettii-var_hall_1852` — hedged, unnamed variant (matches B16's "hedged membership" shape, at species-variety scale)

Plate heading: "Figs. 1-11; and 12-16 var.?" The "?" is Hall's own hedge, attached directly to
the word "var." — there is no separate name, diagnosis, or synonymy for this variety; it exists
only as a caption note under fig. 12 ("An individual having a slightly different form..."). The
tree's `openTaxon` + `questionable: true` (rather than treating it as a formally named variety)
matches this correctly.

### 4.4 Two OCR-garbled `notes` reproduced verbatim from the raw scan

Both the "Lucalyptocrinus" (papulosus, p.211) and "f7. celatus. Ip. pag. 113" (decorus, p.207)
strings in the tree's `notes` fields are byte-for-byte identical to the OCR output for those
lines, not to what Hall printed. In both cases the letter Hall actually used was the genus-initial
abbreviation "E." (for *Eucalyptocrinus*), OCR'd as "L" once and swallowed/mangled ("f7.") once;
"Ip." is almost certainly "Id." (idem). Every other occurrence of "EUCALYPTOCRINUS" spelled out in
full in this same text OCRs correctly, which is why this reads as an OCR artifact rather than a
Hall typo. This is exactly the phenomenon flagged in the assignment brief — worth noting because
it shows the dataset can silently inherit OCR corruption into a `notes` field that looks like a
faithful quote.

### 4.5 `eucalyptocrinus: new: true` contradicts both the printed genus header and `data/taxa.yaml`

See correctness table row above — Hall's own header lacks "(nov. gen.)" and explicitly reconciles
two earlier genera (Goldfuss 1826, Phillips 1839); `data/taxa.yaml`'s own
`eucalyptocrinus: {name: Eucalyptocrinus, altSpellingOf: eucalyptocrinites}` record (no
`authority.source: 1852_hall`) already treats it as a derivative spelling, not a Hall 1852
origination. The tree's `new: true` flag on this one genus node is the clearest internal
inconsistency found in this audit.

### 4.6 Two disjoint stratigraphic taxonomies

Running heads confirm the second `taxonomies` entry's section: "NIAGARA GROUP." appears as the
verso running head on every page read from 237 through 271 (e.g. PDF256/"NIAGARA GROUP. 237",
PDF258/"NIAGARA GROUP. 239", PDF266/"NIAGARA GROUP. 247"). This directly supports the `notes:
"Middle Silurian of Niagra Group."` [sic, matches the tree's own "Niagra" typo-preservation] on
the second `crinoidea-family` node. The first `taxonomies` entry's "Clinton Group" heading itself
falls on pages (~170–195) outside both assigned reading windows and was **not** directly read —
cannot verify its section header text, though the general index's page citations (e.g.
*Glyptocrinus plumosus* p.180, *Caryocrinus ornatus* first cited p.182 vs. the full Niagara
treatment at p.216) are consistent with an earlier, separate section. One caution: the general
index shows *Ichthyocrinus*, `clintonensis`, and (apparently) `lævis` all clustering close to
p.195, which raises the possibility the genus is treated in one continuous passage covering both
species rather than in two fully disjoint sections — cannot verify without reading p.195
directly (outside both assigned windows).

### 4.7 `brachiatus` used for two unrelated species in one volume (B18 `originalParent` worked example)

Confirmed directly: "1. GLYPTASTER BRACHIATUS (n. sp.)" (p.187) and "2. MYELODACTYLUS BRACHIATUS
(n. sp.)" (p.232, in the fragments section) are both genuinely new species in this one work,
sharing an epithet under two different genera. `brachiatus_hall_1852_glyptaster` and
`brachiatus_hall_1852_myelodactylus` in `taxa.yaml` correctly carry `originalParent: glyptaster` /
`originalParent: myelodactylus` to disambiguate the shared key — this is a clean, verified
instance of the pattern the roadmap describes.

### 4.8 Citation-form handling (item A7)

Phillips's 1839 descriptions were published as an appendix inside Murchison's *Silurian System*
(1839) — Hall cites them as "Phillips: Murchison, Sil. System, 1839..." `taxa.yaml` correctly
threads this as `authority: {attributedTo: [phillips.j], source: 1839_murchison}` for
`decorus_phillips.j_1839`, `hypanthocrinites`, and `marsupiocrinites` — a good example of the
source/author split working as designed, not an error.

## 5. Source record check

| Field | `sources.yaml` | Title page (PDF index 12) | Verdict |
|---|---|---|---|
| book | `paleo-ny` | "PALÆONTOLOGY / NEW-YORK." | Match |
| volume | `2` | "VOLUME II." | Match |
| pubDate.year | `1852` | "1852." (imprint line) | Match |
| authors | `[hall]` | "BY JAMES HALL." | Match |

No `title`/`pages`/`identifiers` fields on `1852_hall` — checked against the only other
`paleo-ny` entry in `sources.yaml`, `1847_hall` (vol. 1): it **also** lacks `title`, `pages`, and
`identifiers`. Both `paleo-ny` records follow the same pattern, so this looks like a genuine,
consistent convention for this book (cited by book+volume only) rather than an omission specific
to this entry.

## 6. Uncertainties

- `hemicystites` addenda note's own cross-reference "Genus Hemicystites, page 69" — cannot verify
  what this refers to; does not match the main-text page (245) or the General Index's citation
  (245/246).
- Whether "Clinton Group" appears as an explicit printed section header (parallel to "NIAGARA
  GROUP.") — cannot verify; falls on pp. ~170–195, outside both assigned reading windows.
- Whether *Ichthyocrinus* (`clintonensis` vs. `lævis`) is really treated in two disjoint
  stratigraphic passages, given both cluster near p.195 in the general index — cannot verify
  without reading p.195 directly.
- Full primary-text confirmation for `homocrinus`, `glyptaster` (genus header only, not
  independently read), `thysanocrinus`, `myelodactylus` (genus header), `dendrocrinus`,
  `lyriocrinus`, `lecanocrinus`, `macrostylocrinus`, `saccocrinus`, `heterocystites`,
  `calceocrinus`'s "no species defined" errata claim, and the `ornatus_say_1825` /
  `loricatus_say_1825` synonymy under the second `caryocrinus` node — all on pages 179–233,
  outside both assigned windows; taken as taxa.yaml-consistent but not independently verified
  against Hall's actual wording.
- OCR quality in the addenda/index/plates region (PDF ~365–435) is poor and page numbers are
  frequently missing or garbled; any citation drawn from that region should be treated as
  provisional unless independently cross-checked against a cleaner scan.
