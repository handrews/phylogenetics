# Review: Sumrall, Heredia, Rodríguez & Mestre 2013

Source text: `2013-00-00-p.txt`. Tree: `data/trees/2013_sumrall_heredia_rodríguez.c.m_mestre.yaml` (65 lines).

**Page mapping.** The article runs pp. 763–776 (masthead, p. 763: "Acta Palaeontol. Pol. 58 (4): 763–776, 2013"). The running head/page number recurs at the bottom of every subsequent page, one per PDF index in order, so **printed page = PDF page index + 763** (index 0 = 763, index 1 = 764, … index 13 = 776). Systematic Paleontology runs from p. 773 (index 10) into p. 774 (index 11).

## Gold-slice: rhenopyrgids vs. edrioblastoids (s.l.) and vs. Pyrgocystidae

Ranks exactly as printed.

- Abstract (p. 763): "Phylogenetic analysis shows that rhenopyrgids are more closely related to edrioasterid edrioasteroids such as edrioblastoids and cyathocystids than to pyrgocystid isorophids."
- p. 764: "Smith and Jell (1990) allied rhenopyrgids with edrioblastoids whereas Guensburg and Sprinkle (1994) allied them to cyathocystids." … "New material described here and a reinvestigation of *Pyrgocystis grayae* and *Rhenopyrgus whitei* allows for a new interpretation of morphologies that confirm the distant relation suggested by Holloway and Jell (1983), Smith (1990) and Guensburg and Sprinkle (1994)" [i.e., the distant relation of rhenopyrgids **to pyrgocystids**].
- p. 765: "Two main clades were recovered—an edrioasterid clade including cyathocystids, rhenopyrgids, and edrioblastoids, and an isorophid clade including pyrgocystids." Bootstrap/decay: 98–99%/4–5 steps for the edrioasterid-vs-isorophid split; 91%/2 steps for the (rhenopyrgid+cyathocystid+edrioblastoid) clade specifically. "Guensburg and Sprinkle (1994) suggested that rhynopyrgids [sic] were closer to cyathocystids than to edrioblastoids, however, their matrix included no character support for this conclusion." "Although the exact ordering of taxa within Edrioasterida cannot be determined from this analysis... these taxa are here concluded to form a clade." "These groups differ from one another primarily in the form of the pedunculate zone — organized flexible stalk in rhenopyrgids, fused cup in cyathocystids, and an elongate stem in edrioblastoids."
- Systematic Paleontology, p. 773, under **Order Edrioasterida Bell, 1976**: "Edrioasterida sensu Guensburg and Sprinkle (1994) is greatly expanded compared to the original meaning found in Bell (1976). Based on a new phylogenetic analysis we follow Guensburg and Sprinkle (1994) by including Rhenopyrgidae Holloway and Jell, 1983 in Edrioasterida Bell, 1976 along with Cyathocystidae Bather, 1899 and Astrocystitidae Bassler, 1935 (edrioblastoids)."
- p. 773, under **Family Rhenopyrgidae Holloway and Jell, 1983**, printed rank hierarchy is **Class Edrioasteroidea Billings, 1858 > Order Edrioasterida Bell, 1976 > Suborder Edrioblastoidina Fay, 1962 > Family Rhenopyrgidae**: "The phylogenetic analysis presented here, as well as that presented by Guensburg and Sprinkle (1994), did not uniquely recover rhenopyrgids and cyathocystids as sister taxa. For this reason, we do not include them within Cyathocystidae Bather, 1899, but leave them assigned at family level within Edrioblastoidina Fay, 1962."

**Pyrgocystidae**: the formal family name "Pyrgocystidae" never appears as a printed rank-heading anywhere in this paper (confirmed by full-text search) — only the informal, uncapitalized "pyrgocystid(s)" is used throughout, applied to *Pyrgocystis* and *Argodiscus* as an isorophid clade sister to (not nested with) the edrioasterid clade containing rhenopyrgids. The paper's own systematic hierarchy places rhenopyrgids in Edrioblastoidina within Edrioasterida, with Pyrgocystidae never mentioned in that hierarchy at all.

## 1. Coverage

| Item | Status | Example |
|---|---|---|
| Classification skeleton | Partly | Class–Order–Suborder–Family–Genus–species for the Rhenopyrgus branch captured; the paper's parallel placement of Cyathocystidae Bather, 1899 under Edrioasterida (p. 773) is not represented as a sibling node in the tree |
| New taxa | All | `piojoensis_..._2013` flagged `new: true` |
| Type species | All | `coronaeformis_rievers_1961` flagged `type: true` |
| Synonymy lists | Partly | Only the type-species original combination is captured (see §3); no synonymy list is printed for the genus itself |
| Material | None | Holotype PIL 14656–H, paratypes PIL 14174–14872 (p. 774–775) not in tree |
| Occurrences | None | Type locality/horizon (Los Espejos Fm., lower Ludlow, Argentina, p. 774) not in tree |
| Illustrations | None | Figs. 6, 8 (holotype, paratypes) not referenced |
| Diagnoses | None | Family and genus "Diagnosis (emended)" text (p. 773) not stored; only the `emended: true` flag is present |
| Phylogeny | Partly | Both cladogram topologies and their methodology captured; character matrix (Table 1), tree statistics (CI/RI/RC, bootstrap, decay index) not captured |

If nothing beyond the skeleton and a few flags were captured, this would be the summary — as it stands, the tree captures the classification skeleton, the new species flag, the type designation, and the two cladogram topologies with methodology, and nothing else.

## 2. Correctness of what is captured

| Node | Printed (page) | Verdict |
|---|---|---|
| `edrioasteroidea` | "Class Edrioasteroidea Billings, 1858" (773) | Match |
| `edrioasterida`, notes "sensu Guensburg and Sprinkle (1994)" | "Order Edrioasterida Bell, 1976"; discussion explicitly says "Edrioasterida sensu Guensburg and Sprinkle (1994) is greatly expanded..." (773) | Match |
| `edrioblastoidina` | "Suborder Edrioblastoidina Fay, 1962" (773) | Match |
| `rhenopyrgidae`, `emended: true` | "Family Rhenopyrgidae Holloway and Jell, 1983" with "Diagnosis (emended)" (773) | Match |
| `rhenopyrgus`, `emended: true` | "Genus Rhenopyrgus Dehm, 1961" with "Diagnosis (emended)" (773) | Match |
| `coronaeformis_rievers_1961`, `type: true` | "Type species: Pyrgocystis (Rhenopyrgus) coronaeformis Rievers, 1961" (773) | Match |
| synonym entry, `parents: [rhenopyrgus-subgenus, pyrgocystis]` | Same citation, "Pyrgocystis (Rhenopyrgus) coronaeformis" — original combination with *Rhenopyrgus* as a parenthetical subgenus of *Pyrgocystis* | Match — correctly records the original combination (see §3) |
| `piojoensis_..._2013`, `new: true` | "R. piojoensis sp. nov." in "Species included" (773); full description pp. 773–774 | Match |
| `whitei_holloway_jell_1983` | "R. whitei Holloway and Jell, 1983" (773) | Match |
| `flos_klug_krüger_korn_rücklin_schemm-gregory_debates_mapes_2008` | "Rhenopyrgus flos Klug, Krüger, Korn, Rücklin, Schemm-Gregory, DeBaets, and Mapes, 2008" (773); reference list also spells "DeBaets, K." (774) | **Mismatch** — the taxon record's `auth` list and key both spell the seventh author "DeBates"; the paper spells it "DeBaets" both in the species citation and in its own reference list |
| Phylogeny 1 (strict consensus, 18 steps) | "recovered two most parsimonious trees with length of 18 steps... strict consensus" (Fig. 2A caption, 766) | Cannot verify topology beyond what is stated in the caption text — Fig. 2 is a line drawing not reproduced in the extracted text, so the exact branching among *Paredriophus*/*Cyathotheca*/*Lampteroblastus*/*Rhenopyrgus* cannot be checked pixel-for-pixel; the prose is consistent with a resolved (Isorophus,Carneyella)+Argodiscus clade and a less-resolved Edrioasterida clade, which matches the tree file's shape |
| Phylogeny 2 (constrained, 26 steps, Rhenopyrgus+Argodiscus sister) | "constrained... to retain rhynopyrgid Rhenopyrgus as sister taxon to the pyrgocystid Argodiscus. This analysis recovered one most parsimonious tree of length 26... Except for the placement of Rhenopyrgus, the trees are congruent" (766) | Match — tree file's second cladogram differs from the first only in moving `rhenopyrgus` to be sister of `argodiscus` |

7 of 9 substantive nodes/entries match exactly; two items are noted in full above (one taxon-record spelling mismatch, one "cannot verify" against an unreproduced figure).

## 3. Cases for the data model

- **Parenthetical subgenus notation, correctly modeled.** The type-species citation "*Pyrgocystis (Rhenopyrgus) coronaeformis* Rievers, 1961" (p. 773) uses the standard zoological convention of a subgenus in parentheses. The tree already handles this via a `synonyms` entry with `parents: [rhenopyrgus-subgenus, pyrgocystis]`, i.e., the original combination is recorded as a placement under genus *Pyrgocystis*, subgenus *Rhenopyrgus*. This is a positive confirmation that the existing `parents` mechanism (roadmap B18) covers this printed form; worth keeping as a reference example if one is wanted for the subgenus case specifically, since B18's own examples (*Rhombifera*, *Gogiida*) are all suprageneric.
- **Candidate species neither accepted nor excluded.** Discussion under *Rhenopyrgus* (p. 773) lists seven species "that might belong to *Rhenopyrgus*, but incomplete preservation precludes generic assignment" (*Pyrgocystis gracilis* Gekker 1939, *P. pulkovi* Gekker 1939, *P. sulcata*, *P. procera*, *P. varia*, *P. cylindrica* — all (Aurivillius, 1892) — and *P. ansticei* Bather, 1915), plus *Rhenopyrgus grayae* (Bather, 1915), of which the text says "This species likely warrants a new generic assignment." None of these appear anywhere in the tree, correctly, since the paper explicitly declines to place them. This is not a data-model gap in the current tree (correctly omitted), but the fact that the paper prints a hedged, unresolved candidate-membership list in prose (not a formal synonymy) that the model has no field to represent is worth flagging if the eval ever wants to capture "considered but not assigned" cases; today it can only be recovered from the free-text discussion.
- **Sibling taxon omitted from the tree, not from the source.** The paper's own Systematic Paleontology explicitly nests Cyathocystidae Bather, 1899 as a coeval family alongside Rhenopyrgidae within Edrioasterida (p. 773: "including Rhenopyrgidae Holloway and Jell, 1983 in Edrioasterida Bell, 1976 along with Cyathocystidae Bather, 1899 and Astrocystitidae Bassler, 1935"), but the tree only branches down the Rhenopyrgidae line. Per G9 this is scope history, not an error, but it means a reader of the tree alone would not see that the paper places three coordinate families under Edrioasterida.

## 4. Source record check

`data/sources.yaml` block for `2013_sumrall_heredia_rodríguez.c.m_mestre` matches the printed front matter in full: title verbatim, journal Acta Palaeontologica Polonica 58(4): 763–776, authors Sumrall, Heredia, Rodríguez, Mestre in printed order, received 20 July 2011 / accepted 30 January 2012 / online 10 February 2012, pubDate year 2013.

## 5. Uncertainties

- Fig. 2's actual node-by-node branching pattern (beyond what the caption/prose states) cannot be verified from the extracted text alone; no image was available for direct comparison.
- OCR renders "rhynopyrgids" (missing an e) in several places and "DeBates"/"DeBaets" both occur across sources; the spelling "DeBaets" is treated as certain here because it recurs twice in this paper's own text (species citation and reference list), not because of any external check.
