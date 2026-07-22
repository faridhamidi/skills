from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import time
import uuid

from .case import Case
from .validation import render_diff, validate_artifact


VALID_CONDITIONS = {"control", "treatment"}


def run_trial(
    *,
    case: Case,
    condition: str,
    output_dir: Path,
    repo_root: Path,
    command_template=None,
    model: str | None = None,
    timeout: int = 600,
    source_codex_home: Path | None = None,
) -> dict:
    if condition not in VALID_CONDITIONS:
        raise ValueError(f"unknown condition: {condition}")
    if timeout <= 0:
        raise ValueError("timeout must be positive")

    run_name = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + f"-{uuid.uuid4().hex[:8]}"
    result_dir = output_dir / case.id / condition / run_name
    result_dir.mkdir(parents=True, exist_ok=False)

    with tempfile.TemporaryDirectory(prefix="ptm-eval-") as temporary:
        temporary_path = Path(temporary)
        workspace = temporary_path / "workspace"
        codex_home = temporary_path / "codex-home"
        shutil.copytree(case.fixture, workspace, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        codex_home.mkdir()

        if command_template is None:
            _prepare_codex_home(
                codex_home=codex_home,
                condition=condition,
                repo_root=repo_root,
                source_codex_home=source_codex_home,
            )
            command = _codex_command(workspace, case.prompt, model)
        else:
            command = _render_command(command_template, workspace, case.prompt, condition)

        environment = os.environ.copy()
        environment["CODEX_HOME"] = str(codex_home)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        started = time.monotonic()
        timed_out = False
        try:
            completed = subprocess.run(
                command,
                cwd=workspace,
                env=environment,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            returncode = completed.returncode
            stdout = completed.stdout
            stderr = completed.stderr
        except subprocess.TimeoutExpired as error:
            timed_out = True
            returncode = None
            stdout = _decode_timeout_output(error.stdout)
            stderr = _decode_timeout_output(error.stderr)
        duration = time.monotonic() - started

        validation = validate_artifact(case, case.fixture, workspace)
        shutil.copytree(workspace, result_dir / "artifact")
        (result_dir / "agent.stdout.txt").write_text(stdout)
        (result_dir / "agent.stderr.txt").write_text(stderr)
        (result_dir / "changes.diff").write_text(render_diff(case.fixture, workspace))
        result = {
            "case": case.id,
            "condition": condition,
            "result_dir": str(result_dir.resolve()),
            "agent": {
                "command": command,
                "returncode": returncode,
                "timed_out": timed_out,
                "duration_seconds": round(duration, 3),
            },
            "validation": validation,
        }
        (result_dir / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True))
        return result


def _prepare_codex_home(
    *,
    codex_home: Path,
    condition: str,
    repo_root: Path,
    source_codex_home: Path | None,
) -> None:
    source = source_codex_home or Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    auth = source / "auth.json"
    if not auth.is_file():
        raise FileNotFoundError(f"Codex authentication file not found: {auth}")
    shutil.copy2(auth, codex_home / "auth.json")
    if condition == "treatment":
        skill_source = repo_root / "skills/ptm"
        if not skill_source.is_dir():
            raise FileNotFoundError(f"PTM skill not found: {skill_source}")
        shutil.copytree(skill_source, codex_home / "skills/ptm")


def _codex_command(workspace: Path, prompt: str, model: str | None) -> list[str]:
    command = [
        "codex",
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--skip-git-repo-check",
        "--sandbox",
        "workspace-write",
        "--cd",
        str(workspace),
    ]
    if model:
        command.extend(["--model", model])
    command.append(prompt)
    return command


def _render_command(template, workspace: Path, prompt: str, condition: str) -> list[str]:
    parts = shlex.split(template) if isinstance(template, str) else list(template)
    values = {
        "workspace": str(workspace),
        "prompt": prompt,
        "condition": condition,
    }
    return [part.format(**values) for part in parts]


def _decode_timeout_output(value) -> str:
    if value is None:
        return ""
    return value.decode(errors="replace") if isinstance(value, bytes) else value
