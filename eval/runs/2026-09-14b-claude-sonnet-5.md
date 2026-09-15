# Grades for `2026-09-14b-claude-sonnet-5.jsonl`

| class | questions | mechanical pass |
|---|---|---|
| absent | 3 | 3 |
| answerable | 12 | 8 |
| as-published | 8 | 5 |
| trajectory | 15 | 9 |
| uncaptured | 9 | 7 |

## Failures and notes

### q001 (answerable)

Q: What new class does Fay (1962) erect for the genus Astrocystites, and what family/order sit between the genus and the class?

- failure: free text beside the submission: This confirms Fay (1962) places the genus Astrocystites directly under the new c
- judge contract 0: Header pre-answers the question ("no family or order intervenes") and asserts the taxonomic act ("new class erected"), giving summary and verdict rather than parameters.

Header: Fay (1962): new class erected for Astrocystites, with classification as printed; no family or order intervenes between the genus and the class in this source
- classification {"source": "1962_fay", "record": "edrioblastoidea", "depth": null, "synonymy": false, "path": "0"}

> Fay (1962): new class erected for Astrocystites, with classification as printed; no family or order intervenes between the genus and the class in this source
> 
> Fay 1962
>   Class Edrioblastoidea nov.
>     Genus Astrocystites (moved from Edrioasteroidea)
>       Type species. Astrocystites ottawaensis
>       Astrocystites ottawaensis

### q006 (answerable)

Q: What species do Sumrall, Heredia Rodríguez & Mestre (2013) confirm as the type species of Rhenopyrgus?

- failure: free text beside the submission: This confirms the answer with the contents block showing Sumrall et al. 2013's c
- judge contract 1: Parameters (genus record, no synonyms, source, 2013) are stated plainly, but 'as confirmed by' passes a verdict rather than neutrally naming the opinion.

Header: Type species of Rhenopyrgus (Dehm 1961) as confirmed by Sumrall, Heredia Rodríguez & Mestre 2013, from their emended generic classification; genus record only, no synonyms.
- classification {"source": "2013_sumrall_heredia_rodríguez.c.m_mestre", "record": "rhenopyrgus", "depth": null, "synonymy": false, "path": "0/children/0/children/0/children/0/children/0/children/0"}
- list {"record": "coronaeformis_rievers_1961", "source": null, "kind": null, "actKind": "type"}

> Type species of Rhenopyrgus (Dehm 1961) as confirmed by Sumrall, Heredia Rodríguez & Mestre 2013, from their emended generic classification; genus record only, no synonyms.
> 
> Sumrall et al. 2013
>   Genus Rhenopyrgus emend.
>     Type species. Rhenopyrgus coronaeformis
>     Rhenopyrgus coronaeformis
>     Rhenopyrgus piojoensis sp. nov.
>     Rhenopyrgus whitei
>     Rhenopyrgus flos
> 
> Statements about Pyrgocystis coronaeformis Rievers 1961
>   1961  Dehm             Pyrgocystis (Rhenopyrgus) coronaeformis: type species (p. 16)
>   1966  Regnéll          Pyrgocystis (Rhenopyrgus) coronaeformis: type species
>   1983  Holloway & Jell  Rhenopyrgus coronaeformis: type species
>   2000  Grigo            Rhenopyrgus coronaeformis: type species (p. 95)
>   2013  Sumrall et al.   Rhenopyrgus coronaeformis: type species
>   2020  Ewin et al.      Rhenopyrgus coronaeformis: type species (p. 118)

### q008 (answerable)

Q: In Holloway & Jell (1983), family Rhenopyrgidae is placed under a name that is not itself an order. What is that placeholder, and what does it mean?

- failure: free text beside the submission: The placeholder is "Order uncertain" under Edrioasteroidea in Holloway & Jell (1
- judge contract 2: Header names only taxon, source publication, and scope; no summary, verdict, or mechanism wording. No question back needed since parameters are unambiguous.

Header: Rhenopyrgidae in Holloway & Jell (1983); classification only
- chains {"records": ["rhenopyrgidae"], "includeVariants": true, "trees": ["taxonomy"], "years": null}

> Rhenopyrgidae in Holloway & Jell (1983); classification only
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

### q009 (answerable)

Q: What new species of Rhenopyrgus does Grigo (2000) describe, and from where?

- failure: no composed block is gap {"source": "2000_grigo", "kind": "occurrences"}
- note: composed after the lookup limit was reached
- judge contract 2: Header names only taxon, source tree, scope of new species/occurrence, and year range; no verdict or mechanism wording, and no question needed.

Header: Rhenopyrgus (genus) as classified by Grigo 2000; new species and their occurrence as printed in that source; all years
- classification {"source": "2000_grigo", "record": "rhenopyrgus", "depth": null, "synonymy": true, "path": "0/children/1/children/0/children/0/children/0/children/0"}
- table {"records": ["rhenopyrgus"], "includeSynonyms": true, "includeVariants": true, "trees": ["taxonomy"], "years": [2000, 2000]}

> Rhenopyrgus (genus) as classified by Grigo 2000; new species and their occurrence as printed in that source; all years
> 
> Grigo 2000, p. 95
>   Genus Rhenopyrgus
>     Type species. Rhenopyrgus coronaeformis
>     Rhenopyrgus coronaeformis
>     Rhenopyrgus sp. nov.
> 
> Placed under Rhenopyrgus
> record                     rank     placed by                      sources
> -------------------------  -------  -----------------------------  -------
> Rhenopyrgus sp.            species  Grigo 2000: under Rhenopyrgus  1
> Rhenopyrgus coronaeformis  species  Grigo 2000: under Rhenopyrgus  1

### q013 (uncaptured)

Q: What holotype and paratype specimen numbers does Holloway & Jell (1983) give for Rhenopyrgus whitei?

- failure: free text beside the submission: The corpus does not hold the holotype and paratype specimen numbers for this rec
- judge contract 2: Header names only the taxon, the data type sought (material/specimen), and year scope; no summary, mechanism, or verdict; no unnecessary question.

Header: Rhenopyrgus whitei Holloway & Jell, 1983; material/specimen data from that source; all years
- statement {"source": "1983_holloway_jell", "kind": "material"}

> Rhenopyrgus whitei Holloway & Jell, 1983; material/specimen data from that source; all years
> 
> The material printed in Holloway & Jell 1983 has not yet been entered (none of it is entered so far).

### q018 (uncaptured)

Q: Whose holotype does Briggs et al. (2017) cite for Heropyrgus disterminus, and where is it deposited?

- note: text between lookups: Material coverage is declared "none" for this source, so the corpus does not hol
- judge contract 2: Header names only the taxon and the target publication whose material citation is sought; no verdict, summary, or mechanism wording; no question needed.

Header: Heropyrgus disterminus Briggs et al. 2017; holotype/material citation sought in Briggs et al. 2017
- statement {"source": "2017_briggs.d.e.g_siveter.de.j_siveter.da.j_sutton.m.d_rahman", "kind": "material"}

> Heropyrgus disterminus Briggs et al. 2017; holotype/material citation sought in Briggs et al. 2017
> 
> The material printed in Briggs et al. 2017 has not yet been entered (none of it is entered so far).

### q019 (uncaptured)

Q: Which earlier works does Fay (1962) cite in his synonymy of Astrocystites ottawaensis?

- failure: free text beside the submission: The synonymy Fay (1962) prints is at the genus level (Astrocystites, a monotypic
- failure: the answer does not show "Fay 1962"
- judge contract 1: Parameters are otherwise plainly stated, but "which is monotypic for this species" adds a substantive taxonomic claim beyond the chosen parameters — one lapse.

Header: Synonymy of Astrocystites ottawaensis (Whiteaves 1897) as printed by Fay (1962) — entered under the genus Astrocystites, which is monotypic for this species; no restriction on rank of the earlier name cited; taxonomic content only, all years.
- list {"record": "astrocystites", "source": "1962_fay", "path": "0/children/0"}

> Synonymy of Astrocystites ottawaensis (Whiteaves 1897) as printed by Fay (1962) — entered under the genus Astrocystites, which is monotypic for this species; no restriction on rank of the earlier name cited; taxonomic content only, all years.
> 
> Astrocystites (genus)
>   Steganoblastus

### q021 (as-published)

Q: What exact suborder heading do Ewin et al. (2020) print above family Rhenopyrgidae, and at what rank was that name first established?

- failure: free text beside the submission: The suborder heading Ewin et al. (2020) print above family Rhenopyrgidae is "Sub
- judge contract 1: Parameters (record, scope, year range) stated plainly, but the header pre-empts the answer by naming Edrioblastoidina Fay 1962 — one summary lapse.

Header: Suborder heading above family Rhenopyrgidae Holloway & Jell 1983 in Ewin et al. (2020), and the establishment history of that suborder name (Edrioblastoidina Fay 1962); classifications only, all years
- list {"record": "edrioblastoidina", "source": "2020_ewin_martin.m_isotalo_zamora"}
- timeline {"record": "edrioblastoidina", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Suborder heading above family Rhenopyrgidae Holloway & Jell 1983 in Ewin et al. (2020), and the establishment history of that suborder name (Edrioblastoidina Fay 1962); classifications only, all years
> 
> Edrioblastoidina (Suborder)
>   2020 "Suborder Edrioblastoidina Fay, 1962" Ewin et al. 2020 p. 118
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

### q024 (as-published)

Q: How did Dehm (1961) style the new subgenus name Rhenopyrgus, and how do Sumrall et al. (2013) cite the type species using that name?

- failure: no composed block is printed_forms {"record": "coronaeformis_rievers_1961", "source": "2013_sumrall_heredia_rodríguez.c.m_mestre"}
- failure: the answer does not show "Pyrgocystis (Rhenopyrgus) coronaeformis Rievers, 1961"
- judge contract 1: Parameters and scope stated plainly, but "under the genus Rhenopyrgus" pre-empts the answer about Sumrall et al.'s treatment — one summarizing lapse.

Header: Rhenopyrgus (Dehm 1961, original subgenus of Pyrgocystis) and its type species as cited by Sumrall et al. (2013) under the genus Rhenopyrgus; all years
- list {"record": "rhenopyrgus-subgenus", "source": "1961_dehm", "kind": null, "actKind": null}
- list {"record": "rhenopyrgus-subgenus", "source": "1961_dehm"}
- classification {"source": "2013_sumrall_heredia_rodríguez.c.m_mestre", "record": "rhenopyrgus", "depth": null, "synonymy": false, "path": "0/children/0/children/0/children/0/children/0/children/0"}

> Rhenopyrgus (Dehm 1961, original subgenus of Pyrgocystis) and its type species as cited by Sumrall et al. (2013) under the genus Rhenopyrgus; all years
> 
> Statements about Pyrgocystis (Rhenopyrgus) Dehm 1961
>   1961  Dehm  cites the name as "Rhenopyrgus nov. subgen." (p. 16)
>   1961  Dehm  places it under Pyrgocystis (p. 16)
>   1961  Dehm  named as new (p. 16)
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

### q026 (as-published)

Q: What two different words does Fay (1962) use for the same specimen, No. 752, in Astrocystites ottawaensis?

- note: composed after the lookup limit was reached
- judge contract 2: Header lists only scope parameters—taxon, source record, synonym/rank exclusion, classifications, year range—in community language, with no verdict, summary, or mechanism; no question needed.

Header: Astrocystites ottawaensis (Whiteaves 1897); material statement of Fay 1962; no synonyms or other ranks; classifications only where relevant; all years not applicable (single source)
- list {"record": "ottawaensis_whiteaves_1897", "source": "1962_fay", "kind": "material", "actKind": null}

> Astrocystites ottawaensis (Whiteaves 1897); material statement of Fay 1962; no synonyms or other ranks; classifications only where relevant; all years not applicable (single source)
> 
> Statements about Astrocystites ottawaensis Whiteaves 1897
>   1962  Fay  syntypes: Canadian Geological Survey 752

### q028 (as-published)

Q: What exact heading and parenthetical act does Guensburg & Sprinkle (1994) print for the Rhenopyrgus subfamily?

- failure: free text beside the submission: This gives the answer directly: the 1994 entry shows "Rhenopyrginae, in Cyathocy
- failure: no composed block is contents {"source": "1994_guensburg_sprinkle", "record": "rhenopyrginae"}
- failure: the answer does not show "Subfamily Rhenopyrginae emend. nom. transl."
- judge contract 2: Header names taxon, rank-variant relation, and source publication only; no verdict or mechanism; no question needed since the as-published request is unambiguous.

Header: Rhenopyrginae (subfamily-rank form of Rhenopyrgidae Holloway & Jell, 1983) as printed by Guensburg & Sprinkle (1994); history block shown for context
- timeline {"record": "rhenopyrginae", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Rhenopyrginae (subfamily-rank form of Rhenopyrgidae Holloway & Jell, 1983) as printed by Guensburg & Sprinkle (1994); history block shown for context
> 
> Rhenopyrginae Holloway & Jell 1983: 7 papers, 7 co-author sets, 1983–2020
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

### q035 (trajectory)

Q: Is Isorophus (and its sibling genus Carneyella) attributed to Foerste 1916 or 1917?

- failure: free text beside the submission: Both genera are attributed by the corpus's record authority to Foerste 1916, but
- failure: no composed block is history {"record": "isorophus"}
- failure: no composed block is history {"record": "carneyella"}
- failure: the answer does not show "Isorophus Foerste 1916"
- failure: the answer does not show "Carneyella Foerste 1916"
- judge contract 0: Header pre-answers the question: asserts 1916 as the corpus default and names 1994 as the lone exception — a verdict, and an inaccurate one (Sumrall & Zamora 2011 also print 1917).

Header: Authority attribution for Isorophus and Carneyella: taken as Foerste 1916 in the corpus's records, with the printed forms each source uses (Guensburg & Sprinkle 1994 print "Foerste, 1917" for both); all years.
- list {"record": "isorophus", "source": null}
- list {"record": "carneyella", "source": null}

> Authority attribution for Isorophus and Carneyella: taken as Foerste 1916 in the corpus's records, with the printed forms each source uses (Guensburg & Sprinkle 1994 print "Foerste, 1917" for both); all years.
> 
> Isorophus (genus)
>   1994 "Isorophus Foerste, 1917" Guensburg & Sprinkle 1994
> 
> Carneyella (genus)
>   1994 "Carneyella Foerste, 1917" Guensburg & Sprinkle 1994

### q041 (trajectory)

Q: Which papers in the corpus treat edrioblastoids, and what does each do to the group?

- failure: free text beside the submission: This history block covers all the papers, ranks, placements and acts (the naming
- judge contract 2: Header lists only group, rank variants, scope of sources, all years, and ordering; no summary, mechanism or verdict; no question needed.

Header: Edrioblastoidea taken as the class and its order/suborder forms (Edrioblastoida, Edrioblastoidina); all sources treating the group across all years, ordered by publication date
- timeline {"record": "edrioblastoidea", "includeRelated": true, "synonymy": true, "trees": ["taxonomy"], "years": null}

> Edrioblastoidea taken as the class and its order/suborder forms (Edrioblastoida, Edrioblastoidina); all sources treating the group across all years, ordered by publication date
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

### q043 (trajectory)

Q: At what rank has the edrioblastoid group been treated, and by which co-author sets, over time?

- failure: free text beside the submission: This single timeline block answers the question fully.
- judge contract 2: Header lists only group, included rank-name variants, record type, and year span in community terms; no verdict or summary; no question needed.

Header: Edrioblastoidea taken with its order/suborder name variants (Edrioblastoida, Edrioblastoidina); classifications only; all years (1962–2021)
- timeline {"record": "edrioblastoidea", "includeRelated": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Edrioblastoidea taken with its order/suborder name variants (Edrioblastoida, Edrioblastoidina); classifications only; all years (1962–2021)
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

- failure: free text beside the submission: This directly answers the question via the ancestors block.
- judge contract 1: Header is neutral parameter language, but silently narrows years to 1935–1994, excluding Bather 1900 and 2015, and never asks about this ambiguous scope.

Header: Family placement of Astrocystites (Whiteaves 1897) across sources, 1935–1994; classifications only
- chains {"records": ["astrocystites"], "includeVariants": true, "trees": ["taxonomy"], "years": null}

> Family placement of Astrocystites (Whiteaves 1897) across sources, 1935–1994; classifications only
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

### q048 (trajectory)

Q: What did Holloway & Jell (1983) say Dehm (1961) did with Pyrgocystis octogona, and what does Dehm's own paper do?

- failure: no composed block is gap {"source": "1983_holloway_jell", "kind": "synonymy"}
- failure: the answer does not show "The synonymy printed in Holloway & Jell 1983 has not yet been entered"
- note: composed after the lookup limit was reached
- judge contract 2: Header names the taxon, the two sources compared, statement type, and year range neutrally; 'versus' frames comparison without verdict; no question needed.

Header: Pyrgocystis octogona Richter 1930: what Holloway &amp; Jell (1983) report of Dehm's (1961) treatment, versus Dehm's (1961) own placement; classification statements only, all years
- statement {"source": "1983_holloway_jell", "kind": null, "record": "octogona_richter.r_1930", "actKind": null}
- list {"record": "octogona_richter.r_1930", "source": "1961_dehm", "kind": null, "actKind": null}
- chains {"records": ["octogona_richter.r_1930"], "includeVariants": true, "trees": ["taxonomy"], "years": null}

> Pyrgocystis octogona Richter 1930: what Holloway &amp; Jell (1983) report of Dehm's (1961) treatment, versus Dehm's (1961) own placement; classification statements only, all years
> 
> The classification printed in Holloway & Jell 1983 is entered in full.
> 
> Statements about Pyrgocystis octogona Richter 1930
>   1961  Dehm  cites the name (cited p. 294)
>   1961  Dehm  places it under Pyrgocystis (cited p. 294)
>   1961  Dehm  occurrence: Lower Devonian; greywacke slates; Bornich, near Weisel on the Rhine, Germany (cited p. 294)
> 
> Above Pyrgocystis octogona Richter 1930: 2 papers, 2 co-author sets, 1935–1961
> 
> 1935  Bassler  Edrioasteroidea › Agelacrinitidae › Pyrgocystis › Pyrgocystis octogona
> 1961  Dehm     Pyrgocystis › Pyrgocystis octogona

### q049 (trajectory)

Q: Which cladistic analyses in the corpus include Rhenopyrgus, and where does each place it?

- failure: free text beside the submission: This gives a clear picture. Let me submit with the ancestors block, which shows 
- judge contract 2: Header lists only group, rank-variant handling, tree types, and year span in community terms; no summary, mechanism, or verdict; no question needed.

Header: Cladistic/phylogenetic-diagram analyses in the corpus that include Rhenopyrgus (genus and subgenus forms combined); cladogram and diagram trees; all years
- chains {"records": ["rhenopyrgus", "rhenopyrgus-subgenus"], "includeVariants": true, "trees": ["cladogram", "diagram"], "years": null}

> Cladistic/phylogenetic-diagram analyses in the corpus that include Rhenopyrgus (genus and subgenus forms combined); cladogram and diagram trees; all years
> 
> Above Rhenopyrgus Dehm 1961, Pyrgocystis (Rhenopyrgus) Dehm 1961: 3 papers, 3 co-author sets, 1990–2013
> 
> 1990  Smith & Jell          Rhenopyrgus
> 1990  Smith & Jell          Stromatocystites pentangularis › ? lloydi › Rhenopyrgus
> 1994  Guensburg & Sprinkle  Edrioasteroidea › Rhenopyrgus
> 1994  Guensburg & Sprinkle  Edrioasteroidea › Rhenopyrgus
> 1994  Guensburg & Sprinkle  Edrioasteroidea › Rhenopyrgus
> 1994  Guensburg & Sprinkle  Edrioasteroidea › Rhenopyrgus
> 2013  Sumrall et al.        Rhenopyrgus
> 2013  Sumrall et al.        Rhenopyrgus

