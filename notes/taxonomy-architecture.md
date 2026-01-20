## Principles

Science Moves.

There is no need for a database, just language.

Humans need to be able to verify the language that replaces the database.

AI and humans can populate the human-verifiable language.

AI is needed to query and visualize.

A database serialization may be better for verificaton and some use cases.

A database might be needed for the historical edit/audit trail.

* Plan for everything, even if it will not be done anytime soon if ever
	* This does not mean nail down every detail of everything
	* It does mean specifying _all_ of the big pieces and how they connect
* Capture published facts; this project offers no opinions or judgements
	* Published opinions and judgements are public facts
		* Robust to missing publications
		* Citations can fill in gaps, but need to be clearly secondhand
	* Errors are part of published facts
		* Track errors so people can see how they propagatad
		* But wherever possible based on published fact, show correct form
		* Mark corrected data clearly, especially if subjective
		* Some errors too obvious to have a published correction
		* Errors that will never have a published correction need judgements
		* Clearly capture that a judgement has been made
	* Data is messy.  Capture the mess rather than obscure it
		* Capture informality as best as possible
* No text-based semantic formatting _ever_
* Rely on "AI" to structure and respond to incredibly complex queries
	* "Visualize the history of this taxon"
	* "Visualize the history of this researcher"
	* "Compare all of these data sources to each other"

## Language Base

* Less need to handle edge cases, as LLMs can reason about sentence structure.
* Missing data is just missing.
* Error correction can be another sentence, either sourced or speculated:
  * Paper X corrects statement Y to Z
  * The data entry person thinks X is wrong, and the correct version is Z

## High Level Areas

* Biographical
	* We just need enough to keep track of who's who
	* Data model should be a very solved problem already
	* No need to re-invent at all AFAICT
* Bibliographical
	* Need details, including complexities like:
		* Different editions
		* Bound volumes that do not match cited form
		* Pre-prints
		* Re-prints that are re-packaged
		* Conference readings
		* Plates as well as pages?
	* Data model should be very solved, but...
		* In my experience, there are frequently problems
		* Data model tries to coerce too much
		* Need to understand the state of the art here
		* Strongly prefer to build on rather than re-invent
	* Handle erroneous citations?
		* e.g. incorrect page number in that one Treatise citation
		* That really complicated thing with mis-labled figures
* Geology
	* I do not have any idea how to handle this, but it's critical
	* Fundamentally built on specimens
		* Geological data captured is that needed for specimen tracking
		* This includes associating specimens with time periods
		* "types" of specimens important, but I don't fully understand them
	* Mindat has a data model but there are concerns
		* Some GCD-style text formatting, and I know those problems
		* e.g. they are trying to migrate away from abbreviations
		* I feel like Mindat is a starting rather than ending piont
	* PBDB seems like it might have a better model
		* More fossil-oriented compared to Mindat's mineral-orientation
	* Need to see if other data models exist
		* How precise can formation/member/biozone be?
		* Mindat is primarily about minerals, but fossils require more?
	* Location vs paleolocation
		* Ideally can plug in different tectonic models
		* Temporal aspect is key, not just coarse snapshots
	* Stratigraphic correlation
		* This is a huge problem on its own
		* Probably capture local info, need to stop scope somewhere
* Systematics
	* Fundamentally based on figures and diagnoses
		* These are used as a proxy for specimens
		* Re-descriptions/re-figuring can change things
		* The figure/description is more important here than the specimen
		* This supports changes based on corrected figures/descriptions
	* Each description or pre-formal discussion is its own entry
		* Past entries connected by synonymy, etc. not aliasing
		* Allows Edrioasterida Bell 1976 vs emended per G&S 1994
	* Detailed support of synonomy
	* Support for informal taxa w/cladistics
	* No attempt to track accepted/rejected, just track published facts
		* Acceptamce/rejection can be a published fact, but tracked as that
	* Rules for less-formal descriptions will be a huge challenge

## Layers

* Literal layer
* Error correction layer
* _edge of project scope_
* Application layer
	* inferences
	* judgements

## Data collection and hygiene

* Data trail
	* Who, when, and change history
* Firewall imported data
* Harmonizing competing sources
* Easy reporting of perceived errors
	* Also easy to see error resolution history
* Always document inferences
	* Taxa can differ by a single letter, making typo "correction" fraught

## Role of LLMs

Why not have LLMs read all the papers and work (query and visualize) directly from that ingested language?

Short answer: LLMs can be used to gather data, and LLMs can be used to query and visualize data, but only as two separate steps.  There needs to be a review-able data model in the middle, where humans can verify that we are adding data correctly and working from that data correctly.

For reading papers and entering data (which would also involve an OCR step that can introduce substantial errors on its own), I would trust an LLM substantially less than a qualified researcher who knows the language and time period of the paper.  I might trust an LLM slightly more than a rando from the internet who is dumping OCR text into Google Translate and hoping they get it right.  In all of those cases, we need to be able to verify the entered data, and that requires a fixed, viewable data model.


I don't trust an LLM to do so correctly any more than I trust a human to do so.  I would trust them less than a qualified researcher

The point of the data model is not purely to allow formal queries over structured data.  It is also to have an agreement on exactly what the data and its relationships mean.
