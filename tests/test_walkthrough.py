"""The walkthrough's answers are what the code renders.

`docs/walkthrough.md` pastes, for each plan file under `docs/walkthrough/`,
the answer the plan renders; this test renders each plan and looks for
the text, so the page cannot drift from the code, and checks that every
plan file is the page's.
"""

import os
import pathlib

import pytest
import yaml

from phylohist import plan
from phylohist.render import render_composition

pytestmark = pytest.mark.skipif(
  bool(os.getenv('PHYLOHIST_DRAFTS')),
  reason='the committed claim table covers data/ only',
)

DOCS = pathlib.Path(__file__).parent.parent / 'docs'
PLANS = sorted((DOCS / 'walkthrough').glob('*.yaml'))
PAGE = ' '.join((DOCS / 'walkthrough.md').read_text().split())


@pytest.mark.parametrize('path', PLANS, ids=[p.stem for p in PLANS])
def test_answer_is_what_the_plan_renders(path):
  outcome = plan.execute(yaml.safe_load(path.read_text()))
  assert outcome['errors'] == []
  rendered = ' '.join(render_composition(outcome['composition'], 'text').split())
  assert rendered in PAGE, f'{path.name}: the walkthrough does not show what it renders'
  assert path.name in PAGE


def test_every_plan_is_on_the_page():
  assert len(PLANS) == 5
