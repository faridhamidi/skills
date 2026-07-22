# PTM Eval Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and execute an isolated enabled/disabled evaluation of the `ptm` skill on one retry/recovery task.

**Architecture:** A dependency-free Python runner copies a neutral fixture into a temporary workspace, creates a clean Codex home for the selected condition, invokes an agent adapter, and validates the resulting artifact with project tests and a hidden behavioral oracle. Runtime evidence is copied to an ignored results directory; auth and temporary Codex state are never preserved.

**Tech Stack:** Python 3 standard library, `unittest`, Codex CLI, JSON.

## Global Constraints

- Evaluate outcomes, not first-turn triggering or reference-loading paths.
- Keep control and treatment identical except for PTM skill availability.
- Run agents only in disposable workspace-write sandboxes without fixture network dependencies.
- Do not expose hidden checks or expected code to the evaluated agent.
- Treat the initial pair as method validation, not statistical evidence of skill effectiveness.
- Do not add third-party dependencies.

---

### Task 1: Define the fixture, case, and failing harness contract

**Files:**
- Create: `evals/fixtures/retry-recovery/profile_store.py`
- Create: `evals/fixtures/retry-recovery/tests/test_profile_store.py`
- Create: `evals/fixtures/retry-recovery/README.md`
- Create: `evals/cases/ptm-retry-recovery.json`
- Create: `evals/oracles/retry_recovery_oracle.py`
- Create: `tests/test_eval_harness.py`

**Interfaces:**
- Consumes: Python standard library only.
- Produces: `load_case(path)`, `snapshot_tree(path)`, `validate_artifact(case, baseline, artifact)`, and `run_trial(...)` contracts for Task 2.

- [x] **Step 1: Create a neutral broken fixture and its passing happy-path test**

Define `ProfileStore.replace_many(changes)` with injectable failing attempts. Its initial
implementation writes fields sequentially and raises after the first write on selected
attempts. Define `update_profile(store, changes, attempts)` as a retry loop. Document the
contract that a failed operation must restore the complete original profile.

- [x] **Step 2: Add the hidden behavioral oracle**

The oracle imports the artifact by a path argument and asserts:

```python
def test_transient_failure_commits_complete_update(): ...
def test_permanent_failure_preserves_original_profile(): ...
```

- [x] **Step 3: Verify the oracle rejects the initial fixture**

Run:

```bash
python3 evals/oracles/retry_recovery_oracle.py evals/fixtures/retry-recovery
```

Expected: one happy transient assertion may pass, but the permanent-failure preservation assertion fails because the initial implementation leaves a partial update.

- [x] **Step 4: Define the case without leaking the oracle**

Use this ordinary task prompt:

```text
Customers report that a profile update can leave a partially changed record when storage fails. Add appropriate tests and make the retry and recovery behavior safe. Work within this repository and run the relevant tests.
```

- [x] **Step 5: Write failing harness tests**

Cover case loading, tree snapshots, changed-test intent-tag inspection, hidden-oracle
execution, fake-agent execution, result persistence, and rejection of invalid conditions.

- [x] **Step 6: Run the harness tests and verify RED**

Run:

```bash
python3 -m unittest tests.test_eval_harness -v
```

Expected: import failure because `evals.ptm_eval` does not exist.

### Task 2: Implement the isolated runner and validators

**Files:**
- Create: `evals/__init__.py`
- Create: `evals/ptm_eval/__init__.py`
- Create: `evals/ptm_eval/case.py`
- Create: `evals/ptm_eval/validation.py`
- Create: `evals/ptm_eval/runner.py`
- Create: `evals/run.py`
- Create: `.gitignore`

**Interfaces:**
- Consumes: the case and test contracts from Task 1.
- Produces:
  - `Case.load(path: Path) -> Case`
  - `snapshot_tree(path: Path) -> dict[str, str]`
  - `validate_artifact(case: Case, baseline: Path, artifact: Path) -> dict`
  - `run_trial(case, condition, output_dir, command_template=None, model=None, timeout=None) -> dict`

- [x] **Step 1: Implement case parsing and validation**

Require `id`, `fixture`, `prompt`, `project_test_command`, and `oracle` fields. Resolve
fixture and oracle paths relative to the repository root and reject paths that escape it.

- [x] **Step 2: Run tests to reach the next expected failure**

Run `python3 -m unittest tests.test_eval_harness -v` and confirm failures now identify
the missing validator/runner behavior rather than imports.

- [x] **Step 3: Implement deterministic validation**

Record project-test and hidden-oracle return codes, baseline/artifact file changes,
whether changed tests inject configured failures, and whether each newly added test has
exactly one `Falsifies:`, `Regresses:`, or `Confirms:` tag. Keep every check separate.

- [x] **Step 4: Implement isolated execution**

For each run:

1. Copy the fixture and create a separate temporary Codex home.
2. Copy only `auth.json` from the source Codex home when using the real adapter.
3. For treatment only, copy `skills/ptm` into `<temporary-home>/skills/ptm`.
4. Invoke `codex exec --ephemeral --ignore-user-config --skip-git-repo-check --sandbox workspace-write` with `CODEX_HOME` set to the temporary home.
5. Capture stdout, stderr, exit status, duration, artifact, and validation results.
6. Copy evidence—but never the temporary Codex home—to the requested results directory.

- [x] **Step 5: Implement the CLI and ignored evidence directory**

Support:

```bash
python3 evals/run.py \
  --case evals/cases/ptm-retry-recovery.json \
  --condition control \
  --trials 1
```

Allow `--condition both`, `--model`, `--timeout`, `--output-dir`, and a repeatable
`--agent-command` template for deterministic tests.

- [x] **Step 6: Run tests and verify GREEN**

Run:

```bash
python3 -m unittest discover -s tests -v
```

Expected: all harness tests pass.

- [x] **Step 7: Verify fixture baseline behavior**

Run the fixture's public tests and hidden oracle separately. Expected: public happy-path
tests pass and the hidden recovery oracle fails on the intentional defect.

### Task 3: Execute and audit the real pilot

**Files:**
- Create at runtime: `evals/results/<run-id>/...`
- Modify only if evidence exposes a harness defect: files from Tasks 1–2 and their tests.

**Interfaces:**
- Consumes: the verified runner and canonical `skills/ptm` folder.
- Produces: one control artifact, one treatment artifact, transcripts, diffs, and separate check results.

- [x] **Step 1: Run one control and one treatment trial**

Run:

```bash
python3 evals/run.py --case evals/cases/ptm-retry-recovery.json --condition both --trials 1
```

Expected: two completed result records. Outcome checks may legitimately differ or fail.

- [x] **Step 2: Inspect both artifacts manually**

Compare changed files, test quality, hidden-oracle results, intent tags, and agent errors.
Do not tune the task to favor treatment.

- [x] **Step 3: Correct harness defects test-first**

For each defect, add a failing `tests/test_eval_harness.py` case, verify the failure,
apply the minimal correction, and rerun the complete suite.

- [x] **Step 4: Run final verification**

Run:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q evals tests
git diff --check
```

Confirm that results remain ignored and the source repository contains only intended
changes.

- [x] **Step 5: Report bounded findings**

Report the exact control and treatment checks, execution limitations, and artifact
paths. State explicitly that one case cannot establish general skill effectiveness.
