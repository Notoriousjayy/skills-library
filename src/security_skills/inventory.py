"""Read-only repository inventory; never follows symlinks or executes project code."""

from __future__ import annotations

import os
from pathlib import Path

EXTENSIONS = {".py": "Python", ".c": "C", ".h": "C/C++", ".cc": "C++",
              ".cpp": "C++", ".java": "Java", ".js": "JavaScript",
              ".jsx": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript",
              ".rs": "Rust", ".go": "Go", ".php": "PHP"}
IGNORE = {".git", ".venv", "venv", "node_modules", "dist", "build", "__pycache__"}


def inventory(root: Path) -> dict[str, object]:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("inventory root must be a directory")
    files = []
    for current, dirs, filenames in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in IGNORE and
                         not (Path(current) / d).is_symlink())
        for filename in sorted(filenames):
            path = Path(current) / filename
            if path.is_symlink() or not path.is_file():
                continue
            lang = EXTENSIONS.get(path.suffix.lower())
            if lang:
                files.append({"path": path.relative_to(root).as_posix(), "language": lang})
    counts: dict[str, int] = {}
    for record in files:
        counts[record["language"]] = counts.get(record["language"], 0) + 1
    return {"languages": counts, "files": files, "execution": "none"}
