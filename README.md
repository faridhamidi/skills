# Popperian's Skills

Portable agent skills for Codex, Claude Code, and any runtime that understands the Agent Skills `SKILL.md` folder format.

This is a small skills library for workflows I want agents to run predictably. Each skill is written as a `SKILL.md` plus nearby reference files, so the agent can load the main process first and only open deeper material when the task actually needs it.

The repo keeps one canonical copy of each skill. Runtime-specific folders such as `.claude/skills/<skill-name>/` or `~/.codex/skills/<skill-name>/` are install targets, not source layout.

## Skills

| Skill | Use for |
| --- | --- |
| [`ptm`](ptm/) | Popperian Testing Methodology: falsification-first testing for high-assurance code that changes external state, including intent tags, oracle meta-tests, anomaly tests, defensive branches, architecture-boundary scanners, gates, and ratchets. |

## Layout

Each skill is a portable folder:

- `ptm/SKILL.md` - required skill entrypoint.
- `ptm/*.md` - nearby references loaded only when the skill points to them.

Install the same folder into the runtime that should discover it:

```bash
# Codex personal skill
cp -R ptm ~/.codex/skills/ptm

# Claude Code personal skill
cp -R ptm ~/.claude/skills/ptm

# Claude Code project skill
mkdir -p .claude/skills
cp -R ptm .claude/skills/ptm
```

## Maintenance

When changing a skill, edit the canonical folder and reinstall it where needed. Keep repo-specific examples out of reusable skill text. Use real projects to sharpen trigger language and README descriptions, but keep the skill itself portable.
