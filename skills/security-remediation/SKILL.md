---
name: security-remediation
description: Develop minimal security fixes and verify them with regression evidence. Use after reviewing an actionable vulnerability or when validating a proposed security patch.
license: Apache-2.0
---

# security-remediation

## Steps
1. Start with an evidence-backed issue; confirm impact, prerequisites, affected path, and intended security invariant. Ask for missing context rather than assuming exploitability.
2. Select the smallest change that enforces the invariant at the correct boundary. Prefer platform-standard safe APIs; address all equivalent call sites if supported by evidence.
3. Explain compatibility, migrations, error handling, performance, and security tradeoffs. Never replace a finding with suppression or a purely cosmetic guard.
4. Propose positive and negative regression tests, including boundary values and unauthorized actors. Prepare a verification matrix.
5. Obtain approval before modifying files, running test suites, installing tools, opening network connections, or applying production changes.
6. When authorized, record exact commands, exit status, failing checks, code revisions, and residual uncertainty. Mark remediation verified only with relevant observed evidence.

See [remediation playbook](references/fix-verification.md). A recommended fix is not a verified fix.
