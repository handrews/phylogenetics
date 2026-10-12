"""`scripts/expected_warnings.py` keeps the expected-warnings file to the
warnings the load still produces: a stale line goes on every run, a new
one is added only with `--add`, and nothing is written when the load logs
an error."""

import logging

import pytest

from phylohist import regenerate
from tests import support

script = support.script('expected_warnings')


def _fake_load(*messages, errors=0):
  def load(**_):
    logger = logging.getLogger('phylohist.loader.taxa')
    for message in messages:
      logger.warning(message)
    for n in range(errors):
      logger.error(f'error {n}')
    return {}, {}

  return load


@pytest.fixture
def expected(tmp_path):
  path = tmp_path / 'expected-warnings.txt'
  regenerate.write_expected({'kept', 'stale'}, path)
  return path


def test_a_stale_line_goes_and_a_new_one_waits(monkeypatch, expected, capsys):
  monkeypatch.setattr(script, 'load', _fake_load('kept', 'new'))
  assert script.main(['--file', str(expected)]) == 0
  assert regenerate.read_expected(expected) == {'kept'}
  assert expected.read_text().startswith(regenerate.EXPECTED_HEADER)
  out = capsys.readouterr().out
  assert '1 stale expected warnings removed' in out
  assert '1 new warnings not expected; add them with --add' in out


def test_add_takes_the_new_lines(monkeypatch, expected):
  monkeypatch.setattr(script, 'load', _fake_load('kept', 'new'))
  assert script.main(['--add', '--file', str(expected)]) == 0
  assert regenerate.read_expected(expected) == {'kept', 'new'}


def test_an_error_in_the_load_leaves_the_file(monkeypatch, expected, capsys):
  monkeypatch.setattr(script, 'load', _fake_load('kept', errors=1))
  before = expected.read_text()
  assert script.main(['--file', str(expected)]) == 1
  assert expected.read_text() == before
  assert '1 errors while loading' in capsys.readouterr().err
