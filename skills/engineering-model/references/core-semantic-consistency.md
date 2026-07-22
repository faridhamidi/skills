# Semantic Consistency

## Purpose

This optional Core Hygiene reference helps a repository name system language only after that language becomes load-bearing. It is not a required schema, ontology, registry, or runtime framework.

Use it when repeated or interacting terms make behavior difficult to reconstruct from local code alone. Keep a concept local when one function, type, or direct test remains clearer.

## Diagnostic categories

A system may need to name some of these categories:

- **Entity and state** — what the system acts on and which conditions materially change behavior.
- **Action** — the operation the system performs.
- **Transition** — which state changes are legal or expected.
- **Reason** — why a decision, refusal, or result occurred.
- **Outcome** — what happened in a stable machine-readable form.
- **Recovery** — how retry, repair, or restoration differs from ordinary execution.

A compact diagnostic is:

> An action affects an entity, may move it between states, occurs for a reason, produces an outcome, and may have a recovery path.

Not every repository needs every category. Absence is valid when a concept has not become shared, ambiguous, or behaviorally significant.

## When a declaration is earned

Name a concept once when it begins to influence several call sites, APIs, logs, tests, operator views, or validation paths. A useful declaration should remain:

1. **Single-sourced** — one owner defines the vocabulary.
2. **Behaviorally locked** — tests prove the declaration agrees with implementation.
3. **Derived where practical** — validation, logging, documentation, or presentation reads from the declaration instead of recreating it.

Do not create a complete catalog in anticipation of future complexity. Start with the term or relationship already causing branching, ambiguity, repetition, or ownership confusion.

## Enforcement progression

Use the lightest mechanism that protects the actual seam:

```text
local concept
    -> direct behavioral test
    -> structural ratchet
    -> repository conformance harness
```

A direct test is the default. Escalate to the [`Repository Conformance Harness`](CONFORMANCE_HARNESS.md) only when several stable semantic rules need shared discovery, lifecycle, ownership, ratchets, or audit aggregation.

## Agent procedure

For a meaningful change, an agent should determine:

1. whether shared system language changed;
2. whether the change remains local or requires a direct Core check;
3. whether an existing harness rule or rationale reference must be updated;
4. whether the change alters permission for a consequential shared or external effect.

Report the result in the change summary:

```text
Semantic impact: none | local | shared
Enforcement: none | direct test | harness rule
Authority impact: none | governed review required
```

Agents may maintain declarations and evidence that mirror approved behavior. They must not silently redefine who may authorize or perform a consequential effect.

## Governed boundary

Naming an initiator, execution mode, or condition is ordinary Core Hygiene when it improves legibility or testing. Route to the [Governed Automation adoption check](../governed-automation/ADOPTION_CHECK.md) when actor identity, policy applicability, evidence, or operating conditions determine whether a consequential shared or external effect is permitted.

Core declarations describe and test semantics. Governed Automation owns authority-bearing control selection, authorization, and recovery constraints.