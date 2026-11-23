import copy

import pytest

from security_skills.correlate import correlate
from security_skills.models import ValidationError, validate_finding
from security_skills.report import redact, render_json, render_markdown
from security_skills.sarif import normalize_sarif


def example(rule="rule-1", cwe="CWE-89", tool="First"):
    return {
        "id": "as-abcdef", "title": "Suspected injection", "description": "Needs review",
        "severity": "high", "confidence": "unknown", "status": "inconclusive",
        "cwe": cwe, "location": {"path": "api.py", "line": 4, "end_line": 4},
        "evidence": [{"kind": "scanner_message", "text": "Potential issue"}],
        "provenance": [{"tool": tool, "rule_id": rule}]
    }


def test_cross_scanner_correlation_preserves_all_sources():
    original = [example(), example("another-rule", tool="Second")]
    grouped = correlate(original)
    assert len(grouped) == 1
    assert {source["tool"] for source in grouped[0]["provenance"]} == {"First", "Second"}
    assert len(original[0]["provenance"]) == 1  # no mutation


def test_findings_without_shared_cwe_are_not_collapsed():
    assert len(correlate([example(cwe=None), example("rule-2", cwe=None)])) == 2


def test_invalid_finding_is_rejected():
    finding = example()
    finding["status"] = "invented"
    with pytest.raises(ValidationError):
        validate_finding(finding)


def test_redaction_best_effort():
    assert "super-secret" not in redact("password=super-secret")
    assert "ghp_" not in redact("ghp_" + "a" * 32)
    report = {"schema_version": "1.0", "findings": [example()]}
    assert "Suspected injection" in render_markdown(report)
    assert '"schema_version": "1.0"' in render_json(report)


def test_finding_status_is_not_escalated_by_normalization():
    raw = {"version": "2.1.0", "runs": [{"tool": {"driver": {"name": "Any"}},
                                             "results": [{"level": "error", "message": {"text": "credential=xyz"}}]}]}
    assert normalize_sarif(copy.deepcopy(raw))["findings"][0]["status"] == "inconclusive"
