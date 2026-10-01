# Material re-entry: 1973_sprinkle

Sprinkle 1973, *Morphology and Evolution of Blastozoan Echinoderms*
(Museum of Comparative Zoology, Special Publication), 283 pp., 43 pls.

This is the report of the material re-entry of 2026-09-30 (stage 3 of
the material refactor, roadmap D), written by the model that read the
pages. It is not a review under `BRIEF.md`: the tree's skeleton, flags
and synonymies were not checked and not changed. Every node's `pages`,
`material`, `illustrations`, `contexts` and `ranges` were entered from
page images of the scan; the nulls are statements that the paper prints
none (roadmap G11). A second reader checked the nine `material` nulls,
five locality contexts against Appendix 1, four species' entries and
Plates 4–6 and 21 against the pages; the rest stands on the first
reading until a person reads the page.

**Page mapping.** Printed page = PDF page − 6 in the archive.org scan.
Appendix 1 (Locality Index) is pp. 193–196; the plate descriptions run
from p. 198, each facing its plate.

**Counts.** 127 nodes with `pages`; 160 material entries; 31 file-level
contexts (the Appendix 1 codes some specimen is tied to) and 57
node-level ones; 278 illustrations; 43 ranges; 166 nulls (9 `material`,
75 `illustrations`, 41 `contexts` with 41 `ranges`).

**After the reading (2026-10-01).** Figures are of species, so the
derived coverage stopped counting higher taxa for `illustrations`, and
the 63 `illustrations: null` entered on genera and above were removed;
the table below records them as read. Runs that had been entered
number by number so that a plate could name one of them went back to
range pairs once `of` could name a number inside a run.

## Per node (tree order)

"p." is the page entered in `pages`; the account pages read run from that page to the next heading (all of pp. 54–188, every plate description pp. 198–282, Appendix 1 pp. 193–196, and the morphology text-figures pp. 4–48 were read). Counts are entries; "–" = key absent.

Null reasons, the same throughout: `material: null` = the account cites no specimen; `illustrations: null` = no plate description or text-figure caption names the taxon; `contexts: null` + `ranges: null` = the account prints no age, unit, locality or region for it.

Species whose provenance is wholly in file-level (Appendix 1) contexts carry no node `contexts` and no nulls (durhami, cf. wanneri, palmeri, hobbsi, Gogia sp. 1, resseri, ikecanensis, nevadensis, elongatus, hudsoni, fayi): their range paragraph names only locality codes, entered at file level and linked from the material.

| node | p. | material | illus. | node ctx | ranges | nulls |
|---|---|---|---|---|---|---|
| echinodermata | 56 | – | null | null | null | illustrations, contexts, ranges |
| · blastozoa | 56 | – | 2 | – | 1 |  |
| · · eocrinoidea | 58 | – | 2 | – | 1 |  |
| · · · imbricata | 60 | – | null | – | 1 | illustrations |
| · · · · lepidocystidae | 61 | – | 1 | – | 1 |  |
| · · · · · lepidocystis | 61 | – | null | 1 | – | illustrations |
| · · · · · · wanneri_foerste_1938 | 62 | 9 | 11 | 1 | – |  |
| · · · · · · cf. wanneri_foerste_1938 | 66 | 3 | 2 | – | – |  |
| · · · · · kinzercystis | 68 | – | null | 1 | – | illustrations |
| · · · · · · durhami_sprinkle_1973 | 70 | 3 | 12 | – | – |  |
| · · · eocrinoidea-unnamed-order-1_sprinkle_1973 | 76 | – | null | – | 1 | illustrations |
| · · · · eocrinidae | 76 | – | null | – | 1 | illustrations |
| · · · · · gogia | 76 | – | 1 | – | 1 |  |
| · · · · · · prolifica_walcott_1917 | 80 | 7 | 11 | 3 | – |  |
| · · · · · · longidactylus_walcott_1886 | 83 | 14 | 18 | 3 | – |  |
| · · · · · · multibrachiatus_kirk_1945 | 85 | 3 | 3 | 1 | – |  |
| · · · · · · spiralis_robison_1965 | 86 | 7 | 15 | 3 | – |  |
| · · · · · · granulosa_robison_1965 | 88 | 10 | 18 | 4 | – |  |
| · · · · · · palmeri_sprinkle_1973 | 90 | 4 | 21 | – | – |  |
| · · · · · · guntheri_sprinkle_1973 | 93 | 6 | 10 | 2 | – |  |
| · · · · · · kitchnerensis_sprinkle_1973 | 96 | 7 | 20 | 1 | – |  |
| · · · · · · hobbsi_sprinkle_1973 | 100 | 4 | 10 | – | – |  |
| · · · · · · radiata_sprinkle_1973 | 102 | 3 | 5 | 2 | – |  |
| · · · · · · gogia-sp_robison_1965 | 104 | 2 | 2 | – | – |  |
| · · · · · · gogia-sp-2_sprinkle_1973 | 104 | 1 | 1 | 1 | – |  |
| · · · · · acanthocystites | 105 | – | null | 1 | – | illustrations |
| · · · · · · briareus_barrande_1887 | 105 | null | null | null | null | material, illustrations, contexts, ranges |
| · · · · · akadocrinus | 105 | – | 1 | 1 | – |  |
| · · · · · · jani_prokop_1962 | 106 | 4 | 3 | 1 | – |  |
| · · · · lichenoididae | 108 | – | null | null | null | illustrations, contexts, ranges |
| · · · · · lichenoides | 109 | – | null | – | 1 | illustrations |
| · · · · · · priscus_barrande_1846 | 109 | 3 | 6 | 1 | – |  |
| · · · · rhopalocystidae | 110 | – | null | – | 1 | illustrations |
| · · · · · rhopalocystis | 110 | – | null | – | 1 | illustrations |
| · · · · · · destombesi_ubaghs_1963 | 110 | 1 | null | null | null | illustrations, contexts, ranges |
| · · · eocrinoidea-unnamed-order-2_sprinkle_1973 | 111 | – | null | – | 1 | illustrations |
| · · · · eocrinoidea-indeterminate-family-1_sprinkle_1973 | 112 | – | null | null | null | illustrations, contexts, ranges |
| · · · · · pareocrinus | 112 | – | null | – | 1 | illustrations |
| · · · · · · ljubzovi_yakovlev_1956 | 112 | null | null | null | null | material, illustrations, contexts, ranges |
| · · · · · eustypocystis | 112 | – | 1 | 1 | – |  |
| · · · · · · minor_sprinkle_1973 | 113 | 8 | 12 | 2 | – |  |
| · · · · · nolichuckia | 115 | – | null | 1 | – | illustrations |
| · · · · · · casteri_sprinkle_1973 | 116 | 6 | 6 | 2 | 1 |  |
| · · · · ascocystitidae | 118 | – | null | – | 1 | illustrations |
| · · · · · ascocystites | 118 | – | null | – | 1 | illustrations |
| · · · · · · drabowensis_barrande_1887 | 118 | 1 | 1 | null | null | contexts, ranges |
| · · · · macrocystellidae | 122 | – | null | – | 1 | illustrations |
| · · · · · macrocystella | 122 | – | null | null | null | illustrations, contexts, ranges |
| · · · · · · mariae_callaway_1877 | 122 | null | null | null | null | material, illustrations, contexts, ranges |
| · · · · eocrinoidea-indeterminate-family-2_sprinkle_1973 | 121 | – | null | null | null | illustrations, contexts, ranges |
| · · · · · cambrocrinus | 121 | – | null | 1 | – | illustrations |
| · · · · · · regularis_orłowski_1968 | 121 | null | null | null | null | material, illustrations, contexts, ranges |
| · · · · · eocystites | 121 | – | null | 1 | – | illustrations |
| · · · · · · primaevus_billings_1868 | 121 | 1 | null | null | null | illustrations, contexts, ranges |
| · · · eocrinoidea-indeterminate-order-1_sprinkle_1973 | 123 | – | null | null | null | illustrations, contexts, ranges |
| · · · · trachelocrinidae | 123 | – | null | – | 1 | illustrations |
| · · · · · trachelocrinus | 123 | – | null | 1 | – | illustrations |
| · · · · · · resseri_ulrich_1929 | 124 | 2 | 1 | – | – |  |
| · · · eocrinoidea-indeterminate-order-2_sprinkle_1973 | 126 | – | null | null | null | illustrations, contexts, ranges |
| · · · · cryptocrinitidae | 126 | – | null | – | 1 | illustrations |
| · · · · · cryptocrinites | 126 | – | null | null | null | illustrations, contexts, ranges |
| · · · · · · laevis_pander_1830 | 126 | 1 | 1 | 1 | – |  |
| · · · · eocrinoidea-indeterminate-family-3_sprinkle_1973 | 127 | – | null | null | null | illustrations, contexts, ranges |
| · · · · · bockia_hecker_1938 | 127 | – | null | – | 1 | illustrations |
| · · · · · · neglecta_hecker_1940 | 127 | null | null | null | null | material, illustrations, contexts, ranges |
| · · · eocrinoidea-indeterminate-order-3_sprinkle_1973 | 127 | – | null | null | null | illustrations, contexts, ranges |
| · · · · lingulocystidae | 127 | – | null | – | 1 | illustrations |
| · · · · · lingulocystis | 127 | – | null | null | null | illustrations, contexts, ranges |
| · · · · · · elongata_thoral_1935 | 127 | null | null | null | null | material, illustrations, contexts, ranges |
| · · · · eocrinoidea-indeterminate-family-4_sprinkle_1973 | 127 | – | null | null | null | illustrations, contexts, ranges |
| · · · · · cardiocystites | 127 | – | null | – | 1 | illustrations |
| · · · · · · bohemicus_barrande_1887_cardiocystites | 129 | 1 | 2 | 1 | – |  |
| · · · · rhipidocystidae | 130 | – | 2 | – | 1 |  |
| · · · · · rhipidocystis | 130 | – | null | – | 1 | illustrations |
| · · · · · · gigas_jaekel_1901 | 130 | null | null | null | null | material, illustrations, contexts, ranges |
| · · · · · batherocystis | 130 | – | null | – | 1 | illustrations |
| · · · · · · appressa_bassler_1950 | 130 | null | null | null | null | material, illustrations, contexts, ranges |
| · · · · · petalocystites | 131 | – | null | – | 1 | illustrations |
| · · · · · · ikecanensis_sprinkle_1973 | 132 | 3 | 5 | – | – |  |
| · · blastozoa-indeterminate-class_sprinkle_1973 | 136 | – | null | null | null | illustrations, contexts, ranges |
| · · · cigaria | 136 | – | null | 1 | – | illustrations |
| · · · · dusli_barrande_1887 | 136 | 1 | 1 | 1 | – |  |
| · · · archaeocystites | 138 | – | null | null | null | illustrations, contexts, ranges |
| · · · · medusa_barrande_1887 | 138 | 2 | 2 | 1 | – |  |
| · · · palaeocystites | 139 | – | null | null | null | illustrations, contexts, ranges |
| · · · · dawsoni_billings_1858 | 139 | 1 | null | null | null | illustrations, contexts, ranges |
| · · · lysocystites | 139 | – | – | 2 | – |  |
| · · · · nodosus_hall_1864 | 139 | null | null | null | null | material, illustrations, contexts, ranges |
| · · parablastoidea | 142 | – | 3 | – | 1 |  |
| · · · blastocystidae | 144 | – | null | – | 1 | illustrations |
| · · · · blastoidocrinus | 144 | – | null | – | 1 | illustrations |
| · · · · · charcariaedens_billings_1859 | 147 | 5 | 6 | 6 | – |  |
| · · · · · rossi_sprinkle_1973 | 150 | 10 | 9 | 2 | – |  |
| · · · · · nevadensis_sprinkle_1973 | 152 | 5 | 4 | – | – |  |
| · · · · · elongatus_sprinkle_1973 | 154 | 3 | 3 | – | – |  |
| · · · · blastocystis | 155 | – | null | 1 | – | illustrations |
| · · · · · rossica_jaekel_1918 | 155 | 1 | 1 | null | null | contexts, ranges |
| · · · meristoschismatidae | 156 | – | null | – | 1 | illustrations |
| · · · · meristoschisma | 156 | – | null | 1 | – | illustrations |
| · · · · · hudsoni_sprinkle_1973 | 158 | 8 | 17 | – | – |  |
| · · · · · fayi_sprinkle_1973 | 168 | 5 | 4 | – | – |  |
| · · rhombifera-class | 170 | – | 2 | – | 1 |  |
| · · blastoidea | 171 | – | 3 | – | 2 |  |
| · · diploporita-class | 186 | – | 1 | – | 1 |  |
| · crinozoa | 174 | – | 1 | – | 1 |  |
| · · crinoidea | 175 | – | 3 | – | 2 |  |
| · · · inadunata | 177 | – | null | null | null | illustrations, contexts, ranges |
| · · · camerata | 177 | – | null | null | null | illustrations, contexts, ranges |
| · · · flexibilia | 177 | – | null | null | null | illustrations, contexts, ranges |
| · · · articulata | 177 | – | null | null | null | illustrations, contexts, ranges |
| · · · crinoidea-indeterminate-subclass_sprinkle_1973 | 177 | – | null | null | null | illustrations, contexts, ranges |
| · · · · crinoidea-indeterminate-order_sprinkle_1973 | 177 | – | null | null | null | illustrations, contexts, ranges |
| · · · · · echmatocrinidae | 177 | – | null | – | 1 | illustrations |
| · · · · · · echmatocrinus | 177 | – | 1 | 1 | – |  |
| · · · · · · · brachiatus_sprinkle_1973 | 180 | 5 | 10 | 2 | – |  |
| · · paracrinoidea | 184 | – | – | – | 1 |  |
| · · · springerocystidae | 138 | – | null | 1 | – | illustrations |
| · · · · springerocystis | 138 | – | null | null | null | illustrations, contexts, ranges |
| · · · columbocystis | 138 | – | – | null | null | contexts, ranges |
| · · · foerstecystis | 138 | – | null | null | null | illustrations, contexts, ranges |
| · · · ulrichocystis | 186 | – | null | null | null | illustrations, contexts, ranges |
| · · · palaeocystites | 186 | – | null | null | null | illustrations, contexts, ranges |
| · · · allocystites | 186 | – | null | – | 1 | illustrations |
| · · diploporita-class | 186 | – | 1 | – | 1 |  |
| · echinozoa | 3 | – | null | null | null | illustrations, contexts, ranges |
| · · edrioblastoidea | 187 | – | null | – | 1 | illustrations |
| · · · astrocystites | 187 | – | null | – | 2 | illustrations |

Pages for taxa with no heading of their own (the page where the paper first places or lists them):
- Type species with no species heading take the page of their genus's "Type species" line: briareus 105, ljubzovi 112, mariae 122, regularis 121, primaevus 121, destombesi 110, laevis 126, neglecta 127, elongata 127, gigas 130, appressa 130, dusli 136, medusa 138, dawsoni 139, nodosus 139.
- The order/family "indeterminate" bins take the page of their "Order/Family INDETERMINATE" heading; unnamed orders #1 (76) and #2 (111) their headings; blastozoa-indeterminate-class 136 ("Forms Provisionally or Definitely Removed from the Eocrinoids").
- Inadunata, Camerata, Flexibilia, Articulata: 177 (listed in the Crinoidea discussion). Springerocystis, Columbocystis, Foerstecystis: 138 (Springerocystidae discussion). Ulrichocystis, Allocystites and the paracrinoid placement of Palaeocystites: 186 (listed in the Paracrinoidea discussion). Echinozoa: 3 (the four-subphylum classification in the Introduction; Edrioblastoidea is placed in it on p. 188). Astrocystites: 187.
- The second Diploporita node (under crinozoa) carries the same page, range and Text-fig. 11B as the first (both are the one account on p. 186).

## Taxa, figures and specimens in the paper with no node

- Lysocystites sculptus (Miller): the material and all the figures under Lysocystites are of this species: Springer plesiotypes S3163a–d (p. 139, Pl. 33 figs. 1–8, Laurel Limestone, Indiana) and Text-figs. 34–36 (pp. 140–142). The tree's only species is nodosus (the type species), for which the paper cites nothing; I entered `material: null` there and dropped the migrated S3163 entry. `lysocystites` has no `illustrations` key (not null), since the figures are of the genus's unnoded species.
- Columbocystis typica, holotype USNM 93407: Text-fig. 33 (p. 138). Not entered; `columbocystis` and `paracrinoidea` have no `illustrations` key (the caption calls Columbocystis "true paracrinoids").
- Malocystites murchisoni, plesiotypes MCZ 718a–c, Ville de Laval near Montreal: Text-fig. 46 (p. 186).
- Cystidea nugatula Barrande (Class, Order, and Family INDETERMINATE, p. 183): latex cast S 31, Caster Coll., Pl. 33 fig. 11, D4 middle Ordovician.
- Eocrinoid(?) plates from the Poleta Formation (p. 107): MCZ 667a–n, locality WP-1A., Pl. 25 figs. 9–22.
- Burgess Shale "arms" (p. 125): USNM 165428–31 and GSC 25963, Pl. 24 figs. 8–16, USNM loc. 35k.
- Antelope Valley rhipidocystid plates (p. 134): MCZ 671–675 (IK-2.) and USNM 165412–3 (USGS D719i CO), Pl. 32 figs. 4–18. Their plate locator is entered on `rhipidocystidae` with no `of` (the caption says "possibly belonging to Petalocystites or some other rhipidocystid genus"); the specimens are not entered.
- "Archaeocyathids" from Poland (Family INDETERMINATE, p. 111): Palmer casts 770, 771, 773, 774.
- Possible Ordovician blastoid(?) plate (Order Fissiculata(?), p. 173): USNM 165409, USGS D1634 CO, Text-fig. 43.
- Rhombiferans in Text-fig. 5E (Cheirocrinus anatiformis) and 5F (Caryocrinites ornatus); blastoids in 5H (unidentified globular blastoid), 5I (Costaloblastus sappingtonensis), Text-fig. 9 (Globoblastus) and 19 (Hyperoblastus alveata UMMP 37808, Pentremites conoideus UMMP M-58); Hybocystites USNM S2048, Text-fig. 8; Regnellicystis typicalis holotype USNM 113308 (p. 187, not figured).
- Charts not entered as illustrations: Text-figs. 1 (class ranges, p. 4), 20 (blastozoan class diversity, p. 54), 24 (Gogia species ranges, p. 75), 25 (Gogia occurrence map, p. 77).
- Astrocystites(?) specimen from the Curdsville Limestone of Kentucky, Springer Collection USNM (p. 188), no number, queried genus: not entered (a genus node cannot hold material).

## Places the fields could not say what is printed

- Lepidocystis wanneri plesiotypes: "plesiotypes MCZ 588–590 from localities SH-1. and 2." (p. 66). Split by the plate captions into MCZ 588A/B and 589 (SH-1.) and 590A/B (SH-2.), each with `catalogNumbersAsPrinted: MCZ 588–590`. MCZ 591, 592, 593 are printed without a role ("as well as MCZ 591 (ten additional specimens from SH-1.)"); the migrated `paratype` role was dropped.
- Lepidocystis wanneri types: Walcott's locality 8q ("Kinzers Formation, Lightners Hill near the contact with the Triassic, 2.0 mi. NW of York, Pa.") is a node context with the "not satisfactorily pinpointed" remark in `notes`.
- Lepidocystis cf. wanneri, p. 68: MCZ 628 and PE-199 have no role word in the text; the text says "his figured specimen" for both, entered as `role: figured`. The Pl. 3 caption numbers the casts differently: "MCZ 628 (latex casts A1 and B1)", and "PE 199 and 199A (latex casts MCZ 629-B1 and A0)"; these cast-copy labels are in illustration `notes` only.
- Pl. 1, fig. 7 prints "USNM 09773-C2" (for 90773-C2); in `notes`.
- Gogia prolifica: "six to eight additional unnumbered specimens in the USNM collection" and "an unnumbered slab of three large specimens from Mount Robson in the USNM collection" are `label` entries; MCZ 668 "(24 additional specimens)" is `count: 24` with no context (the text gives none).
- Gogia longidactylus (p. 85): "Lectotype USNM 15315, syntypes USNM 15315" — the same number printed for both roles; entered as printed (two entries). Pl. 10 says "lectotype selected by Robison". The Studied paragraph prints "pleisotypes" [sic]. The localities PI-1 to 7 come from the Pl. 9–10 captions (the text gives the range only); PI-3 and PI-5 are named in the range but no specimen is captioned from them, so they are not entered. "Also found in the Highland Range" is a node context with no specimen.
- Gogia longidactylus cast conflict: text "a single specimen loaned from B. L. Stinchcomb (E-3340; cast MCZ 669)"; Pl. 9 fig. 8 caption "specimen in coll. of B. L. Stinchcomb (cast MCZ 695)". Entered E-3340 with `holder: B. L. Stinchcomb`, MCZ 669 as `preparation: cast, castOf: E-3340` (the text's words; "latex" is not printed there), and MCZ 695 within the MCZ 691–705 run with no context; Pl. 9 fig. 8 is `of: E-3340` with the caption quoted in `notes`. Pl. 10 fig. 11 "plesiotype GCM 2641 (latex cast MCZ 706) (McKee Coll.)" — MCZ 706 is also a Gogia spiralis plesiotype (Pl. 12); the cast number is in `notes` only. Pl. 9 fig. 12 "plesiotype USNM 256500A (Fawcett Coll.)" is not in the Studied paragraph; entered as its own entry (context "Pioche District, SE Nevada" from the caption).
- Gogia multibrachiatus: "additional specimen (topotype?) unfigured by Kirk, USNM 165425" (p. 86); Pl. 11 calls it "plesiotype". Entered `role: plesiotype` (the caption's word) with the text's "(topotype?)" in `notes`. Locality printed "Walcott locality 74e" (text) and "USNM locality 74e" (plate): both in `localityNumbers`.
- Gogia spiralis: "Holotype and paratypes (16 specimens), USNM 139550–65" — one run for two roles; entered as one entry with no role and the words in `notes`. USNM 165421–22 "figured plesiotypes from the Walcott Collection" → `repository: usnm-walcott`. USNM 111716 (Pl. 13 fig. 8, Walcott locality 4) is not in the Studied paragraph; entered from the caption. "Marjum Pass" and the Marjum Formation are in the range paragraph; Marjum Pass is a node context with no specimen.
- Gogia granulosa: "PE-214 from Derstler Coll. (latex cast MCZ 732)" (Pl. 14 fig. 4); the Studied paragraph lists MCZ 732–738 as plesiotypes with no cast word. MCZ 732 entered with `preparation: latex cast, castOf: PE-214`, PE-214 with `holder: Derstler Coll.`. USNM 165435 and UU 1040p (Pl. 15 fig. 1 "locality USNM 55e and exposures in Cataract Canyon") have no context, since the caption does not say which is which. The range says "USGS 55e", the plates "USNM locality 55e": both in `localityNumbers`.
- Gogia palmeri: holotype printed "USNM 165418A and B" (p. 93), entered with `parts`. Pl. 16 figs. 1–2 show the holotype and paratype USNM 165419 on one slab; figs. 3–4 are brachioles "from Fig. 2" with no specimen named.
- Gogia guntheri: "several additional unstudied specimens are filed under numbers UU 1010, 1011, 1040, 1041, and MCZ 742" — entered as one entry. Lloyd Gunther as collector of the holotype comes from Text-fig. 26. "Miners Hollow" in the range paragraph is a node context with no specimen.
- Gogia kitchnerensis: "paratypes GSC 25935–25961 (17 specimens)" — the run is 27 numbers; `notes: (17 specimens)` as printed. GSC 25954 is in this run and is also a Gogia(?) radiata paratype (Pl. 24 figs. 5–6, p. 102). GSC 25960 is "figured specimen" (a fecal or regurgitation wad) on Pl. 21. "additional specimens collected in 1968 (GSC collection)" → `label` with `repository: gsc`; "four specimens at the University of Wisconsin (Laudon Collection)" → `count: 4` (no number; Laudon as collector from p. 96); "six specimens in GSC collection 10088c–h" → range pair with "six specimens" in `notes` (a count would contradict the six numbers).
- Gogia hobbsi: "unfigured paratypes MCZ 642 (24 specimens); and 62 additional specimens under number MCZ 643". MCZ 643 is also printed for Blastoidocrinus(?) nevadensis ("additional material, MCZ 643, approximately 20–30 ... deltoids", p. 154); both entered as printed. USGS locality 5462 is equated with CL-1. (p. 101) and is in its `localityNumbers`.
- Gogia(?) radiata: USNM 165403–4 "may also belong to this taxon" — entered without role (the migrated `paratype` was wrong). The holotype is from 35k/10 (Pl. 24 fig. 1), the paratypes from 35k (caption: "Burgess Shale Quarry (Walcott locality 35k) and accessory quarry (Walcott locality 35k/10) (Fig. 1)").
- Gogia sp. 1: no Studied-specimens paragraph; USNM 165411 (collected by A. R. Palmer, USGS 4148 CO = FC-1.) and the silicified plates MCZ 666a–c (Pl. 25 figs. 2–7) entered. The migrated `role: holotype` on USNM 165411 was not printed and is gone. Gogia sp. 2: USNM 63712, likewise no role.
- Akadocrinus jani: "Two other latex casts (500–501) were borrowed from A. R. Palmer" — no prefix; entered `[['500', '501']]` with `holder: A. R. Palmer`; this is the one new loader warning (unresolvable prefix). E40 is printed "E40 (two counterparts)" in the text and "E 40A and B" in the Pl. 26 caption; entered as [E 40A, E 40B] with `parts`. E62 and E41 are printed without a space, as entered.
- Lichenoides priscus: Pl. 27 figures E 13 and BC 141B, which are not in the Studied list; entered from the caption. Jince Beds "upper Middle Cambrian, several localities in Czechoslovakia".
- Rhopalocystis destombesi: "I examined latex casts from Ubaghs of three large slabs of specimens" — entered `count: 3, preparation: latex cast` with the words in `notes`.
- Ascocystites drabowensis: "cast KR–2" (text) / "KR 2" (Text-fig. 30): entered `KR-2` with `repository: u-cincinnati-caster` (the prefix is not in the registry).
- Eocystites primaevus: "the apparent type specimens that are currently on loan from Cornell University to the University of Cincinnati" — a `label`, no role (the paper says "apparent type specimens").
- Eustypocystis minor: "USNM localities 834 (= SC-4A?) and 835 (= SC-4.?)" — queried equivalences, so separate node contexts `usgs-834`, `usgs-835` with the equivalence in `notes`. USNM 165423–4 "(three specimens)": the caption splits 165423a–b; entered [USNM 165423a, USNM 165423b] and [USNM 165424]. "Three specimens ... collected by Thomas Nolan, Joshua Bridge, and G. Arthur Cooper" (p. 113) are not identified with numbers, so not entered as `collectedBy`.
- Nolichuckia casteri: holotype "apparently collected by P. E. Raymond ... about 1925" — in `notes` (the "apparently" is not a field). "Nolichuckia may also occur in the Upper Cambrian of northwestern Georgia and northern Alabama" → a species `ranges` entry with both regions tentative. TH-1. (named in the range paragraph) has no specimen, so no file context.
- Trachelocrinus resseri: RP-1. = Walcott locality 37o (printed "Walcott locality 37o, my locality RP-1."), both in RP-1's `localityNumbers`. SD-1. and SA-1. (Trachelocrinus(?) plates and columnals) have no specimen number; not entered. MCZ 624–626 "additional plates and columnals" have no stated locality.
- Petalocystites ikecanensis: MCZ 649 has no context; by elimination it is "the fourth, poorly preserved specimen ... found ... (IK-3.)" (p. 132), but the paper does not tie the number to it.
- Cardiocystites bohemicus: unit "D4" (subscript 4) entered as `D₄`.
- Cigaria dusli: E 35 is a latex cast of the "only known slab of type specimens" with two specimens; no role on the cast.
- Archaeocystites medusa: E 32 "(holotype)" and E 33 are latex casts; only E 33 has a context (Pl. 33: "middle Ordovician, Czechoslovakia").
- Palaeocystites dawsoni: "the two syntypes of the type species of this genus (GSC 1021a–b)" — no locality printed.
- Blastoidocrinus carchariaedens: the Studied paragraph puts GSC 1016, UC 26022 and the unnumbered GSC specimen "all from near Montreal"; Pl. 35 gives three different units (Chazy Group, Montreal; Chazy Formation, Village Belanger; Laval Formation (Chazy), Ile Jésus), and the range paragraph says Aylmer Formation for the Montreal region. Each specimen is linked to its caption's context; the range paragraph's two contexts are on the node as well. "plates NYSM 7390–7450": the 14 plates figured on Pl. 34 are entered individually with `catalogNumbersAsPrinted: NYSM 7390–7450` and `listComplete: false` (the rest of the run is not itemised), and no role (it is unclear whether "figured plesiotypes" governs them).
- Blastoidocrinus(?) rossi: "USNM 165379–91" are linked to no context (Pl. 36 spreads figs. 23–36 over LO-1., D190d and D190e without saying which number is which). MU-1. is named in the range paragraph but no specimen comes from it; not entered. "The remainder of this acid residue material is deposited in USGS collections D190d CO and D190e CO (Denver), and MCZ 612": two labels and MCZ 612.
- Blastoidocrinus(?) nevadensis: paratypes printed "MCZ 614 (deltoids D1–6, D8–9)" (text) and "MCZ 614-D1-6, 8-9" (caption); entered as the caption's suffixed numbers. Caption heading says Figures 1–18, the line says "Figs. 10-19".
- Blastoidocrinus(??) elongatus: text "figured paratype MCZ 611a", caption "paratype MCZ 611". "MCZ 611b–c (15 specimens)" → `count: 15`.
- Blastocystis rossica: the only specimen ("not available for study") is a `label`; Text-fig. 38 reproduces Schmidt's 1874 figures, `depicts: drawing` with the source in `notes`.
- Meristoschisma hudsoni: "figured plate paratypes MCZ 596–601"; entered by the caption's lots and suffixes (MCZ 599-D1–10, 600-R1–10, 601A–C) and localities. The range paragraph names CS-2., GV-1., HO-1A., LB-1. and SG-1. too; no specimen is tied to them, so they are not entered. GV-1. is not in Appendix 1 (Appendix has GR-1., which lists M. hudsoni plates). MCZ 645 "nearly 300 additional separate plates ... primarily from locality RC-9." — `notes`, no context. Text-fig. 18 (growth bands) names no specimen in its caption.
- Meristoschisma fayi: "MCZ 602–RO–5 (radials)" is entered as printed (with hyphens); the plates print "MCZ 602-R3" and "MCZ 602-R1-4", which do not match "RO–5" (R0? R1–5?). The Pl. 40–41 captions spread the lot over MC-3., DT-3. and DT-3A.; only the holotype 602-D1 is unambiguous (DT-3.). MC-3., SL-1., DT-3A. are therefore not entered as contexts.
- Echmatocrinus brachiatus: holotype "GSC 25962" (text) / "GSC 25962B and A (two counterparts)" (Pl. 42) → [GSC 25962A, GSC 25962B] with `parts`. Paratypes USNM 165405 and 165406 are A/B in the captions. USNM 165427 is "one poorly preserved possible additional specimen" (text) and "paratype(?)" (Pl. 43): no role. Localities printed "USNM loc. 35k" / "Walcott's Quarry".
- Blastoidea and Crinoidea: the queried "Middle Ordovician(?)" / "Middle Cambrian(?)" have no tentative flag on a time field; each is a separate range with the "(?)" in `notes`. Ranges like "early Cambrian to late Permian" or "middle Cambrian to the Recent" use local series ranges with `asPrinted`.
- Blastoidocrinus genus range "(Chazian and Whiterockian)": two stages that are not a range; kept in `asPrinted` only.
- Lepidocystis genus and Kinzercystis genus contexts: the genus diagnoses print a unit and region; node contexts with no material link (likewise Gogia's Highland Range, Marjum Pass, Miners Hollow, the range-paragraph contexts of carchariaedens, and the genus contexts of Acanthocystites, Akadocrinus, Cambrocrinus, Eocystites, Eustypocystis, Nolichuckia, Trachelocrinus, Blastocystis, Meristoschisma, Echmatocrinus, Springerocystidae, Lysocystites).
- Appendix 1 intro: "localities ... at which I personally collected" — a collector for every code; not entered as `collectedBy` on each context. Appendix remarks entered in `notes`: AS-1 "Top 100 ft. of the Wheeler Shale", CL-1 "Basal 6 ft. of red shaly siltstone ...", FC-1 "About 100 ft. below base of middle limestone member", RP-1 "(locality is in NW Wyo.)", SC-1 "Top of the Secret Canyon Fm.". HL-1's header says "SW Va." and the body "SE Va."; entered as the body prints. PI-2/4/6/7, AS-2, SC-3/4/4A, SH-2, DT-3A, RC-8/9, IK-3 say "same as above": I filled the unit, age and outer location from the entry they refer to.

## Uncertain readings (to check)

- p. 83, prolifica Studied paragraph: "syntype USNM 6431" — entered as printed; likely a misprint (for 64351?).
- p. 151: "Deltoid plate USNM 165478 is here designated as holotype" vs "Holotype USNM 165378" (p. 152 and Pl. 36); entered 165378.
- Pl. 3: "latex casts MCZ 629-B1 and A0" — the "A0" read at 400 dpi; could be "A6" or "AO".
- Appendix AS-1: the township "T. 17 S" is damaged in print; second digit read as 7 (AS-2 prints T. 17 S).
- Pl. 29 heading "Plate 116" (for "Page 116").
- MCZ 602–RO–5: "O" or "0"?
- p. 104 Gogia sp. 1 and Pl. 25: "USGS locality 4148 CO" read clearly; FC-1. equated in the text ("USGS locality 4148 CO (my locality FC-1.)").

## Suspected errors in the existing tree (not touched)

- Root: `echinodermata` has `auth: [Klein], year: 1734`; the paper's heading is "Phylum ECHINODERMATA Bruguière, 1789" (p. 56).
- `charcariaedens_billings_1859`: the paper spells it carchariaedens throughout.
- `granulosa_robison_1965` synonym `auth: [Ressler], year: 1939`: the paper prints "Resser, 1939: 3–4" (p. 88).
- `longidactylus_walcott_1886` synonym `eocrinus`, `auth: [jaekel]`, `year: 1980` — Jaekel's work cannot be 1980 (probably 1918).
- `bockia_hecker_1938` / `neglecta_hecker_1940`: the paper prints "Bockia neglecta Hecker, 1938" as type species (p. 127).
- `palaeocystites` and `dawsoni_billings_1858` notes "Year incorrectly given as 1859": the paper prints 1859 for both.
- `lysocystites` holds only `nodosus_hall_1864`; the paper's material and figures are of L. sculptus (see above).
- Two `diploporita-class` nodes and two `palaeocystites` nodes (one under blastozoa-indeterminate-class, one under paracrinoidea) — same account each; entered on both.
- `kitchnerensis_sprinkle_1973` has `new: true` after `synonyms` (key order), left as is.
- The `cigaria` note says the proper spelling is "Cigara"; the paper prints Cigaria.

## Loader warnings remaining for this file

- `catalog number "500" has no resolvable repository prefix` and the same for "501" (Akadocrinus jani, Palmer's latex casts, printed without prefix). In `tests/expected-warnings.txt`.
- `Unregistered author "Klein" ...` (pre-existing).
- `check_draft.py` also lists author `kirk` without a record (pre-existing, in the multibrachiatus synonym).

## Registry entries added

None. No UMMP number was entered (the UMMP specimens on Text-fig. 19 belong to taxa with no node).
