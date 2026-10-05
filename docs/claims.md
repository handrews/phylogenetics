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
| `id` | `<source>:<path>:<kind>[:<n>]`. `<path>` is the node's position in its tree file as the loader computes it: the taxonomy or phylogeny index, then each step down (`children/2`, `synonyms/0`, `non/1`, `removed/0`, `parents/0`, `moved`, `corrected`, `substituted`, `lapsus`, `lapsusFor`, `type`, `or/0`). `<n>` disambiguates several claims of one kind from one node (a node with three `material` entries yields three `material` claims). Ids are stable as long as the file is not reordered; the tree keeps printed order, so reordering is a data change. |
| `kind` | one of `usage`, `placement`, `acceptance`, `act`, `rejection`, `material`, `secondhand`, `editorial`, `absence`, `section` |
| `source` | the tree file's source key |
| `path` | the node's position and pointer, `0/children/0/children/0`, the same string the id carries |
| `tree` | `taxonomy`, or a phylogeny's `treeType`; a phylogeny's `notes` ride along as `treeNotes` |
| `pages` | the node's `pages` as written. A node without `pages` takes the nearest ancestor's along the `children` axis only, and the claim then carries `pagesInherited: true`. An inferred node written `pages: null` (it has no page in this source) carries none and passes none down: its children without `pages` carry none either. Entries on any other axis never inherit. On a cited entry (a `synonyms` or `non` entry, a `type` node, or the earlier state of a name under `translated`, `corrected`, `substituted`, `moved` or `removed`) `pages` and `illustrations` locate the cited usage in the cited work, whether written flat or inside an `authority` block, so they appear as `citedPages` and `citedIllustrations` and the claim has no `pages` of its own. |
| `subject` | the resolved taxon key the claim is about; a `section` claim's is the section's key (a record of `data/sections.yaml`, no taxon) |
| `printed` | the printed form on that line: `citedAs` verbatim, and `auth`, `year`, `in` as written (A1, A12). Absent `auth` means "as the record"; the claim says so with `printedAttribution: as-record`. |
| `audit` | the source's `audit.state`; `coverageKind`, the coverage kind the claim counts under (`skeleton` for usage, rejection and a taxonomy placement, `phylogeny` for a placement in a phylogeny, `synonymy` for acceptance, `newTaxa`/`types` for the matching acts, `material`/`occurrences`/`illustrations` by material kind); and `coverage`, the effective value for that kind (declared, or derived where "Derived coverage" says so) |
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

Emitted for every node that cites a name: `taxon`, `openTaxon`, and for
every `synonyms`, `non`, `removed`, `parents`, `or` and `type` entry. Fields added:

- `form`: which field carried the name (`taxon` or `openTaxon`); `bracket`
  for a cladogram's bracket, emitted at the start of a bracket span (the
  node with `bracketStart`), with `bracketEnd` the path where the span ends
  (the node with the matching `bracketEnd`; the same path for a one-node
  span).
- `spelling`: the key used on the line. Spellings are undirected (B28); the
  claim never substitutes the record the key points at.
- `axis`: how the node hangs off its parent (`children`, `synonyms`,
  `removed`, `parents`, `type`, …; `root` for a tree's top node). A `type`
  node is a cited entry: its usage is the type under the name the source
  cites it by, and it is no primary node of the tree.
- `compared`: `{sign: cf | aff, taxon}` on the usage of an `openTaxon` node
  that carries a `cf` or `aff` field: the open form's own record is the
  subject, and `taxon` is the named taxon the node compares it with. A
  node's claims belong to the open form, so the compared taxon's
  statements do not include them; `history` lists the form under its own
  name, marked `compared`.
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
  rank belongs to the tree node is G8, not yet in force. A node written
  `rank: null` (the source places the taxon with no rank word) carries
  `rankAsPrinted: null`; `rank` is the record's, as ever.
- Flags copied from the node: `provisional`, `questionable`, `quoted`,
  `quotedParent` (the genus is printed in quotation marks in this
  combination), `nonMonophyletic` (`true`, `paraphyletic` or `polyphyletic`,
  copied with its value: the source says the group is not monophyletic;
  absent says nothing), `pars`, `tentative`, `outgroup`, `stem`;
  `altPlacements` as a list of keys. (`listHedged`, `listComplete` (B16) are
  not in the schema yet.)

A phylogeny's nesting produces placements too, marked
`tree: cladogram | diagram | other` with the phylogeny's `notes`, and a
bracket is a second placement of the name, marked `via: bracket`, whose
parent is the bracket's key. A bracket is a span in the tree's reading order
(a node, its descendants, then its next sibling): from the node that carries
`bracketStart` to the last descendant of the node that carries the matching
`bracketEnd`, so an end on an internal node takes its whole subtree and
every node in between lies in the span, unnamed ones included. Every named
node in the span carries one such placement, one per bracket it lies in when
spans nest, so a bracket over part of an unnamed clade places the named
nodes below it as well.

A `type` node is a placement marked `via: type` when the taxon that carries
it is a primary node of a taxonomy and the same record is not also one of
that taxon's `children`: naming the type places it, whether or not the
tree lists it. The parent is the carrying taxon, there is no `position`,
and the path ends in `/type`. When the record is also a child node, the
child is the placement and the `type` node adds none; a `type` on a cited
entry (a synonym genus) places nothing. The tools list a record placed this
way and mark the line as named only as the type.

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
- `pars`, `tentative` and `quotedParent` copied; `ownName: true` when the
  entry has no name of its own.
- `lapsusFor`: on an entry whose own name is a lapsus, the record the slip
  was printed for (the entry's `lapsusFor` node). The entry is listed as
  the source gives it, "Steganoblastus canadensis (in error for
  ottawaensis) Whiteaves 1898", but it is not a synonym: the closure does
  not follow it.

### `act`

Something this source does to a name. One claim per flag, `actKind` being:

| tree field | `actKind` |
|---|---|
| `new: true` on a named node | `new` (the protologue; F6 checks it) |
| `new: true` on a placeholder | `placeholder` (the source originates the placeholder; C4) |
| `isType: true` | `type` |
| `type: {taxon: y, …}` on the parent | `type`, at the `type` node, the subject being `y`: `typeOf` (the carrying node's record), `parents` (the genus, and subgenus, `y` is cited in), `fixation`, `fixedBy` and `fixedByPages` (the work that fixed it, with its pages), and `listed` (`true` when a `children` node of the carrying node has the same record). `inferred: true` when `editorial.inferred` is `true`; `inferredFields: [fixation]` when it lists `fixation` (the editor's method, not the paper's). It is a cited entry, so its `usage` is on axis `type`, and it emits no `acceptance`. |
| `emended: true` or `emended: {by}` | `emended`; `by` and `byPages` when the source follows another work's emendation |
| `recombined: true` or `recombined: {by}` on a species-group node | `combNov` (comb. nov.); `by` and `byPages` when the source follows another work's recombination |
| `translated: true` or `translated: {taxon: y, by?}` | `nomTransl`; `translatedFrom: y` when the earlier rank is named, `by`/`byPages` when another work made the act, `rankVariants` from the records' `altRankOf` links |
| `nudum: true` | `nomNudum` |
| `corrected: {taxon: y}` | `corrected`, `correctedFrom: y`; the node's own name is the corrected form |
| `substituted: {taxon: y}` | `substituted`, `substitutedFor: y`; the node's own name is the replacement name (nom. subst.), `y` the preoccupied or otherwise unavailable name it replaces |
| `lapsus: {taxon: y}` | `lapsus`, `lapsusAs: y`; the node's own name is the one intended, `y` the name printed in its place by a slip of the pen (lapsus calami) |
| `moved: {taxon: y}` | `moved`, `movedFrom: y` |
| `removed` entry | `removed`, `removedFrom` the group (the source takes the name out of it; B5), beside the `rejection` |
| `homonym: true` on the record | not a claim: key housekeeping |

A node under `translated`, `corrected`, `substituted`, `moved` or `removed` is the
earlier state of the name as this source cites it: its own `authority`,
`auth`, `year`, `pages` and `illustrations` locate that earlier use, and
it emits a `usage` claim on its axis like any cited entry. The change is
this source's act. `emended`, `recombined` and `translated` are the acts
a source may follow rather than perform, and `by` (an `authority`) names
the work that performed it.

`moved` and `recombined` say different things. `moved` is a change of
placement at any rank, often noted only in prose: the node left the group
under `moved`, with a `rejection` of that placement. `recombined` is the
printed nomenclatural act on a species-group name, "comb. nov.", and pairs
with `moved` when the source names the genus the name leaves. Otherwise a
combination is not a claim: the tools derive it from where each source
places the name.

A node under `lapsus` is not an earlier state: it is the name this
source printed by a slip of the pen for the node's own. Its citation
fields are this source's (they do not inherit), and it emits its `usage`
on its axis. A lapsus is not a nomenclatural act and makes no name: `y`
is not a synonym, emits no `acceptance`, and does not occupy the name,
which a later taxon may take without being a homonym. Its place under `lapsus` is its
protologue, so the record needs no `new: true`; it carries one only when
the slip also claimed the name as new, and then emits a `new` act.
Elsewhere a lapsus record appears only as a `synonyms` or `non` entry
carrying `lapsusFor`, where a later source lists the slip; the loader
reports any other place, and a `lapsusFor` anywhere but such an entry.

`corrected` and `substituted` imply the synonymy: the incorrect form and
the replaced name are synonyms of the node's name, and the closure follows
them as it follows `synonyms` entries. A `synonyms` entry repeats the name
only when the source prints a synonymy that lists it, as a revision may;
the synonymy a source prints is still only its `synonyms` and `non`
entries.

### `certainty`

Not a kind of its own. The C-axis markers (`provisional`, `questionable`,
`quotedParent`, `quoted`, `nonMonophyletic`, `tentative`, `pars`, the
`compared` link of a cf. or aff. form, `uncertain` and `roleUncertain` on a
specimen, `illustration.uncertain`) ride on the claim they qualify, as
fields. No separate table.

### `material`

Emitted from four node fields on a primary node; a cited entry (see
`pages`) emits none, since its `illustrations` are the cited work's and
its other material is not this source's. A field that is `null` emits
nothing. One node emits them in a fixed order, which fixes the claim ids
(`<n>` runs through the `material` claims in this order): `contexts`,
then `material`, then `illustrations`, then `ranges`. `materialKind`
says which.

- `occurrence` (field `contexts`): one claim for each context a
  `material` entry refers to and each context the node defines. `occurrence`
  is the context verbatim; `contextKey` is its key and `contextScope`
  (`node` or `file`) where it was defined. A file-level context is
  emitted once for each node that refers to it. `localityKeys`, when the
  context has `localityNumbers`, are `<register>:<folded number>` for
  each locality number that has a register: its `register`, else the tree
  file's `prefixes` map for its `prefix`, else the file's
  `localityRegister` when it has neither `prefix` nor `register`. The
  number is folded whole (an integer as its digits), one with no register
  gives no key, and each key is given once.
  A `tentative` the context carries (`true` for the whole statement, a
  list of the fields whose values are queried) rides inside `occurrence`
  as written.
- `specimen` (field `material`): one claim per entry. `role` is the
  entry's role, absent when the source attaches none. `prefix`, `numbers`
  (a number a string or an integer, a range pair a two-element list) and
  `asPrinted` are kept as written, and nothing is read out of a string.
  `ids` are the numbers as display strings, `"<prefix> <number>"` when the
  entry has a `prefix`, else the number alone, a range pair staying a
  two-element list; an entry with no `numbers` has none. The *register* of
  a prefix is what the tree file's `prefixes` map gives it. `repository` is
  the entry's explicit `repository` (`repositoryVia: explicit`), else the
  register of its prefix (`repositoryVia: file`), else `null`. `joinKeys`
  are `<register>:<folded number>` for every number (both ends of a pair,
  with `rangeJoin: true`), the register being the prefix's, except that an
  explicit `repository` that is neither that register nor within it
  (`within`, as for a collection) replaces it, and the explicit
  `repository` alone when there is no prefix; an entry with only a
  `holder` has none. Two printed prefixes the file maps to one register
  give one key, and the same specimen in two sources shares a key. A
  collection's number printed with its institution's prefix keys under
  the institution (`prefix: USNM` with `repository: usnm-walcott` gives
  `usnm:165421`). `roleAct` is the entry's own value, else `designated` for
  a holotype, paratype, syntype or cotype on a `new: true` node, else
  absent. The entry's other fields are copied as written: `count`,
  `label`, `holder`, `status`, `formerIds`, `fragmentOf`, `parts`,
  `examined`, `listComplete`, `preparation`, `castOf`, `sameAs`,
  `collectedBy`, `collectedDate`, `uncertain` (the specimen is doubtfully assigned to the
  taxon), `roleUncertain` (the role word is queried in the source),
  `contextKey`, `contextTentative` (from the object form of
  the entry's `context`), and the entry's `notes` as `materialNotes`. An
  entry's `editorial` block becomes the claim's `editorial` (the claim is
  about the entry), with `inferredFields` listing the names in its
  `inferred`; the claim's own `inferred` flag is unchanged, because the
  entry is printed and only a field of it is the editor's. `sameAs`, the
  link from this entry to an earlier source's entry for the same specimen
  (`{source, label}` or `{source, number[, prefix]}`), is copied as
  written and is the source's own statement unless `inferredFields` lists
  it; `sameAsClaim` is the id of the one specimen claim in that source it
  names (matched by folded `label`, or by `number` the way a figure's `of`
  is, within `prefix` when given), set once every source's claims are
  built and absent when the source is not among those extracted or the link
  names no entry or several.
  `specimenIllustrations` lists the locators of the node's illustrations
  whose `of` names the entry, and `illustrationClaims` their claim ids.
  `figured: false` marks a specimen no figure names, set only when all
  six hold: the source's effective coverage for `illustrations` is `all`
  (so an unaudited tree, whose figure list may be partial, asserts
  nothing); the node carries `illustrations`, a value or a null; no
  illustration on the node names the entry through `of` (a number inside a
  range pair's run names it); the node has no illustration without an
  `of`, since an untied figure may show the specimen; the entry's `role` is
  not `figured` (the source calls it a figured specimen); and no figure
  names a cast of it (another entry whose `castOf` names this one), since
  a figure of the cast shows the original. It is never set to
  `true`: a figured specimen has `illustrationClaims`.
- `illustration` (field `illustrations`): one claim per entry, this
  source's own figure. `illustration` holds the locator fields (`plate`,
  `page`, `figures`, `textFigures`, `non`, `notes`, `uncertain`); `of`
  and `depicts` ride on the claim. `ofClaim` lists the ids of the specimen
  claims `of` names (a string or an integer, folded and compared with the
  folded numbers, a range endpoint included, and the folded `label`; a
  number inside a pair's run also names it); a figure with no `of` is tied
  to no specimen.
- `range` (field `ranges`): one claim per element, `range` the element
  verbatim, a `tentative` it carries included. It counts under the `occurrences` coverage kind, and
  `statements(kind='occurrences')` returns it with the `occurrence` claims.

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

### `absence`

An auditor's statement that the source prints none of a kind for a node:
a node's `null` (G11) made a claim, so the tools can answer for one taxon.
Emitted on a primary, non-cited, named node of any rank, after its
material claims, one per coverage kind the node nulls and carries no value
for, in this order:

| `absenceOf` | emitted when |
|---|---|
| `material` | `material` is null |
| `occurrences` | `contexts` and/or `ranges` is null, neither has a value, and no `material` entry has a `context` |
| `illustrations` | `illustrations` is null |
| `synonymy` | `synonyms` is null |
| `types` | `type` is null |
| `skeleton` | `children` is null (on a node above the species level: the source places nothing under it) |

Fields: the shared record, `absenceOf`, and `fields`, the node's fields
that are null for that kind (`['contexts', 'ranges']`). Nothing is emitted
for a file-level `unused`, which the source-level `na` already says. The
claim has no `audit.coverageKind`, so the manifest's per-kind counts and
cross-checks ignore it; it does appear in the per-kind `claims` counts.
Ids are numbered per kind, so no other claim's id depends on it.
`statements` words it ("no specimens cited", "no locality or range given",
"not figured", "no synonymy given", "no type stated", "nothing placed under
it") and selects it with the kind it speaks of: `specimens` and `material`
(material), `occurrences`, `illustrations`, `acceptance` (synonymy), `act`
(types, unless an `act_kind` other than `type` is asked), `placement`
(skeleton), and every one with
`kind='absence'`; with a source named, `kind='absence'` instead returns a
table of the source's content for the record, per node and kind. `synonymy` with a named source answers a node with that
absence by a `none` statement block, "<cite> gives no synonymy for <name>".

### `section`

An informal division of a formal group, such as Linnaeus 1758's "Integra",
"Stellatae" and "Radiatae" within *Asterias* or a descriptive heading in a
genus list. A section has no taxonomic status, so it is no placement; it is
a span of siblings in a taxonomy with a record of its own in
`data/sections.yaml`, keyed like `taxa.yaml`. The tree marks it with
`sectionStart` (an object: `section`, the record's key, and optionally
`citedAs`, `pages`, `notes`) on its first sibling and `sectionEnd` (the key)
on its last, both in one `children` list, both markers on one node for a
one-sibling section. The span is those siblings from start to end,
inclusive, each with its subtree; a section never crosses a level. Within
one sibling list sections may nest but not interleave, and the loader and
the draft checker report an end with no open start, a start never closed, a
start for a key already open and an interleaving. A section is valid in a
taxonomy only.

One claim per span, emitted by the start node (a start the list never
closes emits none; the loader reports it). Fields: the shared record (`id`,
`source`, `path`, `tree`, `audit`; no `printedAttribution`) and

- `subject` and `section`: the section's key. The subject is no taxon's, so
  the manifest's per-taxon source lists and the store's `by_subject` index
  leave a `section` claim out.
- `name`: the record's `name`, or its `designation` when the name is null.
- `members`: the record keys of the named siblings in the span, in list
  order; a sibling with no `taxon` or `openTaxon` is a member by path only.
- `memberPaths`: the path of every sibling in the span, in list order (a
  sibling's subtree is no member).
- `endPath`: the path of the node that closes the span (the start node's
  own for a one-sibling span).
- `citedAs`, `pages`, `notes`: from the `sectionStart` marker, when given.

The claim has no `audit.coverageKind`; it appears in the per-kind `claims`
counts only. No tool reads it yet: the tools, `statements` included, leave
it out, and queries and output over sections are deferred.

## Derived coverage

`claims/manifest.json` holds, per source record (every key in
`sources.yaml`, whether or not a tree exists: `tree: false` is how "the
paper is recorded but not yet entered" is derived), the declared `audit`,
the counts of claims by kind, by `actKind` and by `materialKind`, the
counts by coverage kind (`derived`, editor-inferred claims excluded), and
`inconsistencies`. Per taxon, the sources with any claim about it, in
publication-year order. And `authors`, every author key with its
surname, so a printed attribution (`auth: [bell.b.m]`) renders by field,
and `holotypeConflicts`. Coverage is declared by a reviewer and counted by
the extractor; they are cross-checked, never conflated (G1): a source
declaring `all` or `partly` for a kind with no derived claims, or `none`
or `na` with any, is an inconsistency row for the editor to settle either
way. `scripts/claims.py --inconsistencies` prints the rows with the
claims behind them and the review file to check against, and
`tests/test_claims.py` fails while any row exists, so a new one cannot
land unnoticed.

Six kinds, `material`, `occurrences` (the node fields `contexts` and
`ranges`), `illustrations`, `synonymy` (`synonyms` and `non`), `types`
(`type`) and `skeleton` (`children`), are also read from the tree itself (G11): `claims.derived_coverage(roots)` walks the
primary, non-cited, named nodes of a source's taxonomy trees (a cladogram
prints no material). A kind whose fields the file lists as `unused` is
`na` (for `synonymy`, `unused: [synonyms]`; for `types`, `unused: [type]`;
`skeleton` has no `unused` form and is never `na`).
Otherwise, when no node writes a `null` for the kind's fields, it is `None` and declares nothing: a value
records what the source prints, not that the file was audited for it. When
some node writes a null, the kind is `all` if no node lacks the fields
(`partly` if a material entry has `listComplete: false`), and `partly` if
some node does. For `material` and `illustrations` only the species-level
nodes (species, subspecies, variety) are counted, since specimens are
cited and figures drawn for species; `occurrences` counts every named
node, and a node whose `material` entry has a `context` counts as carrying
it. `synonymy` counts every named node of every rank: a node carrying
`synonyms` or `non`, as a value or a null, is present (a `non` list is a
synonymy of rejected names), and only `synonyms: null` writes a null (the
loader rejects it beside a `non` list). `types` counts the named genus
and subgenus nodes only, since a species' type is a specimen: a
placeholder (an unnamed or open genus) has no type and is not counted, and
a family's `type` or `type: null` may be written and is not counted. A
genus is present when it carries `type`, a node or a null, or has a child
marked `isType` (the older form of the same statement); only `type: null`
writes a null. `skeleton` counts the named nodes above the species level,
genus and subgenus included (any rank but the species-level ones, so an
`Unranked` or `section` node counts, and a placeholder, a bin with no members of its own,
does not): `children` as a list or as a null is present, and only
`children: null` writes a null. A genus with no `children` is a genus whose
species are not yet entered, since a source often lists no species; a
species-level node may not write the null, since infraspecific names are
rare enough to be entered when present, and absent `children` on a node
above the species level means the subtree is not entered.
Each source row carries `derivedCoverage` (this raw result)
and `coverage`, the effective map: the declared value for `newTaxa` and
`phylogeny`, and for the six node-state kinds the derived
value when there is one, else the declared one. Each claim's `audit.coverage` and the gap statements read
the effective map. A kind the tree derives is not declared as well: when
the derived value is not `None` and `audit.coverage` declares the kind at
all, an inconsistency row says "declared X but derived from the tree (Y);
remove the declaration", whether or not the two agree. A source whose
tree writes nulls therefore declares `newTaxa` and `phylogeny` only. The
three material kinds have no claim-count check; `synonymy`, `types` and
`skeleton` keep it for a source that writes no null of the kind and so
derives nothing, until a null derives it. `absence` claims are not
counted under any coverage kind.

`holotypeConflicts` is roadmap F5, a report and never a failure: one row
per taxon (`subject`) whose holotype is a different specimen in two
sources, `{taxon, holotypes: [{source, ids, joinKeys, claim}]}` with one
entry per holotype claim, in source year order (an unnumbered holotype's
`label` rides beside). A holotype's identity is the set of its `joinKeys`,
else its `label`, else its printed `ids`; two are the same specimen when
those sets intersect, or when they are linked through `sameAsClaim`
(directly or through a chain of specimen claims, in either direction, or
by the join key of an entry that prints one number; an entry printing
several numbers joins nothing but through its own link). A claim marked `uncertain` is ignored, and a source
that gives the taxon a `lectotype` or `neotype` does not enter the
comparison, since its selection supersedes the earlier holotype.
`scripts/claims.py --inconsistencies` prints the rows after the per-source
ones; they add nothing to its exit status and `tests/test_claims.py` does
not fail on them.

## What the vocabulary does not do

- No consensus and no "current name": every claim is one source's.
- No merging of spellings (B28): a lookup folds ligatures, diacritics,
  hyphens and spaces (G10) to find records, and the claims keep the key
  as cited.
- No rank inference: the record's rank is a convenience until G8.
- No inference from absence: a kind with no claims for a source means
  "not captured", and only the declared coverage can say whether the paper
  prints any.
- No diagnoses (roadmap D10, done 2026-09-27): who published what
  systematic information where, with locators, is the data's scope;
  the text of a printed diagnosis is not.

## Reading the table

Three more generated files sit beside the claims. `claims/repositories.json`
is the repository registry as loaded (`data/repositories.yaml`), keys sorted,
each entry's `name`, `type`, `subject`, `within`, `prefixes`, `otherNames` and
`place` as present: the store reads it to split a catalog number a reader
types into its holder and its bare number.
`claims/names.json` has
one row per taxon record: name, rank, kind (`primary`, `altSpellingOf`,
`altRankOf`, `vulgarSpellingOf`, `placeholder`), the base record of a
variant, the authority as displayed and its resolved source, and the
folded lookup forms (`phylohist/names.py`). A section has no row there: its
record is in `data/sections.yaml` and only its `section` claim names it.
Each manifest source row
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
`list` (a synonymy, the printed forms, the statements about a
record, or the citations of one specimen, under a heading), `statement` (a gap, an absence). `validate`
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
| `statements(record, source, kind, act_kind)` | every claim about a record as a sentence with source, year and page, the drill-down; with a source named and nothing of that kind entered, the gap block for it ("nothing of this kind" when the source holds other claims about the record), and with no kind asked the gap names every kind of the source not yet entered; with a source and `kind='absence'`, a table of what the source gives for the record per content kind (members, specimens, occurrences, figures, synonymy, type; one group per node), each `N entered`, `none printed` (the auditor's `absence` claim, or a source coverage of `na` or `all` that leaves none to enter) or `not entered`; above species rank the specimens and figures rows appear only when the node carries some, since those kinds are cited for species, and the type row appears for a genus or subgenus, and at another rank only with a type statement (a `type` node, or a child marked `isType`) or a `types` absence, and the members row (the placements of the node's children, `N entered`, or a `skeleton` absence) appears for a named node above the species level, and at species level only with children entered or a `skeleton` absence; with no kind and an `act_kind` of `type`, or `kind='act'`, the `types` absence is selected too, and `kind='placement'` selects the `skeleton` absence |
| `specimen_history(number, repository, source, label)` | every citation of one specimen, by catalog number as a paper prints it ("UQF 5404", "F. 5404"): a list of the specimen claims whose `joinKeys` hold the number's key (`<repository>:<folded bare number>`, built as the extractor builds it) and those whose printed range contains it, one line per claim in year order: the role ("holotype of X") or, with none, "cited under X", "(doubtfully assigned)", the number as printed when it is not the one asked about (or "in the run …"), and the figures tied to it (locator notes left out) or "not figured"; for an entry with a run or several numbers only the figures whose own `of` names the number asked about, and nothing about figures when none does unless the claim is `figured: false`. The prefix names the repository; a number without one, or with a shared prefix, takes `repository` (a registry key), and without it the result is the `absent` statement, naming the competing repositories when the prefix is shared. A specimen with no number is asked for by `source` and `label` (the specimen claim of that source whose label matches, folded; no match is the `absent` statement, worded `the specimen "A" of Bather 1914`); with neither a number nor both of them the call is refused. The heading names what was asked (`Specimen UQF 5404 (holder)` or `Specimen "A" of Bather 1914`). Either way every claim in the component of a claim found is listed (`sameAsClaim` in either direction, through a chain, or a shared join key between one-number entries), still in year order; a line reached only through a link ends `(the same specimen according to Bather 1914)`, naming the source that carries the link, or `(the same specimen, editor's inference)` when the carrying claim's `inferredFields` lists `sameAs` |
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
species node. The node's one context (`lady-burn-starfish-bed`) yields an
`occurrence` claim, emitted first, and its `material` entries yield
`specimen` claims after it: the holotype claim has `role: holotype`,
`prefix: NHMUK E`, `numbers: [23470]`, `ids: [NHMUK E 23470]`,
`repository: nhmuk-e` with `repositoryVia: file` (the file's `prefixes` map),
`joinKeys: [nhmuk-e:23470]` and the context's
`contextKey`; the next entry has no role, since the paper attaches none.

### Fay 1962, *ottawaensis* (`data/trees/1962_fay.yaml`)

`act` `type` on `ottawaensis_whiteaves_1897`, carrying `editorial:
{inferred: [isType], basis: "Fay never prints \"type species\"; the genus is
monotypic (p. 201)"}`, plus a separate `editorial` claim with the same
block. A question "does Fay fix the type species?" is answered from the
act claim's `inferred: true`: the flag is the editor's, and the paper
prints monotypy, so the manifest does not count it against the declared
`types: na`. The first `material` claim is the entry for No. 752: it has
`role: lectotype`, `numbers: [752]`, `repository: gsc` with
`repositoryVia: explicit` (the number is printed "Canadian Geological Survey
752", kept as `asPrinted`, with no prefix to map), `joinKeys: [gsc:752]`, and an entry-level
`editorial` block (`inferred: [role]`, with the basis) that is the claim's
`editorial`, with `inferredFields: [role]`; the paper prints "Holotype" in a
caption and "syntype" in the text, and the editor reads lectotype. The
second claim is the lost syntype lent to Hudson, which has a `label` and
`status: lost` and no catalog number, so `ids` is empty and there are no
`joinKeys`. Both carry the node's `notes` quoting "Holotype, 752" beside
"labelled a syntype", so both printed words are returned.
