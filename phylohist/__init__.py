import sys
import os
import collections

import logging
import coloredlog


class LevelCountHandler(logging.StreamHandler):
  """
  A custom logging handler that counts log messages by level.
  """
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.counts = collections.defaultdict(int)

  def emit(self, record):
    """
    Increments the count for the given log record's level.
    """
    self.counts[record.levelname] += 1
    super().emit(record)

  def get_count(self, level):
    """
    Returns a dictionary of log level counts.
    """
    return self.counts[level]


class ColoredLevelCountHandler(coloredlog.ConsoleHandler, LevelCountHandler):
  pass


_phylohist_logger = logging.getLogger(__name__)
_log_formatter = logging.Formatter(
    '%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s',
)
_log_handler = (
    ColoredLevelCountHandler(stream=sys.stderr)
    if sys.stderr.isatty() or os.getenv('PHYLOHIST_COLOR') == '1'
    else LevelCountHandler()
)
_log_handler.setFormatter(_log_formatter)
_phylohist_logger.addHandler(_log_handler)
_phylohist_logger.setLevel(logging.INFO)

logger = _phylohist_logger
