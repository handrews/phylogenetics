"""The acts a claim records, shared by the extractor that emits them
(`claims.py`) and the tools that word them (`words.py`), which read only
the claim table. `docs/claims.md` is the specification.
"""

# The acts a node states by naming, under the axis of the same name, the
# record it changes: the claim field that carries that record's key, and
# the word joining the act to it in a sentence ("corrected from y").
RELATED_ACTS = {
  'corrected': ('correctedFrom', 'from'),
  'substituted': ('substitutedFor', 'for'),
  'moved': ('movedFrom', 'from'),
}
