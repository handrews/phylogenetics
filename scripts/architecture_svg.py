#!/usr/bin/env python3
"""Draw the architecture figure the README shows, in a light and a dark palette.

    poetry run python scripts/architecture_svg.py

Writes `docs/architecture.svg` and `docs/architecture-dark.svg`; the
README wraps them in a `<picture>` so GitHub shows the one matching the
reader's theme. The layout is fixed by hand: three lanes (human, model,
code) and four columns (the data, the CLI, chat, the eval) that each read
top to bottom, with the arrows on column lines so nothing crosses a box.
"""

import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / 'docs'
FONT = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"

PALETTES = {
  'light': {
    'heading': '#444441',
    'arrow': '#5F5E5A',
    'box_fill': '#FFFFFF',
    'box_stroke': '#888780',
    'title': '#2C2C2A',
    'subtitle': '#5F5E5A',
    'lanes': {
      'human': ('#EEEDFE', '#534AB7', '#3C3489'),
      'model': ('#E1F5EE', '#0F6E56', '#085041'),
      'code': ('#F1EFE8', '#5F5E5A', '#444441'),
    },
  },
  'dark': {
    'heading': '#D3D1C7',
    'arrow': '#B4B2A9',
    'box_fill': '#2C2C2A',
    'box_stroke': '#888780',
    'title': '#F1EFE8',
    'subtitle': '#B4B2A9',
    'lanes': {
      'human': ('#26215C', '#AFA9EC', '#CECBF6'),
      'model': ('#04342C', '#5DCAA5', '#9FE1CB'),
      'code': ('#2C2C2A', '#B4B2A9', '#D3D1C7'),
    },
  },
}

TOP = 34  # room above the lanes for the column headings
COLUMNS = ((118, 'The data'), (268, 'The CLI'), (418, 'Chat'), (568, 'The eval'))
LANES = (
  ('human', 40, 100, 'Human'),
  ('model', 170, 100, 'Model (Claude)'),
  ('code', 300, 230, 'Code'),
)
BOXES = (
  (52, 72, 132, 'Edits the data', 'as printed, audits', False),
  (202, 72, 132, 'Asks the CLI', 'no model', False),
  (352, 72, 132, 'Asks in chat', 'Claude Code, MCP', False),
  (502, 72, 132, 'Runs the eval', 'writes, reviews', False),
  (52, 202, 110, 'Reviews data', 'optional, drafts', True),
  (352, 202, 132, 'Claude in chat', 'resolves, plans', False),
  (502, 202, 110, 'Eval model', 'as judge too', False),
  (52, 332, 132, 'Load + extract', 'schema, claims', False),
  (202, 332, 132, 'CLI', 'phylohist &lt;tool&gt;', False),
  (352, 332, 132, 'MCP server', 'tools and plan', False),
  (502, 332, 132, 'Eval runner', 'grader, scripts', False),
  (52, 440, 120, 'claims/', 'committed table', False),
  (202, 440, 432, 'Tools over the claim table', 'store, resolve, words, blocks, render', False),
)
# (x1, y1, x2, y2, two-headed)
ARROWS = (
  (107, 138, 107, 192, True),
  (107, 268, 107, 322, True),
  (176, 128, 176, 322, False),
  (268, 128, 268, 322, False),
  (418, 128, 418, 192, False),
  (418, 258, 418, 322, False),
  (630, 128, 630, 322, False),
  (557, 268, 557, 322, True),
  (118, 388, 118, 430, False),
  (268, 388, 268, 430, False),
  (418, 388, 418, 430, False),
  (568, 388, 568, 430, False),
  (172, 468, 192, 468, False),
)
HEIGHT = 550 + TOP


def draw(palette):
  p = palette
  parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="680" height="{HEIGHT}" '
    f'viewBox="0 0 680 {HEIGHT}" role="img" aria-labelledby="t d">',
    '<title id="t">How phylohist fits together</title>',
    '<desc id="d">Three lanes, human, model and code, read in four columns: the data, the '
    'CLI, chat and the eval. The human edits the data and the model optionally reviews it, '
    "each reviewing the other's work, while code validates both. The CLI has no model in the "
    'lane. In chat the model resolves names and states a plan that the MCP server executes. In '
    'the eval the runner drives the model, which also judges the header, while the human writes '
    'and reviews the eval. Every surface sits on the same tools over the claim table.</desc>',
    '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" '
    'markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" '
    f'stroke="{p["arrow"]}" stroke-width="1.5" stroke-linecap="round" '
    'stroke-linejoin="round"/></marker></defs>',
    '<style>',
    f'text{{font-family:{FONT};text-anchor:middle;dominant-baseline:central}}',
    f'.th{{font-size:14px;font-weight:500;fill:{p["title"]}}}',
    f'.ts{{font-size:12px;fill:{p["subtitle"]}}}',
    '.tl{font-size:14px;font-weight:500;text-anchor:end}',
    f'.tc{{font-size:14px;font-weight:500;fill:{p["heading"]}}}',
    '</style>',
  ]
  for cx, name in COLUMNS:
    parts.append(f'<text x="{cx}" y="18" class="tc">{name}</text>')
  for lane, y, h, label in LANES:
    fill, stroke, text = p['lanes'][lane]
    parts.append(
      f'<rect x="40" y="{y + TOP}" width="600" height="{h}" rx="16" fill="{fill}" '
      f'stroke="{stroke}" stroke-width="0.75"/>'
      f'<text x="612" y="{y + TOP + 18}" class="tl" fill="{text}">{label}</text>'
    )
  for x, y, w, title, sub, dashed in BOXES:
    y += TOP
    dash = ' stroke-dasharray="4 3"' if dashed else ''
    parts.append(
      f'<rect x="{x}" y="{y}" width="{w}" height="56" rx="8" fill="{p["box_fill"]}" '
      f'stroke="{p["box_stroke"]}" stroke-width="0.75"{dash}/>'
      f'<text x="{x + w / 2}" y="{y + 18}" class="th">{title}</text>'
      f'<text x="{x + w / 2}" y="{y + 37}" class="ts">{sub}</text>'
    )
  for x1, y1, x2, y2, both in ARROWS:
    start = ' marker-start="url(#arrow)"' if both else ''
    parts.append(
      f'<line x1="{x1}" y1="{y1 + TOP}" x2="{x2}" y2="{y2 + TOP}" stroke="{p["arrow"]}" '
      f'stroke-width="1.5"{start} marker-end="url(#arrow)"/>'
    )
  parts.append('</svg>')
  return '\n'.join(parts) + '\n'


def main():
  (OUT / 'architecture.svg').write_text(draw(PALETTES['light']))
  (OUT / 'architecture-dark.svg').write_text(draw(PALETTES['dark']))
  print('-> docs/architecture.svg, docs/architecture-dark.svg')


if __name__ == '__main__':
  main()
