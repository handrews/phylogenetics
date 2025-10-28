from pathlib import Path
from collections import defaultdict
import re
import sys
import logging
import yaml

logger = logging.getLogger(__name__)

DTYPES = {
    'e': 'erratum',
    'p': 'published',
    'c': 'proceedings',
    'a': 'accepted',
    'v': 'revised',
    'x': 'pre-print',
    'r': 'received',
    's': 'submitted',
    'z': 'unknown',
}
RANKS = {
    'E': 'Clade',
    'G': 'Grade (Begin)',
    'Z': 'Grade (End)',
    'ZZ': 'Grade (End Branch)',
    'SP': 'Superphylum',
    'BSP': 'Clades',
    'P': 'Phylum',
    'BP': 'Subphylum',
    'SC': 'Superclass',
    'C': 'Class',
    'BC': 'Subclass',
    'IC': 'Infraclass',
    'PC': 'Parvclass',
    'SO': 'Superorder',
    'O': 'Order',
    'BO': 'Suborder',
    'IO': 'Infraorder',
    'PO': 'Parvorder',
    'SF': 'Superfamily',
    'F': 'Family',
    'BF': 'Subfamily',
    'g': 'Genus',
    'bg': 'Subgenus',
    's': 'Species',
    'X': 'outgroup',
}

text = (Path(__file__).parent / 'input.txt' ).read_text()
start = 0
i = start
section = False
paper = {}
tree = {}
level = -1
node_stack = []
needs_author = False
papers = []

lines = text.split('\n')[start:]
for line in lines:
    i += 1
    if needs_author:
        assert all(paper, not section, not tree, line)
        paper['authors'] = line.split('; ')
        needs_author = False

    elif line == '-----':
        assert (paper or i == 1) and not section, f'{i}: "{line}" ({section}, "{paper}")'
        section = True
        if paper and paper['trees']:
            papers.append(paper)
        paper = {}

    elif section and (m := re.match(
        r'(?P<date>\d\d\d\d-\d\d-\d\d)-(?P<dtype>[a-z]) (?P<title>.*)$',
        line,
    )):
        assert section and not paper
        paper = {
            'file': line,
            'title': m.group('title'),
            'date': m.group('date'),
            'date_type': DTYPES[m.group('dtype')],
            'authors': [],
            'trees': [],
        }
        # print(paper['file'])
        section = False

    elif paper and (m := re.match(r'TREE( (?P<note>.*))?$', line)):
        assert not tree
        # tree = {'parent': None, 'level': level, 'children': []}
        tree = {'level': level, 'children': []}
        if note := m.group('note'):
            tree['note'] = note
        node_stack = [tree]

    elif tree and line == '':
        assert len(tree['children']) == 1, f'line {i}'
        paper['trees'].append(tree['children'][0])
        level = -1
        tree = {}
        # print('...added tree')

    elif tree:
        m = re.match('( *)', line).group(1)
        if m is None:
            raise ValueError(f'Invalid tree line on line {i}: "{line}"')

        space = len(re.match('( *)', line).group(1))
        new_level = space // 2
        assert new_level >= 0

        entry = line[space:]
        node = {}

        if m := re.match(
            '(?P<rank>[A-Zbg][A-Zg]?)'
            '( '
                '(?P<name>[-\[\]"\w]+)'
                '( \((?P<modifier>(crown|total))\))?'
            ')?'
            '( (?P<note>.*))?$',
            entry,
        ):
            assert ((rank_code := m.group('rank')) is not None)
            modifier = m.group('modifier')
        elif m := re.match(
            '(?P<name>[-\[\]"\w]+ (\(\w+\) )?\w+\.?)( (?P<note>.*))?$',
            entry,
        ):
            rank_code = 's'
            modifier = None

        else:
            raise ValueError(f'Invalid tree entry on line {i}: "{entry}"')

        node['rank'] = RANKS[rank_code]
        if (name := m.group('name')) is not None:
            node['name'] = name
        if modifier is not None:
            node['modifier'] = modifier
        if (note := m.group('note')) is not None:
            node['note'] = note
        node['level'] = new_level
        node['children'] = []

        if new_level == level:
            assert node_stack[-1]['level'] == new_level
            found = False
            for n in reversed(node_stack):
                if n['level'] == new_level - 1:
                    n['children'].append(node)
                    found = True
            assert found, f'{i}: {line}'
            # node['parent'] = node_stack.pop()['parent']
            node_stack.append(node)

        elif new_level < level:
            while node_stack[-1]['level'] > new_level -1:
                node_stack.pop()
            # node['parent'] = node_stack[-1]
            node_stack[-1]['children'].append(node)
            node_stack.append(node)

        elif new_level == level + 1:
            assert node_stack[-1]['level'] == level
            # node['parent'] = node_stack[-1]
            node_stack[-1]['children'].append(node)
            node_stack.append(node)

        else:
            assert False, \
                   f'New level {new_level} discontinuous with {level} on line {i}: "{line}"'

        level = new_level

yaml.dump(papers, sys.stdout, indent=2, sort_keys=False, allow_unicode=True)
#print(json.dumps(papers, indent=2, ensure_ascii=False))
