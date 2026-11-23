# Evidence-Driven Secure Assessment Workflow (EDSAW)

Original seven-phase review procedure built for portable AI coding agents.

1. **Scope and inventory:** capture repository revision and baseline, assets, languages, authorized tools, services, and exclusions. No implicit execution.
2. **Architecture:** map actors, dataflows, privilege transitions and trust boundaries. Explicitly flag inferred vs confirmed architecture.
3. **Automated analysis:** ingest permitted SAST output, record scanner names/configuration, normalize to finding schema. Scan only if separately approved.
4. **Contextual audit:** inspect concrete paths from untrusted input through transformations, guards and sanitizers to sensitive operations; examine alternative control and exception paths.
5. **Evidence validation:** determine confirmed/likely/inconclusive/false_positive status with file and line evidence. Do not conflate scanner confidence, severity, or exploitability.
6. **Remediation engineering:** propose minimal fixes enforcing the security invariant, design negative/positive tests, assess compatibility and regression risks; modification requires approval.
7. **Verification and reporting:** record exactly which checks were run, summarize resolved and unresolved risk, produce structured and human-readable findings, and identify limitations.

**Required record per finding:** unique stable ID, title, affected location, severity, confidence, validation status, evidence, analyzer provenance, CWE if established, remediation, and verification steps. Additional rich fields are allowed; see the primary skill's finding contract.
