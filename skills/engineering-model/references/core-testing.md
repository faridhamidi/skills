# Testing

This document belongs to the Core Hygiene Layer. It describes how to state and challenge engineering claims; it does not require governed-automation machinery.

## Three independent axes

Classify a test by **intent**, **target**, and **input generation**. These axes communicate more than labels such as unit or integration test.

## Axis A — intent

### Falsification

State a belief that must not hold, then construct a case that would expose it.

Examples:

- a parser silently accepts malformed input;
- a retry duplicates a completed effect;
- a stale update overwrites newer state;
- a module bypasses a designated integration seam.

### Regression

Pin a defect that previously escaped. A regression test is falsification with a known historical hypothesis: the old bug has returned.

### Confirmation

Demonstrate an intended happy path. Confirmation is useful for wiring and ordinary behavior, but it should not be the only evidence for a costly failure mode.

## Axis B — target

### Decision table or oracle

Encode the expected input-to-outcome mapping independently of the implementation. Use this when a finite set of conditions produces classified results.

### Invariant

Assert a property that must survive many operations:

- **conservation** — one operation cannot alter state outside its ownership;
- **determinism** — equal inputs produce equal outputs;
- **idempotency** — repeating completed work creates no additional effect;
- **safe refusal** — missing or ambiguous required input does not produce an unsafe action.

Test the oracle or invariant helper with known-bad data. An assertion that cannot fail creates false confidence.

### Contract and schema

Test both acceptance and rejection:

- valid records are accepted;
- missing, malformed, and unknown fields are rejected.

Pair allowlist tests with a falsifier proving the boundary did not become permissive.

### Structural boundary

Inspect imports, calls, or source structure to prove that a required seam is not bypassed.

Examples:

- external clients are constructed only in designated integration modules;
- decision modules do not import provider SDKs or perform network access;
- presentation code does not become a decision input;
- one module owns a fragile or irreversible external effect.

Structural tests are executable constraints, not style preferences.

### Concurrency safety

Drive stale tokens and racing writers against a stateful backing-store model. Prove that lost updates are rejected and atomicity is preserved where the risk exists.

## Axis C — input generation

Choose how cases are obtained:

- single example;
- parametrized matrix;
- exhaustive finite cross-product;
- boundary values;
- fault injection;
- anomaly sequence, such as failure at step N followed by retry.

Use fault injection and anomaly sequences in proportion to the cost of partial or duplicated work.

## Complete test description

A useful review sentence names all three axes:

> A falsification test of an idempotency invariant using a failure-then-retry anomaly sequence.

## Selecting priorities

Prioritize tests by the cost of being wrong:

1. decisions or transformations whose incorrect result is hard to detect;
2. data ownership and schema boundaries;
3. retries, concurrency, and partial failure;
4. external seams whose failure changes behavior;
5. regressions for escaped defects;
6. seeded bad examples proving important oracles can fail.

Do not copy test counts, naming ceremonies, or coverage thresholds without identifying the risk they control.

## Foundation checks

A new repository usually needs only a few structural checks:

- decision code remains independent of provider clients;
- external clients have designated construction points;
- important mutations have named owners;
- declared terms stay synchronized with consuming behavior;
- known asynchronous hops carry required correlation fields.

### Ratchet incomplete boundaries

When an existing boundary cannot be completed immediately:

1. enumerate the known violation set;
2. fail if a new violation appears;
3. shrink the allowed set as cleanup lands;
4. convert the ratchet to a zero-violation rule when complete.

## Test the checker

For an important architectural rule, test both the repository and the mechanism claiming to protect it.

Each active rule in a conformance harness should declare:

```text
Rule ID:
Canonical rationale:
Lifecycle:
Enforcement mode:
Known violation set:
Checker adapter:
Positive conformance test:
Minimal falsifier:
Owners:
Ownership binding:
Approval-policy reference:
Evidence boundary:
```

The responsibilities are distinct:

- the **positive conformance test** proves the live repository satisfies the rule's declared mode;
- the **minimal falsifier** introduces one prohibited new violation and proves the intended rule rejects it;
- **generic fixture-driven tests** prove ratchet, lifecycle, ownership-binding, and audit mechanics once, independently of live rule identifiers.

Generic harness-engine tests use `FIXTURE.*` identifiers and must not depend on active repository-rule namespaces.

For a zero-violation rule, the positive test expects an empty prohibited set. For a ratcheted rule, it expects the observed set to equal the exact declared set.

A change that modifies a rule, checker, and falsifier must explain whether the protected architectural property changed. Weakening all three merely to restore a passing build is not conformance evidence.

## Minimal template

```text
Intent:
Target:
Generation strategy:
Belief being challenged:
Invariant or oracle:
Known-bad case proving the oracle:
External seams and injected faults:
Evidence boundary:
```

## Repository witness

The examples under [`../examples/`](../examples/) run in CI with the Python standard library. They demonstrate structural call-site checks, a manifest-backed conformance harness, runtime authority checks, fail-closed validation, idempotent reconciliation, and boundary ratchets. They are deliberately smaller than a reference application so the tested property remains visible.
