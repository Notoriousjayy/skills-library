# Skill interoperability

All six directories are independent standards-compliant Agent Skills. `secure-code-review` is the coordinating procedure, not a proprietary subagent dispatcher. Clients with skill discovery may select the relevant skill by name/description; clients without discovery can load the specific SKILL.md manually.

## Inputs and outputs

Inputs: repository source/revision, human-authorized scope, optional diagrams, and optional existing SAST reports. Outputs: a structured `schema_version: "1.0"` JSON document (see `security_skills.models`) plus review narrative and verification plan. For each finding, maintain provenance from each scanner or manual audit.

## Routing

- Architecture/design-only questions → `threat-model-review`.
- Existing SARIF findings and false-positive triage → `static-analysis-triage`.
- Memory-unsafe language and FFI code → `memory-safety-audit`.
- Web/API handlers, sessions, injection and authorization → `web-security-review`.
- Existing confirmed/likely finding and authorized patch work → `security-remediation`.
- Cross-cutting end-to-end assessment → `secure-code-review`.

When an optional capability is unavailable, follow the primary workflow and report the missing specialized analysis. Conflicting findings must be kept until adjudicated. No action is delegated or executed solely because one skill mentions another.

## Platform notes

Codex, Claude Code, and other coding agents can use the core SKILL.md format when their installed versions support the standard. Actual skill discovery paths, scripting permissions, and inter-skill execution vary by runtime; consult current client documentation rather than assuming universal automation.
