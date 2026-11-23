# Architecture

```mermaid
flowchart TD
  U[User authorization and scope] --> H[Agent harness: controls execution]
  H --> P[Primary secure-code-review skill]
  P -. optional instructions .-> T[Threat model review]
  P -. optional instructions .-> S[Static analysis triage]
  P -. optional instructions .-> M[Memory safety audit]
  P -. optional instructions .-> W[Web security review]
  P -. optional instructions .-> R[Security remediation]
  S --> J[Normalized finding contract v1.0]
  T --> J
  M --> J
  W --> J
  R --> J
  J --> Q[Validation and human review]
  Q --> O[JSON and Markdown report]
```

The model proposes conclusions and actions. The harness, user permissions, and external tools control execution. The skill description triggers activation; `SKILL.md` gives scoped instructions and optional references load on demand. There is no built-in cross-skill invocation protocol. The Python package provides deterministic SARIF parsing, correlation, inventory, reporting, evaluation scoring and structural checks. It is **not** a standalone SAST scanner.

**Data boundary:** target source and analyzer output are untrusted inputs. **Execution boundary:** source review defaults to read-only. **Reporting boundary:** machine assertions about vulnerabilities require source-level evidence and human validation. **Sharing boundary:** do not export secrets or private code without permission.
