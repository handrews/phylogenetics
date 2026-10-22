"""The ranks a record or a node may be given, and the groups of them the
loader's checks and the query side both test a rank against.

`RANKS` is the schema's `rank` enum in its order and casing (a test holds
it there); every comparison reads a rank through `fold_rank`, and
`rank_order` sorts by the enum's order. Both sides import this module,
which imports nothing of either. What the informal ranks mean, and how
`Unranked` differs from a rank the source never printed, is not decided
here (roadmap G8).
"""

# The schema's `rank` enum, in its order and casing.
RANKS = (
  'Domain',
  'Kingdom',
  'Subkingdom',
  'Superphylum',
  'Phylum',
  'Subphylum',
  'Infraphylum',
  'Superclass',
  'Class',
  'Subclass',
  'Infraclass',
  'Parvclass',
  'Superorder',
  'Order',
  'Suborder',
  'Superfamily',
  'Family',
  'Subfamily',
  'genus',
  'subgenus',
  'species',
  'subspecies',
  'variety',
  'Division',
  'section',
  'Branch',
  'Group',
  'Grade',
  'Clade',
  'Plesion',
  'Scion',
  'Unranked',
)

# The species group, whose names are combinations with a genus and whose
# types are specimens, and the genus group, whose types are species; folded.
SPECIES_GROUP = ('species', 'subspecies', 'variety')
GENUS_GROUP = ('genus', 'subgenus')

_ORDER = {rank.lower(): index for index, rank in enumerate(RANKS)}


def fold_rank(rank):
  """`rank` as comparisons read it: lower case, and empty for none."""
  return (rank or '').lower()


def rank_order(rank):
  """Where `rank` sorts: its place in `RANKS`, after all of them for a rank
  outside them or none."""
  return _ORDER.get(fold_rank(rank), len(RANKS))


def implied_rank(name):
  """The rank a record or node that gives none takes from its name: a
  species when the name is lower-case, else a genus."""
  return 'species' if name.islower() else 'genus'
