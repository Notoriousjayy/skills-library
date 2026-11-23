from pathlib import Path


def read_document(root: Path, name: str):
    base = root.resolve()
    target = (base / name).resolve()
    if not target.is_relative_to(base):
        raise ValueError("outside authorized root")
    return target.read_text()
