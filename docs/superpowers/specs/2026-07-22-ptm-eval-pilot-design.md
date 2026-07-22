# PTM Eval Pilot Design

## Purpose

Establish the smallest trustworthy experiment that can show whether the `ptm` skill
improves a coding agent's treatment of a high-risk retry and recovery task. The pilot
validates the evaluation method; it does not claim statistical effectiveness for PTM.

## Experiment

Run one neutral fixture twice under otherwise matching conditions:

1. Control: use an isolated Codex home in which `ptm` is unavailable.
2. Treatment: use an isolated Codex home containing only the canonical `ptm` skill.

Each run starts from a fresh copy of the fixture, uses an ephemeral agent session, and
has workspace-write access only to that copy. Do not expose the expected implementation
or validator details in the task prompt.

The fixture models a key-value store whose current retry implementation can leave a
partial write after a transient failure. The agent is asked to add appropriate tests
and make the behavior safe. The task is deliberately phrased in ordinary engineering
language and does not mention PTM.

## Components

- `evals/fixtures/retry-recovery/`: dependency-free Python repository copied for every
  trial.
- `evals/cases/ptm-retry-recovery.json`: prompt, fixture, and outcome expectations.
- `evals/ptm_eval/`: focused Python modules for case loading, isolated execution, and
  validation.
- `evals/run.py`: command-line entry point for real and dry-run executions.
- `tests/`: unit and integration tests for the harness and fixture.
- `evals/results/`: ignored runtime evidence containing transcripts, diffs, and scores.

## Outcome Checks

Score observable artifacts rather than the agent's chosen path:

- The fixture's complete test suite passes.
- A test injects a transient failure.
- A test proves permanent failure cannot leave partial state.
- Each newly added test declares one PTM intent tag in the treatment artifact; report
  this separately rather than allowing it to compensate for unsafe behavior.
- The implementation preserves the original value when an attempted update fails.
- No files outside the disposable fixture are modified by an eval run.

Store individual check results instead of collapsing them into an unsupported global
claim. Compare the control and treatment artifacts manually after the first pair.

## Interfaces

`evals/run.py` accepts a case path, condition, trial count, output directory, model,
and optional command template. The default adapter invokes `codex exec` with an
ephemeral session and a workspace-write sandbox. A fake command template supports
deterministic harness testing without model access.

The runner returns nonzero only for harness failures. A completed agent attempt may
fail outcome checks and still be recorded successfully as evaluation evidence.

## Isolation and Failure Handling

- Create all trial workspaces and Codex homes beneath a fresh temporary directory.
- Copy authentication material required by Codex without copying discoverable skills,
  configuration, history, or task artifacts.
- Disable project/user configuration discovery where supported.
- Preserve the trial workspace, transcript, diff, command metadata, and validator
  results under `evals/results/`.
- Apply an execution timeout and record timeouts or agent failures without treating
  them as successful outcomes.
- Never run the fixture against real network, database, or cloud services.

## Testing Strategy

Develop the harness test-first. Unit tests cover schema loading, condition setup,
validator behavior, result recording, and failure handling. An integration test uses a
deterministic fake agent to modify a temporary fixture and proves that the runner
captures and scores the artifact. The fixture's own tests include a known-bad test that
fails against its initial implementation, proving the recovery oracle is capable of
detecting the defect.

After local tests pass, execute one real control run and one real treatment run. Inspect
both diffs and validator output. Refine only defects in the harness or ambiguous checks;
do not tune the prompt or fixture to make the treatment win.

## Completion Criteria

- Harness tests and fixture tests demonstrate the intended red/green behavior.
- The real enabled/disabled pair completes or produces an honestly recorded external
  runner limitation.
- Evidence is reproducible from a documented command.
- Results make no claim beyond the single evaluated case.
