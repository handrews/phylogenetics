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
| `actAndModifierFields` | `phylogeny#/$defs/actAndModifierFields/properties/recombined/oneOf/1`<br>`phylogeny#/$defs/actAndModifierFields/properties/restrictedBy`<br>`phylogeny#/$defs/actAndModifierFields/properties/restrictedBy/items` |
| `article` | `phylogeny#/$defs/article/oneOf/2`<br>`phylogeny#/$defs/article/properties/reading` |
| `authority` | `phylogeny#/$defs/authority/properties/auctt/oneOf/1` |
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
| `range` | `phylogeny#/$defs/range/properties/inferred` |
| `relationalFields` | `phylogeny#/$defs/relationalFields/properties/type/oneOf/1` |
| `stageRange` | `phylogeny#/$defs/stageRange`<br>`phylogeny#/$defs/stageRange/items` |
| `taxonRecord` | `phylogeny#/$defs/taxonRecord/properties/holotype/additionalProperties/items/items` |
| `timeFields` | `phylogeny#/$defs/timeFields/properties/eon`<br>`phylogeny#/$defs/timeFields/properties/era`<br>`phylogeny#/$defs/timeFields/properties/seriesBoundary`<br>`phylogeny#/$defs/timeFields/properties/stageBoundary`<br>`phylogeny#/$defs/timeFields/properties/stageRange` |
| `tree` | `tree#/then/not`<br>`tree#/then/not/anyOf/0`<br>`tree#/then/not/anyOf/1`<br>`tree#/then/not/anyOf/2` |
| `typeNode` | `phylogeny#/$defs/typeNode/properties/fixedBy` |
| `uncertaintyFields` | `phylogeny#/$defs/uncertaintyFields/properties/nonMonophyletic/oneOf/1` |

## 2. Property frequency by `$defs`

`data %` is the share of that container's instances carrying the
property.

### `actAndModifierFields` -- 5784 instances in `data/`

| property | data | data % |
|---|---|---|
| `new` | 1603 | 27.7% |
| `isType` | 364 | 6.3% |
| `emended` | 55 | 1.0% |
| `pars` | 21 | 0.4% |
| `translated` | 18 | 0.3% |
| `emendedBy` | 9 | 0.2% |
| `nudum` | 7 | 0.1% |
| `recombined` | 3 | 0.1% |
| `restricted` | 1 | 0.0% |
| `stem` | 1 | 0.0% |
| `restrictedBy` | 0 | 0.0% |

### `article` -- 384 instances in `data/`

| property | data | data % |
|---|---|---|
| `authors` | 384 | 100.0% |
| `pubDate` | 383 | 99.7% |
| `volume` | 298 | 77.6% |
| `title` | 284 | 74.0% |
| `identifiers` | 267 | 69.5% |
| `pages` | 254 | 66.1% |
| `journal` | 242 | 63.0% |
| `number` | 185 | 48.2% |
| `identifiers.url` | 184 | 68.9% |
| `book` | 141 | 36.7% |
| `processDates` | 101 | 26.3% |
| `notes` | 71 | 18.5% |
| `processDates.accepted` | 63 | 62.4% |
| `identifiers.doi` | 62 | 23.2% |
| `processDates.received` | 53 | 52.5% |
| `audit` | 48 | 12.5% |
| `audit.notes` | 48 | 100.0% |
| `audit.state` | 48 | 100.0% |
| `audit.coverage` | 30 | 62.5% |
| `processDates.online` | 28 | 27.7% |
| `plates` | 25 | 6.5% |
| `identifiers.jstor` | 24 | 9.0% |
| `processDates.revised` | 18 | 17.8% |
| `series` | 14 | 3.6% |
| `processDates.read` | 11 | 10.9% |
| `articleNumber` | 7 | 1.8% |
| `seen` | 5 | 1.3% |
| `processDates.transmitted` | 4 | 4.0% |
| `processDates.conferenceEnd` | 3 | 3.0% |
| `processDates.conferenceStart` | 3 | 3.0% |
| `processDates.issued` | 3 | 3.0% |
| `processDates.submitted` | 3 | 3.0% |
| `chapter` | 2 | 0.5% |
| `translationOf` | 2 | 0.5% |
| `translations` | 2 | 0.5% |
| `editors` | 1 | 0.3% |
| `inPrep` | 1 | 0.3% |
| `processDates.printed` | 1 | 1.0% |
| `processDates.published` | 1 | 1.0% |
| `processDates.unknown` | 1 | 1.0% |
| `quotes` | 1 | 0.3% |
| `reading` | 0 | 0.0% |

### `authority` -- 2027 instances in `data/`

| property | data | data % |
|---|---|---|
| `source` | 2025 | 99.9% |
| `pages` | 67 | 3.3% |
| `illustrations` | 40 | 2.0% |
| `attributedTo` | 24 | 1.2% |
| `ex` | 15 | 0.7% |
| `notes` | 4 | 0.2% |
| `auctt` | 2 | 0.1% |

### `authorityFields` -- 9419 instances in `data/`

| property | data | data % |
|---|---|---|
| `auth` | 848 | 9.0% |
| `year` | 846 | 9.0% |
| `in` | 28 | 0.3% |

### `citationFields` -- 9407 instances in `data/`

| property | data | data % |
|---|---|---|
| `citedAs` | 1020 | 10.8% |

### `cladisticFields` -- 793 instances in `data/`

| property | data | data % |
|---|---|---|
| `outgroup` | 19 | 2.4% |
| `matrix` | 8 | 1.0% |
| `bootstrap` | 6 | 0.8% |
| `data` | 0 | 0.0% |

### `context` -- 116 instances in `data/`

| property | data | data % |
|---|---|---|
| `location` | 115 | 99.1% |
| `unit` | 107 | 92.2% |
| `biozone` | 48 | 41.4% |
| `localityNumbers` | 46 | 39.7% |
| `mapSheet` | 30 | 25.9% |
| `notes` | 20 | 17.2% |
| `coordinatesAsPrinted` | 12 | 10.3% |
| `biozoneRange` | 7 | 6.0% |
| `biota` | 3 | 2.6% |
| `tentative` | 3 | 2.6% |
| `collectedBy` | 2 | 1.7% |
| `fauna` | 1 | 0.9% |
| `inferred` | 1 | 0.9% |
| `biozones` | 0 | 0.0% |
| `collectedDate` | 0 | 0.0% |
| `paleocontinent` | 0 | 0.0% |
| `sources` | 0 | 0.0% |

### `editorialObject` -- 53 instances in `data/`

| property | data | data % |
|---|---|---|
| `basis` | 53 | 100.0% |
| `inferred` | 39 | 73.6% |
| `corrections` | 14 | 26.4% |
| `corrections.authority` | 9 | 64.3% |
| `corrections.authority.source` | 9 | 100.0% |

### `figureLocatorFields` -- 512 instances in `data/`

| property | data | data % |
|---|---|---|
| `figures` | 443 | 86.5% |
| `plate` | 365 | 71.3% |
| `page` | 134 | 26.2% |
| `textFigures` | 68 | 13.3% |
| `notes` | 25 | 4.9% |
| `non` | 0 | 0.0% |

### `identificationFields` -- 6577 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxon` | 5968 | 90.7% |
| `openTaxon` | 248 | 3.8% |
| `cf` | 15 | 0.2% |
| `aff` | 14 | 0.2% |
| `mineralTaxon` | 1 | 0.0% |
| `designation` | 0 | 0.0% |

### `illustration` -- 512 instances in `data/`

| property | data | data % |
|---|---|---|
| `of` | 254 | 49.6% |
| `depicts` | 177 | 34.6% |
| `uncertain` | 2 | 0.4% |

### `inferredContext` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `paleocontinent` | 1 | 100.0% |
| `basis` | 0 | 0.0% |
| `sources` | 0 | 0.0% |

### `localTimeFields` -- 193 instances in `data/`

| property | data | data % |
|---|---|---|
| `localSeries` | 65 | 33.7% |
| `localSeriesModifier` | 26 | 13.5% |
| `localSeriesRange` | 9 | 4.7% |
| `localStage` | 9 | 4.7% |
| `localStageRange` | 6 | 3.1% |
| `localPeriod` | 3 | 1.6% |
| `localSeriesBoundary` | 1 | 0.5% |
| `localStageModifier` | 1 | 0.5% |
| `localStageBoundary` | 0 | 0.0% |

### `localityNumber` -- 59 instances in `data/`

| property | data | data % |
|---|---|---|
| `number` | 59 | 100.0% |
| `prefix` | 28 | 47.5% |
| `register` | 0 | 0.0% |

### `locationFields` -- 9407 instances in `data/`

| property | data | data % |
|---|---|---|
| `illustrations` | 201 | 2.1% |

### `materialEntry` -- 299 instances in `data/`

| property | data | data % |
|---|---|---|
| `numbers` | 278 | 93.0% |
| `prefix` | 275 | 92.0% |
| `role` | 218 | 72.9% |
| `context` | 150 | 50.2% |
| `asPrinted` | 78 | 26.1% |
| `notes` | 67 | 22.4% |
| `label` | 18 | 6.0% |
| `preparation` | 17 | 5.7% |
| `repository` | 12 | 4.0% |
| `count` | 11 | 3.7% |
| `collectedBy` | 10 | 3.3% |
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

### `materialsFields` -- 5784 instances in `data/`

| property | data | data % |
|---|---|---|
| `material` | 125 | 2.2% |
| `ranges` | 113 | 2.0% |
| `contexts` | 98 | 1.7% |

### `metaFields` -- 6577 instances in `data/`

| property | data | data % |
|---|---|---|
| `notes` | 514 | 7.8% |
| `editorial` | 51 | 0.8% |

### `modularDate` -- 383 instances in `data/`

| property | data | data % |
|---|---|---|
| `year` | 383 | 100.0% |
| `month` | 88 | 23.0% |
| `day` | 33 | 8.6% |
| `/then/oneOf/2.day` | 18 | 100.0% |
| `/then/oneOf/2.month` | 18 | 100.0% |
| `/then/oneOf/1.day` | 13 | 100.0% |
| `/then/oneOf/1.month` | 13 | 100.0% |
| `months` | 6 | 1.6% |
| `/then/oneOf/0.day` | 2 | 100.0% |
| `/then/oneOf/0.month` | 2 | 100.0% |
| `season` | 1 | 0.3% |

### `person` -- 307 instances in `data/`

| property | data | data % |
|---|---|---|
| `given` | 307 | 100.0% |
| `surname` | 307 | 100.0% |
| `birth` | 107 | 34.9% |
| `death` | 105 | 34.2% |
| `suffix` | 0 | 0.0% |

### `phylogeny` -- 36 instances in `data/`

| property | data | data % |
|---|---|---|
| `tree` | 36 | 100.0% |
| `treeType` | 36 | 100.0% |
| `methodology` | 18 | 50.0% |
| `notes` | 7 | 19.4% |
| `characteristics` | 1 | 2.8% |

### `publication` -- 174 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 174 | 100.0% |
| `editors` | 10 | 5.7% |
| `place` | 8 | 4.6% |
| `publisher` | 8 | 4.6% |
| `notes` | 5 | 2.9% |
| `type` | 0 | 0.0% |

### `range` -- 77 instances in `data/`

| property | data | data % |
|---|---|---|
| `regions` | 37 | 48.1% |
| `asPrinted` | 35 | 45.5% |
| `notes` | 10 | 13.0% |
| `tentative` | 7 | 9.1% |
| `regions/items/oneOf/1.tentative` | 2 | 100.0% |
| `regions/items/oneOf/1.value` | 2 | 100.0% |
| `inferred` | 0 | 0.0% |

### `relationalFields` -- 5784 instances in `data/`

| property | data | data % |
|---|---|---|
| `synonyms` | 365 | 6.3% |
| `moved` | 49 | 0.8% |
| `type` | 6 | 0.1% |
| `corrected` | 5 | 0.1% |
| `non` | 5 | 0.1% |
| `lapsus` | 4 | 0.1% |
| `or` | 3 | 0.1% |
| `removed` | 2 | 0.0% |
| `substituted` | 2 | 0.0% |
| `lapsusFor` | 1 | 0.0% |

### `repositories` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `/additionalProperties.name` | 60 | 100.0% |
| `/additionalProperties.type` | 60 | 100.0% |
| `/additionalProperties.prefixes` | 53 | 88.3% |
| `/additionalProperties.place` | 35 | 58.3% |
| `/additionalProperties.within` | 17 | 28.3% |
| `/additionalProperties.subject` | 15 | 25.0% |
| `/additionalProperties.notes` | 9 | 15.0% |
| `/additionalProperties.otherNames` | 3 | 5.0% |

### `roles` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `/additionalProperties.meaning` | 12 | 100.0% |
| `/additionalProperties.regulated` | 12 | 100.0% |
| `/additionalProperties.article` | 6 | 50.0% |
| `/additionalProperties.notes` | 6 | 50.0% |
| `/additionalProperties.equivalent` | 2 | 16.7% |

### `sectionFields` -- 5784 instances in `data/`

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

### `sourceAlias` -- 4 instances in `data/`

| property | data | data % |
|---|---|---|
| `aliasOf` | 4 | 100.0% |

### `taxonRecord` -- 2830 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 2800 | 98.9% |
| `authority` | 1803 | 63.7% |
| `rank` | 962 | 34.0% |
| `pages` | 260 | 9.2% |
| `notes` | 239 | 8.4% |
| `altSpellingOf` | 149 | 5.3% |
| `lang` | 73 | 2.6% |
| `originalParent` | 70 | 2.5% |
| `altRankOf` | 51 | 1.8% |
| `vulgarSpellingOf` | 45 | 1.6% |
| `homonym` | 16 | 0.6% |
| `needsQualification` | 13 | 0.5% |
| `bracket` | 9 | 0.3% |
| `designation` | 4 | 0.1% |
| `holotype` | 1 | 0.0% |
| `mineral` | 1 | 0.0% |
| `status` | 1 | 0.0% |

### `timeFields` -- 194 instances in `data/`

| property | data | data % |
|---|---|---|
| `period` | 110 | 56.7% |
| `series` | 54 | 27.8% |
| `seriesRange` | 24 | 12.4% |
| `stage` | 19 | 9.8% |
| `seriesModifier` | 8 | 4.1% |
| `stageModifier` | 4 | 2.1% |
| `eon` | 0 | 0.0% |
| `era` | 0 | 0.0% |
| `seriesBoundary` | 0 | 0.0% |
| `stageBoundary` | 0 | 0.0% |
| `stageRange` | 0 | 0.0% |

### `translatedNode` -- 15 instances in `data/`

| property | data | data % |
|---|---|---|
| `by` | 1 | 6.7% |

### `tree` -- 6577 instances in `data/`

| property | data | data % |
|---|---|---|
| `children` | 2220 | 33.8% |
| `pages` | 1216 | 18.5% |
| `rank` | 601 | 9.1% |
| `parents` | 329 | 5.0% |
| `authority` | 262 | 4.0% |
| `/if.authority` | 76 | 100.0% |
| `bracketEnd` | 28 | 0.4% |
| `bracketStart` | 28 | 0.4% |
| `mergeInto` | 14 | 0.2% |
| `altPlacements` | 6 | 0.1% |

### `treeDocument` -- 223 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxonomies` | 219 | 98.2% |
| `prefixes` | 31 | 13.9% |
| `phylogenies` | 25 | 11.2% |
| `notes` | 19 | 8.5% |
| `unused` | 5 | 2.2% |
| `contexts` | 2 | 0.9% |
| `assumptions` | 1 | 0.4% |
| `localityRegister` | 1 | 0.4% |

### `typeNode` -- 6 instances in `data/`

| property | data | data % |
|---|---|---|
| `fixation` | 2 | 33.3% |
| `fixedBy` | 0 | 0.0% |

### `uncertaintyFields` -- 6577 instances in `data/`

| property | data | data % |
|---|---|---|
| `provisional` | 129 | 2.0% |
| `tentative` | 17 | 0.3% |
| `questionable` | 14 | 0.2% |
| `quotedParent` | 14 | 0.2% |
| `sensu` | 8 | 0.1% |
| `mutable` | 3 | 0.0% |
| `nonMonophyletic` | 1 | 0.0% |
| `quoted` | 1 | 0.0% |

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

3 of 4 members used, 177 occurrences.

| value | count |
|---|---|
| `'cast'` | 132 |
| `'drawing'` | 41 |
| `'reconstruction'` | 4 |

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

3 of 4 members used, 36 occurrences.

| value | count |
|---|---|
| `'cladogram'` | 27 |
| `'diagram'` | 8 |
| `'other'` | 1 |

**Never used (1):** `'taxonomy'`

### `phylogeny#/$defs/publication/properties/type`

0 of 2 members used, 0 occurrences.

**Never used (2):** `'journal'`, `'book'`

### `phylogeny#/$defs/rank`

24 of 32 members used, 1508 occurrences.

| value | count |
|---|---|
| `'Class'` | 283 |
| `'Order'` | 267 |
| `'species'` | 238 |
| `'Family'` | 222 |
| `'genus'` | 132 |
| `'Phylum'` | 59 |
| `'variety'` | 59 |
| `'Subphylum'` | 52 |
| `'Superfamily'` | 33 |
| `'Subfamily'` | 26 |
| `'Subclass'` | 24 |
| `'Suborder'` | 23 |
| `'subgenus'` | 17 |
| `'Grade'` | 16 |
| `'section'` | 14 |
| `'Group'` | 12 |
| `'Division'` | 9 |
| `'Kingdom'` | 6 |
| `'Superorder'` | 4 |
| `'Subkingdom'` | 3 |
| `'Unranked'` | 3 |
| `'Plesion'` | 3 |
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

3 of 4 members used, 60 occurrences.

| value | count |
|---|---|
| `'institution'` | 39 |
| `'collection'` | 17 |
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

18 of 47 members used, 102 occurrences.

| value | count |
|---|---|
| `'Middle Ordovician'` | 41 |
| `'Lower Ordovician'` | 21 |
| `'Lower Devonian'` | 8 |
| `'Middle Devonian'` | 6 |
| `'Middle Cambrian'` | 5 |
| `'Holocene'` | 5 |
| `'Lower Cambrian'` | 3 |
| `'Upper Devonian'` | 2 |
| `'Upper Ordovician'` | 2 |
| `'Upper Cambrian'` | 1 |
| `'Lower Mississippian'` | 1 |
| `'Middle Permian'` | 1 |
| `'Upper Permian'` | 1 |
| `'Middle Silurian'` | 1 |
| `'Upper Silurian'` | 1 |
| `'Lower Silurian'` | 1 |
| `'Llandovery'` | 1 |
| `'Cambrian Series 2'` | 1 |

**Never used (29):** `'Terrenuevian'`, `'Miaolingian'`, `'Furongian'`, `'Wenlock'`, `'Ludlow'`, `'Přídolí'`, `'Middle Mississippian'`, `'Upper Mississippian'`, `'Lower Pennsylvanian'`, `'Middle Pennsylvanian'`, `'Upper Pennsylvanian'`, `'Lower Permian'`, `'Cisuralian'`, `'Guadalupian'`, `'Lopingian'`, `'Lower Triassic'`, `'Middle Triassic'`, `'Upper Triassic'`, `'Lower Jurassic'`, `'Middle Jurassic'`, `'Upper Jurassic'`, `'Lower Cretaceous'`, `'Upper Cretaceous'`, `'Paleocene'`, `'Eocene'`, `'Oligocene'`, `'Miocene'`, `'Pliocene'`, `'Pleistocene'`

### `phylogeny#/$defs/stage`

10 of 100 members used, 19 occurrences.

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
| `'Cambrian Stage 3'` | 1 |

**Never used (90):** `'Fortunian'`, `'Cambrian Stage 2'`, `'Cambrian Stage 4'`, `'Drumian'`, `'Guzhangian'`, `'Paibian'`, `'Cambrian Stage 10'`, `'Dapingian'`, `'Darriwilian'`, `'Sandbian'`, `'Hirnantian'`, `'Rhuddanian'`, `'Aeronian'`, `'Sheinwoodian'`, `'Homerian'`, `'Gorstian'`, `'Ludfordian'`, `'Lochkovian'`, `'Pragian'`, `'Frasnian'`, `'Famennian'`, `'Touraisian'`, `'Viséan'`, `'Serpukhovian'`, `'Baskirian'`, `'Moscovian'`, `'Kasimovian'`, `'Gzhelian'`, `'Asselian'`, `'Sakmarian'`, `'Artinskian'`, `'Kungurian'`, `'Roadian'`, `'Wordian'`, `'Capitanian'`, `'Wuchiapingian'`, `'Changhsingian'`, `'Induan'`, `'Olenekian'`, `'Anisian'`, `'Ladinian'`, `'Carnian'`, `'Norian'`, `'Rhaetian'`, `'Hettangian'`, `'Sinemurian'`, `'Toarcian'`, `'Aalenian'`, `'Bajocian'`, `'Bathonian'`, `'Callovian'`, `'Oxfordian'`, `'Kimmeridgian'`, `'Tithonian'`, `'Berriasian'`, `'Valanginian'`, `'Hauterivian'`, `'Barremian'`, `'Aptian'`, `'Albian'`, `'Cenomanian'`, `'Turonian'`, `'Coniacian'`, `'Santonian'`, `'Campanian'`, `'Maastrichtian'`, `'Danian'`, `'Selanian'`, `'Thanetian'`, `'Ypresian'`, `'Lutetian'`, `'Bartonian'`, `'Priabonian'`, `'Rupelian'`, `'Chattian'`, `'Aquitanian'`, `'Burdigalian'`, `'Langhian'`, `'Serravallian'`, `'Tortonian'`, `'Messinian'`, `'Zanclean'`, `'Piacenzian'`, `'Gelasian'`, `'Calabrian'`, `'Chibanian'`, `'Upper Pleistocene'`, `'Greenlandian'`, `'Northgrippian'`, `'Meghalayan'`

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

3 of 4 members used, 8 occurrences.

| value | count |
|---|---|
| `'lato'` | 4 |
| `'stricto'` | 3 |
| `'extenso'` | 1 |

**Never used (1):** `'emendato'`

## 4. Observed value types where the schema allows a union

Tests whether each multi-type declaration is actually needed.

| location | declared | observed | string examples | declared but unseen |
|---|---|---|---|---|
| `phylogeny#/$defs/article/properties/articleNumber` | integer/string | intx5, strx2 | `e1465`, `e38296` | - |
| `phylogeny#/$defs/article/properties/chapter` | integer/string | strx2 | `III. Stamm. Echinodermat...`, `Report of E. Billings, E...` | integer |
| `phylogeny#/$defs/article/properties/number` | integer/string | intx172, strx13 | `Supplement`, `1/2`, `Part 4, No. 220`, `Adv. Pr.` | - |
| `phylogeny#/$defs/article/properties/pages/items` | integer/string | intx474, strx46 | `S637`, `S634`, `S631`, `S627` | - |
| `phylogeny#/$defs/article/properties/plates/items` | integer/string | intx31, strx17 | `II`, `I`, `XXXVII`, `VI` | - |
| `phylogeny#/$defs/article/properties/series` | integer/string | intx10, strx4 | `A`, `New Series` | - |
| `phylogeny#/$defs/article/properties/volume` | integer/string | intx272, strx26 | `New Series`, `3: Echinoderms: Notes fo...`, `Report of the 68th Meeti...`, `Eighty-Three Plates to A...` | - |
| `phylogeny#/$defs/citationNumber` | integer/string | intx2643, strx267 | `IV`, `II`, `IX`, `VIII` | - |
| `phylogeny#/$defs/cladisticFields/properties/matrix/items` | integer/string | intx139, strx5 | `?` | - |
| `phylogeny#/$defs/contexts` | object/null | dictx59, nullx41 | - | - |
| `phylogeny#/$defs/editorialObject/properties/inferred` | boolean/array | listx25, boolx14 | - | - |
| `phylogeny#/$defs/locationFields/properties/illustrations` | array/null | listx189, nullx12 | - | - |
| `phylogeny#/$defs/materialsFields/properties/material` | array/null | listx116, nullx9 | - | - |
| `phylogeny#/$defs/materialsFields/properties/ranges` | array/null | listx72, nullx41 | - | - |
| `phylogeny#/$defs/person/properties/death` | integer/null | intx104, nullx1 | - | - |
| `phylogeny#/$defs/phylogeny/properties/characteristics/items/additionalProperties/additionalProperties` | integer/string | intx40 | - | string |
| `phylogeny#/$defs/printedNumber` | string/integer | intx668, strx352 | `B`, `A`, `S-3965`, `SH-2` | - |
| `phylogeny#/$defs/relationalFields/properties/synonyms` | array/null | listx365 | - | null |
| `phylogeny#/$defs/sectionRecord/properties/name` | string/null | strx9, nullx3 | `Stellatae`, `Radiatae`, `Multivalvia`, `Lunatae` | - |
| `phylogeny#/$defs/taxonRecord/properties/holotype/additionalProperties/items` | array/string/integer | strx1 | `E23470` | array, integer |
| `phylogeny#/$defs/taxonRecord/properties/name` | string/null | strx2575, nullx225 | `Zoophytes`, `Zoophyta`, `Zoophites`, `Zoanthida` | - |
| `tree#/properties/children` | array/null | listx2217, nullx3 | - | - |

