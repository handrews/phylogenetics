# Grades for `2026-09-14-planner-d-claude-sonnet-5.jsonl`

| class | questions | mechanical pass |
|---|---|---|
| absent | 3 | 3 |
| answerable | 12 | 11 |
| as-published | 8 | 5 |
| trajectory | 15 | 13 |
| uncaptured | 9 | 9 |

## Failures and notes

### q001 (answerable)

Q: What new class does Fay (1962) erect for the genus Astrocystites, and what family/order sit between the genus and the class?

- failure: no composed block is contents {"source": "1962_fay", "record": "edrioblastoidea"}
- failure: the answer does not show "Class Edrioblastoidea nov."
- failure: the answer does not show "Genus Astrocystites"
- judge contract 2: Header lists only scope parameters—genus, higher chain, classification-only, 1962 year limit—in standard terms, with no verdict, summary, or mechanism; no question asked.

Plan: {"header": "Astrocystites (genus); chain of taxa above it accepted by Fay (1962); classification only; year restricted to 1962", "blocks": [{"tool": "ancestors", "parameters": {"records": ["astrocystites"], "trees": ["taxonomy"], "years": [1962, 1962]}}]}
Header: Astrocystites (genus); chain of taxa above it accepted by Fay (1962); classification only; year restricted to 1962
- chains {"records": ["astrocystites"], "includeVariants": true, "trees": ["taxonomy"], "years": [1962, 1962]}

> Astrocystites (genus); chain of taxa above it accepted by Fay (1962); classification only; year restricted to 1962
> 
> Above Astrocystites Whiteaves 1897: 1 paper, 1 co-author set, 1962
> 
> 1962  Fay  Edrioblastoidea › Astrocystites

### q021 (as-published)

Q: What exact suborder heading do Ewin et al. (2020) print above family Rhenopyrgidae, and at what rank was that name first established?

- failure: no composed block is printed_forms {"record": "edrioblastoidina", "source": "2020_ewin_martin.m_isotalo_zamora"}
- failure: no composed block is history {"record": "edrioblastoidina"}
- failure: the answer does not show "Suborder Edrioblastoidina Fay, 1962"
- failure: the answer does not show "class 1962–1982"
- judge contract 2: States only scope parameters: name group with rank variant, taxonomy trees, source restriction, year range; no verdict, no summary; no question needed.

Plan: {"header": "Rhenopyrgidae (family, with its subfamily-rank form Rhenopyrginae as the same name group) considered; classificatory (taxonomy) trees only; ancestors restricted to Ewin et al. 2020 for the suborder heading, history taken across all years including the related rank to find when the name was first established", "blocks": [{"tool": "ancestors", "parameters": {"records": ["rhenopyrgidae"], "trees": ["taxonomy"], "years": [2020, 2020]}}, {"tool": "history", "parameters": {"record": "rhenopyrgidae", "include_related": true, "trees": ["taxonomy"]}}]}
Header: Rhenopyrgidae (family, with its subfamily-rank form Rhenopyrginae as the same name group) considered; classificatory (taxonomy) trees only; ancestors restricted to Ewin et al. 2020 for the suborder heading, history taken across all years including the related rank to find when the name was first established
- chains {"records": ["rhenopyrgidae"], "includeVariants": true, "trees": ["taxonomy"], "years": [2020, 2020]}
- timeline {"record": "rhenopyrgidae", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Rhenopyrgidae (family, with its subfamily-rank form Rhenopyrginae as the same name group) considered; classificatory (taxonomy) trees only; ancestors restricted to Ewin et al. 2020 for the suborder heading, history taken across all years including the related rank to find when the name was first established
> 
> Above Rhenopyrgidae Holloway & Jell 1983: 1 paper, 1 co-author set, 2020
> 
> 2020  Ewin et al.  Echinodermata › Edrioasteroidea › Edrioasterida › Edrioblastoidina › Rhenopyrgidae
> 
> Rhenopyrgidae Holloway & Jell 1983: 7 papers, 7 co-author sets, 1983–2020
> family since 1983 (5 papers), subfamily 1994–2000 (2 papers)
> in Edrioblastoidina since 2013 (3 papers), in Isorophida 2010 (1 paper), in Cyathocystidae 1994–2000 (2 papers), in Order uncertain 1983 (1 paper)
> 
> 1983  Holloway & Jell       Rhenopyrgidae, in Order uncertain; named as new
> 1994  Guensburg & Sprinkle  Rhenopyrginae, in Cyathocystidae; emended; nomen translatum from Rhenopyrgidae
> 2000  Grigo                 Rhenopyrginae, in Cyathocystidae
> 2010  Müller & Hahn         Rhenopyrgidae, in Isorophida
> 2013  Sumrall et al.        Rhenopyrgidae, in Edrioblastoidina; emended; moved from Cyathocystidae; declines a placement in Cyathocystidae
> 2017  Briggs et al.         Rhenopyrgidae, in Edrioblastoidina
> 2020  Ewin et al.           Rhenopyrgidae, in Edrioblastoidina; emended (p. 118)

### q024 (as-published)

Q: How did Dehm (1961) style the new subgenus name Rhenopyrgus, and how do Sumrall et al. (2013) cite the type species using that name?

- failure: no composed block is printed_forms {"record": "coronaeformis_rievers_1961", "source": "2013_sumrall_heredia_rodríguez.c.m_mestre"}
- failure: the answer does not show "Pyrgocystis (Rhenopyrgus) coronaeformis Rievers, 1961"
- judge contract 2: Header names the taxon, notes inclusion of subgenus-rank usage, scope of years, and restates the parameters without verdict, summary, or mechanism wording.

Plan: {"header": "Rhenopyrgus taken as the genus (with its subgenus-rank use by Dehm); how Dehm (1961) printed the new subgenus name and how Sumrall et al. (2013) cite the type species under that name; all years", "blocks": [{"tool": "printed_forms", "parameters": {"record": "rhenopyrgus-subgenus", "source": "Dehm 1961"}}, {"tool": "contents", "parameters": {"record": "rhenopyrgus", "source": "Sumrall et al. 2013"}}]}
Header: Rhenopyrgus taken as the genus (with its subgenus-rank use by Dehm); how Dehm (1961) printed the new subgenus name and how Sumrall et al. (2013) cite the type species under that name; all years
- list {"record": "rhenopyrgus-subgenus", "source": "1961_dehm"}
- classification {"source": "2013_sumrall_heredia_rodríguez.c.m_mestre", "record": "rhenopyrgus", "depth": null, "synonymy": false, "path": "0/children/0/children/0/children/0/children/0/children/0"}

> Rhenopyrgus taken as the genus (with its subgenus-rank use by Dehm); how Dehm (1961) printed the new subgenus name and how Sumrall et al. (2013) cite the type species under that name; all years
> 
> Pyrgocystis (Rhenopyrgus) (subgenus)
>   1961 "Rhenopyrgus nov. subgen." Dehm 1961 p. 16
> 
> Sumrall et al. 2013
>   Genus Rhenopyrgus emend.
>     Type species. Rhenopyrgus coronaeformis
>     Rhenopyrgus coronaeformis
>     Rhenopyrgus piojoensis sp. nov.
>     Rhenopyrgus whitei
>     Rhenopyrgus flos

### q028 (as-published)

Q: What exact heading and parenthetical act does Guensburg & Sprinkle (1994) print for the Rhenopyrgus subfamily?

- failure: no composed block is contents {"source": "1994_guensburg_sprinkle", "record": "rhenopyrginae"}
- failure: the answer does not show "Subfamily Rhenopyrginae emend. nom. transl."
- note: text beside the submission: No subfamily-rank record named "Rhenopyrgus" exists in the corpus — only genus a
- judge contract 0: Header states no parameters; instead it delivers a verdict/summary ('no subfamily-rank taxon present', 'reporting the gap'), and asks no clarifying question.

Plan: {"header": "No subfamily-rank taxon named Rhenopyrgus is present in the corpus (only genus and subgenus records exist); reporting the gap for that name", "blocks": [{"tool": "gap", "parameters": {"name": "Rhenopyrgus (subfamily)"}}], "question": null}
Header: No subfamily-rank taxon named Rhenopyrgus is present in the corpus (only genus and subgenus records exist); reporting the gap for that name
- statement {"name": "Rhenopyrgus (subfamily)"}

> No subfamily-rank taxon named Rhenopyrgus is present in the corpus (only genus and subgenus records exist); reporting the gap for that name
> 
> No source in the corpus mentions the name Rhenopyrgus (subfamily).

### q034 (trajectory)

Q: Who does the corpus credit as the author of Cambraster, and does every source agree?

- failure: no composed block is printed_forms {"record": "cambraster"}
- failure: the answer does not show "Cabibel, Termier, and Termier, 1958"
- judge contract 2: Header names only taxon scope, synonym/rank exclusion, and year range in neutral community language; no verdict, summary, or mechanism word; no question needed.

Plan: {"header": "Authorship of the genus Cambraster (as printed by each source that treats it); no synonyms or variant ranks included; all years", "blocks": [{"tool": "history", "parameters": {"record": "cambraster", "include_related": false}}]}
Header: Authorship of the genus Cambraster (as printed by each source that treats it); no synonyms or variant ranks included; all years
- timeline {"record": "cambraster", "includeRelated": false, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Authorship of the genus Cambraster (as printed by each source that treats it); no synonyms or variant ranks included; all years
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

### q035 (trajectory)

Q: Is Isorophus (and its sibling genus Carneyella) attributed to Foerste 1916 or 1917?

- failure: no composed block is history {"record": "isorophus"}
- failure: no composed block is history {"record": "carneyella"}
- failure: the answer does not show "Isorophus Foerste 1916"
- failure: the answer does not show "Carneyella Foerste 1916"
- judge contract 2: Header names taxa, rank, sources, and full year range in community language; states the 1916/1917 comparison as scope, not verdict; no question needed.

Plan: {"header": "Isorophus and Carneyella (genus-rank records) as printed by each source; verbatim printed forms across all years to compare the Foerste 1916 vs 1917 attribution", "blocks": [{"tool": "printed_forms", "parameters": {"record": "Isorophus"}}, {"tool": "printed_forms", "parameters": {"record": "Carneyella"}}]}
Header: Isorophus and Carneyella (genus-rank records) as printed by each source; verbatim printed forms across all years to compare the Foerste 1916 vs 1917 attribution
- list {"record": "isorophus", "source": null}
- list {"record": "carneyella", "source": null}

> Isorophus and Carneyella (genus-rank records) as printed by each source; verbatim printed forms across all years to compare the Foerste 1916 vs 1917 attribution
> 
> Isorophus (genus)
>   1994 "Isorophus Foerste, 1917" Guensburg & Sprinkle 1994
> 
> Carneyella (genus)
>   1994 "Carneyella Foerste, 1917" Guensburg & Sprinkle 1994

