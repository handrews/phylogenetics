"""The loader: hand-edited YAML into checked records and trees.

Everything under this package reads `data/` (and `drafts/` on request)
against `schemas/phylogeny.yaml`, builds the author, publication, source,
taxon and section records and the per-source trees into a `Corpus`, and
reports what does not hold together. Nothing above it reads YAML:
`phylohist.claims` extracts the claim table from the corpus `load`
returns, and the tools read only that table.
"""

from .corpus import Corpus
from .io import LoadError
from .load import collecting, load

__all__ = ['Corpus', 'LoadError', 'collecting', 'load']
