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


@pytest.mark.parametrize('argv, expected', [
  (['contents', '1994_guensburg_sprinkle', 'astrocystitidae'],
   lambda: tools.contents('1994_guensburg_sprinkle', 'astrocystitidae')[0]['rendered']),
  (['history', 'rhenopyrgus'], lambda: tools.history('rhenopyrgus')['rendered']),
  (['gap', '1983_holloway_jell', 'material'],
   lambda: tools.gap('1983_holloway_jell', 'material')['rendered']),
  (['descendants', 'edrioblastoidea', '--no-synonyms'],
   lambda: tools.descendants(['edrioblastoidea'], include_synonyms=False)['rendered']),
  (['ancestors', 'rhenopyrgidae', '--years', '1990', '2020'],
   lambda: tools.ancestors(['rhenopyrgidae'], years=(1990, 2020))['rendered']),
  (['under', 'Rhenopyrgus grayae', 'Rhenopyrgidae'],
   lambda: tools.placed_under('Rhenopyrgus grayae', 'Rhenopyrgidae')['rendered']),
  (['placements', 'astrocystitidae', 'rhenopyrgidae', '--sources', '1994_guensburg_sprinkle'],
   lambda: tools.placements(['astrocystitidae', 'rhenopyrgidae'], sources=['1994_guensburg_sprinkle'])['rendered']),
  (['statements', 'rhenopyrgidae', '--act', 'new'],
   lambda: tools.statements('rhenopyrgidae', act_kind='new')['rendered']),
  (['printed', 'edrioblastoidina'], lambda: tools.printed_forms('edrioblastoidina')['rendered']),
  (['synonymy', 'grayae_bather_1915', '--source', '2020_ewin_martin.m_isotalo_zamora'],
   lambda: tools.synonymy('grayae_bather_1915', source='2020_ewin_martin.m_isotalo_zamora')[0]['rendered']),
])
def test_subcommand_matches_library(capsys, argv, expected):
  code, out = run(capsys, *argv)
  assert code == 0
  assert out == expected()


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


def test_ambiguous_name_exits_2(capsys):
  assert cli.main(['history', 'casteri']) == 2
  err = capsys.readouterr().err
  assert 'casteri_sprinkle_1973' in err and 'name one by its key' in err
  assert cli.main(['history', 'Rhenopyrgus grayae']) == 0


def test_bad_argument_exits_2(capsys):
  with pytest.raises(SystemExit) as exc:
    cli.main(['gap', '1983_holloway_jell', 'no-such-kind'])
  assert exc.value.code == 2
