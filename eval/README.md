# Eval set v1

Questions over the gold slice, Edrioblastoidea (Astrocystitidae) and
Rhenopyrgidae, written before the claim table exists so that they say what
it must be able to express. `questions.yaml` holds them; `docs/claims.md`
is the vocabulary their expected answers are written in.

## The answer contract

| class | what the data holds | the right answer | the shape |
|---|---|---|---|
| answerable | a claim exists | the claim, cited by source and page | the source's listing under the record (`contents`), or the statements about it |
| uncaptured | the paper prints it; the corpus does not hold it (a declared coverage of `none` or `partly`, or a source recorded with no tree entered yet) | "not captured for <source>", with the declared coverage value; never "not in the paper" | the gap block for the source and kind |
| as-published | the printed form differs from the record or from later usage | the printed form verbatim, cited; a correction only if asked | the printed forms in that source |
| trajectory | several sources treat the same question over time | the measured present, then the history, then the dissent; no verdict | the name's history, the sources holding a position, the matrix, or the chains |
| absent | nothing in the corpus mentions it | "no source in the corpus mentions <x>"; no answer from general knowledge | the gap block for the name or the paper |

An expected answer is written as the blocks it is made of, each a tool
and the parameters that matter, with alternatives under `anyOf` where
two compositions are both right, and the strings the rendered answer
must show:

    expected:
      blocks:
      - tool: placed_under
        parameters: {record: rhenopyrgidae, parent: cyathocystidae}
      shows:
      - first Guensburg & Sprinkle 1994
      answer: |
        (the answer in prose, for the reader)

The contract is the closed-world rule of `notes/development/plan.md` made testable: an
answer is right only when every fact in it is a claim, cited, and every
gap is named as a gap of the data rather than of the literature.

## Trajectory answers

Science is dynamic; disagreement is how it moves, and this tool exists to
make that movement visible, not to treat it as a fault to resolve. A
trajectory answer therefore:

1. leads with the measured present: how many papers in the corpus hold the
   latest position, over what years, from how many distinct sets of
   co-authors;
2. then gives the history: who proposed each position and when, and the
   last paper to hold each earlier one;
3. names dissent with source and year, and reports a rejection stated by a
   source as such;
4. gives no verdict. "Treated as a genus by every paper since 1983, six
   papers from five co-author sets" is a measurement; "it is a genus" is
   not ours to say.

Counting rule: each publishing set of co-authors is one unit. Papers that
share an author are not merged; the overlap is stated as an observation
("Jell appears in two of them"). A researcher can hold different positions
with different co-authors, and a multi-author paper states the position
the group settled on, which every author need not share.

## Language

Answers are written for researchers who read the literature, in the
words of the scientific community. They never mention files, YAML,
records as storage, internal field names or mechanisms, or how a fact is
held; they say what the corpus credits, where a source places a name, and
whether a statement is the source's or the editor's. A translated name is
a nomen translatum, not an "alternate-rank form".

They never leak scope, schedule or planning: no gold slice, milestone or
demo, and no opinion on how important a gap is. A gap is stated as a fact
about the corpus, in a form that assumes the work goes on: "the material
printed there has not yet been entered", never "was not entered" as a
finished judgement, and never a word that reads as a reproach to whoever
entered the data. Readers judge the implications themselves.

## The entries

```yaml
- id: q001
  class: answerable
  question: In which family does Holloway & Jell 1983 place Rhenopyrgus?
  scope: {taxon: rhenopyrgus, source: 1983_holloway_jell}
  expected:
    blocks:
    - tool: contents
      parameters: {source: 1983_holloway_jell, record: rhenopyrgidae}
    shows:
    - Family Rhenopyrgidae fam. nov.
    - Genus Rhenopyrgus
    answer: Rhenopyrgidae, a new family; the order is left uncertain.
  evidence: {source: 1983_holloway_jell, pages: 1002}
  verified: data/trees/1983_holloway_jell.yaml, taxonomies/0/children/0/children/0/children/0
```

`expected.blocks` names the tools and the parameters that matter; a
parameter left out is not graded, so a composition that also asks for
synonymy or a year range still matches. Alternatives go under `anyOf`;
an alternative that renders differently carries its own `shows` beside
its `blocks` (`anyOf: [{blocks: […], shows: […]}, …]`).
`expected.shows` are the strings the rendered answer must contain
whichever alternative it takes, taken from the rendering of the
expected blocks. `verified` says what
was checked when the question was written: the tree path, the
`audit.coverage` value, or the review file with the printed page.

## Running the eval

`eval/system-prompt.md` is the closed-world prompt: compose only blocks
the tools return, name a gap as not yet entered, follow the trajectory
contract and the language rules above.

    poetry run python scripts/eval_run.py --model claude-sonnet-5
    poetry run python scripts/eval_grade.py eval/runs/<date>-<model>.jsonl
    poetry run python scripts/eval_run.py --ask "Who first placed Rhenopyrgus under Edrioblastoidina?"
    poetry run python scripts/eval_run.py --mode planner --model claude-sonnet-5

Two modes. In `compose` mode, the default, the model calls the tools,
reads the rendered blocks and submits the ids of the ones to show. In
`planner` mode (`planner-prompt.md`) it may call only the two
resolvers, then states a plan: the header, the blocks as tool and
parameters, the question back; `phylohist.plan.execute` builds the
composition and returns what could not be built once for a revised
plan. The model never sees a block, so the run costs a fraction of the
input tokens, and the plan is the form the expected answers take.

`--ask` answers one question typed on the command line exactly as a run
would (same prompt, tools and composition step), prints the rendered
answer and then the trail (the lookups, the header, any question back,
any text the model wrote beside its calls, the tokens), and writes
nothing.

The runner answers every question in a bounded tool-use loop over
`phylohist/tools.py`. The model sees each block's id, type and rendered
text and finishes by calling `submit`: a one-line header stating the
parameters it chose, the ids of the blocks to show in order, and a
question back when a parameter is ambiguous. The runner validates the
submission against the blocks it kept, renders the composition, and
writes `eval/runs/<date>-<model>.jsonl`: the question, each tool call,
the composition (header, blocks with their types, parameters and claim
ids, question, any invalid ids, any free text), the rendered answer,
token usage and the prompt's hash. At the lookup limit the model is
made to submit from what it has, and the record says so. Runs are
committed; they are the evidence the write-up rests on. The grader
(`scripts/eval_grade.py`, whose checks are `phylohist.evaluation`) is
mechanical: for one of the expected alternatives every expected block
must be matched by a composed block of the same tool whose parameters
agree on those the expectation names (keys and citations compared after
resolution; extra blocks are not failures), every `shows` string must
appear in the rendered answer, the question's and that alternative's, and the header must leak nothing and
pass no verdict; text the model writes beside its calls or its
submission is noted, never failed, since no reader sees it; `--judge`
adds a judge model's score for the header alone. It writes `<run>.grades.jsonl` and `<run>.md` with per-class
pass rates and every failure beside the composition the model chose.
The API key comes from `ANTHROPIC_API_KEY` or a git-ignored `.env`,
never from the repository.

## Maintenance

- A question is added with its `verified` line, its blocks and its
  shows; a question whose expected answer stops matching the data is
  either updated with the data change that broke it or removed, never
  left stale. `tests/test_claims.py` enforces this: every expected block
  must build from the corpus and rest on claims, and every shows string
  must appear in the rendered expectation.
- When a source gains coverage, its uncaptured questions turn into
  answerable ones; keep the id and change the class.
- The mix (roughly 12 answerable, 9 uncaptured, 8 as-published, 17
  trajectory, 3 absent) is a floor for each class, not a quota.
