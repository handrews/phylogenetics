# Review: Sprinkle & Sumrall 2015

Source text: `2014-07-13-a.txt`. Tree: `data/trees/2015_sprinkle_sumrall.yaml` (25 lines).

**Publication year and page mapping.** The file is named for the printed "Accepted 13 July 2014" line at the end of the article (last page). The printed masthead reads "Journal of Paleontology, 89(2), 2015, p. 346–352", copyright "© 2015, The Paleontological Society", DOI 10.1017/jpa.2014.29. **The publication year is 2015** (volume 89, issue 2); 2014-07-13 is only the acceptance date, not a publication date — no separate "received" or "available online" date is printed anywhere in the article (the recurring "Published online by Cambridge University Press" footer under the DOI is CUP's generic platform boilerplate on every page, not an article-specific online-first date). Running head "Sprinkle and Sumrall—New Early Ordovician edrioasteroids" plus page number recurs each page, so **printed page = PDF page index + 346** (index 0 = 346 … index 6 = 352).

## Gold-slice: astrocystitids are edrioblastoids

Systematic headers, quoted exactly, p. 348 (index 2):
```
Class Edrioasteroidea Billings, 1858
Order Edrioasterida Bell, 1976
Suborder Edrioasterina, Bather, 1898
Family Edrioasteridae Bather, 1899
Genus Pseudedriophus new genus
```
and p. 351 (index 5), continuing under the same Order Edrioasterida heading (not repeated):
```
Suborder Edrioblastoidina Fay, 1962
Family Astrocystitidae Bassler, 1935
Genus Porosublastus new genus
```
The title itself calls the second new taxon an "astrocystitid" ("New edrioasterine and astrocystitid (Echinodermata: Edrioasteroidea)…"), and the abstract calls it "a new edrioblastoid, *Porosublastus inexpectus*… only the second edrioblastoid ever found in the Early Ordovician" — i.e. the paper uses "astrocystitid" and "edrioblastoid" interchangeably for a member of Family Astrocystitidae within Suborder Edrioblastoidina, matching the systematic heading exactly. **No act** (nom. transl., emendation, synonymy, or rank change) is printed against Edrioblastoidea/Edrioblastoidina/Astrocystitidae anywhere in this paper — Fay 1962's and Bassler 1935's names are used unchanged; the only new nomenclature in the whole paper is the two new genera and two new species.

## 1. Coverage

This is a short, purely descriptive paper (two new monotypic taxa, no phylogenetic analysis, no synonymy lists — both taxa are brand new).

| Item | Status | Example |
|---|---|---|
| Classification skeleton | All | Both full hierarchies (Class→Order→Suborder→Family→Genus→species) captured, which is the entire printed classification |
| New taxa | All | Both new genera and both new species flagged `new: true` |
| Type species | All | Both species flagged `type: true` ("Type species.—…new genus new species", pp. 348, 351) |
| Synonymy lists | n/a | None printed — both taxa are newly named |
| Material | None | Holotype/paratype catalogue numbers (e.g. "Holotype 1777TX7; paratypes 1781TX9, 1777TX8, 1778TX16… and 1779TX2", p. 348) not captured |
| Occurrences | None | Detailed collecting-locality data for each specimen (pp. 348, 351) not captured |
| Illustrations | None | Figs. 1–3 not referenced |
| Diagnoses | None | Both genus diagnoses read "Diagnosis.—Same as for species." (pp. 348, 351) and both species diagnoses are printed in full; none stored |
| Phylogeny | n/a | The paper contains no cladogram — its "Phylogenetic placement" content is prose comparison only, so there is no `phylogenies` section to capture and none is missing |

Beyond the classification skeleton and the new/type flags, nothing else is captured — consistent with an early-scope entry (roadmap G9).

## 2. Correctness of what is captured

| Node | Printed (page) | Verdict |
|---|---|---|
| `edrioasteroidea` | "Class Edrioasteroidea Billings, 1858" (348) | Match |
| `edrioasterida` | "Order Edrioasterida Bell, 1976" (348) | Match |
| `edrioasterina` | "Suborder Edrioasterina, Bather, 1898" (348) | Match (taxa.yaml: rank Suborder, auth Bather, year 1898) |
| `edrioasteridae` | "Family Edrioasteridae Bather, **1899**" (348) | **Mismatch** — the taxon record (`edrioasteridae`) carries `year: 1898`, but this paper prints 1899 for the family while printing 1898 for the coordinate suborder Edrioasterina one line above, citing the same underlying Bather work in both cases. The paper itself is internally inconsistent about the year (see §3); flag rather than silently trust either |
| `pseudedriophus`, `new: true` | "Genus Pseudedriophus new genus" (348) | Match |
| `guensburgi_sprinkle_sumrall_2015`, `type: true`, `new: true` | "Type species.—Pseudedriophus guensburgi new genus new species" (348) | Match |
| `edrioblastoidina` | "Suborder Edrioblastoidina Fay, 1962" (351) | Match |
| `astrocystitidae` | "Family Astrocystitidae Bassler, 1935" (351) | Match |
| `porosublastus`, `new: true` | "Genus Porosublastus new genus" (351) | Match |
| `inexpectus_sprinkle_sumrall_2015`, `type: true`, `new: true` | "Type species.—Porosublastus inexpectus new genus new species" (351) | Match |

8 of 9 nodes match exactly; one mismatch (Edrioasteridae's year) is detailed above and in §3.

## 3. Cases for the data model

- **Same source, two years for two coordinate names.** On p. 348 the paper prints, four lines apart, "Suborder Edrioasterina, **Bather, 1898**" and "Family Edrioasteridae **Bather, 1899**". Both names trace to the same underlying Bather work — his 1899 "phylogenetic classification of the Pelmatozoa," published in the "Report of the 68th meeting" of the British Association, itself "for 1898" (per this paper's own reference list: "Bather, F.A., 1899… British Association for the Advancement of Science, Report for 1898, v. 68, p. 916–923") — the classic dual-dating case of a proceedings volume reporting on one year's meeting but issued the next (roadmap A7/A8 territory: a reading year vs. an issue year). The paper is not internally consistent about which year it prints for which coordinate name from that one work. Both years should be recorded exactly as printed on their respective nodes rather than assumed to be a single typo; today neither tree node carries an explicit `year`/`citedAs` override, so the discrepancy is invisible unless the taxa.yaml records themselves are checked (as done above for Edrioasteridae).
- **"Diagnosis.—Same as for species."** Both new, monotypic genera use this exact phrase (pp. 348, 351) instead of repeating the diagnosis. This is a printed statement of diagnostic redundancy specific to monotypy, distinct from simply omitting a diagnosis; if diagnoses are captured in future, this phrase is worth preserving verbatim (in `notes` or as the `diagnosis` value itself) rather than treating the genus as having "no diagnosis printed."

## 4. Source record check

`data/sources.yaml` block for `2015_sprinkle_sumrall` matches the printed front matter in full: title verbatim, journal Journal of Paleontology 89(2): 346–352, authors Sprinkle, Sumrall in printed order, accepted 2014-07-13, doi 10.1017/jpa.2014.29, pubDate year 2015.

## 5. Uncertainties

- No "received" or "available online" date is printed anywhere in the article; the source record correctly carries only the accepted date, and nothing further can be verified.
- The Edrioasteridae/Edrioasterina year discrepancy (1899 vs. 1898) is the paper's own inconsistency, not an OCR artifact — both digits are clear in the extracted text — so this is reported as a genuine printed discrepancy, not "cannot verify."
