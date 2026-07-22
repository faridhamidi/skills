---
name: engineering-model
description: Revertible-envelope guidance for classifying engineering changes, preserving Core boundaries, and selecting governed controls. Use when planning or changing a non-trivial system, when work touches shared or external state, or when authority, evidence, blast radius, or recovery affects what may safely happen.
---

# Engineering Model

Keep work inside a **revertible envelope**: act autonomously while authoring remains
local and recoverable, and require explicit human approval before an external-substrate
effect. Use the lightest engineering control that protects the actual risk.

## 1. Classify The Work

Identify each intended action and answer:

- Does it change or reach shared or external state?
- Can the authoring change be undone locally in one step?
- Does the next action itself affect an external substrate?

Treat uncertainty as above the blast-radius line. Do not treat git as an undo mechanism
for an external effect.

**Complete when:** every intended action is classified as local and reversible, above
the line for further judgment, or an external effect requiring approval.

## 2. Select The Layer

For every non-trivial codebase, read [Core Hygiene](references/core-readme.md) and use
[Starting Foundation](references/core-foundation.md) to identify decision owners,
external-effect boundaries, shared language, operation context, and the smallest useful
checks.

Read only the additional branch the work earns:

- When shared states, actions, transitions, reasons, outcomes, or recovery terms have
  become load-bearing, read
  [Semantic Consistency](references/core-semantic-consistency.md).
- When selecting test intent or structural checks, read
  [Testing](references/core-testing.md).
- When recording direction, an implementation plan, or a durable decision, read
  [Documentation](references/core-documentation.md).
- When several stable cross-cutting rules need shared lifecycle, ownership, ratchets,
  or audit output, read
  [Conformance Harness](references/core-conformance-harness.md).
- When the system performs a consequential shared or external effect, orient with the
  [Governed Automation overview](references/governed-readme.md), then read the
  [Governed Automation Adoption Check](references/governed-adoption-check.md) before
  selecting any governed model. If the gate is crossed, continue through the
  [Decision Tree](references/governed-decision-tree.md) and the canonical
  [Models](references/governed-models.md).
- When the complete authority chain is justified, read
  [Automated Authority](references/governed-automated-authority.md) and
  [Principles](references/governed-principles.md). Use
  [Vocabulary](references/governed-vocabulary.md) only to resolve local terms.

**Complete when:** the adoption is recorded as Core only, selected governed models, or
the complete governed layer, with every added mechanism tied to a concrete trigger and
every rejected mechanism left out.

## 3. Protect The Load-Bearing Seams

Before editing, inspect how the repository already handles the same concern, including
configuration, error handling, logging, parsing, dependencies, and test structure.
Preserve those patterns unless the task deliberately changes them, except where preserving a pattern would let a failure corrupt or lose accepted data — then protect the data and note the intentional departure. Before completion,
self-audit modified code for unused or misplaced imports, dead parameters or
dependencies, unsafe collection access, fragile parsing, and accidental inconsistency;
fix findings in the same pass or record why a departure is intentional.

Implement the selected controls in the product repository. Protect each changed
load-bearing behavior with the lightest test that would fail on a realistic defect. For
new or changed branching business logic, cover the intended path and the
failure, fallback, or guard paths whose outcomes carry material risk. Replace external
services with test doubles unless the test explicitly targets their integration. Treat
a test as enforcement only when an existing executable artifact names the protected
behavior and has run successfully in the current increment. Prefer a direct test before
a ratchet, a ratchet before a manifest-backed harness, and repository-host or substrate
controls when actual admission or authority must be enforced.

This skill owns risk classification and control selection. Use PTM as the specialized
testing profile only when the work is writing, reviewing, or adopting high-assurance
tests for a changed state-changing surface covered by PTM's trigger. PTM obligations
apply to the changed or newly protected risk surface, not automatically to every
historical seam in the repository. When PTM does not trigger, this skill's proportional
test selection remains authoritative.

Add diagnostic context at external, asynchronous, or persistence seams when an
otherwise silent failure would impede detection or recovery. Preserve operation
identifiers and meaningful outcome or reason fields where they exist. Do not log every
function, duplicate telemetry already supplied by the runtime, or expose secrets.
Record an exception before intentionally swallowing it. For data mutation, prove that
failures cannot silently discard or corrupt accepted data; choose validation, atomicity,
and recovery mechanisms in proportion to that risk.

Do not claim an authority boundary unless distinct identities and permissions prevent
weaker components from exercising stronger powers. Do not let missing, stale,
conflicting, or unreadable evidence authorize a consequential action. Route recovery
through the normal authority path.

**Complete when:** every consequential decision and external effect has a named owner;
every changed load-bearing behavior has either an executed test artifact or a recorded
reason that no test is proportionate; every claimed enforcement level maps to an
existing artifact and observed result; every new checker rejects a realistic known-bad
case; relevant silent-failure seams carry enough context to diagnose and recover; and
the self-audit leaves no unexplained dead, fragile, or pattern-divergent code.

## 4. Operate Inside The Envelope

Inspect `git status` before editing and distinguish pre-existing user work from the task
baseline. Confirm that git is available, the project is a repository, and a checkpoint
can be created before relying on git as recovery. If it cannot, do not create a shadow
repository merely to satisfy the ritual or claim that the envelope exists; preserve the
local changes and report the constraint. After a coherent increment satisfies its
declared completion criterion and relevant checks, inspect the effective hooks path,
relevant hooks, configured filters, and commit-time helpers, including filters that may
run while staging. Only when those mechanisms are known not to perform shared or
external effects, stage task-owned changes using explicit paths or selective hunks and
commit with a focused message. Otherwise classify the checkpointing sequence above the
blast-radius line and obtain approval or leave the work uncommitted. Never bypass
legitimate controls merely to keep the action local. Never commit
secrets, generated junk, unrelated changes, or pre-existing user work. Do not rewrite
existing history automatically. If verification fails unexpectedly, preserve the work
without reporting the increment as complete. If task-owned changes cannot be isolated
safely, leave the work uncommitted and report why.

Treat push, pull-request creation, deployment, release, and every other
external-substrate effect as a separate action. Stop, state its target, consequence,
reversibility, and proposed action, then obtain explicit human approval. Approval for
one described effect does not authorize a broader or materially different effect.

**Complete when:** the baseline is known, every new commit is coherent, verified, and
limited to task-owned changes, unresolved work is represented honestly, and no external
effect occurred without approval for that exact effect.

## 5. Report The Result

Include this impact record in the final change summary:

```text
Layer: core only | selected governed models | complete governed layer
Semantic impact: none | local | shared
Enforcement: none | direct test | ratchet | harness rule | protected control
Quality evidence: artifacts and observed results | none with reason
Recovery: checkpointed | uncommitted with reason
Authority impact: none | governed review required
External effects: none | approved and performed | approval required
Residual risk:
```

**Complete when:** each field reflects the implemented behavior and observed evidence,
every named test or check was actually run, and no structural check is promoted into a
claim of runtime enforcement.

## Install The Steering

When installing this skill, place [the steering block](assets/steering.md) in the
runtime's always-on instruction surface. Use the packaged
[AGENTS.md template](assets/AGENTS.md) for Codex-compatible runtimes and the packaged
[CLAUDE.md template](assets/CLAUDE.md) for Claude. Preserve the marked block verbatim so
package validation can detect drift. Keep runtime-specific command syntax outside the
shared block: invoke the skill as `$engineering-model` in Codex and
`/engineering-model` in Claude. If the runtime has no always-on instruction surface,
tell the user that the skill remains on-demand and the external-effect pause is not
continuously steered.

**Complete when:** every native instruction file used by the runtime loads the steering
on every turn, the skill is discoverable and invocable through the runtime's native
form, and each installed block is identical to the packaged canonical block.
