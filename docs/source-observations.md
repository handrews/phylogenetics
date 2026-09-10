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

# Reading round of 2026-09-09: 24 papers

Reviewed against their trees with the shared brief in the session scratchpad; coverage is stated per kind only (G9). The roadmap items this round produced are A12–A13, B23–B27, D8–D9, E9 and the extensions to B14, B16, C4, G7 and G8.

## 1842_vanuxem — Agelacrinites hamiltonensis (Geology of New-York, Part III)

Read from the volume's text layer across two windows (pp. 156–171, 304–306); printed page = PDF index − 9. The tree holds one taxonomy, no phylogeny, keyed to Vanuxem's brief survey-report treatment of *Agelacrinites*. Coverage in one sentence: beyond the classification skeleton, the *hamiltonensis* protologue carries an occurrence, an exact plate/figure citation and an English diagnosis, but three further species keys rest on bibliographic cross-reference outside the read windows and were not verified this pass (G9).

**A new genus proposed in first-person narrative (p. 158).** Vanuxem writes: "it therefore establishes a new genus, for which the name of Agela-crinites is proposed... and hamiltonensis for the species." The tree's `new: true` on both `agelacrinites` and `hamiltonensis_vanuxem_1842` is fully supported; no other author is credited anywhere in the passage.

**A diagnosis captured with a genuine mid-paragraph elision (p. 158).** The `diagnosis` field quotes the opening and closing of Vanuxem's description verbatim but elides the middle sentences on the six medallions' size and arrangement via "....". This is a coverage choice within an already-populated field, not a printed truncation; the field should be read as partial rather than complete.

**A name credited to another author, undescribed in this source (no page cited on the node).** `hallii_conrad.t.a_1842` carries `new: true` and the taxon record's `authority: {attributedTo: [conrad.t.a], source: 1842_vanuxem}`, but the node's own note reads "No description or figures," and no page could be located in either read window to check the printed passage. This is a name attributed in print to one author (Conrad) inside another author's (Vanuxem's) publication with no accompanying description — closer to A3's `attributedTo` mechanism than to a protologue, but the printed wording itself could not be verified.

Source record: title, book, date, and single authorship all check out against the title page and the first-person narrative voice.

Data checks:

- `1842_vanuxem.yaml`: the `hamiltonensis_vanuxem_1842` occurrence's `location` list merges "United States" and a stray "upper quarry" continuation line into one six-element list (should be seven), a YAML block-scalar artifact, not a printed value.

**Addendum, full read (2026-09-10).** All nine nodes now check against the
print. *Nucleocrinus hallii* is on p. 163, a bare binomial under a rank-less
"Crinoidea." heading in a list Vanuxem blanket-credits to "the Reports, etc.
of T. A. Conrad"; `attributedTo` is right and `new: true` remains the open
question (B25). The root "Crinoidea." is printed (p. 163) but as a list
label, not a family. Of the four names in the top-level note: *Pentacrinites
hamptonii* (pp. 63–65) is a figured bare name; *Encrinites lævis* (p. 132,
"for the present may be termed") is Vanuxem's own hedged name and has no
record (`lævis_conrad.t.a_1842` is Conrad's *Ichthyocrinus lævis*, a
different species); *E. triciclas* (pp. 182–183) is figured and described
and credited "it appears" to the late Prof. Eaton; *Echinus drydenensis*
(p. 184) carries a full description under a conditional name, a hedged
protologue (B24), not a nomen nudum. Wood-cut numbers run through the
volume, which is why cut 80 sits at the end.

## 1848b_forbes — Cystideæ of the Silurian Rocks of the British Islands (Mem. Geol. Surv. Gt. Britain 2)

Read from the text layer, printed page = PDF index + 374; the Cystideæ paper (pp. 483–538) follows the companion Asteriadæ paper in the same continuous scan. The tree holds one taxonomy, no phylogeny, covering all 8 genera Forbes treats. Coverage in one sentence: new taxa, most synonymy lists, and the `or` alternative-name convention are captured; material, occurrences, illustrations and all but one diagnosis are not (G9).

**A genus credited to the wrong author (p. 504).** Forbes writes "the characters which were assigned by **Von Meyer** to his genus Echino-encrinites," crediting Von Meyer throughout for the genus name; `taxa.yaml`'s `echino-encrinus`/`echinoencrinus` record instead carries `auth: [Volborth], year: 1842`. Volborth is credited in this same paper only for observations on tentacula and a separate Bulletin note, never for the genus. The node carries no attribution field, so the disagreement (A2/B19) is currently invisible.

**Two alternative generic names as one printed heading, not two synonymous genera (pp. 514–515).** "SPHÆRONITES (Hisinger), or ECHINO-SPHÆRITES (Wahlemberg)" is a single header presenting two names joined by "or," each with its author in parentheses as a citation, not a subgenus. The tree's `sphæronites: {or: [echino-sphærites]}` matches this exactly.

**Blanket hedges on a genus's whole species list, not individually flagged (pp. 510, 512).** Forbes writes "I provisionally refer to this genus the following fossils" for *Hemicosmites* and "With the exception of the first species in the list, the descriptions given must be regarded merely as provisional" for *Caryocystites*. Neither hedge is recorded in `notes` on the respective parent node, though B16 calls for exactly this; the individual `provisional` flags on the "?"-marked species within each list are correctly unaffected.

**Prose-only "provisionally" hedges with no printed "?" (pp. 504, 518).** Two new species — *Prunocystites fletcheri* ("I have named it provisionally...") and *Sphæronites arachnoideus* ("I name it provisionally as above") — are hedged in prose only, with no "?" in their headers. Neither carries `provisional: true`, consistent with the model's convention of flagging only a printed "?," but the textual hedge itself is recorded nowhere on either node.

Source record: title, journal, volume/number, pages and plates all match the printed article; `sources.yaml`'s title field carries a trailing ".pdf" not part of the printed title ("On the CYSTIDEÆ of the Silurian Rocks...", p. 483).

Data checks:

- `1848b_forbes.yaml`: the `echino-encrinus` node's `notes` assigns "Echino-encrinus" to the formal diagnosis and "Echino-encrinites" to general commentary; printed usage is the reverse (diagnosis headed "ECHINO-ENCRINITES," p. 509; general prose "ECHINO-ENCRINUS," p. 504).
- `sources.yaml` `1848b_forbes.title`: drop the trailing ".pdf".

## 1852_hall — Palæontology of New-York, vol. 2 (Clinton and Niagara Cystideæ, Asteriadæ, crinoids)

Read across two windows (PDF 255–265, printed p. 236–246; PDF 374–380, a non-unique page range shared by the main text and the "Additions and Corrections" section). The tree holds two disjoint taxonomies (Clinton and Niagara groups), no phylogeny. Coverage in one sentence: new-taxon flags and illustrations are captured for the read windows' genera; synonymy beyond a few genera, material, occurrences and diagnoses are not (G9).

**A genus flagged new though the source reconciles two earlier ones.** Hall's header reads "Genus EUCALYPTOCRINUS." with no "(nov. gen.)" tag, followed by the printed synonymy "*Eucalyptocrinites*, Goldfuss, 1826" and "*Hypanthocrinites*, Phillips, 1839," and Hall's own text: "there is no sufficient character to separate it from the Genus Hypanthocrinites." `taxa.yaml` already treats `eucalyptocrinus` as `altSpellingOf: eucalyptocrinites` with no authority tied to this source, directly contradicting the tree's `new: true` on the same node — the clearest internal inconsistency found in this file.

**A genuine printed dagger, not a data artifact (p. 246).** "Figs. 18, 19, 20 and 20†," with "Fig. 20†. A still farther enlargement of a part of a specimen" printed as its own caption, confirms `illustrations: [[18,20], "20†"]` matches the source exactly.

**A synonymy assembled from two passages 55 pages apart (pp. 238, 300).** The tree's tentative *Hemicystites*/*Agelacrinites* synonym note draws on Hall's Addenda ("this genus is apparently identical with Agelacrinites of Vanuxem... which I had overlooked," p. 300) and an earlier footnote on Forbes's unrelated redefinition of the name (p. 238), neither of which sits on the genus's own main-text page (245). The synonymy is correctly resolved to Vanuxem's record, but the node's `pages: 245` field does not point to the text that actually supports the claim.

**The same epithet, two genera, one volume (pp. 187, 232).** *Glyptaster brachiatus* n. sp. and *Myelodactylus brachiatus* n. sp. are both genuinely new in this work; `taxa.yaml`'s `originalParent: glyptaster` / `originalParent: myelodactylus` on the two `brachiatus_hall_1852_*` keys is a clean, verified instance of the disambiguation the roadmap describes.

Source record: book, volume, year and author all match the title page; neither `paleo-ny` record in `sources.yaml` (1847 or 1852) carries `title`/`pages`/`identifiers`, a consistent convention for this book rather than an omission.

Data checks:

- `1852_hall.yaml`: `eucalyptocrinus` carries `new: true`, contradicted by the printed heading (no "nov. gen.") and by `taxa.yaml`'s own `altSpellingOf: eucalyptocrinites` record (genus heading, pp. 207–211 area).
- `1852_hall.yaml`: `papulosus_hall_1852` notes field reads "Compare Lucalyptocrinus decorus"; the printed text (p. 211) uses Hall's own abbreviation "*E.*" [Eucalyptocrinus], not the OCR-garbled genus name.
- `1852_hall.yaml`: `decorus_phillips.j_1839` notes field reads "Compare f7. celatus. Ip. pag. 113..."; the printed line (p. 207) reads "Compare *E.* cælatus. *Id.* pag. 113...".

## 1854c_billings — Cystidea from the Trenton Limestone, Second Paper (Canadian Journal 2)

Read from pp. 268–274 of the whole-volume scan (printed page = PDF index − 53 in this stretch); the article is Billings's "Second Paper," distinct from the identically-titled `1854a_billings`/`1854b_billings` "First Paper" split across two issues. The tree holds one taxonomy, no phylogeny. Coverage in one sentence: new genera and species are fully flagged; synonymy, material, occurrences and diagnoses are not captured at all (G9).

**A genus name introduced twice, narrative then formal (pp. 268–269).** Billings first names *Comarocystites* in a descriptive header ("the fossil for which the above generic name is proposed") on p. 268, then gives its terse formal diagnosis ("Body ovate... column round") on p. 269 under a repeated header. The tree's note ("First given on page 268, formal definition starts on page 269") is verified word-for-word correct.

**Two populations under one placeholder (pp. 271–273).** Billings reports small specimens he confidently calls *Agelacrinites* ("I have no doubt but that they are Agelucrinites [sic]") and, separately, a large, extensively redescribed fossil he suspects is "certainly... a different genus" but does not name. The tree's `openTaxon: agelacrinites-sp_billings_1854` correctly captures the small-specimen population (C4); the large, unnamed suspected-different-genus population is not represented anywhere, though it receives the greater share of Billings's description.

**Inconsistent new-taxon notation across the author's own two papers.** This installment introduces both new genera in full prose with no "n. gen."/"n. sp." abbreviation, unlike the First Paper's explicit "(Now. gen.)" [Nov. gen.] marker (p. 215). Not a dataset error, but a documented inconsistency in Billings's own practice worth keeping distinct from a modelling gap.

Source record: pages 268–274, volume 2, and authorship all confirmed directly; the "Limestonee" double-e spelling recurs identically in both the First and Second Papers and is the genuine printed title, not a data-entry duplication.

Data checks:

- `1854c_billings.yaml`: `punctuatus_billings_1854` illustrations list records only figs. 1 and 3; fig. 2's caption is also printed on p. 270 and is omitted.

## 1857_billings — Report of E. Billings for 1856 (Geological Survey of Canada, Report of Progress 1853–56)

Read from pp. 256–295 ("Descriptions of New Fossils," Asteriadæ subsection pp. 290–295); printed page = PDF index − 15 in this range. The tree holds one taxonomy, no phylogeny, spanning Crinoidea, Cystideae and Asteriadae. Coverage in one sentence: the classification skeleton and every `new` flag match the Contents page exactly; synonymy, material, occurrences and diagnoses are entirely uncaptured, matching this report's early place in scope (G9).

**Three new species keyed under the wrong genus (pp. 290–291).** "PALŒASTERINA STELLATA," "PALiEASTERINA RIGIDUS" and "PALJEASTERINA RUGOSUS" (OCR renderings of *Palæasterina*) are all printed directly under that genus heading; the tree keys `stellata_billings_1857`, `rigidus_billings_1857` and `rugosus_billings_1857` under `palæaster` instead. The `palæasterina` node's own note, "Noted from other source, but no new species described," is directly contradicted by these three species.

**Two attribution conventions in one report (pp. 261, 292).** Billings's own new genera carry no author at all ("Genus CYCLASTER." / "CYCLASTER BIGSBYI."), marked instead with the phrase "(new genus.)" (Hybocrinus, Carabocrinus, Cleiocrinus); genera he is merely using carry "(Author.)" ("Genus HETEROCRINUS, (Hall.)"). One paper later, `1858b_billings` prints "Billings" directly on his own new taxa. Neither convention is captured in any `citedAs` field on either tree — an unused mechanism for exactly this case (A1/A2).

**A subgenus given in parentheses, at both genus and species rank (pp. 261, 263).** "Genus THYSANOCRINUS (Hall), RHODOCRINUS (Miller)" and "THYSANOCRINUS (RHODOCRINUS) MICROBASALIS" both use the standard bracketed-subgenus form. The tree already nests `rhodocrinus-subgenus` correctly under `thysanocrinus`, but no node preserves the exact printed heading form.

Source record: chapter title, pages 247–346 and authorship match the printed Contents entry exactly.

Data checks:

- `1857_billings.yaml`: `stellata_billings_1857`, `rigidus_billings_1857` and `rugosus_billings_1857` are keyed under `palæaster`; all three are printed under `Palæasterina` (pp. 290–291), and the `palæasterina` node's note is contradicted by them.

## 1858b_billings — On the Asteriadae of the Lower Silurian Rocks of Canada (Figures and Descriptions of Canadian Organic Remains, Decade III)

Read pp. 75–85 (printed page = PDF index − 3), plate VIII. The tree holds two taxonomies (the genus-level revision, and a second "speculative" suborder tree), no phylogeny. Coverage in one sentence: the *Edrioaster*/*Agelacrinites* half of this revision is fully placed with illustrations and synonymy; the paper's other main achievement — three new genera absorbing five recombined species — is represented only as bare, childless genus nodes (G9).

**A junior homonym forces a replacement name, with a priority argument (p. 82).** "In my report for 1856 this genus is called Cyclaster; but I find that this name had been a short time previously given to a genus of sea-urchins by M. Cotteau... This number of the Bulletin was published in March 1857, but my Report was not issued until the autumn following." The identity side is modelled (`cyclaster` vs. `cyclaster_billings_1857`, `homonym: true`), but Billings's own priority argument — the reasoning behind the replacement — exists only in this quoted paragraph.

**An attribution traced to a one-line popular-journal diagnosis (p. 75).** Billings quotes his own 1857 introduction: his attribution of *Palasterina* (and *Palæaster*, *Palæocoma*) rests on a single-sentence generic diagnosis in Silliman's Journal, November 1856, itself superseded by Salter's fuller 1857 paper, which Billings cites only by mention. The current `notes: "As defined by Mr. Salter, 1857"` compresses this 1856-diagnosis/1857-details distinction into one year the quoted prose does not support.

**An author's own admission of a mixed-up specimen (p. 83).** "I regret, that, in consequence of mistaking the meaning of Prof. E. Forbes' remarks... I supposed this [*Edrioaster Bigsbyi*] to be the specimen discovered by Dr. Bigsby... Since then I have seen Dr. Bigsby's specimen, and find it to be A. Dicksoni. It is too late now to change the names." Neither `bigsbyi_billings_1857` nor `dicksoni_billings_1857` records this admitted name/specimen crossover; it belongs in `notes` on one or both.

**The Edrioasteridae name proposed as a hedge, not an act (p. 85).** "...it is probable that they will be arranged as a sub-order, for which the name Edrioasteridæ would be appropriate..." — three layers of hedging around a name that is nonetheless treated as the group's working label in the same sentence, and is universally cited as the taxon's protologue. The tree's `questionable`, `provisional` and `new` flags on `edrioasteridæ-suborder` capture this reasonably, but no single flag distinguishes "proposed as a suggestion" from "proposed and now in use."

Source record: title, volume (Decade III), pages 75–85 and authorship all match the printed title page and plate heading.

Data checks:

- `taxa.yaml`: `palasterina` (used by this tree) is an orphan record with no `altSpellingOf`, distinct from the linked `palaeasterina`/`palæasterina` pair that `1857_billings.yaml` uses for the same genus — three identity records for one name.

## 1915_bather — Studies in Edrioasteroidea (self-published, reprinted from Geological Magazine)

No tree file exists for this source. The volume collects nine numbered Studies (Dec. 1898 – Sept. 1915) plus two short 1899 letters, each kept in its original *Geological Magazine* pagination; this is an A11 "several printings" situation on the reprint/original-serial axis rather than the printing/printing axis. Nine studies contain: two new genera and species from disarticulated material (I, *Dinocystis Barroisi*), one full redescription (II, *Edrioaster Buchianus*), one new genus by recombination (III, *Lebetodiscus* for Billings's *Agelacrinites Dicksoni*), a broader revision naming at least one further new species in running text (IV, "*E. laevis*"), one new genus from a misclassified Cystidean (V, *Steganoblastus*), one new genus with three new species (VI, *Pyrgocystis*), and three synthetic/comparative studies with no new taxa (VII–IX).

**A source record that matches none of the nine printed items.** The single existing record, `1915_bather`, is titled "Studies in Edrioasteroidea IV. Pyrgocystis n. g." with `pages: [49, 90]` and `pubDate: 1915-12-06`. *Pyrgocystis* is printed as Study VI, not IV; its two parts run pp. 5–12 (Jan. 1915) and 49–60 (Feb. 1915), so the record's pages match neither part fully, and `number: 5–12` reads as a fragment of Part I's own range misfiled into the wrong schema field. The 1915-12-06 date matches no printed date for either part.

**A cited authority with no source record to resolve to.** *Lebetodiscus* (Study III) is credited in `taxa.yaml` to `auth: [bather], year: 1908`, but no `1908_bather` source record exists anywhere in `sources.yaml` — an established citation with nothing to resolve to (A6).

A source record for this volume would need: separate entries per Study (or per Study-part, where a Study prints two citation brackets, e.g. VI and VII), each keyed to its own year and *Geological Magazine* pagination; a `printingOf`-style link from each to the 1915 volume, which adds a stated corrigendum (a text-figure's ray numbering, Study VII) and new horizon information (Studies I and V) not in the originals.

Data checks:

- `sources.yaml` `1915_bather`: title, Roman numeral, `pages` and `pubDate` all misidentify the printed item; the record should describe Study VI ("Pyrgocystis, n.g.," pp. 5–12 and 49–60, Jan./Feb. 1915), not Study IV, and likely needs splitting into two part-records.

## 1935_bassler — The Classification of the Edrioasteroidea (Smithsonian Misc. Collections 93)

Printed page = PDF index − 1 (pp. 1–11 plus one unnumbered plate). The tree holds one taxonomy, no phylogeny, matching the paper's Class→Family→genus→species order exactly (18 genera under Agelacrinitidae, 2 under Edrioasteridae, 2 under Cyathocystidae). Coverage in one sentence: the classification skeleton, all six new genera, all three new species and every type-species flag are captured; material, occurrences, illustrations, diagnoses and attribution fields are not (G9).

**Two "not X" genus-homonym citations, conflated with the record they exclude.** The paper prints three "A, author, year, not B, year" citations (p. 3, p. 9): "Cyclaster Billings, 1857, not Cotteau, 1856," "Agelacrinites Forbes, 1848, not Vanuxem," and "Hemicystites of authors not Hall." Only the first has a distinct identity record in the corpus; the second is entirely absent from the tree's synonymy, and the third (`cincinnatidiscus`'s synonym entry) points its `taxon` at the very `hemicystites` record the printed phrase excludes. This is the same shape as the *Caryocystites*/*Heliocrinites* misidentification case B10 already covers: a name reused by a different author needs an anchor of its own, not a pointer to the name it was excluded from.

**A bracketed genus name that means two different things in one paper.** In the systematic text, "X (Y) species" is a same-year subgenus grouping (e.g. "Hemicystites (Cystaster) granulatus Hall, 1871," p. 3); in the plate explanation, the identical bracket shape becomes a "current genus (original genus) species" cross-reference for readers of older literature, and even drops the actually-cited subgenus (*Lepidodiscus*) in favour of the plain original genus (p. 10). Six of the plate's ten described figures follow this second pattern; a single bracket-reading rule cannot serve both parts of the paper.

**"New name" at family rank, worded identically, treated two different ways.** "Family AGELAGRINITIDAE, new name" (p. 2) and "Family ASTROCYSTITIDAE, new name" (p. 10) are worded the same, but only the latter carries `new: true` in the tree — because `taxa.yaml`'s authority choice differs (Astrocystitidae: Bassler 1935; Agelacrinidae/Agelacrinitidae: Chapman, 1860), not because of anything in the printed line. Bassler's own paper credits the superseded family form to "Agelacrinidae Jaekel, 1899" (p. 2), not Chapman 1860, and the Chapman, 1860 date matches the adjacent Class-level synonym on the same page — worth checking whether the family record's authority is a copy of that neighbouring entry.

Source record: title, journal, volume/number, `pubDate` 1935-04-04 and author all match the printed title page; the record has no `pages` field (printed pagination is pp. 1–11).

Data checks:

- `1935_bassler.yaml`: `agelacrinites` synonyms list omits "Agelacrinus authors," the fourth of four printed synonyms (p. 7).
- `1935_bassler.yaml`: `edrioaster` synonyms list omits "Agelacrinites Forbes, 1848, not Vanuxem," the fifth of five printed synonyms (p. 9).
- `1935_bassler.yaml`: `buchianus_forbes_1848`'s synonym entry has `parents: [agelacrinites]`, pointing at Vanuxem's genus though the printed line explicitly excludes it ("not Vanuxem," p. 9).
- `1935_bassler.yaml`: `cincinnatidiscus`'s `pars: true` synonym entry has `taxon: hemicystites`, pointing at Hall's genus though the printed phrase excludes it ("Hemicystites of authors not Hall," p. 3).

## 1936_bassler — New Species of American Edrioasteroidea (Smithsonian Misc. Collections 95)

Printed page = PDF index − 181 (pp. 1–33 plus seven unnumbered plates). The tree holds one taxonomy, no phylogeny. Coverage in one sentence: the classification skeleton and every type-species flag are captured; synonymy, occurrences, illustrations and diagnoses are essentially uncaptured, and material is captured for only 3 of roughly 23 new species (G9).

**A stated convention explains every bracketed name in the paper (p. 2).** Bassler writes: "For facility of reference the original generic name of the described species is inserted in parentheses." Every "(Agelacrinus)," "(Agelacrinites)," "(Hemicystites)" bracket in this paper is this declared shorthand for "originally described in genus X," not a subgenus claim. The existing `*-subgenus_*` taxa.yaml records (each flagged "unsure if correct") can now drop that doubt for citations from this specific source; the paper also supplies two different original genera ("Agelacrinus" and "Agelacrinites") for species presently grouped under the same current genus, which the mismatches below show the tree sometimes conflates.

**A new species credited to two authors, printed in the same typographic slot as the case above (pp. 8–9).** *Carneyella ulrichi* and *C. foerstei* are headed "n. sp. (Bassler and Shideler)," explained in prose: "The writer has included Dr. Shideler as coauthor of these two species." This reuses the paper's own parenthetical-name convention for a different purpose (joint authorship, not original genus) — worth flagging so a future data-enterer does not conflate the two uses of the same slot.

**A genus account previews an unnamed species that turns out to be the next heading (p. 2).** The *Walcottidiscus* genus account describes "a second species possessing the same generic features... but with curved ambulacra, four... directed to the left, and one... to the right" — the identical curvature described in the very next heading, "WALCOTTIDISCUS MAGISTER, n. sp." No other species of the genus is mentioned anywhere in the paper. This is a general risk for `openTaxon` placeholders: a genus diagnosis's forward reference to "another form" must be checked against the next heading before treating it as a distinct, unnamed taxon.

**An editorial synthesis presented as a hierarchy the paper never draws.** The words "Pelmatozoa" and "Blastoidea" never appear as classification headings; Bassler's statements are two disconnected sentences (displaced genera "might well be assigned to the Protoblastoidea," p. 23; Cyclocystoididae "must be left... as an uncertain order of Pelmatozoa," p. 23). The tree's `pelmatozoa` root with `blastoidea`/`protoblastoidea` and `pelmatozoa-incertae-sedis` children is an editorial assembly of these two sentences (G7/B20), and neither branch carries an `editorial.inferred` marker.

Source record: title, journal, volume/number, authors and `pubDate` (May 4, 1936) match the printed title page; the record has no `pages` field, a gap shared with `1935_bassler`.

Data checks:

- `1936_bassler.yaml`: `walcottidiscus-sp_bassler_1936` (openTaxon, `new: true`) double-counts *W. magister*, described by anticipation in the same genus account (p. 2), as a separate unnamed species.
- `1936_bassler.yaml`: `granulatus_hall_1871`'s synonym note asserts the source prints "(Hemicystite)" (singular); both printed occurrences (p. 4; plate 1 caption, p. 25) read "(Hemicystites)."
- `1936_bassler.yaml`: `billingsi_chapman_1860` is grouped under `agelacrinites-subgenus`; both printed occurrences (p. 12; plate 3 caption, p. 26) read "(Agelacrinus) billingsi," not "(Agelacrinites)."
- `1936_bassler.yaml`: `ulrichi_bassler_shideler_1936` carries no flags at all, despite being headed "n. sp." twice (p. 8; plate 6 caption).
- `1936_bassler.yaml`: no node exists for *Carneyella foerstei*, n. sp. (holotype USNM S-3965, plate 6 figs. 7–8, p. 8), though its siblings *nicklesi* and *ulrichi* are both present.

## 1945_regnell — Non-Crinoid Pelmatozoa from the Paleozoic of Sweden (Meddel. Lunds Geol.-Min. Inst. 108)

No source record or tree file exists for this paper; it surfaces in the corpus today only as an external citation in later trees. Printed page = PDF index − 9 for the arabic-paginated body (pp. 1–255). The relevant content is two systematic treatments (a classification-chapter pass, pp. 43–49, and a full systematic pass, pp. 197–223) plus an extensive historical-citation apparatus naming essentially every prior author on Edrioasteroidea and Cyclocystoidea.

**Two new species, one new class-level act, within scope.** *Cyclocystoides lindströmi* and *C. insularis* (pp. 216–223) are both full new-species descriptions with holotypes. "Class Paracrinoidea nov." (p. 14) is a new class-list entry whose diagnosis (p. 37) is outside the read range. No genus or family is erected for edrioasteroids in this paper; *Stromatocystites balticus*, *Cyathotheca suecica*, and all four *Pyrgocystis* species are redescriptions/recombinations, not new acts.

**A footnoted self-correction of another author's date (p. 14).** "In his paper of 1918... JAEKEL gave 1899 as the year of publication for the term Eocrinoidea. This is not correct... since the term was not... even mentioned in JAEKEL's memoir of 1899." A worked A8 case: Regnéll corrects a cited author's own self-citation.

**A citation Regnéll uses to override a later author's priority claim (pp. 208–209).** Regnéll cites Bather 1915a (pp. 52–53) as having "described and analysed the spiral plate arrangement years before Hecker (1939) claimed it as a first observation" — a printed B19-style correction of one cited work by another, made by the current source itself rather than merely reported.

A source record for this paper would need: title, author (OCR renders "Regnell" as "Reonell" on the first title-page scan), series/number (Meddelanden från Lunds Geologisk-Mineralogiska Institution N:r 108), 1945, pp. I–VIII + 1–255 + 15 plates; no received/accepted/online date is printed anywhere in the volume. `data/sources.yaml` and `data/trees/` confirm no record or tree exists.

Data checks:

- None — no existing record to check against.

## 1961_rievers — Eine neue Pyrgocystis aus den Bundenbacher Dachschiefern (Mitt. Bayer. Staatssamml. Paläont. hist. Geol. 1)

Printed page = PDF index − 9 (pp. 9–11); a posthumous manuscript (Rievers died 1955) edited for publication by Dehm, who states he limited his own contribution to foreword, minor edits, added measurements, and the plate. The tree holds one taxonomy, no phylogeny — the sole new species and its genus. Coverage in one sentence: the holotype, occurrence, and illustration range are fully captured; the diagnosis is only partly captured and per-figure captions are not (G9).

**A two-sentence diagnosis captured only in part (pp. 10–11).** The printed Diagnose reads, in full: "Eine Pyrgocystis von 95 mm Größe mit einem geschuppten Turm..." (dimensions) followed by "Am oberen Ende trägt der Turm die kronenförmige Theka, von der sich, durch 5 Dreiecke gebildet, die Ambulacra abheben" (the crown and five-triangle ambulacral arrangement). The tree's `diagnosis` field stops after the first sentence; the second — diagnostically the more distinctive character — is omitted even though `pages: [[10, 11]]` already spans both pages.

**A holotype identified only by a plate figure, in a private collection (p. 11).** "Holotyp (und einziges Stück): das in Taf. 2, Fig. 1—4 dargestellte Fossil, Sammlung Rievers, Enkirch (Mosel)" — there was never a museum accession number. The dataset's D1 mechanism ("a material entry may have no catalogue number... a `label` and its `illustrations`, and nothing else") is a direct fit, though the current node still uses the pre-D1 `specimens: {RVS: {holotypes: [...]}}` shape with the plate citation standing in for an `ids` value.

Source record: title, journal, volume, `pages: [9, 11]`, `pubDate.year: 1961` and author all match the printed article completely.

Data checks:

- None confirmed; the diagnosis omission is a coverage gap within an already-populated field rather than a printed-text mismatch.

## 1961_dehm — Über Pyrgocystis (Rhenopyrgus nov. subgen.) coronaeformis Rievers (Mitt. Bayer. Staatssamml. Paläont. hist. Geol. 1)

Printed page = PDF index − 11 (pp. 13–17), immediately following Rievers's paper in the same Heft. The tree holds one taxonomy assembled from comparative prose, no phylogeny. Coverage in one sentence: the type-species flag and all nine comparanda's placements/occurrences are captured; the subgenus diagnosis itself is not captured anywhere (G9).

**The subgenus diagnosis has no home on its own node (p. 16).** "Diagnose von Rhenopyrgus nov. subgen.: Pyrgocystis (mit turmförmiger... Theka...) mit folgenden Besonderheiten: Theka groß und schlank... Typus-Art der Untergattung: Pyrgocystis coronaeformis Rievers (1961)." Only the final, type-fixing sentence is reflected (as `type: true`); since this is one of the two gold-slice protologues, the missing diagnosis text is the single most consequential gap in the file.

**A tree assembled from comparative prose, not a printed list (G7).** The species list under `pyrgocystis` (sardesoni, grayae, volborthi, gracilis, pulkovi, sulcata, procera, cylindrica, octogona) is compiled from one paragraph (p. 15) written to establish which species resemble *coronaeformis*, not to classify the genus. The tree presents it as an ordinary `children` list indistinguishable from a printed systematic list, the same situation G7 already describes for the 1994 tree.

**A same-volume, already-resolved citation with no roadmap label.** Dehm cites Rievers twice: informally ("(S.9)") and fully, resolved, in the bibliography ("Rıevers, J. †, 1961... Diese Zeitschr., 9—11"). Unlike A6's in-press case, this citation resolves cleanly — both papers share one publication date, and the direction (Dehm cites Rievers, never the reverse, since Rievers wrote in 1955) is fixed. Neither node marks this same-volume relationship, which the roadmap does not yet have a label for.

Source record: title, journal, volume and author match, with two small wording differences from the printed title (bracket placement, and species-epithet case).

Data checks:

- `1961_dehm.yaml`: the subgenus node is keyed `taxon: rhenopyrgus` with a node-level `rank: subgenus` override, instead of the dedicated `rhenopyrgus-subgenus` record that three later trees (`1966_regnéll`, `2013_sumrall_heredia_rodríguez.c.m_mestre`, `2020_ewin_martin.m_isotalo_zamora`) use for this same identity.
- `sources.yaml` `1961_dehm.pages`: `[12, 17]`; the article begins at printed p. 13 (p. 12 belongs to Rievers's plate leaves) — should read `[13, 17]`.

## 1962_fay — Edrioblastoidea, a New Class of Echinodermata (J. Paleontology 36)

Printed page = PDF index + 199 (pp. 201–205). The tree holds one taxonomy, no phylogeny — class, genus and species only, since the paper erects no order or family. Coverage in one sentence: the classification skeleton is complete; synonymy is partly captured (one of five citations), and material, occurrences, illustrations and the class diagnosis are not (G9).

**A class placed directly over a pre-existing genus, no order or family between them (p. 201).** "The genus *Astrocystites* Whiteaves is removed from the Edrioasteroidea and placed in a new class of echinoderms, Edrio-blastoidea..." Both words "order" and "family" are absent from the paper entirely. This monotypic class-directly-over-genus shape is unusual for the rank hierarchy but is exactly what the source prints.

**A `type: true` flag the source itself never states (throughout).** Fay never writes "type species" for *Astrocystites*; the genus is simply treated as monotypic. The flag on `ottawaensis_whiteaves_1897` is plausible but would have been fixed, if anywhere, in Whiteaves's 1897 original description, which has no source record in this dataset — a B20-style case (editorial inference of identity rather than placement) with no `editorial.inferred` marker.

**The same specimen called both "holotype" and "syntype" by its own author (pp. 201, 205).** The plate caption reads "Holotype, 752"; the body text reads "The holotype, No. 752... It is labelled a syntype because another specimen, lent to Mr. Hudson... was the other syntype. When Hudson died, this specimen disappeared." This is Fay's own contradiction, not an OCR artifact. The tree's `specimens.syntypes` entry picks one term without noting either the contradiction or the lost second syntype.

Source record: title, journal, volume/number, pages and `pubDate` all match; `identifiers.jstor: 13011100` has an extra digit (the printed Stable URL has seven digits, `1301100`).

Data checks:

- `sources.yaml` `1962_fay.identifiers.jstor`: `13011100` should be `1301100` (extra digit).

## 1978_bell.b.m_sprinkle — Totiglobus, an Unusual New Edrioasteroid (J. Paleontology 52)

Printed page = PDF index + 242 (pp. 243–266); the source file is named for the revised manuscript's receipt date, not the 1978 publication date the running head and citation line both confirm. The tree holds one taxonomy, no phylogeny, matching the printed Systematic Paleontology hierarchy exactly. Coverage in one sentence: the classification skeleton, with correct `new`/`emended` flags, is fully captured; diagnoses, material, occurrences and illustrations are not (G9).

**A family's diagnosis explicitly deferred to its species, because monotypic (p. 247).** "Genus TOTIGLOBUS n. gen.... Diagnosis.—The monotypic genus has the characteristics of the type species." The genus's printed "diagnosis" is a statement that none is needed; the schema's single-string `diagnosis` field has no way to record "deferred to <node>, because monotypic" distinct from "not printed." The identical pattern recurs in the companion 1983 Holloway & Jell paper (family deferring to genus).

**A second in-preparation citation earlier than the roadmap's own example (pp. 245–246).** "*Aepyaster* Sprinkle & Strimple (in preparation)" is treated here as a second, coordinate genus of family Totiglobidae, described in the family diagnosis with a "clavate theca" contrasted against *Totiglobus*'s "subgloboid theca" — but no node exists for it, so the family's `children` list is visibly incomplete against its own printed diagnosis. This citation predates the one A9 currently documents from Bell 1980.

**Two informal, quoted prior citations of the new species (p. 247).** "'Poorly preserved edrioasteroid,' SPRINKLE, 1973... 'New edrioasteroid,' SPRINKLE, 1976..." sit exactly where a synonymy would go. Neither is captured; both are clean H-table candidates ("a usage with no name, cited by a phrase") for `openTaxon`/`quoted` placeholders.

**A family attribution the tree cannot show disagrees with the record (pp. 245–246).** The paper credits family Edrioasteridae to "Bell, 1976" throughout, but `taxa.yaml`'s canonical authority is Bather, 1898. The node carries no `auth`/`year` at all, so this disagreement (A2) is currently invisible; which authorship is correct cannot be verified without both works in hand.

Source record: title, journal, volume/number, pages, `pubDate` and JSTOR identifier all match with no discrepancy.

Data checks:

- None confirmed as data errors; the Edrioasteridae and *Isorophus* year questions are attribution conflicts (see the closing list), not tree mistakes.

## 1983_holloway_jell — Silurian and Devonian Edrioasteroids from Australia (J. Paleontology 57)

Printed page numbers appear directly in the text (pp. 1001–1016). The tree holds one taxonomy, no phylogeny, covering five families across two branches (Rhenopyrgidae; Isorophida's three families). Coverage in one sentence: the classification skeleton, `new` and `type` flags are fully and correctly captured; diagnoses, material, occurrences and illustrations are not, and every synonymy/`parents` entry omits its printed citation detail (G9).

**A family's diagnosis deferred to its genus, and the genus's type fixed by monotypy alone (p. 1002).** Family Rhenopyrgidae's protologue has no "Diagnosis" heading at all, only "Remarks... distinguished by the characters cited in the generic diagnosis below." No "Type genus" sentence is ever printed either — the family is simply stated to "include only *Rhenopyrgus*." Neither deferral nor the implicit type-genus fixation has a place on the `rhenopyrgidae` node, which carries no `diagnosis` field.

**An order left unresolved between two named candidates, not a bin (pp. 1002–1004).** "Order UNCERTAIN" is followed by an extended two-sided argument weighing Isorophida against Edrioasterida for Rhenopyrgidae's placement. This fits neither of C4's senses (not a heterogeneous bin, not simply unnamed) — the source names two specific orders and cannot choose. The `openTaxon` placeholder captures the heading correctly, but the argument giving the uncertainty its content is not referenced anywhere in the tree.

**A secondhand claim that appears to contradict its own cited source (p. 1004).** "*P. octogona* Richter, 1930 was assigned to *Rhenopyrgus* by Dehm (1961)..." — but Dehm's actual 1961 paper concludes the opposite, keeping the two species separate and naming only *coronaeformis* as type. Since both works are in this dataset, the B19 comparison is directly checkable; neither tree records it.

**An explicit, named rank-elevation argument against two prior authors (p. 1004).** "Although considered to be a subgenus of *Pyrgocystis* by Dehm (1961) and Regnell (1966), *Rhenopyrgus* differs from that taxon... we discount the possibility of an evolutionary relationship... suggested by Dehm (1961)." This is the printed reasoning behind the B18 genus/subgenus split already present in `taxa.yaml`; the tree uses the correct (genus) key, but the argument itself is recorded nowhere.

Source record: title, journal, volume/number, pages, `pubDate` and both manuscript dates all match with no discrepancy.

Data checks:

- None confirmed; the recurring missing citation detail on synonymy entries is a coverage gap (four instances in this file), not a specific error.

## 2006_sumrall_brett_cornell — Pyrgopostibulla belli (J. Paleontology 80)

Printed page = PDF index + 186 (pp. 187–192). The tree holds one taxonomy, no phylogeny, matching the printed header exactly. Coverage in one sentence: the classification skeleton and both new-taxon/type flags are fully captured; synonymy (none printed), material, occurrences, illustrations and diagnoses are not (G9).

**A rankless hierarchy, with one exception (p. 190).** The printed header runs "EDRIOASTEROIDEA Billings, 1858 / ISOROPHINA Bell, 1976b / ISOROPHIDA Bell, 1976b / AGELACRINITIDAE Chapman, 1860 / POSTIBULLINAE Sumrall, et al., 2000 / Genus PYRGOPOSTIBULLA new genus." No rank word appears above genus level, but "Genus" is printed before the genus name. The tree's top-level `notes: No ranks are included` slightly overstates this — the supra-generic convention is correct, but the genus-level "Genus" tag is in fact printed.

**A printed sequence that inverts true rank order, corrected silently (p. 190).** The header lists Isorophina (suborder) above Isorophida (order), an inversion of an otherwise high-to-low list. The tree nests by the correct rank hierarchy rather than reproducing print order, flagging the anomaly with `notes: "Isorophida and Isorophina are switched, surely by error"` rather than an `editorial` block — a defensible choice since the placement itself is not in doubt, only the print sequence, but a borderline case worth keeping on record for when `editorial` vs. `notes` is next revisited.

Source record: title, journal, volume/number, pages, authors, acceptance date and JSTOR id all match with no discrepancy.

Data checks:

- `2006_sumrall_brett_cornell.yaml`: the top-level `notes`, "No ranks are included," overstates the print — the word "Genus" is printed before the genus name (p. 190).

## 2009_sumrall — Neoisorophusella maslennikovi (J. Paleontology 83)

Printed page = PDF index + 989 (pp. 990–993). The tree holds one taxonomy, no phylogeny. Coverage in one sentence: the classification skeleton and the new-species flag are captured; the paper's central nomenclatural story — a genus- and species-level nomen nudum resolved by this paper — is entirely absent, along with material, occurrences, illustrations and diagnoses (G9).

**Ranks printed under explicit editorial disclaimer, not the author's own usage (p. 991).** "Discussion.—Inclusion of Linnaean ranks reflects editorial policy rather than the views of the author." The tree's top-level `notes` paraphrases this accurately — a clean instance for G8 ("rank stated in the tree, not the record"), since rank here is *Journal of Paleontology* house style, yet `taxa.yaml` records it as if it were a settled property of the name.

**A resolved nomen nudum, printed in synonymy form, entirely uncaptured (pp. 990–992).** "'Yakutidiscus maslennikovi' (Arendt, 1983) from the Permian Verkhoyansk Region was named in a short paper without diagnosis or illustration and is consequently a nomen nudum," restated in the Systematic Paleontology section as three printed lines ("'Yakutidiscus' Arendt, 1983, p. 136, nomen nudum," and two more), with the specimens tied directly to the new name ("The holotype of Neoisorophusella maslennikovi n. sp. is PIN 4010/1 = 'Yakutidiscus maslennikovi' of Arendt (1983)"). None of this — genus, two nominal species, or the specimen-identity link — is in the tree; it is exactly the shape B6's `act: [nomNudum]` is meant for.

Source record: title, journal, volume/number, pages, author and acceptance date all match with no discrepancy.

Data checks:

- `2009_sumrall.yaml`: the family node is keyed `agelacrinitidae`; the paper prints "Family Agelacrinidae Chapman, 1860" (p. 991, clean typeset text, not OCR), and `taxa.yaml` already carries a dedicated `agelacrinidae` `altSpellingOf` record used elsewhere in the corpus (`1900_bather`, `1935_bassler`).

## 2010_zhao.y.l_sumrall_parsley_peng.j — Kailidiscus chinensis (J. Paleontology 84)

Printed page = PDF index + 668 (pp. 668–680). The tree holds one taxonomy, no phylogeny. Coverage in one sentence: the classification skeleton, both new-taxon/type flags, and all sixteen material numbers are captured; occurrences, illustrations and diagnoses are not (G9).

**Two uncertain ranks printed as two separate lines, cleanly modelled (p. 674).** "Order uncertain" and "Family uncertain" appear as two distinct printed lines, removing the C5 ambiguity of a single combined English heading. The tree's two nested `openTaxon` placeholders map one per line, each correctly sourced and ranked in `taxa.yaml` — a clean confirmation of the C4 mechanism rather than a problem case.

**Type fixation stated as monotypy, with no field yet to hold it (p. 674).** "Diagnosis.—Same as for species by monotypy" is an explicit B14 "M" statement; the schema has no `typeFixation` field yet, so nothing is missing that should be present, but this is a ready-made example for when B14 is implemented.

Source record: title, journal, volume, pages, authors, acceptance date and DOI all match; `number: 5` in the record conflicts with the printed masthead and six separate running heads, all reading "84(4)."

Data checks:

- `2010_zhao.y.l_sumrall_parsley_peng.j.yaml`: the paratype list gives `GM 2013`; the Types paragraph and three figure captions (pp. 676, 679) all read "2103," unambiguously and repeatedly.
- `sources.yaml` `2010_zhao.y.l_sumrall_parsley_peng.j.number`: `5`; six printed running heads read "84(4)" — should be `4`.

## 2011_sumrall_zamora — Ordovician edrioasteroids from Morocco (J. Systematic Palaeontology 9)

Printed page = PDF index + 424 (pp. 425–454). The tree holds two taxonomies (Edrioasteroidea, Eocrinoidea) and one phylogeny (Fig. 6 cladogram, with `notes` on naming/rank discrepancies). Coverage in one sentence: the classification skeleton, all new-taxon/type flags and the cladogram's taxon sampling are captured; synonymy, material, occurrences, illustrations and diagnoses are not (G9).

**Classification and cladogram kept as two separate structures, correctly (pp. 432–434).** The paper runs a classification with unevenly printed rank words alongside a full cladistic analysis whose figure explicitly uses a different rank label ("Pyrgocystinae," a subfamily, for the clade the classification calls "Pyrgocystidae," a family). The tree's `taxonomies`/`phylogenies` split, with a `notes` on the cladogram's `pyrgocystinae` node recording the naming mismatch, is the right call rather than inventing a correspondence the source itself only states informally. A second cladogram `notes` inferring an unlabelled node's placement ("Presumably also Isorophina...") is the editor's own judgement riding on a plain `notes` field rather than the `editorial.inferred` block B20 defines.

**Two Hall dates for one genus, an independent A11 case (pp. 432, 435).** The Systematic section credits "Genus Streptaster Hall, 1872," matching this paper's own reference list, but a figure caption elsewhere cites the type species as "Streptaster vorticellatus Hall, 1866" — the same multi-printing pattern A11 already documents for Hall. Neither year is captured on the tree's `streptaster` node.

**An online-first date not captured, matching an existing schema slot.** The cover page states "Published online: 03 May 2011," distinct from "printed 15 September 2011," but `sources.yaml` records only `received`/`accepted`/`printed`, though `processDates.online` already exists in the schema for exactly this case.

Source record: title, journal, volume/issue, pages, authors, received/accepted/printed dates and DOI all match; no `online` date is recorded (see above).

Data checks:

- `2011_sumrall_zamora.yaml` and `taxa.yaml`: the species is keyed/spelled `epilezorum_sumrall_zamora_2011`; the paper prints "espilezorum" nine times with no variant spelling anywhere (abstract and eight further occurrences) — a corpus-wide transcription slip in both files.

## 2013_sumrall_heredia_rodríguez.c.m_mestre — Rhenopyrgids and Edrioasterida phylogeny (Acta Palaeontol. Polonica 58)

Printed page = PDF index + 763 (pp. 763–776). The tree holds one taxonomy and two phylogeny topologies (strict consensus; a constrained alternative). Coverage in one sentence: the classification skeleton, new-species and type flags, and both cladogram topologies with methodology are captured; material, occurrences, illustrations, most diagnoses and the character matrix/tree statistics are not (G9).

**A sibling family placed by the source, absent from the tree.** The paper's Systematic Paleontology explicitly nests Cyathocystidae Bather, 1899 as a coordinate family alongside Rhenopyrgidae within Edrioasterida (p. 773: "including Rhenopyrgidae Holloway and Jell, 1983 in Edrioasterida Bell, 1976 along with Cyathocystidae Bather, 1899 and Astrocystitidae Bassler, 1935"), but the tree only branches down the Rhenopyrgidae line. Per G9 this is scope, not error, but a reader of the tree alone would not see the paper's three-family placement.

**A hedged, unresolved candidate-membership list, correctly omitted (p. 773).** Seven species "that might belong to *Rhenopyrgus*, but incomplete preservation precludes generic assignment" are named in prose, not a formal synonymy, and none appears in the tree — correct, since the paper explicitly declines to place them, but the model has no field to represent "considered but not assigned" beyond the free-text discussion.

**A subgenus correctly modelled through the existing `parents` mechanism (p. 773).** "*Pyrgocystis (Rhenopyrgus) coronaeformis* Rievers, 1961" is captured as a `synonyms` entry with `parents: [rhenopyrgus-subgenus, pyrgocystis]` — a positive confirmation that B18's mechanism, worked out for suprageneric cases, also covers a parenthetical subgenus citation cleanly.

Source record: title, journal, volume/issue/pages, authors and all three process dates match with no discrepancy.

Data checks:

- `taxa.yaml`: the seventh author of *Rhenopyrgus flos* is keyed/spelled "DeBates" in `flos_klug_krüger_korn_rücklin_schemm-gregory_debates_mapes_2008`; both the species citation and the reference list in this paper spell it "DeBaets" (pp. 773–774).

## 2015_sprinkle_sumrall — New edrioasterine and astrocystitid edrioasteroids (J. Paleontology 89)

Printed page = PDF index + 346 (pp. 346–352); the source file is named for the acceptance date, and the publication year (2015, vol. 89 issue 2) is confirmed by the masthead and copyright line. The tree holds one taxonomy, no phylogeny — two new, monotypic genera. Coverage in one sentence: the classification skeleton and all four new/type flags are captured; material, occurrences, illustrations and diagnoses are not (G9).

**Two coordinate names from one Bather work, printed with two different years (p. 348).** Four lines apart: "Suborder Edrioasterina, Bather, 1898" and "Family Edrioasteridae Bather, 1899." Both trace to the same 1899 British Association report, itself "for 1898" — the classic proceedings dual-dating case (A7/A8). The paper is not internally consistent about which year it prints for which coordinate name, and neither tree node carries an explicit `year` to record the discrepancy.

**"Diagnosis.—Same as for species," printed twice for two monotypic genera (pp. 348, 351).** A specific, printed statement of diagnostic redundancy under monotypy, distinct from simply omitting a diagnosis; if diagnoses are captured for this source, the phrase is worth preserving verbatim rather than treating the genus as undiagnosed.

Source record: title, journal, volume/issue/pages, authors, acceptance date and DOI all match with no discrepancy; no received/online date is printed anywhere in the article.

Data checks:

- None confirmed as tree errors; the Edrioasterina/Edrioasteridae year split is an attribution conflict (see the closing list), reflecting the source's own inconsistency rather than a data-entry mistake.

## 2015_zamora_stromatocystites — The Cambrian edrioasteroid Stromatocystites (Geobios 48)

No source record or tree file exists for this paper. Printed page = PDF index + 416 (pp. 417–426); the extraction includes a ResearchGate cover sheet (index 0) that is not part of the article and should not feed a source record. The paper reviews all six proposed species of *Stromatocystites*, retaining three as valid (*pentangularis*, *walcotti*, *reduncus*), reaffirming Smith 1985's nomen dubium status for *balticus*, and synonymizing one (*S. flexibilis* Parsley and Prokop, 2004, into *S. pentangularis*) — its one new nomenclatural act. Three lots of new material are described in open nomenclature ("*Stromatocystites* cf. *pentangularis*," "*Stromatocystites* sp. A," "*Stromatocystites* sp.") with no new species named anywhere.

**A new synonymy, stated plainly (p. 418).** "This species is thus reinterpreted here as a junior synonym of *S. pentangularis*," for *S. flexibilis* — a clean synonymy act with no existing taxon record (`flexibilis_parsley_prokop_2004`) to attach it to.

**A name kept as a nomen dubium, with its lost material tentatively reassigned (p. 420).** "We agree with Smith (1985) that the original description from Jaekel (1899) is too vague... we tentatively suggest that these two specimens are probably similar to those described herein from Sweden, suggesting *S. balticus* should also be treated as *Stromatocystites* cf. *pentangularis*." The existing `balticus_jaekel_1899` record carries neither the nomen dubium status (dating to Smith 1985, reaffirmed here) nor this tentative material reassignment.

**A chimaera untangled across three papers, cited by the "vide" convention (p. 421).** Three Polish specimens, once figured as part of the ctenocystoid "*Jugoszovia archaeocyathoides*" (Dzik and Orłowski, 1995) and later "Stromatocystitidae indet." (Domínguez Alonso, 1999b), are here assigned to *Stromatocystites* but left as "*Stromatocystites* sp. A" in open nomenclature, with both prior citations printed in "v. [year]" synonymy form.

A source record for this paper would need: title, seven authors in printed order, Geobios vol. 48, pp. 417–426 (no issue number is printed anywhere), received/accepted/online dates (26 Nov 2014 / 19 Jul 2015 / 7 Aug 2015), DOI 10.1016/j.geobios.2015.07.004.

Data checks:

- None — no existing record to check against; see the closing list for the Stromatocystitidae 1935/1936 attribution conflict this paper surfaces.

## 2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman — An edrioasteroid from the Herefordshire Lagerstätte (Proc. R. Soc. B 284)

Printed page = PDF page-index + 1. The tree holds one taxonomy, no phylogeny — one new genus and species. Coverage in one sentence: the classification skeleton and both new/type flags are captured; material, occurrences, illustrations and the diagnosis are not (G9).

**A full systematic treatment in the main text of a Royal Society paper (p. 2).** Unlike journals that push taxonomy into supplementary material, this paper's entire "Systematic palaeontology" section — heading, etymology, diagnosis, material, locality, description — sits in the body text; nothing in this tree could have come from material outside what this file contains.

**Monotypy stated in a structured line the schema has no place for (p. 2).** "(b) Diagnosis of genus (monotypic) and species... Other species: None," printed directly under the type-species designation — a Treatise-style structured statement with no field beyond `notes`.

**Discussion-section classification history correctly excluded (pp. 4–5).** The Discussion narrates three earlier, different placements of *Rhenopyrgus* (Holloway & Jell 1983, "order uncertain"; Smith & Jell 1990; Guensburg & Sprinkle 1994) before stating the paper's own choice, "We assign *Heropyrgus* to the Rhenopyrgidae." The tree reflects only this final placement, correctly leaving the three superseded schemes to their own sources' trees (H table).

Source record: title, journal, volume and article number match; the issue number (1862) is not printed anywhere in the captured text and cannot be verified from this source alone.

Data checks:

- None confirmed; whether "Edrioblastoidina" is Fay's own 1962 coinage at suborder rank (his paper's own title names a class) cannot be verified without that source.

## 2020_ewin_martin.m_isotalo_zamora — New rhenopyrgid edrioasteroids (J. Paleontology 94)

Printed page = PDF page-index + 115 (pp. 115–130). The tree holds one taxonomy, no phylogeny. Coverage in one sentence: the classification skeleton, all material and (mostly) all synonymy and species-level occurrences are captured; family/genus-level range summaries and species-level diagnoses are staged as disabled blocks rather than live data (G9).

**Family Rhenopyrgidae emended and given a second genus (p. 118).** "Diagnosis (Emended).—Pyrgate edrioasteroids with relatively small oral surfaces..." broadens the family to admit floor plates "that may or may not be fused," following the paper's finding that some species fuse them and *R. grayae* does not; "Genera included.—*Rhenopyrgus* Dehm, 1961; *Heropyrgus* Briggs et al., 2017" is fully reflected in the tree.

**A family-rank name for the edrioblastoid group appearing once, off the systematic header (p. 128).** The Conclusions once use "the other stalked edrioasterid families Cyathocystidae and Edrioblastidae," a name printed nowhere else in the paper (elsewhere "edrioblastoids" or suborder "Edrioblastoidina" only) and absent from `taxa.yaml`. Whether this is a slip for Edrioblastoidina or a deliberate distinct name cannot be settled from this paper alone.

**A verified citation gap, handled by silent omission rather than a flag.** The `rhenopyrgus-sp-3` node's `notes` records that a 2013 citation "in synonym list with no explanation" does not actually cover this specimen at the cited page — an editor-verified discrepancy that is the *source's own* citation error, the "noted for later" case the roadmap's Ground Rules anticipate as a possible third `editorial` kind. It is handled today as an omission from the captured synonymy, not a flagged exclusion.

Source record: title, journal, volume/number/pages, authors, acceptance date and DOI all match with no discrepancy.

Data checks:

- `2020_ewin_martin.m_isotalo_zamora.yaml`: `rhenopyrgidae`/`rhenopyrgus` diagnosis fields carry dropped-ligature OCR text ("ve" for "five," "oor" for "floor," pp. 118, 120) copied verbatim instead of the plain printed words.
- `2020_ewin_martin.m_isotalo_zamora.yaml`: `grayae_bather_1915`'s synonym entry gives `pages: 48`; the paper prints "p. 58" (p. 122).
- `2020_ewin_martin.m_isotalo_zamora.yaml`: `grayae_bather_1915`'s occurrence location reads "Givran"; the paper prints "Girvan" (p. 122).
- `2020_ewin_martin.m_isotalo_zamora.yaml`: `rhenopyrgus-sp-2`'s occurrence stores `localStage: Girvan?` (a place name, not a stage) and omits "Scotland, UK," present on every other occurrence in the file (p. 123).

## 2021_jell_sprinkle — Revision of Whitehouse's eocrinoids Peridionites and Cymbionites (Alcheringa 45)

Printed page = PDF page-index (pp. 1–55); the tree is scoped to the paper's echinoderm content only, per its own `audit.notes` ("Non-echinoderm trees not captured"), leaving the paper's full trilobite/brachiopod/mollusc/hyolith/sponge treatment (pp. 37–55) out as documented scope (G9). The tree holds one taxonomy, no phylogeny, across two branches (Lichenoididae; Edrioblastoida). Coverage in one sentence: new taxa, type species and all material numbers are captured; synonymy citation detail, occurrences, illustrations and diagnoses are not (G9).

**Open-nomenclature species carrying `new: true`, per the dataset's own placeholder convention (p. 35–36).** "*Cambraster* sp." and "*Kailidiscus* sp." are plain indeterminate assignments to existing genera, correctly modelled as `openTaxon`; both also carry `new: true`, which is consistent with C4's rule that `new` on a placeholder marks the source that originates it, not a nomenclatural act.

**A chain of informal placements across three papers, resolved cleanly (pp. 26–27).** Smith et al.'s unnamed "Lichenoidid gen. et sp. nov." becomes Zamora et al.'s "*Lichenoides* sp.," and this paper tentatively allies both with Thorntonitidae without committing to genus. The tree represents this as two nested `openTaxon` records at the family level, with the later naming nested as a `synonyms` entry under the earlier placeholder — a clean example of the model handling a chain of other papers' open nomenclature.

**A genus attribution that reads as a match only because nothing marks the disagreement (p. 35).** "*Cambraster* Cabibel et al., 1958" is printed; `taxa.yaml`'s record carries `auth: [jaekel], year: 1923`, a different author and year. The tree node has no `auth`/`year` override or `notes`, so under A2's convention (bare node = agrees with the record) this silently reads as a match when the paper's own attribution disagrees.

Source record: title, journal, volume/number/pages, all four process dates, DOI and both authors match with no discrepancy.

Data checks:

- `taxa.yaml`: `stromatocystitida-incertae-sedis` carries `auth: [linnaeus], year: 1758`, unsupported by this paper (which prints "Family UNCERTAIN," p. 36, with no attribution) or by any other source — likely a leftover template value.
- `2021_jell_sprinkle.yaml`: the `echinodermata` node keys attribution to "brugière" (missing the "u" of Bruguière, unlike `1791_bruguière` used elsewhere in the corpus) and carries `auth`/`year` duplicating the taxon record, unlike every other backbone node in this same file (p. 6).

## Data corrections surfaced by this round

| file or key | correction | shown at |
|---|---|---|
| `1842_vanuxem.yaml` | `hamiltonensis_vanuxem_1842` occurrence `location` list merges "United States" and a stray "upper quarry" continuation into one item (six elements, not seven) | occurrence block, tree lines ~35–42 |
| `sources.yaml` `1848b_forbes` | `title` carries a trailing ".pdf" not part of the printed title | printed title, p. 483 |
| `1848b_forbes.yaml` | `echino-encrinus` node's `notes` reverses which section is "definitions" vs. "commentary" | pp. 504, 509 |
| `1852_hall.yaml` | `eucalyptocrinus` carries `new: true`, contradicted by the printed heading and by `taxa.yaml`'s own `altSpellingOf: eucalyptocrinites` | genus heading, pp. 207–211 area |
| `1852_hall.yaml` | `papulosus_hall_1852` notes reproduce OCR garble "Lucalyptocrinus" for Hall's own abbreviation "*E.*" | p. 211 |
| `1852_hall.yaml` | `decorus_phillips.j_1839` notes reproduce OCR garble "f7. celatus. Ip." for "*E.* cælatus. *Id.*" | p. 207 |
| `1854c_billings.yaml` | `punctuatus_billings_1854` illustrations list omits fig. 2, captioned on the same page | p. 270 |
| `1857_billings.yaml` | `stellata_billings_1857`, `rigidus_billings_1857`, `rugosus_billings_1857` keyed under `palæaster`; all three printed under *Palæasterina*, contradicting the `palæasterina` node's own note | pp. 290–291 |
| `taxa.yaml` | `palasterina` (used by `1858b_billings.yaml`) is an orphan record with no `altSpellingOf`, distinct from the linked `palaeasterina`/`palæasterina` pair `1857_billings.yaml` uses | — |
| `sources.yaml` `1915_bather` | title, Roman numeral, `pages` and `pubDate` all misidentify the printed item (Study VI, not IV; pp. 5–12 and 49–60, Jan./Feb. 1915, not `[49, 90]`/1915-12-06) | Study VI headings |
| `1935_bassler.yaml` | `agelacrinites` synonyms omit "Agelacrinus authors," the fourth of four printed synonyms | p. 7 |
| `1935_bassler.yaml` | `edrioaster` synonyms omit "Agelacrinites Forbes, 1848, not Vanuxem," the fifth of five printed synonyms | p. 9 |
| `1935_bassler.yaml` | `buchianus_forbes_1848` synonym entry's `parents: [agelacrinites]` points at the genus the printed line explicitly excludes ("not Vanuxem") | p. 9 |
| `1935_bassler.yaml` | `cincinnatidiscus`'s `pars: true` synonym entry's `taxon: hemicystites` points at the genus the printed phrase excludes ("Hemicystites of authors not Hall") | p. 3 |
| `1936_bassler.yaml` | `walcottidiscus-sp_bassler_1936` (openTaxon) double-counts *W. magister*, previewed in the same genus account, as a separate unnamed species | p. 2 |
| `1936_bassler.yaml` | `granulatus_hall_1871` synonym note asserts the print reads "(Hemicystite)"; both printed occurrences read "(Hemicystites)" | p. 4; plate 1, p. 25 |
| `1936_bassler.yaml` | `billingsi_chapman_1860` grouped under `agelacrinites-subgenus`; both printed occurrences read "(Agelacrinus) billingsi," not "(Agelacrinites)" | p. 12; plate 3, p. 26 |
| `1936_bassler.yaml` | `ulrichi_bassler_shideler_1936` carries no flags at all, despite being headed "n. sp." twice | p. 8; plate 6 |
| `1936_bassler.yaml` | no node exists for *Carneyella foerstei*, n. sp. (holotype USNM S-3965) | p. 8 |
| `1961_dehm.yaml` | subgenus node keyed `taxon: rhenopyrgus` with a `rank: subgenus` override, instead of the dedicated `rhenopyrgus-subgenus` record three later trees use | p. 16 |
| `sources.yaml` `1961_dehm` | `pages: [12, 17]`; the article begins at printed p. 13 | running heads, pp. 13–17 |
| `1961_rievers.yaml` | `coronaeformis_rievers_1961` diagnosis field stops after the first Diagnose sentence; the second (crown, five-triangle ambulacra) is omitted | pp. 10–11 |
| `sources.yaml` `1962_fay` | `identifiers.jstor: 13011100` has an extra digit | printed Stable URL, `.../1301100` |
| `2009_sumrall.yaml` | family node keyed `agelacrinitidae`; paper prints "Family Agelacrinidae Chapman, 1860" (no "-iti-"), and a dedicated `agelacrinidae` record already exists | p. 991 |
| `2010_zhao.y.l_sumrall_parsley_peng.j.yaml` | paratype list gives `GM 2013`; five printed occurrences read "2103" | pp. 676, 679 |
| `sources.yaml` `2010_zhao.y.l_sumrall_parsley_peng.j` | `number: 5`; six running heads read "84(4)" | pp. 670–680 |
| `2011_sumrall_zamora.yaml` and `taxa.yaml` | species keyed/spelled `epilezorum`; the paper prints "espilezorum" nine times with no variant | pp. 425–441 |
| `taxa.yaml` | `flos_klug_krüger_korn_rücklin_schemm-gregory_debates_mapes_2008` spells the seventh author "DeBates"; the citing paper and its own reference list spell it "DeBaets" | pp. 773–774 |
| `2020_ewin_martin.m_isotalo_zamora.yaml` | `rhenopyrgidae`/`rhenopyrgus` diagnosis fields carry dropped-ligature OCR text ("ve" for "five," "oor" for "floor") | pp. 118, 120 |
| `2020_ewin_martin.m_isotalo_zamora.yaml` | `grayae_bather_1915` synonym entry gives `pages: 48`; the paper prints "p. 58" | p. 122 |
| `2020_ewin_martin.m_isotalo_zamora.yaml` | `grayae_bather_1915` occurrence location reads "Givran"; the paper prints "Girvan" | p. 122 |
| `2020_ewin_martin.m_isotalo_zamora.yaml` | `rhenopyrgus-sp-2` occurrence stores `localStage: Girvan?` (a place name) and omits "Scotland, UK" | p. 123 |
| `taxa.yaml` | `stromatocystitida-incertae-sedis` carries `auth: [linnaeus], year: 1758`, unsupported by any source | p. 36 (2021_jell_sprinkle prints "Family UNCERTAIN," no attribution) |
| `2021_jell_sprinkle.yaml` | `echinodermata` node keys attribution to "brugière" (missing the "u") and carries `auth`/`year` duplicating the taxon record, unlike every other backbone node in the file | p. 6 |
| `2006_sumrall_brett_cornell.yaml` | top-level `notes` "No ranks are included" overstates the print — "Genus" is printed before the genus name | p. 190 |

Attribution conflicts to resolve:

- **Cambraster**: `taxa.yaml` credits Jaekel, 1923; printed "Cabibel, Termier & Termier, 1958" in `1985_jell_burrett_banks` (p. 185; Smith 1985's Table 3, p. 749), `1994_guensburg_sprinkle` (p. 42), and `2021_jell_sprinkle` (p. 35).
- **Foerste 1916/1917**: `taxa.yaml`'s `isorophus` gives 1916; printed "Foerste, 1917" in `1978_bell.b.m_sprinkle`, `1994_guensburg_sprinkle` (p. 42), and `2011_sumrall_zamora` (p. 435).
- **Edrioasteridae 1898/1899 and Bather/Bell 1976**: `taxa.yaml` gives Bather, 1898; `2015_sprinkle_sumrall` prints "Bather, 1899" for the family four lines below "Bather, 1898" for the coordinate suborder (p. 348, the paper's own inconsistency); `1978_bell.b.m_sprinkle` credits the family to "Bell, 1976" throughout (pp. 245–246).
- **Camptostromatidae 1967/1968**: `taxa.yaml` gives 1967 (per `1994_guensburg_sprinkle`, already documented in `source-observations.md`); that paper prints "Durham, 1968" (pp. 12, 42).
- **Stromatocystitidae 1935/1936**: `taxa.yaml` gives Bassler, 1936; `2015_zamora_stromatocystites` prints "Family STROMATOCYSTITIDAE Bassler, 1935" (p. 418).
- **Echino-encrinites Von Meyer/Volborth**: `taxa.yaml` credits Volborth, 1842; `1848b_forbes` credits "Von Meyer" for the genus throughout (p. 504).
- **Agelacrinitidae Chapman 1860 vs Jaekel 1899**: `taxa.yaml` gives Chapman, 1860; `1935_bassler`'s own paper credits the superseded family form to "Agelacrinidae Jaekel, 1899" (p. 2), and its adjacent Class-level synonym on the same page independently reads "Thyroidea Chapman, 1860," suggesting a possible copy error.
- **stellatus 1856/1866**: the `hemicystites-subgenus > stellatus_hall_1866` key gives 1866; `1936_bassler` prints "(Hall), 1856" (p. 5).


# Reading round of 2026-09-10: six papers

Bell 1891, Haeckel 1896, Pompeckj 1896, Bather 1899 and 1900, Jaekel 1899;
PDFs in `example-publications/09-10`. Four have no tree; Bell 1891 has a
draft tree in `drafts/` for audit. Coverage is stated per kind only (G9).

## 1891_bell.f.j — "On the Arrangement and Inter-relations of the Classes of the Echinodermata" (Ann. & Mag. Nat. Hist., Ser. 6, Vol. 8)

Read from the OCR text, printed pp. 206–215, with the p. 211 diagram read
separately from the page image (the text layer renders it as garbage). No
source record, no tree and no author record exist for this paper — the
expected author key `bell.f.j` is absent from `data/authors.yaml`, which
holds only `bell.b.m`, a different, later author. A draft tree
(`drafts/1891_bell.f.j.yaml`) has been prepared for the owner to audit before
entry. Coverage in one sentence: the paper prints one linear classification
with formal diagnoses for nearly every name and a phylogenetic diagram, and
proposes several new names at several ranks (G9).

**The linear arrangement (pp. 211–212).** "Put in the ordinary linear way
the proposed arrangement will read thus:—" introduces two Branches
(Incaliculata, Caliculata), each split into Stages, Sub-branches and
Sub-stages down to Class. Diagnoses follow for nearly every name (pp.
213–215); Bell declines two: "It is not necessary for the purpose I have in
view to offer definitions of the Cystidea or Blastoidea; perhaps a
palaeontologist will oblige" (p. 215).

**Eleutherozoa and Statozoa, named in one sentence (p. 210).** "…the other
leads to the Echinoidea, Asteroidea, and Ophiuroidea; the former may be
called the Statozoa, the latter the Eleutherozoa." Both get formal
diagnoses at p. 214. `eleutherozoa` already exists in `data/taxa.yaml`
(`auth: [Bell]`, `year: 1891`, `rank: Subphylum`) — this paper is that
record's source — but the paper's own table places it as "2nd Sub-branch"
(p. 213), not a Subphylum. The rank word the record carries and the rank
word the source prints are two different things, exactly the shape G8
describes.

**Four more coined names, no diagnosis before the table (pp. 211–213).**
Incaliculata/Caliculata are introduced only as the table's Branch headings
(no separate proposing sentence); Anactinogonidiata/Actinogonidiata as
Stage headings; Zygopoda/Azygopoda are proposed as adjectives first ("I
propose, provisionally at any rate, to speak of it as zygopodous in the
Urchin and azygopodous in the Starfish," p. 211) and only later become
Division-rank substantives (p. 213). None of the six has a taxon record.

**Three rank words absent from the enum (pp. 212–213).** Bell's table uses
six rank-like words — Branch, Stage, Sub-branch, Sub-stage, Division, Class
— against `$defs/rank` in `schemas/phylogeny.yaml`; Branch, Division and
Class are in the enum, Stage, Sub-branch and Sub-stage are not. The words
are not even used consistently within Bell's own tree: the same depth is
"Sub-stage" on the Statozoa side of the split and "Division" on the
Eleutherozoa side.

**Two unnamed placeholders (p. 213).** "Sub-stage i. Apelmatozoic." and
"Sub-stage ii. Pelmatozoic." each carry a member list but no substantive
name, only an adjective already used elsewhere in the paper ("there were
apelmatozoic and pelmatozoic Cystids," p. 210) — the C4 "unnamed" shape, not
the "uncertain" one, since Bell believes each grouping is real.

**The p. 211 diagram, read from the page image.** Captioned "Phylogeny of
the Echinodermata," rooted on "Primitive Echinoderm" (not itself a taxon).
Three main branches, with small side labels "Pedata" and "Apoda" on the
Holothurioidea branch; Cystidea appears twice, once labelled "(pelmatozoic)"
and once "Apelmatozoic Anactinogonidial Cystidea," matching the two Cystidea
placements in the linear arrangement. Branch lengths and the order of
branching along the Statozoa stem still need checking against the image by
the auditor.

Source record: none exists yet. A record needs the author key `bell.f.j`
added to `data/authors.yaml` first (only `bell.b.m` is present); pages
206–215; journal Ann. & Mag. Nat. Hist., Ser. 6, Vol. 8, 1891; no
read/received date is printed anywhere in the supplied pages.

Data checks:

- `draft_1891_bell.f.j.yaml`: three printed rank words (Stage, Sub-branch,
  Sub-stage, pp. 212–213) have no value in the rank enum and are currently
  parked in each node's `notes`.
- `draft_1891_bell.f.j.yaml`: two unnamed sub-stage placeholders
  (`statozoa-unnamed-substage-1_bell.f.j_1891`,
  `statozoa-unnamed-substage-2_bell.f.j_1891`, p. 213) need the C4 "unnamed"
  marker once that field exists.
- `draft_1891_bell.f.j.yaml` phylogeny: the p. 211 diagram was read from the
  page image, not the OCR text; branch order and lengths along the Statozoa
  stem are unverified.
- `eleutherozoa`: the existing record's `rank: Subphylum` disagrees with
  this paper's own printed rank for the same node, "2nd Sub-branch" (p.
  213).

## 1896_haeckel — "Die Amphorideen und Cystoideen" (Festschrift für Carl Gegenbaur)

Read from the OCR text, printed pp. [1]–179 (own separate pagination, offset
confirmed against running heads at eight points). No tree exists; a source
record exists with several gaps. Coverage in one sentence: the paper prints
a whole-phylum system plus two fully worked class-level systems (Amphoridea,
Cystoidea) with full family synonymies, roughly twenty new genera and six
new family/subfamily names, and no new species at all (G9).

**No species proposed, by the author's own statement (p. 6).** "Weiter als
bis zu den Gattungen hinabzugehen, schien mir nicht rathsam" ("I did not
think it advisable to go further down than to the genera"), confirmed by a
full-text search: no "n. sp."/"nov. sp." anywhere. Everything marked new in
this paper is genus rank or above.

**Edrioasteroid-relevant genera stay inside Cystoidea, and a rival class
proposal is named and rejected (p. 108).** All of Agelacrinidae's relatives
sit as one family (Agelacystida) with two subfamilies inside Class
Cystoidea. Haeckel names and disagrees with Jaekel's competing proposal:
"Otto Jaekel (49, pag. 110) hält die Hemicystiden … für 'die primitivsten
Formen der Pelmatozoen' … er bildet aus ihnen die besondere Klasse der
Thecoidea. Nach meiner Auffassung dagegen gehören dieselben zu den höchst
entwickelten Formen der Cystoideen." No edrioasteroid-shaped taxon of any
rank exists in this paper.

**Edriocystis as a replacement name, same type species (p. 117–118).** New
genus Edriocystis replaces Edrioaster Billings, 1858 (itself replacing
Billings's own Cyclaster, 1856) without changing the type species:
"Species typica: Edriocystis Bigsbyi, E. Haeckel. — Edrioaster Bigsbyi,
BILLINGS, 15, pag. 82." The same genus complex is also split across two
same-author decisions on facing pages: Barrande's Bohemian *Agelacrinites*
is synonymized under genus Hemicystis (p. 111), while Vanuxem's own
*Agelacrinites* stays under genus Agelacrinus (p. 112) — two same-named
usages, resolved two different ways by the same reviewer.

**Three `taxa.yaml` records that disagree with the print.** `amphorida`
(Order, Haeckel 1896) is printed here as Klasse "Amphoridea," and Haeckel's
own text credits the name to his 1895 paper, not 1896 (p. 8–9); `hemicystis`
(credited to Haeckel, 1896) is printed as a genus of Hall, 1852 (p. 111),
with no Haeckel authorship attached anywhere; `placocystida` (recorded rank
Suborder) is printed as a Subfamilia (p. 37, table heading "I. Subfamilia:
Placoecystida, Hkl.").

**Mixed novelty-marking, one work, three conventions.** An explicit "(nov.
gen.)" tag covers most new genera; a bare author abbreviation with no year
covers the three new Anomocystida subfamilies ("Hkl.," p. 37); a first-person
proposing verb with no tag covers two Cystoidea subfamilies ("unterscheide
ich," p. 107) and genus Staurocystis ("gründe ich," p. 134).

Source record: title, year and author match; series (Festschrift für Carl
Gegenbaur), publisher (Wilhelm Engelmann, Leipzig), the work's own pagination
(pp. [1]–179), and its status as a separately-paginated chapter in a
multi-author dedicatory volume are all unrecorded — no Festschrift-shaped
record exists anywhere in the corpus yet (`grep -rin festschrift` over
`data/` and `docs/` returns nothing); the closest existing shape is
`1857_billings`'s `book:`+`chapter:`+`pages:` pattern.

Data checks:

- `amphorida`: printed as Klasse "Amphoridea" (p. 8–9, 164), Haeckel's own
  1895 self-citation, not 1896 — name, rank and year all differ from the
  record.
- `hemicystis`: printed as a genus of Hall, 1852 (p. 111), not of Haeckel —
  the record's authorship is wrong for this citation.
- `placocystida`: printed rank is Subfamilia (p. 37), not Suborder.

## 1896_pompeckj — "Die Fauna des Cambrium von Tejřovic und Skrej in Böhmen" (Jahrbuch d. k. k. geol. Reichsanstalt 45)

Read from the OCR text, printed pages confirmed against running heads at
four points. Tree: one taxonomy, no phylogeny, matching the paper's own
count of "4 Cystoideen" (p. 564). Coverage in one sentence: the
classification skeleton, both new taxa and their illustrations are captured;
type fixation, material, occurrences and diagnoses are not, and two
open-nomenclature entities the paper itself prints have no node at all (G9).

**Stromatocystites, erected without a stated type (p. 505–506).**
"Stromatocystites nov. gen.," diagnosed "Kelch ungestielt, vieltäfelig,
niedrig, von ungefähr fünfseitigem Umriss" and continuing for four more
sentences, none of it captured in `diagnosis`. The genus is monotypic here
(only *S. pentangularis* is assigned to it), so the type is fixed only by
subsequent monotypy — Pompeckj never writes "Typus" or "Genotypus."

**A genus-level "(?)" that hedges placement, not the species (p. 504).**
"Mitrocystites (?) nov. spec." — the question mark sits after the genus
name, and Pompeckj states exactly what it hedges: "Das Vorkommen einer
solchen seitlichen Oeffnung kann die Zuzählung der vorliegenden Form zu
Mitrocystites Barr. als bedingt richtig erscheinen lassen" ("…can make the
assignment to *Mitrocystites* Barr. appear only conditionally correct").
The tree's `provisional: true` on `mitrocystites-sp_pompeckj_1896` is the
right mapping (B16); the bracketed-after-the-genus form of the hedge is
worth naming separately so it is not misread as doubt on the species.

**A hedged synonymy, restated three times, captured nowhere.** Pompeckj
proposes that Barrande's *Cystidea concomitans* is the same species as his
new *pentangularis*: "scheint auf schlecht erhaltene Reste der eben
beschriebenen Form begründet zu sein" (p. 507, "seems to be based on poorly
preserved remains of the form just described"), repeated at p. 585
("wahrscheinlich … auch bei Skrej … vertreten") and p. 590. None of the
three statements is in the tree.

**A fourth taxon-like entity that never gets a node.** Under *Trochocystites
bohemicus* (p. 503), isolated thick plates from three localities are
described as "Sehr wahrscheinlich … einer Cystoideenform … möglicherweise …
von einer Trochocystiten-Art," and the plate caption gives them their own
line, locality and figures, distinct from *T. bohemicus*'s own: "Trochoeystites?
sp. pag. 503 [9]" (Taf. XIII, Fig. 9–11). Pompeckj's own genus count treats
this as material under *Trochocystites*, not a fifth species, but it is a
distinct, figured, open-nomenclature unit — exactly the disarticulated-plate
scope G9 flags as belonging in this project.

**A bare, rank-less heading for the whole class (p. 502).** "Cystoidea."
carries no rank word in the original — the Class rank the tree assigns comes
entirely from the `cystidea` taxon record (`cystoidea` is `altSpellingOf:
cystidea`), not from anything Pompeckj printed. Every higher-taxon heading in
the paper follows the same bare-noun convention (G8).

Source record: title, journal, volume 45, `notes` on the 1895-annual/1896-
publication gap, `pubDate.year: 1896` and author all match the printed
running head and table of contents; no discrepancy found.

Data checks:

- Add an `openTaxon` child of `trochocystites` for "Trochocystites? sp."
  (p. 503, Taf. XIII fig. 9–11), currently uncaptured.
- Add a hedged `synonyms` entry for *Cystidea concomitans* Barr. under
  `pentangularis_pompeckj_1896` (pp. 507, 585, 590).

## 1899_bather — "A Phylogenetic Classification of the Pelmatozoa" (Rep. Brit. Assoc. Adv. Sci. for 1898, pp. 916–923)

Read from the OCR text of the Report volume; offset confirmed at both ends
of the paper. No tree exists. Coverage in one sentence: the paper prints one
full linear classification, Sub-Phylum to family, ending mid-family where
the section's business closed, with no explicit "new" marker anywhere in it
(G9).

**The classification (pp. 919–923).** Sub-Phylum Pelmatozoa contains Class I
Cystidea (4 orders, 17 families), Class II Blastoidea (two Grades, an
intermediate "Series" rank between Grade and family), Class III Crinoidea,
and Class IV Edrioasteroidea, printed as three families with no orders
("Not divided into Orders" is the 1900 book's sentence, not this paper's).
The paper is cut off mid-family by the next item on the sitting's agenda.

**No name in the paper carries a "new" marker.** "n. fam.," "n. gen.," "gen.
nov.," "established," "proposed" and "erect(ed)" occur nowhere in the text.
Every name is presented as "an epitome of that adopted in a forthcoming
text-book of zoology edited by Professor Ray Lankester" (p. 916) — i.e.
`1900_bather`. Novelty has to be inferred from the absence of a prior
author, not read off the page.

**The year problem: Bather's own later self-citations disagree.** The
printed 1899 paper carries no year on any of its own names. In `1900_bather`
Bather cites this paper's grade Protoblastoidea as "Bather (1899)" (p. 79)
and its genus Dinocystis as "Bather (1898)" (p. 209) — within pages of each
other, in the same book. `taxa.yaml` follows both conventions inconsistently
across different names from the same 1899 paper; nothing printed in the 1899
paper itself supports one year over the other for any specific name.

**Haplocystis, likely a wrong genus authority.** `taxa.yaml` credits the
genus to Bather, 1899, but this paper only lists "Haplocystis" among
Agelacrinidae's genera with no attribution and no "new" marker, while
`1900_bather` explicitly credits it to "C. F. Roemer (1855)" (p. 208) — an
error discoverable only by holding both papers together.

**Tiaracrinidae, apparently pre-dated.** `taxa.yaml` credits the family to
`1900_bather`, but "Tiaracrinide" is already printed here in 1899 (p. 921),
with the same lack of attribution as every other family in the paper.
Crediting it to 1900 looks wrong unless some still-earlier, unexamined
source used the name first.

**Steganoblastus, provisionally placed.** Appears here only as a genus,
bracketed "[?]" inside family Asteroblastidae under Grade Protoblastoidea
(p. 921) — a placement `1900_bather` overturns a year later by giving it its
own family, Steganoblastidae, under Edrioasteroidea, while explicitly
citing this very paper for the placement it is now rejecting ("Bather,
1899," p. 209).

Source record: title, journal reference, pages [916, 923] and sole
authorship all match, confirmed independently by Bather's own bibliography
entry in `1900_bather` (item 12, p. 216). `processDates.conferenceStart` and
`conferenceEnd` are both `1898-09-07`, but the paper was read specifically
in the Tuesday, 13 September 1898 sitting of a Section that ran business
across at least six days (8–14 September) — one identical date captures
neither the meeting's span nor this paper's own reading date.

Data checks:

- `haplocystis`: credited to Bather, 1899; `1900_bather` p. 208 explicitly
  credits "C. F. Roemer (1855)" instead.
- `tiaracrinidae`: credited to `1900_bather`; the family is already printed,
  unattributed, in `1899_bather` p. 921.
- `1899_bather` (once entered): `processDates.conferenceStart`/`conferenceEnd`
  both read `1898-09-07`; the paper's own reading date was 13 September 1898.
- `glyptocystinae`: credited to "Calvin, 1899," already flagged unverified by
  the editor; `1899_bather` p. 920 is a plausible actual source (appears in
  Bather's own sentence beside the confirmed Callocystinae/Echinoencrininae)
  but this is not confirmed — cannot verify without checking Calvin directly.

## 1899_jaekel — *Stammesgeschichte der Pelmatozoen*, Erster Band: Thecoidea und Cystoidea (Berlin: Julius Springer)

Read from the OCR text; offset confirmed at eight anchors across the whole
main text. No tree exists; a source record exists. Coverage in one sentence:
the volume prints two full class-level systems (Thecoidea, Cystoidea) with
family/genus synonymies, several new genera and species, and one
family-rank name Jaekel explicitly claims as his own (G9).

**Two classes, one volume, no single Pelmatozoa table.** Thecoidea (pp.
6–51) and Cystoidea (pp. 53–436) are simply the two halves of this Band;
Pelmatozoa itself is never subdivided in one printed table anywhere in the
book.

**Billings's name for the group is quoted and declined (p. 9).** Jaekel
cites Billings 1858 proposing "Edrioasteridae" for this group and explains
why he does not adopt it: "die genannte Wortbildung nach den heutigen Regeln
der Nomenklatur nur zur Bezeichnung einer Familie, nicht aber einer Klasse
verwendet werden darf" ("that word-formation may, by today's rules of
nomenclature, be used only to denote a family, not a class"). He also
rejects Miller's 1889 "Agelacrinoidea" as a replacement.

**Dinocystis, erected in Jaekel's own name with no citation to Bather
anywhere (pp. 10, 46–47).** "Dinocystis n. g.," diagnosed and given a type
species, *D. Barroisi* n. sp. ("Ich nenne die Art zu Ehren des Herrn CHARLES
BARROIS"). `taxa.yaml`'s `dinocystis` record reads `auth: [bather], year:
1898`; nothing in this book supports that — Jaekel lists "Dinocystis, n. g."
in his own name at p. 10 and erects it formally at p. 46, with no Bather
citation anywhere the name occurs in the volume.

**Agelacrinidae claimed as Jaekel's own, apparently in ignorance of Chapman
(p. 47, 49).** "II. Fam. Agelacrinidae m." — "m." (*mihi*, "of me"). The only
place Chapman's name touches this material at all is a species citation, "H.
Billingsi CHAPMAN 1860" (p. 49); Chapman is never connected to the family
name itself. `taxa.yaml`'s `agelacrinidae` record correctly keeps Chapman
1860 as authority, so no change is indicated there, but the printed "m." is
worth a note if this source is entered.

**Three spelling/identity mismatches against `taxa.yaml`.** `apiocystitinae`
is printed throughout as "Apiocystinae" (p. 277), never with the "-tit-";
`cheirocrinidae` is printed consistently as "Chirocrinidae" (p. 212, and the
genus is always "Chirocrinus," never "Cheirocrinus"); `scoliocystinae` does
not occur anywhere in the book at all — only family Scoliocystidae exists,
with no subfamily subdivision in either the table of contents or the text.

**Eocrinoidea confirmed absent (p. 174, 210).** "Eocrinoidea"/"Eocrinida" do
not occur anywhere, checked for every occurrence; the only related word is
the informal collective "Eocriniten," used descriptively, never as a formal
Klasse/Ordnung with a Latin diagnosis. This corroborates Regnéll 1945 (p.
14) and matches `taxa.yaml`'s own correct dating of `eocrinoidea` to Jaekel
1918, not 1899.

Source record: author, title stem (`book: stamm`) and year all match. The
volume-specific subtitle, "Erster Band: Thecoidea und Cystoidea," is not
carried in any field — the project uses a `title:` field for exactly this
purpose elsewhere on a multi-part work (`1900_bather`: `title: Part III —
The Echinoderma`) — worth adding if Jaekel's later Bände are ever entered.

Data checks:

- `dinocystis`: credited to Bather, 1898; Jaekel erects "Dinocystis n. g."
  in his own name (pp. 10, 46), with no Bather citation anywhere in the
  volume.
- `apiocystitinae`: spelling; printed throughout as "Apiocystinae" (p. 277).
- `cheirocrinidae`: spelling; printed consistently as "Chirocrinidae" (p.
  212).
- `scoliocystinae`: not found anywhere in the book — cannot confirm this
  subfamily exists as printed; only family Scoliocystidae is present.

## 1900_bather — "The Echinoderma," Part III of Lankester's *A Treatise on Zoology*

Read from the OCR text; offset confirmed at four anchors across the
examined chapters. Tree: `data/trees/1900_bather.yaml`, one taxonomy, no
phylogeny. Coverage in one sentence: the classification skeleton from
Kingdom to Sub-family is captured cleanly for every chapter read; type
species, material, occurrences, illustrations and phylogeny are not, and
most attribution on the covered nodes is missing even where the book prints
it (G9).

**35 of 39 nodes match the print cleanly** on identity, rank, placement and
(where present) notes, including a word-for-word quote check on the
`blastoidea` node spanning a page break (pp. 78–79).

**A compound, multi-author attribution the schema cannot yet hold (p.
205).** "CLASS IV. EDRIOASTEROIDEA, E. Billings (1854,-58; Huxley, 1877; and
Bather, 1899) (=Thyroida, Chapman, 1860; Agelacrinoidea, S. A. Miller,
1877-83; Worthen, 1883; Cystasteroidea, Steinmann, 1888; F. Bernard, 1893;
Thecoidea, Jaekel, 1895)." The class name is credited to three independent
author-years at once, and two of the four listed synonyms are each credited
to two authors. `taxa.yaml`'s `edrioasteroidea` record picks one authority
(`1858b_billings`); the tree node carries none of this — no `auth`, `year`
or `citedAs` on the class or on any of its four synonym entries.

**Two spelling and one omitted attribution, all against the paper's own
sibling nodes.** The `amphorida` node's `notes` spell the printed authority
"Haekel (1896, pars)" (p. 43) for what the book actually prints as
"Haeckel"; the same misspelling recurs on `eocystidae`'s notes ("Haekel's
Eocystida" for "Haeckel's Eocystida"). `rhombifera-order` carries no `notes`
at all, though its sibling orders `aporita` and `diploporita-order` both
carry the book's identical attribution pattern ("Zittel (1879, restr.)" /
"Zittel (1879, emend.)"), and Rhombifera is credited the same way at p. 52.

**Tiaracrinidae's `new: true` is very likely wrong.** "Famity 4.
TIARACRINIDAE" (p. 57) carries no attribution or "new" language here, and
the family is already in print, equally unattributed, in `1899_bather` a
year earlier — flagging it new to this 1900 source looks wrong unless a
still-earlier use is ruled out.

**Rank drift for Pelmatozoa, within one work and between two.** The formal
heading reads "GRADE A. PELMATOZOA" (p. 1), which the tree follows
(`pelmatozoa-grade`); the book's own prose, 33 pages later, gives a
different reason and a different rank: "their genetic connection is so
evident that it should be recognised by the establishment of a Sub-phylum,
to which we shall continue to apply the name Pelmatozoa" (p. 33) — almost
verbatim `1899_bather`'s own prose and formal heading, both of which use
Sub-Phylum. The same name is a Sub-Phylum in 1899 (formal heading and
prose) and a Grade in 1900's formal heading, while 1900's own prose still
calls it a Sub-phylum.

**An internal `taxa.yaml` inconsistency, visible only because two linked
records disagree.** `anomalocystidae` (`altSpellingOf: anomalocystitidae`)
carries `auth: [Hall], year: 1859`, but `anomalocystitidae` itself carries
`auth: [bassler], year: 1938`; neither 1899 nor 1900 prints any attribution
for this family, so this review cannot settle which is right, only that the
two linked records disagree. The same split exists for `dendrocystidae`
(Barrande 1887) vs. `dendrocystitidae` (Bassler 1938); here the 1900 book at
least credits the *genus* Dendrocystis to Barrande, 1887 (p. 47), matching
the alt-spelling record, not the primary one.

Source record: title page, `book: treatise-zoo`, `pubDate.year: 1900` and
`authors: [bather]` all match exactly; the title page's "assisted by" credit
(J. W. Gregory, E. S. Goodrich) has no field to land in, which is not an
error — `authors` correctly reflects the "BY" line — but is worth a `notes`
line if the record is touched again.

Data checks:

- `amphorida` / `eocystidae`: `notes` spell "Haekel" where the book prints
  "Haeckel" (p. 43).
- `rhombifera-order`: missing the `notes` attribution ("Zittel (1879,
  emend.)," p. 52) that its sibling orders both carry.
- `edrioasteroidea`: node carries no `auth`/`year`/`citedAs` for the
  compound three-author printed attribution (p. 205); its four `synonyms`
  entries (`thyroida`, `agelacrinoidea`, `cystasteroidea`, `thecoidea`)
  likewise carry none of their printed attributions.
- `tiaracrinidae`: `new: true` is very likely wrong — the family is already
  printed, unattributed, in `1899_bather` p. 921.
- `anomalocystidae`/`anomalocystitidae`: the linked records disagree on
  authority (Hall, 1859 vs. Bassler, 1938); neither source read in this
  round prints an attribution for the family.

## Data corrections surfaced by the 09-10 round

| file or key | correction | shown at |
|---|---|---|
| `amphorida` (taxa.yaml) | printed as Klasse "Amphoridea," self-cited by Haeckel to 1895, not 1896 | 1896_haeckel p. 8–9, 164 |
| `hemicystis` (taxa.yaml) | printed as a genus of Hall, 1852, not of Haeckel | 1896_haeckel p. 111 |
| `placocystida` (taxa.yaml) | printed rank is Subfamilia, not Suborder | 1896_haeckel p. 37 |
| `dinocystis` (taxa.yaml) | Jaekel erects it in his own name; no Bather citation anywhere in the volume | 1899_jaekel pp. 10, 46 |
| `apiocystitinae` (taxa.yaml) | spelling; printed "Apiocystinae" | 1899_jaekel p. 277 |
| `cheirocrinidae` (taxa.yaml) | spelling; printed consistently "Chirocrinidae" | 1899_jaekel p. 212 |
| `haplocystis` (taxa.yaml) | credited to Bather, 1899; Bather's own later book credits Roemer, 1855 | 1900_bather p. 208, re: 1899_bather |
| `tiaracrinidae` (taxa.yaml) | credited to `1900_bather`; already printed, unattributed, a year earlier | 1899_bather p. 921 |
| `1899_bather` `processDates` (sources.yaml, once entered) | `conferenceStart`/`conferenceEnd` both `1898-09-07`; the paper's own reading date was 13 September 1898 | 1899_bather p. 916 |
| `amphorida` / `eocystidae` `notes` (1900_bather tree) | "Haekel" for printed "Haeckel" | 1900_bather p. 43 |
| `rhombifera-order` (1900_bather tree) | missing the attribution its sibling orders both carry | 1900_bather p. 52 |
| `edrioasteroidea` and its four `synonyms` (1900_bather tree) | no `auth`/`year`/`citedAs` captured for any of the printed attributions | 1900_bather p. 205 |
| `tiaracrinidae` `new: true` (1900_bather tree) | very likely wrong; family already printed unattributed a year earlier | 1900_bather p. 57, re: 1899_bather p. 921 |
| `anomalocystidae`/`anomalocystitidae` (taxa.yaml) | linked records disagree on authority (Hall, 1859 vs. Bassler, 1938) | — |
| `eleutherozoa` `rank: Subphylum` (taxa.yaml) | this paper's own table prints "2nd Sub-branch" for the same node | 1891_bell.f.j p. 213 |

Attribution conflicts to resolve

- **Bather 1898 vs. 1899, for names from the same paper.** The printed
  1899 paper (`1899_bather`) carries no year on any of its own names.
  Bather's own later book (`1900_bather`) cites the grade Protoblastoidea
  as "Bather (1899)" (p. 79) and the genus Dinocystis from the same paper
  as "Bather (1898)" (p. 209) — within pages of each other. `taxa.yaml`
  follows both conventions inconsistently; nothing in the 1899 paper itself
  favors either year for any specific name.
- **haplocystis: Roemer, 1855 vs. Bather, 1899.** `taxa.yaml` credits the
  genus to Bather, 1899; `1899_bather` merely lists the name unattributed;
  `1900_bather` p. 208 explicitly credits "C. F. Roemer (1855)."
- **tiaracrinidae: 1899 vs. 1900.** `taxa.yaml` credits `1900_bather`; the
  family is already printed, equally unattributed, in `1899_bather` p. 921,
  a year earlier.
- **dinocystis: Bather, 1898 vs. Jaekel, 1899 "n. g."** `taxa.yaml` credits
  Bather, 1898; Jaekel erects "Dinocystis n. g." in his own name (pp. 10,
  46), with no Bather citation anywhere in the book.
- **Agelacrinidae: Jaekel, 1899 "m." vs. Chapman, 1860.** Jaekel prints "II.
  Fam. Agelacrinidae m." (mihi, p. 47), apparently unaware of Chapman's
  prior use — Chapman is cited in the volume only for a species, never
  connected to the family name. `taxa.yaml` correctly keeps Chapman, 1860.
- **amphorida, hemicystis, placocystida vs. Haeckel's own print.** Three of
  eight Haeckel-1896-attributed `taxa.yaml` records disagree with what
  `1896_haeckel` actually prints: name/rank/year for `amphorida`,
  authorship entirely for `hemicystis`, rank for `placocystida`.
- **The Haeckel 1895 paper as the true source of several family names.**
  Most of `1896_haeckel`'s family-rank names (Eocystida's components,
  Palaeocystida, Pomocystida, Fungocystida, Agelacystida, Ascocystida,
  Glyptocystida) are explicitly self-cited by Haeckel to his 1895 paper
  ("Die cambrische Stammgruppe der Echinodermen"), not proposed new in 1896;
  no `1895_haeckel` source record exists yet to resolve these citations
  against.
- **Jaekel spellings Apiocystinae/Chirocrinidae, and the missing
  scoliocystinae.** `taxa.yaml`'s `apiocystitinae` and `cheirocrinidae` both
  carry spellings the book never uses (printed "Apiocystinae" p. 277,
  "Chirocrinidae" p. 212 throughout); `scoliocystinae` does not occur
  anywhere in the volume at all — only family Scoliocystidae, unsplit,
  exists.
- **Eocrinoidea absent from Jaekel 1899.** Checked for every occurrence:
  "Eocrinoidea"/"Eocrinida" do not appear anywhere in the book, only the
  informal "Eocriniten." This corroborates Regnéll 1945 (p. 14) and matches
  `taxa.yaml`'s own correct dating of `eocrinoidea` to Jaekel, 1918.

## 1895_haeckel — "Die cambrische Stammgruppe der Echinodermen" (Jenaische Zeitschr. Naturwiss. 30)

Read from an offprint with a clean text layer (Antiqua, unlike the 1896
Festschrift), own pagination pp. 1–12; no source record, no tree. This is the
paper Haeckel 1896 self-cites for Amphoridea and most of its family names,
and all nine of those citations resolve to it with matching page and
spelling. It prints Class Amphoridea with four families, Class Cystoidea
with six, and a closing diagram (p. 12) that groups the eight echinoderm
classes into Monorchonia and Pentorchonia.

**Two dates for one paper (pp. 1, 11).** The text is "Vorgetragen in der
Sitzung der Medicinisch-Naturwissenschaftlichen Gesellschaft zu Jena am 13.
December 1895" and signed "Jena, am 15. December 1895."; the offprint
wrapper and the catalogue give 1896. The key-year rule takes the printing,
which needs the Heft's issue date; if that is 1896 the key collides with the
Festschrift paper and both become `1896a_haeckel`/`1896b_haeckel` (A7,
A11). The reading date goes in `processDates.read` either way.

**Novelty marked by verbs, never by a tag (p. 2, 11).** "die Bezeichnung
Amphoridea vorschlage", "unter dem Begriffe der Monorchonia zusammenfassen";
the four Amphoridea families and the six Cystoidea families are simply
listed. No "n.", "nov." or "m." anywhere. `new: true` rests on the verb or
on the list, and the sentence goes in `notes` (B24's hedged protologue is
the same problem from the other side).

**Bell 1891's names cited as alternatives (p. 11).** "Monorchonia (oder
,,Anactinogonidiata")" and "Pentorchonia (oder ,,Actinogonidiata")": Haeckel
offers Bell's 1891 stage names as synonyms of his own, without citing Bell.
An `or` entry on each node, with `citedAs` holding the printed parenthesis;
the attribution to Bell is derived from the 1891 record, not printed here.

**Every family heading carries an alternative name in parentheses (pp.
4–10).** "Archaeocystida (oder Protamphorida)", "Glyptocystida (oder
Apiocystida)" and so on: one heading, two names, the second sometimes
marked "p. p." or "sensu restricto". The `or` relation already covers the
Forbes 1848 form of this (H table); the qualifiers ride on the `or` entry.

**"Cladoma" as a rank word (p. 11).** "zwei verschiedenen Cladomen oder
Hauptclassen": a coined rank with its own gloss. Quote it in `notes` on the
node; it is another G8 case.

Source record: none exists. It needs journal Jenaische Zeitschrift für
Naturwissenschaft, Bd. 30 (N. F. 23), the article's pages in the volume
(the offprint's 1–12 cannot be assumed), the reading date 1895-12-13, and a
decision on the key year.

Data checks:

- `amphorida` (taxa.yaml): printed "Amphoridea", rank "Classe", proposed
  here in 1895, not 1896; the record has the wrong name, rank and year.
- Of the eight `auth: [haeckel]` records, only `amphorida` originates in
  this paper; the rest belong to 1896 or to an 1874 work, and `hemicystis`
  is Hall 1852.
- `anactinogonidiata`/`actinogonidiata` (from the Bell 1891 draft): this
  paper is their second use, as alternatives to Haeckel's own names.
