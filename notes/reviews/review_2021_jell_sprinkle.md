# Review: 2021_jell_sprinkle

Jell & Sprinkle 2021, *Alcheringa: An Australasian Journal of Palaeontology*
45(1):1–55 — "Revision of Whitehouse's eocrinoids *Peridionites* and
*Cymbionites*, with description of the associated fauna including two new
echinoderm genera, lower Middle Cambrian Thorntonia Limestone, northwestern
Queensland."

**Page mapping.** PDF page-index 0 is the journal's separate Taylor & Francis
cover/citation sheet (not part of the article's own pagination). From
page-index 1 (the article's own first page, unnumbered) on, a running foot
("PETER A. JELL AND JAMES SPRINKLE" / "REVISION OF PERIDIONITES AND
CYMBIONITES") plus a bare digit gives the printed page. Printed page = PDF
page-index, for index 1–55.

**Scope note.** The source record's `audit.notes` reads "Non-echinoderm
trees not captured." The paper also gives full systematic treatments of
associated trilobites, brachiopods, molluscs, hyoliths and sponges
(pp. 37–55, "PETER A. JELL AND JAMES SPRINKLE"'s Systematic palaeontology
continuing past the echinoderms) — none of that is in this tree, and per
G9 that is documented scope, not a gap. This review covers only the
echinoderm content the tree is scoped to.

## 1. Coverage (echinoderm content only)

| kind | coverage | example |
|---|---|---|
| classification skeleton | all | full header p. 6, Phylum→Family Lichenoididae; p. 27, Subphylum Echinozoa→Order Edrioblastoida |
| new taxa | all | Family Thorntonitidae nov. (p. 19), *Thorntonites* gen. nov. (p. 21), *T. dowlingi* gen. et sp. nov. (p. 21), *Ikerus* gen. nov. (p. 27), *I. edgari* gen. et sp. nov. (p. 34) — all five flagged `new: true` |
| type species | all | all six genus-level type-species designations captured (*Peridionites*→*navicula*, *Cymbionites*→*craticula*, *Thorntonites*→*dowlingi*, *Ikerus*→*edgari*, *Cambraster*→*cannati*, *Kailidiscus*→*chinensis*) |
| synonymy lists | partly | the family-level Lichenoididae synonymy bracket (p. 6) is captured; the species-level citation lists for *P. navicula* (3 entries, p. 6) and *C. craticula* (4 entries, p. 15) are not captured at all |
| material | all | every catalogue number/range printed for every taxon (holotypes, paratypes, topotypes, and the open-nomenclature material) is on the corresponding node |
| occurrences | none | no `occurrences`/bed/locality field on any node, despite each holotype line naming a specific bed and locality (e.g., "from bed G... UQL453," p. 6) |
| illustrations | none | no `illustrations` field anywhere, despite extensive figured-specimen captions (Figs 3–34) |
| diagnoses | none | no `diagnosis` field anywhere in the tree; the paper prints full diagnoses for Lichenoididae (p. 6), *Peridionites* (p. 6), *Cymbionites* (p. 15), Thorntonitidae (p. 19–21), *Thorntonites* (p. 21) and *Ikerus* (p. 27) |
| phylogeny | none (n/a) | no `phylogenies` section; the paper proposes no cladogram |

## 2. Disarticulated-plate and open-nomenclature material

This paper is built almost entirely on disassociated plates recovered by
acid etching, and it heads that material in several different ways:

- **Formal new taxa built from disarticulated plates.** Both new genera are
  explicitly diagnosed from dissociated material: "The genus is known only
  from disarticulated plates, meres and short stalk segments, and distal
  holdfasts, necessitating the use of inference to reconstruct the skeleton
  of the animal" (*Thorntonites*, p. 21). These get ordinary `new: true` +
  `type: true` treatment in the tree (`thorntonitidae`, `thorntonites`,
  `dowlingi_jell_sprinkle_2021`; `ikerus`, `edgari_jell_sprinkle_2021`) —
  correct, since a full protologue with diagnosis, holotype and etymology
  was published, regardless of the material being disarticulated.
- **Open-nomenclature species referred to an existing genus, not new taxa.**
  "*Cambraster* sp." (p. 35) and "*Kailidiscus* sp." (p. 36) are both plain
  indeterminate-species assignments — no new Latin name is proposed for
  either, and neither is printed as "sp. nov." Both are captured as
  `openTaxon` (`cambraster-sp_jell_sprinkle_2021`,
  `kailidiscus-sp_jell_sprinkle_2021`), which is right, but **both also
  carry `new: true`**, which does not fit the field's stated meaning
  ("protologue here" — a nomenclatural act). Neither entry is a
  nomenclatural act; this looks like `new` being used to mean "newly
  reported at this source" rather than "new taxon name," and is inconsistent
  with its use everywhere else in this same tree, where it only marks true
  "gen./sp. nov." acts.
- **An informal designation carried across three papers, unresolved.**
  "The species Lichenoidid gen. et sp. nov. (Smith et al. 2013, fig. 4i),
  later Lichenoides sp. (Zamora et al. 2017)... may be assigned to
  Thorntonitidae based on the nature of its stalk... Whether it belongs to
  *Thorntonites* or not is difficult to determine given the dissociated
  nature of the Queensland species and the less than complete understanding
  of the Moroccan taxon" (pp. 26–27). "Lichenoidid gen. et sp. nov." is
  Smith et al.'s own informal placeholder for a taxon they recognized as new
  but did not name; Zamora et al. 2017 refined it to "*Lichenoides* sp."
  (a cf.-type open placement in an existing genus, not a new-taxon claim).
  The tree represents this as two openTaxon records, `lichenoididae-gen_...`
  (rank genus) with a child `lichenoididae-gen-sp_...` (rank species),
  `provisional: true`, placed as a family-level (Thorntonitidae) sibling of
  `thorntonites` rather than under it — correctly reflecting "may be
  assigned to Thorntonitidae" without committing to genus. The later
  "*Lichenoides* sp." naming is nested as a `synonyms` entry
  (`lichenoides-sp_zamora_..._2017`) under the *Smith et al.* placeholder,
  capturing the renaming lineage across the two secondhand sources. This is
  a clean example of the model handling a chain of other papers' open
  nomenclature.
- **Explicitly out-of-scope open nomenclature.** The paper's final
  echinoderm section, "OTHER UNIDENTIFIED ECHINODERM PLATES" (p. 37 on),
  reports several plate morphotypes ("Type 1 plates," etc.) "in open
  nomenclature," explicitly because they "may not be readily placed
  taxonomically below the level of phylum with any confidence" (p. 37).
  None of this is in the tree. Given the paper itself declines to treat
  these as one taxon or bin, omitting them (rather than forcing a
  placeholder) is defensible, but it sits outside anything the audit note
  says was excluded, so flagging for visibility.

## 3. Correctness of what is captured

18 of the 21 taxon-bearing nodes checked (backbone ranks, genera, type
species, and every specimen list) match the printed text exactly with no
discrepancy, including all specimen number ranges for `navicula_...`,
`craticula_...`, `dowlingi_...`, `edgari_...`, `cambraster-sp_...` and
`kailidiscus-sp_...`, and all six `type: true` flags. Mismatches and
cannot-verify rows:

| node | printed (page) | verdict |
|---|---|---|
| `cambraster` (genus) | "*Cambraster* Cabibel et al., 1958" (p. 35) | **mismatch**: `taxa.yaml`'s `cambraster` record carries `auth: [jaekel], year: 1923` — a different author and year entirely — and the tree node has no `auth`/`year` override or `notes` to record the disagreement, so per A2's convention (bare node = agrees with the record) this reads as a match when it is not |
| `stromatocystitida-incertae-sedis` (the "Family UNCERTAIN" placeholder) | "Family UNCERTAIN" (p. 36) — no attribution at all | **mismatch**: the `taxa.yaml` record carries `auth: [linnaeus], year: 1758`, which cannot be right for a 2021-authored uncertain-family placeholder and is not printed anywhere in this paper |
| `echinodermata` (root node) `auth`/`year` | "Phylum ECHINODERMATA Brugiere, 1791" (p. 6) | node carries `auth: [brugière], year: 1791`. Two issues: (1) the key is misspelled — "brugière" (missing the "u" of Bruguière) against the dataset's own established spelling `1791_bruguière` used for this same authority elsewhere; (2) per A2 this attribution should be dropped (it agrees with the `taxa.yaml` authority `source: 1791_bruguière`) — every other backbone node in this same tree (`blastozoa`, `eocrinoidea`, `gogiida`, `lichenoididae`, `peridionites`, `cymbionites`) correctly omits its matching node-level `auth`, so this one is an inconsistency within the file itself |
| `lichenoididae` `synonyms` (5 entries) | "[= Subphylum HAPLOZOA Whitehouse, 1941, **p. 4**; = Class CYAMOIDEA Whitehouse, 1941, **p. 5**; = Class CYCLOIDEA Whitehouse, 1941, **p. 8**; = Family PERIDIONITIDAE Whitehouse, 1941; = Family CYMBIONITIDAE Whitehouse, 1941]" (p. 6) | not captured: none of the five synonym entries (`haplozoa`, `cyamoidea`, `cycloidea`, `peridionitidae`, `cymbionitidae`) carries `authority.pages`, though three of the five have a printed page (of the cited 1941 Whitehouse work) |
| `navicula_whitehouse_1941`, `craticula_whitehouse_1941` | full synonymy citation lists: "1941 *Peridionites navicula* Whitehouse, p. 5... 1968b...Ubaghs... 1971...Hill et al...." (p. 6); "1941 *Cymbionites craticula* Whitehouse, p. 9... 1968b...Ubaghs... 1971...Hill et al.... 1982...Smith..." (p. 15) | not captured: neither species node has a `synonyms` block, though both lists are printed in full synonymy-citation form |

The five synonymized names under `lichenoididae` *do* correctly carry their
own original rank on their `taxa.yaml` records (`haplozoa`: Subphylum;
`cyamoidea`/`cycloidea`: Class; `peridionitidae`/`cymbionitidae`: Family,
all against the current Family rank of Lichenoididae) — a working
illustration of B18's "same taxon [concept], several ranks and names"
resolved through the taxon record rather than the tree node.

## 4. Source record check

`sources.yaml` title, journal, volume (45), number (1), pages (1–55),
`pubDate.year` (2021), all four `processDates` (received 2020-07-03, revised
2020-11-22, accepted 2021-01-04, online 2021-06-02), DOI
(10.1080/03115518.2021.1913512) and both authors match the printed article
exactly.

## 5. Uncertainties

- Whether `cambraster`'s `auth: [jaekel], year: 1923` reflects a genuine
  earlier (objective or subjective) synonym Jaekel used for the same
  concept, entered from some other source not in this batch, or is a data
  error — **cannot verify** from this paper alone, which only ever cites
  "Cabibel et al., 1958."
- Whether the `stromatocystitida-incertae-sedis` record's
  `auth: [linnaeus], year: 1758` is a leftover default/template value or an
  intentional (if unexplained) placeholder authority — **cannot verify**;
  nothing in this paper supports it.
- This PDF has a clean text layer (not a scan), so the OCR caveat does not
  apply to spelling in the tree — the "brugière" vs "bruguière" and
  "Cabibel"/"Jaekel" discrepancies above are data-entry matters, not
  reading ambiguity, and are reported with that confidence.
