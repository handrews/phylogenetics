# Grades for `2026-09-14-claude-sonnet-5.jsonl`

| class | questions | mechanical pass |
|---|---|---|
| absent | 3 | 3 |
| answerable | 12 | 6 |
| as-published | 8 | 5 |
| trajectory | 17 | 8 |
| uncaptured | 9 | 4 |

## Failures and notes

### q001 (answerable)

Q: What new class does Fay (1962) erect for the genus Astrocystites, and what family/order sit between the genus and the class?

- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1962_fay', 'actKind': 'new', 'subject': 'edrioblastoidea'}
- note: page 201 not among the composed claims
- judge contract 1: Parameters (record, tree, no synonyms, year) stated correctly, but header pre-empts the answer by announcing the new class Edrioblastoidea — one summary lapse.

Header: Fay (1962): new class Edrioblastoidea for Astrocystites; classification (taxonomy tree) only, no synonyms
- classification {"source": "1962_fay", "record": "astrocystites", "depth": null, "synonymy": false, "path": "0/children/0"}
- table {"records": ["astrocystites"], "sources": ["1962_fay"], "years": null, "includeVariants": true, "includeSynonyms": true, "trees": ["taxonomy"]}

> Fay (1962): new class Edrioblastoidea for Astrocystites; classification (taxonomy tree) only, no synonyms
> 
> Fay 1962
>   Genus Astrocystites (moved from Edrioasteroidea)
>     Type species. Astrocystites ottawaensis
>     Astrocystites ottawaensis
> 
> Placements by source
> schemes: Astrocystitidae: 6 papers (1935–1994), 6 co-author sets, last Guensburg & Sprinkle 1994; Steganoblastidae: 2 papers (1968–1982), 2 co-author sets, last Sprinkle 1982; Edrioblastoidea: 2 papers (1962–1973), 2 co-author sets, last Sprinkle 1973; Protoblastoidea: 1 paper (1936), 1 co-author set, last Bassler 1936
> record         rank   Fay 1962
> -------------  -----  ------------------------------------
> Astrocystites  genus  Edrioblastoidea; not Edrioasteroidea

### q005 (answerable)

Q: What new genus and type species do Sprinkle & Sumrall (2015) place in family Astrocystitidae?

- note: page 351 not among the composed claims
- judge contract 2: Header names only scope parameters (family, authors/year, classification-only), states no verdict or summary; question class answerable so no query needed.

Header: New taxa placed in family Astrocystitidae by Sprinkle & Sumrall (2015); classification only
- classification {"source": "2015_sprinkle_sumrall", "record": "astrocystitidae", "depth": null, "synonymy": false, "path": "0/children/0/children/1/children/0"}

> New taxa placed in family Astrocystitidae by Sprinkle & Sumrall (2015); classification only
> 
> Sprinkle & Sumrall 2015
>   Family Astrocystitidae
>     Genus Porosublastus gen. nov.
>       Type species. Porosublastus inexpectus
>       Porosublastus inexpectus sp. nov.

### q006 (answerable)

Q: What species do Sumrall, Heredia Rodríguez & Mestre (2013) confirm as the type species of Rhenopyrgus?

- failure: no composed block carries a claim matching {'kind': 'act', 'source': '2013_sumrall_heredia_rodríguez.c.m_mestre', 'actKind': 'emended', 'subject': 'rhenopyrgus'}
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '2013_sumrall_heredia_rodríguez.c.m_mestre', 'actKind': 'type', 'subject': 'coronaeformis_rievers_1961'}
- failure: no composed block carries a claim matching {'kind': 'acceptance', 'source': '2013_sumrall_heredia_rodríguez.c.m_mestre', 'stance': 'accepts', 'subject': 'coronaeformis_rievers_1961', 'parents': ['rhenopyrgus-subgenus', 'pyrgocystis']}
- note: page 773 not among the composed claims
- judge contract 1: Header names group and source year but says "confirmed", a verdict; otherwise parameter-like and no question asked.

Header: Type species of Rhenopyrgus (genus) confirmed by Sumrall et al. 2013
- list {"record": "rhenopyrgus", "source": "2013_sumrall_heredia_rodríguez.c.m_mestre", "kind": null, "actKind": "type"}

> Type species of Rhenopyrgus (genus) confirmed by Sumrall et al. 2013
> 
> Statements about Rhenopyrgus Dehm 1961

### q008 (answerable)

Q: In Holloway & Jell (1983), family Rhenopyrgidae is placed under a name that is not itself an order. What is that placeholder, and what does it mean?

- failure: free text beside the submission: This gives the classification block showing the placeholder directly.
- judge contract 2: Header lists only group, synonym/rank scope, tree type, and year; no verdict or mechanism wording; no question needed for answerable class.

Header: Placement of family Rhenopyrgidae in Holloway & Jell (1983): class Edrioasteroidea; synonyms and rank variants not included; classification (taxonomy) tree; year 1983 only.
- classification {"source": "1983_holloway_jell", "record": "edrioasteroidea", "depth": 2, "synonymy": false, "path": "0"}

> Placement of family Rhenopyrgidae in Holloway & Jell (1983): class Edrioasteroidea; synonyms and rank variants not included; classification (taxonomy) tree; year 1983 only.
> 
> Holloway & Jell 1983
>   Class Edrioasteroidea
>     Order uncertain
>       Family Rhenopyrgidae fam. nov.
>     Order Isorophida
>       Family Lebetodiscidae
>       Family Pyrgocystidae
>       Family Hemicystitidae
>       Genus uncertain

### q009 (answerable)

Q: What new species of Rhenopyrgus does Grigo (2000) describe, and from where?

- failure: page 96 not shown
- note: composed after the lookup limit was reached
- judge contract 2: Header lists only scope parameters (taxon, source, synonym exclusion, classification scope, year); no summary, mechanism, or verdict; no question needed as answerable.

Header: Rhenopyrgus (genus) as treated by Grigo (2000); no synonyms; classification only; year 2000
- classification {"source": "2000_grigo", "record": "rhenopyrgus", "depth": null, "synonymy": false, "path": "0/children/1/children/0/children/0/children/0/children/0"}

> Rhenopyrgus (genus) as treated by Grigo (2000); no synonyms; classification only; year 2000
> 
> Grigo 2000
>   Genus Rhenopyrgus
>     Type species. Rhenopyrgus coronaeformis
>     Rhenopyrgus coronaeformis
>     Rhenopyrgus sp. sp. nov.

### q010 (answerable)

Q: What is the holotype specimen number for Rhenopyrgus viviani, named by Ewin, Martin, Isotalo & Zamora (2020)?

- failure: no composed block carries a claim matching {'kind': 'act', 'source': '2020_ewin_martin.m_isotalo_zamora', 'actKind': 'new', 'subject': 'viviani_ewin_martin.m_isotalo_zamora_2020'}
- judge contract 2: Header names only the taxon, the datum sought, and the source; no verdict, summary, or mechanism wording; no needless question asked.

Header: Holotype of Rhenopyrgus viviani Ewin, Martin, Isotalo & Zamora, 2020, as stated in that source
- list {"record": "viviani_ewin_martin.m_isotalo_zamora_2020", "source": null, "kind": "material", "actKind": null}

> Holotype of Rhenopyrgus viviani Ewin, Martin, Isotalo & Zamora, 2020, as stated in that source
> 
> Statements about Rhenopyrgus viviani Ewin et al. 2020
>   2020  Ewin et al.  occurrence: Telychian; Cybèle Member, Jupiter Formation; Rock Pool Ledge, Jupiter River Section, Anticosti Island, Québec, Canada (pp. 120–122)
>   2020  Ewin et al.  holotypes: NHMUK EE16642 (pp. 120–122)
>   2020  Ewin et al.  paratypes: NHMUK EE15752, EE15755 (pp. 120–122)
>   2020  Ewin et al.  paratypes: MPEP 1126.1 (pp. 120–122)
>   2020  Ewin et al.  occurrence: Telychian; Pavillon Member, Jupiter Formation; Pavillon River Section, Anticosti Island, Québec, Canada (pp. 120–122)
>   2020  Ewin et al.  paratypes: NHMUK EE15756 (pp. 120–122)
>   2020  Ewin et al.  occurrence (pp. 120–122)
>   2020  Ewin et al.  unspecified: MPEP 1143.1 (pp. 120–122)
>   2020  Ewin et al.  illustration: fig. 2, 4–5 (pp. 120–122)

### q011 (answerable)

Q: What is the holotype specimen number for Rhenopyrgus grayae, per Ewin et al. (2020)?

- note: page 122 not among the composed claims
- judge contract 2: Header names only taxon, authority, and source citation; no summary, mechanism, or verdict, and no question needed for this answerable query.

Header: Holotype specimen of Rhenopyrgus grayae (Bather 1915), as stated by Ewin et al. (2020)
- list {"record": "grayae_bather_1915", "source": "2020_ewin_martin.m_isotalo_zamora", "kind": "material", "actKind": null}

> Holotype specimen of Rhenopyrgus grayae (Bather 1915), as stated by Ewin et al. (2020)
> 
> Statements about Pyrgocystis grayae Bather 1915
>   2020  Ewin et al.  Rhenopyrgus grayae: occurrence: Katian; Upper Ordovician; Farden Member, South Threave Formation, Drummuck Group; Lady Burn Starfish Bed, part of the Craighead inlier., Lady Burn, near Girvan, Scotland, UK (p. 118)
>   2020  Ewin et al.  Rhenopyrgus grayae: holotypes: NHMUK E23470 (p. 118)
>   2020  Ewin et al.  Rhenopyrgus grayae: unspecified: NHMUK E23674, E29570 (p. 118)

### q012 (answerable)

Q: Which two genera does Ewin et al. (2020) list under the emended family Rhenopyrgidae?

- failure: page 118 not shown
- judge contract 2: Header names only scope (Rhenopyrgidae genera, Ewin et al. 2020 classification) in community language, no verdict or summary; no question needed.

Header: Genera listed under the emended family Rhenopyrgidae in Ewin et al. (2020)'s classification
- classification {"source": "2020_ewin_martin.m_isotalo_zamora", "record": "rhenopyrgidae", "depth": null, "synonymy": false, "path": "0/children/0/children/0/children/0/children/0"}

> Genera listed under the emended family Rhenopyrgidae in Ewin et al. (2020)'s classification
> 
> Ewin et al. 2020
>   Family Rhenopyrgidae emend.
>     Genus Rhenopyrgus emend.
>       Type species. Rhenopyrgus coronaeformis
>       Rhenopyrgus coronaeformis
>       Rhenopyrgus grayae
>       Rhenopyrgus whitei
>       Rhenopyrgus flos
>       Rhenopyrgus piojoensis
>       Rhenopyrgus viviani sp. nov.
>       Rhenopyrgus sp. indet. 1
>       Rhenopyrgus sp. indet. 2
>       Rhenopyrgus sp. indet. 3
>       Rhenopyrgus sp. indet. 4
>     Genus Heropyrgus

### q013 (uncaptured)

Q: What holotype and paratype specimen numbers does Holloway & Jell (1983) give for Rhenopyrgus whitei?

- failure: no gap block for 1983_holloway_jell / material
- note: page 1004 not among the composed claims
- judge contract 2: Header lists only scope parameters—source, taxon, rank, coverage—in community language, with no summary, mechanism term, or verdict; no question needed.

Header: Material (holotype and paratype numbers) reported by Holloway & Jell (1983) for Rhenopyrgus whitei; species-rank record only, this source only
- list {"record": "whitei_holloway_jell_1983", "source": "Holloway &amp; Jell 1983", "kind": "material", "actKind": null}

> Material (holotype and paratype numbers) reported by Holloway & Jell (1983) for Rhenopyrgus whitei; species-rank record only, this source only
> 
> Statements about Rhenopyrgus whitei Holloway & Jell 1983

### q014 (uncaptured)

Q: What occurrence data does Guensburg & Sprinkle (1994) print for the new species Lampteroblastus hintzei?

- note: text between lookups: The coverage declares occurrence data as "none" entered for this source, so I sh
- judge contract 2: Header names only the taxon, the new-species status, and the single source restriction; no summary, mechanism, or verdict; no question needed here.

Header: Occurrence data for Lampteroblastus hintzei Guensburg & Sprinkle 1994, sp. nov.; Guensburg & Sprinkle 1994 only
- statement {"source": "1994_guensburg_sprinkle", "kind": "occurrences"}

> Occurrence data for Lampteroblastus hintzei Guensburg & Sprinkle 1994, sp. nov.; Guensburg & Sprinkle 1994 only
> 
> The occurrences printed in Guensburg & Sprinkle 1994 have not yet been entered (none of them is entered so far).

### q015 (uncaptured)

Q: What is the full printed diagnosis of Rhenopyrgus nov. subgen. in Dehm (1961)?

- failure: no gap block for 1961_dehm / diagnoses
- note: page 16 not among the composed claims
- judge contract 2: Header names only taxon, rank status, source and year in standard taxonomic language; no verdict or summary; no question needed for uncaptured text.

Header: Diagnosis of Rhenopyrgus, proposed as a new subgenus (of Pyrgocystis) by Dehm (1961)
- list {"record": "rhenopyrgus-subgenus", "source": "1961_dehm", "kind": "diagnosis", "actKind": null}

> Diagnosis of Rhenopyrgus, proposed as a new subgenus (of Pyrgocystis) by Dehm (1961)
> 
> Statements about Pyrgocystis (Rhenopyrgus) Dehm 1961

### q016 (uncaptured)

Q: What illustrations does Fay (1962) print for Astrocystites ottawaensis?

- note: text between lookups: Illustrations coverage is "none" for Fay 1962, so I'll return the gap block.
- note: page 201 not among the composed claims
- judge contract 2: Header names taxon, source, year scope only; no verdict, summary, or mechanism wording; no question needed since parameters unambiguous.

Header: Illustrations for Astrocystites ottawaensis in Fay 1962; no other years or sources considered
- statement {"source": "1962_fay", "kind": "illustrations"}

> Illustrations for Astrocystites ottawaensis in Fay 1962; no other years or sources considered
> 
> The illustrations printed in Fay 1962 have not yet been entered (none of them is entered so far).

### q017 (uncaptured)

Q: What is the second sentence of Rievers's (1961) printed diagnosis for Pyrgocystis coronaeformis?

- note: text between lookups: Diagnoses coverage for Rievers 1961 is only partly entered, so a second sentence
- judge contract 2: Header lists only taxon, source diagnosis, rank and year scope in community language; no verdict or summary; no question asked.

Header: Pyrgocystis coronaeformis Rievers 1961; diagnosis as printed by Rievers 1961; species-level record; all years
- list {"record": "coronaeformis_rievers_1961", "source": "1961_rievers", "kind": "diagnosis", "actKind": null}
- statement {"source": "1961_rievers", "kind": "diagnoses"}

> Pyrgocystis coronaeformis Rievers 1961; diagnosis as printed by Rievers 1961; species-level record; all years
> 
> Statements about Pyrgocystis coronaeformis Rievers 1961
>   1961  Rievers  diagnosis: A *Pyrgocystis* specimen measuring 95 mm in overall length, featuring a scaly column (stem) approximately 13 mm in diameter, which transitions at its lower end into a rounded, sac-like structure measuring 27 mm in height and approximately 17 mm in diameter. (pp. 10–11)
> 
> The diagnoses printed in Rievers 1961 have not yet been entered (only part of them is entered so far).

### q018 (uncaptured)

Q: Whose holotype does Briggs et al. (2017) cite for Heropyrgus disterminus, and where is it deposited?

- failure: no gap block for 2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman / material
- judge contract 2: Header names only the taxon and cited source as scope parameters, gives no verdict, summary, or mechanism; no clarifying question needed here.

Header: Holotype material statement for Heropyrgus disterminus, as cited by Briggs et al. 2017
- list {"record": "disterminus_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman_2017", "source": null, "kind": "material", "actKind": null}

> Holotype material statement for Heropyrgus disterminus, as cited by Briggs et al. 2017
> 
> Statements about Heropyrgus disterminus Briggs et al. 2017

### q019 (uncaptured)

Q: Which earlier works does Fay (1962) cite in his synonymy of Astrocystites ottawaensis?

- note: page 201 not among the composed claims
- judge contract 2: Header names only taxon, authority, and source work whose synonymy is at issue; no verdict, summary, or mechanism wording; no question needed.

Header: Astrocystites ottawaensis (Whiteaves 1897); synonymy as printed by Fay 1962
- statement {"source": "1962_fay", "kind": "synonymy"}

> Astrocystites ottawaensis (Whiteaves 1897); synonymy as printed by Fay 1962
> 
> The synonymy printed in Fay 1962 has not yet been entered (only part of it is entered so far).

### q020 (uncaptured)

Q: What holotype and paratype numbers does Sumrall et al. (2013) give for Rhenopyrgus piojoensis?

- failure: no gap block for 2013_sumrall_heredia_rodríguez.c.m_mestre / material
- judge contract 2: Header names only the taxon and requested material scope, in community language, with no summary, mechanism, or verdict; no question needed.

Header: Rhenopyrgus piojoensis Sumrall, Heredia, Rodríguez &amp; Mestre 2013: holotype and paratype material as stated by Sumrall et al. (2013)
- list {"record": "piojoensis_sumrall_heredia_rodríguez.c.m_mestre_2013", "source": "2013_sumrall_heredia_rodríguez.c.m_mestre", "kind": "material", "actKind": null}

> Rhenopyrgus piojoensis Sumrall, Heredia, Rodríguez &amp; Mestre 2013: holotype and paratype material as stated by Sumrall et al. (2013)
> 
> Statements about Rhenopyrgus piojoensis Sumrall et al. 2013

### q021 (as-published)

Q: What exact suborder heading do Ewin et al. (2020) print above family Rhenopyrgidae, and at what rank was that name first established?

- failure: free text beside the submission: The exact heading Ewin et al. (2020) print above Rhenopyrgidae is "Edrioblastoid
- judge contract 0: Header answers the question outright—names the heading and Fay's class rank plus 1994 change—delivering verdict and summary, not just chosen parameters.

Header: Suborder heading above Rhenopyrgidae in Ewin et al. (2020): "Edrioblastoidina"; the name (as Edrioblastoidea) was first established at class rank by Fay (1962), later treated as a suborder from 1994 onward. Ancestors block for Rhenopyrgidae and full history of Edrioblastoidina/Edrioblastoidea shown; all sources, taxonomy tree, name-at-other-ranks included.
- chains {"records": ["rhenopyrgidae"], "includeVariants": true, "trees": ["taxonomy"], "years": null}
- timeline {"record": "edrioblastoidina", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Suborder heading above Rhenopyrgidae in Ewin et al. (2020): "Edrioblastoidina"; the name (as Edrioblastoidea) was first established at class rank by Fay (1962), later treated as a suborder from 1994 onward. Ancestors block for Rhenopyrgidae and full history of Edrioblastoidina/Edrioblastoidea shown; all sources, taxonomy tree, name-at-other-ranks included.
> 
> Above Rhenopyrgidae Holloway & Jell 1983: 7 papers, 7 co-author sets, 1983–2020
> 
> 1983  Holloway & Jell       Edrioasteroidea › Order uncertain › Rhenopyrgidae
> 1994  Guensburg & Sprinkle  Echinozoa › Edrioasteroidea › Edrioasterida › Edrioblastoidina › Cyathocystidae › Rhenopyrginae
> 2000  Grigo                 Edrioasteroidea › Edrioasterida › Edrioblastoidina › Cyathocystidae › Rhenopyrginae
> 2010  Müller & Hahn         Isorophida › Rhenopyrgidae
> 2013  Sumrall et al.        Echinodermata › Edrioasteroidea › Edrioasterida › Edrioblastoidina › Rhenopyrgidae
> 2017  Briggs et al.         Echinodermata › Edrioasteroidea › Edrioasterida › Edrioblastoidina › Rhenopyrgidae
> 2020  Ewin et al.           Echinodermata › Edrioasteroidea › Edrioasterida › Edrioblastoidina › Rhenopyrgidae
> 
> Edrioblastoidina Fay 1962: 15 papers, 13 co-author sets, 1962–2020
> suborder since 1994 (6 papers), class 1962–1982 (9 papers)
> in Edrioasterida since 1994 (6 papers), in Echinozoa 1973–1982 (2 papers, 1 co-author sets), in Crinozoa 1965–1970 (4 papers), in Pelmatozoa 1968 (1 paper)
> 
> 1962  Fay                   Edrioblastoidea; named as new
> 1965  Fell                  Edrioblastoidea, in Crinozoa
> 1967  Fay                   Edrioblastoidea, in Crinozoa
> 1967  Ubaghs                Edrioblastoidea, in Crinozoa
> 1968  Webby                 Edrioblastoidea, in Pelmatozoa
> 1970  Mintz                 Edrioblastoidea, in Crinozoa
> 1973  Sprinkle              Edrioblastoidea, in Echinozoa; moved from Crinozoa; declines a placement in Crinozoa
> 1980  Bell                  Edrioblastoidea
> 1982  Sprinkle              Edrioblastoidea, in Echinozoa
> 1994  Guensburg & Sprinkle  Edrioblastoidina, in Edrioasterida; emended; nomen translatum from Edrioblastoidea
> 2000  Grigo                 Edrioblastoidina, in Edrioasterida
> 2013  Sumrall et al.        Edrioblastoidina, in Edrioasterida
> 2015  Sprinkle & Sumrall    Edrioblastoidina, in Edrioasterida
> 2017  Briggs et al.         Edrioblastoidina, in Edrioasterida
> 2020  Ewin et al.           Edrioblastoidina, in Edrioasterida (p. 118)

### q023 (as-published)

Q: How does Bassler (1936) print the original-genus citation for Cystaster granulatus?

- failure: no composed block carries a claim matching {'kind': 'acceptance', 'source': '1936_bassler', 'subject': 'granulatus_hall_1871', 'printed': {'citedAs': 'C. (Hemicystites) granulatus (Hall)'}, 'parents': ['cystaster-subgenus', 'hemicystites']}
- judge contract 2: Header names taxon, source and year only; no verdict, summary, or mechanism word; no question needed since the parameter is unambiguous.

Header: Printed form of the original-genus citation for Cystaster granulatus in Bassler (1936)
- list {"record": "granulatus_hall_1871", "source": "1936_bassler"}

> Printed form of the original-genus citation for Cystaster granulatus in Bassler (1936)
> 
> Cystaster granulatus
>   1936 "C. (Hemicystites) granulatus (Hall)" Bassler 1936

### q024 (as-published)

Q: How did Dehm (1961) style the new subgenus name Rhenopyrgus, and how do Sumrall et al. (2013) cite the type species using that name?

- failure: no composed block carries a claim matching {'kind': 'acceptance', 'source': '2013_sumrall_heredia_rodríguez.c.m_mestre', 'subject': 'coronaeformis_rievers_1961', 'printed': {'citedAs': 'Pyrgocystis (Rhenopyrgus) coronaeformis Rievers, 1961'}}
- judge contract 2: Header lists only scope parameters: taxon, sources, no synonym/rank expansion, block types, all years; no verdict or summary; no question needed.

Header: Rhenopyrgus (Dehm 1961, original subgenus of Pyrgocystis) taken with its printed forms in Dehm 1961 and Sumrall et al. 2013; no synonym or rank expansion beyond the subgenus/genus pair; classification and printed-form blocks only; all years
- list {"record": "rhenopyrgus-subgenus", "source": "1961_dehm"}
- list {"record": "rhenopyrgus-subgenus", "source": "1961_dehm", "kind": null, "actKind": null}
- list {"record": "coronaeformis_rievers_1961", "source": "2013_sumrall_heredia_rodríguez.c.m_mestre"}

> Rhenopyrgus (Dehm 1961, original subgenus of Pyrgocystis) taken with its printed forms in Dehm 1961 and Sumrall et al. 2013; no synonym or rank expansion beyond the subgenus/genus pair; classification and printed-form blocks only; all years
> 
> Pyrgocystis (Rhenopyrgus) (subgenus)
>   1961 "Rhenopyrgus nov. subgen." Dehm 1961 p. 16
> 
> Statements about Pyrgocystis (Rhenopyrgus) Dehm 1961
>   1961  Dehm  cites the name as "Rhenopyrgus nov. subgen." (p. 16)
>   1961  Dehm  places it under Pyrgocystis (p. 16)
>   1961  Dehm  named as new (p. 16)
> 
> Pyrgocystis (Rhenopyrgus) coronaeformis / Pyrgocystis coronaeformis / Rhenopyrgus coronaeformis
>   2013 "Pyrgocystis (Rhenopyrgus) coronaeformis Rievers, 1961" Sumrall et al. 2013

### q026 (as-published)

Q: What two different words does Fay (1962) use for the same specimen, No. 752, in Astrocystites ottawaensis?

- note: composed after the lookup limit was reached
- judge contract 2: Header names taxon, scope (material statement), source, tree type and year only; no summary, mechanism, or verdict; no question posed.

Header: Astrocystites ottawaensis Whiteaves 1897, material statement in Fay 1962; classifications only; year 1962
- list {"record": "ottawaensis_whiteaves_1897", "source": "1962_fay", "kind": "material", "actKind": null}

> Astrocystites ottawaensis Whiteaves 1897, material statement in Fay 1962; classifications only; year 1962
> 
> Statements about Astrocystites ottawaensis Whiteaves 1897
>   1962  Fay  syntypes: Canadian Geological Survey 752

### q028 (as-published)

Q: What exact heading and parenthetical act does Guensburg & Sprinkle (1994) print for the Rhenopyrgus subfamily?

- note: page 21 not among the composed claims
- judge contract 2: Header names only the record, its rank variant, the source publication and scope; no verdict or mechanism, and the as-published query needs no clarification.

Header: Rhenopyrginae (subfamily-rank name for Rhenopyrgidae Holloway & Jell 1983), as printed by Guensburg & Sprinkle (1994); classification heading only.
- classification {"source": "1994_guensburg_sprinkle", "record": "rhenopyrginae", "depth": null, "synonymy": false, "path": "0/children/0/children/4/children/1/children/1/children/1"}

> Rhenopyrginae (subfamily-rank name for Rhenopyrgidae Holloway & Jell 1983), as printed by Guensburg & Sprinkle (1994); classification heading only.
> 
> Guensburg & Sprinkle 1994
>   Subfamily Rhenopyrginae emend. nom. transl.
>     Genus Rhenopyrgus

### q032 (trajectory)

Q: What class or order has Astrocystites been placed in, across the sources that treat it?

- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1962_fay', 'actKind': 'new', 'subject': 'edrioblastoidea'}
- judge contract 1: Parameter-style and verdict-free, but "all 11 sources ... (1935–1994)" is a count/range assertion that conflicts with "all years" and later sources.

Header: Astrocystites Whiteaves 1897: class/order-level placements across all 11 sources treating it (1935–1994); classifications only, all years
- chains {"records": ["astrocystites"], "includeVariants": true, "trees": ["taxonomy"], "years": null}

> Astrocystites Whiteaves 1897: class/order-level placements across all 11 sources treating it (1935–1994); classifications only, all years
> 
> Above Astrocystites Whiteaves 1897: 11 papers, 8 co-author sets, 1935–1994
> 
> 1935  Bassler               Edrioasteroidea › ? Astrocystitidae (or Blastoidea) › Astrocystites
> 1936  Bassler               Pelmatozoa › Blastoidea › Protoblastoidea › ? Astrocystites
> 1962  Fay                   Edrioblastoidea › Astrocystites
> 1967  Fay                   Echinodermata › Crinozoa › Edrioblastoidea › Pentacystida › Astrocystitidae › Astrocystites
> 1968  Webby                 Pelmatozoa › Edrioblastoidea › Steganoblastidae › Astrocystites
> 1970  Mintz                 Crinozoa › Edrioblastoidea › Astrocystitidae › Astrocystites
> 1973  Sprinkle              Echinodermata › Echinozoa › Edrioblastoidea › Astrocystites
> 1980  Bell                  Edrioblastoidea › Astrocystitidae › Astrocystites
> 1982  Sprinkle              Echinodermata › Echinozoa › Edrioblastoidea › Pentacystida › Steganoblastidae › Astrocystites
> 1990  Smith & Jell          Edrioasteroidea › Edrioblastoida › Astrocystitidae › Astrocystites
> 1994  Guensburg & Sprinkle  Echinozoa › Edrioasteroidea › Edrioasterida › Edrioblastoidina › Astrocystitidae › Astrocystites

### q034 (trajectory)

Q: Who does the corpus credit as the author of Cambraster, and does every source agree?

- failure: free text beside the submission: This gives clear evidence: the resolver's authority is Jaekel 1923, but Guensbur
- judge contract 2: Header lists only scope parameters — taxon name, source coverage, year range — in community language, with no verdict or summary; no question needed.

Header: Authorship of the genus Cambraster; all sources that cite the name, all years
- list {"record": "cambraster", "source": null, "kind": null, "actKind": null}
- list {"record": "cambraster", "source": null}

> Authorship of the genus Cambraster; all sources that cite the name, all years
> 
> Statements about Cambraster Jaekel 1923
>   1985  Jell et al.           cites the name
>   1985  Jell et al.           places it under Stromatocystitidae
>   1985  Smith                 cites the name
>   1985  Smith                 places it under Isorophida
>   1985  Smith                 cites the name
>   1985  Smith                 places it under an unnamed group
>   1985  Smith                 cites the name
>   1985  Smith                 places it under an unnamed group in a cladogram
>   1990  Smith & Jell          cites the name
>   1990  Smith & Jell          places it under an unnamed group in a cladogram
>   1990  Smith & Jell          cites the name
>   1990  Smith & Jell          places it under Stromatocystites walcotti / Cambraster walcotti in a diagram
>   1994  Guensburg & Sprinkle  cites the name as "Cambraster Cabibel, Termier, and Termier, 1958"
>   1994  Guensburg & Sprinkle  places it under Family uncertain
>   1994  Guensburg & Sprinkle  cites the name
>   1994  Guensburg & Sprinkle  places it under Edrioasteroidea in a cladogram
>   1994  Guensburg & Sprinkle  cites the name
>   1994  Guensburg & Sprinkle  places it under Edrioasteroidea in a cladogram
>   1994  Guensburg & Sprinkle  cites the name
>   1994  Guensburg & Sprinkle  places it under Edrioasteroidea in a cladogram
>   1994  Guensburg & Sprinkle  cites the name
>   1994  Guensburg & Sprinkle  places it under Edrioasteroidea in a cladogram
>   2011  Sumrall & Zamora      cites the name
>   2011  Sumrall & Zamora      places it under an unnamed group in a cladogram
>   2013  Zamora                cites the name
>   2013  Zamora                places it under Aragocystites in a cladogram
>   2013  Zamora et al.         cites the name
>   2013  Zamora et al.         places it under Stromatocystitidae
>   2021  Jell & Sprinkle       cites the name
>   2021  Jell & Sprinkle       places it under Stromatocystitidae
> 
> Cambraster (genus)
>   1994 "Cambraster Cabibel, Termier, and Termier, 1958" Guensburg & Sprinkle 1994

### q035 (trajectory)

Q: Is Isorophus (and its sibling genus Carneyella) attributed to Foerste 1916 or 1917?

- failure: free text beside the submission: Both genera are attributed to **Foerste 1916** in the corpus.
- note: page 42 not among the composed claims
- judge contract 2: Header names the two genus-group records, scope of sources and years, adds no verdict or mechanism; omitted question is acceptable since parameters are unambiguous.

Header: Attribution of Isorophus and Carneyella (genus-group names); taxonomic history across all citing sources, all years
- timeline {"record": "isorophus", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}
- timeline {"record": "carneyella", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Attribution of Isorophus and Carneyella (genus-group names); taxonomic history across all citing sources, all years
> 
> Isorophus Foerste 1916: 9 papers, 7 co-author sets, 1935–2011
> in Isorophidae since 1976 (3 papers, 2 co-author sets), in Agelacrinitidae 1935–1994 (5 papers, 4 co-author sets), in Hemicystitidae 1983 (1 paper)
> 
> 1935  Bassler               Isorophus, in Agelacrinitidae
> 1936  Bassler               Isorophus, in Agelacrinitidae
> 1966  Regnéll               Isorophus, in Agelacrinitidae
> 1976  Bell                  Isorophus, in Isorophidae
> 1980  Bell                  Isorophus, in Isorophidae
> 1983  Holloway & Jell       Isorophus, in Hemicystitidae
> 1988  Guensburg             Isorophus, in Agelacrinitidae
> 1994  Guensburg & Sprinkle  Isorophus, in Agelacrinitidae
> 2011  Sumrall & Zamora      Isorophus, in Isorophidae
> 
> Carneyella Foerste 1916: 7 papers, 5 co-author sets, 1935–2010
> in Carneyellidae / Carneyellinae since 1976 (4 papers, 3 co-author sets), in Hemicystitidae 1936–1966 (2 papers), in Agelacrinitidae 1935 (1 paper)
> 
> 1935  Bassler               Carneyella, in Agelacrinitidae
> 1936  Bassler               Carneyella, in Hemicystitidae
> 1966  Regnéll               Carneyella, in Hemicystitidae
> 1976  Bell                  Carneyella, in Carneyellidae
> 1980  Bell                  Carneyella, in Carneyellidae
> 1994  Guensburg & Sprinkle  Carneyella, in Carneyellinae
> 2010  Sumrall               Carneyella, in Carneyellidae

### q036 (trajectory)

Q: At what rank do the sources treat Edrioblastoidea: a class, an order, or a suborder?

- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1990_smith.a.b_jell', 'subject': 'astrocystitidae', 'parent': 'edrioblastoida'}
- judge contract 2: Header names taxon, lists included rank variants, and states source/year scope; no summary, mechanism, or verdict; no question posed.

Header: Edrioblastoidea Fay 1962, its rank-variant forms Edrioblastoida and Edrioblastoidina included; history across all sources and years
- timeline {"record": "edrioblastoidea", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Edrioblastoidea Fay 1962, its rank-variant forms Edrioblastoida and Edrioblastoidina included; history across all sources and years
> 
> Edrioblastoidea Fay 1962: 18 papers, 16 co-author sets, 1962–2021
> order since 1990 (3 papers), suborder 1994–2020 (6 papers), class 1962–1982 (9 papers)
> in Edrioasteroidea since 1990 (3 papers), in Edrioasterida 1994–2020 (6 papers), in Echinozoa 1973–1982 (2 papers, 1 co-author sets), in Crinozoa 1965–1970 (4 papers), in Pelmatozoa 1968 (1 paper)
> 
> 1962  Fay                   Edrioblastoidea; named as new
> 1965  Fell                  Edrioblastoidea, in Crinozoa
> 1967  Fay                   Edrioblastoidea, in Crinozoa
> 1967  Ubaghs                Edrioblastoidea, in Crinozoa
> 1968  Webby                 Edrioblastoidea, in Pelmatozoa
> 1970  Mintz                 Edrioblastoidea, in Crinozoa
> 1973  Sprinkle              Edrioblastoidea, in Echinozoa; moved from Crinozoa; declines a placement in Crinozoa
> 1980  Bell                  Edrioblastoidea
> 1982  Sprinkle              Edrioblastoidea, in Echinozoa
> 1990  Smith & Jell          Edrioblastoida, in Edrioasteroidea
> 1994  Guensburg & Sprinkle  Edrioblastoidina, in Edrioasterida; emended; nomen translatum from Edrioblastoidea
> 2000  Grigo                 Edrioblastoidina, in Edrioasterida
> 2013  Sumrall et al.        Edrioblastoidina, in Edrioasterida
> 2014  Zhu et al.            Edrioblastoida, in Edrioasteroidea
> 2015  Sprinkle & Sumrall    Edrioblastoidina, in Edrioasterida
> 2017  Briggs et al.         Edrioblastoidina, in Edrioasterida
> 2020  Ewin et al.           Edrioblastoidina, in Edrioasterida (p. 118)
> 2021  Jell & Sprinkle       Edrioblastoida, in Edrioasteroidea

### q037 (uncaptured)

Q: What does Whiteaves (1897) print as the original type-species designation for Astrocystites?

- failure: no gap block for 1897_whiteaves / newTaxa
- judge contract 2: Header names only taxon, authority and the parameter queried (type-species designation); no verdict, summary or mechanism term; no question needed.

Header: Astrocystites (Whiteaves 1897), type species designation
- statement {"source": "1897_whiteaves", "kind": "types"}

> Astrocystites (Whiteaves 1897), type species designation
> 
> Whiteaves 1897 is on record; its content has not yet been entered, so nothing it prints about type designations can be reported yet.

### q041 (trajectory)

Q: Which papers in the corpus treat edrioblastoids, and what does each do to the group (erect, emend, re-rank, move, add a genus)?

- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1900_bather', 'actKind': 'new', 'subject': 'steganoblastidae'}
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1935_bassler', 'actKind': 'new', 'subject': 'astrocystitidae'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1936_bassler', 'subject': 'astrocystites', 'parent': 'protoblastoidea'}
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1968_webby', 'actKind': 'new', 'subject': 'distans_webby_1968'}
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1983_holloway_jell', 'actKind': 'new', 'subject': 'rhenopyrgidae'}
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1994_guensburg_sprinkle', 'actKind': 'nomTransl', 'subject': 'rhenopyrginae', 'altRankOf': 'rhenopyrgidae'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2000_grigo', 'subject': 'rhenopyrginae', 'parent': 'cyathocystidae'}
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '2013_sumrall_heredia_rodríguez.c.m_mestre', 'actKind': 'emended', 'subject': 'rhenopyrgidae'}
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '2020_ewin_martin.m_isotalo_zamora', 'actKind': 'emended', 'subject': 'rhenopyrgidae'}
- judge contract 2: Header names only the taxon, its rank variants, record type and year range in community terms; no verdict, summary or mechanism; no question needed.

Header: Edrioblastoidea taken as the class and its order/suborder rank variants (Edrioblastoida, Edrioblastoidina); classifications only, all years — first the timeline of every paper's act on the group itself (erection, emendation, re-ranking, movement between higher taxa), then the timelines of the genera each paper newly added to it
- timeline {"record": "edrioblastoidea", "includeRelated": true, "synonymy": true, "trees": ["taxonomy"], "years": null}
- timeline {"record": "cambroblastus", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}
- timeline {"record": "lampteroblastus", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}
- timeline {"record": "porosublastus", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}
- timeline {"record": "heropyrgus", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}
- timeline {"record": "ikerus", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Edrioblastoidea taken as the class and its order/suborder rank variants (Edrioblastoida, Edrioblastoidina); classifications only, all years — first the timeline of every paper's act on the group itself (erection, emendation, re-ranking, movement between higher taxa), then the timelines of the genera each paper newly added to it
> 
> Edrioblastoidea Fay 1962: 18 papers, 16 co-author sets, 1962–2021
> order since 1990 (3 papers), suborder 1994–2020 (6 papers), class 1962–1982 (9 papers)
> in Edrioasteroidea since 1990 (3 papers), in Edrioasterida 1994–2020 (6 papers), in Echinozoa 1973–1982 (2 papers, 1 co-author sets), in Crinozoa 1965–1970 (4 papers), in Pelmatozoa 1968 (1 paper)
> 
> 1962  Fay                   Edrioblastoidea; named as new
> 1965  Fell                  Edrioblastoidea, in Crinozoa
> 1967  Fay                   Edrioblastoidea, in Crinozoa
> 1967  Ubaghs                Edrioblastoidea, in Crinozoa
> 1968  Webby                 Edrioblastoidea, in Pelmatozoa
> 1970  Mintz                 Edrioblastoidea, in Crinozoa
> 1973  Sprinkle              Edrioblastoidea, in Echinozoa; moved from Crinozoa; declines a placement in Crinozoa
> 1980  Bell                  Edrioblastoidea
> 1982  Sprinkle              Edrioblastoidea, in Echinozoa
> 1990  Smith & Jell          Edrioblastoida, in Edrioasteroidea
> 1994  Guensburg & Sprinkle  Edrioblastoidina, in Edrioasterida; emended; nomen translatum from Edrioblastoidea
> 2000  Grigo                 Edrioblastoidina, in Edrioasterida
> 2013  Sumrall et al.        Edrioblastoidina, in Edrioasterida
> 2014  Zhu et al.            Edrioblastoida, in Edrioasteroidea
> 2015  Sprinkle & Sumrall    Edrioblastoidina, in Edrioasterida
> 2017  Briggs et al.         Edrioblastoidina, in Edrioasterida
> 2020  Ewin et al.           Edrioblastoidina, in Edrioasterida (p. 118)
> 2021  Jell & Sprinkle       Edrioblastoida, in Edrioasteroidea
> 
> Cambroblastus Smith & Jell 1990: 3 papers, 3 co-author sets, 1990–2014
> in Edrioblastoida since 2014 (1 paper), in Astrocystitidae 1990–1994 (2 papers)
> 
> 1990  Smith & Jell          Cambroblastus, in Astrocystitidae; named as new
> 1994  Guensburg & Sprinkle  Cambroblastus, in Astrocystitidae
> 2014  Zhu et al.            Cambroblastus, in Edrioblastoida
> 
> Lampteroblastus Guensburg & Sprinkle 1994: 1 paper, 1 co-author set, 1994
> in Astrocystitidae since 1994 (1 paper)
> 
> 1994  Guensburg & Sprinkle  Lampteroblastus, in Astrocystitidae; named as new
> 
> Porosublastus Sprinkle & Sumrall 2015: 1 paper, 1 co-author set, 2015
> in Astrocystitidae since 2015 (1 paper)
> 
> 2015  Sprinkle & Sumrall  Porosublastus, in Astrocystitidae; named as new
> 
> Heropyrgus Briggs et al. 2017: 2 papers, 2 co-author sets, 2017–2020
> in Rhenopyrgidae since 2017 (2 papers)
> 
> 2017  Briggs et al.  Heropyrgus, in Rhenopyrgidae; named as new
> 2020  Ewin et al.    Heropyrgus, in Rhenopyrgidae (p. 118)
> 
> Ikerus Jell & Sprinkle 2021: 1 paper, 1 co-author set, 2021
> in Edrioblastoida since 2021 (1 paper)
> 
> 2021  Jell & Sprinkle  Ikerus, in Edrioblastoida; named as new

### q043 (trajectory)

Q: At what rank has the edrioblastoid group been treated, and by which co-author sets, over time?

- failure: free text beside the submission: This history block fully answers the question about rank and treatment over time
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1990_smith.a.b_jell', 'subject': 'astrocystitidae', 'parent': 'edrioblastoida'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2014_zhu.x.j_zamora_lefebvre', 'subject': 'cambroblastus', 'parent': 'edrioblastoida'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2021_jell_sprinkle', 'subject': 'ikerus', 'parent': 'edrioblastoida'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2000_grigo', 'subject': 'cyathocystidae', 'parent': 'edrioblastoidina'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2013_sumrall_heredia_rodríguez.c.m_mestre', 'subject': 'rhenopyrgidae', 'parent': 'edrioblastoidina'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2015_sprinkle_sumrall', 'subject': 'astrocystitidae', 'parent': 'edrioblastoidina'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman', 'subject': 'rhenopyrgidae', 'parent': 'edrioblastoidina'}
- judge contract 2: Header lists only group, rank variants included, record type, and year span in community terms; no verdict or mechanism; no unnecessary question.

Header: Edrioblastoidea taken with its order and suborder rank variants (Edrioblastoida, Edrioblastoidina); classifications only; all years (1962–2021)
- timeline {"record": "edrioblastoidea", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Edrioblastoidea taken with its order and suborder rank variants (Edrioblastoida, Edrioblastoidina); classifications only; all years (1962–2021)
> 
> Edrioblastoidea Fay 1962: 18 papers, 16 co-author sets, 1962–2021
> order since 1990 (3 papers), suborder 1994–2020 (6 papers), class 1962–1982 (9 papers)
> in Edrioasteroidea since 1990 (3 papers), in Edrioasterida 1994–2020 (6 papers), in Echinozoa 1973–1982 (2 papers, 1 co-author sets), in Crinozoa 1965–1970 (4 papers), in Pelmatozoa 1968 (1 paper)
> 
> 1962  Fay                   Edrioblastoidea; named as new
> 1965  Fell                  Edrioblastoidea, in Crinozoa
> 1967  Fay                   Edrioblastoidea, in Crinozoa
> 1967  Ubaghs                Edrioblastoidea, in Crinozoa
> 1968  Webby                 Edrioblastoidea, in Pelmatozoa
> 1970  Mintz                 Edrioblastoidea, in Crinozoa
> 1973  Sprinkle              Edrioblastoidea, in Echinozoa; moved from Crinozoa; declines a placement in Crinozoa
> 1980  Bell                  Edrioblastoidea
> 1982  Sprinkle              Edrioblastoidea, in Echinozoa
> 1990  Smith & Jell          Edrioblastoida, in Edrioasteroidea
> 1994  Guensburg & Sprinkle  Edrioblastoidina, in Edrioasterida; emended; nomen translatum from Edrioblastoidea
> 2000  Grigo                 Edrioblastoidina, in Edrioasterida
> 2013  Sumrall et al.        Edrioblastoidina, in Edrioasterida
> 2014  Zhu et al.            Edrioblastoida, in Edrioasteroidea
> 2015  Sprinkle & Sumrall    Edrioblastoidina, in Edrioasterida
> 2017  Briggs et al.         Edrioblastoidina, in Edrioasterida
> 2020  Ewin et al.           Edrioblastoidina, in Edrioasterida (p. 118)
> 2021  Jell & Sprinkle       Edrioblastoida, in Edrioasteroidea

### q044 (trajectory)

Q: Which family name has been used for Astrocystites and by whom, Steganoblastidae or Astrocystitidae?

- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1900_bather', 'actKind': 'new', 'subject': 'steganoblastidae'}
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1935_bassler', 'actKind': 'new', 'subject': 'astrocystitidae'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2015_sprinkle_sumrall', 'subject': 'porosublastus', 'parent': 'astrocystitidae'}
- judge contract 2: Header names only the record, source scope and year range in ordinary taxonomic language, passes no verdict; no question needed since scope is fully stated.

Header: Family assignments used for Astrocystites Whiteaves 1897, across all sources and years (history of the genus's placement)
- timeline {"record": "astrocystites", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Family assignments used for Astrocystites Whiteaves 1897, across all sources and years (history of the genus's placement)
> 
> Astrocystites Whiteaves 1897: 11 papers, 8 co-author sets, 1935–1994
> in Astrocystitidae since 1935 (6 papers), in Steganoblastidae 1968–1982 (2 papers), in Edrioblastoidea 1962–1973 (2 papers), in Protoblastoidea 1936 (1 paper)
> 
> 1935  Bassler               Astrocystites, in Astrocystitidae
> 1936  Bassler               Astrocystites, in Protoblastoidea (provisional)
> 1962  Fay                   Astrocystites, in Edrioblastoidea; moved from Edrioasteroidea; declines a placement in Edrioasteroidea
> 1967  Fay                   Astrocystites, in Astrocystitidae
> 1968  Webby                 Astrocystites, in Steganoblastidae (p. 513)
> 1970  Mintz                 Astrocystites, in Astrocystitidae
> 1973  Sprinkle              Astrocystites, in Edrioblastoidea
> 1980  Bell                  Astrocystites, in Astrocystitidae
> 1982  Sprinkle              Astrocystites, in Steganoblastidae
> 1990  Smith & Jell          Astrocystites, in Astrocystitidae
> 1994  Guensburg & Sprinkle  Astrocystites, in Astrocystitidae

### q046 (trajectory)

Q: Has any single author appeared in papers holding different ranks for the edrioblastoid group?

- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1982i_sprinkle', 'subject': 'astrocystites', 'parent': 'steganoblastidae'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2015_sprinkle_sumrall', 'subject': 'astrocystitidae', 'parent': 'edrioblastoidina'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2021_jell_sprinkle', 'subject': 'ikerus', 'parent': 'edrioblastoida'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1990_smith.a.b_jell', 'subject': 'astrocystitidae', 'parent': 'edrioblastoida'}
- judge contract 1: Parameters (taxon, rank variants, classifications, all years) stated correctly, but the header then summarizes the finding—Sprinkle's rank spread—pre-empting the answer: one lapse.

Header: Edrioblastoidea taken with its rank variants (order Edrioblastoida, suborder Edrioblastoidina, class Edrioblastoidea); classifications only; all years — Sprinkle appears across papers assigning it class rank (1973, 1982), suborder rank (1994 with Guensburg, 2015 with Sumrall) and order rank (2021 with Jell)
- timeline {"record": "edrioblastoidea", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Edrioblastoidea taken with its rank variants (order Edrioblastoida, suborder Edrioblastoidina, class Edrioblastoidea); classifications only; all years — Sprinkle appears across papers assigning it class rank (1973, 1982), suborder rank (1994 with Guensburg, 2015 with Sumrall) and order rank (2021 with Jell)
> 
> Edrioblastoidea Fay 1962: 18 papers, 16 co-author sets, 1962–2021
> order since 1990 (3 papers), suborder 1994–2020 (6 papers), class 1962–1982 (9 papers)
> in Edrioasteroidea since 1990 (3 papers), in Edrioasterida 1994–2020 (6 papers), in Echinozoa 1973–1982 (2 papers, 1 co-author sets), in Crinozoa 1965–1970 (4 papers), in Pelmatozoa 1968 (1 paper)
> 
> 1962  Fay                   Edrioblastoidea; named as new
> 1965  Fell                  Edrioblastoidea, in Crinozoa
> 1967  Fay                   Edrioblastoidea, in Crinozoa
> 1967  Ubaghs                Edrioblastoidea, in Crinozoa
> 1968  Webby                 Edrioblastoidea, in Pelmatozoa
> 1970  Mintz                 Edrioblastoidea, in Crinozoa
> 1973  Sprinkle              Edrioblastoidea, in Echinozoa; moved from Crinozoa; declines a placement in Crinozoa
> 1980  Bell                  Edrioblastoidea
> 1982  Sprinkle              Edrioblastoidea, in Echinozoa
> 1990  Smith & Jell          Edrioblastoida, in Edrioasteroidea
> 1994  Guensburg & Sprinkle  Edrioblastoidina, in Edrioasterida; emended; nomen translatum from Edrioblastoidea
> 2000  Grigo                 Edrioblastoidina, in Edrioasterida
> 2013  Sumrall et al.        Edrioblastoidina, in Edrioasterida
> 2014  Zhu et al.            Edrioblastoida, in Edrioasteroidea
> 2015  Sprinkle & Sumrall    Edrioblastoidina, in Edrioasterida
> 2017  Briggs et al.         Edrioblastoidina, in Edrioasterida
> 2020  Ewin et al.           Edrioblastoidina, in Edrioasterida (p. 118)
> 2021  Jell & Sprinkle       Edrioblastoida, in Edrioasteroidea

### q047 (trajectory)

Q: Which taxon in the edrioblastoid group has the most distinct placements across sources?

- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1935_bassler', 'subject': 'astrocystites', 'parent': 'astrocystitidae'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1936_bassler', 'subject': 'astrocystites', 'parent': 'protoblastoidea'}
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1962_fay', 'actKind': 'new', 'subject': 'edrioblastoidea'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1967a_fay', 'subject': 'astrocystites', 'parent': 'astrocystitidae'}
- judge contract 0: Header delivers the full verdict with counts and citations rather than only parameters, and asks no question despite genuine genus-vs-family ambiguity.

Header: Within the Edrioblastoidea (class) group – comprising Pentacystida, Astrocystitidae (with its synonym Steganoblastidae), Cyathocystidae/Cyathocystinae, Cyathothecidae, Rhenopyrgidae/Rhenopyrginae, Thecocystidae and their genera and species – the family Astrocystitidae has been given the most distinct placements across sources (five: under "Edrioasteroidea" questionably by Bassler 1935, under Pentacystida by Fay 1967, under Edrioblastoidea by Mintz 1970 and Bell 1980, under Edrioblastoida by Smith & Jell 1990, and under Edrioblastoidina by Guensburg & Sprinkle 1994 and Sprinkle & Sumrall 2015), more than any other taxon in the group (e.g. Astrocystites: four; Cyathocystidae: four; Rhenopyrgidae: three). Taxonomy tree only; synonyms included; all years.
- table {"records": ["astrocystitidae"], "sources": null, "years": null, "includeVariants": true, "includeSynonyms": true, "trees": ["taxonomy"]}

> Within the Edrioblastoidea (class) group – comprising Pentacystida, Astrocystitidae (with its synonym Steganoblastidae), Cyathocystidae/Cyathocystinae, Cyathothecidae, Rhenopyrgidae/Rhenopyrginae, Thecocystidae and their genera and species – the family Astrocystitidae has been given the most distinct placements across sources (five: under "Edrioasteroidea" questionably by Bassler 1935, under Pentacystida by Fay 1967, under Edrioblastoidea by Mintz 1970 and Bell 1980, under Edrioblastoida by Smith & Jell 1990, and under Edrioblastoidina by Guensburg & Sprinkle 1994 and Sprinkle & Sumrall 2015), more than any other taxon in the group (e.g. Astrocystites: four; Cyathocystidae: four; Rhenopyrgidae: three). Taxonomy tree only; synonyms included; all years.
> 
> Placements by source
> schemes: Edrioblastoidina: 2 papers (1994–2015), 2 co-author sets, last Sprinkle & Sumrall 2015; Edrioblastoida: 1 paper (1990), 1 co-author set, last Smith & Jell 1990; Edrioblastoidea: 2 papers (1970–1980), 2 co-author sets, last Bell 1980; Pentacystida: 1 paper (1967), 1 co-author set, last Fay 1967; Edrioasteroidea: 1 paper (1935), 1 co-author set, last Bassler 1935
> record            rank    Bather 1900      Bassler 1935       Fay 1967      Webby 1968       Mintz 1970       Bell 1980        Sprinkle 1982  Smith & Jell 1990  Guensburg & Sprinkle 1994  Sprinkle & Sumrall 2015
> ----------------  ------  ---------------  -----------------  ------------  ---------------  ---------------  ---------------  -------------  -----------------  -------------------------  -----------------------
> Astrocystitidae   Family                   ? Edrioasteroidea  Pentacystida                   Edrioblastoidea  Edrioblastoidea                 Edrioblastoida     Edrioblastoidina           Edrioblastoidina
> Steganoblastidae  Family  Edrioasteroidea                                   Edrioblastoidea                                    Pentacystida

### q048 (trajectory)

Q: What did Holloway & Jell (1983) say Dehm (1961) did with Pyrgocystis octogona, and what does Dehm's own paper do?

- note: composed after the lookup limit was reached
- judge contract 2: Header lists only taxon, sources entered, coverage limits and year range in community language; no summary, mechanism or verdict; no question needed.

Header: Pyrgocystis octogona Richter 1930; Dehm's (1961) own treatment shown from statements entered for that source; Holloway & Jell's (1983) account of Dehm's treatment not available (synonymy only partly entered for that source); all years.
- list {"record": "octogona_richter.r_1930", "source": null, "kind": null, "actKind": null}
- statement {"source": "1983_holloway_jell", "kind": "synonymy"}

> Pyrgocystis octogona Richter 1930; Dehm's (1961) own treatment shown from statements entered for that source; Holloway & Jell's (1983) account of Dehm's treatment not available (synonymy only partly entered for that source); all years.
> 
> Statements about Pyrgocystis octogona Richter 1930
>   1935  Bassler  cites the name
>   1935  Bassler  places it under Pyrgocystis
>   1961  Dehm     cites the name (cited p. 294)
>   1961  Dehm     places it under Pyrgocystis (cited p. 294)
>   1961  Dehm     occurrence: Lower Devonian; greywacke slates; Bornich, near Weisel on the Rhine, Germany (cited p. 294)
> 
> The synonymy printed in Holloway & Jell 1983 has not yet been entered (only part of it is entered so far).

