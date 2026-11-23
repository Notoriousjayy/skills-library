# Dataflow and SAST triage

Identify the external source and its controllability, each transformation, and the sink's security-sensitive operation. A sanitizer is specific to its downstream context: SQL parameter binding does not imply safe shell command construction. Check alternative data paths, guards, exception branches, and interprocedural aliases.

Case classification: **confirmed** if direct code evidence establishes the violated invariant; **likely** if a plausible unmitigated path exists but prerequisites remain; **inconclusive** when context is missing; **false_positive** only when specific code evidence disproves the rule for the case. Explain why in the finding's evidence.

The normalization utility supports SARIF 2.1.0 inputs and preserves codeFlows and relatedLocations when supplied. No flow reconstruction is performed. It preserves original scanner attribution and does not claim to verify exploitability. Correlation by matching CWE/path/line is heuristic; inspect merged findings before action. Tool severities are provisional and cannot be mapped directly to CVSS.
