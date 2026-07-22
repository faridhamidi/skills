# Governed Automation Adoption Check

Use this check before introducing staged truth, commit authorities, policy-derived activation, reconciliation, or governed recovery.

## Need gate

### Gate 1 — consequential external effect

Does the system create, change, disable, delete, admit, expose, or grant access to shared or external resources?

- **No:** remain in the Core Hygiene Layer.
- **Yes:** continue.

A local report, cache, generated file, or easily regenerated personal artifact does not normally satisfy this gate.

### Gate 2 — durable authority

Does the system encode a decision such as approval, entitlement, admission, lifecycle state, policy applicability, or another judgment that must remain attributable?

### Gate 3 — material blast radius

Can one incorrect, stale, or overly permissive default affect multiple resources, accounts, users, services, financial positions, or compliance obligations?

### Gate 4 — evidence-sensitive action

Could missing, stale, malformed, conflicting, or unreadable evidence accidentally authorize a privileged or destructive action?

### Gate 5 — governed recovery

Could retry, repair, restoration, or offboarding bypass the authority or evidence required by the normal path?

## Need decision

The complete governed-automation layer is a candidate when Gate 1 is **Yes** and at least one of Gates 2–5 is also **Yes**.

Selected models may be sufficient when Gate 1 is Yes but the effect is narrow, reversible, and has no durable governance meaning. Examples include idempotency, a single mutation owner, or observe-before-repair without a staging system.

Use core hygiene only when the system transforms local data, generates replaceable artifacts, or performs a direct low-risk operation whose failure can be corrected by rerunning it.

## Readiness gate — technical enforceability

Before claiming the complete layer, answer **Yes** to each applicable question:

- Can discovery, commitment, execution, and recovery use separate workload identities?
- Can permissions prevent each component from exercising another component's protected effect?
- Are authority-boundary requests authenticated and contract-validated?
- Can redelivered requests be detected or handled idempotently?
- Are privileged actions recorded independently enough to investigate bypass or misuse?
- Is break-glass access separate, explicit, time-bounded where possible, and auditable?

A design may need the model before these controls exist, but it is not conformant until the controls are enforceable.

## Adoption-cost declaration

Record the cost before choosing the complete layer:

```text
Additional durable states:
Additional services or workers:
Additional privileged identities:
New queues, failure stores, or recovery paths:
New operator steps:
New contributor concepts:
Added deployment and on-call surface:
Expected promotion or execution latency:
Simpler alternative considered:
Risk reduced by the added machinery:
```

Adopt the complete layer only when the expected reduction in consequential risk is greater than the coordination, operational, and cognitive cost. Exact numeric estimates are not always possible; an explicit qualitative comparison is still required.

## Stop signals

Do not add the full authority model when most of these are true:

- one operator owns the task;
- the operation affects one local or replaceable artifact;
- there is no approval or admission decision;
- the direct action is already the authoritative intent;
- failure is visible and a rerun is sufficient;
- a staging layer would duplicate state without creating a review boundary;
- recovery requires no privilege beyond the original operation;
- technical identities cannot enforce the proposed separation;
- the additional operating surface is larger than the risk being controlled.

## Record the result

A product repository should retain:

```text
External effect:
Durable decision:
Blast radius:
Evidence failure risk:
Recovery bypass risk:
Technical enforceability:
Adoption: core only | selected models | complete governed layer
Models selected:
Models explicitly rejected:
Cost declaration:
Review trigger:
```

Revisit the result when the system gains new actors, broader mutation scope, approvals, asynchronous recovery, new credentials, or shared-state ownership.
