"""The closures reproduce the worked example of notes/development/structured-answers.md.

"Under what higher taxa have edrioblastoids been placed across the
corpus?": the records that constitute the group, everything any source
places under them, everything any source places them under, and the
measurement of a name's trajectory, all computed from the committed
claim table.
"""

import os

import pytest

pytestmark = pytest.mark.skipif(
  bool(os.getenv('PHYLOHIST_DRAFTS')),
  reason='the committed claim table covers data/ only',
)


def test_group_resolves_to_rank_variants(closure):
  assert closure.variants('edrioblastoidea') == ['edrioblastoida', 'edrioblastoidina']
  assert closure.store.resolve_name('Edrioblastida') == []


def test_descendants_of_edrioblastoids(closure):
  found = closure.descendants(['edrioblastoidea'])
  expected = {
    'pentacystida',
    'astrocystitidae',
    'steganoblastidae',
    'cyathocystidae',
    'rhenopyrgidae',
    'cyathocystinae',
    'rhenopyrginae',
    'astrocystites',
    'cambroblastus',
    'lampteroblastus',
    'porosublastus',
    'ikerus',
    'cyathocystis',
    'cyathotheca',
    'rhenopyrgus',
    'heropyrgus',
    'steganoblastus',
  }
  missing = expected - set(found)
  assert not missing, missing
  # Steganoblastus enters through synonymy, not a placement.
  assert any('synonymOf' in via for via in found['steganoblastus'])
  # Every placement hit names its source, year and claim.
  for via in found['rhenopyrgidae']:
    assert via.get('variantOf') or (via['source'] and via['year'] and via['claim'])


def test_descendants_without_synonyms(closure):
  found = closure.descendants(['edrioblastoidea'], include_synonyms=False)
  assert 'lampteroblastus' in found
  assert not any('synonymOf' in via for vias in found.values() for via in vias)


def test_ancestors_of_edrioblastoids(closure):
  members = ['edrioblastoidea', 'astrocystitidae', 'cyathocystidae', 'rhenopyrgidae']
  found = closure.ancestors(members)
  for key in (
    'edrioasteroidea',
    'edrioasterida',
    'echinozoa',
    'crinozoa',
    'pelmatozoa',
    'isorophida',
    'cyathocystida',
  ):
    assert key in found, key
  blastoidea = found['blastoidea']
  assert {via['kind'] for via in blastoidea} == {'alternative'}
  assert any(via['source'] == '1935_bassler' for via in blastoidea)
  uncertain = found['edrioasteroidea-order-uncertain_holloway_jell_1983']
  assert {via['kind'] for via in uncertain} == {'placeholder'}
  # Depth counts steps up the chain within one source.
  assert min(via['depth'] for via in found['edrioasteroidea']) == 1


def test_year_range(closure):
  found = closure.descendants(['edrioblastoidea'], years=(1994, 2000))
  assert 'lampteroblastus' in found
  assert all(
    1994 <= via['year'] <= 2000 for vias in found.values() for via in vias if 'year' in via
  )


def test_schemes_for_rhenopyrgidae(closure):
  schemes = closure.schemes(['rhenopyrgidae'])
  by_parent = {s['parents'][0]['key']: s for s in schemes}
  assert set(by_parent) >= {'edrioblastoidina', 'cyathocystidae'}
  cyatho = by_parent['cyathocystidae']
  assert cyatho['sources'] == ['1994_guensburg_sprinkle', '2000_grigo']
  assert cyatho['papers'] == 2 and len(cyatho['coauthorSets']) == 2
  assert schemes[0]['lastYear'] >= schemes[-1]['lastYear']


def test_measurement_of_rhenopyrgus(closure):
  m = closure.measurement('rhenopyrgus')
  assert m['records'] == ['rhenopyrgus', 'rhenopyrgus-subgenus']
  ranks = {r['rank']: r for r in m['ranks']}
  assert m['latestRank']['rank'] == 'genus'
  assert ranks['genus']['firstYear'] == 1983
  assert ranks['genus']['papers'] == 5
  assert len(ranks['genus']['coauthorSets']) == 5
  assert ranks['subgenus']['lastSource'] == '1966_regnéll'
  assert ranks['subgenus']['sources'] == ['1961_dehm', '1966_regnéll']
  assert m['papers'] == 7
  # A cladogram enters only when asked for.
  with_clado = closure.measurement('rhenopyrgus', trees=('taxonomy', 'cladogram'))
  assert {r['rank']: r['papers'] for r in with_clado['ranks']}['genus'] == 6
