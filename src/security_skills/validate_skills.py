"""Offline structural checks complement but do not replace official skills-ref."""

from __future__ import annotations

import re
from pathlib import Path

NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_skill(root: Path) -> list[str]:
    path = root / "SKILL.md"
    if not path.is_file():
        return [f"{root}: missing SKILL.md"]
    text = path.read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    if len(parts) != 3 or parts[0] != "":
        return [f"{path}: YAML frontmatter delimiters are missing"]
    # Skills in this library deliberately use plain single-line scalar YAML fields.
    fields = dict(line.split(":", 1) for line in parts[1].splitlines() if ":" in line)
    name = fields.get("name", "").strip()
    desc = fields.get("description", "").strip()
    problems = []
    if name != root.name or len(name) > 64 or not NAME.fullmatch(name):
        problems.append(f"{path}: invalid or mismatched name")
    if not desc or len(desc) > 1024:
        problems.append(f"{path}: missing or oversized description")
    if not parts[2].strip():
        problems.append(f"{path}: missing instructions")
    for relative in re.findall(r"\]\((references/[^)#]+|assets/[^)#]+|scripts/[^)#]+)\)", parts[2]):
        if not (root / relative).is_file():
            problems.append(f"{path}: missing reference: {relative}")
    return problems


def validate_library(root: Path) -> list[str]:
    if not root.is_dir():
        return ["skills directory is missing"]
    skills = [path for path in root.iterdir() if path.is_dir()]
    if not skills:
        return ["no skills found"]
    return [problem for skill in sorted(skills) for problem in validate_skill(skill)]
