import json
from pathlib import Path

from security_skills.cli import main
from security_skills.validate_skills import validate_library

ROOT = Path(__file__).parents[2]


def test_all_six_skills_valid():
    assert validate_library(ROOT / "skills") == []
    assert len([p for p in (ROOT / "skills").iterdir() if p.is_dir()]) == 6


def test_cli_pipeline(tmp_path):
    source = tmp_path / "scan.sarif"
    source.write_text(json.dumps({"version": "2.1.0", "runs": [{
        "tool": {"driver": {"name": "synthetic"}},
        "results": [{"ruleId": "x", "message": {"text": "review"}}]
    }]}))
    normalized = tmp_path / "normalized.json"
    report = tmp_path / "report.md"
    assert main(["normalize", str(source), "--output", str(normalized)]) == 0
    assert main(["report", str(normalized), "--format", "markdown", "--output", str(report)]) == 0
    assert "review" in report.read_text()
    assert main(["validate", str(ROOT / "skills")]) == 0


def test_cli_fails_on_invalid_json(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{")
    assert main(["normalize", str(bad)]) == 2


def test_twelve_synthetic_evaluation_cases_exist():
    cases = json.loads((ROOT / "evaluations" / "cases" / "index.json").read_text())["cases"]
    assert len(cases) == 12
    assert len({case["id"] for case in cases}) == 12
    for case in cases:
        assert (ROOT / "evaluations" / "cases" / case["file"]).is_file()
        assert case["ground_truth"] in {"vulnerable", "secure", "inconclusive", "structural"}
