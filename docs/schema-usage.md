# Schema usage census

**Generated** by `scripts/schema_audit.py` -- do not edit by hand.
Narrative analysis of these numbers is in `docs/schema-audit.md`.

Counts are *distinct instance locations* that reached a given schema
location, measured from the `jschon` evaluation result tree.

> `trees.yaml` do not currently validate. They are still censused -- presence does not require validity -- so their columns show what is *used*, not what is correct.

## 1. Unreached schema locations

Schema locations no data anywhere reaches. A nested location is listed
even when its parent is also unreached, so read parents first.

| `$defs` | unreached locations |
|---|---|
| `basicOccurrence` | `phylogeny#/$defs/basicOccurrence/properties/eon`<br>`phylogeny#/$defs/basicOccurrence/properties/era`<br>`phylogeny#/$defs/basicOccurrence/properties/seriesBoundary`<br>`phylogeny#/$defs/basicOccurrence/properties/seriesRange`<br>`phylogeny#/$defs/basicOccurrence/properties/stageRange` |
| `eon` | `phylogeny#/$defs/eon` |
| `era` | `phylogeny#/$defs/era` |
| `illustration` | `phylogeny#/$defs/illustration/properties/collectedFrom`<br>`phylogeny#/$defs/illustration/properties/location`<br>`phylogeny#/$defs/illustration/properties/source` |
| `localSeriesRange` | `phylogeny#/$defs/localSeriesRange`<br>`phylogeny#/$defs/localSeriesRange/items` |
| `occurrence` | `phylogeny#/$defs/occurrence/properties/localSeriesBoundary`<br>`phylogeny#/$defs/occurrence/properties/localSeriesRange` |
| `person` | `phylogeny#/$defs/person/properties/suffix` |
| `publication` | `phylogeny#/$defs/publication/properties/type` |
| `seriesRange` | `phylogeny#/$defs/seriesRange`<br>`phylogeny#/$defs/seriesRange/items` |
| `specimen` | `phylogeny#/$defs/specimen/oneOf/1/properties/id`<br>`phylogeny#/$defs/specimen/oneOf/1/properties/illustrations`<br>`phylogeny#/$defs/specimen/oneOf/1/properties/illustrations/items`<br>`phylogeny#/$defs/specimen/oneOf/1/properties/repository` |
| `specimens` | `phylogeny#/$defs/specimens/properties/allotype`<br>`phylogeny#/$defs/specimens/properties/neotype`<br>`phylogeny#/$defs/specimens/properties/repository` |
| `taxon` | `phylogeny#/$defs/taxon/properties/holotype/additionalProperties/items/items`<br>`phylogeny#/$defs/taxon/properties/modifier`<br>`phylogeny#/$defs/taxon/properties/reason` |
| `tree` | `tree#/properties/categories`<br>`tree#/properties/categories/items`<br>`tree#/properties/citation/properties/figures`<br>`tree#/properties/citation/properties/pages`<br>`tree#/properties/citation/properties/pages/items`<br>`tree#/properties/citation/properties/plates`<br>`tree#/properties/citation/properties/plates/items`<br>`tree#/properties/data`<br>`tree#/properties/data/additionalProperties`<br>`tree#/properties/plates` |
| `trees` | `phylogeny#/$defs/trees/additionalProperties/properties/source` |

## 2. Property frequency by `$defs`

`data %` is the share of that container's instances carrying the
property. `personal` is counted separately.

### `article` -- 289 instances in `data/`

| property | data | data % | personal |
|---|---|---|---|
| `authors` | 289 | 100.0% | 1 |
| `pubDate` | 288 | 99.7% | 1 |
| `title` | 239 | 82.7% | 1 |
| `volume` | 218 | 75.4% | 0 |
| `identifiers` | 203 | 70.2% | 0 |
| `pages` | 199 | 68.9% | 0 |
| `journal` | 197 | 68.2% | 1 |
| `number` | 149 | 51.6% | 0 |
| `identifiers.url` | 123 | 60.6% | 0 |
| `processDates` | 91 | 31.5% | 0 |
| `book` | 90 | 31.1% | 0 |
| `processDates.accepted` | 61 | 67.0% | 0 |
| `identifiers.doi` | 59 | 29.1% | 0 |
| `processDates.received` | 52 | 57.1% | 0 |
| `processDates.online` | 27 | 29.7% | 0 |
| `identifiers.jstor` | 24 | 11.8% | 0 |
| `complete` | 23 | 8.0% | 0 |
| `complete.history` | 23 | 100.0% | 0 |
| `notes` | 23 | 8.0% | 0 |
| `complete.named` | 22 | 95.7% | 0 |
| `complete.open` | 21 | 91.3% | 0 |
| `complete.specimens` | 21 | 91.3% | 0 |
| `complete.specimens.all` | 21 | 100.0% | 0 |
| `complete.specimens.basic` | 21 | 100.0% | 0 |
| `processDates.revised` | 18 | 19.8% | 0 |
| `plates` | 10 | 3.5% | 0 |
| `articleNumber` | 7 | 2.4% | 0 |
| `processDates.read` | 7 | 7.7% | 0 |
| `seen` | 5 | 1.7% | 0 |
| `processDates.transmitted` | 3 | 3.3% | 0 |
| `processDates.conferenceEnd` | 2 | 2.2% | 0 |
| `processDates.conferenceStart` | 2 | 2.2% | 0 |
| `processDates.issued` | 2 | 2.2% | 0 |
| `series` | 2 | 0.7% | 0 |
| `translationOf` | 2 | 0.7% | 0 |
| `translations` | 2 | 0.7% | 0 |
| `chapter` | 1 | 0.3% | 0 |
| `complete.notes` | 1 | 4.3% | 0 |
| `editors` | 1 | 0.3% | 0 |
| `inPrep` | 1 | 0.3% | 0 |
| `processDates.printed` | 1 | 1.1% | 0 |
| `processDates.published` | 1 | 1.1% | 0 |
| `processDates.submitted` | 1 | 1.1% | 0 |
| `processDates.unknown` | 1 | 1.1% | 0 |
| `quotes` | 1 | 0.3% | 0 |
| `reading` | 1 | 0.3% | 0 |

### `authority` -- 1640 instances in `data/`

| property | data | data % | personal |
|---|---|---|---|
| `source` | 1640 | 100.0% | 0 |
| `page` | 46 | 2.8% | 0 |
| `attributedTo` | 24 | 1.5% | 0 |
| `illustrations` | 24 | 1.5% | 0 |
| `pages` | 7 | 0.4% | 0 |
| `ex` | 2 | 0.1% | 0 |
| `notes` | 2 | 0.1% | 0 |

### `basicOccurrence` -- 33 instances in `data/`

| property | data | data % | personal |
|---|---|---|---|
| `location` | 29 | 87.9% | 35 |
| `unit` | 21 | 63.6% | 35 |
| `specimens` | 15 | 45.5% | 14 |
| `notes` | 14 | 42.4% | 20 |
| `stage` | 14 | 42.4% | 23 |
| `series` | 13 | 39.4% | 18 |
| `period` | 5 | 15.2% | 7 |
| `biozone` | 3 | 9.1% | 25 |
| `stageModifier` | 3 | 9.1% | 0 |
| `biozoneRange` | 1 | 3.0% | 0 |
| `fauna` | 1 | 3.0% | 0 |
| `paleocontinent` | 1 | 3.0% | 42 |
| `biota` | 0 | 0.0% | 4 |
| `biozones` | 0 | 0.0% | 2 |
| `eon` | 0 | 0.0% | 0 |
| `era` | 0 | 0.0% | 0 |
| `possibleSpecimens` | 0 | 0.0% | 2 |
| `section` | 0 | 0.0% | 2 |
| `seriesBoundary` | 0 | 0.0% | 0 |
| `seriesRange` | 0 | 0.0% | 0 |
| `sources` | 0 | 0.0% | 40 |
| `stageBoundary` | 0 | 0.0% | 10 |
| `stageRange` | 0 | 0.0% | 0 |
| `subunit` | 0 | 0.0% | 20 |
| `superunit` | 0 | 0.0% | 2 |

### `illustration` -- 181 instances in `data/`

| property | data | data % | personal |
|---|---|---|---|
| `figures` | 130 | 71.8% | 0 |
| `plate` | 100 | 55.2% | 0 |
| `page` | 70 | 38.7% | 0 |
| `figure` | 43 | 23.8% | 0 |
| `textFigure` | 5 | 2.8% | 0 |
| `notes` | 3 | 1.7% | 0 |
| `textFigures` | 3 | 1.7% | 0 |
| `uncertain` | 1 | 0.6% | 0 |
| `collectedFrom` | 0 | 0.0% | 0 |
| `location` | 0 | 0.0% | 0 |
| `source` | 0 | 0.0% | 0 |

### `modularDate` -- 288 instances in `data/`

| property | data | data % | personal |
|---|---|---|---|
| `year` | 288 | 100.0% | 1 |
| `month` | 66 | 22.9% | 0 |
| `/then/oneOf/0.day` | 22 | 100.0% | 0 |
| `/then/oneOf/0.month` | 22 | 100.0% | 0 |
| `/then/oneOf/1.day` | 22 | 100.0% | 0 |
| `/then/oneOf/1.month` | 22 | 100.0% | 0 |
| `/then/oneOf/2.day` | 22 | 100.0% | 0 |
| `/then/oneOf/2.month` | 22 | 100.0% | 0 |
| `day` | 22 | 7.6% | 0 |
| `months` | 3 | 1.0% | 0 |
| `season` | 1 | 0.3% | 0 |

### `occurrence` -- 32 instances in `data/`

| property | data | data % | personal |
|---|---|---|---|
| `localPeriod` | 3 | 9.4% | 0 |
| `localSeries` | 2 | 6.2% | 2 |
| `localStage` | 2 | 6.2% | 11 |
| `inferred` | 1 | 3.1% | 25 |
| `localStageModifier` | 1 | 3.1% | 0 |
| `localSeriesBoundary` | 0 | 0.0% | 0 |
| `localSeriesRange` | 0 | 0.0% | 0 |
| `localStageBoundary` | 0 | 0.0% | 2 |
| `localStageRange` | 0 | 0.0% | 1 |
| `tentative` | 0 | 0.0% | 1 |

### `person` -- 273 instances in `data/`

| property | data | data % | personal |
|---|---|---|---|
| `family` | 273 | 100.0% | 1 |
| `given` | 273 | 100.0% | 1 |
| `birth` | 77 | 28.2% | 0 |
| `death` | 76 | 27.8% | 0 |
| `suffix` | 0 | 0.0% | 0 |

### `phylogeny` -- 36 instances in `data/`

| property | data | data % | personal |
|---|---|---|---|
| `tree` | 36 | 100.0% | 0 |
| `treeType` | 36 | 100.0% | 0 |
| `methodology` | 18 | 50.0% | 0 |
| `notes` | 6 | 16.7% | 0 |
| `characteristics` | 1 | 2.8% | 0 |

### `publication` -- 126 instances in `data/`

| property | data | data % | personal |
|---|---|---|---|
| `name` | 126 | 100.0% | 1 |
| `editors` | 9 | 7.1% | 0 |
| `place` | 3 | 2.4% | 0 |
| `publisher` | 3 | 2.4% | 0 |
| `notes` | 1 | 0.8% | 0 |
| `type` | 0 | 0.0% | 0 |

### `specimens` -- 88 instances in `data/`

| property | data | data % | personal |
|---|---|---|---|
| `holotype` | 68 | 77.3% | 0 |
| `lectotype` | 2 | 2.3% | 0 |
| `syntype` | 1 | 1.1% | 0 |
| `allotype` | 0 | 0.0% | 0 |
| `neotype` | 0 | 0.0% | 0 |
| `repository` | 0 | 0.0% | 0 |

### `taxon` -- 2743 instances in `data/`

| property | data | data % | personal |
|---|---|---|---|
| `name` | 2704 | 98.6% | 0 |
| `authority` | 1552 | 56.6% | 0 |
| `auth` | 963 | 35.1% | 0 |
| `year` | 960 | 35.0% | 0 |
| `rank` | 730 | 26.6% | 0 |
| `notes` | 206 | 7.5% | 0 |
| `altSpellingOf` | 160 | 5.8% | 0 |
| `lang` | 75 | 2.7% | 0 |
| `originalParent` | 64 | 2.3% | 0 |
| `vulgarSpellingOf` | 47 | 1.7% | 0 |
| `altRankOf` | 45 | 1.6% | 0 |
| `needsQualification` | 28 | 1.0% | 0 |
| `in` | 26 | 0.9% | 0 |
| `homonym` | 16 | 0.6% | 0 |
| `bracket` | 13 | 0.5% | 0 |
| `holotype` | 13 | 0.5% | 0 |
| `synonym` | 8 | 0.3% | 0 |
| `status` | 5 | 0.2% | 0 |
| `identifier` | 4 | 0.1% | 0 |
| `modifier` | 0 | 0.0% | 0 |
| `reason` | 0 | 0.0% | 0 |

### `tree` -- 6445 instances in `data/`

| property | data | data % | personal |
|---|---|---|---|
| `taxon` | 5838 | 90.6% | 368 |
| `children` | 2215 | 34.4% | 124 |
| `new` | 1480 | 23.0% | 0 |
| `type` | 389 | 6.0% | 105 |
| `synonyms` | 385 | 6.0% | 49 |
| `notes` | 364 | 5.6% | 9 |
| `parents` | 326 | 5.1% | 38 |
| `openTaxon` | 230 | 3.6% | 16 |
| `page` | 138 | 2.1% | 0 |
| `provisional` | 120 | 1.9% | 23 |
| `illustrations` | 115 | 1.8% | 0 |
| `specimens` | 88 | 1.4% | 0 |
| `authority` | 86 | 1.3% | 0 |
| `diagnosis` | 69 | 1.1% | 0 |
| `pages` | 56 | 0.9% | 0 |
| `emended` | 49 | 0.8% | 0 |
| `year` | 48 | 0.7% | 2 |
| `auth` | 46 | 0.7% | 2 |
| `bracket` | 35 | 0.5% | 0 |
| `moved` | 29 | 0.4% | 0 |
| `occurrences` | 26 | 0.4% | 31 |
| `modifier` | 20 | 0.3% | 1 |
| `outgroup` | 19 | 0.3% | 0 |
| `quoted` | 18 | 0.3% | 1 |
| `pars` | 17 | 0.3% | 4 |
| `affTaxon` | 16 | 0.2% | 0 |
| `tentative` | 16 | 0.2% | 0 |
| `cfTaxon` | 15 | 0.2% | 1 |
| `citation` | 12 | 0.2% | 0 |
| `citation.source` | 12 | 100.0% | 0 |
| `citation.year` | 12 | 100.0% | 0 |
| `questionable` | 12 | 0.2% | 3 |
| `citation.authors` | 11 | 91.7% | 0 |
| `citation.content` | 11 | 91.7% | 0 |
| `matrix` | 8 | 0.1% | 0 |
| `rank` | 8 | 0.1% | 0 |
| `altPlacements` | 7 | 0.1% | 0 |
| `bootstrap` | 6 | 0.1% | 0 |
| `corrected` | 6 | 0.1% | 0 |
| `mergeInto` | 5 | 0.1% | 0 |
| `non` | 4 | 0.1% | 0 |
| `or` | 3 | 0.0% | 0 |
| `in` | 2 | 0.0% | 0 |
| `citation.disambiguator` | 1 | 8.3% | 0 |
| `removed` | 1 | 0.0% | 0 |
| `stem` | 1 | 0.0% | 0 |
| `categories` | 0 | 0.0% | 0 |
| `citation.figures` | 0 | 0.0% | 0 |
| `citation.pages` | 0 | 0.0% | 0 |
| `citation.plates` | 0 | 0.0% | 0 |
| `data` | 0 | 0.0% | 0 |
| `plates` | 0 | 0.0% | 0 |

### `trees` -- 9 instances in `data/`

| property | data | data % | personal |
|---|---|---|---|
| `/additionalProperties.taxonomies` | 214 | 98.2% | 1 |
| `/additionalProperties.phylogenies` | 25 | 11.5% | 0 |
| `/additionalProperties.notes` | 20 | 9.2% | 0 |
| `/additionalProperties.assumptions` | 1 | 0.5% | 0 |
| `/additionalProperties.source` | 0 | 0.0% | 0 |

## 3. Enum member usage

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

2 of 22 members used, 12 occurrences.

| value | count |
|---|---|
| `'Ordovician'` | 10 |
| `'Cambrian'` | 2 |

**Never used (20):** `'Siderian'`, `'Rhyacian'`, `'Orosirian'`, `'Statherian'`, `'Calymmian'`, `'Ectasian'`, `'Stenian'`, `'Tonian'`, `'Cryogenian'`, `'Ediacaran'`, `'Silurian'`, `'Devonian'`, `'Carboniferous'`, `'Permian'`, `'Triassic'`, `'Jurassic'`, `'Cretaceous'`, `'Paleogene'`, `'Neogene'`, `'Quaternary'`

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

24 of 32 members used, 738 occurrences.

| value | count |
|---|---|
| `'Family'` | 182 |
| `'species'` | 116 |
| `'Order'` | 114 |
| `'Class'` | 88 |
| `'variety'` | 32 |
| `'genus'` | 27 |
| `'Subfamily'` | 26 |
| `'section'` | 22 |
| `'Suborder'` | 18 |
| `'subgenus'` | 18 |
| `'Superfamily'` | 18 |
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

8 of 38 members used, 31 occurrences.

| value | count |
|---|---|
| `'Miaolingian'` | 8 |
| `'Cambrian Series 2'` | 5 |
| `'Lower Devonian'` | 4 |
| `'Middle Devonian'` | 4 |
| `'Furongian'` | 4 |
| `'Lower Ordovician'` | 3 |
| `'Llandovery'` | 2 |
| `'Upper Ordovician'` | 1 |

**Never used (30):** `'Terrenuevian'`, `'Middle Ordovician'`, `'Wenlock'`, `'Ludlow'`, `'Přídolí'`, `'Upper Devonian'`, `'Lower Mississippian'`, `'Middle Mississippian'`, `'Upper Mississippian'`, `'Lower Pennsylvanian'`, `'Middle Pennsylvanian'`, `'Upper Pennsylvanian'`, `'Cisuralian'`, `'Guadalupian'`, `'Lopingian'`, `'Lower Triassic'`, `'Middle Triassic'`, `'Upper Triassic'`, `'Lower Jurassic'`, `'Middle Jurassic'`, `'Upper Jurassic'`, `'Lower Cretaceous'`, `'Upper Cretaceous'`, `'Paleocene'`, `'Eocene'`, `'Oligocene'`, `'Miocene'`, `'Pliocene'`, `'Pleistocene'`, `'Holocene'`

### `phylogeny#/$defs/specimens/propertyNames`

10 of 14 members used, 146 occurrences.

| value | count |
|---|---|
| `'holotype'` | 68 |
| `'paratypes'` | 48 |
| `'unknowntypes'` | 15 |
| `'plesiotypes'` | 6 |
| `'topotypes'` | 3 |
| `'lectotype'` | 2 |
| `'additional'` | 1 |
| `'syntype'` | 1 |
| `'hypotypes'` | 1 |
| `'syntypes'` | 1 |

**Never used (4):** `'allotype'`, `'neotype'`, `'kleptotypes'`, `'paralectotypes'`

### `phylogeny#/$defs/stage`

12 of 100 members used, 57 occurrences.

| value | count |
|---|---|
| `'Wuliuan'` | 15 |
| `'Cambrian Stage 4'` | 14 |
| `'Floian'` | 7 |
| `'Jiangshanian'` | 5 |
| `'Eifelian'` | 3 |
| `'Telychian'` | 3 |
| `'Emsian'` | 2 |
| `'Katian'` | 2 |
| `'Cambrian Stage 3'` | 2 |
| `'Drumian'` | 2 |
| `'Givetian'` | 1 |
| `'Tremadocian'` | 1 |

**Never used (88):** `'Fortunian'`, `'Cambrian Stage 2'`, `'Guzhangian'`, `'Paibian'`, `'Cambrian Stage 10'`, `'Dapingian'`, `'Darriwilian'`, `'Sandbian'`, `'Hirnantian'`, `'Rhuddanian'`, `'Aeronian'`, `'Sheinwoodian'`, `'Homerian'`, `'Gorstian'`, `'Ludfordian'`, `'Lochkovian'`, `'Pragian'`, `'Frasnian'`, `'Famennian'`, `'Touraisian'`, `'Viséan'`, `'Serpukhovian'`, `'Baskirian'`, `'Moscovian'`, `'Kasimovian'`, `'Gzhelian'`, `'Asselian'`, `'Sakmarian'`, `'Artinskian'`, `'Kungurian'`, `'Roadian'`, `'Wordian'`, `'Capitanian'`, `'Wuchiapingian'`, `'Changhsingian'`, `'Induan'`, `'Olenekian'`, `'Anisian'`, `'Ladinian'`, `'Carnian'`, `'Norian'`, `'Rhaetian'`, `'Hettangian'`, `'Sinemurian'`, `'Toarcian'`, `'Aalenian'`, `'Bajocian'`, `'Bathonian'`, `'Callovian'`, `'Oxfordian'`, `'Kimmeridgian'`, `'Tithonian'`, `'Berriasian'`, `'Valanginian'`, `'Hauterivian'`, `'Barremian'`, `'Aptian'`, `'Albian'`, `'Cenomanian'`, `'Turonian'`, `'Coniacian'`, `'Santonian'`, `'Campanian'`, `'Maastrichtian'`, `'Danian'`, `'Selanian'`, `'Thanetian'`, `'Ypresian'`, `'Lutetian'`, `'Bartonian'`, `'Priabonian'`, `'Rupelian'`, `'Chattian'`, `'Aquitanian'`, `'Burdigalian'`, `'Langhian'`, `'Serravallian'`, `'Tortonian'`, `'Messinian'`, `'Zanclean'`, `'Piacenzian'`, `'Gelasian'`, `'Calabrian'`, `'Chibanian'`, `'Upper Pleistocene'`, `'Greenlandian'`, `'Northgrippian'`, `'Meghalayan'`

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
| `phylogeny#/$defs/article/properties/complete/properties/history` | boolean/null | boolx14, nullx9 | - | - |
| `phylogeny#/$defs/article/properties/complete/properties/named` | boolean/null | boolx19, nullx3 | - | - |
| `phylogeny#/$defs/article/properties/complete/properties/open` | boolean/null | nullx13, boolx8 | - | - |
| `phylogeny#/$defs/article/properties/complete/properties/specimens/properties/all` | boolean/null | boolx12, nullx9 | - | - |
| `phylogeny#/$defs/article/properties/complete/properties/specimens/properties/basic` | boolean/null | boolx12, nullx9 | - | - |
| `phylogeny#/$defs/article/properties/number` | integer/string | intx140, strx9 | `Supplement`, `1/2`, `5–12`, `Adv. Pr.` | - |
| `phylogeny#/$defs/article/properties/pages/items` | integer/string | intx364, strx42 | `S637`, `S634`, `S631`, `S627` | - |
| `phylogeny#/$defs/article/properties/plates/items` | integer/string | intx11, strx8 | `II`, `I`, `IV`, `VII` | - |
| `phylogeny#/$defs/article/properties/series` | integer/string | intx2 | - | string |
| `phylogeny#/$defs/article/properties/volume` | integer/string | intx210, strx8 | `New Series`, `3: Echinoderms: Notes fo...`, `4th Series`, `III` | - |
| `phylogeny#/$defs/basicOccurrence/properties/possibleSpecimens/additionalProperties/items` | string/array | listx4, strx2 | `EE15329` | - |
| `phylogeny#/$defs/basicOccurrence/properties/specimens/additionalProperties/items/items` | string/integer | intx26, strx6 | `E63531`, `E63527`, `GM 3295c`, `GM 3295a` | - |
| `phylogeny#/$defs/basicOccurrence/properties/specimens/additionalProperties/items` | string/integer/array | listx16, strx15, intx4 | `EE15373`, `E63527`, `GM 9292`, `GM 8052` | - |
| `phylogeny#/$defs/basicOccurrence/properties/unit` | string/array | strx36, listx20 | `Craighead inlier`, `Mantou Formation`, `Wilberns Formation`, `Wulongqing Formation` | - |
| `phylogeny#/$defs/citationNumber` | integer/string | intx607, strx191, listx137 | `2D`, `1B`, `3N`, `3I` | - |
| `phylogeny#/$defs/person/properties/death` | integer/null | intx75, nullx1 | - | - |
| `phylogeny#/$defs/phylogeny/properties/characteristics/items/additionalProperties/additionalProperties` | integer/string | intx40 | - | string |
| `phylogeny#/$defs/specimens/additionalProperties/items` | string/array | strx513, listx4 | `PE 93415`, `YKLP 13553`, `NHMUK EE 1660`, `QMF59668` | - |
| `phylogeny#/$defs/taxon/properties/holotype/additionalProperties/items` | array/string/integer | intx10, strx3 | `EE15373`, `EE 1659`, `E23470` | array |
| `phylogeny#/$defs/taxon/properties/name` | string/null | strx2502, nullx202 | `Zoophytes`, `Zoophyta`, `Zoophites`, `Zoanthida` | - |
| `tree#/properties/diagnosis` | string/null | strx68, nullx1 | `Gogiids with a non-pored...`, `Theca large, cup-shaped ...`, `Theca small, cup-shaped ...`, `Gogiid eocrinoids with r...` | - |
| `tree#/properties/emended` | boolean/null | boolx49 | - | null |
| `tree#/properties/matrix/items` | integer/string | intx139, strx5 | `?` | - |

