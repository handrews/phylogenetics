# Schema usage census

**Generated** by `scripts/schema_audit.py` -- do not edit by hand.
Narrative analysis of these numbers is in `notes/audits/schema-audit.md`.

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

### `article` -- 305 instances in `data/`

| property | data | data % |
|---|---|---|
| `authors` | 305 | 100.0% |
| `pubDate` | 304 | 99.7% |
| `title` | 255 | 83.6% |
| `volume` | 234 | 76.7% |
| `pages` | 216 | 70.8% |
| `journal` | 213 | 69.8% |
| `identifiers` | 208 | 68.2% |
| `number` | 155 | 50.8% |
| `identifiers.url` | 126 | 60.6% |
| `processDates` | 98 | 32.1% |
| `book` | 90 | 29.5% |
| `processDates.accepted` | 63 | 64.3% |
| `identifiers.doi` | 61 | 29.3% |
| `processDates.received` | 53 | 54.1% |
| `audit` | 48 | 15.7% |
| `audit.notes` | 48 | 100.0% |
| `audit.state` | 48 | 100.0% |
| `notes` | 37 | 12.1% |
| `audit.coverage` | 30 | 62.5% |
| `processDates.online` | 28 | 28.6% |
| `identifiers.jstor` | 24 | 11.5% |
| `plates` | 21 | 6.9% |
| `processDates.revised` | 18 | 18.4% |
| `series` | 9 | 3.0% |
| `processDates.read` | 8 | 8.2% |
| `articleNumber` | 7 | 2.3% |
| `seen` | 5 | 1.6% |
| `processDates.transmitted` | 4 | 4.1% |
| `processDates.conferenceEnd` | 3 | 3.1% |
| `processDates.conferenceStart` | 3 | 3.1% |
| `processDates.issued` | 3 | 3.1% |
| `processDates.submitted` | 3 | 3.1% |
| `translationOf` | 2 | 0.7% |
| `translations` | 2 | 0.7% |
| `chapter` | 1 | 0.3% |
| `editors` | 1 | 0.3% |
| `inPrep` | 1 | 0.3% |
| `processDates.printed` | 1 | 1.0% |
| `processDates.published` | 1 | 1.0% |
| `processDates.unknown` | 1 | 1.0% |
| `quotes` | 1 | 0.3% |
| `reading` | 1 | 0.3% |

### `authority` -- 1633 instances in `data/`

| property | data | data % |
|---|---|---|
| `source` | 1633 | 100.0% |
| `pages` | 62 | 3.8% |
| `illustrations` | 28 | 1.7% |
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

### `illustration` -- 196 instances in `data/`

| property | data | data % |
|---|---|---|
| `figures` | 187 | 95.4% |
| `plate` | 113 | 57.7% |
| `page` | 70 | 35.7% |
| `textFigures` | 9 | 4.6% |
| `notes` | 4 | 2.0% |
| `uncertain` | 2 | 1.0% |
| `collectedFrom` | 0 | 0.0% |
| `location` | 0 | 0.0% |
| `source` | 0 | 0.0% |

### `modularDate` -- 304 instances in `data/`

| property | data | data % |
|---|---|---|
| `year` | 304 | 100.0% |
| `month` | 73 | 24.0% |
| `/then/oneOf/0.day` | 24 | 100.0% |
| `/then/oneOf/0.month` | 24 | 100.0% |
| `/then/oneOf/1.day` | 24 | 100.0% |
| `/then/oneOf/1.month` | 24 | 100.0% |
| `/then/oneOf/2.day` | 24 | 100.0% |
| `/then/oneOf/2.month` | 24 | 100.0% |
| `day` | 24 | 7.9% |
| `months` | 4 | 1.3% |
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

### `person` -- 279 instances in `data/`

| property | data | data % |
|---|---|---|
| `given` | 279 | 100.0% |
| `surname` | 279 | 100.0% |
| `birth` | 80 | 28.7% |
| `death` | 79 | 28.3% |
| `suffix` | 0 | 0.0% |

### `phylogeny` -- 36 instances in `data/`

| property | data | data % |
|---|---|---|
| `tree` | 36 | 100.0% |
| `treeType` | 36 | 100.0% |
| `methodology` | 18 | 50.0% |
| `notes` | 6 | 16.7% |
| `characteristics` | 1 | 2.8% |

### `publication` -- 135 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 135 | 100.0% |
| `editors` | 9 | 6.7% |
| `place` | 8 | 5.9% |
| `publisher` | 8 | 5.9% |
| `notes` | 2 | 1.5% |
| `type` | 0 | 0.0% |

### `specimens` -- 89 instances in `data/`

| property | data | data % |
|---|---|---|
| `holotype` | 69 | 77.5% |
| `lectotype` | 2 | 2.2% |
| `syntype` | 1 | 1.1% |
| `allotype` | 0 | 0.0% |
| `neotype` | 0 | 0.0% |
| `repository` | 0 | 0.0% |

### `taxon` -- 2721 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 2682 | 98.6% |
| `authority` | 1536 | 56.4% |
| `auth` | 939 | 34.5% |
| `year` | 936 | 34.4% |
| `rank` | 716 | 26.3% |
| `notes` | 216 | 7.9% |
| `altSpellingOf` | 165 | 6.1% |
| `lang` | 75 | 2.8% |
| `originalParent` | 65 | 2.4% |
| `altRankOf` | 59 | 2.2% |
| `vulgarSpellingOf` | 47 | 1.7% |
| `in` | 26 | 1.0% |
| `homonym` | 16 | 0.6% |
| `bracket` | 13 | 0.5% |
| `holotype` | 13 | 0.5% |
| `needsQualification` | 12 | 0.4% |
| `status` | 5 | 0.2% |
| `designation` | 4 | 0.1% |
| `modifier` | 0 | 0.0% |
| `reason` | 0 | 0.0% |

### `tree` -- 6350 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxon` | 5751 | 90.6% |
| `children` | 2184 | 34.4% |
| `new` | 1461 | 23.0% |
| `notes` | 377 | 5.9% |
| `type` | 368 | 5.8% |
| `synonyms` | 362 | 5.7% |
| `parents` | 326 | 5.1% |
| `openTaxon` | 219 | 3.4% |
| `pages` | 219 | 3.4% |
| `illustrations` | 123 | 1.9% |
| `provisional` | 120 | 1.9% |
| `authority` | 95 | 1.5% |
| `specimens` | 89 | 1.4% |
| `diagnosis` | 69 | 1.1% |
| `year` | 63 | 1.0% |
| `auth` | 62 | 1.0% |
| `emended` | 53 | 0.8% |
| `citedAs` | 44 | 0.7% |
| `bracket` | 35 | 0.6% |
| `moved` | 30 | 0.5% |
| `occurrences` | 26 | 0.4% |
| `modifier` | 22 | 0.3% |
| `outgroup` | 19 | 0.3% |
| `pars` | 19 | 0.3% |
| `quoted` | 18 | 0.3% |
| `tentative` | 17 | 0.3% |
| `affTaxon` | 16 | 0.3% |
| `cfTaxon` | 15 | 0.2% |
| `questionable` | 12 | 0.2% |
| `matrix` | 8 | 0.1% |
| `altPlacements` | 7 | 0.1% |
| `rank` | 7 | 0.1% |
| `bootstrap` | 6 | 0.1% |
| `corrected` | 6 | 0.1% |
| `editorial` | 6 | 0.1% |
| `editorial.basis` | 6 | 100.0% |
| `mergeInto` | 5 | 0.1% |
| `editorial.inferred` | 4 | 66.7% |
| `non` | 4 | 0.1% |
| `or` | 3 | 0.0% |
| `editorial.source` | 2 | 33.3% |
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

4 of 4 members used, 270 occurrences.

| value | count |
|---|---|
| `'none'` | 100 |
| `'all'` | 70 |
| `'partly'` | 55 |
| `'na'` | 45 |

### `phylogeny#/$defs/article/properties/audit/properties/coverage/propertyNames`

9 of 9 members used, 270 occurrences.

| value | count |
|---|---|
| `'phylogeny'` | 30 |
| `'diagnoses'` | 30 |
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

24 of 32 members used, 723 occurrences.

| value | count |
|---|---|
| `'Family'` | 177 |
| `'species'` | 115 |
| `'Order'` | 111 |
| `'Class'` | 89 |
| `'variety'` | 32 |
| `'Subfamily'` | 26 |
| `'genus'` | 25 |
| `'section'` | 22 |
| `'Superfamily'` | 18 |
| `'subgenus'` | 17 |
| `'Subclass'` | 15 |
| `'Suborder'` | 14 |
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

10 of 14 members used, 148 occurrences.

| value | count |
|---|---|
| `'holotype'` | 69 |
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
| `phylogeny#/$defs/article/properties/number` | integer/string | intx146, strx9 | `Supplement`, `1/2`, `Adv. Pr.`, `1–2` | - |
| `phylogeny#/$defs/article/properties/pages/items` | integer/string | intx398, strx42 | `S637`, `S634`, `S631`, `S627` | - |
| `phylogeny#/$defs/article/properties/plates/items` | integer/string | intx29, strx12 | `II`, `I`, `VI`, `V` | - |
| `phylogeny#/$defs/article/properties/series` | integer/string | intx8, strx1 | `A` | - |
| `phylogeny#/$defs/article/properties/volume` | integer/string | intx225, strx9 | `New Series`, `3: Echinoderms: Notes fo...`, `Report of the 68th Meeti...`, `4th Series` | - |
| `phylogeny#/$defs/basicOccurrence/properties/unit` | string/array | listx20, strx1 | `Craighead inlier` | - |
| `phylogeny#/$defs/citationNumber` | integer/string | intx678, listx358, strx185 | `IX`, `VIII`, `V`, `b` | - |
| `phylogeny#/$defs/person/properties/death` | integer/null | intx78, nullx1 | - | - |
| `phylogeny#/$defs/phylogeny/properties/characteristics/items/additionalProperties/additionalProperties` | integer/string | intx40 | - | string |
| `phylogeny#/$defs/specimens/additionalProperties/items` | string/array | strx516, listx4 | `F. 5420`, `F. 5419`, `F. 5418`, `F. 5417` | - |
| `phylogeny#/$defs/taxon/properties/holotype/additionalProperties/items` | array/string/integer | intx10, strx3 | `EE15373`, `EE 1659`, `E23470` | array |
| `phylogeny#/$defs/taxon/properties/name` | string/null | strx2486, nullx196 | `Zoophytes`, `Zoophyta`, `Zoophites`, `Zoanthida` | - |
| `tree#/properties/diagnosis` | string/null | strx68, nullx1 | `A cast of it shows a con...`, `Body hemisphæric, slight...`, `A *Pyrgocystis* specimen...`, `Mouth surrounded and cov...` | - |
| `tree#/properties/editorial/properties/inferred` | boolean/array | listx2, boolx2 | - | - |
| `tree#/properties/emended` | boolean/null | boolx53 | - | null |
| `tree#/properties/matrix/items` | integer/string | intx139, strx5 | `?` | - |

