import ast
import difflib
from hashlib import sha256
import os
from pathlib import Path
import re
import subprocess
import sys

from .case import Case


IGNORED_PARTS = {".git", "__pycache__"}
INTENT_TAG = re.compile(r"\b(?:Falsifies|Regresses|Confirms):")


def snapshot_tree(root: Path) -> dict[str, str]:
    snapshot = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        relative = path.relative_to(root).as_posix()
        snapshot[relative] = sha256(path.read_bytes()).hexdigest()
    return snapshot


def validate_artifact(case: Case, baseline: Path, artifact: Path) -> dict:
    baseline_snapshot = snapshot_tree(baseline)
    artifact_snapshot = snapshot_tree(artifact)
    changed_files = sorted(
        path
        for path in baseline_snapshot.keys() | artifact_snapshot.keys()
        if baseline_snapshot.get(path) != artifact_snapshot.get(path)
    )
    project_tests = _run(case.project_test_command, artifact)
    hidden_oracle = _run((sys.executable, str(case.oracle), str(artifact)), artifact)
    baseline_tests = _test_functions(baseline)
    artifact_tests = _test_functions(artifact)
    new_test_ids = sorted(artifact_tests.keys() - baseline_tests.keys())
    tag_counts = {test_id: artifact_tests[test_id]["tag_count"] for test_id in new_test_ids}
    changed_test_text = "\n".join(
        (artifact / path).read_text(errors="replace")
        for path in changed_files
        if path.startswith("tests/") and path.endswith(".py") and (artifact / path).is_file()
    )

    return {
        "project_tests": project_tests,
        "hidden_oracle": hidden_oracle,
        "changed_files": changed_files,
        "new_tests": new_test_ids,
        "fault_injection_present": bool(new_test_ids)
        and case.failure_token in changed_test_text,
        "intent_tags": {
            "passed": bool(new_test_ids) and all(count == 1 for count in tag_counts.values()),
            "counts": tag_counts,
        },
    }


def render_diff(baseline: Path, artifact: Path) -> str:
    before = snapshot_tree(baseline)
    after = snapshot_tree(artifact)
    sections = []
    for relative in sorted(before.keys() | after.keys()):
        if before.get(relative) == after.get(relative):
            continue
        old_path = baseline / relative
        new_path = artifact / relative
        try:
            old_lines = old_path.read_text().splitlines(keepends=True) if old_path.exists() else []
            new_lines = new_path.read_text().splitlines(keepends=True) if new_path.exists() else []
        except UnicodeDecodeError:
            sections.append(f"Binary file changed: {relative}\n")
            continue
        sections.extend(
            difflib.unified_diff(
                old_lines,
                new_lines,
                fromfile=f"a/{relative}",
                tofile=f"b/{relative}",
            )
        )
    return "".join(sections)


def _run(command, cwd: Path) -> dict:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        list(command),
        cwd=cwd,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "passed": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def _test_functions(root: Path) -> dict[str, dict[str, int]]:
    tests = {}
    test_root = root / "tests"
    if not test_root.exists():
        return tests
    for path in sorted(test_root.rglob("test*.py")):
        source = path.read_text(errors="replace")
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        lines = source.splitlines()
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not node.name.startswith("test"):
                continue
            relative = path.relative_to(root).as_posix()
            tests[f"{relative}::{node.name}"] = {
                "tag_count": _declared_intent_tag_count(node, lines)
            }
    return tests


def _declared_intent_tag_count(node, lines: list[str]) -> int:
    declarations = [ast.get_docstring(node, clean=False) or ""]
    declaration_line = min(
        [node.lineno, *(decorator.lineno for decorator in node.decorator_list)]
    )
    preceding_comments = []
    index = declaration_line - 2
    while index >= 0 and lines[index].lstrip().startswith("#"):
        preceding_comments.append(lines[index])
        index -= 1
    declarations.extend(reversed(preceding_comments))
    return len(INTENT_TAG.findall("\n".join(declarations)))
