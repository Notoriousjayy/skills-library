"""Conservative SARIF 2.1.0 normalization. Tool findings remain unverified hypotheses."""

from __future__ import annotations

import re
from typing import Any

from .models import SCHEMA_VERSION, ValidationError, require_list, require_mapping, stable_id

_CWE_RE = re.compile(r"CWE-(\d+)", re.IGNORECASE)


def _message(value: Any) -> str:
    if isinstance(value, dict):
        return str(value.get("text") or value.get("markdown") or "")
    return ""


def _location(result: dict[str, Any]) -> dict[str, Any]:
    locations = result.get("locations", [])
    if not isinstance(locations, list):
        raise ValidationError("result.locations must be an array")
    if not locations:
        return {"path": "", "line": None, "end_line": None}
    primary = require_mapping(locations[0], "result.locations[0]")
    physical = require_mapping(primary.get("physicalLocation", {}), "physicalLocation")
    artifact = require_mapping(physical.get("artifactLocation", {}), "artifactLocation")
    region = require_mapping(physical.get("region", {}), "region")
    path = artifact.get("uri", "")
    if not isinstance(path, str):
        raise ValidationError("artifactLocation.uri must be a string")
    return {"path": path, "line": region.get("startLine"), "end_line": region.get("endLine")}


def _cwe(rule: dict[str, Any], result: dict[str, Any]) -> str | None:
    candidates: list[str] = []
    for item in (rule.get("id"), result.get("ruleId")):
        if isinstance(item, str):
            candidates.append(item)
    for taxonomy in (rule.get("relationships", []), result.get("taxa", [])):
        if not isinstance(taxonomy, list):
            continue
        for entry in taxonomy:
            if isinstance(entry, dict):
                target = entry.get("target", entry)
                if isinstance(target, dict):
                    candidates.append(str(target.get("id", "")))
    tags = rule.get("properties", {}).get("tags", []) if isinstance(rule.get("properties"), dict) else []
    if isinstance(tags, list):
        candidates.extend(str(tag) for tag in tags)
    for candidate in candidates:
        match = _CWE_RE.search(candidate)
        if match:
            return f"CWE-{int(match.group(1))}"
    return None


def _severity(level: object) -> str:
    return {"error": "high", "warning": "medium", "note": "note", "none": "unknown"}.get(
        level, "unknown"
    )


def normalize_sarif(document: Any) -> dict[str, Any]:
    root = require_mapping(document, "SARIF")
    if root.get("version") != "2.1.0":
        raise ValidationError("expected SARIF version 2.1.0")
    if root.get("$schema") is not None and not isinstance(root["$schema"], str):
        raise ValidationError("SARIF $schema must be a string")
    findings: list[dict[str, Any]] = []
    for run_idx, raw_run in enumerate(require_list(root.get("runs"), "SARIF.runs")):
        run = require_mapping(raw_run, f"runs[{run_idx}]")
        tool = require_mapping(run.get("tool"), "run.tool")
        driver = require_mapping(tool.get("driver"), "run.tool.driver")
        scanner = driver.get("name")
        if not isinstance(scanner, str) or not scanner:
            raise ValidationError("run.tool.driver.name is required")
        rules_raw = require_list(driver.get("rules", []), "driver.rules")
        rules = {}
        for raw_rule in rules_raw:
            rule = require_mapping(raw_rule, "driver.rules[]")
            if isinstance(rule.get("id"), str):
                rules[rule["id"]] = rule
        for index, raw_result in enumerate(require_list(run.get("results", []), "run.results")):
            result = require_mapping(raw_result, f"run.results[{index}]")
            rule_id = result.get("ruleId", "unclassified")
            if not isinstance(rule_id, str):
                raise ValidationError("result.ruleId must be a string")
            rule = rules.get(rule_id, {})
            desc = _message(result.get("message"))
            if not desc:
                desc = f"Tool reported rule {rule_id}; message not provided"
            location = _location(result)
            config = rule.get("defaultConfiguration", {})
            if not isinstance(config, dict):
                raise ValidationError("rule.defaultConfiguration must be an object")
            raw_level = result.get("level", config.get("level", "warning"))
            fingerprints = result.get("partialFingerprints", {})
            if not isinstance(fingerprints, dict):
                raise ValidationError("result.partialFingerprints must be an object")
            if not isinstance(raw_level, str):
                raise ValidationError("result.level must be a string")
            evidence = [{"kind": "scanner_message", "text": desc}]
            if result.get("codeFlows"):
                evidence.append({"kind": "sarif_code_flows", "data": result["codeFlows"]})
            if result.get("relatedLocations"):
                evidence.append({"kind": "sarif_related_locations", "data": result["relatedLocations"]})
            title = _message(rule.get("shortDescription")) or rule_id
            finding_id = stable_id(scanner, rule_id, location, sorted(fingerprints.items()), desc)
            findings.append({
                "id": finding_id, "title": title, "description": desc,
                "severity": _severity(raw_level), "confidence": "unknown",
                "status": "inconclusive", "cwe": _cwe(rule, result),
                "location": location, "evidence": evidence,
                "provenance": [{"tool": scanner, "rule_id": rule_id,
                                "run_index": run_idx, "result_index": index,
                                "fingerprints": fingerprints}],
                "remediation": None, "verification": None,
                "assumptions": ["Scanner output is not proof of exploitability"],
            })
    return {"schema_version": SCHEMA_VERSION, "findings": findings,
            "metadata": {"source": "SARIF 2.1.0", "verification": "not performed"}}
