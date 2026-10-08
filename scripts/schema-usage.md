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
| `actAndModifierFields` | `phylogeny#/$defs/actAndModifierFields/properties/emended/oneOf/1`<br>`phylogeny#/$defs/actAndModifierFields/properties/recombined/oneOf/1` |
| `catalogNumber` | `phylogeny#/$defs/catalogNumber`<br>`phylogeny#/$defs/catalogNumber/oneOf/0`<br>`phylogeny#/$defs/catalogNumber/oneOf/1`<br>`phylogeny#/$defs/catalogNumber/oneOf/1/items` |
| `citedAct` | `phylogeny#/$defs/citedAct`<br>`phylogeny#/$defs/citedAct/properties/by` |
| `cladisticFields` | `phylogeny#/$defs/cladisticFields/properties/data`<br>`phylogeny#/$defs/cladisticFields/properties/data/additionalProperties` |
| `context` | `phylogeny#/$defs/context/properties/biota`<br>`phylogeny#/$defs/context/properties/biozones`<br>`phylogeny#/$defs/context/properties/biozones/items`<br>`phylogeny#/$defs/context/properties/collectedDate`<br>`phylogeny#/$defs/context/properties/localityNumbers/items/not`<br>`phylogeny#/$defs/context/properties/localityNumbers/items/properties/register`<br>`phylogeny#/$defs/context/properties/paleocontinent`<br>`phylogeny#/$defs/context/properties/sources`<br>`phylogeny#/$defs/context/properties/sources/items`<br>`phylogeny#/$defs/context/properties/tentative/oneOf/0` |
| `contextRef` | `phylogeny#/$defs/contextRef/oneOf/1`<br>`phylogeny#/$defs/contextRef/oneOf/1/properties/key`<br>`phylogeny#/$defs/contextRef/oneOf/1/properties/tentative` |
| `eon` | `phylogeny#/$defs/eon` |
| `era` | `phylogeny#/$defs/era` |
| `figureLocatorFields` | `phylogeny#/$defs/figureLocatorFields/properties/non` |
| `identificationFields` | `phylogeny#/$defs/identificationFields/properties/designation` |
| `inferredContext` | `phylogeny#/$defs/inferredContext/properties/basis`<br>`phylogeny#/$defs/inferredContext/properties/sources`<br>`phylogeny#/$defs/inferredContext/properties/sources/items` |
| `localTimeFields` | `phylogeny#/$defs/localTimeFields/properties/localStageBoundary` |
| `materialEntry` | `phylogeny#/$defs/materialEntry/properties/formerIds`<br>`phylogeny#/$defs/materialEntry/properties/formerIds/items`<br>`phylogeny#/$defs/materialEntry/properties/fragmentOf`<br>`phylogeny#/$defs/materialEntry/properties/roleUncertain`<br>`phylogeny#/$defs/materialEntry/properties/sameAs`<br>`phylogeny#/$defs/materialEntry/properties/sameAs/oneOf/0`<br>`phylogeny#/$defs/materialEntry/properties/sameAs/oneOf/1`<br>`phylogeny#/$defs/materialEntry/properties/sameAs/properties/label`<br>`phylogeny#/$defs/materialEntry/properties/sameAs/properties/number`<br>`phylogeny#/$defs/materialEntry/properties/sameAs/properties/prefix`<br>`phylogeny#/$defs/materialEntry/properties/sameAs/properties/source` |
| `modularDate` | `phylogeny#/$defs/modularDate/then/oneOf/2/properties/month/anyOf/5` |
| `person` | `phylogeny#/$defs/person/properties/suffix` |
| `publication` | `phylogeny#/$defs/publication/properties/type` |
| `range` | `phylogeny#/$defs/range/properties/inferred`<br>`phylogeny#/$defs/range/properties/tentative/oneOf/0` |
| `relationalFields` | `phylogeny#/$defs/relationalFields/properties/type`<br>`phylogeny#/$defs/relationalFields/properties/type/oneOf/0`<br>`phylogeny#/$defs/relationalFields/properties/type/oneOf/1` |
| `stageRange` | `phylogeny#/$defs/stageRange`<br>`phylogeny#/$defs/stageRange/items` |
| `taxonRecord` | `phylogeny#/$defs/taxonRecord/properties/holotype/additionalProperties/items/items`<br>`phylogeny#/$defs/taxonRecord/properties/rank/oneOf/1` |
| `timeFields` | `phylogeny#/$defs/timeFields/properties/eon`<br>`phylogeny#/$defs/timeFields/properties/era`<br>`phylogeny#/$defs/timeFields/properties/seriesBoundary`<br>`phylogeny#/$defs/timeFields/properties/stageBoundary`<br>`phylogeny#/$defs/timeFields/properties/stageRange` |
| `tree` | `tree#/properties/rank/oneOf/1` |
| `typeNode` | `phylogeny#/$defs/typeNode`<br>`phylogeny#/$defs/typeNode/properties/fixation`<br>`phylogeny#/$defs/typeNode/properties/fixedBy` |
| `uncertaintyFields` | `phylogeny#/$defs/uncertaintyFields/properties/nonMonophyletic/oneOf/1`<br>`phylogeny#/$defs/uncertaintyFields/properties/sensu` |

## 2. Property frequency by `$defs`

`data %` is the share of that container's instances carrying the
property.

### `actAndModifierFields` -- 5680 instances in `data/`

| property | data | data % |
|---|---|---|
| `new` | 1593 | 28.0% |
| `isType` | 369 | 6.5% |
| `emended` | 54 | 1.0% |
| `pars` | 19 | 0.3% |
| `translated` | 16 | 0.3% |
| `nudum` | 4 | 0.1% |
| `recombined` | 1 | 0.0% |
| `stem` | 1 | 0.0% |

### `article` -- 337 instances in `data/`

| property | data | data % |
|---|---|---|
| `authors` | 337 | 100.0% |
| `pubDate` | 336 | 99.7% |
| `volume` | 262 | 77.7% |
| `title` | 259 | 76.9% |
| `identifiers` | 235 | 69.7% |
| `pages` | 232 | 68.8% |
| `journal` | 216 | 64.1% |
| `number` | 166 | 49.3% |
| `identifiers.url` | 153 | 65.1% |
| `book` | 119 | 35.3% |
| `processDates` | 98 | 29.1% |
| `processDates.accepted` | 63 | 64.3% |
| `identifiers.doi` | 61 | 26.0% |
| `notes` | 54 | 16.0% |
| `processDates.received` | 53 | 54.1% |
| `audit` | 48 | 14.2% |
| `audit.notes` | 48 | 100.0% |
| `audit.state` | 48 | 100.0% |
| `audit.coverage` | 30 | 62.5% |
| `processDates.online` | 28 | 28.6% |
| `identifiers.jstor` | 24 | 10.2% |
| `plates` | 21 | 6.2% |
| `processDates.revised` | 18 | 18.4% |
| `series` | 9 | 2.7% |
| `processDates.read` | 8 | 8.2% |
| `articleNumber` | 7 | 2.1% |
| `seen` | 5 | 1.5% |
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

### `authority` -- 1810 instances in `data/`

| property | data | data % |
|---|---|---|
| `source` | 1810 | 100.0% |
| `pages` | 65 | 3.6% |
| `illustrations` | 29 | 1.6% |
| `attributedTo` | 24 | 1.3% |
| `ex` | 2 | 0.1% |
| `notes` | 2 | 0.1% |

### `authorityFields` -- 9323 instances in `data/`

| property | data | data % |
|---|---|---|
| `authority` | 1807 | 19.4% |
| `auth` | 976 | 10.5% |
| `year` | 974 | 10.4% |
| `in` | 28 | 0.3% |

### `citationFields` -- 9311 instances in `data/`

| property | data | data % |
|---|---|---|
| `citedAs` | 578 | 6.2% |

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
| `localityNumbers/items.number` | 52 | 100.0% |
| `biozone` | 48 | 42.5% |
| `localityNumbers` | 46 | 40.7% |
| `mapSheet` | 30 | 26.5% |
| `localityNumbers/items.prefix` | 21 | 40.4% |
| `notes` | 20 | 17.7% |
| `coordinatesAsPrinted` | 12 | 10.6% |
| `biozoneRange` | 7 | 6.2% |
| `tentative` | 3 | 2.7% |
| `collectedBy` | 2 | 1.8% |
| `fauna` | 1 | 0.9% |
| `inferred` | 1 | 0.9% |
| `biota` | 0 | 0.0% |
| `biozones` | 0 | 0.0% |
| `collectedDate` | 0 | 0.0% |
| `localityNumbers/items.register` | 0 | 0.0% |
| `paleocontinent` | 0 | 0.0% |
| `sources` | 0 | 0.0% |

### `editorialObject` -- 14 instances in `data/`

| property | data | data % |
|---|---|---|
| `basis` | 14 | 100.0% |
| `inferred` | 12 | 85.7% |
| `corrections` | 2 | 14.3% |
| `corrections.authority` | 2 | 100.0% |
| `corrections.authority.source` | 2 | 100.0% |

### `figureLocatorFields` -- 484 instances in `data/`

| property | data | data % |
|---|---|---|
| `figures` | 419 | 86.6% |
| `plate` | 345 | 71.3% |
| `page` | 126 | 26.0% |
| `textFigures` | 65 | 13.4% |
| `notes` | 23 | 4.8% |
| `non` | 0 | 0.0% |

### `identificationFields` -- 6474 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxon` | 5878 | 90.8% |
| `openTaxon` | 245 | 3.8% |
| `cf` | 15 | 0.2% |
| `aff` | 14 | 0.2% |
| `designation` | 0 | 0.0% |

### `illustration` -- 484 instances in `data/`

| property | data | data % |
|---|---|---|
| `of` | 241 | 49.8% |
| `depicts` | 171 | 35.3% |
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

### `locationFields` -- 9311 instances in `data/`

| property | data | data % |
|---|---|---|
| `illustrations` | 191 | 2.1% |

### `materialEntry` -- 291 instances in `data/`

| property | data | data % |
|---|---|---|
| `numbers` | 270 | 92.8% |
| `prefix` | 267 | 91.8% |
| `role` | 217 | 74.6% |
| `context` | 141 | 48.5% |
| `asPrinted` | 71 | 24.4% |
| `notes` | 66 | 22.7% |
| `label` | 18 | 6.2% |
| `preparation` | 17 | 5.8% |
| `repository` | 12 | 4.1% |
| `count` | 11 | 3.8% |
| `collectedBy` | 10 | 3.4% |
| `collectedDate` | 7 | 2.4% |
| `parts` | 6 | 2.1% |
| `holder` | 5 | 1.7% |
| `castOf` | 3 | 1.0% |
| `uncertain` | 2 | 0.7% |
| `editorial` | 1 | 0.3% |
| `examined` | 1 | 0.3% |
| `listComplete` | 1 | 0.3% |
| `roleAct` | 1 | 0.3% |
| `status` | 1 | 0.3% |
| `formerIds` | 0 | 0.0% |
| `fragmentOf` | 0 | 0.0% |
| `roleUncertain` | 0 | 0.0% |
| `sameAs` | 0 | 0.0% |
| `sameAs.label` | 0 | - |
| `sameAs.number` | 0 | - |
| `sameAs.prefix` | 0 | - |
| `sameAs.source` | 0 | - |

### `materialsFields` -- 5680 instances in `data/`

| property | data | data % |
|---|---|---|
| `material` | 119 | 2.1% |
| `contexts` | 97 | 1.7% |
| `ranges` | 90 | 1.6% |

### `metaFields` -- 6474 instances in `data/`

| property | data | data % |
|---|---|---|
| `notes` | 411 | 6.3% |
| `editorial` | 12 | 0.2% |

### `modularDate` -- 336 instances in `data/`

| property | data | data % |
|---|---|---|
| `year` | 336 | 100.0% |
| `month` | 82 | 24.4% |
| `day` | 32 | 9.5% |
| `/then/oneOf/2.day` | 19 | 100.0% |
| `/then/oneOf/2.month` | 19 | 100.0% |
| `/then/oneOf/1.day` | 11 | 100.0% |
| `/then/oneOf/1.month` | 11 | 100.0% |
| `months` | 4 | 1.2% |
| `/then/oneOf/0.day` | 2 | 100.0% |
| `/then/oneOf/0.month` | 2 | 100.0% |
| `season` | 1 | 0.3% |

### `person` -- 285 instances in `data/`

| property | data | data % |
|---|---|---|
| `given` | 285 | 100.0% |
| `surname` | 285 | 100.0% |
| `birth` | 85 | 29.8% |
| `death` | 84 | 29.5% |
| `suffix` | 0 | 0.0% |

### `phylogeny` -- 36 instances in `data/`

| property | data | data % |
|---|---|---|
| `tree` | 36 | 100.0% |
| `treeType` | 36 | 100.0% |
| `methodology` | 18 | 50.0% |
| `notes` | 6 | 16.7% |
| `characteristics` | 1 | 2.8% |

### `publication` -- 147 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 147 | 100.0% |
| `editors` | 9 | 6.1% |
| `place` | 8 | 5.4% |
| `publisher` | 8 | 5.4% |
| `notes` | 2 | 1.4% |
| `type` | 0 | 0.0% |

### `range` -- 52 instances in `data/`

| property | data | data % |
|---|---|---|
| `regions` | 34 | 65.4% |
| `asPrinted` | 13 | 25.0% |
| `notes` | 8 | 15.4% |
| `tentative` | 5 | 9.6% |
| `regions/items/oneOf/1.tentative` | 2 | 100.0% |
| `regions/items/oneOf/1.value` | 2 | 100.0% |
| `inferred` | 0 | 0.0% |

### `relationalFields` -- 5680 instances in `data/`

| property | data | data % |
|---|---|---|
| `synonyms` | 358 | 6.3% |
| `moved` | 31 | 0.5% |
| `corrected` | 5 | 0.1% |
| `non` | 4 | 0.1% |
| `or` | 3 | 0.1% |
| `lapsus` | 2 | 0.0% |
| `substituted` | 2 | 0.0% |
| `lapsusFor` | 1 | 0.0% |
| `removed` | 1 | 0.0% |
| `type` | 0 | 0.0% |

### `repositories` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `/additionalProperties.name` | 55 | 100.0% |
| `/additionalProperties.type` | 55 | 100.0% |
| `/additionalProperties.prefixes` | 50 | 90.9% |
| `/additionalProperties.place` | 34 | 61.8% |
| `/additionalProperties.within` | 15 | 27.3% |
| `/additionalProperties.subject` | 14 | 25.5% |
| `/additionalProperties.notes` | 8 | 14.5% |
| `/additionalProperties.otherNames` | 3 | 5.5% |

### `roles` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `/additionalProperties.meaning` | 12 | 100.0% |
| `/additionalProperties.regulated` | 12 | 100.0% |
| `/additionalProperties.article` | 6 | 50.0% |
| `/additionalProperties.notes` | 6 | 50.0% |
| `/additionalProperties.equivalent` | 2 | 16.7% |

### `sectionFields` -- 5680 instances in `data/`

| property | data | data % |
|---|---|---|
| `sectionEnd` | 23 | 0.4% |
| `sectionStart` | 23 | 0.4% |
| `sectionStart.section` | 23 | 100.0% |
| `sectionStart.citedAs` | 12 | 52.2% |
| `sectionStart.new` | 12 | 52.2% |
| `sectionStart.pages` | 12 | 52.2% |
| `sectionStart.notes` | 5 | 21.7% |
| `sectionStart.designation` | 3 | 13.0% |
| `sectionStart.editorial` | 1 | 4.3% |

### `sectionRecord` -- 12 instances in `data/`

| property | data | data % |
|---|---|---|
| `citedAs` | 12 | 100.0% |
| `name` | 12 | 100.0% |
| `pages` | 12 | 100.0% |
| `notes` | 5 | 41.7% |
| `/if.name` | 3 | 100.0% |
| `designation` | 3 | 25.0% |
| `needsQualification` | 1 | 8.3% |

### `taxonRecord` -- 2837 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 2801 | 98.7% |
| `rank` | 972 | 34.3% |
| `pages` | 255 | 9.0% |
| `notes` | 224 | 7.9% |
| `altSpellingOf` | 145 | 5.1% |
| `lang` | 73 | 2.6% |
| `originalParent` | 70 | 2.5% |
| `altRankOf` | 58 | 2.0% |
| `vulgarSpellingOf` | 45 | 1.6% |
| `homonym` | 16 | 0.6% |
| `bracket` | 13 | 0.5% |
| `needsQualification` | 11 | 0.4% |
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

### `tree` -- 6474 instances in `data/`

| property | data | data % |
|---|---|---|
| `children` | 2201 | 34.0% |
| `pages` | 810 | 12.5% |
| `parents` | 324 | 5.0% |
| `rank` | 124 | 1.9% |
| `bracketEnd` | 28 | 0.4% |
| `bracketStart` | 28 | 0.4% |
| `altPlacements` | 7 | 0.1% |
| `mergeInto` | 4 | 0.1% |

### `treeDocument` -- 220 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxonomies` | 216 | 98.2% |
| `prefixes` | 30 | 13.6% |
| `phylogenies` | 25 | 11.4% |
| `notes` | 17 | 7.7% |
| `unused` | 5 | 2.3% |
| `assumptions` | 1 | 0.5% |
| `contexts` | 1 | 0.5% |
| `localityRegister` | 1 | 0.5% |

### `uncertaintyFields` -- 6474 instances in `data/`

| property | data | data % |
|---|---|---|
| `provisional` | 123 | 1.9% |
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

24 of 32 members used, 1096 occurrences.

| value | count |
|---|---|
| `'species'` | 236 |
| `'Order'` | 210 |
| `'Family'` | 177 |
| `'genus'` | 132 |
| `'Class'` | 110 |
| `'variety'` | 59 |
| `'Subfamily'` | 26 |
| `'Superfamily'` | 18 |
| `'subgenus'` | 17 |
| `'Subclass'` | 15 |
| `'section'` | 14 |
| `'Suborder'` | 13 |
| `'Phylum'` | 12 |
| `'Subphylum'` | 11 |
| `'Group'` | 10 |
| `'Grade'` | 9 |
| `'Division'` | 7 |
| `'Kingdom'` | 6 |
| `'Subkingdom'` | 3 |
| `'Unranked'` | 3 |
| `'Plesion'` | 3 |
| `'Superorder'` | 2 |
| `'Branch'` | 2 |
| `'Parvclass'` | 1 |

**Never used (8):** `'Domain'`, `'Superphylum'`, `'Infraphylum'`, `'Superclass'`, `'Infraclass'`, `'subspecies'`, `'Clade'`, `'Scion'`

### `phylogeny#/$defs/repositories/additionalProperties/properties/subject`

2 of 4 members used, 14 occurrences.

| value | count |
|---|---|
| `'specimens'` | 8 |
| `'localities'` | 6 |

**Never used (2):** `'samples'`, `'unknown'`

### `phylogeny#/$defs/repositories/additionalProperties/properties/type`

3 of 4 members used, 55 occurrences.

| value | count |
|---|---|
| `'institution'` | 36 |
| `'collection'` | 15 |
| `'person'` | 4 |

**Never used (1):** `'unknown'`

### `phylogeny#/$defs/role`

12 of 12 members used, 231 occurrences.

| value | count |
|---|---|
| `'paratype'` | 95 |
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

2 of 6 members used, 9 occurrences.

| value | count |
|---|---|
| `'type'` | 5 |
| `'illustrations'` | 4 |

**Never used (4):** `'material'`, `'contexts'`, `'ranges'`, `'synonyms'`

### `phylogeny#/$defs/typeNode/properties/fixation`

0 of 8 members used, 0 occurrences.

**Never used (8):** `'originalDesignation'`, `'monotypy'`, `'subsequentDesignation'`, `'subsequentMonotypy'`, `'objectiveSynonymy'`, `'tautonymy'`, `'typus'`, `'iczn'`

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
| `phylogeny#/$defs/article/properties/number` | integer/string | intx156, strx10 | `Supplement`, `1/2`, `Adv. Pr.`, `1–2` | - |
| `phylogeny#/$defs/article/properties/pages/items` | integer/string | intx430, strx46 | `S637`, `S634`, `S631`, `S627` | - |
| `phylogeny#/$defs/article/properties/plates/items` | integer/string | intx29, strx12 | `II`, `I`, `VI`, `V` | - |
| `phylogeny#/$defs/article/properties/series` | integer/string | intx8, strx1 | `A` | - |
| `phylogeny#/$defs/article/properties/volume` | integer/string | intx249, strx13 | `New Series`, `3: Echinoderms: Notes fo...`, `Report of the 68th Meeti...`, `II` | - |
| `phylogeny#/$defs/citationNumber` | integer/string | intx2204, strx217 | `IV`, `IX`, `VIII`, `V` | - |
| `phylogeny#/$defs/cladisticFields/properties/matrix/items` | integer/string | intx139, strx5 | `?` | - |
| `phylogeny#/$defs/contexts` | object/null | dictx57, nullx41 | - | - |
| `phylogeny#/$defs/editorialObject/properties/inferred` | boolean/array | boolx6, listx6 | - | - |
| `phylogeny#/$defs/illustration/properties/of/oneOf/0` | string/integer | intx160, strx43 | `B`, `A`, `25962B`, `602-RO-5` | - |
| `phylogeny#/$defs/illustration/properties/of/oneOf/1/items` | string/integer | strx54, intx48 | `165406A`, `165406B`, `165405B`, `165405A` | - |
| `phylogeny#/$defs/locationFields/properties/illustrations` | array/null | listx179, nullx12 | - | - |
| `phylogeny#/$defs/materialEntry/properties/castOf` | string/integer | intx3 | - | string |
| `phylogeny#/$defs/materialsFields/properties/material` | array/null | listx110, nullx9 | - | - |
| `phylogeny#/$defs/materialsFields/properties/ranges` | array/null | listx49, nullx41 | - | - |
| `phylogeny#/$defs/person/properties/death` | integer/null | intx83, nullx1 | - | - |
| `phylogeny#/$defs/phylogeny/properties/characteristics/items/additionalProperties/additionalProperties` | integer/string | intx40 | - | string |
| `phylogeny#/$defs/printedNumber` | string/integer | intx437, strx246 | `S-3965`, `SH-2`, `SH-1`, `SC-4A` | - |
| `phylogeny#/$defs/relationalFields/properties/synonyms` | array/null | listx358 | - | null |
| `phylogeny#/$defs/sectionRecord/properties/name` | string/null | strx9, nullx3 | `Stellatae`, `Radiatae`, `Multivalvia`, `Lunatae` | - |
| `phylogeny#/$defs/taxonRecord/properties/holotype/additionalProperties/items` | array/string/integer | strx1 | `E23470` | array, integer |
| `phylogeny#/$defs/taxonRecord/properties/name` | string/null | strx2581, nullx220 | `Zoophytes`, `Zoophyta`, `Zoophites`, `Zoanthida` | - |
| `tree#/properties/children` | array/null | listx2201 | - | null |

