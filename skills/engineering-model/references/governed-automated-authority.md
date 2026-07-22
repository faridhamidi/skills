# Automated Authority

## Problem

Automation often begins as a convenience: discover resources, update records, and call an API. At organizational scale, the same automation begins exercising authority. A small incorrect decision can then be multiplied across an estate.

The engineering problem becomes:

> How can a machine act repeatedly and quickly without silently acquiring the authority to decide what should be true?

Complete the [`ADOPTION_CHECK.md`](ADOPTION_CHECK.md) before applying the full model. The individual mechanisms and their costs are canonical in [`MODELS.md`](MODELS.md).

## Seven powers

### 1. Discover

Read facts from an upstream authority. Discovery may refresh fields it owns or create a proposal. It may not convert existence into admission.

### 2. Propose

Create mutable, non-authoritative state representing a possible decision. A proposal may originate from an operator or a bounded system rule.

### 3. Validate

Evaluate the proposal against a versioned contract: required fields, field ownership, transitions, evidence freshness, concurrency, and prohibited combinations.

### 4. Commit

Use one designated logical authority to write canonical state atomically and record provenance. Commitment does not directly mutate the managed resource.

### 5. Derive

Compute effective desired state from canonical intent and current policy. The result is reproducible, classified, and not maintained as an independent mutable truth.

### 6. Execute

Use one designated reconciler to compare effective desired state with observed state and apply idempotent corrections. Execution does not originate policy.

### 7. Recover

Re-drive a committed decision, restore a known version, or escalate when proof is insufficient. Recovery does not infer a more permissive decision from failure.

## Authority matrix

| Capability | Discovery | Operator interface | Commit authority | Reconciler | Recovery |
|---|---:|---:|---:|---:|---:|
| Refresh externally owned facts | Yes | No | No | No | No |
| Edit proposal state | Limited | Yes | No | No | Limited |
| Write canonical decision | No | No | Yes | No | Restore-only through commit path |
| Derive effective state | Advisory only | Advisory only | Validate | Yes | No |
| Mutate managed resource | No | No | No | Yes | No |
| Invent new governance authority | No | No | No | No | No |

A table alone does not create a boundary.

## Technical enforcement

Each protected power should map to an enforceable identity and permission set:

- discovery credentials can read upstream facts but cannot commit or mutate;
- commit credentials can write canonical state but cannot mutate the managed substrate;
- reconciler credentials can mutate the defined resource class but cannot create governance decisions;
- recovery credentials can request bounded re-entry but cannot impersonate commit or reconciliation identities;
- authority-boundary messages are authenticated, schema-validated, and replay-safe;
- privileged actions emit independently retained audit evidence;
- where normal recovery cannot address a credible emergency, break-glass access is separate, time-bounded, auditable, and distinct from ordinary recovery.

Workload-identity provisioning, substrate permission policies, credential rotation and revocation, independently retained audit storage, and break-glass authorization and post-use review are production controls outside the executable witness.

See [Authority-component security](MODELS.md#10-authority-component-security) for the canonical model.

## Core invariants

1. Discovery cannot enable a governed capability merely by finding a resource.
2. Proposal state cannot cause downstream mutation.
3. Only the commit authority can create or change canonical governance state.
4. Only the reconciler can mutate the managed resource.
5. Effective state is derived from canonical data and policy.
6. Missing or conflicting evidence produces the safe non-acting state.
7. Human decisions are not silently overwritten by weaker machine inference.
8. Recovery reuses normal authority gates.
9. Every mutation is attributable to a canonical decision.
10. Reapplying an already converged operation is a no-op.
11. No weaker component can obtain or reuse credentials that exercise a stronger power.
12. Direct substrate permissions do not contradict the logical authority matrix.

## Why this is not merely a workflow

A workflow describes order. An authority model describes who may exercise each power, which evidence is required, which technical identity is allowed, and which bypasses are forbidden.

The distinction matters during failure. A workflow engine may resume at the next step. An authority-aware system must establish whether the next step is still permitted and whether the caller is technically authorized to perform it.

## Executable witness

The dependency-free [`governed_authority_python`](../examples/governed_authority_python/) specimen demonstrates draft isolation, fail-closed validation, sole canonical writing, sole external mutation, runtime role enforcement, idempotent reconciliation, recovery re-entry, and static bypass checks. It is a proof that these constraints are executable, not a production reference architecture. Its [Model 10 coverage matrix](../examples/governed_authority_python/README.md#model-10-coverage) identifies the production security controls it does not demonstrate.
