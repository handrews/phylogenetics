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
