from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Case:
    id: str
    fixture: Path
    prompt: str
    project_test_command: tuple[str, ...]
    oracle: Path
    failure_token: str

    @classmethod
    def load(cls, path: Path, repo_root: Path) -> "Case":
        data = json.loads(path.read_text())
        required = {
            "id",
            "fixture",
            "prompt",
            "project_test_command",
            "oracle",
            "failure_token",
        }
        missing = sorted(required - data.keys())
        if missing:
            raise ValueError(f"case is missing required fields: {', '.join(missing)}")

        root = repo_root.resolve()
        fixture = _inside_root(root, data["fixture"], "fixture")
        oracle = _inside_root(root, data["oracle"], "oracle")
        if not fixture.is_dir():
            raise ValueError(f"fixture is not a directory: {fixture}")
        if not oracle.is_file():
            raise ValueError(f"oracle is not a file: {oracle}")
        command = data["project_test_command"]
        if not isinstance(command, list) or not command or not all(
            isinstance(item, str) and item for item in command
        ):
            raise ValueError("project_test_command must be a non-empty string list")

        return cls(
            id=str(data["id"]),
            fixture=fixture,
            prompt=str(data["prompt"]),
            project_test_command=tuple(command),
            oracle=oracle,
            failure_token=str(data["failure_token"]),
        )


def _inside_root(root: Path, value: str, label: str) -> Path:
    candidate = (root / value).resolve()
    if not candidate.is_relative_to(root):
        raise ValueError(f"{label} escapes repository root: {value}")
    return candidate
