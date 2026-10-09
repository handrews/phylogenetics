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
| `context` | `phylogeny#/$defs/context/properties/biozones`<br>`phylogeny#/$defs/context/properties/biozones/items`<br>`phylogeny#/$defs/context/properties/collectedDate`<br>`phylogeny#/$defs/context/properties/localityNumbers/items/not`<br>`phylogeny#/$defs/context/properties/localityNumbers/items/properties/register`<br>`phylogeny#/$defs/context/properties/paleocontinent`<br>`phylogeny#/$defs/context/properties/sources`<br>`phylogeny#/$defs/context/properties/sources/items`<br>`phylogeny#/$defs/context/properties/tentative/oneOf/0` |
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
| `relationalFields` | `phylogeny#/$defs/relationalFields/properties/type/oneOf/1` |
| `stageRange` | `phylogeny#/$defs/stageRange`<br>`phylogeny#/$defs/stageRange/items` |
| `taxonRecord` | `phylogeny#/$defs/taxonRecord/properties/holotype/additionalProperties/items/items` |
| `timeFields` | `phylogeny#/$defs/timeFields/properties/eon`<br>`phylogeny#/$defs/timeFields/properties/era`<br>`phylogeny#/$defs/timeFields/properties/seriesBoundary`<br>`phylogeny#/$defs/timeFields/properties/stageBoundary`<br>`phylogeny#/$defs/timeFields/properties/stageRange` |
| `tree` | `tree#/then/not`<br>`tree#/then/not/anyOf/0`<br>`tree#/then/not/anyOf/1`<br>`tree#/then/not/anyOf/2` |
| `typeNode` | `phylogeny#/$defs/typeNode/properties/fixedBy` |
| `uncertaintyFields` | `phylogeny#/$defs/uncertaintyFields/properties/nonMonophyletic/oneOf/1`<br>`phylogeny#/$defs/uncertaintyFields/properties/sensu` |

## 2. Property frequency by `$defs`

`data %` is the share of that container's instances carrying the
property.

### `actAndModifierFields` -- 5679 instances in `data/`

| property | data | data % |
|---|---|---|
| `new` | 1592 | 28.0% |
| `isType` | 366 | 6.4% |
| `emended` | 56 | 1.0% |
| `pars` | 19 | 0.3% |
| `translated` | 17 | 0.3% |
| `nudum` | 4 | 0.1% |
| `recombined` | 2 | 0.0% |
| `stem` | 1 | 0.0% |

### `article` -- 340 instances in `data/`

| property | data | data % |
|---|---|---|
| `authors` | 340 | 100.0% |
| `pubDate` | 339 | 99.7% |
| `volume` | 265 | 77.9% |
| `title` | 261 | 76.8% |
| `identifiers` | 236 | 69.4% |
| `pages` | 235 | 69.1% |
| `journal` | 218 | 64.1% |
| `number` | 167 | 49.1% |
| `identifiers.url` | 154 | 65.3% |
| `book` | 120 | 35.3% |
| `processDates` | 98 | 28.8% |
| `processDates.accepted` | 63 | 64.3% |
| `identifiers.doi` | 61 | 25.8% |
| `notes` | 56 | 16.5% |
| `processDates.received` | 53 | 54.1% |
| `audit` | 48 | 14.1% |
| `audit.notes` | 48 | 100.0% |
| `audit.state` | 48 | 100.0% |
| `audit.coverage` | 30 | 62.5% |
| `processDates.online` | 28 | 28.6% |
| `identifiers.jstor` | 24 | 10.2% |
| `plates` | 21 | 6.2% |
| `processDates.revised` | 18 | 18.4% |
| `series` | 11 | 3.2% |
| `processDates.read` | 8 | 8.2% |
| `articleNumber` | 7 | 2.1% |
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

### `authority` -- 1846 instances in `data/`

| property | data | data % |
|---|---|---|
| `source` | 1846 | 100.0% |
| `pages` | 65 | 3.5% |
| `illustrations` | 30 | 1.6% |
| `attributedTo` | 24 | 1.3% |
| `ex` | 13 | 0.7% |
| `notes` | 2 | 0.1% |

### `authorityFields` -- 9323 instances in `data/`

| property | data | data % |
|---|---|---|
| `auth` | 968 | 10.4% |
| `year` | 966 | 10.4% |
| `in` | 28 | 0.3% |

### `citationFields` -- 9311 instances in `data/`

| property | data | data % |
|---|---|---|
| `citedAs` | 630 | 6.8% |

### `cladisticFields` -- 794 instances in `data/`

| property | data | data % |
|---|---|---|
| `outgroup` | 19 | 2.4% |
| `matrix` | 8 | 1.0% |
| `bootstrap` | 6 | 0.8% |
| `data` | 0 | 0.0% |

### `context` -- 114 instances in `data/`

| property | data | data % |
|---|---|---|
| `location` | 113 | 99.1% |
| `unit` | 105 | 92.1% |
| `localityNumbers/items.number` | 52 | 100.0% |
| `biozone` | 48 | 42.1% |
| `localityNumbers` | 46 | 40.4% |
| `mapSheet` | 30 | 26.3% |
| `localityNumbers/items.prefix` | 21 | 40.4% |
| `notes` | 20 | 17.5% |
| `coordinatesAsPrinted` | 12 | 10.5% |
| `biozoneRange` | 7 | 6.1% |
| `tentative` | 3 | 2.6% |
| `collectedBy` | 2 | 1.8% |
| `biota` | 1 | 0.9% |
| `fauna` | 1 | 0.9% |
| `inferred` | 1 | 0.9% |
| `biozones` | 0 | 0.0% |
| `collectedDate` | 0 | 0.0% |
| `localityNumbers/items.register` | 0 | 0.0% |
| `paleocontinent` | 0 | 0.0% |
| `sources` | 0 | 0.0% |

### `editorialObject` -- 17 instances in `data/`

| property | data | data % |
|---|---|---|
| `basis` | 17 | 100.0% |
| `inferred` | 12 | 70.6% |
| `corrections` | 5 | 29.4% |
| `corrections.authority` | 4 | 80.0% |
| `corrections.authority.source` | 4 | 100.0% |

### `figureLocatorFields` -- 490 instances in `data/`

| property | data | data % |
|---|---|---|
| `figures` | 425 | 86.7% |
| `plate` | 346 | 70.6% |
| `page` | 131 | 26.7% |
| `textFigures` | 65 | 13.3% |
| `notes` | 24 | 4.9% |
| `non` | 0 | 0.0% |

### `identificationFields` -- 6473 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxon` | 5879 | 90.8% |
| `openTaxon` | 243 | 3.8% |
| `cf` | 15 | 0.2% |
| `aff` | 14 | 0.2% |
| `designation` | 0 | 0.0% |

### `illustration` -- 490 instances in `data/`

| property | data | data % |
|---|---|---|
| `of` | 246 | 50.2% |
| `depicts` | 174 | 35.5% |
| `uncertain` | 2 | 0.4% |

### `inferredContext` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `paleocontinent` | 1 | 100.0% |
| `basis` | 0 | 0.0% |
| `sources` | 0 | 0.0% |

### `localTimeFields` -- 166 instances in `data/`

| property | data | data % |
|---|---|---|
| `localSeries` | 65 | 39.2% |
| `localSeriesModifier` | 26 | 15.7% |
| `localSeriesRange` | 9 | 5.4% |
| `localStage` | 9 | 5.4% |
| `localStageRange` | 6 | 3.6% |
| `localPeriod` | 3 | 1.8% |
| `localSeriesBoundary` | 1 | 0.6% |
| `localStageModifier` | 1 | 0.6% |
| `localStageBoundary` | 0 | 0.0% |

### `locationFields` -- 9311 instances in `data/`

| property | data | data % |
|---|---|---|
| `illustrations` | 192 | 2.1% |

### `materialEntry` -- 292 instances in `data/`

| property | data | data % |
|---|---|---|
| `numbers` | 271 | 92.8% |
| `prefix` | 268 | 91.8% |
| `role` | 218 | 74.7% |
| `context` | 143 | 49.0% |
| `asPrinted` | 71 | 24.3% |
| `notes` | 67 | 22.9% |
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

### `materialsFields` -- 5679 instances in `data/`

| property | data | data % |
|---|---|---|
| `material` | 119 | 2.1% |
| `contexts` | 98 | 1.7% |
| `ranges` | 90 | 1.6% |

### `metaFields` -- 6473 instances in `data/`

| property | data | data % |
|---|---|---|
| `notes` | 415 | 6.4% |
| `editorial` | 15 | 0.2% |

### `modularDate` -- 339 instances in `data/`

| property | data | data % |
|---|---|---|
| `year` | 339 | 100.0% |
| `month` | 82 | 24.2% |
| `day` | 32 | 9.4% |
| `/then/oneOf/2.day` | 19 | 100.0% |
| `/then/oneOf/2.month` | 19 | 100.0% |
| `/then/oneOf/1.day` | 11 | 100.0% |
| `/then/oneOf/1.month` | 11 | 100.0% |
| `months` | 4 | 1.2% |
| `/then/oneOf/0.day` | 2 | 100.0% |
| `/then/oneOf/0.month` | 2 | 100.0% |
| `season` | 1 | 0.3% |

### `person` -- 286 instances in `data/`

| property | data | data % |
|---|---|---|
| `given` | 286 | 100.0% |
| `surname` | 286 | 100.0% |
| `birth` | 86 | 30.1% |
| `death` | 85 | 29.7% |
| `suffix` | 0 | 0.0% |

### `phylogeny` -- 36 instances in `data/`

| property | data | data % |
|---|---|---|
| `tree` | 36 | 100.0% |
| `treeType` | 36 | 100.0% |
| `methodology` | 18 | 50.0% |
| `notes` | 6 | 16.7% |
| `characteristics` | 1 | 2.8% |

### `publication` -- 149 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 149 | 100.0% |
| `editors` | 9 | 6.0% |
| `place` | 8 | 5.4% |
| `publisher` | 8 | 5.4% |
| `notes` | 2 | 1.3% |
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

### `relationalFields` -- 5679 instances in `data/`

| property | data | data % |
|---|---|---|
| `synonyms` | 357 | 6.3% |
| `moved` | 31 | 0.5% |
| `corrected` | 5 | 0.1% |
| `non` | 5 | 0.1% |
| `or` | 3 | 0.1% |
| `type` | 3 | 0.1% |
| `lapsus` | 2 | 0.0% |
| `removed` | 2 | 0.0% |
| `substituted` | 2 | 0.0% |
| `lapsusFor` | 1 | 0.0% |

### `repositories` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `/additionalProperties.name` | 58 | 100.0% |
| `/additionalProperties.type` | 58 | 100.0% |
| `/additionalProperties.prefixes` | 51 | 87.9% |
| `/additionalProperties.place` | 35 | 60.3% |
| `/additionalProperties.within` | 16 | 27.6% |
| `/additionalProperties.subject` | 14 | 24.1% |
| `/additionalProperties.notes` | 8 | 13.8% |
| `/additionalProperties.otherNames` | 3 | 5.2% |

### `roles` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `/additionalProperties.meaning` | 12 | 100.0% |
| `/additionalProperties.regulated` | 12 | 100.0% |
| `/additionalProperties.article` | 6 | 50.0% |
| `/additionalProperties.notes` | 6 | 50.0% |
| `/additionalProperties.equivalent` | 2 | 16.7% |

### `sectionFields` -- 5679 instances in `data/`

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

### `taxonRecord` -- 2838 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 2802 | 98.7% |
| `authority` | 1702 | 60.0% |
| `rank` | 972 | 34.2% |
| `pages` | 256 | 9.0% |
| `notes` | 229 | 8.1% |
| `altSpellingOf` | 145 | 5.1% |
| `lang` | 75 | 2.6% |
| `originalParent` | 70 | 2.5% |
| `altRankOf` | 57 | 2.0% |
| `vulgarSpellingOf` | 47 | 1.7% |
| `homonym` | 16 | 0.6% |
| `bracket` | 13 | 0.5% |
| `needsQualification` | 12 | 0.4% |
| `designation` | 4 | 0.1% |
| `status` | 4 | 0.1% |
| `holotype` | 1 | 0.0% |

### `timeFields` -- 167 instances in `data/`

| property | data | data % |
|---|---|---|
| `period` | 110 | 65.9% |
| `series` | 48 | 28.7% |
| `stage` | 16 | 9.6% |
| `seriesModifier` | 8 | 4.8% |
| `seriesRange` | 8 | 4.8% |
| `stageModifier` | 4 | 2.4% |
| `eon` | 0 | 0.0% |
| `era` | 0 | 0.0% |
| `seriesBoundary` | 0 | 0.0% |
| `stageBoundary` | 0 | 0.0% |
| `stageRange` | 0 | 0.0% |

### `translatedNode` -- 16 instances in `data/`

| property | data | data % |
|---|---|---|
| `by` | 1 | 6.2% |

### `tree` -- 6473 instances in `data/`

| property | data | data % |
|---|---|---|
| `children` | 2198 | 34.0% |
| `pages` | 853 | 13.2% |
| `parents` | 325 | 5.0% |
| `rank` | 167 | 2.6% |
| `authority` | 123 | 1.9% |
| `bracketEnd` | 28 | 0.4% |
| `bracketStart` | 28 | 0.4% |
| `altPlacements` | 7 | 0.1% |
| `/if.authority` | 4 | 100.0% |
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

### `typeNode` -- 3 instances in `data/`

| property | data | data % |
|---|---|---|
| `fixation` | 2 | 66.7% |
| `fixedBy` | 0 | 0.0% |

### `uncertaintyFields` -- 6473 instances in `data/`

| property | data | data % |
|---|---|---|
| `provisional` | 126 | 1.9% |
| `tentative` | 17 | 0.3% |
| `quotedParent` | 14 | 0.2% |
| `questionable` | 13 | 0.2% |
| `nonMonophyletic` | 1 | 0.0% |
| `quoted` | 1 | 0.0% |
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

3 of 4 members used, 174 occurrences.

| value | count |
|---|---|
| `'cast'` | 131 |
| `'drawing'` | 40 |
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

24 of 32 members used, 1136 occurrences.

| value | count |
|---|---|
| `'species'` | 236 |
| `'Order'` | 215 |
| `'Family'` | 178 |
| `'genus'` | 132 |
| `'Class'` | 125 |
| `'variety'` | 59 |
| `'Phylum'` | 28 |
| `'Subfamily'` | 26 |
| `'Superfamily'` | 18 |
| `'subgenus'` | 17 |
| `'Suborder'` | 15 |
| `'Subclass'` | 15 |
| `'section'` | 14 |
| `'Subphylum'` | 12 |
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

3 of 4 members used, 58 occurrences.

| value | count |
|---|---|
| `'institution'` | 38 |
| `'collection'` | 16 |
| `'person'` | 4 |

**Never used (1):** `'unknown'`

### `phylogeny#/$defs/role`

12 of 12 members used, 232 occurrences.

| value | count |
|---|---|
| `'paratype'` | 95 |
| `'holotype'` | 80 |
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

8 of 38 members used, 64 occurrences.

| value | count |
|---|---|
| `'Middle Ordovician'` | 35 |
| `'Lower Ordovician'` | 15 |
| `'Lower Devonian'` | 6 |
| `'Middle Devonian'` | 4 |
| `'Upper Devonian'` | 1 |
| `'Llandovery'` | 1 |
| `'Upper Ordovician'` | 1 |
| `'Cambrian Series 2'` | 1 |

**Never used (30):** `'Terrenuevian'`, `'Miaolingian'`, `'Furongian'`, `'Wenlock'`, `'Ludlow'`, `'Přídolí'`, `'Lower Mississippian'`, `'Middle Mississippian'`, `'Upper Mississippian'`, `'Lower Pennsylvanian'`, `'Middle Pennsylvanian'`, `'Upper Pennsylvanian'`, `'Cisuralian'`, `'Guadalupian'`, `'Lopingian'`, `'Lower Triassic'`, `'Middle Triassic'`, `'Upper Triassic'`, `'Lower Jurassic'`, `'Middle Jurassic'`, `'Upper Jurassic'`, `'Lower Cretaceous'`, `'Upper Cretaceous'`, `'Paleocene'`, `'Eocene'`, `'Oligocene'`, `'Miocene'`, `'Pliocene'`, `'Pleistocene'`, `'Holocene'`

### `phylogeny#/$defs/stage`

9 of 100 members used, 16 occurrences.

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
| `'Cambrian Stage 3'` | 1 |

**Never used (91):** `'Fortunian'`, `'Cambrian Stage 2'`, `'Cambrian Stage 4'`, `'Wuliuan'`, `'Drumian'`, `'Guzhangian'`, `'Paibian'`, `'Cambrian Stage 10'`, `'Dapingian'`, `'Darriwilian'`, `'Sandbian'`, `'Hirnantian'`, `'Rhuddanian'`, `'Aeronian'`, `'Sheinwoodian'`, `'Homerian'`, `'Gorstian'`, `'Ludfordian'`, `'Lochkovian'`, `'Pragian'`, `'Frasnian'`, `'Famennian'`, `'Touraisian'`, `'Viséan'`, `'Serpukhovian'`, `'Baskirian'`, `'Moscovian'`, `'Kasimovian'`, `'Gzhelian'`, `'Asselian'`, `'Sakmarian'`, `'Artinskian'`, `'Kungurian'`, `'Roadian'`, `'Wordian'`, `'Capitanian'`, `'Wuchiapingian'`, `'Changhsingian'`, `'Induan'`, `'Olenekian'`, `'Anisian'`, `'Ladinian'`, `'Carnian'`, `'Norian'`, `'Rhaetian'`, `'Hettangian'`, `'Sinemurian'`, `'Toarcian'`, `'Aalenian'`, `'Bajocian'`, `'Bathonian'`, `'Callovian'`, `'Oxfordian'`, `'Kimmeridgian'`, `'Tithonian'`, `'Berriasian'`, `'Valanginian'`, `'Hauterivian'`, `'Barremian'`, `'Aptian'`, `'Albian'`, `'Cenomanian'`, `'Turonian'`, `'Coniacian'`, `'Santonian'`, `'Campanian'`, `'Maastrichtian'`, `'Danian'`, `'Selanian'`, `'Thanetian'`, `'Ypresian'`, `'Lutetian'`, `'Bartonian'`, `'Priabonian'`, `'Rupelian'`, `'Chattian'`, `'Aquitanian'`, `'Burdigalian'`, `'Langhian'`, `'Serravallian'`, `'Tortonian'`, `'Messinian'`, `'Zanclean'`, `'Piacenzian'`, `'Gelasian'`, `'Calabrian'`, `'Chibanian'`, `'Upper Pleistocene'`, `'Greenlandian'`, `'Northgrippian'`, `'Meghalayan'`

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

1 of 8 members used, 2 occurrences.

| value | count |
|---|---|
| `'originalDesignation'` | 2 |

**Never used (7):** `'monotypy'`, `'subsequentDesignation'`, `'subsequentMonotypy'`, `'objectiveSynonymy'`, `'tautonymy'`, `'typus'`, `'iczn'`

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
| `phylogeny#/$defs/article/properties/number` | integer/string | intx156, strx11 | `Supplement`, `1/2`, `Adv. Pr.`, `1–2` | - |
| `phylogeny#/$defs/article/properties/pages/items` | integer/string | intx436, strx46 | `S637`, `S634`, `S631`, `S627` | - |
| `phylogeny#/$defs/article/properties/plates/items` | integer/string | intx29, strx12 | `II`, `I`, `VI`, `V` | - |
| `phylogeny#/$defs/article/properties/series` | integer/string | intx10, strx1 | `A` | - |
| `phylogeny#/$defs/article/properties/volume` | integer/string | intx251, strx14 | `New Series`, `3: Echinoderms: Notes fo...`, `Report of the 68th Meeti...`, `II` | - |
| `phylogeny#/$defs/citationNumber` | integer/string | intx2256, strx225 | `IV`, `II`, `IX`, `VIII` | - |
| `phylogeny#/$defs/cladisticFields/properties/matrix/items` | integer/string | intx139, strx5 | `?` | - |
| `phylogeny#/$defs/contexts` | object/null | dictx58, nullx41 | - | - |
| `phylogeny#/$defs/editorialObject/properties/inferred` | boolean/array | listx7, boolx5 | - | - |
| `phylogeny#/$defs/illustration/properties/of/oneOf/0` | string/integer | intx165, strx43 | `B`, `A`, `25962B`, `602-RO-5` | - |
| `phylogeny#/$defs/illustration/properties/of/oneOf/1/items` | string/integer | strx54, intx48 | `165406A`, `165406B`, `165405B`, `165405A` | - |
| `phylogeny#/$defs/locationFields/properties/illustrations` | array/null | listx180, nullx12 | - | - |
| `phylogeny#/$defs/materialEntry/properties/castOf` | string/integer | intx3 | - | string |
| `phylogeny#/$defs/materialsFields/properties/material` | array/null | listx110, nullx9 | - | - |
| `phylogeny#/$defs/materialsFields/properties/ranges` | array/null | listx49, nullx41 | - | - |
| `phylogeny#/$defs/person/properties/death` | integer/null | intx84, nullx1 | - | - |
| `phylogeny#/$defs/phylogeny/properties/characteristics/items/additionalProperties/additionalProperties` | integer/string | intx40 | - | string |
| `phylogeny#/$defs/printedNumber` | string/integer | intx437, strx248 | `S-3965`, `SH-2`, `SH-1`, `SC-4A` | - |
| `phylogeny#/$defs/relationalFields/properties/synonyms` | array/null | listx357 | - | null |
| `phylogeny#/$defs/sectionRecord/properties/name` | string/null | strx9, nullx3 | `Stellatae`, `Radiatae`, `Multivalvia`, `Lunatae` | - |
| `phylogeny#/$defs/taxonRecord/properties/holotype/additionalProperties/items` | array/string/integer | strx1 | `E23470` | array, integer |
| `phylogeny#/$defs/taxonRecord/properties/name` | string/null | strx2582, nullx220 | `Zoophytes`, `Zoophyta`, `Zoophites`, `Zoanthida` | - |
| `tree#/properties/children` | array/null | listx2198 | - | null |

