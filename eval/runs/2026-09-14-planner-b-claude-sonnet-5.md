# Grades for `2026-09-14-planner-b-claude-sonnet-5.jsonl`

| class | questions | mechanical pass |
|---|---|---|
| absent | 3 | 3 |
| answerable | 12 | 8 |
| as-published | 8 | 5 |
| trajectory | 15 | 12 |
| uncaptured | 9 | 6 |

## Failures and notes

### q001 (answerable)

Q: What new class does Fay (1962) erect for the genus Astrocystites, and what family/order sit between the genus and the class?

- failure: no composed block is contents {"source": "1962_fay", "record": "edrioblastoidea"}
- failure: the answer does not show "Class Edrioblastoidea nov."
- failure: the answer does not show "Genus Astrocystites"
- judge contract 1: Parameters (taxon, source, trees, year) stated plainly, but "including the new class Fay erects" pre-announces a finding rather than a scope parameter.

Plan: {"header": "Chain of higher taxa above the genus Astrocystites as given by Fay 1962, including the new class Fay erects; classification trees only, restricted to 1962", "blocks": [{"tool": "ancestors", "parameters": {"records": ["astrocystites"], "trees": ["taxonomy"], "years": [1962, 1962]}}, {"tool": "statements", "parameters": {"record": "astrocystites", "source": "Fay 1962", "kind": "placement"}}]}
Header: Chain of higher taxa above the genus Astrocystites as given by Fay 1962, including the new class Fay erects; classification trees only, restricted to 1962
- chains {"records": ["astrocystites"], "includeVariants": true, "trees": ["taxonomy"], "years": [1962, 1962]}
- list {"record": "astrocystites", "source": "1962_fay", "kind": "placement", "actKind": null}

> Chain of higher taxa above the genus Astrocystites as given by Fay 1962, including the new class Fay erects; classification trees only, restricted to 1962
> 
> Above Astrocystites Whiteaves 1897: 1 paper, 1 co-author set, 1962
> 
> 1962  Fay  Edrioblastoidea › Astrocystites
> 
> Statements about Astrocystites Whiteaves 1897
>   1962  Fay  places it under Edrioblastoidea

### q003 (answerable)

Q: What species do Smith & Jell (1990) designate as the type species of the new genus Cambroblastus?

- failure: no composed block is contents {"source": "1990_smith.a.b_jell", "record": "cambroblastus"}
- failure: the answer does not show "Type species. Cambroblastus enubilatus"
- judge contract 2: Header lists only scope parameters (taxon, source year, no synonyms/variants, no trees), passes no verdict; question unambiguous so none asked.

Plan: {"header": "Type species of the new genus Cambroblastus as designated by Smith & Jell (1990); single-source statement, no synonyms or variants, no classification trees needed", "blocks": [{"tool": "statements", "parameters": {"record": "cambroblastus", "source": "Smith & Jell 1990", "act_kind": "type"}}]}
Header: Type species of the new genus Cambroblastus as designated by Smith & Jell (1990); single-source statement, no synonyms or variants, no classification trees needed
- statement {"source": "1990_smith.a.b_jell", "kind": null, "record": "cambroblastus", "actKind": "type"}

> Type species of the new genus Cambroblastus as designated by Smith & Jell (1990); single-source statement, no synonyms or variants, no classification trees needed
> 
> How much of the classification in Smith & Jell 1990 is entered has not been reviewed.

### q006 (answerable)

Q: What species do Sumrall, Heredia Rodríguez & Mestre (2013) confirm as the type species of Rhenopyrgus?

- failure: no composed block is contents {"source": "2013_sumrall_heredia_rodríguez.c.m_mestre", "record": "rhenopyrgus"}
- failure: the answer does not show "Rhenopyrgus coronaeformis"
- judge contract 2: Header names taxon, rank variants, the nomenclatural act's author/year and all-years scope in community language; no verdict or summary; no question needed.

Plan: {"header": "Rhenopyrgus (genus and subgenus forms) — type species act by Sumrall, Heredia Rodríguez & Mestre (2013); all years", "blocks": [{"tool": "statements", "parameters": {"record": "rhenopyrgus", "source": "2013_sumrall_heredia_rodríguez.c.m_mestre", "act_kind": "type"}}]}
Header: Rhenopyrgus (genus and subgenus forms) — type species act by Sumrall, Heredia Rodríguez & Mestre (2013); all years
- statement {"source": "2013_sumrall_heredia_rodríguez.c.m_mestre", "kind": null, "record": "rhenopyrgus", "actKind": "type"}

> Rhenopyrgus (genus and subgenus forms) — type species act by Sumrall, Heredia Rodríguez & Mestre (2013); all years
> 
> The classification printed in Sumrall et al. 2013 has not yet been entered (only part of it is entered so far).

### q009 (answerable)

Q: What new species of Rhenopyrgus does Grigo (2000) describe, and from where?

- failure: no composed block is gap {"source": "2000_grigo", "kind": "occurrences"}
- judge contract 2: Header names group, rank variants, source/year, and scope of records only; no verdict, summary, or mechanism talk; no question needed since answerable.

Plan: {"header": "Rhenopyrgus (genus and subgenus forms) in Grigo 2000: new species erected and their material/locality, drawn from the contents this source places under the genus and the material statements it records.", "blocks": [{"tool": "contents", "parameters": {"source": "Grigo 2000", "record": "Rhenopyrgus", "depth": 2}}, {"tool": "statements", "parameters": {"record": "Rhenopyrgus", "source": "Grigo 2000", "kind": "material"}}]}
Header: Rhenopyrgus (genus and subgenus forms) in Grigo 2000: new species erected and their material/locality, drawn from the contents this source places under the genus and the material statements it records.
- classification {"source": "2000_grigo", "record": "rhenopyrgus", "depth": 2, "synonymy": false, "path": "0/children/1/children/0/children/0/children/0/children/0"}
- statement {"source": "2000_grigo", "kind": "material", "record": "rhenopyrgus", "actKind": null}

> Rhenopyrgus (genus and subgenus forms) in Grigo 2000: new species erected and their material/locality, drawn from the contents this source places under the genus and the material statements it records.
> 
> Grigo 2000, p. 95
>   Genus Rhenopyrgus
>     Type species. Rhenopyrgus coronaeformis
>     Rhenopyrgus coronaeformis
>     Rhenopyrgus sp. nov.
> 
> How much of the material in Grigo 2000 is entered has not been reviewed.

### q014 (uncaptured)

Q: What occurrence data does Guensburg & Sprinkle (1994) print for the new species Lampteroblastus hintzei?

- failure: no composed block is gap {"source": "1994_guensburg_sprinkle", "kind": "occurrences"}
- failure: the answer does not show "The occurrences printed in Guensburg & Sprinkle 1994 have not yet been entered"
- judge contract 2: Header lists only taxon, source, and synonymy scope in standard taxonomic language; no summary, mechanism, or verdict; no unnecessary question asked.

Plan: {"header": "Occurrence data for Lampteroblastus hintzei (new species) as printed by Guensburg & Sprinkle 1994; single source, no synonymy", "blocks": [{"tool": "statements", "parameters": {"record": "hintzei_guensburg_sprinkle_1994", "source": "Guensburg & Sprinkle 1994", "kind": "material"}}]}
Header: Occurrence data for Lampteroblastus hintzei (new species) as printed by Guensburg & Sprinkle 1994; single source, no synonymy
- statement {"source": "1994_guensburg_sprinkle", "kind": "material", "record": "hintzei_guensburg_sprinkle_1994", "actKind": null}

> Occurrence data for Lampteroblastus hintzei (new species) as printed by Guensburg & Sprinkle 1994; single source, no synonymy
> 
> The material printed in Guensburg & Sprinkle 1994 has not yet been entered (none of it is entered so far).

### q015 (uncaptured)

Q: What is the full printed diagnosis of Rhenopyrgus nov. subgen. in Dehm (1961)?

- failure: no composed block is gap {"source": "1961_dehm", "kind": "diagnoses"}
- judge contract 2: Header neutrally names taxon, rank, source and year without summary, mechanism wording, or verdict; no question needed since parameters are unambiguous.

Plan: {"header": "Diagnosis of Rhenopyrgus (subgenus) as printed by Dehm 1961", "blocks": [{"tool": "statements", "parameters": {"record": "rhenopyrgus-subgenus", "source": "Dehm 1961", "kind": "diagnosis"}}]}
Header: Diagnosis of Rhenopyrgus (subgenus) as printed by Dehm 1961
- statement {"source": "1961_dehm", "kind": "diagnosis", "record": "rhenopyrgus-subgenus", "actKind": null}

> Diagnosis of Rhenopyrgus (subgenus) as printed by Dehm 1961
> 
> The diagnoses printed in Dehm 1961 have not yet been entered (none of them is entered so far).

### q016 (uncaptured)

Q: What illustrations does Fay (1962) print for Astrocystites ottawaensis?

- failure: the answer does not show "The illustrations printed in Fay 1962 have not yet been entered"
- judge contract 2: Header names only the source, taxon, and synonym/variant scope in community language; no summary, mechanism, or verdict; no question needed.

Plan: {"header": "Illustrations Fay (1962) prints for Astrocystites ottawaensis; single source, no synonyms/variants expansion needed", "blocks": [{"tool": "statements", "parameters": {"record": "ottawaensis_whiteaves_1897", "source": "Fay 1962", "kind": "illustrations"}}]}
Header: Illustrations Fay (1962) prints for Astrocystites ottawaensis; single source, no synonyms/variants expansion needed
- statement {"source": "1962_fay", "kind": "illustrations", "record": "ottawaensis_whiteaves_1897", "actKind": null}

> Illustrations Fay (1962) prints for Astrocystites ottawaensis; single source, no synonyms/variants expansion needed
> 
> The classification printed in Fay 1962 is entered in full.

### q021 (as-published)

Q: What exact suborder heading do Ewin et al. (2020) print above family Rhenopyrgidae, and at what rank was that name first established?

- failure: no composed block is printed_forms {"record": "edrioblastoidina", "source": "2020_ewin_martin.m_isotalo_zamora"}
- failure: no composed block is history {"record": "edrioblastoidina"}
- failure: the answer does not show "Suborder Edrioblastoidina Fay, 1962"
- failure: the answer does not show "class 1962–1982"
- judge contract 1: Header gives group, trees and year range in proper language and no verdict, but appends a purpose/task restatement and omits synonym/rank-variant scope.

Plan: {"header": "Family Rhenopyrgidae (Holloway & Jell 1983); showing the classificatory (taxonomy) chain of parent taxa given by each source across all years, to identify both the suborder heading Ewin et al. (2020) print above it and the rank at which that name was first used by the earliest source", "blocks": [{"tool": "ancestors", "parameters": {"records": ["Rhenopyrgidae"], "trees": ["taxonomy"]}}]}
Header: Family Rhenopyrgidae (Holloway & Jell 1983); showing the classificatory (taxonomy) chain of parent taxa given by each source across all years, to identify both the suborder heading Ewin et al. (2020) print above it and the rank at which that name was first used by the earliest source
- chains {"records": ["rhenopyrgidae"], "includeVariants": true, "trees": ["taxonomy"], "years": null}

> Family Rhenopyrgidae (Holloway & Jell 1983); showing the classificatory (taxonomy) chain of parent taxa given by each source across all years, to identify both the suborder heading Ewin et al. (2020) print above it and the rank at which that name was first used by the earliest source
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

### q024 (as-published)

Q: How did Dehm (1961) style the new subgenus name Rhenopyrgus, and how do Sumrall et al. (2013) cite the type species using that name?

- failure: no composed block is printed_forms {"record": "coronaeformis_rievers_1961", "source": "2013_sumrall_heredia_rodríguez.c.m_mestre"}
- failure: the answer does not show "Pyrgocystis (Rhenopyrgus) coronaeformis Rievers, 1961"
- judge contract 2: Header names taxon, rank, sources, and year scope in standard nomenclatural language; no summary, mechanism, or verdict; no unnecessary question asked.

Plan: {"header": "Rhenopyrgus taken at the subgenus rank as erected by Dehm 1961; printed form of the new subgenus name in Dehm 1961, and the type-species citation using that subgenus name in Sumrall et al. 2013; all years", "blocks": [{"tool": "printed_forms", "parameters": {"record": "rhenopyrgus-subgenus", "source": "Dehm 1961"}}, {"tool": "statements", "parameters": {"record": "rhenopyrgus-subgenus", "source": "Sumrall et al. 2013", "kind": "act", "act_kind": "type"}}], "question": null}
Header: Rhenopyrgus taken at the subgenus rank as erected by Dehm 1961; printed form of the new subgenus name in Dehm 1961, and the type-species citation using that subgenus name in Sumrall et al. 2013; all years
- list {"record": "rhenopyrgus-subgenus", "source": "1961_dehm"}
- statement {"source": "2013_sumrall_heredia_rodríguez.c.m_mestre", "kind": "act", "record": "rhenopyrgus-subgenus", "actKind": "type"}

> Rhenopyrgus taken at the subgenus rank as erected by Dehm 1961; printed form of the new subgenus name in Dehm 1961, and the type-species citation using that subgenus name in Sumrall et al. 2013; all years
> 
> Pyrgocystis (Rhenopyrgus) (subgenus)
>   1961 "Rhenopyrgus nov. subgen." Dehm 1961 p. 16
> 
> The classification printed in Sumrall et al. 2013 has not yet been entered (only part of it is entered so far).

### q028 (as-published)

Q: What exact heading and parenthetical act does Guensburg & Sprinkle (1994) print for the Rhenopyrgus subfamily?

- failure: no composed block is contents {"source": "1994_guensburg_sprinkle", "record": "rhenopyrginae"}
- failure: the answer does not show "Subfamily Rhenopyrginae emend. nom. transl."
- judge contract 2: Header names only taxon, source and the as-published scope in neutral taxonomic language; no verdict or summary, and no needless clarifying question.

Plan: {"header": "Printed heading and parenthetical act for the subfamily Rhenopyrginae as given by Guensburg & Sprinkle (1994)", "blocks": [{"tool": "printed_forms", "parameters": {"record": "rhenopyrginae", "source": "Guensburg & Sprinkle 1994"}}]}
Header: Printed heading and parenthetical act for the subfamily Rhenopyrginae as given by Guensburg & Sprinkle (1994)
- list {"record": "rhenopyrginae", "source": "1994_guensburg_sprinkle"}

> Printed heading and parenthetical act for the subfamily Rhenopyrginae as given by Guensburg & Sprinkle (1994)
> 
> Rhenopyrginae (Subfamily)

### q034 (trajectory)

Q: Who does the corpus credit as the author of Cambraster, and does every source agree?

- failure: no composed block is printed_forms {"record": "cambraster"}
- failure: the answer does not show "Cabibel, Termier, and Termier, 1958"
- judge contract 2: Header lists only scope parameters (genus, authorship field, all years, classifications), neutral wording, no verdict or mechanism; omitting a question is acceptable here.

Plan: {"header": "Cambraster taken as the genus; authorship as credited by each source; all years, classifications only", "blocks": [{"tool": "history", "parameters": {"record": "cambraster", "include_related": false}}]}
Header: Cambraster taken as the genus; authorship as credited by each source; all years, classifications only
- timeline {"record": "cambraster", "includeRelated": false, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Cambraster taken as the genus; authorship as credited by each source; all years, classifications only
> 
> Cambraster Jaekel 1923: 5 papers, 5 co-author sets, 1985–2021
> in Stromatocystitidae since 1985 (3 papers), in Family uncertain 1994 (1 paper), in Isorophida 1985 (1 paper)
> 
> 1985  Jell et al.           Cambraster, in Stromatocystitidae
> 1985  Smith                 Cambraster, in Isorophida
> 1985  Smith                 Cambraster
> 1994  Guensburg & Sprinkle  Cambraster, in Family uncertain
> 2013  Zamora et al.         Cambraster, in Stromatocystitidae
> 2021  Jell & Sprinkle       Cambraster, in Stromatocystitidae

### q038 (absent)

Q: What does Klug et al. (2008) themselves print in their protologue for Rhenopyrgus flos?

- note: text beside the submission: The corpus contains no source matching "Klug et al. (2008)", so their protologue
- judge contract 1: Scope note of absence is acceptable, but 'gap block' is internal mechanism jargon, not community language; one lapse.

Plan: {"header": "Source \"Klug et al. 2008\" not found in the corpus; gap block for this source", "blocks": [{"tool": "gap", "parameters": {"source": "Klug et al. 2008", "kind": "newTaxa"}}], "question": null}
Header: Source "Klug et al. 2008" not found in the corpus; gap block for this source
- statement {"source": "Klug et al. 2008", "kind": "newTaxa"}

> Source "Klug et al. 2008" not found in the corpus; gap block for this source
> 
> No source in the corpus mentions the source Klug et al. 2008.

### q039 (absent)

Q: Which sources place the genus Rhenoblastus, and where?

- note: text beside the submission: No source in the corpus carries the name "Rhenoblastus".
- judge contract 1: Header states the answer's conclusion (no source carries the name) rather than only parameters; one summary lapse, otherwise clean with no verdict and no question needed.

Plan: {"header": "Rhenoblastus: no source in the corpus carries this name", "blocks": [{"tool": "gap", "parameters": {"name": "Rhenoblastus"}}]}
Header: Rhenoblastus: no source in the corpus carries this name
- statement {"name": "Rhenoblastus"}

> Rhenoblastus: no source in the corpus carries this name
> 
> No source in the corpus mentions the name Rhenoblastus.

### q045 (trajectory)

Q: Who proposed placing rhenopyrgids inside Cyathocystidae, who followed, and who rejected it?

- failure: no composed block is placements {"records": ["rhenopyrgidae"]}
- failure: the answer does not show "not Cyathocystidae"
- judge contract 2: Header lists only taxa, rank variants, source scope and year range in standard taxonomic language; no verdict, summary, or mechanism; no question needed.

Plan: {"header": "Placement history of Rhenopyrgidae (including the rank variant Rhenopyrginae) under Cyathocystidae (including its rank variants Cyathocystinae and Cyathothecidae); all sources, all years", "blocks": [{"tool": "placed_under", "parameters": {"record": "Rhenopyrgidae", "parent": "Cyathocystidae", "include_variants": true}}]}
Header: Placement history of Rhenopyrgidae (including the rank variant Rhenopyrginae) under Cyathocystidae (including its rank variants Cyathocystinae and Cyathothecidae); all sources, all years
- chains {"record": "rhenopyrgidae", "parent": "cyathocystidae", "includeVariants": true, "trees": ["taxonomy"], "years": null}

> Placement history of Rhenopyrgidae (including the rank variant Rhenopyrginae) under Cyathocystidae (including its rank variants Cyathocystinae and Cyathothecidae); all sources, all years
> 
> Rhenopyrgidae Holloway & Jell 1983 under Cyathocystidae Bather 1899: 2 papers, 2 co-author sets, 1994–2000
> first Guensburg & Sprinkle 1994, last Grigo 2000
> 
> 1994  Guensburg & Sprinkle  Rhenopyrginae
> 2000  Grigo                 Rhenopyrginae

### q048 (trajectory)

Q: What did Holloway & Jell (1983) say Dehm (1961) did with Pyrgocystis octogona, and what does Dehm's own paper do?

- failure: no composed block is gap {"source": "1983_holloway_jell", "kind": "synonymy"}
- failure: the answer does not show "The synonymy printed in Holloway & Jell 1983 has not yet been entered"
- judge contract 2: Header names only the record, statement kinds, and no synonym/rank expansion, with neutral framing of two sources; no verdict, summary, or mechanism; no question needed.

Plan: {"header": "Pyrgocystis octogona (Richter 1930): what Holloway & Jell (1983) report of Dehm's (1961) treatment, and what Dehm (1961) himself states; all statement kinds, single species record, no synonym or rank-variant expansion", "blocks": [{"tool": "statements", "parameters": {"record": "octogona_richter.r_1930", "source": "Holloway & Jell 1983"}}, {"tool": "statements", "parameters": {"record": "octogona_richter.r_1930", "source": "Dehm 1961"}}], "question": null}
Header: Pyrgocystis octogona (Richter 1930): what Holloway & Jell (1983) report of Dehm's (1961) treatment, and what Dehm (1961) himself states; all statement kinds, single species record, no synonym or rank-variant expansion
- statement {"source": "1983_holloway_jell", "kind": null, "record": "octogona_richter.r_1930", "actKind": null}
- list {"record": "octogona_richter.r_1930", "source": "1961_dehm", "kind": null, "actKind": null}

> Pyrgocystis octogona (Richter 1930): what Holloway & Jell (1983) report of Dehm's (1961) treatment, and what Dehm (1961) himself states; all statement kinds, single species record, no synonym or rank-variant expansion
> 
> The classification printed in Holloway & Jell 1983 is entered in full.
> 
> Statements about Pyrgocystis octogona Richter 1930
>   1961  Dehm  cites the name (cited p. 294)
>   1961  Dehm  places it under Pyrgocystis (cited p. 294)
>   1961  Dehm  occurrence: Lower Devonian; greywacke slates; Bornich, near Weisel on the Rhine, Germany (cited p. 294)

