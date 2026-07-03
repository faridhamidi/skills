# Intent Tags

Every test declares exactly one intent tag in a docstring unless a file-level `Test philosophy: Popperian` banner makes `Falsifies:` the default for that file.

## `Falsifies:`

Use for the house default: a belief that must not hold.

Good shape:

```python
def test_unknown_fields_are_rejected():
    """Falsifies: 'wire input can add unknown fields without being rejected'.
    spec: INV-SCHEMA-UNKNOWN
    """
```

Reach for `Falsifies:` when there is a decision table, invariant, contract, seam, retry path, boundary, concurrency rule, fail-closed behavior, or negative test.

## `Regresses:`

Use for a specific past bug that must not return.

Good shape:

```python
def test_empty_token_no_longer_grants_access():
    """Regresses: 'empty auth token was accepted as an admin token'.
    spec: INV-AUTH-EMPTY-TOKEN
    """
```

A regression test is a falsification whose belief is "the old bug is back."

## `Confirms:`

Use for wiring, UI flow, smoke checks, or glue where there is no sharp property to refute.

Good shape:

```python
def test_user_can_open_settings_panel():
    """Confirms: 'the settings panel is reachable from the account menu'."""
```

If `Confirms:` is the only coverage of a real decision, treat that as a smell and find the falsifiable property.

## Spec IDs

When a behavior is governed by a spec, cite the stable ID in the docstring. Universal starter prefixes: `INV-` for invariants and `CONC-` for concurrency. Add short domain prefixes only when the repo already uses or needs them.

