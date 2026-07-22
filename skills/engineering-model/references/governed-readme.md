# Governed Automation Layer

This layer is intentionally narrow. It applies when software does more than transform local data: it encodes a durable decision, exercises authority, or changes shared external state where an incorrect default can cause material harm.

## Prerequisite

Complete [`governed-adoption-check.md`](governed-adoption-check.md) before adopting this layer. The check includes both risk and adoption-cost accounting.

Core hygiene is always useful. Governed-automation machinery is conditional.

## Canonical reading order

1. [`governed-adoption-check.md`](governed-adoption-check.md) — decide whether the layer is needed and affordable.
2. [`governed-decision-tree.md`](governed-decision-tree.md) — identify candidate models using plain trigger questions.
3. [`governed-models.md`](governed-models.md) — canonical model definitions, including cost and security implications.
4. [`governed-automated-authority.md`](governed-automated-authority.md) — compose the seven powers when the complete model is justified.

Supporting projections:

- [`governed-principles.md`](governed-principles.md) — cross-cutting positions only.
- [`governed-vocabulary.md`](governed-vocabulary.md) — short definitions linked to canonical model entries.

## Security condition

Logical separation is not sufficient. A commit authority, reconciler, or recovery component must have a distinct workload identity and least-privilege permissions that technically enforce its role. If a weaker component can reuse stronger credentials or call the protected substrate directly, the claimed authority boundary does not exist. See [Authority-component security](governed-models.md#10-authority-component-security).

## Non-goals

This layer is not a default application architecture. It should not be used merely because a system:

- has a database;
- runs scheduled jobs;
- calls a cloud API;
- has more than one module;
- needs retries;
- benefits from clean code.

Those are core-hygiene concerns unless they also carry consequential authority, shared-state risk, or durable governance decisions.
