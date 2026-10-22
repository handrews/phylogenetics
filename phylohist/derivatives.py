"""The ways one taxon record derives from another.

A record in `data/taxa.yaml` may carry one of the fields below, naming the
record it is a variant of: another spelling, a gender form, the Latin or a
vernacular form of a name, or the same name at another rank. The loader
builds the variant from its target by the row's flags, the names index
writes the field name as the row's `kind`, and the query side reads that
kind back here for the candidate order and the wording. Both sides import
this module, which imports nothing of either.

Every kind takes its target's authority unless the record gives its own
`auth` or `authority`. `homonym`, `originalParent` and `needsQualification`
are never borrowed: they tell identically spelled records apart, so each
spelling carries its own.
"""

import collections

# field: the record field naming the target.
# relation: the words of the loader's message for a target it cannot find
#   ("Taxon x alt spelling of unknown y").
# borrows_name: takes the target's name unless the record gives one.
# borrows_rank: takes the target's rank and mineral flag.
# lang: which record must carry `lang`: 'record' for a vernacular form,
#   'target' for the Latin spelling of one, None otherwise.
# words: how the variant relates to its target ("<words> <target>").
# reverse: how the target relates to the variant, read from the other end.
# order: the resolver's candidate order (a primary record is 0, a
#   placeholder last).
Kind = collections.namedtuple(
  'Kind', 'field relation borrows_name borrows_rank lang words reverse order'
)

# In precedence order, should a record ever carry two of the fields.
KINDS = (
  Kind(
    field='altSpellingOf',
    relation='alt spelling',
    borrows_name=False,
    borrows_rank=True,
    lang=None,
    words='spelling variant of',
    reverse='spelling variant of',
    order=2,
  ),
  Kind(
    field='altGenderOf',
    relation='gender variant',
    borrows_name=False,
    borrows_rank=True,
    lang=None,
    words='gender variant of',
    reverse='gender variant of',
    order=2,
  ),
  Kind(
    field='latinSpellingOf',
    relation='Latin spelling',
    borrows_name=False,
    borrows_rank=True,
    lang='target',
    words='Latin form of',
    reverse='vernacular form of',
    order=2,
  ),
  Kind(
    field='vulgarSpellingOf',
    relation='vulgar spelling',
    borrows_name=False,
    borrows_rank=True,
    lang='record',
    words='vernacular form of',
    reverse='Latin form of',
    order=3,
  ),
  Kind(
    field='altRankOf',
    relation='alt rank',
    borrows_name=True,
    borrows_rank=False,
    lang=None,
    words='same name at another rank as',
    reverse='same name at another rank as',
    order=1,
  ),
)
BY_FIELD = {kind.field: kind for kind in KINDS}
FIELDS = tuple(BY_FIELD)


def kind_of(record):
  """The `Kind` a raw record derives by, the first of `KINDS` whose field it
  carries; `None` for a record that derives from nothing."""
  return next((kind for kind in KINDS if kind.field in record), None)
