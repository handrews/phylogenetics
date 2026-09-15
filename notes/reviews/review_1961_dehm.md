# Review: 1961_dehm

Dehm, R. 1961. "Über Pyrgocystis (Rhenopyrgus nov. subgen.) coronaeformis
Rievers aus dem rheinischen Unter-Devon." *Mitt. Bayer. Staatssamml. Paläont.
hist. Geol.*, Heft 1, pp. 13–17. München, 15. März 1961.

**Page mapping.** The scan is the whole Heft 1. Each article's running head
gives "Mitt. Bayer. Staatsslg. Pal. hist. Geol. 1, x–y." Dehm's paper carries
the head "1, 13—17" (PDF index 24) and printed page-foot digits 13–17 appear
in sequence through PDF index 24–28 (index 24=p.13, 25=p.14, 26=p.15, 27=p.16,
28=p.17, confirmed by the digit at the end of each block). Rievers' companion
paper (see separate review) is "1, 9—11" immediately before it, with no
intervening numbered page (the Rievers plate, Tafel 2, occupies unnumbered
leaves between them — see the source-record note below).

## 1. Coverage

| kind | captured | example |
|---|---|---|
| classification skeleton | partly | genus *Pyrgocystis* + 9 comparanda + subgenus *Rhenopyrgus* captured, but see §3: this is an editor-assembled list from prose (p. 15), not a printed systematic list |
| new taxa | all | *Rhenopyrgus* nov. subgen., flagged `new: true` |
| type species | all | `type: true` on *coronaeformis* under *Rhenopyrgus*, matching "Typus-Art der Untergattung: Pyrgocystis coronaeformis Rievers (1961)" (p. 16) |
| synonymy lists | none printed as such; one recombination note captured (see §3) | — |
| material | none | the holotype (already described by Rievers, p. 11) is not re-cited here |
| occurrences | all | e.g. *octogona* "Bornich bei Weisel am Rhein" (p. 13) → `location: [Bornich, near Weisel on the Rhine, Germany]` |
| illustrations | partly | Richter 1930 fig. 1h cited for *octogona* (p. 15) captured; the paper's own comparison table of measurements (p. 15) is not |
| diagnoses | **none** | the printed subgenus diagnosis (p. 16, quoted in full in §3) is not stored anywhere on the `rhenopyrgus` node |
| phylogeny | none | Section C ("stammesgeschichtliche Stellung," pp. 16–17) is a prose phylogenetic discussion, not a diagram; correctly left uncaptured, but see the commented-out block in the file (§3) |

## 2. Correctness of what is captured

19 of 21 nodes match the printed text (occurrences, `type` flags, and the
Richter 1930 citation all verified as printed). Two rows need attention:

| node | printed (page) | verdict |
|---|---|---|
| `rhenopyrgus` (`taxon: rhenopyrgus`, `rank: subgenus`) | "eine eigene Untergattung, Rhenopyrgus nov. subgen." (p. 16) | **mismatch** — the tree keys this node to `rhenopyrgus` (the dataset's genus-rank identity record: `taxa.yaml` `rhenopyrgus: {name: Rhenopyrgus, auth: [Dehm], year: 1961}`, no rank = genus by the dataset's own convention) and then overrides the rank with a node-level `rank: subgenus`. But the dataset already carries a dedicated subgenus-rank record, `rhenopyrgus-subgenus`, for exactly this identity (`rhenopyrgus-subgenus: {name: Rhenopyrgus, rank: subgenus, auth: [Dehm], year: 1961}`), and three other trees that cite Dehm's subgenus (`1966_regnéll.yaml`, `2013_sumrall_heredia_rodríguez.c.m_mestre.yaml`, `2020_ewin_martin.m_isotalo_zamora.yaml`) all key to `rhenopyrgus-subgenus`, nested one level under `pyrgocystis`. `1961_dehm.yaml` — the source that originates the subgenus — is the one file in the dataset using the bare genus-rank key with a rank override instead of the dedicated record. This is the B18 "same name at different ranks" case the roadmap already anticipated a fix for; the fix is a key change (`rhenopyrgus` → `rhenopyrgus-subgenus`), not a new field. |
| `synonyms` entry under `coronaeformis_rievers_1961` (`- parents: [taxon: pyrgocystis]`) | Dehm's paper repeatedly narrates that Rievers placed the species directly in *Pyrgocystis* (unqualified) and that Dehm's own act is to insert the subgenus between genus and species | **cannot verify intent** — the entry has no `taxon`, `auth`, `year`, `citedAs`, or `pages`, so nothing on the entry itself says whose usage ("Pyrgocystis coronaeformis Rievers 1961," pp. 9–11) is being recorded or on what page. As written it is legal under the schema (an implicit self-reference via omitted `taxon`) but carries none of the bibliographic information the model elsewhere requires for a cited earlier usage (A1's table: a `parents`/`synonyms` node "identifies... the work in which the cited usage appeared"). |

The genus root node (`taxon: pyrgocystis`) carries no `authority`, while Dehm's
own heading text for the section ("innerhalb der Gattung Pyrgocystis BATHER,"
p. 15) does credit Bather — omission is defensible under A2 (it matches the
`taxa.yaml` record and would be redundant), but note that the companion
`1961_rievers.yaml` tree *does* state `authority: {source: 1915_bather}` on
the same node for the same fact, so the two sibling trees are inconsistent in
how they treat this printed line even though the underlying identity is not
in dispute.

## 3. Cases for the data model

**The subgenus diagnosis is not captured at all.** The protologue reads (p.
16):

> "Diagnose von Rhenopyrgus nov. subgen.: Pyrgocystis (mit turmförmiger, aus
> adoral imbrikaten, alternierenden Plattenreihen gebildeter Theka und mit
> fünf Ambulakralfurchen mit kräftigen Saumplatten) mit folgenden
> Besonderheiten: Theka groß und schlank, oben kegelförmig erweitert,
> Thekaplatten zum Teil mit verstärktem Rand und Mediankiel; Basal-Säckchen
> aus kleinen Platten. Typus-Art der Untergattung: Pyrgocystis coronaeformis
> Rıevers (1961)."

Only the final sentence (the type-species fixation) is reflected in the tree
(as the `type: true` flag); the diagnosis text itself has no home on the
`rhenopyrgus` node. Since this is one of the two protologues anchoring the
gold slice, this is the single most consequential coverage gap in the file.

**A tree assembled from prose, not from a printed list (G7).** Dehm's paper
has no "Systematic Paleontology" section or classification table. The species
list under `pyrgocystis` (sardesoni, grayae, volborthi, gracilis, pulkovi,
sulcata, procera, cylindrica, octogona) is compiled from a single
comparative paragraph on p. 15 ("Die meisten Arten der Gattung Pyrgocystis
gehören dem Unter-Silur..."), written to establish which species are close to
*coronaeformis*, not to classify the genus. The tree presents it as an
ordinary `children` list indistinguishable from a printed systematic list.
This is the same situation G7 describes for the 1994 tree; a `notes` on the
`pyrgocystis` node saying the list is assembled from comparative prose (with
the page) would make the editorial act visible.

**"Genotypus" as the printed word for type species.** p. 15: "sardesoni
BATHER 1915, Genotypus" — an older German nomenclatural term, captured only
as the `type: true` flag with no record of the term itself. Minor, but an
instance of the general pattern (roadmap A5/D1 "`roleAsPrinted`") of printed
terminology being replaced silently by the enum value.

**Same-volume cross-citation, not in-press (relevant to both 1961 papers).**
Dehm's paper cites Rievers' twice: in the Zusammenfassung/Einleitung as a bare
page pointer, "(S.9)" ("as J. Rievers's find... (p. 9)" — no title, no year,
just a page number, meant to be read within the same Heft); and in the
Schriftenverzeichnis (bibliography) as a full, already-resolved citation:

> "Rıevers, J. †, 1961: Eine neue Pyrgocystis (Echin., Edrioasteroidea) aus
> den Bundenbacher Dachschiefern (Devon). — Diese Zeitschr., 9—11. München."

"Diese Zeitschr." = "this journal" — a self-referential citation form for a
paper in the same Heft, by the same publication date (15 März 1961), not an
in-press citation (contrast A6's Bell 1974/1976 case, where the cited work
genuinely postdates the citing one). Both papers were edited into print by
Dehm together (he edited Rievers' paper posthumously from Rievers' 1955
manuscript — see the companion review) so the direction is fixed: Dehm cites
Rievers, and Rievers' text (written by 1955, years before Dehm's analysis
existed) cannot and does not cite Dehm. Neither node captures this
same-volume relationship; the A6 `editorial.source` mechanism is built for a
citation that "cannot resolve as printed," but this one resolves cleanly —
the roadmap doesn't yet have a label for "same-volume, already-resolved,
one-directional" citations, which is worth a note since the gold slice
contains exactly this pattern.

**Parenthetical year without a genus change.** "Pyrgocystis coronaeformis
RıEvers (1961)" (p. 16) uses parentheses around the year alone, not around
author+year, and the genus (*Pyrgocystis*) is unchanged by the subgenus
placement — this is very likely Dehm's own citation style rather than an
ICZN parenthetical-authorship signal (which would apply to a genus change,
not a subgenus addition). Flagged only so it is not mistaken for a coded
convention.

**Commented-out `phylogenies` block.** The file's own `# TODO: I'm not sure
where the phylogeny came from?` on the disabled block is itself an
uncertainty flag the data editor already left; nothing in the printed text
(prose discussion only, pp. 16–17, no diagram) supports reinstating it as
printed.

## 4. Source record check

`sources.yaml`'s `1961_dehm` record has one discrepancy: `pages: [12, 17]`.
The printed running head is "1, 13—17" throughout the article (confirmed on
every page from 13 to 17); nothing in the volume carries a printed page 12
for this paper — page 11 ends Rievers' article and unnumbered plate leaves
(Tafel 2) follow before Dehm's article opens at page 13. `pages` should read
`[13, 17]`. Title, journal (`mitt` = "Mitteilungen der Bayerischen
Staatssammlung für Paläontologie und historische Geologie," matches
`data/publications.yaml`), volume, `pubDate.year: 1961`, and author (`dehm`)
all match. One further wording note: the record's title, "Über Pyrgocystis
(Rhenopyrgus) nov. subgen. Coronaeformis Rievers...," differs from the
printed title in two small ways — the printed form is "Über Pyrgocystis
(Rhenopyrgus nov. subgen.) coronaeformis Rievers..." (the parenthesis
encloses "nov. subgen." together with the name, and "coronaeformis" is
lower-case as a species epithet).

## 5. Uncertainties

- OCR of the German is largely clean and legible; no readings marked
  "cannot verify" were needed for the passages quoted above.
- Whether the `pyrgocystis` root node's missing `authority` is a deliberate
  A2 omission or simply not yet migrated cannot be determined from the file
  alone — flagged in §2, not resolved.
