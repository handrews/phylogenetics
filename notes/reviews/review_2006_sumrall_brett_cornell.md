# Review: 2006_sumrall_brett_cornell (Sumrall, Brett & Cornell 2006, *Pyrgopostibulla belli*)

Page mapping: PDF page index 1 = printed p. 187 (running head "PALEONTOLOGICAL
NOTES"/"187"); index N = printed p. (186 + N) through index 6 = p. 192.

## 1. Coverage

| item | status | example |
|---|---|---|
| classification skeleton | all | Edrioasteroidea > Isorophida > Isorophina > Agelacrinitidae > Postibullinae > *Pyrgopostibulla* > *belli*, matches p. 190 header |
| new taxa | all | genus and species both flagged `new: true` |
| type species | all | `type: true` on *belli* under the new genus |
| synonymy lists | none | paper has no synonymy (new-taxon description only) |
| material | none | holotype PRI 50689 + paratypes PRI 50690–50709 (p. 191) not in tree |
| occurrences | none | Thacher Member/Manlius Fm. locality (p. 191) not in tree |
| illustrations | none | Figs 2–4 (holotype/paratype figures) not in tree |
| diagnoses | none | genus and species diagnoses (p. 190–191) not in tree |
| phylogeny | none | paper has no cladogram (ontogeny/discussion only) |

Beyond the classification skeleton, the tree captures only the two new-taxon
flags and the type flag; material, occurrence, illustration and diagnosis text
are not entered. No printed attribution (`auth`/`year`/`citedAs`) is captured
on any node either — every node carries only `taxon`, flags, and (at two
nodes) `notes`.

## 2. Correctness of what is captured

All 7 nodes match the printed classification in identity and placement.
Rank identity (Class/Order/Suborder/Family/Subfamily/Genus/Species) checked
against `taxa.yaml` ranks for `edrioasteroidea`, `isorophida`, `isorophina`,
`agelacrinitidae`, `postibullinae` — all consistent with the nesting used.
`new`/`type` flags match "new genus" / "n. gen. and sp." exactly. No
mismatches or unverifiable nodes; count: 7/7 match.

## 3. Cases for the data model

**Rankless names (owner's prompt).** The Systematic Paleontology header
(p. 190) reads exactly:

```
SYSTEMATIC PALEONTOLOGY
EDRIOASTEROIDEA Billings, 1858
ISOROPHINA Bell, 1976b
ISOROPHIDA Bell, 1976b
AGELACRINITIDAE Chapman, 1860
POSTIBULLINAE Sumrall, et al., 2000
Genus PYRGOPOSTIBULLA new genus
```

and the species heading (also p. 190) reads "PYRGOPOSTIBULLA BELLI new
species." The tree's top-level `notes: No ranks are included` is close but
not exact: no rank word is printed for Class/Order/Suborder/Family/Subfamily,
but the word "Genus" *is* printed before the genus name. The note describes
the supra-generic convention correctly but overstates it as covering the
whole hierarchy.

**The Isorophida/Isorophina swap (owner's prompt).** As quoted above, the
printed order is EDRIOASTEROIDEA, then ISOROPHINA, then ISOROPHIDA, then
AGELACRINITIDAE — i.e. the suborder-rank name (Isorophina) is printed
*above* the order-rank name (Isorophida) in a list that otherwise runs from
high to low rank. `taxa.yaml` fixes Isorophida as `rank: Order` and
Isorophina as `rank: Suborder` (both authorized by `1976_bell.b.m`), so the
printed sequence inverts the true rank order. The tree does not reproduce the
printed line order; it nests by the correct rank hierarchy instead
(`isorophida` > `isorophina` > `agelacrinitidae`...) and carries an identical
`notes: Isorophida and Isorophina are switched, surely by error.` on both the
`isorophida` and `isorophina` nodes. This is a modelling choice worth noting
explicitly: the tree encodes the *editor's* correction of a printed sequencing
anomaly (nesting by known rank, not print order) and uses `notes` rather than
an `editorial` block to flag it. Per the ground rules' `editorial` block
(source cannot resolve as printed / placement is the editor's own), this is
arguably not quite either case — the *placement* Class > Order > Suborder >
Family is not in doubt (it follows the established ranks and both names'
own authorities), only the print sequence is anomalous — so a plain `notes`
rather than `editorial.inferred` seems the right call, but it is a borderline
example worth having on record for when `editorial` vs. `notes` is next
revisited.

## 4. Source record check

`sources.yaml`'s `2006_sumrall_brett_cornell` matches the printed cover page
in full: title verbatim, *J. Paleont.* vol. 80, no. 1, Jan. 2006, pp. 187–192,
authors Sumrall/Brett/Cornell, accepted 8 Dec 2004 (printed "ACCEPTED 8
DECEMBER 2004"), JSTOR id 4095094.

## 5. Uncertainties

None found; this is a clean, short, born-digital JSTOR scan of typeset text
with no OCR ambiguity affecting any taxon name, date, or page number used
above.
