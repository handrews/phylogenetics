"""Matching an eval selector against a claim.

A selector is a subset of a claim: every key present with an equal value,
nested dicts matched the same way, lists compared element by element.
"""


def matches(selector, value):
  if isinstance(selector, dict):
    return isinstance(value, dict) and all(
      key in value and matches(sub, value[key])
      for key, sub in selector.items()
    )
  if isinstance(selector, list):
    return (
      isinstance(value, list) and len(value) == len(selector) and
      all(matches(a, b) for a, b in zip(selector, value))
    )
  return selector == value
