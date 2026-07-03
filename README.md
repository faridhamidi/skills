# Farid's Skills

Personal agent skills packaged for both Codex and Claude Code.

This repo is organized as a reusable skills library: each skill lives in its own top-level directory for Codex-style installs, with a mirrored `.claude/skills/` copy for Claude Code project-skill discovery.

## Skills

- [`ftm`](ftm/) - Farid Testing Methodology: falsification-first testing for high-assurance code that changes external state, including intent tags, oracle meta-tests, anomaly tests, defensive branches, architecture-boundary scanners, gates, and ratchets.

## Layout

This repo keeps each skill in two locations:

- `ftm/` - Codex-compatible skill folder.
- `.claude/skills/ftm/` - Claude Code-compatible project skill folder.

The contents are intentionally the same in both locations.
