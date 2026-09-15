"""The read-only tools over the committed claim table, returning blocks.

Every tool reads the store (`store.py`) and returns blocks (`blocks.py`)
rendered in a style (`render.py`), or plain dicts for the resolvers and
the coverage view. Nothing writes, nothing infers, and an empty result
is the closed-world answer: the corpus holds nothing that matches. The
CLI, the MCP server, the eval runner and plans all go through `call`,
which applies the caller's style and names the tool on each block.
"""

from .store import ClaimStore as ClaimStore
from .words import COVERAGE_WORDS as COVERAGE_WORDS
from .words import short_citation as short_citation

# -- module-level surface ---------------------------------------------------

_store = None


def store():
  global _store
  if _store is None:
    _store = ClaimStore()
  return _store


def resolve_name(query, rank=None):
  return store().resolve_name(query, rank=rank)


def resolve_source(query):
  return store().resolve_source(query)


def contents(source=None, record=None, depth=None, synonymy=False, style='text'):
  return store().contents(source, record, depth=depth, synonymy=synonymy, style=style)


def placements(
  records,
  sources=None,
  years=None,
  include_variants=True,
  include_synonyms=True,
  trees=None,
  style='text',
):
  return store().placements(
    records, sources, years, include_variants, include_synonyms, trees, style
  )


def descendants(
  records, include_synonyms=True, include_variants=True, trees=None, years=None, style='text'
):
  return store().descendants(records, include_synonyms, include_variants, trees, years, style)


def ancestors(records, include_variants=True, trees=None, years=None, style='text'):
  return store().ancestors(records, include_variants, trees, years, style)


def placed_under(record, parent, include_variants=True, trees=None, years=None, style='text'):
  return store().placed_under(record, parent, include_variants, trees, years, style)


def history(record, include_related=True, synonymy=False, trees=None, years=None, style='text'):
  return store().history(record, include_related, synonymy, trees, years, style)


def synonymy(record, source=None, style='text'):
  return store().synonymy(record, source, style)


def statements(record, source=None, kind=None, act_kind=None, style='text'):
  return store().statements(record, source, kind, act_kind, style)


def source_coverage(source):
  return store().source_coverage(source)


def gap(source=None, kind=None, name=None, style='text'):
  return store().gap(source, kind, name, style)


def printed_forms(record, source=None, style='text'):
  return store().printed_forms(record, source, style)


TOOL_DESCRIPTIONS = {
  'resolve_name': (
    'Find the records a printed name can refer to. Folds ligatures, '
    'diacritics, capitals, hyphens and spaces, so "Palæaster", '
    '"Echino-encrinites" and "Edrioaster Bigsbyi" all resolve. A two-word '
    'query is a species. Each candidate gives the record key to use with '
    'the other tools, the rank, whether the record is a spelling or rank '
    'variant of another (and of which, under "variants": the same name at '
    'other ranks, which together make one group), the authority as cited, '
    'and how many sources make statements about it '
    '("sourcesWithStatements", not a count of citations of anything). '
    'Unnamed records (a bin such as "order uncertain", a taxon in open '
    'nomenclature such as "Rhenopyrgus sp. indet. 1") are never found by '
    'name, since the words in their designation name other taxa; reach '
    'them by the key a listing shows. Record and source keys are '
    'lowercase; the other tools accept them in any case, or a printed '
    'name that resolves to one record (a name that can mean several is '
    'refused with the candidates). A combination is written as the '
    'literature writes it: "Rhenopyrgus grayae", "Pyrgocystis '
    '(Rhenopyrgus) coronaeformis", "Pyrgocystis (Rhenopyrgus)". An empty list '
    'means no source in the corpus carries the name; it does not mean the '
    'name does not exist. Optionally restrict by rank word.'
  ),
  'resolve_source': (
    'The sources a citation can mean: "Dehm 1961", "Holloway & Jell '
    '1983", "Sumrall et al. 2013", "Fay 1967a". Each candidate gives the '
    'key, the citation as the blocks print it, the year, the authors and '
    "whether the paper's content is entered. Every tool that takes a "
    'source accepts the citation itself, so this is needed only when a '
    'citation can mean several papers (the tool then refuses with their '
    'keys) or to check whether a paper is in the corpus at all: an empty '
    'list means no source in the corpus is that paper.'
  ),
  'contents': (
    'What one source places under a record, as the source prints it: a '
    'classification block laid out as a Systematic Paleontology section '
    '(rank words on the headings, the type species under its genus, new '
    'names marked as the source prints them or by rank: fam. nov., gen. '
    'nov., sp. nov.; provisional or questionable names ?), optionally '
    "with each name's synonymy. Use it to see the genera a source puts in a family, the "
    'species in a genus, or a whole scheme. With no source, one block per '
    "source that places the record. When a source's declared coverage of "
    'new taxa is complete, everything it names sits in this block; look '
    'here before concluding that something has not been entered.'
  ),
  'placements': (
    'Where each source places each record: a matrix with the records as '
    'rows (the same name at other ranks folded in) and their rank, the '
    'sources as columns in publication order, and the parent each gives '
    'in the cell (a rejected placement marked "; not X"). The '
    'header measures the schemes: each distinct placement with its papers, '
    'years, co-author sets and last paper. Pass several records to see a '
    'group at once (for example the descendants of a family). Synonyms '
    'accepted as these records are included as rows unless told not to.'
  ),
  'descendants': (
    'Everything any source has ever placed under the given records, '
    'transitively within each source, including names accepted as their '
    'synonyms and the same names at other ranks: a table of records with '
    'rank, which sources place them and under what, and a count. This is '
    'how "what belongs to the edrioblastoids" is answered; feed its '
    'records to placements or ancestors.'
  ),
  'ancestors': (
    'The chain of taxa above the given records in every source that '
    'places them: one line per source in year order, top down, with a '
    'placeholder such as "Order uncertain" in the source\'s words and an '
    'alternative placement the source offers beside the taxon it applies '
    'to. The heading counts the papers, co-author sets and years.'
  ),
  'placed_under': (
    'The sources that place a record under a higher taxon, directly or '
    'through intermediate taxa: one line per source in year order with '
    'the taxa between, the first and last source stated in the heading. '
    'Answers "who placed X under Y", "who first", "who followed".'
  ),
  'history': (
    'What each source does with a name, one line per source in year '
    'order: the name as that source uses it (a species as its '
    'combination there), its position above what the combination says, '
    'the acts (named as new, emended, nomen translatum, moved, a rejected '
    'placement), the page; the heading measures the papers, co-author '
    'sets and years, the ranks used and the positions given (which is the '
    "trajectory's present and history). The same name at other ranks is "
    'included unless include_related is false. With synonymy true each '
    "source's synonymy entries follow its line."
  ),
  'synonymy': (
    'The synonymy a source prints under a record, as a dated list: each '
    'earlier usage accepted or rejected, with the original combination, '
    'the cited work and page, and the printed form. Every source with one '
    'when no source is named.'
  ),
  'statements': (
    'Every statement the corpus holds about one record, in publication '
    'order, each as a sentence with its source, year and page: the name '
    'cited, the placement given, an act (named as new, emended, moved, '
    'type species), a synonymy acceptance, a rejection, material, a '
    'diagnosis. Optionally one source, one kind of statement '
    '(usage, placement, acceptance, act, rejection, material, diagnosis, '
    'editorial; or occurrences, illustrations, specimens for one kind of '
    'material) or one act kind (new, type, emended, nomTransl, moved, '
    'removed, corrected). A statement marked "editor" is the '
    "editor's inference, not the paper's words. When a source is named "
    'and nothing of that kind about the record is entered, the result is '
    'the gap block for that source and kind: compose it as the answer.'
  ),
  'source_coverage': (
    'What the corpus holds of one publication: its citation, whether its '
    'content has been entered at all, the audit state and, per kind of '
    'statement, whether the reviewer declared all, part or none of what '
    'the paper prints to be entered, and the counts derived. Consult it '
    'before saying anything has not been entered: when the declared '
    'coverage for a kind is complete, a statement you have not found is '
    'one you have not looked for in the right place.'
  ),
  'gap': (
    'The sentence to give when the corpus does not hold what was asked: '
    'for a source and a kind of statement (skeleton, newTaxa, types, '
    'synonymy, material, occurrences, illustrations, diagnoses, '
    'phylogeny), whether the source is entered and what its declared '
    'coverage says, worded as work not yet done, never as the paper '
    'lacking it; or, with a name, that no source in the corpus carries '
    'that name (use it when the resolver finds nothing). Use this block, '
    'not your own words, for a gap or an absence.'
  ),
  'printed_forms': (
    'Each form a source prints for a record, verbatim, with the page: '
    'how a name, author or year appears on the page, for questions about '
    'what a paper actually prints. Never corrected.'
  ),
}

_COMBINATION_NOTE = (
  ' Species-group names are shown as the combination the source uses '
  '(genus, subgenus in parentheses, epithet); a species recombined into '
  'another genus appears once per combination, since each is a name of its own.'
)
for _name in ('contents', 'placements', 'descendants', 'history', 'statements', 'synonymy'):
  TOOL_DESCRIPTIONS[_name] += _COMBINATION_NOTE

_RECORDS = {
  'type': 'array',
  'items': {'type': 'string'},
  'description': 'record keys from resolve_name',
}
_SOURCE = {
  'type': ['string', 'null'],
  'description': (
    'a source key or the citation as the blocks print it ("Dehm 1961", "Sumrall et al. 2013")'
  ),
}
_YEARS = {
  'type': 'array',
  'items': {'type': ['integer', 'null']},
  'minItems': 2,
  'maxItems': 2,
  'description': '[first, last] publication years, either may be null',
}
_TREES = {
  'type': 'array',
  'items': {'type': 'string', 'enum': ['taxonomy', 'cladogram', 'diagram', 'other']},
  'description': 'tree kinds to read placements from; default taxonomy only',
}


def _spec(name, properties, required):
  return {
    'name': name,
    'description': TOOL_DESCRIPTIONS[name],
    'input_schema': {'type': 'object', 'properties': properties, 'required': required},
  }


TOOL_SPECS = [
  _spec(
    'resolve_name',
    {
      'query': {'type': 'string', 'description': 'the printed name'},
      'rank': {'type': 'string', 'description': 'optional rank word'},
    },
    ['query'],
  ),
  _spec(
    'resolve_source',
    {
      'query': {'type': 'string', 'description': 'a citation or a key'},
    },
    ['query'],
  ),
  _spec(
    'contents',
    {
      'source': {
        'type': ['string', 'null'],
        'description': (
          'a source key or citation ("Dehm 1961"); omit for every source that places the record'
        ),
      },
      'record': {'type': 'string', 'description': 'a record key'},
      'depth': {
        'type': ['integer', 'null'],
        'description': 'levels below the record; omit for all',
      },
      'synonymy': {'type': 'boolean', 'description': "include each name's synonymy"},
    },
    ['record'],
  ),
  _spec(
    'placements',
    {
      'records': _RECORDS,
      'sources': {
        'type': 'array',
        'items': {'type': 'string'},
        'description': 'restrict to these sources, keys or citations',
      },
      'years': _YEARS,
      'include_variants': {'type': 'boolean'},
      'include_synonyms': {'type': 'boolean'},
      'trees': _TREES,
    },
    ['records'],
  ),
  _spec(
    'descendants',
    {
      'records': _RECORDS,
      'include_synonyms': {'type': 'boolean'},
      'include_variants': {'type': 'boolean'},
      'trees': _TREES,
      'years': _YEARS,
    },
    ['records'],
  ),
  _spec(
    'ancestors',
    {
      'records': _RECORDS,
      'include_variants': {'type': 'boolean'},
      'trees': _TREES,
      'years': _YEARS,
    },
    ['records'],
  ),
  _spec(
    'placed_under',
    {
      'record': {'type': 'string', 'description': 'the record key or printed name'},
      'parent': {'type': 'string', 'description': 'the higher taxon, key or printed name'},
      'include_variants': {'type': 'boolean'},
      'trees': _TREES,
      'years': _YEARS,
    },
    ['record', 'parent'],
  ),
  _spec(
    'history',
    {
      'record': {'type': 'string', 'description': 'the record key or printed name'},
      'include_related': {'type': 'boolean'},
      'synonymy': {'type': 'boolean'},
      'trees': _TREES,
      'years': _YEARS,
    },
    ['record'],
  ),
  _spec(
    'synonymy',
    {
      'record': {'type': 'string'},
      'source': _SOURCE,
    },
    ['record'],
  ),
  _spec(
    'statements',
    {
      'record': {'type': 'string'},
      'source': _SOURCE,
      'kind': {'type': ['string', 'null']},
      'act_kind': {'type': ['string', 'null']},
    },
    ['record'],
  ),
  _spec(
    'source_coverage',
    {
      'source': {'type': 'string', 'description': 'a source key or citation'},
    },
    ['source'],
  ),
  _spec(
    'gap',
    {
      'source': {
        'type': 'string',
        'description': 'a source key or the citation as the blocks print it',
      },
      'kind': {'type': 'string', 'enum': list(COVERAGE_WORDS)},
      'name': {
        'type': 'string',
        'description': 'a name no source carries, instead of source and kind',
      },
    },
    [],
  ),
  _spec(
    'printed_forms',
    {
      'record': {'type': 'string'},
      'source': _SOURCE,
    },
    ['record'],
  ),
]


# The parameters that name records and sources, wherever a tool takes them;
# a value given as a printed name or a citation resolves to a key.
RECORD_PARAMETERS = frozenset({'record', 'records', 'parent'})
SOURCE_PARAMETERS = frozenset({'source', 'sources'})

# The tools that answer a lookup rather than a reader: no block, no style.
LOOKUPS = frozenset({'resolve_name', 'resolve_source', 'source_coverage'})

TOOLS = {
  'resolve_name': resolve_name,
  'resolve_source': resolve_source,
  'contents': contents,
  'placements': placements,
  'descendants': descendants,
  'ancestors': ancestors,
  'placed_under': placed_under,
  'history': history,
  'synonymy': synonymy,
  'statements': statements,
  'source_coverage': source_coverage,
  'gap': gap,
  'printed_forms': printed_forms,
}


def call(name, arguments, style='text'):
  """Dispatch a tool call by name with the parameters its spec lists; what
  the CLI, the MCP server, the runner and plans all go through. The style
  is the caller's, applied to the blocks on the way out; a lookup has
  none."""
  arguments = dict(arguments)
  if 'years' in arguments and arguments['years'] is not None:
    arguments['years'] = tuple(arguments['years'])
  if name not in LOOKUPS:
    arguments['style'] = style
  result = TOOLS[name](**arguments)
  for block in result if isinstance(result, list) else [result]:
    if isinstance(block, dict) and 'blockId' in block:
      block['tool'] = name
  return result
