"""The acts a claim records, shared by the extractor that emits them
(`claims.py`) and the tools that word and offer them (`words.py`,
`tools.py`), which read only the claim table. `docs/claims.md` is the
specification.
"""

# The acts a node states by naming, under the axis of the same name, the
# record it relates the name to: the claim field that carries that
# record's key, and the words before its name in a sentence ("corrected
# from y").
RELATED_ACTS = {
  'corrected': ('correctedFrom', 'corrected from'),
  'substituted': ('substitutedFor', 'substituted for'),
  'lapsus': ('lapsusAs', 'printed by lapsus calami as'),
  'moved': ('movedFrom', 'moved from'),
}

# Every `actKind`, in the order a node emits its acts.
ACT_KINDS = (
  'new',
  'placeholder',
  'type',
  'emended',
  'nomTransl',
  'nomNudum',
  *RELATED_ACTS,
  'removed',
)

# The acts that make the record they name a synonym of the node's name
# without the source printing a synonymy: an incorrect form and a replaced
# name. A `synonyms` entry repeats it only when a synonymy is printed.
SYNONYMY_ACTS = ('corrected', 'substituted')
