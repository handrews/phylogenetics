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

from . import tools
from .render import styles


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
  p.add_argument('--alone', dest='include_related', action='store_false',
                 help='this record only, not the same name at other ranks')
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

  p = add_parser('coverage', help="what the corpus holds of a source")
  p.add_argument('source')

  p = add_parser('gap', help='the sentence for what is not yet entered, or for a name no source carries')
  p.add_argument('source', nargs='?')
  p.add_argument('kind', nargs='?', choices=list(tools.COVERAGE_WORDS))
  p.add_argument('--name', help='a name no source in the corpus carries')

  p = add_parser('printed', help='each form a source prints for a record')
  p.add_argument('record')
  p.add_argument('--source')

  add_parser('tools', help='the tools and what they answer')
  return parser


def main(argv=None):
  try:
    return _main(argv)
  except ValueError as exc:
    print(exc, file=sys.stderr)
    return 2


def _main(argv):
  args = build_parser().parse_args(argv)
  style = getattr(args, 'style', 'text')
  command = args.command
  if command == 'tools':
    for name, text in tools.TOOL_DESCRIPTIONS.items():
      print(f'{name}\n  {text}\n')
    return 0
  if command == 'resolve':
    result = tools.resolve_name(args.query, rank=args.rank)
    if style == 'json':
      print(json.dumps(result, ensure_ascii=False, indent=1))
    elif not result:
      print('(no record in the corpus carries this name)')
    else:
      for c in result:
        line = f"{c['key']}  {c['name'] or '[placeholder]'} ({c['rank']}, {c['kind']}"
        if c.get('of'):
          line += f", of {c['of']}"
        line += f"); {c.get('authority') or 'authority not recorded'}; "
        line += f"{c['sourcesWithStatements']} sources"
        if c.get('variants'):
          line += f"; same name at other ranks or spellings: {', '.join(c['variants'])}"
        if c.get('combinations'):
          line += '; as ' + '; '.join(
            f"{x['label']} {x['firstYear']}" + (f"–{x['lastYear']}" if x['lastYear'] != x['firstYear'] else '')
            for x in c['combinations'])
        print(line)
    return 0
  if command == 'source':
    result = tools.resolve_source(args.query)
    if style == 'json':
      print(json.dumps(result, ensure_ascii=False, indent=1))
    elif not result:
      print('(no source in the corpus is that paper)')
    else:
      for c in result:
        print(f"{c['key']}  {c['cite']}; {'entered' if c['entered'] else 'not entered'}; "
              + ', '.join(c['authors']))
    return 0
  if command == 'coverage':
    print(json.dumps(tools.source_coverage(args.source), ensure_ascii=False, indent=1))
    return 0

  years = tuple(args.years) if getattr(args, 'years', None) else None
  if command == 'contents':
    source = None if args.source in (None, '-') else args.source
    result = tools.contents(source, args.record, depth=args.depth, synonymy=args.synonymy, style=style)
  elif command == 'placements':
    result = tools.placements(args.records, sources=args.sources, years=years,
                              include_variants=args.include_variants,
                              include_synonyms=args.include_synonyms, trees=args.trees, style=style)
  elif command == 'descendants':
    result = tools.descendants(args.records, include_synonyms=args.include_synonyms,
                               include_variants=args.include_variants, trees=args.trees,
                               years=years, style=style)
  elif command == 'ancestors':
    result = tools.ancestors(args.records, include_variants=args.include_variants,
                             trees=args.trees, years=years, style=style)
  elif command == 'under':
    result = tools.placed_under(args.record, args.parent, include_variants=args.include_variants,
                                trees=args.trees, years=years, style=style)
  elif command == 'history':
    result = tools.history(args.record, include_related=args.include_related,
                           synonymy=args.synonymy, trees=args.trees, years=years, style=style)
  elif command == 'synonymy':
    result = tools.synonymy(args.record, source=args.source, style=style)
  elif command == 'statements':
    result = tools.statements(args.record, source=args.source, kind=args.kind,
                              act_kind=args.act_kind, style=style)
  elif command == 'gap':
    result = tools.gap(args.source, args.kind, name=args.name, style=style)
  elif command == 'printed':
    result = tools.printed_forms(args.record, source=args.source, style=style)
  else:
    return 2
  _print_blocks(result, style)
  return 0


if __name__ == '__main__':
  sys.exit(main())
