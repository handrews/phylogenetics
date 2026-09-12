# Grades for `2026-09-12-claude-sonnet-5.jsonl`

| class | questions | mechanical pass |
|---|---|---|
| absent | 3 | 2 |
| answerable | 12 | 8 |
| as-published | 8 | 4 |
| trajectory | 17 | 5 |
| uncaptured | 9 | 6 |

## Failures and notes

### q001 (answerable)

Q: What new class does Fay (1962) erect for the genus Astrocystites, and what family/order sit between the genus and the class?

- failure: free text beside the submission: Fay (1962) erects the class **Edrioblastoidea**, and places the genus *Astrocyst
- note: page 201 not among the composed claims

Header: Astrocystites and its placement in Fay (1962); classification tree from that source only, no synonyms, no other-rank variants, no year restriction
- classification {"source": "1962_fay", "record": "edrioblastoidea", "depth": null, "synonymy": false, "path": "0"}

> Astrocystites and its placement in Fay (1962); classification tree from that source only, no synonyms, no other-rank variants, no year restriction
> 
> Edrioblastoidea*
>   Astrocystites (moved from Edrioasteroidea)
>     Astrocystites ottawaensis [type] (inferred)

### q005 (answerable)

Q: What new genus and type species do Sprinkle & Sumrall (2015) place in family Astrocystitidae?

- note: page 351 not among the composed claims

Header: Astrocystitidae as classified by Sprinkle & Sumrall (2015); new genus and type species only; classification tree; year 2015
- classification {"source": "2015_sprinkle_sumrall", "record": "astrocystitidae", "depth": null, "synonymy": false, "path": "0/children/0/children/1/children/0"}

> Astrocystitidae as classified by Sprinkle & Sumrall (2015); new genus and type species only; classification tree; year 2015
> 
> Astrocystitidae
>   Porosublastus*
>     Porosublastus inexpectus* [type]

### q006 (answerable)

Q: What species do Sumrall, Heredia Rodríguez & Mestre (2013) confirm as the type species of Rhenopyrgus?

- failure: free text beside the submission: Confirmed: Sumrall, Heredia Rodríguez & Mestre (2013) list *Rhenopyrgus coronaef
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '2013_sumrall_heredia_rodríguez.c.m_mestre', 'actKind': 'emended', 'subject': 'rhenopyrgus'}
- note: page 773 not among the composed claims

Header: Type species act for Rhenopyrgus (Sumrall, Heredia Rodríguez & Mestre 2013), shown via the full name history of Rhenopyrgus coronaeformis (= Pyrgocystis (Rhenopyrgus) coronaeformis / Pyrgocystis coronaeformis); classifications only; all years
- table {"record": "coronaeformis_rievers_1961", "includeRelated": true, "trees": ["taxonomy"], "years": null}

> Type species act for Rhenopyrgus (Sumrall, Heredia Rodríguez & Mestre 2013), shown via the full name history of Rhenopyrgus coronaeformis (= Pyrgocystis (Rhenopyrgus) coronaeformis / Pyrgocystis coronaeformis); classifications only; all years
> 
> History of Pyrgocystis (Rhenopyrgus) coronaeformis / Pyrgocystis coronaeformis / Rhenopyrgus coronaeformis
> latest rank: species: 7 papers 1961–2020, 7 co-author sets, last Ewin et al. 2020
> positions: Rhenopyrgus (genus) / Pyrgocystis (Rhenopyrgus) (subgenus): 6 papers (1961–2020), 6 co-author sets, last Ewin et al. 2020; Pyrgocystis (genus): 1 paper (1961), 1 co-author set, last Rievers 1961
> papers: 7, 7 co-author sets
> source                year  as                                       rank     placed under                          acts                                                                                                        printed as                                             pages
> --------------------  ----  ---------------------------------------  -------  ------------------------------------  ----------------------------------------------------------------------------------------------------------  -----------------------------------------------------  ----------
> Dehm 1961             1961  Pyrgocystis (Rhenopyrgus) coronaeformis  species  Pyrgocystis (Rhenopyrgus) (subgenus)  type species / accepts Pyrgocystis coronaeformis (Rievers 1961) as Pyrgocystis (Rhenopyrgus) coronaeformis                                                         16
> Rievers 1961          1961  Pyrgocystis coronaeformis                species  Pyrgocystis (genus)                   named as new                                                                                                                                                       [[10, 11]]
> Regnéll 1966          1966  Pyrgocystis (Rhenopyrgus) coronaeformis  species  Pyrgocystis (Rhenopyrgus) (subgenus)  type species
> Holloway & Jell 1983  1983  Rhenopyrgus coronaeformis                species  Rhenopyrgus (genus)                   type species / accepts Pyrgocystis coronaeformis as Rhenopyrgus coronaeformis
> Grigo 2000            2000  Rhenopyrgus coronaeformis                species  Rhenopyrgus (genus)                   type species                                                                                                                                                       95
> Sumrall et al. 2013   2013  Rhenopyrgus coronaeformis                species  Rhenopyrgus (genus)                   type species / accepts Rhenopyrgus (Pyrgocystis) coronaeformis as Rhenopyrgus coronaeformis                 Pyrgocystis (Rhenopyrgus) coronaeformis Rievers, 1961
> Ewin et al. 2020      2020  Rhenopyrgus coronaeformis                species  Rhenopyrgus (genus)                   type species / accepts Rhenopyrgus (Pyrgocystis) coronaeformis as Rhenopyrgus coronaeformis                                                                        118

### q010 (answerable)

Q: What is the holotype specimen number for Rhenopyrgus viviani, named by Ewin, Martin, Isotalo & Zamora (2020)?

- failure: no composed block carries a claim matching {'kind': 'act', 'source': '2020_ewin_martin.m_isotalo_zamora', 'actKind': 'new', 'subject': 'viviani_ewin_martin.m_isotalo_zamora_2020'}

Header: Rhenopyrgus viviani Ewin, Martin, Isotalo & Zamora, 2020; holotype material statement as printed in the source
- table {"record": "viviani_ewin_martin.m_isotalo_zamora_2020", "source": null, "kind": "material", "actKind": null}

> Rhenopyrgus viviani Ewin, Martin, Isotalo & Zamora, 2020; holotype material statement as printed in the source
> 
> Statements about Rhenopyrgus viviani
> source            as                   kind      statement                                                                                                                                    page        by
> ----------------  -------------------  --------  -------------------------------------------------------------------------------------------------------------------------------------------  ----------  ------
> Ewin et al. 2020  Rhenopyrgus viviani  material  occurrence: Telychian; Cybèle Member', 'Jupiter Formation; Rock Pool Ledge', 'Jupiter River Section', 'Anticosti Island', 'Québec', 'Canada  [120, 122]  source
> Ewin et al. 2020  Rhenopyrgus viviani  material  holotypes: NHMUK EE16642                                                                                                                     [120, 122]  source
> Ewin et al. 2020  Rhenopyrgus viviani  material  paratypes: NHMUK ['EE15752', 'EE15755']                                                                                                      [120, 122]  source
> Ewin et al. 2020  Rhenopyrgus viviani  material  paratypes: MPEP 1126.1                                                                                                                       [120, 122]  source
> Ewin et al. 2020  Rhenopyrgus viviani  material  occurrence: Telychian; Pavillon Member', 'Jupiter Formation; Pavillon River Section', 'Anticosti Island', 'Québec', 'Canada                  [120, 122]  source
> Ewin et al. 2020  Rhenopyrgus viviani  material  paratypes: NHMUK EE15756                                                                                                                     [120, 122]  source
> Ewin et al. 2020  Rhenopyrgus viviani  material  occurrence:                                                                                                                                  [120, 122]  source
> Ewin et al. 2020  Rhenopyrgus viviani  material  unspecified: MPEP 1143.1                                                                                                                     [120, 122]  source
> Ewin et al. 2020  Rhenopyrgus viviani  material  illustration: {"figures": [2, [4, 5]]}                                                                                                       [120, 122]  source

### q011 (answerable)

Q: What is the holotype specimen number for Rhenopyrgus grayae, per Ewin et al. (2020)?

- note: page 122 not among the composed claims

Header: Holotype of Rhenopyrgus grayae (Bather, 1915), as given by Ewin, Martin, Isotalo & Zamora (2020)
- table {"record": "grayae_bather_1915", "source": "2020_ewin_martin.m_isotalo_zamora", "kind": "material", "actKind": null}

> Holotype of Rhenopyrgus grayae (Bather, 1915), as given by Ewin, Martin, Isotalo & Zamora (2020)
> 
> Statements about Pyrgocystis grayae / Rhenopyrgus grayae
> source            as                  kind      statement                                                                                                                                                                                                page  by
> ----------------  ------------------  --------  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  ----  ------
> Ewin et al. 2020  Rhenopyrgus grayae  material  occurrence: Katian; Upper Ordovician; Farden Member', 'South Threave Formation', 'Drummuck Group; Lady Burn Starfish Bed', 'part of the Craighead inlier.', 'Lady Burn', 'near Girvan', 'Scotland', 'UK  118   source
> Ewin et al. 2020  Rhenopyrgus grayae  material  holotypes: NHMUK E23470                                                                                                                                                                                  118   source
> Ewin et al. 2020  Rhenopyrgus grayae  material  unspecified: NHMUK E23674, E29570                                                                                                                                                                        118   source

### q012 (answerable)

Q: Which two genera does Ewin et al. (2020) list under the emended family Rhenopyrgidae?

- failure: page 118 not shown

Header: Genera placed under the emended family Rhenopyrgidae by Ewin et al. (2020): classification only, this source, all years
- classification {"source": "2020_ewin_martin.m_isotalo_zamora", "record": "rhenopyrgidae", "depth": null, "synonymy": false, "path": "0/children/0/children/0/children/0/children/0"}

> Genera placed under the emended family Rhenopyrgidae by Ewin et al. (2020): classification only, this source, all years
> 
> Rhenopyrgidae emend.
>   Rhenopyrgus emend.
>     Rhenopyrgus coronaeformis [type]
>     Rhenopyrgus grayae
>     Rhenopyrgus whitei
>     Rhenopyrgus flos
>     Rhenopyrgus piojoensis
>     Rhenopyrgus viviani*
>     Rhenopyrgus sp. indet. 1
>     Rhenopyrgus sp. indet. 2
>     Rhenopyrgus sp. indet. 3
>     Rhenopyrgus sp. indet. 4
>   Heropyrgus

### q013 (uncaptured)

Q: What holotype and paratype specimen numbers does Holloway & Jell (1983) give for Rhenopyrgus whitei?

- note: page 1004 not among the composed claims

Header: Rhenopyrgus whitei Holloway &amp; Jell, 1983 — holotype and paratype specimen numbers as printed in that source
- statement {"source": "1983_holloway_jell", "kind": "material"}

> Rhenopyrgus whitei Holloway &amp; Jell, 1983 — holotype and paratype specimen numbers as printed in that source
> 
> The material printed in Holloway & Jell 1983 has not yet been entered (none of it is entered so far).

### q014 (uncaptured)

Q: What occurrence data does Guensburg & Sprinkle (1994) print for the new species Lampteroblastus hintzei?

- note: text between lookups: The occurrence coverage for this source is declared "none," so this is a gap.

Header: Lampteroblastus hintzei Guensburg & Sprinkle, 1994; occurrence data from that source only
- statement {"source": "1994_guensburg_sprinkle", "kind": "occurrences"}

> Lampteroblastus hintzei Guensburg & Sprinkle, 1994; occurrence data from that source only
> 
> The occurrences printed in Guensburg & Sprinkle 1994 have not yet been entered (none of them is entered so far).

### q015 (uncaptured)

Q: What is the full printed diagnosis of Rhenopyrgus nov. subgen. in Dehm (1961)?

- failure: no gap block for 1961_dehm / diagnoses
- note: composed after the lookup limit was reached

Header: Rhenopyrgus taken as the subgenus (Pyrgocystis (Rhenopyrgus)) named as new by Dehm 1961; diagnosis sought in that source only
- table {"record": "rhenopyrgus-subgenus", "source": null, "kind": null, "actKind": null}
- statement {"source": "Dehm 1961", "kind": "diagnoses"}

> Rhenopyrgus taken as the subgenus (Pyrgocystis (Rhenopyrgus)) named as new by Dehm 1961; diagnosis sought in that source only
> 
> Statements about Pyrgocystis (Rhenopyrgus)
> source               as                         kind       statement                                     page  by
> -------------------  -------------------------  ---------  --------------------------------------------  ----  ------
> Dehm 1961            Pyrgocystis (Rhenopyrgus)  usage      cites the name as "Rhenopyrgus nov. subgen."  16    source
> Dehm 1961            Pyrgocystis (Rhenopyrgus)  placement  places it under Pyrgocystis (genus)           16    source
> Dehm 1961            Pyrgocystis (Rhenopyrgus)  act        named as new                                  16    source
> Regnéll 1966         Pyrgocystis (Rhenopyrgus)  usage      cites the name                                      source
> Regnéll 1966         Pyrgocystis (Rhenopyrgus)  placement  places it under Pyrgocystis (genus)                 source
> Sumrall et al. 2013  Pyrgocystis (Rhenopyrgus)  usage      cites the name                                      source
> Ewin et al. 2020     Pyrgocystis (Rhenopyrgus)  usage      cites the name                                      source
> 
> No source in the corpus mentions the source Dehm 1961.

### q016 (uncaptured)

Q: What illustrations does Fay (1962) print for Astrocystites ottawaensis?

- note: page 201 not among the composed claims

Header: Astrocystites ottawaensis (Whiteaves 1897), as treated by Fay (1962); illustrations only
- statement {"source": "1962_fay", "kind": "illustrations"}

> Astrocystites ottawaensis (Whiteaves 1897), as treated by Fay (1962); illustrations only
> 
> The illustrations printed in Fay 1962 have not yet been entered (none of them is entered so far).

### q017 (uncaptured)

Q: What is the second sentence of Rievers's (1961) printed diagnosis for Pyrgocystis coronaeformis?

- note: text between lookups: Diagnoses coverage is only "partly" for this source, so a second sentence beyond

Header: Pyrgocystis coronaeformis Rievers, 1961 — diagnosis as printed by Rievers (1961); no rank or synonym expansion; classification/diagnosis statements only; all years
- statement {"source": "1961_rievers", "kind": "diagnoses"}

> Pyrgocystis coronaeformis Rievers, 1961 — diagnosis as printed by Rievers (1961); no rank or synonym expansion; classification/diagnosis statements only; all years
> 
> The diagnoses printed in Rievers 1961 have not yet been entered (only part of them is entered so far).

### q018 (uncaptured)

Q: Whose holotype does Briggs et al. (2017) cite for Heropyrgus disterminus, and where is it deposited?

- failure: free text beside the submission: The gap block answers this directly.

Header: Heropyrgus disterminus (Briggs, Siveter, Siveter, Sutton & Rahman, 2017); holotype/deposition sought from the material statements of that source; all years
- statement {"source": "2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman", "kind": "material"}

> Heropyrgus disterminus (Briggs, Siveter, Siveter, Sutton & Rahman, 2017); holotype/deposition sought from the material statements of that source; all years
> 
> The material printed in Briggs et al. 2017 has not yet been entered (none of it is entered so far).

### q019 (uncaptured)

Q: Which earlier works does Fay (1962) cite in his synonymy of Astrocystites ottawaensis?

- note: page 201 not among the composed claims

Header: Astrocystites ottawaensis (Whiteaves 1897), synonymy as printed by Fay (1962); all years
- statement {"source": "1962_fay", "kind": "synonymy"}

> Astrocystites ottawaensis (Whiteaves 1897), synonymy as printed by Fay (1962); all years
> 
> The synonymy printed in Fay 1962 has not yet been entered (only part of it is entered so far).

### q023 (as-published)

Q: How does Bassler (1936) print the original-genus citation for Cystaster granulatus?

- failure: no composed block carries a claim matching {'kind': 'acceptance', 'source': '1936_bassler', 'subject': 'granulatus_hall_1871', 'printed': {'citedAs': 'C. (Hemicystites) granulatus (Hall)'}, 'parents': ['cystaster-subgenus', 'hemicystites']}

Header: Cystaster granulatus (originally Hall 1871); printed form of the original-genus citation as given by Bassler (1936)
- list {"record": "granulatus_hall_1871", "source": "1936_bassler"}

> Cystaster granulatus (originally Hall 1871); printed form of the original-genus citation as given by Bassler (1936)
> 
> Cystaster granulatus
>   1936 "C. (Hemicystites) granulatus (Hall)" Bassler 1936

### q024 (as-published)

Q: How did Dehm (1961) style the new subgenus name Rhenopyrgus, and how do Sumrall et al. (2013) cite the type species using that name?

- failure: free text beside the submission: Now composing the answer with the relevant blocks.
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1961_dehm', 'actKind': 'new', 'subject': 'rhenopyrgus-subgenus', 'printed': {'citedAs': 'Rhenopyrgus nov. subgen.'}}

Header: Rhenopyrgus (subgenus of Pyrgocystis, Dehm 1961) and its type species Rhenopyrgus coronaeformis (Rievers, 1961); printed forms and the type-species citation as given by Sumrall et al. (2013); classifications only, all years
- list {"record": "rhenopyrgus-subgenus", "source": null}
- list {"record": "coronaeformis_rievers_1961", "source": "2013_sumrall_heredia_rodríguez.c.m_mestre"}
- table {"record": "coronaeformis_rievers_1961", "source": "2013_sumrall_heredia_rodríguez.c.m_mestre", "kind": null, "actKind": null}

> Rhenopyrgus (subgenus of Pyrgocystis, Dehm 1961) and its type species Rhenopyrgus coronaeformis (Rievers, 1961); printed forms and the type-species citation as given by Sumrall et al. (2013); classifications only, all years
> 
> Pyrgocystis (Rhenopyrgus) (subgenus)
>   1961 "Rhenopyrgus nov. subgen." Dehm 1961 p. 16
> 
> Pyrgocystis (Rhenopyrgus) coronaeformis / Pyrgocystis coronaeformis / Rhenopyrgus coronaeformis
>   2013 "Pyrgocystis (Rhenopyrgus) coronaeformis Rievers, 1961" Sumrall et al. 2013
> 
> Statements about Pyrgocystis (Rhenopyrgus) coronaeformis / Pyrgocystis coronaeformis / Rhenopyrgus coronaeformis
> source               as                                       kind        statement                                                                     page          by
> -------------------  ---------------------------------------  ----------  ----------------------------------------------------------------------------  ------------  ------
> Sumrall et al. 2013  Rhenopyrgus coronaeformis                usage       cites the name                                                                              source
> Sumrall et al. 2013  Rhenopyrgus coronaeformis                placement   places it under Rhenopyrgus (genus)                                                         source
> Sumrall et al. 2013  Rhenopyrgus coronaeformis                act         type species                                                                                source
> Sumrall et al. 2013  Rhenopyrgus (Pyrgocystis) coronaeformis  usage       cites the name as "Pyrgocystis (Rhenopyrgus) coronaeformis Rievers, 1961"     cited p. 773  source
> Sumrall et al. 2013  Rhenopyrgus (Pyrgocystis) coronaeformis  acceptance  accepts Rhenopyrgus (Pyrgocystis) coronaeformis as Rhenopyrgus coronaeformis  cited p. 773  source

### q026 (as-published)

Q: What two different words does Fay (1962) use for the same specimen, No. 752, in Astrocystites ottawaensis?

- note: composed after the lookup limit was reached

Header: Astrocystites ottawaensis (Whiteaves, 1897); material statement of Fay (1962); no synonyms or other-rank forms; classification/material tree only; year 1962
- table {"record": "ottawaensis_whiteaves_1897", "source": "1962_fay", "kind": "material", "actKind": null}

> Astrocystites ottawaensis (Whiteaves, 1897); material statement of Fay (1962); no synonyms or other-rank forms; classification/material tree only; year 1962
> 
> Statements about Astrocystites ottawaensis
> source    as                         kind      statement                                 page  by
> --------  -------------------------  --------  ----------------------------------------  ----  ------
> Fay 1962  Astrocystites ottawaensis  material  syntypes: Canadian Geological Survey 752        source

### q027 (as-published)

Q: What two years does Sprinkle & Sumrall (2015) print for coordinate names from the same Bather work, Suborder Edrioasterina and Family Edrioasteridae?

- failure: free text beside the submission: Sprinkle & Sumrall (2015) prints "Suborder Edrioasterina, Bather, 1898" and "Fam

Header: Years printed by Sprinkle & Sumrall (2015) for the Bather names Suborder Edrioasterina and Family Edrioasteridae (coordinate ranks of the same taxon); full nomenclatural history shown for context; all years.
- table {"record": "edrioasterina", "includeRelated": true, "trees": ["taxonomy"], "years": null}
- table {"record": "edrioasteridae", "includeRelated": true, "trees": ["taxonomy"], "years": null}

> Years printed by Sprinkle & Sumrall (2015) for the Bather names Suborder Edrioasterina and Family Edrioasteridae (coordinate ranks of the same taxon); full nomenclatural history shown for context; all years.
> 
> History of Edrioasterina
> latest rank: family: 11 papers 1900–2015, 9 co-author sets, last Sprinkle & Sumrall 2015
> earlier ranks: suborder: 2 papers 1994–2015, last Sprinkle & Sumrall 2015
> positions: Edrioasterida (Order): 6 papers (1976–2015), 5 co-author sets, last Sprinkle & Sumrall 2015; Edrioasterina (Suborder): 2 papers (1994–2015), 2 co-author sets, last Sprinkle & Sumrall 2015; Edrioasteroidea (Class): 5 papers (1900–1975), 4 co-author sets, last Kolata 1975
> papers: 11, 9 co-author sets
> source                     year  as                              rank              placed under                                      acts                                            printed as                                                                 pages
> -------------------------  ----  ------------------------------  ----------------  ------------------------------------------------  ----------------------------------------------  -------------------------------------------------------------------------  -----
> Bather 1900                1900  Edrioasteridae                  Family            Edrioasteroidea (Class)
> Bassler 1935               1935  Edrioasteridae                  Family            Edrioasteroidea (Class)
> Bassler 1936               1936  Edrioasteridae                  Family            Edrioasteroidea (Class)
> Regnéll 1966               1966  Edrioasteridae                  Family            Edrioasteroidea (Class)
> Kolata 1975                1975  Edrioasteridae                  Family            Edrioasteroidea (Class)
> Bell 1976                  1976  Edrioasteridae                  Family            Edrioasterida (Order)
> Bell & Sprinkle 1978       1978  Edrioasteridae                  Family            Edrioasterida (Order)                             emended                                         Family Edrioasteridae Bell, 1976 [emend. herein]                           246
> Bell 1980                  1980  Edrioasteridae                  Family            Edrioasterida (Order)
> Smith 1985                 1985  Edrioasteridae                  Family            Edrioasterida (Order)
> Guensburg & Sprinkle 1994  1994  Edrioasterina / Edrioasteridae  Family, Suborder  Edrioasterida (Order) / Edrioasterina (Suborder)  emended / nomen translatum from Edrioasteridae
> Sprinkle & Sumrall 2015    2015  Edrioasterina / Edrioasteridae  Family, Suborder  Edrioasterida (Order) / Edrioasterina (Suborder)                                                  Suborder Edrioasterina, Bather, 1898 / Family Edrioasteridae Bather, 1899  348
> 
> History of Edrioasteridae
> latest rank: family: 11 papers 1900–2015, 9 co-author sets, last Sprinkle & Sumrall 2015
> earlier ranks: suborder: 3 papers 1858–2015, last Sprinkle & Sumrall 2015
> positions: Edrioasterida (Order): 6 papers (1976–2015), 5 co-author sets, last Sprinkle & Sumrall 2015; Edrioasterina (Suborder): 2 papers (1994–2015), 2 co-author sets, last Sprinkle & Sumrall 2015; Edrioasteroidea (Class): 5 papers (1900–1975), 4 co-author sets, last Kolata 1975; Asteriadæ (Order): 1 paper (1858), 1 co-author set, last Billings 1858
> papers: 12, 10 co-author sets
> source                     year  as                              rank              placed under                                      acts                                            printed as                                                                 pages
> -------------------------  ----  ------------------------------  ----------------  ------------------------------------------------  ----------------------------------------------  -------------------------------------------------------------------------  -----
> Billings 1858              1858  Edrioasteridæ                   Suborder          Asteriadæ (Order)                                 named as new                                                                                                               85
> Bather 1900                1900  Edrioasteridae                  Family            Edrioasteroidea (Class)
> Bassler 1935               1935  Edrioasteridae                  Family            Edrioasteroidea (Class)
> Bassler 1936               1936  Edrioasteridae                  Family            Edrioasteroidea (Class)
> Regnéll 1966               1966  Edrioasteridae                  Family            Edrioasteroidea (Class)
> Kolata 1975                1975  Edrioasteridae                  Family            Edrioasteroidea (Class)
> Bell 1976                  1976  Edrioasteridae                  Family            Edrioasterida (Order)
> Bell & Sprinkle 1978       1978  Edrioasteridae                  Family            Edrioasterida (Order)                             emended                                         Family Edrioasteridae Bell, 1976 [emend. herein]                           246
> Bell 1980                  1980  Edrioasteridae                  Family            Edrioasterida (Order)
> Smith 1985                 1985  Edrioasteridae                  Family            Edrioasterida (Order)
> Guensburg & Sprinkle 1994  1994  Edrioasteridae / Edrioasterina  Family, Suborder  Edrioasterina (Suborder) / Edrioasterida (Order)  emended / nomen translatum from Edrioasteridae
> Sprinkle & Sumrall 2015    2015  Edrioasteridae / Edrioasterina  Family, Suborder  Edrioasterina (Suborder) / Edrioasterida (Order)                                                  Family Edrioasteridae Bather, 1899 / Suborder Edrioasterina, Bather, 1898  348

### q028 (as-published)

Q: What exact heading and parenthetical act does Guensburg & Sprinkle (1994) print for the Rhenopyrgus subfamily?

- failure: free text beside the submission: The history table already gives the exact heading and act; I'll present that alo
- note: page 21 not among the composed claims

Header: Guensburg & Sprinkle (1994) heading and act for the Rhenopyrgus subfamily (Rhenopyrginae, a subfamily-rank variant of Rhenopyrgidae); classification/history data only, no synonyms beyond the variant fold, all years
- list {"record": "rhenopyrginae", "source": "guensburg_sprinkle_1994"}
- table {"record": "rhenopyrginae", "source": null, "kind": null, "actKind": null}

> Guensburg & Sprinkle (1994) heading and act for the Rhenopyrgus subfamily (Rhenopyrginae, a subfamily-rank variant of Rhenopyrgidae); classification/history data only, no synonyms beyond the variant fold, all years
> 
> Rhenopyrginae (Subfamily)
> 
> Statements about Rhenopyrginae
> source                     as             kind       statement                                page  by
> -------------------------  -------------  ---------  ---------------------------------------  ----  ------
> Guensburg & Sprinkle 1994  Rhenopyrginae  usage      cites the name                                 source
> Guensburg & Sprinkle 1994  Rhenopyrginae  placement  places it under Cyathocystidae (Family)        source
> Guensburg & Sprinkle 1994  Rhenopyrginae  act        emended                                        source
> Guensburg & Sprinkle 1994  Rhenopyrginae  act        nomen translatum from Rhenopyrgidae            source
> Grigo 2000                 Rhenopyrginae  usage      cites the name                                 source
> Grigo 2000                 Rhenopyrginae  placement  places it under Cyathocystidae (Family)        source

### q030 (trajectory)

Q: Is Rhenopyrgus a genus or a subgenus of Pyrgocystis?

- failure: free text beside the submission: Both records give the same single history table (the two ranks fold together as 

Header: Rhenopyrgus, taken as the genus together with its earlier subgenus-rank form (Pyrgocystis (Rhenopyrgus)); classifications only; all years
- table {"record": "rhenopyrgus", "includeRelated": true, "trees": ["taxonomy"], "years": null}

> Rhenopyrgus, taken as the genus together with its earlier subgenus-rank form (Pyrgocystis (Rhenopyrgus)); classifications only; all years
> 
> History of Rhenopyrgus
> latest rank: genus: 5 papers 1983–2020, 5 co-author sets, last Ewin et al. 2020
> earlier ranks: subgenus: 2 papers 1961–1966, last Regnéll 1966
> positions: Rhenopyrgidae (Family) / Rhenopyrginae (Subfamily): 5 papers (1983–2020), 5 co-author sets, last Ewin et al. 2020; Pyrgocystis (genus): 2 papers (1961–1966), 2 co-author sets, last Regnéll 1966
> papers: 7, 7 co-author sets
> source                     year  as                         rank      placed under               acts          printed as                pages
> -------------------------  ----  -------------------------  --------  -------------------------  ------------  ------------------------  -----
> Dehm 1961                  1961  Pyrgocystis (Rhenopyrgus)  subgenus  Pyrgocystis (genus)        named as new  Rhenopyrgus nov. subgen.  16
> Regnéll 1966               1966  Pyrgocystis (Rhenopyrgus)  subgenus  Pyrgocystis (genus)
> Holloway & Jell 1983       1983  Rhenopyrgus                genus     Rhenopyrgidae (Family)
> Guensburg & Sprinkle 1994  1994  Rhenopyrgus                genus     Rhenopyrginae (Subfamily)
> Grigo 2000                 2000  Rhenopyrgus                genus     Rhenopyrginae (Subfamily)                                          95
> Sumrall et al. 2013        2013  Rhenopyrgus                genus     Rhenopyrgidae (Family)     emended
> Ewin et al. 2020           2020  Rhenopyrgus                genus     Rhenopyrgidae (Family)     emended                                 118

### q031 (trajectory)

Q: What genus is Pyrgocystis octogona (Richter, 1930) placed in across the corpus?

- failure: no composed block carries a claim matching {'kind': 'usage', 'source': '1935_bassler', 'subject': 'octogona_richter.r_1930', 'form': 'taxon'}
- failure: no composed block carries a claim matching {'kind': 'usage', 'source': '1961_dehm', 'subject': 'octogona_richter.r_1930', 'form': 'taxon'}

Header: Pyrgocystis octogona (Richter, 1930) taken as the species combination; placements across the corpus's two sources that carry it; all years.
- table {"records": ["octogona_richter.r_1930"], "sources": null, "years": null, "includeVariants": true, "includeSynonyms": true, "trees": ["taxonomy"]}

> Pyrgocystis octogona (Richter, 1930) taken as the species combination; placements across the corpus's two sources that carry it; all years.
> 
> Placements by source
> schemes: Pyrgocystis (genus): 2 papers (1935–1961), 2 co-author sets, last Dehm 1961
> record                Bassler 1935         Dehm 1961
> --------------------  -------------------  -------------------
> Pyrgocystis octogona  Pyrgocystis (genus)  Pyrgocystis (genus)

### q032 (trajectory)

Q: What class or order has Astrocystites been placed in, across the sources that treat it?

- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1962_fay', 'actKind': 'new', 'subject': 'edrioblastoidea'}

Header: Astrocystites (genus); higher taxa it has been placed under (classes, orders and other ranks), across all sources that treat it; classifications only; all years
- table {"records": ["astrocystites"], "includeVariants": true, "trees": ["taxonomy"], "years": null}

> Astrocystites (genus); higher taxa it has been placed under (classes, orders and other ranks), across all sources that treat it; classifications only; all years
> 
> Placed above Astrocystites
> higher taxon      rank       edge                    sources                                                                                           count
> ----------------  ---------  ----------------------  ------------------------------------------------------------------------------------------------  -----
> Edrioblastoidea   Class      placement               Fay 1962 / Fay 1967 / Webby 1968 / Mintz 1970 / Sprinkle 1973 / Bell 1980 / Sprinkle 1982         7
> Astrocystitidae   Family     placement               Bassler 1935 / Fay 1967 / Mintz 1970 / Bell 1980 / Smith & Jell 1990 / Guensburg & Sprinkle 1994  6
> Echinodermata     Phylum     placement               Fay 1967 / Sprinkle 1973 / Sprinkle 1982                                                          3
> Echinozoa         Subphylum  placement               Sprinkle 1973 / Sprinkle 1982 / Guensburg & Sprinkle 1994                                         3
> Edrioasteroidea   Class      placement               Bassler 1935 / Smith & Jell 1990 / Guensburg & Sprinkle 1994                                      3
> Blastoidea        Class      alternative, placement  Bassler 1935 / Bassler 1936                                                                       2
> Crinozoa          Subphylum  placement               Fay 1967 / Mintz 1970                                                                             2
> Pelmatozoa        Subphylum  placement               Bassler 1936 / Webby 1968                                                                         2
> Pentacystida      Order      placement               Fay 1967 / Sprinkle 1982                                                                          2
> Steganoblastidae  Family     placement               Webby 1968 / Sprinkle 1982                                                                        2
> Edrioasterida     Order      placement               Guensburg & Sprinkle 1994                                                                         1
> Edrioblastoida    Order      placement               Smith & Jell 1990                                                                                 1
> Edrioblastoidina  Suborder   placement               Guensburg & Sprinkle 1994                                                                         1
> Protoblastoidea   Grade      placement               Bassler 1936                                                                                      1

### q035 (trajectory)

Q: Is Isorophus (and its sibling genus Carneyella) attributed to Foerste 1916 or 1917?

- failure: free text beside the submission: I have the history tables showing both attributions (1916 by resolve_name's auth
- note: page 42 not among the composed claims

Header: Isorophus and Carneyella (genus-rank history, all sources, all years); classifications only
- table {"record": "isorophus", "includeRelated": true, "trees": ["taxonomy"], "years": null}
- table {"record": "carneyella", "includeRelated": true, "trees": ["taxonomy"], "years": null}

> Isorophus and Carneyella (genus-rank history, all sources, all years); classifications only
> 
> History of Isorophus
> latest rank: genus: 9 papers 1935–2011, 7 co-author sets, last Sumrall & Zamora 2011
> positions: Isorophidae (Family): 3 papers (1976–2011), 2 co-author sets, last Sumrall & Zamora 2011; Agelacrinitidae (Family): 5 papers (1935–1994), 4 co-author sets, last Guensburg & Sprinkle 1994; Hemicystitidae (Family): 1 paper (1983), 1 co-author set, last Holloway & Jell 1983
> papers: 9, 7 co-author sets
> source                     year  as         rank   placed under              acts  printed as               pages
> -------------------------  ----  ---------  -----  ------------------------  ----  -----------------------  -----
> Bassler 1935               1935  Isorophus  genus  Agelacrinitidae (Family)
> Bassler 1936               1936  Isorophus  genus  Agelacrinitidae (Family)
> Regnéll 1966               1966  Isorophus  genus  Agelacrinitidae (Family)
> Bell 1976                  1976  Isorophus  genus  Isorophidae (Family)
> Bell 1980                  1980  Isorophus  genus  Isorophidae (Family)
> Holloway & Jell 1983       1983  Isorophus  genus  Hemicystitidae (Family)
> Guensburg 1988             1988  Isorophus  genus  Agelacrinitidae (Family)
> Guensburg & Sprinkle 1994  1994  Isorophus  genus  Agelacrinitidae (Family)        Isorophus Foerste, 1917
> Sumrall & Zamora 2011      2011  Isorophus  genus  Isorophidae (Family)
> 
> History of Carneyella
> latest rank: genus: 7 papers 1935–2010, 5 co-author sets, last Sumrall 2010
> positions: Carneyellidae (Family) / Carneyellinae (Subfamily): 4 papers (1976–2010), 3 co-author sets, last Sumrall 2010; Hemicystitidae (Family): 2 papers (1936–1966), 2 co-author sets, last Regnéll 1966; Agelacrinitidae (Family): 1 paper (1935), 1 co-author set, last Bassler 1935
> papers: 7, 5 co-author sets
> source                     year  as          rank   placed under               acts  printed as                pages
> -------------------------  ----  ----------  -----  -------------------------  ----  ------------------------  -----
> Bassler 1935               1935  Carneyella  genus  Agelacrinitidae (Family)
> Bassler 1936               1936  Carneyella  genus  Hemicystitidae (Family)
> Regnéll 1966               1966  Carneyella  genus  Hemicystitidae (Family)
> Bell 1976                  1976  Carneyella  genus  Carneyellidae (Family)
> Bell 1980                  1980  Carneyella  genus  Carneyellidae (Family)
> Guensburg & Sprinkle 1994  1994  Carneyella  genus  Carneyellinae (Subfamily)        Carneyella Foerste, 1917
> Sumrall 2010               2010  Carneyella  genus  Carneyellidae (Family)

### q036 (trajectory)

Q: At what rank do the sources treat Edrioblastoidea: a class, an order, or a suborder?

- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1990_smith.a.b_jell', 'subject': 'astrocystitidae', 'parent': 'edrioblastoida'}

Header: Edrioblastoidea taken as the class and its order (Edrioblastoida) and suborder (Edrioblastoidina) rank variants; history of usage across all sources, all years
- table {"record": "edrioblastoidea", "includeRelated": true, "trees": ["taxonomy"], "years": null}

> Edrioblastoidea taken as the class and its order (Edrioblastoida) and suborder (Edrioblastoidina) rank variants; history of usage across all sources, all years
> 
> History of Edrioblastoidea
> latest rank: order: 3 papers 1990–2021, 3 co-author sets, last Jell & Sprinkle 2021
> earlier ranks: suborder: 6 papers 1994–2020, last Ewin et al. 2020; class: 9 papers 1962–1982, last Sprinkle 1982
> positions: Edrioasteroidea (Class): 3 papers (1990–2021), 3 co-author sets, last Jell & Sprinkle 2021; Edrioasterida (Order): 6 papers (1994–2020), 6 co-author sets, last Ewin et al. 2020; Echinozoa (Subphylum): 2 papers (1973–1982), 1 co-author set, last Sprinkle 1982; Crinozoa (Subphylum): 4 papers (1965–1970), 4 co-author sets, last Mintz 1970; Pelmatozoa (Subphylum): 1 paper (1968), 1 co-author set, last Webby 1968
> papers: 18, 16 co-author sets
> source                     year  as                rank      placed under             acts                                                                printed as                           pages
> -------------------------  ----  ----------------  --------  -----------------------  ------------------------------------------------------------------  -----------------------------------  -----
> Fay 1962                   1962  Edrioblastoidea   Class                              named as new
> Fell 1965                  1965  Edrioblastoidea   Class     Crinozoa (Subphylum)
> Fay 1967                   1967  Edrioblastoidea   Class     Crinozoa (Subphylum)
> Ubaghs 1967                1967  Edrioblastoidea   Class     Crinozoa (Subphylum)
> Webby 1968                 1968  Edrioblastoidea   Class     Pelmatozoa (Subphylum)
> Mintz 1970                 1970  Edrioblastoidea   Class     Crinozoa (Subphylum)
> Sprinkle 1973              1973  Edrioblastoidea   Class     Echinozoa (Subphylum)    moved from Crinozoa / declines a placement in Crinozoa (Subphylum)
> Bell 1980                  1980  Edrioblastoidea   Class
> Sprinkle 1982              1982  Edrioblastoidea   Class     Echinozoa (Subphylum)
> Smith & Jell 1990          1990  Edrioblastoida    Order     Edrioasteroidea (Class)
> Guensburg & Sprinkle 1994  1994  Edrioblastoidina  Suborder  Edrioasterida (Order)    emended / nomen translatum from Edrioblastoidea
> Grigo 2000                 2000  Edrioblastoidina  Suborder  Edrioasterida (Order)
> Sumrall et al. 2013        2013  Edrioblastoidina  Suborder  Edrioasterida (Order)
> Zhu et al. 2014            2014  Edrioblastoida    Order     Edrioasteroidea (Class)
> Sprinkle & Sumrall 2015    2015  Edrioblastoidina  Suborder  Edrioasterida (Order)
> Briggs et al. 2017         2017  Edrioblastoidina  Suborder  Edrioasterida (Order)
> Ewin et al. 2020           2020  Edrioblastoidina  Suborder  Edrioasterida (Order)                                                                        Suborder Edrioblastoidina Fay, 1962  118
> Jell & Sprinkle 2021       2021  Edrioblastoida    Order     Edrioasteroidea (Class)

### q037 (uncaptured)

Q: What does Whiteaves (1897) print as the original type-species designation for Astrocystites?

- failure: no gap block for 1897_whiteaves / newTaxa

Header: Astrocystites (genus) and its type species Astrocystites ottawaensis, as attributed to Whiteaves (1897); type designation sought directly from that source; no year restriction
- statement {"source": "1897_whiteaves", "kind": "types"}

> Astrocystites (genus) and its type species Astrocystites ottawaensis, as attributed to Whiteaves (1897); type designation sought directly from that source; no year restriction
> 
> Whiteaves 1897 is on record; its content has not yet been entered, so nothing it prints about type designations can be reported yet.

### q038 (absent)

Q: What does Klug et al. (2008) themselves print in their protologue for Rhenopyrgus flos?

- failure: no block states that 2008_klug_krüger_korn_rücklin_schemm-gregory_debaets_mapes is not entered
- note: composed after the lookup limit was reached

Header: Rhenopyrgus flos (Klug, Krüger, Korn, Rücklin, Schemm-Gregory, DeBaets & Mapes, 2008); protologue sought in Klug et al. (2008) itself; no synonyms beyond the species record; all years
- table {"record": "flos_klug_krüger_korn_rücklin_schemm-gregory_debaets_mapes_2008", "includeRelated": true, "trees": ["taxonomy"], "years": null}
- table {"record": "flos_klug_krüger_korn_rücklin_schemm-gregory_debaets_mapes_2008", "source": null, "kind": null, "actKind": null}
Question back: Klug et al. (2008) is cited only as the authority for Rhenopyrgus flos; the corpus holds no source entry for that paper itself (its statements are not among those recorded, which run only from Sumrall et al. 2013 and Ewin et al. 2020), so no protologue text from it can be produced — do you want the history and statement records that the corpus does hold for this species instead?

> Rhenopyrgus flos (Klug, Krüger, Korn, Rücklin, Schemm-Gregory, DeBaets & Mapes, 2008); protologue sought in Klug et al. (2008) itself; no synonyms beyond the species record; all years
> 
> History of Rhenopyrgus flos
> latest rank: species: 2 papers 2013–2020, 2 co-author sets, last Ewin et al. 2020
> positions: Rhenopyrgus (genus): 2 papers (2013–2020), 2 co-author sets, last Ewin et al. 2020
> papers: 2, 2 co-author sets
> source               year  as                rank     placed under         acts  printed as  pages
> -------------------  ----  ----------------  -------  -------------------  ----  ----------  -----
> Sumrall et al. 2013  2013  Rhenopyrgus flos  species  Rhenopyrgus (genus)
> Ewin et al. 2020     2020  Rhenopyrgus flos  species  Rhenopyrgus (genus)                    118
> 
> Statements about Rhenopyrgus flos
> source               as                kind       statement                            page  by
> -------------------  ----------------  ---------  -----------------------------------  ----  ------
> Sumrall et al. 2013  Rhenopyrgus flos  usage      cites the name                             source
> Sumrall et al. 2013  Rhenopyrgus flos  placement  places it under Rhenopyrgus (genus)        source
> Ewin et al. 2020     Rhenopyrgus flos  usage      cites the name                       118   source
> Ewin et al. 2020     Rhenopyrgus flos  placement  places it under Rhenopyrgus (genus)  118   source
> 
> Question: Klug et al. (2008) is cited only as the authority for Rhenopyrgus flos; the corpus holds no source entry for that paper itself (its statements are not among those recorded, which run only from Sumrall et al. 2013 and Ewin et al. 2020), so no protologue text from it can be produced — do you want the history and statement records that the corpus does hold for this species instead?

### q041 (trajectory)

Q: Which papers in the corpus treat edrioblastoids, and what does each do to the group (erect, emend, re-rank, move, add a genus)?

- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1900_bather', 'actKind': 'new', 'subject': 'steganoblastidae'}
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1935_bassler', 'actKind': 'new', 'subject': 'astrocystitidae'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1936_bassler', 'subject': 'astrocystites', 'parent': 'protoblastoidea'}
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1983_holloway_jell', 'actKind': 'new', 'subject': 'rhenopyrgidae'}

Header: Edrioblastoidea taken as the class and its order (Edrioblastoida) and suborder (Edrioblastoidina) rank-forms together (a nomen translatum lineage); synonyms not separately listed; classifications and history shown; all years (1962–2021)
- table {"record": "edrioblastoidea", "includeRelated": true, "trees": ["taxonomy"], "years": null}
- classification {"source": "1962_fay", "record": "edrioblastoidea", "depth": null, "synonymy": false, "path": "0"}
- classification {"source": "1965_fell", "record": "edrioblastoidea", "depth": null, "synonymy": false, "path": "0/children/1/children/4"}
- classification {"source": "1967a_fay", "record": "edrioblastoidea", "depth": null, "synonymy": false, "path": "0/children/0/children/0"}
- classification {"source": "1967a_ubaghs", "record": "edrioblastoidea", "depth": null, "synonymy": false, "path": "0/children/1/children/5"}
- classification {"source": "1968_webby", "record": "edrioblastoidea", "depth": null, "synonymy": false, "path": "0/children/0"}
- classification {"source": "1970_mintz", "record": "edrioblastoidea", "depth": null, "synonymy": false, "path": "0/children/0"}
- classification {"source": "1973_sprinkle", "record": "edrioblastoidea", "depth": null, "synonymy": false, "path": "0/children/2/children/0"}
- classification {"source": "1980_bell.b.m", "record": "edrioblastoidea", "depth": null, "synonymy": false, "path": "1"}
- classification {"source": "1982i_sprinkle", "record": "edrioblastoidea", "depth": null, "synonymy": false, "path": "0/children/0/children/0"}
- classification {"source": "1990_smith.a.b_jell", "record": "edrioblastoida", "depth": null, "synonymy": false, "path": "0/children/3"}
- classification {"source": "2014_zhu.x.j_zamora_lefebvre", "record": "edrioblastoida", "depth": null, "synonymy": false, "path": "0/children/0/children/0"}
- classification {"source": "2021_jell_sprinkle", "record": "edrioblastoida", "depth": null, "synonymy": false, "path": "0/children/1/children/0/children/0"}
- classification {"source": "1994_guensburg_sprinkle", "record": "edrioblastoidina", "depth": null, "synonymy": false, "path": "0/children/0/children/4/children/1"}
- classification {"source": "2000_grigo", "record": "edrioblastoidina", "depth": null, "synonymy": false, "path": "0/children/1/children/0"}
- classification {"source": "2013_sumrall_heredia_rodríguez.c.m_mestre", "record": "edrioblastoidina", "depth": null, "synonymy": false, "path": "0/children/0/children/0/children/0"}
- classification {"source": "2015_sprinkle_sumrall", "record": "edrioblastoidina", "depth": null, "synonymy": false, "path": "0/children/0/children/1"}
- classification {"source": "2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman", "record": "edrioblastoidina", "depth": null, "synonymy": false, "path": "0/children/0/children/0/children/0"}
- classification {"source": "2020_ewin_martin.m_isotalo_zamora", "record": "edrioblastoidina", "depth": null, "synonymy": false, "path": "0/children/0/children/0/children/0"}

> Edrioblastoidea taken as the class and its order (Edrioblastoida) and suborder (Edrioblastoidina) rank-forms together (a nomen translatum lineage); synonyms not separately listed; classifications and history shown; all years (1962–2021)
> 
> History of Edrioblastoidea
> latest rank: order: 3 papers 1990–2021, 3 co-author sets, last Jell & Sprinkle 2021
> earlier ranks: suborder: 6 papers 1994–2020, last Ewin et al. 2020; class: 9 papers 1962–1982, last Sprinkle 1982
> positions: Edrioasteroidea (Class): 3 papers (1990–2021), 3 co-author sets, last Jell & Sprinkle 2021; Edrioasterida (Order): 6 papers (1994–2020), 6 co-author sets, last Ewin et al. 2020; Echinozoa (Subphylum): 2 papers (1973–1982), 1 co-author set, last Sprinkle 1982; Crinozoa (Subphylum): 4 papers (1965–1970), 4 co-author sets, last Mintz 1970; Pelmatozoa (Subphylum): 1 paper (1968), 1 co-author set, last Webby 1968
> papers: 18, 16 co-author sets
> source                     year  as                rank      placed under             acts                                                                printed as                           pages
> -------------------------  ----  ----------------  --------  -----------------------  ------------------------------------------------------------------  -----------------------------------  -----
> Fay 1962                   1962  Edrioblastoidea   Class                              named as new
> Fell 1965                  1965  Edrioblastoidea   Class     Crinozoa (Subphylum)
> Fay 1967                   1967  Edrioblastoidea   Class     Crinozoa (Subphylum)
> Ubaghs 1967                1967  Edrioblastoidea   Class     Crinozoa (Subphylum)
> Webby 1968                 1968  Edrioblastoidea   Class     Pelmatozoa (Subphylum)
> Mintz 1970                 1970  Edrioblastoidea   Class     Crinozoa (Subphylum)
> Sprinkle 1973              1973  Edrioblastoidea   Class     Echinozoa (Subphylum)    moved from Crinozoa / declines a placement in Crinozoa (Subphylum)
> Bell 1980                  1980  Edrioblastoidea   Class
> Sprinkle 1982              1982  Edrioblastoidea   Class     Echinozoa (Subphylum)
> Smith & Jell 1990          1990  Edrioblastoida    Order     Edrioasteroidea (Class)
> Guensburg & Sprinkle 1994  1994  Edrioblastoidina  Suborder  Edrioasterida (Order)    emended / nomen translatum from Edrioblastoidea
> Grigo 2000                 2000  Edrioblastoidina  Suborder  Edrioasterida (Order)
> Sumrall et al. 2013        2013  Edrioblastoidina  Suborder  Edrioasterida (Order)
> Zhu et al. 2014            2014  Edrioblastoida    Order     Edrioasteroidea (Class)
> Sprinkle & Sumrall 2015    2015  Edrioblastoidina  Suborder  Edrioasterida (Order)
> Briggs et al. 2017         2017  Edrioblastoidina  Suborder  Edrioasterida (Order)
> Ewin et al. 2020           2020  Edrioblastoidina  Suborder  Edrioasterida (Order)                                                                        Suborder Edrioblastoidina Fay, 1962  118
> Jell & Sprinkle 2021       2021  Edrioblastoida    Order     Edrioasteroidea (Class)
> 
> Edrioblastoidea*
>   Astrocystites (moved from Edrioasteroidea)
>     Astrocystites ottawaensis [type] (inferred)
> 
> Edrioblastoidea
> 
> Edrioblastoidea
>   Pentacystida
>     Astrocystitidae
>       Astrocystites
>         Astrocystites ottawaensis [type]
> 
> Edrioblastoidea
> 
> Edrioblastoidea
>   Steganoblastidae
>     Astrocystites
>       Astrocystites ottawaensis [type]
>       Astrocystites distans*
>       Astrocystites [astrocystites-sp_webby_1968]
> 
> Edrioblastoidea
>   Astrocystitidae
>     Astrocystites
>       Astrocystites ottawaensis [type]
>       Astrocystites distans
> 
> Edrioblastoidea (moved from Crinozoa)
>   Astrocystites
> 
> Edrioblastoidea
>   Astrocystitidae
>     Astrocystites
> 
> Edrioblastoidea
>   Pentacystida
>     Steganoblastidae
>       Astrocystites
>         Astrocystites ottawaensis [type]
>         Astrocystites [astrocystites-sp-a_sprinkle_1982i]
>         Astrocystites [astrocystites-sp-b_sprinkle_1982i]
> 
> Edrioblastoida
>   Astrocystitidae
>     Astrocystites
>       Astrocystites ottawaensis [type]
>       Astrocystites distans
>     Cambroblastus*
>       Cambroblastus enubilatus* [type]
> 
> Edrioblastoida
>   Cambroblastus
>     Cambroblastus enubilatus [type]
>     Cambroblastus guolensis*
> 
> Edrioblastoida
>   Ikerus*
>     Ikerus edgari* [type]
> 
> Edrioblastoidina emend. nom. transl.
>   Astrocystitidae emend.
>     Astrocystites
>     Cambroblastus
>     Lampteroblastus*
>       Lampteroblastus hintzei* [type]
>   Cyathocystidae emend.
>     Cyathocystinae emend. nom. transl.
>       Cyathocystis
>     Rhenopyrginae emend. nom. transl.
>       Rhenopyrgus
> 
> Edrioblastoidina
>   Cyathocystidae
>     Rhenopyrginae
>       Rhenopyrgus
>         Rhenopyrgus coronaeformis [type]
>         Rhenopyrgus [rhenopyrgus-sp_grigo_2000]*
> 
> Edrioblastoidina
>   Rhenopyrgidae emend. (moved from Cyathocystidae)
>     Rhenopyrgus emend.
>       Rhenopyrgus coronaeformis [type]
>       Rhenopyrgus piojoensis*
>       Rhenopyrgus whitei
>       Rhenopyrgus flos
> 
> Edrioblastoidina
>   Astrocystitidae
>     Porosublastus*
>       Porosublastus inexpectus* [type]
> 
> Edrioblastoidina
>   Rhenopyrgidae
>     Heropyrgus*
>       Heropyrgus disterminus* [type]
> 
> Edrioblastoidina
>   Rhenopyrgidae emend.
>     Rhenopyrgus emend.
>       Rhenopyrgus coronaeformis [type]
>       Rhenopyrgus grayae
>       Rhenopyrgus whitei
>       Rhenopyrgus flos
>       Rhenopyrgus piojoensis
>       Rhenopyrgus viviani*
>       Rhenopyrgus sp. indet. 1
>       Rhenopyrgus sp. indet. 2
>       Rhenopyrgus sp. indet. 3
>       Rhenopyrgus sp. indet. 4
>     Heropyrgus

### q043 (trajectory)

Q: At what rank has the edrioblastoid group been treated, and by which co-author sets, over time?

- failure: free text beside the submission: This directly answers the question with full detail.
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1990_smith.a.b_jell', 'subject': 'astrocystitidae', 'parent': 'edrioblastoida'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2014_zhu.x.j_zamora_lefebvre', 'subject': 'cambroblastus', 'parent': 'edrioblastoida'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2021_jell_sprinkle', 'subject': 'ikerus', 'parent': 'edrioblastoida'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2000_grigo', 'subject': 'cyathocystidae', 'parent': 'edrioblastoidina'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2013_sumrall_heredia_rodríguez.c.m_mestre', 'subject': 'rhenopyrgidae', 'parent': 'edrioblastoidina'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2015_sprinkle_sumrall', 'subject': 'astrocystitidae', 'parent': 'edrioblastoidina'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman', 'subject': 'rhenopyrgidae', 'parent': 'edrioblastoidina'}

Header: Edrioblastoidea (with its order and suborder rank forms, Edrioblastoida/Edrioblastoidina) taken as one group; rank history across all sources, all years, classifications only
- table {"record": "edrioblastoidea", "includeRelated": true, "trees": ["taxonomy"], "years": null}

> Edrioblastoidea (with its order and suborder rank forms, Edrioblastoida/Edrioblastoidina) taken as one group; rank history across all sources, all years, classifications only
> 
> History of Edrioblastoidea
> latest rank: order: 3 papers 1990–2021, 3 co-author sets, last Jell & Sprinkle 2021
> earlier ranks: suborder: 6 papers 1994–2020, last Ewin et al. 2020; class: 9 papers 1962–1982, last Sprinkle 1982
> positions: Edrioasteroidea (Class): 3 papers (1990–2021), 3 co-author sets, last Jell & Sprinkle 2021; Edrioasterida (Order): 6 papers (1994–2020), 6 co-author sets, last Ewin et al. 2020; Echinozoa (Subphylum): 2 papers (1973–1982), 1 co-author set, last Sprinkle 1982; Crinozoa (Subphylum): 4 papers (1965–1970), 4 co-author sets, last Mintz 1970; Pelmatozoa (Subphylum): 1 paper (1968), 1 co-author set, last Webby 1968
> papers: 18, 16 co-author sets
> source                     year  as                rank      placed under             acts                                                                printed as                           pages
> -------------------------  ----  ----------------  --------  -----------------------  ------------------------------------------------------------------  -----------------------------------  -----
> Fay 1962                   1962  Edrioblastoidea   Class                              named as new
> Fell 1965                  1965  Edrioblastoidea   Class     Crinozoa (Subphylum)
> Fay 1967                   1967  Edrioblastoidea   Class     Crinozoa (Subphylum)
> Ubaghs 1967                1967  Edrioblastoidea   Class     Crinozoa (Subphylum)
> Webby 1968                 1968  Edrioblastoidea   Class     Pelmatozoa (Subphylum)
> Mintz 1970                 1970  Edrioblastoidea   Class     Crinozoa (Subphylum)
> Sprinkle 1973              1973  Edrioblastoidea   Class     Echinozoa (Subphylum)    moved from Crinozoa / declines a placement in Crinozoa (Subphylum)
> Bell 1980                  1980  Edrioblastoidea   Class
> Sprinkle 1982              1982  Edrioblastoidea   Class     Echinozoa (Subphylum)
> Smith & Jell 1990          1990  Edrioblastoida    Order     Edrioasteroidea (Class)
> Guensburg & Sprinkle 1994  1994  Edrioblastoidina  Suborder  Edrioasterida (Order)    emended / nomen translatum from Edrioblastoidea
> Grigo 2000                 2000  Edrioblastoidina  Suborder  Edrioasterida (Order)
> Sumrall et al. 2013        2013  Edrioblastoidina  Suborder  Edrioasterida (Order)
> Zhu et al. 2014            2014  Edrioblastoida    Order     Edrioasteroidea (Class)
> Sprinkle & Sumrall 2015    2015  Edrioblastoidina  Suborder  Edrioasterida (Order)
> Briggs et al. 2017         2017  Edrioblastoidina  Suborder  Edrioasterida (Order)
> Ewin et al. 2020           2020  Edrioblastoidina  Suborder  Edrioasterida (Order)                                                                        Suborder Edrioblastoidina Fay, 1962  118
> Jell & Sprinkle 2021       2021  Edrioblastoida    Order     Edrioasteroidea (Class)

### q044 (trajectory)

Q: Which family name has been used for Astrocystites and by whom, Steganoblastidae or Astrocystitidae?

- failure: free text beside the submission: This directly answers the question with the placements table.
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1900_bather', 'actKind': 'new', 'subject': 'steganoblastidae'}
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1935_bassler', 'actKind': 'new', 'subject': 'astrocystitidae'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2015_sprinkle_sumrall', 'subject': 'porosublastus', 'parent': 'astrocystitidae'}

Header: Astrocystites (Whiteaves 1897): family placements across sources — Astrocystitidae (Bassler) vs Steganoblastidae (Bather); synonyms not included; classifications only; all years
- table {"records": ["astrocystites"], "sources": null, "years": null, "includeVariants": true, "includeSynonyms": true, "trees": ["taxonomy"]}

> Astrocystites (Whiteaves 1897): family placements across sources — Astrocystitidae (Bassler) vs Steganoblastidae (Bather); synonyms not included; classifications only; all years
> 
> Placements by source
> schemes: Astrocystitidae (Family): 6 papers (1935–1994), 6 co-author sets, last Guensburg & Sprinkle 1994; Steganoblastidae (Family): 2 papers (1968–1982), 2 co-author sets, last Sprinkle 1982; Edrioblastoidea (Class): 2 papers (1962–1973), 2 co-author sets, last Sprinkle 1973; Protoblastoidea (Grade): 1 paper (1936), 1 co-author set, last Bassler 1936
> record                 Bassler 1935              Bassler 1936                           Fay 1962                 Fay 1967                  Webby 1968                 Mintz 1970                Sprinkle 1973            Bell 1980                 Sprinkle 1982              Smith & Jell 1990         Guensburg & Sprinkle 1994
> ---------------------  ------------------------  -------------------------------------  -----------------------  ------------------------  -------------------------  ------------------------  -----------------------  ------------------------  -------------------------  ------------------------  -------------------------
> Astrocystites (genus)  Astrocystitidae (Family)  Protoblastoidea (Grade) (provisional)  Edrioblastoidea (Class)  Astrocystitidae (Family)  Steganoblastidae (Family)  Astrocystitidae (Family)  Edrioblastoidea (Class)  Astrocystitidae (Family)  Steganoblastidae (Family)  Astrocystitidae (Family)  Astrocystitidae (Family)

### q045 (trajectory)

Q: Who proposed placing rhenopyrgids inside Cyathocystidae, who followed, and who rejected it?

- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1994_guensburg_sprinkle', 'actKind': 'nomTransl', 'subject': 'rhenopyrginae', 'altRankOf': 'rhenopyrgidae'}
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '2013_sumrall_heredia_rodríguez.c.m_mestre', 'actKind': 'emended', 'subject': 'rhenopyrgidae'}
- failure: no composed block carries a claim matching {'kind': 'rejection', 'source': '2013_sumrall_heredia_rodríguez.c.m_mestre', 'subject': 'rhenopyrgidae', 'declinedParent': 'cyathocystidae'}

Header: Rhenopyrgidae/Rhenopyrginae placements relative to Cyathocystidae; same-rank variants included; classifications only; all years (1983–2020)
- table {"records": ["rhenopyrgidae"], "sources": null, "years": null, "includeVariants": true, "includeSynonyms": true, "trees": ["taxonomy"]}

> Rhenopyrgidae/Rhenopyrginae placements relative to Cyathocystidae; same-rank variants included; classifications only; all years (1983–2020)
> 
> Placements by source
> schemes: Edrioblastoidina (Suborder): 3 papers (2013–2020), 3 co-author sets, last Ewin et al. 2020; Isorophida (Order): 1 paper (2010), 1 co-author set, last Müller & Hahn 2010; Cyathocystidae (Family): 2 papers (1994–2000), 2 co-author sets, last Grigo 2000; [edrioasteroidea-order-uncertain_holloway_jell_1983] (Order): 1 paper (1983), 1 co-author set, last Holloway & Jell 1983
> record                     Holloway & Jell 1983                                                        Guensburg & Sprinkle 1994  Grigo 2000               Müller & Hahn 2010  Sumrall et al. 2013          Briggs et al. 2017           Ewin et al. 2020
> -------------------------  --------------------------------------------------------------------------  -------------------------  -----------------------  ------------------  ---------------------------  ---------------------------  ---------------------------
> Rhenopyrgidae (Family)     [edrioasteroidea-order-uncertain_holloway_jell_1983] (Order) [placeholder]                                                      Isorophida (Order)  Edrioblastoidina (Suborder)  Edrioblastoidina (Suborder)  Edrioblastoidina (Suborder)
> Rhenopyrginae (Subfamily)                                                                              Cyathocystidae (Family)    Cyathocystidae (Family)

### q046 (trajectory)

Q: Has any single author appeared in papers holding different ranks for the edrioblastoid group?

- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1982i_sprinkle', 'subject': 'astrocystites', 'parent': 'steganoblastidae'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2015_sprinkle_sumrall', 'subject': 'astrocystitidae', 'parent': 'edrioblastoidina'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '2021_jell_sprinkle', 'subject': 'ikerus', 'parent': 'edrioblastoida'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1990_smith.a.b_jell', 'subject': 'astrocystitidae', 'parent': 'edrioblastoida'}

Header: Edrioblastoidea (class) and its order/suborder-rank forms (Edrioblastoida, Edrioblastoidina), taken together as one group; taxonomic placements only, all years
- table {"record": "edrioblastoidea", "includeRelated": true, "trees": ["taxonomy"], "years": null}

> Edrioblastoidea (class) and its order/suborder-rank forms (Edrioblastoida, Edrioblastoidina), taken together as one group; taxonomic placements only, all years
> 
> History of Edrioblastoidea
> latest rank: order: 3 papers 1990–2021, 3 co-author sets, last Jell & Sprinkle 2021
> earlier ranks: suborder: 6 papers 1994–2020, last Ewin et al. 2020; class: 9 papers 1962–1982, last Sprinkle 1982
> positions: Edrioasteroidea (Class): 3 papers (1990–2021), 3 co-author sets, last Jell & Sprinkle 2021; Edrioasterida (Order): 6 papers (1994–2020), 6 co-author sets, last Ewin et al. 2020; Echinozoa (Subphylum): 2 papers (1973–1982), 1 co-author set, last Sprinkle 1982; Crinozoa (Subphylum): 4 papers (1965–1970), 4 co-author sets, last Mintz 1970; Pelmatozoa (Subphylum): 1 paper (1968), 1 co-author set, last Webby 1968
> papers: 18, 16 co-author sets
> source                     year  as                rank      placed under             acts                                                                printed as                           pages
> -------------------------  ----  ----------------  --------  -----------------------  ------------------------------------------------------------------  -----------------------------------  -----
> Fay 1962                   1962  Edrioblastoidea   Class                              named as new
> Fell 1965                  1965  Edrioblastoidea   Class     Crinozoa (Subphylum)
> Fay 1967                   1967  Edrioblastoidea   Class     Crinozoa (Subphylum)
> Ubaghs 1967                1967  Edrioblastoidea   Class     Crinozoa (Subphylum)
> Webby 1968                 1968  Edrioblastoidea   Class     Pelmatozoa (Subphylum)
> Mintz 1970                 1970  Edrioblastoidea   Class     Crinozoa (Subphylum)
> Sprinkle 1973              1973  Edrioblastoidea   Class     Echinozoa (Subphylum)    moved from Crinozoa / declines a placement in Crinozoa (Subphylum)
> Bell 1980                  1980  Edrioblastoidea   Class
> Sprinkle 1982              1982  Edrioblastoidea   Class     Echinozoa (Subphylum)
> Smith & Jell 1990          1990  Edrioblastoida    Order     Edrioasteroidea (Class)
> Guensburg & Sprinkle 1994  1994  Edrioblastoidina  Suborder  Edrioasterida (Order)    emended / nomen translatum from Edrioblastoidea
> Grigo 2000                 2000  Edrioblastoidina  Suborder  Edrioasterida (Order)
> Sumrall et al. 2013        2013  Edrioblastoidina  Suborder  Edrioasterida (Order)
> Zhu et al. 2014            2014  Edrioblastoida    Order     Edrioasteroidea (Class)
> Sprinkle & Sumrall 2015    2015  Edrioblastoidina  Suborder  Edrioasterida (Order)
> Briggs et al. 2017         2017  Edrioblastoidina  Suborder  Edrioasterida (Order)
> Ewin et al. 2020           2020  Edrioblastoidina  Suborder  Edrioasterida (Order)                                                                        Suborder Edrioblastoidina Fay, 1962  118
> Jell & Sprinkle 2021       2021  Edrioblastoida    Order     Edrioasteroidea (Class)

### q047 (trajectory)

Q: Which taxon in the edrioblastoid group has the most distinct placements across sources?

- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1935_bassler', 'subject': 'astrocystites', 'parent': 'astrocystitidae'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1935_bassler', 'subject': 'astrocystitidae', 'provisional': True, 'altPlacements': ['blastoidea']}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1936_bassler', 'subject': 'astrocystites', 'parent': 'protoblastoidea'}
- failure: no composed block carries a claim matching {'kind': 'act', 'source': '1962_fay', 'actKind': 'new', 'subject': 'edrioblastoidea'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1967a_fay', 'subject': 'astrocystites', 'parent': 'astrocystitidae'}
- failure: no composed block carries a claim matching {'kind': 'placement', 'source': '1994_guensburg_sprinkle', 'subject': 'astrocystitidae', 'parent': 'edrioblastoidina'}

Header: Within the Edrioblastoidea group (all ranks and rank-variant names folded together; synonymous names excluded; taxonomic classifications only; all years), the family Cyathocystidae (with its subfamily-rank variant Cyathocystinae folded in) is the taxon carried across the most sources, having been placed under five distinct parent taxa spanning eleven source papers from Bather 1900 through Grigo 2000 — as many distinct placements as its closest rival, Astrocystitidae, but over a broader span of sources
- table {"records": ["cyathocystidae"], "sources": null, "years": null, "includeVariants": true, "includeSynonyms": false, "trees": ["taxonomy"]}

> Within the Edrioblastoidea group (all ranks and rank-variant names folded together; synonymous names excluded; taxonomic classifications only; all years), the family Cyathocystidae (with its subfamily-rank variant Cyathocystinae folded in) is the taxon carried across the most sources, having been placed under five distinct parent taxa spanning eleven source papers from Bather 1900 through Grigo 2000 — as many distinct placements as its closest rival, Astrocystitidae, but over a broader span of sources
> 
> Placements by source
> schemes: Edrioblastoidina (Suborder): 2 papers (1994–2000), 2 co-author sets, last Grigo 2000; Cyathocystidae (Family): 1 paper (1994), 1 co-author set, last Guensburg & Sprinkle 1994; Cyathocystida (Order): 2 papers (1983–1985), 2 co-author sets, last Smith 1985; Cyathocystina (Suborder): 3 papers (1975–1982), 1 co-author set, last Bell 1982; Edrioasteroidea (Class): 4 papers (1900–1966), 3 co-author sets, last Regnéll 1966
> record                      Bather 1900              Bassler 1935             Bassler 1936             Regnéll 1966             Bell 1975                 Bell 1980                 Bell 1982                 Bockelie & Paul 1983   Smith 1985                                     Guensburg & Sprinkle 1994    Grigo 2000
> --------------------------  -----------------------  -----------------------  -----------------------  -----------------------  ------------------------  ------------------------  ------------------------  ---------------------  ---------------------------------------------  ---------------------------  ---------------------------
> Cyathocystidae (Family)     Edrioasteroidea (Class)  Edrioasteroidea (Class)  Edrioasteroidea (Class)  Edrioasteroidea (Class)  Cyathocystina (Suborder)  Cyathocystina (Suborder)  Cyathocystina (Suborder)  Cyathocystida (Order)  Cyathocystida (Order) / Cyathocystida (Order)  Edrioblastoidina (Suborder)  Edrioblastoidina (Suborder)
> Cyathocystinae (Subfamily)                                                                                                                                                                                                                                                          Cyathocystidae (Family)

### q048 (trajectory)

Q: What did Holloway & Jell (1983) say Dehm (1961) did with Pyrgocystis octogona, and what does Dehm's own paper do?

- note: composed after the lookup limit was reached

Header: Pyrgocystis octogona (Richter 1930); history of the name's treatment by Dehm (1961) as entered in the corpus, since no statement by Holloway & Jell (1983) about this species is recorded there; synonyms not included; classifications only; all years.
- table {"record": "octogona_richter.r_1930", "includeRelated": true, "trees": ["taxonomy"], "years": null}
- table {"record": "octogona_richter.r_1930", "source": null, "kind": null, "actKind": null}
Question back: The corpus holds no statement by Holloway & Jell (1983) about Pyrgocystis octogona itself (their 1983 paper's entries under Pyrgocystis/Rhenopyrgus cover sardesoni, petalus, coronaeformis and grayae, not octogona) — did you instead mean what they said about Pyrgocystis grayae or another species Dehm placed in Pyrgocystis, or is there a specific page in Holloway & Jell 1983 you have in mind that mentions octogona?

> Pyrgocystis octogona (Richter 1930); history of the name's treatment by Dehm (1961) as entered in the corpus, since no statement by Holloway & Jell (1983) about this species is recorded there; synonyms not included; classifications only; all years.
> 
> History of Pyrgocystis octogona
> latest rank: species: 2 papers 1935–1961, 2 co-author sets, last Dehm 1961
> positions: Pyrgocystis (genus): 2 papers (1935–1961), 2 co-author sets, last Dehm 1961
> papers: 2, 2 co-author sets
> source        year  as                    rank     placed under         acts  printed as  pages
> ------------  ----  --------------------  -------  -------------------  ----  ----------  -----
> Bassler 1935  1935  Pyrgocystis octogona  species  Pyrgocystis (genus)
> Dehm 1961     1961  Pyrgocystis octogona  species  Pyrgocystis (genus)
> 
> Statements about Pyrgocystis octogona
> source        as                    kind       statement                                                                                     page          by
> ------------  --------------------  ---------  --------------------------------------------------------------------------------------------  ------------  ------
> Bassler 1935  Pyrgocystis octogona  usage      cites the name                                                                                              source
> Bassler 1935  Pyrgocystis octogona  placement  places it under Pyrgocystis (genus)                                                                         source
> Dehm 1961     Pyrgocystis octogona  usage      cites the name                                                                                cited p. 294  source
> Dehm 1961     Pyrgocystis octogona  placement  places it under Pyrgocystis (genus)                                                           cited p. 294  source
> Dehm 1961     Pyrgocystis octogona  material   occurrence: Lower Devonian; greywacke slates; Bornich', 'near Weisel on the Rhine', 'Germany  cited p. 294  source
> 
> Question: The corpus holds no statement by Holloway & Jell (1983) about Pyrgocystis octogona itself (their 1983 paper's entries under Pyrgocystis/Rhenopyrgus cover sardesoni, petalus, coronaeformis and grayae, not octogona) — did you instead mean what they said about Pyrgocystis grayae or another species Dehm placed in Pyrgocystis, or is there a specific page in Holloway & Jell 1983 you have in mind that mentions octogona?

### q049 (trajectory)

Q: Which cladistic analyses in the corpus include Rhenopyrgus, and where does each place it?

- failure: free text beside the submission: The placements table already gives the full picture (unnamed groups for Smith & 

Header: Cladistic analyses (cladogram trees) in the corpus that include Rhenopyrgus (genus and its subgenus-rank variant), showing where each places it
- table {"records": ["rhenopyrgus", "rhenopyrgus-subgenus"], "sources": null, "years": null, "includeVariants": true, "includeSynonyms": true, "trees": ["cladogram"]}

> Cladistic analyses (cladogram trees) in the corpus that include Rhenopyrgus (genus and its subgenus-rank variant), showing where each places it
> 
> Placements by source
> schemes: Edrioasteroidea (Class): 1 paper (1994), 1 co-author set, last Guensburg & Sprinkle 1994
> record               Smith & Jell 1990  Guensburg & Sprinkle 1994                                                                              Sumrall et al. 2013
> -------------------  -----------------  -----------------------------------------------------------------------------------------------------  ---------------------------------
> Rhenopyrgus (genus)  (unnamed group)    Edrioasteroidea (Class) / Edrioasteroidea (Class) / Edrioasteroidea (Class) / Edrioasteroidea (Class)  (unnamed group) / (unnamed group)

