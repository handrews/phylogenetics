# Schema usage census

**Generated** by `scripts/schema_audit.py` -- do not edit by hand.
Narrative analysis of these numbers is in `docs/schema-audit.md`.

Counts are *distinct instance locations* that reached a given schema
location, measured from the `jschon` evaluation result tree.

## 1. Unreached schema locations

Schema locations no data anywhere reaches. A nested location is listed
even when its parent is also unreached, so read parents first.

| `$defs` | unreached locations |
|---|---|
| `basicOccurrence` | `phylogeny#/$defs/basicOccurrence/properties/biota`<br>`phylogeny#/$defs/basicOccurrence/properties/biozones`<br>`phylogeny#/$defs/basicOccurrence/properties/biozones/items`<br>`phylogeny#/$defs/basicOccurrence/properties/eon`<br>`phylogeny#/$defs/basicOccurrence/properties/era`<br>`phylogeny#/$defs/basicOccurrence/properties/possibleSpecimens`<br>`phylogeny#/$defs/basicOccurrence/properties/possibleSpecimens/additionalProperties`<br>`phylogeny#/$defs/basicOccurrence/properties/possibleSpecimens/additionalProperties/items`<br>`phylogeny#/$defs/basicOccurrence/properties/possibleSpecimens/additionalProperties/items/items`<br>`phylogeny#/$defs/basicOccurrence/properties/section`<br>`phylogeny#/$defs/basicOccurrence/properties/seriesBoundary`<br>`phylogeny#/$defs/basicOccurrence/properties/seriesRange`<br>`phylogeny#/$defs/basicOccurrence/properties/sources`<br>`phylogeny#/$defs/basicOccurrence/properties/sources/items`<br>`phylogeny#/$defs/basicOccurrence/properties/specimens/additionalProperties/items`<br>`phylogeny#/$defs/basicOccurrence/properties/specimens/additionalProperties/items/items`<br>`phylogeny#/$defs/basicOccurrence/properties/stageBoundary`<br>`phylogeny#/$defs/basicOccurrence/properties/stageRange`<br>`phylogeny#/$defs/basicOccurrence/properties/subunit`<br>`phylogeny#/$defs/basicOccurrence/properties/superunit` |
| `eon` | `phylogeny#/$defs/eon` |
| `era` | `phylogeny#/$defs/era` |
| `illustration` | `phylogeny#/$defs/illustration/properties/collectedFrom`<br>`phylogeny#/$defs/illustration/properties/location`<br>`phylogeny#/$defs/illustration/properties/source` |
| `localSeriesRange` | `phylogeny#/$defs/localSeriesRange`<br>`phylogeny#/$defs/localSeriesRange/items` |
| `localStageRange` | `phylogeny#/$defs/localStageRange`<br>`phylogeny#/$defs/localStageRange/items` |
| `occurrence` | `phylogeny#/$defs/occurrence/properties/localSeriesBoundary`<br>`phylogeny#/$defs/occurrence/properties/localSeriesRange`<br>`phylogeny#/$defs/occurrence/properties/localStageBoundary`<br>`phylogeny#/$defs/occurrence/properties/localStageRange`<br>`phylogeny#/$defs/occurrence/properties/tentative` |
| `person` | `phylogeny#/$defs/person/properties/suffix` |
| `publication` | `phylogeny#/$defs/publication/properties/type` |
| `seriesRange` | `phylogeny#/$defs/seriesRange`<br>`phylogeny#/$defs/seriesRange/items` |
| `specimen` | `phylogeny#/$defs/specimen/oneOf/1/properties/id`<br>`phylogeny#/$defs/specimen/oneOf/1/properties/illustrations`<br>`phylogeny#/$defs/specimen/oneOf/1/properties/illustrations/items`<br>`phylogeny#/$defs/specimen/oneOf/1/properties/repository` |
| `specimens` | `phylogeny#/$defs/specimens/properties/allotype`<br>`phylogeny#/$defs/specimens/properties/neotype`<br>`phylogeny#/$defs/specimens/properties/repository` |
| `stageRange` | `phylogeny#/$defs/stageRange`<br>`phylogeny#/$defs/stageRange/items` |
| `taxon` | `phylogeny#/$defs/taxon/properties/holotype/additionalProperties/items/items`<br>`phylogeny#/$defs/taxon/properties/modifier`<br>`phylogeny#/$defs/taxon/properties/reason` |
| `tree` | `tree#/properties/categories`<br>`tree#/properties/categories/items`<br>`tree#/properties/data`<br>`tree#/properties/data/additionalProperties`<br>`tree#/properties/plates` |
| `trees` | `phylogeny#/$defs/trees/additionalProperties/properties/source` |

## 2. Property frequency by `$defs`

`data %` is the share of that container's instances carrying the
property.

### `article` -- 290 instances in `data/`

| property | data | data % |
|---|---|---|
| `authors` | 290 | 100.0% |
| `pubDate` | 289 | 99.7% |
| `title` | 240 | 82.8% |
| `volume` | 219 | 75.5% |
| `identifiers` | 205 | 70.7% |
| `pages` | 200 | 69.0% |
| `journal` | 198 | 68.3% |
| `number` | 149 | 51.4% |
| `identifiers.url` | 125 | 61.0% |
| `processDates` | 92 | 31.7% |
| `book` | 90 | 31.0% |
| `processDates.accepted` | 61 | 66.3% |
| `identifiers.doi` | 59 | 28.8% |
| `processDates.received` | 52 | 56.5% |
| `audit` | 48 | 16.6% |
| `audit.notes` | 48 | 100.0% |
| `audit.state` | 48 | 100.0% |
| `audit.coverage` | 29 | 60.4% |
| `processDates.online` | 27 | 29.3% |
| `identifiers.jstor` | 24 | 11.7% |
| `notes` | 24 | 8.3% |
| `processDates.revised` | 18 | 19.6% |
| `plates` | 10 | 3.4% |
| `articleNumber` | 7 | 2.4% |
| `processDates.read` | 7 | 7.6% |
| `seen` | 5 | 1.7% |
| `processDates.conferenceEnd` | 3 | 3.3% |
| `processDates.conferenceStart` | 3 | 3.3% |
| `processDates.transmitted` | 3 | 3.3% |
| `processDates.issued` | 2 | 2.2% |
| `series` | 2 | 0.7% |
| `translationOf` | 2 | 0.7% |
| `translations` | 2 | 0.7% |
| `chapter` | 1 | 0.3% |
| `editors` | 1 | 0.3% |
| `inPrep` | 1 | 0.3% |
| `processDates.printed` | 1 | 1.1% |
| `processDates.published` | 1 | 1.1% |
| `processDates.submitted` | 1 | 1.1% |
| `processDates.unknown` | 1 | 1.1% |
| `quotes` | 1 | 0.3% |
| `reading` | 1 | 0.3% |

### `authority` -- 1619 instances in `data/`

| property | data | data % |
|---|---|---|
| `source` | 1619 | 100.0% |
| `pages` | 56 | 3.5% |
| `illustrations` | 27 | 1.7% |
| `attributedTo` | 24 | 1.5% |
| `ex` | 2 | 0.1% |
| `notes` | 2 | 0.1% |

### `basicOccurrence` -- 33 instances in `data/`

| property | data | data % |
|---|---|---|
| `location` | 30 | 90.9% |
| `unit` | 21 | 63.6% |
| `notes` | 15 | 45.5% |
| `specimens` | 15 | 45.5% |
| `stage` | 14 | 42.4% |
| `series` | 13 | 39.4% |
| `period` | 5 | 15.2% |
| `biozone` | 3 | 9.1% |
| `stageModifier` | 3 | 9.1% |
| `biozoneRange` | 1 | 3.0% |
| `fauna` | 1 | 3.0% |
| `paleocontinent` | 1 | 3.0% |
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

### `illustration` -- 189 instances in `data/`

| property | data | data % |
|---|---|---|
| `figures` | 180 | 95.2% |
| `plate` | 106 | 56.1% |
| `page` | 70 | 37.0% |
| `textFigures` | 9 | 4.8% |
| `notes` | 4 | 2.1% |
| `uncertain` | 1 | 0.5% |
| `collectedFrom` | 0 | 0.0% |
| `location` | 0 | 0.0% |
| `source` | 0 | 0.0% |

### `modularDate` -- 289 instances in `data/`

| property | data | data % |
|---|---|---|
| `year` | 289 | 100.0% |
| `month` | 66 | 22.8% |
| `/then/oneOf/0.day` | 22 | 100.0% |
| `/then/oneOf/0.month` | 22 | 100.0% |
| `/then/oneOf/1.day` | 22 | 100.0% |
| `/then/oneOf/1.month` | 22 | 100.0% |
| `/then/oneOf/2.day` | 22 | 100.0% |
| `/then/oneOf/2.month` | 22 | 100.0% |
| `day` | 22 | 7.6% |
| `months` | 3 | 1.0% |
| `season` | 1 | 0.3% |

### `occurrence` -- 32 instances in `data/`

| property | data | data % |
|---|---|---|
| `localPeriod` | 3 | 9.4% |
| `localSeries` | 2 | 6.2% |
| `inferred` | 1 | 3.1% |
| `localStage` | 1 | 3.1% |
| `localStageModifier` | 1 | 3.1% |
| `localSeriesBoundary` | 0 | 0.0% |
| `localSeriesRange` | 0 | 0.0% |
| `localStageBoundary` | 0 | 0.0% |
| `localStageRange` | 0 | 0.0% |
| `tentative` | 0 | 0.0% |

### `person` -- 273 instances in `data/`

| property | data | data % |
|---|---|---|
| `family` | 273 | 100.0% |
| `given` | 273 | 100.0% |
| `birth` | 77 | 28.2% |
| `death` | 76 | 27.8% |
| `suffix` | 0 | 0.0% |

### `phylogeny` -- 36 instances in `data/`

| property | data | data % |
|---|---|---|
| `tree` | 36 | 100.0% |
| `treeType` | 36 | 100.0% |
| `methodology` | 18 | 50.0% |
| `notes` | 6 | 16.7% |
| `characteristics` | 1 | 2.8% |

### `publication` -- 128 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 128 | 100.0% |
| `editors` | 9 | 7.0% |
| `place` | 3 | 2.3% |
| `publisher` | 3 | 2.3% |
| `notes` | 1 | 0.8% |
| `type` | 0 | 0.0% |

### `specimens` -- 88 instances in `data/`

| property | data | data % |
|---|---|---|
| `holotype` | 68 | 77.3% |
| `lectotype` | 2 | 2.3% |
| `syntype` | 1 | 1.1% |
| `allotype` | 0 | 0.0% |
| `neotype` | 0 | 0.0% |
| `repository` | 0 | 0.0% |

### `taxon` -- 2719 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 2680 | 98.6% |
| `authority` | 1525 | 56.1% |
| `auth` | 961 | 35.3% |
| `year` | 958 | 35.2% |
| `rank` | 717 | 26.4% |
| `notes` | 210 | 7.7% |
| `altSpellingOf` | 161 | 5.9% |
| `lang` | 75 | 2.8% |
| `originalParent` | 65 | 2.4% |
| `altRankOf` | 49 | 1.8% |
| `vulgarSpellingOf` | 47 | 1.7% |
| `in` | 26 | 1.0% |
| `homonym` | 16 | 0.6% |
| `bracket` | 13 | 0.5% |
| `holotype` | 13 | 0.5% |
| `needsQualification` | 12 | 0.4% |
| `status` | 5 | 0.2% |
| `identifier` | 4 | 0.1% |
| `modifier` | 0 | 0.0% |
| `reason` | 0 | 0.0% |

### `tree` -- 6343 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxon` | 5747 | 90.6% |
| `children` | 2183 | 34.4% |
| `new` | 1461 | 23.0% |
| `notes` | 372 | 5.9% |
| `type` | 367 | 5.8% |
| `synonyms` | 358 | 5.6% |
| `parents` | 326 | 5.1% |
| `openTaxon` | 219 | 3.5% |
| `pages` | 209 | 3.3% |
| `illustrations` | 120 | 1.9% |
| `provisional` | 118 | 1.9% |
| `authority` | 92 | 1.5% |
| `specimens` | 88 | 1.4% |
| `diagnosis` | 69 | 1.1% |
| `year` | 59 | 0.9% |
| `auth` | 56 | 0.9% |
| `emended` | 49 | 0.8% |
| `bracket` | 35 | 0.6% |
| `moved` | 29 | 0.5% |
| `occurrences` | 26 | 0.4% |
| `modifier` | 22 | 0.3% |
| `outgroup` | 19 | 0.3% |
| `quoted` | 18 | 0.3% |
| `citedAs` | 17 | 0.3% |
| `pars` | 17 | 0.3% |
| `affTaxon` | 16 | 0.3% |
| `tentative` | 16 | 0.3% |
| `cfTaxon` | 15 | 0.2% |
| `questionable` | 12 | 0.2% |
| `matrix` | 8 | 0.1% |
| `altPlacements` | 7 | 0.1% |
| `rank` | 7 | 0.1% |
| `bootstrap` | 6 | 0.1% |
| `corrected` | 6 | 0.1% |
| `editorial` | 5 | 0.1% |
| `editorial.basis` | 5 | 100.0% |
| `mergeInto` | 5 | 0.1% |
| `non` | 4 | 0.1% |
| `editorial.inferred` | 3 | 60.0% |
| `or` | 3 | 0.0% |
| `editorial.source` | 2 | 40.0% |
| `in` | 2 | 0.0% |
| `removed` | 1 | 0.0% |
| `stem` | 1 | 0.0% |
| `categories` | 0 | 0.0% |
| `data` | 0 | 0.0% |
| `plates` | 0 | 0.0% |

### `trees` -- 218 instances in `data/`

| property | data | data % |
|---|---|---|
| `/additionalProperties.taxonomies` | 214 | 98.2% |
| `/additionalProperties.phylogenies` | 25 | 11.5% |
| `/additionalProperties.notes` | 20 | 9.2% |
| `/additionalProperties.assumptions` | 1 | 0.5% |
| `/additionalProperties.source` | 0 | 0.0% |

## 3. Enum member usage

### `phylogeny#/$defs/article/properties/audit/properties/coverage/additionalProperties`

4 of 4 members used, 261 occurrences.

| value | count |
|---|---|
| `'none'` | 98 |
| `'all'` | 66 |
| `'partly'` | 53 |
| `'na'` | 44 |

### `phylogeny#/$defs/article/properties/audit/properties/coverage/propertyNames`

9 of 9 members used, 261 occurrences.

| value | count |
|---|---|
| `'phylogeny'` | 29 |
| `'diagnoses'` | 29 |
| `'illustrations'` | 29 |
| `'occurrences'` | 29 |
| `'material'` | 29 |
| `'synonymy'` | 29 |
| `'types'` | 29 |
| `'newTaxa'` | 29 |
| `'skeleton'` | 29 |

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

24 of 32 members used, 724 occurrences.

| value | count |
|---|---|
| `'Family'` | 177 |
| `'species'` | 116 |
| `'Order'` | 112 |
| `'Class'` | 88 |
| `'variety'` | 32 |
| `'genus'` | 25 |
| `'Subfamily'` | 25 |
| `'section'` | 22 |
| `'Superfamily'` | 18 |
| `'subgenus'` | 17 |
| `'Suborder'` | 15 |
| `'Subclass'` | 15 |
| `'Phylum'` | 13 |
| `'Subphylum'` | 11 |
| `'Group'` | 9 |
| `'Grade'` | 9 |
| `'Division'` | 6 |
| `'Subkingdom'` | 3 |
| `'Unranked'` | 3 |
| `'Superorder'` | 2 |
| `'Branch'` | 2 |
| `'Plesion'` | 2 |
| `'Parvclass'` | 1 |
| `'Kingdom'` | 1 |

**Never used (8):** `'Domain'`, `'Superphylum'`, `'Infraphylum'`, `'Superclass'`, `'Infraclass'`, `'subspecies'`, `'Clade'`, `'Scion'`

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

10 of 14 members used, 147 occurrences.

| value | count |
|---|---|
| `'holotype'` | 68 |
| `'paratypes'` | 48 |
| `'unknowntypes'` | 16 |
| `'plesiotypes'` | 6 |
| `'topotypes'` | 3 |
| `'lectotype'` | 2 |
| `'syntypes'` | 1 |
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

## 4. Observed value types where the schema allows a union

Tests whether each multi-type declaration is actually needed.

| location | declared | observed | string examples | declared but unseen |
|---|---|---|---|---|
| `phylogeny#/$defs/article/properties/articleNumber` | integer/string | intx5, strx2 | `e1465`, `e38296` | - |
| `phylogeny#/$defs/article/properties/chapter` | integer/string | strx1 | `Report of E. Billings, E...` | integer |
| `phylogeny#/$defs/article/properties/number` | integer/string | intx140, strx9 | `Supplement`, `1/2`, `5–12`, `Adv. Pr.` | - |
| `phylogeny#/$defs/article/properties/pages/items` | integer/string | intx366, strx42 | `S637`, `S634`, `S631`, `S627` | - |
| `phylogeny#/$defs/article/properties/plates/items` | integer/string | intx11, strx8 | `II`, `I`, `IV`, `VII` | - |
| `phylogeny#/$defs/article/properties/series` | integer/string | intx2 | - | string |
| `phylogeny#/$defs/article/properties/volume` | integer/string | intx210, strx9 | `New Series`, `3: Echinoderms: Notes fo...`, `Report of the 68th Meeti...`, `4th Series` | - |
| `phylogeny#/$defs/basicOccurrence/properties/unit` | string/array | listx20, strx1 | `Craighead inlier` | - |
| `phylogeny#/$defs/citationNumber` | integer/string | intx643, listx344, strx183 | `IX`, `VIII`, `V`, `b` | - |
| `phylogeny#/$defs/person/properties/death` | integer/null | intx75, nullx1 | - | - |
| `phylogeny#/$defs/phylogeny/properties/characteristics/items/additionalProperties/additionalProperties` | integer/string | intx40 | - | string |
| `phylogeny#/$defs/specimens/additionalProperties/items` | string/array | strx513, listx4 | `F. 5420`, `F. 5419`, `F. 5418`, `F. 5417` | - |
| `phylogeny#/$defs/taxon/properties/holotype/additionalProperties/items` | array/string/integer | intx10, strx3 | `EE15373`, `EE 1659`, `E23470` | array |
| `phylogeny#/$defs/taxon/properties/name` | string/null | strx2483, nullx197 | `Zoophytes`, `Zoophyta`, `Zoophites`, `Zoanthida` | - |
| `tree#/properties/diagnosis` | string/null | strx68, nullx1 | `A cast of it shows a con...`, `Body hemisphæric, slight...`, `A *Pyrgocystis* specimen...`, `Mouth surrounded and cov...` | - |
| `tree#/properties/editorial/properties/inferred` | boolean/array | boolx2, listx1 | - | - |
| `tree#/properties/emended` | boolean/null | boolx49 | - | null |
| `tree#/properties/matrix/items` | integer/string | intx139, strx5 | `?` | - |

