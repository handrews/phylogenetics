# Review: 2020_ewin_martin.m_isotalo_zamora

Ewin, Martin, Isotalo & Zamora 2020, *Journal of Paleontology* 94(1):115–130 —
"New rhenopyrgid edrioasteroids (Echinodermata) and their implications for
taxonomy, functional morphology, and paleoecology."

**Page mapping.** Running foot "Journal of Paleontology 94(1):115–130" plus a
bare digit, or "Ewin et al.—New rhenopyrgid edrioasteroids and their
implications" plus a bare digit, appears on every page. Printed page =
PDF page-index + 115 (PDF index 0 = printed p. 115, the article's first
page; index 15 = printed p. 130, the last).

## 1. Coverage

| kind | coverage | example |
|---|---|---|
| classification skeleton | all | full header p. 118, "Genera included.—*Rhenopyrgus* Dehm, 1961; *Heropyrgus* Briggs et al., 2017" |
| new taxa | all | *Rhenopyrgus viviani* n. sp. (p. 120), fully captured with `new: true` |
| type species | all | "Type species.—*Pyrgocystis* (*Rhenopyrgus*) *coronaeformis* Rievers, 1961" (p. 118) → `type: true` |
| synonymy lists | all | *R. grayae* (p. 122), *R.* sp. indet. 1 (p. 123), *R.* sp. indet. 3 (p. 124) — every printed synonymy list in the paper is represented (2 transcription issues noted below) |
| material | all | every specimen number printed for every taxon (holotypes, paratypes, unspecified) is on the corresponding node |
| occurrences | partly | species/specimen-level occurrences are all captured; the family-level (p. 120) and genus-level (p. 120) range-summary paragraphs exist only as commented-out `occurrenceSummary` blocks, not live data |
| illustrations | partly | new-species figures (2, 4, 5) and the sp.-indet. plate figures (3.3–3.8) are captured; the paper's own new photographs of *R. grayae* (fig. 3.1, 3.2, p. 121) are not recorded anywhere on the `grayae_bather_1915` node |
| diagnoses | partly | family (p. 118) and genus (p. 120) emended diagnoses are captured; no species diagnosis is captured (*R. viviani*'s own "Diagnosis.—..." p. 120, and *R. grayae*'s own "Diagnosis (Emended).—..." p. 122, are both absent) |
| phylogeny | none | no `phylogenies` section; the paper only discusses relationships in prose ("the phylogenetic trichotomy of rhenopyrgids, cyathocystids, and edrioblastoids... cannot be resolved," p. 125) |

## 2. What the paper does to Rhenopyrgidae, Pyrgocystidae, and Edrioblastoidea/Edrioblastoidina

- **Rhenopyrgidae** (p. 118): retained at family rank, attributed unchanged
  to "Holloway and Jell, 1983." Given an **emended** diagnosis
  ("Diagnosis (Emended).—Pyrgate edrioasteroids with relatively small oral
  surfaces...", p. 118) broadened specifically to admit floor plates "that
  may or may not be fused," following the paper's finding that some species
  (*coronaeformis*, *flos*, *viviani*) fuse their floor and interradial oral
  plates while others (*grayae*) do not. "Genera included.—*Rhenopyrgus*
  Dehm, 1961; *Heropyrgus* Briggs et al., 2017" (p. 118) — the family now
  holds two genera, both correctly present as children in the tree.
- **Pyrgocystidae**: this name is **never printed** in the paper. Only the
  superseded genus **"Pyrgocystis" Bather, 1915** appears — always in a
  historical role, as the original genus of species now placed in
  *Rhenopyrgus* (a subgenus Dehm 1961 erected within it: "*Pyrgocystis*
  (*Rhenopyrgus*) *coronaeformis*", p. 118). The paper explicitly resolves
  one *Pyrgocystis* species: "we consider *Pyrgocystis procera* a nomen
  dubium" (p. 123), with the material provisionally reassigned to
  *Rhenopyrgus* sp. indet. The tree matches this exactly — `pyrgocystis`
  appears only inside `parents` on synonymy entries, never as a family, and
  there is no Pyrgocystidae node anywhere in the file.
- **Edrioblastoidina / "Edrioblastoidea"**: the suborder is reprinted
  unchanged in the header, "Suborder Edrioblastoidina Fay, 1962" (p. 118),
  with no reclassifying act — matching the tree exactly. But the paper's
  own **Conclusions** (p. 128) once uses a *different*, family-rank name for
  apparently the same/an allied group: "the other stalked edrioasterid
  families Cyathocystidae and **Edrioblastidae**." That family-rank
  "Edrioblastidae" is printed nowhere else in the paper (elsewhere it is
  always the informal "edrioblastoids," or the suborder "Edrioblastoidina"),
  is not in `taxa.yaml`, and has no node in this tree. It cannot be
  determined from this paper alone whether "Edrioblastidae" is a slip for
  "Edrioblastoidina"/informal "edrioblastoids," or a genuine (if
  unexplained) family name the authors intend — **cannot verify**.

## 3. Correctness of what is captured

The five inherited backbone nodes (`echinodermata`…`rhenopyrgidae`) all
match the printed header (p. 118: "Phylum Echinodermata de Bruguière, 1791
(ex. Klein, 1734) / Class Edrioasteroidea Billings, 1858 / Order
Edrioasterida Bell, 1976 / Suborder Edrioblastoidina Fay, 1962 / Family
Rhenopyrgidae Holloway and Jell, 1983") with no node-level `auth`/`year`
needed, correctly, since each resolves to its `taxa.yaml` authority (A2).
`rhenopyrgus` (genus), `coronaeformis_rievers_1961` (type species),
`whitei_holloway_jell_1983`, `flos_klug_..._2008`,
`piojoensis_sumrall_..._2013` and `heropyrgus` (all bare children, correctly
minimal since none is redescribed in this paper) also match with no
discrepancy — 6 further clean matches.

Mismatches and cannot-verify rows:

| node | printed (page) | verdict |
|---|---|---|
| `rhenopyrgidae` / `rhenopyrgus` `diagnosis` text | "...bearing **five**, short, straight..." and "...alternating **floor** plates..." (family, p. 118); "...ambulacral **floor** and interradial..." (genus, p. 120) | **mismatch**: both diagnosis fields in the tree read "...bearing **ve**, short..." and "...alternating **oor** plates..." / "...ambulacral **oor** and interradial...". This is a dropped-ligature OCR artifact ("fi"/"fl" lost) copied into the data verbatim rather than corrected against the plain printed words "five" and "floor" |
| `grayae_bather_1915` synonym 1 (`1915_bather`) | "1915 *Pyrgocystis grayae* Bather, **p. 58**, pl. 3, figs. 1, 2." (p. 122) | **mismatch**: tree has `pages: 48`, not 58 |
| `grayae_bather_1915` occurrence `location` | "...Lady Burn, near **Girvan**, Scotland, UK." (p. 122) | **mismatch**: tree has "near **Givran**" |
| `grayae_bather_1915` (node) | fig. 3.1, 3.2 caption: "*Rhenopyrgus grayae*... details of oral surface..." (p. 121) | not captured: no `illustrations` on this node for the paper's own new photographs of the holotype (only the Bather 1915 synonymy citation carries illustrations) |
| `rhenopyrgus-sp-2_..._2020` occurrence | "'Ardmillan' [**?Girvan**], Scotland, UK, Ardmillan Series" (p. 123) | **cannot verify / likely mismatch**: tree has `localStage: Girvan?` — "Girvan" is a place name in the printed bracket, not a stage, and "Scotland, UK" (present on every other occurrence in this file) is missing from this entry entirely |
| `viviani_..._2020` `pages` | species account (Holotype…Remarks) runs p. 120, then (after fig. 3, an unrelated plate of *other* taxa, occupying all of p. 121) continues and ends on p. 122, where *R. grayae*'s account begins | **cannot verify precisely**: tree has `pages: [[120, 123]]`; by this mapping the account does not reach p. 123, which is occupied by the tail of *R. grayae*'s remarks and the start of *R.* sp. indet. 1 |
| `rhenopyrgus-sp-3_..._2020` occurrences, `stageModifier` | "...**late** Tremadocian, Lower Ordovician" (p. 123); "...**late** Floian, Lower Ordovician" (p. 123) | terminology substitution, not a printing: tree stores `stageModifier: upper` for both — not what is printed at this location. (Contrast: the genus-level Occurrence paragraph, p. 120, does print "upper Tremadocian" — the source itself uses both "late" and "upper" for the same rank in different paragraphs.) |
| `rhenopyrgus-sp-1_..._2020` occurrence | "middle Llandovery..." (p. 123) | not captured live: the tree has a commented-out `# seriesModifier: middle` beside the live `series: Llandovery` |

Everything else checked (synonymy attributions for `grayae` entries 2–5;
both `procera` synonymy entries under `sp-1`; both `?Pyrgocystis sp.`
entries and the illustrations under `sp-3`; every specimen number under
every node; the `type`/`new` flags; the *R.* sp. indet. 4 mention and its
page) matches the printed text exactly — 20+ further individual checks with
no discrepancy.

## 4. Cases for the data model

- **Subgenus / parenthetical notation.** "*Pyrgocystis* (*Rhenopyrgus*)
  *coronaeformis* Rievers, 1961" (p. 118) is captured as `parents:
  [rhenopyrgus-subgenus, pyrgocystis]` on the synonymy entry — an ordered
  list standing in for genus-with-parenthetical-subgenus, with no dedicated
  field for the notation itself. It works, but nothing marks that this is
  the parenthetical-subgenus case rather than an arbitrary two-level
  `parents` chain; a reader has to already know the convention to recover
  "*Pyrgocystis* (*Rhenopyrgus*)" from it.
- **A verified-but-rejected citation, matching the roadmap's "noted for
  later" case.** The `rhenopyrgus-sp-3` node's `notes` reads: `"2013
  Rhenopyrgidae Sumrall et al., p. 773" in synonym list with no explanation;
  that page in the referenced paper does not include this specimen.` This
  is exactly the open case flagged under "The `editorial` block" in the
  Ground Rules — an editor-verified discrepancy that is a **source's own**
  citation error, as opposed to `editorial.source`/`editorial.inferred`.
  Here it is handled as a plain `notes` explaining an *omission* (the 2013
  citation is simply left out of the captured synonymy rather than included
  and flagged), which is a workable but silent choice: nothing marks that a
  citation was deliberately dropped as opposed to overlooked.
- **Draft aggregate-range fields, present but disabled.** The file carries
  three commented-out blocks: a family-level `occurrenceSummary` (p. 118's
  "Occurrence.—North Africa..."), a genus-level `occurrenceSummary` (p. 120's
  "Occurrence.—Lower Ordovician (Tremadocian) to Lower Devonian
  (Emsian)..."), and a `typeTaxon` cross-reference duplicating the
  `coronaeformis`/`type: true` information already live under `children`.
  None of these is live data; the genus-level draft is itself only
  partial (it has France's two entries but not the printed UK, Canada,
  Argentina, Australia, Germany ranges). Worth knowing when assessing
  "occurrences" coverage above — the paper's own range summaries are staged
  but not delivered.
- **The source itself is inconsistent in stage terminology.** "Upper
  Tremadocian" (genus Occurrence, p. 120) and "late Tremadocian" (sp. indet.
  3 occurrence, p. 123) name the same interval within one paper. The tree
  normalizes both to `stageModifier: upper` for the live sp-3 entries (see
  §3), which discards which word was actually printed at that specific
  location — worth a `notes` if the printed wording is to be recoverable.
- **A family-rank name for the edrioblastoid group appears once, off the
  systematic header.** See §2: "Edrioblastidae" (p. 128, Conclusions) beside
  the header's suborder "Edrioblastoidina" (p. 118). This is squarely the
  B18 "same name [group] at different ranks/spellings" territory, but with
  the added wrinkle that the family-rank form appears only in prose, never
  in a systematic heading, so it is unclear whether it earns a `taxa.yaml`
  record at all under the "a case earns a field when it appears in a second
  source" rule (H). Flagging for visibility; not proposing a specific fix.
- **Species-level diagnoses are structurally absent even where everything
  else about the species is captured.** `viviani_..._2020` is a fully
  fleshed out node (pages, illustrations, three occurrences with specimens)
  but its own printed diagnosis is nowhere in the tree, unlike the family
  and genus nodes, which do carry `diagnosis`. This is a coverage choice,
  not a defect, but it means "diagnoses" coverage cannot be read off the
  presence of a well-populated species node.
- **`procera_aurivillius_1892` / gender agreement.** The `taxa.yaml` record
  links this printed epithet to `altSpellingOf: procerum_aurivillius_1892`
  — the *Preface*'s gender-agreement class of alternate spelling (x–xi).
  Confirms that mechanism is already exercised by this source's material,
  even though the epithet appears in this paper only inside synonymy
  entries citing Bather 1915 and Sumrall et al. 2013 (pp. 123, 764), not as
  a combination this paper itself uses.

## 5. Source record check

`sources.yaml` title, journal, volume (94), number (1), pages (115–130),
`pubDate.year` (2020), `processDates.accepted` (2019-08-05, matching
"Accepted: 5 August 2019," p. 129), DOI (10.1017/jpa.2019.65) and all four
authors match the printed article exactly.

## 6. Uncertainties

- Whether "Edrioblastidae" (p. 128) is a slip for "Edrioblastoidina" or a
  deliberate distinct name cannot be settled from this paper alone.
- The exact intended page-anchor convention for a single `pages` value
  (start of systematic entry vs. full span) is not documented; this affects
  whether `rhenopyrgus`'s `pages: 118` (genus heading, p. 118, though its
  own emended diagnosis prints on p. 120 after an intervening full-page
  figure) should be read as a mismatch or as a deliberate start-page
  citation — treated here as the latter and not flagged as an error.
- The taxon key segment "...debates_mapes_2008" for *R. flos*'s authority
  chain appears to render author "de Baets" as "debates" (letters
  transposed); this sits in `taxa.yaml`/author records outside this tree
  file and was not independently verified against those records.
- OCR of this PDF is generally clean (a text layer, not a scan), so the
  dropped "fi"/"fl" ligatures in the two diagnosis fields (§3) are file
  artifacts, not source ambiguity — high confidence, not a "cannot verify."
