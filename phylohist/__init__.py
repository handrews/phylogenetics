import logging
import collections

# AI code
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

  def get_counts(self):
    """
    Returns a dictionary of log level counts.
    """
    return dict(self.counts)

LEVEL = logging.INFO
log_counter = LevelCountHandler()
log_counter.setLevel(LEVEL)
logger = logging.getLogger(__name__)
logger.setLevel(LEVEL)
logger.addHandler(log_counter)
logger.setLevel(LEVEL)

class L():
  error_count = 0
  warn_count = 0
  def error(self, message):
    self.error_count += 1
    if LEVEL <= logging.ERROR:
      print(f'*** ERROR: {message}')
  def warn(self, message):
    self.warn_count += 1
    if LEVEL <= logging.WARNING:
      print(f'*** WARNING: {message}')
  def info(self, message):
    if LEVEL <= logging.INFO:
      print(f'*** INFO: {message}')
  def debug(self, message):
    if LEVEL <= logging.DEBUG:
      print(f'*** DEBUG: {message}')
