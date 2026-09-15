# Grades for `2026-09-14-planner-c-claude-sonnet-5.jsonl`

| class | questions | mechanical pass |
|---|---|---|
| absent | 3 | 3 |
| answerable | 12 | 9 |
| as-published | 8 | 5 |
| trajectory | 15 | 10 |
| uncaptured | 9 | 9 |

## Failures and notes

### q001 (answerable)

Q: What new class does Fay (1962) erect for the genus Astrocystites, and what family/order sit between the genus and the class?

- failure: no composed block is contents {"source": "1962_fay", "record": "edrioblastoidea"}
- failure: the answer does not show "Class Edrioblastoidea nov."
- failure: the answer does not show "Genus Astrocystites"
- judge contract 2: Header lists only scope parameters—genus, source/year restriction, taxonomy tree—in neutral taxonomic language, no verdict or summary; no question needed since answerable.

Plan: {"header": "Astrocystites (genus); classification chain given by Fay 1962; taxonomy tree only; year restricted to 1962", "blocks": [{"tool": "ancestors", "parameters": {"records": ["astrocystites"], "trees": ["taxonomy"], "years": [1962, 1962]}}]}
Header: Astrocystites (genus); classification chain given by Fay 1962; taxonomy tree only; year restricted to 1962
- chains {"records": ["astrocystites"], "includeVariants": true, "trees": ["taxonomy"], "years": [1962, 1962]}

> Astrocystites (genus); classification chain given by Fay 1962; taxonomy tree only; year restricted to 1962
> 
> Above Astrocystites Whiteaves 1897: 1 paper, 1 co-author set, 1962
> 
> 1962  Fay  Edrioblastoidea › Astrocystites

### q002 (answerable)

Q: Does Fay (1962) himself write that ottawaensis is the type species of Astrocystites, or is that flag the editor's own inference?

- failure: no composed block is statements {"record": "ottawaensis_whiteaves_1897", "source": "1962_fay"}
- failure: the answer does not show "(editor)"
- judge contract 2: Header names genus, authority, source paper and the precise parameter at issue in taxonomic language; no verdict, no mechanism talk; no unnecessary question asked.

Plan: {"header": "Astrocystites (genus, Whiteaves 1897); checking whether Fay 1962 himself designates ottawaensis as the type species", "blocks": [{"tool": "statements", "parameters": {"record": "astrocystites", "source": "1962_fay", "act_kind": "type"}}, {"tool": "contents", "parameters": {"source": "1962_fay", "record": "astrocystites"}}]}
Header: Astrocystites (genus, Whiteaves 1897); checking whether Fay 1962 himself designates ottawaensis as the type species
- statement {"record": "astrocystites", "source": "1962_fay", "kind": "skeleton", "actKind": "type", "statementKind": null}
- classification {"source": "1962_fay", "record": "astrocystites", "depth": null, "synonymy": false, "path": "0/children/0"}

> Astrocystites (genus, Whiteaves 1897); checking whether Fay 1962 himself designates ottawaensis as the type species
> 
> The classification printed in Fay 1962 is entered in full.
> 
> Fay 1962
>   Genus Astrocystites (moved from Edrioasteroidea)
>     Type species. Astrocystites ottawaensis
>     Astrocystites ottawaensis

### q009 (answerable)

Q: What new species of Rhenopyrgus does Grigo (2000) describe, and from where?

- failure: no composed block is contents {"source": "2000_grigo", "record": "rhenopyrgus"}
- failure: no composed block is gap {"source": "2000_grigo", "kind": "occurrences"}
- failure: the answer does not show "Rhenopyrgus sp. nov."
- judge contract 1: Parameters (genus, year 2000) stated in proper terms and no verdict, but the "(draft, will refine)" process aside is an extraneous non-parameter lapse.

Plan: {"header": "Probe: species placed under Rhenopyrgus by sources published in 2000, to identify Grigo's new species (draft, will refine)", "blocks": [{"tool": "descendants", "parameters": {"records": ["rhenopyrgus"], "years": [2000, 2000]}}]}
Header: Probe: species placed under Rhenopyrgus by sources published in 2000, to identify Grigo's new species (draft, will refine)
- table {"records": ["rhenopyrgus"], "includeSynonyms": true, "includeVariants": true, "trees": ["taxonomy"], "years": [2000, 2000]}

> Probe: species placed under Rhenopyrgus by sources published in 2000, to identify Grigo's new species (draft, will refine)
> 
> Placed under Rhenopyrgus
> record                     rank     placed by                      sources
> -------------------------  -------  -----------------------------  -------
> Rhenopyrgus sp.            species  Grigo 2000: under Rhenopyrgus  1
> Rhenopyrgus coronaeformis  species  Grigo 2000: under Rhenopyrgus  1

### q021 (as-published)

Q: What exact suborder heading do Ewin et al. (2020) print above family Rhenopyrgidae, and at what rank was that name first established?

- failure: no composed block is printed_forms {"record": "edrioblastoidina", "source": "2020_ewin_martin.m_isotalo_zamora"}
- failure: no composed block is history {"record": "edrioblastoidina"}
- failure: the answer does not show "Suborder Edrioblastoidina Fay, 1962"
- failure: the answer does not show "class 1962–1982"
- note: composed after the lookup limit was reached
- judge contract 0: Header pre-answers the question by asserting the suborder heading is Isorophina, a verdict on the disputed point, and asks no clarifying question despite that ambiguity.

Plan: {"header": "Suborder heading above Rhenopyrgidae taken as Isorophina (with its subfamily-rank variant Isorophinae); first block restricted to Ewin et al. 2020 to show the exact heading printed above the family, second block giving the full rank history of the Isorophina/Isorophinae name group across all sources and years; classifications (taxonomy) only", "blocks": [{"tool": "ancestors", "parameters": {"records": ["rhenopyrgidae"], "trees": ["taxonomy"], "years": [2020, 2020]}}, {"tool": "history", "parameters": {"record": "isorophina", "include_related": true, "trees": ["taxonomy"]}}], "question": null}
Header: Suborder heading above Rhenopyrgidae taken as Isorophina (with its subfamily-rank variant Isorophinae); first block restricted to Ewin et al. 2020 to show the exact heading printed above the family, second block giving the full rank history of the Isorophina/Isorophinae name group across all sources and years; classifications (taxonomy) only
- chains {"records": ["rhenopyrgidae"], "includeVariants": true, "trees": ["taxonomy"], "years": [2020, 2020]}
- timeline {"record": "isorophina", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Suborder heading above Rhenopyrgidae taken as Isorophina (with its subfamily-rank variant Isorophinae); first block restricted to Ewin et al. 2020 to show the exact heading printed above the family, second block giving the full rank history of the Isorophina/Isorophinae name group across all sources and years; classifications (taxonomy) only
> 
> Above Rhenopyrgidae Holloway & Jell 1983: 1 paper, 1 co-author set, 2020
> 
> 2020  Ewin et al.  Echinodermata › Edrioasteroidea › Edrioasterida › Edrioblastoidina › Rhenopyrgidae
> 
> Isorophina Bell 1976: 16 papers, 11 co-author sets, 1976–2011
> suborder since 1976 (16 papers), subfamily 1985 (1 paper)
> in Isorophida since 1976 (16 papers, 11 co-author sets), in Agelacrinitidae 1985 (1 paper)
> 
> 1976  Bell               Isorophina, in Isorophida; named as new
> 1976  Bell & Petersen    Isorophina, in Isorophida
> 1979  Guensburg          Isorophina, in Isorophida
> 1980  Bell               Isorophina, in Isorophida
> 1985  Smith              Isorophina, in Isorophida
> 1985  Smith              Isorophinae, in Agelacrinitidae; nomen translatum from Isorophina
> 1987  Smith & Arbizu     Isorophinae, cited as a synonym of Agelacrinitinae
> 1992  Sumrall            Isorophina, in Isorophida
> 1996  Sumrall            Isorophina, in Isorophida
> 1996  Sumrall & Bowsher  Isorophina, in Isorophida
> 2000  Sumrall et al.     Isorophina, in Isorophida
> 2001  Sumrall            Isorophina, in Isorophida
> 2006  Sumrall et al.     Isorophina, in Isorophida
> 2006  Sumrall et al.     Isorophina, in Isorophida
> 2009  Sumrall            Isorophina, in Isorophida
> 2009  Sumrall et al.     Isorophina, in Isorophida
> 2010  Sumrall            Isorophina, in Isorophida
> 2011  Sumrall & Zamora   Isorophina, in Isorophida

### q024 (as-published)

Q: How did Dehm (1961) style the new subgenus name Rhenopyrgus, and how do Sumrall et al. (2013) cite the type species using that name?

- failure: no composed block is printed_forms {"record": "coronaeformis_rievers_1961", "source": "2013_sumrall_heredia_rodríguez.c.m_mestre"}
- failure: the answer does not show "Pyrgocystis (Rhenopyrgus) coronaeformis Rievers, 1961"
- judge contract 2: Header lists only record choice, rank variant, source scope and year range in neutral taxonomic language; no verdict, summary, or mechanism; no question asked.

Plan: {"header": "Rhenopyrgus taken as the subgenus-rank record (Dehm 1961); usage statements in Sumrall et al. 2013; all years", "blocks": [{"tool": "printed_forms", "parameters": {"record": "rhenopyrgus-subgenus", "source": "Dehm 1961"}}, {"tool": "statements", "parameters": {"record": "rhenopyrgus-subgenus", "source": "Sumrall et al. 2013", "kind": "usage"}}]}
Header: Rhenopyrgus taken as the subgenus-rank record (Dehm 1961); usage statements in Sumrall et al. 2013; all years
- list {"record": "rhenopyrgus-subgenus", "source": "1961_dehm"}
- list {"record": "rhenopyrgus-subgenus", "source": "2013_sumrall_heredia_rodríguez.c.m_mestre", "kind": "usage", "actKind": null}

> Rhenopyrgus taken as the subgenus-rank record (Dehm 1961); usage statements in Sumrall et al. 2013; all years
> 
> Pyrgocystis (Rhenopyrgus) (subgenus)
>   1961 "Rhenopyrgus nov. subgen." Dehm 1961 p. 16
> 
> Statements about Pyrgocystis (Rhenopyrgus) Dehm 1961
>   2013  Sumrall et al.  cites the name

### q028 (as-published)

Q: What exact heading and parenthetical act does Guensburg & Sprinkle (1994) print for the Rhenopyrgus subfamily?

- failure: no composed block is contents {"source": "1994_guensburg_sprinkle", "record": "rhenopyrginae"}
- failure: the answer does not show "Subfamily Rhenopyrginae emend. nom. transl."
- judge contract 2: Header names only the taxon (with rank variants), source and year; no summary, mechanism term or verdict; no question needed.

Plan: {"header": "Printed heading for the subfamily Rhenopyrginae (as the name Rhenopyrgidae/Rhenopyrginae group) in Guensburg & Sprinkle 1994", "blocks": [{"tool": "printed_forms", "parameters": {"record": "rhenopyrginae", "source": "1994_guensburg_sprinkle"}}]}
Header: Printed heading for the subfamily Rhenopyrginae (as the name Rhenopyrgidae/Rhenopyrginae group) in Guensburg & Sprinkle 1994
- list {"record": "rhenopyrginae", "source": "1994_guensburg_sprinkle"}

> Printed heading for the subfamily Rhenopyrginae (as the name Rhenopyrgidae/Rhenopyrginae group) in Guensburg & Sprinkle 1994
> 
> Rhenopyrginae (Subfamily)

### q034 (trajectory)

Q: Who does the corpus credit as the author of Cambraster, and does every source agree?

- failure: no composed block is printed_forms {"record": "cambraster"}
- failure: the answer does not show "Cabibel, Termier, and Termier, 1958"
- judge contract 2: Header lists only scope parameters (genus record, synonyms excluded, all classifications, all years) in standard terms, passes no verdict; no question needed.

Plan: {"header": "Cambraster (genus); authorship as credited across all sources; no synonyms/variants beyond this record; all classifications; all years", "blocks": [{"tool": "history", "parameters": {"record": "cambraster"}}]}
Header: Cambraster (genus); authorship as credited across all sources; no synonyms/variants beyond this record; all classifications; all years
- timeline {"record": "cambraster", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Cambraster (genus); authorship as credited across all sources; no synonyms/variants beyond this record; all classifications; all years
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
- judge contract 1: Parameters and neutral framing are fine, but "its sibling genus" asserts a phylogenetic relationship rather than merely naming the second record scoped.

Plan: {"header": "Isorophus and its sibling genus Carneyella: verbatim printed forms of the name across all sources, to compare the authority year (Foerste 1916 vs 1917) as cited", "blocks": [{"tool": "printed_forms", "parameters": {"record": "Isorophus"}}, {"tool": "printed_forms", "parameters": {"record": "Carneyella"}}]}
Header: Isorophus and its sibling genus Carneyella: verbatim printed forms of the name across all sources, to compare the authority year (Foerste 1916 vs 1917) as cited
- list {"record": "isorophus", "source": null}
- list {"record": "carneyella", "source": null}

> Isorophus and its sibling genus Carneyella: verbatim printed forms of the name across all sources, to compare the authority year (Foerste 1916 vs 1917) as cited
> 
> Isorophus (genus)
>   1994 "Isorophus Foerste, 1917" Guensburg & Sprinkle 1994
> 
> Carneyella (genus)
>   1994 "Carneyella Foerste, 1917" Guensburg & Sprinkle 1994

### q038 (absent)

Q: What does Klug et al. (2008) themselves print in their protologue for Rhenopyrgus flos?

- note: text beside the submission: The corpus does not contain a paper by Klug et al. (2008), so no protologue text
- judge contract 1: Header names no search parameters and instead announces the conclusion ('corpus has no source'), a summary verdict; otherwise brief and no question needed.

Plan: {"header": "Gap: the corpus has no source \"Klug et al. 2008\" for Rhenopyrgus flos", "blocks": [{"tool": "gap", "parameters": {"source": "Klug et al. 2008"}}]}
Header: Gap: the corpus has no source "Klug et al. 2008" for Rhenopyrgus flos
- statement {"source": "Klug et al. 2008", "kind": "skeleton"}

> Gap: the corpus has no source "Klug et al. 2008" for Rhenopyrgus flos
> 
> No source in the corpus mentions the source Klug et al. 2008.

### q039 (absent)

Q: Which sources place the genus Rhenoblastus, and where?

- note: text beside the submission: No source in the corpus carries the name "Rhenoblastus."
- judge contract 1: Header announces the conclusion (name absent) rather than merely stating search parameters; one verdict-like lapse, otherwise neutral wording and no spurious question.

Plan: {"header": "Gap: no source in the corpus carries the name \"Rhenoblastus\"", "blocks": [{"tool": "gap", "parameters": {"name": "Rhenoblastus"}}]}
Header: Gap: no source in the corpus carries the name "Rhenoblastus"
- statement {"name": "Rhenoblastus"}

> Gap: no source in the corpus carries the name "Rhenoblastus"
> 
> No source in the corpus mentions the name Rhenoblastus.

### q044 (trajectory)

Q: Which family name has been used for Astrocystites and by whom, Steganoblastidae or Astrocystitidae?

- failure: no composed block is history {"record": "astrocystites"}
- judge contract 2: Header names the genus, the two competing family names as the contrast, and 'all years'; no verdict, summary, or mechanism language; omitting a question is acceptable.

Plan: {"header": "Astrocystites (genus, Whiteaves 1897): sources placing it under Steganoblastidae vs. Astrocystitidae; all years", "blocks": [{"tool": "placed_under", "parameters": {"record": "astrocystites", "parent": "Steganoblastidae"}}, {"tool": "placed_under", "parameters": {"record": "astrocystites", "parent": "Astrocystitidae"}}]}
Header: Astrocystites (genus, Whiteaves 1897): sources placing it under Steganoblastidae vs. Astrocystitidae; all years
- chains {"record": "astrocystites", "parent": "steganoblastidae", "includeVariants": true, "trees": ["taxonomy"], "years": null}
- chains {"record": "astrocystites", "parent": "astrocystitidae", "includeVariants": true, "trees": ["taxonomy"], "years": null}

> Astrocystites (genus, Whiteaves 1897): sources placing it under Steganoblastidae vs. Astrocystitidae; all years
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
- judge contract 2: Header lists only group, rank variants, synonym scope, tree type and year range; no verdict, summary or mechanism; no question needed.

Plan: {"header": "Rhenopyrgidae (family, including its subfamily-rank variant Rhenopyrginae) as placed under Cyathocystidae (family, including its variants); no synonym expansion beyond these variants; classificatory placements only; all years", "blocks": [{"tool": "placed_under", "parameters": {"record": "Rhenopyrgidae", "parent": "Cyathocystidae"}}, {"tool": "history", "parameters": {"record": "Rhenopyrgidae", "include_related": false}}]}
Header: Rhenopyrgidae (family, including its subfamily-rank variant Rhenopyrginae) as placed under Cyathocystidae (family, including its variants); no synonym expansion beyond these variants; classificatory placements only; all years
- chains {"record": "rhenopyrgidae", "parent": "cyathocystidae", "includeVariants": true, "trees": ["taxonomy"], "years": null}
- timeline {"record": "rhenopyrgidae", "includeRelated": false, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Rhenopyrgidae (family, including its subfamily-rank variant Rhenopyrginae) as placed under Cyathocystidae (family, including its variants); no synonym expansion beyond these variants; classificatory placements only; all years
> 
> Rhenopyrgidae Holloway & Jell 1983 under Cyathocystidae Bather 1899: 2 papers, 2 co-author sets, 1994–2000
> first Guensburg & Sprinkle 1994, last Grigo 2000
> 
> 1994  Guensburg & Sprinkle  Rhenopyrginae
> 2000  Grigo                 Rhenopyrginae
> 
> Rhenopyrgidae Holloway & Jell 1983: 5 papers, 5 co-author sets, 1983–2020
> in Edrioblastoidina since 2013 (3 papers), in Isorophida 2010 (1 paper), in Order uncertain 1983 (1 paper)
> 
> 1983  Holloway & Jell  Rhenopyrgidae, in Order uncertain; named as new
> 2010  Müller & Hahn    Rhenopyrgidae, in Isorophida
> 2013  Sumrall et al.   Rhenopyrgidae, in Edrioblastoidina; emended; moved from Cyathocystidae; declines a placement in Cyathocystidae
> 2017  Briggs et al.    Rhenopyrgidae, in Edrioblastoidina
> 2020  Ewin et al.      Rhenopyrgidae, in Edrioblastoidina; emended (p. 118)

### q048 (trajectory)

Q: What did Holloway & Jell (1983) say Dehm (1961) did with Pyrgocystis octogona, and what does Dehm's own paper do?

- failure: no composed block is gap {"source": "1983_holloway_jell", "kind": "synonymy"}
- failure: the answer does not show "The synonymy printed in Holloway & Jell 1983 has not yet been entered"
- judge contract 2: Header names the species, the two sources compared, year range and taxonomic scope; no summary, mechanism or verdict; no question needed.

Plan: {"header": "Species Pyrgocystis octogona (Richter, 1930): statements made about it by Holloway & Jell (1983) regarding Dehm (1961)'s treatment, and Dehm (1961)'s own statements; all years, taxonomic sense only", "blocks": [{"tool": "statements", "parameters": {"record": "octogona_richter.r_1930", "source": "1983_holloway_jell"}}, {"tool": "statements", "parameters": {"record": "octogona_richter.r_1930", "source": "1961_dehm"}}]}
Header: Species Pyrgocystis octogona (Richter, 1930): statements made about it by Holloway & Jell (1983) regarding Dehm (1961)'s treatment, and Dehm (1961)'s own statements; all years, taxonomic sense only
- statement {"record": "octogona_richter.r_1930", "source": "1983_holloway_jell", "kind": "skeleton", "actKind": null, "statementKind": null}
- list {"record": "octogona_richter.r_1930", "source": "1961_dehm", "kind": null, "actKind": null}

> Species Pyrgocystis octogona (Richter, 1930): statements made about it by Holloway & Jell (1983) regarding Dehm (1961)'s treatment, and Dehm (1961)'s own statements; all years, taxonomic sense only
> 
> The classification printed in Holloway & Jell 1983 is entered in full.
> 
> Statements about Pyrgocystis octogona Richter 1930
>   1961  Dehm  cites the name (cited p. 294)
>   1961  Dehm  places it under Pyrgocystis (cited p. 294)
>   1961  Dehm  occurrence: Lower Devonian; greywacke slates; Bornich, near Weisel on the Rhine, Germany (cited p. 294)

