# Review: 1936_bassler — "New Species of American Edrioasteroidea"

**Page mapping.** The Bassler paper occupies its own title page at PDF index
178 (duplicated at index 180, a scan artifact), with running text starting at
PDF index 182. The paper carries its own printed pagination starting at 1 on
that page (no visible folio on p. 1 itself, but the running head
"Smithsonian Miscellaneous Collections, Vol. 95, No. 6" confirms it; PDF
index 183 shows the printed "2" explicitly). The mapping is:

**printed page = PDF index − 181**, valid for pages 1–33 (PDF index 182–214).

Text ends on printed p. 33 (index 214, plate-explanation text for Plate 7).
Plates I–VII themselves are unpaginated image pages at PDF index ~216–222.
PDF index 223 is blank; a new article ("The Gold-Banded Skipper," vol. 95
no. 7) begins at PDF index 224. All page citations below are printed pages
per this mapping, never PDF indexes.

## 1. Coverage

- **Classification skeleton**: all. Every family, genus and species Bassler
  places in a hierarchy is present, with one exception (Cyathotheca, see
  Correctness/Cases below) and a small number of previously-described species
  he mentions in passing under a genus account without a formal heading
  (e.g. Lepidodiscus squamosus, beecheri, buttsi, lebouri, milleri, p. 20;
  Isorophuosella's and Ulrichidiscus's and Cooperidiscus's genotypes).
- **New taxa**: partly. One new species described under its own heading with
  material and locality — *Carneyella foerstei*, n. sp. (Bassler and
  Shideler), p. 8 — has no node at all. See Correctness.
- **Type species**: all. Every explicit "genotype" / "type of the genus"
  statement is captured with `type: true`.
- **Synonymy lists**: none. Bassler's paper is not a revision with formal
  synonymy blocks; the one substantive exception is the two-line citation
  under *Discocystis kaskaskiensis* (p. 21: "Agelacrinus kaskaskiensis Hall,
  Geol. Iowa, vol. 1, pt. 2, p. 696 ..."; "Echinodiscus optatus Worthen and
  Miller, Geol. Surv. Illinois, vol. 7, p. 336 ..."), which is not captured.
- **Material**: partly. Holotype numbers are captured for three nodes
  (*magister*, *carteri*, *ulrichi* Bassler 1936 under Cystaster); every
  other new species' printed holotype/paratype/cotype number (about 20 of
  them) is uncaptured.
- **Occurrences**: none. Every species account ends with an "Occurrence.—"
  line (formation, locality); none is captured.
- **Illustrations**: none. Every species has a plate and figure citation,
  cross-referenced in the "Explanation of Plates" (pp. 25–33); none is
  captured.
- **Diagnoses**: none. The prose diagnostic paragraphs are not captured.
- **Phylogeny**: not applicable — the paper prints no cladogram, only
  classification lists.

## 2. Correctness

77 nodes checked. All type flags, all "new" family/genus/species flags
except one node listed below, and all genus/species placements not listed
below match the printed text. Summary: **68 matches**, 5 mismatches, 1
cannot-verify, 1 missing node, 1 modeling-relevant omission (Cyathotheca — see
Coverage).

| node | printed (page) | verdict |
|---|---|---|
| `walcottidiscus-sp_bassler_1936` (openTaxon, `new: true`) | p. 2: "Associated with the genotype, *W. typicalis* Bassler, is a second species possessing the same generic features ... but with curved ambulacra, four (1 to 4) directed to the left, and one, the right posterior (5), to the right." | **Mismatch.** No independent species is ever named. The very next heading, "WALCOTTIDISCUS MAGISTER, n. sp." (p. 2–3), describes "long, narrow, strongly curved ambulacra, four curved to the left and the right posterior to the right" — the same curvature pattern, same genus, no other species mentioned anywhere else in the paper (checked: "Walcottidiscus" and "typicalis" occur nowhere else in the text). The "second species" of the genus account *is* magister, introduced by anticipation before its formal heading. This openTaxon node appears to double-count magister as a separate open-nomenclature taxon. |
| `granulatus_hall_1871`, `synonyms` entry with `parents: [cystaster-subgenus, hemicystites]` and note "Given as \"C. (Hemicystite) granulatus\"" | p. 4: "CYSTASTER Hall, 1871 / The view of the genotype *C. (Hemicystites) granulatus* (Hall) ..."; plate 1 caption (p. 25): "*Cystaster (Hemicystites) granulatus* Hall" | **Mismatch.** Both occurrences in this paper read "(Hemicystites)" — the genus name itself, matching the note's own claimed-correct spelling — not "(Hemicystite)" as the tree's note asserts was printed. The note's premise (that the source reverses Cystaster/Hemicystites) is not supported by this paper's text. See also Cases §1 below on what the parenthetical means. |
| `hemicystites-subgenus > stellatus_hall_1866` (`type: true`) | p. 5: "CINCINNATIDISCUS (HEMICYSTITES) STELLATUS (Hall), 1856" | **Mismatch / cannot fully verify.** Printed year reads 1856, not 1866. The digits are clearly formed (no OCR ligature/italic risk), so this is either a real discrepancy between this citation and the taxon record's year, or a Bassler-side error; cannot verify without Hall's original publication. |
| `agelacrinites-subgenus > billingsi_chapman_1860` | p. 12: "HEMICYSTITES (AGELACRINUS) BILLINGSI (Chapman), i860"; plate 3 caption (p. 26): "*Hemicystites (Agelacrinus) billingsi* (Chapman)" | **Mismatch.** Printed twice as "(Agelacrinus)", not "(Agelacrinites)". Its sibling in the same node, `rectiradiatus_shideler_1918`, correctly prints "(Agelacrinites)" (p. 14). The two species do not share an original-genus citation and should not be grouped under the same subgenus-shaped node. (The printed year "i860" is the common OCR substitution of "i" for "1"; context makes 1860 certain.) |
| `carneyella > ulrichi_bassler_shideler_1936` (no flags at all) | p. 8: "CARNEYELLA ULRICHI, n. sp. (Bassler and Shideler)"; plate 6 caption: "Carneyella ulrichi, new species (Bassler and Shideler)"; prose (pp. 8–9): "The writer has included Dr. Shideler as coauthor of these two species, since both of us wish to name them in honor, respectively, of Drs. Ulrich and Foerste ..." | **Mismatch.** Node carries no `new: true`, despite being explicitly headed "n. sp." twice (main text and plate caption). See Cases §2 for the joint-authorship convention. |
| — (no node) | p. 8: "CARNEYELLA FOERSTEI, n. sp. (Bassler and Shideler)", plate 6 figs. 7–8, holotype "U.S.N.M. no. S-3965," occurrence Richmond (Arnheim), Russellville, Ohio | **Missing node.** No entry for this species anywhere in the tree. Its sibling *nicklesi* and *ulrichi* are both present under `carneyella`. |

## 3. Cases for the data model

**1. Bassler states his own parenthetical convention, and it is not a
subgenus.** P. 2: *"For facility of reference the original generic name of
the described species is inserted in parentheses."* This sentence is the
paper's own gloss on every "(Agelacrinus)", "(Agelacrinites)",
"(Hemicystites)", "(Lebetodiscus)", "(Echinodiscus)", "(Lepidodiscus)" seen
throughout — it is declared shorthand for "originally described in genus X,"
not a taxonomic subgenus assertion and not the standard ICZN
changed-combination convention (which would put the author's name, not the
genus, in parentheses). The existing `*-subgenus_*` taxa.yaml records
(`rank: subgenus`, `originalParent`, each flagged "Copied auth/year from
genus, unsure if correct") already approximate this well as a mechanism, but
this paper answers the "unsure if correct" doubt directly: it is not a
subgenus claim at all, only an editorial cross-reference device the author
names explicitly. Worth documenting the convention against this exact quote
so future sources citing similar parenthetical genera are not modeled as
true subgenera by default. It also means the grouping needs to be by
*genus cited*, not by current-genus + rank-shaped node: this paper alone
supplies two different original genera ("(Agelacrinus)" and
"(Agelacrinites)") for species presently held in the same current genus
(*Hemicystites*, *Discocystis*), which the mismatches above show the tree
sometimes conflates.

**2. A new species credited to two authors mid-paper, not on the title
page.** The title page and every other new-species heading credit Bassler
alone. Two species — *Carneyella ulrichi* and *C. foerstei* — are headed
"n. sp." followed by "(Bassler and Shideler)" in the same typographic slot
that elsewhere holds the original-genus parenthetical (case 1), then
explained in prose: *"This and the following new species ... were
discovered by Dr. W. H. Shideler ... The writer has included Dr. Shideler as
coauthor of these two species"* (pp. 8–9). This is a genuine joint
authorship for a protologue, printed via a parenthetical that formally reuses
the paper's other parenthetical convention for an unrelated purpose (credit,
not original genus). `auth: [Bassler, Shideler]` on both nodes, with the
explanatory sentence quoted in `notes`, would capture it; nothing in the
current schema conflicts, but the two unrelated uses of the same
"(Name)"-after-heading typographic slot are worth flagging so a future
data-enterer does not read a co-author parenthetical as an original-genus
citation or vice versa.

**3. A genus's account anticipates an unnamed species that turns out to be
the next heading.** See the `walcottidiscus-sp` mismatch above. The general
pattern — a genus diagnosis previews "a second species" or "another form" in
descriptive terms, then the very next heading names and redescribes exactly
that form — is a real risk for `openTaxon` placeholders: the diagnostic
prose must be checked against the next heading before a "new, unnamed
species" node is created from it.

**4. A tree assembled across a "Position Uncertain" aside that never draws
one hierarchy.** The words "Pelmatozoa" and "Blastoidea" appear nowhere in
this paper as classification headings. Bassler's only statements are: displaced
genera "might well be assigned to the Protoblastoidea, the first order of
blastoids" (p. 23, of *Astrocystites* and three genera not entered:
*Asteroblastus*, *Asterocystis*, *Blastoidocrinus*), and the family
Cyclocystoididae "must be left at present as an uncertain order of
Pelmatozoa" (p. 23). The tree's root (`pelmatozoa`, with children
`edrioasteroidea`, `blastoidea`, and the `pelmatozoa-incertae-sedis`
openTaxon) is an editorial synthesis of these two disconnected sentences,
not a hierarchy the paper itself draws — the same shape as roadmap B20 and
G7. Neither the `blastoidea`/`protoblastoidea` branch nor the `pelmatozoa`
root carries an `editorial.inferred` marker.

**5. The source contradicts itself on one parenthetical spelling.** *Discocystis
kaskaskiensis* is cited "(Agelacrinus)" in its heading (p. 21) and in the
plate 1 caption (p. 25), but "(Agelacrinites)" in the plate 7 caption
(p. 32). This is not obviously an OCR artifact (the two words are not visually
similar in this typeface) — it looks like the source's own inconsistency.
The tree follows the majority ("Agelacrinus") form; noting the print's own
inconsistency in `notes` would preserve it.

**6. "Genotype," no fixation method.** The paper uses only "genotype" or "the
type of the genus" throughout (pre-1966 terminology; the modern equivalent is
simply "type species"), and never states a fixation method (no "OD," "M,"
etc., anywhere in the text) — consistent with `type: true` alone and no
`typeFixation` value being available from this source.

## 4. Source record check

Title, journal, volume, number, authors and pubDate in `sources.yaml` all
match the printed title page (p. [i], PDF index 178/180: "SMITHSONIAN
MISCELLANEOUS COLLECTIONS / VOLUME 95. NUMBER 6 / NEW SPECIES OF AMERICAN
EDRIOASTEROIDEA ... BY R. S. BASSLER ... MAY 4, 1936").

**Missing `pages` field.** The record has no `pages` entry. From the running
heads and the printed pagination established above, the paper's own text
runs pp. 1–33 within vol. 95, no. 6, plus seven unpaginated plates ("With
Seven Plates," title page). The companion record `1935_bassler` also lacks
`pages`, so this is a shared gap rather than one specific to this record.
`1936_bassler` additionally has no `audit` block at all (unlike
`1935_bassler`, which carries `audit.state: partial`), so it defaults to
`unaudited`.

## 5. Uncertainties

- Plate images (I–VII) were not inspected — only the printed "Explanation of
  Plates" text (pp. 25–33) was read. Anything visible only in the figures
  themselves (e.g. the actual curvature or plate arrangement shown) cannot be
  verified from text alone.
- `stellatus_hall_1866`'s printed year on p. 5 reads "1856"; digit clarity is
  good, so this is flagged as a real discrepancy rather than an OCR guess,
  but which figure (1856 in this paper vs. 1866 in the taxon record) is
  correct cannot be verified without Hall's original publication.
- The plate-7-caption spelling "(Agelacrinites)" for *kaskaskiensis*
  (Case 5, Cases section) versus "(Agelacrinus)" elsewhere: cannot verify
  which, if either, is a compositor error internal to the 1936 printing.
- "(Miller), 1894" for *Carneyella faberi* (p. 9) gives no initials; whether
  this is S. A. Miller (as the taxon key `faberi_miller.s.a_1894` asserts)
  cannot be confirmed from this text alone.
- No year is printed anywhere in this paper for *Carneyella pileus* (Hall) —
  the genus account (p. 6) cites it only as "the genotype," no date. The
  taxon key's year (1866) cannot be checked against this source.
- Several isolated OCR corruptions in running prose (e.g. "Hohtype" for
  "Holotype," "V.S.'NM." / "U.S.'NM." for "U.S.N.M.," "ICENTUCKYENSIS" for
  "KENTUCKYENSIS") did not affect any taxonomic content checked above and are
  not listed individually.
