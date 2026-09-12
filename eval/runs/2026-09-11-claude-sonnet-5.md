# Grades for `2026-09-11-claude-sonnet-5.jsonl`

| class | questions | mechanical pass | judge 2/2/2 |
|---|---|---|---|
| absent | 3 | 3 | 0 |
| answerable | 12 | 2 | 1 |
| as-published | 8 | 8 | 1 |
| trajectory | 16 | 9 | 0 |
| uncaptured | 9 | 7 | 0 |

## Failures and low scores

### q001 (answerable)

Q: What new class does Fay (1962) erect for the genus Astrocystites, and what family/order sit between the genus and the class?

- judge contract 0: Two mechanism leaks: the internal 'act: moved' tag and the 'skeleton (name-and-placement) coverage is declared complete' aside about how data is held.

> Fay (1962), in the paper titled "Edrioblastoidea, a new class of Echinodermata" (Journal of Paleontology 36(2), pp. 201–205), erects the new class **Edrioblastoidea** and places the genus *Astrocystites* directly under it, moving the genus out of the class Edrioasteroidea (Fay 1962, act: moved).
> 
> In the hierarchy as entered from that paper — whose skeleton (name-and-placement) coverage is declared complete — *Astrocystites* sits immediately beneath the class Edrioblastoidea, with no family or order interposed between the genus and the class. This differs from the placements given in other sources, where the genus is put in the family Astrocystitidae (e.g. Bassler 1935, Fay 1967, Mintz 1970, Bell 1980, Smith & Jell 1990, Guensburg & Sprinkle 1994) or Steganoblastidae (Webby 1968; Sprinkle 1982), or provisionally under the class Protoblastoidea (Bassler 1936); Sprinkle (1973) likewise places it directly under Edrioblastoidea, following Fay's arrangement.

### q002 (answerable)

Q: Does Fay (1962) himself write that ottawaensis is the type species of Astrocystites, or is that flag the editor's own inference?

- mechanical: did not retrieve a claim matching {'kind': 'editorial', 'source': '1962_fay', 'subject': 'ottawaensis_whiteaves_1897', 'inferred': ['type']}
- judge grounded 1: Core claim of editorial inference matches, but the holotype caption and syntype anecdote quotes are extra detail not supported by the expected answer.
- judge complete 1: Gives the editorial-inference finding and its stated basis, but omits that a formal designation would lie in Whiteaves (1897), absent from the corpus.
- judge contract 1: Speaks of "the record's editorial note" and "Fay's entry", leaking storage/record language rather than purely community idiom.

> The type-species flag for Fay (1962) is the editor's own inference, not something Fay states in print. The record's editorial note is explicit: "Fay never prints 'type species'; the genus is monotypic (p. 201)" — the editor infers the type designation from the fact that *Astrocystites* is monotypic in Fay's treatment, rather than from any statement by Fay that *ottawaensis* is "the type species."
> 
> What Fay (1962) does print, at p. 201, is a caption reading "Holotype, 752, Canadian Geological Survey," and, at p. 205, an account of the specimen's history ("It is labelled a syntype because another specimen, lent to Mr. Hudson, Plattsburg, New York, was the other syntype. When Hudson died, this specimen disappeared."). Neither passage uses the phrase "type species" for the genus; the type-species act attached to Fay's entry is marked as inferred by the editor on that basis.

### q003 (answerable)

Q: What species do Smith & Jell (1990) designate as the type species of the new genus Cambroblastus?

- mechanical: did not retrieve a claim matching {'kind': 'act', 'source': '1990_smith.a.b_jell', 'actKind': 'type', 'subject': 'enubilatus_smith.a.b_jell_1990'}
- mechanical: did not retrieve a claim matching {'kind': 'act', 'source': '1990_smith.a.b_jell', 'actKind': 'new', 'subject': 'enubilatus_smith.a.b_jell_1990'}
- note: answered after the lookup limit was reached
- judge grounded 0: Claims no type-species act exists for Cambroblastus, which the expected answer contradicts (C. enubilatus is designated and recorded).
- judge complete 0: The required binomen Cambroblastus enubilatus and its holotype are entirely absent; an unwarranted refusal replaces the answer.
- judge contract 0: Repeatedly leaks mechanism—"corpus tools returned", "record", "retrieved", "entered", "coverage"—and treats an answerable question as a gap.

> Based on what the corpus tools returned, Smith & Jell (1990) establish *Cambroblastus* as a new genus (act "new", placed in the family Astrocystitidae, within Edrioblastoida), and this genus is subsequently carried by Guensburg & Sprinkle (1994, 2009) and Zhu, Zamora & Lefebvre (2014). However, the type-species designation itself has not yet been entered for this record: the statements retrieved for *Cambroblastus* in Smith & Jell (1990) consist only of its usage and placement in the taxonomy tree and in the cladogram, plus the act recording it as a new genus — no type-species act or associated species record is present among what has been entered for that source. The source's overall coverage confirms that type-species acts exist in this paper (six such acts are recorded across its new taxa), but none of them is attached to the *Cambroblastus* record as retrieved here, so the specific binomen Smith & Jell (1990) fixed as the type species cannot be reported from the corpus as it stands.

### q004 (answerable)

Q: What new genus and type species does Guensburg & Sprinkle (1994) erect within family Astrocystitidae?

- mechanical: did not retrieve a claim matching {'kind': 'act', 'source': '1994_guensburg_sprinkle', 'actKind': 'new', 'subject': 'lampteroblastus'}
- mechanical: did not retrieve a claim matching {'kind': 'act', 'source': '1994_guensburg_sprinkle', 'actKind': 'type', 'subject': 'hintzei_guensburg_sprinkle_1994'}
- mechanical: did not retrieve a claim matching {'kind': 'act', 'source': '1994_guensburg_sprinkle', 'actKind': 'new', 'subject': 'hintzei_guensburg_sprinkle_1994'}
- note: answered after the lookup limit was reached
- judge grounded 0: Asserts no new genus is recorded for the family, contradicting the corpus which holds Lampteroblastus hintzei.
- judge complete 0: The expected genus and type species are entirely absent from the answer.
- judge contract 0: Repeatedly cites tools, lookups, 'skeleton', field names like newTaxa/types, and proposes further searching.

> Based on what the tools returned for the corpus, I cannot report a new genus and type species that Guensburg & Sprinkle (1994) erected within Astrocystitidae. What has been entered from that source for this family is limited to: the family Astrocystitidae itself, which Guensburg & Sprinkle (1994) place as a child of Edrioblastoidina with an "emended" act (no "new" act recorded for the family), and, as its sole recorded genus-level child in the corpus's skeleton for this source, the pre-existing genus *Astrocystites* Whiteaves 1897 — carrying only a usage and a placement statement from this source, with no "new" act attached to it and no species-level (child) entries returned under it for 1994.
> 
> The source's declared coverage marks "newTaxa" and "types" as fully entered (10 new acts and 5 type acts recorded overall for this paper), so a new genus and type species are stated to exist somewhere in Guensburg & Sprinkle (1994)'s taxonomy; but among the statements the tools returned for Astrocystitidae and for *Astrocystites*, none names or places a new genus in this family, and I was not able to identify it within the lookups available. Rather than supply a name the corpus did not return to me for this family, I have to say: the new genus and type species erected in Astrocystitidae by Guensburg & Sprinkle (1994) has not been located in what was retrieved here, and a further, more targeted search of the corpus (e.g., against the family's full genus list or the paper's new-taxa acts directly) would be needed to identify it.

### q005 (answerable)

Q: What new genus and type species do Sprinkle & Sumrall (2015) place in family Astrocystitidae?

- mechanical: did not retrieve a claim matching {'kind': 'act', 'source': '2015_sprinkle_sumrall', 'actKind': 'new', 'subject': 'porosublastus'}
- mechanical: did not retrieve a claim matching {'kind': 'act', 'source': '2015_sprinkle_sumrall', 'actKind': 'type', 'subject': 'inexpectus_sprinkle_sumrall_2015'}
- mechanical: did not retrieve a claim matching {'kind': 'act', 'source': '2015_sprinkle_sumrall', 'actKind': 'new', 'subject': 'inexpectus_sprinkle_sumrall_2015'}
- note: page 351 was not among the retrieved claims
- note: answered after the lookup limit was reached
- judge grounded 1: Placement under Edrioblastoidina is plausible, but the counts of four new taxa and two type acts read as unverified embellishment.
- judge complete 0: The required answer—Porosublastus n. gen. with type species P. inexpectus, p. 351—is entirely absent.
- judge contract 0: Repeatedly cites lookups, records, coverage fields, this session and a proposed further query, leaking mechanism and planning.

> Based on what the corpus has returned, I can confirm that **Sprinkle & Sumrall (2015)**, "New edrioasterine and astrocystitid (Echinodermata: Edrioasteroidea) from the Ninemile Shale (Lower Ordovician), central Nevada" (*Journal of Paleontology* 89(2): 346–352), place family Astrocystitidae as a child of suborder Edrioblastoidina, within the paper's classification tree, and the source's declared coverage shows four new taxa and two new-type acts entered for that paper (coverage of new taxa and types recorded as "all").
> 
> However, none of my lookups succeeded in resolving the specific new genus-and-species name that the paper assigns to Astrocystitidae — my attempts to identify it via the taxonomic hierarchy (working down from Edrioblastoidina → Astrocystitidae) returned only the family-level usage and placement records, not the genus entered beneath it, and my attempts to resolve candidate genus names returned nothing in the corpus. I therefore cannot report the new genus and type species from what has been retrieved: that specific statement has not been surfaced in this session, even though the source itself is on record with "newTaxa" and "types" coverage marked as fully entered. A further targeted lookup (resolving the actual genus name printed in Sprinkle & Sumrall 2015 and pulling its placement/act record) would be needed to answer precisely.

### q006 (answerable)

Q: What species do Sumrall, Heredia Rodríguez & Mestre (2013) confirm as the type species of Rhenopyrgus?

- mechanical: did not retrieve a claim matching {'kind': 'act', 'source': '2013_sumrall_heredia_rodríguez.c.m_mestre', 'actKind': 'type', 'subject': 'coronaeformis_rievers_1961'}
- mechanical: did not retrieve a claim matching {'kind': 'acceptance', 'source': '2013_sumrall_heredia_rodríguez.c.m_mestre', 'stance': 'accepts', 'subject': 'coronaeformis_rievers_1961', 'parents': ['rhenopyrgus-subgenus', 'pyrgocystis']}
- note: page 773 was not among the retrieved claims
- note: answered after the lookup limit was reached
- judge grounded 0: Denies a type-species statement the corpus does hold, and adds record-level detail contradicting the expected answer.
- judge complete 0: Fails to name Pyrgocystis (Rhenopyrgus) coronaeformis Rievers, 1961, or cite p. 773.
- judge contract 0: Repeatedly cites tools, queries, records, act "kinds" and what has "come back", leaking mechanism instead of scientific language.

> Based on what the corpus returns for the 2013 source, Sumrall, Heredia Rodríguez & Mestre (2013) treat *Rhenopyrgus* Dehm, 1961 as a genus placed in Rhenopyrgidae, and they record an emendation act for the genus (kind "emended") at that placement. However, the statements entered for this source under "type"-kind acts for *Rhenopyrgus* (or for its included species) have not come back through any of the queries performed — no type-species act is attached to the *Rhenopyrgus* record for the 2013 source in what has been entered so far. There is a species-level record nested beneath *Rhenopyrgus* in the 2013 taxonomy tree (visible only as a synonymy pointing back to *Pyrgocystis* and to the subgenus *Rhenopyrgus* Dehm, 1961), but its actual species name has not surfaced in the statements returned, and no explicit "confirmed as type species" act tied to it has come back either.
> 
> In short: for Sumrall, Heredia Rodríguez & Mestre (2013), the corpus confirms an emended placement/diagnosis of the genus *Rhenopyrgus* within Rhenopyrgidae, but the specific type-species designation this paper is said to confirm has not yet been entered (or at least has not been returned) for this source — I cannot name that species from what the tools have provided.

### q007 (answerable)

Q: What new genus does Briggs et al. (2017) place in family Rhenopyrgidae, and what is its type species?

- mechanical: did not retrieve a claim matching {'kind': 'act', 'source': '2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman', 'actKind': 'new', 'subject': 'heropyrgus'}
- mechanical: did not retrieve a claim matching {'kind': 'placement', 'source': '2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman', 'subject': 'heropyrgus', 'parent': 'rhenopyrgidae'}
- mechanical: did not retrieve a claim matching {'kind': 'act', 'source': '2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman', 'actKind': 'type', 'subject': 'disterminus_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman_2017'}
- mechanical: did not retrieve a claim matching {'kind': 'act', 'source': '2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman', 'actKind': 'new', 'subject': 'disterminus_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman_2017'}
- note: answered after the lookup limit was reached
- judge grounded 1: Bibliographic and coverage details are plausible, but the Edrioblastoidina placement and the Rhenopyrgus/Postibulla elimination are unsupported embellishments.
- judge complete 0: Fails to name Heropyrgus gen. nov. and its type species Heropyrgus disterminus, which the corpus holds.
- judge contract 0: Repeatedly cites tools, searches, records, coverage values and lookups, and treats a held claim as unretrievable rather than answering.

> Based on what the tools have returned for this corpus, I can confirm that Briggs et al. (2017), in "An edrioasteroid from the Silurian Herefordshire Lagerstätte of England reveals the nature of the water vascular system in an extinct echinoderm" (*Proceedings of the Royal Society B*, vol. 284), place the family Rhenopyrgidae within Edrioblastoidina, and the source's declared coverage shows two new taxa and one type-species designation entered for this paper (coverage for new taxa and types is recorded as "all").
> 
> However, the specific new genus and its type species have not been resolved among the records I was able to check in the corpus (the searches I ran for candidate genus names under Rhenopyrgidae, including the previously established genera Rhenopyrgus (Dehm, 1961) and Postibulla (Bell, 1976), returned no 2017 entries, meaning neither is the genus in question). The actual name of the new genus Briggs et al. (2017) erected, and its type species, has not yet been identified from what the tools returned — this remains work in progress rather than something the corpus can be said to lack, since the paper is known to the corpus and its new-taxon and type-species content is marked as entered, but I was not able to retrieve the specific record within the lookups available.

### q008 (answerable)

Q: In Holloway & Jell (1983), family Rhenopyrgidae is placed under a name that is not itself an order. What is that placeholder, and what does it mean?

- mechanical: did not retrieve a claim matching {'kind': 'act', 'source': '1983_holloway_jell', 'actKind': 'new', 'subject': 'rhenopyrgidae'}
- judge grounded 1: Core placement is right, but calling it an 'editorial stand-in' misattributes a phrase the paper itself prints as 'Order UNCERTAIN'.
- judge complete 1: Names the placeholder and class but omits the page citation and the two weighed candidate orders (Isorophida vs. Edrioasterida).
- judge contract 0: Repeatedly describes internal structure and storage ('the corpus records as', 'placeholder node', 'listed as a child at the rank of order') and gives no source page.

> In Holloway & Jell (1983), the family Rhenopyrgidae is not placed directly under a named order but under a placeholder node the corpus records as "order uncertain" — i.e. an order-rank slot within the class Edrioasteroidea whose identity Holloway & Jell leave unspecified. That placeholder node is itself listed as a child of Edrioasteroidea at the rank of order, but it carries no order name; it simply marks that Holloway & Jell (1983) assign Rhenopyrgidae to Edrioasteroidea without committing to which (or any) order it belongs in. So the "name" under which Rhenopyrgidae is placed in that paper is not a genuine order but an editorial stand-in for "order uncertain" within Edrioasteroidea.

### q009 (answerable)

Q: What new species of Rhenopyrgus does Grigo (2000) describe, and from where?

- mechanical: did not retrieve a claim matching {'kind': 'act', 'source': '2000_grigo', 'actKind': 'placeholder', 'subject': 'rhenopyrgus-sp_grigo_2000', 'placeholder': 'open'}
- mechanical: did not retrieve a claim matching {'kind': 'placement', 'source': '2000_grigo', 'subject': 'rhenopyrgus-sp_grigo_2000', 'parent': 'rhenopyrgus'}
- note: page 96 was not among the retrieved claims
- note: answered after the lookup limit was reached
- judge grounded 1: Placement on p. 95 is plausible corpus content, but the flat denial that a new Rhenopyrgus species is recorded conflicts with the held claim.
- judge complete 0: Misses the Rhenopyrgus sp. nov. on p. 96 and the Eifelian Ahrdorf Formation localities near Gerolstein and Gees entirely.
- judge contract 0: Exposes internal mechanism ('source-level record', 'acts of the new kind', 'skeleton-level, unaudited') and frames the gap as the source lacking the statement.

> Based on what the corpus has entered so far, no source records a new species of *Rhenopyrgus* by Grigo (2000). What has been entered for Grigo (2000) regarding *Rhenopyrgus* is a single usage and placement of the genus itself (as a member of Rhenopyrginae, p. 95) — no species-level statement, and no act of the "new" kind is attached to the genus *Rhenopyrgus* in that source. The source-level record for Grigo (2000) does show two acts of the "new" kind and two "type" acts overall in the paper, but these have not been resolved in the corpus to any species placed in *Rhenopyrgus*; the taxon or taxa they concern have not been entered under that name. Given the coverage declared for this source (skeleton-level, unaudited for these statements), I can't say from what has been entered whether Grigo (2000) does or does not name a new *Rhenopyrgus* species, or supply a locality for one — that detail has not yet been entered for this source.

### q010 (answerable)

Q: What is the holotype specimen number for Rhenopyrgus viviani, named by Ewin, Martin, Isotalo & Zamora (2020)?

- mechanical: did not retrieve a claim matching {'kind': 'act', 'source': '2020_ewin_martin.m_isotalo_zamora', 'actKind': 'new', 'subject': 'viviani_ewin_martin.m_isotalo_zamora_2020'}

> According to Ewin, Martin, Isotalo & Zamora (2020, pp. 120–122), the holotype of *Rhenopyrgus viviani* is specimen **NHMUK EE16642**, from Rock Pool Ledge, Jupiter River Section, Anticosti Island, Québec, Canada (Cybèle Member, Jupiter Formation, Telychian).

### q011 (answerable)

Q: What is the holotype specimen number for Rhenopyrgus grayae, per Ewin et al. (2020)?

- note: page 122 was not among the retrieved claims
- judge grounded 1: Cites p. 118 rather than p. 122 and adds 'Craighead Inlier' and authorship, details not supported by the expected answer.

> Ewin et al. (2020, p. 118) list the holotype of *Rhenopyrgus grayae* (Bather, 1915) as NHMUK E23470, recovered from the Lady Burn Starfish Bed (Farden Member, South Threave Formation, Drummuck Group), Craighead Inlier, near Girvan, Scotland (Upper Ordovician, Katian). The same entry lists additional, unspecified NHMUK material (E23674 and E29570) from the same occurrence.

### q012 (answerable)

Q: Which two genera does Ewin et al. (2020) list under the emended family Rhenopyrgidae?

- mechanical: did not retrieve a claim matching {'kind': 'placement', 'source': '2020_ewin_martin.m_isotalo_zamora', 'subject': 'heropyrgus', 'parent': 'rhenopyrgidae', 'position': 1}
- note: answered after the lookup limit was reached
- judge grounded 1: Rhenopyrgus placement is supported, but the claim that no second genus is held contradicts the corpus, which holds Heropyrgus.
- judge complete 1: Only Rhenopyrgus is named; Heropyrgus Briggs et al., 2017 and the emended diagnosis wording are missing.
- judge contract 0: Opens with "what the tools returned" and repeatedly cites records retrieved, leaking mechanism language forbidden by the contract.

> Based on what the tools returned for Ewin, Isotalo, Martin & Zamora (2020, p. 118), the corpus records the emended family Rhenopyrgidae as containing the genus **Rhenopyrgus**, placed there with an emended diagnosis in that same source. That is the only genus-level placement under Rhenopyrgidae that has been entered for this source in the corpus; a second genus belonging to the family has not turned up in the records retrieved here, so I cannot name it. If the printed paper lists a second genus under the family, that placement has not yet been entered for this source in the corpus.

### q013 (uncaptured)

Q: What holotype and paratype specimen numbers does Holloway & Jell (1983) give for Rhenopyrgus whitei?

- judge complete 1: The refusal is correctly framed but omits the page location (p. 1004) and the note that the paper prints type numbers for each species.
- judge contract 1: Names the gap as not yet entered rather than absent from the paper, but leaks internal mechanism with "entered for this record in the corpus" and "not available here".

> The corpus records that Holloway & Jell (1983) erected *Rhenopyrgus whitei* as a new species, placed under *Rhenopyrgus* (Holloway & Jell 1983). However, no material (specimen) statements — holotype or paratype numbers — have been entered for this record in the corpus, so the specific holotype and paratype numbers printed in Holloway & Jell (1983) are not available here; that material has not yet been entered.

### q014 (uncaptured)

Q: What occurrence data does Guensburg & Sprinkle (1994) print for the new species Lampteroblastus hintzei?

- judge complete 1: Names the gap and the coverage value but omits what the paper prints (formation, member, zone, locality, pp. 14–37).
- judge contract 1: Correctly frames the gap as not yet entered, but leaks internal field names ('material' and 'occurrences' statements, 'on record').

> The corpus records Guensburg & Sprinkle (1994) as having established *Lampteroblastus hintzei* as a new species (with a type act recorded), placed as a species under *Lampteroblastus*. However, for this source the declared coverage for both "material" and "occurrences" statements is **none** — meaning any specimen or locality/occurrence data the paper prints for *Lampteroblastus hintzei* has not yet been entered into the corpus. So I cannot report what occurrence data the paper contains; only that the paper is on record and its occurrence content awaits entry.

### q015 (uncaptured)

Q: What is the full printed diagnosis of Rhenopyrgus nov. subgen. in Dehm (1961)?

- judge complete 1: Names the gap and the coverage value but omits the type-species fixation of Pyrgocystis coronaeformis Rievers (1961) that the corpus does hold.
- judge contract 1: Refusal is properly framed as a corpus gap, but "has not been entered" and "still outstanding work" read as a finished judgement and process aside.

> The corpus records Dehm's (1961) establishment of *Rhenopyrgus* nov. subgen. (in *Pyrgocystis*, p. 16) as an act of new-taxon erection and gives its placement under *Pyrgocystis*, but the diagnosis for this paper has not been entered: Dehm 1961's declared coverage for diagnoses is "none," meaning the diagnostic text printed in that paper is not yet part of the corpus. I cannot supply the printed diagnosis of *Rhenopyrgus* nov. subgen. from Dehm (1961) — only that a diagnosis exists in the paper is implied by its status as a formal subgeneric proposal, not the wording itself, which is still outstanding work.

### q016 (uncaptured)

Q: What illustrations does Fay (1962) print for Astrocystites ottawaensis?

- judge complete 1: Correctly names the gap and coverage value but omits the printed plate 34, figs. 1–5 and text-figures 1–3.
- judge contract 1: Names the gap properly but slips into storage language ("entered into the corpus", "specimen record", "so far recorded").

> For Fay (1962), the illustrations coverage for this source is declared "none" — that is, the illustrations Fay's paper prints have not been entered into the corpus. The only material statement so far recorded for *Astrocystites ottawaensis* is the specimen citation on p. 201, where the holotype (captioned "Holotype, 752, Canadian Geological Survey," discussed further on p. 205 as originally one of two syntypes) is noted, but this is a specimen record, not an illustration.
> 
> So the answer is that any figures/plates Fay (1962) prints for this species have not yet been entered for this source, and nothing can be reported about their content from the corpus at this time.

### q017 (uncaptured)

Q: What is the second sentence of Rievers's (1961) printed diagnosis for Pyrgocystis coronaeformis?

- judge grounded 1: The first sentence is rendered as a loose English paraphrase with added gloss '(stem)' rather than the entered printed wording.
- judge complete 1: Correctly flags the gap and the 'partly' coverage, but omits the second sentence's text that the expected answer supplies.
- judge contract 1: Phrasing of the gap is acceptable, but the hedge 'if the original printed diagnosis contains one' casts doubt on the paper rather than the corpus.

> The corpus currently holds only a single sentence of Rievers's (1961) diagnosis for *Pyrgocystis coronaeformis* (as printed on pages 10–11): "A *Pyrgocystis* specimen measuring 95 mm in overall length, featuring a scaly column (stem) approximately 13 mm in diameter, which transitions at its lower end into a rounded, sac-like structure measuring 27 mm in height and approximately 17 mm in diameter." 
> 
> Rievers 1961's diagnoses are declared only "partly" entered for this source, so any further sentence — including a second one, if the original printed diagnosis contains one — has not yet been entered into the corpus.

### q018 (uncaptured)

Q: Whose holotype does Briggs et al. (2017) cite for Heropyrgus disterminus, and where is it deposited?

- judge complete 1: The refusal and coverage value are right, but the printed holotype OUMNH C.36043 with paratypes, cited to p. 2, is missing.
- judge contract 1: Gap is correctly named as not yet entered, but the closing remark about inventing facts and talk of 'entered' coverage fields drifts from the community's voice.

> The type-act statement for *Heropyrgus disterminus* in Briggs, Siveter, Siveter, Sutton & Rahman (2017) is recorded only as an act (a type designation), with no accompanying specimen or repository detail entered — the corpus's declared coverage of "material" statements (specimens, occurrences, repositories) for this paper is "none," even though its coverage of "types" acts is "all." In other words, the paper is on record as fixing a holotype for the species, but the identity of the specimen and where it is deposited have not yet been entered from that paper. I can't report a specimen number or a museum for the holotype without that being a fact I invented rather than one the corpus holds.

### q019 (uncaptured)

Q: Which earlier works does Fay (1962) cite in his synonymy of Astrocystites ottawaensis?

- mechanical: refusal says the paper lacks it: paper lacks
- judge grounded 1: Correctly names the partly coverage but wrongly states no earlier usage is held as a synonym, whereas the Steganoblastus usage is recorded.
- judge complete 1: The refusal with declared coverage is present, but the printed list of cited works and the one held Steganoblastus entry are missing.
- judge contract 1: Names the gap as the corpus's and passes no verdict, but speaks of the corpus's 'transcription', a mechanism of how facts are held.

> For *Astrocystites ottawaensis* (Whiteaves, 1897), the corpus does not carry any entered synonymy citations from Fay (1962). The claims recorded for that species under Fay 1962 are limited to its placement under *Astrocystites* and an (editorially inferred) type-species designation, plus the material note on the syntypes (p. 201, 205); no acceptance of any earlier usage as a synonym appears among them.
> 
> This matches the declared coverage for Fay (1962): the synonymy content of that paper is recorded as only "partly" entered into the corpus. So the earlier works Fay actually cites in his synonymy of this species — whatever they are in the printed paper — have not yet been entered; the gap is in the corpus's transcription of that synonymy, not evidence that Fay's paper lacks one.

### q020 (uncaptured)

Q: What holotype and paratype numbers does Sumrall et al. (2013) give for Rhenopyrgus piojoensis?

- mechanical: refusal does not say the material has not yet been entered
- judge complete 1: The refusal and coverage value are present, but the printed holotype PIL 14656-H, paratypes PIL 14174–14872 and pages 774–775 are missing.
- judge contract 1: Names the gap correctly as not yet entered, but leaks storage language with "entered for this record".

> The corpus records that Sumrall, Heredia, Rodríguez and Mestre (2013) establish *Rhenopyrgus piojoensis* as a new species and place it under *Rhenopyrgus* (Sumrall et al. 2013), but no material statement carrying holotype or paratype specimen numbers has been entered for this record. The paper's declared coverage for material is "none," so this is a case of the underlying content not yet having been entered rather than the paper lacking such data — the specimen numbers printed in Sumrall et al. (2013) are simply not yet available in the corpus.

### q021 (as-published)

Q: What exact suborder heading do Ewin et al. (2020) print above family Rhenopyrgidae, and at what rank was that name first established?

- judge grounded 1: Core facts match, but the long chain of intermediate papers and the claim of an emendation are embellishments beyond the expected answer.
- judge contract 1: Gives the printed form verbatim with citation and an asked-for correction, but leaks mechanism with "recorded in the corpus as an act of new establishment at the rank of Class".

> Ewin, Martin, Isotalo & Zamora (2020, p. 118) print the heading **"Suborder Edrioblastoidina Fay, 1962"** directly above the family Rhenopyrgidae.
> 
> That name, however, was not established as a suborder at all: Fay (1962) originally proposed it as the new class Edrioblastoidea (recorded in the corpus as an act of new establishment at the rank of Class). It was carried at class rank through Fell (1965), Fay (1967), Ubaghs (1967), Webby (1968), Mintz (1970) and Sprinkle (1973, 1982). Guensburg & Sprinkle (1994) then emended it and, as a nomen translatum, transferred/altered its rank to the suborder Edrioblastoidina placed within Edrioasterida — the rank and spelling that Grigo (2000), Sumrall et al. (2013), Sprinkle & Sumrall (2015), Briggs et al. (2017) and, finally, Ewin et al. (2020) all continue to use.

### q022 (as-published)

Q: What author and year does Bell & Sprinkle (1978) print for family Edrioasteridae?

- judge complete 1: Gives the verbatim family line and page but omits the p. 245 'order Edrioasterida as proposed by Bell (1976a)' support.

> Bell & Sprinkle (1978, p. 246) print the family as "Family Edrioasteridae Bell, 1976 [emend. herein]" — i.e., they cite the authorship as Bell, 1976, with an emendation of their own noted at that place.

### q023 (as-published)

Q: How does Bassler (1936) print the original-genus citation for Cystaster granulatus?

- judge grounded 0: Calls Hemicystites a subgenus and glosses Hall's parentheses from general nomenclature, contradicting Bassler's stated original-genus convention.
- judge complete 1: Gives the printed string but omits the p. 4 and p. 25 occurrences, page citations, and the p. 2 convention.
- judge contract 1: Quotes the printed form but supplies no citation and adds unrequested interpretive correction rather than verbatim reportage.

> Bassler (1936) cites this species as "C. (Hemicystites) granulatus (Hall)" — i.e., under *Cystaster* with *Hemicystites* given as the subgenus, and the author Hall placed in parentheses to indicate the species was originally described in a different genus.

### q024 (as-published)

Q: How did Dehm (1961) style the new subgenus name Rhenopyrgus, and how do Sumrall et al. (2013) cite the type species using that name?

- judge grounded 1: Verbatim forms and pages match, but the invented author list "Rodríguez-Cíntas & Mestre" and the added current-classification gloss are unsupported embellishment.
- judge contract 0: Repeatedly leaks internals — "record: rhenopyrgus-subgenus", "the corpus records this as a 'new' act", "the acceptance there naming both ... as the parents".

> Dehm (1961) introduced Rhenopyrgus explicitly as a new subgenus: at p. 16 he prints it "Rhenopyrgus nov. subgen." within Pyrgocystis (record: rhenopyrgus-subgenus), and the corpus records this as a "new" act on that page.
> 
> Sumrall, Rodríguez-Cíntas & Mestre… (i.e. Sumrall et al. 2013), when giving the synonymy of the type species, cite it under the older combination exactly as "Pyrgocystis (Rhenopyrgus) coronaeformis Rievers, 1961" (p. 773), with the acceptance there naming both Rhenopyrgus (as subgenus) and Pyrgocystis as the parents of that synonymized usage. In their own current classification, however, Sumrall et al. (2013) place the same species, coronaeformis, directly under the genus Rhenopyrgus (an emended genus in their taxonomy), so the subgeneric combination appears only in the synonymy list, not as the name they use for current placement.

### q025 (as-published)

Q: What year does Bassler (1936) print for Hall's authorship of Cincinnatidiscus (Hemicystites) stellatus?

- judge complete 1: Gives the printed year and form but omits the page citation (p. 5) and Bassler's own 1935 paper crediting 1866.
- judge contract 1: Quotes the printed form as required but says "other records in the corpus", using storage language instead of naming sources.

> Bassler (1936) prints the name as "CINCINNATIDISCUS (HEMICYSTITES) STELLATUS (Hall), 1856" — that is, the year 1856 is given as Hall's authorship date, even though other records in the corpus treat Hall's authorship as 1866.

### q026 (as-published)

Q: What two different words does Fay (1962) use for the same specimen, No. 752, in Astrocystites ottawaensis?

- judge grounded 1: Both terms, pages and the Hudson quotation match, but the repository is rendered "Geological Survey of Canada" rather than the printed "Canadian Geological Survey."
- judge contract 1: For an as-published question it silently modernizes the printed institution name instead of quoting it verbatim; otherwise clean and citation-bound.

> Fay (1962) applies two different terms to the same specimen, No. 752 (Geological Survey of Canada): it is captioned as the "Holotype" in the plate/figure caption on p. 201, while in the text on p. 205 Fay calls it a "syntype," explaining that "it is labelled a syntype because another specimen, lent to Mr. Hudson, Plattsburg, New York, was the other syntype," which disappeared after Hudson's death.

### q028 (as-published)

Q: What exact heading and parenthetical act does Guensburg & Sprinkle (1994) print for the Rhenopyrgus subfamily?

- note: page 21 was not among the retrieved claims
- judge grounded 1: Core acts are right, but the Cyathocystidae placement and the claim of no page attached are unsupported embellishments.
- judge complete 1: Names nomen transl. and emend., yet omits the verbatim parenthetical heading, the 'ex ... Rhenopyrgidae' wording and p. 21.
- judge contract 0: Repeatedly leaks internal mechanics — 'the record's own authority citation', 'no page attached to the statement', 'recorded in the corpus'.

> Guensburg & Sprinkle (1994, in Fieldiana Geology n.s. 29) enter Rhenopyrginae as a subfamily placed under the family Cyathocystidae, printed with the authority as recorded, i.e. as "Subfamily Rhenopyrginae Holloway & Jell, 1983" (the corpus notes the printed attribution matches the record's own authority citation, with no page attached to the statement).
> 
> Under that heading the paper carries two acts on the name: it is treated as **emended**, and it is marked as a **nomen translatum** from the family-rank name Rhenopyrgidae — the parenthetical wording the corpus preserves for this second act is "**nomen transl.**". No separate parenthetical wording is recorded in the corpus for the "emended" act beyond the act itself.

### q029 (trajectory)

Q: Where do sources place family Rhenopyrgidae (or its subfamily-rank predecessor) across the 1983-2020 literature?

- judge grounded 1: Adds a Müller & Hahn (2010) Isorophida placement and audit/coverage status not supported by the expected account.
- judge complete 1: Present position and main history are given, but Sumrall et al.'s explicit rejection quote and nearly all page citations are missing.
- judge contract 0: Multiple lapses: 'unaudited', 'entry', 'flagged as only partly covering', 'declared as fully entered' expose records and coverage machinery.

> **Measured present (2013–2020):** three papers, from three distinct sets of co‑authors, currently place Rhenopyrgidae as a family under the taxon Edrioblastoidina: Sumrall, Heredia, Rodríguez & Mestre (2013), who also re‑emended the family in that placement; Briggs, Siveter, Siveter, Sutton & Rahman (2017); and Ewin, Martin, Isotalo & Zamora (2020, p. 118), who likewise state an emendation there. No author is shared across these three papers, so this is an independently converged position held continuously from 2013 to 2020.
> 
> **History of earlier positions:**
> - The family was erected by Holloway & Jell (1983) as new, placed under "Edrioasteroidea, order uncertain" — i.e. under an explicit placeholder for an unresolved ordinal assignment, not a named order.
> - Guensburg & Sprinkle (1994) treated it as a nomen translatum at subfamily rank, "Rhenopyrginae," emending it and placing it under family Cyathocystidae.
> - Grigo (2000) is the last paper in the corpus to hold that subfamilial placement under Cyathocystidae.
> - Müller & Hahn (2010) instead placed the family Rhenopyrgidae under the order Isorophida; this placement is not echoed by any other paper in the corpus and its entry is unaudited.
> - From 2013 onward the three papers named above place it under Edrioblastoidina, the position still held in the latest source (Ewin et al. 2020).
> 
> A note on completeness: the 2013 Sumrall et al. entry is flagged as only partly covering that paper's placement statements, though the Rhenopyrgidae placement itself is among what has been entered; the 1983, 2017 and 2020 entries are declared as fully entered for this kind of statement, while the 2010 Müller & Hahn entry remains unaudited.

### q030 (trajectory)

Q: Is Rhenopyrgus a genus or a subgenus of Pyrgocystis?

- note: did not retrieve a claim matching {'kind': 'act', 'source': '1983_holloway_jell', 'actKind': 'new', 'subject': 'rhenopyrgidae'}
- judge grounded 1: Sources and quotes look corpus-based, but the tally of 'five papers/co-author sets' misstates the six papers it itself lists.
- judge complete 1: Has Dehm, Regnéll, the 1983 elevation and the paper list, but miscounts, omits the Jell overlap and the Holloway & Jell rejection statement.
- judge contract 1: Leads with the 1961 history rather than the measured present, and closes with the editorial 'no longer linked to Pyrgocystis'.

> Rhenopyrgus was originally proposed by Dehm (1961: 16) as a new subgenus under the genus Pyrgocystis ("Rhenopyrgus nov. subgen."), and Regnéll (1966) likewise carried it as a subgenus of Pyrgocystis.
> 
> From Holloway & Jell (1983) onward, however, it is treated as a full genus, placed in family Rhenopyrgidae — a position followed by Smith & Jell (1990), Guensburg & Sprinkle (1994, within Rhenopyrginae), Grigo (2000: 95, within Rhenopyrginae), Sumrall et al. (2013, with an emendation, in Rhenopyrgidae), and Ewin et al. (2020: 118, also emended, in Rhenopyrgidae).
> 
> So the present, and long-standing, treatment across five papers/co-author sets spanning 1983–2020 is as an independent genus, no longer linked to Pyrgocystis; the subgeneric placement under Pyrgocystis is the original 1961 concept, last held in the corpus by Regnéll (1966).

### q031 (trajectory)

Q: What genus is Pyrgocystis octogona (Richter, 1930) placed in across the corpus?

- judge complete 1: Captures both Pyrgocystis placements but omits Dehm's comparandum framing, Holloway & Jell's misattribution, and the Klug/Müller & Hahn dissent.
- judge contract 1: Language and absence of verdict are fine, but the trajectory form lacks the later history and named dissent.

> Both sources in the corpus that treat this species place it in the genus **Pyrgocystis**: Bassler (1935) lists *Pyrgocystis octogona* (Richter, 1930) as a species of *Pyrgocystis*, and Dehm (1961) likewise places it under *Pyrgocystis*, citing Richter (1930, p. 294, fig. 1h) and recording an occurrence at Bornich, near Weisel on the Rhine, Germany, in Lower Devonian greywacke slates. No other genus is used for this name across the corpus.

### q032 (trajectory)

Q: What class or order has Astrocystites been placed in, across the sources that treat it?

- note: did not retrieve a claim matching {'kind': 'act', 'source': '1962_fay', 'actKind': 'new', 'subject': 'edrioblastoidea'}
- judge grounded 0: Invents Sprinkle (1973) and Bell (1980) placements and Pelmatozoa/Crinozoa details, and asserts Guensburg & Sprinkle (1994) is the most recent source.
- judge complete 1: Captures the 1935–1994 history but omits the measured present (Zhu et al. 2014, Sprinkle & Sumrall 2015, Jell & Sprinkle 2021, rhenopyrgid papers) and Bassler's "POSITION UNCERTAIN".
- judge contract 1: Leads with a source-by-source list rather than the measured present, and misreports which position currently stands, though it passes no verdict.

> Across the eleven sources in the corpus that carry a placement for the genus *Astrocystites* (Whiteaves, 1897), the higher assignment has shifted several times and the direct parent named is not always the same rank:
> 
> **Placed directly in a class**
> - Fay (1962) moves the genus out of Edrioasteroidea and places it directly in the class **Edrioblastoidea**.
> - Sprinkle (1973) likewise places it directly under the class **Edrioblastoidea**, which he in turn sets within Echinozoa.
> 
> **Placed in a family that is itself referred to a class/order**
> - Bassler (1935) erects the family Astrocystitidae for it (called there a "new name," provisionally) and places that family under the class **Edrioasteroidea**.
> - Bassler (1936) instead places the genus, provisionally, in the **Protoblastoidea**, which he ranks as a "Grade" under Blastoidea — a different lineage from the Edrioasteroidea placement of his own 1935 paper.
> - Fay (1967) puts the genus in family Astrocystitidae, that family in the order **Pentacystida**, and Pentacystida in the class **Edrioblastoidea**.
> - Webby (1968), citing Bather's objection to the genus name and the substitute Steganoblastus, places *Astrocystites* in family **Steganoblastidae**, which he refers to the class Edrioblastoidea, itself placed under Pelmatozoa (p. 513–514).
> - Mintz (1970) places the genus in family Astrocystitidae under the class Edrioblastoidea, which he in turn places under Crinozoa.
> - Bell (1980) likewise places it in family Astrocystitidae under the class Edrioblastoidea.
> - Sprinkle (1982) places it in family Steganoblastidae, under order Pentacystida, under class Edrioblastoidea (itself under Echinozoa).
> - Smith & Jell (1990) place it in family Astrocystitidae, which they refer to the order **Edrioblastoida**, itself placed under the class Edrioasteroidea.
> - Guensburg & Sprinkle (1994) — the most recent source in the corpus to carry this placement — put the genus in family Astrocystitidae, that family under the suborder **Edrioblastoidina**, itself under order Edrioasterida within the class Edrioasteroidea (which they place under Echinozoa).
> 
> So, measured across the corpus: 11 sources spanning 1935–1994 treat *Astrocystites*, and no single co-author group repeats a placement — each paper (Bassler 1935, Bassler 1936, Fay 1962, Fay 1967, Webby 1968, Mintz 1970, Sprinkle 1973, Bell 1980, Sprinkle 1982, Smith & Jell 1990, Guensburg & Sprinkle 1994) is a distinct authorial position. The recurring higher term is **Edrioblastoidea** (as class, or, in later schemes, demoted to order/Edrioblastoida or suborder/Edrioblastoidina), used by Fay (1962, 1967), Webby (1968), Mintz (1970), Sprinkle (1973, 1982), Smith & Jell (1990) and Guensburg & Sprinkle (1994) in one rank or another, itself nested at various times under Pelmatozoa (Webby 1968), Crinozoa (Mintz 1970) or Echinozoa (Sprinkle 1973, 1982; Guensburg & Sprinkle 1994), or under class Edrioasteroidea (Smith & Jell 1990; Guensburg & Sprinkle 1994). Bassler's two papers stand apart: in 1935 he referred the containing family directly to class Edrioasteroidea, and in 1936 he moved the genus, provisionally, to the Protoblastoidea under Blastoidea — a placement not repeated by any later source in the corpus.

### q033 (trajectory)

Q: What year does the corpus give for family Edrioasteridae's authorship, Bather 1898 or 1899?

- mechanical: answer does not cite Bell & Sprinkle 1978
- mechanical: answer does not cite Sprinkle & Sumrall 2015
- note: did not retrieve a claim matching {'kind': 'usage', 'source': '2015_sprinkle_sumrall', 'subject': 'edrioasteridae', 'printed': {'citedAs': 'Family Edrioasteridae Bather, 1899'}}
- note: did not retrieve a claim matching {'kind': 'usage', 'source': '2015_sprinkle_sumrall', 'subject': 'edrioasterina', 'printed': {'citedAs': 'Suborder Edrioasterina, Bather, 1898'}}
- note: did not retrieve a claim matching {'kind': 'usage', 'source': '1978_bell.b.m_sprinkle', 'subject': 'edrioasteridae', 'printed': {'citedAs': 'Family Edrioasteridae Bell, 1976 [emend. herein]'}}
- judge grounded 0: Claims 11 sources cite Bather 1899, whereas only Sprinkle & Sumrall (2015) prints a year for the family.
- judge complete 0: Omits the page citation, the coordinate suborder's 1898 date, and Bell & Sprinkle's competing 'Bell, 1976' attribution.
- judge contract 0: No measured present with counts and co-author sets, no history, no dissent named, and no source-and-page citation.

> The corpus records the family Edrioasteridae with the authority "Bather 1899" (11 sources cite it under this authorship/year), not 1898.

### q034 (trajectory)

Q: Who does the corpus credit as the author of Cambraster, and does every source agree?

- mechanical: answer leaks internals: "resolve_name"
- judge grounded 0: Asserts Jell & Sprinkle (2021) prints no author, which the expected answer contradicts — it prints "Cabibel et al., 1958".
- judge complete 1: Captures Jaekel 1923 and Guensburg & Sprinkle 1994 but misses the 2021 printed attribution, the Sprinkle overlap, and the absence of any stated correction.
- judge contract 0: Leaks mechanism ("default record", "resolve_name attribution", "as-record") and editorializes with "working attribution" and "documented exception" rather than neutral measurement.

> The corpus's default record for *Cambraster* carries the authority "Jaekel, 1923" (resolve_name attribution), and every other source that uses the name — Jell, Burrett & Banks (1985), Smith (1985), Smith & Jell (1990), Sumrall & Zamora (2011), Zamora (2013), Zamora et al. (2013) and Jell & Sprinkle (2021) — cites it "as‑record," i.e. without printing a different author, so their usage is consistent with the Jaekel 1923 attribution.
> 
> One source disagrees explicitly: Guensburg & Sprinkle (1994) print the genus as "*Cambraster* Cabibel, Termier, and Termier, 1958" in their placement under Edrioasteroidea (family uncertain). So while the corpus's working attribution is Jaekel 1923 and the great majority of citing sources are silent-consistent with it, Guensburg & Sprinkle (1994) is a documented exception, crediting the name instead to Cabibel, Termier & Termier, 1958.

### q035 (trajectory)

Q: Is Isorophus (and its sibling genus Carneyella) attributed to Foerste 1916 or 1917?

- note: page 42 was not among the retrieved claims
- judge grounded 0: Asserts Sumrall & Zamora (2011) prints no alternate year, which the expected answer contradicts (it prints Foerste, 1917, p. 435).
- judge complete 1: Captures the Guensburg & Sprinkle 1994 divergence but misses the second 1917 source and omits that no paper adjudicates.
- judge contract 0: Leaks mechanism repeatedly ("resolved records", "record's default authority", missing page citation) and frames one year as the "standard attribution".

> Both genera are attributed to Foerste 1916 as their primary authority in this corpus's resolved records (Isorophus: 14 sources; Carneyella: 11 sources; both cited "Foerste 1916").
> 
> However, one paper prints a different year for both: Guensburg & Sprinkle (1994) explicitly cite them as "Isorophus Foerste, 1917" and "Carneyella Foerste, 1917" in their usage and placement statements (p. inherited from the taxonomic listing). Every other source that carries these names in the corpus — Bassler (1935, 1936), Regnéll (1966), Bell (1976, 1980), Holloway & Jell (1983), Smith & Arbizu (1987), Guensburg (1988), Sumrall (1993, 2010), Sumrall & Zamora (2011), Sumrall et al. (2013), Sumrall & Gahn (2006), and Zamora et al. (2022) — simply cites the names without an alternate year (their printed form matches the record's default authority of Foerste 1916).
> 
> So within this corpus the standard attribution running through nearly every paper from 1935 to 2022 is Foerste 1916, and the only source that prints "1917" for either genus is Guensburg & Sprinkle (1994).

### q036 (trajectory)

Q: At what rank do the sources treat Edrioblastoidea: a class, an order, or a suborder?

- mechanical: answer does not cite Smith & Jell 1990
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '1990_smith.a.b_jell', 'subject': 'astrocystitidae', 'parent': 'edrioblastoida'}
- note: did not retrieve a claim matching {'kind': 'usage', 'source': '2020_ewin_martin.m_isotalo_zamora', 'subject': 'edrioblastoidina', 'printed': {'citedAs': 'Suborder Edrioblastoidina Fay, 1962'}}
- judge grounded 0: Asserts no source uses order rank, which the corpus contradicts (Smith & Jell 1990; Jell & Sprinkle 2021), and adds unverifiable class-rank chain.
- judge complete 1: Present-position count and six author sets are right, but the order-rank dissent and Sumrall's overlap are missing.
- judge contract 1: Leads with present then history as required, but delivers a verdict-like claim that the suborder position stands unopposed.

> The corpus shows a clear shift from class rank to suborder rank, with the suborder position now standing unopposed.
> 
> **Measured present:** Since 1994 six papers, from six sets of authors (Guensburg & Sprinkle 1994; Grigo 2000; Sumrall, Heredia, Rodríguez & Mestre 2013; Sprinkle & Sumrall 2015; Briggs, Siveter, Siveter, Sutton & Rahman 2017; Ewin, Martin, Isotalo & Zamora 2020 — note the overlap of Sprinkle between the 1994 and 2015 papers), have all placed the taxon as a **suborder**, under the order Edrioasterida, using the corrected spelling **Edrioblastoidina**. Ewin et al. (2020, p. 118) cite it explicitly as "Suborder Edrioblastoidina Fay, 1962."
> 
> **History:** The name originated as **Fay 1962**'s new class-rank taxon Edrioblastoidea. It was carried at class rank, under various superior taxa, by Fell (1965, under Crinozoa), Fay (1967, under Crinozoa), Ubaghs (1967, under Crinozoa), Webby (1968, under Pelmatozoa), Mintz (1970, under Crinozoa), Sprinkle (1973, who explicitly moved it from Crinozoa to Echinozoa), and finally Sprinkle (1982, retained under Echinozoa) — the last paper in the corpus to hold class rank. Bell (1980) cites the name, but no placement statement for that paper has been entered, so its treatment of rank cannot be reported.
> 
> The rank change came with **Guensburg & Sprinkle (1994)**, who emended the taxon and treated "Edrioblastoidina" as a *nomen translatum* of Edrioblastoidea at suborder rank, placed within Edrioasterida — the position every subsequent source in the corpus (Grigo 2000 through Ewin et al. 2020) has followed.
> 
> No source in the corpus treats Edrioblastoidea/Edrioblastoidina at the intermediate rank of "order."

### q037 (uncaptured)

Q: What does Whiteaves (1897) print as the original type-species designation for Astrocystites?

- judge complete 1: Names the gap for Whiteaves 1897 but omits that later papers, Fay 1962 included, treat ottawaensis as type by monotypy.
- judge contract 1: Leaks internal state language — claims "listed as not yet derived" and the source "marked as not entered" — though the gap is otherwise framed as ongoing work.

> The 1897 paper itself is on record in the corpus (Whiteaves, "Description of a new genus and species of cystideans from the Trenton limestone at Ottawa," Canadian Record of Science 7(5): 287–292, 1897), but its content has not been entered: the paper's claims of every kind, including any type-species designation for *Astrocystites*, are listed as not yet derived, and the source itself is marked as not entered.
> 
> Consequently no statement attributed directly to Whiteaves (1897) about the type species of *Astrocystites* is available in the corpus. What can be reported instead is what later sources say about that original designation: Webby (1968:513–514), citing the genus as "Astrocystites Whiteaves 1897 (= Steganoblastus Whiteaves 1898)," notes that "Bather raised objections to Whiteaves's generic name on the grounds of possible confusion with Asterocystis Haeckel, and suggested that Whiteaves substitute the name Steganoblastus. The new generic name was introduced by Whiteaves (1898)" — but this is Webby's account of the naming history, not a transcription of Whiteaves's own 1897 type designation, which remains work still to be entered from the original paper.

### q038 (absent)

Q: What does Klug et al. (2008) themselves print in their protologue for Rhenopyrgus flos?

- judge contract 1: Correctly names the gap as unentered rather than absent from the paper, but leaks internal storage language with "under this record".

> The corpus does not contain any statements from Klug et al. (2008) themselves for *Rhenopyrgus flos* — the only two sources carrying claims about this species are Sumrall et al. (2013) and Ewin et al. (2020), both simply citing/placing the species under *Rhenopyrgus* as later usages. The Klug et al. (2008) publication itself, in which the species was presumably established, has not been entered into the corpus under this record, so no protologue content (diagnosis, material, type designation, etc.) attributed to Klug et al. (2008) is available here. This is a gap in what has been entered rather than an indication that the original paper lacks such content.

### q039 (absent)

Q: What placement does the record give for the genus Rhenoblastus among the edrioblastoids?

- judge contract 1: Correct absent-class framing, but 'resolving the name returned no matching record' leaks lookup mechanism and record-as-storage language.

> No source in this corpus carries the name "Rhenoblastus." That is a fact about the corpus's coverage, not a claim about the literature—resolving the name returned no matching record at all, so I cannot report any placement for it among the edrioblastoids.

### q040 (absent)

Q: How does Richter (1930) himself classify Pyrgocystis octogona?

- judge complete 1: States the unrecoverability and the Bassler/Dehm placements but omits the later Rhenopyrgus/Pyrgocystis dispute placements of octogona.
- judge contract 1: Gap is framed as data not yet entered, but "the source is marked as not entered at all" leaks internal state language.

> Richter's 1930 paper (Senckenbergiana 12: 279–304) is on record in the corpus as the original description of *Pyrgocystis octogona*, but its content has not yet been entered — the source is marked as not entered at all. So I cannot report from the corpus how Richter himself classified the species; no usage, placement, or other statement attributed directly to Richter (1930) has been entered.
> 
> What the corpus does hold are later citations of Richter's species: Bassler (1935) places *octogona* as a species under *Pyrgocystis*, and Dehm (1961, citing Richter 1930, p. 294, fig. 1h) likewise places it as a species under *Pyrgocystis*, with an occurrence recorded from Bornich, near Weisel on the Rhine, Germany, in Lower Devonian greywacke slates. Neither of these substitutes for Richter's own classification, which remains unentered.

### q041 (trajectory)

Q: Which papers in the corpus treat edrioblastoids, and what does each do to the group (erect, emend, re-rank, move, add a genus)?

- mechanical: answer does not cite Bather 1900
- mechanical: answer does not cite Bassler 1935
- mechanical: answer does not cite Bassler 1936
- mechanical: answer does not cite Holloway & Jell 1983
- mechanical: answer does not cite Smith & Jell 1990
- mechanical: answer does not cite Jell & Sprinkle 2021
- note: did not retrieve a claim matching {'kind': 'act', 'source': '1900_bather', 'actKind': 'new', 'subject': 'steganoblastidae'}
- note: did not retrieve a claim matching {'kind': 'act', 'source': '1935_bassler', 'actKind': 'new', 'subject': 'astrocystitidae'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '1936_bassler', 'subject': 'astrocystites', 'parent': 'protoblastoidea'}
- note: did not retrieve a claim matching {'kind': 'act', 'source': '1968_webby', 'actKind': 'new', 'subject': 'distans_webby_1968'}
- note: did not retrieve a claim matching {'kind': 'act', 'source': '1983_holloway_jell', 'actKind': 'new', 'subject': 'rhenopyrgidae'}
- note: did not retrieve a claim matching {'kind': 'act', 'source': '1990_smith.a.b_jell', 'actKind': 'new', 'subject': 'cambroblastus'}
- note: did not retrieve a claim matching {'kind': 'act', 'source': '1994_guensburg_sprinkle', 'actKind': 'nomTransl', 'subject': 'rhenopyrginae', 'altRankOf': 'rhenopyrgidae'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '2000_grigo', 'subject': 'rhenopyrginae', 'parent': 'cyathocystidae'}
- note: did not retrieve a claim matching {'kind': 'act', 'source': '2013_sumrall_heredia_rodríguez.c.m_mestre', 'actKind': 'emended', 'subject': 'rhenopyrgidae'}
- note: did not retrieve a claim matching {'kind': 'act', 'source': '2015_sprinkle_sumrall', 'actKind': 'new', 'subject': 'porosublastus'}
- note: did not retrieve a claim matching {'kind': 'act', 'source': '2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman', 'actKind': 'new', 'subject': 'heropyrgus'}
- note: did not retrieve a claim matching {'kind': 'act', 'source': '2020_ewin_martin.m_isotalo_zamora', 'actKind': 'emended', 'subject': 'rhenopyrgidae'}
- note: did not retrieve a claim matching {'kind': 'act', 'source': '2021_jell_sprinkle', 'actKind': 'new', 'subject': 'ikerus'}
- judge grounded 0: Asserts Fell 1965, Ubaghs 1967, Webby under Pelmatozoa, a Sprinkle 1973 move, and denies any genus additions, all contradicted.
- judge complete 0: Omits Bather, Bassler, Dehm, Regnéll, Holloway & Jell, Smith & Jell, and every genus addition and Rhenopyrgidae act.
- judge contract 0: Repeatedly speaks of "records", "the corpus's later record", and "no act has been entered" as a finished judgement.

> The corpus tracks this group under two linked records: **Edrioblastoidea** (class rank) and, from 1994 on, **Edrioblastoidina** (suborder rank, a nomen translatum of the same name).
> 
> **Present position.** Since 1994 the group has been carried as the suborder Edrioblastoidina, nested in Edrioasterida, in six papers spanning 1994–2020 from six partly overlapping author sets: Guensburg & Sprinkle (1994), Grigo (2000), Sumrall, Heredia, Rodríguez & Mestre (2013), Sprinkle & Sumrall (2015), Briggs, Siveter, Siveter, Sutton & Rahman (2017), and Ewin, Martin, Isotalo & Zamora (2020, who cite it explicitly as "Suborder Edrioblastoidina Fay, 1962," p. 118). J. Sprinkle recurs across the 1994 and 2015 papers, and C. Sumrall across the 2013, 2015 and (as reviewer of the corpus's later record) 2020 lineage, so the six papers are not fully independent co-author sets, but each states the same suborder placement under Edrioasterida.
> 
> **History of the earlier, class-rank position.** Fay (1962) erected the class Edrioblastoidea (a "new" act). It was then simply placed, at class rank, by successive authors: Fell (1965) and Fay (1967) and Ubaghs (1967) all place it under Crinozoa; Webby (1968) places it instead under Pelmatozoa; Mintz (1970) again under Crinozoa. Sprinkle (1973) explicitly moves the class, recording an act of moving it from Crinozoa to Echinozoa. Bell (1980) cites the name Edrioblastoidea, but no placement or act for that citation has been entered for his paper. Sprinkle (1982) continues the class under Echinozoa, the last paper in the corpus to carry it at class rank.
> 
> **The re-ranking.** Guensburg & Sprinkle (1994) convert the class into the suborder Edrioblastoidina, recording this both as a nomen translatum of Edrioblastoidea and as an emendation, and placing the new suborder under Edrioasterida. Every subsequent paper in the corpus (Grigo 2000; Sumrall et al. 2013; Sprinkle & Sumrall 2015; Briggs et al. 2017; Ewin et al. 2020) simply repeats this suborder placement under Edrioasterida.
> 
> No statement among those entered for either record shows a paper adding a genus to the group; the acts recorded are limited to Fay's original erection, Sprinkle's 1973 move, and Guensburg & Sprinkle's 1994 emendation/rank-translation.

### q042 (trajectory)

Q: What genera and species have ever been classified as edrioblastoids by any definition, and which of those placements were later abandoned by some sources?

- note: did not retrieve a claim matching {'kind': 'placement', 'source': '1994_guensburg_sprinkle', 'subject': 'cambroblastus', 'parent': 'astrocystitidae'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '1994_guensburg_sprinkle', 'subject': 'lampteroblastus', 'parent': 'astrocystitidae'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '2015_sprinkle_sumrall', 'subject': 'porosublastus', 'parent': 'astrocystitidae'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '2021_jell_sprinkle', 'subject': 'ikerus', 'parent': 'edrioblastoida'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '1994_guensburg_sprinkle', 'subject': 'rhenopyrgus', 'parent': 'rhenopyrginae'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '2000_grigo', 'subject': 'rhenopyrgus', 'parent': 'rhenopyrginae'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '2013_sumrall_heredia_rodríguez.c.m_mestre', 'subject': 'rhenopyrgus', 'parent': 'rhenopyrgidae'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman', 'subject': 'heropyrgus', 'parent': 'rhenopyrgidae'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '1994_guensburg_sprinkle', 'subject': 'cyathocystis', 'parent': 'cyathocystinae'}
- note: answered after the lookup limit was reached
- judge grounded 0: Asserts Astrocystites is the only genus ever placed in edrioblastoid taxa, which the corpus contradicts (Cambroblastus, Rhenopyrgus, Ikerus, etc.).
- judge complete 0: Misses seven of eight genera and their species, plus the Cyathocystidae/Rhenopyrginae abandonment; only the class-rank history matches.
- judge contract 1: Structure, citation and verdict-free tone are largely right, but it opens with a taxon list rather than the measured present.

> ## The genus and species classified as edrioblastoids
> 
> Across the corpus, exactly one genus has ever been carried inside the "edrioblastoid" concept, at whatever rank it has been given (class Edrioblastoidea, order Edrioblastoida, or suborder Edrioblastoidina): **Astrocystites** Whiteaves, 1897, with its type species **Astrocystites ottawaensis** (Whiteaves, 1897), fixed as type in every source that states a type (Fay 1962, p. 201/205 — an inferred type‑fixation, since Fay never prints "type species" but the genus is monotypic; Fay 1967; Webby 1968, p. 513; Mintz 1970; Sprinkle 1982; Smith & Jell 1990). The genus name **Steganoblastus** Whiteaves, 1898 is carried throughout as a junior objective synonym of Astrocystites (Bassler 1935; Fay 1962; Fay 1967; Webby 1968, p. 513, citing Whiteaves 1898:395; Mintz 1970).
> 
> The family housing it has been printed under two competing names: **Astrocystitidae** Bassler, 1935 (a replacement name, per Bassler's own heading) and **Steganoblastidae** Bather, 1900. Webby (1968, p. 514) argued that Steganoblastidae has priority as based on a senior name and "would seem desirable that it be retained," a stance he treated as an acceptance, and Sprinkle (1982) followed him in using Steganoblastidae; but Bassler (1935), Fay (1967), Mintz (1970), Bell (1980), Smith & Jell (1990), and Guensburg & Sprinkle (1994) all use Astrocystitidae instead, so Webby's reversal was not carried forward by the later sources on record.
> 
> ## The measured present
> 
> The current, most‑followed placement is as suborder **Edrioblastoidina** (a nomen translatum of Edrioblastoidea, per Guensburg & Sprinkle 1994) under order Edrioasterida, itself under class Edrioasteroidea. This position is held by six papers spanning 1994–2020 from largely distinct co-author sets: Guensburg & Sprinkle 1994, Grigo 2000, Sumrall, Heredia, Rodríguez & Mestre 2013, Sprinkle & Sumrall 2015, Briggs, Siveter, Siveter, Sutton & Rahman 2017, and Ewin, Martin, Isotalo & Zamora 2020 (the last citing it as "Suborder Edrioblastoidina Fay, 1962," p. 118). Sprinkle and Sumrall each recur across some of these papers, an author-overlap worth noting rather than treating as independent corroboration.
> 
> Running in parallel, a second current usage keeps the group at ordinal rank, as **Edrioblastoida**, likewise nested in class Edrioasteroidea rather than as its own class: Smith & Jell 1990, Zhu, Zamora & Lefebvre 2014, and Jell & Sprinkle 2021 (Jell recurs across the first and last of these).
> 
> Within both of these still-current schemes, the genus Astrocystites remains lodged in family Astrocystitidae (Guensburg & Sprinkle 1994; Smith & Jell 1990), and the species ottawaensis remains its type.
> 
> ## The history and what was abandoned
> 
> Before any "edrioblastoid" taxon existed, Bassler (1935) placed Astrocystitidae/Astrocystites under class Edrioasteroidea (with an alternative placement under Blastoidea noted), and Bassler (1936) then provisionally moved Astrocystites to class Protoblastoidea. Neither placement is continued in the corpus after 1936.
> 
> **Fay (1962)** created class Edrioblastoidea expressly to receive Astrocystites, recording the act as a move out of Edrioasteroidea. From 1962 to 1982, Edrioblastoidea was carried as an independent class by seven further papers from distinct co-author sets — Fell 1965, Fay 1967, Ubaghs 1967, Webby 1968, Mintz 1970, Sprinkle 1973, Bell 1980, and Sprinkle 1982 — though they disagreed on what superior taxon it sat under: Crinozoa (Fell 1965; Fay 1967; Ubaghs 1967; Mintz 1970), Pelmatozoa (Webby 1968), or Echinozoa, the last following an explicit move by Sprinkle (1973) out of Crinozoa, continued by Sprinkle 1982.
> 
> That independent-class status was abandoned starting with **Smith & Jell (1990)**, who demoted it to order Edrioblastoida and folded it back into class Edrioasteroidea — reversing Fay's 1962 removal of the group from that class. **Guensburg & Sprinkle (1994)** went further, emending it and treating it as a nomen translatum at suborder rank, Edrioblastoidina, under order Edrioasterida within Edrioasteroidea; this suborder-rank placement is the one carried by Grigo 2000, Sumrall et al. 2013, Sprinkle & Sumrall 2015, Briggs et al. 2017, and Ewin et al. 2020, as noted above. The competing order-rank treatment (Edrioblastoida, following Smith & Jell 1990) was not abandoned outright, however: it persists in Zhu, Zamora & Lefebvre 2014 and Jell & Sprinkle 2021.
> 
> At a finer level, Fay (1967) and Sprinkle (1982) interposed an order **Pentacystida** (Jaekel, 1918) between Edrioblastoidea and the family; this ordinal placement is not continued by Mintz 1970, Bell 1980, Smith & Jell 1990, or Guensburg & Sprinkle 1994, all of which place the family directly under the class/order/suborder without that intermediate rank — so Pentacystida as a home for this material was not carried forward.
> 
> No other genus or species is recorded in the corpus as ever having been placed within Edrioblastoidea, Edrioblastoida, or Edrioblastoidina under any of these definitions.

### q043 (trajectory)

Q: At what rank has the edrioblastoid group been treated, and by which co-author sets, over time?

- mechanical: answer does not cite Smith & Jell 1990
- mechanical: answer does not cite Zhu et al. 2014
- mechanical: answer does not cite Jell & Sprinkle 2021
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '1990_smith.a.b_jell', 'subject': 'astrocystitidae', 'parent': 'edrioblastoida'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '2014_zhu.x.j_zamora_lefebvre', 'subject': 'cambroblastus', 'parent': 'edrioblastoida'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '2021_jell_sprinkle', 'subject': 'ikerus', 'parent': 'edrioblastoida'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '2000_grigo', 'subject': 'cyathocystidae', 'parent': 'edrioblastoidina'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '2013_sumrall_heredia_rodríguez.c.m_mestre', 'subject': 'rhenopyrgidae', 'parent': 'edrioblastoidina'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '2015_sprinkle_sumrall', 'subject': 'astrocystitidae', 'parent': 'edrioblastoidina'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman', 'subject': 'rhenopyrgidae', 'parent': 'edrioblastoidina'}
- judge grounded 0: Adds Fell 1965, Ubaghs 1967a, Sprinkle 1973, Bell 1980 and Edrioasterida placement not supported, and denies post-1994 non-suborder usage.
- judge complete 1: The suborder set is right, but the entire order-rank convention (Smith & Jell 1990, Zhu et al. 2014, Jell & Sprinkle 2021) is missing.
- judge contract 0: Leads with history rather than the measured present, asserts a 'clear break' verdict, and uses record/entered storage language.

> The edrioblastoidean group has been treated at two different ranks in the corpus, with a clear break between the earlier and later literature.
> 
> **As a class, "Edrioblastoidea" (1962–1982).**
> Fay 1962 established the class-rank name (a "new" act on the record Edrioblastoidea). It was carried at class rank, in each case placed under a parent superclass, by:
> - Fell 1965, under Crinozoa;
> - Fay 1967a, under Crinozoa;
> - Ubaghs 1967a, under Crinozoa;
> - Webby 1968, under Pelmatozoa;
> - Mintz 1970, under Crinozoa;
> - Sprinkle 1973, who moved it from Crinozoa to Echinozoa, still at class rank;
> - Sprinkle 1982, again under Echinozoa.
> Bell 1980 also cites the name, but only a bare usage has been entered for that paper, with no rank or placement recorded.
> 
> That gives seven distinct co-author sets (Fay, Fell, Ubaghs, Webby, Mintz, Sprinkle, Bell) holding class rank across 1962–1982, Fay's papers and Sprinkle's papers each appearing twice.
> 
> **As a suborder, "Edrioblastoidina" (1994–present).**
> Guensburg & Sprinkle 1994 emended the group and explicitly treated it as a nomen translatum from Fay's class-rank Edrioblastoidea, reducing it to the suborder Edrioblastoidina and placing it within the order Edrioasterida. Every subsequent paper in the corpus that carries the name follows this suborder-rank placement under Edrioasterida:
> - Grigo 2000;
> - Sumrall, Heredia, Rodríguez & Mestre 2013;
> - Sprinkle & Sumrall 2015;
> - Briggs, Siveter, Siveter, Sutton & Rahman 2017;
> - Ewin, Martin, Isotalo & Zamora 2020, who cite it explicitly as "Suborder Edrioblastoidina Fay, 1962" (p. 118).
> 
> That is the measured present: six papers spanning 1994–2020, from six distinct co-author sets, all holding the suborder-rank Edrioblastoidina nested in Edrioasterida, with no source in the corpus reverting to class rank after 1994.

### q044 (trajectory)

Q: Which family name has been used for Astrocystites and by whom, Steganoblastidae or Astrocystitidae?

- mechanical: answer does not cite Bather 1900
- mechanical: answer does not cite Sprinkle & Sumrall 2015
- note: did not retrieve a claim matching {'kind': 'act', 'source': '1900_bather', 'actKind': 'new', 'subject': 'steganoblastidae'}
- note: did not retrieve a claim matching {'kind': 'act', 'source': '1935_bassler', 'actKind': 'new', 'subject': 'astrocystitidae'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '2015_sprinkle_sumrall', 'subject': 'porosublastus', 'parent': 'astrocystitidae'}
- judge grounded 1: Core usages match, but several added placements (Bassler 1936, Fay 1962, Sprinkle 1973, the 'lloydi' timeline) are embellishments beyond the expected support.
- judge complete 1: Omits Bather (1900) erecting Steganoblastidae and Sprinkle & Sumrall (2015), plus Bassler's priority rationale and Webby's Art. 40 argument.
- judge contract 1: Does not lead with the measured present as counts over years and distinct co-author sets, though it otherwise avoids verdicts and mechanism talk.

> Both family names appear in the corpus for *Astrocystites* Whiteaves, 1897, used at different times by different authors:
> 
> **Astrocystitidae** — the majority usage. It is used by Bassler (1935), Fay (1967), Mintz (1970), Bell (1980), Smith & Jell (1990), and Guensburg & Sprinkle (1994).
> 
> **Steganoblastidae** — used by Webby (1968, p. 513), who explicitly notes the nomenclatural background: "In the same year Bather raised objections to Whiteaves's generic name on the grounds of possible confusion with Asterocystis Haeckel, and suggested that Whiteaves substitute the name Steganoblastus. The new generic name was introduced by Whiteaves (1898)" (Webby 1968, p. 514). Sprinkle (1982) likewise places the genus under Steganoblastidae.
> 
> In between, Bassler (1936) placed the genus provisionally in Protoblastoidea rather than either family, Fay (1962) and Sprinkle (1973) placed it in Edrioblastoidea, and Smith & Jell (1990) also show it on an evolutionary-timeline diagram under "lloydi" (Sprinkle, 1985) in addition to their taxonomic placement in Astrocystitidae. So across the corpus, Astrocystitidae is the more frequently used family assignment, with Steganoblastidae employed specifically by Webby (1968) and Sprinkle (1982).

### q045 (trajectory)

Q: Who proposed placing rhenopyrgids inside Cyathocystidae, who followed, and who rejected it?

- judge grounded 0: Asserts no rejection is recorded, contradicting the corpus's explicit Sumrall et al. (2013) rejection quotation and reasoning.
- judge complete 1: Proposer and follower correct, but the stated 2013 rejection—the heart of the question—is denied rather than reported.
- judge contract 0: Leaks storage language ("recorded", "entered", "the record shows") and does not lead with the measured present or count co-author sets.

> Placing the rhenopyrgids inside Cyathocystidae is a step taken by only one source in the corpus: Guensburg & Sprinkle (1994), who erected the subfamily Rhenopyrginae as an emended nomen translatum of Holloway & Jell's (1983) family Rhenopyrgidae and placed it as a subfamily under Cyathocystidae (itself then set within Edrioblastoidina).
> 
> That placement was followed once more, by Grigo (2000), who likewise carries Rhenopyrginae as a subfamily of Cyathocystidae.
> 
> No source in the corpus is recorded as explicitly rejecting the placement in Cyathocystidae — there is no statement of that kind entered for either Rhenopyrgidae or Cyathocystidae. What the record shows instead is later authors simply placing the family elsewhere without addressing Guensburg & Sprinkle's arrangement: Müller & Hahn (2010) list Rhenopyrgidae as a family of Isorophida, while Sumrall, Heredia Rodríguez & Mestre (2013), Briggs et al. (2017), and Ewin, Martin, Isotalo & Zamora (2020) each place an emended Rhenopyrgidae as a family within Edrioblastoidina, independent of Cyathocystidae. So the corpus documents a move away from the 1994/2000 subfamily-of-Cyathocystidae position, but not a stated rejection of it.

### q046 (trajectory)

Q: Has any single author appeared in papers holding different ranks for the edrioblastoid group?

- mechanical: answer does not cite Smith & Jell 1990
- mechanical: answer does not cite Jell & Sprinkle 2021
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '1982i_sprinkle', 'subject': 'astrocystites', 'parent': 'steganoblastidae'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '2015_sprinkle_sumrall', 'subject': 'astrocystitidae', 'parent': 'edrioblastoidina'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '2021_jell_sprinkle', 'subject': 'ikerus', 'parent': 'edrioblastoida'}
- note: did not retrieve a claim matching {'kind': 'placement', 'source': '1990_smith.a.b_jell', 'subject': 'astrocystitidae', 'parent': 'edrioblastoida'}
- judge grounded 0: Cites many sources (Fay 1962, Fell 1965, Ubaghs 1967, Grigo 2000, Ewin et al. 2020) the corpus does not hold.
- judge complete 1: Identifies Sprinkle and the 1982/1994/2015 papers but omits the order rank, Jell & Sprinkle 2021, and Jell's two order-rank papers.
- judge contract 1: No measured present or co-author-set counts, and it attributes positions to Sprinkle personally rather than to the papers.

> Yes. James Sprinkle is the one author who recurs across the two rank treatments of this taxon.
> 
> **Class-rank treatment (as "Edrioblastoidea," within Crinozoa then Echinozoa):**
> - Fay 1962 (erecting the class)
> - Fell 1965, Fay 1967, Ubaghs 1967, Webby 1968, Mintz 1970 (all under Crinozoa, or Pelmatozoa for Webby)
> - Sprinkle 1973, who moves it from Crinozoa to Echinozoa but keeps it at class rank
> - Sprinkle 1982, again as a class within Echinozoa
> 
> **Suborder-rank treatment (as "Edrioblastoidina," a nomen translatum within Edrioasterida):**
> - Guensburg & Sprinkle 1994, who perform the nomen translatum, emending the taxon and placing it as a suborder of Edrioasterida
> - Grigo 2000, Sumrall et al. 2013, Sprinkle & Sumrall 2015, Briggs et al. 2017, and Ewin et al. 2020 (the last citing it as "Suborder Edrioblastoidina Fay, 1962," p. 118) all continue the suborder placement
> 
> Sprinkle is the sole author present on both sides of this rank change: he holds the class-rank position solo in 1973 and 1982, then co-authors the suborder-rank nomen translatum with Guensburg in 1994 and again places it as a suborder with Sumrall in 2015. No other author in the corpus appears under both rank treatments.

### q047 (trajectory)

Q: Which taxon in the edrioblastoid group has the most distinct placements across sources?

- judge grounded 0: Asserts placements and sources (Pentacystida, Bell 1980, Webby 1968, Steganoblastidae parentage, Ewin 2020) the expected answer contradicts or does not support.
- judge complete 0: Identifies the wrong taxon (family rather than Astrocystites), miscounts its placements, and omits the Rhenopyrgus comparison entirely.
- judge contract 1: Does not lead with the measured present and refers to "the taxonomic-classification tree" rather than plain literature language.

> Within the edrioblastoid group, the family **Astrocystitidae** Bassler, 1935 is the taxon whose placement has moved most often across the sources in the corpus.
> 
> Its parent taxon changes five times over seven citing sources spanning 1935–2015:
> 
> - **Edrioasteroidea** – Bassler 1935 (a provisional placement, alongside a note that the family name is meant to correct/replace "Steganoblastidae")
> - **Pentacystida** – Fay 1967
> - **Edrioblastoidea** – Mintz 1970 and again Bell 1980
> - **Edrioblastoida** – Smith & Jell 1990
> - **Edrioblastoidina** – Guensburg & Sprinkle 1994 (an emendation, on the taxonomic-classification tree; the same paper's four cladograms instead show it nested in Edrioasteroidea) and again Sprinkle & Sumrall 2015
> 
> By comparison, the genus it contains, **Astrocystites** Whiteaves, 1897, shows four distinct parents across its own history in the corpus — Astrocystitidae (Bassler 1935, Fay 1967, Mintz 1970, Bell 1980, Smith & Jell 1990, Guensburg & Sprinkle 1994), Protoblastoidea (Bassler 1936, provisional), Edrioblastoidea (Fay 1962, Sprinkle 1973), and Steganoblastidae (Webby 1968, Sprinkle 1982) — and the class-level name **Edrioblastoidea**/its suborder-rank counterpart **Edrioblastoidina** shows four as well (Crinozoa: Fell 1965, Fay 1967, Ubaghs 1967, Mintz 1970; Pelmatozoa: Webby 1968; Echinozoa: Sprinkle 1973, 1982; Edrioasterida, at suborder rank: Guensburg & Sprinkle 1994 onward through Ewin et al. 2020). The related family **Steganoblastidae** Bather, 1900 shows only three (Edrioasteroidea, Bather 1900; Edrioblastoidea, Webby 1968; Pentacystida, Sprinkle 1982).
> 
> So among the names carried in the corpus for the edrioblastoid group, Astrocystitidae is the one credited with the most distinct placements.

### q048 (trajectory)

Q: What did Holloway & Jell (1983) say Dehm (1961) did with Pyrgocystis octogona, and what does Dehm's own paper do?

- note: answered after the lookup limit was reached
- judge grounded 1: Dehm's placement is well grounded, but the claim that no Holloway & Jell statement on this name is entered contradicts the corpus.
- judge complete 1: Dehm's retention in Pyrgocystis is given, but the Holloway & Jell quote 'assigned to Rhenopyrgus by Dehm (1961)' (p. 1004) and the conflict are missing.
- judge contract 1: Gaps are phrased as not-yet-entered, but 'usage record', 'the record for', and 'no usage, placement, acceptance, or rejection claim' leak internal mechanism language.

> Based on what the corpus has entered so far, I can report on Dehm's own paper directly, but not yet on what Holloway & Jell (1983) said about Dehm's treatment of *Pyrgocystis octogona*.
> 
> **Dehm (1961):** The source's own usage record places *Pyrgocystis octogona* (originally described by Richter 1930) as a species within the genus *Pyrgocystis*, citing Richter 1930 at page 294 and figure 1h. Dehm also records material for this species from Bornich, near Weisel on the Rhine, Germany, in Lower Devonian greywacke slates. So Dehm (1961) retains the species under Bather's genus *Pyrgocystis*, following Richter's original figured material.
> 
> **Holloway & Jell (1983):** The corpus does not yet have any statement entered against the record for *Pyrgocystis octogona* itself from this source — no usage, placement, acceptance, or rejection claim tied to that name appears among what has been entered for Holloway & Jell (1983). Holloway & Jell (1983) is on record in the corpus (their paper on Silurian and Devonian edrioasteroids from Australia, *Journal of Paleontology* 57(5): 1001–1016), and its synonymy statements are declared as only partly entered. Given that gap, any remark that paper may make specifically about what Dehm (1961) did with *P. octogona* has not yet been entered for this source, so I cannot report it.

