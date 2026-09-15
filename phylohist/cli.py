"""The command line: one subcommand per tool, output in a style.

    phylohist resolve "Palæaster"
    phylohist contents 1994_guensburg_sprinkle astrocystitidae --synonymy
    phylohist descendants edrioblastoidea
    phylohist placements astrocystitidae rhenopyrgidae --years 1990 2020
    phylohist ancestors astrocystitidae cyathocystidae rhenopyrgidae
    phylohist history rhenopyrgus
    phylohist synonymy grayae_bather_1915
    phylohist statements ottawaensis_whiteaves_1897 --source 1962_fay
    phylohist coverage 1983_holloway_jell
    phylohist gap 1983_holloway_jell material
    phylohist printed edrioblastoidina
    phylohist tools

Reads the committed `claims/` directory only, so it needs no loader and
starts at once. `--style text|markdown|json` picks the rendering; json is
the block itself. An unresolved name or an unknown source is an answer
(the corpus holds nothing), exit 0; a bad argument is exit 2.
"""

import argparse
import json
import sys

import yaml

from . import plan as plans
from . import tools
from .render import render_composition, styles

# Every subcommand that is a tool, by the tool's name; `plan` and `tools`
# are the CLI's own.
SUBCOMMANDS = {
  'resolve': 'resolve_name',
  'source': 'resolve_source',
  'contents': 'contents',
  'placements': 'placements',
  'descendants': 'descendants',
  'ancestors': 'ancestors',
  'under': 'placed_under',
  'history': 'history',
  'synonymy': 'synonymy',
  'statements': 'statements',
  'coverage': 'source_coverage',
  'gap': 'gap',
  'printed': 'printed_forms',
}


def _print_blocks(result, style):
  if isinstance(result, list):
    if not result:
      print('(nothing in the corpus)')
      return
    for i, block in enumerate(result):
      if i:
        print()
      if style == 'json':
        print(json.dumps(block, ensure_ascii=False, indent=1))
      else:
        print(block['rendered'])
  elif isinstance(result, dict) and 'rendered' in result and style != 'json':
    print(result['rendered'])
  else:
    print(json.dumps(result, ensure_ascii=False, indent=1))


def build_parser():
  parser = argparse.ArgumentParser(prog='phylohist', description=__doc__.split('\n\n')[0])
  common = argparse.ArgumentParser(add_help=False)
  common.add_argument('--style', choices=styles(), default=argparse.SUPPRESS)
  parser.add_argument('--style', choices=styles(), default=argparse.SUPPRESS)
  sub = parser.add_subparsers(dest='command', required=True)

  def add_parser(name, **kwargs):
    return sub.add_parser(name, parents=[common], **kwargs)

  p = add_parser('resolve', help='records a printed name can refer to')
  p.add_argument('query')
  p.add_argument('--rank')

  p = add_parser('source', help='the sources a citation can mean')
  p.add_argument('query')

  p = add_parser('contents', help='what a source places under a record')
  p.add_argument('source', nargs='?', help='a source key, or - for every source')
  p.add_argument('record')
  p.add_argument('--depth', type=int)
  p.add_argument('--synonymy', action='store_true')

  for name, help_text in (
    ('placements', 'where each source places each record'),
    ('descendants', 'everything any source places under the records'),
    ('ancestors', 'every higher taxon any source places the records under'),
  ):
    p = add_parser(name, help=help_text)
    p.add_argument('records', nargs='+')
    p.add_argument('--years', nargs=2, type=int, metavar=('FIRST', 'LAST'))
    p.add_argument('--trees', nargs='+', choices=['taxonomy', 'cladogram', 'diagram', 'other'])
    p.add_argument('--no-variants', dest='include_variants', action='store_false')
    if name != 'ancestors':
      p.add_argument('--no-synonyms', dest='include_synonyms', action='store_false')
    if name == 'placements':
      p.add_argument('--sources', nargs='+')

  p = add_parser('under', help='the sources that place a record under a higher taxon')
  p.add_argument('record')
  p.add_argument('parent')
  p.add_argument('--years', nargs=2, type=int, metavar=('FIRST', 'LAST'))
  p.add_argument('--trees', nargs='+', choices=['taxonomy', 'cladogram', 'diagram', 'other'])
  p.add_argument('--no-variants', dest='include_variants', action='store_false')

  p = add_parser('history', help='what each source does with a name')
  p.add_argument('record')
  p.add_argument(
    '--alone',
    dest='include_related',
    action='store_false',
    help='this record only, not the same name at other ranks',
  )
  p.add_argument('--synonymy', action='store_true', help="each source's synonymy under its line")
  p.add_argument('--years', nargs=2, type=int, metavar=('FIRST', 'LAST'))
  p.add_argument('--trees', nargs='+', choices=['taxonomy', 'cladogram', 'diagram', 'other'])

  p = add_parser('synonymy', help='the synonymy a source prints under a record')
  p.add_argument('record')
  p.add_argument('--source')

  p = add_parser('statements', help='every statement about a record, in words')
  p.add_argument('record')
  p.add_argument('--source')
  p.add_argument('--kind')
  p.add_argument('--act', dest='act_kind')

  p = add_parser('coverage', help='what the corpus holds of a source')
  p.add_argument('source')

  p = add_parser(
    'gap', help='the sentence for what is not yet entered, or for a name no source carries'
  )
  p.add_argument('source', nargs='?')
  p.add_argument('kind', nargs='?', choices=list(tools.COVERAGE_WORDS))
  p.add_argument('--name', help='a name no source in the corpus carries')

  p = add_parser('printed', help='each form a source prints for a record')
  p.add_argument('record')
  p.add_argument('--source')

  p = add_parser(
    'plan', help='execute a plan (YAML or JSON: header, blocks, question) and print the answer'
  )
  p.add_argument('file', help='a plan file, or - for stdin')

  add_parser('tools', help='the tools and what they answer')
  return parser


def main(argv=None):
  try:
    return _main(argv)
  except ValueError as exc:
    print(exc, file=sys.stderr)
    return 2


def _arguments(args, tool):
  """The tool's parameters, from the parsed arguments of the same names."""
  properties = next(s for s in tools.TOOL_SPECS if s['name'] == tool)['input_schema']['properties']
  arguments = {name: getattr(args, name) for name in properties if hasattr(args, name)}
  if tool == 'contents' and arguments.get('source') == '-':
    arguments['source'] = None
  return arguments


def _main(argv):
  args = build_parser().parse_args(argv)
  style = getattr(args, 'style', 'text')
  command = args.command
  if command == 'tools':
    for name, text in tools.TOOL_DESCRIPTIONS.items():
      print(f'{name}\n  {text}\n')
    return 0
  if command == 'plan':
    text = sys.stdin.read() if args.file == '-' else open(args.file).read()
    outcome = plans.execute(yaml.safe_load(text))
    for error in outcome['errors']:
      where = f'block {error["block"]} ({error["tool"]})' if error.get('block') else 'plan'
      print(f'{where}: {error["error"]}', file=sys.stderr)
    if outcome['composition'] is None:
      return 2
    if style == 'json':
      print(json.dumps(outcome['composition'], ensure_ascii=False, indent=1))
    else:
      print(render_composition(outcome['composition'], style))
    return 0
  tool = SUBCOMMANDS[command]
  result = tools.call(tool, _arguments(args, tool), style=style)
  if command == 'resolve':
    _print_resolved(result, style)
  elif command == 'source':
    _print_sources(result, style)
  elif command == 'coverage':
    print(json.dumps(result, ensure_ascii=False, indent=1))
  else:
    _print_blocks(result, style)
  return 0


def _print_resolved(result, style):
  if style == 'json':
    print(json.dumps(result, ensure_ascii=False, indent=1))
    return
  if not result:
    print('(no record in the corpus carries this name)')
    return
  for c in result:
    line = f'{c["key"]}  {c["name"] or "[placeholder]"} ({c["rank"]}, {c["kind"]}'
    if c.get('of'):
      line += f', of {c["of"]}'
    line += f'); {c.get("authority") or "authority not recorded"}; '
    line += f'{c["sourcesWithStatements"]} sources'
    if c.get('variants'):
      line += f'; same name at other ranks or spellings: {", ".join(c["variants"])}'
    if c.get('combinations'):
      line += '; as ' + '; '.join(
        f'{x["label"]} {x["firstYear"]}'
        + (f'–{x["lastYear"]}' if x['lastYear'] != x['firstYear'] else '')
        for x in c['combinations']
      )
    print(line)


def _print_sources(result, style):
  if style == 'json':
    print(json.dumps(result, ensure_ascii=False, indent=1))
    return
  if not result:
    print('(no source in the corpus is that paper)')
    return
  for c in result:
    print(
      f'{c["key"]}  {c["cite"]}; {"entered" if c["entered"] else "not entered"}; '
      + ', '.join(c['authors'])
    )


if __name__ == '__main__':
  sys.exit(main())
