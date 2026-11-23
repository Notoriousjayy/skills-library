"""Minimal deterministic report renderers with best-effort credential redaction."""

from __future__ import annotations

import json
import re
from typing import Any

from .models import validate_report

_PATTERNS = [
    (re.compile(r"\b(?:ghp_|gho_|ghs_|ghu_)\w{20,}"), "[REDACTED_TOKEN]"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"), "[REDACTED_TOKEN]"),
    (re.compile(r"(?i)\b(password|api[_-]?key|secret|token)\s*[:=]\s*['\"]?[^\s,'\";]+"),
     r"\1=[REDACTED]"),
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]{8,}"), "Bearer [REDACTED]"),
]


def redact(value: str) -> str:
    for pattern, replacement in _PATTERNS:
        value = pattern.sub(replacement, value)
    return value


def _sanitize(value: Any) -> Any:
    if isinstance(value, str):
        return redact(value)
    if isinstance(value, list):
        return [_sanitize(item) for item in value]
    if isinstance(value, dict):
        return {key: _sanitize(val) for key, val in value.items()}
    return value


def render_json(report: dict[str, Any]) -> str:
    validate_report(report)
    return json.dumps(_sanitize(report), indent=2, sort_keys=True) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    validate_report(report)
    lines = ["# Security Assessment Findings", "", "Tool output is unverified until reviewed.", "",
             f"Findings: **{len(report['findings'])}**", ""]
    for finding in report["findings"]:
        location = finding["location"]
        at = f"{location['path']}:{location['line'] or '?'}"
        title = redact(finding["title"]).replace("\n", " ")
        lines.extend([f"## {title}", "", f"- ID: `{finding['id']}`",
                      f"- Location: `{redact(at)}`",
                      f"- Severity: **{finding['severity']}**; confidence: **{finding['confidence']}**",
                      f"- Validation: **{finding['status']}**",
                      f"- CWE: {finding.get('cwe') or 'Not established'}", "",
                      redact(finding["description"]), "",
                      "**Evidence:**", ""])
        for evidence in finding["evidence"]:
            kind = evidence.get("kind", "unknown") if isinstance(evidence, dict) else "unknown"
            details = evidence.get("text", "Structured details preserved in JSON") if isinstance(evidence, dict) else str(evidence)
            lines.append(f"- {kind}: {redact(str(details))}")
        lines.extend(["", "**Remediation:** " + redact(str(finding.get("remediation") or "Requires contextual assessment")),
                      "", "**Verification:** " + redact(str(finding.get("verification") or "Not performed")), ""])
    lines.append("_Redaction is best-effort: review output before distributing._")
    return "\n".join(lines) + "\n"
