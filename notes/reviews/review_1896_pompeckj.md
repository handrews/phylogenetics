# Review: Pompeckj 1896, "Die Fauna des Cambrium von Tejřovic und Skrej in Böhmen"

Page mapping: printed page = PDF index − 49 (checked against running heads/page
numbers at PDF indexes 551, 552, 558 and 561 → printed 502, 503, 509, 512; holds
across the whole echinoderm section). All page citations below are printed
pages. Title, journal, volume, Heft and year are confirmed from the running
head "Jahrbuch d. k. k. geol. Reichsanstalt, 1895, 45. Band, 3. Heft." printed
on every page of the article, and from the table of contents (PDF index 6),
OCR: "Die Fauna des Oambrium von Tejrovice und Skrej in Böhmen. Von J. F.
Pompeckj. Mit 5 [lithographirten] Tafeln (Nr. XIII—XVII)..." ("Oambrium" is an
OCR misread of "Cambrium"; the running heads throughout read "Cambrium"
correctly). The TOC gives the article's start page as 495.

## The erection of the genus and species

Heading (p. 505): **"Stromatocystites nov. gen."**

Erecting sentence (p. 505): "Diese Unterschiede, auf welche bei der
Beschreibung der einzigen Art des böhmischen Cambrium eingegangen werden
soll, bestimmen mich, dieses vorliegende Material als einer neuen Gattung
zugehörend aufzufassen, welche ich Stromato[c/e]vstites nenne." — OCR reads
the name here as "Stromatoevstites"; the heading and every other occurrence in
running text read "Stromatocystites" cleanly, so the intended reading is
certain, but this one character string ("evstites" for "cystites") cannot
itself be verified from the OCR.

Diagnosis, first sentence (p. 505): **"Kelch ungestielt, vieltäfelig, niedrig,
von ungefähr fünfseitigem Umriss."** ("Calyx unstalked, many-plated, low, of
approximately five-sided outline.") The diagnosis continues for four more
sentences (pore pattern, five ambulacra, mouth, anal pyramid) — none of it is
captured in the tree's `diagnosis` field (none exists on any node in this
file).

Species heading (p. 506): "Stromatocystites pentangularıs nov. spec." (OCR:
dotless-ı in "pentangularıs"; not a spelling variant, an OCR artifact —
confirmed by the clean "pentangularis" spelling used everywhere else,
including the plate caption).

**Type fixation.** No type-species statement ("Typus", "Genotypus") anywhere
in the genus or species treatment. The genus is monotypic in this paper (only
*S. pentangularis* is assigned to it), so the type is fixed only by
subsequent monotypy — not stated explicitly by Pompeckj.

**Material cited.** No catalogue/specimen numbers anywhere in the
Stromatocystites treatment. For the species: "Eine beträchtliche Anzahl von
Abdrücken der Oberseite und Unterseite der Kelche, sowie einzelne
Bruchstücke von Steinkernen liegen vor" (p. 506, "a considerable number of
impressions... lie before me"), and under "Vorkommen" (p. 507): "In der
(Kalk-)Sandsteineinlagerung der Lokalität „Pod trnim" bei Tejrovie (40
Exemplare)" — 40 specimens, no repository named for this species specifically.
The paper's introduction (p. 496) lists the general pool of museums the whole
paper's material came from (k. k. geolog. Reichsanstalt Wien; geolog. and
palaeontolog. Institute of Vienna University; on-loan pieces from the
Naturhistorisches Hofmuseum Wien, several Prague institutions, the Böhmisches
Landesmuseum, and private collections of M. Dusl and W. Kuthan) but assigns no
piece of that list to Stromatocystites by name.

**Figures/plate:** "Taf. XIII, Fig. 1—6" (p. 506), confirmed by the plate
caption (PDF index 683, printed unnumbered plate-explanation leaf): "Erklärung
zu Tafel XII[I]. Stromatocystites pentangularis nov. gen. nov. spec. pag. 506
[12]." (OCR drops the final "I" of "XIII"; the caption's own content — six
figures matching Fig. 1a–6b, then Lichenoides priscus Fig. 7–8, then
"Trochoeystites? sp." Fig. 9–11 — is the same plate the main text calls
XIII, so the plate number is not actually in doubt despite the OCR). The
caption also states the repository for the plate's originals: "Das Original
zu Fig. 7 [Lichenoides] befindet sich im palaeontolog. Institut der
Universität Wien. Die übrigen Originale gehören der k. k. geolog.
Reichsanstalt Wien" — i.e. the Stromatocystites and Trochocystites-plate
originals are at the k.k. geologische Reichsanstalt, Vienna. This is the one
place in the paper that ties any Stromatocystites specimen to a named
repository, and it is not in the tree.

**Horizon and locality:** "(Kalk-)Sandsteineinlagerung der Lokalität „Pod
trnim" bei Tejrovie" — a limestone-sandstone interbed at the "Pod trnim"
locality near Tejřovice, within the green Paradoxides-shale sequence
(Barrande's Etage C / C-c₂ of the Bohemian geologists, per the stratigraphic
column on p. 497); "Mittleres Cambrium" ("Middle Cambrium") per the plate
caption. None of this is captured (see coverage, below).

**Placement in a higher group:** Pompeckj gives Stromatocystites no family or
order. The only higher heading above any genus in this part of the paper is
the bare, unranked heading **"Cystoidea."** (p. 502), directly followed by
genus headings with no intervening rank. Pompeckj explicitly declines to
place the genus relative to its closest comparator, *Mesites* Hofmann emend.
Nikitin: "Nach dem mir vorliegenden Materiale der böhmischen Form kann ich
dieselbe nicht mit Mesites vereinigen, wenn ich sie auch für eine verwandte
der russischen Gattung halten muss" (p. 508) — "I cannot unite it with
*Mesites*, though I must consider it a related [genus] of the Russian one."

## Coverage, one line per kind

- **Classification skeleton:** all — the four Cystoidea genus/species pairs
  Pompeckj treats (Lichenoides priscus, Trochocystites bohemicus, Mitrocystites
  sp., Stromatocystites pentangularis) are all present, matching his own
  summary count "4 Cystoideen" (p. 564).
- **New taxa:** partly — genus and species `new: true` are flagged for
  Stromatocystites/pentangularis, and `mitrocystites-sp_pompeckj_1896` is
  flagged `new`, but a fourth new-taxon usage on this same plate,
  "**Trochoeystites? sp.**" (= Trochocystites? sp., isolated plates, p. 503,
  Taf. XIII Fig. 9–11), is not in the tree at all (see Cases, below).
- **Type species:** none — no `typeFixation`/type marker on any node; not
  applicable to record since Pompeckj states none, but the monotypy fact
  itself is not noted either.
- **Synonymy lists:** partly — the Barrande(Waagen) 1887 synonymy quotes for
  *Lichenoides priscus* and *Trochocystites bohemicus* are captured in
  `notes`; the tentative synonymy of *Cystidea concomitans* Barr. with
  *Stromatocystites pentangularis*, stated three times in the paper, is not
  captured anywhere (see Cases).
- **Material:** none — no `specimens` field anywhere in the file; specimen
  counts ("40 Exemplare", "acht Abdrücke") and the one named repository
  (k. k. geolog. Reichsanstalt Wien, for the Taf. XIII originals) are absent.
- **Occurrences:** none — both new-taxon nodes carry a `# TODO: Occurrences`
  comment, and the two pre-existing species (Lichenoides priscus, Trochocystites
  bohemicus) have no occurrence data either, despite each having a printed
  "Vorkommen" paragraph with named localities.
- **Illustrations:** partly — captured only for the two new taxa
  (`mitrocystites-sp`: plate XIV, fig. 1–2; `pentangularis`: plate XIII, fig.
  1–6, both correct against the text and the plate caption); not captured for
  *Lichenoides priscus* (p. 502: "Taf, INT, „Eig, 7,8" — cannot verify this OCR,
  but the plate caption confirms Taf. XIII, Fig. 7–8) or *Trochocystites
  bohemicus* (which has no figure of its own in the main text, though the
  associated indeterminate plates are figured at Taf. XIII, Fig. 9–11).
- **Diagnoses:** none — the full generic diagnosis of Stromatocystites (five
  sentences, p. 505, quoted above in part) is not in any `diagnosis` field.
- **Phylogeny:** not applicable — the paper contains no phylogeny/cladogram
  section; there is no `phylogenies` block in the file, correctly.

## Correctness of what IS captured

| node | printed (page) | verdict |
|---|---|---|
| `cystoidea` (p. 502) | heading "Cystoidea." with no rank word | match (identity/placement correct; see Cases for the rank-word point) |
| `lichenoides` (p. 502) | "Lichenoides Barrande." | match |
| `priscus_barrande_1846` (p. 502) | "Lichenoides priscus Barr." + 1887 synonymy quote | match; synonymy text in `notes` matches the printed citation (OCR-adjusted) |
| `trochocystites` (p. 503) | "Trochocystites Barrande." | match |
| `bohemicus_barrande_1887_trochocystites` (p. 503) | "Trochocystites bohemicus Barr." + 1887 synonymy quote | match |
| `mitrocystites` (p. 504) | "Mitrocystites Barrande." | match |
| `mitrocystites-sp_pompeckj_1896` (p. 504) | "Mitrocystites (?) nov. spec.", `openTaxon`+`provisional`+`new`, illustrations Taf. XIV Fig. 1–2 | match — see Cases for the exact form of the hedge |
| `stromatocystites` (p. 505) | "Stromatocystites nov. gen.", `new: true` | match |
| `pentangularis_pompeckj_1896` (p. 506) | "Stromatocystites pentangularıs nov. spec.", `new: true`, illustrations Taf. XIII Fig. 1–6 | match |

9 of 9 nodes match the printed text on identity, rank, placement, flags and
attribution. No mismatches found. Two items above are marked "cannot verify"
for an OCR reading that does not affect the node's correctness (Lichenoides
priscus's own figure citation on p. 502; the "Stromatoevstites" spelling
variant on p. 505) — neither is a discrepancy in the tree, both are limits of
the scan.

## Cases for the data model

- **A genus-level "(?)" hedging generic placement, distinct from the C table's
  "?" before a name.** The Mitrocystites heading reads **"Mitrocystites (?)
  nov. spec."** — a question mark in parentheses *after* the genus name, not
  before it. Pompeckj states explicitly what it hedges: "Das Vorkommen einer
  solchen seitlichen Oeffnung kann die Zuzählung der vorliegenden Form zu
  Mitrocystites Barr. als bedingt richtig erscheinen lassen" (p. 504) — the
  assignment to *Mitrocystites* is only "conditionally correct." This is
  squarely the C table's `provisional` axis ("placement... tentative"), and
  the tree's `provisional: true` is the right mapping, but the printed form —
  "(?)" bracketed after the genus, not a bare "?" before it — is a variant of
  the convention worth naming for future OCR/entry work, since it is easy to
  misread as doubt on the species (`questionable`) rather than the genus
  assignment.

- **An uncaptured hedged synonymy, restated three times.** Pompeckj proposes,
  hedged, that Barrande's *Cystidea concomitans* is the same species as his
  new *Stromatocystites pentangularis*:
  - p. 507: "Cystidea concomitans Barr. — von Skrej ohne nähere
    Fundortsbezeichnung — scheint auf schlecht erhaltene Reste der eben
    beschriebenen Form begründet zu sein" ("...seems to be based on poorly
    preserved remains of the form just described").
  - p. 585 (§IV, faunal summary): "Stromatocystites pentangularis... ist
    wahrscheinlich (Cystidea concomitans Barr.) auch bei Skrej... vertreten"
    ("...is probably also represented... at Skrej [as C. concomitans]").
  - p. 590: "ebensowohl auch Stromatocystites pentangularis (Cystidea
    concomitans Barr.)".

  This is a `synonyms` entry (Barrande's name, at the rank of species, hedged)
  that is absent from the tree; the source's own repeated hedging language
  ("scheint... zu sein", "wahrscheinlich") is exactly the printed-hedge case
  the roadmap's C axis and B16 are built for, and the `Cystidea` spelling is
  itself of interest ("Cystidea" vs. the class-level "Cystoidea"/"Cystidea"
  identity question already on the `cystoidea`/`cystidea` records — this is a
  different, species-level "Cystidea", i.e. Barrande's genus name, not to be
  confused with Buch's class name).

- **An uncaptured open-nomenclature usage tied to disarticulated plates
  (G9).** Under *Trochocystites bohemicus* (p. 503), Pompeckj describes
  isolated thick plates from Slapy, Dlouhá hora and above Luh that he cannot
  assign with confidence: "Sehr wahrscheinlich gehören diese Platten einer
  Cystoideenform an und möglicherweise dürften sie von einer
  Trochocystiten-Art herrühren" ("very probably... possibly... of a
  Trochocystites species"). These same plates get their own line in the plate
  caption (p. 683/unnumbered): **"Trochoeystites? sp. pag. 503 [9]"** (OCR for
  "Trochocystites? sp."), with its own locality ("Hegerhaus Slapy
  (Buchavä-Steinbruch)") and figures (Taf. XIII, Fig. 9–11) distinct from
  *T. bohemicus*'s own figures (which the main text does not illustrate at
  all). This is disarticulated-plate open nomenclature exactly matching the
  scope G9 flags as belonging in this project ("the earliest echinoderm
  records are plates"), and it is a fourth taxon-like entity in this paper
  that has no node — the tree's genus-level "4 Cystoideen" count from
  Pompeckj's own summary (p. 564) does not include it either, so Pompeckj
  himself treats it as material under *Trochocystites*, not a fifth species;
  still, as a distinct plate/figure/locality unit with its own open-nomenclature
  label it is a candidate `openTaxon` child of `trochocystites`, parallel in
  shape to `mitrocystites-sp_pompeckj_1896`.

- **A class-rank heading printed with no rank word (G8).** "Cystoidea."
  (p. 502) carries no rank word in the original, exactly the G8 pattern; the
  Class rank the data model assigns comes entirely from the `cystidea` taxon
  record (`cystoidea` is `altSpellingOf: cystidea`, `rank: Class`, authority
  Buch 1844), not from anything Pompeckj printed. Every other higher-taxon
  heading in the paper follows the same convention (bare "Hydrozoa.",
  "Bryozoa.", "Brachiopoda." with sub-heading "Inartieulata." [Inarticulata],
  none ranked), so this is the paper's systematic style throughout, not a
  one-off.

- **A genus record whose background note (unrelated to this paper) could be
  misread as about this paper.** `taxa.yaml`'s `trochocystites` record carries
  a `notes` field calling the name a "Nomen nudum, used (or re-defined?) for
  T. cannati, which is actually an edrioasteroide, Cambraser cannati" — none
  of that concerns Pompeckj 1896, where *Trochocystites* is used exactly as
  Barrande (1887, posthumous, ed. Waagen) established it, with *T. bohemicus*
  as its type-by-original-designation species. No fix needed; noted only
  because the note reads at first as if it might undermine this tree's usage,
  and it does not.

- **A repository statement recoverable only from the plate caption.** As
  noted above, the plate-explanation leaf (not the main descriptive text) is
  the only place the paper names a repository for the Stromatocystites/
  Trochocystites plate material ("k. k. geolog. Reichsanstalt Wien"). Any
  future `specimens`/repository capture for this paper needs the plate
  captions, not just the species accounts.

## Source record check

`1896_pompeckj` in `data/sources.yaml`: title, journal (`jahrbuch` →
"Jahrbuch der Kaiserlich-Königlichen Geologischen Reichsanstalt"), volume 45,
`notes: 1895 annual, but publication year is 1896`, `pubDate.year: 1896`,
author `pompeckj` (→ Josef Felix Pompeckj) all match the printed running head
("Jahrbuch d. k. k. geol. Reichsanstalt, 1895, 45. Band, 3. Heft.
(J. F. Pompeckj.)") and the table of contents. No `pages` field is present on
the source record; the article's own start page (495, from the TOC) is not
recorded there, consistent with the rest of this dataset's practice of not
always carrying a start page on the source block — not a discrepancy.

## Uncertainties

- OCR readings marked "cannot verify" above: "Stromatoevstites" for
  Stromatocystites (p. 505, prose); "pentangularıs" (dotless ı, p. 506
  heading — reads consistently elsewhere so the name itself is not in doubt,
  only this glyph); "Taf, INT, „Eig, 7,8" as the figure citation under
  *Lichenoides priscus* (p. 502 — the plate caption independently confirms
  Taf. XIII, Fig. 7–8, so the genus/species identity is not in doubt, only
  this particular OCR string); "Erklärung zu Tafel XII." on the plate-caption
  leaf, which the caption's own content shows must be Tafel XIII.
- A cross-reference at p. 589 cites "Taf. XVI, Fig 1" for the same
  *Mitrocystites (?) nov. spec.* specimen the main text (p. 504) and the tree
  both cite as Taf. XIV, Fig. 1–2. This is almost certainly an OCR misread of
  "XIV" as "XVI" (not located: the plate-caption text for Taf. XIV itself was
  not in the pages fetched for this review) — cannot verify which reading is
  correct without the plate image or the Taf. XIV caption leaf.
- The full plate captions for Taf. XIV (Mitrocystites) were not located within
  the page ranges reviewed; only the Taf. XIII caption (covering
  Stromatocystites, Lichenoides and the indeterminate Trochocystites? plates)
  was found (unnumbered leaf, PDF index 683).
- Pages 633–660 and 683 were sampled for Cystoidea-relevant passages
  (faunal-distribution list, the *Cystidea concomitans* restatements, the
  Trochocystites-in-France/Spain biogeography discussion, and the plate
  caption) rather than read exhaustively; the surrounding trilobite/brachiopod
  material in that range was not reviewed since it falls outside echinoderms.
