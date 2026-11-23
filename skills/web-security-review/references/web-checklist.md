# Web/API security checklist

| Concern | Evidence to gather | Typical secure invariant |
| --- | --- | --- |
| Injection | handler input, propagation, query execution | data does not change command/query structure |
| Authorization | session/principal, resource ID, handler and storage filters | each operation enforces the intended principal/tenant scope |
| SSRF | user-directed URL, resolver/redirects, outbound policy | untrusted URLs cannot reach disallowed targets |
| Path access | user-controlled path, normalization, filesystem root | final resolved path stays within authorized directory |
| Sessions | issuance/rotation, expiration, cookie attributes | tokens remain scoped, unpredictable, and appropriately limited |
| Secret handling | source, configuration, logs, persistence | secrets are protected and not disclosed |

When evaluating SQL APIs, confirm *actual parameterization*; escaping alone is not interchangeable. When evaluating authorization, test negative cases with a different legitimate principal in a controlled environment, not production users.
