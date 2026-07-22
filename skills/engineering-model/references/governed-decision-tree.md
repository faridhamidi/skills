# Plain-Language Decision Tree

Use the trigger, not the term, to decide what the system needs. Full definitions live in [`governed-models.md`](governed-models.md).

## Boundaries and ownership

**Do observed facts, human intent, derived policy, and real effects legitimately diverge?**

- No → keep one state model.
- Yes → consider [Fact, decision, and effect separation](governed-models.md#1-fact-decision-and-effect-separation).

**Can two components perform the same consequential write?**

- No → no sole-writer model is required.
- Yes, but ownership is disjoint → declare field ownership.
- Yes, and writes can conflict → consider [Sole-writer authority](governed-models.md#4-sole-writer-authority) and [Authority-component security](governed-models.md#10-authority-component-security).

## State and commitment

**Must an edit be reviewed or corrected before becoming authoritative?**

- No → write directly with validation.
- Yes → consider [Draft-to-canonical promotion](governed-models.md#2-draft-to-canonical-promotion).

**Can requested intent remain valid while policy blocks current execution?**

- No → store direct state.
- Yes → consider [Derived effective state](governed-models.md#3-derived-effective-state).

## Execution and repair

**Can shared external state drift from valid committed intent?**

- No → do not add reconciliation.
- Yes → consider [Policy-driven reconciliation](governed-models.md#5-policy-driven-reconciliation).

**Could incomplete observation make repair unsafe?**

- No → ordinary retry may be enough.
- Yes → consider [Observe-then-repair](governed-models.md#6-observe-then-repair).

**Could retry or restoration gain stronger authority than the original path?**

- No → ordinary retry semantics may be enough.
- Yes → consider [Recovery without privilege escalation](governed-models.md#7-recovery-without-privilege-escalation).

## Evidence and delivery

**Can inferred data be mistaken for authoritative fact?**

- No → store the value normally.
- Yes → consider [Confidence-bearing knowledge](governed-models.md#8-confidence-bearing-knowledge).

**Must delivered output remain attributable to one committed source state?**

- No → regenerate directly.
- Yes → consider [Committed snapshot delivery](governed-models.md#9-committed-snapshot-delivery).

## Security and cost check

**Does any selected model create a privileged component?**

- No → apply the selected model proportionally.
- Yes → [Authority-component security](governed-models.md#10-authority-component-security) is mandatory, not optional.

Before adopting, complete the [cost declaration](governed-adoption-check.md#adoption-cost-declaration). If the mechanism only adds terminology, states, or operational surface without reducing a consequential risk, skip it.
