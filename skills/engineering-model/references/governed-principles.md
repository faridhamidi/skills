# Principles

These are cross-cutting positions. Model-specific triggers and mechanisms belong in [`MODELS.md`](MODELS.md).

## Begin with the governed decision

Do not begin with labels such as control plane, SRE, platform, or agent. Begin with the decision that must be made repeatedly and the consequence of making it incorrectly.

## Risk must justify cost

Additional states, services, identities, queues, operator steps, and contributor concepts are liabilities as well as controls. Adopt a mechanism only when the consequential risk it reduces is greater than its operating and cognitive cost.

## Discovery does not create permission

Finding a resource proves that it exists. It does not prove that the resource should be admitted, monitored, exposed, deleted, funded, or modified.

## Logical authority must match technical authority

A diagrammed separation is false when components share credentials or permissions that permit bypass. Workload identity, authorization, and substrate permissions must enforce the same boundary described by the operating model.

## Uncertainty cannot authorize

Incomplete, stale, malformed, conflicting, or unreadable evidence must not authorize a privileged action. Refusal should be classified, visible, and recoverable.

## Recovery cannot gain authority

Retry, restoration, healing, and offboarding must not acquire a stronger identity or decision power than the normal path. Exceptional break-glass action must be separately authorized and audited.

## Preserve provenance as operational data

Who decided, why, when, under which rule, and from which evidence are part of the system state when later explanation or reversal matters.

## Enforce load-bearing boundaries

A boundary that exists only in prose will decay. Protect high-consequence seams through runtime authorization, contracts, static checks, or tests that reject bypass.

## Establish legibility early, then earn depth

A small codebase is the cheapest place to name external effects, shared vocabulary, and operation context. Use the lightest seam that works and deepen it only after concrete pressure demonstrates the need.

## Keep claims smaller than the system

A domain-specific control plane can be serious without being equivalent to a general orchestration platform. Interfaces can reduce coupling without proving portability. Strong tests can improve confidence without proving correctness.
