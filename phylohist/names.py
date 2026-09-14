"""Folding printed names to lookup forms.

G10 in `notes/development/semantics-roadmap.md`: ligatures, capitals, diacritics,
hyphens and spaces are typographical variation, not spelling, and a
resolver folds them on lookup while the records keep what was entered.
Folding is for finding a record; it never changes a key or a name.
"""

import re
import unicodedata

_LIGATURES = (('æ', 'ae'), ('œ', 'oe'), ('ß', 'ss'))
_UMLAUTS = (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'))
_SEPARATORS = re.compile(r'[\s\-_.]+')


def fold(text):
  """Lowercase, ligatures expanded, diacritics dropped, separators removed."""
  text = text.lower()
  for ligature, plain in _LIGATURES:
    text = text.replace(ligature, plain)
  text = unicodedata.normalize('NFKD', text)
  text = ''.join(ch for ch in text if not unicodedata.combining(ch))
  return _SEPARATORS.sub('', text)


def fold_forms(text):
  """Every folded form a printed name can take.

  A German umlaut in a name published before 1985 becomes ue/oe/ae, other
  diacritics are dropped (G10), and which rule the data entry followed is
  not visible in the query, so both forms are tried.
  """
  forms = {fold(text)}
  lowered = text.lower()
  for umlaut, expansion in _UMLAUTS:
    lowered = lowered.replace(umlaut, expansion)
  forms.add(fold(lowered))
  return forms


def key_stem(key):
  """The name part of a record key: before the authority suffix."""
  return key.split('_', 1)[0]
