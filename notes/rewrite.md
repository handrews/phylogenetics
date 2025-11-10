# Phylogenetic Browser

* Capture everythign as-is
  * Things that could connect sometimes won't — need to handle this gracefully
  * Adding sources whenever possible is preferred, but need to handle otherwise
  * Errors will be present that can't be verified (Sphaeronites page number error)
  * Errors will be corrected in later publications and need to be handled
  * Imprecise prose may be the only available data source
  * _We have to handle each paper as if it is the only thing in existence_
  * Connection is a conceptual layer on top of data capture, _not_ an integral part of it
  * May need to support some duct-taping to bridge gaps (2nd-/3rd-hand knowledge)
  * Duct-taping should be obvious, and should be (automatically?) removed when possible

* Three-layred system
  * Data capture
  * Data-driven connection
  * Human-driven connection, analysis, and visualization

* Business model?
  * Data entry, connection, and visualization of those two layers is free
  * Sell ads on visualization site?
  * Sell API access to build apps?

* Identity is hard
  * For sources, a hash of normalized info?  Plus citation-specific info?
    * Alternatively, always work to build out the source graph
    * Should be easy to add journals, volumes, issues, books, publishers?
  * For taxa... it will have to be a traversal query, I think.

* Capture all taxonomic / phylogenetic data
  * Systematic Paleontology (Linnaean taxonomy)
  * Cladograms, including brackets, including nesting or overlapping
  * Informal trees (a.k.a. best guess of high-level taxonomy)

* Defining a source
  * Standard bibliographical citation
  * Specific page / plate numbers for taxon definition / use where possible
  * Re-consideration over time
    * Echinodermata (Klein 1734, Klein 1778, Bruguiére 1791, the "ex" option)
    * These would be synonymized
    * Need a way to mark the "winning" taxon
    * See also ICZN decisions contra to "first wins"
    * See also the chaos of supra-familial rank names

* Defining a taxon
  * Implicit vs explicit
    * If all sources and trees were fully captured, no need for taxon nodes.
    * Taxon nodes collect info for which we do not have full tree info.
  * Identity
    * Name group (encompassing orthographic and rank-based variations)
    * Authority (publication, authors if different, page(s)/plate(s))
    * Emendations
      * How formal does the emendation need to be?
      * Same but not same
      * Need to express using with or without a specific emendation
  * Appearances
    * Original definition (actual new and re-stated new, apparently a thing)
    * Emendation
    * Correction
    * Translation
    * Synonymy (and not-synonomy)
    * Erroneous labeling
    * Restatement without modification
    * Quotes and question marks
  * Open nomenclature
    * How much context?
    * Identity?
    * Text descriptions ("closely allied to") vs formal latin (cf., aff., etc.)
  * Name
    * Variations in spelling
      * Latin gender agreement
      * General confusion (Cystidea / Cystoidea / etc.)
      * Variations in endings or roots
        * Capture endings and roots?
        * Bather's tendency to drop a "ti"
        * Lichenoididae vs Lichenoidae
        * Lepidocystidae vs Lepidocystoidae
        * Protocrnoida vs Protocrinoidea
      * Older conventions:
        * Capitalization of species (Angelin)
        * Use of hyphens (Echino-encrinus)
        * Use of non-US-ASCII characters (æ, ü, etc.) (Cystideæ)
        * Incorrect forms (Diploporiten)
    * Do we group name variations?  Cystidea/Cystoidea/etc.
    * Re-ranked names
      * Edrioblastoidea, Edrioblastida, Edrioblastina
      * Rhombifera (Class), Rhombifera (Order)
    * Homonyms at different ranks
      * Gogiida (Subclass), Gogiida (Order)
      * Rhombifera (Class or Order), Rhombifera (genus)
      * Mixture of homonyms and ranks, taxa and adjectives
        * Eldoniidae, Eldonioidea, eldoniid, eldonioid
        * Glyptocystitida, Glyptocystoida, glyptocystitid, glyptocystitoid
    * Informal groups (Cambroernids vs Cambroernida)
    * What about name variations that are also homonyms?
    * Suffix enforcement?  Note exceptions?
      * How to handle sporadic patterns in upper taxa conventions

  * Ranks
    * Tracking different ranks for the same name
    * Tracking "nom. trans." adjusted name per rank
    * How do Plesion and Grade fit in?
    * How do "informal groups" fit in?

* Defining a tree
  * Trees should be in the same relative order as in text
  * Different types
    * Formal linnaean taxonomy
      * Possibly with diagnostic criteria
    * Cladogram
      * Possibly with character scores
      * Possibly with statistical info
      * Brackets / labels / color coding
    * Schematic
      * Diagram inferred from more detailed sources
      * Often shows hypothesis of higher taxa relationships
  * Relationships
    * Standard node and branch
    * Evolutionary series (node and branch gets verbose; Plesions?)
    * Vague relationships between nodes (schematics)
  * Implicit data
    * Sometimes the text adds information that seems to fit in the tree
      * This could be formal enough to be certain
      * Or it could be a vague association that may or may not be correct
    * Sometimes the text outlines a tree without clearly saying so
    * Sometimes the larger context of the tree is implied to varying degrees

All relationships come from trees of some sort (although they might be as simple as a "tree" synonomizing a single taxon with another, or correcting a single taxon name, e.g. Regnéll definitively settling on Cystoidea over Cystidea).

When we don't have the appropriate tree, we can add _synthetic relationships_ based on text, secondhand reports, and other plausible assumptions **that can be documented**.

A taxon node is where we can hang info that is immutable (a taxon's initial source publication and page definition).
