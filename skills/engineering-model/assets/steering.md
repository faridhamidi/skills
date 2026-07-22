<!-- engineering-model-steering:start -->
## Revertible Envelope

Classify each intended action before performing it:

- If it is local and reversible in one step, continue autonomously.
- If it touches shared ground, is hard to undo, or is uncertain, fail closed and load
  the installed `engineering-model` skill for the depth the decision earns.
- Keep agent-authored work recoverable. At coherent, verified task boundaries, commit
  only task-owned changes with a focused message. Never commit secrets, generated junk,
  unrelated changes, or pre-existing user work. If the task cannot be isolated safely,
  leave the work uncommitted and report why.
- Before relying on git as recovery, verify that the project can create a checkpoint.
  If it cannot, keep the changes local and report the missing recovery mechanism.
- Before any external-substrate effect, stop and obtain explicit human approval for the
  exact target, consequence, and action. Do not treat approval for one effect as
  approval for a broader effect.
- Git can undo authoring; it cannot undo an external effect.

## Implementation Quality

This applies to any code change, regardless of how it is classified above. Load the
installed `engineering-model` skill before editing whenever the change will alter
executable behavior, add or change branching or validation logic, parse external or
untrusted input, or touch a persistence, external, or asynchronous seam. Decide by these
concrete triggers, not by a subjective sense of how large or important the change is; skip
the skill only for pure formatting, comments, or a single-line reversible edit. If the skill
is unavailable, install the packaged skill before continuing; use only the depth the work earns.

- Reuse the repository's existing patterns for the same concern, then self-audit changed code
  for dead or fragile constructs and divergence before completion, and fix findings in the same pass.
  Safety and data integrity override existing conventions: if a pattern would let a failure
  corrupt or lose accepted data, do not preserve it — protect the data and note the intentional
  departure.
- Protect changed load-bearing behavior with the lightest test that would fail on a
  realistic defect. Run the tests and checks you cite. Add diagnostic context at external,
  asynchronous, or persistence seams only when failure would otherwise be silent; never
  silently discard or corrupt data.
<!-- engineering-model-steering:end -->
