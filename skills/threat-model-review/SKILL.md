---
name: threat-model-review
description: Review application designs, trust boundaries, identity transitions, and threat scenarios. Use for design security reviews, architecture audits, and risk-based code-review planning.
license: Apache-2.0
---

# threat-model-review

## Steps
1. Collect supported architecture diagrams, entry points, security requirements, deployment boundaries, service identities, and data classifications. Mark inferred facts as hypotheses.
2. Enumerate users, administrators, services, outside systems, secrets, and security-sensitive state. Identify which actors control each input.
3. Draw a dataflow with trust-boundary annotations. For each crossing, ask which principal authenticates, who authorizes the operation, and where enforcement happens.
4. Use STRIDE as a structured brainstorming aid: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege. Do not mistake the list for proof of risks.
5. Record attack scenarios, affected security properties, existing controls, assumptions, likelihood qualifiers, and review priorities.
6. Ask a human to validate architectural assumptions. Send risky entry points to code review and document unanswered questions.

Use [threat model worksheet](references/model-worksheet.md). Do not invent network connectivity or credentials from names alone.
