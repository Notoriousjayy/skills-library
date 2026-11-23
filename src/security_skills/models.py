"""Shared finding contract and conservative data validation."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

SCHEMA_VERSION = "1.0"
STATUSES = frozenset({"confirmed", "likely", "inconclusive", "false_positive"})
CONFIDENCES = frozenset({"high", "medium", "low", "unknown"})
SEVERITIES = frozenset({"critical", "high", "medium", "low", "note", "unknown"})
CWE_PATTERN = re.compile(r"^CWE-\d+$")


class ValidationError(ValueError):
    """Malformed external data or an invalid normalized report."""


def require_mapping(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{context} must be an object")
    return value


def require_list(value: Any, context: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValidationError(f"{context} must be an array")
    return value


def stable_id(*components: object) -> str:
    data = json.dumps(components, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return "as-" + hashlib.sha256(data.encode("utf-8")).hexdigest()[:16]


def validate_finding(finding: Any) -> dict[str, Any]:
    finding = require_mapping(finding, "finding")
    required = {"id", "title", "description", "severity", "confidence", "status", "location", "evidence", "provenance"}
    missing = required - set(finding)
    if missing:
        raise ValidationError("missing finding fields: " + ", ".join(sorted(missing)))
    for name in ("id", "title", "description"):
        if not isinstance(finding[name], str) or not finding[name].strip():
            raise ValidationError(f"finding.{name} must be a nonempty string")
    for name, allowed in (("severity", SEVERITIES), ("confidence", CONFIDENCES), ("status", STATUSES)):
        if finding[name] not in allowed:
            raise ValidationError(f"finding.{name} is invalid")
    location = require_mapping(finding["location"], "finding.location")
    if not isinstance(location.get("path"), str):
        raise ValidationError("finding.location.path must be a string")
    for key in ("line", "end_line"):
        value = location.get(key)
        if value is not None and (type(value) is not int or value < 1):
            raise ValidationError(f"finding.location.{key} must be a positive integer or null")
    if (location.get("line") and location.get("end_line") and
            location["end_line"] < location["line"]):
        raise ValidationError("end_line precedes line")
    require_list(finding["evidence"], "finding.evidence")
    require_list(finding["provenance"], "finding.provenance")
    if not finding["provenance"]:
        raise ValidationError("finding.provenance cannot be empty")
    cwe = finding.get("cwe")
    if cwe is not None and (not isinstance(cwe, str) or not CWE_PATTERN.fullmatch(cwe)):
        raise ValidationError("finding.cwe must be null or a CWE-<number> identifier")
    return finding


def validate_report(report: Any) -> dict[str, Any]:
    report = require_mapping(report, "report")
    if report.get("schema_version") != SCHEMA_VERSION:
        raise ValidationError(f"schema_version must equal {SCHEMA_VERSION}")
    for finding in require_list(report.get("findings"), "report.findings"):
        validate_finding(finding)
    return report
