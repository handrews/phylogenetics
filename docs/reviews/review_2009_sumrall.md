# Review: 2009_sumrall (Sumrall 2009, *Neoisorophusella maslennikovi*)

Page mapping: PDF page index 1 = printed p. 990 (running head "990" and
"J. Paleont., 83(6), 2009, pp. 990-993"); index N = printed p. (989 + N)
through index 4 = p. 993.

## 1. Coverage

| item | status | example |
|---|---|---|
| classification skeleton | all | Class > Order > Suborder > Family > Genus > species, matches p. 991 header, one spelling issue (see §2) |
| new taxa | all | *maslennikovi* flagged `new: true` (genus not new) |
| type species | n/a | genus is pre-existing (Kammer et al. 1987); no type-species act in this paper |
| synonymy lists | none | the two nomina nuda ("Yakutidiscus...") printed like a synonymy block are not entered at all |
| material | none | holotype PIN 4010/1, paratype PIN 4010/2 (p. 992) not in tree |
| occurrences | none | Takamkyt Fm./Verkhoyansk locality (p. 992) not in tree |
| illustrations | none | Figs 1–2 not in tree |
| diagnoses | none | genus/species diagnosis (p. 991–992) not in tree |
| phylogeny | none | paper has no cladogram |

Beyond the skeleton, the only thing captured is the `new: true` flag on the
species; everything else, including the paper's central nomenclatural story
(see §3), is absent.

## 2. Correctness of what is captured

| node | printed (page) | verdict |
|---|---|---|
| `edrioasteroidea` | "Class Edrioasteroidea Billings, 1858" (p. 991) | match |
| `isorophida` | "Order Isorophida Bell, 1976" (p. 991) | match (rank, placement) |
| `isorophina` | "Suborder Isorophina Bell, 1976" (p. 991) | match |
| `agelacrinitidae` | "Family **Agelacrinidae** Chapman, 1860" (p. 991) | **mismatch** — see below |
| `neoisorophusella` | "Genus Neoisorophusella Kammer et al., 1987" (p. 991) | match |
| `maslennikovi_sumrall_2009` | "Neoisorophusella maslennikovi n. sp." (p. 991) | match, `new: true` correct |

**Family-name mismatch.** The printed heading reads "Family Agelacrinidae
Chapman, 1860" — without the "-iti-" that appears in this genus's usual
family name. The tree's node uses `taxon: agelacrinitidae` (the standard
spelling), not `agelacrinidae`. This is not an OCR artefact: `taxa.yaml`
already carries a dedicated record for exactly this spelling —
`agelacrinidae: {name: Agelacrinidae, rank: Family, auth: [Chapman],
year: 1860, altSpellingOf: agelacrinitidae}` — and that key is used correctly
as a tree node elsewhere in the corpus (`1900_bather.yaml`,
`1935_bassler.yaml`). Per the ground rule that identity is captured "as
printed" (the worked *Balanticystis*/`altSpellingOf` case in the `editorial`
block section), this source's node should be `taxon: agelacrinidae`, not
`agelacrinitidae`. As it stands the tree silently normalizes a spelling the
data model already has a mechanism to capture as printed.

## 3. Cases for the data model

**Ranks as editorial mandate (owner's prompt; bears on G8).** Printed
verbatim (p. 991, immediately before the classification):

> "Discussion.?Inclusion of Linnaean ranks reflects editorial policy rather
> than the views of the author."

("?" is the extraction's rendering of an em dash.) The tree's top-level
`notes: Ranks included only due to editorial policy` paraphrases this
accurately. This is a strong instance for G8 ("Rank stated in the tree, not
the record"): the source explicitly disclaims the ranks it prints — they are
*Journal of Paleontology* house style, not the author's own taxonomic
opinion — yet the only place rank lives in this dataset is `taxa.yaml`
(`isorophida: rank: Order`, etc.), which records rank as if it were a
settled attribute of the name rather than this particular source's forced
usage. The tree's `notes` captures the disclaimer at the top level, but
under G8's proposal (rank on the tree node, not the taxon record) the
disclaimer would attach to each rank word individually rather than as one
blanket sentence — worth keeping as a concrete example when G8 is scheduled.

**The nomen nudum (owner's prompt).** Two passages state it. In the
introduction (p. 990):

> "'Yakutidiscus maslennikovi' (Arendt, 1983) from the Permian Verkhoyansk
> Region was named in a short paper without diagnosis or illustration and is
> consequently a nomen nudum."

And in the Systematic Paleontology section itself (p. 991), printed in a
synonymy-like format directly under the genus and species headings:

> "'Yakutidiscus' Arendt, 1983, p. 136, nomen nudum."
> "'Yakutidiscus maslennikovi' Arendt, 1983, p. 136, nomen nudum."
> "'Yakutidiscus (?) yeltyshevae' Arendt, 1983, p. 136, nomen nudum."

The Discussion (p. 992) restates it: "Arendt (1983) described
Neoisorophusella maslennikovi n. sp. as two species, 'Yakutidiscus
maslennikovi' and 'Yakutidiscus (?) yeltyshevae' though without illustration
or diagnosis, thereby making them nomina nuda." Critically, the Type material
paragraph (p. 992) ties the specimens directly to the new name: "The
holotype of Neoisorophusella maslennikovi n. sp. is PIN 4010/1 = 'Yakutidiscus
maslennikovi' of Arendt (1983), and the paratype is PIN 4010/2 = 'Yakutidiscus
(?) yeltyshevae' of Arendt (1983)."

None of this is in the tree: there is no node, `synonyms` entry, or `notes`
for "Yakutidiscus" (genus-level nomen nudum) or its two nominal species, and
no record of the specimen-identity link between them and the new name. This
is exactly the shape B6's `act: [nomNudum]` is meant for — the printed lines
are formatted like ordinary synonymy entries (name, author, year, page,
status) and would sit naturally as `synonyms` entries on `neoisorophusella`
and on `maslennikovi_sumrall_2009` with `act: [nomNudum]`, the specimen
identity noted via `notes` or a shared `material` id once D1 lands. Currently
the paper's whole nomenclatural point — the earlier name was unavailable and
this paper is the first *available* one for the same specimens — is invisible
in the tree.

## 4. Source record check

`sources.yaml`'s `2009_sumrall` matches: title (aside from an internal
double space, harmless), *J. Paleont.* vol. 83, no. 6, Nov. 2009,
pp. 990–993, sole author Sumrall, accepted 26 July 2009 (printed "Accepted 26
July 2009").

## 5. Uncertainties

The printed family spelling "Agelacrinidae" (p. 991, §2) reads unambiguously
in a clean, typeset (non-scanned) JSTOR text extraction, so this is reported
as a real discrepancy rather than "cannot verify." No other OCR-sensitive
readings affect the nodes checked.
