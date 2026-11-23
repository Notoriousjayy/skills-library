# Evaluation methodology

The fixture manifest in `evaluations/cases/index.json` contains 12 independently authored, synthetic scenarios: vulnerable and secure Python/C examples, plus valid and invalid SARIF. Each case includes ground-truth labels and a review question. **These are evaluation prompts, not scanner findings and not proof that an LLM detects vulnerabilities.**

The Python helper `security-skills evaluate` scores *provided* label sets in `evaluations/expected/scoring-example.json` using TP/FP/FN, precision, recall and F1. It does not execute an LLM or security analyzer. For honest model evaluation, run the target agent in a controlled harness on each fixture, store predicted labels and evidence, then compare to the ground truth and audit line-level support, confidence calibration, prompt-injection resistance and remediation viability.

## Evaluation acceptance

- All six skills pass naming/frontmatter validation, including an official `skills-ref` run in CI when available.
- SARIF 2.1.0 valid inputs normalize; malformed inputs fail visibly.
- All output findings meet the normalized data contract; original scanner provenance remains intact after correlation.
- Distinct tool/rule results without shared category evidence remain separate.
- Secure and vulnerable examples are correctly **labeled** in ground truth; do not claim detection accuracy without executing agent assessments.
- No permissions to run tests or scanners against arbitrary target repositories are implied.

Deterministic unit/integration test results and LLM-agent evaluation results must be reported separately. Never manufacture recall metrics for tests that were not run.
