# Open Agent Security Skills Library

Six portable [Agent Skills](https://agentskills.io/specification) for evidence-driven application security review. `secure-code-review` is the entry point; the five neighboring skills can run independently. All methodology, examples, and code in this repository are original; source books are **not** bundled.

## Skills

| Skill | Trigger |
| --- | --- |
| [`secure-code-review`](skills/secure-code-review/SKILL.md) | Full repository / PR security review and assessment reporting |
| [`static-analysis-triage`](skills/static-analysis-triage/SKILL.md) | SARIF, SAST, source-to-sink triage |
| [`threat-model-review`](skills/threat-model-review/SKILL.md) | Architecture, trust boundaries, design review |
| [`memory-safety-audit`](skills/memory-safety-audit/SKILL.md) | C/C++, FFI, unsafe operations, arithmetic |
| [`web-security-review`](skills/web-security-review/SKILL.md) | Web application and API security |
| [`security-remediation`](skills/security-remediation/SKILL.md) | Evidence-driven patches and regression verification |

## Installation and usage

Copy the desired `skills/<name>/` directory to the skill directory of a compatible agent environment, or point the harness to this repository's `skills/` directory if it supports that configuration. Skill locations and auto-activation depend on the client. This project does not assume cross-skill tool invocation.

The Python utilities are optional, read-only utilities for existing scanner results; they do **not** scan source code on their own:

```sh
python -m pip install -e '.[dev]'
python -m security_skills.cli validate skills
python -m security_skills.cli inventory .
python -m security_skills.cli normalize example.sarif --output findings.json
python -m security_skills.cli correlate findings.json --output correlated.json
python -m security_skills.cli report correlated.json --format markdown --output report.md
python -m security_skills.cli evaluate evaluations/expected/scoring-example.json
pytest -q
```

External scanners (CodeQL, Semgrep, Bandit) may produce SARIF reports independently; scanner integration is **file-based**, not an automatic tool installation or process execution. Existing source files, SARIF and tool descriptions are untrusted inputs. Obtain authorization before running scanners, project code, or applying patches.

## Design and limitations

The original [EDSAW methodology](docs/assessment-methodology.md) requires explicit scope, architecture, analysis, code audit, evidence validation, remediation planning, and reporting. SARIF normalization preserves reported metadata and flow structures but does not reconstruct dataflow. Initial scanner findings are **inconclusive** until verified; severity is only a provisional tool-level category. Correlation is a heuristic and must be reviewed manually. The CLI's credential redaction is best-effort; inspect outputs before sharing. No dynamic execution, exploitability confirmation, or LLM evaluation is implied.

See [architecture](docs/architecture.md), [interoperability](docs/skill-interoperability.md), [security model](docs/security-model.md), [evaluation](docs/evaluation-methodology.md) and [source provenance](docs/source-provenance.md).

Original repository materials: Apache-2.0. Security books and third-party standards remain separately copyrighted/licensed.
