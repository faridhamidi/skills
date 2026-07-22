# Vocabulary

These definitions are intentionally narrow. Canonical mechanisms live in [`MODELS.md`](MODELS.md); the seven workflow powers live in [`AUTOMATED_AUTHORITY.md`](AUTOMATED_AUTHORITY.md).

| Term | Narrow meaning | Canonical reference |
|---|---|---|
| **Admission** | A governed decision that a discovered resource may participate in a managed capability. Existence does not imply admission. | [Discover and Commit](AUTOMATED_AUTHORITY.md#seven-powers) |
| **Authority boundary** | A restriction defining which identity or component may make a decision or perform a protected effect. | [Authority-component security](MODELS.md#10-authority-component-security) |
| **Canonical state** | Committed state from which downstream policy and execution are derived; authoritative within the operating model, not infallible. | [Draft-to-canonical promotion](MODELS.md#2-draft-to-canonical-promotion) |
| **Commit authority** | The logical component permitted to convert a valid proposal into canonical governance state. | [Sole-writer authority](MODELS.md#4-sole-writer-authority) |
| **Confidence-bearing knowledge** | A value accompanied by source and conflict state so inference is not mistaken for authoritative fact. | [Confidence-bearing knowledge](MODELS.md#8-confidence-bearing-knowledge) |
| **Control plane** | Software that governs desired state and causes another system to converge through explicit policy, authority, observation, and reconciliation. | [Policy-driven reconciliation](MODELS.md#5-policy-driven-reconciliation) |
| **Decision metadata** | Actor, reason, time, rule, version, and evidence associated with a governed decision. | [Fact, decision, and effect separation](MODELS.md#1-fact-decision-and-effect-separation) |
| **Desired state** | The state a managed system should converge toward after canonical intent has been evaluated by policy. | [Derived effective state](MODELS.md#3-derived-effective-state) |
| **Discovery** | Observation of facts from an upstream authority; it does not grant admission by itself. | [Discover](AUTOMATED_AUTHORITY.md#1-discover) |
| **Draft state** | Mutable proposal state that is non-authoritative and cannot cause managed-resource effects. | [Draft-to-canonical promotion](MODELS.md#2-draft-to-canonical-promotion) |
| **Drift** | A meaningful difference between effective desired state and readable observed state. Unknown observation is evidence failure, not ordinary drift. | [Policy-driven reconciliation](MODELS.md#5-policy-driven-reconciliation) |
| **Effective state** | The permitted result derived from intent, policy, lifecycle, approval, exclusions, and evidence. | [Derived effective state](MODELS.md#3-derived-effective-state) |
| **Fail closed** | Refuse a privileged action when required evidence is missing, stale, malformed, conflicting, or unreadable. | [Derived effective state](MODELS.md#3-derived-effective-state) |
| **Field ownership** | Assignment of each mutable field group to the component and identity permitted to write it. | [Fact, decision, and effect separation](MODELS.md#1-fact-decision-and-effect-separation) |
| **Healer** | A bounded recovery component that re-drives committed work or requests restoration without acquiring new authority. | [Recovery without privilege escalation](MODELS.md#7-recovery-without-privilege-escalation) |
| **Idempotency** | Reapplying an operation after convergence produces no additional effect. | [Policy-driven reconciliation](MODELS.md#5-policy-driven-reconciliation) |
| **Observed state** | State reported by the managed system or external source, which may be stale, incomplete, or unavailable. | [Policy-driven reconciliation](MODELS.md#5-policy-driven-reconciliation) |
| **Promotion** | Validated, attributable transition from proposal state to canonical state. | [Draft-to-canonical promotion](MODELS.md#2-draft-to-canonical-promotion) |
| **Provenance** | Recorded origin and rationale of a fact, proposal, decision, restoration, or mutation. | [Fact, decision, and effect separation](MODELS.md#1-fact-decision-and-effect-separation) |
| **Reconciliation** | Comparison of effective desired state with observed state followed by bounded idempotent correction. | [Policy-driven reconciliation](MODELS.md#5-policy-driven-reconciliation) |
| **Recovery re-entry** | Retry and repair request the same validation and mutation authorities used by ordinary work. | [Recovery without privilege escalation](MODELS.md#7-recovery-without-privilege-escalation) |
| **Sole writer** | One logical authority permitted to mutate a protected state or resource class, possibly implemented by several instances behind concurrency control. | [Sole-writer authority](MODELS.md#4-sole-writer-authority) |
| **Workload identity** | The non-human identity under which a component authenticates and receives its bounded permissions. | [Authority-component security](MODELS.md#10-authority-component-security) |
