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
| `authority` | `phylogeny#/$defs/authority/oneOf/3/not`<br>`phylogeny#/$defs/authority/oneOf/3/not/anyOf/0`<br>`phylogeny#/$defs/authority/oneOf/3/not/anyOf/1`<br>`phylogeny#/$defs/authority/oneOf/3/not/anyOf/2`<br>`phylogeny#/$defs/authority/oneOf/3/not/anyOf/3`<br>`phylogeny#/$defs/authority/properties/auctt/oneOf/1` |
| `catalogNumber` | `phylogeny#/$defs/catalogNumber`<br>`phylogeny#/$defs/catalogNumber/oneOf/0`<br>`phylogeny#/$defs/catalogNumber/oneOf/1`<br>`phylogeny#/$defs/catalogNumber/oneOf/1/items` |
| `citedAct` | `phylogeny#/$defs/citedAct`<br>`phylogeny#/$defs/citedAct/properties/by` |
| `citedWork` | `phylogeny#/$defs/citedWork/anyOf/1` |
| `cladisticFields` | `phylogeny#/$defs/cladisticFields/properties/data`<br>`phylogeny#/$defs/cladisticFields/properties/data/additionalProperties` |
| `context` | `phylogeny#/$defs/context/properties/biozones`<br>`phylogeny#/$defs/context/properties/biozones/items`<br>`phylogeny#/$defs/context/properties/collectedDate`<br>`phylogeny#/$defs/context/properties/paleocontinent`<br>`phylogeny#/$defs/context/properties/sources`<br>`phylogeny#/$defs/context/properties/sources/items`<br>`phylogeny#/$defs/context/properties/tentative/oneOf/0` |
| `contextRef` | `phylogeny#/$defs/contextRef/oneOf/1`<br>`phylogeny#/$defs/contextRef/oneOf/1/properties/key`<br>`phylogeny#/$defs/contextRef/oneOf/1/properties/tentative` |
| `editorialObject` | `phylogeny#/$defs/editorialObject/properties/corrections/not`<br>`phylogeny#/$defs/editorialObject/properties/corrections/not/anyOf/0`<br>`phylogeny#/$defs/editorialObject/properties/corrections/not/anyOf/1`<br>`phylogeny#/$defs/editorialObject/properties/corrections/not/anyOf/2`<br>`phylogeny#/$defs/editorialObject/properties/corrections/properties/authority/properties/in`<br>`phylogeny#/$defs/editorialObject/properties/corrections/properties/authority/properties/in/items` |
| `entryRef` | `phylogeny#/$defs/entryRef` |
| `entryRefFields` | `phylogeny#/$defs/entryRefFields`<br>`phylogeny#/$defs/entryRefFields/oneOf/0`<br>`phylogeny#/$defs/entryRefFields/oneOf/1`<br>`phylogeny#/$defs/entryRefFields/properties/label`<br>`phylogeny#/$defs/entryRefFields/properties/number`<br>`phylogeny#/$defs/entryRefFields/properties/prefix` |
| `entryRefOrNumber` | `phylogeny#/$defs/entryRefOrNumber/oneOf/1` |
| `eon` | `phylogeny#/$defs/eon` |
| `era` | `phylogeny#/$defs/era` |
| `figureLocatorFields` | `phylogeny#/$defs/figureLocatorFields/properties/non` |
| `inferredContext` | `phylogeny#/$defs/inferredContext/properties/basis`<br>`phylogeny#/$defs/inferredContext/properties/sources`<br>`phylogeny#/$defs/inferredContext/properties/sources/items` |
| `localTimeFields` | `phylogeny#/$defs/localTimeFields/properties/localStageBoundary` |
| `localityNumber` | `phylogeny#/$defs/localityNumber/not`<br>`phylogeny#/$defs/localityNumber/properties/register` |
| `materialEntry` | `phylogeny#/$defs/materialEntry/properties/formerIds`<br>`phylogeny#/$defs/materialEntry/properties/formerIds/items`<br>`phylogeny#/$defs/materialEntry/properties/fragmentOf`<br>`phylogeny#/$defs/materialEntry/properties/roleUncertain`<br>`phylogeny#/$defs/materialEntry/properties/sameAs`<br>`phylogeny#/$defs/materialEntry/properties/sameAs/properties/source` |
| `modularDate` | `phylogeny#/$defs/modularDate/then/oneOf/2/properties/month/anyOf/5` |
| `person` | `phylogeny#/$defs/person/properties/suffix` |
| `publication` | `phylogeny#/$defs/publication/properties/type` |
| `range` | `phylogeny#/$defs/range/properties/inferred` |
| `relationalFields` | `phylogeny#/$defs/relationalFields/properties/type/oneOf/1` |
| `sectionRecord` | `phylogeny#/$defs/sectionRecord/properties/authority/not` |
| `stageRange` | `phylogeny#/$defs/stageRange`<br>`phylogeny#/$defs/stageRange/items` |
| `taxonRecord` | `phylogeny#/$defs/taxonRecord/else/oneOf/3`<br>`phylogeny#/$defs/taxonRecord/else/oneOf/4`<br>`phylogeny#/$defs/taxonRecord/properties/altGenderOf`<br>`phylogeny#/$defs/taxonRecord/properties/authority/not`<br>`phylogeny#/$defs/taxonRecord/properties/holotype/additionalProperties/items/items`<br>`phylogeny#/$defs/taxonRecord/properties/latinSpellingOf` |
| `timeFields` | `phylogeny#/$defs/timeFields/properties/eon`<br>`phylogeny#/$defs/timeFields/properties/era`<br>`phylogeny#/$defs/timeFields/properties/seriesBoundary`<br>`phylogeny#/$defs/timeFields/properties/stageBoundary`<br>`phylogeny#/$defs/timeFields/properties/stageRange` |
| `typeNode` | `phylogeny#/$defs/typeNode/properties/fixedBy` |
| `uncertaintyFields` | `phylogeny#/$defs/uncertaintyFields/properties/nonMonophyletic/oneOf/1` |

## 2. Property frequency by `$defs`

`data %` is the share of that container's instances carrying the
property.

### `actAndModifierFields` -- 5934 instances in `data/`

| property | data | data % |
|---|---|---|
| `new` | 1631 | 27.5% |
| `isType` | 364 | 6.1% |
| `emended` | 56 | 0.9% |
| `pars` | 21 | 0.4% |
| `translated` | 19 | 0.3% |
| `emendedBy` | 9 | 0.2% |
| `nudum` | 7 | 0.1% |
| `recombined` | 3 | 0.1% |
| `restricted` | 1 | 0.0% |
| `stem` | 1 | 0.0% |
| `restrictedBy` | 0 | 0.0% |

### `article` -- 400 instances in `data/`

| property | data | data % |
|---|---|---|
| `authors` | 400 | 100.0% |
| `pubDate` | 399 | 99.8% |
| `volume` | 312 | 78.0% |
| `title` | 284 | 71.0% |
| `identifiers` | 283 | 70.8% |
| `pages` | 254 | 63.5% |
| `journal` | 242 | 60.5% |
| `identifiers.url` | 200 | 70.7% |
| `number` | 199 | 49.8% |
| `book` | 157 | 39.2% |
| `processDates` | 101 | 25.2% |
| `notes` | 71 | 17.8% |
| `processDates.accepted` | 63 | 62.4% |
| `identifiers.doi` | 62 | 21.9% |
| `processDates.received` | 53 | 52.5% |
| `audit` | 48 | 12.0% |
| `audit.notes` | 48 | 100.0% |
| `audit.state` | 48 | 100.0% |
| `audit.coverage` | 30 | 62.5% |
| `processDates.online` | 28 | 27.7% |
| `plates` | 25 | 6.2% |
| `identifiers.jstor` | 24 | 8.5% |
| `processDates.revised` | 18 | 17.8% |
| `series` | 14 | 3.5% |
| `processDates.read` | 11 | 10.9% |
| `articleNumber` | 7 | 1.8% |
| `seen` | 5 | 1.2% |
| `processDates.transmitted` | 4 | 4.0% |
| `processDates.conferenceEnd` | 3 | 3.0% |
| `processDates.conferenceStart` | 3 | 3.0% |
| `processDates.issued` | 3 | 3.0% |
| `processDates.submitted` | 3 | 3.0% |
| `chapter` | 2 | 0.5% |
| `translationOf` | 2 | 0.5% |
| `translations` | 2 | 0.5% |
| `/oneOf/3.inPrep` | 1 | 100.0% |
| `editors` | 1 | 0.2% |
| `inPrep` | 1 | 0.2% |
| `processDates.printed` | 1 | 1.0% |
| `processDates.published` | 1 | 1.0% |
| `processDates.unknown` | 1 | 1.0% |
| `quotes` | 1 | 0.2% |
| `reading` | 0 | 0.0% |

### `authority` -- 2953 instances in `data/`

| property | data | data % |
|---|---|---|
| `source` | 2078 | 70.4% |
| `auth` | 851 | 28.8% |
| `year` | 848 | 28.7% |
| `pages` | 401 | 13.6% |
| `illustrations` | 86 | 2.9% |
| `in` | 27 | 0.9% |
| `attributedTo` | 25 | 0.8% |
| `ex` | 15 | 0.5% |
| `notes` | 4 | 0.1% |
| `auctt` | 2 | 0.1% |

### `citationFields` -- 9601 instances in `data/`

| property | data | data % |
|---|---|---|
| `citedAs` | 1055 | 11.0% |

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

### `editorialObject` -- 81 instances in `data/`

| property | data | data % |
|---|---|---|
| `basis` | 81 | 100.0% |
| `inferred` | 67 | 82.7% |
| `corrections` | 14 | 17.3% |
| `corrections.authority` | 10 | 71.4% |
| `corrections.authority.source` | 9 | 90.0% |
| `corrections.authority.auth` | 8 | 80.0% |
| `corrections.authority.year` | 8 | 80.0% |
| `corrections.authority.in` | 0 | 0.0% |

### `figureLocatorFields` -- 561 instances in `data/`

| property | data | data % |
|---|---|---|
| `figures` | 486 | 86.6% |
| `plate` | 413 | 73.6% |
| `page` | 135 | 24.1% |
| `textFigures` | 69 | 12.3% |
| `notes` | 25 | 4.5% |
| `non` | 0 | 0.0% |

### `identificationFields` -- 6727 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxon` | 6091 | 90.5% |
| `openTaxon` | 268 | 4.0% |
| `cf` | 16 | 0.2% |
| `aff` | 14 | 0.2% |
| `designation` | 2 | 0.0% |
| `mineralTaxon` | 2 | 0.0% |

### `illustration` -- 561 instances in `data/`

| property | data | data % |
|---|---|---|
| `of` | 254 | 45.3% |
| `depicts` | 177 | 31.6% |
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

### `locationFields` -- 6727 instances in `data/`

| property | data | data % |
|---|---|---|
| `illustrations` | 203 | 3.0% |

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

### `materialsFields` -- 5934 instances in `data/`

| property | data | data % |
|---|---|---|
| `material` | 125 | 2.1% |
| `ranges` | 113 | 1.9% |
| `contexts` | 98 | 1.7% |

### `metaFields` -- 6727 instances in `data/`

| property | data | data % |
|---|---|---|
| `notes` | 525 | 7.8% |
| `editorial` | 79 | 1.2% |

### `modularDate` -- 399 instances in `data/`

| property | data | data % |
|---|---|---|
| `year` | 399 | 100.0% |
| `month` | 88 | 22.1% |
| `day` | 33 | 8.3% |
| `/then/oneOf/2.day` | 18 | 100.0% |
| `/then/oneOf/2.month` | 18 | 100.0% |
| `/then/oneOf/1.day` | 13 | 100.0% |
| `/then/oneOf/1.month` | 13 | 100.0% |
| `months` | 6 | 1.5% |
| `/then/oneOf/0.day` | 2 | 100.0% |
| `/then/oneOf/0.month` | 2 | 100.0% |
| `season` | 1 | 0.3% |

### `person` -- 310 instances in `data/`

| property | data | data % |
|---|---|---|
| `given` | 310 | 100.0% |
| `surname` | 310 | 100.0% |
| `birth` | 110 | 35.5% |
| `death` | 108 | 34.8% |
| `suffix` | 0 | 0.0% |

### `phylogeny` -- 36 instances in `data/`

| property | data | data % |
|---|---|---|
| `tree` | 36 | 100.0% |
| `treeType` | 36 | 100.0% |
| `methodology` | 18 | 50.0% |
| `notes` | 7 | 19.4% |
| `characteristics` | 1 | 2.8% |

### `publication` -- 177 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 177 | 100.0% |
| `editors` | 10 | 5.6% |
| `place` | 8 | 4.5% |
| `publisher` | 8 | 4.5% |
| `notes` | 5 | 2.8% |
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

### `ranks` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `ranks/items.name` | 31 | 100.0% |
| `ranks/items.informal` | 8 | 25.8% |
| `exceptions/items.name` | 7 | 100.0% |
| `exceptions/items.note` | 7 | 100.0% |
| `exceptions/items.rank` | 7 | 100.0% |
| `suffixes/items.ranks` | 6 | 100.0% |
| `suffixes/items.suffix` | 6 | 100.0% |
| `ranks/items.group` | 5 | 16.1% |
| `ranks/items.endings/items.suffix` | 4 | 100.0% |
| `ranks/items.endings` | 3 | 9.7% |
| `checkedFrom` | 1 | 100.0% |
| `exceptions` | 1 | 100.0% |
| `ranks` | 1 | 100.0% |
| `ranks/items.endings/items.before` | 1 | 25.0% |
| `suffixes` | 1 | 100.0% |

### `relationalFields` -- 5934 instances in `data/`

| property | data | data % |
|---|---|---|
| `synonyms` | 373 | 6.3% |
| `moved` | 81 | 1.4% |
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

### `sectionFields` -- 5934 instances in `data/`

| property | data | data % |
|---|---|---|
| `sectionEnd` | 25 | 0.4% |
| `sectionStart` | 25 | 0.4% |
| `sectionStart.section` | 25 | 100.0% |
| `sectionStart.new` | 14 | 56.0% |
| `sectionStart.pages` | 14 | 56.0% |
| `sectionStart.citedAs` | 12 | 48.0% |
| `sectionStart.notes` | 5 | 20.0% |
| `sectionStart.designation` | 3 | 12.0% |
| `sectionStart.editorial` | 1 | 4.0% |

### `sectionRecord` -- 14 instances in `data/`

| property | data | data % |
|---|---|---|
| `authority` | 14 | 100.0% |
| `citedAs` | 14 | 100.0% |
| `name` | 14 | 100.0% |
| `notes` | 5 | 35.7% |
| `/if.name` | 3 | 100.0% |
| `designation` | 3 | 21.4% |
| `needsQualification` | 1 | 7.1% |

### `sourceAlias` -- 4 instances in `data/`

| property | data | data % |
|---|---|---|
| `aliasOf` | 4 | 100.0% |

### `taxonRecord` -- 2874 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 2844 | 99.0% |
| `authority` | 2651 | 92.2% |
| `/if.authority` | 2650 | 100.0% |
| `rank` | 1020 | 35.5% |
| `notes` | 253 | 8.8% |
| `altSpellingOf` | 149 | 5.2% |
| `lang` | 76 | 2.6% |
| `originalParent` | 71 | 2.5% |
| `altRankOf` | 51 | 1.8% |
| `vulgarSpellingOf` | 45 | 1.6% |
| `homonym` | 18 | 0.6% |
| `needsQualification` | 17 | 0.6% |
| `bracket` | 9 | 0.3% |
| `designation` | 4 | 0.1% |
| `holotype` | 1 | 0.0% |
| `mineral` | 1 | 0.0% |
| `status` | 1 | 0.0% |
| `altGenderOf` | 0 | 0.0% |
| `latinSpellingOf` | 0 | 0.0% |

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

### `translatedNode` -- 16 instances in `data/`

| property | data | data % |
|---|---|---|
| `by` | 1 | 6.2% |

### `tree` -- 6727 instances in `data/`

| property | data | data % |
|---|---|---|
| `children` | 2237 | 33.3% |
| `pages` | 1222 | 18.2% |
| `rank` | 639 | 9.5% |
| `authority` | 337 | 5.0% |
| `parents` | 335 | 5.0% |
| `bracketEnd` | 28 | 0.4% |
| `bracketStart` | 28 | 0.4% |
| `mergeInto` | 14 | 0.2% |
| `altPlacements` | 6 | 0.1% |

### `treeDocument` -- 227 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxonomies` | 223 | 98.2% |
| `prefixes` | 31 | 13.7% |
| `phylogenies` | 25 | 11.0% |
| `notes` | 20 | 8.8% |
| `unused` | 5 | 2.2% |
| `contexts` | 2 | 0.9% |
| `assumptions` | 1 | 0.4% |
| `localityRegister` | 1 | 0.4% |

### `typeNode` -- 6 instances in `data/`

| property | data | data % |
|---|---|---|
| `fixation` | 2 | 33.3% |
| `fixedBy` | 0 | 0.0% |

### `uncertaintyFields` -- 6727 instances in `data/`

| property | data | data % |
|---|---|---|
| `provisional` | 140 | 2.1% |
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

23 of 31 members used, 1601 occurrences.

| value | count |
|---|---|
| `'Order'` | 305 |
| `'Class'` | 285 |
| `'species'` | 273 |
| `'Family'` | 222 |
| `'genus'` | 147 |
| `'variety'` | 65 |
| `'Phylum'` | 59 |
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
| `'Plesion'` | 3 |
| `'Branch'` | 2 |
| `'Parvclass'` | 1 |

**Never used (8):** `'Domain'`, `'Superphylum'`, `'Infraphylum'`, `'Superclass'`, `'Infraclass'`, `'subspecies'`, `'Clade'`, `'Scion'`

### `phylogeny#/$defs/ranks/properties/ranks/items/properties/group`

2 of 2 members used, 5 occurrences.

| value | count |
|---|---|
| `'species'` | 3 |
| `'genus'` | 2 |

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
| `phylogeny#/$defs/article/properties/number` | integer/string | intx186, strx13 | `Supplement`, `1/2`, `Part 4, No. 220`, `Adv. Pr.` | - |
| `phylogeny#/$defs/article/properties/pages/items` | integer/string | intx474, strx46 | `S637`, `S634`, `S631`, `S627` | - |
| `phylogeny#/$defs/article/properties/plates/items` | integer/string | intx31, strx17 | `II`, `I`, `XXXVII`, `VI` | - |
| `phylogeny#/$defs/article/properties/series` | integer/string | intx10, strx4 | `A`, `New Series` | - |
| `phylogeny#/$defs/article/properties/volume` | integer/string | intx286, strx26 | `New Series`, `3: Echinoderms: Notes fo...`, `Report of the 68th Meeti...`, `Eighty-Three Plates to A...` | - |
| `phylogeny#/$defs/citationNumber` | integer/string | intx2787, strx316 | `IV`, `X`, `VII`, `VIII` | - |
| `phylogeny#/$defs/cladisticFields/properties/matrix/items` | integer/string | intx139, strx5 | `?` | - |
| `phylogeny#/$defs/contexts` | object/null | dictx59, nullx41 | - | - |
| `phylogeny#/$defs/editorialObject/properties/corrections/properties/authority/properties/auth` | array/null | nullx7, listx1 | - | - |
| `phylogeny#/$defs/editorialObject/properties/inferred` | boolean/array | boolx41, listx26 | - | - |
| `phylogeny#/$defs/locationFields/properties/illustrations` | array/null | listx190, nullx13 | - | - |
| `phylogeny#/$defs/materialsFields/properties/material` | array/null | listx116, nullx9 | - | - |
| `phylogeny#/$defs/materialsFields/properties/ranges` | array/null | listx72, nullx41 | - | - |
| `phylogeny#/$defs/person/properties/death` | integer/null | intx107, nullx1 | - | - |
| `phylogeny#/$defs/phylogeny/properties/characteristics/items/additionalProperties/additionalProperties` | integer/string | intx40 | - | string |
| `phylogeny#/$defs/printedNumber` | string/integer | intx668, strx352 | `B`, `A`, `S-3965`, `SH-2` | - |
| `phylogeny#/$defs/relationalFields/properties/synonyms` | array/null | listx373 | - | null |
| `phylogeny#/$defs/sectionRecord/properties/name` | string/null | strx11, nullx3 | `Stellatae`, `Radiatae`, `Multivalvia`, `Lunatae` | - |
| `phylogeny#/$defs/taxonRecord/properties/holotype/additionalProperties/items` | array/string/integer | strx1 | `E23470` | array, integer |
| `phylogeny#/$defs/taxonRecord/properties/name` | string/null | strx2605, nullx239 | `Zoophytes`, `Zoophyta`, `Zoophites`, `Zoanthida` | - |
| `tree#/properties/children` | array/null | listx2231, nullx6 | - | - |

