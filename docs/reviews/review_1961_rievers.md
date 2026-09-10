# Review: 1961_rievers

Rievers, J. †. 1961. "Eine neue Pyrgocystis (Echinod., Edrioasteroidea) aus
den Bundenbacher Dachschiefern (Devon)." Ed. R. Dehm. *Mitt. Bayer.
Staatssamml. Paläont. hist. Geol.*, Heft 1, pp. 9–11. München, 15. März 1961.

**Page mapping.** As in the companion review (1961_dehm): the running head
"Mitt. Bayer. Staatsslg. Pal. hist. Geol. 1, 9—11" appears at the head of PDF
index 18, and printed page-foot digits confirm index 18 = p. 9, index 19 =
p. 10, index 20 = p. 11.

**Authorship note.** Rievers died 12 December 1955; the paper is a
posthumous manuscript ("Aus dem Nachlaß herausgegeben von Richard Dehm")
prepared for publication by Dehm, who states in his editor's foreword (p. 9)
that he limited himself to the foreword, minor editorial changes, added
measurements, and arranging the plate. The species diagnosis and description
are Rievers' own text.

## 1. Coverage

Everything beyond the classification skeleton is at least partly captured;
nothing is entirely absent except illustration detail and phylogeny.

| kind | captured | example |
|---|---|---|
| classification skeleton | partly | only genus *Pyrgocystis* + the one new species; no order/family, but none is printed here either |
| new taxa | all | *Pyrgocystis coronaeformis* n. sp., `new: true` |
| type species | not applicable | no genus/family is erected in this paper |
| synonymy lists | none | none printed (species is brand new) |
| material | all | the sole specimen (holotype, "einziges Stück") is captured |
| occurrences | all | locality, horizon, and associated-fauna character all captured (p. 10) |
| illustrations | partly | plate/figure range captured (`plate: 2, figures: [1,4]`); the plate explanation's per-figure captions and magnifications (p. 11, quoted in §3) are not |
| diagnoses | partly | see §2 — only the first of two diagnosis sentences is stored |
| phylogeny | none | none printed |

## 2. Correctness of what is captured

| node | printed (page) | verdict |
|---|---|---|
| `pyrgocystis` (`authority: {source: 1915_bather}`) | genus not attributed in this heading, but consistent with the taxon record | match |
| `coronaeformis_rievers_1961` `pages: [[10, 11]]` | Diagnose begins p. 10, continues onto p. 11 (see below) | match |
| `illustrations: [{plate: 2, figures: [[1, 4]]}]` | "das in Taf. 2, Fig. 1—4 dargestellte Fossil" (p. 11) | match |
| `occurrences[0]` (series/unit/location) | "Fundort: Hunsrück, Bundenbach bei Kirn (Nahe). Schicht: Unter-Devon, Hunsrückschiefer, Dachschiefer." (p. 11) | match |
| `occurrences[0].fauna: [Shallow-marine]` | "Begleitfauna: flachmeerisch." (p. 11) | match (rendering "accompanying fauna: shallow-marine" as a single `fauna` value loses that "Begleitfauna" names a category, not a value — minor) |
| `specimens.RVS.holotypes: ["[Plate 2, Figures 1–4]"]` | "Holotyp (und einziges Stück): das in Taf. 2, Fig. 1—4 dargestellte Fossil, Sammlung RıEvers, Enkirch (Mosel)." (p. 11) | match — `RVS` resolves in `repositories.yaml` to "Rievers Collection, Enkirch (Moselle)," and no catalogue number was ever assigned (see §3) |
| `diagnosis` (first two sentences of English paraphrase) | Diagnose, first sentence only (pp. 9–10, see §3) | **partial** — the second diagnosis sentence, on the crown, is not stored |

## 3. Cases for the data model

**The diagnosis is captured only in part.** The printed Diagnose (spanning
the pp. 9–10 page break, then continuing onto p. 10–11) is two sentences:

> "Eine Pyrgocystis von 95 mm Größe mit einem geschuppten Turm von etwa 13 mm
> Durchmesser, der am unteren Ende in ein unten abgerundetes, beutelartiges
> Gebilde von 27 mm Höhe und etwa 17 mm Durchmesser übergeht. Am oberen Ende
> trägt der Turm die kronenförmige Theka, von der sich, durch 5 Dreiecke
> gebildet, die Ambulacra abheben." (pp. 10–11)

The `diagnosis` field's English text stops after the first sentence (the
overall dimensions); the second sentence — the crown/theca and the
five-triangle ambulacral arrangement, which is diagnostically the more
distinctive character — is omitted even though `pages: [[10, 11]]` already
spans both pages correctly. Since this is one of the two gold-slice
protologues, the missing sentence is worth restoring even though it is a
translation/paraphrase field rather than a verbatim quote field.

**No catalogue number, ever.** The Diagnose fixes a holotype identified only
as "das in Taf. 2, Fig. 1—4 dargestellte Fossil" in a named private
collection ("Sammlung Rıevers, Enkirch (Mosel)") — there was never a museum
accession number for this specimen (Rievers was an amateur collector; his
plate is the only identifier that exists). The dataset already has a
mechanism for exactly this (D1: "A material entry may have no catalogue
number... the entry then carries a `label` and its `illustrations`, and
nothing else") and a resolved repository code (`RVS`), but the current
node still uses the pre-D1 `specimens: {RVS: {holotypes: [...]}}` shape with
the plate/figure citation standing in for an `ids` value inside a
free-text-ish holotypes list — worth flagging as a candidate for the D1
migration specifically because it is a clean instance of the "no catalogue
number" case the design already anticipates.

**Illustration captions not captured individually.** The plate explanation
(p. 11) gives four figures with distinct content and magnification, not
captured beyond the bare range:

> "Fig.1: Gesamtaufnahme; natürliche Größe. Fig.2: Ambulakral-Krone und
> oberer Teil des Theka-Turms; x 2,3. Fig.3: wie Fig.2, von der Rückseite
> präpariert; x 2,3. Fig. 4: Basal-Säckchen der Theka; x 3,2."

**Rank of "Fundort"/"Schicht"/"Begleitfauna."** The printed record uses three
separate labelled fields (locality, formation/age, associated fauna
character) that map cleanly onto the `occurrence` shape's `location`,
`series`/`unit`, and (loosely) `fauna` — a clean case, included here mainly
to note that "Begleitfauna: flachmeerisch" is an adjective describing the
associated fauna's character (shallow-marine), not itself a taxon list; the
current `fauna: [Shallow-marine]` value is defensible but is the only field
on the schema being asked to carry a descriptive adjective rather than a
list of associated taxa.

## 4. Source record check

`sources.yaml`'s `1961_rievers` record matches the printed article
completely: title verbatim, journal `mitt` (matches
`data/publications.yaml`), volume 1, `pages: [9, 11]` (confirmed by the
running head on every page), `pubDate.year: 1961`, author `rievers`.

## 5. Uncertainties

- The OCR of this article is clean; German diacritics (ü, ß) render
  correctly and no readings needed a "cannot verify" flag for the passages
  quoted above.
- Whether "flachmeerisch" was intended by Rievers as a stratigraphic
  environment term or as a loose descriptive aside cannot be settled from
  this one line alone.
