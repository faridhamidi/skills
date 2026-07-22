# Skill Package Integrity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair the packaged skill graph and continuously reject future package-integrity drift.

**Architecture:** A dependency-free Python validator discovers skills and checks repository invariants. Markdown and skill-policy edits make the current tree honest, navigable, and compositionally explicit; GitHub Actions executes the same validator and test suite.

**Tech Stack:** Python standard library, `unittest`, Markdown/YAML text validation, GitHub Actions.

## Global Constraints

- Keep the flattened `skills/engineering-model/references/` layout.
- Do not import upstream witness projects.
- Do not choose a reuse license for the owner.
- Do not add runtime dependencies.

---

### Task 1: Repository validator

**Files:**
- Create: `scripts/validate_repository.py`
- Create: `tests/test_repository_validation.py`

**Interfaces:**
- Produces: `validate_repository(root: Path) -> list[str]` and a CLI returning nonzero when errors exist.

- [ ] Write fixture-based tests for metadata, broken targets/anchors, README registry drift, steering drift, OpenAI metadata, and absent-artifact claims.
- [ ] Run `python3 -m unittest tests.test_repository_validation -v` and confirm failures caused by the missing validator.
- [ ] Implement the smallest standard-library validator satisfying the tests.
- [ ] Run the test module and confirm it passes.

### Task 2: Package repair and behavior contracts

**Files:**
- Modify: `skills/engineering-model/references/*.md`
- Modify: `skills/engineering-model/SKILL.md`
- Modify: `skills/engineering-model/assets/{steering.md,AGENTS.md,CLAUDE.md}`
- Modify: `skills/ptm/SKILL.md`
- Create: `skills/ptm/agents/openai.yaml`
- Modify: `README.md`

**Interfaces:**
- Consumes: validator invariants from Task 1.
- Produces: a fully resolvable package and explicit policy boundaries.

- [ ] Run the repository validator against the current tree and retain the expected failure diagnostics.
- [ ] Rewrite local links and remove unsupported witness/CI claims.
- [ ] Add PTM composition and changed-surface scoping; add commit-time side-effect classification.
- [ ] Add PTM UI metadata and accurate install/licensing language.
- [ ] Run the validator and skill validation commands.

### Task 3: Continuous validation

**Files:**
- Create: `.github/workflows/validate.yml`

**Interfaces:**
- Consumes: `scripts/validate_repository.py` and the `unittest` suite.
- Produces: push and pull-request validation on supported Python.

- [ ] Add a minimal workflow invoking the validator and `python3 -m unittest discover -s tests -v`.
- [ ] Run the same commands locally.
- [ ] Run `git diff --check` and inspect the complete diff before reporting completion.
