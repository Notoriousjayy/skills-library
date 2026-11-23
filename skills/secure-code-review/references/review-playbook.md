# Security code review playbook

## Scope record
Record repository URI, commit, base revision, review owner, permitted operations, in-scope services, auth model, languages, and exclusions. A lack of design documentation reduces confidence; it does not justify fabricated architecture.

## Review target selection
Prioritize external request handlers, deserializers, file and process interfaces, database access, cryptography boundaries, identity enforcement, secrets, unsafe code, and high-privilege automation. Investigate historical risk and dependencies, but do not equate age with exposure.

## Review sequence
Inspect entry points and sensitive sinks; enumerate plausible sources; trace data through calls and validation; test the claimed protection against its exact downstream context; check exceptional/control paths; correlate scanner evidence; create a minimally sufficient explanation for each issue.

## Baseline-aware PR review
Attribute an issue to the changed line or changed dataflow. When git history is unavailable, mark introduction as unknown. Never label an unchanged issue newly introduced without evidence.
