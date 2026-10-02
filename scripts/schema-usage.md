# Schema usage census

**Generated** by `scripts/schema_audit.py` -- do not edit by hand.
Narrative analysis of these numbers is in `notes/audits/schema-audit.md`.

Counts are *distinct instance locations* that reached a given schema
location, measured from the `json-schema-engine` verbose output tree.

## 1. Unreached schema locations

Schema locations no data anywhere reaches. A nested location is listed
even when its parent is also unreached, so read parents first.

| `$defs` | unreached locations |
|---|---|
| `actAndModifierFields` | `phylogeny#/$defs/actAndModifierFields/properties/emended/oneOf/1`<br>`phylogeny#/$defs/actAndModifierFields/properties/recombined`<br>`phylogeny#/$defs/actAndModifierFields/properties/recombined/oneOf/0`<br>`phylogeny#/$defs/actAndModifierFields/properties/recombined/oneOf/1` |
| `citedAct` | `phylogeny#/$defs/citedAct`<br>`phylogeny#/$defs/citedAct/properties/by` |
| `cladisticFields` | `phylogeny#/$defs/cladisticFields/properties/data`<br>`phylogeny#/$defs/cladisticFields/properties/data/additionalProperties` |
| `context` | `phylogeny#/$defs/context/properties/biota`<br>`phylogeny#/$defs/context/properties/biozones`<br>`phylogeny#/$defs/context/properties/biozones/items`<br>`phylogeny#/$defs/context/properties/collectedDate`<br>`phylogeny#/$defs/context/properties/paleocontinent`<br>`phylogeny#/$defs/context/properties/sources`<br>`phylogeny#/$defs/context/properties/sources/items` |
| `contextRef` | `phylogeny#/$defs/contextRef/oneOf/1`<br>`phylogeny#/$defs/contextRef/oneOf/1/properties/key`<br>`phylogeny#/$defs/contextRef/oneOf/1/properties/tentative` |
| `eon` | `phylogeny#/$defs/eon` |
| `era` | `phylogeny#/$defs/era` |
| `figureLocatorFields` | `phylogeny#/$defs/figureLocatorFields/properties/non` |
| `inferredContext` | `phylogeny#/$defs/inferredContext/properties/basis`<br>`phylogeny#/$defs/inferredContext/properties/sources`<br>`phylogeny#/$defs/inferredContext/properties/sources/items` |
| `localTimeFields` | `phylogeny#/$defs/localTimeFields/properties/localStageBoundary` |
| `materialEntry` | `phylogeny#/$defs/materialEntry/properties/formerIds`<br>`phylogeny#/$defs/materialEntry/properties/formerIds/items`<br>`phylogeny#/$defs/materialEntry/properties/fragmentOf`<br>`phylogeny#/$defs/materialEntry/properties/roleUncertain` |
| `modularDate` | `phylogeny#/$defs/modularDate/then/oneOf/1/properties/month/anyOf/3`<br>`phylogeny#/$defs/modularDate/then/oneOf/2/properties/month/anyOf/5` |
| `person` | `phylogeny#/$defs/person/properties/suffix` |
| `publication` | `phylogeny#/$defs/publication/properties/type` |
| `range` | `phylogeny#/$defs/range/properties/inferred` |
| `stageRange` | `phylogeny#/$defs/stageRange`<br>`phylogeny#/$defs/stageRange/items` |
| `taxonRecord` | `phylogeny#/$defs/taxonRecord/properties/holotype/additionalProperties/items/items` |
| `timeFields` | `phylogeny#/$defs/timeFields/properties/eon`<br>`phylogeny#/$defs/timeFields/properties/era`<br>`phylogeny#/$defs/timeFields/properties/seriesBoundary`<br>`phylogeny#/$defs/timeFields/properties/stageBoundary`<br>`phylogeny#/$defs/timeFields/properties/stageRange` |
| `treeDocument` | `phylogeny#/$defs/treeDocument/properties/unused`<br>`phylogeny#/$defs/treeDocument/properties/unused/items` |
| `uncertaintyFields` | `phylogeny#/$defs/uncertaintyFields/properties/nonMonophyletic/oneOf/1`<br>`phylogeny#/$defs/uncertaintyFields/properties/sensu` |

## 2. Property frequency by `$defs`

`data %` is the share of that container's instances carrying the
property.

### `actAndModifierFields` -- 5580 instances in `data/`

| property | data | data % |
|---|---|---|
| `new` | 1472 | 26.4% |
| `type` | 369 | 6.6% |
| `emended` | 54 | 1.0% |
| `pars` | 19 | 0.3% |
| `translated` | 16 | 0.3% |
| `nudum` | 4 | 0.1% |
| `stem` | 1 | 0.0% |
| `recombined` | 0 | 0.0% |

### `article` -- 310 instances in `data/`

| property | data | data % |
|---|---|---|
| `authors` | 310 | 100.0% |
| `pubDate` | 309 | 99.7% |
| `title` | 255 | 82.3% |
| `volume` | 238 | 76.8% |
| `pages` | 216 | 69.7% |
| `identifiers` | 213 | 68.7% |
| `journal` | 213 | 68.7% |
| `number` | 155 | 50.0% |
| `identifiers.url` | 131 | 61.5% |
| `processDates` | 98 | 31.6% |
| `book` | 95 | 30.6% |
| `processDates.accepted` | 63 | 64.3% |
| `identifiers.doi` | 61 | 28.6% |
| `processDates.received` | 53 | 54.1% |
| `audit` | 48 | 15.5% |
| `audit.notes` | 48 | 100.0% |
| `audit.state` | 48 | 100.0% |
| `notes` | 37 | 11.9% |
| `audit.coverage` | 30 | 62.5% |
| `processDates.online` | 28 | 28.6% |
| `identifiers.jstor` | 24 | 11.3% |
| `plates` | 21 | 6.8% |
| `processDates.revised` | 18 | 18.4% |
| `series` | 9 | 2.9% |
| `processDates.read` | 8 | 8.2% |
| `articleNumber` | 7 | 2.3% |
| `seen` | 5 | 1.6% |
| `processDates.transmitted` | 4 | 4.1% |
| `processDates.conferenceEnd` | 3 | 3.1% |
| `processDates.conferenceStart` | 3 | 3.1% |
| `processDates.issued` | 3 | 3.1% |
| `processDates.submitted` | 3 | 3.1% |
| `translationOf` | 2 | 0.6% |
| `translations` | 2 | 0.6% |
| `chapter` | 1 | 0.3% |
| `editors` | 1 | 0.3% |
| `inPrep` | 1 | 0.3% |
| `processDates.printed` | 1 | 1.0% |
| `processDates.published` | 1 | 1.0% |
| `processDates.unknown` | 1 | 1.0% |
| `quotes` | 1 | 0.3% |
| `reading` | 1 | 0.3% |

### `authority` -- 1659 instances in `data/`

| property | data | data % |
|---|---|---|
| `source` | 1659 | 100.0% |
| `pages` | 65 | 3.9% |
| `illustrations` | 29 | 1.7% |
| `attributedTo` | 24 | 1.4% |
| `ex` | 2 | 0.1% |
| `notes` | 2 | 0.1% |

### `authorityFields` -- 9099 instances in `data/`

| property | data | data % |
|---|---|---|
| `authority` | 1656 | 18.2% |
| `auth` | 1000 | 11.0% |
| `year` | 998 | 11.0% |
| `in` | 28 | 0.3% |

### `citationFields` -- 9099 instances in `data/`

| property | data | data % |
|---|---|---|
| `rank` | 752 | 8.3% |
| `bracket` | 48 | 0.5% |

### `cladisticFields` -- 794 instances in `data/`

| property | data | data % |
|---|---|---|
| `outgroup` | 19 | 2.4% |
| `matrix` | 8 | 1.0% |
| `bootstrap` | 6 | 0.8% |
| `data` | 0 | 0.0% |

### `context` -- 113 instances in `data/`

| property | data | data % |
|---|---|---|
| `location` | 112 | 99.1% |
| `unit` | 104 | 92.0% |
| `biozone` | 48 | 42.5% |
| `localityNumbers` | 46 | 40.7% |
| `mapSheet` | 30 | 26.5% |
| `notes` | 20 | 17.7% |
| `coordinatesAsPrinted` | 12 | 10.6% |
| `biozoneRange` | 7 | 6.2% |
| `collectedBy` | 2 | 1.8% |
| `fauna` | 1 | 0.9% |
| `inferred` | 1 | 0.9% |
| `biota` | 0 | 0.0% |
| `biozones` | 0 | 0.0% |
| `collectedDate` | 0 | 0.0% |
| `paleocontinent` | 0 | 0.0% |
| `sources` | 0 | 0.0% |

### `editorialObject` -- 9 instances in `data/`

| property | data | data % |
|---|---|---|
| `basis` | 9 | 100.0% |
| `inferred` | 7 | 77.8% |
| `corrections` | 2 | 22.2% |
| `corrections.authority` | 2 | 100.0% |
| `corrections.authority.source` | 2 | 100.0% |

### `figureLocatorFields` -- 479 instances in `data/`

| property | data | data % |
|---|---|---|
| `figures` | 414 | 86.4% |
| `plate` | 340 | 71.0% |
| `page` | 126 | 26.3% |
| `textFigures` | 65 | 13.6% |
| `notes` | 23 | 4.8% |
| `non` | 0 | 0.0% |

### `identificationFields` -- 6374 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxon` | 5777 | 90.6% |
| `openTaxon` | 247 | 3.9% |
| `citedAs` | 53 | 0.8% |
| `cf` | 15 | 0.2% |
| `aff` | 14 | 0.2% |

### `illustration` -- 479 instances in `data/`

| property | data | data % |
|---|---|---|
| `of` | 241 | 50.3% |
| `depicts` | 171 | 35.7% |
| `uncertain` | 2 | 0.4% |

### `inferredContext` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `paleocontinent` | 1 | 100.0% |
| `basis` | 0 | 0.0% |
| `sources` | 0 | 0.0% |

### `localTimeFields` -- 165 instances in `data/`

| property | data | data % |
|---|---|---|
| `localSeries` | 65 | 39.4% |
| `localSeriesModifier` | 26 | 15.8% |
| `localSeriesRange` | 9 | 5.5% |
| `localStage` | 9 | 5.5% |
| `localStageRange` | 6 | 3.6% |
| `localPeriod` | 3 | 1.8% |
| `localSeriesBoundary` | 1 | 0.6% |
| `localStageModifier` | 1 | 0.6% |
| `localStageBoundary` | 0 | 0.0% |

### `locationFields` -- 9099 instances in `data/`

| property | data | data % |
|---|---|---|
| `pages` | 350 | 3.8% |
| `illustrations` | 186 | 2.0% |

### `materialEntry` -- 280 instances in `data/`

| property | data | data % |
|---|---|---|
| `catalogNumbers` | 263 | 93.9% |
| `role` | 209 | 74.6% |
| `context` | 137 | 48.9% |
| `catalogNumbersAsPrinted` | 78 | 27.9% |
| `notes` | 66 | 23.6% |
| `preparation` | 16 | 5.7% |
| `label` | 14 | 5.0% |
| `count` | 11 | 3.9% |
| `collectedBy` | 10 | 3.6% |
| `repository` | 10 | 3.6% |
| `collectedDate` | 7 | 2.5% |
| `parts` | 6 | 2.1% |
| `holder` | 5 | 1.8% |
| `castOf` | 3 | 1.1% |
| `uncertain` | 2 | 0.7% |
| `editorial` | 1 | 0.4% |
| `examined` | 1 | 0.4% |
| `listComplete` | 1 | 0.4% |
| `roleAct` | 1 | 0.4% |
| `status` | 1 | 0.4% |
| `formerIds` | 0 | 0.0% |
| `fragmentOf` | 0 | 0.0% |
| `roleUncertain` | 0 | 0.0% |

### `materialsFields` -- 5580 instances in `data/`

| property | data | data % |
|---|---|---|
| `material` | 119 | 2.1% |
| `contexts` | 97 | 1.7% |
| `ranges` | 90 | 1.6% |

### `metaFields` -- 6374 instances in `data/`

| property | data | data % |
|---|---|---|
| `notes` | 385 | 6.0% |
| `editorial` | 8 | 0.1% |

### `modularDate` -- 309 instances in `data/`

| property | data | data % |
|---|---|---|
| `year` | 309 | 100.0% |
| `month` | 73 | 23.6% |
| `day` | 24 | 7.8% |
| `/then/oneOf/2.day` | 14 | 100.0% |
| `/then/oneOf/2.month` | 14 | 100.0% |
| `/then/oneOf/1.day` | 8 | 100.0% |
| `/then/oneOf/1.month` | 8 | 100.0% |
| `months` | 4 | 1.3% |
| `/then/oneOf/0.day` | 2 | 100.0% |
| `/then/oneOf/0.month` | 2 | 100.0% |
| `season` | 1 | 0.3% |

### `person` -- 282 instances in `data/`

| property | data | data % |
|---|---|---|
| `given` | 282 | 100.0% |
| `surname` | 282 | 100.0% |
| `birth` | 82 | 29.1% |
| `death` | 81 | 28.7% |
| `suffix` | 0 | 0.0% |

### `phylogeny` -- 36 instances in `data/`

| property | data | data % |
|---|---|---|
| `tree` | 36 | 100.0% |
| `treeType` | 36 | 100.0% |
| `methodology` | 18 | 50.0% |
| `notes` | 6 | 16.7% |
| `characteristics` | 1 | 2.8% |

### `publication` -- 138 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 138 | 100.0% |
| `editors` | 9 | 6.5% |
| `place` | 8 | 5.8% |
| `publisher` | 8 | 5.8% |
| `notes` | 2 | 1.4% |
| `type` | 0 | 0.0% |

### `range` -- 52 instances in `data/`

| property | data | data % |
|---|---|---|
| `regions` | 34 | 65.4% |
| `asPrinted` | 13 | 25.0% |
| `notes` | 10 | 19.2% |
| `regions/items/oneOf/1.tentative` | 2 | 100.0% |
| `regions/items/oneOf/1.value` | 2 | 100.0% |
| `inferred` | 0 | 0.0% |

### `relationalFields` -- 5580 instances in `data/`

| property | data | data % |
|---|---|---|
| `synonyms` | 360 | 6.5% |
| `moved` | 30 | 0.5% |
| `corrected` | 5 | 0.1% |
| `non` | 4 | 0.1% |
| `or` | 3 | 0.1% |
| `lapsus` | 1 | 0.0% |
| `lapsusFor` | 1 | 0.0% |
| `removed` | 1 | 0.0% |
| `substituted` | 1 | 0.0% |

### `repositories` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `/additionalProperties.name` | 49 | 100.0% |
| `/additionalProperties.type` | 49 | 100.0% |
| `/additionalProperties.prefixes` | 45 | 91.8% |
| `/additionalProperties.place` | 34 | 69.4% |
| `/additionalProperties.within` | 11 | 22.4% |
| `/additionalProperties.subject` | 8 | 16.3% |
| `/additionalProperties.notes` | 6 | 12.2% |
| `/additionalProperties.otherNames` | 3 | 6.1% |

### `roles` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `/additionalProperties.meaning` | 12 | 100.0% |
| `/additionalProperties.regulated` | 12 | 100.0% |
| `/additionalProperties.article` | 6 | 50.0% |
| `/additionalProperties.notes` | 6 | 50.0% |
| `/additionalProperties.equivalent` | 2 | 16.7% |

### `taxonRecord` -- 2725 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 2686 | 98.6% |
| `notes` | 213 | 7.8% |
| `altSpellingOf` | 143 | 5.2% |
| `lang` | 75 | 2.8% |
| `originalParent` | 65 | 2.4% |
| `altRankOf` | 61 | 2.2% |
| `vulgarSpellingOf` | 47 | 1.7% |
| `homonym` | 16 | 0.6% |
| `needsQualification` | 12 | 0.4% |
| `status` | 5 | 0.2% |
| `designation` | 4 | 0.1% |
| `holotype` | 1 | 0.0% |

### `timeFields` -- 166 instances in `data/`

| property | data | data % |
|---|---|---|
| `period` | 110 | 66.3% |
| `series` | 47 | 28.3% |
| `stage` | 15 | 9.0% |
| `seriesModifier` | 8 | 4.8% |
| `seriesRange` | 8 | 4.8% |
| `stageModifier` | 4 | 2.4% |
| `eon` | 0 | 0.0% |
| `era` | 0 | 0.0% |
| `seriesBoundary` | 0 | 0.0% |
| `stageBoundary` | 0 | 0.0% |
| `stageRange` | 0 | 0.0% |

### `translatedNode` -- 15 instances in `data/`

| property | data | data % |
|---|---|---|
| `by` | 1 | 6.7% |

### `tree` -- 6374 instances in `data/`

| property | data | data % |
|---|---|---|
| `children` | 2191 | 34.4% |
| `parents` | 324 | 5.1% |
| `altPlacements` | 7 | 0.1% |
| `mergeInto` | 5 | 0.1% |

### `treeDocument` -- 221 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxonomies` | 217 | 98.2% |
| `phylogenies` | 25 | 11.3% |
| `notes` | 20 | 9.0% |
| `repositories` | 6 | 2.7% |
| `assumptions` | 1 | 0.5% |
| `contexts` | 1 | 0.5% |
| `unused` | 0 | 0.0% |

### `uncertaintyFields` -- 6374 instances in `data/`

| property | data | data % |
|---|---|---|
| `provisional` | 122 | 1.9% |
| `tentative` | 17 | 0.3% |
| `quotedParent` | 14 | 0.2% |
| `questionable` | 13 | 0.2% |
| `quoted` | 2 | 0.0% |
| `nonMonophyletic` | 1 | 0.0% |
| `sensu` | 0 | 0.0% |

## 3. Enum member usage

### `phylogeny#/$defs/article/properties/audit/properties/coverage/additionalProperties`

4 of 4 members used, 240 occurrences.

| value | count |
|---|---|
| `'none'` | 75 |
| `'all'` | 70 |
| `'partly'` | 50 |
| `'na'` | 45 |

### `phylogeny#/$defs/article/properties/audit/properties/coverage/propertyNames`

8 of 8 members used, 240 occurrences.

| value | count |
|---|---|
| `'phylogeny'` | 30 |
| `'illustrations'` | 30 |
| `'occurrences'` | 30 |
| `'material'` | 30 |
| `'synonymy'` | 30 |
| `'types'` | 30 |
| `'newTaxa'` | 30 |
| `'skeleton'` | 30 |

### `phylogeny#/$defs/article/properties/audit/properties/state`

1 of 5 members used, 48 occurrences.

| value | count |
|---|---|
| `'partial'` | 48 |

**Never used (4):** `'complete'`, `'unaudited'`, `'unauditable'`, `'unobtainable'`

### `phylogeny#/$defs/eon`

0 of 4 members used, 0 occurrences.

**Never used (4):** `'Hadean'`, `'Archean'`, `'Proterozoic'`, `'Phanerozoic'`

### `phylogeny#/$defs/era`

0 of 10 members used, 0 occurrences.

**Never used (10):** `'Eoarchean'`, `'Paleoarchean'`, `'Mesoarchean'`, `'Neoarchean'`, `'Paleoproterozoic'`, `'Mesoproterozoic'`, `'Neoproterozoic'`, `'Paleozoic'`, `'Mesozoic'`, `'Cenozoic'`

### `phylogeny#/$defs/illustration/properties/depicts`

3 of 4 members used, 171 occurrences.

| value | count |
|---|---|
| `'cast'` | 130 |
| `'drawing'` | 38 |
| `'reconstruction'` | 3 |

**Never used (1):** `'specimen'`

### `phylogeny#/$defs/materialEntry/properties/roleAct`

1 of 2 members used, 1 occurrences.

| value | count |
|---|---|
| `'designated'` | 1 |

**Never used (1):** `'reported'`

### `phylogeny#/$defs/materialEntry/properties/status`

1 of 2 members used, 1 occurrences.

| value | count |
|---|---|
| `'lost'` | 1 |

**Never used (1):** `'untraced'`

### `phylogeny#/$defs/modularDate/properties/season`

1 of 5 members used, 1 occurrences.

| value | count |
|---|---|
| `'summer'` | 1 |

**Never used (4):** `'spring'`, `'fall'`, `'autumn'`, `'winter'`

### `phylogeny#/$defs/period`

3 of 22 members used, 110 occurrences.

| value | count |
|---|---|
| `'Cambrian'` | 63 |
| `'Ordovician'` | 44 |
| `'Silurian'` | 3 |

**Never used (19):** `'Siderian'`, `'Rhyacian'`, `'Orosirian'`, `'Statherian'`, `'Calymmian'`, `'Ectasian'`, `'Stenian'`, `'Tonian'`, `'Cryogenian'`, `'Ediacaran'`, `'Devonian'`, `'Carboniferous'`, `'Permian'`, `'Triassic'`, `'Jurassic'`, `'Cretaceous'`, `'Paleogene'`, `'Neogene'`, `'Quaternary'`

### `phylogeny#/$defs/phylogeny/properties/treeType`

2 of 4 members used, 36 occurrences.

| value | count |
|---|---|
| `'cladogram'` | 27 |
| `'diagram'` | 9 |

**Never used (2):** `'taxonomy'`, `'other'`

### `phylogeny#/$defs/publication/properties/type`

0 of 2 members used, 0 occurrences.

**Never used (2):** `'journal'`, `'book'`

### `phylogeny#/$defs/rank`

24 of 32 members used, 752 occurrences.

| value | count |
|---|---|
| `'Family'` | 177 |
| `'species'` | 140 |
| `'Order'` | 114 |
| `'Class'` | 90 |
| `'variety'` | 32 |
| `'Subfamily'` | 26 |
| `'genus'` | 24 |
| `'section'` | 22 |
| `'Superfamily'` | 18 |
| `'subgenus'` | 17 |
| `'Subclass'` | 15 |
| `'Phylum'` | 13 |
| `'Suborder'` | 13 |
| `'Subphylum'` | 11 |
| `'Group'` | 10 |
| `'Grade'` | 9 |
| `'Division'` | 6 |
| `'Subkingdom'` | 3 |
| `'Unranked'` | 3 |
| `'Plesion'` | 3 |
| `'Superorder'` | 2 |
| `'Branch'` | 2 |
| `'Parvclass'` | 1 |
| `'Kingdom'` | 1 |

**Never used (8):** `'Domain'`, `'Superphylum'`, `'Infraphylum'`, `'Superclass'`, `'Infraclass'`, `'subspecies'`, `'Clade'`, `'Scion'`

### `phylogeny#/$defs/repositories/additionalProperties/properties/subject`

2 of 4 members used, 8 occurrences.

| value | count |
|---|---|
| `'specimens'` | 5 |
| `'localities'` | 3 |

**Never used (2):** `'samples'`, `'unknown'`

### `phylogeny#/$defs/repositories/additionalProperties/properties/type`

3 of 4 members used, 49 occurrences.

| value | count |
|---|---|
| `'institution'` | 36 |
| `'collection'` | 10 |
| `'person'` | 3 |

**Never used (1):** `'unknown'`

### `phylogeny#/$defs/role`

12 of 12 members used, 223 occurrences.

| value | count |
|---|---|
| `'paratype'` | 87 |
| `'holotype'` | 79 |
| `'plesiotype'` | 32 |
| `'syntype'` | 8 |
| `'lectotype'` | 4 |
| `'figured'` | 3 |
| `'hypotype'` | 3 |
| `'topotype'` | 3 |
| `'chirotype'` | 1 |
| `'cotype'` | 1 |
| `'neotype'` | 1 |
| `'paralectotype'` | 1 |

### `phylogeny#/$defs/series`

7 of 38 members used, 63 occurrences.

| value | count |
|---|---|
| `'Middle Ordovician'` | 35 |
| `'Lower Ordovician'` | 15 |
| `'Lower Devonian'` | 6 |
| `'Middle Devonian'` | 4 |
| `'Upper Devonian'` | 1 |
| `'Llandovery'` | 1 |
| `'Upper Ordovician'` | 1 |

**Never used (31):** `'Terrenuevian'`, `'Cambrian Series 2'`, `'Miaolingian'`, `'Furongian'`, `'Wenlock'`, `'Ludlow'`, `'Přídolí'`, `'Lower Mississippian'`, `'Middle Mississippian'`, `'Upper Mississippian'`, `'Lower Pennsylvanian'`, `'Middle Pennsylvanian'`, `'Upper Pennsylvanian'`, `'Cisuralian'`, `'Guadalupian'`, `'Lopingian'`, `'Lower Triassic'`, `'Middle Triassic'`, `'Upper Triassic'`, `'Lower Jurassic'`, `'Middle Jurassic'`, `'Upper Jurassic'`, `'Lower Cretaceous'`, `'Upper Cretaceous'`, `'Paleocene'`, `'Eocene'`, `'Oligocene'`, `'Miocene'`, `'Pliocene'`, `'Pleistocene'`, `'Holocene'`

### `phylogeny#/$defs/stage`

8 of 100 members used, 15 occurrences.

| value | count |
|---|---|
| `'Eifelian'` | 3 |
| `'Emsian'` | 2 |
| `'Tremadocian'` | 2 |
| `'Floian'` | 2 |
| `'Katian'` | 2 |
| `'Telychian'` | 2 |
| `'Givetian'` | 1 |
| `'Jiangshanian'` | 1 |

**Never used (92):** `'Fortunian'`, `'Cambrian Stage 2'`, `'Cambrian Stage 3'`, `'Cambrian Stage 4'`, `'Wuliuan'`, `'Drumian'`, `'Guzhangian'`, `'Paibian'`, `'Cambrian Stage 10'`, `'Dapingian'`, `'Darriwilian'`, `'Sandbian'`, `'Hirnantian'`, `'Rhuddanian'`, `'Aeronian'`, `'Sheinwoodian'`, `'Homerian'`, `'Gorstian'`, `'Ludfordian'`, `'Lochkovian'`, `'Pragian'`, `'Frasnian'`, `'Famennian'`, `'Touraisian'`, `'Viséan'`, `'Serpukhovian'`, `'Baskirian'`, `'Moscovian'`, `'Kasimovian'`, `'Gzhelian'`, `'Asselian'`, `'Sakmarian'`, `'Artinskian'`, `'Kungurian'`, `'Roadian'`, `'Wordian'`, `'Capitanian'`, `'Wuchiapingian'`, `'Changhsingian'`, `'Induan'`, `'Olenekian'`, `'Anisian'`, `'Ladinian'`, `'Carnian'`, `'Norian'`, `'Rhaetian'`, `'Hettangian'`, `'Sinemurian'`, `'Toarcian'`, `'Aalenian'`, `'Bajocian'`, `'Bathonian'`, `'Callovian'`, `'Oxfordian'`, `'Kimmeridgian'`, `'Tithonian'`, `'Berriasian'`, `'Valanginian'`, `'Hauterivian'`, `'Barremian'`, `'Aptian'`, `'Albian'`, `'Cenomanian'`, `'Turonian'`, `'Coniacian'`, `'Santonian'`, `'Campanian'`, `'Maastrichtian'`, `'Danian'`, `'Selanian'`, `'Thanetian'`, `'Ypresian'`, `'Lutetian'`, `'Bartonian'`, `'Priabonian'`, `'Rupelian'`, `'Chattian'`, `'Aquitanian'`, `'Burdigalian'`, `'Langhian'`, `'Serravallian'`, `'Tortonian'`, `'Messinian'`, `'Zanclean'`, `'Piacenzian'`, `'Gelasian'`, `'Calabrian'`, `'Chibanian'`, `'Upper Pleistocene'`, `'Greenlandian'`, `'Northgrippian'`, `'Meghalayan'`

### `phylogeny#/$defs/stageModifier`

3 of 3 members used, 39 occurrences.

| value | count |
|---|---|
| `'upper'` | 21 |
| `'lower'` | 15 |
| `'middle'` | 3 |

### `phylogeny#/$defs/treeDocument/properties/unused/items`

0 of 5 members used, 0 occurrences.

**Never used (5):** `'material'`, `'illustrations'`, `'contexts'`, `'ranges'`, `'synonyms'`

### `phylogeny#/$defs/uncertaintyFields/properties/nonMonophyletic/oneOf/1`

0 of 2 members used, 0 occurrences.

**Never used (2):** `'paraphyletic'`, `'polyphyletic'`

### `phylogeny#/$defs/uncertaintyFields/properties/sensu`

0 of 3 members used, 0 occurrences.

**Never used (3):** `'stricto'`, `'lato'`, `'emendato'`

## 4. Observed value types where the schema allows a union

Tests whether each multi-type declaration is actually needed.

| location | declared | observed | string examples | declared but unseen |
|---|---|---|---|---|
| `phylogeny#/$defs/article/properties/articleNumber` | integer/string | intx5, strx2 | `e1465`, `e38296` | - |
| `phylogeny#/$defs/article/properties/chapter` | integer/string | strx1 | `Report of E. Billings, E...` | integer |
| `phylogeny#/$defs/article/properties/number` | integer/string | intx146, strx9 | `Supplement`, `1/2`, `Adv. Pr.`, `1–2` | - |
| `phylogeny#/$defs/article/properties/pages/items` | integer/string | intx398, strx42 | `S637`, `S634`, `S631`, `S627` | - |
| `phylogeny#/$defs/article/properties/plates/items` | integer/string | intx29, strx12 | `II`, `I`, `VI`, `V` | - |
| `phylogeny#/$defs/article/properties/series` | integer/string | intx8, strx1 | `A` | - |
| `phylogeny#/$defs/article/properties/volume` | integer/string | intx225, strx13 | `New Series`, `3: Echinoderms: Notes fo...`, `Report of the 68th Meeti...`, `II` | - |
| `phylogeny#/$defs/citationNumber` | integer/string | intx1460, strx212 | `IX`, `VIII`, `V`, `b` | - |
| `phylogeny#/$defs/cladisticFields/properties/matrix/items` | integer/string | intx139, strx5 | `?` | - |
| `phylogeny#/$defs/contexts` | object/null | dictx57, nullx41 | - | - |
| `phylogeny#/$defs/editorialObject/properties/inferred` | boolean/array | listx4, boolx3 | - | - |
| `phylogeny#/$defs/locationFields/properties/illustrations` | array/null | listx174, nullx12 | - | - |
| `phylogeny#/$defs/materialsFields/properties/material` | array/null | listx110, nullx9 | - | - |
| `phylogeny#/$defs/materialsFields/properties/ranges` | array/null | listx49, nullx41 | - | - |
| `phylogeny#/$defs/person/properties/death` | integer/null | intx80, nullx1 | - | - |
| `phylogeny#/$defs/phylogeny/properties/characteristics/items/additionalProperties/additionalProperties` | integer/string | intx40 | - | string |
| `phylogeny#/$defs/relationalFields/properties/synonyms` | array/null | listx360 | - | null |
| `phylogeny#/$defs/taxonRecord/properties/holotype/additionalProperties/items` | array/string/integer | strx1 | `E23470` | array, integer |
| `phylogeny#/$defs/taxonRecord/properties/name` | string/null | strx2466, nullx220 | `Zoophytes`, `Zoophyta`, `Zoophites`, `Zoanthida` | - |

