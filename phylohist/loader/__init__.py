"""The loader: hand-edited YAML into checked records and trees.

Everything under this package reads `data/` (and `drafts/` on request)
against `schemas/phylogeny.yaml`, builds the author, publication, source
and taxon records and the per-source trees, and reports what does not
hold together. Nothing above it reads YAML: `phylohist.claims` extracts
the claim table from what `load` returns, and the tools read only that
table.
"""

from .io import LoadError
from .load import counting_errors, load

__all__ = ['LoadError', 'counting_errors', 'load']
