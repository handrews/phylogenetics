# Closed-world question answering over recorded opinions: the first run

The run of 2026-09-11 (`eval/runs/2026-09-11-claude-sonnet-5.*`): 48
questions, Sonnet 5 answering through four read-only tools over the claim
table, Opus 5 judging. This document keeps the failures and says what
each one is: a fault of the tools, of the prompt, of the model, of the
grader, or of the questions. The point of the exercise is the last four
words of `notes/development/plan.md`'s stance: no answer passes a verdict, and no
answer says more than the corpus holds.

## The setup

The corpus is 218 publications on Palaeozoic echinoderms, each recorded
as a tree of the names it prints, exactly as printed, and 48 of them
audited against the paper with a declared coverage per kind of
statement. `scripts/claims.py` turns the trees into 13,770 claims, one
per printed statement, with source, page, printed form and audit state.
Four tools read the claims and nothing else: resolve a printed name,
list the statements about a record, report a source's coverage, follow a
name across sources (`docs/claims.md`, "Reading the table"). The system
prompt (`eval/system-prompt.md`) says: answer only from what the tools
return, cite source and page, name a gap as not yet entered and never as
the paper lacking it, lead a trajectory with the measured present and
pass no verdict, speak the community's language.

The 48 questions (`eval/questions.yaml`) fall in five classes: 12
answerable, 8 as-published, 9 uncaptured, 3 absent, 16 trajectory. Each
carries the claims a right answer rests on, or the refusal it must give.

The model had at most twelve lookups per question and answered from
what it had when it reached the limit; the run records that. It made
342 tool calls (median 4 per question; 138 statement lookups, 137 name
resolutions, 49 histories, 18 coverage checks) and consumed 2.3 million
input tokens.

## The numbers

Mechanical checks (`scripts/eval_grade.py`): did the model retrieve
every claim the expected answer rests on, cite the expected sources and
page, word a refusal as the contract asks, leak nothing internal. Judge:
grounded, complete, contract, each 0–2.

| class | n | mechanical pass | grounded | complete | contract |
|---|---|---|---|---|---|
| answerable | 12 | 2 | 0.92 | 0.75 | 0.42 |
| as-published | 8 | 8 | 1.25 | 1.50 | 1.00 |
| uncaptured | 9 | 7 | 1.78 | 1.00 | 1.00 |
| absent | 3 | 3 | 2.00 | 1.67 | 1.00 |
| trajectory | 16 | 9 | 0.38 | 0.75 | 0.56 |

Two answers earned full marks from the judge (q010, q027). Nine
questions reached the lookup limit, seven of them answerable.

## What held

**The closed world held.** Every source any answer cites was returned by
a tool. A mechanical sweep of author-and-year citations against the
sources retrieved flags seven answers, and all seven cite an authority
the resolver had displayed (Whiteaves 1897 for *Astrocystites*, Richter
1930 for *octogona*, Bather 1899 for Edrioasteridae), not a paper pulled
from memory. No answer names a taxon, a specimen number or a page that
the tools had not returned. The one fabrication the run holds is about
the corpus, not the literature: q041 says Sumrall recurs "as reviewer of
the corpus's later record", which nothing returned.

**The as-published class works.** Eight of eight reproduce the printed
form the question asks for: "Bather, 1898" beside "Bather, 1899" in one
paper (q027), Bassler's "1856" (q025), "Suborder Edrioblastoidina Fay,
1962" (q021). One answer modernised a repository name, "Geological
Survey of Canada" for the printed "Canadian Geological Survey" (q026):
the normalisation of printed forms the reading rounds caught in data
entry, caught again in answering.

**Refusals are refusals.** Every uncaptured and absent question was
answered with a gap, none with a fact from outside. q037, on Whiteaves
1897, is the shape the design aimed at: the paper "is on record in the
corpus as the authority for the genus Astrocystites, but its content
has not yet been entered".

## What failed, and whose fault it is

### 1. A tool-shape gap turns answerable questions into refusals

"What new genus and type species does Guensburg & Sprinkle (1994) erect
within Astrocystitidae?" cannot be answered with the tools as built. No
tool lists what a source places under a node: the statements about
Astrocystitidae are statements about the family, and its children are
reachable only by name. The model resolved the family, read its
history, then guessed names to search for. In q005 it tried thirteen
genus names (*Antelopia*, *Nevadacystis*, *Sprinklecystis*, …), in q007
fifteen (*Anglopyrgus*, *Britanopyrgus*, *Siluropyrgus*, …), none of them
in the corpus, and reached the limit. Seven of the ten answerable
failures are this shape (q003, q004, q005, q006, q007, q009, q012).

Two things follow. The fix is a tool, not a prompt: a lookup of the
statements a source makes under a node ("the contents of Astrocystitidae
in Guensburg & Sprinkle 1994"). And the guessing is a leak of general
knowledge into the search, even though none reached an answer; a
contents lookup removes the occasion for it.

### 2. "Not found" becomes "not yet entered"

When the search failed the model applied the refusal rule to its own
failure: q004 concludes that no new genus "has been entered" for the
family, q003 that the type-species designation "has not yet been
entered for this record", q006 the same for a type species the corpus
holds. The contract distinguishes a gap in the corpus from a gap in the
literature; the run shows a third case, a gap in the search, and the
model has no way to tell it from the first. The coverage tool would
have told it: Guensburg & Sprinkle 1994 declares its new taxa fully
entered. A prompt rule ("when the declared coverage for the kind is
complete, a statement you cannot find is one you have not found, not one
that is absent") and the contents tool together close this.

### 3. The mechanism leaks

Forty-four of 48 answers lost contract points, most for speaking the
table's language: "an explicit 'moved' act, movedFrom Edrioasteroidea"
(q001), "no 'new' act attached" (q004), "the record's editorial note"
(q002), "skeleton-level, unaudited" (q009), a tool name in prose
(q034). The prompt forbids it; the tool outputs speak it, and the model
repeats what it reads. The remedy is on the tool side: render statements
in the community's words before the model sees them ("moved from
Edrioasteroidea", "the editor inferred the type species from
monotypy"), so that quoting the output is not a lapse.

### 4. A field misread

q033 answers that Edrioasteridae is credited to Bather 1899 and that "11
sources cite it under this authorship/year". The resolver had returned
the authority string and, beside it, the number of sources with any
statement about the record. The model read the count as a count of
citations of the year, and never opened a single source. One lookup,
no citation, wrong. Labels that cannot be misread ("sources with
statements about this record") are cheap.

### 5. Trajectories are told as history, not measured

The contract asks for the measured present first: how many papers hold
the latest position, over what years, from how many co-author sets;
then the history; then the dissent. The model leads with the history
(q030, q032, q043), miscounts what it has just listed ("five papers"
for six, q030), omits the dissenting order-rank papers (Smith & Jell
1990, Jell & Sprinkle 2021: q036, q043, q046) and once slides into a
verdict ("stands unopposed", q036). The history tool returns one entry
per source and leaves the counting to the model. Counting is not the
model's job: the tool can return the measurement (positions by period,
papers and co-author sets per position, the last paper for each) and
leave the model the prose.

### 6. Refusals are complete only as refusals

Every uncaptured answer scored 1 for completeness. The expected answers
say what the paper prints (the holotype number on p. 2, the plate and
figures), facts the reviews recorded and the corpus does not hold. No
closed-world answer can supply them, and none tried. The rubric is
wrong, not the answers: for a refusal, complete means the gap named
and the declared coverage stated.

## Where the grading is wrong

**The judge grades against the expected answer, not the corpus.** It
scored q041, q043 and q046 as ungrounded for citing Fell 1965, Ubaghs
1967, Sprinkle 1973 and Bell 1980, sources the model had retrieved and
that place Edrioblastoidea exactly as the answers say. The expected
answers list a subset of the corpus, and the judge treats the rest as
invention. The mechanical grounding sweep above is the honest measure;
the judge should either see the retrieved claims or stop scoring
grounding.

**The mechanical checks are literal.** q019 was failed for "paper
lacks", in the sentence "not evidence that Fay's paper lacks one". q010
was failed for not retrieving the act that names the species new,
while giving the holotype number, repository, locality and pages
exactly. A page check fired where no retrieved claim carried the page.
Each is a rule that wants a narrower trigger.

**Two questions outrun the data.** q045 expects a rejection stated by
Sumrall et al. 2013 ("we do not include them within Cyathocystidae");
the sentence sits in a review, not in the tree, and no rejection
statement exists for that source in the table. The model's answer, that
no source is recorded as rejecting the placement, was right about the
corpus and was scored 0 for it. q045 needs the tree to carry the
statement (the `rejectedPlacements` shape `docs/claims.md` reserves) or
the expectation removed. q033's expected answer likewise rests on
printed forms the model could have found but the question does not
point at.

## Against the reading rounds' catalogue

The reading rounds (`notes/reviews/`, `notes/audits/source-observations.md`)
catalogued how data entry goes wrong: OCR errors, misattribution,
placement slips, normalisation of printed forms, and gap-filling. The
answering side reproduces two of them and adds two of its own.

| failure | in data entry | in answering |
|---|---|---|
| normalisation of printed forms | "holotypes" for one holotype; a modern institution name for the printed one | q026: "Geological Survey of Canada" for "Canadian Geological Survey" |
| gap-filling | an inferred type species, flagged as the editor's (Fay 1962) | names guessed to search for (§1); "not found" recorded as "not entered" (§2) |
| misattribution | "Bell, 1974" for Bell 1975; *Cambraster*'s author | none in the answers; the as-published questions that test it passed |
| OCR errors | ligatures, umlauts, "1889" for 1879 | none: the answers repeat what the table holds, errors included, which is the design |
| mechanism leak | not applicable | §3: the table's vocabulary in the answer |
| field misread | not applicable | §4: a count read as a citation |

Gap-filling is the shared mode and the one the whole design exists to
contain. In data entry it is contained by the editorial block: an
inference is marked as the editor's and the manifest does not count it.
In answering it was contained by the closed world for the literature
(no invented papers, taxa or specimens) and not contained for the
search and for the corpus's own state. The next fixes are all on that
seam.

## What changes next, in order

1. A contents lookup: the statements a source makes under a node. Closes
   §1 and most of §2.
2. A prompt rule separating not-found from not-entered, keyed to the
   declared coverage. Closes the rest of §2.
3. Tool outputs rendered in the community's words. Addresses §3 and §4.
4. The history tool returns the measurement (counts by position, years,
   co-author sets, last paper per position). Addresses §5.
5. Grading: the mechanical grounding sweep replaces the judge's grounded
   axis, the judge sees the retrieved claims, the refusal rubric asks for
   the gap and the declared coverage, and the literal checks get narrower
   triggers.
6. Eval upkeep: q045 (enter the rejection or drop the expectation), q010
   and q019 (the checks), q033 (point at the printed forms).
7. The same run again with the fixes, Sonnet 5 first, then Opus 5 for
   comparison, both kept under `eval/runs/`.
