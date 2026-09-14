# Review: 2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman

Briggs, Siveter D.J., Siveter D.J. (David), Sutton & Rahman 2017, *Proc. R.
Soc. B* 284: 20171189 — "An edrioasteroid from the Silurian Herefordshire
Lagerstätte of England reveals the nature of the water vascular system in an
extinct echinoderm."

**Page mapping.** The article carries no printed page numbers on its first
page; the running foot "Proc. R. Soc. B 284: 20171189" plus a bare digit
appears on every later page, reading 2, 3, 4, 5, 6, 7 on PDF page-index 1–6.
So printed page = PDF page-index + 1 (PDF index 0 = printed p. 1).

## 1. Coverage

| kind | coverage | example |
|---|---|---|
| classification skeleton | all | full header, phylum→genus, p. 2 |
| new taxa | all | *Heropyrgus* gen. nov., *H. disterminus* sp. nov., p. 2 |
| type species | all | "Type species: *Heropyrgus disterminus* sp. nov." p. 2 |
| synonymy lists | none printed | genus and species are new; no synonymy exists to capture |
| material | none | Holotype OUMNH C.36043, paratypes, unground specimens (p. 2) not in tree |
| occurrences | none | "Herefordshire, England, UK; Wenlock Series, Silurian" (p. 2) not in tree |
| illustrations | none | figure 1 (16 panels) and its caption not in tree |
| diagnoses | none | "(b) Diagnosis of genus (monotypic) and species" (p. 2) not in tree |
| phylogeny | none (n/a) | paper reports no cladogram of its own; discusses Sumrall et al.'s |

Beyond the classification skeleton and the two new-taxon/type flags, nothing
else printed for this source is captured — expected for a source this small
and early in scope (G9).

## 2. Correctness of what is captured

All 7 nodes checked against the printed systematic header (p. 2):

> Phylum Echinodermata [20] (ex [21]) / Class Edrioasteroidea [22] / Order
> Edrioasterida [23] / Suborder Edrioblastoidina [24] / Family
> Rhenopyrgidae [25] / Genus *Heropyrgus* gen. nov. / Type species:
> *Heropyrgus disterminus* sp. nov. / Other species: None.

Reference list resolves: [20] Bruguière 1791, [21] Klein 1734 ("ex"),
[22] Billings 1858, [23] Bell 1976, [24] Fay 1962 ("Edrioblastoidea, a new
class of Echinodermata"), [25] Holloway & Jell 1983.

6 of 7 nodes match with no discrepancy: none of the five inherited-name
nodes (`echinodermata`…`rhenopyrgidae`) carries a node-level `auth`/`year`,
which is correct under A2 — each resolves to the same source as its
`taxa.yaml` authority record (`1791_bruguière`/ex `1734_klein`,
`1858b_billings`, `1976_bell.b.m`, `1976_bell.b.m`... `1983` for
Holloway/Jell), so the field would carry no information. `heropyrgus`
(`new: true`) and the species node `disterminus_..._2017` (`type: true`,
`new: true`) both match the printed "gen. nov."/"sp. nov."/"Type species"
wording.

One node worth a closer look: **`edrioblastoidina`**. The paper cites ref
[24] — Fay 1962, "Edrioblastoidea, a new class of Echinodermata" — as the
authority for "Suborder Edrioblastoidina" (p. 2). The `taxa.yaml` record
(`auth: [fay]`, `year: 1962`) matches the printed citation, but the cited
paper's own title names a *class*-rank *-oidea* form, not the *suborder*
-rank *-ina* form used here; nothing on the printed line or the record
marks that the name has been transposed to a different rank/suffix by
Briggs et al.'s citation chain. This is not an error in this tree (the
printed line genuinely reads as shown) but it is the B18 case: coordinate
names, one author, two ranks. Not verifiable from this paper alone whether
"Edrioblastoidina" is Fay's own coinage at a different rank or a later
author's transposition — cannot verify without the Fay 1962 text.

## 3. Cases for the data model

- **Monotypy stated but not captured.** The paper heads its diagnosis "(b)
  Diagnosis of genus (monotypic) and species" and explicitly states "Other
  species: None" (p. 2) directly under "Type species: *Heropyrgus
  disterminus* sp. nov." No field records this; it is the kind of
  printed, structured statement ("Other species: None") that a Treatise-
  style protologue habitually makes and that the model currently has no
  place for beyond `notes`.
- **Rhenopyrgidae authority citation vs. rank history.** See the
  `edrioblastoidina` note above (B18) — the suborder-rank name is
  attributed to a paper that (per its own title, printed in this source's
  reference list) established a class.
- **How a Royal Society paper prints its systematics.** Unlike some
  journals that push taxonomy into supplementary/electronic material, this
  paper's entire "3. Systematic palaeontology" section — heading,
  etymology, diagnosis, material, locality/horizon, description — is in
  the main text (§3, p. 2–4). The article has no electronic supplementary
  material file; "Data accessibility" (p. 5) points only to a Dryad
  repository of serial-grinding datasets and 3D mesh files, not to any
  taxonomic text. So nothing in this tree could have come from material
  the PDF here does not contain — the whole classification, the new-genus
  and new-species acts, and the type-species designation are all printed
  in the body text captured in this file.
- **Discussion-section classification history is not the paper's own
  placement and is correctly left out of the tree.** The paper's Discussion
  (p. 4) narrates three earlier, different placements of *Rhenopyrgus*
  (Holloway & Jell 1983, "order uncertain"; Smith & Jell 1990, grouped with
  *Totiglobus* and *Cambroblastus*; Guensburg & Sprinkle 1994, subfamily
  Rhenopyrginae of family Cyathocystidae) before the paper states its own
  choice: "We assign *Heropyrgus* to the Rhenopyrgidae..." (p. 5). The tree
  correctly reflects only the paper's own systematic header (family rank,
  not subfamily-within-Cyathocystidae), consistent with H's "an earlier
  classification reproduced" rule — those three superseded schemes belong
  to their own sources' trees, not this one.

## 4. Source record check

`sources.yaml` title, journal, volume (284), article number (20171189) and
authors all match the printed citation block (p. 1). `number: 1862` (the
issue) is not printed anywhere in the captured text — cannot verify from
this source alone. Author order and initials match: "Derek J. Siveter" and
"David J. Siveter" resolve to `siveter.de.j` and `siveter.da.j`
respectively per the affiliations list (p. 1).

## 5. Uncertainties

- Whether "Edrioblastoidina" is Fay's own 1962 coinage or a later rank
  transposition cannot be verified without the Fay 1962 text (not in this
  batch).
- Issue number 1862 in the source record cannot be verified against this
  PDF (not printed).
- OCR renders "Lagerstätte" as "Lagersta¨tte" throughout (broken umlaut);
  not a substantive risk here since the source record spells it correctly.
