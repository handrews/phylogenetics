# Closed-world question answering over recorded opinions: the second run

The run of 2026-09-12 (`eval/runs/2026-09-12-claude-sonnet-5.*`): 49
questions, Sonnet 5 composing blocks the tools return, graded
mechanically. The first run (`prose-eval-writeup.md`) had the model
write prose from four bare tools; this one has it write nothing. It
chooses what the question means in the corpus's terms, fetches blocks,
and submits a one-line header, the block ids in order, and a question
back when a parameter is ambiguous. The reader sees the rendered blocks
and nothing else. The purpose of this document, beyond the numbers, is
the catalogue of what the model composed, per class of question,
because step 2 (`notes/development/structured-answers.md`) is to be designed from
recorded compositions.

## The setup

What changed since the first run, against its closing list:

| closing-list item | landed as |
|---|---|
| a contents lookup | `contents(source, record)`: the classification a source prints under a node |
| not-found is not not-entered | prompt section "Gaps are not absences"; the gap block's sentence is the only refusal wording |
| tool outputs in the community's words | blocks rendered by style: classification listings, tables, synonymy lists, gap sentences |
| the history tool returns the measurement | `history` and `placements` carry the measurement as decorations (papers, years, co-author sets, last paper) |
| grading over what was composed | every expected claim must be carried by a composed block; leak, verdict and denial checks on the header only; free text beside the submission fails, text between lookups is noted |
| the judge sees only the header | Opus 5 scores the header and question back for contract (0–2): parameters only, community language, no verdict |
| eval upkeep | q045's rejection entered as data (`moved`); q033 asks what each paper prints; q010 and q019 left for the grader to re-test |

The corpus: 305 sources on record, 218 with a tree entered, 48 audited
against the paper; 13,802 claims. Eleven tools read the claim table
(`docs/claims.md`, "Reading the table"). The 49 questions
(`eval/questions.yaml`): 12 answerable, 8 as-published, 9 uncaptured, 3
absent, 17 trajectory.

The model had twelve lookups per question and was made to submit from
what it had at the limit. It made 257 lookups (median 4 per question,
max 18) and consumed 1.80 million input tokens (first run: 342 lookups,
2.34 million). Four questions reached the limit (first run: nine).
Every question ended in a composition; 34 compositions are one block,
12 are two, one is three, one is nineteen, one is none.

| tool | calls |
|---|---|
| resolve_name | 73 |
| statements | 45 |
| history | 27 |
| source_coverage | 22 |
| placements | 20 |
| contents | 18 |
| printed_forms | 18 |
| gap | 12 |
| synonymy | 10 |
| ancestors | 6 |
| descendants | 6 |

## The numbers

The two runs' mechanical columns are not the same test. The first
counted claims retrieved by any tool call; this one counts claims
carried by a composed block, which is stricter. The last column sets
aside the one failure that is about the transcript rather than the
answer, text written beside the `submit` call.

| class | n | first run | second run | free text set aside | judge contract | full marks |
|---|---|---|---|---|---|---|
| answerable | 12 | 2 | 8 | 9 | 1.83 | 10 |
| as-published | 8 | 8 | 4 | 6 | 1.75 | 7 |
| uncaptured | 9 | 7 | 6 | 7 | 2.00 | 9 |
| absent | 3 | 3 | 2 | 2 | 1.00 | 1 |
| trajectory | 17 | 9 of 16 | 5 | 8 | 1.59 | 11 |
| all | 49 | 29 of 48 | 25 | 32 | 1.71 | 38 |

Failures by check, over the 24 failed questions:

| check | selectors or questions |
|---|---|
| expected claim not carried by a composed block | 35 selectors in 13 questions |
| free text beside the submission | 11 questions, 7 of them failing for nothing else |
| no gap block for the source and kind | q015, q037 |
| no block stating the source is not entered | q038 |
| page named by the evidence not shown | q012 |

No header leaked a mechanism word, passed a verdict, or said a paper
lacks something, by the checks. No submission named a block id the
tools had not returned.

The judge gave 38 of 49 headers full marks (first run: 2 of 48
answers). Every lapse it found is one kind: the header states a finding
before the blocks do. Three headers scored 0 (q021, q039, q047) and
eight scored 1 (q002, q004, q030, q031, q033, q038, q042, q048); the
reasons read "pre-answers the question", "pre-announces the finding",
"asserts a finding". The first run's judge disagreed with the corpus;
this one disagrees with the model's habit of summarising, which the
checks (§1, §5 below) also see.

## Composition shapes

Blocks named by the tool that produced them, in submitted order, with
the count of questions composing that shape.

**answerable** (12; lookups median 2.5, max 9)

| shape | questions |
|---|---|
| contents | 6 |
| statements | 3 |
| history | 1 |
| ancestors + contents | 1 |
| contents + statements | 1 |

**as-published** (8; median 4.5, max 13)

| shape | questions |
|---|---|
| printed_forms | 3 |
| printed_forms + history | 1 |
| printed_forms + statements | 1 |
| printed_forms + printed_forms + statements | 1 |
| statements | 1 |
| history + history | 1 |

**uncaptured** (9; median 4, max 15)

| shape | questions |
|---|---|
| gap | 8 |
| statements + gap | 1 |

**absent** (3; median 6, max 16)

| shape | questions |
|---|---|
| gap | 1 |
| history + statements, with a question back | 1 |
| no block; the header states the absence | 1 |

**trajectory** (17; median 3, max 18)

| shape | questions |
|---|---|
| placements | 6 |
| history | 4 |
| ancestors | 1 |
| history + history | 1 |
| history + statements | 1 |
| printed_forms + history | 1 |
| printed_forms + statements | 1 |
| descendants + ancestors | 1 |
| history + contents × 18 | 1 |

Questions back: two. q038 says the corpus holds no source entry for
Klug et al. 2008 and offers the species' history instead; q048 says
Holloway & Jell 1983 record nothing about *Pyrgocystis octogona* and
asks whether another species was meant. Both state what the corpus
lacks; neither asks about a parameter.

Parameters set away from their defaults, over all 257 lookups: a
`source` on `contents`, `statements`, `printed_forms`, `synonymy` and
`gap` (point questions and refusals, 57 calls); a `kind` on
`statements` and `gap` (material, diagnosis, types, occurrences,
illustrations, synonymy; 29 calls); `synonymy: true` on `contents` (3);
`act_kind` (3); `rank` on the resolver (2); `include_synonyms: false`
(4, all q047); `years` (1, q029); `trees: ["cladogram"]` (2, both q049,
the question that asks for cladistic analyses). `include_variants` was
never turned off.

Three traces, as the run records them.

q004 (answerable): "What new genus and type species does Guensburg &
Sprinkle (1994) erect within family Astrocystitidae?"

    resolve_name  {"query": "Astrocystitidae"}
    contents      {"record": "astrocystitidae", "synonymy": true}
    submit        header: Guensburg & Sprinkle (1994) classification of
                  Astrocystitidae (emended); new genus and type species
                  new to the corpus
                  blocks: [the 1994 classification]

    Astrocystitidae emend.
      Astrocystites
      Cambroblastus
      Lampteroblastus*
        Lampteroblastus hintzei* [type]

q045 (trajectory): "Who proposed placing rhenopyrgids inside
Cyathocystidae, who followed, and who rejected it?"

    resolve_name  {"query": "Rhenopyrgidae"}
    resolve_name  {"query": "Cyathocystidae"}
    placements    {"records": ["rhenopyrgidae"], "include_variants": true}
    submit        header: Rhenopyrgidae/Rhenopyrginae placements relative
                  to Cyathocystidae; same-rank variants included;
                  classifications only; all years (1983–2020)

    schemes: Edrioblastoidina (Suborder): 3 papers (2013–2020), 3 co-author
    sets, last Ewin et al. 2020; Isorophida (Order): 1 paper (2010) …;
    Cyathocystidae (Family): 2 papers (1994–2000), 2 co-author sets, last
    Grigo 2000; …
    record                     Holloway & Jell 1983  Guensburg & Sprinkle 1994  Grigo 2000  …  Sumrall et al. 2013  …
    Rhenopyrgidae (Family)     [order uncertain]                                                Edrioblastoidina     …
    Rhenopyrginae (Subfamily)                        Cyathocystidae             Cyathocystidae

q019 (uncaptured): "Which earlier works does Fay (1962) cite in his
synonymy of Astrocystites ottawaensis?"

    resolve_name  {"query": "Astrocystites ottawaensis"}
    synonymy      {"record": "ottawaensis_whiteaves_1897", "source": "1962_fay"}
    gap           {"kind": "synonymy", "source": "1962_fay"}
    submit        header: Astrocystites ottawaensis (Whiteaves 1897),
                  synonymy as printed by Fay (1962); all years

    The synonymy printed in Fay 1962 has not yet been entered (only part
    of it is entered so far).

## What held

**Point questions collapsed to two or three lookups.** Seven of the
twelve answerable questions reached the lookup limit in the first run,
for want of a way to see what a source places under a node. None did
this time; the median is 2.5 and six of the twelve are a single
classification block. q004 above is the shape the design aimed at.

**Refusals are blocks.** Eight of nine uncaptured questions composed
the gap block for the source and kind, and the wording is the block's:
"has not yet been entered (only part of it is entered so far)". The
first run's "paper lacks" phrasing cannot occur, and the two mechanism
words the model did write, the coverage values "none" and "partly"
(q014, q017), it wrote between lookups, where the reader never sees
them.

**The first run's grader false positives are gone.** q019 passes.
q010's page check no longer fires; it fails only on an expected claim
the question does not ask for (below). q033, reworded to ask what each
paper prints, passes on a printed-forms list showing "Family
Edrioasteridae Bell, 1976 [emend. herein]" beside "Family
Edrioasteridae Bather, 1899".

**Trees are a parameter the model reaches for only when asked.** Every
lookup ran over classifications except the two for q049, which asks
for cladistic analyses. The default is right and the exception is
found.

**The closed world held.** Every composed block came from this
conversation; the header checks found no leak and no verdict; the
absent questions composed nothing about the missing taxon.

## What failed, and whose fault it is

### 1. Text beside the submission: the model's habit

Eleven questions carry text in the reply that calls `submit`, seven of
them failing for nothing else. The prompt now says in so many words
that the reply contains the call and nothing else. The text is
commentary on the composition ("This directly answers the question with
the placements table.", "The gap block answers this directly.") and
three times a summary of the answer (q001, q006, q027). The reader
never sees it. Under step 2 the output is a plan and the habit has
nowhere to go; for a third run under step 1 the grader could note it,
as it notes text between lookups, and the count is the measure of
prompt-following.

### 2. Source keys are guessed: a tool-shape gap

Twenty-eight lookups in seven questions passed a source key the corpus
does not have: `dehm1961`, `dehm-1961`, `Dehm 1961`, `dehm61`,
`sumrall-et-al-2013`, `1983_holloway.jell`, `guensburg_sprinkle_1994`,
and nine spellings of Klug et al. 2008. Two questions (q015, q038) spent
nine lookups each on this and reached the limit. The blocks the model
sees cite sources as the community does ("Dehm 1961") and never show
the key, and no tool turns a citation into a key. q038 shows a second
face of the same gap: the source is not in the corpus at all, and
`source_coverage` says "known: false" for a misspelt key and for an
absent paper alike.

The fix is either: the compact view of every block lists its source
keys beside the citations (the placements table already carries them
as `sourceKeys`), or every `source` parameter accepts a citation
("Dehm 1961", "Sumrall et al. 2013") resolved the way names are, by
folded author name and year. The second also gives the model a way
to say "Klug et al. 2008" and be told the corpus has no such source.

### 3. An absent name has no block

q039 asks about *Rhenoblastus*, which no source carries. The resolver
returned nothing, twice, and the model wrote the fact into the header:
"no source in the corpus carries this name, so no placement record
exists for it." The grader counts the empty composition as a pass, but
the sentence belongs in a block and there is none: `gap` speaks of a
source and a kind of statement, not of a name. A resolver that finds
nothing should return the statement block ("No source in the corpus
carries the name Rhenoblastus"), so the absence is composed like every
other refusal.

### 4. Blocks carry fewer claims than they show

Eight expected claims in five questions sit at the same node as a claim
the composed block carries, in a kind the block does not list.

| question | composed | carried at the node | expected |
|---|---|---|---|
| q045 | placements of Rhenopyrgidae | placement | the nomen translatum (1994), the emendation and the rejection (2013) |
| q031 | placements of *P. octogona* | placement | the usage in each source |
| q024 | printed forms of the subgenus | usage | the act naming it new |
| q023 | printed forms in Bassler 1936 | usage | the acceptance whose printed form it is |
| q010 | material statements | material | the act naming the species new |

The placements table shows Rhenopyrginae under Cyathocystidae in 1994
and 2000 and Rhenopyrgidae under Edrioblastoidina from 2013, which
answers "who proposed" and "who followed"; "who rejected it" is a
rejection statement at the 2013 node that the table neither shows nor
carries, and the model did not fetch the statements table that would.
The classification block already carries a node's acts and shows them
as marks; the tables should carry every claim at the node the same way,
and a placements cell could mark a rejection as the listing marks an
act. q010 is the exception: the question asks for a holotype number, the
material table shows it, and the expected act is the expectation's
excess.

### 5. Expectations written for one route

Twenty-seven expected claims in nine questions exist in the corpus and
were not fetched, because the model took a different route to the
answer.

- q036, q043, q046 ask at what rank the edrioblastoid group has been
  treated and by whom. The expectations list the members' placements
  under Edrioblastoida and Edrioblastoidina as the evidence. The model
  composed the group's history, whose rank rows rest on the group's own
  usage claims: "latest rank: order: 3 papers 1990–2021, 3 co-author
  sets, last Jell & Sprinkle 2021; earlier ranks: suborder: 6 papers
  1994–2020; class: 9 papers 1962–1982". That is the direct route and
  the expectations do not admit it.
- q041 and q044 ask which family name was used for *Astrocystites* and
  by whom, and what each paper does to the group; the expectations
  include the acts erecting Steganoblastidae (Bather 1900) and
  Astrocystitidae (Bassler 1935). The model composed placements (q044)
  and the group's history with the classification each source prints
  (q041, nineteen blocks). The acts are on the families' own nodes,
  which none of those blocks visit.
- q032 asks what class or order *Astrocystites* has been placed in and
  expects, besides the placements, Fay's act erecting the class. q006
  asks for the type species Sumrall et al. 2013 confirm and expects an
  emendation.
- q047 asks which taxon has the most distinct placements. No block
  computes that. The model fetched the descendants and nine placements
  tables, chose one, and wrote the comparison into a hundred-word
  header ("the family Cyathocystidae … is the taxon carried across the
  most sources, having been placed under five distinct parent taxa …
  as many distinct placements as its closest rival"): a verdict in all
  but the checked words, and the clearest case for step 2.

For the first three groups the selectors should admit either route:
the members' placements or the group's usage at each rank. q047 needs
a measurement over a closure (distinct parents per descendant) that a
plan language must be able to express.

### 6. Gap kinds and sources not on record

q037 composed `gap(1897_whiteaves, types)` for a type-species
designation; the expectation says `newTaxa`. Whiteaves 1897 has no tree
entered, so the block says the same sentence for any kind: "is on
record; its content has not yet been entered". The grader should accept
any kind for an unentered source. q038's scope names a source key that
is not in the corpus; the model's question back says exactly that, and
the grader wants a statement block, which the source-key fix (§2)
would let it compose. q015 is §2 entirely: the right blocks were
fetched under the wrong key and came back empty.

### 7. Pages in classification blocks

q012 composed the classification of Rhenopyrgidae in Ewin et al. 2020,
which names the two genera the question asks for; the evidence names
p. 118, the block's top claim carries it, and the listing style prints
no pages. Either the style prints the page of the top node or the check
exempts classifications.

## Against the first run's failure modes

| first run | second run |
|---|---|
| over-exploration to the limit on point questions | gone: answerable median 2.5 lookups, none at the limit |
| not-found recorded as not-entered | gone: refusals are gap blocks keyed to declared coverage |
| mechanism leaks in the answer | gone from the answer; two coverage values written between lookups, unseen |
| a count read as a citation | not observed |
| trajectories as history, not measurement | the measurement is in the block header; the failures are route mismatches (§5) |
| refusals complete as refusals | 8 of 9 uncaptured composed; the ninth lost to source keys (§2) |
| new | source keys guessed (§2); the absent name has no block (§3); blocks carry fewer claims than they show (§4) |

## The third run

The run of 2026-09-14 (`eval/runs/2026-09-14-claude-sonnet-5.*`): the
same 49 questions after the answer shapes (chains, `placed_under`, the
Systematic Paleontology listing, the timeline, statements as sentences,
the absent-name block) and after every source argument began to accept
a citation. A smoke, not a verdict: the eval's expectations still name
claims, and the shapes are what the next eval should be written
against.

| | second run | third run |
|---|---|---|
| lookups | 257 (median 4, max 18) | 228 (median 3, max 16) |
| input tokens | 1.80 M | 1.72 M |
| at the lookup limit | 4 | 3 |
| source arguments the corpus could not resolve | 28 in 7 questions | 6 in 4 questions |
| free text beside the submission | 11 questions | 5 |
| questions back | 2 | 0 |
| mechanical pass | 25 | 26 |
| judge contract, full marks | 1.71, 38 | 1.82, 42 |

| class | n | second run | third run |
|---|---|---|---|
| answerable | 12 | 8 | 6 |
| as-published | 8 | 4 | 5 |
| uncaptured | 9 | 6 | 4 |
| absent | 3 | 2 | 3 |
| trajectory | 17 | 5 | 8 |

**Citations replaced keys.** Twenty-four source arguments were
citations the resolver turned into keys; `resolve_source` was called
27 times, usually once per question before the first lookup. Five of
the six unresolved arguments are one habit, the ampersand written as
an HTML entity ("Holloway &amp; Jell 1983"), which the resolver now
tolerates; the sixth is Klug et al. 2008, which the corpus does not
have, and the answer composed the absent-source block for it. No
question ran to the limit on keys; q015, sixteen lookups in the second
run, took three.

**The new shapes were reached for.** Every absent question composed
the gap block, q039 by name. `placed_under` was used twice, both on
q045 ("who proposed, who followed, who rejected") and composed with
the matrix; `ancestors` five times as chains. The trajectory class
composed history alone in five questions and rose from 5 to 8 passes
with 13 of 17 headers at full marks.

**One regression, from the shapes.** Uncaptured fell from 6 to 4: in
q013, q015, q018 and q020 the model asked `statements` for one kind in
one source, got an empty list, and composed it. The second run's empty
table looked as empty, but the model went on to `gap`; the sentence
list's bare heading reads as a finished answer. `statements` now
returns the gap block itself when a source is named and nothing of the
kind is entered (commit on the same branch), so the block the model
stops at is the right one.

**What stays.** The route-specific expectations (§5) account for the
rest of the failures: q036, q043, q046 composed the group's history,
q041 and q044 the matrix, q047 wrote its comparison into the header
again (judge 0). q001 composed the genus's listing in Fay 1962, which
does not carry the class's act above it. Two classification blocks
were composed whose evidence page is not rendered (q009, q012); the
listing's heading now carries the page when the root has one, which
covers q012.

## The fourth run

The run of 2026-09-14, later the same day
(`eval/runs/2026-09-14b-claude-sonnet-5.*`): 47 questions under the
rewritten eval, whose expected answers are shapes with parameters and
the strings the rendered answer must show. The first run the grader
scores on what a reader would see.

| | third run | fourth run |
|---|---|---|
| questions | 49 | 47 |
| lookups | 228 (median 3, max 16) | 215 (median 3, max 20) |
| input tokens | 1.72 M | 1.62 M |
| at the lookup limit | 3 | 3 |
| source arguments the corpus could not resolve | 6 in 4 questions | 1 (Klug et al. 2008, which it lacks) |
| free text beside the submission | 5 questions | 12 |
| mechanical pass (free text set aside) | 26 (31) | 32 (41) |
| judge contract, full marks | 1.82, 42 | 1.77, 38 |

| class | n | pass | free text set aside |
|---|---|---|---|
| answerable | 12 | 8 | 11 |
| as-published | 8 | 5 | 6 |
| uncaptured | 9 | 7 | 8 |
| absent | 3 | 3 | 3 |
| trajectory | 15 | 9 | 13 |

The third run re-graded by the new grader scores 35 of 47, so the two
grades are comparable and the model did not change much between them;
what changed is what is measured.

**Routes are no longer failures.** q032, q036 and q043 pass on the
group's history. Six expectations gained an alternative after this
run, where the model's route was as good as the one written: the
entered part of a diagnosis beside the gap for the rest (q017), the
synonymy list beside the gap (q019), the chains beside the history
(q044, q049), and the material statements without a kind filter (q010,
q011). Those are recorded here because the run's grades were computed
after the change.

**What still fails on substance.** Five questions: q009 composed
Grigo's listing without the occurrence gap ("from where"); q024 fetched
Dehm's printed form but not Sumrall et al.'s citation of the type
species; q028 composed the subfamily's history where the question asks
for the exact printed heading, which only the listing shows; q035
composed statements and chains for two genera whose attribution the
history states in its heading; q048 did not compose the gap for
Holloway & Jell's synonymy. All five are the model's choice of shape,
not a tool's or the grader's.

**Text beside the submission is now the main failure.** Twelve
questions, nine failing for nothing else: "This confirms the answer
with the contents block", "This single timeline block answers the
question fully". The reader never sees it and the prompt forbids it;
the habit is the model's, and it grew from five questions to twelve
with no prompt change. A run that set it aside would pass 41 of 47.
Whether to keep failing it is a contract decision, not a tooling one.
Decided the same day: it is noted, not failed, from the next run on,
since it costs a few hundred output tokens a run and reaches no reader.

## The planner run

Step 2: the model resolves names and citations, then states a plan
(header, blocks as tool and parameters, question back) and code builds
the composition. Two runs the same day (`eval/runs/2026-09-14-planner-a-…`
and `-b-…`, 47 questions each). Run a was spoilt by one habit the
executor let through: `trees: "classification"` and `years: "all"` as
strings, which the tools took as tuples of characters, so twenty-odd
blocks came back empty ("no source uses the name"). The executor now
refuses a parameter of the wrong type with the type and the reason,
and the prompt names the values; run b followed.

| | fourth run (compose) | planner run b |
|---|---|---|
| lookups | 215 (median 3, max 20) | 105 (median 2, max 8) |
| input tokens | 1.62 M | 0.41 M |
| output tokens | 44 k | 37 k |
| wall time | ~25 min | ~8 min |
| at the lookup limit | 3 | 0 |
| plans revised after an error | – | 1 (q019) |
| questions back | 0 | 0 |
| mechanical pass | 32 | 34 |
| judge contract, full marks | 1.77, 38 | 1.81, 38 |

| class | n | compose | planner |
|---|---|---|---|
| answerable | 12 | 8 | 8 |
| as-published | 8 | 5 | 5 |
| uncaptured | 9 | 7 | 6 |
| absent | 3 | 3 | 3 |
| trajectory | 15 | 9 | 12 |

**The same answers for a quarter of the tokens.** The planner never
sees a block, so a question costs its resolver calls and one plan; the
fourth run's 1.6 million input tokens were the rendered blocks the
model read and discarded. Pass rates are level with compose mode and
the trajectory class is better: the plans reach for history and the
chains and get them right first time.

**Three grader and tool changes came out of run b.** A gap block the
`statements` tool returns for an empty query now counts as the gap the
expectation names (the planner asks `statements` for material in a
source rather than `gap`, and is right to); `statements` takes
`occurrences`, `illustrations` and `specimens` as kinds; and a gap so
returned keeps the coverage kind as its own parameter. The grades above
are what the run's records show; q014, q015 and q016 would pass on a
fresh run with those changes. Two expectations gained the chains as an
alternative (q029, q031).

**What fails on substance.** The planner chose `statements` for a
genus's type species (q003, q006) and `ancestors` for Fay's class
(q001), where only the listing shows what is asked; the prompt now says
so. The rest are the fourth run's misses again: q009, q024, q028, q034,
q045, q048.

**What the plans look like.** Forty-two of 47 are one block; four are
two; none is more. Every parameter varied in compose mode was varied
here (source, kind, act_kind, synonymy, years, trees, include_related),
and the header is written before any block exists, which shows in the
judge's marks: 38 of 47 at full, none at zero.

## The planner run repeated

Run c (`eval/runs/2026-09-14-planner-c-claude-sonnet-5`) is the planner
again after the changes run b prompted: the gap `statements` returns
keeps the coverage kind, and the prompt says a genus's type species and
a new class are shown by the listing. Same 47 questions, same grader.

| | planner run b | planner run c |
|---|---|---|
| lookups | 105 (median 2, max 8) | 128 (median 2, max 10) |
| input tokens | 0.41 M | 0.57 M |
| output tokens | 37 k | 48 k |
| wall time | ~8 min | ~10 min |
| at the lookup limit | 0 | 1 (q021) |
| plans revised after an error | 1 | 0 |
| questions back | 0 | 0 |
| mechanical pass | 34 | 36 |
| judge contract, full marks | 1.81, 38 | 1.79, 38 |

| class | n | run b | run c |
|---|---|---|---|
| answerable | 12 | 8 | 9 |
| as-published | 8 | 5 | 5 |
| uncaptured | 9 | 6 | 9 |
| absent | 3 | 3 | 3 |
| trajectory | 15 | 12 | 10 |

**What the fixes bought.** q014, q015 and q016 pass: the gap for
material in a named source now matches whichever tool states it. q003
and q006 pass: the plans ask `contents` for a type species. q001 still
plans `ancestors` for Fay's class, and the chain does not print the
"nov." the listing does.

**What moved the other way.** Three questions that passed in run b
fail here on the block chosen: q002 plans `statements` about the genus
with `act_kind: type` beside the listing, where the expectation is the
statements about the species in Fay 1962 (the editor's designation is
a statement about *ottawaensis*); q035 plans `printed_forms` for two
genera where a history is asked; q044 plans `placed_under` twice
instead of a history. Nothing in the tools or prompt changed for these
three: the planner's choice varies between runs on a handful of
questions, which is the noise floor of a 47-question set with one run
per configuration. Thirty-nine plans are one block, eight are two.

**Tokens.** Input rose with the lookups (q021 spent its twelve turns
resolving suborder names); still a third of compose mode.

## The planner run after the block-choice fixes

Run d (`eval/runs/2026-09-14-planner-d-claude-sonnet-5`) follows three
tool fixes, an eval change and one prompt sentence, all prompted by
run c's misses. `statements` for a record in a named source with no
kind asked now says nothing about the record is entered from that
source and names every kind of the source not yet entered, instead of
"the classification is entered in full" alone (q048). `printed_forms`
for a source that recorded no verbatim form gives the heading as the
listing is entered, marked as such, instead of nothing (q028). The
listing's "Type species." line marks the editor's inference (q002),
and a synonymy listing says whose it is. An expected alternative may
carry its own `shows`, so a plan that renders the same fact in other
words is accepted: two `placed_under` blocks for q044, the timeline's
"declines a placement in Cyathocystidae" for q045, the statements
route for q048. The prompt says the plan is final, after run c planned
a "probe" for q009.

| | planner run c | planner run d |
|---|---|---|
| lookups | 128 (median 2, max 10) | 114 (median 2, max 20) |
| input tokens | 0.57 M | 0.56 M |
| output tokens | 48 k | 48 k |
| wall time | ~10 min | ~11 min |
| at the lookup limit | 1 | 0 |
| plans revised after an error | 0 | 0 |
| questions back | 0 | 0 |
| mechanical pass | 36 | 41 |
| judge contract, full marks | 1.79, 38 | 1.77, 39 |

| class | n | run c | run d |
|---|---|---|---|
| answerable | 12 | 9 | 11 |
| as-published | 8 | 5 | 5 |
| uncaptured | 9 | 9 | 9 |
| absent | 3 | 3 | 3 |
| trajectory | 15 | 10 | 13 |

**Level with compose mode.** Forty-one of 47 is the fourth run's figure
on the same yardstick (`metrics.md`), at a third of its input tokens.
Five questions turned: q002, q009, q044, q045 and q048; none turned
the other way. Two of the five (q044, q045) passed because the eval
now admits the plan the model chose; the other three because the
blocks it chose say more than they did.

**What remains.** q001 plans the chain where the listing is asked;
q021 needs the suborder name from the first block to parameterise the
second, which a plan cannot express; q024, q034 and q035 prefer a
listing, a timeline or the printed forms where the expectation wants
another; q028 resolved "the Rhenopyrgus subfamily" against the genus,
found no subfamily-rank variant there (Rhenopyrginae is a rank variant
of the family, not the genus) and planned the gap for a name the
corpus does carry, which is a wrong answer, not a wrong shape.

**The judge's three zeros** are all headers that state a finding. One
is false: q002's header says the type species is "marked as printed"
when the listing marks it as the editor's inference, which is the
question's point. The header is the one place the model still speaks
in its own words, and the judge is there for exactly this.

## What changes next, in order

1. Source keys: citations accepted wherever a source is a parameter
   (done 2026-09-14: `resolve_source`, every source argument takes a
   citation). Closes §2 and q015, q038.
2. A statement block for a name no source carries (done 2026-09-13:
   `gap(name=…)`). Closes §3.
3. Tables carry every claim at a node and the placements cell marks a
   rejection (done 2026-09-13). Closes §4 except q010.
4. Eval upkeep (done 2026-09-14: expected answers are shapes with
   parameters and shows strings; q046 and q047 dropped).
5. Step 2 (done 2026-09-14: `phylohist/plan.py`, planner mode, the
   planner run above). What remains open: an operation mapped over the
   sources a closure returns, and a measurement over a closure (the
   dropped q047), neither of which a plan can yet express.
