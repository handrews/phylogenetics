# Structured answers: the AI as query planner, not narrator

Discussion notes, 2026-09-11, after the first eval run. Nothing here is
decided; it is the owner's framing and the responses it prompted, kept
so the next planning pass starts from it.

## The owner's frame

- This is a project about structured, closed-world data. What AI brings
  is not narrative synthesis but flexible, complex, multi-step, iterative
  queries that SQL or a graph database could not express. The desired
  result looks like the rows a query returns, assembled coherently, not a
  conversation.
- Worked example: "under what higher taxa have edrioblastoids been placed
  across the entire corpus?"
  1. Decide which records constitute "edrioblastoids" (Edrioblastoidea,
     Edrioblastida, Edrioblastoidina: one name at three ranks).
  2. Find everything any source has ever placed under them, transitively
     and including synonyms: Pentacystida; Astrocystitidae (with
     Steganoblastidae), Cyathocystidae, Rhenopyrgidae; Cyathocystinae,
     Rhenopyrginae; Astrocystites (with Steganoblastus), Cambroblastus,
     Lampteroblastus, Porosublastus, Ikerus, Cyathocystis, Cyathotheca,
     Rhenopyrgus, Heropyrgus, and their species.
  3. Find every higher taxon any of those has been placed under, in any
     source: Echinozoa, Edrioasteroidea, Edrioasterida, but also
     Blastoidea, Cystidea/Cystoidea, Cyathocystida, perhaps Crinoidea for
     the oldest species. Beyond what one head holds.
  4. Assemble a lower-to-higher map, concise, tabular.
- Users want the essential information efficiently and will ask for more;
  a wall of narrative is the wrong default even when the writer likes
  writing walls.
- The AI's critical role: flexible data-finder and correlator.
- Answer templates: the AI fills a fixed shape (finding the right things
  is the hard part) and has little room to add; mechanical code can
  validate that every value in the template comes from the corpus.
- The CLI prints ASCII classification trees with minimal information,
  mimicking a "Systematic Paleontology" section; it does one thing and is
  completely reliable. The aim is that reliability inside the multi-step
  frame.

## What the eval run says about this frame

The run supports it rather than merely tolerating it.

- The class that behaved was the structured one. As-published answers,
  which reproduce a printed form and cite it, passed 8 of 8. The
  narrative class, trajectories, failed on counting, on ordering and on
  verdict-like phrasing, and the judge could not even grade it reliably.
- Every failure mode in the write-up is a narrative failure or a search
  failure. Leaks of the table's vocabulary, miscounts, "stands unopposed",
  history-before-present: all are properties of prose the model composed.
  The search failures (guessing genus names, "not found" recorded as
  "not entered") are the model doing by hand what a closure query does
  in code.
- Mechanical grading worked where the answer was structured and failed
  where it was prose. A template answer makes grounding a check on cells
  rather than a judgement on sentences.

## Three layers, and which one the AI owns

The worked example separates into three kinds of work, and only one of
them needs a model.

1. **Planning.** Decide what the question means in the corpus's terms:
   which records are "edrioblastoids", whether "placed under" includes
   synonymised names, whether "higher" means every ancestor or the
   nearest, whether rank variants of one name count as one group. These
   are judgements; they are the flexible part; they are what SQL cannot
   do because the parameters are not known until a reader with taxonomic
   sense picks them.
2. **Execution.** Given the parameters, every step is deterministic:
   descendants of a set of records across all sources (transitive,
   through acceptance claims for synonyms, through the rank-variant
   links for one name at several ranks); ancestors of a set across all
   sources; counts by position and year and co-author set. Code does
   this exactly; a model does it by guesswork twelve lookups at a time.
3. **Assembly.** Render the result in a shape a reader expects, with
   every cell carrying the statement it came from.

The AI owns layer 1 and chooses the shape in layer 3. Layers 2 and 3 are
code. The first eval asked the model to do all three in prose, and the
failures line up with layers 2 and 3.

## Answer templates as the community's own genres

The shapes need not be invented. The literature already has structured
forms, and readers know how to read them:

- **Classification listing**: the indented tree the CLI already prints;
  a "Systematic Paleontology" section. Answers "what does source S
  place under X".
- **Synonymy list**: the dated list under a species heading. Answers
  "which earlier usages does S accept or reject". The CLI does not print
  these yet; adding them is small.
- **Placement table**: rows are taxa, columns are sources in year order,
  cells are the parent (and rank) each source gives. Answers the worked
  example and every "where has X been placed" question. Rank variants and
  synonyms fold into a row with their record named.
- **History table**: one row per source in year order: position, rank,
  act, printed form, page. Answers a trajectory; the "measured present"
  is a header computed by code (positions, papers and co-author sets per
  position, the last paper for each), not prose the model counts out.
- **Gap statement**: source, kind of statement, declared coverage, and
  the sentence "has not yet been entered". Answers uncaptured and absent
  questions with no room to add.
- **Printed-form line**: source, page, the form verbatim, the record it
  resolves to. Answers as-published questions.

Each template is a JSON structure that a renderer prints and a validator
checks: every taxon key, source key, page, rank word and printed form
must exist in the claim table, and every cell must name the claim that
supports it. The answer becomes verifiable data. This is the owner's
standing stance (gathering and querying separated by a verifiable data
model) applied to the answer itself.

Where the judgement lives is then visible: the template's header states
the parameters the planner chose ("edrioblastoids taken as
Edrioblastoidea, Edrioblastida, Edrioblastoidina; membership through any
source's placement; synonyms included"). A reader who disagrees with a
parameter can ask again with a different one; an eval can check the
parameters against the expected ones as selectors, exactly as it checks
claims now.

## Drill-down instead of detail

"Ask for more" needs a handle. If every cell carries its claim id, a
follow-up ("expand the Cyathocystidae row", "show the 1994 statement")
is a query over the previous answer, and the conversation's state is a
table, not a transcript. The first answer stays short because the
second is cheap.

## Where prose still belongs

- The planner's parameters, one line, so the reader knows what was
  counted.
- A question back when the parameters are ambiguous ("Edrioblastida is
  used by two sources for the same group; include it?"). A question is
  the right narrative; a story is not.
- The printed sentence when the question is about the printed sentence.

Everything else the run produced as prose (history retold, comparative
asides, "this contrasts with later authors") is either a row in a table
the reader did not ask for or a verdict.

## What this says about notes in the trees

The draft trees' notes were the open question of the day: too much
narrative, and eval answers seemed to lean on it. In this frame the
answer is mechanical.

- A structured query cannot see a note. Whatever a question should be
  able to retrieve must be a field. The run showed the cost: q045's
  expected rejection lives in a review's notes, not in the tree, so the
  table holds no rejection and the model's "no rejection is recorded"
  was correct. The note was invisible where it mattered.
- So the criterion for a note is: does any query need its content? If
  yes, it is a missing field (rejectedPlacements, secondhand, a quoted
  diagnosis, a type fixation method) and belongs on the roadmap. If no,
  the note is for the human auditor, and the auditor's material belongs
  in the review file, with the tree note reduced to the fact, the page
  and the printed words when the words matter.
- The draft notes that recount the paper's history, the OCR provenance
  and the scratch filenames are review material. The tree should carry
  the page and the quotation; the review carries the reasoning.
- This also settles the eval: an expected answer may rest on a field,
  never on a note. Where today's expected answers quote notes, each is
  either a field to add or an expectation to trim.

## Gap-filling under this frame

The write-up found gap-filling contained for the literature and not for
the search or the corpus's own state. Templates and closure tools remove
both occasions: there is no search to guess in when the descendants of a
node are one call, and there is no "not yet entered" to reach for when
the declared coverage sits in the gap template as a field the model must
copy rather than infer. What remains is the planner choosing parameters,
and that is where an inference would show, in the header, where it can
be read.

## Open questions

- How much flexibility the template set costs. A fixed set of six shapes
  may not fit every question; the alternative is a small generic table
  whose columns the planner picks from the claim fields. The first is
  safer, the second is the "flexible query" the frame wants. Probably
  both: named genres for the common shapes, a generic table behind them.
- Whether the planner should emit a plan (a composition of closure and
  history calls with parameters) that code executes, rather than calling
  tools one at a time. That is the cleanest form of "AI writes the query,
  code runs it", and the eval then checks plans. It is a larger change
  than adding tools.
- Which closure semantics the corpus can support today: descendants
  through `children` are exact; through synonyms they depend on
  acceptance claims; across rank variants they depend on `altRankOf`
  links, ten of which are missing (the nomen translatum nodes without a
  linked record).
- Whether a trajectory's "measured present" should be defined in code
  once (the latest position by year, counts per position, co-author
  sets as units) so that every history answer carries the same
  measurement; the contract in `eval/README.md` already says what it is.

## Follow-up, 2026-09-12: building blocks, and two steps

The owner's clarification: not a fixed set of templates but a planner
that hands off to code, plus building-block shapes for answers. A block
such as the classification listing can stand alone, be repeated (one
per competing scheme), or be extended (a relationship annotated with
how often it occurs in publications over a time range, the whole corpus
by default). On the output side the AI chooses, assembles and extends
blocks; it does not convert data into narrative.

Refinement: the extension is a computed decoration on an edge of a
block, and it is the "measured present" generalised. A count over
sources and years on a placement edge is the trajectory's measurement
without a paragraph; competing schemes are the same block instantiated
once per group of sources sharing a placement, and grouping sources by
the placement they give is a computable operation. The trajectory class
becomes blocks plus decorations.

Block vocabulary, first cut:

- classification (a tree; the CLI's block; edges carry claim ids)
- table (rows and typed columns, cells carry claim ids; the placement
  table and the history table are instances)
- list (a synonymy list under a heading)
- statement (a gap statement, a printed-form line)
- decorators over any of them: counts by source and year range,
  co-author sets as units, last source for a position, provenance
  footnotes
- a one-line header: the parameters the planner chose

### Step 1: tools return blocks; the model composes them

On the architecture that exists. Each tool returns a block rather than
raw claims: `contents(source, node)` a classification block;
`placements_of(records, sources?)` a placement table with the sources
grouped by the parent they give; `history(record)` a history table with
the measurement computed as its header; `gap(source, kind)` a statement.
Closure operations (descendants and ancestors of a set across sources,
through acceptance claims and rank-variant links) feed them. The model
still calls tools one at a time, but its answer is a composition: a
list of blocks, each one returned by a tool call in the conversation
(carrying an id or hash), plus the header and, when needed, a question
back. Code renders; a validator confirms every block came from a tool
result, so grounding is checked with no judge.

What it closes: write-up fixes 1, 3, 4 and 5. What it reuses: the tool
library, the runner, the grader (which now checks blocks and headers
against selectors). What it produces besides answers: a record of
which compositions the model reaches for, question by question.

### Step 2: the planner emits a plan; code executes it

The model's output becomes a plan: a composition of closure,
measurement and block operations with their parameters, in a small
query language, instead of a sequence of tool calls. An executor runs
the plan deterministically, the renderer prints the blocks, and the
validator is unnecessary because a plan can only name corpus
operations. "Ask for more" is an edit to the plan. The eval checks plans
(operations and parameters) against expected plans, and the parameters
are the one place a judgement can hide.

Why second: the language should be designed from the compositions step
1 records, not guessed; and the closure semantics need to be complete
first (ten nomen translatum nodes lack the rank-variant link, so a
closure across ranks is not yet exact). Step 1 is a few days on the
current code; step 2 is a design.
