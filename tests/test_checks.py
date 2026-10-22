"""The loader and `scripts/check_draft.py` run one set of checks.
`phylohist.loader.checks` is the contract: a draft's tables are the
loader's, in the loader's order and with the same arguments, and besides
them only the checks a draft alone needs."""

from phylohist.loader import checks

# The loader pairs bracket and section markers as it builds each `Tree`;
# only an auditor sets a null.
DRAFT_ONLY = {'bracket_errors', 'section_errors', 'draft_nulls'}


def _entries(*tables):
  return [(check.__name__, names) for table in tables for check, names in table]


def test_the_draft_runs_the_loaders_checks_and_only_the_draft_only_ones_besides():
  draft_file, draft_node = _entries(checks.DRAFT_FILE_CHECKS), _entries(checks.DRAFT_NODE_CHECKS)
  assert [e for e in draft_file if e[0] not in DRAFT_ONLY] == _entries(checks.FILE_CHECKS)
  assert [e for e in draft_node if e[0] not in DRAFT_ONLY] == _entries(
    checks.MATERIAL_CHECKS, checks.NOMENCLATURE_CHECKS
  )
  loader = {
    n for n, _ in _entries(checks.FILE_CHECKS, checks.MATERIAL_CHECKS, checks.NOMENCLATURE_CHECKS)
  }
  assert {n for n, _ in draft_file + draft_node} - loader == DRAFT_ONLY
