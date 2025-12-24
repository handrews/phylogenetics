import sys
import os
import collections

import logging
import coloredlog


_phylohist_logger = logging.getLogger(__name__)
_log_formatter = logging.Formatter(
    '%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s',
)
_log_handler = (
    coloredlog.ConsoleHandler(stream=sys.stderr)
    if sys.stderr.isatty() or os.getenv('PHYLOHIST_COLOR') == '1'
    else LevelCountHandler()
)
_log_handler.setFormatter(_log_formatter)
_phylohist_logger.addHandler(_log_handler)
_phylohist_logger.setLevel(logging.INFO)

logger = _phylohist_logger
