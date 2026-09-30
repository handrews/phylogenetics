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

Migrated mechanically; re-entry from the paper is stage 3. Until then:

- "EE 39" and "EE 51" resolve to `nhmuk` by prefix, which is probably
  wrong: the inline comment calls them casts, and the paper's E and BC
  casts are the Caster Collection's. Check the page.
- The bare numbers "610", "611a", "611b", "611c" on elongatus are MCZ
  numbers in the paper ("Holotype MCZ 610; figured paratype MCZ 611a").
- "PE-199" and "PE-199-A" are the North Museum's, to be deposited; the
  casts MCZ 629A and B are `castOf` them.

## Other

- data/trees/2015_zhao.y.l_peng.j_wu.m.y_luo.x.c_wen.r.q_liu.y.j.yaml,
  yini: an illustration carried a `pages` key (255). Decide whether it
  is the illustration's `page` or belongs to the node's `pages`.
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
