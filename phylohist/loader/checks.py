"""Which integrity checks run over a raw tree file, and on what.

The loader (`load.py`) and `scripts/check_draft.py` run the checks of
`material.py` and `nomenclature.py` from these tables, so a check added to a
table reaches both; what each check reports is in its own docstring. An
entry is a check and the names of its arguments in a scope: `file_scope`
describes a tree file, and `node_messages` adds each node, whether it is a
cited entry, and its own `contexts` and `material`. The loader runs
`FILE_CHECKS` and `MATERIAL_CHECKS` in one pass and `NOMENCLATURE_CHECKS` in
a second; a draft runs the `DRAFT_` tables, which add the checks only a
draft needs: the pairing of bracket and section markers, which the loader
does as it builds each `Tree`, and the nulls only an auditor sets. The
checks across files (`material.registry_links`, `material.same_as_links`,
`nomenclature.compared_link_conflicts`) take more than one file, and each
caller makes them itself.
"""

from . import material, nomenclature

FILE_CHECKS = (
  (material.unreferenced_file_contexts, ('document',)),
  (material.unused_fields, ('document',)),
  (material.file_prefixes, ('document', 'repositories')),
  (
    material.locality_objects,
    ('file_contexts', 'file_prefixes', 'locality_register', 'repositories'),
  ),
  (material.context_tentatives, ('file_contexts', 'file_level')),
)
MATERIAL_CHECKS = (
  (material.context_refs, ('node', 'node_contexts', 'file_contexts')),
  (material.figure_refs, ('node', 'is_cited')),
  (material.number_entries, ('node', 'file_prefixes', 'repositories')),
  (
    material.locality_objects,
    ('node_contexts', 'file_prefixes', 'locality_register', 'repositories', 'node_material'),
  ),
  (material.context_tentatives, ('node_contexts',)),
  (material.range_tentatives, ('node',)),
  (material.cast_refs, ('node',)),
  (material.null_material, ('node', 'is_cited')),
)
NOMENCLATURE_CHECKS = (
  (nomenclature.compared_links, ('node', 'taxa')),
  (nomenclature.quoted_parent, ('node', 'taxa')),
  (nomenclature.mineral_fields, ('node', 'taxa')),
  (nomenclature.role_uncertain, ('node',)),
  (nomenclature.type_node, ('node', 'is_cited')),
  (nomenclature.children_null, ('node', 'is_cited')),
  (nomenclature.inferred_pages, ('node',)),
)
DRAFT_FILE_CHECKS = (
  (material.bracket_errors, ('document',)),
  (material.section_errors, ('document',)),
  *FILE_CHECKS,
)
DRAFT_NODE_CHECKS = (
  *MATERIAL_CHECKS,
  (material.draft_nulls, ('node', 'is_cited')),
  *NOMENCLATURE_CHECKS,
)


def file_scope(document, repositories, taxa=None):
  """The names the tables' arguments are read from, for the raw tree file
  `document`; `taxa` (`Taxon.get`, or `nomenclature.record_lookup`) is read
  only by `NOMENCLATURE_CHECKS`."""
  return {
    'document': document,
    'repositories': repositories,
    'taxa': taxa,
    'file_contexts': document.get('contexts') or {},
    'file_prefixes': document.get('prefixes') or {},
    'locality_register': document.get('localityRegister'),
    'file_level': True,
  }


def file_messages(scope, table):
  """`(level, message)` for each check of `table` over the file, in table
  order."""
  for check, names in table:
    yield from check(*(scope[name] for name in names))


def node_messages(scope, table):
  """`(path, level, message)` for each check of `table` over every node of
  the file, node by node in `material.walk_document` order and in table
  order on each node; the message has no prefix."""
  for path, node, is_cited in material.walk_document(scope['document']):
    node_scope = {
      **scope,
      'file_level': False,
      'node': node,
      'is_cited': is_cited,
      'node_contexts': node.get('contexts') or {},
      'node_material': node.get('material') or (),
    }
    for check, names in table:
      for level, message in check(*(node_scope[name] for name in names)):
        yield path, level, message
