# Adopting PTM

Adopt PTM incrementally. Each new gate should be green on arrival and then tighten.

## Checklist

1. Read the repo's test setup. Identify the runner, test directories, coverage tool, existing fakes, and parser/AST library for the language.
2. Add the intent-tag ratchet and generate the baseline from the current suite.
3. Identify pure decision modules and put only those behind G-BRANCH.
4. Identify seams that must not be bypassed: single owners, layer lines, purity rules, protected resources, clock/network/database/cloud access.
5. For each seam, build the boundary pattern: scanner, manifest, scanner meta-tests, real-file enforcement, seeded mutation where practical.
6. Find retry, recovery, and multi-step failure paths; give each Method A anomaly tests, permanent case first.
7. Find "cannot happen if upstream is correct" guards; mark them `# DEFENSIVE` and add Method B bypass tests when touched.
8. Wire G-BRANCH and G-BOUNDARY into CI.

## Language Notes

- Python: stdlib `ast`.
- TypeScript/JavaScript: `ts-morph` or `@babel/parser`.
- Go: `go/ast`.
- Java: JavaParser or the repo's existing parser.
- Rust: `syn`.

Prefer the repo's existing test framework and parser when one is already established.

