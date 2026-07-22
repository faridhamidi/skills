# Documentation

## Problem

Repositories accumulate roadmaps, implementation plans, settled decisions, runbooks, and historical notes. When these artifacts use the same status language and remain in the same active location, readers cannot distinguish possibility from commitment or current truth from obsolete context.

## Three-record discipline

Use three deliberately different record types.

| Record | Question | Binding status | End state |
|---|---|---|---|
| **Forward document** | Where might the system go, and in what order? | Non-binding direction | Archived when realized, superseded, or withdrawn |
| **Design document** | How will a scoped change be built and verified safely? | Binding while active | Archived after implementation |
| **Architecture decision record** | What durable rule was decided, and why? | Binding until superseded | Remains in the active decision history |

The compact mental model is:

```text
forward document = direction
design document  = worked plan
decision record  = durable rule
```

## Promotion loop

```text
Forward direction
    -> selected item becomes a design document
    -> implementation may establish a durable decision
    -> decision becomes an ADR
    -> completion feeds back into the forward document
```

A forward item may also become an ADR directly when the work is a convention choice that requires no implementation plan.

Promotion should be recorded at both ends. The new record cites its origin, and the origin points to the promoted record.

## Disambiguation test

When unsure what to write:

- If deleting the document would let a future engineer **re-make a settled decision**, write an ADR.
- If deleting it would let them **repeat work without the implementation rationale**, write a design document.
- If deleting it would only lose **a sense of intended direction**, write a forward document.

## Archive asymmetry

Forward and design documents are point-in-time artifacts. Archive them when completed or no longer active.

ADRs are different. A superseded ADR should remain visible in the decision set with a pointer to its successor. Moving it to an archive hides the lineage of the current rule.

## Non-maintaining documentation

A stable methodology document should describe conventions, not volatile inventories.

Prefer:

- concepts and classifications;
- pointers to live sources of truth;
- a small number of stable examples;
- commands that query current reality.

Avoid copying test counts, file lists, deployment state, or other data that changes every commit. If the document and executable code disagree, explicitly define which source wins.

## Documentation as governed state

A documentation index should mark each entry with a lifecycle or freshness status such as:

- verified;
- needs review;
- draft;
- historical.

Presence is not correctness. Automated checks can prove that a document exists, carries the required header, or links to a valid successor. They cannot by themselves prove that prose matches runtime behavior.

## Minimal record headers

Every governed record should make these facts greppable:

```text
Type:
Status:
Origin or provenance:
Owner:
Last verified against:
Supersedes / superseded by:
```

## Human rationale and executable projection

When a repository adopts a conformance harness, keep ownership explicit:

| Artifact | Owns |
|---|---|
| Methodology document or ADR | Why the rule exists, trade-offs, scope, exceptions, cost, and security implications |
| Harness manifest | Mechanically enforceable projection and lifecycle metadata |
| Checker adapter | Detection implementation |
| Positive conformance test | Evidence that the current repository satisfies the declared mode |
| Minimal falsifier | Evidence that the checker rejects a prohibited new violation |
| Generic engine tests | Evidence that lifecycle, ratchet, ownership-binding, and audit mechanics behave correctly |
| Audit report | Point-in-time conformance, ownership-binding, and lineage result |
| Repository-host controls | Actual review and merge enforcement |

The manifest must point to rationale. It must not duplicate the rationale. A short rule statement may describe the mechanically checked property, but trade-offs and exceptions remain in the canonical document.

Retired and superseded rule records remain visible with equivalent fidelity across manifest versions. Ordinary format migrations must preserve identifiers, lifecycle, successor relationships, retirement reasons, ownership, and audit continuity. Any deliberate lineage reduction requires a separate reviewed architecture decision focused explicitly on that evidence loss.

An audit report is point-in-time evidence. It does not prove that hosting-platform branch protection or required-review settings are enabled unless those controls are verified separately.

## Boundary

Documentation governance can become its own bureaucracy. Use the smallest lifecycle that prevents actual confusion. A solo or small project may keep all three record types as top-level files; the distinctions matter more than the directory structure.
