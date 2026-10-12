import copy
import logging
import os
import sys

import coloredlog


class ColourHandler(coloredlog.ConsoleHandler):
  """`coloredlog` writes its colour codes into the record it is given, and
  every handler after it then sees them: a collector comparing messages
  with the expected warnings, pytest's caplog. This colours a copy."""

  def emit(self, record):
    super().emit(copy.copy(record))


_phylohist_logger = logging.getLogger(__name__)
_log_formatter = logging.Formatter(
  '%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s',
)
_log_handler = (
  ColourHandler(stream=sys.stderr)
  if sys.stderr.isatty() or os.getenv('PHYLOHIST_COLOR') == '1'
  else logging.StreamHandler()
)
_log_handler.setFormatter(_log_formatter)
_phylohist_logger.addHandler(_log_handler)
_phylohist_logger.setLevel(logging.INFO)

logger = _phylohist_logger
