"""Evidence-preserving correlation; only combine findings with specific matching evidence."""

from __future__ import annotations

import copy
from typing import Any

from .models import validate_finding


def correlate(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], dict[str, Any]] = {}
    for original in findings:
        finding = copy.deepcopy(validate_finding(original))
        location = finding["location"]
        # Cross-tool correlation is only justified when an explicit CWE and exact source
        # line are shared. Otherwise use the same tool and rule as a conservative key.
        cwe = finding.get("cwe")
        if cwe and location["path"] and location["line"]:
            key = ("cwe-location", cwe, location["path"], location["line"])
        else:
            source = finding["provenance"][0]
            key = ("tool-rule", source.get("tool"), source.get("rule_id"),
                   location["path"], location["line"], finding["description"])
        if key not in groups:
            groups[key] = finding
        else:
            current = groups[key]
            current["provenance"].extend(finding["provenance"])
            current["evidence"].extend(finding["evidence"])
            current["confidence"] = "unknown"
            current["status"] = "inconclusive"
            current.setdefault("assumptions", []).append(
                "Correlated results require independent source-code validation"
            )
            if current["severity"] != finding["severity"]:
                current["severity"] = "unknown"  # avoid silently choosing a score
    return list(groups.values())
