# Method A: Anomaly Testing

Use anomaly testing for every retry, recovery, or multi-step failure path.

An anomaly test advances the failure point. Inject a failure at the Nth call to a seam, assert the system responds correctly, then advance N until the operation can complete without hitting the simulated failure.

Run two modes:

- Transient: failure heals after the injected calls. The operation completes and state is fully consistent.
- Permanent: failure continues indefinitely. The operation fails closed, returns the correct error, and leaves state identical to the pre-call snapshot.

No exception should escape the service boundary in either mode unless the public contract explicitly says it should.

## Sequencing

For retry/self-healing work, write the permanent fail-closed case before implementing retry logic. Then the transient cases go green when retry lands.

## Injection Hook

Keep the hook test-local unless the repo already has a shared equivalent.

```python
class _FailOnN:
    """Wrap a fake method to raise on attempts 1..raise_through, then delegate."""

    def __init__(self, original, raise_through, *, permanent=False, exc=None):
        self._original = original
        self._raise_through = raise_through
        self._permanent = permanent
        self._exc = exc or RuntimeError("injected transient failure")
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        if self.calls <= self._raise_through or (self._permanent and self.calls > 0):
            raise self._exc
        return self._original(*args, **kwargs)
```

## Matrix

| Scenario | `raise_through` | `permanent` | Expected |
| --- | --- | --- | --- |
| First attempt fails, then heals | 1 | False | Success, retry recovers |
| First two attempts fail, then heals | 2 | False | Success, retry recovers |
| All attempts fail | large | True | Fail closed, no state change |
| No failure | n/a | n/a | Covered by the baseline happy path |

For a retry budget of `k` extra attempts, parametrize transient over `raise_through in 1..k` and add one permanent exhaustion case.

## Test Shape

```python
import pytest


@pytest.mark.parametrize("raise_through", [1, 2])
def test_operation_recovers_after_transient_failure(raise_through):
    """Falsifies: 'a transient failure on <seam> aborts the operation'.
    Anomaly test: <seam> raises on attempts 1..raise_through, then heals.
    spec: INV-<AREA>-ANOMALY-1
    """
    svc, fake = make_service_under_test()
    fake.seam = _FailOnN(fake.seam, raise_through=raise_through)

    result = svc.do_operation(...)

    assert result.ok is True
    assert_state_is_fully_consistent(fake)
    assert fake.seam.calls == raise_through + 1


def test_operation_fails_closed_when_failure_is_permanent():
    """Falsifies: 'exhausting retries silently proceeds or corrupts state'.
    Anomaly test: every attempt raises.
    spec: INV-<AREA>-ANOMALY-2
    """
    svc, fake = make_service_under_test()
    before = snapshot_state(fake)
    fake.seam = _FailOnN(fake.seam, raise_through=10_000, permanent=True)

    result = svc.do_operation(...)

    assert result.ok is False
    assert result.error_code == "EXPECTED_FAIL_CLOSED_CODE"
    assert snapshot_state(fake) == before
```

