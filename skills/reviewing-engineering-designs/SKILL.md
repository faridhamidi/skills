---
name: reviewing-engineering-designs
description: Use when reviewing ADRs, DDs, FDs, RFCs, architecture documents, engineering proposals, control planes, governed automation, implementations against accepted designs, or revisions intended to close prior architectural findings.
---

# Reviewing Engineering Designs

Treat a design as a set of falsifiable claims about authority, state, behavior, and operations. Determine whether its mechanisms can preserve the stated invariants under normal execution, failure, recovery, and change.

## Select the review mode

Choose one mode explicitly before analyzing:

1. **Design review** — Test the decision system expressed by the document. Do not present unimplemented mechanisms as repository truth.
2. **Implementation-conformance review** — Treat the accepted design as authority for intended behavior and repository/runtime evidence as authority for existing behavior. Report divergence; do not silently choose one source.
3. **Revision verification** — Re-run each original failure sequence against the changed artifact. Separate closed, partially closed, still open, and newly introduced findings. Do not accept edited prose or added tests as closure without testing the underlying mechanism.

If the required artifact, governing source, or revision is unavailable, narrow the verdict to the available evidence. Do not manufacture certainty from generic practice.

## Establish the evidence boundary

Resolve and state:

- target artifact, review mode, maturity, revision, and repository head when applicable;
- governing ADRs, decisions, vocabulary, invariants, interfaces, and prior findings;
- available code, tests, configuration, deployment wiring, policies, and runtime evidence;
- exclusions, conflicts between sources, and material unknowns.

Read referenced governing material before judging a dependent document. Preserve the requested scope; identify adjacent consequences without turning the review into an unsolicited redesign.

## Reconstruct the decision contract

Build a compact model before listing findings:

- problem, protected assets, actors, owners, trust boundaries, and authority boundaries;
- canonical source of truth, discovered inputs, derived state, and enforcement points;
- allowed actions and who may request, approve, execute, override, repair, and audit them;
- invariants: what must always happen and what must never happen;
- lifecycle and transitions across bootstrap, steady state, mutation, failure, recovery, migration, and retirement;
- completion boundary, non-goals, rejected alternatives, and accepted trade-offs.

Keep requested, approved, authoritative, executed, persisted, and observed state distinct. If the design collapses them, test the consequences.

## Trace consequential paths

Trace each load-bearing claim through:

`claim → mechanism → enforcement owner → durable evidence → verification → recovery`

Walk at least the normal path, the most damaging reachable failure path, and the recovery/re-entry path. For authority-bearing or destructive systems, also test missing, stale, malformed, duplicated, reordered, and contradictory inputs; concurrency; replay; timeout; throttling; dependency failure; partial success; and eventual consistency.

Determine whether each failure denies, permits, retries, queues, degrades, rolls back, or becomes indeterminate. “Fail closed,” “idempotent,” “atomic,” “auditable,” and “verified” are claims to prove, not assurances to repeat.

## Attack the architecture

Concentrate on consequential defects across these dimensions:

- **Semantic coherence:** precedence, terminology, lifecycle symmetry, state transitions, and claims stronger than mechanisms.
- **Authority and blast radius:** privilege, self-approval, bypass paths, shared-resource effects, irreversible actions, and mechanical separation of duties.
- **Failure and recovery:** commit ordering, conflict resolution, leases, retries, reconciliation, rollback, orphan handling, restore provenance, retention, and re-entry.
- **Evidence and operability:** distinguish intent recorded, action attempted, enforcement applied, and desired state verified; assess correlation, freshness, integrity, retention, alarms, ownership, and operator interpretation.
- **Implementation conformance:** inspect actual call paths, ports, policy evaluation order, persistence, exception handling, tests, IAM/resource policies, deployment wiring, and alternate mutation paths.
- **Proportionality and adoption:** complexity earned by authority and consequence, rollout blast radius, compatibility, quotas, latency, operator burden, exceptions, ownership cost, reversibility, and exit path.

Credit deliberate trade-offs when their consequences are explicit and bounded. Record falsification probes that held; they are evidence of strength, not ceremonial praise.

## Calibrate findings

Report only material issues. Derive severity from consequence, reachability, and affected scope.

Each finding must contain:

1. severity and concise title;
2. violated, contradictory, or unsupported contract claim;
3. exact document, code, test, or runtime evidence;
4. plausible failure sequence and operational impact;
5. smallest sufficient correction expressed as an invariant or decision, not speculative implementation detail;
6. acceptance test or evidence that would prove closure;
7. uncertainty or residual trade-off when material.

Classify missing evidence as missing evidence unless the artifact claims the mechanism exists. Do not promote taste, stylistic preferences, or fashionable patterns into findings.

## Produce the review

Use this order:

1. **Verdict** — approve, approve with required changes, revise, reject, or insufficient evidence; give the load-bearing reason and confidence boundary.
2. **Decision contract** — summarize only the reconstructed invariants and authority/state model needed to understand the verdict.
3. **Findings** — descending severity, each using the complete evidence-to-impact chain.
4. **Surviving probes** — mechanisms that resisted a plausible failure path, when relevant.
5. **Evidence boundaries and next verification** — unresolved unknowns and the smallest action that would materially change confidence.

Prefer a concise essay with restrained bullets. Use a table only when several claims, states, or revisions require exact comparison.

Do not summarize instead of testing, equate documentation with enforcement, use “best practice” as evidence, recommend generic hardening without a failure path, re-litigate settled choices without new evidence, or declare remediation complete without checking the changed artifact and regression surface.
