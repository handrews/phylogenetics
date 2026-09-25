# Claims: the vocabulary the extractor implements

A claim is one statement a source prints about one name, carried with its
provenance. The claim table is generated from the tree files by
`scripts/claims.py` (the logic is `phylohist/claims.py`, over the `Tree`
walk), deterministically: the same YAML always yields the same claims, in
the same order, nothing is merged across sources, and nothing is normalised
beyond resolving keys. The output is committed: `claims/<source>.jsonl`,
one claim per line for every tree file, and `claims/manifest.json`; CI
reruns the script and fails on a stale directory, so every data commit
regenerates it. This document fixes what a claim is and which tree fields
produce which claims; the eval questions in `eval/` are written against
it, and `tests/test_claims.py` checks that they still match. Field
meanings are the roadmap's (`semantics-roadmap.md`); item codes below
point there.

## The record

Every claim carries:

| field | value |
|---|---|
| `id` | `<source>:<path>:<kind>[:<n>]`. `<path>` is the node's position in its tree file as the loader computes it: the taxonomy or phylogeny index, then each step down (`children/2`, `synonyms/0`, `non/1`, `removed/0`, `parents/0`, `moved`, `corrected`, `substituted`, `or/0`). `<n>` disambiguates several claims of one kind from one node (a node with three `specimens` roles yields three `material` claims). Ids are stable as long as the file is not reordered; the tree keeps printed order, so reordering is a data change. |
| `kind` | one of `usage`, `placement`, `acceptance`, `act`, `rejection`, `material`, `diagnosis`, `secondhand`, `editorial` |
| `source` | the tree file's source key |
| `path` | the node's position and pointer, `0/children/0/children/0`, the same string the id carries |
| `tree` | `taxonomy`, or a phylogeny's `treeType`; a phylogeny's `notes` ride along as `treeNotes` |
| `pages` | the node's `pages` as written. A node without `pages` takes the nearest ancestor's along the `children` axis only, and the claim then carries `pagesInherited: true`. Entries on any other axis never inherit. On a cited entry (a `synonyms` or `non` entry, or the earlier state of a name under `translated`, `corrected`, `substituted`, `moved` or `removed`) `pages` and `illustrations` locate the cited usage in the cited work, whether written flat or inside an `authority` block, so they appear as `citedPages` and `citedIllustrations` and the claim has no `pages` of its own. |
| `subject` | the resolved taxon key the claim is about |
| `printed` | the printed form on that line: `citedAs` verbatim, and `auth`, `year`, `in` as written (A1, A12). Absent `auth` means "as the record"; the claim says so with `printedAttribution: as-record`. |
| `audit` | the source's `audit.state`; `coverageKind`, the coverage kind the claim counts under (`skeleton` for usage, rejection and a taxonomy placement, `phylogeny` for a placement in a phylogeny, `synonymy` for acceptance, `newTaxa`/`types` for the matching acts, `material`/`occurrences`/`illustrations` by material kind, `diagnoses`); and `coverage`, the declared value for that kind when the source declares one |
| `editorial` | the node's `editorial` block, copied through |
| `inferred` | `true` when the editorial block says the editor supplied the field this claim comes from (`inferred: true`, or a list naming it). The claim is then the editor's, not the paper's, and the manifest does not count it |
| `erroneous` | `true` when the editorial block's `corrections` touch the field this claim comes from. The claim stays the paper's and is counted; what the editor reads instead is in `corrected` |
| `printedErrors` | the printed attribution fields (`auth`, `year`, `in`, `citedAs`, `authority`) the editorial block's `corrections` touch |
| `corrected` | the attribution as the editor reads it, when the editorial block gives `corrections`: the same keys as the printed attribution (`printed`, `citesSource`, `citedPages`, ...) for whichever differ. The corrections are a JSON Merge Patch over the node; only the attribution is derived here |
| `notes` | the node's `notes`, copied through verbatim |

A claim whose subject is a placeholder (an `openTaxon` key) carries
`placeholder: uncertain | unnamed | open` from the key's form (C4), so a
bin is never reported as a taxon and an unnamed group is not reported as
a bin. A placement whose parent is a placeholder carries the parent's
kind as `parentPlaceholder`.

Attribution appears in trees in two shapes and both produce the same
`printed` fields: the flat form (`auth`, `year`, `in`, `citedAs`) and the
nested form (`authority: {source, pages, illustrations}`), which also
resolves the citation to a source record and carries the cited pages. When
the nested form names a source, the claim adds `citesSource`, `citedPages`,
`citedIllustrations` and `citedAttributedTo` as present.

## The kinds

### `usage`

Emitted for every node that cites a name: `taxon`, `openTaxon`, `cfTaxon`,
`affTaxon`, and for every `synonyms`, `non`, `removed`, `parents` and `or`
entry. Fields added:

- `form`: which field carried the name; `bracket` for a cladogram's
  bracket label.
- `spelling`: the key used on the line. Spellings are undirected (B28); the
  claim never substitutes the record the key points at.
- `axis`: how the node hangs off its parent (`children`, `synonyms`,
  `removed`, `parents`, …; `root` for a tree's top node).
- `target`: for `cfTaxon` and `affTaxon`, the compared name (C1).
- `sensu`: `stricto`, `lato` or `emendato` when the node prints the
  qualifier.
- A `synonyms` or `non` entry with no name field of its own is a usage of
  the node's own name by the cited source (the 2020 tree's stacked
  citations of *grayae* are this shape); it carries `ownName: true`.

### `placement`

Emitted for every child under its parent in a taxonomy. Fields added:

- `parent`: the nearest named ancestor's key; `position`: index among the
  siblings, since the tree keeps the printed order. Under an unnamed clade
  node the parent is null and `parentPath` points at the node; when the
  named ancestor is further up, `parentPath` says so too.
- `rank`: the record's rank today. When the tree carries a printed rank
  word in `citedAs` or `notes`, `rankAsPrinted` holds it; the rule that
  rank belongs to the tree node is G8, not yet in force.
- Flags copied from the node: `provisional`, `questionable`, `quoted`,
  `pars`, `tentative`, `outgroup`, `stem`; `altPlacements` as a list of
  keys. (`listHedged`, `listComplete` (B16) are not in the schema yet.)

A phylogeny's nesting produces placements too, marked
`tree: cladogram | diagram | other` with the phylogeny's `notes`, and a
`bracket` label is a second placement of the node's name whose parent is
the bracket's key, marked `via: bracket`.

A source can also say where a name does *not* belong. Two printed shapes,
one claim: "we are confining the family Cyathocystidae to Cyathocystis and
Cyathotheca" (Bockelie & Paul 1983, the `removed` list, B5) and "we do not
include them within Cyathocystidae Bather, 1899" (Sumrall et al. 2013,
p. 773). The first is written from the group's side and the second from
the taxon's side, and whether anyone had placed the name there before is
the source's business, not the claim's. Both emit a `rejection`: subject,
`declinedParent`, the printed words. `removed` under a group node and
`moved` on the taxon node are the two spellings (Sumrall et al. 2013
carry `moved: {taxon: cyathocystidae}` on Rhenopyrgidae), and each also
yields its `act`. The tree uses `moved` when the source gives the new
place and `removed` when it gives none, or none worth tracking; a
`moved` name is not also listed as `removed` under its old group.

Placements, closures and the history's counts read taxonomy trees unless
a `trees` parameter says otherwise: the cladograms and diagrams under
`phylogenies` are entered less consistently and are a later concern.

`follows`: the source adopts a placement by citing another work for it
("Edrioasterida sensu Guensburg and Sprinkle (1994)", 2013). A source that
argues a placement from its own evidence is a decider; one that adopts
another's by citation is a follower. The distinction is carried on the
placement claim so that agreement can be counted both ways.

### `acceptance`

Emitted for each `synonyms` entry (the source accepts the cited usage as
this name) and each `non` entry (the source rejects it) (B1). Fields added:

- `stance`: `accepts | rejects`.
- `under`: the node whose name the entry is accepted or rejected under.
- `parents`: the original combination, as the list of keys under the
  entry's `parents` (a genus, or a genus and a subgenus).
- `pars`, `tentative` copied; `ownName: true` when the entry has no name
  of its own.

### `act`

Something this source does to a name. One claim per flag, `actKind` being:

| tree field | `actKind` |
|---|---|
| `new: true` on a named node | `new` (the protologue; F6 checks it) |
| `new: true` on a placeholder | `placeholder` (the source originates the placeholder; C4) |
| `type: true` | `type` (the fixation method joins when B14 lands) |
| `emended: true` or `emended: {by}` | `emended`; `by` and `byPages` when the source follows another work's emendation |
| `translated: true` or `translated: {taxon: y, by?}` | `nomTransl`; `translatedFrom: y` when the earlier rank is named, `by`/`byPages` when another work made the act, `rankVariants` from the records' `altRankOf` links |
| `nudum: true` | `nomNudum` |
| `corrected: {taxon: y}` | `corrected`, `correctedFrom: y`; the node's own name is the corrected form |
| `substituted: {taxon: y}` | `substituted`, `substitutedFor: y`; the node's own name is the replacement name (nom. subst.), `y` the preoccupied or otherwise unavailable name it replaces |
| `moved: {taxon: y}` | `moved`, `movedFrom: y` |
| `removed` entry | `removed`, `removedFrom` the group (the source takes the name out of it; B5), beside the `rejection` |
| `homonym: true` on the record | not a claim: key housekeeping |

A node under `translated`, `corrected`, `substituted`, `moved` or `removed` is the
earlier state of the name as this source cites it: its own `authority`,
`auth`, `year`, `pages` and `illustrations` locate that earlier use, and
it emits a `usage` claim on its axis like any cited entry. The change is
this source's act. `emended` and `translated` are the two acts a source
may follow rather than perform, and `by` (an `authority`) names the work
that performed it.

`corrected` and `substituted` imply the synonymy: the incorrect form and
the replaced name are synonyms of the node's name, and the closure follows
them as it follows `synonyms` entries. A `synonyms` entry repeats the name
only when the source prints a synonymy that lists it, as a revision may;
the synonymy a source prints is still only its `synonyms` and `non`
entries.

### `certainty`

Not a kind of its own. The C-axis markers (`provisional`, `questionable`,
`quoted`, `tentative`, `pars`, `cf.`, `aff.`, `illustration.uncertain`) ride
on the claim they qualify, as fields. No separate table.

### `material`

Emitted for each `specimens` role entry, each `occurrences` entry and each
`illustrations` entry on a node other than a cited entry (see `pages`),
whose illustrations are the cited work's. Fields added: `materialKind: specimen |
occurrence | illustration`, `role` as recorded today (`holotype`,
`paratypes`, `syntypes`, `unknowntypes`, and the occurrence blocks'
`holotypes` and `unspecified`), `ids`, `repository`, and the occurrence or
illustration fields copied verbatim (`occurrence`, `illustration`). An
occurrence's own specimens yield specimen claims too, with `inOccurrence`
giving the occurrence's index; those blocks nest role then repository in
most trees and the other way round in two (Vanuxem 1842, Rievers 1961), so
the role word decides which level is which. The shape follows the YAML as
it stands; when D1 migrates material, only the extractor's material
adapter changes and these claims keep their fields.

### `diagnosis`

Emitted for a node's `diagnosis`, `text` verbatim. It is the one tree
field with a coverage kind (`diagnoses`) and, without a claim, no way to
be counted.

### `secondhand`

A source's statement about what another source did, accurate or not: "P.
octogona … was assigned to Rhenopyrgus by Dehm (1961)" (Holloway & Jell
1983 p. 1004). Fields: `about` (the cited source key), `says` (the act or
placement attributed to it), and `matches`, derived by comparing `says`
with the cited source's own claims (B19); here Dehm's tree does not bear
the statement out. Not emitted from any tree field today; reserved so that
"what did later authors say he did" has a home, and so the derived
comparison feeds the citation-error part of the eval.

### `editorial`

The node's `editorial` block emitted as a claim of its own, so a question
can ask whether a placement is the paper's or the editor's. Fields:
`inferred` (`true`, or the list of inferred fields), `corrections` (a JSON
Merge Patch over the node: every key it touches is printed in error, and
its value is what the editor reads instead; `null` deletes a printed field
that is wrong with nothing known to replace it; an array is restated
whole), `basis`. Bell 1975 cites "Bell, 1974" for a paper that appeared in
1976: corrections delete `auth` and `year` and set `authority.source:
1976_bell.b.m`. The claim it qualifies
carries the same block, so both directions are answerable.

## Derived coverage

`claims/manifest.json` holds, per source record (every key in
`sources.yaml`, whether or not a tree exists: `tree: false` is how "the
paper is recorded but not yet entered" is derived), the declared `audit`,
the counts of claims by kind, by `actKind` and by `materialKind`, the
counts by coverage kind (`derived`, editor-inferred claims excluded), and
`inconsistencies`. Per taxon, the sources with any claim about it, in
publication-year order. And `authors`, every author key with its
surname, so a printed attribution (`auth: [bell.b.m]`) renders by field. Coverage is declared by a reviewer and counted by
the extractor; they are cross-checked, never conflated (G1): a source
declaring `all` or `partly` for a kind with no derived claims, or `none`
or `na` with any, is an inconsistency row for the editor to settle either
way. `scripts/claims.py --inconsistencies` prints the rows with the
claims behind them and the review file to check against, and
`tests/test_claims.py` fails while any row exists, so a new one cannot
land unnoticed.

## What the vocabulary does not do

- No consensus and no "current name": every claim is one source's.
- No merging of spellings (B28): a lookup folds ligatures, diacritics,
  hyphens and spaces (G10) to find records, and the claims keep the key
  as cited.
- No rank inference: the record's rank is a convenience until G8.
- No material redesign: D1 is a later change to one adapter.
- No inference from absence: a kind with no claims for a source means
  "not captured", and only the declared coverage can say whether the paper
  prints any.

## Reading the table

Two more generated files sit beside the claims. `claims/names.json` has
one row per taxon record: name, rank, kind (`primary`, `altSpellingOf`,
`altRankOf`, `vulgarSpellingOf`, `placeholder`), the base record of a
variant, the authority as displayed and its resolved source, and the
folded lookup forms (`phylohist/names.py`). Each manifest source row
carries a `citation` so a source can be named as a reader cites it.

Answers are assembled from **blocks** (`phylohist/blocks.py`): data,
never text. A block has a type, an id (a hash of its content), the
parameters that produced it, the claim ids it rests on, and a payload
that keeps keys, names, ranks, sources, years and claim ids on every
node and cell. Six types, one per answer shape: `classification` (a
tree as a source prints it), `chains` (one line per source: the taxa
from a higher taxon down to a record), `timeline` (one line per source
in year order: what it does with a name), `table` (typed columns; a
cell holds several values when one source places a record twice),
`list` (a synonymy, the printed forms, or the statements about a
record, under a heading), `statement` (a gap, an absence). `validate`
confirms every id and key against the store; `compose` makes an answer
of blocks with a one-line header and an optional question back.
Rendering is a registry of styles (`phylohist/render.py`): `text` and
`markdown`; `json` is the block. A new style is one function and a
registration.

The renderings follow the community's conventions. The listing is a
Systematic Paleontology section: rank words on the headings above the
species level (the paper's rank where it writes one, else the
record's), the type species as its own line under the genus, a new
taxon marked by the rank's abbreviation (`fam. nov.`, `gen. nov.`,
`sp. nov.`), `emend.`, `nom. transl.`, `nom. correct.` and
`nom. subst.` after the name, `?` for a provisional or questionable
name, `=` lines for the synonymy:

    Family Rhenopyrgidae fam. nov.
      Genus Rhenopyrgus
        Type species. Rhenopyrgus coronaeformis
        Rhenopyrgus coronaeformis
          = Pyrgocystis coronaeformis
        Rhenopyrgus whitei sp. nov.

A listing is headed by its source, the tree indented under it, so a
list of listings reads source by source. An `or` entry (the same taxon
under another name in that source) reads on the node's line, "Genus
Pentacrinites or Pentacrinus", and the `or` name matches wherever its
node does: `contents`, `placements`, `history` and the closures treat
the node as that name's own.

A block's heading names the combination that was asked for with the
recorded author, in parentheses when the corpus knows the name is a
recombination: "Pyrgocystis grayae Bather 1915", "Rhenopyrgus grayae
(Bather 1915)", "Rhenopyrgidae Holloway & Jell 1983". The original
combination is the record's placement in its authority's paper when
that tree is entered, else the one a synonymy entry gives, else the
parent recorded with it; when none is on record the author is shown
without parentheses. A placeholder reads in the source's words ("Order
uncertain", "Unnamed family", "Pyrgocystis sp. a"), never as a key.
Rank words otherwise appear only in a rank column or a heading; sources
are always the short citation; pages read "p. 118" or "pp. 120–122".

Species-group names are shown as the combination the source uses: the
nearest genus up the node's chain, a subgenus between in parentheses,
the species above a variety, then the epithet ("Rhenopyrgus grayae",
"Pyrgocystis (Rhenopyrgus) coronaeformis", "Genus species var.
epithet"); a subgenus reads "Genus (Subgenus)". A species recombined
into another genus appears once per combination in every table, since
each is a name of its own; a cited name takes its original combination
from the synonymy entry, or the genus of the name it is cited under.
Where a source lists a species with no genus above it (thirteen nodes in
eight old sources) the epithet alone is shown: the corpus does not
invent a genus; an unnamed species with a printed designation shows it
("Rhenopyrgus sp. indet. 1"). Every rendering is built from the
recorded fields: `citedAs`, the line as printed, is kept on the node
and every claim and is searchable, but it reaches a reader only through
`printed_forms`; what an answer needs from the printed line is captured
as a field. No authority is
appended. An epithet is not a name on its own: species-group records
relate to one another only through an explicit spelling link (*procera*
/ *procerum*), never by a shared epithet, so *Nolichuckia casteri* and
*Timeischytes casteri* are unrelated names.

The closures (`phylohist/closure.py`) are the execution layer:
descendants of a set across every source (transitive within a source,
through accepted synonyms and through the same name at other ranks),
ancestors with each source's chain (alternative placements and
placeholders marked), the sources partitioned by the placement they
give, and the measurement a trajectory asks for (positions and ranks
with papers, co-author sets and years; the latest; the last paper for
each earlier one).

The store (`phylohist/store.py`) reads only these files and builds
the blocks; `phylohist/resolve.py` turns printed names and citations
into keys, and `phylohist/words.py` phrases what the blocks carry. The
tools (`phylohist/tools.py`) are the surface over the store: they return
blocks; the CLI (`phylohist <tool>`, `--style`), the MCP server
(`scripts/mcp_server.py`, `.mcp.json`) and the eval runner all go through
`tools.call`:

| tool | answers |
|---|---|
| `resolve_name(query, rank)` | which records a printed name can mean, with each record's variants (the same name at other ranks or spellings) and the count of sources with statements about it; empty is the closed-world answer. Unnamed records (bins, open nomenclature) are never found by name: the words in their designation name other taxa. Keys are lowercase; every tool accepts a key in any case, or a printed name that resolves to one record ("Rhenopyrgus grayae", "Pyrgocystis (Rhenopyrgus) coronaeformis", "Pyrgocystis (Rhenopyrgus)"); a name that can mean several records is refused with the candidates |
| `resolve_source(query)` | the sources a citation can mean ("Dehm 1961", "Holloway & Jell 1983", "Sumrall et al. 2013", "Fay 1967a"): key, citation, year, authors, entered or not; empty means no source in the corpus is that paper. Every `source` parameter accepts a key or the citation as the blocks print it; a citation that can mean several papers is refused with their keys |
| `contents(source, record, depth, synonymy)` | a classification block of what a source places under a record; every source that places it when no source is given |
| `placements(records, sources, years, …)` | the matrix: records as rows (variants folded) with their rank, sources as columns in year order, the parent each gives (a rejection marked "; not X"); the schemes measured in the header |
| `descendants(records, …)` | a table over the closure: everything any source places under the records, with how each was reached |
| `ancestors(records, …)` | a chains block: each source's chain of taxa above the records, one line per source |
| `placed_under(record, parent)` | a chains block of the sources that place the record under the parent, with the taxa between; first and last stated |
| `history(record, include_related, synonymy)` | a timeline: one line per source in year order with the name as used, its position, the acts and the page; the measurement as the heading; each source's synonymy with `synonymy` |
| `synonymy(record, source)` | the synonymy a source prints under a record, as a list |
| `statements(record, source, kind, act_kind)` | every claim about a record as a sentence with source, year and page, the drill-down; with a source named and nothing of that kind entered, the gap block for it, and with no kind asked the gap names every kind of the source not yet entered |
| `gap(source, kind)` / `gap(name=…)` | the contract's sentence for what is not yet entered, or for a name no source carries |
| `printed_forms(record, source)` | each form a source prints, verbatim (folded to one line in text and markdown; the claim keeps its line breaks), with the page; when the named source recorded no verbatim form, the heading as its listing is entered, marked as such |
| `source_coverage(key)` | the raw coverage view |

A **plan** (`phylohist/plan.py`) is an answer as data before it is
built: a one-line header stating the parameters chosen, the blocks in
order, each a tool and the parameters that matter, and a question back
when a parameter is genuinely ambiguous. `validate` checks a plan
against the tool surface; `execute` builds the composition, one tool
call per block, and reports what could not be built (an ambiguous name
or citation lists what it can mean). `phylohist plan <file>` executes
a plan written by hand; the MCP server's `plan` tool executes one a
chat model states and returns the rendered answer; the eval's expected
answers are plans; in the runner's planner mode the model resolves
names and citations and then states a plan, never seeing the blocks.

`tests/test_tools.py`, `tests/test_closure.py`, `tests/test_blocks.py`
and `tests/test_cli.py` check the tools, the worked example of
`notes/development/structured-answers.md`, the renderings and the subcommands.

## Worked examples

### Holloway & Jell 1983, *Rhenopyrgus* (`data/trees/1983_holloway_jell.yaml`)

The node sits at `taxonomies/0/children/0/children/0/children/0`: class
Edrioasteroidea, placeholder "order uncertain", family Rhenopyrgidae,
genus *Rhenopyrgus*. It yields:

- `placement`: subject `rhenopyrgus`, parent `rhenopyrgidae`, position 0,
  `printedAttribution: as-record`, `pagesInherited: true` if the family
  node has pages (it does not today, so `pages` is absent).
- The parent yields `act` `new` (Rhenopyrgidae is `new: true`) and its own
  `placement` under `edrioasteroidea-order-uncertain_holloway_jell_1983`
  with `parentPlaceholder: uncertain`; the placeholder's own claims carry
  `placeholder: uncertain`.
- Under the genus, *coronaeformis* yields `act` `type`, and its `synonyms`
  entry yields a `usage` and an `acceptance` with `parents: [pyrgocystis]`:
  the original combination *Pyrgocystis coronaeformis*.
- `audit`: state `partial`; coverage `skeleton: all`, `synonymy: partly`,
  `material: none`.

### Ewin et al. 2020, *grayae* (`data/trees/2020_ewin_martin.m_isotalo_zamora.yaml`)

The species node has five `synonyms` entries, none with a name field, so
each is a usage of *grayae* by the cited source, and each is an
`acceptance` with `stance: accepts`, `citesSource` and the cited pages:
`1915b_bather` p. 58 with plate 3 figures 1–2, `1983_holloway_jell`
p. 1004, `1985_smith.a.b` p. 732 with text-figure 11, and two entries for
`2013_sumrall_heredia_rodríguez.c.m_mestre` (figure 1; p. 773). The first
and fourth carry `parents: [pyrgocystis]`. None inherits `pages` from the
species node. The node's `occurrences` yield `material` claims, and the
specimens inside the first occurrence yield more: the holotype claim has
`role: holotypes` (the recorded word), `repository: NHMUK`, `ids:
[E23470]`, `inOccurrence: 0`.

### Fay 1962, *ottawaensis* (`data/trees/1962_fay.yaml`)

`act` `type` on `ottawaensis_whiteaves_1897`, carrying `editorial:
{inferred: [type], basis: "Fay never prints \"type species\"; the genus is
monotypic (p. 201)"}`, plus a separate `editorial` claim with the same
block. A question "does Fay fix the type species?" is answered from the
act claim's `inferred: true`: the flag is the editor's, and the paper
prints monotypy, so the manifest does not count it against the declared
`types: na`. The `material` claim has `role: syntypes` and the node's
`notes` quoting "Holotype, 752" beside "labelled a syntype", so both printed
words are returned.
