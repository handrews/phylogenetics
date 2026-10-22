"""The ranks a record or a node may be given, and the groups of them the
loader's checks and the query side both test a rank against.

`data/ranks.yaml` is the table: the rank words in order and as the data
writes them, the informal words flagged, the endings the loader's suffix
lint expects, and the names it lets pass. This module reads it once at
import for the constants both sides use (`RANKS`, the schema's `rank` enum
in its order and casing, held equal by a test; `SPECIES_GROUP`;
`GENUS_GROUP`); a load reads its own copy into a `RankTable`, which the lint
runs over. Every comparison reads a rank through `fold_rank`, and
`rank_order` sorts by the table's order. A record written `rank: null`
(the source prints no rank word and no cladistic term) has no rank: its
`rank` is `None`.
"""

import pathlib

import yaml

TABLE_PATH = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'ranks.yaml'


def fold_rank(rank):
  """`rank` as comparisons read it: lower case, and empty for none."""
  return (rank or '').lower()


def implied_rank(name):
  """The rank a record or node that gives none takes from its name: a
  species when the name is lower-case, else a genus."""
  return 'species' if name.islower() else 'genus'


class RankTable:
  """A `ranks.yaml` document as the code reads it: `names` in order,
  `informal` (folded), `exceptions` as `(name, rank)` pairs, the groups, and
  the suffix lint's rules."""

  def __init__(self, document):
    self.document = document
    entries = document['ranks']
    self.names = tuple(entry['name'] for entry in entries)
    self._entries = {fold_rank(entry['name']): entry for entry in entries}
    self.informal = frozenset(fold_rank(e['name']) for e in entries if e.get('informal'))
    self._checked_from = document['checkedFrom']
    self._suffixes = tuple(
      (rule['suffix'], tuple(rule['ranks']), frozenset(fold_rank(r) for r in rule['ranks']))
      for rule in document['suffixes']
    )
    self.exceptions = tuple((e['name'], e['rank']) for e in document['exceptions'])
    self._excepted = {(name, fold_rank(rank)) for name, rank in self.exceptions}

  def group(self, group):
    """The folded names of the `genus` or `species` group, in order."""
    return tuple(fold_rank(e['name']) for e in self._entries.values() if e.get('group') == group)

  def suffix_problems(self, name, rank, year):
    """What the suffix lint says of a name at a rank in a work of `year`:
    nothing for a work before `checkedFrom` or with no year, for no rank or
    one outside the table, for an informal rank or the genus and species
    groups, or for an exception; else, in both directions, the ending the
    rank expects (an ending with `before` only in a work before that year)
    and the ranks the name's ending expects."""
    if year is None or year < self._checked_from:
      return []
    folded = fold_rank(rank)
    entry = self._entries.get(folded)
    if (
      entry is None
      or entry.get('informal')
      or entry.get('group')
      or (name, folded) in self._excepted
    ):
      return []
    problems = []
    endings = [
      e['suffix'] for e in entry.get('endings', ()) if 'before' not in e or year < e['before']
    ]
    if endings and not name.endswith(tuple(endings)):
      expected = ' or '.join(f'"{suffix}"' for suffix in endings)
      problems.append(f'{name} of rank {rank} expected to end with suffix {expected}')
    for suffix, ranks, folded_ranks in self._suffixes:
      if name.endswith(suffix) and folded not in folded_ranks:
        problems.append(
          f'{name} with suffix "{suffix}" expected to have one of ranks '
          f'({", ".join(ranks)}) but has rank {rank}'
        )
    return problems


with open(TABLE_PATH) as _fd:
  TABLE = RankTable(yaml.safe_load(_fd))

# The table's rank words, in its order and casing.
RANKS = TABLE.names

# The species group, whose names are combinations with a genus and whose
# types are specimens, and the genus group, whose types are species; folded.
SPECIES_GROUP = TABLE.group('species')
GENUS_GROUP = TABLE.group('genus')

_ORDER = {rank.lower(): index for index, rank in enumerate(RANKS)}


def rank_order(rank):
  """Where `rank` sorts: its place in `RANKS`, after all of them for a rank
  outside them or none."""
  return _ORDER.get(fold_rank(rank), len(RANKS))
