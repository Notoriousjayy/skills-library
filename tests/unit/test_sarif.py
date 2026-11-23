import copy

import pytest

from security_skills.models import ValidationError, validate_report
from security_skills.sarif import normalize_sarif


@pytest.fixture
def sarif():
    return {
        "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {"name": "SyntheticScanner", "rules": [{
                "id": "sql-risk", "shortDescription": {"text": "Potential SQL injection"},
                "properties": {"tags": ["external/CWE-89"]}
            }]}},
            "results": [{
                "ruleId": "sql-risk", "level": "error",
                "message": {"text": "Flow may be unparameterized"},
                "locations": [{"physicalLocation": {
                    "artifactLocation": {"uri": "app.py"},
                    "region": {"startLine": 9, "endLine": 9}
                }}],
                "codeFlows": [{"threadFlows": []}]
            }]
        }]
    }


def test_normalize_keeps_flow_cwe_and_provenance(sarif):
    normalized = normalize_sarif(sarif)
    validate_report(normalized)
    finding = normalized["findings"][0]
    assert finding["cwe"] == "CWE-89"
    assert finding["severity"] == "high"
    assert finding["status"] == "inconclusive"
    assert finding["confidence"] == "unknown"
    assert finding["location"] == {"path": "app.py", "line": 9, "end_line": 9}
    assert finding["provenance"][0]["tool"] == "SyntheticScanner"
    assert finding["evidence"][1]["kind"] == "sarif_code_flows"
    assert finding["id"] == normalize_sarif(copy.deepcopy(sarif))["findings"][0]["id"]


@pytest.mark.parametrize("bad", [{}, {"version": "2.0.0", "runs": []},
                                {"version": "2.1.0", "runs": {}},
                                {"version": "2.1.0", "runs": [{"tool": {"driver": {}}}]}])
def test_malformed_sarif_raises(bad):
    with pytest.raises(ValidationError):
        normalize_sarif(bad)


def test_no_location_retains_missing_evidence():
    result = normalize_sarif({"version": "2.1.0", "runs": [{
        "tool": {"driver": {"name": "Test"}},
        "results": [{"ruleId": "x", "message": {"text": "hello"}}]
    }]})["findings"][0]
    assert result["location"]["line"] is None
    assert result["status"] == "inconclusive"
