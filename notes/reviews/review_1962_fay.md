# Review: 1962_fay

Fay, R. O. 1962. "Edrioblastoidea, a New Class of Echinodermata." *Journal of
Paleontology* 36(2): 201–205, pl. 34, 3 text-figs. March 1962.

**Page mapping.** The printed running head, "JOURNAL OF PALEONTOLOGY, V. 36,
NO. 2, P. 201-205, PL. 34, 3 TEXT-FIGS., MARCH, 1962," appears at the top of
the first article page (PDF index 2); printed page-foot numbers 201–205
appear at the bottom of PDF index 2–6 respectively, so PDF index *n* = printed
page 199+n for n = 2..6.

## 1. Coverage

The tree captures the classification skeleton only — no diagnosis, no
material detail beyond a bare specimen number, no occurrence, and no
illustration is recorded anywhere in the file.

| kind | captured | example |
|---|---|---|
| classification skeleton | all | class, genus, species nodes present; nothing above class or below species is printed to capture |
| new taxa | all | Edrioblastoidea (class) is the only new taxon in the paper, flagged `new: true` |
| type species | none printed here (see §2) | *Astrocystites* is pre-existing (Whiteaves, 1897); no type-species designation is printed in this paper |
| synonymy lists | partly | the full synonymy for *A. ottawaensis* (Whiteaves 1897; Bather 1914 as *Steganoblastus*; Hudson 1917, 1925, 1927; Bassler 1936; Wilson 1946, p. 201) is printed with volumes/pages/plates; only the Bather/*Steganoblastus* entry is captured, and even that entry carries no `auth`/`year`/`pages` |
| material | partly | the holotype/syntype number (752) is captured; the second (now-lost) syntype and the "labelled a syntype" wording are not (§2–3) |
| occurrences | none | "Middle Ordovician, Trenton, Cobourg beds... Booth Street, Ottawa, Ontario, Canada" (p. 205; also on the plate caption, p. 201) is nowhere in the tree |
| illustrations | none | Pl. 34, figs. 1–5, and Text-figs. 1–3, all captioned in the paper, are not recorded |
| diagnoses | none | the class-level diagnosis (the entire second paragraph of the paper, p. 201, quoted in part in §3) has no home on the `edrioblastoidea` node |
| phylogeny | none | the Discussion (pp. 205) argues a directional hypothesis (Edrioblastoidea ancestral to Blastoidea) in prose; no diagram is printed |

In one sentence: beyond the class/genus/species skeleton, essentially nothing
this paper prints is captured.

## 2. Correctness of what is captured

| node | printed (page) | verdict |
|---|---|---|
| `edrioblastoidea`, `new: true` | "The new class of echinoderms, Edrioblastoidea, is established..." (Abstract, p. 201) | match |
| `astrocystites`, `moved: {taxon: edrioasteroidea}` | "The genus *Astrocystites* Whiteaves is removed from the Edrioasteroidea and placed in a new class..." (p. 201) | match |
| `astrocystites` `synonyms: [{taxon: steganoblastus}]` | "BATHER, 1914, Geol. Magazine... p. 195... (as *Steganoblastus*)" (p. 201) | **partial** — identity match, but the entry carries none of the printed citation (author, year, page, plate) |
| `ottawaensis_whiteaves_1897`, `type: true` | no printed statement in this paper designates a type species for *Astrocystites*; the genus is treated as monotypic throughout but "type species" is never the phrase used | **cannot verify from this text** — see §3 |
| `specimens.syntypes: ["Canadian Geological Survey 752"]` | "Types—The holotype, No. 752... is on deposit with the Canadian Geological Survey. It is labelled a syntype because another specimen, lent to Mr. Hudson... was the other syntype. When Hudson died, this specimen disappeared." (p. 205) | **partial / cannot verify which term is definitive** — the paper itself uses both "the holotype" (in the plate caption, p. 201, and in the running text, p. 205) and "labelled a syntype" (p. 205) for the *same* specimen No. 752, and the tree picks one (`syntypes`) without noting the contradiction or the missing second (lost) syntype |

`sources.yaml`'s `1962_fay.audit.notes` — "Migrated from complete:
named=true open=null history=true specimens.basic=true specimens.all=true" —
is consistent with a thin, skeleton-only capture; nothing here contradicts
that self-description.

## 3. Cases for the data model

**Fay's paper erects a class only — no order, no family.** The brief for
this review expected order/family acts; the text has none. Both "order" and
"family" are absent from the paper entirely (checked exhaustively — the words
never occur). The genus and species are pre-existing (Whiteaves, 1897) and
unchanged; the single nomenclatural act is the class name itself, applied
directly to an existing genus with nothing intervening:

> "The genus *Astrocystites* Whiteaves is removed from the Edrioasteroidea
> and placed in a new class of echinoderms, Edrio-blastoidea, which includes
> forms that have five basals, five radials, five deltoids, and five orals,
> with numerous infradeltoids between the deltoid limbs and radial limbs,
> and five straight petaloid ambulacra with a double row of ambulacral
> plates above marginal edges of the deltoids." (p. 201, opening of the
> diagnosis paragraph)

This is worth noting explicitly because a monotypic class-directly-over-genus
structure (no order, no family) is an unusual shape for the model's rank
hierarchy to represent cleanly, and it is exactly what this source prints.

**No printed type-species designation, but `type: true` is set anyway.**
Fay's paper never says "type species" (searched exhaustively). *Astrocystites*
is treated as effectively monotypic in this paper (one species discussed), so
the `type: true` flag on `ottawaensis_whiteaves_1897` is plausible but is not
something *this* source states — it would have been fixed, if anywhere, in
Whiteaves' 1897 original description, which has no source record anywhere in
this dataset (`1897_whiteaves` does not exist in `sources.yaml`). This is a
clean instance of B20 ("placements the editor inferred") except for identity
rather than placement — there is no `editorial.inferred` marker recording
that the flag is not printed here.

**The holotype/syntype contradiction is Fay's own, not an OCR artifact.**
The paper's plate caption unambiguously reads "Holotype, 752, Canadian
Geological Survey" (p. 201), but the body text under "Types" reads:

> "Types.—The holotype, No. 752, from the Middle Ordovician, Trenton,
> Cobourg beds, collected from Booth Street, Ottawa, Ontario, Canada, is on
> deposit with the Canadian Geological Survey. It is labelled a syntype
> because another specimen, lent to Mr. Hudson, Plattsburg, New York, was the
> other syntype. When Hudson died, this specimen disappeared." (p. 205)

Fay calls the same specimen "the holotype" three times (plate caption; "the
holotype" opening the Types paragraph; "the holotype" again on p. 203, "only
one specimen is now known to exist") and "labelled a syntype" once, in the
same breath as explaining that the original description apparently
recognized two syntypes, of which No. 752 is one and the (now lost) other
was never renumbered or refound. This is not modelled by D2's `holotype` /
`syntype` role enum as currently used (single value per material entry) —
the printed record needs to carry both the author's own word ("labelled a
syntype," matching D1's `roleAsPrinted`) and the fact that this is the same
specimen the paper's own caption calls a holotype. The missing second
syntype (lost, never had a number of its own) is also absent from the tree —
a case for `examined: false`-with-no-`ids` (D1) rather than silence.

**A pre-existing genus name used under a different name by an earlier
author, printed inline rather than in a formal synonymy list.** "BATHER,
1914... (as *Steganoblastus*)" (p. 201) is exactly the citation-list format
A1's table describes for a `synonyms` entry, but the current entry
(`{taxon: steganoblastus}`) carries none of the bibliographic content that
makes the printed line a claim ("Bather 1914 used the name Steganoblastus for
this species") rather than a bare identity link.

## 4. Source record check

Mostly matches: title (case-normalized only), journal `jofpaleo`, volume 36,
number 2, pages 201–205, `pubDate.year: 1962, month: 3` all agree with the
printed running head and the JSTOR citation line ("Journal of Paleontology,
Mar., 1962, Vol. 36, No. 2..."). One discrepancy: `identifiers.jstor:
13011100` has an extra digit — the printed Stable URL is
`https://www.jstor.org/stable/1301100` (seven digits), not eight.

## 5. Uncertainties

- The OCR of this JSTOR scan is generally clean for prose but garbles some
  running-text page headers ("EDRIOASTEROIDEA, NEW CLASS OF ECHINODERMA TA"
  with a stray space) and one figure caption region (p. 204) into
  fragments; none of this affected any reading relied on above.
- Whether Whiteaves 1897 (or a later author before Fay) ever printed an
  explicit type-species designation for *Astrocystites* cannot be verified —
  that source is not in this dataset and not in the text provided for this
  review.
