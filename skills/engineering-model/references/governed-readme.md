# Governed Automation Layer

This layer is intentionally narrow. It applies when software does more than transform local data: it encodes a durable decision, exercises authority, or changes shared external state where an incorrect default can cause material harm.

## Prerequisite

Complete [`ADOPTION_CHECK.md`](ADOPTION_CHECK.md) before adopting this layer. The check includes both risk and adoption-cost accounting.

Core hygiene is always useful. Governed-automation machinery is conditional.

## Canonical reading order

1. [`ADOPTION_CHECK.md`](ADOPTION_CHECK.md) — decide whether the layer is needed and affordable.
2. [`DECISION_TREE.md`](DECISION_TREE.md) — identify candidate models using plain trigger questions.
3. [`MODELS.md`](MODELS.md) — canonical model definitions, including cost and security implications.
4. [`AUTOMATED_AUTHORITY.md`](AUTOMATED_AUTHORITY.md) — compose the seven powers when the complete model is justified.

Supporting projections:

- [`PRINCIPLES.md`](PRINCIPLES.md) — cross-cutting positions only.
- [`VOCABULARY.md`](VOCABULARY.md) — short definitions linked to canonical model entries.
- [`../examples/governed_authority_python/`](../examples/governed_authority_python/) — a dependency-free executable witness.

## Security condition

Logical separation is not sufficient. A commit authority, reconciler, or recovery component must have a distinct workload identity and least-privilege permissions that technically enforce its role. If a weaker component can reuse stronger credentials or call the protected substrate directly, the claimed authority boundary does not exist. See [Authority-component security](MODELS.md#10-authority-component-security).

## Non-goals

This layer is not a default application architecture. It should not be used merely because a system:

- has a database;
- runs scheduled jobs;
- calls a cloud API;
- has more than one module;
- needs retries;
- benefits from clean code.

Those are core-hygiene concerns unless they also carry consequential authority, shared-state risk, or durable governance decisions.
