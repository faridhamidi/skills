# Starting Foundation

## Purpose

A new codebase should be easy to understand, test, and diagnose before it becomes large enough to demand those properties.

The foundation is not a framework or a required folder layout. It is a small set of steering constraints that prevent important boundaries from disappearing into incidental code.

## The three constraints

### 1. Name the boundaries

Keep decision logic separate from code that talks to databases, cloud APIs, queues, files, clocks, or user interfaces.

A boundary may be a protocol, function parameter, small wrapper, or module seam. Use the lightest mechanism that makes these questions answerable:

- Which code decides?
- Which code performs the external effect?
- Which component owns the mutation?
- Can the decision be tested without the external system?

Do not introduce an interface for every function. Add a boundary where an external dependency, irreversible effect, authority change, or difficult test seam appears.

### 2. Declare the system's important language

Important states, actions, outcomes, reasons, and recovery levels should be named in one place once they begin influencing behavior across several call sites.

A useful declaration has three properties:

1. **Single source** — the vocabulary is declared once rather than recreated in conditionals.
2. **Behavioral lock** — tests prove the declaration agrees with the implementation.
3. **Derived use** — validation, gating, logging, documentation, or operator presentation is derived from the declaration where practical.

Start with the vocabulary that is already causing branching or ambiguity. Do not design a complete ontology before the system earns it. See [`SEMANTIC_CONSISTENCY.md`](SEMANTIC_CONSISTENCY.md) when repeated or interacting system language needs a more explicit Core treatment.

### 3. Preserve execution context across every hop

Every remote or asynchronous boundary should carry enough context to reconstruct one operation end to end.

At minimum, use stable identifiers and structured fields consistently across:

- API calls;
- queue messages;
- scheduled jobs;
- event payloads;
- background workers;
- logs and status records.

Distributed tracing is optional. Traceability is not. A later tracing system can only connect work cleanly if the propagation seams already exist.

## Enforcement

A foundation that exists only in prose will decay.

Add small tests or static checks for the boundaries that matter most, such as:

- external clients may be constructed only in designated modules;
- core decision modules cannot import provider SDKs;
- one component owns a particular irreversible mutation;
- declared actions and outcomes remain synchronized with behavior;
- correlation fields are propagated across known hops.

When a boundary cannot be completed immediately, lock the current violation set so it cannot grow. Improve it later without allowing regression in the meantime.

## Enforcement escalation

Use the lightest mechanism that protects the actual seam:

```text
Level 1 — direct test
Level 2 — structural ratchet
Level 3 — manifest-backed conformance harness
Level 4 — protected admission or authority control
```

### Level 1 — direct test

Use one small executable test for a real boundary.

### Level 2 — structural ratchet

When a valid boundary has existing violations, enumerate the current set, fail on growth, shrink it as cleanup lands, and convert to zero violations when complete.

### Level 3 — manifest-backed conformance harness

Escalate when several rules need stable identifiers, common discovery, lifecycle, ratchet state, ownership declarations, paired evidence, historical lineage, and audit aggregation. See [`CONFORMANCE_HARNESS.md`](CONFORMANCE_HARNESS.md).

### Level 4 — protected admission or authority control

Repository-host controls govern actual merge admission. If an automated actor can add or weaken blocking rules, approve itself, merge, deploy, override failed checks, or mutate shared systems, complete the [Governed Automation adoption check](../governed-automation/ADOPTION_CHECK.md).

## Proportional adoption

The smallest useful starting point may be:

```text
src/
  decisions.py
  service.py
  integrations.py
  entrypoint.py

tests/
  test_decisions.py
  test_boundaries.py
```

The names do not matter. The separation does.

A larger system may later split into domain, application, adapters, and entrypoints. That structure should emerge from real pressure rather than being copied in advance.

## Foundation checklist

Before the first substantial feature lands, answer:

- What decisions belong to the system rather than an external provider?
- What external effects exist, and where are they allowed?
- Which mutations require a single owner?
- Which states, actions, and outcomes are already shared vocabulary?
- What identifier follows one operation through all remote or asynchronous hops?
- Which two or three tests would prevent the architecture from silently collapsing?

The objective is not architectural purity. It is to make the codebase difficult to misunderstand and cheap to change.

## Executable witness

The dependency-free [`core_boundaries_python`](../examples/core_boundaries_python/) specimen demonstrates three claims from this document: decision code remains independent of an external client, client construction is confined to one integration module, and an operation identifier crosses the service boundary. Its tests are examples of executable constraints, not a required project layout.