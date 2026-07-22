# Popperian Skills

Personal agent skills packaged as portable `SKILL.md` folders for Codex, Claude Code, and any runtime that understands the Agent Skills format.

This is a small skills library for workflows I want agents to run predictably. Skills live under `skills/`, and each skill gets its own `SKILL.md` entrypoint plus nearby reference files, so agents can load the main process first and only open deeper material when the task actually needs it.

The repo keeps one canonical copy of each skill. Runtime-specific folders such as `.claude/skills/<skill-name>/` or `~/.codex/skills/<skill-name>/` are install targets, not source layout.

## Skills

| Skill | Use for |
| --- | --- |
| [`engineering-model`](skills/engineering-model/) | Revertible-envelope guidance for safe engineering changes, external-effect approval, recoverable commits, proportional tests, Core boundaries, and governed automation controls. |
| [`ptm`](skills/ptm/) | Popperian Testing Methodology: falsification-first testing for high-assurance code that changes external state, including intent tags, oracle meta-tests, anomaly tests, defensive branches, architecture-boundary scanners, gates, and ratchets. |

## Layout

The layout follows a flat skills library:

- `skills/<skill-name>/SKILL.md` - required skill entrypoint.
- `skills/<skill-name>/*.md` - nearby references loaded only when the skill points to them.

Install the same folder into the runtime that should discover it:

```bash
# Codex personal skill
cp -R skills/<skill-name> ~/.codex/skills/<skill-name>

# Claude Code personal skill
cp -R skills/<skill-name> ~/.claude/skills/<skill-name>

# Claude Code project skill
mkdir -p .claude/skills
cp -R skills/<skill-name> .claude/skills/<skill-name>
```

Some skills also ship runtime steering assets. `engineering-model` includes
`assets/AGENTS.md`, `assets/CLAUDE.md`, and `assets/steering.md`; copy the matching
block into the runtime's always-on instruction file so the skill is loaded before
external effects, executable behavior changes, and other load-bearing engineering work.

## Maintenance

When changing a skill, edit the canonical folder and reinstall it where needed. Keep repo-specific examples out of reusable skill text. Use real projects to sharpen trigger language and README descriptions, but keep the skill itself portable.
