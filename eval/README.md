# Eval set v1

Questions over the gold slice, Edrioblastoidea (Astrocystitidae) and
Rhenopyrgidae, written before the claim table exists so that they say what
it must be able to express. `questions.yaml` holds them; `docs/claims.md`
is the vocabulary their expected answers are written in.

## The answer contract

| class | what the data holds | the right answer |
|---|---|---|
| answerable | a claim exists | the claim, cited by source and page |
| uncaptured | the paper prints it; the tree does not hold it | "not captured for <source>", with the declared coverage value; never "not in the paper" |
| as-published | the printed form differs from the record or from later usage | the printed form verbatim, cited; a correction only if asked |
| conflict | two sources, or record and print, disagree | every value with its source; no adjudication |
| absent | nothing in the corpus mentions it | "no source in the data mentions <x>"; no answer from general knowledge |

The contract is the closed-world rule of `docs/plan.md` made testable: an
answer is right only when every fact in it is a claim, cited, and every
gap is named as a gap of the data rather than of the literature.

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
- The mix (roughly 12 answerable, 8 uncaptured, 8 as-published, 8
  conflict, 4 absent) is a floor for each class, not a quota.
