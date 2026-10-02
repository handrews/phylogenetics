# Material migration: the hand list

Items the material migrations could not settle without the paper. Each
is a small YAML edit. The loader's material checks and
`scripts/check_draft.py` report a dangling `context`, `of` or `castOf`,
a `prefix` missing from the file's `prefixes` map, and a map entry
nothing uses, so run the suite after a batch.

## Free-text identifiers

When numbers moved to `prefix` and `numbers` (2026-10-01), a string
that described a specimen became its `label`, text unchanged. Each
still wants a proper entry.

- data/trees/1897_whiteaves.yaml, ottawaensis: three labels that are
  descriptions of the specimens. They want a short `label` each,
  `repository: gsc` for the two Survey specimens, `holder: Walter R.
  Billings` for the third, and `collectedBy` / `collectedDate` for "John
  Stewart, 1886". All three could take the node's one context.
- data/trees/1961_rievers.yaml, coronaeformis: the holotype's label is
  a figure citation ("RVS [Plate 2, Figures 1–4]"). It wants a `label`
  of its own and an `illustrations` entry with `of` naming it.
- data/trees/1842_vanuxem.yaml: the holotype's label is "Page 306,
  Figure 80", a figure citation in the same way.
- drafts/1927_jaekel.yaml: two long descriptive labels. Each wants a
  short `label`, with the holder either a new registry entry
  (Riksmuseum Stockholm; Museum Berlin) or `holder`, and the rest in
  `notes`.
- data/trees/1962_fay.yaml: No. 752 is `repository: gsc`, `numbers:
  [752]`, with `asPrinted: Canadian Geological Survey 752`. The caption
  prints "Holotype, 752, Canadian Geological Survey" (p. 201); set
  `asPrinted` to what is printed, or drop it.

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

- One number cited under two species (MCZ 643, MCZ 644, GSC 25954) is
  entered under both as printed.

## Open nomenclature, after the 2026-10-01 migration

- Gill & Caster 1960: the two forms entered as "aff. *wilkinsi*" are
  now `victoriacystis-aff-wilkinsi-a_gill_caster_1960` and `-b`, in
  tree order. Read what the paper calls them and set each record's
  `designation` (or rename the keys).
- Schlotheim 1826: the aff. form of *pomum* still carries
  `questionable`. Whether the "?" doubts the form or the comparison
  is for whoever reads that paper.
- Sprinkle 1973, *Gogia multibrachiatus*: USNM 165425 is "additional
  specimen (topotype?)" in the text (p. 86) and "plesiotype" on
  Pl. 11. It is entered as `role: plesiotype` with the query in
  `notes`. If the text's word is taken, it is `role: topotype` with
  `roleUncertain: true`.
- Guensburg & Sprinkle 1994 and Guensburg et al. 2020: *lloydi*
  carries `provisional` beside `quotedParent`. The note attributes
  the provisional assignment to Sprinkle 1985; check whether either
  paper makes it its own.
- Müller, Hahn & Bohatý 2013: "Timeischytes" *prescheri*? Grigo, 2000
  is one specimen from the Prescher collection (Grigo's fig. 7). The
  tree has no material for *prescheri*; when it does, that specimen
  is an entry with `uncertain: true`.
- Bell 1891 (draft): "Cystidea" is `quoted` twice, from a diagram.
  What the quotes mean there is undecided.
- `provisional` on a synonymy entry (twelve uses) is stored and
  carried on no claim, so the tools do not print "Eocystites?
  longidactylus" as cited.

## `sameAs` links to enter

The mechanism is built and no link is entered. Each of these needs
the paper's own words (or an editorial block saying it is inferred):

- *Astrocystites ottawaensis*: Whiteaves 1897's three specimens,
  Bather 1914's A, B and C, Fay 1962's No. 752 and the specimen lent
  to Hudson.
- The Bigsby specimen: Sowerby 1825, the later Billings papers, Bell
  1976.
- Bell 1976's two UCLAPC fragments ("Genus and Species
  Indeterminate") and Sumrall & Bowsher 1996's *Giganticlavus* cf.
  *G. bennisoni*. These carry numbers, so they join by number once
  the 1996 tree has its material.
- Grigo 2000's doubtfully assigned specimen (fig. 7) and Müller, Hahn
  & Bohatý 2013's "Timeischytes" *prescheri*?.

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
