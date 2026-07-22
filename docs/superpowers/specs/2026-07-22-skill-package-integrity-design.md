# Skill Package Integrity Design

## Goal

Make the repository operationally trustworthy as a distributable Agent Skills library without importing the large upstream example repository.

## Decisions

- Keep `engineering-model/references/` flat and rewrite every local Markdown link to the packaged filename.
- Remove claims that executable witnesses and CI evidence ship with `engineering-model`; retain methodology descriptions only when they do not claim local proof.
- Add one dependency-free repository validator covering skill metadata, local Markdown targets and anchors, README/skill-directory reconciliation, steering-copy equality, OpenAI metadata, and references to absent examples or scripts.
- Run the validator and existing tests in GitHub Actions on pushes and pull requests.
- Define `engineering-model` as risk/control-selection policy and PTM as the testing profile used only when PTM's explicit high-assurance trigger applies. Scope PTM obligations to the changed or newly protected surface.
- Treat a local commit as autonomous only after commit-time hooks, configured filters, and helpers are known not to cause shared or external effects.
- Add Codex UI metadata for PTM and document direct public-GitHub installation as a Codex prompt, not a shell command.
- State that no reuse license is currently granted; do not choose a license on the owner's behalf.

## Validation behavior

`scripts/validate_repository.py` returns zero only when all repository invariants pass. Diagnostics identify the referring file and defect. Tests exercise each invariant against temporary repository fixtures, including known-bad links and artifact claims.

## Scope

This change does not add upstream witnesses, choose an open-source license, publish, push, or create a pull request.
