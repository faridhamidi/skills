---
name: ptm
description: "Use PTM when writing, reviewing, or adopting high-assurance tests for state-changing systems: falsification intent tags, oracle meta-tests, anomaly/recovery tests, architecture-boundary gates, defensive branches, and ratchets."
---

# Popperian Testing Methodology

PTM is falsification-first testing. Each test tries to break a belief, names that belief, proves its oracle can fail, and gates the seam that could otherwise drift.

Use PTM as a hard gate for control planes, data mutation, recovery/self-healing, governance tooling, and automation that changes external state. For prototypes, UI glue, and small scripts, use it as a checklist.

The smell is not "needs more tests." The smell is "a false belief could survive": a retry half-writes state, a scanner never catches its forbidden import, a fake accepts impossible writes, a boundary can be bypassed, or a test says what happens without saying what it falsifies.

## Hard-Gate Non-Negotiables

These are mandatory for control planes, data mutation, recovery/self-healing, governance tooling, and external-state automation.

- Every new or changed test declares exactly one intent tag: `Falsifies:`, `Regresses:`, or `Confirms:`.
- Falsification is the default for any sharp contract, decision, invariant, seam, or failure path.
- Any assertion helper, invariant helper, scanner, or oracle you add gets a known-bad meta-test proving it fails.
- Every external seam gets at least one fault-injection test. Every retry, recovery, or multi-step failure path gets an anomaly test.
- Every protected architecture seam gets the three-layer boundary pattern: scanner, explicit manifest, scanner meta-tests plus real-file enforcement.
- Tests must not hit real network, database, cloud SDK, clock, or filesystem services when a unit-level seam exists; use small stateful fakes that enforce the real contract.
- Run the relevant tests and gates before claiming done.

## Workflow

1. Discover the repo's current test posture.
   Completion criterion: the test runner, test directories, existing intent-tag convention, boundary scanners, coverage gates, and spec-ID style are known from the repo itself.

2. Classify the behavior before writing the test.
   Completion criterion: you have chosen one intent, one target, and one generation strategy from the axes below, and the choice matches the behavior rather than the implementation.

3. Write one vertical test slice.
   Completion criterion: the next test is red for the intended reason, names observable behavior through a public interface, and does not depend on private structure.

4. Make the slice green with minimal implementation.
   Completion criterion: the new test passes, no speculative behavior was added, and existing relevant tests still pass.

5. Add PTM obligations triggered by the slice.
   Completion criterion: every triggered oracle meta-test, seam fault injection, anomaly loop, defensive-branch bypass, boundary scanner, ratchet, or gate update has been handled.

6. Refactor only while green.
   Completion criterion: tests remain green after each refactor step, and test names still describe behavior rather than implementation.

7. Verify before done.
   Completion criterion: relevant unit/integration tests, G-BRANCH for pure decision modules, G-BOUNDARY for architectural seams, and any ratchets touched by the change have passed or their failures are reported.

## The Axes

Every PTM test chooses one value from each axis.

| Axis | Question | Values |
| --- | --- | --- |
| Intent | Why does this test exist? | Falsification, Regression, Confirmation |
| Target | What property is asserted? | Decision-table oracle, invariant, contract/schema, architecture boundary, concurrency-safety |
| Generation | How are inputs produced? | Single example, parametrized, exhaustive cross-product, boundary-value, fault injection, anomaly |

Use [intent-tags.md](intent-tags.md) when choosing or wording an intent tag.

## Decision Recipe

- Pure decision: use a decision-table oracle, `Falsifies:`, cross-product or boundary-value inputs, and enroll it in G-BRANCH.
- Invariant: add or extend an `assert_*` helper, call it from behavior tests, and meta-test it with known-bad input.
- Contract: pair acceptance with a falsifier proving unknown fields, wrong types, or missing required values fail closed.
- Boundary: use the architecture-boundary pattern; exempt only the sanctioned adapter and meta-test the scanner.
- Optimistic concurrency or racing writers: test against a stateful fake/model that enforces the storage contract, plus fault injection on the conflict path.
- Recovery: use Method A anomaly testing; write the permanent fail-closed case before implementing retry logic.
- Defensive branch: mark it `# DEFENSIVE` and add Method B bypass coverage in the same change.
- Blast radius: prove fields you must not touch are conserved, with an explicit diff/report where useful.
- Wiring, UI, or glue: `Confirms:` is acceptable, but still fault-inject any external call.

Read [anomaly-testing.md](anomaly-testing.md), [defensive-branches.md](defensive-branches.md), [architecture-boundaries.md](architecture-boundaries.md), or [ratchets-and-gates.md](ratchets-and-gates.md) only when their trigger appears.

## Adoption

When adopting PTM in a repo, do not rewrite the suite. Add green-on-arrival ratchets that may only tighten. Use [adoption.md](adoption.md) for the checklist.
