# Material migration: the hand list (branch material-model)

Items the migration script could not settle mechanically. Each is a small
YAML edit; the loader's material checks and `scripts/check_draft.py`
report dangling references, so run `poetry run pytest -q` after a batch.

## Free-text identifiers to `label`, `repository`, `holder`

- data/trees/1897_whiteaves.yaml, ottawaensis: three entries whose
  "catalog numbers" are descriptions ("first specimen collected by John
  Stewart, 1886, …", "second specimen …", "an imperfect specimen lent by
  Walter R. Billings"). Suggest `label: first specimen` / `second specimen`
  with `repository: GSC` (the registry's `formerly` covers "Museum of the
  Geological Survey of Canada"), and `label: the specimen lent by Billings`
  with `holder: Walter R. Billings`; the collector and year go in `notes`.
  All three could take `context: division-st` (the node's one context).
- data/trees/1914c_bather.yaml, ottawaensis: labels "A -- Victoria Memorial
  Museum, Ottawa" etc. → `label: A`, `repository: VMM` (registry entry
  added); `label: C`, `holder: Walter R. Billings`. A is `role: holotype,
  roleAct: designated` (Bather selects it, p. 194); B and C `syntype`. The
  figures' `notes: specimen A` / `specimen B` become `of: A` / `of: B`.
  The three entries take `context: division-street`.
- data/trees/1936_bassler.yaml, carteri: "Collection New York State
  Museum" → `repository: NYSM`, `count: 1`, `role: holotype`.
- data/trees/1961_rievers.yaml, coronaeformis: "RVS [Plate 2, Figures
  1–4]" → `label: the specimen of Pl. 2, Figs. 1–4`, `repository: RVS`,
  `role: holotype`, and a figure `{plate: 2, figures: [[1, 4]], of: <that
  label>}` (D1's worked case).
- drafts/1925_hudson.yaml and drafts/1927_hudson.yaml: "cotype A" /
  "cotype B" → `label: A` / `B`, `role: syntype`, `roleAsPrinted: cotype`.
- drafts/1927_jaekel.yaml: the two long descriptive strings → `label`
  plus `repository` (a Riksmuseum Stockholm entry and a Museum Berlin
  entry would need adding to data/repositories.yaml) with the rest in
  `notes`.

## Duplicates left side by side

- data/taxa.yaml holotypes that the script could not match to the
  protologue node's entry by folding: craticula_whitehouse_1941 ("F. 5409"
  in 1941_whitehouse vs "UQF 5409"), navicula_whitehouse_1941 ("F. 5404"
  vs "UQF 5404"), viviani_ewin… ("NHMUK EE16642" vs "EE 16642"). The
  script added the taxa.yaml number as a second entry on the node; keep
  one. For Whitehouse, "F." is the 1941 printed prefix and UQF the modern
  one, so `catalogNumbers: ["F. 5409"]` with `notes` or `formerIds` is the
  faithful form.
- data/taxa.yaml grayae_bather_1915 still carries `holotype:` because
  source 1915b_bather has no tree; enter the tree or move the number to
  the record's `notes`.

## Prefixes the registry cannot resolve (warnings in tests/expected-warnings.txt)

- 1973_sprinkle: "E …" numbers on Bohemian taxa (a Prague register, not
  NHMUK), "PE-…", and bare numbers "610", "611a/b/c" on elongatus. Add
  `repositoryAbbreviations` to the 1973_sprinkle source record once the
  paper's abbreviation list is checked, or `repository` on the entries.
- Registry entries marked "unconfirmed" in data/repositories.yaml (BC,
  DPO, "F.", GCM, GSG, ISU, M, OF, PWL, RS, S, TMF, UC, USGD, UU): confirm
  against the papers when convenient.

## Other

- data/trees/2015_zhao.y.l_peng.j_wu.m.y_luo.x.c_wen.r.q_liu.y.j.yaml,
  yini: an illustration carried a `pages` key (255); check what it meant
  and place it (`page` on the figure, or the node's `pages`).
- Node-level entries with no `context` on nodes that have exactly one
  context: the script never links them, since the old data did not. Link
  where the paper says so (Bather 1914, Whiteaves 1897 above; check
  1961_rievers, 2000_grigo, 1842_vanuxem).
- Sowerby 1825 (four-part locality, no period) and Jaekel 1927's
  Petersburg entry stayed contexts, not ranges; confirm.
- Roles printed as `plesiotypes`/`hypotypes` kept their role; add
  `roleAsPrinted` where the paper's word differs from the role.
