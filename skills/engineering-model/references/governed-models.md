# Governed Automation Models

This file is the canonical source for model definitions. The [decision tree](governed-decision-tree.md) and [vocabulary](governed-vocabulary.md) link here rather than restating full mechanisms.

Select models by trigger. Do not copy the complete set as a starter template.

| Symptom | Canonical model |
|---|---|
| Observed facts, human intent, and real effects can diverge | [Fact, decision, and effect separation](#1-fact-decision-and-effect-separation) |
| An edit must be reviewed before becoming authoritative | [Draft-to-canonical promotion](#2-draft-to-canonical-promotion) |
| Requested intent can be blocked by current policy | [Derived effective state](#3-derived-effective-state) |
| Multiple components can perform the same consequential write | [Sole-writer authority](#4-sole-writer-authority) |
| Shared resources can drift from valid policy | [Policy-driven reconciliation](#5-policy-driven-reconciliation) |
| Operators need a safe exceptional repair path | [Observe-then-repair](#6-observe-then-repair) |
| Retry or restoration could bypass normal controls | [Recovery without privilege escalation](#7-recovery-without-privilege-escalation) |
| Inference must not be confused with authoritative fact | [Confidence-bearing knowledge](#8-confidence-bearing-knowledge) |
| Delivered output must be reproducible from one committed state | [Committed snapshot delivery](#9-committed-snapshot-delivery) |
| A component holds privileged commit, mutation, or recovery capability | [Authority-component security](#10-authority-component-security) |

## 1. Fact, decision, and effect separation

**Trigger:** one record mixes externally observed facts, human decisions, machine recommendations, and real-world effects.

**Definition:** these are independent state axes because they have different authorities, freshness, and failure modes.

**Mechanism:** separate observed facts, governance intent, derived effective state, and observed external effect. Assign write ownership to each group.

**Invariant:** refreshing facts cannot change intent; governance edits cannot rewrite externally owned facts; observed effect is not mistaken for desired state.

**Adoption cost:** additional fields, projections, conflict states, migrations, and operator explanation. The model increases the number of states that must be tested and displayed.

**Security implications:** permissions should follow field ownership; a broad object-replacement permission can invalidate logical separation even when the schema is well designed.

**Skip when:** the states cannot legitimately diverge.

## 2. Draft-to-canonical promotion

**Trigger:** a proposal may be incomplete, reviewed, rejected, or corrected before it becomes authoritative.

**Definition:** proposal state and committed state have different authority and side-effect semantics.

**Mechanism:** write proposals to a reversible workspace, validate them, and promote through one atomic commitment path. Downstream execution reads committed state only.

**Invariant:** draft changes cause no external side effect; stale proposals cannot overwrite newer truth; commitment preserves fields outside the proposal's ownership.

**Adoption cost:** a second durable state, promotion workflow, conflict handling, cleanup, additional latency, and contributor concepts.

**Security implications:** proposal writers must not possess canonical-write credentials. The promotion request must be authenticated and bound to the proposal version being validated.

**Skip when:** one low-risk direct write with validation is already the authoritative intent.

## 3. Derived effective state

**Trigger:** requested intent may remain valid while lifecycle, approval, evidence, or policy prevents current execution.

**Definition:** requested intent records what is wanted; effective state records what is currently permitted.

**Mechanism:** retain requested intent and derive the effective result through a deterministic policy function that returns a classified reason.

**Invariant:** equal inputs produce equal results; missing required evidence produces a safe outcome; presentation labels are not policy inputs.

**Adoption cost:** policy versioning, reason codes, more test combinations, and operator education about requested versus active state.

**Security implications:** policy inputs must have defined provenance and integrity. Attackers must not be able to satisfy gates by changing presentation or low-confidence fields.

**Skip when:** stored state is already direct, authoritative, and unconstrained.

## 4. Sole-writer authority

**Trigger:** multiple components can write the same authoritative state or perform the same consequential external mutation.

**Definition:** one logical authority owns a protected effect, even if several runtime instances implement it behind concurrency control.

**Mechanism:** designate one writer per state or resource class and require all callers to cross the same narrow seam. Add runtime and static bypass checks.

**Invariant:** no production path bypasses the writer; policy remains independent of provider clients; conflicting writers cannot silently win.

**Adoption cost:** an additional service or module boundary, queueing or availability dependency, concurrency control, operational ownership, and possible latency.

**Security implications:** the sole writer requires a distinct workload identity and exclusive substrate permission. Shared credentials turn the sole-writer rule into documentation only.

**Skip when:** components own disjoint fields or effects and cannot conflict.

## 5. Policy-driven reconciliation

**Trigger:** a managed system can drift from valid committed intent as resources appear, close, change, or fail midway through mutation.

**Definition:** reconciliation is execution of already-authorized desired state against observed state; it is not a policy source.

**Mechanism:** read committed state, derive desired state, observe the managed resource, classify the difference, and apply bounded idempotent corrections.

**Invariant:** reconciliation does not originate policy; repeated execution converges; unknown observation does not authorize mutation.

**Adoption cost:** recurring execution, observation APIs, retry and dead-letter behavior, status storage, on-call surface, and eventual-consistency reasoning.

**Security implications:** the reconciler should have only the exact mutation permissions it needs and no permission to create or alter governance decisions.

**Skip when:** there is no durable desired state or no meaningful drift.

## 6. Observe-then-repair

**Trigger:** a manual repair action could become a privileged bypass or act on incomplete evidence.

**Definition:** diagnosis and mutation are separate operations with different safety properties.

**Mechanism:** provide a read-only difference operation, block repair when observation is incomplete, and route approved repair through the normal mutation owner.

**Invariant:** the operator can see what will change and why; exceptional repair does not create a second execution authority.

**Adoption cost:** a diagnostic view, confirmation path, reason capture, and additional operator steps during incidents.

**Security implications:** read-only diagnosis credentials should not imply mutation permission. Repair requests must identify the operator and cannot smuggle direct substrate credentials.

**Skip when:** the operation is local, reversible, and ordinary retry is sufficient.

## 7. Recovery without privilege escalation

**Trigger:** retry, restoration, offboarding, or healing might bypass the controls required by the primary path.

**Definition:** recovery restores progress or known state; it does not create new governance authority.

**Mechanism:** re-drive an existing committed decision, restore a known version, or escalate when proof is insufficient. Reuse normal validation and mutation boundaries.

**Invariant:** recovery cannot create approval, turn unknown state into enabled state, or hide recursive failure.

**Adoption cost:** recovery classification, request records, idempotency, status projection, operator escalation, and another failure path to operate.

**Security implications:** recovery identity must not possess commit or substrate-mutation credentials. It may request re-entry from the component that already owns the protected power.

**Skip when:** recovery has exactly the same narrow effect as an ordinary rerun and carries no additional privilege.

## 8. Confidence-bearing knowledge

**Trigger:** inferred data can be confused with authoritative observation or human judgment.

**Definition:** a value's source and conflict state are part of its meaning; a naked value is insufficient.

**Mechanism:** store value, source, and conflict status separately. Add confidence only when its semantics are defined and testable.

**Invariant:** weaker evidence cannot silently replace stronger evidence; uncertainty remains visible; confidence does not authorize a governed action.

**Adoption cost:** metadata, conflict-resolution workflows, ripening rules, and additional presentation states.

**Security implications:** source identity and evidence integrity matter more than a numeric confidence score. Untrusted producers must not label their own output authoritative.

**Skip when:** every value has one unambiguous authoritative source.

## 9. Committed snapshot delivery

**Trigger:** reports or artifacts generated from mutable live state must remain reproducible across delivery retries.

**Definition:** one immutable source snapshot owns the meaning of every delivered artifact and retry.

**Mechanism:** commit source state, create an immutable snapshot, render outputs from that snapshot, and persist delivery progress against it.

**Invariant:** every delivered artifact is attributable to one committed state even if live state changes later.

**Adoption cost:** snapshot storage, lifecycle cleanup, delivery ledger, retry state, and possible delay between editing and publication.

**Security implications:** the snapshot and delivery record require integrity protection when they support audit or external communication. Delivery credentials should not permit editing the committed source.

**Skip when:** output is disposable, local, and cheap to regenerate without accountability requirements.

## 10. Authority-component security

**Trigger:** a component can commit canonical decisions, mutate consequential external state, or initiate privileged recovery.

**Definition:** logical authority boundaries are valid only when identities, credentials, request authentication, and substrate permissions enforce the same separation.

**Mechanism:**

- assign separate workload identities to discovery, commitment, reconciliation, and recovery;
- grant least-privilege permissions for each protected effect;
- authenticate and contract-validate requests crossing authority boundaries;
- bind operations to version or idempotency tokens to handle replay and redelivery;
- retain audit evidence outside the mutable business record where practical;
- rotate and revoke credentials without transferring authority to weaker components;
- where normal recovery cannot address a credible emergency, define a separate, explicit, time-bounded, and auditable break-glass procedure.

**Invariant:** no component can impersonate a stronger power, reuse its credentials, or call the protected substrate directly outside the designated boundary.

**Adoption cost:** additional identities, permission policies, token validation, audit storage, credential lifecycle work, security review, and incident procedures.

**Security implications:** this model is the security implication. Its failure invalidates the authority matrix even if application tests pass.

**Skip when:** the system has no protected authority or consequential external effect. Ordinary application authentication may still be required, but it is outside this model.
