# Eval set v1

Questions over the gold slice, Edrioblastoidea (Astrocystitidae) and
Rhenopyrgidae, written before the claim table exists so that they say what
it must be able to express. `questions.yaml` holds them; `docs/claims.md`
is the vocabulary their expected answers are written in.

## The answer contract

| class | what the data holds | the right answer |
|---|---|---|
| answerable | a claim exists | the claim, cited by source and page |
| uncaptured | the paper prints it; the corpus does not hold it | "not captured for <source>", with the declared coverage value; never "not in the paper" |
| as-published | the printed form differs from the record or from later usage | the printed form verbatim, cited; a correction only if asked |
| trajectory | several sources treat the same question over time | the measured present, then the history, then the dissent; no verdict |
| absent | nothing in the corpus mentions it | "no source in the corpus mentions <x>"; no answer from general knowledge |

The contract is the closed-world rule of `docs/plan.md` made testable: an
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

Answers are written for readers of the literature, not of this
repository. They never mention files, YAML, records as storage, or how a
fact is held; they say what the corpus credits, where a source places a
name, and whether a statement is the source's or the editor's.

## The entries

```yaml
- id: q001
  class: answerable
  question: In which family does Holloway & Jell 1983 place Rhenopyrgus?
  scope: {taxon: rhenopyrgus, source: 1983_holloway_jell}
  expected:
    claims:
    - {kind: placement, source: 1983_holloway_jell, subject: rhenopyrgus, parent: rhenopyrgidae}
    answer: Rhenopyrgidae, a new family; the order is left uncertain.
  evidence: {source: 1983_holloway_jell, pages: 1002}
  verified: data/trees/1983_holloway_jell.yaml, taxonomies/0/children/0/children/0/children/0
```

`expected.claims` are selectors, field matches against the claim table's
records, because claim ids exist only once the extractor runs. A refusal
class carries `expected.refusal` (`not-captured` with `coverageKind`, or
`absent`) instead of claims. `verified` says what was checked when the
question was written: the tree path, the `audit.coverage` value, or the
review file with the printed page.

## Maintenance

- A question is added only with its `verified` line; a question whose
  expected answer stops matching the data is either updated with the data
  change that broke it or removed, never left stale.
- When a source gains coverage, its uncaptured questions turn into
  answerable ones; keep the id and change the class.
- The mix (roughly 12 answerable, 8 uncaptured, 8 as-published, 16
  trajectory, 4 absent) is a floor for each class, not a quota.
