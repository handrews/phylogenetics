"""Each CLI subcommand prints what the library renders, and nothing else.

Runs the parser and `main` in-process over the committed claim table:
the output of a subcommand equals the rendered block from the library
call with the same parameters, `--style` works on any subcommand, an
unresolved name is an answer with exit 0, and a bad argument exits 2.
"""

import json
import os

import pytest

from phylohist import cli, tools

pytestmark = pytest.mark.skipif(
  bool(os.getenv('PHYLOHIST_DRAFTS')),
  reason='the committed claim table covers data/ only',
)


def run(capsys, *argv):
  code = cli.main(list(argv))
  out = capsys.readouterr().out
  return code, out.rstrip('\n')


@pytest.mark.parametrize(
  'argv, expected, shows',
  [
    (
      ['contents', '1994_guensburg_sprinkle', 'astrocystitidae'],
      lambda: tools.contents('1994_guensburg_sprinkle', 'astrocystitidae')[0]['rendered'],
      'Genus Lampteroblastus gen. nov.',
    ),
    (
      ['history', 'rhenopyrgus'],
      lambda: tools.history('rhenopyrgus')['rendered'],
      'Rhenopyrgus Dehm 1961',
    ),
    (
      ['gap', '1983_holloway_jell', 'material'],
      lambda: tools.gap('1983_holloway_jell', 'material')['rendered'],
      'The material printed in Holloway & Jell 1983 has not yet been entered',
    ),
    (
      ['descendants', 'edrioblastoidea', '--no-synonyms'],
      lambda: tools.descendants(['edrioblastoidea'], include_synonyms=False)['rendered'],
      'Astrocystites',
    ),
    (
      ['ancestors', 'rhenopyrgidae', '--years', '1990', '2020'],
      lambda: tools.ancestors(['rhenopyrgidae'], years=(1990, 2020))['rendered'],
      'Above Rhenopyrgidae',
    ),
    (
      ['under', 'Rhenopyrgus grayae', 'Rhenopyrgidae'],
      lambda: tools.placed_under('Rhenopyrgus grayae', 'Rhenopyrgidae')['rendered'],
      'under Rhenopyrgidae',
    ),
    (
      ['placements', 'astrocystitidae', 'rhenopyrgidae', '--sources', '1994_guensburg_sprinkle'],
      lambda: tools.placements(
        ['astrocystitidae', 'rhenopyrgidae'], sources=['1994_guensburg_sprinkle']
      )['rendered'],
      'Guensburg & Sprinkle 1994',
    ),
    (
      ['statements', 'rhenopyrgidae', '--act', 'new'],
      lambda: tools.statements('rhenopyrgidae', act_kind='new')['rendered'],
      'named as new',
    ),
    (
      ['printed', 'edrioblastoidina'],
      lambda: tools.printed_forms('edrioblastoidina')['rendered'],
      'Edrioblastoidina',
    ),
    (
      ['synonymy', 'grayae_bather_1915', '--source', '2020_ewin_martin.m_isotalo_zamora'],
      lambda: tools.synonymy('grayae_bather_1915', source='2020_ewin_martin.m_isotalo_zamora')[0][
        'rendered'
      ],
      'Synonymy under Rhenopyrgus grayae in Ewin et al. 2020',
    ),
  ],
)
def test_subcommand_matches_library(capsys, argv, expected, shows):
  # The wiring: the subcommand prints what the library renders for the
  # same arguments. The literal: a rendering regression fails here too.
  code, out = run(capsys, *argv)
  assert code == 0
  assert out == expected()
  assert shows in out


def test_style_on_any_subcommand(capsys):
  _, after = run(capsys, 'history', 'rhenopyrgus', '--style', 'markdown')
  _, before = run(capsys, '--style', 'markdown', 'history', 'rhenopyrgus')
  assert after == before == tools.history('rhenopyrgus', style='markdown')['rendered']
  _, as_json = run(capsys, 'gap', '1983_holloway_jell', 'material', '--style', 'json')
  block = json.loads(as_json)
  assert block['type'] == 'statement' and 'rendered' not in block


def test_resolve_and_absence(capsys):
  code, out = run(capsys, 'resolve', 'Palæaster')
  assert code == 0 and out.splitlines()[0].startswith('palaeaster  Palaeaster (genus, primary)')
  code, out = run(capsys, 'resolve', 'Rhenoblastus')
  assert code == 0 and out == '(no record in the corpus carries this name)'
  code, out = run(capsys, 'contents', '1994_guensburg_sprinkle', 'no_such_record')
  assert code == 0 and out == '(nothing in the corpus)'
  code, out = run(capsys, 'coverage', '1897_whiteaves')
  assert code == 0 and json.loads(out)['entered'] is False


def test_source_subcommand_and_citations(capsys):
  code, out = run(capsys, 'source', 'Holloway & Jell 1983')
  assert code == 0 and out == '1983_holloway_jell  Holloway & Jell 1983; entered; Holloway, Jell'
  code, out = run(capsys, 'source', 'Klug et al. 2008')
  assert code == 0 and out == '(no source in the corpus is that paper)'
  assert cli.main(['gap', 'Lamarck 1816', 'material']) == 2
  assert '1816a_lamarck, 1816b_lamarck' in capsys.readouterr().err
  _, by_cite = run(capsys, 'gap', 'Dehm 1961', 'diagnoses')
  _, by_key = run(capsys, 'gap', '1961_dehm', 'diagnoses')
  assert by_cite == by_key


def test_plan_subcommand(capsys, tmp_path):
  path = tmp_path / 'plan.yaml'
  path.write_text(
    'header: Rhenopyrgidae under Cyathocystidae\nblocks:\n'
    '- tool: placed_under\n  parameters: {record: rhenopyrgidae, parent: cyathocystidae}\n'
  )
  code, out = run(capsys, 'plan', str(path))
  assert code == 0 and out.startswith('Rhenopyrgidae under Cyathocystidae\n\n')
  assert 'first Guensburg & Sprinkle 1994' in out
  path.write_text('header: x\nblocks:\n- tool: bogus\n  parameters: {}\n')
  assert cli.main(['plan', str(path)]) == 2
  assert 'unknown tool bogus' in capsys.readouterr().err


def test_ambiguous_name_exits_2(capsys):
  assert cli.main(['history', 'casteri']) == 2
  err = capsys.readouterr().err
  assert 'casteri_sprinkle_1973' in err and 'name one by its key' in err
  assert cli.main(['history', 'Rhenopyrgus grayae']) == 0


def test_bad_argument_exits_2(capsys):
  with pytest.raises(SystemExit) as exc:
    cli.main(['gap', '1983_holloway_jell', 'no-such-kind'])
  assert exc.value.code == 2
