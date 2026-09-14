Fundamental units:
  * pgNode (phylogenetic node)
  * published location (source, pages, plates, figures)
  * specimen
  * specimen locality
  * geoNode

Specimens are the real, physical items being described.  To truly understand taxonomic changes over time, you need to know which specimens are associated with each pgNode. Two pgNodes with the same specimen set are either identical or true synonyms.  Absent that, two pgNodes with the same type specimen are equivalent in some sense, but may or may not be identical depending on information that is likely unavailable (most papers do not enumerate every single specimen, if such a thing were even possible for taxa with thousands of specimens).

Published locations are where specimens are assigned to pgNodes, and pgNodes are related to each other.  Without a level of detail down to the exact mentioned specimens and any photos or illustrations, it is impossible to evaluate future references and detect errors such as mis-labeled figures or incorrect page numbers.

pgNodes are the scientific opinions or hypotheses expressed about specimens.  They provide various possible structures and relationships, and may be based on diagnoses or coded data that can be associated with the node.  This is the paleontological work to be captured in order to make sense of the results of the geologic expeditions and specimen preparation work.

specimen localities provide the temporal dimension to the paleontological work.  Many trees or diagrams show fossil occurrences, and it is also desirable to know the temporal location of each specimen, and therefore the temporal range of a pgNode.

geoNodes allow correlating temporal information across localities, which are given in terms of the local geology.  Correlation of local geological elements with the overall scale is also a matter of scientific opinion, and changes over time.  Both paleontological papers and geological papers publish opinions on this.


Structured data vs prose and unclear wording:
=============================================

While all pgNode and geoNode data _could_ be expressed in a structured way, often at least some data is expressed in prose.  Sometimes that's because it's obvious to human readers (e.g. these taxa are all part of Phylum Echinodermata (by whichever authority)).  Sometimes it is simply too speculative to fit the structure, but still worth capturing.  And other times, particularly in the 1700s and 1800s, the formal structures were not yet codified or used consistently.

Sometimes even intended-to-be-structured data is too complex for formal conventions, and data entry will require some human interpretation; this is also considered a node "form prose", or perhaps "with interpretation" is a better way to think about it.

We need to be able to capture and mark such nodes.  It needs to be possible to either ignore or use them in queries, as they provide more data but introduce uncertainty as some human interpretation of the prose or ambiguous structure is inevitable.

Errors:
=======
All information contains errors.

Ideally, we capture things as written, no matter how "obvious" the error, and allow corrections to appear through additional nodes.  However, some are too trivial to be formally called out (e.g. we probably just know that "Cigaria" is really "Cigara" unless someone captured Sprinkle's misspelling in a later paper.  But Cigara is rarely mentioned s, probably not.  Others are worth highlighting whether we can find a published correction or not, even if we are uncertain (analogous to the uncertainty of "with interpretation" nodes).

Need to understand how much we want queries to default to using corrected data, knowing that the corrections themselves can be wrong.

Example: 2021-00-00-p Evolution, Functional Morphology and Paedomorphism in the Gogiid-Ascocystitid Lineage (Eocrinoidea; Cambrian-Ordovician).pdf uses "Cambrocystidae (Dzik and Orłowski, 1993)" in the systematic paleontology, but "Cambrocystitidae" in a caption.  And the actual paper cited defines the taxon as "Cambrocrinidae", after the genus "Cambrocrinus" (which is referenced and spelled correctly in the 2021 paper).

Audit trail:
============
We need to keep track of which accounts (or import tools) added data, and also allow for review / affirmation / questioning of data.
Option matrix:
==============
* most recent correction (yes; could be multiple levels; no means use all)
* imprecise data (yes; could be multiple levels; no)

Supporting info:
================

Everything else is a convenience to more precisely capture identity, e.g. ensuring all locationos point to the same article, journal/book, volume, issue, etc. nodes, all specimens point to the same repositories, and specimen localities point to the same geological elements.

pgNodes:
--------


specimens:
----------
* identifier (property)
* repository (node)
* locality (node?)
  * repository locality w/identifier
  * informal locality w/description
* type
* info on fossils per slab?
* info on cast vs... ?


* pgNode # phylogenetic node

