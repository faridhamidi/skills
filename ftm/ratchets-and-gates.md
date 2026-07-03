# Ratchets And Gates

FTM uses gates for rules that should block merge and ratchets for rules that must improve without a big-bang rewrite.

## G-BRANCH

Use 100% branch coverage only for pure decision modules and explicit decision-table oracles.

Do not chase whole-system coverage. Adapters, handlers, and glue earn confidence through contract tests, fault injection, anomaly tests, and boundary tests.

Keep the list of pure decision modules in coverage config or an explicit manifest. Add a lockstep test if needed so a new pure module cannot avoid both the manifest and G-BRANCH.

## G-BOUNDARY

G-BOUNDARY is the architecture-boundary suite. It passes only when no module bypasses the protected seam.

For a seam that has known existing violations, add a forward lock: pin the current violation set and fail if a new violation appears. Upgrade to hard enforcement when the seam is extracted.

## Intent-Tag Ratchet

The ratchet is green today and may only tighten. Baseline existing untagged tests, fail on new untagged tests, and fail when baseline entries have been fixed so the baseline cannot rot.

Python shape:

```python
"""Methodology enforcement gate. Test philosophy: Popperian."""
import ast
import pathlib

TESTS = pathlib.Path(__file__).resolve().parent
SELF = pathlib.Path(__file__).name
INTENT_TAGS = ("Falsifies:", "Regresses:", "Confirms:")
POPPER_BANNER = "Test philosophy: Popperian"
REGRESSION_CLASS = ("Regression", "BackwardCompat")
BASELINE = TESTS / "methodology_intent_baseline.txt"


def _doc(node):
    return ast.get_docstring(node) or ""


def _any(text, needles):
    return any(n in text for n in needles)


def _tests(tree):
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)) and sub.name.startswith("test"):
                    yield sub.name, _doc(sub), _doc(node), node.name
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test"):
            yield node.name, _doc(node), "", ""


def _scan():
    untagged = set()
    for path in sorted(TESTS.rglob("test_*.py")):
        if path.name == SELF:
            continue
        tree = ast.parse(path.read_text())
        file_doc = ast.get_docstring(tree) or ""
        file_intent = POPPER_BANNER in file_doc or _any(file_doc, INTENT_TAGS)
        for name, own, cdoc, cname in _tests(tree):
            tagged = (
                _any(own, INTENT_TAGS)
                or _any(cdoc, INTENT_TAGS)
                or POPPER_BANNER in cdoc
                or _any(cname, REGRESSION_CLASS)
                or file_intent
            )
            if not tagged:
                untagged.add(f"{path.name}::{name}")
    return untagged


def _baseline():
    return set(BASELINE.read_text().split()) if BASELINE.exists() else set()


def test_every_test_declares_intent():
    """Falsifies: 'a test can exist without an Axis-A intent tag'. Ratchet: may only shrink."""
    current = _scan()
    base = _baseline()
    new = sorted(current - base)
    fixed = sorted(base - current)
    problems = []
    if new:
        problems.append("NEW untagged test(s):\n  " + "\n  ".join(new))
    if fixed:
        problems.append("baseline entries now fixed; regenerate baseline:\n  " + "\n  ".join(fixed))
    assert not problems, "\n\n".join(problems)
```

