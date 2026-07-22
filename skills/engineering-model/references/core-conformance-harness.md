# Repository Conformance Harness

## Purpose

A repository conformance harness is an optional Core Hygiene mechanism for repositories that have accumulated several stable, cross-cutting architectural constraints.

It coordinates machine-readable rule projections, deterministic checker adapters, positive conformance tests, minimal falsifiers, ratchets, ownership bindings, lifecycle lineage, and point-in-time audit output.

It is not a framework, mandatory starter structure, universal AI containment system, or replacement for engineering judgment.

## Adoption trigger

Consider a manifest-backed harness when several of these conditions are present:

- architectural rules are scattered across tests and documents;
- contributors repeatedly reconstruct the same architectural intent;
- multiple human or AI-assisted contributors change the repository;
- architectural checks need stable identifiers;
- checker correctness is important enough to test directly;
- incomplete boundaries require coordinated ratcheting;
- rule ownership needs to be explicit;
- retired or superseded rules need visible lineage;
- CI failures need a consolidated report;
- direct structural tests no longer provide adequate discoverability.

## Skip condition

Do not add the harness when:

- two or three direct tests remain clearer;
- no stable rule identity is needed;
- the rules are too volatile for a manifest;
- an aggregated audit provides no practical value;
- the manifest would only duplicate existing tests;
- the repository is local, regenerable, and adequately protected by direct Core checks;
- the contributor concepts and maintenance cost exceed the risk reduction.

A repository may legitimately adopt Core boundaries, tests, and safe defaults without adopting this mechanism.

## Local vocabulary

| Term | Narrow meaning |
|---|---|
| **Repository conformance harness** | Coordinated rule projections, deterministic checkers, conformance evidence, ratchets, lifecycle records, ownership declarations, and audit output. |
| **Rule identifier** | Stable, immutable namespaced identifier in `<layer>.<domain>.<number>` form for one mechanically checked architectural property. |
| **Positive conformance test** | Test showing that the current repository satisfies the rule's declared enforcement mode. |
| **Minimal falsifier** | Smallest known-bad input or repository fragment proving that the checker detects a prohibited new violation. |
| **Checker adapter** | Language- or tool-specific implementation of a more general rule meaning. |
| **Enforcement mode** | Whether an active rule requires zero violations or preserves an exact shrinking ratchet set. |
| **Historical rule** | Retired or superseded rule whose identity, reason, and lineage remain visible but which no longer executes as an active check. |
| **Ownership binding** | Mechanical correspondence between owners declared in the manifest and principals covering the manifest through repository ownership configuration. |

These terms are local to this optional escalation. They are not additions to the Governed Automation vocabulary.

## Identifier format

Rule identifiers use:

```text
<LAYER>.<DOMAIN>.<NUMBER>
```

Examples:

```text
CORE.ARCH.001
CORE.CONTEXT.001
GOV.AUTH.001
FIXTURE.ARCH.001
```

The layer identifies the adoption surface, the domain identifies the enduring architectural concern, and the final segment is a zero-padded sequence within that namespace. Fixture-only rules use `FIXTURE.*` and must not appear in the live repository manifest.

Identifiers are immutable after activation and are never reused. Do not encode lifecycle, enforcement mode, severity, checker kind, implementation language, file paths, or module names in the identifier. Those properties may change while rule identity remains stable.

Use the validation form:

```regex
^(CORE|GOV|FIXTURE)\.[A-Z][A-Z0-9_]*\.\d{3}$
```

Create a new domain only for an enduring architectural concern, not for one checker implementation or file layout.

## Escalation ladder

```text
direct test
    -> structural ratchet
    -> manifest-backed conformance harness
    -> protected admission or authority control
```

Use the lightest level that protects the actual seam.

### Level 1 — direct test

Use one small executable test for a real boundary.

### Level 2 — structural ratchet

Use when the boundary is valid but existing violations cannot all be removed immediately:

1. enumerate the known violation set;
2. fail when a new violation appears;
3. shrink the set as cleanup lands;
4. convert to zero violations when complete.

### Level 3 — manifest-backed harness

Use when several rules need stable identifiers, common discovery, checker registration, lifecycle state, ratchet state, ownership, paired evidence, lineage, and audit aggregation.

### Level 4 — protected admission or authority control

Use repository-host or Governed Automation controls when an actor can merge, approve itself, weaken protected CI, deploy, mutate shared resources, override checks, or perform privileged recovery.

The harness remains Core Hygiene. The authority exercising it may not.

## Four cooperating layers

### Orientation

`README.md`, `AGENTS.md`, `CONTRIBUTING.md`, canonical documents, and required validation commands reduce reconstruction cost. Orientation is preventive guidance, not enforcement.

### Contract projection

The manifest contains only mechanically useful projections: rule identity, lifecycle, enforcement mode, a concise statement, rationale reference, owners, approval-policy reference, checker kind, scope, configuration, evidence references, ratchet state, and lineage.

A manifest entry is not the canonical architectural explanation.

### Refutation and conformance

Each active rule has:

- a positive conformance test proving the current repository satisfies the declared mode;
- a minimal falsifier proving the checker rejects a prohibited new violation.

Generic fixture-driven tests separately prove ratchet, lifecycle, ownership-binding, and audit mechanics.

### Admission and authority

```text
Instruction          = guidance
Checker              = detection
CI result            = admission signal
Protected CI         = admission enforcement
CODEOWNERS mapping   = ownership declaration and routing
Required review      = hosting-platform enforcement
Credentials and roles = authority control
```

The executable witness demonstrates detection, CI-executable results, CODEOWNERS correspondence, and audit output. It does not demonstrate required review, protected branches, administrative bypass prevention, autonomous merge, deployment, or production mutation controls.

## Human rationale and executable projection

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

The manifest must point to rationale. It must not duplicate the rationale.

## Optional semantic-consistency domain

The rationale for shared states, actions, transitions, reasons, outcomes, and recovery semantics belongs in [`SEMANTIC_CONSISTENCY.md`](SEMANTIC_CONSISTENCY.md). A harness rule in this domain must link to that reference or to a more specific product decision; it must not restate the category definitions in the manifest or checker documentation.

Possible rule families include:

- declared vocabulary agrees with implementation;
- important transitions are complete;
- shared reason and outcome values are single-sourced;
- call sites do not recreate competing semantic catalogs;
- generated semantic references agree with their declarations.

These remain Core rules while they protect legibility and coherence. If actor identity, policy applicability, evidence, or operating conditions determine permission for a consequential effect, apply the Governed Automation adoption check and use governed controls rather than relabelling authorization as semantic consistency.

## Lifecycle

Lifecycle and enforcement completeness are independent.

- **proposed** — documented but not executed as a blocking rule;
- **active** — executed according to its enforcement mode;
- **retired** — trigger no longer exists; retirement reason remains visible;
- **superseded** — another rule owns the property; successor and reason remain visible.

## Enforcement modes

### Zero violation

The checker must observe no prohibited violations.

### Ratchet

The rule is active with an exact known violation set. The observed set must equal the declared set. New violations fail. Cleanup without shrinking the declaration also fails, because the manifest would no longer describe current reality.

The primary invariant is:

> A rule is enforced when the current repository satisfies its declared enforcement mode and a minimal falsifier proves that the checker detects a prohibited new violation.

## Historical rules

Rule identifiers are immutable and never reused. Retired and superseded records remain recoverable and visible with equivalent fidelity across all manifest versions. Active execution excludes historical rules, while audit output preserves their lineage.

Manifest migrations must preserve identifiers, lifecycle, successor relationships, retirement reasons, ownership records, and audit continuity. A format migration may not weaken historical retention as an incidental consequence.

Any deliberate weakening of historical-retention guarantees requires a separate reviewed architecture decision whose explicit subject is lineage reduction. It must state the affected records, justification, approval authority, risks, preservation strategy, rollback approach, and resulting evidence loss.

## Ownership and approval boundary

The witness uses exact, already-public CODEOWNERS principals and validates that they cover the manifest and harness enforcement files.

That correspondence proves ownership declaration and routing, not required-review enforcement. Branch protection and required code-owner review require separate hosting-platform evidence.

All rules stored in one manifest must use an owner set compatible with the CODEOWNERS entry governing that file. File-level CODEOWNERS cannot assign different reviewers to individual JSON records.

## Checker adapters

Rule meanings may be reusable across languages. Checker implementations normally are not.

The witness uses Python AST inspection for:

- forbidden imports;
- exclusive constructor ownership;
- required context parameters.

Other repositories may use ecosystem-specific analyzers. No cross-language implementation is claimed here.

## Adoption cost

The full witness in this repository adds **26 new files** plus targeted changes to Core documentation, contribution rules, repository navigation, case-study indexing, and CI. It introduces at least six contributor concepts beyond direct structural testing: lifecycle, enforcement mode, ratchet state, ownership binding, historical lineage, and the separation between per-rule evidence and generic engine tests. It also adds a dedicated fixture tree, three checker adapters, manifest validation, an audit runner, CODEOWNERS maintenance, CI runtime, and a separate review requirement for any future lineage reduction.

A product repository should not copy that entire surface by default. A minimal justified adoption may be one manifest, one checker entry point, paired positive and negative tests, and one CI command. Add ratchets, ownership binding, historical records, audit artifacts, and migration governance only when the corresponding pressure exists.

Before adoption, record:

```text
New contributor concepts:
New files and scripts:
Checker and fixture maintenance:
Known-violation ownership:
Required reviewers:
CI runtime and failure triage:
Historical-retention obligations:
Migration review obligations:
Simpler direct-test alternative:
Risk reduced by the added machinery:
```

Skip the harness when this cost exceeds the ambiguity or regression risk it controls.

## Security implications

A rule that can fail CI affects admission. It therefore needs explicit ownership, protected change paths where available, and honest claims about what is and is not technically enforced.

If an automated actor can add rules, weaken checks, approve itself, merge, deploy, or override failures, apply the Governed Automation adoption check.

## Evidence boundary

The reusable pattern was extracted from one operational, infrastructure-adjacent system. The witness proves that selected constraints are executable. It does not prove productivity improvement, defect reduction, long-term maintenance cost, universal applicability, or cross-language portability.

## Non-goals

The harness does not:

- replace Markdown rationale with structured data;
- prescribe a project layout;
- enforce all semantic correctness statically;
- make prompts a security boundary;
- contain an AI model;
- prove hosting-platform review settings;
- justify Governed Automation without its adoption gate.