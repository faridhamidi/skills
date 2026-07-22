# Method B: Defensive Branches

Use Method B for branches that are unreachable in normal operation only because an upstream layer is supposed to protect them.

Mark the branch with `# DEFENSIVE` and add a bypass test in the same change. A defensive branch without a bypass test is indistinguishable from dead code.

## Marking Convention

```python
# DEFENSIVE: the service layer always supplies a write_token for protected writes.
# Unreachable in normal operation; fires loud if a refactor bypasses the service.
if write_token is None and target == PROTECTED:
    raise ValueError(f"{target} write requires a write_token")
```

## Bypass Test Shape

```python
def test_adapter_rejects_protected_write_without_token():
    """Falsifies: 'the adapter guard can be removed without any test failing'.
    Defensive-branch coverage: bypasses the service to hit the lower-layer guard.
    spec: INV-ARCH-TOKEN
    """
    adapter = Adapter(client=FakeClient())

    with pytest.raises(ValueError, match="requires a write_token"):
        adapter.commit(PROTECTED, records=[...], expected=None, write_token=None)
```

If the only way to reach a branch is to lie to the function, it is probably a defensive branch.

