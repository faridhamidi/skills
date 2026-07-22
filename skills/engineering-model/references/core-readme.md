# Core Hygiene Layer

Adopt this layer independently. It is intended for any non-trivial operational codebase, including tools that do not encode governance or mutate shared infrastructure.

## What it provides

- [`FOUNDATION.md`](FOUNDATION.md) — name meaningful boundaries, declare important system language, and preserve execution context.
- [`SEMANTIC_CONSISTENCY.md`](SEMANTIC_CONSISTENCY.md) — optionally name shared states, actions, transitions, reasons, outcomes, and recovery semantics when local code and direct tests stop being sufficient.
- [`TESTING.md`](TESTING.md) — classify tests by intent, target, and input generation; use small structural checks to stop boundary decay.
- [`DOCUMENTATION.md`](DOCUMENTATION.md) — separate non-binding direction, worked implementation plans, and durable decisions.
- [`../examples/core_boundaries_python/`](../examples/core_boundaries_python/) — a dependency-free executable witness for boundary and context-propagation checks.

## Minimum adoption

A small repository should be able to answer:

1. Where do decisions happen?
2. Where are external effects allowed?
3. Which terms influence behavior across multiple call sites?
4. What identifier follows one operation through remote or asynchronous work?
5. Which two or three tests prevent the structure from collapsing?

No prescribed folder layout is required. A function parameter, wrapper, module seam, or protocol is enough when it makes ownership and testing clear.

## Optional escalation

Use [`SEMANTIC_CONSISTENCY.md`](SEMANTIC_CONSISTENCY.md) when repeated or interacting system language has become load-bearing. Keep direct tests as the default until several stable semantic or structural rules need common discovery and lifecycle.

When several structural constraints have stable identities, multiple contributors depend on them, or architectural intent is repeatedly reconstructed, consider escalating direct checks into a [`Repository Conformance Harness`](CONFORMANCE_HARNESS.md).

This mechanism is optional. It adds rule lifecycle, ratchets, ownership binding, historical lineage, generic engine tests, and audit reporting. Do not adopt it when two or three direct tests remain clearer.

## What this layer does not imply

Using the core layer does not mean the system needs:

- staged and canonical state;
- an approval workflow;
- a reconciliation loop;
- a dedicated recovery component;
- a governance vocabulary;
- distributed tracing infrastructure.

Those mechanisms belong only where the problem earns them. See the [Governed Automation Layer](../governed-automation/README.md) and complete its adoption check before using it.