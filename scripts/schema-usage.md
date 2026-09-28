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
| `article` | `phylogeny#/$defs/article/properties/repositoryAbbreviations`<br>`phylogeny#/$defs/article/properties/repositoryAbbreviations/additionalProperties`<br>`phylogeny#/$defs/article/properties/repositoryAbbreviations/propertyNames` |
| `basicOccurrence` | `phylogeny#/$defs/basicOccurrence/properties/biota`<br>`phylogeny#/$defs/basicOccurrence/properties/biozones`<br>`phylogeny#/$defs/basicOccurrence/properties/biozones/items`<br>`phylogeny#/$defs/basicOccurrence/properties/eon`<br>`phylogeny#/$defs/basicOccurrence/properties/era`<br>`phylogeny#/$defs/basicOccurrence/properties/possibleSpecimens`<br>`phylogeny#/$defs/basicOccurrence/properties/possibleSpecimens/additionalProperties`<br>`phylogeny#/$defs/basicOccurrence/properties/possibleSpecimens/additionalProperties/items`<br>`phylogeny#/$defs/basicOccurrence/properties/possibleSpecimens/additionalProperties/items/items`<br>`phylogeny#/$defs/basicOccurrence/properties/section`<br>`phylogeny#/$defs/basicOccurrence/properties/seriesBoundary`<br>`phylogeny#/$defs/basicOccurrence/properties/seriesRange`<br>`phylogeny#/$defs/basicOccurrence/properties/sources`<br>`phylogeny#/$defs/basicOccurrence/properties/sources/items`<br>`phylogeny#/$defs/basicOccurrence/properties/specimens/additionalProperties/items`<br>`phylogeny#/$defs/basicOccurrence/properties/specimens/additionalProperties/items/items`<br>`phylogeny#/$defs/basicOccurrence/properties/stageBoundary`<br>`phylogeny#/$defs/basicOccurrence/properties/stageRange`<br>`phylogeny#/$defs/basicOccurrence/properties/subunit`<br>`phylogeny#/$defs/basicOccurrence/properties/superunit` |
| `catalogNumber` | `phylogeny#/$defs/catalogNumber`<br>`phylogeny#/$defs/catalogNumber/oneOf/0`<br>`phylogeny#/$defs/catalogNumber/oneOf/1`<br>`phylogeny#/$defs/catalogNumber/oneOf/1/items` |
| `citedAct` | `phylogeny#/$defs/citedAct`<br>`phylogeny#/$defs/citedAct/properties/by` |
| `cladisticFields` | `phylogeny#/$defs/cladisticFields/properties/data`<br>`phylogeny#/$defs/cladisticFields/properties/data/additionalProperties` |
| `context` | `phylogeny#/$defs/context`<br>`phylogeny#/$defs/context/allOf/0`<br>`phylogeny#/$defs/context/allOf/1`<br>`phylogeny#/$defs/context/properties/biota`<br>`phylogeny#/$defs/context/properties/biozone`<br>`phylogeny#/$defs/context/properties/biozoneRange`<br>`phylogeny#/$defs/context/properties/biozoneRange/items`<br>`phylogeny#/$defs/context/properties/biozones`<br>`phylogeny#/$defs/context/properties/biozones/items`<br>`phylogeny#/$defs/context/properties/fauna`<br>`phylogeny#/$defs/context/properties/fauna/items`<br>`phylogeny#/$defs/context/properties/inferred`<br>`phylogeny#/$defs/context/properties/location`<br>`phylogeny#/$defs/context/properties/location/items`<br>`phylogeny#/$defs/context/properties/notes`<br>`phylogeny#/$defs/context/properties/paleocontinent`<br>`phylogeny#/$defs/context/properties/sources`<br>`phylogeny#/$defs/context/properties/sources/items`<br>`phylogeny#/$defs/context/properties/unit`<br>`phylogeny#/$defs/context/properties/unit/items` |
| `contextKey` | `phylogeny#/$defs/contextKey` |
| `contextRef` | `phylogeny#/$defs/contextRef`<br>`phylogeny#/$defs/contextRef/oneOf/0`<br>`phylogeny#/$defs/contextRef/oneOf/1`<br>`phylogeny#/$defs/contextRef/oneOf/1/properties/key`<br>`phylogeny#/$defs/contextRef/oneOf/1/properties/tentative` |
| `contexts` | `phylogeny#/$defs/contexts`<br>`phylogeny#/$defs/contexts/additionalProperties`<br>`phylogeny#/$defs/contexts/propertyNames` |
| `eon` | `phylogeny#/$defs/eon` |
| `era` | `phylogeny#/$defs/era` |
| `figure` | `phylogeny#/$defs/figure`<br>`phylogeny#/$defs/figure/anyOf/0`<br>`phylogeny#/$defs/figure/anyOf/1`<br>`phylogeny#/$defs/figure/anyOf/2`<br>`phylogeny#/$defs/figure/anyOf/3`<br>`phylogeny#/$defs/figure/properties/depicts`<br>`phylogeny#/$defs/figure/properties/of`<br>`phylogeny#/$defs/figure/properties/of/oneOf/0`<br>`phylogeny#/$defs/figure/properties/of/oneOf/1`<br>`phylogeny#/$defs/figure/properties/of/oneOf/1/items`<br>`phylogeny#/$defs/figure/properties/uncertain` |
| `figureLocatorFields` | `phylogeny#/$defs/figureLocatorFields/properties/non` |
| `inferredContext` | `phylogeny#/$defs/inferredContext`<br>`phylogeny#/$defs/inferredContext/properties/basis`<br>`phylogeny#/$defs/inferredContext/properties/paleocontinent`<br>`phylogeny#/$defs/inferredContext/properties/sources`<br>`phylogeny#/$defs/inferredContext/properties/sources/items` |
| `localSeriesRange` | `phylogeny#/$defs/localSeriesRange`<br>`phylogeny#/$defs/localSeriesRange/items` |
| `localStageRange` | `phylogeny#/$defs/localStageRange`<br>`phylogeny#/$defs/localStageRange/items` |
| `localTimeFields` | `phylogeny#/$defs/localTimeFields`<br>`phylogeny#/$defs/localTimeFields/properties/localPeriod`<br>`phylogeny#/$defs/localTimeFields/properties/localSeries`<br>`phylogeny#/$defs/localTimeFields/properties/localSeriesBoundary`<br>`phylogeny#/$defs/localTimeFields/properties/localSeriesRange`<br>`phylogeny#/$defs/localTimeFields/properties/localStage`<br>`phylogeny#/$defs/localTimeFields/properties/localStageBoundary`<br>`phylogeny#/$defs/localTimeFields/properties/localStageModifier`<br>`phylogeny#/$defs/localTimeFields/properties/localStageRange` |
| `materialEntry` | `phylogeny#/$defs/materialEntry`<br>`phylogeny#/$defs/materialEntry/anyOf/0`<br>`phylogeny#/$defs/materialEntry/anyOf/1`<br>`phylogeny#/$defs/materialEntry/anyOf/2`<br>`phylogeny#/$defs/materialEntry/properties/catalogNumbers`<br>`phylogeny#/$defs/materialEntry/properties/catalogNumbers/items`<br>`phylogeny#/$defs/materialEntry/properties/catalogNumbersAsPrinted`<br>`phylogeny#/$defs/materialEntry/properties/context`<br>`phylogeny#/$defs/materialEntry/properties/count`<br>`phylogeny#/$defs/materialEntry/properties/examined`<br>`phylogeny#/$defs/materialEntry/properties/formerIds`<br>`phylogeny#/$defs/materialEntry/properties/formerIds/items`<br>`phylogeny#/$defs/materialEntry/properties/fragmentOf`<br>`phylogeny#/$defs/materialEntry/properties/holder`<br>`phylogeny#/$defs/materialEntry/properties/label`<br>`phylogeny#/$defs/materialEntry/properties/listComplete`<br>`phylogeny#/$defs/materialEntry/properties/notes`<br>`phylogeny#/$defs/materialEntry/properties/parts`<br>`phylogeny#/$defs/materialEntry/properties/parts/items`<br>`phylogeny#/$defs/materialEntry/properties/repository`<br>`phylogeny#/$defs/materialEntry/properties/role`<br>`phylogeny#/$defs/materialEntry/properties/roleAct`<br>`phylogeny#/$defs/materialEntry/properties/roleAsPrinted`<br>`phylogeny#/$defs/materialEntry/properties/status` |
| `materialsFields` | `phylogeny#/$defs/materialsFields/properties/contexts`<br>`phylogeny#/$defs/materialsFields/properties/figures`<br>`phylogeny#/$defs/materialsFields/properties/figures/items`<br>`phylogeny#/$defs/materialsFields/properties/material`<br>`phylogeny#/$defs/materialsFields/properties/material/items`<br>`phylogeny#/$defs/materialsFields/properties/range` |
| `modularDate` | `phylogeny#/$defs/modularDate/then/oneOf/1/properties/month/anyOf/3`<br>`phylogeny#/$defs/modularDate/then/oneOf/2/properties/month/anyOf/5` |
| `occurrence` | `phylogeny#/$defs/occurrence/properties/localSeriesBoundary`<br>`phylogeny#/$defs/occurrence/properties/localSeriesRange`<br>`phylogeny#/$defs/occurrence/properties/localStageBoundary`<br>`phylogeny#/$defs/occurrence/properties/localStageRange`<br>`phylogeny#/$defs/occurrence/properties/tentative` |
| `person` | `phylogeny#/$defs/person/properties/suffix` |
| `publication` | `phylogeny#/$defs/publication/properties/type` |
| `range` | `phylogeny#/$defs/range`<br>`phylogeny#/$defs/range/allOf/0`<br>`phylogeny#/$defs/range/allOf/1`<br>`phylogeny#/$defs/range/properties/asPrinted`<br>`phylogeny#/$defs/range/properties/inferred`<br>`phylogeny#/$defs/range/properties/notes`<br>`phylogeny#/$defs/range/properties/regions`<br>`phylogeny#/$defs/range/properties/regions/items`<br>`phylogeny#/$defs/range/properties/regions/items/oneOf/0`<br>`phylogeny#/$defs/range/properties/regions/items/oneOf/1`<br>`phylogeny#/$defs/range/properties/regions/items/oneOf/1/properties/tentative`<br>`phylogeny#/$defs/range/properties/regions/items/oneOf/1/properties/value` |
| `repositories` | `phylogeny#/$defs/repositories`<br>`phylogeny#/$defs/repositories/additionalProperties`<br>`phylogeny#/$defs/repositories/additionalProperties/properties/formerly`<br>`phylogeny#/$defs/repositories/additionalProperties/properties/formerly/items`<br>`phylogeny#/$defs/repositories/additionalProperties/properties/kind`<br>`phylogeny#/$defs/repositories/additionalProperties/properties/name`<br>`phylogeny#/$defs/repositories/additionalProperties/properties/notes`<br>`phylogeny#/$defs/repositories/additionalProperties/properties/place`<br>`phylogeny#/$defs/repositories/propertyNames` |
| `role` | `phylogeny#/$defs/role` |
| `roles` | `phylogeny#/$defs/roles`<br>`phylogeny#/$defs/roles/properties/printedWords`<br>`phylogeny#/$defs/roles/properties/printedWords/additionalProperties`<br>`phylogeny#/$defs/roles/properties/printedWords/additionalProperties/properties/era`<br>`phylogeny#/$defs/roles/properties/printedWords/additionalProperties/properties/notes`<br>`phylogeny#/$defs/roles/properties/printedWords/additionalProperties/properties/role`<br>`phylogeny#/$defs/roles/properties/printedWords/additionalProperties/properties/role/oneOf/0`<br>`phylogeny#/$defs/roles/properties/printedWords/additionalProperties/properties/role/oneOf/1`<br>`phylogeny#/$defs/roles/properties/roles`<br>`phylogeny#/$defs/roles/properties/roles/additionalProperties`<br>`phylogeny#/$defs/roles/properties/roles/additionalProperties/properties/article`<br>`phylogeny#/$defs/roles/properties/roles/additionalProperties/properties/meaning`<br>`phylogeny#/$defs/roles/properties/roles/additionalProperties/properties/notes`<br>`phylogeny#/$defs/roles/properties/roles/additionalProperties/properties/regulated`<br>`phylogeny#/$defs/roles/properties/roles/propertyNames` |
| `seriesRange` | `phylogeny#/$defs/seriesRange`<br>`phylogeny#/$defs/seriesRange/items` |
| `specimen` | `phylogeny#/$defs/specimen/oneOf/1`<br>`phylogeny#/$defs/specimen/oneOf/1/properties/id`<br>`phylogeny#/$defs/specimen/oneOf/1/properties/illustrations`<br>`phylogeny#/$defs/specimen/oneOf/1/properties/illustrations/items`<br>`phylogeny#/$defs/specimen/oneOf/1/properties/repository` |
| `specimens` | `phylogeny#/$defs/specimens/properties/allotype`<br>`phylogeny#/$defs/specimens/properties/neotype`<br>`phylogeny#/$defs/specimens/properties/repository` |
| `stageRange` | `phylogeny#/$defs/stageRange`<br>`phylogeny#/$defs/stageRange/items` |
| `taxonRecord` | `phylogeny#/$defs/taxonRecord/properties/holotype/additionalProperties/items/items` |
| `timeFields` | `phylogeny#/$defs/timeFields`<br>`phylogeny#/$defs/timeFields/properties/eon`<br>`phylogeny#/$defs/timeFields/properties/era`<br>`phylogeny#/$defs/timeFields/properties/period`<br>`phylogeny#/$defs/timeFields/properties/series`<br>`phylogeny#/$defs/timeFields/properties/seriesBoundary`<br>`phylogeny#/$defs/timeFields/properties/seriesRange`<br>`phylogeny#/$defs/timeFields/properties/stage`<br>`phylogeny#/$defs/timeFields/properties/stageBoundary`<br>`phylogeny#/$defs/timeFields/properties/stageModifier`<br>`phylogeny#/$defs/timeFields/properties/stageRange` |
| `treeDocument` | `phylogeny#/$defs/treeDocument/properties/contexts`<br>`phylogeny#/$defs/treeDocument/properties/unused`<br>`phylogeny#/$defs/treeDocument/properties/unused/items` |
| `uncertaintyFields` | `phylogeny#/$defs/uncertaintyFields/properties/sensu` |

## 2. Property frequency by `$defs`

`data %` is the share of that container's instances carrying the
property.

### `actAndModifierFields` -- 5586 instances in `data/`

| property | data | data % |
|---|---|---|
| `new` | 1464 | 26.2% |
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
| `repositoryAbbreviations` | 0 | 0.0% |

### `authority` -- 1635 instances in `data/`

| property | data | data % |
|---|---|---|
| `source` | 1635 | 100.0% |
| `pages` | 64 | 3.9% |
| `illustrations` | 28 | 1.7% |
| `attributedTo` | 24 | 1.5% |
| `ex` | 2 | 0.1% |
| `notes` | 2 | 0.1% |

### `authorityFields` -- 9082 instances in `data/`

| property | data | data % |
|---|---|---|
| `authority` | 1632 | 18.0% |
| `auth` | 998 | 11.0% |
| `year` | 996 | 11.0% |
| `in` | 28 | 0.3% |

### `basicOccurrence` -- 35 instances in `data/`

| property | data | data % |
|---|---|---|
| `location` | 32 | 91.4% |
| `unit` | 23 | 65.7% |
| `notes` | 16 | 45.7% |
| `specimens` | 15 | 42.9% |
| `stage` | 14 | 40.0% |
| `series` | 13 | 37.1% |
| `period` | 5 | 14.3% |
| `biozone` | 3 | 8.6% |
| `stageModifier` | 3 | 8.6% |
| `biozoneRange` | 1 | 2.9% |
| `fauna` | 1 | 2.9% |
| `paleocontinent` | 1 | 2.9% |
| `biota` | 0 | 0.0% |
| `biozones` | 0 | 0.0% |
| `eon` | 0 | 0.0% |
| `era` | 0 | 0.0% |
| `possibleSpecimens` | 0 | 0.0% |
| `section` | 0 | 0.0% |
| `seriesBoundary` | 0 | 0.0% |
| `seriesRange` | 0 | 0.0% |
| `sources` | 0 | 0.0% |
| `stageBoundary` | 0 | 0.0% |
| `stageRange` | 0 | 0.0% |
| `subunit` | 0 | 0.0% |
| `superunit` | 0 | 0.0% |

### `citationFields` -- 9082 instances in `data/`

| property | data | data % |
|---|---|---|
| `rank` | 728 | 8.0% |
| `bracket` | 48 | 0.5% |

### `cladisticFields` -- 794 instances in `data/`

| property | data | data % |
|---|---|---|
| `outgroup` | 19 | 2.4% |
| `matrix` | 8 | 1.0% |
| `bootstrap` | 6 | 0.8% |
| `data` | 0 | 0.0% |

### `editorialObject` -- 8 instances in `data/`

| property | data | data % |
|---|---|---|
| `basis` | 8 | 100.0% |
| `inferred` | 6 | 75.0% |
| `corrections` | 2 | 25.0% |
| `corrections.authority` | 2 | 100.0% |
| `corrections.authority.source` | 2 | 100.0% |

### `figureLocatorFields` -- 200 instances in `data/`

| property | data | data % |
|---|---|---|
| `figures` | 189 | 94.5% |
| `plate` | 115 | 57.5% |
| `page` | 71 | 35.5% |
| `textFigures` | 11 | 5.5% |
| `notes` | 6 | 3.0% |
| `non` | 0 | 0.0% |

### `identificationFields` -- 6380 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxon` | 5780 | 90.6% |
| `openTaxon` | 219 | 3.4% |
| `citedAs` | 52 | 0.8% |
| `affTaxon` | 16 | 0.3% |
| `cfTaxon` | 15 | 0.2% |

### `illustration` -- 200 instances in `data/`

| property | data | data % |
|---|---|---|
| `uncertain` | 2 | 1.0% |

### `locationFields` -- 9082 instances in `data/`

| property | data | data % |
|---|---|---|
| `pages` | 223 | 2.5% |
| `illustrations` | 125 | 1.4% |

### `materialsFields` -- 5586 instances in `data/`

| property | data | data % |
|---|---|---|
| `specimens` | 91 | 1.6% |
| `occurrences` | 28 | 0.5% |
| `contexts` | 0 | 0.0% |
| `figures` | 0 | 0.0% |
| `material` | 0 | 0.0% |
| `range` | 0 | 0.0% |

### `metaFields` -- 6380 instances in `data/`

| property | data | data % |
|---|---|---|
| `notes` | 382 | 6.0% |
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

### `occurrence` -- 34 instances in `data/`

| property | data | data % |
|---|---|---|
| `localPeriod` | 3 | 8.8% |
| `localSeries` | 2 | 5.9% |
| `inferred` | 1 | 2.9% |
| `localStage` | 1 | 2.9% |
| `localStageModifier` | 1 | 2.9% |
| `localSeriesBoundary` | 0 | 0.0% |
| `localSeriesRange` | 0 | 0.0% |
| `localStageBoundary` | 0 | 0.0% |
| `localStageRange` | 0 | 0.0% |
| `tentative` | 0 | 0.0% |

### `person` -- 281 instances in `data/`

| property | data | data % |
|---|---|---|
| `given` | 281 | 100.0% |
| `surname` | 281 | 100.0% |
| `birth` | 82 | 29.2% |
| `death` | 81 | 28.8% |
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

### `relationalFields` -- 5586 instances in `data/`

| property | data | data % |
|---|---|---|
| `synonyms` | 362 | 6.5% |
| `moved` | 30 | 0.5% |
| `corrected` | 5 | 0.1% |
| `non` | 4 | 0.1% |
| `or` | 3 | 0.1% |
| `lapsus` | 1 | 0.0% |
| `lapsusFor` | 1 | 0.0% |
| `removed` | 1 | 0.0% |
| `substituted` | 1 | 0.0% |

### `specimens` -- 91 instances in `data/`

| property | data | data % |
|---|---|---|
| `holotype` | 70 | 76.9% |
| `lectotype` | 2 | 2.2% |
| `syntype` | 1 | 1.1% |
| `allotype` | 0 | 0.0% |
| `neotype` | 0 | 0.0% |
| `repository` | 0 | 0.0% |

### `taxonRecord` -- 2702 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 2663 | 98.6% |
| `notes` | 216 | 8.0% |
| `altSpellingOf` | 144 | 5.3% |
| `lang` | 75 | 2.8% |
| `originalParent` | 65 | 2.4% |
| `altRankOf` | 61 | 2.3% |
| `vulgarSpellingOf` | 47 | 1.7% |
| `homonym` | 16 | 0.6% |
| `holotype` | 13 | 0.5% |
| `needsQualification` | 12 | 0.4% |
| `status` | 5 | 0.2% |
| `designation` | 4 | 0.1% |

### `translatedNode` -- 15 instances in `data/`

| property | data | data % |
|---|---|---|
| `by` | 1 | 6.7% |

### `tree` -- 6380 instances in `data/`

| property | data | data % |
|---|---|---|
| `children` | 2191 | 34.3% |
| `parents` | 327 | 5.1% |
| `altPlacements` | 7 | 0.1% |
| `mergeInto` | 5 | 0.1% |

### `treeDocument` -- 221 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxonomies` | 217 | 98.2% |
| `phylogenies` | 25 | 11.3% |
| `notes` | 20 | 9.0% |
| `assumptions` | 1 | 0.5% |
| `contexts` | 0 | 0.0% |
| `unused` | 0 | 0.0% |

### `uncertaintyFields` -- 6380 instances in `data/`

| property | data | data % |
|---|---|---|
| `provisional` | 121 | 1.9% |
| `quoted` | 18 | 0.3% |
| `tentative` | 17 | 0.3% |
| `questionable` | 12 | 0.2% |
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

### `phylogeny#/$defs/figure/properties/depicts`

0 of 4 members used, 0 occurrences.

**Never used (4):** `'specimen'`, `'cast'`, `'reconstruction'`, `'drawing'`

### `phylogeny#/$defs/materialEntry/properties/roleAct`

0 of 2 members used, 0 occurrences.

**Never used (2):** `'designated'`, `'reported'`

### `phylogeny#/$defs/materialEntry/properties/status`

0 of 2 members used, 0 occurrences.

**Never used (2):** `'lost'`, `'untraced'`

### `phylogeny#/$defs/modularDate/properties/season`

1 of 5 members used, 1 occurrences.

| value | count |
|---|---|
| `'summer'` | 1 |

**Never used (4):** `'spring'`, `'fall'`, `'autumn'`, `'winter'`

### `phylogeny#/$defs/period`

1 of 22 members used, 5 occurrences.

| value | count |
|---|---|
| `'Ordovician'` | 5 |

**Never used (21):** `'Siderian'`, `'Rhyacian'`, `'Orosirian'`, `'Statherian'`, `'Calymmian'`, `'Ectasian'`, `'Stenian'`, `'Tonian'`, `'Cryogenian'`, `'Ediacaran'`, `'Cambrian'`, `'Silurian'`, `'Devonian'`, `'Carboniferous'`, `'Permian'`, `'Triassic'`, `'Jurassic'`, `'Cretaceous'`, `'Paleogene'`, `'Neogene'`, `'Quaternary'`

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

24 of 32 members used, 728 occurrences.

| value | count |
|---|---|
| `'Family'` | 177 |
| `'species'` | 115 |
| `'Order'` | 114 |
| `'Class'` | 90 |
| `'variety'` | 32 |
| `'Subfamily'` | 26 |
| `'genus'` | 25 |
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

### `phylogeny#/$defs/repositories/additionalProperties/properties/kind`

0 of 3 members used, 0 occurrences.

**Never used (3):** `'institution'`, `'person'`, `'locality'`

### `phylogeny#/$defs/role`

0 of 9 members used, 0 occurrences.

**Never used (9):** `'holotype'`, `'paratype'`, `'syntype'`, `'lectotype'`, `'paralectotype'`, `'neotype'`, `'topotype'`, `'hypotype'`, `'plesiotype'`

### `phylogeny#/$defs/series`

5 of 38 members used, 13 occurrences.

| value | count |
|---|---|
| `'Lower Devonian'` | 4 |
| `'Middle Devonian'` | 4 |
| `'Lower Ordovician'` | 3 |
| `'Llandovery'` | 1 |
| `'Upper Ordovician'` | 1 |

**Never used (33):** `'Terrenuevian'`, `'Cambrian Series 2'`, `'Miaolingian'`, `'Furongian'`, `'Middle Ordovician'`, `'Wenlock'`, `'Ludlow'`, `'Přídolí'`, `'Upper Devonian'`, `'Lower Mississippian'`, `'Middle Mississippian'`, `'Upper Mississippian'`, `'Lower Pennsylvanian'`, `'Middle Pennsylvanian'`, `'Upper Pennsylvanian'`, `'Cisuralian'`, `'Guadalupian'`, `'Lopingian'`, `'Lower Triassic'`, `'Middle Triassic'`, `'Upper Triassic'`, `'Lower Jurassic'`, `'Middle Jurassic'`, `'Upper Jurassic'`, `'Lower Cretaceous'`, `'Upper Cretaceous'`, `'Paleocene'`, `'Eocene'`, `'Oligocene'`, `'Miocene'`, `'Pliocene'`, `'Pleistocene'`, `'Holocene'`

### `phylogeny#/$defs/specimens/propertyNames`

10 of 14 members used, 151 occurrences.

| value | count |
|---|---|
| `'holotype'` | 70 |
| `'paratypes'` | 48 |
| `'unknowntypes'` | 17 |
| `'plesiotypes'` | 6 |
| `'topotypes'` | 3 |
| `'syntypes'` | 2 |
| `'lectotype'` | 2 |
| `'hypotypes'` | 1 |
| `'syntype'` | 1 |
| `'additional'` | 1 |

**Never used (4):** `'allotype'`, `'neotype'`, `'kleptotypes'`, `'paralectotypes'`

### `phylogeny#/$defs/stage`

8 of 100 members used, 14 occurrences.

| value | count |
|---|---|
| `'Eifelian'` | 3 |
| `'Emsian'` | 2 |
| `'Floian'` | 2 |
| `'Katian'` | 2 |
| `'Telychian'` | 2 |
| `'Givetian'` | 1 |
| `'Jiangshanian'` | 1 |
| `'Tremadocian'` | 1 |

**Never used (92):** `'Fortunian'`, `'Cambrian Stage 2'`, `'Cambrian Stage 3'`, `'Cambrian Stage 4'`, `'Wuliuan'`, `'Drumian'`, `'Guzhangian'`, `'Paibian'`, `'Cambrian Stage 10'`, `'Dapingian'`, `'Darriwilian'`, `'Sandbian'`, `'Hirnantian'`, `'Rhuddanian'`, `'Aeronian'`, `'Sheinwoodian'`, `'Homerian'`, `'Gorstian'`, `'Ludfordian'`, `'Lochkovian'`, `'Pragian'`, `'Frasnian'`, `'Famennian'`, `'Touraisian'`, `'Viséan'`, `'Serpukhovian'`, `'Baskirian'`, `'Moscovian'`, `'Kasimovian'`, `'Gzhelian'`, `'Asselian'`, `'Sakmarian'`, `'Artinskian'`, `'Kungurian'`, `'Roadian'`, `'Wordian'`, `'Capitanian'`, `'Wuchiapingian'`, `'Changhsingian'`, `'Induan'`, `'Olenekian'`, `'Anisian'`, `'Ladinian'`, `'Carnian'`, `'Norian'`, `'Rhaetian'`, `'Hettangian'`, `'Sinemurian'`, `'Toarcian'`, `'Aalenian'`, `'Bajocian'`, `'Bathonian'`, `'Callovian'`, `'Oxfordian'`, `'Kimmeridgian'`, `'Tithonian'`, `'Berriasian'`, `'Valanginian'`, `'Hauterivian'`, `'Barremian'`, `'Aptian'`, `'Albian'`, `'Cenomanian'`, `'Turonian'`, `'Coniacian'`, `'Santonian'`, `'Campanian'`, `'Maastrichtian'`, `'Danian'`, `'Selanian'`, `'Thanetian'`, `'Ypresian'`, `'Lutetian'`, `'Bartonian'`, `'Priabonian'`, `'Rupelian'`, `'Chattian'`, `'Aquitanian'`, `'Burdigalian'`, `'Langhian'`, `'Serravallian'`, `'Tortonian'`, `'Messinian'`, `'Zanclean'`, `'Piacenzian'`, `'Gelasian'`, `'Calabrian'`, `'Chibanian'`, `'Upper Pleistocene'`, `'Greenlandian'`, `'Northgrippian'`, `'Meghalayan'`

### `phylogeny#/$defs/stageModifier`

3 of 3 members used, 4 occurrences.

| value | count |
|---|---|
| `'upper'` | 2 |
| `'lower'` | 1 |
| `'middle'` | 1 |

### `phylogeny#/$defs/treeDocument/properties/unused/items`

0 of 5 members used, 0 occurrences.

**Never used (5):** `'material'`, `'figures'`, `'contexts'`, `'range'`, `'synonyms'`

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
| `phylogeny#/$defs/basicOccurrence/properties/unit` | string/array | listx22, strx1 | `Craighead inlier` | - |
| `phylogeny#/$defs/citationNumber` | integer/string | intx703, strx185 | `IX`, `VIII`, `V`, `b` | - |
| `phylogeny#/$defs/cladisticFields/properties/matrix/items` | integer/string | intx139, strx5 | `?` | - |
| `phylogeny#/$defs/editorialObject/properties/inferred` | boolean/array | listx3, boolx3 | - | - |
| `phylogeny#/$defs/person/properties/death` | integer/null | intx80, nullx1 | - | - |
| `phylogeny#/$defs/phylogeny/properties/characteristics/items/additionalProperties/additionalProperties` | integer/string | intx40 | - | string |
| `phylogeny#/$defs/specimens/additionalProperties/items` | string/array | strx521, listx4 | `an imperfect specimen le...`, `second specimen collecte...`, `first specimen collected...`, `C -- remains in the poss...` | - |
| `phylogeny#/$defs/taxonRecord/properties/holotype/additionalProperties/items` | array/string/integer | intx10, strx3 | `EE15373`, `EE 1659`, `E23470` | array |
| `phylogeny#/$defs/taxonRecord/properties/name` | string/null | strx2467, nullx196 | `Zoophytes`, `Zoophyta`, `Zoophites`, `Zoanthida` | - |

