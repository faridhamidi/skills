# Popperian's Skills

Personal agent skills packaged for both Codex and Claude Code.

This is a small skills library for workflows I want agents to run predictably. Each skill is written as a `SKILL.md` plus nearby reference files, so the agent can load the main process first and only open deeper material when the task actually needs it.

The repo is intentionally cross-agent:

- Codex-compatible skills live as top-level folders such as `ptm/`.
- Claude Code-compatible project skills live under `.claude/skills/`.
- Mirrored copies are kept byte-identical so both agents read the same instructions.

## Skills

| Skill | Use for |
| --- | --- |
| [`ptm`](ptm/) | Popperian Testing Methodology: falsification-first testing for high-assurance code that changes external state, including intent tags, oracle meta-tests, anomaly tests, defensive branches, architecture-boundary scanners, gates, and ratchets. |

## Layout

Each skill is stored twice:

- `ptm/` - Codex-compatible skill folder.
- `.claude/skills/ptm/` - Claude Code-compatible project skill folder.

For Codex, copy the top-level skill folder into your Codex skills directory. For Claude Code, copy or keep the `.claude/skills/<skill-name>/` folder in the project where Claude should discover it.

## Maintenance

When changing a skill, update both copies and verify they match:

```bash
diff -r ptm .claude/skills/ptm
```

Keep repo-specific examples out of reusable skill text. Use real projects to sharpen trigger language and README descriptions, but keep the skill itself portable.
