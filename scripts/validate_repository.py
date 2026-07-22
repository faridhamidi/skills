#!/usr/bin/env python3
"""Validate the distributable Agent Skills repository."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote


FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", re.DOTALL)
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_DEFINITION = re.compile(r"^\s*\[([^\]]+)\]:\s*(\S+)", re.MULTILINE)
REFERENCE_USE = re.compile(r"(?<!!)\[([^\]]+)\]\[([^\]]*)\]")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
YAML_SCALAR = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
ARTIFACT_PATH = re.compile(
    r"(?<![A-Za-z0-9_])((?:\.\./)*(?:examples|scripts)/[A-Za-z0-9._/-]+)"
)


def parse_frontmatter(path: Path) -> dict[str, str]:
    match = FRONTMATTER.match(path.read_text())
    if not match:
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        scalar = YAML_SCALAR.match(line)
        if not scalar:
            continue
        value = scalar.group(2)
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[scalar.group(1)] = value
    return values


def markdown_anchor(heading: str) -> str:
    heading = re.sub(r"<[^>]+>", "", heading)
    heading = heading.replace("`", "").strip().lower()
    characters = [
        character
        for character in heading
        if character.isalnum() or character in {" ", "-", "_"}
    ]
    return re.sub(r"[ -]+", "-", "".join(characters)).strip("-")


def anchors_in(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in path.read_text().splitlines():
        match = HEADING.match(line)
        if not match:
            continue
        base = markdown_anchor(match.group(1))
        count = counts.get(base, 0)
        counts[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def markdown_files(root: Path) -> list[Path]:
    files = [root / "README.md"] if (root / "README.md").is_file() else []
    for directory in (root / "skills", root / "docs"):
        if directory.is_dir():
            files.extend(directory.rglob("*.md"))
    return sorted(set(files))


def split_link(raw_target: str) -> tuple[str, str]:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = target.split(maxsplit=1)[0]
    path, separator, fragment = target.partition("#")
    return unquote(path), unquote(fragment) if separator else ""


def validate_markdown_target(root: Path, markdown: Path, raw_target: str) -> list[str]:
    if raw_target.startswith(("http://", "https://", "mailto:", "data:")):
        return []
    relative_target, fragment = split_link(raw_target)
    target = markdown if not relative_target else markdown.parent / relative_target
    resolved_target = target.resolve()
    if not resolved_target.is_relative_to(root):
        return [f"{markdown.relative_to(root)}: local target is outside repository: {raw_target}"]
    skills_root = root / "skills"
    if markdown.is_relative_to(skills_root):
        skill_name = markdown.relative_to(skills_root).parts[0]
        skill_root = (skills_root / skill_name).resolve()
        if not resolved_target.is_relative_to(skill_root):
            return [
                f"{markdown.relative_to(root)}: local target is outside skill package: {raw_target}"
            ]
    if not target.exists():
        return [f"{markdown.relative_to(root)}: missing local target {raw_target}"]
    if not fragment:
        return []
    if not target.is_file() or target.suffix.lower() not in {".md", ".markdown"}:
        return [
            f"{markdown.relative_to(root)}: anchor target is not Markdown: {raw_target}"
        ]
    if fragment not in anchors_in(target):
        return [f"{markdown.relative_to(root)}: missing local anchor {raw_target}"]
    return []


def validate_markdown_links(root: Path) -> list[str]:
    errors: list[str] = []
    for markdown in markdown_files(root):
        text = markdown.read_text()
        for raw_target in MARKDOWN_LINK.findall(text):
            errors.extend(validate_markdown_target(root, markdown, raw_target))
        definitions = {
            identifier.casefold(): target
            for identifier, target in REFERENCE_DEFINITION.findall(text)
        }
        for raw_target in definitions.values():
            errors.extend(validate_markdown_target(root, markdown, raw_target))
        prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        prose = re.sub(r"`[^`]*`", "", prose)
        for label, identifier in REFERENCE_USE.findall(prose):
            normalized = (identifier or label).casefold()
            if normalized not in definitions:
                errors.append(
                    f"{markdown.relative_to(root)}: undefined reference-style link [{normalized}]"
                )
    return errors


def validate_skill_metadata(root: Path) -> list[str]:
    errors: list[str] = []
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return ["skills/: skill directory is missing"]
    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{skill_dir.relative_to(root)}: SKILL.md is missing")
            continue
        metadata = parse_frontmatter(skill_file)
        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if name != skill_dir.name:
            errors.append(
                f"{skill_file.relative_to(root)}: name {name!r} must match directory {skill_dir.name!r}"
            )
        if name and not SKILL_NAME.fullmatch(name):
            errors.append(f"{skill_file.relative_to(root)}: invalid skill name {name!r}")
        if not description or len(description) > 1024:
            errors.append(
                f"{skill_file.relative_to(root)}: description must contain 1-1024 characters"
            )
    return errors


def validate_artifact_references(root: Path) -> list[str]:
    errors: list[str] = []
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return []
    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        for markdown in skill_dir.rglob("*.md"):
            text = re.sub(r"https?://\S+", "", markdown.read_text())
            for relative_path in ARTIFACT_PATH.findall(text):
                relative_path = relative_path.rstrip(".,;:)")
                target = (
                    markdown.parent / relative_path
                    if relative_path.startswith("../")
                    else skill_dir / relative_path
                )
                if not target.exists():
                    errors.append(
                        f"{markdown.relative_to(root)}: missing claimed artifact {relative_path}"
                    )
    return errors


def validate_readme_registry(root: Path) -> list[str]:
    readme = root / "README.md"
    if not readme.is_file():
        return ["README registry: README.md is missing"]
    registry_rows = re.findall(
        r"^\|\s*\[([^\]]+)\]\(skills/([a-z0-9-]+)/\)\s*\|",
        readme.read_text(),
        re.MULTILINE,
    )
    registered = {target for _, target in registry_rows}
    errors = [
        f"README registry label {label!r} does not match target {target!r}"
        for raw_label, target in registry_rows
        if (label := raw_label.strip().strip("`")) != target
    ]
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return ["README registry cannot resolve missing skills/ directory"]
    actual = {
        path.name
        for path in skills_root.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    if registered == actual:
        return errors
    errors.append(
        "README registry does not match skills/: "
        f"missing={sorted(actual - registered)}, unknown={sorted(registered - actual)}"
    )
    return errors


def validate_steering_copies(root: Path) -> list[str]:
    errors: list[str] = []
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return []
    for assets in sorted(skills_root.glob("*/assets")):
        paths = [assets / name for name in ("steering.md", "AGENTS.md", "CLAUDE.md")]
        if not any(path.exists() for path in paths):
            continue
        if not all(path.is_file() for path in paths):
            errors.append(f"{assets.relative_to(root)}: steering copies are incomplete")
            continue
        if len({path.read_bytes() for path in paths}) != 1:
            errors.append(f"{assets.relative_to(root)}: steering copies differ")
    return errors


def parse_openai_interface(text: str) -> tuple[dict[str, str] | None, str | None]:
    lines = [line for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    if not lines or lines[0] != "interface:":
        return None, "interface mapping is missing"
    values: dict[str, str] = {}
    for line in lines[1:]:
        match = re.fullmatch(r"  ([A-Za-z_][A-Za-z0-9_]*):\s*(.+)", line)
        if not match:
            return None, f"malformed OpenAI metadata line: {line!r}"
        key = match.group(1)
        if key in values:
            return None, f"duplicate OpenAI metadata key: {key}"
        try:
            value = json.loads(match.group(2))
        except json.JSONDecodeError:
            return None, f"malformed OpenAI metadata scalar: {line!r}"
        if not isinstance(value, str):
            return None, f"OpenAI metadata value must be a quoted string: {line!r}"
        values[key] = value
    return values, None


def validate_openai_metadata(root: Path) -> list[str]:
    errors: list[str] = []
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return []
    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        metadata = skill_dir / "agents/openai.yaml"
        relative = metadata.relative_to(root)
        if not metadata.is_file():
            errors.append(f"{relative}: OpenAI metadata is missing")
            continue
        interface, parse_error = parse_openai_interface(metadata.read_text())
        if interface is None:
            errors.append(f"{relative}: {parse_error}")
            continue
        display_name = interface.get("display_name", "")
        short_description = interface.get("short_description", "")
        default_prompt = interface.get("default_prompt", "")
        if not display_name:
            errors.append(f"{relative}: display_name is missing")
        if not 25 <= len(short_description) <= 64:
            errors.append(f"{relative}: short_description must contain 25-64 characters")
        if f"${skill_dir.name}" not in default_prompt:
            errors.append(f"{relative}: default_prompt must mention ${skill_dir.name}")
    return errors


def validate_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors = []
    errors.extend(validate_skill_metadata(root))
    errors.extend(validate_markdown_links(root))
    errors.extend(validate_artifact_references(root))
    errors.extend(validate_readme_registry(root))
    errors.extend(validate_steering_copies(root))
    errors.extend(validate_openai_metadata(root))
    return sorted(errors)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    arguments = parser.parse_args(argv)
    errors = validate_repository(arguments.root)
    if errors:
        for error in errors:
            print(error)
        print(f"repository validation failed with {len(errors)} error(s)")
        return 1
    print("repository validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
