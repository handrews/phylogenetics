# The five runs on one yardstick

The write-ups (`eval-writeup.md`, `eval-writeup-2.md`) grade each run
by the eval as it stood that day, so their figures do not line up. This
note re-grades runs 2 to 6 with the final grader over the final 47
questions (`scripts/eval_grade.py`, shapes and shown strings; text
beside an answer noted, not failed), and counts tokens, time and
lookups over those same questions. All runs are Claude Sonnet 5 over
the same corpus; the planner's first run, spoiled by a parameter-type
defect, is left out.

| run | date | how the model answers | questions passed | input tokens | output tokens | wall clock | lookups |
|---|---|---|---|---|---|---|---|
| 1 | 2026-09-11 | writes prose from tool results | 61 % † | 2.25 M | 112 k | 25 min | 326 |
| 2 | 2026-09-12 | picks blocks the tools return | 45 % | 1.66 M | 46 k | 10 min | 237 |
| 3 | 2026-09-14 | same, blocks rendered as answer shapes | 83 % | 1.58 M | 44 k | 12 min | 213 |
| 4 | 2026-09-14 | same, eval rewritten to shapes | 87 % | 1.62 M | 44 k | 10 min | 215 |
| 5 | 2026-09-14 | states a plan; code builds the answer | 72 % ‡ | 0.41 M | 37 k | 8 min | 105 |
| 6 | 2026-09-14 | same, after the tool and prompt fixes run 5 prompted | 77 % | 0.57 M | 48 k | 10 min | 128 |

† Run 1 has no blocks to re-grade: 28 of its 46 answers passed the
eval of its day (every statement the answer rests on retrieved, the
expected sources cited). ‡ Run 5's grades predate a tool defect and a
prompt gap fixed since; run 6 is the same configuration after those
fixes, and is the figure to quote for the planner.

## Classes of failure, by questions affected

| failure | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| answer rests on statements the model never looked up | 20 | – | – | – | – | – |
| expected source not cited | 14 | – | – | – | – | – |
| answer summarises or passes a verdict in its own words (judge score 0) | 18 | 2 | 1 | 2 | 0 | 1 |
| internal names leak into the answer | 1 | 0 | 0 | 0 | 0 | 0 |
| lookup limit reached before answering | 9 | 4 | 3 | 3 | 0 | 1 |
| wrong or missing block | – | 12 | 8 | 5 | 12 | 11 |
| expected wording missing from the rendered answer | – | 21 | 8 | 5 | 11 | 10 |
| commentary written beside the answer (reaches no reader) | – | 11 | 5 | 12 | 2 | 2 |

The first two rows end with run 2 by construction: an answer made of
blocks the tools returned cannot rest on anything unretrieved or cite
a source the corpus lacks. Verdicts and leaks end when the model's own
words shrink to a one-line header. The lookup limit all but stops
mattering when the model plans instead of reading. The wording row falls from
run 2 to run 3 because the renderer, not the model, learned to print
rank words, new-taxon marks and type species; what remains in runs 4
to 6 is the model choosing a block the question did not ask for, which
varies by a few questions from run to run.
