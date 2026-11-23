import pytest

from security_skills.evaluate import score, score_document
from security_skills.inventory import inventory
from security_skills.models import ValidationError


def test_inventory_read_only_skips_symlink(tmp_path):
    (tmp_path / "a.py").write_text("print('test')")
    (tmp_path / "file.txt").write_text("text")
    (tmp_path / "linked.py").symlink_to(tmp_path / "a.py")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "should_skip.c").write_text("x")
    result = inventory(tmp_path)
    assert result["files"] == [{"path": "a.py", "language": "Python"}]
    assert result["execution"] == "none"


def test_score_is_labeled_and_deterministic():
    result = score(["a", "b"], ["b", "c"])
    assert result == {"tp": 1, "fp": 1, "fn": 1, "precision": 0.5, "recall": 0.5, "f1": 0.5}
    assert score_document({"expected": ["a"], "predicted": ["a"]})["f1"] == 1.0
    with pytest.raises(ValidationError):
        score(["x", "x"], [])
