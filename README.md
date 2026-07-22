![Farid's Skills](ref/header.jpg)

# Farid's Skills

Agent skills I use to make coding agents more predictable.

This is a small personal skills library, packaged as portable `SKILL.md` folders for Codex, Claude Code, and any runtime that understands the Agent Skills format. It is meant to be practical rather than polished into a product: a place for workflows that are worth reusing across projects.

The repo keeps one canonical copy of each skill. Runtime-specific folders such as `.claude/skills/<skill-name>/` or `~/.codex/skills/<skill-name>/` are install targets, not source layout.

Skills live under `skills/`. Each skill has its own `SKILL.md` entrypoint plus nearby reference files, so agents can load the main process first and only open deeper material when the task actually needs it.

## Stance

AI-generated output is not trusted by default. Karl Popper — the philosopher of science who
argued that theories are never confirmed, only ever survive attempts to refute them — is the
root of the posture here: a claim earns belief by surviving an active attempt to break it, not
by absence of complaint. Corroboration is cheap; "I tried hard to break it and could not" is the
only evidence that counts. This repo's skills are three applications of that Popperian stance, aimed at three different
objects — what a system produces, what a system is permitted to do, and what a design claims
will hold.

## Skills

| Skill | Use for |
| --- | --- |
| [`ptm`](skills/ptm/) | Trust in claims about code: falsification-first testing. A test does not confirm a belief about the code — it attacks it. `Falsifies:` is the default intent; an oracle that cannot fail is worse than no oracle. |
| [`engineering-model`](skills/engineering-model/) | Trust in actions: burden-of-proof-on-action. Inaction is the safe ground state; an effect that reaches shared or external state must earn explicit approval before it is granted leverage. |
| [`reviewing-engineering-designs`](skills/reviewing-engineering-designs/) | Trust in claims about designs: treats an ADR, RFC, or architecture document as a set of falsifiable claims about authority, state, behavior, and operations, and tests whether its mechanisms hold under failure, recovery, and change — not whether the prose reads well. |

## Install

Copy the skill folder into the runtime that should discover it.

**Prefer the project-scoped target** over the personal/global one: these skills are
**opinionated** and carry real gates (hard merge blocks, mandatory tags, burden-of-proof
postures), and loading them globally applies that weight to every repo you open, including
ones where it's disproportionate. Install globally only for a skill you want active
everywhere, deliberately.

```bash
# Codex personal skill
cp -R skills/<skill-name> ~/.codex/skills/<skill-name>

# Claude Code personal skill
cp -R skills/<skill-name> ~/.claude/skills/<skill-name>

# Claude Code project skill
mkdir -p .claude/skills
cp -R skills/<skill-name> .claude/skills/<skill-name>
```

For a public-GitHub install in Codex, invoke the built-in installer with a natural-language
request such as:

```text
Use $skill-installer to install https://github.com/faridhamidi/skills/tree/main/skills/engineering-model
Use $skill-installer to install https://github.com/faridhamidi/skills/tree/main/skills/ptm
Use $skill-installer to install https://github.com/faridhamidi/skills/tree/main/skills/reviewing-engineering-designs
```

Some skills also ship runtime steering assets. `engineering-model` includes
`assets/AGENTS.md`, `assets/CLAUDE.md`, and `assets/steering.md`; copy the matching
block into the runtime's always-on instruction file so the skill is loaded before
external effects, executable behavior changes, and other load-bearing engineering work.

## Layout

- `skills/<skill-name>/SKILL.md` - required skill entrypoint.
- `skills/<skill-name>/*.md` - nearby references loaded only when the skill points to them.
- `skills/<skill-name>/assets/` - optional install assets, templates, or steering blocks.
- `skills/<skill-name>/references/` - optional deeper docs loaded through context pointers.

## Maintenance

When changing a skill, edit the canonical folder and reinstall it where needed. Keep repo-specific examples out of reusable skill text. Use real projects to sharpen trigger language and README descriptions, but keep the skill itself portable.

## License status

This repository currently has no license. Public visibility and these installation
instructions do not grant third parties permission to redistribute or reuse the contents
beyond rights provided by applicable law. Add an explicit license only after choosing the
intended reuse terms.

## Evaluate

The initial eval pilot compares `ptm` unavailable (control) with the canonical skill
installed in an otherwise isolated Codex home (treatment). Each trial starts from a
fresh copy of a deliberately faulty retry/recovery fixture and records the artifact,
agent output, project tests, and a hidden behavioral oracle.

```bash
python3 evals/run.py \
  --case evals/cases/ptm-retry-recovery.json \
  --condition both \
  --trials 1
```

Raw evidence is written beneath the ignored `evals/results/` directory. A successful
agent process is not automatically a passing outcome: inspect the individual
`project_tests`, `hidden_oracle`, fault-injection, and intent-tag checks in each
`result.json`. One paired run validates the harness and provides a case result; it does
not establish general skill effectiveness. Repeat cases and trials before making a
reliability claim.

Use `evals/cases/ptm-retry-recovery-explicit.json` to measure follow-through after an
intentional `$ptm` invocation. The default case leaves invocation to the model and
therefore exercises both discovery and follow-through.
