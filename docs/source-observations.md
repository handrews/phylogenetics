# Source observations: what the example publications show about the model

Read from the PDFs in `~/src/example-publications` and compared against the
tree files at `roadmap` @ `8cf0666`. Page numbers are the printed ones. Each
section ends with data checks for that source. Items that change the roadmap
are cross-referenced by id.

## 1975_bell.b.m — Bell, *Timeischytes casteri* (Bull. Am. Paleont. 67)

Scanned PDF with no text layer; read from page images.

**The in-press citation (p. 33 footnote; p. 35 "Order ISOROPHIDA Bell, 1974";
bibliography p. 50: "Bell, B. M. 1974. A Study of North American
Edrioasteroidea. New York State Museum Mem. 21, 500 pp., 63 pls.").** The
bibliography entry is for a book that did not exist as described: 447 pages
and 1976 when it appeared. The tree records "Bell, 1974" as printed with a
note. This is the case A6 is for.

**"May include" (p. 36).** Under the new suborder: "In addition to
*Timeischytes megapinacotus* and *Timeischytes casteri*, other members of this
group may include:" followed by eight species with author, year, age and
region, one of them "? *Postibulla jasperensis* Harker, 1953". Then "Family
CYATHOCYSTIDAE Bather, 1899 — ? Characters of the suborder." And on p. 37:
"Bather's family … is here placed under the new suborder Cyathocystina with
question. *Timeischytes* and *Hadrochthus* are tentatively added to the
Cyathocystidae."

So there are three hedges at three levels, all printed:

| level | printed | meaning |
|---|---|---|
| the whole list | "may include" | every listed membership is the author's guess |
| one item | "?" before *Postibulla jasperensis* | that item is doubted even within the guess |
| the family | "with question", "? Characters of the suborder" | the family's placement under the suborder is tentative |

The tree marks *Hadrochthus*, *Timeischytes* and *Postibulla* `provisional`
and leaves *Cyathocystis*, *Cyathotheca*, their species, and the family
unmarked. Under the roadmap's C table, "may include" is `provisional` on
every listed member, the "?" item is `provisional` plus `questionable`, and
the family node is `provisional` too, with the printed phrase in `notes` on
the suborder. See B16.

**Schmidt's year.** Bell prints "Cyathocystis plautinae Schmidt, 1880" and
"C. rhizophora Schmidt, 1880", and his bibliography (p. 51) gives "Schmidt,
Fr. 1880. Ueber Cyathocystis plautinae … Verh., ser. 2, vol. 15, pp. 1–5".
Bockelie & Paul 1983 cite the same paper as "Schmidt, F. 1879 … 1–7". Bassler
1935 gives 1880. A volume dated 1879 and issued in 1880 is the usual cause.
Both years are printed attributions of one work; the source record decides
which to use and says why. See A8.

**Two spellings of one epithet.** *plautinae* here and in Bockelie & Paul;
*plautini* in Bassler. The record already links them with `altSpellingOf`.

**Dual printed date.** Bibliography p. 51: "Jaekel, O. 1918 (1921)". Two
years on one entry, the second presumably the actual issue date. A8 again.

**Material (p. 48).** "Holotype NYSM 13289, Paratypes, NYSM 13263–13288,
13290", with a locality to the quarter-section and collectors named, then a
measurement per paratype (p. 49). A catalogue range plus a stray number is the
D1 `ids` shape; the measurements table is D1 `measurements`.

**Tentative combination in prose (p. 34).** "*Agelacrinites* (*sensu lato*)
*hanoveri* may belong to the genus *Postibulla* Bell, 1974." A hedged
recombination stated in the introduction, not in the systematics. It is a
placement claim with `provisional` and a `notes`, and it uses "sensu lato"
(B13).

Data checks:

- `plautinae_schmidt_1879` entry in the 1975 tree has `year: 1980` and
  `citedAs: Schmidt, 1980`. Bell prints 1880. Typo.
- The tree gives `rhizophora_schmidt_1889`; Bell prints "Schmidt, 1880";
  Bockelie & Paul write "(C. rhizophora; Jaekel 1899)", which may be an
  occurrence reference rather than an attribution. Three different years for
  one epithet, none of them verified against Schmidt. Record all three as
  printed and leave the taxon record's year with a note saying it is
  unverified.
- Cyathocystidae, *Cyathocystis*, *Cyathotheca* and their species are not
  `provisional` although the paper hedges all of them.

## 1980_bell.b.m — Bell, "Edrioasteroidea and Edrioblastoidea" (short course)

**"In preparation" (p. 164).** "Aepyaster Sprinkle and Strimple (in
preparation)" listed under Totiglobidae with no other comment. The data has
the `inprep_sprinkle_strimple` source with `inPrep: true` and the taxon record
says "never published so nomen nudum". Whether it was never published is not
established; a later summary cites the name without comment. The printed fact
is the citation; the availability judgement is editorial and should say when
it was last checked. See A9.

**Printed attributions per genus (pp. 163–168).** Every genus carries its
author and year, e.g. "Discocystis Gregory, 1879" (the record has 1897),
"Isorophosella Bassler, 1935" (a misspelling of *Isorophusella*). The tree
records the placements only. These printed attributions are the A-given data
that A2 turns into claims when they differ from the record.

**Tentative membership by "?" (pp. 165, 167).** "?Pyrgocystis Bather, 1915"
under Lebetodiscidae and "?Hadrochthus Bell, 1976a" under Cyathocystidae.
Both captured as `provisional`.

**Year letters.** "Bell, 1976a" throughout, and "Bell, 1976b" for the
ontogeny paper: the author's own letters, kept in `citedAs` (A7).

Data checks: none beyond the missing A-given attributions.

## 1983_bockelie_paul.c.r.c — *Cyathotheca suecica* (Lethaia 16)

**Rank change with parentheses (p. 263).** "Systematic position. — Class
Edrioasteroidea Billings 1858; Order Cyathocystida (Bell 1975). Definition
(emended)." The act itself is in prose on p. 262: "Since the suborder
Cyathocystina was defined (Bell 1975) on some of the characters of the
Devonian genera, we are redefining to exclude the Devonian genera, and
elevating it to an order." The parentheses around the authority are the
species-level convention for a changed combination, borrowed for a
suprafamilial rank change. In Treatise style this is "nom. transl. et emend.
Bockelie & Paul, 1983 (ex Cyathocystina Bell, 1975)". The tree has
`emended: true` and a note; B6 gives it `act: [nomTransl]`, and B17 records
the printed parentheses.

**Explicit exclusion (p. 262).** "we agree with Bell's original suggestion and
are confining the family Cyathocystidae to *Cyathocystis* and *Cyathotheca*."
The Devonian genera are removed. That is the `removed` relation (B5), and the
tree currently expresses it only by placing them elsewhere.

**Placement inferred by the editor.** The tree puts *Timeischytes* and
*Hadrochthus* under Isorophida with placeholder suborder and family and the
note "This part from the paper's text, order and suborder assumed." The paper
says only "specialized, probably neotenous, offshoots from the
Agelacrinitidae. We are uncertain whether to assign them to that family or to
a family (or families) of their own." The order is an inference from
Agelacrinitidae's placement in Bell 1980. An inference of this kind needs a
marker the claim table can read, not only a note. See B20.

**Informal phylogenetic diagram (Fig. 6, p. 263).** "Suggested phylogenetic
relationships between Cyathocystida, Edrioasterida and Isorophida and their
common ancestor *Stromatocystites*." Captured as a `diagram` phylogeny. The
caption names the ancestor as the genus; the tree's root is the order
`stromatocystitida`. Check the figure.

**Printed errors in citations.** "Cyathotheca suecica Jaekel 1977" (for 1927),
"Repell 1967" (Regnéll's 1966 Treatise chapter cited as 1967), "C. oklahomae,
Bell 1983" against a reference list entry of 1982, and Bell 1980 summarized as
placing Cyathocystina in "the order Isorophina" (it is Isorophida). All four
are printed attributions that do not match the works they point at. Each is
recorded as printed with `editorial.source` (A6), and each is a candidate for
the citation-error eval class.

**Type fixation statements.** "Type species. — *Cyathotheca suecica* Jaekel
1977, by original designation." and "Type species. — *Cyathocystis plautinae*
Schmidt, by monotypy." B14 fields, with the printed year error on the first.

Data checks: the diagram root rank; `oklahomae` and `rhizophora` notes are
right to leave the ambiguity open.

## 1993_dzik_orłowski — *Cambrocrinus* (Acta Palaeont. Polonica 38)

**Systematics (pp. 32–33).** "Class Cystoidea; Order Eocrinida Jaekel 1918;
Cambrocrinidae fam. n. — Genera included: *Cambrocrinus* Orłowski 1968,
*Eocystites* Billings 1868; *Cambrocrinus* — Type species; Species included:
Monotypic; *C. regularis* — 'Cambrocrinus regularis sp. n.; Orłowski 1968: p.
265, Pl. 3: 1–13.'; Holotype: UWWG W-970; Orłowski 1968: Pl. 3: 5; Type
horizon and locality; Emended diagnosis."

The tree has the skeleton, `new`, `type`, `emended` and the diagnoses. Missing:
the protologue usage with its page and plate, the holotype with its figure
locator, the type horizon and locality, and "Species included: Monotypic" as
an explicit statement of a complete list (the opposite of B16's hedge).

**What they said about relationships (pp. 28–32).** They accept Paul 1988's
placement "in his informal branch of the glyptocystitid rhombiferans" as a
phylogenetic position but argue *Cambrocrinus* "hardly has anything to do
with the lineage leading to *Macrocystella*" and "represents clearly a
separate branch of the eocrinoids". This matters for the next source.

Data checks: none.

## 2021_parsley — Gogiid–ascocystitid lineage (Paleont. J. 55)

**A subclass with the same name as its order (p. 974–975).** "SUBCLASS
GOGIIDA NOV." containing "Order Gogiida Broadhead, 1982". A subclass, not a
class; the record has it as Subclass. Same name, two ranks, two authorities,
one hierarchy. See B18.

**Declared incompleteness (p. 974).** "This is not a comprehensive listing of
the probable orders to be included in this sub class and those listed below
and includes only those whose representatives were part of this study." And
"Genera, e.g. *Gogia*, *Sinoeocrinus*, *Guizhoueocrinus*, *Globoeocrinus*". A
source stating that its own list is incomplete is different from a source
hedging membership: the listed placements are firm, the list is not the
whole. The tree quotes the sentence in `notes`. B16 gives it a field.

**A name that does not exist (p. 975; Fig. 1 caption p. 970).** "Family
Cambrocystidae Dzik and Orłowski, 1993" in the systematics and
"Cambrocystitidae" in the caption, for the family Dzik & Orłowski named
Cambrocrinidae. Two incorrect subsequent spellings in one paper, both linked
by `altSpellingOf` in the record with a note. Correct handling.

**A citation that contradicts its source (p. 970).** "Other authors have
placed them in post Cambrian lineages e.g. Cambrocrinus—Macrocystellids (Dzik
and Orłowski, 1993)". Dzik & Orłowski argued against exactly that placement
(their pp. 28–32); the placement was Paul 1988's. Both trees are captured, so
the claim table can put the two side by side. This is the best case in the
corpus for the citation-error eval.

**Attributions that differ from the record.** "Order Ascocystitida Frest,
2005" (record: 1982_broadhead); "Family Rhopalocystitidae Frest, 2005";
"Genus Rhopalocystis Ubaghs, 1967" (record: 1963); "CLASS EOCRINOIDA JAEKEL,
1918" (a third form beside Eocrinida and Eocrinoidea). The tree's notes on
Frest are right; A2 makes the differences claims.

Data checks: the "e.g." genera under Eocrinoidae have no incompleteness
marker; "Rhopalocystis Ubaghs, 1967" as printed is not recorded.

## Stokes 2021 — "Attribution of the taxon name Echinodermata to Klein, 1778" (Zootaxa 5061)

Not in `sources.yaml`. A two-page argument that Echinodermata should be
attributed to Klein 1778, p. 6, because Art. 11.4's binominal requirement does
not apply above the family group. It lists the competing attributions in use:
Klein 1734 (Hyman 1955), "Bruguière, 1791 [ex Klein, 1734]" (WoRMS, ITIS, and
this dataset's record), Bruguière 1789 (Ubaghs 1967, vernacular).

Across the tree files, Echinodermata is attributed 51 times: 34 with no
attribution, 9 to Bruguière 1791, 5 to Klein 1734, 1 to Bruguière 1789, 1 to
Fleming 1828. Two consequences:

- The record's `authority` is an editorial choice among published opinions and
  should say so; each differing printed attribution is a claim (A2), and
  Stokes 2021 is a source whose one claim is the attribution itself.
- Thirty-four sources print no attribution. Nothing is inferred from that. The
  link from a bare "Echinodermata" to the single record is an identity
  assumption the model makes for well-established high-rank names and nowhere
  else, and it is stated once as a rule (A10).

## Paul et al. 2024 — *Rhombifera* Barrande, 1867 (Spanish J. Palaeont. 39)

Not in `sources.yaml`.

**The same name at class and genus in one hierarchy (p. 5).** "Class
RHOMBIFERA Zittel, 1879 / Order DICHOPORITA Jaekel, 1899. Emend. Paul, 1972 /
Superfamily GLYPTOCYSTITOIDA Bather, 1899 / Family RHOMBIFERIDAE Kesling, 1962
/ Genus *Rhombifera* Barrande, 1867". The *Preface 2023* (xvii) says this
should not happen; it has happened since 1879. Separate records with different
authorities already exist; B18 states the resolution rule.

**Genus-level usages inside a species synonymy (p. 5).** "1879 Rhombifera
Barrande; Zittel, p. 424." and "1900 Rhombifera Barrande; Bather, p. 57."
listed among the *R. bohemica* lines because the genus is monotypic. Usages of
a genus accepted as usages of its only species. Record them under the species
with the genus as `taxon`; the claim table sees a genus-level usage accepted
for a species node, which is exactly what was printed.

**Lectotype designation (p. 5).** "As far as we are aware, no type has
previously been designated. We select as lectotype the original of Barrande,
1867, plate 11, figure 5, now in the National Museum, Prague (Reg. no.
L13001)." The specimen is identified first by the figure that depicts it and
second by its number. D2's designation act, with `formerIds` empty and a
figure locator on the material entry.

**Exclusion at figure level (p. 5).** "1996 Rhombifera bohemica Barrande;
Gutiérrez-Marco et al., p. 111, pl. 2, figs. 1–5, 11 (non fig. 6)." A usage
accepted except one figure. Neither `pars` nor `non` says which figures. See
D6.

**Other printed forms.** "?2015 Rhombifera sp.; Sumrall et al." ("?" before a
synonymy line: `tentative`); "2015ª" (a year letter as a superscript);
"Blastoidea *sensu lato*" (B13); "Paul, in press" (A6); "Emend. Paul, 1972"
on the order (`emendedBy`).

Data checks: the record has `rhombifera-class` and `rhombifera-order` as
"zittel 1870". This paper prints "Zittel, 1879" for the class, and its
synonymy cites Zittel 1879, p. 424. Check which Zittel work the record means.
The two records share one authority and should be linked by `altRankOf`.
