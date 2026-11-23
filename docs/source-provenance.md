# Source provenance and licensing

**Foundational sources (conceptual use only):**

- Brian Chess and Jacob West, *Secure Programming with Static Analysis*, Addison-Wesley, 2007, ISBN 0-321-42477-8. Informs source-to-sink reasoning, taint propagation concepts, analyzer limitations, result triage, and secure coding principles.
- Mark Dowd, John McDonald and Justin Schuh, *The Art of Software Security Assessment: Identifying and Preventing Software Vulnerabilities*, Addison-Wesley, 2006, ISBN 0-321-44442-6. Informs design review, assessment scoping, audit planning, trust relationships and vulnerability reasoning.

The **EDSAW** name, workflow wording, implementation, templates, fixtures, and reference texts are independently created. We do not redistribute original PDFs, chapters, figures, or verbatim code listings. Citation does not grant permission to reproduce copyrighted material.

**Contemporary primary sources (verify before version-sensitive mapping):**

- [Agent Skills specification](https://agentskills.io/specification) — skill format.
- [MITRE CWE](https://cwe.mitre.org/) — weakness identifiers, not automatic CVEs.
- [OWASP ASVS 5.0.0](https://asvs.owasp.org/) — verification requirements, not inferred mappings.
- [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/).
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/).
- [NIST SSDF publications](https://csrc.nist.gov/Projects/ssdf/publications) — SP 800-218 v1.1 final; as of November 2026 the v1.2 listing is draft.
- [SEI CERT C](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard) and [CERT C++](https://wiki.sei.cmu.edu/confluence/display/cplusplus/SEI+CERT+C%2B%2B+Coding+Standard).
- [SARIF 2.1.0 standard](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html).
- [Semgrep documentation](https://semgrep.dev/docs/), [CodeQL documentation](https://codeql.github.com/docs/), [Bandit documentation](https://bandit.readthedocs.io/).

The bundled tool consumes compatible SARIF reports but does **not** run or bundle Semgrep, CodeQL, or Bandit. Control mappings must be verified against the exact standard version and code evidence.
