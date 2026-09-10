# Audit: 1842_vanuxem (Vanuxem, *Geology of New-York. Part III*, 1842)

## 1. Page-index mapping

**Printed page = PDF index − 9**, confirmed at both windows read:
- PDF index 167 → running head "GEOLOGY OF THE THIRD DISTRICT" / printed page "158" (Agelacrinites description).
- PDF index 165/166/168–171 → printed pages 156/157/159–162 (consistent, same offset).
- PDF index 314/315 → running head "GEOLOGY OF THE THIRD DISTRICT" / printed page "306" (Agelacrinites figure).
- PDF index 313 → printed page 304 (also offset −9).

Offset is stable across both windows; no page renumbering detected in between.

## 2. Coverage

| Kind | Status | Example |
|---|---|---|
| Classification skeleton | All (for what exists) | 4 genus-level branches under `crinoidea-family` |
| New taxa (`new: true`) | Partly | `agelacrinites` + `hamiltonensis_vanuxem_1842` verified against print; `hallii_conrad.t.a_1842` flagged `new: true` but unverifiable (no page cited) |
| Type species | None | `agelacrinites` has no `type` flag on its sole species, though monotypy is evident from the text |
| Synonymy lists | None | expected — this is informal survey prose, not a systematic monograph (per assignment framing) |
| Material/specimens | Partly | `hamiltonensis_vanuxem_1842.specimens[""].holotypes = ["Page 306, Figure 80"]`, no catalog number (early-source gap, G9) |
| Occurrences | Partly | captured for `hamiltonensis_vanuxem_1842`, `hamptonii_unknown`, `gebhardi_conrad.t.a_1840`; absent for `hallii_conrad.t.a_1842` (matches its own "No description or figures" note) |
| Illustrations | Partly | `hamiltonensis_vanuxem_1842` → p.306 fig.80, confirmed exact; two other illustration entries not in my read window |
| Diagnoses | Partly | only `hamiltonensis_vanuxem_1842` carries one (an English descriptive paragraph, not a Latin diagnosis — appropriate for this source) |
| Phylogeny | None | file has no `phylogenies` key — correct, no cladograms in this source |

Beyond the Agelacrinites material, coverage is a skeleton keyed to bibliographic cross-references (pages 64–65, 117) rather than fully verified transcription; this is scope history (G9), not an error.

## 3. Correctness table

| Node | Printed (page) | Verdict |
|---|---|---|
| `crinoidea-family` (root) | n/a — organizing container | Not a printed entity; `notes` on unresolved species names is editorial commentary, addressed under §6 |
| `agelacrinites` (new, rank: genus, pages: 158) | p.158: "it therefore establishes a new genus, for which the name of Agela-crinites is proposed, from [Greek] agele, a herd or group, and hamiltonensis for the species" | **Match.** `new: true` and `rank: genus` fully supported — Vanuxem explicitly claims a new genus, in his own first-person narrative ("I found a fragment..."), no other author is credited |
| `hamiltonensis_vanuxem_1842` (new, pages: 158, diagnosis, illustrations p.306/fig.80) | p.158 description; p.306 caption "Hamilton agelacrinite (Agelacrinites hamiltonensis). [See page 158.]" over figure "80." | **Match**, with one note: the `diagnosis` field quotes the opening and closing of the printed paragraph verbatim but elides (via "....") the middle sentences describing the six medallions' relative sizes/count/arrangement (three large ~1 in., three small, clustered in an angle) — see §4. Illustration cross-reference (page 306, figure 80) is exact |
| `nucleocrinus` (no `new`, notes on priority vs. Conrad 1842) | not encountered in read windows (p.156–171, p.304–306) | **Cannot verify** — out of scope of indexed pages. Its `notes` field is internally consistent with `taxa.yaml`'s own annotation ("Possibly first published in 1842_vanuxem") on the `nucleocrinus` genus record |
| `hallii_conrad.t.a_1842` (new: true, notes: "No description or figures") | no `pages` field given on the node; not encountered in read windows | **Cannot verify** — no page citation exists to check against, and the node's own note says the source gives no description/figures for it. See §4 for the attribution pattern this node presents |
| `pentacrinites` (no `new`) | not encountered; genus is Blumenbach 1804 per `taxa.yaml`, correctly not claimed new here | **Consistent by omission** — absence of `new: true` matches the pre-existing genus; specific print location for this source's usage not in my read window |
| `hamptonii_unknown` (pages: 64, illustrations p.65) | p.64/65, not in assigned read window | **Cannot verify without a fuller search** — out of scope of the indexed pages, per assignment instructions |
| `lepocrinites` (no `new`) | genus per `taxa.yaml`: Conrad 1840, *in* Vanuxem — correctly not claimed new in this 1842 source | **Consistent by omission**; specific print location not in my read window |
| `gebhardi_conrad.t.a_1840` (pages: 117, illustrations p.117) | p.117, not in assigned read window | **Cannot verify without a fuller search** — out of scope of the indexed pages |

Summary: 2 of 9 nodes fall inside my assigned read windows and both match the print (one with a noted mid-paragraph elision, not an error). The remaining 6 taxon nodes reference pages outside the assigned windows (64, 65, 117, and an uncited page for `hallii`) and were intentionally not chased down per the assignment's scope limits.

## 4. Cases for the data model

**A. YAML location-field oddity (data-file issue, not a printed-text mismatch).**
`data/trees/1842_vanuxem.yaml` lines 35–42, the `hamiltonensis_vanuxem_1842` occurrence's `location` list:
```yaml
        location:
        - upper quarry
        - the hill back of the Seminary
        - West-Hamilton village
        - Madison County
        - New York
        - United States
          upper quarry
```
Parsed with `yaml.safe_load`, this produces a **6-element list**, not 7:
```
0: 'upper quarry'
1: 'the hill back of the Seminary'
2: 'West-Hamilton village'
3: 'Madison County'
4: 'New York'
5: 'United States upper quarry'
```
The final `- United States` item's block-scalar continuation line (`  upper quarry`, indented past the dash) folds into that same list entry as a plain-scalar continuation, joined with a space: `"United States upper quarry"`. This looks like an accidental duplication of "upper quarry" (already item 0) via a stray unindented continuation line, rather than an intended compound value — worth the owner's attention. Not fixed here per instructions.

**B. Attribution pattern on `hallii_conrad.t.a_1842`.**
`data/taxa.yaml` records this identity as `authority: {attributedTo: [conrad.t.a], source: 1842_vanuxem}`, and the tree node carries `new: true` with the comment `# It's a little unclear how to handle this situation` and `notes: No description or figures.` This is a name credited in print to one person (Conrad) but whose only located occurrence is in another author's (Vanuxem's) publication, with no accompanying description — i.e., possibly a nomen nudum citing a manuscript/verbal name. This doesn't cleanly match A6 (that's a citation-year mismatch resolved via `editorial.source`) or the `editorial.inferred` case (node existence being the *editor's* inference — here it's the *source's* own attribution that's unclear, not the editor's addition). It reads as a Section-H-style case: "a name used ... other formatting the fields cannot cleanly capture," specifically for attributed-but-undescribed names. I could not locate or quote the actual printed passage (no page is cited on the node, and it wasn't in either assigned read window), so I cannot confirm the exact printed wording behind this — flagged structurally only, from the tree/taxa.yaml records.

**C. Minor OCR/typographic notes on the Agelacrinites passage (not data-model issues, informational only).**
- The genus name is line-broken in print as "Agela-/crinites" (end-of-line hyphenation); the tree/taxa.yaml correctly records the unhyphenated "Agelacrinites."
- The Greek etymon is garbled in OCR as "ctgele" (almost certainly ἀγέλη, "herd" — Vanuxem's own gloss "a herd or group" confirms the intended word). This is an OCR artifact, not something the dataset needs to capture; the source's `diagnosis`/`notes` fields do not currently carry the etymology, which is a coverage choice, not an error.

## 5. Source record check

Title, book, date, and single authorship all check out. Running heads throughout the read windows read "GEOLOGY OF THE THIRD DISTRICT," consistent with the record's title "Geology of New-York. Part III. Comprising the Survey of the Third Geological District," and the narrator writes in first person throughout ("I found a fragment...") consistent with sole authorship by Vanuxem. I did not examine the actual title page (outside my read windows), so full title-page wording is not independently confirmed, but nothing in the read windows conflicts with the source record.

## 6. Uncertainties

- `hallii_conrad.t.a_1842`: no page number is recorded on the node, so its printed location in the ~882KB volume could not be located within the assigned read windows or the scope of this audit — cannot verify beyond what §4B describes.
- `hamptonii_unknown` (p.64/65), `gebhardi_conrad.t.a_1840` (p.117), `pentacrinites` and `lepocrinites` generic-level text: cannot verify without a fuller search; explicitly out of scope of the indexed pages per the assignment.
- Echinus drydenensis, Pentacrinites hamptonii (species-level text at p.64), Encrinites lævis, and E. triciclas (mentioned only in the tree's top-level `notes` as unresolved/nomen-nudum candidates): none of these appeared in either read window (pp.156–171, 304–306). Cannot verify the "seems to have been a nomen nudum" characterization from what I read — out of scope of the indexed pages, would require a fuller search of the volume.
- Errata list (PDF index 316, printed unnumbered page after 306) covers pages 22–295 and does not mention page 158 or 306 — no errata affect the Agelacrinites material, but I did not check the errata list against the other nodes' pages (64, 65, 117) since those pages were themselves out of scope.
