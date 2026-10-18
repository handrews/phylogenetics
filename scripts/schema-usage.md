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
| `actAndModifierFields` | `phylogeny#/$defs/actAndModifierFields/properties/recombined/oneOf/1`<br>`phylogeny#/$defs/actAndModifierFields/properties/restricted`<br>`phylogeny#/$defs/actAndModifierFields/properties/restrictedBy`<br>`phylogeny#/$defs/actAndModifierFields/properties/restrictedBy/items` |
| `authority` | `phylogeny#/$defs/authority/oneOf/1`<br>`phylogeny#/$defs/authority/properties/auctt`<br>`phylogeny#/$defs/authority/properties/auctt/oneOf/0`<br>`phylogeny#/$defs/authority/properties/auctt/oneOf/1` |
| `catalogNumber` | `phylogeny#/$defs/catalogNumber`<br>`phylogeny#/$defs/catalogNumber/oneOf/0`<br>`phylogeny#/$defs/catalogNumber/oneOf/1`<br>`phylogeny#/$defs/catalogNumber/oneOf/1/items` |
| `citedAct` | `phylogeny#/$defs/citedAct`<br>`phylogeny#/$defs/citedAct/properties/by` |
| `cladisticFields` | `phylogeny#/$defs/cladisticFields/properties/data`<br>`phylogeny#/$defs/cladisticFields/properties/data/additionalProperties` |
| `context` | `phylogeny#/$defs/context/properties/biozones`<br>`phylogeny#/$defs/context/properties/biozones/items`<br>`phylogeny#/$defs/context/properties/collectedDate`<br>`phylogeny#/$defs/context/properties/paleocontinent`<br>`phylogeny#/$defs/context/properties/sources`<br>`phylogeny#/$defs/context/properties/sources/items`<br>`phylogeny#/$defs/context/properties/tentative/oneOf/0` |
| `contextRef` | `phylogeny#/$defs/contextRef/oneOf/1`<br>`phylogeny#/$defs/contextRef/oneOf/1/properties/key`<br>`phylogeny#/$defs/contextRef/oneOf/1/properties/tentative` |
| `entryRef` | `phylogeny#/$defs/entryRef` |
| `entryRefFields` | `phylogeny#/$defs/entryRefFields`<br>`phylogeny#/$defs/entryRefFields/oneOf/0`<br>`phylogeny#/$defs/entryRefFields/oneOf/1`<br>`phylogeny#/$defs/entryRefFields/properties/label`<br>`phylogeny#/$defs/entryRefFields/properties/number`<br>`phylogeny#/$defs/entryRefFields/properties/prefix` |
| `entryRefOrNumber` | `phylogeny#/$defs/entryRefOrNumber/oneOf/1` |
| `eon` | `phylogeny#/$defs/eon` |
| `era` | `phylogeny#/$defs/era` |
| `figureLocatorFields` | `phylogeny#/$defs/figureLocatorFields/properties/non` |
| `identificationFields` | `phylogeny#/$defs/identificationFields/properties/designation` |
| `inferredContext` | `phylogeny#/$defs/inferredContext/properties/basis`<br>`phylogeny#/$defs/inferredContext/properties/sources`<br>`phylogeny#/$defs/inferredContext/properties/sources/items` |
| `localTimeFields` | `phylogeny#/$defs/localTimeFields/properties/localStageBoundary` |
| `localityNumber` | `phylogeny#/$defs/localityNumber/not`<br>`phylogeny#/$defs/localityNumber/properties/register` |
| `materialEntry` | `phylogeny#/$defs/materialEntry/properties/formerIds`<br>`phylogeny#/$defs/materialEntry/properties/formerIds/items`<br>`phylogeny#/$defs/materialEntry/properties/fragmentOf`<br>`phylogeny#/$defs/materialEntry/properties/roleUncertain`<br>`phylogeny#/$defs/materialEntry/properties/sameAs`<br>`phylogeny#/$defs/materialEntry/properties/sameAs/properties/source` |
| `modularDate` | `phylogeny#/$defs/modularDate/then/oneOf/2/properties/month/anyOf/5` |
| `person` | `phylogeny#/$defs/person/properties/suffix` |
| `publication` | `phylogeny#/$defs/publication/properties/type` |
| `range` | `phylogeny#/$defs/range/properties/inferred`<br>`phylogeny#/$defs/range/properties/tentative/oneOf/0` |
| `relationalFields` | `phylogeny#/$defs/relationalFields/properties/type`<br>`phylogeny#/$defs/relationalFields/properties/type/oneOf/0`<br>`phylogeny#/$defs/relationalFields/properties/type/oneOf/1` |
| `sourceAlias` | `phylogeny#/$defs/sourceAlias`<br>`phylogeny#/$defs/sourceAlias/properties/aliasOf` |
| `sources` | `phylogeny#/$defs/sources/additionalProperties/oneOf/1` |
| `stageRange` | `phylogeny#/$defs/stageRange`<br>`phylogeny#/$defs/stageRange/items` |
| `taxonRecord` | `phylogeny#/$defs/taxonRecord/properties/holotype/additionalProperties/items/items`<br>`phylogeny#/$defs/taxonRecord/properties/rank/oneOf/1` |
| `timeFields` | `phylogeny#/$defs/timeFields/properties/eon`<br>`phylogeny#/$defs/timeFields/properties/era`<br>`phylogeny#/$defs/timeFields/properties/seriesBoundary`<br>`phylogeny#/$defs/timeFields/properties/stageBoundary`<br>`phylogeny#/$defs/timeFields/properties/stageRange` |
| `tree` | `tree#/then/not`<br>`tree#/then/not/anyOf/0`<br>`tree#/then/not/anyOf/1`<br>`tree#/then/not/anyOf/2` |
| `typeNode` | `phylogeny#/$defs/typeNode`<br>`phylogeny#/$defs/typeNode/properties/fixation`<br>`phylogeny#/$defs/typeNode/properties/fixedBy` |
| `uncertaintyFields` | `phylogeny#/$defs/uncertaintyFields/properties/mutable`<br>`phylogeny#/$defs/uncertaintyFields/properties/nonMonophyletic/oneOf/1`<br>`phylogeny#/$defs/uncertaintyFields/properties/sensu` |

## 2. Property frequency by `$defs`

`data %` is the share of that container's instances carrying the
property.

### `actAndModifierFields` -- 5686 instances in `data/`

| property | data | data % |
|---|---|---|
| `new` | 1593 | 28.0% |
| `isType` | 369 | 6.5% |
| `emended` | 54 | 0.9% |
| `pars` | 19 | 0.3% |
| `translated` | 17 | 0.3% |
| `nudum` | 7 | 0.1% |
| `emendedBy` | 2 | 0.0% |
| `recombined` | 1 | 0.0% |
| `stem` | 1 | 0.0% |
| `restricted` | 0 | 0.0% |
| `restrictedBy` | 0 | 0.0% |

### `article` -- 344 instances in `data/`

| property | data | data % |
|---|---|---|
| `authors` | 344 | 100.0% |
| `pubDate` | 343 | 99.7% |
| `volume` | 267 | 77.6% |
| `title` | 264 | 76.7% |
| `identifiers` | 238 | 69.2% |
| `pages` | 237 | 68.9% |
| `journal` | 221 | 64.2% |
| `number` | 168 | 48.8% |
| `identifiers.url` | 156 | 65.5% |
| `book` | 121 | 35.2% |
| `processDates` | 98 | 28.5% |
| `processDates.accepted` | 63 | 64.3% |
| `identifiers.doi` | 61 | 25.6% |
| `notes` | 58 | 16.9% |
| `processDates.received` | 53 | 54.1% |
| `audit` | 48 | 14.0% |
| `audit.notes` | 48 | 100.0% |
| `audit.state` | 48 | 100.0% |
| `audit.coverage` | 30 | 62.5% |
| `processDates.online` | 28 | 28.6% |
| `identifiers.jstor` | 24 | 10.1% |
| `plates` | 21 | 6.1% |
| `processDates.revised` | 18 | 18.4% |
| `series` | 11 | 3.2% |
| `processDates.read` | 8 | 8.2% |
| `articleNumber` | 7 | 2.0% |
| `seen` | 5 | 1.5% |
| `processDates.transmitted` | 4 | 4.1% |
| `processDates.conferenceEnd` | 3 | 3.1% |
| `processDates.conferenceStart` | 3 | 3.1% |
| `processDates.issued` | 3 | 3.1% |
| `processDates.submitted` | 3 | 3.1% |
| `chapter` | 2 | 0.6% |
| `translationOf` | 2 | 0.6% |
| `translations` | 2 | 0.6% |
| `editors` | 1 | 0.3% |
| `inPrep` | 1 | 0.3% |
| `processDates.printed` | 1 | 1.0% |
| `processDates.published` | 1 | 1.0% |
| `processDates.unknown` | 1 | 1.0% |
| `quotes` | 1 | 0.3% |
| `reading` | 1 | 0.3% |

### `authority` -- 1829 instances in `data/`

| property | data | data % |
|---|---|---|
| `source` | 1829 | 100.0% |
| `pages` | 65 | 3.6% |
| `illustrations` | 30 | 1.6% |
| `attributedTo` | 24 | 1.3% |
| `ex` | 2 | 0.1% |
| `notes` | 2 | 0.1% |
| `auctt` | 0 | 0.0% |

### `authorityFields` -- 9332 instances in `data/`

| property | data | data % |
|---|---|---|
| `auth` | 967 | 10.4% |
| `year` | 965 | 10.3% |
| `in` | 28 | 0.3% |

### `citationFields` -- 9320 instances in `data/`

| property | data | data % |
|---|---|---|
| `citedAs` | 605 | 6.5% |

### `cladisticFields` -- 794 instances in `data/`

| property | data | data % |
|---|---|---|
| `outgroup` | 19 | 2.4% |
| `matrix` | 8 | 1.0% |
| `bootstrap` | 6 | 0.8% |
| `data` | 0 | 0.0% |

### `context` -- 115 instances in `data/`

| property | data | data % |
|---|---|---|
| `location` | 114 | 99.1% |
| `unit` | 106 | 92.2% |
| `biozone` | 48 | 41.7% |
| `localityNumbers` | 46 | 40.0% |
| `mapSheet` | 30 | 26.1% |
| `notes` | 20 | 17.4% |
| `coordinatesAsPrinted` | 12 | 10.4% |
| `biozoneRange` | 7 | 6.1% |
| `tentative` | 3 | 2.6% |
| `biota` | 2 | 1.7% |
| `collectedBy` | 2 | 1.7% |
| `fauna` | 1 | 0.9% |
| `inferred` | 1 | 0.9% |
| `biozones` | 0 | 0.0% |
| `collectedDate` | 0 | 0.0% |
| `paleocontinent` | 0 | 0.0% |
| `sources` | 0 | 0.0% |

### `editorialObject` -- 18 instances in `data/`

| property | data | data % |
|---|---|---|
| `basis` | 18 | 100.0% |
| `inferred` | 13 | 72.2% |
| `corrections` | 5 | 27.8% |
| `corrections.authority` | 4 | 80.0% |
| `corrections.authority.source` | 4 | 100.0% |

### `figureLocatorFields` -- 492 instances in `data/`

| property | data | data % |
|---|---|---|
| `figures` | 427 | 86.8% |
| `plate` | 353 | 71.7% |
| `page` | 126 | 25.6% |
| `textFigures` | 65 | 13.2% |
| `notes` | 24 | 4.9% |
| `non` | 0 | 0.0% |

### `identificationFields` -- 6480 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxon` | 5886 | 90.8% |
| `openTaxon` | 243 | 3.8% |
| `cf` | 15 | 0.2% |
| `aff` | 14 | 0.2% |
| `designation` | 0 | 0.0% |

### `illustration` -- 492 instances in `data/`

| property | data | data % |
|---|---|---|
| `of` | 247 | 50.2% |
| `depicts` | 171 | 34.8% |
| `uncertain` | 2 | 0.4% |

### `inferredContext` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `paleocontinent` | 1 | 100.0% |
| `basis` | 0 | 0.0% |
| `sources` | 0 | 0.0% |

### `localTimeFields` -- 170 instances in `data/`

| property | data | data % |
|---|---|---|
| `localSeries` | 65 | 38.2% |
| `localSeriesModifier` | 26 | 15.3% |
| `localSeriesRange` | 9 | 5.3% |
| `localStage` | 9 | 5.3% |
| `localStageRange` | 6 | 3.5% |
| `localPeriod` | 3 | 1.8% |
| `localSeriesBoundary` | 1 | 0.6% |
| `localStageModifier` | 1 | 0.6% |
| `localStageBoundary` | 0 | 0.0% |

### `localityNumber` -- 59 instances in `data/`

| property | data | data % |
|---|---|---|
| `number` | 59 | 100.0% |
| `prefix` | 28 | 47.5% |
| `register` | 0 | 0.0% |

### `locationFields` -- 9320 instances in `data/`

| property | data | data % |
|---|---|---|
| `illustrations` | 197 | 2.1% |

### `materialEntry` -- 298 instances in `data/`

| property | data | data % |
|---|---|---|
| `numbers` | 277 | 93.0% |
| `prefix` | 274 | 91.9% |
| `role` | 217 | 72.8% |
| `context` | 148 | 49.7% |
| `asPrinted` | 78 | 26.2% |
| `notes` | 66 | 22.1% |
| `label` | 18 | 6.0% |
| `preparation` | 17 | 5.7% |
| `repository` | 12 | 4.0% |
| `count` | 11 | 3.7% |
| `collectedBy` | 10 | 3.4% |
| `collectedDate` | 7 | 2.3% |
| `localityNumbers` | 7 | 2.3% |
| `parts` | 6 | 2.0% |
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
| `sameAs.source` | 0 | - |

### `materialsFields` -- 5686 instances in `data/`

| property | data | data % |
|---|---|---|
| `material` | 125 | 2.2% |
| `contexts` | 97 | 1.7% |
| `ranges` | 93 | 1.6% |

### `metaFields` -- 6480 instances in `data/`

| property | data | data % |
|---|---|---|
| `notes` | 420 | 6.5% |
| `editorial` | 16 | 0.2% |

### `modularDate` -- 343 instances in `data/`

| property | data | data % |
|---|---|---|
| `year` | 343 | 100.0% |
| `month` | 82 | 23.9% |
| `day` | 32 | 9.3% |
| `/then/oneOf/2.day` | 19 | 100.0% |
| `/then/oneOf/2.month` | 19 | 100.0% |
| `/then/oneOf/1.day` | 11 | 100.0% |
| `/then/oneOf/1.month` | 11 | 100.0% |
| `months` | 4 | 1.2% |
| `/then/oneOf/0.day` | 2 | 100.0% |
| `/then/oneOf/0.month` | 2 | 100.0% |
| `season` | 1 | 0.3% |

### `person` -- 288 instances in `data/`

| property | data | data % |
|---|---|---|
| `given` | 288 | 100.0% |
| `surname` | 288 | 100.0% |
| `birth` | 88 | 30.6% |
| `death` | 86 | 29.9% |
| `suffix` | 0 | 0.0% |

### `phylogeny` -- 36 instances in `data/`

| property | data | data % |
|---|---|---|
| `tree` | 36 | 100.0% |
| `treeType` | 36 | 100.0% |
| `methodology` | 18 | 50.0% |
| `notes` | 6 | 16.7% |
| `characteristics` | 1 | 2.8% |

### `publication` -- 154 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 154 | 100.0% |
| `editors` | 9 | 5.8% |
| `place` | 8 | 5.2% |
| `publisher` | 8 | 5.2% |
| `notes` | 3 | 1.9% |
| `type` | 0 | 0.0% |

### `range` -- 55 instances in `data/`

| property | data | data % |
|---|---|---|
| `regions` | 37 | 67.3% |
| `asPrinted` | 13 | 23.6% |
| `notes` | 8 | 14.5% |
| `tentative` | 5 | 9.1% |
| `regions/items/oneOf/1.tentative` | 2 | 100.0% |
| `regions/items/oneOf/1.value` | 2 | 100.0% |
| `inferred` | 0 | 0.0% |

### `relationalFields` -- 5686 instances in `data/`

| property | data | data % |
|---|---|---|
| `synonyms` | 358 | 6.3% |
| `moved` | 33 | 0.6% |
| `corrected` | 5 | 0.1% |
| `non` | 5 | 0.1% |
| `lapsus` | 3 | 0.1% |
| `or` | 3 | 0.1% |
| `removed` | 2 | 0.0% |
| `substituted` | 2 | 0.0% |
| `lapsusFor` | 1 | 0.0% |
| `type` | 0 | 0.0% |

### `repositories` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `/additionalProperties.name` | 57 | 100.0% |
| `/additionalProperties.type` | 57 | 100.0% |
| `/additionalProperties.prefixes` | 52 | 91.2% |
| `/additionalProperties.place` | 34 | 59.6% |
| `/additionalProperties.within` | 16 | 28.1% |
| `/additionalProperties.subject` | 15 | 26.3% |
| `/additionalProperties.notes` | 9 | 15.8% |
| `/additionalProperties.otherNames` | 3 | 5.3% |

### `roles` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `/additionalProperties.meaning` | 12 | 100.0% |
| `/additionalProperties.regulated` | 12 | 100.0% |
| `/additionalProperties.article` | 6 | 50.0% |
| `/additionalProperties.notes` | 6 | 50.0% |
| `/additionalProperties.equivalent` | 2 | 16.7% |

### `sectionFields` -- 5686 instances in `data/`

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
| `authority` | 11 | 91.7% |
| `notes` | 5 | 41.7% |
| `/if.name` | 3 | 100.0% |
| `designation` | 3 | 25.0% |
| `needsQualification` | 1 | 8.3% |

### `taxonRecord` -- 2840 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 2804 | 98.7% |
| `authority` | 1703 | 60.0% |
| `rank` | 973 | 34.3% |
| `pages` | 255 | 9.0% |
| `notes` | 231 | 8.1% |
| `altSpellingOf` | 148 | 5.2% |
| `lang` | 73 | 2.6% |
| `originalParent` | 70 | 2.5% |
| `altRankOf` | 58 | 2.0% |
| `vulgarSpellingOf` | 45 | 1.6% |
| `homonym` | 16 | 0.6% |
| `bracket` | 13 | 0.5% |
| `needsQualification` | 11 | 0.4% |
| `status` | 6 | 0.2% |
| `designation` | 4 | 0.1% |
| `holotype` | 1 | 0.0% |

### `timeFields` -- 171 instances in `data/`

| property | data | data % |
|---|---|---|
| `period` | 110 | 64.3% |
| `series` | 47 | 27.5% |
| `stage` | 18 | 10.5% |
| `seriesModifier` | 8 | 4.7% |
| `seriesRange` | 8 | 4.7% |
| `stageModifier` | 4 | 2.3% |
| `eon` | 0 | 0.0% |
| `era` | 0 | 0.0% |
| `seriesBoundary` | 0 | 0.0% |
| `stageBoundary` | 0 | 0.0% |
| `stageRange` | 0 | 0.0% |

### `translatedNode` -- 16 instances in `data/`

| property | data | data % |
|---|---|---|
| `by` | 1 | 6.2% |

### `tree` -- 6480 instances in `data/`

| property | data | data % |
|---|---|---|
| `children` | 2205 | 34.0% |
| `pages` | 837 | 12.9% |
| `parents` | 324 | 5.0% |
| `rank` | 150 | 2.3% |
| `authority` | 118 | 1.8% |
| `bracketEnd` | 28 | 0.4% |
| `bracketStart` | 28 | 0.4% |
| `/if.authority` | 8 | 100.0% |
| `altPlacements` | 7 | 0.1% |
| `mergeInto` | 4 | 0.1% |

### `treeDocument` -- 220 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxonomies` | 216 | 98.2% |
| `prefixes` | 31 | 14.1% |
| `phylogenies` | 25 | 11.4% |
| `notes` | 17 | 7.7% |
| `unused` | 5 | 2.3% |
| `contexts` | 2 | 0.9% |
| `assumptions` | 1 | 0.5% |
| `localityRegister` | 1 | 0.5% |

### `uncertaintyFields` -- 6480 instances in `data/`

| property | data | data % |
|---|---|---|
| `provisional` | 124 | 1.9% |
| `tentative` | 17 | 0.3% |
| `quotedParent` | 14 | 0.2% |
| `questionable` | 13 | 0.2% |
| `quoted` | 2 | 0.0% |
| `nonMonophyletic` | 1 | 0.0% |
| `mutable` | 0 | 0.0% |
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

24 of 32 members used, 1121 occurrences.

| value | count |
|---|---|
| `'species'` | 236 |
| `'Order'` | 213 |
| `'Family'` | 180 |
| `'genus'` | 132 |
| `'Class'` | 117 |
| `'variety'` | 59 |
| `'Subfamily'` | 26 |
| `'Superfamily'` | 19 |
| `'subgenus'` | 17 |
| `'Phylum'` | 16 |
| `'Subphylum'` | 16 |
| `'Subclass'` | 15 |
| `'section'` | 14 |
| `'Suborder'` | 14 |
| `'Group'` | 11 |
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

2 of 4 members used, 15 occurrences.

| value | count |
|---|---|
| `'specimens'` | 8 |
| `'localities'` | 7 |

**Never used (2):** `'samples'`, `'unknown'`

### `phylogeny#/$defs/repositories/additionalProperties/properties/type`

3 of 4 members used, 57 occurrences.

| value | count |
|---|---|
| `'institution'` | 37 |
| `'collection'` | 16 |
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

9 of 100 members used, 18 occurrences.

| value | count |
|---|---|
| `'Wuliuan'` | 3 |
| `'Eifelian'` | 3 |
| `'Emsian'` | 2 |
| `'Tremadocian'` | 2 |
| `'Floian'` | 2 |
| `'Katian'` | 2 |
| `'Telychian'` | 2 |
| `'Givetian'` | 1 |
| `'Jiangshanian'` | 1 |

**Never used (91):** `'Fortunian'`, `'Cambrian Stage 2'`, `'Cambrian Stage 3'`, `'Cambrian Stage 4'`, `'Drumian'`, `'Guzhangian'`, `'Paibian'`, `'Cambrian Stage 10'`, `'Dapingian'`, `'Darriwilian'`, `'Sandbian'`, `'Hirnantian'`, `'Rhuddanian'`, `'Aeronian'`, `'Sheinwoodian'`, `'Homerian'`, `'Gorstian'`, `'Ludfordian'`, `'Lochkovian'`, `'Pragian'`, `'Frasnian'`, `'Famennian'`, `'Touraisian'`, `'Viséan'`, `'Serpukhovian'`, `'Baskirian'`, `'Moscovian'`, `'Kasimovian'`, `'Gzhelian'`, `'Asselian'`, `'Sakmarian'`, `'Artinskian'`, `'Kungurian'`, `'Roadian'`, `'Wordian'`, `'Capitanian'`, `'Wuchiapingian'`, `'Changhsingian'`, `'Induan'`, `'Olenekian'`, `'Anisian'`, `'Ladinian'`, `'Carnian'`, `'Norian'`, `'Rhaetian'`, `'Hettangian'`, `'Sinemurian'`, `'Toarcian'`, `'Aalenian'`, `'Bajocian'`, `'Bathonian'`, `'Callovian'`, `'Oxfordian'`, `'Kimmeridgian'`, `'Tithonian'`, `'Berriasian'`, `'Valanginian'`, `'Hauterivian'`, `'Barremian'`, `'Aptian'`, `'Albian'`, `'Cenomanian'`, `'Turonian'`, `'Coniacian'`, `'Santonian'`, `'Campanian'`, `'Maastrichtian'`, `'Danian'`, `'Selanian'`, `'Thanetian'`, `'Ypresian'`, `'Lutetian'`, `'Bartonian'`, `'Priabonian'`, `'Rupelian'`, `'Chattian'`, `'Aquitanian'`, `'Burdigalian'`, `'Langhian'`, `'Serravallian'`, `'Tortonian'`, `'Messinian'`, `'Zanclean'`, `'Piacenzian'`, `'Gelasian'`, `'Calabrian'`, `'Chibanian'`, `'Upper Pleistocene'`, `'Greenlandian'`, `'Northgrippian'`, `'Meghalayan'`

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
| `phylogeny#/$defs/article/properties/chapter` | integer/string | strx2 | `III. Stamm. Echinodermat...`, `Report of E. Billings, E...` | integer |
| `phylogeny#/$defs/article/properties/number` | integer/string | intx157, strx11 | `Supplement`, `1/2`, `Adv. Pr.`, `1–2` | - |
| `phylogeny#/$defs/article/properties/pages/items` | integer/string | intx440, strx46 | `S637`, `S634`, `S631`, `S627` | - |
| `phylogeny#/$defs/article/properties/plates/items` | integer/string | intx29, strx12 | `II`, `I`, `VI`, `V` | - |
| `phylogeny#/$defs/article/properties/series` | integer/string | intx10, strx1 | `A` | - |
| `phylogeny#/$defs/article/properties/volume` | integer/string | intx253, strx14 | `New Series`, `3: Echinoderms: Notes fo...`, `Report of the 68th Meeti...`, `II` | - |
| `phylogeny#/$defs/citationNumber` | integer/string | intx2250, strx226 | `IV`, `II`, `IX`, `VIII` | - |
| `phylogeny#/$defs/cladisticFields/properties/matrix/items` | integer/string | intx139, strx5 | `?` | - |
| `phylogeny#/$defs/contexts` | object/null | dictx58, nullx41 | - | - |
| `phylogeny#/$defs/editorialObject/properties/inferred` | boolean/array | listx9, boolx4 | - | - |
| `phylogeny#/$defs/locationFields/properties/illustrations` | array/null | listx185, nullx12 | - | - |
| `phylogeny#/$defs/materialsFields/properties/material` | array/null | listx116, nullx9 | - | - |
| `phylogeny#/$defs/materialsFields/properties/ranges` | array/null | listx52, nullx41 | - | - |
| `phylogeny#/$defs/person/properties/death` | integer/null | intx85, nullx1 | - | - |
| `phylogeny#/$defs/phylogeny/properties/characteristics/items/additionalProperties/additionalProperties` | integer/string | intx40 | - | string |
| `phylogeny#/$defs/printedNumber` | string/integer | intx661, strx350 | `B`, `A`, `S-3965`, `SH-2` | - |
| `phylogeny#/$defs/relationalFields/properties/synonyms` | array/null | listx358 | - | null |
| `phylogeny#/$defs/sectionRecord/properties/name` | string/null | strx9, nullx3 | `Stellatae`, `Radiatae`, `Multivalvia`, `Lunatae` | - |
| `phylogeny#/$defs/taxonRecord/properties/holotype/additionalProperties/items` | array/string/integer | strx1 | `E23470` | array, integer |
| `phylogeny#/$defs/taxonRecord/properties/name` | string/null | strx2584, nullx220 | `Zoophytes`, `Zoophyta`, `Zoophites`, `Zoanthida` | - |
| `tree#/properties/children` | array/null | listx2202, nullx3 | - | - |

