# Architecture Boundaries

Use the boundary pattern when a rule says a seam must not be bypassed: only one adapter may construct a client, pure code may not import infrastructure, the domain may not read the clock, or layers may not import inward/outward across a line.

Boundary tests are static fitness functions. They parse source and fail CI when the architecture is violated without executing production behavior.

## Three Layers

1. Scanner: pure function, source string to `list[Finding]`, no filesystem access.
2. Manifest: explicit file-to-category classification and sanctioned-owner exemptions.
3. Tests: meta-test the scanner on synthetic source, then apply it to real files through the manifest.

## Scanner Rules

- Use the language's parser or AST, not string grep, when practical.
- The scanner receives source text and a module name, not a path.
- Emit stable findings with a machine code, module name, line number, and detail.
- Keep scanner logic free of repository paths so synthetic meta-tests can exercise it.

Python skeleton:

```python
import ast
from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    code: str
    module_name: str
    lineno: int
    detail: str

    def format(self) -> str:
        return f"{self.module_name}:{self.lineno} {self.detail}"


def _parse(source: str, *, module_name: str) -> ast.Module:
    try:
        return ast.parse(source)
    except SyntaxError as error:
        raise AssertionError(f"{module_name}:{error.lineno or 1} cannot be parsed") from error
```

## Manifest Rules

- The manifest is the only layer that knows real paths.
- Prefer explicit sets of files over folder globs.
- Add a classification-completeness test so every production file is classified exactly once.
- Exempt only the sanctioned adapter/owner for single-owner rules.

## Mandatory Scanner Meta-Tests

Every scanner gets:

- a must-catch test with synthetic bad source;
- a must-not-false-positive test with synthetic clean source.

```python
def test_forbidden_import_scanner_catches_violation():
    """Falsifies: 'the scanner passes when a forbidden import is present'."""
    source = "import boto3\nfrom os import path\n"
    assert _codes(audit_forbidden_imports(source, module_name="x.py")) == {"forbidden_import"}


def test_forbidden_import_scanner_allows_clean_source():
    """Confirms: ordinary domain imports are not flagged."""
    source = "from dataclasses import dataclass\nimport logging\n"
    assert audit_forbidden_imports(source, module_name="x.py") == []
```

## Real-File Enforcement

The real-file test loops over manifest files, applies the scanner, and asserts the formatted violation list is empty or equals a temporary forward-lock baseline.

Add a seeded mutation test when possible: take a real clean file, append or inject a known-bad snippet in memory, and assert the scanner catches it. This proves the real-file enforcement path can actually fail.

