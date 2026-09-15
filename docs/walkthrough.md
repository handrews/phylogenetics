# Five questions, answered by plans

Each question below is from the eval set, with the plan Claude Sonnet 5
stated for it in the planner run of 2026-09-14 and the answer that plan
renders today. In planner mode the model sees no block: it resolves the
names and papers the question mentions, states which blocks the answer
is made of and with what parameters, and code builds and renders them.
The one-line header at the top of each answer is the only text of the
model's own; everything under it is the corpus.

The plans are files under `docs/walkthrough/`, so any of them runs
without a model:

    poetry run phylohist plan docs/walkthrough/01-listing.yaml

`tests/test_walkthrough.py` renders every plan and checks that the
answers pasted here are what the code prints, so this page cannot go
stale. The eval's own account of the run, and of the six that came
before it, is under `eval/findings/`.

## What new genus and type species do Sprinkle & Sumrall (2015) place in family Astrocystitidae?

The plan (`docs/walkthrough/01-listing.yaml`):

    blocks:
    - tool: contents
      parameters:
        source: Sprinkle & Sumrall 2015
        record: Astrocystitidae

The answer:

    New genus and type species placed under family Astrocystitidae by Sprinkle & Sumrall (2015), as that source's contents show, with new names marked

    Sprinkle & Sumrall 2015
      Family Astrocystitidae
        Genus Porosublastus gen. nov.
          Type species. Porosublastus inexpectus
          Porosublastus inexpectus sp. nov.

A point question about one paper is answered by that paper's listing, laid out as a Systematic Paleontology section prints it: the rank words, the new-taxon marks and the type species are the source's own statements. One block; the model chose `contents` for the family in that source and nothing else.

## Who proposed placing rhenopyrgids inside Cyathocystidae, who followed, and who rejected it?

The plan (`docs/walkthrough/02-placement.yaml`):

    blocks:
    - tool: placed_under
      parameters:
        record: rhenopyrgidae
        parent: cyathocystidae
    - tool: history
      parameters:
        record: rhenopyrgidae
        include_related: false

The answer:

    Placement of Rhenopyrgidae (family, including its subfamily rank variant Rhenopyrginae) within Cyathocystidae: proposer, followers and rejecters shown via the placement record and the full placement history; classification trees; all years

    Rhenopyrgidae Holloway & Jell 1983 under Cyathocystidae Bather 1899: 2 papers, 2 co-author sets, 1994–2000
    first Guensburg & Sprinkle 1994, last Grigo 2000

    1994  Guensburg & Sprinkle  Rhenopyrginae
    2000  Grigo                 Rhenopyrginae

    Rhenopyrgidae Holloway & Jell 1983: 5 papers, 5 co-author sets, 1983–2020
    in Edrioblastoidina since 2013 (3 papers), in Isorophida 2010 (1 paper), in Order uncertain 1983 (1 paper)

    1983  Holloway & Jell  Rhenopyrgidae, in Order uncertain; named as new
    2010  Müller & Hahn    Rhenopyrgidae, in Isorophida
    2013  Sumrall et al.   Rhenopyrgidae, in Edrioblastoidina; emended; moved from Cyathocystidae; declines a placement in Cyathocystidae
    2017  Briggs et al.    Rhenopyrgidae, in Edrioblastoidina
    2020  Ewin et al.      Rhenopyrgidae, in Edrioblastoidina; emended (p. 118)

A trajectory question needs two blocks. `placed_under` gives the sources that made the placement, first and last stated, with the taxa between; `history` gives every source's treatment of the name in year order, so the rejection reads in its place: Sumrall et al. 2013 "declines a placement in Cyathocystidae", and the two papers that follow keep the family under Edrioblastoidina. The heading measures the agreement (papers, co-author sets, years) so the reader sees how settled a position is without being told a verdict.

## What do the papers in the corpus print as the attribution of family Edrioasteridae, name-bearer and year? Is it Bather 1898 or 1899?

The plan (`docs/walkthrough/03-printed.yaml`):

    blocks:
    - tool: printed_forms
      parameters:
        record: edrioasteridae

The answer:

    Attribution of family Edrioasteridae (name-bearer and year) as printed across sources; family rank only; all years

    Edrioasteridae (Family)
      1978 "Family Edrioasteridae Bell, 1976 [emend. herein]" Bell & Sprinkle 1978 p. 246
      2015 "Family Edrioasteridae Bather, 1899" Sprinkle & Sumrall 2015 p. 348

When the question is about what papers print, the answer is the printed forms, verbatim with their pages. The two sources disagree, one crediting Bell 1976 and the other Bather 1899, and the answer shows both as printed rather than choosing. That disagreement is the object of study, not a defect to resolve.

## What occurrence data does Guensburg & Sprinkle (1994) print for the new species Lampteroblastus hintzei?

The plan (`docs/walkthrough/04-gap.yaml`):

    blocks:
    - tool: statements
      parameters:
        record: hintzei_guensburg_sprinkle_1994
        source: 1994_guensburg_sprinkle
        kind: occurrences

The answer:

    Occurrence data for the new species Lampteroblastus hintzei as printed by Guensburg & Sprinkle (1994)

    Nothing about Lampteroblastus hintzei Guensburg & Sprinkle 1994 is entered from Guensburg & Sprinkle 1994. The occurrences printed in Guensburg & Sprinkle 1994 have not yet been entered (none of them is entered so far).

The paper is on record and its classification is entered, but its occurrence data is not. The closed world answers with what the corpus holds and what it does not yet hold, in the community's words, and never says the paper lacks the data. The model asked `statements` for occurrences in that source; the tool answered with the gap.

## What exact suborder heading do Ewin et al. (2020) print above family Rhenopyrgidae, and at what rank was that name first established?

The plan (`docs/walkthrough/05-miss.yaml`):

    blocks:
    - tool: ancestors
      parameters:
        records:
        - rhenopyrgidae
        trees:
        - taxonomy
        years:
        - 2020
        - 2020
    - tool: history
      parameters:
        record: rhenopyrgidae
        include_related: true
        trees:
        - taxonomy

The answer:

    Rhenopyrgidae (family, with its subfamily-rank form Rhenopyrginae as the same name group) considered; classificatory (taxonomy) trees only; ancestors restricted to Ewin et al. 2020 for the suborder heading, history taken across all years including the related rank to find when the name was first established

    Above Rhenopyrgidae Holloway & Jell 1983: 1 paper, 1 co-author set, 2020

    2020  Ewin et al.  Echinodermata › Edrioasteroidea › Edrioasterida › Edrioblastoidina › Rhenopyrgidae

    Rhenopyrgidae Holloway & Jell 1983: 7 papers, 7 co-author sets, 1983–2020
    family since 1983 (5 papers), subfamily 1994–2000 (2 papers)
    in Edrioblastoidina since 2013 (3 papers), in Isorophida 2010 (1 paper), in Cyathocystidae 1994–2000 (2 papers), in Order uncertain 1983 (1 paper)

    1983  Holloway & Jell       Rhenopyrgidae, in Order uncertain; named as new
    1994  Guensburg & Sprinkle  Rhenopyrginae, in Cyathocystidae; emended; nomen translatum from Rhenopyrgidae
    2000  Grigo                 Rhenopyrginae, in Cyathocystidae
    2010  Müller & Hahn         Rhenopyrgidae, in Isorophida
    2013  Sumrall et al.        Rhenopyrgidae, in Edrioblastoidina; emended; moved from Cyathocystidae; declines a placement in Cyathocystidae
    2017  Briggs et al.         Rhenopyrgidae, in Edrioblastoidina
    2020  Ewin et al.           Rhenopyrgidae, in Edrioblastoidina; emended (p. 118)

This one the eval marks as a miss, and it shows a limit of the plan language. The chain answers the first half: the heading above Rhenopyrgidae in Ewin et al. 2020 is Edrioblastoidina. The second half needs the history of *that* name, which the model could only learn from the first block's result; a plan is stated in full before any block is built, so the model asked for the history of Rhenopyrgidae instead. The answer is honest and grounded, and it is not the answer to the question. A dependent lookup is one of the two things a plan cannot yet express.
