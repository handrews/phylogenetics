Track papers with authors and probably journal (all citation info?  Would be nice), note whether a copy is available or not

Taxonomic name and taxonomic opinions, formal and informal, able to note differences from the paper's authors (sometimes it is a subset, or possibly rarely a different set that may or may not overlap).

Potentially track database associations, although they are such a dumpster fire that's rather challenging.

Need to handle duplicate names (e.g. class Rhombifera vs genus ``Rhombifera``) and confusing spelling variations (Glyptocystitida vs Glyptocystitoida, which do not seem to matter, but Eldoniid, Eldonioid, Eldoniidae, Eldonioidea may or may not matter depending on the source)

Ranks where relevant, also note re-ranked names.

Phylogenetic trees and systematic paleontology are different overlays.

Node
	* name (optional)
	* rank (optional)
	* authority (optional)
	* type (monophyletic, paraphyletic, polyphyletic, unknown)

Taxonomic nodes need a name and ideally an authority, phylogenetic nodes can be anonymous

Edge
	* type (taxonomic vs phylogenetic vs synonym vs replacement vs subtraction from paraphyletic vs addition to polyphyletic)
	* sources (list)

How to handle paraphyly and polyphyly?

Phylogenetic node is a taxonomic node or an anonymous node (e.g. node 