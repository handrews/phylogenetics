# Material migration: the hand list

Items the stage 2 migration could not settle without the paper. Each is a
small YAML edit. The loader's material checks and `scripts/check_draft.py`
report a dangling `context`, `of` or `castOf`, an ambiguous prefix, and a
listed repository no number uses, so run the suite after a batch.

## Free-text identifiers

- data/trees/1897_whiteaves.yaml, ottawaensis: three entries whose
  "catalog numbers" are descriptions of the specimens. They want a
  `label` each, `repository: gsc` for the two Survey specimens (the
  registry's `otherNames` covers "Museum of the Geological Survey of
  Canada"), `holder: Walter R. Billings` for the third, and
  `collectedBy` / `collectedDate` for "John Stewart, 1886". All three
  could take the node's one context.
- data/trees/1961_rievers.yaml, coronaeformis: the holotype's
  identifier is a figure citation. It wants a `label`, `repository:
  rievers`, and an `illustrations` entry with `of` naming that label.
- drafts/1927_jaekel.yaml: two long descriptive strings. Each wants a
  `label`, with the holder either a new registry entry (Riksmuseum
  Stockholm; Museum Berlin) or `holder`, and the rest in `notes`.

## Record-level holotypes

- grayae_bather_1915 still carries `holotype:` on its record, because
  source 1915b_bather has no tree. Enter the tree, or move the number to
  the record's `notes`.

## Sprinkle 1973

Re-entered from the paper on 2026-09-30; the report, with every null
and its reason, is `notes/reviews/review_1973_sprinkle.md`. Left for the
owner, each with its page there:

- Skeleton: the tree has no node for *Lysocystites sculptus*, which is
  the species all the *Lysocystites* material and figures belong to
  (pp. 139–142, Pl. 33); `nodosus`, the type species, carries
  `material: null`. The other figured or cited taxa with no node
  (*Columbocystis typica*, *Malocystites murchisoni*, *Cystidea
  nugatula*, the unassigned plates) are listed there.
- Three `material` nulls are on species whose specimens the paper
  mentions without citing: *Acanthocystites briareus* ("Only a single
  specimen ... is known to exist", p. 105), *Pareocrinus ljubzovi*
  ("based on only a single complete specimen ... No material was
  available for study", p. 112) and *Cambrocrinus regularis*
  (Orłowski's "approximately 50 partially complete specimens", p. 121).
  *Blastocystis rossica*, the same case but figured, has a `label`
  entry with `examined: false`. Decide which reading the null means.
- "(not figured)" and a drawing tied to no specimen. *Kinzercystis
  durhami*'s MCZ 729 is printed "unfigured paratypes MCZ 729" (p. 76),
  yet the tools do not say "(not figured)" for it. The derived rule
  marks a specimen only when no figure on the node is without an `of`,
  since an untied figure might show it, and the node carries Text-fig.
  5A (p. 16), a drawing whose caption names no specimen. So nothing on
  the node is marked, MCZ 729 included. Recommended: let only an untied
  photograph or cast block the statement, and treat an untied `drawing`
  or `reconstruction` as a generalised diagram that shows no particular
  specimen. That is one condition in `_NodeClaims._unfigured`
  (`phylohist/claims.py`) and a sentence in `docs/claims.md`, and it
  would mark more specimens across the tree. The case against: a line
  drawing can be of one specimen whose number the caption omits, and
  the looser rule would then call that specimen unfigured. Decide while
  reading the text-figure captions.
- Misprints to read: "syntype USNM 6431" (p. 83); holotype "USNM
  165478" against 165378 elsewhere (p. 151); "MCZ 602–RO–5" against
  the plates' "602-R3" and "602-R1-4" (p. 168, Pls. 40–41); the cast
  numbers of Pl. 3.
- Suspected errors in the tree itself, not touched: the root's
  attribution (the paper prints "Bruguière, 1789"), the key
  `charcariaedens` (printed *carchariaedens*), "Ressler" for Resser,
  Jaekel "1980", *Bockia neglecta* "Hecker, 1938", the two
  "incorrectly given as 1859" notes, and the doubled `diploporita-class`
  and `palaeocystites` nodes.

What the model could not say, for stage 4:

- A queried age ("Middle Ordovician(?)") has no tentative form; the
  "(?)" is in the range's `notes`.
- One number cited under two species (MCZ 643, MCZ 644, GSC 25954) is
  entered under both as printed.

## Von Buch 1844: the two genus-level `affTaxon` nodes

Not a material item; recorded here until the open-nomenclature fields
are settled. The tree reads two prose notes at the end of the paper as
"aff." and neither is. The passage, in the 1846 translation:

> Pseudocrinites bicopuladigiti, figured by Mr. R. Garnet [...] and
> described by Messrs. Bennett and Pearce, is manifestly a Cystidea
> resembling Caryocystites. [...]
>
> A species figured and described by Mr. J. Sowerby in the 'Zoological
> Journal' (ii. 318) also probably belongs to this family. [...] a
> considerable number of irregular plates surround, as in Sphaeronites,
> the spheroidal figure. It was discovered by Mr. Bigsby not far from
> the falls of La Chaudière on the Ottawa river in Lower Canada.

"aff." marks a form its author thinks new and relates to a named taxon
(Matthews 1973, p. 716; Bengtson 1988, p. 224). Von Buch does neither:
he makes two placements in his family Cystidea and adds a comparison of
form to each.

- *Pseudocrinites bicopuladigiti*: "manifestly a Cystidea" is a firm
  placement. The species goes under a `pseudocrinites` node, as he cites
  it, directly under `cystidea-family`; "resembling Caryocystites" goes
  in `notes`, quoted. Today it sits under `affTaxon: caryocystites` with
  *Pseudocrinites* as a former genus, which reads as a recombination he
  never makes.
- Sowerby's species: "also probably belongs to this family" is a
  provisional placement of a form Sowerby left unnamed. An open species
  under `cystidea-family` with `provisional: true`; "as in Sphaeronites"
  describes the plating and goes in `notes` or nowhere. Today it sits
  under `affTaxon: sphaeronites`.
- The form is already in the corpus under its own records. "Zoological
  Journal (ii. 318)" is `1825b_sowerby.g.b`, the Bigsby specimen from
  the Chaudière falls, whose tree has `asteriadae-gen_sowerby.g.b_1825`
  and `asteriadae-gen-sp_sowerby.g.b_1825`. Von Buch's tree uses three
  placeholders made before that source was identified:
  `cystidea-sp_buch_1944` and the two
  `crinoidea-secondhand-…_sowerby_1833` records (dated 1933, "date
  uncertain"). Pointing von Buch's node at Sowerby's own open records
  replaces all three, and is the worked case for an open record shared
  by its author's tree and a later source that cites it.
- These are the only genus-level cf. or aff. nodes in the corpus, so
  once they go nothing prints one, and how to record a genus-level cf.
  or aff. can wait for a source that does.

## Other

- Nodes with exactly one context whose entries carry no `context`: the
  script links an entry to a context only where the old data nested the
  specimen inside the occurrence. Link the rest where the paper says so
  (check 1842_vanuxem, 2000_grigo, 2010_müller.p_hahn).
- Sowerby 1825's four-part locality and the Jaekel draft's Petersburg
  entry stayed contexts, since neither gives a period. Confirm.
- Müller & Hahn 2010: every holotype is a cast in Mainz of an original
  in the Seibert collection. The entries want `preparation` and, where
  both numbers are entered, `castOf`.

## Already applied in the migration commit

Listed so they can be checked: the Hudson drafts' cotypes (`label: A`,
`B`, `role: cotype`); Bather 1914's A, B and C (labels, `repository:
vmm` or `holder`, A as the designated holotype, the context link, and
`of` on the plate `illustrations`); Bassler 1936's holotype (`repository: nysm`,
`count: 1`); Fay 1962's No. 752 (`role: lectotype`, inferred, with its
basis) and the lost second syntype.
