# The test corpus

A frozen slice of `data/` for the tests, taken at commit 34f21b5 (main,
11 October 2026): the seven record files whole, and 53 of the 220
trees. It is not resynced with `data/`, since the tests must not depend
on what the curated data says today. Edit it only to add the case a test
needs or to migrate it alongside a schema change, and keep it loading
with no error.

The trees are the sources the tests name, with a few the tests lean on
without naming: 1815_lamarck, which 1816a and 1816b merge into;
1820_say, which places Pentacrinus beside Miller 1821's "Pentacrinites
or Pentacrinus"; 1961_rievers, for the combination Pyrgocystis
(Rhenopyrgus) coronaeformis; 1981_bockelie and 2012_doweld, whose
combinations of Bockia neglecta differ from Sprinkle 1973's;
2013_müller.p_hahn_bohatý, which places Timeischytes casteri beside Bell
1975; and 2015_sprinkle_sumrall, which places Porosublastus. The record
files stay whole because a record a tree cites must exist, and a record
no tree cites costs nothing; dropping a whole tree only removes
"Protologue not flagged" warnings, which the corpus does not snapshot.

    1758_linnaeus
    1761_linnaeus
    1766_linnaeus
    1815_lamarck
    1816a_lamarck
    1816b_lamarck
    1820_say
    1821_miller.j.s
    1844_buch
    1857_billings
    1858b_billings
    1897_whiteaves
    1914c_bather
    1935_bassler
    1936_bassler
    1941_whitehouse
    1960_gill_caster
    1961_dehm
    1961_rievers
    1962_fay
    1966_regnéll
    1967a_fay
    1968b_paul.c.r.c
    1973_sprinkle
    1975_bell.b.m
    1975_kolata
    1976_bell.b.m
    1981_bockelie
    1982c_parsley
    1983_holloway_jell
    1985_jell_burrett_banks
    1985_smith.a.b
    1985_sprinkle
    1990_smith.a.b_jell
    1994_guensburg_sprinkle
    1996_sumrall_bowsher
    1998_dean.j_smith.a.b
    2000_grigo
    2003_guensburg_sprinkle
    2004_parsley_prokop
    2005_frest
    2010_müller.p_hahn
    2012_doweld
    2013_müller.p_hahn_bohatý
    2013_nardin_bohatý
    2013_sumrall_heredia_rodríguez.c.m_mestre
    2015_sprinkle_sumrall
    2017_nardin_lefebvre_fatka_nohejlová_kašiča_šinágl_szabad
    2017_zamora_sumrall_zhu.x.j_lefebvre
    2020_ewin_martin.m_isotalo_zamora
    2020_guensburg_sprinkle_mooi_lefebvre_david_roux_derstler
    2021_jell_sprinkle
    2022_zamora_rahman_sumrall_gibson_thompson

`tests/conftest.py` loads the corpus once per session (the `corpus`
fixture), writes its claim table to a temporary directory, and gives
every test the registries as that load left them. To see the claims it
yields, or to check a draft against it:

    poetry run python scripts/claims.py --data tests/corpus --out /tmp/corpus-claims
    poetry run python scripts/check_draft.py --data tests/corpus some-draft.yaml

`data/time.yaml` is not copied; nothing reads it.
