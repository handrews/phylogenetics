# Semantics roadmap: finalizing the MVP data model

Decisions needed to give every field one meaning, mapped to the nomenclatural
term it records. Companion to [`schema-audit.md`](schema-audit.md), which holds
the usage evidence; numbers here are from that census (`productize` @ `4e64c36`).

Each item has an id (`A1`, `D4`, …) so decisions can be referenced. Items marked
**MVP** must be settled before the claim table is built; the rest can be decided
now and migrated best-effort, gold slice first.

Conventions are checked against two Treatise Editorial Prefaces: Moore's in
Part U (1966, pp. ix–xxiii; cited as *Preface* with the roman page) and Selden
& Ausich's in Part V, 2nd revision (2023, pp. xi–xxvi; cited as *Preface 2023*).
Where they differ, the 2023 usage is the convention and the 1966 form is
recorded as a synonym; see [Terminology updates](#terminology-updates-1966--2023).

## Ground rules

- The data model is the product. Code changes only where they enforce integrity
  or are unavoidable.
- Every field records something *a source printed*. Editorial judgement is
  allowed, but it is a separate, marked layer, never mixed into a source's claim.
- One field, one meaning. Where a field means different things in different
  contexts, either the meaning is "as printed on this line" for all of them, or
  the field splits.
- Attribution is written the way the literature writes it. A synonymy line
  cites "Name AUTHOR, year, p. n" in the same form as a nomenclatural authority,
  so the data does likewise and does not invent a second vocabulary.
- Species names are entities in their own right, not halves of a binomial. A
  species node always sits under a genus node, so the tree encodes the
  combination, and a recombination is the same species entity appearing under a
  different genus in a later source. The original combination is whatever the
  protologue node (`new: true`) sits under; `parents` on a synonymy entry is
  the combination the cited usage employed. `originalParent` on the taxon
  record is not a combination claim: it disambiguates the key when one author
  used one epithet for two species under different genera in one work
  (`brachiatus_hall_1852_myelodactylus` beside `brachiatus_hall_1852_glyptaster`).
  It belongs with `needsQualification` as key housekeeping and should be
  renamed to say so (`keyQualifier`); it disappears when the YAML gives way
  to a database.
- Source keys carry the year of publication, never of a reading. A `reading`
  record, or a key that follows a volume's nominal year rather than its issue,
  is an error to fix (A11).
- Every rule in this document has been broken by some publication. The model
  does not have to fit everything; it has to make it visible when something
  does not fit. `notes` is the last-resort escape hatch on every object, and
  any object that lacks one gets one when needed.
- `notes` is the one field that may be read from enclosing objects, because
  a note sometimes covers several taxa. Apply an inherited note with caution,
  and have derived data mark it as inherited rather than as the node's own.
- Absence of a field is not a statement. A source that does not list a
  synonym, a specimen, or a range has not denied it; the data only records
  what was captured. Nothing may be inferred from a missing value, and the
  audit state (G1) says how much was looked for.
- Prefer stated uncertainty to confidence. The audience is researchers who
  will follow the citation; the job is access to what was printed, not
  synthesis of it.
- Early works are authoritative by their date and inadequate by every later
  standard: no catalogue number, sometimes no illustration, a name proposed in
  a sentence. The model must carry such a source with the same fields as a
  modern one and simply leave most of them empty.
- Consult `notes` before deciding what a value means. YAML comments carry no
  meaning.
- Migrations are data-only wherever possible. Tree-node attribution fields
  (`authority`, `auth`, `year`, `in`) are not read by `phylohist/taxa.py`.

### The `editorial` block

A tree node's own fields record what the source printed: the resolved
`taxon`, `auth`/`year`/`citedAs` as printed, and the printed flags.
`editorial` sits beside them and never replaces any of them. It records what
the data editor did that the printed line does not establish, and `basis`
says on what evidence. Two kinds:

- `source: <key>`: the printed citation cannot resolve as printed (in press,
  wrong year, a page from another printing) and the editor resolves it to
  this source record. The printed `auth`/`year`/`citedAs` stay (A6).
- `inferred: true`: the node's existence or placement is the editor's, not
  the source's (B20).

What it is not for: an alternative authority, year or spelling. The name's
true authority lives on the taxon record; a printed misspelling is an
`altSpellingOf` record; a printed attribution that disagrees with the record
is kept as printed and the disagreement is derived (B19), never stored.
Bockelie 1981's "Balanticystis Ubaghs 1972" is the worked case: `auth`,
`year`, `citedAs` as printed, identity through `balanticystis`
(`altSpellingOf: balantiocystis`), the reading in `notes`, no `editorial`.

Noted for later: an editor-verified marker for a discrepancy that is the
source's own error, if the eval needs to separate verified from unverified
ones. That would be a third kind, not a change to these two.

## Terminology updates, 1966 → 2023

What changed between the two prefaces, and what it means for the data.

| topic | 1966 | 2023 | consequence |
|---|---|---|---|
| Code edition | 1961 | 4th ed. 1999; new acts must be registered in ZooBank (xi) | none for historical data; a `zoobank` identifier slot on sources is worth reserving |
| replacement name | "nom. subst." preferred (xii) | "nom. nov. pro X, non Y" (xx) | `act` member is `nomNov`; treat "nom. subst." as its synonym |
| name-group Latin (nom. inviol., perf., imperf., van., neg., vet., null.) | defined and used (xii–xiv) | named once, then "authors have used fewer terms" (xiii) | do not pre-populate `act` with them; add only when a source prints one |
| citing an act | author and year (xv, xviii) | author, year **and page** (xv, xvii–xviii) | `actBy` is a full `authority`, so it can carry `pages` |
| combined act | "if desired … nom. transl. et correct." (xviii) | a recognized form (xvii) | `act` is a list |
| emend. | author and date (xix) | author, date and page; style "…; emend., Williams & Wright, 1965, p. 299" (xviii) | add `emendedBy: authority`, used when the emender is not the current source |
| superfamily suffix | unspecified (xv) | -oidea mandated, -acea disallowed, tribe -ini (Art. 29.2, xiv) | suffix lint must be era-aware; older sources print -acea legitimately |
| suprafamilial endings | may not end in -idae/-inae (xvii) | may not end in -oidea/-idae/-inae (xvii) | prescriptive for new names only; Crinoidea and Edrioasteroidea stand |
| type-species fixation | M, OS, OD, SD, SM, ICZN (xx) | OD, M, SD (with page), typus/typicus, tautonymy, ICZN; post-1930 genus without fixation is invalid, later fixation re-dates the name (xix–xx) | `typeFixation` enum keeps all; SM and OS are historical |
| type species form | original combination (xix) | "always given in the exact form it had in the original publication" (xix) | supports `originalParent` and capture-as-published |
| synonym history | not addressed | "syn. by AUTHOR, year, p." records who first synonymized a name; "an important part of the history of a taxon" (xxii) | new field `synonymizedBy` (B15) |
| subjective synonyms | "(obj.)" marks objective ones (xxi) | same, and the synonym's own type species is cited (xxi) | B11 unchanged; the type is already a species node |
| homonym by misidentification | cited in synonymies with "(non AUTHOR, year)" (xxi) | not repeated | B10 unchanged |
| stratigraphy | Treatise's own European and North American tables (xxviii–xxx) | ICS International Chronostratigraphic Chart; ranges to biozone level in Part V (xxii) | E6: `time.yaml` follows ICS; the 1966 tables feed the `regional` section |
| author names | Cyrillic transliterated, alternates in brackets (xxiv) | Western name order for all; full given names for Chinese authors; **each author's own romanization retained per publication** (xxi–xxii) | authors need aliases (A5) |
| repositories | not listed | abbreviation table with former names, e.g. "NHMUK (formerly BMNH)" (xxv–xxvi) | `repositories.yaml` needs `formerly` aliases (F2) |
| online first | — | Treatise Online and print are one entity; cite the online date as earliest (xxii) | `processDates.online` already exists |

## MVP cut line

The MVP claim table needs, per source, unambiguous answers to four questions
about a taxon: what name was used, where it was placed, which earlier usages the
source accepted or rejected for it, and how sure the source was. That is phases
A, B and C plus the coverage flag in G. Material (D) and time (E) can be carried
through as per-source blobs attached to the node until their designs are
migrated.

---

## A. Attribution

One field, `authority` (or `auth`+`year`+`in`), whose meaning is always "the
attribution printed on this line". What that attribution *identifies* depends on
where the line is:

| where | identifies | question it answers |
|---|---|---|
| `taxa.yaml` record | the name's nomenclatural authority | who made this name available, and where |
| tree node under `children` / root | the attribution as this source printed it | how did *this* source credit the name |
| tree node under `synonyms`, `non`, `parents` | the work in which the cited usage appeared | which earlier work, page and figure is being listed |

```yaml
# taxa.yaml: nomenclatural authority
echinodermata:
  authority: {source: 1791_bruguière, ex: {source: 1734_klein}}

# 1975_kolata tree: Kolata credits Fleming
- taxon: echinodermata
  auth: [Fleming]
  year: 1828

# 1976_bell.b.m synonymy of Lebetodiscus (p. 54): an accepted earlier usage
- taxon: agelacrinites
  authority: {source: 1858b_billings, pages: 84,
              illustrations: [{plate: 8, figures: [3, 3a, 4, 4a]}]}
  citedAs: "Geol. Surv. Canada, Fig. and Descriptions of Canadian Organic Remains, dec. 3:84"
```

**A1 (MVP). Document the table above in the schema; no rename.** `citedAs`
stays a node field: the bibliographic string exactly as the source printed it.

**A2 (MVP). Attribution on a `children` node that matches the record.**
Integrity check, report not error: if the printed attribution resolves to the
same source, or the same author set and year, as the taxon record's authority,
the field carries no information and should be dropped. Where it differs, the
difference is a claim ("Kolata 1975 credits Echinodermata to Fleming 1828") and
the claim table emits it.

**A3 (MVP). `ex`, `in`, `attributedTo`.**

- `ex` — the name derives from an earlier work that could not make it available;
  `source` is the work that did. Two uses, both Klein 1734. The *Preface* (xv,
  xviii) uses "ex" in a second sense, the name a nom. transl. was derived from;
  that sense is handled by `altRankOf` and B6, not by this field.
- `attributedTo` (with a source record) and `in` (with `auth`+`year`) — the
  credited authors differ from the work's authors ("Luo & Hu in Luo et al.,
  1999"). One per mechanism; they never co-occur.

**A4.** Finish the `auth`→`authority` migration from the audit (117 mechanical,
54 needing a choice). Not MVP-blocking.

**A6 (MVP). Attribution that cannot resolve as printed.** Bell 1975 cites
"Bell, 1974" for a work that appeared in 1976; the correct citation would have
been "in press". The tree records what was printed (`auth: [bell.b.m]`,
`year: 1974`, `citedAs: Bell, 1974`) and explains in `notes`. That is right,
and the taxon record already carries the true authority. What is missing is a
machine-readable link from the printed line to the resolved work, so the claim
table can attach the usage to `1976_bell.b.m` without guessing. Reuse the
editorial block from B8:

```yaml
- taxon: isorophida
  auth: [bell.b.m]
  year: 1974
  citedAs: Bell, 1974
  editorial:
    source: 1976_bell.b.m
    basis: cited before publication; printed with the intended year
```

The same block covers a wrong page, a wrong year, or a citation to a reprint.
It is editorial because the printed line alone does not establish it. See
"The `editorial` block" under Ground rules.

**A7. Printed year letters.** Bell writes "1858b" and "1896b" using his own
bibliography's letters. They happen to match this dataset's `1858b_billings`
and would not match a differently lettered `1896_haeckel`. Keep the letter in
`citedAs` (it is part of what was printed) and never derive a source key from
it. Index numbers can themselves be wrong: the Treatise's "BATHER in REED (12)"
(S229) describes its reference (11), Bather 1906 in Reed's Burma memoir, under
the number of (12), the 1913 Girvan memoir, which never mentions
*Caryocystites*.

**A8. A cited work's year is itself contested.** Schmidt's *Cyathocystis*
paper is 1879 in Bockelie & Paul 1983 and 1880 in Bell 1975 and Bassler 1935;
Regnéll's Treatise chapter is 1966 and "1967"; Bell 1975 prints "Jaekel, O.
1918 (1921)". The source record carries one `pubDate` and a `notes` saying why
that year, and each printed attribution stays as printed. Resolution uses A6's
editorial block only when the printed year would otherwise resolve to the
wrong record or to none. Never "correct" a printed year in place.

**A9. "In preparation" citations.** Bell 1980 lists "Aepyaster Sprinkle and
Strimple (in preparation)". The `inPrep` source record is the anchor for the
usage, and that is all the data says. No editorial availability judgement is
recorded: the nomen nudum status will be captured as a claim when the
publication that states it is added, and until then the absence of a
protologue is visible from the `inPrep` flag alone. The "never published"
wording on the record should go.

**A11. One work, several printings.** Von Buch's *Über Cystideen* was read
on a date reported as 3 March, 3 May or 14 May 1844, reported in the
Academy's Bericht for 1844 (pp. 120–133), preprinted separately in 1845 (its
own pagination), issued in the Abhandlungen for 1844 in 1846 (pp. 89–116),
noticed in English in 1846 and translated in 1846. The Treatise (S229) cites
"VON BUCH, 1846, p. 128" and "1846, p. 19": the year of the Abhandlungen with
pages that exist only in the Bericht and the preprint. Rules:

- Each physical printing is its own source record, linked by `printingOf`
  (the analogue of `translationOf`), with the reading as `processDates.read`
  on whichever record is treated as first.
- A printed citation resolves to the printing whose pagination it fits, and
  where year and page disagree the editorial block (A6) names the printing
  and says why.
- The taxon record's authority names a printing, never a reading, and the
  key's year is that printing's year. `1844_buch` is therefore a record to
  convert, not to keep: the 1844 Bericht (pp. 120–133) is the first printing
  that carries the names, so the record becomes the Bericht article with
  `processDates.read: 1844-03-14`, and the keys `_buch_1844` stand. The
  `reading` form of `$defs/article` is retired once no record uses it (G6).
  `1963_brown.i.a` (issued 1964-04-10) becomes `1964_brown.i.a`, and
  `branagani_brown.i.a_1963` follows.

The Bericht settles the von Buch case: the reading was 14 March 1844 (Bericht
p. 120), the genus is on Bericht p. 128 and the species on p. 129, so the
Treatise's "1846, p. 128" is the Abhandlungen's year with the Bericht's page
and its "p. 19" is a dropped digit. Both printed variants of the reading date
(3 May, 14 May) go in `notes`.

The same shape recurs with Hall: the 1866 advance print of the New York State
Museum 20th Annual Report, the 1871 advance print of the revised paper, and
the 1872 24th Annual Report. Bell 1976 dates *pilea* and *vorticellatus* to
1866, *Cystaster* to 1871 and *Streptaster* to 1872, each to the printing that
first carried the name. The data has records for 1866 and 1872 only, and
Bather (1919, Geol. Mag., p. 73) adds that the 20th Annual Report itself was
issued in parts from 1864, complete in January 1865 and again in 1867, and
revised in 1870.

A source key's year should then be the year of the printing the record
describes. Today `1963_brown.i.a` is keyed to its reading year and issued in
1964, and Schmidt is 1879 or 1880 by the same ambiguity; decide the rule once
and note exceptions on the record.

**A10 (MVP). The record's authority is an editorial choice, and silence is
not a choice.** Echinodermata is attributed in the tree files to Bruguière
1791, Klein 1734, Bruguière 1789 and Fleming 1828, and Stokes 2021 argues for
Klein 1778; thirty-four sources print no attribution at all. The `taxa.yaml`
authority is the dataset's canonical pick, marked as such with a `basis`; every
differing printed attribution is a claim (A2); a source that prints none makes
no claim, and nothing is inferred. The one assumption the model does make is
identity: a bare "Echinodermata" at phylum rank resolves to the single record.
That is an editorial rule for well-established high-rank names, stated here,
and it does not extend downward.

**A5.** `auth` free-text names (521 uses, 220 distinct): decide the rule for
family-only author records. Add alias support to `person` while there: the
*Preface 2023* (xxi–xxii) retains each author's own romanization per
publication, so one person legitimately appears under several spellings
(Chang / Zhang; Gekker / Hecker). An `altSpellingOf`-style link between author
records keeps the printed form and the identity. Not MVP-blocking.

---

## B. Relations and their nomenclatural terms

**B1 (MVP). Field-to-term map.** This becomes the schema's documentation.
"Nested node" is what the child node under the field denotes.

| field | printed form | term | nested node denotes | decision |
|---|---|---|---|---|
| `children` | indentation / headings | placement | a member | keep |
| `synonyms` | synonymy list | accepted earlier usage (B2) | a usage this source accepts | keep |
| `parents` (on an entry) | "*Echinosphaerites malum* PANDER" | combination as cited | the genus of the cited usage | keep |
| `non` | "non VANUXEM, 1842" | rejected usage (B2) | a usage this source excludes | keep |
| `pars` | "partim", "pars" | partial acceptance | — (flag) | keep |
| `tentative` | "?" before an entry | questionable acceptance | — (flag) | keep; default → `false` (B4) |
| `moved` | "transferred from" | prior placement | where the taxon came from | keep; document direction |
| `corrected` | "nom. correct." (*Preface* xiii–xv, xviii) | corrected form, no rank change | the form being corrected | keep; document direction |
| `or` | "vel", "or" | alternative name offered | the alternative | keep |
| `altPlacements` | "or possibly in", "sedis mutabilis" | alternative placement | the other parent | keep |
| `removed` | "removed from", "excluded" | explicit exclusion of a member | the removed member | keep; fix recursion (B5) |
| `mergeInto` | multi-part work | continuation of a taxonomy | — | keep; integrity: target exists |
| `new` | "n. gen.", "sp. nov." | protologue here | — (flag) | keep |
| `type` | "*" before the type species (*Preface* xix) | name-bearing type at genus/family level | — (flag) | keep; see B3, B14 |
| `emended` | "emend." (*Preface* xix: scope change only) | emended diagnosis, same name | — (flag) | keep; drop `null` from its type |
| `modifier` | "nom. transl.", "nomen nudum", "n. comb." | nomenclatural act or name group | — | replace with `act` (B6) |
| `stem` | "stem-group" | stem-group usage | — (flag) | keep |
| `outgroup` | cladogram outgroup | outgroup | — (flag) | keep |
| `bracket` (tree) | clade bracket / label | named clade in a cladogram | — | keep |
| `rank` (tree) | rank as printed here | rank as used by this source | — | keep; overrides taxon rank |

Taxon-record relations:

| field | term | decision |
|---|---|---|
| `altSpellingOf` | subsequent spelling, incl. incorrect ones, gender agreement, æ/ae (*Preface* x–xi) | keep |
| `vulgarSpellingOf` | vernacular-language form | keep |
| `altRankOf` | nomen translatum: same name at another rank, so a distinct record (*Preface* xv) | keep |
| `originalParent` | original combination (*Preface* xix) | keep |
| `homonym` | homonymy (*Preface* xx) | keep; see B10 |
| `needsQualification` | key-disambiguation housekeeping | keep |
| `bracket` (taxon) | vernacular plural ("Edrioasteroids") | rename `vernacular` (B7) |
| `synonym` | unsourced equation | move to the editorial layer (B8) |
| `status` | mixed: `informal`, `unregistered`, `monophyletic` | split (B9) |
| `identifier` | open-nomenclature label ("*Rhenopyrgus* sp. indet. 1") | keep |

**B2 (MVP). What a synonymy entry asserts.** Every entry under `synonyms`
means: *this source accepts the cited usage as belonging to this taxon*. That is
the whole claim, and it is the same claim whether the cited usage carries the
same name or a different one. A thorough revision such as Bell 1974 lists every
earlier usage it agrees with, so a name appearing "as a synonym of itself" is the
author's accounting of the taxon's history, not an error. `non` is the same claim
negated: the cited usage does not belong here. `pars` and `tentative` qualify the
acceptance.

The claim table emits one `accepts-usage` (or `rejects-usage`) claim per entry,
carrying the cited work, pages, figures, and the combination from `parents`.
When the entry's name differs from the node's name it additionally derives a
`junior-synonym` claim between the two names. No data change.

**B3 (MVP). `type: true` on a synonymy entry** means the species was the type
species of the genus given in that entry's `parents`, at the time of the cited
usage. All three uses fit: Kesling 1966 lists *cincinnatiensis* and *ornatus*
as types of *Narrawayella* and *Savagella*, which became junior synonyms of
*Cyclocystoides* when their types moved; Doweld 2012 lists *neglecta* as type
of *Bockia*, replaced by *Heckerocrinus*. Rule: on a synonymy entry `type`
requires `parents`, and the claim table emits "type species of `parents[0]`"
for the entry rather than a type claim about the node. This is distinct from
`type: true` on a `children` node, which is the type of the node's own parent.

**B4 (MVP). `tentative` defaults to `true`.** Every sibling flag defaults to
`false`, code never reads it, and all 16 uses set it explicitly. Change the
default to `false`.

**B5 (MVP). `removed` is invisible.** `Tree.__init__` does not recurse it, so
its one use reaches no consumer. Explicit exclusion is a claim worth keeping,
since it is exactly what consensus databases discard. Add it to
`RELATED_LIST`. The one code change in phase B.

**B6. Replace free-text `modifier` with `act` + `actBy`.** The *Preface 2023*
(xv, xvii–xviii) cites an act as its name, author, year and page, then the
name it derives from:

```
Order CORYNEXOCHIDA Kobayashi, 1935
  [nom. transl. Moore, 1959, p. 217, ex suborder Corynexochida Kobayashi, 1935, p. 81]
Order HYBOCRINIDA Jaekel, 1918
  [nom. transl. et correct. Moore in Moore, Lalicker, & Fischer, 1952, p. 613, ex …]
```

`act` is a list, because "nom. transl. et correct." is one act with two
kinds. `actBy` is an `authority` (so it carries `pages`), used only when the
act's author is not the current source. The derived-from name is `altRankOf`
(nom. transl.) or `corrected` (nom. correct.). Observed values map as:

| printed | count | `act` | notes |
|---|---|---|---|
| nomen transl. / nom. transl. / nom. tranls. Paul 1968b / nom. transl.? | 14 | `[nomTransl]` | "Paul 1968b" → `actBy`; "?" → `provisional` |
| nomen nudum | 4 | `[nomNudum]` | |
| n. comb. | 1 | `[combNov]` | |
| (Plesion) | 1 | — | a rank; move to `rank: Plesion` |

Add members only when a source prints them, under the 2023 spelling:
`nomCorrect`, `nomNov` (1966 "nom. subst." maps here), `nomDubium`,
`nomOblitum`, `nomConserv`. The Treatise Part S cystoid chapter prints "nom.
null." and "nom. van." throughout its synonymies (S229: *Caryoclstites*
d'Orbigny, *Caryocystis* Angelin, *Amorphocystis* Jaekel), so `nomNullum` and
`nomVanum` are needed for a target source and enter now; `nomNegatum` and
`nomVetitum` wait for a sighting.

Emendation of scope is not a name act and stays on `emended`, but the *Preface
2023* (xviii) requires its author, date and page, so add `emendedBy: authority`
for the case where the emender is not the current source.

Authors trained under the botanical code use its words in zoological papers:
Doweld 2012 writes "nom. illeg.", "legitimate", "generotype", "Holotypus" and
"Heckerocrinus (Bockia) cucumis", with the replaced genus in parentheses as a
citation device. The act is still `nomNov`; the printed words go in `citedAs`
or `notes`. No enum member for another code's vocabulary unless it recurs.

**B7. Rename taxon-level `bracket` to `vernacular`** (13 uses).

**B8 (MVP). Drop taxon-level `synonym`.** An early idea, superseded by the
trees. Of the 8 uses, 5 are already stated by a later source's synonymy:
Broadhead 1982 lists Sprinkle's unnamed orders 1 and 2 under Gogiida and
Ascocystitida, Doweld 2012 lists Bockiidae under Heckerocrinidae, Luo et al.
2008 and Deshmukh 2022 cover the two species cases. The remaining 3 (Sprinkle's
indeterminate order 1 = Trachelocrinida, indeterminate families 2 and 3 =
Cambrocrinidae and Heckerocrinidae) have no source in the data that equates
them. Delete the field everywhere; for those three, either add the source that
makes the identification or let the placeholder stand unequated. No editorial
block: an equation nobody printed is not recorded.

**B9. Split `status`.** `monophyletic` is an opinion and belongs on a tree.
`informal` and `unregistered` describe availability; fold them into
`availability: informal | unregistered` on the record, or into `act` on the node
that prints the judgement.

**B10 (MVP). Homonyms by misidentification.** The *Preface* (xx–xxi) cites
"Posidonomya PACHT, 1852 (non BRONN, 1834)" inside a synonymy: Pacht used
Bronn's name for something else, and that misuse is what is being synonymized.
The Treatise entry for *Caryocystites* (S229) forces the choice: von Buch's
"*Caryocystites testudinarius*" is a *nomen in errore* for a specimen that was
not Hisinger's *testudinarius*, it carries von Buch's type designation, and it
was later named *angelini* by Haeckel and *buchi* by Jaekel. None of that can
be said if von Buch's usage is only a usage of Hisinger's name.

Decision: a misidentification is a taxon record of its own, with a link to the
name the author applied. `misidentificationOf` answers one question only:
whose name was this? It does not say what the material was, or what the
name's author thought the material was; those are synonymy claims made by
whichever source makes them.

```yaml
testudinarius_buch_1844:
  name: testudinarius
  authority: {source: 1844_buch, pages: 129}
  misidentificationOf: testudinarius_hisinger_1837
  notes: |
    "Caryocystites testudinarius His." applied to the elongated form von Buch
    read as Hisinger's pl. 25 fig. 9d; the figure is 8d, Hisinger's unnamed
    "Formæ irregulares" under S. Citrus. nom. in errore per Kesling 1967, S229.
```

Von Buch printed Hisinger's name, so the link goes to Hisinger's
*testudinarius*. What the material actually was is stated by the sources
that say so: the Treatise's node for *angelini* lists von Buch's usage and
Hisinger's "Formæ irregulares" node (fig. 8d) in `synonyms`, and Hisinger's
*testudinarius* and *citrus* in `non`. Hisinger's own view sits in his own
tree, where the forms are an `openTaxon` under *citrus*. Von Buch's belief
about Hisinger's belief is a sentence in `notes` (B19). Nothing needs to be
captured twice, and nothing beyond this goes into structure.

Von Buch's own words matter here, and so do Hisinger's. The 1846 translation
(p. 34) says "Hisinger has united this species with the former under the name
Sphæronites testudinarius … I have thought it better to apply his name to this
remarkable species which he has considered as a variety." Hisinger's text
(Lethaea Suecica, p. 92) says something else: the elongated forms are an
"Obs. Formæ irregulares … (fig. 8. d.)" appended to *S. Citrus*, with "striae
as in *Sphæronites Citro*", and the word variety is absent, although the same
book marks varieties elsewhere ("c. varietas", pp. 82, 93). So von Buch's
"variety of *testudinarius*" is his reading of the misplaced figure, and his
transfer of the name was deliberate on a false premise. Three consequences:
Hisinger's unnamed forms are an `openTaxon` node under *citrus* with
`identifier: "Formæ irregulares"`, fig. 8d, and no rank inferred; von Buch's
misidentification record points at that node, not merely at a figure; and the
sentence about the variety is a secondhand claim contradicted by its source
(B19), recorded in `notes` as printed.

Later synonymies then read naturally: *angelini* Haeckel 1896 has
`synonyms: [testudinarius_buch_1844, buchi_jaekel_1899, <Hisinger's Formæ
irregulares node>]` and `non: [testudinarius_hisinger_1837,
citrus_hisinger_1837]`. The same shape covers a
genus: Jaekel's *Caryocystites* (for what is now *Heliocrinites*) is a record
with `misidentificationOf: caryocystites`. "nom. in errore pro" is the printed
marker for this and goes in `citedAs`.

**Taxon-level `homonym: true` is key housekeeping, not a claim.** It marks
that a record's name collides with another record's or with a name outside the
corpus, so the key needs a suffix. The homonymy itself is a claim some source
makes, and it lives in that source's tree: Doweld 2012 is
`heckerocrinus` with `act: [nomNov]`, `synonyms: [bockia_hecker_1938]`, and
`non: [bockia_reisinger_1924]`, which needs a record for the turbellarian
*Bockia* even though it is outside the corpus. Of the 16 flags, the trees
state the homonymy for *Cyclaster* (Billings 1858 replaces it with
*Edrioaster*) and can for *Bockia* once the `non` is added; *Actinia*,
*Fistularia*, *Tentaculites* and *Umbellularia* have the senior name only in
`notes`; *Alcyonium* and the two *Encrinus* records appear in no tree at all;
*Himantopus*, *Kerona*, *Proteus*, *Penicillus*, *Urceolaria*, *Echinodiscus*
and *Kailidiscus* have neither. Keep the flag, treat it like
`needsQualification`, and add an integrity check that a flagged record has
either a tree claim or a `notes` citation of the senior homonym.

**B11. Objective synonyms.** The *Preface* (xxi) marks "(obj.)" and treats the
rest as subjective. Add `objective: true` to a synonymy entry only where a source
prints it.

**B12. "auctt."** (*Preface* xxii: auctorum, "of authors") marks a usage by
various later authors rather than the original one. Allow `auth: [auctt.]` on
an entry and document it.

**B13. "s.l." and "s.s."** (*Preface* xxiii). A `sensu: lato | stricto` flag on
the node, added when first printed.

**B14. Type-species fixation.** Both prefaces record how the type was fixed.
Current forms (*Preface 2023*, xix–xx): OD (original designation, including
pre-1931 "n. gen., n. sp." on a single species), M (monotypy), SD (subsequent
designation, with author, date and page), typus/typicus, tautonymy, and ICZN
(with the Opinion number). Historical forms (*Preface*, xx): SM (subsequent
monotypy) and OS (objective synonymy). This volume prints them: "Lebetodiscus
BATHER, 1908 [*Agelacrinites dicksoni BILLINGS, 1857; OD]". Add `typeFixation`
with the union of both lists and `typeFixedBy` (an `authority`) for SD and
ICZN, on the `type: true` node. Two rules from the 2023 text affect identity:
a genus published after 1930 without a fixed type is unavailable, and a later
fixation makes the name available under the later author and date, which the
model expresses as a second taxon record with its own authority. Doweld 2012
applies exactly this: *Bockia* Hecker 1938 "failed to publish an available
name" for want of a type (Art. 13.3), so he dates it 1940, where the type was
fixed. The 2012 tree's "Reason for erroneous year unclear" is answered: the
year is a printed re-dating, and the tree records it as printed with Doweld's
reason in `notes`.

**B15. "syn. by".** Part V records the work that first synonymized a name,
"syn. by Zalasiewicz, 1995, p. 34", because "such information is an important
part of the history of a taxon" (*Preface 2023*, xxii). Add `synonymizedBy:
authority` on a synonymy entry. It is a secondhand claim: the current source
attributes the synonymy to the cited work. The claim table emits it as such,
and when the cited work's own tree is captured the two can be compared, which
is the citation-error check the MVP eval wants.

**B16 (MVP). Hedged and declared-incomplete membership.** Two different
things a source can say about a list of members, both met in the examples:

- **Hedged membership.** Bell 1975 (p. 36): "other members of this group may
  include:" followed by eight species, one with a "?". Decision: `provisional`
  only where a "?" is printed against the item; the list-level "may include"
  and the family-level "with question" go in `notes` on the parent, quoted.
  The reason not to mark every member is that the hedge is not uniform:
  the suborder is named from *Cyathocystis*, which under the *Preface 2023*
  (xvii) presumes that genus as its type, while Bell defines it on
  *Timeischytes*; marking *Cyathocystis* provisional in its own nominate
  suborder would assert more doubt than the page shows. The cost is that the
  claim table sees firm placements unless it reads the note; if that matters,
  a single `listHedged: true` on the parent, the twin of `listComplete`, is
  the smallest structural marker and is left to your call.
- **Declared incompleteness.** Parsley 2021 (p. 974): "This is not a
  comprehensive listing of the probable orders to be included in this sub
  class", and "Genera, e.g. Gogia, …". The placements are firm; the source
  says the list is partial. Add `listComplete: false` on the parent node, with
  the phrase in `notes`. Its opposite is also printed: Dzik & Orłowski 1993
  "Species included: Monotypic" is `listComplete: true`.

The ground rule that absence is not a statement still holds; `listComplete`
records what the source *said* about its list, nothing more.

**B17. Parentheses around a suprafamilial authority.** Bockelie & Paul 1983
print "Order Cyathocystida (Bell 1975)" for a suborder they raise to order and
redefine, with the act stated in prose on p. 262. The parentheses borrow the
species-level changed-combination convention. Record it as `act: [nomTransl]`
with `emended: true` (B6), and keep the parenthesized form in `citedAs` so
the printed convention is not lost.

**B18 (MVP). The same name at different ranks.** *Rhombifera* is a class
(Zittel 1879), an order, an informal group, and a genus (Barrande 1867), and
Paul et al. 2024 use class and genus in one hierarchy. Zittel's own page
(Handbuch, p. 417) prints "3. Gruppe. Rhombiferi. Joh. Müll.": rank
"Gruppe", spelling *Rhombiferi*, credited to Müller 1854, whose own tree has
the group unnamed. So the record for the suprageneric name is Zittel's
*Rhombiferi* (A-given: Müller), and the later class and order *Rhombifera*
are `corrected` forms at other ranks; "1870" on the current records is a
typo for 1879, which the `aporita` record already carries. *Gogiida* is an order
(Broadhead 1982) and, in Parsley 2021, a subclass containing that order.
Jaekel's 1918 name appears as Eocrinida, Eocrinoida and Eocrinoidea at order
and class. The rule: one record per name-and-authority-and-rank;
`altRankOf` links records only when they are the same author's name
transferred (the two Zittel *Rhombifera* records, not the Barrande genus);
name resolution is rank-aware and returns every record; the claim table never
merges on the string. The *Preface 2023* (xvii) says such duplication should
not happen, which is why it must be modelled rather than assumed away.

`altRankOf` is only the identity link between coordinate family-group names;
it says nothing about who re-ranked. The act belongs to the tree of the source
that did it (`modifier: nomen transl.` today, `act: [nomTransl]` after B6), so
Smith 1985 (suborder Isorophina to subfamily Isorophinae) and Guensburg &
Sprinkle 1994 (suborder Lebetodiscina to family Lebetodiscidae; families
Lebetodiscidae, Carneyellidae and Pyrgocystidae to subfamilies) each carry
their own. B6 will revisit whether the derived-from link should move into the
tree as well.

**B19. Secondhand claims that contradict their source.** Parsley 2021 (p.
970) cites Dzik & Orłowski 1993 for a placement those authors argued against;
Bockelie & Paul 1983 summarize Bell 1980 as placing Cyathocystina in "the
order Isorophina". Both are recorded as printed. When both works are captured
the claim table can set the secondhand claim beside the source's own claim.
That comparison is derived, never stored, and it is the citation-error class
of the MVP eval.

**B20 (MVP). Placements the editor inferred.** The 1983 tree places
*Timeischytes* and *Hadrochthus* under Isorophida with the note "order and
suborder assumed", because the paper says only "offshoots from the
Agelacrinitidae". An inferred node needs a marker the claim table can read:

```yaml
- taxon: isorophida
  editorial:
    inferred: true
    basis: Agelacrinitidae is in Isorophida per Bell 1980, which the paper cites
```

The claim table emits the placement as editorial, not as the source's. See
"The `editorial` block" under Ground rules.

**B21. A `non` entry that says where the usage belongs.** "non S. citrus
HISINGER, 1837, p. 91, = Echinosphaerites aurantium (GYLLENHAAL)" (S229).
The exclusion is the claim of this node; the "=" is a cross-reference to the
node where that usage is accepted, which exists on S233. Allow `identifiedAs:
<taxon>` on a `non` entry; the claim table emits the exclusion here and
checks that an acceptance exists there.

**B22. Errors in other works are claims, not record annotations.** The
`sphaeronites` record carries "notes: The 1967 Treatise incorrectly cites
page 185". That statement is about the Treatise. It belongs on the Treatise
tree's *Sphaeronites* node: `pages: 185` as printed, an editorial correction
with `basis`, and nothing on the taxon record. Same for every "X gives Y" note
now sitting on records.


---

## C. Open nomenclature and uncertainty

Ten markers, each hedging a different thing. Keep them distinct but name the
axis each one sits on.

| axis | field | printed form | meaning |
|---|---|---|---|
| identification of material | `cfTaxon` | "cf." (*Preface* xxii: confer, compare) | compared with the named taxon; identification tentative |
| identification of material | `affTaxon` | "aff." (*Preface* xxii: affinis, related to) | related to but distinct from the named taxon; usually undescribed |
| identification of material | `illustration.uncertain` | "?" on a figure | figured specimen doubtfully assigned, no cf. target |
| name in open nomenclature | `openTaxon` + `identifier` | "sp.", "sp. indet.", "gen. et sp. nov." | unnamed placeholder |
| placement | `provisional` | "?" before the parent, "incertae sedis" | assignment to parent tentative |
| validity of the taxon | `questionable` | "?" before the name | the taxon itself doubtful |
| validity of the taxon | `quoted` | name in quotation marks | name used informally or as unavailable |
| acceptance of a usage | `tentative` | "?" before the entry | acceptance tentative |
| acceptance of a usage | `pars` | "partim" | only part of the cited material |
| name identity | `needsQualification` | — | housekeeping only |

**C1 (MVP). The tree encodes where cf. and aff. apply.** Because species are
entities, "*Gogia* cf. *G. spiralis*" is a genus node with a `cfTaxon` species
child, and "cf. *Gogia*" is a `cfTaxon` genus node with species children. The
data already does this: all 29 species-level qualifiers sit under a genus node
with no children, and both genus-level ones (Buch 1844) carry children. Document
the convention; no new field.

**C2 (MVP). Integrity check on cf./aff. targets.** The target key resolves; a
species-rank target sits under a genus node; a genus-rank target may carry
children.

**C3.** "ex gr.", "?" between genus and species, and the B12/B13 markers appear
in the literature but not yet in the data. Add fields only when a source prints
them, on the identification axis.

---

## D. Material: specimens, illustrations, occurrences

Principle from `notes/graph.txt`: specimens are the physical anchors,
illustrations are proxies for them, occurrences say where specimens came from.
The current model keeps all three as siblings on the node with no links between
them, in four different specimen shapes.

**D1. One `material` list per node, one entry per specimen or batch.**

```yaml
- taxon: coronaeformis_rievers_1961
  new: true
  pages: [[10, 11]]
  material:
  - ids: [RVS 1]
    role: holotype
    illustrations:
    - {plate: 2, figures: [[1, 4]], depicts: cast}
    occurrence: bundenbach   # id of one of this node's occurrences
  - ids: [[QMF 59647, QMF 59653]]   # a batch, ranges allowed
    role: paratype
  illustrations:             # only figures the source does not tie to a specimen
  - {plate: 3, figures: 7, notes: "specimen not identified"}
  occurrences:
  - id: bundenbach
    series: Lower Devonian
    unit: [Roofing Slate facies, Hunsrück Slate]
    location: [Bundenbach, Hunsrück Region, Germany]
```

- Occurrences carry a short `id`, unique within the node, and material entries
  refer to it by name. Spelling the id twice is a weak check, and F1 makes it a
  real one: an `occurrence` reference must resolve within its node.
- An illustration nested under a material entry *depicts* that specimen. A
  node-level illustration is a figure the source never ties to a specimen,
  which is the honest state for most pre-1900 work. Migration is therefore
  incremental: nothing moves until the paper supports the link.
- `depicts: specimen | cast | reconstruction | drawing` records the medium, so
  a latex cast is a property of the figure, not a second specimen.
- The repository is the id prefix, resolved against `repositories.yaml` (F2).
  An explicit `repository` field is allowed when the prefix is absent or
  ambiguous (`NHMUK` vs `NHM UK` vs `EE`).
- Occurrence-level `specimens` and `possibleSpecimens` (D3) become
  `occurrence` back-references from material entries, so a specimen is written
  once.
- A material entry may have **no catalogue number**. Bell's "Bigsby specimen"
  (1976, p. 63) is identified only by the four works that figured it; the
  entry then carries a `label` and its `illustrations`, and nothing else.
- `formerIds` records renumbering ("YPM 28451 (old 2361)"; "ROM 161-t-a …
  described … as 'GSC 1415'", pp. 61–62), including a move between
  repositories. `fragmentOf` marks a piece of a lost or dispersed specimen
  (GSC 1407-B, "a fragment of the holotype", p. 60).
- `roleAsPrinted` keeps the author's word when it is not in the role enum:
  Bell's "Illustrated Specimen", Bassler's "plesiotype". The enum value is
  the editorial mapping; the printed word is the fact.
- `examined: false` for specimens the source reports from other works without
  seeing them (Bell, p. 62: "Three other representatives … have been
  reported").
- `holotypeFixation: monotypy` parallels B14 at the species level; Bell
  states it explicitly for *L. dicksoni* (p. 62).
- `measurements` as free text or a small map, since every Bell specimen has
  two diameters; not a modelling priority.

**D2. Type roles, checked against the Code.** ICZN Art. 72–75 regulate the
name-bearing types; the rest are conventions the literature uses and the data
must still record as printed.

| role | regulated | meaning |
|---|---|---|
| `holotype` | yes | the single specimen designated as name-bearing type in the original publication |
| `paratype` | yes | any other specimen of the type series cited in the original publication |
| `syntype` | yes | each specimen of a type series when no holotype was designated |
| `lectotype` | yes | a syntype later designated as the name-bearing type |
| `paralectotype` | yes | a remaining syntype after lectotype designation |
| `neotype` | yes | designated when the original name-bearing type is lost |
| `topotype` | no | from the type locality |
| `hypotype`, `plesiotype` | no | figured or described in a later work; older North American usage; both kept as printed (`hypotype` in Durham 1966) |
| `allotype` | no | a paratype of the opposite sex; not applicable here, drop |
| `kleptotype` | no | never used; drop |
| (none) | — | material cited without a role; replaces `unknowntypes`, `unknown`, `unspecified`, `additional` |

**Holotypes are singular by definition.** Two catalogue numbers for one holotype
are one specimen with two parts, written as two `ids` on one entry with
`parts: [part, counterpart]`; the plural `holotypes` role goes away. Integrity
check across all sources: a name has at most one holotype specimen, unless a
later source records a `lectotype` or `neotype` designation, which is itself a
nomenclatural act on that source's node.

**D3. Occurrence-level `specimens` and `possibleSpecimens`.** Both are
validated by nothing today. Under D1 they are replaced by back-references.
`possibleSpecimens` (2 uses, personal) records that the source is unsure which
specimens came from this horizon; that becomes `tentative: true` on the
material entry's occurrence link.

**D4. Illustrations as locators versus depictions.** The same `illustration`
shape serves two roles, fixed by context: under a synonymy entry's `authority` it
locates a figure *in the cited work*; under `material` or a node it records what
a figure *in this source* shows. No rename. Drop `illustration.source`,
`location` and `collectedFrom`, which were earlier attempts at the specimen link
and are unused.

**D6. Exclusion at figure level.** Paul et al. 2024 accept "Gutiérrez-Marco
et al., p. 111, pl. 2, figs. 1–5, 11 (non fig. 6)". Neither `pars` nor a
`non` entry says which figures. Allow `non` inside an `illustrations` locator:

```yaml
illustrations:
- {plate: 2, figures: [[1, 5], 11], non: [6]}
```

The same shape records a **correction of another work's figure number**:
Kesling 1967 (S229) writes "HISINGER, 1837, pl. 25, fig. 8d, non fig. 9d"
because the plate's fig. 8d is drawn level with series 9 and von Buch read it
as 9d; Hisinger's plate explanation and labels agree with each other (Lethaea
Suecica pp. 91–92, pl. XXV). Von Buch's tree keeps 9d as printed; the
Treatise's locator is `{plate: 25, figures: 8d, non: [9d]}` with the
explanation in `notes`. The disagreement is derived, as in B19, never resolved
in place.

**D7. A type designated by figure.** The same paper selects a lectotype as
"the original of Barrande, 1867, plate 11, figure 5, now in the National
Museum, Prague (Reg. no. L13001)". The material entry carries the number, the
role `lectotype`, the designation as this source's act, and the 1867 figure as
the identifying locator. Older works identify specimens by figure alone
(Bell's Bigsby specimen), so the locator must be able to stand without a
number.

**D5. Migration.** 88 node-level `specimens` blocks, 13 `taxon.holotype`
entries, 30 occurrence-level blocks. Mechanical for the typed-role shapes;
`taxon.holotype` moves onto the protologue node (`new: true`) of the same name.
Do the gold slice first and leave the rest on the old shape behind a
deprecation flag in the schema until migrated.

---

## E. Stratigraphic time

Four distinct statements a source can make about age, plus two scales:

| statement | example | proposed field |
|---|---|---|
| point | "Wuliuan" | `stage: Wuliuan` |
| span | "Wuliuan to Drumian" | `stageRange: [Wuliuan, Drumian]` |
| boundary | "at the Wuliuan–Drumian boundary" | `stageBoundary: [Wuliuan, Drumian]` |
| informal subdivision | "lower Wuliuan" | `stage: Wuliuan` + `stageModifier: lower` |

**E1. One pattern for every rank on both scales.** For each rank in `period`,
`series`, `stage`: the four fields above. For the regional scale, the same four
with a `local` prefix (`localStage`, `localStageRange`, …). Today `series` and
`stage` have the variants and `period` does not; boundary and range share one
def though they mean different things. All of this is under 70 instances, so
the cost of making it uniform is small now and large later.

**E2. Biozones follow the same pattern** with one addition: `biozones` (a list)
means several zones from *different* zonations apply at once, which is neither
a range nor a boundary. Document the three.

**E3. Units are one ordered list.** `unit: [member, formation, group]`, most
specific first, as the personal tree already does. Drop `superunit`,
`subunit`, `section`.

**E4. Merge `basicOccurrence` into `occurrence`.** The split exists only so
`inferred` cannot itself contain `inferred` or regional fields. Use one def and
enforce that constraint in the loader: an `inferred` block may carry only
global-scale fields, `basis` and `sources`.

**E5. `inferred` is editorial and must say so.** It records the data-enterer's
or a later source's translation of a regional age to the global scale. Require
`basis` (free text) or `sources` on every `inferred` block.

**E6. Validate against `time.yaml`.** The schema's `period`, `series` and
`stage` enums duplicate `time.yaml`. Load `time.yaml`, check values against it,
and delete the enums, or generate them. `time.yaml` follows the ICS
International Chronostratigraphic Chart, which the *Preface 2023* (xxii) names
as the Treatise standard. Add a `regional` section for the names now
free-floating in `localStage` (Sunwaptan, Dyerian, Delamaran, Ardmillan) so
they validate too; the *Preface* (xxviii–xxx) tabulates the 1966 European and
North American regional units and is a ready source for the Ordovician and
Devonian names the corpus uses.

**E8. Doubt on one element of a range.** "M.Ord., ?U.Ord., Asia(China)-Eu.
(Sweden-Est.-?Wales)-?N. Am.(USA)" (Kesling 1967, S229). The "?" attaches to
one age and two regions, not to the occurrence. Each element of a range or
location list may be written as `{value, tentative: true}` in place of the
bare string, so the doubt stays where it was printed.

**E7. Delete `geology.yaml`.** Every specimen it records is already on a tree
node. Its formation and member registry is an idea for later (F3), not a file to
keep loading nothing from.

---

## F. Registries and integrity checks

The only code this roadmap asks for. Each check reports, and the ones marked
fail also exit non-zero.

**F1 (MVP). Reference resolution, fail.** Every source id, taxon key (including
`cfTaxon`, `affTaxon`, `openTaxon`, `mergeInto` targets), author id and
`altSpellingOf` / `altRankOf` / `vulgarSpellingOf` target resolves.

**F2. Repository prefixes, fail.** Every material id prefix resolves. Resolution
is **scoped to the source**: Bell 1976 (p. 2) defines UCMP as the University of
Cincinnati, where current usage means the University of California, and cites
the Field Museum as CFM, CFMP, CFMPE and CFMUC. So `repositories.yaml` holds
global defaults with `formerly` aliases (the *Preface 2023*, xxv–xxvi, lists
"NHMUK (formerly BMNH)"), and a source record may carry its own
`repositoryAbbreviations` map that wins within that source. The id string
keeps the printed prefix either way.

**F3. Time values, fail.** Every `stage`, `series`, `period` and regional value
resolves in `time.yaml` (E6).

**F4 (MVP). Attribution redundancy, report** (A2).

**F5. Holotype uniqueness, report** (D2).

**F6 (MVP). Protologue consistency, fail.** Exactly one `new: true` node per
name across all sources, and its source equals the name's authority source. The
second half exists in `Tree._check_primary_taxon`; the first does not.

**F7 (MVP). `removed` recursion** (B5).

**F8 (MVP). cf./aff. position** (C2).

---

## G. Leftovers

**G1 (MVP). Replace `complete` with an audit state.** `complete` was used on 23
of 289 sources and its sub-flags were never used consistently. Replace with:

```yaml
audit:
  state: complete | partial | unaudited | unauditable | unobtainable
  notes: "open nomenclature not captured"
```

Default is `unaudited`. `unauditable` means a copy exists but no
machine-readable text does. `unobtainable` means no copy could be had at all:
not digitized, or behind institutional access. Palaeontologia Indica n.s. 2(3)
(1906), where the *Caryocystites* type-species question was settled, is the
first such case; every chain of citations eventually ends at one, and the
manifest must say so rather than leave the source looking merely uncaptured.
The MVP coverage manifest reads this plus derived facts (page anchors present,
material present, node count).

**G2. `sources.yaml` `pages` and `plates`** use the flat alternating encoding
(199 uses). Convert to `citationNumbers`; mechanical.

**G3. Dead leaves from the audit.** `tree.categories`, `tree.data`,
`tree.plates`, `taxon.modifier`, `taxon.reason`, `person.suffix`,
`publication.type`, `trees.<id>.source`, the object form of `$defs/specimen`.
Delete after D1 lands, since that is the only design that could have wanted any
of them.

**G4. `phylohist/support.py` and `phylohist/source.py`.** Orphaned; delete.

**G6. Retire the `reading` article form.** Once `1844_buch` is converted
(A11), no record uses `oneOf` branch 3 of `$defs/article`; readings are
`processDates.read` on the printed record.

---

## H. Things that do not fit, and where they go

Cases met in the Bell 1976 audit ([`audit-1976_bell.b.m.md`](audit-1976_bell.b.m.md)).
Each has a home; none needs a new top-level construct.

| case | example | where it lands |
|---|---|---|
| a usage with no name, cited by a phrase | "A Fossil Belonging to the Class Radiaria", Sowerby 1825 (p. 55) | `openTaxon` placeholder in `taxa.yaml`, cited like any usage |
| two names in one synonymy line | "1946 *Lebetodiscus* … Wilson, 19; *Lepidoconia* Wilson, ibid.: 21" (p. 54) | two entries with the same attribution |
| a claim about another work's error | Wilson "erroneously considered the specimen to be the holotype" (p. 61) | a claim of this source about that source: material entry `notes` now; a `disputes` link later if it recurs |
| classification of taxa the work does not treat | Stromatocystitidae, Cyathocystidae, Pyrgocystidae under "Others" with genera bracketed (p. 50) | ordinary `children` placements; the source's own scope is a `notes` on the tree |
| an earlier classification reproduced | Jaekel 1899, Bather 1900, Bassler 1935–36 summarized (pp. 4–8) | belongs to those sources' own trees; here, at most a `notes` that Bell reproduces them, with page |
| specimen identity that moved | ROM 161-t-a formerly GSC 1415 (p. 61) | `formerIds` (D1) |
| a nickname for a specimen | the "Grant specimen", the "Fitzpatrick specimen" (p. 61) | `label` on the material entry |
| a printed attribution that is wrong | "Bell, 1974" in Bell 1975 | as printed, plus `editorial.source` (A6) |
| a role word outside the enum | "Illustrated Specimen" (p. 61) | `roleAsPrinted` (D1) |
| horizon given as a quoted local name plus a hierarchy | "'Cobourg beds' (= the 'Cystid beds, about 180 feet below the top of the Trenton')" (p. 65) | `unit` list for the hierarchy; the quoted equivalence in `notes` until E1 has a `localUnit` alias |
| a list the source says is partial | "not a comprehensive listing", "Genera, e.g." (Parsley 2021, pp. 974–975) | `listComplete: false` (B16) |
| a list the source hedges as a whole | "other members of this group may include" (Bell 1975, p. 36) | `provisional` on each member (B16) |
| a placement the editor inferred | "order and suborder assumed" (1983 tree) | `editorial.inferred` (B20) |
| a name at two ranks in one hierarchy | Class Rhombifera / genus *Rhombifera* (Paul et al. 2024, p. 5) | separate records; rank-aware resolution (B18) |
| a citation that contradicts the cited work | Parsley 2021 on Dzik & Orłowski 1993 | as printed; comparison derived (B19) |
| a usage accepted except some figures | "(non fig. 6)" (Paul et al. 2024, p. 5) | `non` inside the locator (D6) |
| two years for one cited work | Schmidt 1879 / 1880; "1918 (1921)" | as printed; source record picks one with `notes` (A8) |
| a tentative recombination in prose | "*Agelacrinites* (*sensu lato*) *hanoveri* may belong to the genus *Postibulla*" (Bell 1975, p. 34) | placement with `provisional` and `sensu: lato` |
| a citation whose year and page come from different printings | "VON BUCH, 1846, p. 128" (Kesling 1967, S229) | printings as separate records; `editorial.source` names the one the page fits (A11) |
| a name used for the wrong specimen | "*C. testudinarius* VON BUCH … nom. in errore pro …" (S229) | a misidentification record (B10) |
| one author's name meaning another's genus | Jaekel's *Caryocystites* = *Heliocrinites* (S229) | genus-level misidentification record (B10); Jaekel's tree unchanged |
| a corrected figure number in a cited work | "pl. 25, fig. 8d, non fig. 9d" (S229) | `non` in the locator (D6) |
| an exclusion that names the right home | "non S. citrus … = Echinosphaerites aurantium" (S229) | `identifiedAs` on the `non` entry (B21) |
| a dichotomous key | "Key to Genera of Caryocystitidae" (S229) | `listComplete: true`; characters stay prose in `notes` |
| doubt on one element of a range | "?U.Ord.", "?Wales" (S229) | per-element `tentative` (E8) |
| citations by a volume's index numbers | "(31)", "(69)" (S229) | `citedAs`; resolve through that volume's list (A7) |
| anything else | — | `notes`, on the node, and the audit state records that it was seen |

The example sources are catalogued in
[`source-observations.md`](source-observations.md).

The rule for adding structure: a case earns a field when it appears in a
second source. Until then it lives in `notes`, and the claim table surfaces
the note verbatim with the claim.

---

## Sequence

0. **Pre-build cleanup, gold slice only.** Small enough for one sitting and
   mechanical enough for a cheaper model, then checked:
   - `1976_bell.b.m.yaml`: the *Lebetodiscus* entry's `year: 1901` → 1908;
     `valcourensis_clark_1920` gains `provisional: true`.
   - `1975_bell.b.m.yaml`: `plautinae` entry's `year: 1980` and `citedAs` →
     1880.
   - Delete taxon-level `synonym` from the 8 records (B8) and remove the field
     from the schema.
   - Schema: `tentative` default → `false` (B4); add the `audit` block (G1)
     and the `editorial` block with `source`, `inferred`, `basis` (A6, B20);
     set `audit.state` on the gold-slice sources and leave the rest defaulted.
   - Code: add `removed` to `Tree.RELATED_LIST` (B5); add the F1 reference
     check for `mergeInto` targets and the F6 protologue-uniqueness check.
   - Mark the 1975 in-press entries and the 1983 inferred placement with the
     new `editorial` block, since the claim table reads them.
   Everything else in the data checks (Zittel 1879 and *Rhombiferi*, the
   `1963_brown.i.a` key, Doweld's *Bockia* `non`, Hisinger's `nomNov`, the
   Hall 1871 record, the 1840c `translationOf`, Volborth's read date) is
   outside the gold slice and waits.
1. **A1–A3, A6, A10, B1–B5, B8, B10, B16, B18, B20, C1, C2, F1, F4, F6–F8,
   G1.** The MVP set. Each is a documentation decision, a small data
   migration, or one integrity check. Nothing here depends on D or E.
2. **B6, B7, B9, B11–B15, B17, B19, B21, B22, A4, A5, A7–A9, A11, D6, D7,
   E8.** Vocabulary the literature uses that the data does not yet need
   everywhere; decide the convention now, add fields on first use.
3. **D1–D5 decided, then migrated on the Edrioasteroidea gold slice only.**
   The rest of the corpus keeps the old shapes behind a deprecation flag.
4. **E1–E7 and F2, F3, F5.** Same pattern: decide now, migrate the gold slice,
   validate everything.
5. **G2–G4.** Housekeeping whenever convenient.

## Open items

Every question raised during the semantics pass has been answered and folded
into the numbered items above, with two exceptions that are deferred on
purpose:

- **`1844_buch`** stays as it is for now. The von Buch printings are outside
  the Edrioasteroidea gold slice, the field itself treats them as confusing
  (Kesling 1967, S229: "1846 (or variously reported as 1844 or 1845)"), and
  the rewrite deserves its own look at why the record was built around the
  reading. A11 states the rule; the record will follow when the cystoids come
  into scope.
- **Unobtainable sources** are a standing condition, not a to-do. Bather 1906
  in Reed's Northern Shan States memoir is the worked example: the Treatise's
  account of the *Caryocystites* type species rests on it, and no archive has
  it. G1's `unobtainable` state and the note in `source-observations.md` are
  the whole of the response.
