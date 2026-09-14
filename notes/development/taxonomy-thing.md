Historical visualization:

How did classification of echinoderms get started, and at what point were the five extant clades grouped under the same higher taxon?  At what point were non-echinoderms excluded from that higher taxon?

* Pre-Linnaean and transitional data modeling
* Quinarian System (William Sharp Macleay)
* Lamarck is a bit inconsistent with "family" vs "section"?
* The concept of a "section" is unclear, as are description-based partitions
* Partitions that split species within genera and group them with other genera?  Cuvier may have done this.

Key people/publications:

* Johann Heinrich Linck
  * 1733 (pre-Linnaeus, asteroids and ophiuroids, ?and comatulids?)
* Jacob Theodor Klein 
  * 1734 (pre-Linnaeus, echinoids, name "Echinodermata")
  * 1778 posthumous reprint, arguably makes "Echinodermata" available
* C. F. Schultze
  * 1760 _encrinum_ non-binomial but often cited for _encrinus_
* Johann Gerhard Reinhard Andreae
  * 1764 (encrinus, nomen nudum suppressed by ICZN)
* Carl Linnaeus (Carolus a Linné)
  * 1735 1st ed. (pre-ICZN) _echinus_ and _asterias_ (vermes/zoophyta)
  * 1758 10th ed. adds a different _holothuria_ (vermes/mollusca)
  * 12th ed. corrects (more or less) _holothuria_; divisions of _asterias_ and _echinus_
* O. F. Müller
  * 1776 _asterias_ and (separately) _holothuria_ under mollusca; _echinus_ under testacea
* Nathanael Gottfried Leske
  * 1778 Reprints and converts Klein (1734) to Latin
* * Johann Freidrich Blumenbach
  * 1779 _encrinus_ binomial but not as currently used
* Jean Guillaume Bruguière
  * 1789 Groups _echinus_ (based on Klein) and _asterias_ under "Échindermes" (french), under vermes but not mollusca; _holothuria_ remains under mollusca note that species details are not online as only volume 1 has been scanned
  * 1791 Used "Echinodermata" after Klein although its contents are relegated to plate descriptions due AFAICT to superseding work by Lamarck
* Georges Cuvier
  * 1798 Groups _holothuria_ with _echinus_ and _asteria_ under "échinodermes" within zoophyta
* Jean-Baptiste Lamarck
  * 1801 _encrinus_ under polypi/zoophytes; _sipunculus_ joins the three proper echinoderm taxa, grouped with _holothuria_ under Fistulides; _asteria_ expanded to Stellerides (_asteria_ and _ophiura_); _echinus_ expanded to Echinides (several genera)
  * 1816: _comatula_ and _euryale_ split from _asteria_ and _ophiura_, respectively, all within Stellerides, more genrea within Echinides, but Fistulides is expanded with more sea cucumbers but also priapulids and corals, the latter seeming to be due to a conflation of two usages of _actinia_

_From AnimalBase http://www.animalbase.uni-goettingen.de/zooweb/servlet/AnimalBase/home/reference?id=4 (Linnaeus 1758 source page):_

```
In his work, Linnæus referred to about 400 different older zoological works and used cryptic abbreviations. The information contained in these older works is part of many species taxa descriptions. In 2002, when we started working, there was no literature list (the basic work of zoological taxonomy was published without any list of references). We (the AnimalBase project team) have tried to detect the publications behind the Linnean abbreviations. In some cases Linnæus seemed to have consulted different editions published in different years, but with most cited works it is clear what was meant. Please go to the AnimalBase search page and click at 'References of Linnæus (1758)' for the literature list of about 200 of the most frequently cited references. We regret not to have had enough funding to digitize the other 200 references, which were only rarely cited.
For an index of books and authors see Heller 2007.

ICZN 0.279: any intermediate term placed between a generic and specific name in any work published by C. Linnæus is not to be treated as having acquired the status of a subgeneric name by reason of having been so published (ICZN 1987: 319).
````

---

Contentious names: Encrinus

* Andreae: pre-Linnaean binomial-ish but nomen nudum
* Schulze: Used "Encrinum" non-binomially but often cited 
* Blumenbach: Binomial, but groups non-crinoids and a non-Encrinus crinoid
* Lamarck: First binomial use agreeing with later usage
* Various people noted as using various citations
* 1960 ICZN plenary powers decision

What could we show here?  How to show nomen nudum?

Contentious names: Holothuria

* Linnaeus 1758 had no holothuroideans, and is considered suppressed
* Linnaeus 1767 has holothuroideans but also some (all?) past contents
* The contents of holothruia and higher taxa grouping it have been a mess

----

A successful project of this scale will need social support.  Places where people can ask how to handle unexpected scenarios, or interpret confusing sources.  Like a "tech support" ("taxon support"?) system.

----

Value Proposition:

* End-user experience
	* Browse
	* Search
	* Visualization
* Application developer experience
	* API
	* data model
	* documentation
* Technological advantages
	* Graph database for complex traversals
	* LLM integration?  LLM as app?
	* Modern front-end technologies and design
* Non-competetion
	* Duplication with other projects is welcome
	* Synchronize or reference rather than change data models
	* Encourage data contribution / harmonization by delivering value
	* Data freely available, exported for easy import	

Ideally:

* We could access every paper and understand its language and idioms
* We would know what the author(s) assumed from context
* We could determine what statements are "formal" (to varying degrees?)
* We could determine what are errors, typos, etc.

Prior art:

* Multiple projects with narrower scope
* Some integration, although as a user it feels circular more than helpful
* Contradictory and outdated opinions obscure ongoing activity
* Static visualizations, at best, with few controls
* No acknowledgement of or correlation across methodologies

Scope:

The fully-defined scope is intentionally ambitious, to show the full potential of the ideas.  However, the intent is to _choose smaller scopes to pursue_ in a way that could, over time, build up to the large scope.  _This means not losing sight of the larger scope._  Without the larger scope, many pieces of this end up looking like re-implementations of existing projects, _which would not add value._

Distinctions:

* Examine different approaches to systematics simultaneously
	* Pre-Linnaean
	* Linnaean
		* Early, still-forming Linnaean approaches
		* Fully formalized, ICZN Linnaean taxononmy
	* Post-Linnaean (e.g. rankless, or hybrid cladistics)
		* Has the ICZN codified this in any way?
	* Cladistics
	* Different nomenclatural requirements of the above
	* Need to incorporate informal usage, particularly with cladistics due to their refusal to formally name things that they still need to discuss
* Capture meaning of taxa
	* Type specimens
	* Diagnosis for each taxon, if at all possible
	* Cladogram character matrices and algorithms
* Examine changes over time
   * Awareness of and handling of incomplete data
* Superior UX considered worth the investment
   * All known existing systems suffer greatly in this area
   * Data entry, sync, and approval UX
   * Application developer UX
   * User UX with browse, search, and visualization
   * Possible to install and populate locally
	   * Choose your own policies
	   * Take the relevant data subset
* Technological advances
   * Graph database technology
   * Proper APIs (RESTish or otherwise)
   * Considering how AI (LLMs) might utilize the system

Neither competition nor dependence

* Compatible (probably not identical) data models
* The ability to import/export/synchronize data
* Data exchange subject to each project's editorial policies, independently

Trying to get different projects to truly align is rarely feasible- it's no doubt why there are so many projects already.

Different data storage and interfaces serve different purposes, at different levels of investment.

Goal is to not just allow but encourage all projects to continue as they are.  Projects might choose to consolidate, but let's not waste effort trying to make it happen.

Several of the existing databases already interconnect in _some_ way (that I generally don't find helpful, but that's me).

