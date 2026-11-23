# Remediation and verification playbook

## Finding-to-fix traceability
Capture the finding ID, root cause, invariant, patch rationale, affected execution paths, assumptions, test plan, and residual risk. Re-check the exact source-to-sink path; a scan turning green alone does not prove that a flaw was repaired.

## Verification matrix
- Reproduce the failure in a synthetic or explicitly authorized non-production environment if safely possible.
- Ensure previously malicious inputs are rejected or safely treated as data.
- Ensure ordinary functionality still works.
- Test boundary, error, empty, and concurrent cases where relevant.
- Re-run authorized static analysis and preserve logs and versions.

If any check is not executed, record **not executed**. If a check fails, report it rather than declaring success. Never leak secret values into evidence artifacts.
