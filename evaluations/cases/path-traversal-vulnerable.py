from pathlib import Path

def read_document(root: Path, name: str):
    return (root / name).read_text()
