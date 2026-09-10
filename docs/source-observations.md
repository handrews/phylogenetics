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

## Kesling 1967, Treatise Part S — *Caryocystites* (pp. S229–S233)

`1967a_kesling` in `sources.yaml`; no tree captured. Read from the PDF text
layer. The genus entry on S229 is short and contains, by my count, eleven
distinct kinds of statement the model must carry. Parsed:

**The header.** "Caryocystites VON BUCH, 1846, p. 128". The Treatise's own
reference list (S263) has three von Buch entries: (29) 1840, Bericht, pp.
56–60; (30) 1844, Bericht "for year 1844", pp. 120–133; (31) "1846 (1845)",
Abhandlungen for 1844, pp. 89–116, "Gelesen … am 14. Mai 1844", "Preprinted
in 1845; regular issue in 1846". Page 128 falls inside (30), not (31). The
type-species citation "Caryocystites testudinarius VON BUCH, 1846, p. 19"
fits neither: p. 19 can only be the 1845 preprint's own pagination. So one
entry cites "1846" with pages from two other physical printings. The
bracketed remark on S229 adds "In 1846 (31) (or variously reported as 1844 or
1845)". The data has `1844_buch` (a `reading`, dated 3 March with a note that
"some sources incorrectly give May 3rd"), `1846a_buch` (Abhandlungen, pp.
89–116), and `1846b`/`1846c` (the English notice and translation), and no
record for the 1844 Bericht or the 1845 preprint. The Treatise says 14 May.
Three reading dates and four printings for one paper. See A11.

**The type species.** "*Caryocystis angelini HAECKEL, 1896, p. 59
(=*Caryocystites testudinarius VON BUCH, 1846, p. 19, OD, nom. in errore pro
'Sphaeronites testudinarius' HISINGER, 1837, pl. 25, fig. 8d, non fig. 9d,
recte 'S. citrus' HISINGER; non S. testudinarius HISINGER, 1826, p. 115,
=Heliocrinites granatum (WAHLENBERG); non S. citrus HISINGER, 1837, p. 91,
=Echinosphaerites aurantium (GYLLENHAAL); Amorphocystis buchi JAEKEL, 1899,
p. 339)". Unpacked, with the prose on S229 as the guide:

1. Von Buch designated a type (OD) and called it *Caryocystites
   testudinarius*, believing it to be Hisinger's *Sphaeronites testudinarius*.
2. He cited Hisinger's *Lethaea Suecica* "taf. 25, figure 9d". The lithographer
   had misplaced the numbers: the specimen von Buch meant is fig. 8d, which
   Hisinger's plate explanation labels "*S. citrus*", and which is neither
   *S. citrus* nor *S. testudinarius* but an unnamed species.
3. So von Buch's name is a *nomen in errore*: a name used for the wrong
   specimen. It is *not* Hisinger's 1826 *testudinarius* (which is
   *Heliocrinites granatum*) and *not* *S. citrus* (which is *Echinosphaerites
   aurantium*).
4. Haeckel 1896 named *Caryocystis angelini* for Angelin's plate 13, figs.
   4–9, which "more by accident than design" represent the same specimen. So
   the type species has a valid name after all, Haeckel's, and *Caryocystites*
   stands.
5. Jaekel 1899 overlooked Haeckel and named the same thing *Amorphocystis
   buchi*; under his scheme *Caryocystites* meant what is now *Heliocrinites*
   and *Amorphocystites* meant what is now *Caryocystites*.

What this needs from the model:

- **A misidentification record** (B10). Von Buch's usage is not a usage of
  Hisinger's name; it is a distinct name-in-error with its own type. It needs
  its own record, linked to the name it was mistaken for. Without it, the
  chain from *testudinarius* Hisinger to *angelini* Haeckel to *buchi* Jaekel
  cannot be stated.
- **A locator that corrects another work's locator** ("fig. 8d, non fig.
  9d"). Von Buch's tree keeps "9d" as printed; the Treatise's tree records
  the locator as `{plate: 25, figures: 8d, non: [9d]}` (D6) with the prose in
  `notes`. The mismatch is then a derived comparison, as in B19.
- **A genus-level name swap.** Jaekel's *Caryocystites* is a genus-level
  misidentification: the same name applied by him to a different genus. His
  own tree says what he said; the Treatise's synonymy says "Amorphocystites
  JAEKEL, 1896 (type, A. buchi JAEKEL = C. testudinarius VON BUCH)". No
  translation of Jaekel's names into later concepts is ever stored.
- **A `non` entry that also says where the excluded usage belongs** ("non S.
  citrus HISINGER, 1837, p. 91, = Echinosphaerites aurantium"). See B21.
- **Type fixation under a wrong name.** OD by von Buch, but the species the
  designation attaches to carries Haeckel's name. `type: true` and
  `typeFixation: OD` sit on *angelini*, whose synonymy holds von Buch's
  usage.

**Genus synonyms with name-group Latin.** "Caryoclstites D'ORBIGNY, 1850 (nom.
null.); Caryocystis ANGELIN, 1878 (nom. van.); Amorphocystites JAEKEL, 1896
…; Amorphocystis JAEKEL, 1899 (nom. van.)". The 1966 name groups are printed
in a source this dataset targets, so `nomNullum` and `nomVanum` enter the
`act` enum now (B6).

**Other vocabulary on these pages.** "recte" (correctly); "subgen. ad
Heliocystis" (a subgenus of); "sp. hypoth.?" on *Pomonites* (a hypothetical
species, S241); "partim"; "var."; "?Ulrichocystis" as a provisional genus in a
family; a dichotomous "Key to Genera", which is a complete membership list
with diagnostic characters (B16, `listComplete: true`).

**"?" inside a range.** "M.Ord., ?U.Ord., Asia(China)-Eu.(Sweden-Est.-?Wales)
- ?N. Am.(USA)". Doubt attaches to single elements of an age or region list,
not to the occurrence as a whole. See E8.

**Citations by index number.** Figures and remarks cite "(31)", "(69)",
"(99)": the volume's own numbered reference list. Like Bell's year letters
(A7), the number is what was printed and goes in `citedAs`; it resolves only
through that volume's list.

**Works cited but absent from the reference list.** "HISINGER, 1826, p. 115"
and "HISINGER, 1837, pl. 25" appear in the text; the Hisinger entries on S264
are 1802 and 1828 only. "BATHER in REED (12)" is Reed 1913, *Caradocian
Cystidea from Girvan*, with Bather's contribution, which is where "the
confusion regarding the type species was adequately resolved".

**The volume's year.** The title page says "Published 1967"; Paul et al. 2024
cite "Kesling, 1968, p. S178". A8 again.

**A pattern already in the data.** `sphaeronites` in `taxa.yaml` carries
"notes: The 1967 Treatise incorrectly cites page 185". That is a claim about
the Treatise, and it belongs on the Treatise's node for *Sphaeronites* as
printed (`pages: 185`) with an editorial correction, not on the taxon record.
See B22.

Data checks:

- `testudinarius_hisinger_1837` is `new: true` in the 1837 tree. The Treatise
  dates the name to Hisinger 1826, p. 115, and treats 1837 as the figure. If
  1826 is right, the 1837 node is a usage and the record's authority moves.
  Needs Hisinger 1826.
- `1840b_buch` has pages 56–59; the Treatise reference (29) gives 56–60.
- The 1844 Bericht (reference 30, pp. 120–133) and the 1845 preprint are not
  source records. The Treatise's page citations resolve only to them.
- Not in `taxa.yaml`: *angelini* Haeckel 1896, *buchi* Jaekel 1899,
  *Amorphocystites*, *Amorphocystis*, *Caryoclstites*, *Orocystites*,
  *Arachnocystites*. Not in `sources.yaml`: Angelin 1878, d'Orbigny 1850,
  Reed 1913, Hisinger 1826.
- The reading date: 3 March (record), 3 May (the typo the record mentions),
  14 May (Treatise). Which is the typo is not established by anything I have
  read.

Papers worth having for this one entry: Reed 1913 with Bather's appendix,
Hisinger 1826, the 1845 preprint of von Buch, and the 1844 Bericht.

## Printings in `sources.yaml` — the other preprint

A scan of `sources.yaml` for reprints, advance prints, readings and issue
dates. Five situations, one of them the twin of von Buch's.

**Hall 1866 / 1871 / 1872.** `1866_hall` is keyed as its own source: New York
State Museum 20th Annual Report, "number: Adv. Pr.", 17 pages, with the note
"Original 17 pages of the paper eventually published as 1872b_hall … there
was a revised edition with its own difficult-to-locate preprint." Bell 1976
cites all three printings in his synonymies (pp. 82, 91):

| year | printed as | what Bell dates to it |
|---|---|---|
| 1866 | "New York State Mus., 20th Ann. Rept. (adv. pub.): 7–8" | *pilea*, *stellatus*, *vorticellatus* (Hall), 1866 |
| 1871 | "24th Ann. Rept. (adv. pub.): Explanation of pl. 2, fig. 1–6" | *Cystaster* Hall, 1871; *C. granulatus* Hall, 1871 |
| 1872 | "24th Ann. Rept.: 215, pl. 6" | *Streptaster* Hall, 1872 |

So one paper's names are dated to three printings by the same later author,
depending on which printing first carried each name. The data has records for
1866 and 1872 and none for 1871, yet dates *cystaster* and *granulatus* to
1871. This is A11 exactly, and the Hall case is the cleaner of the two because
Bell spells out which printing carries what.

**Say 1825 reprinted with a commentary.** `1825a_say` (Journal of the Academy
of Natural Sciences) was reprinted in October 1825 in The Zoological Journal,
vol. II, pp. 311–315, immediately followed by `1825a_sowerby.g.b`, "A Note on
the foregoing Paper". The reprint is described in `notes` and is not a record,
so Sowerby's "foregoing Paper" resolves only through prose.

**Von Buch 1840 / 1841.** `1840a_buch` (the book) and `1841_buch` ("a direct
reprint, right down to identically typeset pages") are separate records with
no link between them. `1840c_buch` has `translationOf: 1840a_buch` while the
note on `1840a_buch` says 1840c translates 1840b. One of the two is wrong.

**Read, then printed.** `1854a`–`1854c_billings` carry `processDates.read`
and a `pubDate` months later; `1963_brown.i.a` is `read: 1963-11-27`,
`issued: 1964-04-10`, and keyed 1963. `1842_volborth` is headed "Read March
18, 1842" in the translation but has no `read` date in the record. The
Schmidt 1879/1880 question (A8) is the same question asked of the key: does
the year in a source key follow the volume, the reading, or the issue? The
records answer it three different ways.

Data checks:

- `streptaster` is `auth: [Hall], year: 1866`; Bell 1976 (p. 82) dates it to
  the 1872 printing, as a subgenus of *Agelacrinus*. Check the 1866 pages.
- No `1871_hall` record exists for the revised advance print that
  *Cystaster* and *granulatus* are dated to. The BHL page in the 1866 note is
  the lead.
- `1840c_buch.translationOf` disagrees with the `1840a_buch` note.
- `1842_volborth` lacks `processDates.read: 1842-03-18`.

## S229 revisited with the primary sources

Read from the 1844 Bericht, the 1846 Quarterly Journal translation, Hisinger
1828 and 1837, and Trans. Roy. Soc. Edinburgh 49 (1913). Each open item from
the Caryocystites section above, with what the sources say.

**The reading date is 14 March 1844.** Bericht 1844, p. 120: "14. März.
Gesammtsitzung der Akademie. Hr. v. Buch las über Cystideen, eingeleitet
durch …". So the record's 3 March has the wrong day and the Treatise's "14.
Mai" has the wrong month; the "May 3rd" the record calls a typo is a third
variant. Set `processDates.read: 1844-03-14` on the reading, and put the two
printed variants in `notes` with their sources.

**"1846, p. 128" is the Bericht, and "p. 19" is almost certainly p. 129.**
The Bericht report runs pp. 120–133. The genus header "CARYOCYSTITES" and
"3) Caryocystites Granatum Wahl." are on p. 128; "4) Caryocystites
testudinarius His." is on p. 129 (PDF 474–475). The Treatise's page for the
genus is therefore the Bericht's, cited under the Abhandlungen's year, and
its "p. 19" for the species is one dropped digit from 129 rather than a
preprint page. The English version (Quarterly Journal 2, pt. 2) has the genus
on p. 32 and the species on p. 33, inside the record's `1846c_buch` span.

**Von Buch's *testudinarius*: a deliberate transfer on a false premise.**
Bericht p. 129 cites "Sphaeronites testudinarius, Hisinger, Lethaea Suecica,
t. XXV. f. 9. d" for the elongated form and "t. XXV. f. 9. a" under *C.
granatum* for the round one. The 1846 translation (p. 34) explains: "Hisinger
has united this species with the former under the name Sphæronites
testudinarius, but since he has not given the reasons which induced him to
abandon the older name, S. granatum … I have thought it better to apply his
name to this remarkable species which he has considered as a variety."

Hisinger did no such uniting. Lethaea Suecica p. 92 treats the elongated
forms as "Obs. Formæ irregulares, globoso-subovatæ, rostris oppositis,
crassis, elongatis … ad Bödahamn Oelandiæ occurunt. Striæ valvularum ut in
Sphæronite Citro directæ (fig. 8. d.)": an observation appended to *S.
Citrus*, unnamed, unranked, and the only "Obs." in the book. He does not call
them a variety, and the book has a notation for that ("c. varietas" under
*Leptaena depressa*, p. 82; "ejusdem varietas", p. 93) which he did not use.
Von Buch, taking the spindle-shaped 8d for the fourth figure of series 9,
concluded that Hisinger had placed it under *testudinarius* as a variety, and
on that reading chose to apply *testudinarius* to it. Knowing act, wrong
premise.

For the model: Hisinger's forms become an `openTaxon` under *citrus* carrying
`identifier: "Formæ irregulares"`, the fig. 8d locator, and the sentence in
`notes`, with no rank inferred from von Buch's word; von Buch's
misidentification record (B10) then has a concrete target; and "which he has
considered as a variety" joins B19 as a printed claim about another work that
the work contradicts. "Variety" was a rank below species in 1837 and still
is in botany; here it is von Buch's word only.

**The plate is consistent with its explanation; the misplacement is
spatial.** Lethaea Suecica p. 91 lists "Tab. XXV. fig. 8 … d. rostris
elongatis" under *S. Citrus* and p. 92 lists "fig. 9. a. — b. valvula … c.
valvula … d. unus rhomboidum" under *S. testudinarius*; the plate (PDF 194)
matches: 8d is the spindle-shaped specimen with two rostra, 9d a single
rhomb. But 8d is drawn at the far right of the bottom row, level with 9a–9c,
so a reader takes it for the fourth figure of series 9. That is the
"lithographer's lapse in placing the numbers": the placement, not the
labels. Von Buch's "f. 9. d" is the reader's error the layout invited, and
the Treatise's "fig. 8d, non fig. 9d" is the correction. D6's locator shape
records both.

**Hisinger's *testudinarius* dates from 1837 and is a replacement name.**
Lethaea Suecica p. 92: "SPHAERONITES testudinarius … Echinosphærites granatum
VAHLENB. l. c. pag. 53. Sphæronites granatum His. Anteckn. VI. pag. 195. Tab.
VIII. fig. 1." He renamed his own 1828 combination of Wahlenberg's *granatum*
without stating a reason, which is what von Buch objected to. In the 1966
vocabulary that is a nomen vanum, a junior objective synonym; the 1837 node
gets `act: [nomNov]` and the existing synonymy already says the rest. The
name does not occur in the 1828 Anteckningar, whose *Sphaeronites* section
(pp. 195–197) has only *pomum* and *granatum*. The Treatise's "HISINGER,
1826, p. 115" is unsupported by anything here, and its own reference list
(S264) has no 1826 entry. Treat it as an error, as you supposed.

**Where the Treatise's "p. 185" for *Sphaeronites* came from.** Hisinger 1828
introduces *Sphaeronites* on p. 195. His footnote on p. 196 cites Meyer's
*Echino-Encrinites* in "Kæstners Archiv f. die Naturlehre, 1826 B. VII. S.
185". The Treatise's 185 is the page of the work Hisinger cites, not
Hisinger's page. The record's note is right; B22 says where it belongs.

**Reed 1913 is the wrong reference.** Trans. Roy. Soc. Edinburgh 49 contains
Bather's own memoir "Caradocian Cystidea from Girvan" (pp. 359–529; "Read May
13, 1912. MS. received March 8, 1913. Issued separately July 24, 1913"), and
the string "Caryocyst" occurs nowhere in the volume; the memoir's index has
*Caryocrinidae* and *Heliocrinus* only. The Treatise's "(12)" is Bather 1913
in its list, but the words "BATHER in REED" fit reference (13), "Note on
Yunnan Cystidea" (1918–19), which are Bather's notes in Reed's Yunnan
papers. So the resolution of the type-species question is in a work not yet
in hand, and the Treatise mis-numbered it. Index numbers can be wrong too
(A7). The Bather memoir's dates are another reading-then-separate-issue case
for A11.

Data checks from this pass:

- `1844_buch`: `processDates.read` should be 1844-03-14; the note about "May
  3rd" should say the Treatise prints 14 May.
- Add the 1844 Bericht as a source (Bericht 1844, pp. 120–133; genus p. 128,
  species p. 129), linked to `1846a_buch` by `printingOf` (A11).
- `testudinarius_hisinger_1837`: keep `new: true`; add `act: [nomNov]`.
- Von Buch's *testudinarius* needs its misidentification record (B10), keyed
  to whichever printing the authority rule picks, with the 1846 sentence in
  `notes`.
- Reed 1913 need not be added for this purpose; Bather's Yunnan notes are the
  target.

## Bather 1919 (Geol. Mag. dec. 6, vol. 6) — the wrong paper, twice over

**"Bather in Reed" is reference (11), not (12) or (13).** The Treatise's own
list has Bather (11) 1906, "Ordovician Cystidea from Burma: in [Reed], The
Lower Palaeozoic fossils of the Northern Shan States, Burma: Geol. Survey
India, Palaeontologia Indica, n.s. v. 2, mem. 3"; (12) is the 1913 Girvan
memoir; (13) the Yunnan notes of 1918–19 in the Geological Magazine. The
phrase "BATHER in REED (12)" on S229 pairs (11)'s description with (12)'s
number. The Girvan memoir never mentions *Caryocystites*, and the 1919 volume
holds only part III of the Yunnan notes ("Sinocystis compared with similar
genera", pp. 71–77, 110–15, 255–62, 318–25), which is about Diploporita.
The type-species resolution is in Bather 1906 in Reed's Burma memoir, which
also explains the Treatise's "Asia(Burma)" range for *Heliocrinites*.

**What the 1919 paper does contribute.** Two things for the model, neither
about *Caryocystites*:

- *Caryocystites* as a genus-level misapplication a second time (pp. 73–74).
  Hall 1861 named Silurian diploporites "*Caryocystites cylindricum*" and
  "*C. alternatum*" before erecting *Holocystites* for them in the 20th Annual
  Report; Winchell & Marcy 1865 added "*C. sphericus*". Under B18 and B10 these
  are records of *Caryocystites* sensu Hall with `misidentificationOf:
  caryocystites`, exactly as Jaekel's usage is.
- The printing history of the 20th Annual Report of the New York State
  Museum, the report your `1866_hall` advance print belongs to. Bather (p. 73):
  "the earlier pages seem first to have been issued in 1864 … The complete
  Report was issued (presumably in a limited edition) in January, 1865, and
  (more freely) in 1867; a revised edition was published in 1870." That is
  four issues in addition to the 1866 advance print Bell cites, and Bather
  dates names from it "1865-67". A11's Hall case has more printings than
  either Bell or the record knows.

Data check: none new. The paper still to find for S229 is Palaeontologia
Indica n.s. 2(3), 1906, Reed's Burma memoir with Bather's cystid chapter.

## 2012_doweld — *Heckerocrinus* nom. nov. (Paläont. Z. 86)

A two-page replacement-name note, read in full.

**The act.** "Heckerocrinus nom. nov. … proposed as a replacement name for
Bockia Hecker non Reisinger" and "Heckerocrinidae nom. nov. … instead of
illegitimate Bockiidae Ubaghs (1972: 4)". Under B6 both nodes carry `act:
[nomNov]`; the senior homonym *Bockia* Reisinger 1924 (a turbellarian) needs a
record so the `non` can point at it, even though it is outside the corpus.

**A re-dating by Article 13.3 (p. 457).** "Hecker did not designate type of the
genus, and thereby failed to publish an available (valid) generic name in
1938 … This was done later … (Hecker 1940: 38)". So Doweld cites "Bockia
Hecker 1940" throughout. The 2012 tree records `year: 1940` with "Reason for
erroneous year unclear"; the reason is now known and the year is a printed
claim, not an error. B14.

**Botanical vocabulary in a zoological paper.** "nom. illeg.", "legitimate",
"generotype", "Holotypus", "Derivatio nominis", and the citation device
"Heckerocrinus (Bockia) cucumis" with the replaced genus in parentheses. B6
records the words as printed and maps the act.

**Gender endings.** *neglecta* becomes *neglectus* under the masculine
replacement name, with *grava*/*gravus* and *sculpta*/*sculptus*. The tree
uses `altSpellingOf` pairs, which is the *Preface* rule (x–xi): agreement
changes are not new names.

**Material and doubt.** One line per species with "Holotypus: 2801/22 [Geol.
Institute, Russ. Acad. Sci. Moscow]" (repository in brackets after the
number) and an occurrence with "?Southwestern USA (West Texas) and ?Western
USA" (per-element doubt, E8).

**`type: true` on a synonymy entry (B3).** "Type species: H. neglectus
(Hecker) (Bockia neglecta Hecker)". The tree has *neglectus* as type under
*Heckerocrinus* and the *neglecta* entry with `type: true` and `parents:
[bockia_hecker_1938, bockiidae]`: the species was the type of *Bockia*. Same
shape as Kesling 1966's *Narrawayella* and *Savagella* entries.

Data checks: add `bockia_reisinger_1924` and the `non` on the 2012 node;
resolve the "erroneous year" note into the Art. 13.3 statement.

## Sources that cannot be had

Palaeontologia Indica n.s. 2(3) (Reed 1906, with Bather's cystid chapter) is
not in any online archive, and the Treatise's account of the *Caryocystites*
type species rests on it. This is the normal end of a citation chain, not an
exception: works exist that are undigitized, or digitized behind institutional
subscriptions priced for libraries. G1's `unobtainable` audit state records
the fact, and every claim that cites such a work stays secondhand with the
citing source named.


## Zittel 1879 — Handbuch der Palaeontologie, Band I, Abtheilung 1

The bound half-volume in hand carries "1876–1880" on its title page and
"1880" on the wrapper. The Vorwort (pp. vi–vii) says the first and second
Lieferungen were more than two years apart and that the Halbband is
"completed with the present Lieferung"; the Nachträge (p. 723) are "zur
ersten Lieferung" and cover the Protozoa. The scan has no part wrappers, so
the Lieferung that holds the Echinodermata (pp. 308–460 or so; the section
opens on p. 309) cannot be dated from it. Bather 1899, the Treatise, and Paul
et al. 2024 all cite the cystoid pages as 1879, which is the conventional
date of that part. Under A11 the source record is keyed `1879_zittel` for
that printing, with a note that the volume is 1876–1880 and the part date is
taken from later citations, not from a wrapper.

**What Zittel printed (p. 412, p. 417).** He adopts Johannes Müller's
three-way division and says so: "Joh. Müller … theilte darnach die Cystoideen
in 3 Gruppen ein: a) Formen ohne Poren (Aporitidae), b) Formen mit Doppelporen
(Diploporitidae), c) Formen mit Porenrauten oder gestreiften Rhomben
(Rhombiferi). Die Müller'sche Einteilung wurde auch im vorliegenden Buche
beibehalten". The heading is "3. Gruppe. Rhombiferi. Joh. Müll." So the
name is *Rhombiferi*, the rank is "Gruppe", and the attribution printed is
Müller's. The data's 1854 Müller tree records the rhomb-bearing group as an
unnamed placeholder ("Rhombifera, but not named") and *Diploporiten* as a
German vernacular, which is consistent: Zittel latinized what Müller left in
German or unnamed, and later authors credit the latinization to Zittel.
"Rhombifera Zittel, 1879" is therefore a corrected form (B6 `nomCorrect`) at a
different rank of Zittel's *Rhombiferi*, which Zittel credits to Müller: the
A10 pattern where the record's authority is a choice among printed
attributions.

Data checks:

- `rhombifera-order` and `rhombifera-class` have `year: 1870`; no Zittel work
  of 1870 exists in the data, and `aporita` already says 1879. Typo.
- Add a record for *Rhombiferi* (Zittel 1879, rank Group, `notes` quoting the
  heading) and link the class and order records to it as corrected forms.
- Add `1879_zittel` to `sources.yaml` with the volume note above.

## 1985_smith.a.b — Cambrian eleutherozoans and edrioasteroid diversification (Palaeontology 28)

Read from the volume scan's text layer; Table 3 (p. 734) checked against the
page image. Tree: `data/trees/1985_smith.a.b.yaml`, three taxonomies (Table 3
traditional column; Table 3 revised column; systematic headings pp. 736–753)
and one phylogeny.

**Re-ranking with the authority kept (p. 734).** The revised column prints
"Subfamily ISOROPHINAE Bell, 1976" and "Subfamily LEBETODISCINAE Bell, 1976";
the prose (p. 733) says "The two suborders erected by Bell could then be
transformed to the rank of subfamily; Lebetodiscinae (for the Lebetodiscina)
and Isorophinae (for the Isorophina)". Authority stays Bell's, the act is
Smith's. This is the `altRankOf` identity link plus a tree-level act (B18,
B6); both nodes now carry `modifier: nomen transl.`.

**Variant spellings printed in a table.** The traditional column prints "Order
STROMATOCYSTITOIDA Termier and Termier, 1969" and "Order EDRIOASTEROIDA Bell,
1976" (confirmed on the image), against Stromatocystitida and Edrioasterida
everywhere else, including the revised column. Records as printed: two
`altSpellingOf` records, cited from this tree; the current nodes point at the
standard spellings and lose the printed forms.

**A source that contradicts itself.** Table 3 prints "Genus EDRIODISCUS Smith,
1985" (p. 734); the genus heading prints "Genus EDRIODISCUS Jell, Burrett and
Banks, 1985" with the synonymy line "1985 *Edriodiscus* Jell, Burrett and
Banks, p. 190" (p. 753). Cyathocystidae is "Bather, 1899" in the traditional
column and "Bather, 1898" in the revised column of the same table, with the
prose (p. 730) saying 1899. Both are printed attributions that disagree with
the taxon record; recorded as printed on each node (`auth`/`year`/`citedAs`),
and the disagreement is derived (B19). Nodes in this tree carry no
attribution fields at all, so neither case is visible yet.

**"sedis mutabilis" and "(emend.)" (p. 734).** All three orders under the
plesion print "(sedis mutabilis)"; Isorophida and Cyathocystida print
"(emend.)" and have emended definitions (pp. 734–736). The tree has both only
on Cyathocystida. "sedis mutabilis" rides on `notes`; it has now appeared
three times in one table and once in the 1983 paper's vocabulary, so it earns
a flag (Wiley's convention for unresolved sibling order; distinct from
`provisional`).

**Plesion (Class).** "Plesion (Class) EDRIOASTEROIDEA Billings, 1858": a rank
and a parenthesised conventional rank on one line. The tree has `rank:
Plesion`; the "(Class)" is not captured. `citedAs` can hold the printed form.

**Editorial resolution recorded as prose.** The `stromatocystitida` node's
note explains that Termier & Termier 1969 is printed but Bell 1980 is used
as authority. That is `editorial.source` with the printed `citedAs`
preserved, exactly the A6 form.

**"Suborder uncertain".** The traditional column's "Suborder UNCERTAIN"
(Pyrgocystidae, Lispidecodidae, Rhenocystidae) is captured with Bell 1976's
placeholder `isorophida-uncertain-suborder_bell.b.m_1976`. The column is
"based on Bell 1980, but with later additions" and Rhenocystidae is 1984, so
the placeholder's identity across sources is an editorial equation, not a
printed one; a note on the node should say so.

**Type fixation.** Every "Type species." line names the mechanism: "by
original monotypy" (pp. 736, 746), "by original designation" (pp. 748, 749,
753). B14.

**Type species cited in its original combination (p. 753).** "Type species.
*Cyclocystoides primotica* Henderson and Shergold, 1971"; the recombination
line "1985 *Edriodiscus primotica* (Henderson and Shergold); Jell, Burrett and
Banks, p. 190" is not captured as `synonyms` + `parents`.

**One phylogeny for three cladograms.** The paper prints text-figs 9 (p. 728),
10 (p. 730) and 12 (p. 735). The single `phylogenies` entry is unlabelled and
its `savagella` exemplar belongs to text-fig. 10. Text-fig. 12 is image-only
in the scan, so the topology was not verified. Each printed figure should be
its own phylogeny with a `notes` naming it. The `bracket: edrioasteridae`
clade includes *Walcottidiscus*, which Table 3 places in the order, not the
family: a clade label wider than the formal name.

**Not captured:** genus and species synonymy lists (0 of 12 except
*typicalis*/*magister*), diagnoses and emended definitions (0 of 13),
material (0; BM(NH), USNM, MCZ, NYSM, CPC), occurrences (0), illustrations
(0; text-figs 1–20, pls. 87–89).

Source record: title, volume 28 part 4, pp. 715–756, received 7 October 1984,
revised 25 March 1985 all match. Plates 87–89 are not recorded.

Data checks:

- Add `emended: true` and the sedis mutabilis marker to `edrioasterida` and
  `isorophida` in the revised taxonomy.
- Add `citedAs` on `edriodiscus` (both taxonomies) and `cyathocystidae`
  (revised: 1898) so the printed disagreements are recorded.
- Alt-spelling records for *Stromatocystitoida* and *Edrioasteroida*.
- Split the phylogeny into the three printed figures, once text-fig. 12 has
  been read from the image.

## 1985_jell_burrett_banks — Cambrian and Ordovician echinoderms from eastern Australia (Alcheringa 9)

Read from the text layer; printed page = PDF index + 182. Tree:
`data/trees/1985_jell_burrett_banks.yaml`, one taxonomy, no `notes`.

**A whole class missing from the tree (p. 205).** "Class RHOMBIFERA / Family
ECHINOENCRINITIDAE Bather 1899 / Echinoencrinitid indet." with material
UTGD54622, announced in the abstract (p. 183). Also missing: "Family
undetermined / Eocrinoid plates indet." (ANU36961–36964, p. 205). Both keys
exist in `taxa.yaml`; the gap is in this tree.

**`new` on open placeholders.** Six open or cf. nodes carry `new: true` with
no nomenclatural act printed ("CAMBRASTER sp.", "?STROMATOCYSTITES sp.",
"Stromatocystitid indet.", "Isorophid indet.", "Macrocystellid indet.",
"CAMBRASTER sp. cf. C. TASTUDORUM"). In this dataset a placeholder's
authority is the source that first needed it, and the loader requires `new`
wherever a node's taxon has this source as authority, so the flag is
consistent. It is not a protologue. The roadmap should say that `new` on an
`openTaxon` or `cfTaxon` means "this source originates the placeholder", so
the claim table does not emit it as a new name.

**"the holotype" of an unnamed form (p. 196).** "Details of the oral frame are
not clear, particularly on the holotype" is said of NMVP107129 under
"Isorophid indet.", which the paper leaves "in open nomenclature within the
order". A printed role word that cannot be a nomenclatural type. Record the
word as printed (`roleAsPrinted`, D1) and let the contradiction stand.

**A paratype that is not one (p. 190).** The `primotica` node lists
`paratypes: [CPCl1396, NMVP107479]`. The paper designates only CPCl1396 as
"Paratype" (Henderson & Shergold's 1971 type series); NMVP107479 is this
paper's own new specimen, assigned "based on comparison". A referred
specimen, not a paratype; a data error to fix.

**Type species with original combination and fixation (p. 185, p. 192).**
"Type species. *Trochocystites cannati* Miquel 1894 … by original
designation" is captured as the type flag only; the original combination
(`synonyms` + `parents`, as done for *primotica*) and the fixation (B14) are
not. "*Stromatocystites pentangularis* Pompeckj 1896, by monotypy" has no
node at all.

**Attribution on the record disagrees with every source (p. 185).**
"CAMBRASTER Cabibel, Termier & Termier 1958" here and in Smith 1985 (p. 734,
p. 749); `taxa.yaml` has `auth: [jaekel]`, `year: 1923`, and no tree in the
data marks the genus `new`. Check where 1923 came from; if Jaekel 1923 is a
nomen nudum or a different name, the record needs a note either way.

**Paper-internal inconsistencies, kept as printed.** UTGD122233 is a paratype
of *C. tastudorum* (p. 186) and material of *C.* sp. cf. *C. tastudorum*
(p. 188). NMVP107074 is figured (fig. 10B, p. 198) but absent from the *C.
jagoi* paratype list (p. 197). Both belong in `notes` on the material entry;
neither is a data error.

**Genus synonymy in prose (p. 185).** "the synonymy of *Eikosacystis*
Cabibel, Termier & Termier 1958 … recognised … by Ubaghs (1971)": a synonymy
this source accepts from another, not captured.

**Not captured:** occurrences (0 of 6 localities, four numbered NMVPL
localities with grid references, formation and zone, pp. 183–184), all 18
figures, diagnoses (0 of 5), repository prefixes NMVP, UTGD, CPC, TMF, ANU
(p. 184; F-item registry, scoped per source).

Source record: title, volume 9 number 3, pp. 183–208, DOI, received 22
November 1984 and online 27 November 2008 all match. The header prints
"1985:08:26", which is not in the record; meaning unverified (an issue date
would matter for the key-year rule).

Data checks:

- Add the Rhombifera and "Family undetermined" branches.
- Add `pentangularis_pompeckj_1896` as type under *Stromatocystites*, and
  the *Trochocystites cannati* original combination.
- Move NMVP107479 out of `paratypes`.
- Resolve the *Cambraster* authority.

## 1994_guensburg_sprinkle — Revised phylogeny of the Edrioasteroidea (Fieldiana Geol. n.s. 29)

Read from the text layer; printed page = PDF index − 11. Tree:
`data/trees/1994_guensburg_sprinkle.yaml`, one taxonomy and four
phylogenies (Fig. 2A–D, p. 5). The taxonomy is a synthesis of three printed
structures: the Systematic Paleontology header (p. 13), the Revised
Classification (pp. 12–13, repeated verbatim as section headings) and the
Appendix genus compilation (pp. 42–43). None of the three alone is the tree;
a `notes` on the tree should say so.

**Eight re-rankings, each with its derivation printed.** All are this paper's
acts, all downward except two: "Family LEBETODISCIDAE Bell, 1976 (nomen
transl., emend.)" ex suborder Lebetodiscina; "Subfamily LEBETODISCINAE Bell,
1976" ex "the Lebetodiscidae Bell, 1976" (p. 27); "Subfamily CARNEYELLINAE
Bell, 1976" ex "the family Carneyellidae Bell, 1976" (p. 27); "Subfamily
PYRGOCYSTINAE Kesling, 1967"; "Suborder EDRIOASTERINA Bather, 1898" ex
"Bather's family Edrioasteridae as defined by Bell (1976a, 1980)" (p. 13);
"Suborder EDRIOBLASTOIDINA Fay, 1962" ex class Edrioblastoidea; "Subfamily
CYATHOCYSTINAE Bather, 1899" ex "the family Cyathocystidae of Bather, 1898,
and the order Cyathocystida, Bell, 1975" (p. 21); "Subfamily RHENOPYRGINAE
Holloway and Jell, 1983" ex "their family Rhenopyrgidae" (p. 21). All eight
carry `modifier: nomen transl.`. This source and Smith 1985 re-rank
Lebetodiscina in opposite directions, which is why the act lives in each
tree (B18). Note the Cyathocystinae line, which names two predecessors at
two ranks in one sentence: the B6 derived-from link may need to be a list.

**One name, two acts in one paper.** Lebetodiscinae is "(nomen transl.)" on
p. 12 and "(nomen transl.. emend.)" on p. 27, with "it is emended to allow for
separation of pyrgocystinids". The tree follows p. 12. The node should carry
`emended: true` with a note that the classification list omits it; the
discrepancy is the source's own.

**Placeholder invented at two ranks.** The Appendix heading "Order and Family
Uncertain" (p. 42) holds *Cambraster* and *Walcottidiscus* directly. The tree
nests `edrioasteroidea-order-uncertain` over
`edrioasteroidea-family-uncertain`. One printed placeholder, two editorial
ones; mark the inner node `editorial.inferred` or collapse to one placeholder
whose note quotes the heading.

**Provisional in prose, unflagged.** "'Totiglobus' lloydi was provisionally
assigned to genus at the time of its description because of poor
preservation (Sprinkle, 1985)" (p. 19): `quoted: true` is captured,
`provisional` is not. "The new genus is provisionally assigned to … the most
primitive taxon of agelacrinitids" (p. 25) for *Deltadiscus*: not flagged.
B16 said `provisional` only where "?" is printed; "provisionally" in the
prose is at least as strong and should count.

**Attributions printed here that disagree with the records.** Camptostromatidae
"Durham, 1968" (pp. 12, 42) against 1967; *Isorophus* and *Carneyella*
"Foerste, 1917" (p. 42) against 1916; *Edriodiscus* "Smith, 1985" (p. 42),
the same slip Smith's own Table 3 makes; *Cambraster* "Cabibel, Termier, and
Termier, 1958" (p. 42) against Jaekel 1923. The 1916/1917 pair looks like a
reading-versus-issue question (A8) rather than two typos. None is visible
because the nodes carry no attribution fields.

**Declared scope limits (p. 42).** "several subfamilies are likely present,
but these are not treated here" and "the list is not exhaustive": the
`listComplete: false` case (B16) on Agelacrinitidae and on the Appendix as a
whole.

**In-press addendum (p. 25, footnote).** A second *Deltadiscus* specimen,
paratype FMNH PE 52719, "discovered by Colin Sumrall while this paper was in
press", with its own occurrence. Material added after acceptance is still
this source's statement; a note on the material entry suffices.

**Secondhand placement declined (p. 19).** "*Walcottidiscus* … has been
presented as the sister group to the edrioasterids (Smith & Jell, 1990, p.
771) … we omitted this taxon from the parsimony analysis." A B19 citation
attached to a taxon this source places only under the uncertain placeholder.

**Cladogram terminals of mixed rank (p. 5).** Agelacrinitidae (family),
Pyrgocystinae and Lebetodiscinae (subfamilies) and *Chatsworthia* (a genus
the classification puts inside Lebetodiscinae) are coordinate terminals. The
flat `taxon` reference handles it; recorded as the example. Branching was
checked against the prose (pp. 3–4, 18–20) only; the figure's line structure
is not in the text layer.

**Not captured:** material and occurrences for the five new species and three
"Species Indeterminate" groups (pp. 14–37), diagnoses (0), Table 1 (42
characters) and the matrix (Fig. 1), the prose comparison with Bell 1980 and
Smith 1985 (pp. 12–13), the Jaekel 1927 attribution and "(Fig. 17D)" on the
*Cyathotheca* synonymy note (p. 21).

Source record: title, series and number, authors and the printed "Published
December 30, 1994" match. "Accepted May 27, 1994" is on the same page and is
not recorded; pages 1–43 are not recorded.

Data checks:

- `lebetodiscinae`: `emended: true` with a note on the p. 12 / p. 27
  difference.
- `provisional` on `lloydi_sprinkle_1985` and `deltadiscus`.
- Mark or collapse the two-rank uncertain placeholder.
- `citedAs` on the five nodes whose printed attribution disagrees with the
  record; resolve *Cambraster* and the Foerste 1916/1917 question.
- `processDates.accepted: 1994-05-27` and `pages: [1, 43]` on the source.

## Across the three papers

- The same family-group name is re-ranked in opposite directions by Smith
  1985 and Guensburg & Sprinkle 1994. Identity stays one `altRankOf` chain in
  `taxa.yaml`; each act is a node in the tree that made it.
- Attribution on classification nodes is absent in all three trees, so every
  printed attribution that disagrees with a record (six cases across the
  three) is invisible. The claim table's citation-error class needs
  `auth`/`year`/`citedAs` on nodes wherever the printed line has them.
- "sedis mutabilis", "provisionally assigned", and "(nomen transl., emend.)"
  are each printed more than once across the set; each earns a field or a
  documented mapping rather than `notes`.
- *Cambraster* Jaekel 1923 in `taxa.yaml` is contradicted by both 1985 papers
  and by 1994.
