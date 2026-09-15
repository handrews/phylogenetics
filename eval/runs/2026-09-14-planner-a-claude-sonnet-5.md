# Grades for `2026-09-14-planner-claude-sonnet-5.jsonl`

| class | questions | mechanical pass |
|---|---|---|
| absent | 3 | 3 |
| answerable | 12 | 6 |
| as-published | 8 | 5 |
| trajectory | 15 | 3 |
| uncaptured | 9 | 3 |

## Failures and notes

### q001 (answerable)

Q: What new class does Fay (1962) erect for the genus Astrocystites, and what family/order sit between the genus and the class?

- failure: no composed block is contents {"source": "1962_fay", "record": "edrioblastoidea"}
- failure: the answer does not show "Class Edrioblastoidea nov."
- failure: the answer does not show "Genus Astrocystites"
- judge contract 1: Parameters (taxon, source, tree type, year) are stated plainly, but the header presupposes a new class and an interposed family/order — an anticipatory summary.

Plan: {"header": "Astrocystites (genus); classification chain from Fay (1962) alone, showing the new class and the family/order between it and the genus; classificatory tree only, year 1962", "blocks": [{"tool": "ancestors", "parameters": {"records": ["astrocystites"], "trees": "classification", "years": "1962"}}]}
Header: Astrocystites (genus); classification chain from Fay (1962) alone, showing the new class and the family/order between it and the genus; classificatory tree only, year 1962
- chains {"records": ["astrocystites"], "includeVariants": true, "trees": ["c", "l", "a", "s", "s", "i", "f", "i", "c", "a", "t", "i", "o", "n"], "years": ["1", "9", "6", "2"]}

> Astrocystites (genus); classification chain from Fay (1962) alone, showing the new class and the family/order between it and the genus; classificatory tree only, year 1962
> 
> Above Astrocystites Whiteaves 1897
> (no source places it there)

### q002 (answerable)

Q: Does Fay (1962) himself write that ottawaensis is the type species of Astrocystites, or is that flag the editor's own inference?

- failure: no composed block is statements {"record": "ottawaensis_whiteaves_1897", "source": "1962_fay"}
- failure: the answer does not show "(editor)"
- judge contract 2: Header names only scope parameters (Astrocystites type-species statements, Fay 1962 only), gives no verdict, summary, or mechanism language; no question needed.

Plan: {"header": "Whether Fay (1962) himself designates ottawaensis as the type species of Astrocystites: type-species act statements for Astrocystites from Fay 1962 only", "blocks": [{"tool": "statements", "parameters": {"record": "astrocystites", "source": "1962_fay", "kind": "act", "act_kind": "type"}}]}
Header: Whether Fay (1962) himself designates ottawaensis as the type species of Astrocystites: type-species act statements for Astrocystites from Fay 1962 only
- statement {"source": "1962_fay", "kind": "act", "record": "astrocystites", "actKind": "type"}

> Whether Fay (1962) himself designates ottawaensis as the type species of Astrocystites: type-species act statements for Astrocystites from Fay 1962 only
> 
> The classification printed in Fay 1962 is entered in full.

### q003 (answerable)

Q: What species do Smith & Jell (1990) designate as the type species of the new genus Cambroblastus?

- failure: no composed block is contents {"source": "1990_smith.a.b_jell", "record": "cambroblastus"}
- failure: the answer does not show "Type species. Cambroblastus enubilatus"
- judge contract 2: Header names only the taxon, source paper, and exclusion of synonyms/rank variants; no verdict or summary, and no spurious question asked.

Plan: {"header": "Type species of the new genus Cambroblastus as designated by Smith & Jell (1990); single-source statement, no synonyms or variants", "blocks": [{"tool": "statements", "parameters": {"record": "cambroblastus", "source": "Smith & Jell 1990", "kind": "act", "act_kind": "type"}}]}
Header: Type species of the new genus Cambroblastus as designated by Smith & Jell (1990); single-source statement, no synonyms or variants
- statement {"source": "1990_smith.a.b_jell", "kind": "act", "record": "cambroblastus", "actKind": "type"}

> Type species of the new genus Cambroblastus as designated by Smith & Jell (1990); single-source statement, no synonyms or variants
> 
> How much of the classification in Smith & Jell 1990 is entered has not been reviewed.

### q006 (answerable)

Q: What species do Sumrall, Heredia Rodríguez & Mestre (2013) confirm as the type species of Rhenopyrgus?

- failure: no composed block is contents {"source": "2013_sumrall_heredia_rodríguez.c.m_mestre", "record": "rhenopyrgus"}
- failure: the answer does not show "Rhenopyrgus coronaeformis"
- judge contract 1: Parameters (taxon, rank, years, source) are stated neutrally, but "as confirmed by" imports a verdict about the opinion rather than merely citing it.

Plan: {"header": "Type species of the genus Rhenopyrgus as confirmed by Sumrall, Heredia Rodríguez & Mestre (2013); genus rank only, all years", "blocks": [{"tool": "statements", "parameters": {"record": "rhenopyrgus", "source": "Sumrall et al. 2013", "kind": "act", "act_kind": "type"}}], "question": null}
Header: Type species of the genus Rhenopyrgus as confirmed by Sumrall, Heredia Rodríguez & Mestre (2013); genus rank only, all years
- statement {"source": "2013_sumrall_heredia_rodríguez.c.m_mestre", "kind": "act", "record": "rhenopyrgus", "actKind": "type"}

> Type species of the genus Rhenopyrgus as confirmed by Sumrall, Heredia Rodríguez & Mestre (2013); genus rank only, all years
> 
> The classification printed in Sumrall et al. 2013 has not yet been entered (only part of it is entered so far).

### q008 (answerable)

Q: In Holloway & Jell (1983), family Rhenopyrgidae is placed under a name that is not itself an order. What is that placeholder, and what does it mean?

- failure: the answer does not show "Order uncertain"
- judge contract 2: Header lists only taxon, source, tree type, and year in standard terms; no verdict, summary, or mechanism; no unnecessary question asked.

Plan: {"header": "Ancestry of family Rhenopyrgidae as given by Holloway & Jell (1983); classification tree only; year 1983", "blocks": [{"tool": "ancestors", "parameters": {"records": ["Rhenopyrgidae"], "trees": "classification", "years": [1983, 1983]}}]}
Header: Ancestry of family Rhenopyrgidae as given by Holloway & Jell (1983); classification tree only; year 1983
- chains {"records": ["rhenopyrgidae"], "includeVariants": true, "trees": ["c", "l", "a", "s", "s", "i", "f", "i", "c", "a", "t", "i", "o", "n"], "years": [1983, 1983]}

> Ancestry of family Rhenopyrgidae as given by Holloway & Jell (1983); classification tree only; year 1983
> 
> Above Rhenopyrgidae Holloway & Jell 1983
> (no source places it there)

### q009 (answerable)

Q: What new species of Rhenopyrgus does Grigo (2000) describe, and from where?

- failure: no composed block is gap {"source": "2000_grigo", "kind": "occurrences"}
- judge contract 2: Header lists only group (genus with authority), scope (new species and their material/locality), and year 2000; no summary, mechanism, or verdict; no question needed.

Plan: {"header": "Rhenopyrgus taken as the genus (Dehm 1961); new species erected by Grigo (2000) and the material/locality recorded for them; year 2000 only.", "blocks": [{"tool": "contents", "parameters": {"source": "Grigo 2000", "record": "Rhenopyrgus", "depth": 1}}, {"tool": "statements", "parameters": {"record": "Rhenopyrgus", "source": "Grigo 2000", "kind": "material", "act_kind": "new"}}]}
Header: Rhenopyrgus taken as the genus (Dehm 1961); new species erected by Grigo (2000) and the material/locality recorded for them; year 2000 only.
- classification {"source": "2000_grigo", "record": "rhenopyrgus", "depth": 1, "synonymy": false, "path": "0/children/1/children/0/children/0/children/0/children/0"}
- statement {"source": "2000_grigo", "kind": "material", "record": "rhenopyrgus", "actKind": "new"}

> Rhenopyrgus taken as the genus (Dehm 1961); new species erected by Grigo (2000) and the material/locality recorded for them; year 2000 only.
> 
> Grigo 2000, p. 95
>   Genus Rhenopyrgus
>     Type species. Rhenopyrgus coronaeformis
>     Rhenopyrgus coronaeformis
>     Rhenopyrgus sp. nov.
> 
> How much of the new taxa in Grigo 2000 is entered has not been reviewed.

### q013 (uncaptured)

Q: What holotype and paratype specimen numbers does Holloway & Jell (1983) give for Rhenopyrgus whitei?

- failure: no composed block is gap {"source": "1983_holloway_jell", "kind": "material"}
- judge contract 2: Header names only taxon, data type, and source paper; no verdict, summary or mechanism wording; no question needed since parameters are unambiguous.

Plan: {"header": "Material (holotype and paratype specimen numbers) for Rhenopyrgus whitei as given by Holloway & Jell (1983)", "blocks": [{"tool": "statements", "parameters": {"record": "whitei_holloway_jell_1983", "source": "1983_holloway_jell", "kind": "material"}}]}
Header: Material (holotype and paratype specimen numbers) for Rhenopyrgus whitei as given by Holloway & Jell (1983)
- statement {"source": "1983_holloway_jell", "kind": "material", "record": "whitei_holloway_jell_1983", "actKind": null}

> Material (holotype and paratype specimen numbers) for Rhenopyrgus whitei as given by Holloway & Jell (1983)
> 
> The material printed in Holloway & Jell 1983 has not yet been entered (none of it is entered so far).

### q014 (uncaptured)

Q: What occurrence data does Guensburg & Sprinkle (1994) print for the new species Lampteroblastus hintzei?

- failure: no composed block is gap {"source": "1994_guensburg_sprinkle", "kind": "occurrences"}
- failure: the answer does not show "The occurrences printed in Guensburg & Sprinkle 1994 have not yet been entered"
- judge contract 2: Header lists only taxon, source restriction, and scope in standard terms; no summary, mechanism, or verdict; no question needed.

Plan: {"header": "Lampteroblastus hintzei (new species); material/occurrence statements from Guensburg & Sprinkle 1994 only; no synonyms or other ranks involved", "blocks": [{"tool": "statements", "parameters": {"record": "hintzei_guensburg_sprinkle_1994", "source": "Guensburg & Sprinkle 1994", "kind": "material"}}]}
Header: Lampteroblastus hintzei (new species); material/occurrence statements from Guensburg & Sprinkle 1994 only; no synonyms or other ranks involved
- statement {"source": "1994_guensburg_sprinkle", "kind": "material", "record": "hintzei_guensburg_sprinkle_1994", "actKind": null}

> Lampteroblastus hintzei (new species); material/occurrence statements from Guensburg & Sprinkle 1994 only; no synonyms or other ranks involved
> 
> The material printed in Guensburg & Sprinkle 1994 has not yet been entered (none of it is entered so far).

### q015 (uncaptured)

Q: What is the full printed diagnosis of Rhenopyrgus nov. subgen. in Dehm (1961)?

- failure: no composed block is gap {"source": "1961_dehm", "kind": "diagnoses"}
- judge contract 2: Header names only taxon, rank variant, and source year in community language; no verdict, summary, or mechanism; no spurious question.

Plan: {"header": "Diagnosis of Rhenopyrgus (subgenus), as printed by Dehm 1961", "blocks": [{"tool": "statements", "parameters": {"record": "rhenopyrgus-subgenus", "source": "Dehm 1961", "kind": "diagnosis"}}]}
Header: Diagnosis of Rhenopyrgus (subgenus), as printed by Dehm 1961
- statement {"source": "1961_dehm", "kind": "diagnosis", "record": "rhenopyrgus-subgenus", "actKind": null}

> Diagnosis of Rhenopyrgus (subgenus), as printed by Dehm 1961
> 
> The diagnoses printed in Dehm 1961 have not yet been entered (none of them is entered so far).

### q016 (uncaptured)

Q: What illustrations does Fay (1962) print for Astrocystites ottawaensis?

- failure: no composed block is gap {"source": "1962_fay", "kind": "illustrations"}
- failure: the answer does not show "The illustrations printed in Fay 1962 have not yet been entered"
- judge contract 2: Header names taxon, source, and synonym/variant scope in community language, passes no verdict; no question needed since parameters are unambiguous.

Plan: {"header": "Illustrations Fay (1962) prints for Astrocystites ottawaensis; single source, no synonyms or variants involved", "blocks": [{"tool": "statements", "parameters": {"record": "ottawaensis_whiteaves_1897", "source": "Fay 1962", "kind": "illustrations"}}]}
Header: Illustrations Fay (1962) prints for Astrocystites ottawaensis; single source, no synonyms or variants involved
- statement {"source": "1962_fay", "kind": "illustrations", "record": "ottawaensis_whiteaves_1897", "actKind": null}

> Illustrations Fay (1962) prints for Astrocystites ottawaensis; single source, no synonyms or variants involved
> 
> The classification printed in Fay 1962 is entered in full.

### q017 (uncaptured)

Q: What diagnosis does Rievers (1961) print for Pyrgocystis coronaeformis?

- note: text beside the submission: I'll plan the diagnosis lookup for this species as printed by Rievers (1961).
- judge contract 2: Header lists only scope parameters—taxon, source restriction, statement type, year range—in standard terms, with no verdict or summary; no question needed.

Plan: {"header": "Species record Pyrgocystis coronaeformis (as printed by Rievers 1961); diagnosis statements from that source only; all years", "blocks": [{"tool": "statements", "parameters": {"record": "coronaeformis_rievers_1961", "source": "1961_rievers", "kind": "diagnosis"}}]}
Header: Species record Pyrgocystis coronaeformis (as printed by Rievers 1961); diagnosis statements from that source only; all years
- list {"record": "coronaeformis_rievers_1961", "source": "1961_rievers", "kind": "diagnosis", "actKind": null}

> Species record Pyrgocystis coronaeformis (as printed by Rievers 1961); diagnosis statements from that source only; all years
> 
> Statements about Pyrgocystis coronaeformis Rievers 1961
>   1961  Rievers  diagnosis: A *Pyrgocystis* specimen measuring 95 mm in overall length, featuring a scaly column (stem) approximately 13 mm in diameter, which transitions at its lower end into a rounded, sac-like structure measuring 27 mm in height and approximately 17 mm in diameter. (pp. 10–11)

### q018 (uncaptured)

Q: Whose holotype does Briggs et al. (2017) cite for Heropyrgus disterminus, and where is it deposited?

- failure: no composed block is gap {"source": "2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman", "kind": "material"}
- judge contract 2: Header names taxon, source and scope of records only, in community language; no verdict or mechanism; no question needed as parameters unambiguous.

Plan: {"header": "Heropyrgus disterminus (species), Briggs et al. 2017: holotype material statement only", "blocks": [{"tool": "statements", "parameters": {"record": "disterminus_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman_2017", "source": "Briggs et al. 2017", "kind": "material"}}]}
Header: Heropyrgus disterminus (species), Briggs et al. 2017: holotype material statement only
- statement {"source": "2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman", "kind": "material", "record": "disterminus_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman_2017", "actKind": null}

> Heropyrgus disterminus (species), Briggs et al. 2017: holotype material statement only
> 
> The material printed in Briggs et al. 2017 has not yet been entered (none of it is entered so far).

### q020 (uncaptured)

Q: What holotype and paratype numbers does Sumrall et al. (2013) give for Rhenopyrgus piojoensis?

- failure: no composed block is gap {"source": "2013_sumrall_heredia_rodríguez.c.m_mestre", "kind": "material"}
- judge contract 2: Header names only taxon, record type, and source restriction in community terms; no verdict or summary; no unnecessary question asked.

Plan: {"header": "Rhenopyrgus piojoensis (species); material statements from Sumrall et al. 2013 only", "blocks": [{"tool": "statements", "parameters": {"record": "piojoensis_sumrall_heredia_rodríguez.c.m_mestre_2013", "source": "Sumrall et al. 2013", "kind": "material"}}], "question": null}
Header: Rhenopyrgus piojoensis (species); material statements from Sumrall et al. 2013 only
- statement {"source": "2013_sumrall_heredia_rodríguez.c.m_mestre", "kind": "material", "record": "piojoensis_sumrall_heredia_rodríguez.c.m_mestre_2013", "actKind": null}

> Rhenopyrgus piojoensis (species); material statements from Sumrall et al. 2013 only
> 
> The material printed in Sumrall et al. 2013 has not yet been entered (none of it is entered so far).

### q021 (as-published)

Q: What exact suborder heading do Ewin et al. (2020) print above family Rhenopyrgidae, and at what rank was that name first established?

- failure: no composed block is printed_forms {"record": "edrioblastoidina", "source": "2020_ewin_martin.m_isotalo_zamora"}
- failure: no composed block is history {"record": "edrioblastoidina"}
- failure: the answer does not show "Suborder Edrioblastoidina Fay, 1962"
- failure: the answer does not show "class 1962–1982"
- judge contract 2: Header gives only group, rank-variant inclusion, tree-only records, and all-years scope; trailing clause justifies year range without summarizing or judging.

Plan: {"header": "Rhenopyrgidae (family, with its subfamily-rank variant Rhenopyrginae included); classification trees only; all years, to show both the position Ewin et al. (2020) print above it and the rank at which the name was first erected", "blocks": [{"tool": "history", "parameters": {"record": "Rhenopyrgidae", "include_related": true, "trees": "classification", "years": "all"}}]}
Header: Rhenopyrgidae (family, with its subfamily-rank variant Rhenopyrginae included); classification trees only; all years, to show both the position Ewin et al. (2020) print above it and the rank at which the name was first erected
- timeline {"record": "rhenopyrgidae", "includeRelated": true, "synonymy": false, "trees": ["c", "l", "a", "s", "s", "i", "f", "i", "c", "a", "t", "i", "o", "n"], "years": ["a", "l", "l"]}

> Rhenopyrgidae (family, with its subfamily-rank variant Rhenopyrginae included); classification trees only; all years, to show both the position Ewin et al. (2020) print above it and the rank at which the name was first erected
> 
> Rhenopyrgidae Holloway & Jell 1983
> (no source uses the name)

### q024 (as-published)

Q: How did Dehm (1961) style the new subgenus name Rhenopyrgus, and how do Sumrall et al. (2013) cite the type species using that name?

- failure: no composed block is printed_forms {"record": "coronaeformis_rievers_1961", "source": "2013_sumrall_heredia_rodríguez.c.m_mestre"}
- failure: the answer does not show "Pyrgocystis (Rhenopyrgus) coronaeformis Rievers, 1961"
- judge contract 2: Header states only scope (subgenus Rhenopyrgus, Dehm 1961 and Sumrall 2013 printed forms, all years) in taxonomic idiom; no verdict, summary, or mechanism; no question needed.

Plan: {"header": "Rhenopyrgus taken as the subgenus (as erected by Dehm 1961); printed forms of the subgenus name in Dehm 1961 and of its type species as cited by Sumrall et al. 2013; all years", "blocks": [{"tool": "printed_forms", "parameters": {"record": "rhenopyrgus-subgenus", "source": "Dehm 1961"}}, {"tool": "statements", "parameters": {"record": "rhenopyrgus-subgenus", "source": "Dehm 1961", "kind": "act", "act_kind": "type"}}, {"tool": "printed_forms", "parameters": {"record": "rhenopyrgus-subgenus", "source": "Sumrall et al. 2013"}}]}
Header: Rhenopyrgus taken as the subgenus (as erected by Dehm 1961); printed forms of the subgenus name in Dehm 1961 and of its type species as cited by Sumrall et al. 2013; all years
- list {"record": "rhenopyrgus-subgenus", "source": "1961_dehm"}
- statement {"source": "1961_dehm", "kind": "act", "record": "rhenopyrgus-subgenus", "actKind": "type"}
- list {"record": "rhenopyrgus-subgenus", "source": "2013_sumrall_heredia_rodríguez.c.m_mestre"}

> Rhenopyrgus taken as the subgenus (as erected by Dehm 1961); printed forms of the subgenus name in Dehm 1961 and of its type species as cited by Sumrall et al. 2013; all years
> 
> Pyrgocystis (Rhenopyrgus) (subgenus)
>   1961 "Rhenopyrgus nov. subgen." Dehm 1961 p. 16
> 
> The classification printed in Dehm 1961 has not yet been entered (only part of it is entered so far).
> 
> Pyrgocystis (Rhenopyrgus) (subgenus)

### q028 (as-published)

Q: What exact heading and parenthetical act does Guensburg & Sprinkle (1994) print for the Rhenopyrgus subfamily?

- failure: no composed block is contents {"source": "1994_guensburg_sprinkle", "record": "rhenopyrginae"}
- failure: the answer does not show "Subfamily Rhenopyrginae emend. nom. transl."
- judge contract 2: Header names taxon, rank-variant scope, authority, source and year, limited to heading/parenthetical; no verdict or mechanism word; no clarifying question needed.

Plan: {"header": "Rhenopyrginae (subfamily, alt-rank form of Rhenopyrgidae, Holloway & Jell 1983) as printed by Guensburg & Sprinkle (1994); heading and parenthetical act only", "blocks": [{"tool": "printed_forms", "parameters": {"record": "rhenopyrginae", "source": "Guensburg & Sprinkle 1994"}}, {"tool": "statements", "parameters": {"record": "rhenopyrginae", "source": "Guensburg & Sprinkle 1994", "kind": "act"}}]}
Header: Rhenopyrginae (subfamily, alt-rank form of Rhenopyrgidae, Holloway & Jell 1983) as printed by Guensburg & Sprinkle (1994); heading and parenthetical act only
- list {"record": "rhenopyrginae", "source": "1994_guensburg_sprinkle"}
- list {"record": "rhenopyrginae", "source": "1994_guensburg_sprinkle", "kind": "act", "actKind": null}

> Rhenopyrginae (subfamily, alt-rank form of Rhenopyrgidae, Holloway & Jell 1983) as printed by Guensburg & Sprinkle (1994); heading and parenthetical act only
> 
> Rhenopyrginae (Subfamily)
> 
> Statements about Rhenopyrginae Holloway & Jell 1983
>   1994  Guensburg & Sprinkle  emended
>   1994  Guensburg & Sprinkle  nomen translatum from Rhenopyrgidae

### q029 (trajectory)

Q: Where do sources place family Rhenopyrgidae (or its subfamily-rank predecessor) across the 1983-2020 literature?

- failure: no composed block is placements {"records": ["rhenopyrgidae"]}
- failure: the answer does not show "Cyathocystidae"
- failure: the answer does not show "Edrioblastoidina"
- failure: the answer does not show "Order uncertain"
- judge contract 2: Header lists only group, rank-variant inclusion, source scope and year range in standard taxonomic language; no summary, mechanism, or verdict; no question needed.

Plan: {"header": "Family Rhenopyrgidae (and its subfamily-rank predecessor Rhenopyrginae) taken together; ancestry across all sources 1983-2020, classifications only", "blocks": [{"tool": "ancestors", "parameters": {"records": ["rhenopyrgidae", "rhenopyrginae"], "trees": "classification", "years": "1983-2020"}}], "question": null}
Header: Family Rhenopyrgidae (and its subfamily-rank predecessor Rhenopyrginae) taken together; ancestry across all sources 1983-2020, classifications only
- chains {"records": ["rhenopyrgidae", "rhenopyrginae"], "includeVariants": true, "trees": ["c", "l", "a", "s", "s", "i", "f", "i", "c", "a", "t", "i", "o", "n"], "years": ["1", "9", "8", "3", "-", "2", "0", "2", "0"]}

> Family Rhenopyrgidae (and its subfamily-rank predecessor Rhenopyrginae) taken together; ancestry across all sources 1983-2020, classifications only
> 
> Above Rhenopyrgidae Holloway & Jell 1983, Rhenopyrginae Holloway & Jell 1983
> (no source places it there)

### q030 (trajectory)

Q: Is Rhenopyrgus a genus or a subgenus of Pyrgocystis?

- failure: the answer does not show "genus since 1983"
- failure: the answer does not show "subgenus 1961–1966"
- judge contract 2: Header lists only taxon, rank variants, source scope, year range and tree type; no verdict, summary or mechanism language; no question needed.

Plan: {"header": "Rhenopyrgus (genus and subgenus rank variants) as placed relative to Pyrgocystis; all sources, all years, classification trees only", "blocks": [{"tool": "history", "parameters": {"record": "rhenopyrgus", "include_related": true, "synonymy": false, "trees": "classification", "years": "all"}}]}
Header: Rhenopyrgus (genus and subgenus rank variants) as placed relative to Pyrgocystis; all sources, all years, classification trees only
- timeline {"record": "rhenopyrgus", "includeRelated": true, "synonymy": false, "trees": ["c", "l", "a", "s", "s", "i", "f", "i", "c", "a", "t", "i", "o", "n"], "years": ["a", "l", "l"]}

> Rhenopyrgus (genus and subgenus rank variants) as placed relative to Pyrgocystis; all sources, all years, classification trees only
> 
> Rhenopyrgus Dehm 1961
> (no source uses the name)

### q032 (trajectory)

Q: What class or order has Astrocystites been placed in, across the sources that treat it?

- failure: the answer does not show "Edrioblastoidea"
- failure: the answer does not show "Protoblastoidea"
- failure: the answer does not show "Edrioblastoidina"
- judge contract 2: Header lists only scope parameters (genus, sources treating it, class/order rank, all years) in community language; no verdict, summary, or mechanism word; no question needed.

Plan: {"header": "Astrocystites (genus); classification history across all sources that treat it, showing the class or order it has been placed under; all years", "blocks": [{"tool": "ancestors", "parameters": {"records": ["astrocystites"], "trees": "classifications", "years": "all"}}]}
Header: Astrocystites (genus); classification history across all sources that treat it, showing the class or order it has been placed under; all years
- chains {"records": ["astrocystites"], "includeVariants": true, "trees": ["c", "l", "a", "s", "s", "i", "f", "i", "c", "a", "t", "i", "o", "n", "s"], "years": ["a", "l", "l"]}

> Astrocystites (genus); classification history across all sources that treat it, showing the class or order it has been placed under; all years
> 
> Above Astrocystites Whiteaves 1897
> (no source places it there)

### q034 (trajectory)

Q: Who does the corpus credit as the author of Cambraster, and does every source agree?

- failure: no composed block is printed_forms {"record": "cambraster"}
- failure: the answer does not show "Cabibel, Termier, and Termier, 1958"
- judge contract 2: Header names only the genus scope, the attribution field tracked, and an unrestricted year range; no verdict, summary, or mechanism wording; no question needed.

Plan: {"header": "Cambraster taken as the genus; authorship as credited by each source; all years", "blocks": [{"tool": "history", "parameters": {"record": "Cambraster", "include_related": false}}]}
Header: Cambraster taken as the genus; authorship as credited by each source; all years
- timeline {"record": "cambraster", "includeRelated": false, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Cambraster taken as the genus; authorship as credited by each source; all years
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

### q036 (trajectory)

Q: At what rank do the sources treat Edrioblastoidea: a class, an order, or a suborder?

- failure: no composed block is history {"record": "edrioblastoidea"}
- failure: the answer does not show "order since 1990"
- failure: the answer does not show "suborder 1994–2020"
- failure: the answer does not show "class 1962–1982"
- judge contract 2: Header lists only group, rank variants, tree type, and year range in neutral taxonomic language; no verdict or mechanism; no question asked.

Plan: {"header": "Edrioblastoidea taken together with its variant ranks (Edrioblastoida, Edrioblastoidina); classifications only; all years", "blocks": [{"tool": "history", "parameters": {"record": "edrioblastoidea", "include_related": true, "years": true}}]}
Plan errors: [{"block": 1, "tool": "history", "parameters": {"record": "edrioblastoidea", "include_related": true, "years": true}, "error": "'bool' object is not iterable"}]
Header: Edrioblastoidea taken together with its variant ranks (Edrioblastoida, Edrioblastoidina); classifications only; all years

> 

### q041 (trajectory)

Q: Which papers in the corpus treat edrioblastoids, and what does each do to the group?

- failure: the answer does not show "named as new"
- failure: the answer does not show "nomen translatum"
- failure: the answer does not show "Smith & Jell"
- judge contract 2: Header names only group, rank variants, synonymy setting, and year span in taxonomic language; no verdict, summary, or mechanism; no question posed.

Plan: {"header": "Edrioblastoidea taken as the class and its variant-rank forms (Edrioblastoida, Edrioblastoidina); synonymy included; all years", "blocks": [{"tool": "history", "parameters": {"record": "edrioblastoidea", "include_related": true, "synonymy": true, "trees": "all", "years": "all"}}]}
Header: Edrioblastoidea taken as the class and its variant-rank forms (Edrioblastoida, Edrioblastoidina); synonymy included; all years
- timeline {"record": "edrioblastoidea", "includeRelated": true, "synonymy": true, "trees": ["a", "l", "l"], "years": ["a", "l", "l"]}

> Edrioblastoidea taken as the class and its variant-rank forms (Edrioblastoida, Edrioblastoidina); synonymy included; all years
> 
> Edrioblastoidea Fay 1962
> (no source uses the name)

### q042 (trajectory)

Q: What genera and species have ever been classified as edrioblastoids by any definition, and which of those placements were later abandoned by some sources?

- failure: the answer does not show "Astrocystites"
- failure: the answer does not show "Cambroblastus"
- failure: the answer does not show "Steganoblastidae"
- judge contract 2: Header lists only group scope, rank variants, synonym inclusion, tree and year coverage in standard taxonomic terms; no verdict, summary, or mechanism; no question needed.

Plan: {"header": "Edrioblastoidea taken as the class together with its order/suborder-rank variants (Edrioblastoida, Edrioblastoidina); genus- and species-level members ever placed within it, synonyms and variant names included; all classification trees; all years", "blocks": [{"tool": "descendants", "parameters": {"records": ["edrioblastoidea", "edrioblastoida", "edrioblastoidina"], "include_synonyms": true, "include_variants": true, "trees": "all", "years": "all"}}]}
Header: Edrioblastoidea taken as the class together with its order/suborder-rank variants (Edrioblastoida, Edrioblastoidina); genus- and species-level members ever placed within it, synonyms and variant names included; all classification trees; all years
- table {"records": ["edrioblastoidea", "edrioblastoida", "edrioblastoidina"], "includeSynonyms": true, "includeVariants": true, "trees": ["a", "l", "l"], "years": ["a", "l", "l"]}

> Edrioblastoidea taken as the class together with its order/suborder-rank variants (Edrioblastoida, Edrioblastoidina); genus- and species-level members ever placed within it, synonyms and variant names included; all classification trees; all years
> 
> Placed under Edrioblastoidea, Edrioblastoida, Edrioblastoidina
> record  rank  placed by  sources
> ------  ----  ---------  -------

### q043 (trajectory)

Q: At what rank has the edrioblastoid group been treated, and by which co-author sets, over time?

- failure: the answer does not show "co-author sets"
- failure: the answer does not show "order since 1990"
- judge contract 2: Header names group, rank variants, synonym exclusion, and full year span in community language; no summary, mechanism, or verdict; no question needed.

Plan: {"header": "Edrioblastoidea taken as the class and its variant ranks (Edrioblastoida, Edrioblastoidina); synonyms not separately included; classification history across all years", "blocks": [{"tool": "history", "parameters": {"record": "edrioblastoidea", "include_related": true, "synonymy": false, "trees": "all", "years": "all"}}]}
Header: Edrioblastoidea taken as the class and its variant ranks (Edrioblastoida, Edrioblastoidina); synonyms not separately included; classification history across all years
- timeline {"record": "edrioblastoidea", "includeRelated": true, "synonymy": false, "trees": ["a", "l", "l"], "years": ["a", "l", "l"]}

> Edrioblastoidea taken as the class and its variant ranks (Edrioblastoida, Edrioblastoidina); synonyms not separately included; classification history across all years
> 
> Edrioblastoidea Fay 1962
> (no source uses the name)

### q044 (trajectory)

Q: Which family name has been used for Astrocystites and by whom, Steganoblastidae or Astrocystitidae?

- failure: no composed block is history {"record": "astrocystites"}
- judge contract 2: Header names genus, the two competing family placements, full year range and ordering; no summary, mechanism or verdict; no unnecessary question.

Plan: {"header": "Astrocystites (genus, Whiteaves 1897) as placed under Steganoblastidae and under Astrocystitidae; all years, sources in year order", "blocks": [{"tool": "placed_under", "parameters": {"record": "Astrocystites", "parent": "Steganoblastidae"}}, {"tool": "placed_under", "parameters": {"record": "Astrocystites", "parent": "Astrocystitidae"}}]}
Header: Astrocystites (genus, Whiteaves 1897) as placed under Steganoblastidae and under Astrocystitidae; all years, sources in year order
- chains {"record": "astrocystites", "parent": "steganoblastidae", "includeVariants": true, "trees": ["taxonomy"], "years": null}
- chains {"record": "astrocystites", "parent": "astrocystitidae", "includeVariants": true, "trees": ["taxonomy"], "years": null}

> Astrocystites (genus, Whiteaves 1897) as placed under Steganoblastidae and under Astrocystitidae; all years, sources in year order
> 
> Astrocystites Whiteaves 1897 under Steganoblastidae Bather 1900: 2 papers, 2 co-author sets, 1968–1982
> first Webby 1968, last Sprinkle 1982
> 
> 1968  Webby     Astrocystites
> 1982  Sprinkle  Astrocystites
> 
> Astrocystites Whiteaves 1897 under Astrocystitidae Bassler 1935: 6 papers, 6 co-author sets, 1935–1994
> first Bassler 1935, last Guensburg & Sprinkle 1994
> 
> 1935  Bassler               Astrocystites
> 1967  Fay                   Astrocystites
> 1970  Mintz                 Astrocystites
> 1980  Bell                  Astrocystites
> 1990  Smith & Jell          Astrocystites
> 1994  Guensburg & Sprinkle  Astrocystites

### q045 (trajectory)

Q: Who proposed placing rhenopyrgids inside Cyathocystidae, who followed, and who rejected it?

- failure: no composed block is placements {"records": ["rhenopyrgidae"]}
- failure: the answer does not show "not Cyathocystidae"
- judge contract 2: Header names taxon, rank-variant inclusion, parent of interest, and full source/year scope; no summary, mechanism, or verdict; no question needed.

Plan: {"header": "Rhenopyrgidae (including the rank variant Rhenopyrginae) as placed under Cyathocystidae; all sources, all years", "blocks": [{"tool": "placed_under", "parameters": {"record": "Rhenopyrgidae", "parent": "Cyathocystidae"}}]}
Header: Rhenopyrgidae (including the rank variant Rhenopyrginae) as placed under Cyathocystidae; all sources, all years
- chains {"record": "rhenopyrgidae", "parent": "cyathocystidae", "includeVariants": true, "trees": ["taxonomy"], "years": null}

> Rhenopyrgidae (including the rank variant Rhenopyrginae) as placed under Cyathocystidae; all sources, all years
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
- judge contract 2: Header names taxon, the two sources/trees compared, and year range; neutral wording, no summary or verdict; absent question is acceptable here.

Plan: {"header": "Pyrgocystis octogona (Richter 1930): what Holloway & Jell (1983) state about Dehm (1961)'s treatment of the species, and Dehm (1961)'s own statements about it; all years", "blocks": [{"tool": "statements", "parameters": {"record": "octogona_richter.r_1930", "source": "Holloway & Jell 1983"}}, {"tool": "statements", "parameters": {"record": "octogona_richter.r_1930", "source": "Dehm 1961"}}]}
Header: Pyrgocystis octogona (Richter 1930): what Holloway & Jell (1983) state about Dehm (1961)'s treatment of the species, and Dehm (1961)'s own statements about it; all years
- statement {"source": "1983_holloway_jell", "kind": null, "record": "octogona_richter.r_1930", "actKind": null}
- list {"record": "octogona_richter.r_1930", "source": "1961_dehm", "kind": null, "actKind": null}

> Pyrgocystis octogona (Richter 1930): what Holloway & Jell (1983) state about Dehm (1961)'s treatment of the species, and Dehm (1961)'s own statements about it; all years
> 
> The classification printed in Holloway & Jell 1983 is entered in full.
> 
> Statements about Pyrgocystis octogona Richter 1930
>   1961  Dehm  cites the name (cited p. 294)
>   1961  Dehm  places it under Pyrgocystis (cited p. 294)
>   1961  Dehm  occurrence: Lower Devonian; greywacke slates; Bornich, near Weisel on the Rhine, Germany (cited p. 294)

### q049 (trajectory)

Q: Which cladistic analyses in the corpus include Rhenopyrgus, and where does each place it?

- failure: no composed block is placements {"records": ["rhenopyrgus"], "trees": ["cladogram"]}
- failure: the answer does not show "Smith & Jell"
- failure: the answer does not show "Guensburg & Sprinkle"
- failure: the answer does not show "Sumrall et al."
- judge contract 2: Header lists only group with rank variants, tree-only restriction, and unrestricted years; no summary, mechanism or verdict; no question needed.

Plan: {"header": "Rhenopyrgus taken as the genus and its subgenus form; phylogenetic trees only; all years", "blocks": [{"tool": "ancestors", "parameters": {"records": ["rhenopyrgus", "rhenopyrgus-subgenus"], "trees": "phylogeny", "years": "all"}}]}
Header: Rhenopyrgus taken as the genus and its subgenus form; phylogenetic trees only; all years
- chains {"records": ["rhenopyrgus", "rhenopyrgus-subgenus"], "includeVariants": true, "trees": ["p", "h", "y", "l", "o", "g", "e", "n", "y"], "years": ["a", "l", "l"]}

> Rhenopyrgus taken as the genus and its subgenus form; phylogenetic trees only; all years
> 
> Above Rhenopyrgus Dehm 1961, Pyrgocystis (Rhenopyrgus) Dehm 1961
> (no source places it there)

