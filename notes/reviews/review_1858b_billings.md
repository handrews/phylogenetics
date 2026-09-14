# Review: 1858b_billings

Source: Billings, "On the Asteriadae of the Lower Silurian Rocks of Canada," in
*Figures and Descriptions of Canadian Organic Remains*, Decade III (Geological Survey
of Canada), pp. 75-85, plate VIII.

**Page mapping.** Text file `1858-00-00-p.txt`, PDF page index *N* = printed page
*N-3* (confirmed: index 85→82, 86→83, 87→84, 88→85; the article's own title page,
index 78, corresponds to p. 75, its recorded start page). Printed page numbers are
cited below, not PDF indexes.

## 1. Coverage

| Kind | Status | Example |
|---|---|---|
| Classification skeleton | partly | *Edrioaster* and *Agelacrinites* are fully placed with their species; *Palasterina*, *Stenaster*, *Petraster*, *Tæniaster* are entered as bare genus nodes with none of their species |
| New taxa | partly | The four new genera (*Stenaster*, *Petraster*, *Tæniaster*, plus the replacement name *Edrioaster*) are flagged `new`; none of the seven new or recombined species under them (see §3) is entered at all |
| Type species | none | No type-species designation is printed or captured (see 1857 review; same era) |
| Synonymy lists | partly | *Edrioaster*'s and *Agelacrinites Dicksoni*'s basionym citations to the 1857 report are captured as `synonyms`; the five recombinations under *Stenaster*, *Petraster* and *Tæniaster* (each also citing its 1857 basionym, e.g. "Palasterina rigidus, ... 1856, page 291") are not captured at all, because the species nodes themselves are missing |
| Material/specimens | none | "Collector.—E. Billings" / "Collector.—J. Richardson" printed for every species; not captured |
| Occurrences | none | "Locality and Formation.—" printed for every species; not captured |
| Illustrations | partly | Captured in full for *Edrioaster Bigsbyi* (Plate VIII, figs. 1, 1a, 2, 2a) and *Agelacrinites Dicksoni* (Plate VIII, figs. 3, 3a, 4, 4a), matching the plate explanation on the unnumbered plate-VIII page exactly; not captured for any of the missing *Stenaster*/*Petraster*/*Tæniaster* species, which have their own plate IX/X figures |
| Diagnoses | none | Full generic-characters paragraphs are printed for *Edrioaster*, *Stenaster*, *Petraster*, *Tæniaster* (e.g. p. 82, *Edrioaster*'s "Generic Characters.—Body sessile, circular, discoid..."); none is captured |
| Phylogeny | not applicable | Prose only; the tentative "sub-order Edrioasteridae" grouping is captured as a second `taxonomies` entry, which is the right mechanism for a hedged classification, not a phylogeny |

The paper's real content is a comprehensive revision: it renames *Cyclaster* to
*Edrioaster* (homonymy), and recombines five of the six other 1857 Asteriadae species
into three brand-new genera. Only the *Edrioaster*/*Agelacrinites* half of that revision
is in the tree; the *Stenaster*/*Petraster*/*Tæniaster* half — three new genera with
full descriptions, plates, and explicit basionym citations — is represented only as
four bare, childless genus nodes plus one leftover `palasterina` node. This is a
substantial coverage gap for the paper's own main achievement, not an error (G9): the
genus-level skeleton is there, the species-level recombinations are not yet entered.

## 2. Correctness

17 taxon nodes in the tree (5 bare genus stubs, `edrioaster` with 1 child, `agelacrinites`
with 1 child, plus the second, "speculative," tree's 4 nodes). All nodes present were
checked; none is a placement or attribution error. One note and one taxon-identity
issue are flagged below.

| Node | Printed (page) | Verdict |
|---|---|---|
| `edrioaster`, `pages: 82`, `new: true` | "Genus EDRIOASTER, Billings." (p. 82) | Match |
| `edrioaster.synonyms[0]` → `cyclaster_billings_1857`, pages 292 | "(Genus Cyclaster, Geological Survey of Canada, Report, 1856, page 292.)" (p. 82) | Match |
| `bigsbyi_billings_1857` (under `edrioaster`), `pages: 82` | "VIII. Edrioaster Bigsbyi, Billings." heading is on p. 82; description continues to p. 83 | Match (heading page); description in fact spans 82-83 |
| `bigsbyi_billings_1857.illustrations`: plate 8, figs 1, 1a, 2, 2a | "EXPLANATION OF Figures. Plate VIII. Figure 1... la... 2... 2a." (p. 83); confirmed again on the separate plate-VIII list page ("EDRIOASTER BIGSBYI (page 82)") | Match |
| `bigsbyi_billings_1857.synonyms[0]` → `cyclaster_billings_1857`, pages 293, `parents: cyclaster_billings_1857` pages 292 | "(Cyclaster Bigsbyi, Geological Survey of Canada, Report, 1856, page 293.)" (p. 82) | Match |
| `agelacrinites`, `pages: 84`, `notes: "No separate genus description."` | "AGELACRINITES Dicksoni, Billings." (p. 84) with no preceding genus-level "Generic Characters" paragraph, exactly as in the 1857 printing | Match |
| `dicksoni_billings_1857` (under `agelacrinites`), `pages: 84` | Heading on p. 84; description continues to p. 85 | Match (heading page); description spans 84-85 |
| `dicksoni_billings_1857.illustrations`: plate 8, figs 3, 3a, 4, 4a | "EXPLANATION oF Figures. Plate VIII... Figure 4... 4a... 3... 3a." (p. 84); confirmed on the plate-VIII list page ("AGELACRINITES Dicksoni (page 84)") | Match |
| `dicksoni_billings_1857.synonyms[0]`, pages 294 (no `taxon` key, same species) | "(A. Dicksoni, Geological Survey of Canada, Report, 1856, page 294.)" (p. 84) | Match |
| `palasterina`, `notes: "As defined by Mr. Salter, 1857"` | Genus attributed by Billings to a paper by "Mr. Salter" in Silliman's Journal, Nov. 1856, quoted verbatim on p. 75 (see §3) | Match in substance, though see the taxon-key/identity issue below |
| `edrioasteridæ-suborder`, `pages: 85`, flags `questionable`, `provisional`, `new` | "...it is probable that they will be arranged as a sub-order, for which the name Edrioasteridæ would be appropriate..." (p. 85) | Match — the hedge is real and heavily qualified; see §3 for the exact wording |
| `edrioaster`, `agelacrinites`, `hemicystites` under `edrioasteridæ-suborder`, each `provisional` | "...all such genera as Edrioaster, Agelacrinites and Hemicystites, belong to a very different division..." (p. 85) | Match |

### Taxon-identity issue (not a tree error, but affects correctness of the underlying data)

`palasterina` (the key used in this tree, no æ ligature) resolves to a **separate,
unlinked** `taxa.yaml` record (`name: Palasterina, auth: [mccoy], year: 1851`, no
`altSpellingOf`), distinct from the properly-linked pair `palaeasterina`
(`auth: [mccoy], year: 1851`) / `palæasterina` (`altSpellingOf: palaeasterina`) used
elsewhere (e.g. by the `1857_billings` tree, which keys this same genus as
`palæasterina`). Three identity records for one genus, one of them an orphan — a
correctness problem in `taxa.yaml`, surfaced by comparing the two Billings trees rather
than by anything wrong in either tree individually.

## 3. Cases for the data model

**A junior homonym forces a replacement name, argued with a priority date.** Page 82:
"In my report for 1856 this genus is called Cyclaster; but I find that this name had
been a short time previously given to a genus of sea-urchins by M. Cotteau, and it is
therefore necessary now to provide a new one... (See Catalogue des Echinides Fossiles
des Pyrénnées. Par MM. Leymerie et Cotteau. Bulletin de la Société Géologique de France,
18 Février 4 [sic] 17 Mars 1856.) This number of the Bulletin was published in March
1857, but my Report was not issued until the autumn following." This is a full nom. nov.
argument with its own priority reasoning (Cotteau's *Cyclaster* predates Billings's by
publication date, even though both carry a nominal "1856"/"1856" date on their host
volumes) — exactly the kind of printing/dating problem the roadmap already tracks under
A8/A11, but here it is the reason *for* a replacement name rather than a resolution of
which printing a citation fits. `cyclaster_billings_1857` already carries `homonym:
true` and `cyclaster` (Cotteau's) has its own `auth: [Cotteau], in: [Leymerie,
Cotteau], year: 1856` — the identity side is modeled; the *argument* (whose 1856 was
first, stated by Billings himself with the specific publication dates) exists only in
this printed paragraph, quoted here, and isn't captured anywhere.

**A genus's authorship is credited to a *description*, not a first name-bearing act,
and the source doubts the description.** Page 75, Billings quotes his own 1857
introduction verbatim: "The species of Star-fishes in the collection appear to be
referrable to the genera proposed by Mr. Salter at the meeting of the British
Association, in August last. I have seen no other description of these genera than
that given in Silliman's Journal of November, 1856, which is as follows:— 'PALÆASTER.—
Without disc, avenues deep.' 'PALÆASTERINA.—Pentagonal, disc moderate.' 'PALÆOCOMA.—No
disc, avenues very shallow.'" Then, new in 1858: "Since then Mr. Salter has published
full details of the above and some other genera, and I have also examined some of the
species described by him and Prof. Forbes." So Billings's own attribution of
*Palasterina* (and *Palaeaster*, *Palaeocoma*) is to Salter, 1856, sourced from a
one-line diagnosis in a popular science journal, itself now superseded by a fuller 1857
paper Billings cites only by mention, not by full reference. None of this is capturable
as a clean `auth`/`year` on the tree node as it stands — it's exactly a `citedAs`-plus-
`notes` case, and the current `notes: "As defined by Mr. Salter, 1857"` compresses the
1856-diagnosis/1857-details distinction into one year, which the quoted prose does not
support (Salter's fuller "1857" details are for genera Billings does not fully cite by
page).

**A wholesale genus-level recombination, argued from a redefined character.** Pages
77-79: Billings erects *Stenaster* new for two species he had put in *Palæasterina* in
1857 ("As it has been suggested that the two species hereinafter described should be
referred to Palæaster, I give the following figure of that genus in order to show the
difference," p. 78, followed by a two-point anatomical argument distinguishing oral vs.
adambulacral vs. marginal plates), and similarly erects *Petraster* and *Tæniaster* for
the remaining species, each with its own basionym citation in the species heading, e.g.
p. 79: "V. PETRASTER RIGIDUS, Billings. (Palasterina rigidus, Geological Survey of
Canada, Report, 1856, page 291.)" This is the paper's central taxonomic act and none of
it is yet in the tree (see Coverage, above) — it is a clean case for entering the five
missing species nodes with `parents` pointing at their 1857 combinations, exactly the
mechanism the roadmap's B1 table already describes for `parents`.

**Gender disagreement between an original combination and its citation of itself.**
Page 79: "IV. STENASTER PULCHELLUS, Billings. (Paleaster pulchella, Geological Survey
of Canada, 1856, p. 292.)" — the recombined name is masculine "pulchellus" but the
basionym citation gives the feminine "pulchella." The 1857 printing itself reads
"PALÆASTER PULCHELLUS" (masculine, matching the current taxon key
`pulchellus_billings_1857`). One of the two printings has a gender-agreement slip;
cannot verify which without the original page image, but the discrepancy is worth
recording once the species is entered.

**Correction of a mixed-up specimen attribution, stated as regret.** Page 83: "I
regret, that, in consequence of mistaking the meaning of Prof. E. Forbes' remarks on
the genus Agelacrinites in his memoir on the British Cystideae, I supposed this
[*Edrioaster Bigsbyi*] to be the specimen discovered by Dr. Bigsby, and accordingly gave
it his name. Since then I have seen Dr. Bigsby's specimen, and find it to be A.
Dicksoni. It is too late now to change the names." This is Billings admitting, in the
very paper that redescribes both species, that the two specimens' names and their
namesake specimens got crossed in 1857 and that he is declining to fix it. Nothing on
either the `bigsbyi_billings_1857` or `dicksoni_billings_1857` node records this; it
would be a `notes` entry on one or both (H table: "a claim about another work's error,"
except here it is the same author admitting his own).

**The Edrioasteridae hedge, quoted in full.** Page 85: "None of the Cystideae have
ambulacra whose pores penetrate through the covering of the body, and therefore all
such genera as Edrioaster, Agelacrinites and Hemicystites, belong to a very different
division of the Echinodermata. When we know more of their structure it is probable that
they will be arranged as a sub-order, for which the name Edrioasteridae would be
appropriate, as it would suggest their sessile condition on the one hand, and on the
other their affinity to the Asteriadae." The rank word given is "sub-order." The
hedging is layered three deep — "when we know more," "it is probable," "would be
appropriate" — this is a suggestion for a future act, not an assertion of one, and yet
it is universally cited as the protologue of Edrioasteroidea. The tree's
`edrioasteridæ-suborder` node already carries `questionable`, `provisional`, and `new`,
which is a reasonable three-flag reading of this, but no single existing flag means
specifically "the source itself frames this as a suggestion, not a name it is now
using." That is closest to A9's "in preparation" treatment (a name whose availability
is exactly as strong as the source's own hedge) but is a new shape: a name proposed
*and* used as a working label (Billings does treat "Edrioasteridae" as the group's name
in the very sentence that hedges it) while explicitly disclaiming certainty about the
rank. Worth a second source before adding structure (roadmap's own rule for H), but
flagged here because task assignment specifically asked for it.

## 4. Source record check

`sources.yaml` block for `1858b_billings`: `title: "On the Asteriadæ of the Lower
Silurian Rocks of Canada"`, `journal: fig-desc-can`, `volume: III`, `pages: [75, 85]`,
`pubDate.year: 1858`, `authors: [billings]`. All of it matches: the printed title page
reads "On the ASTERIADÆ of the Lower Silurian Rocks of Canada. By E. Billings, Esq.,
F.G.S." (p. 75, the recorded start page); the article's last page (85) carries the
Edrioasteridae paragraph quoted above and the section ends there; the accompanying
plate is headed "DECADE 3. Pl. 8," confirming Decade III.

## 5. Uncertainties

- OCR of the æ ligature is unreliable ("PALiEASTERINA" / "PALJEASTERINA" / "Palasterina"
  all appear for the same word across the two papers); see the taxon-identity finding
  in §2.
- "Paleaster pulchella" vs. "PALÆASTER PULCHELLUS" (§3): cannot verify which printing
  has the gender-agreement slip without the original page image.
- The plate citations for *Stenaster*, *Petraster*, *Tæniaster* species (Plates IX and
  X) were read from the running text, not independently cross-checked against a
  separate plate-explanation page the way Plate VIII was; treat as "printed, not
  independently confirmed."
