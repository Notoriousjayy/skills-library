---
name: web-security-review
description: Audit web applications and APIs for injection, identity, authorization, request handling, sessions, SSRF, and sensitive-data exposure. Use during backend and full-stack security reviews.
license: Apache-2.0
---

# web-security-review

## Steps
1. Inventory endpoints, handlers, middleware, trust proxies, request inputs, templating contexts, data stores, and cross-service calls.
2. Analyze input handling by sink context: SQL placeholders, shell argument separation, HTML contextual output encoding, safe filesystem access, and parser controls. Generic input filtering is not an interchangeable sanitizer.
3. Verify identity and object-level authorization at each sensitive operation, including tenant and resource ownership checks. Do not infer security solely from route names.
4. Review session lifetime/rotation, CSRF where cookies authenticate requests, cookie flags, redirect behavior, CORS assumptions, and relevant HTTP controls.
5. Examine outbound requests for SSRF, deserialization boundaries, uploaded files, secret exposure, error logging, and cloud metadata reachability.
6. Tie each finding to actual source locations, application configuration, and appropriate framework/version behavior. Check current upstream guidance; do not copy historical framework advice.

See [web review checklist](references/web-checklist.md). Where a control cannot be observed, state what needs to be verified.
