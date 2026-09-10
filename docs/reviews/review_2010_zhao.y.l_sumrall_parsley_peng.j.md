# Review: 2010_zhao.y.l_sumrall_parsley_peng.j (Zhao, Sumrall, Parsley & Peng 2010, *Kailidiscus chinensis*)

Page mapping: PDF page index 0 = printed p. 668 (masthead "J. Paleont.,
84(4), 2010, pp. 668-680" and footer "668"); index N = printed p. (668 + N)
through index 12 = p. 680.

## 1. Coverage

| item | status | example |
|---|---|---|
| classification skeleton | all | Class > Order uncertain > Family uncertain > Genus > species, matches p. 674 header |
| new taxa | all | genus and species both flagged `new: true` |
| type species | all | `type: true` on *chinensis*, matches "Type species.—*Kailidiscus chinensis*" |
| synonymy lists | none/n-a | no formal synonymy; paper only discusses undiagnosable look-alikes (*Walcottidiscus*, "*Stromatocystites walcotti*") in prose, not entered |
| material | partly | holotype + 15 paratype numbers captured under `specimens`, but one is mistyped (see §2) |
| occurrences | none | Kaili Fm./Miaobanpo Quarry locality (p. 679) not in tree |
| illustrations | none | Figs 1–7 not in tree |
| diagnoses | none | genus/species diagnoses (p. 674, 675) not in tree |
| phylogeny | none | paper states a fuller phylogenetic treatment "is in preparation to be published elsewhere" (p. 668); none here |

## 2. Correctness of what is captured

| node | printed (page) | verdict |
|---|---|---|
| `edrioasteroidea` | "Class EDRIOASTEROIDEA Billings, 1858" (p. 674) | match |
| `edrioasteroidea-order-uncertain_..._2010` | "Order uncertain" (p. 674) | match; `taxa.yaml` rank Order, sourced to this paper |
| `edrioasteroidea-family-uncertain_..._2010` | "Family uncertain" (p. 674) | match; `taxa.yaml` rank Family, sourced to this paper |
| `kailidiscus_..._2010` | "Genus KAILIDISCUS new genus" (p. 674) | match, `new: true` correct; `homonym: true` on the record is not this paper's own claim (the homonymy is only discovered later, by 2022_deshmukh) and is correctly absent from this tree |
| `chinensis_..._2010` | "Type species.—*Kailidiscus chinensis* n. gen. and sp." (p. 674) | match, `type`/`new` correct |
| `specimens.paratypes` | "paratypes GM-70, 746, 1331, 1670, 1898, **2103**, 2146, 3295a, b, c, 3035, 3600, 3665, 8052, 9292" (p. 679) | **mismatch** — tree lists `GM 2013` |

**Paratype number transcription error.** The tree's paratype list has `GM
2013`; the paper's Types paragraph (p. 679) and the figure captions for that
specimen (p. 676, three separate captions, plus the Types list) all read
"2103" — never "2013." The digits are unambiguous throughout (no OCR
ambiguity: five independent occurrences of "2103," zero of "2013"). This is a
data-entry transposition that should read `GM 2103`.

## 3. Cases for the data model

**Two separate uncertain ranks, printed as two separate lines (relates to
C4/C5).** Unlike the C5 example ("Order and Family Uncertain" as one English
heading), this paper prints "Order uncertain" and "Family uncertain" as two
distinct lines (p. 674), removing the ambiguity C5 discusses. The tree's two
nested `openTaxon` placeholders (`edrioasteroidea-order-uncertain_...`,
`edrioasteroidea-family-uncertain_...`) map cleanly onto this, one per
printed line, and each placeholder record in `taxa.yaml` correctly carries
its own `rank` and is `source`d to this paper — a clean confirmation of the
C4 mechanism rather than a problem case.

**Type fixation stated as monotypy, unflagged.** The genus diagnosis reads
"Diagnosis.—Same as for species by monotypy" (p. 674), an explicit statement
of type fixation by monotypy (B14's "M"). No `typeFixation` field exists yet
in the schema, so nothing is missing that should be present; noted here as a
ready-made example for when B14 is implemented (`typeFixation: monotypy` on
the `chinensis` node paired with `Type species.—Kailidiscus chinensis`).

## 4. Source record check

`sources.yaml`'s `2010_zhao.y.l_sumrall_parsley_peng.j` matches the printed
article on title, journal, volume 84, pages 668–680, authors, accepted date
(2010-03-20, printed "ACCEPTED 20 MARCH 2010"), and DOI
(10.1666/09-159.1). One mismatch: `number: 5`, but the printed masthead and
every running head on the article (pp. 670, 674, 676, 678, 680 — six
separate instances) read "84(4)"/"NO.4"/"NO. 4," never "5." The issue number
should be 4, not 5.

## 5. Uncertainties

None beyond the two items already flagged as confirmed mismatches; this is a
clean text-layer PDF (Cambridge University Press "Published online by"
footer) with no scanning-related OCR risk to the digits or names checked.
