# The test corpus

A frozen copy of `data/` for the tests: the seven record files and the
trees, as they stood at commit 34f21b5 (main, 11 October 2026). It is
not resynced with `data/`, since the tests must not depend on what the
curated data says today. Edit it only to add the case a test needs or to
migrate it alongside a schema change, and keep it loading with no error.

`tests/conftest.py` loads it once per session (the `corpus` fixture),
writes its claim table to a temporary directory, and gives every test
the registries as that load left them. To see the claims it yields, or
to check a draft against it:

    poetry run python scripts/claims.py --data tests/corpus --out /tmp/corpus-claims
    poetry run python scripts/check_draft.py --data tests/corpus some-draft.yaml

`data/time.yaml` is not copied; nothing reads it.
