import re
import datetime
import pathlib
import logging

logger = logging.getLogger(__name__)

LIST_DIR = pathlib.Path(__file__).parent / '..' / 'notes' / 'lists'

RANKS = {
  'P': 'Phylum',
  'BP': 'Subphylum',
  'SC': 'Superclass',
  'C': 'Class',
  'BC': 'Subclass',
  'SO': 'Superorder',
  'O': 'Order',
  'BO': 'Suborder',
  'SF': 'Superfamily',
  'F': 'Family',
  'BF': 'Subfamily',
  'g': 'genus',
  'bg': 'subgenus',
  's': 'species',
  'bs': 'subspecies'
}

SPECIMENS = {
  'HT': 'holotype',
  'PT': 'paratype',
  'ST': 'plesiotype',
  'LT': 'lectotype',
  'YT': 'syntype',
  'OT': 'topotype',
  'TT': 'type?',
  'LC': 'latex cast',
}

FLAGS = {
  'N': 'new',
  'T': 'type',
  'Q': 'dubiuos',
  '?': 'parent dubious',
  'X': 'unclear',
}

def _parse_to_delim(line, delim, length_range=None):
  print(line)
  index = line.index(delim)
  token = line[0:index]
  if length_range is not None:
    assert len(token) in length_range
  else:
    assert len(token) > 0
  return token, line[index + len(delim):]

def _parse_authority(authority, year=None):

  if year is None:
    # In the treatise, there are never more than two authors,
    # and they are always separated by " & "
    year = authority[-4:]
    if year == '????':
      year = None
    else:
      year = int(year)
      assert year > 1700
      assert year <= datetime.datetime.now().year

  authority = authority[:-4].strip()

  second = None
  if '&' in authority:
    first, second = authority.split('&')
    first = first.strip()
    second = second.strip()
  else:
    first = authority.strip()

  return first, second, year

def convert(*files):
  data = {
    'authors': {},
    'sources': {},
    'taxa': {},
    'trees': {},
  }

  files = [
    LIST_DIR / 'only-treatise.txt',
    LIST_DIR / 'sprinkle.txt',
  ]

  for filename in files:
    print(filename)
    for line in (open(filename)):
      if line[0] == '#':
        continue

      if '#' in line:
        line, comment = line.split('#')
        comment = comment.strip()
      line = line.strip()

      indentation = re.match('( *)', line).group(0)
      print(len(indentation))
      line = line[len(indentation):]

      rank, line = _parse_to_delim(line, ' ', [1, 2])
      print(f'rank or specimen: {rank}')
      if rank in SPECIMENS:
        continue
      assert rank in RANKS, rank
      print(f'"{RANKS[rank]}"')

      flags = ''
      if ' ' in line:
        name, line = _parse_to_delim(line, ' ')
        assert line[0] == '('
        line = line[1:]
        if line.index(')') == len(line) - 1:
          authority = line[:-1]
        else:
          authority, flags = line.split(')')
          flags = flags.strip()
          print(f'flags: "{flags}"')

        assert ')' not in authority
        # Currently, "in" and "ex" never appear together
        in_first, in_second, in_year = None, None, None
        if ' in ' in authority:
          authority, in_publication = authority.split(' in ')
          in_first, in_second, in_year = _parse_authority(
            in_publication.strip()
          )
        ex_first, ex_second, ex_year = None, None, None
        if ' ex ' in authority:
          authority, ex_authority = authority.split(' ex ')
          ex_first, ex_second, ex_year = _parse_authority(
            ex_authority.strip()
          )
        first, second, year = _parse_authority(authority.strip(), in_year)
        print(f'First author: "{first}"')
        if second:
          print(f'Second author: "{second}"')
        print(f'Year: {year}')
        if in_first:
          print('  in:')
          print(f'    First author: "{in_first}"')
          if in_second:
            print(f'    Second author: "{in_second}"')
          print(f'   Year: {in_year}')
        if ex_first:
          print('  ex:')
          print(f'    First author: "{ex_first}"')
          if ex_second:
            print(f'    Second author: "{ex_second}"')
          print(f'   Year: {ex_year}')

      else:
        assert (line[0], line[-1]) == ('_', '_')
        name = None
      print(f'"{name}"')
      print('')
    print('------------------------------------------------')
    print('')
