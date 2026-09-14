# Review: 1978_bell.b.m_sprinkle

Bell, B. M. and Sprinkle, J. 1978. "*Totiglobus*, an Unusual New Edrioasteroid
from the Middle Cambrian of Nevada." *Journal of Paleontology* 52(2):
243–266, 6 pls., 4 text-figs. March 1978.

**Publication year.** The source file is named `1977-07-05-v.txt`. That date
is neither the publication date nor a reading date: the paper's own
end-of-article line reads "MANUSCRIPT RECEIVED APRIL 5, 1977 / REVISED
MANUSCRIPT RECEIVED JULY 5, 1977" — the filename carries the *revised*
manuscript's receipt date. The printed running head ("JOURNAL OF
PALEONTOLOGY, V. 52, NO. 2, P. 243-266... MARCH 1978") and the citation line
("Journal of Paleontology, Mar., 1978, Vol. 52, No. 2... pp. 243-266") agree
on **1978** as the publication year, and the dataset keys the source
`1978_bell.b.m_sprinkle` — correctly following the publication date rather
than the filename's manuscript date, consistent with the roadmap's ground
rule (A11) that a source key carries the year of publication, never of a
reading.

**Page mapping.** Printed page-foot numbers appear directly in the text: PDF
index 1 = p. 243 (no digit shown, but the header states P. 243-266 and this
is the article's first page), index 2 ends "244," index 3 ends "245," index
4 ends "246," index 5 begins the Genus *Totiglobus* section and runs to p.
247 (confirmed by the next digit, 247, later in the file).

## 1. Coverage

| kind | captured | example |
|---|---|---|
| classification skeleton | all | class > order > two sibling families > genus > species, matching the printed "SYSTEMATIC PALEONTOLOGY" hierarchy exactly |
| new taxa | all | family Totiglobidae, genus *Totiglobus*, species *nimius*, all flagged `new: true` |
| type species | all | `type: true` on `nimius` under `totiglobus`, matching "Type species.—*Totiglobus nimius* n. sp." (p. 247) |
| synonymy lists | none | the two informal prior citations under *T. nimius* (§3) are not captured; no other synonymy is printed |
| material | none | "Type specimens.—Holotype MCZ 983; paratypes MCZ 984–996 and NYSM 13293–13326" (p. 247) is absent from the tree entirely |
| occurrences | none | the Chisholm Shale / Glossopleura Zone / Pioche, Nevada locality data (pp. 243–244) is absent |
| illustrations | none | Pls. 1–6 and Text-figs. 1–4 are absent |
| diagnoses | none | none of the five printed diagnoses (order, family, genus, species, plus the family's own deferred diagnosis, §3) are stored |
| phylogeny | none | no diagram printed; the paper's evolutionary discussion is confined to prose comparisons with Pyrgocystidae and Stromatocystitidae |

In one sentence: the classification skeleton (with correct `new`/`emended`
flags) is fully and correctly captured; everything else the paper prints —
diagnoses, material, occurrences, illustrations — is not captured at all.

## 2. Correctness of what is captured

All eight nodes structurally match the printed systematic hierarchy (Class
Edrioasteroidea Billings 1858 > Order Edrioasterida Bell 1976 [emend. herein]
> Family Edrioasteridae Bell 1976 [emend. herein] and Family Totiglobidae
n. fam., the latter > Genus *Totiglobus* n. gen. > *T. nimius* n. sp., type
species). One attribution question:

| node | printed (page) | verdict |
|---|---|---|
| `edrioasterida`, `emended: true` | "Order EDRIOASTERIDA Bell, 1976 [emend. herein]" (p. 245) | match |
| `edrioasteridae`, `emended: true` | "Family EDRIOASTERIDAE Bell, 1976 [emend. herein]" (p. 246) | match, **but see below** |
| `totiglobidae`, `new: true` | "Family TOTIGLOBIDAE n. fam." (p. 246) | match |
| `totiglobus`, `new: true` | "Genus TOTIGLOBUS n. gen." (p. 247) | match |
| `nimius_bell.b.m_sprinkle_1978`, `type: true`, `new: true` | "TOTIGLOBUS NIMIUS n. sp." ... "Type species.—*Totiglobus nimius* n. sp." (p. 247) | match |

**`edrioasteridae` attribution conflict.** This paper credits the family to
"Bell, 1976" throughout (heading, p. 246, and discussion, p. 245: "the order
Edrioasterida as proposed by Bell (1976a)... the order Isorophida Bell
(1976a)"). But `taxa.yaml`'s canonical record is `edrioasteridae: {name:
Edrioasteridae, rank: Family, auth: [bather], year: 1898}` — Bather, 1898,
not Bell, 1976. The tree node carries no `auth`/`year` of its own (it only
has `emended: true`), so this printed attribution is not recorded on the node
at all and the disagreement with the taxon record's authority — exactly the
kind of claim A2 says the model should surface ("Where it differs, the
difference is a claim... the claim table emits it") — is currently invisible.
**Cannot verify** which authorship is correct without Bather 1898 and Bell
1976a in hand; flagged as a discrepancy either way.

**A second, smaller authorship question.** `taxa.yaml`'s `isorophus` record
gives `auth: [foerste], year: 1916`; the current paper's heading reads
"Genus ISOROPHUS Foerste, 1917" — a one-year difference. (This genus is not
in the current tree's scope — it belongs to a different, unrelated part of
the paper — noted here only because it surfaced while checking author
records against this text; **cannot verify** which year is correct.)

## 3. Cases for the data model

**A family's diagnosis explicitly deferred to its genus.** Family Totiglobidae
gets a full diagnosis (p. 246), but at the genus level the paper writes:

> "Genus TOTIGLOBUS n. gen. ... Diagnosis.—The monotypic genus has the
> characteristics of the type species." (p. 247)

and later, for the species itself:

> "TOTIGLOBUS NIMIUS n. sp. ... Diagnosis.—A Totiglobidae with: subgloboid
> theca, central plates of aboral surface form basal discoidal structure of
> larger outer plates surrounding smaller central ones..." (p. 247)

So the genus's printed "diagnosis" is not a diagnosis at all but an explicit
statement that none is needed, because the genus is monotypic and the
species carries the content. The schema's `diagnosis` field is a single
string with no way to record "deferred to <node>, because monotypic" as
distinct from "not printed" or "not captured" — worth a marker, since this
exact pattern (deferral-by-monotypy) recurs in the 1983 Holloway & Jell paper
reviewed alongside this one (Family Rhenopyrgidae deferring to its genus, and
species *Epipaston ixine* deferring to its genus with the identical phrase
"Diagnosis.—As for genus").

**"Aepyaster Sprinkle & Strimple (in preparation)" appears here — earlier
than the roadmap's cited source.** The roadmap's A9 item documents this
in-preparation citation from "Bell 1980." It in fact already appears in this
1978 paper, twice:

> "Addition of two new, monotypic genera, *Totiglobus* n. gen. and
> *Aepyaster* Sprinkle & Strimple (in preparation) in the new family
> Totiglobidae requires only the following modest changes of the ordinal
> description." (p. 245)
>
> "The family Totiglobidae includes only two monotypic genera, *Totiglobus*
> n. gen. and *Aepyaster* Sprinkle & Strimple (in preparation), both Cambrian
> forms." (p. 246)

*Aepyaster* is treated here as a second, coordinate genus of Totiglobidae —
described in the family diagnosis and discussion as having a "clavate
theca" contrasted with *Totiglobus*'s "subgloboid theca" — but the tree has
no node for it at all (the family shows only one child, `totiglobus`). Under
the ground rule that absence is not a statement, leaving *Aepyaster*
uncaptured is defensible as scope (G9), but worth flagging because (a) it is
a second in-prep citation predating the one the roadmap already records, and
(b) it means the family node's `children` list is visibly incomplete against
what the family's own printed diagnosis describes.

**Two prior informal citations of the new species, in quotation marks.**
Directly under the "TOTIGLOBUS NIMIUS n. sp." heading (p. 247), before the
type specimens:

> "'Poorly preserved edrioasteroid,' SPRINKLE, 1973, Pl. 9, figs. 5, 6.
> 'New edrioasteroid,' SPRINKLE, 1976, Pl. 1, fig. 2."

This is the H-table's "a usage with no name, cited by a phrase" case (cf.
Sowerby's "A Fossil Belonging to the Class Radiaria") — two earlier,
un-named mentions of the same specimens, printed in quotation marks exactly
where a synonymy list would go. Neither is captured in the tree; both are
clean candidates for `openTaxon`/`quoted` placeholders "cited like any
usage," per the roadmap's own prescription for this pattern.

## 4. Source record check

`sources.yaml`'s `1978_bell.b.m_sprinkle` record matches the printed article
in full: title, journal `jofpaleo`, volume 52, number 2, pages 243–266,
`pubDate: {year: 1978, month: 3}`, authors `bell.b.m` + `sprinkle`,
`identifiers.jstor: 1303701` (matches the Stable URL exactly). No
discrepancy.

## 5. Uncertainties

- OCR is clean throughout the passages consulted; no readings needed a
  "cannot verify" flag for spelling or year.
- The Foerste 1916/1917 date discrepancy for *Isorophus* (§2) cannot be
  resolved from material available for this review.
- Whether the *Aepyaster* omission (§3) is deliberate scope or an oversight
  cannot be determined from the tree file alone.
