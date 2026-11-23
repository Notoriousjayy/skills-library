# Memory and arithmetic checklist

- For every buffer: determine capacity units (bytes/elements), actual length, termination, and all writes.
- For every integer conversion: note source width, target width, signedness, promotion order, underflow/overflow, and whether validation occurs before conversion.
- For pointer ownership: identify allocation, aliases, frees, invalidation, lifetime, and error cleanup paths.
- For synchronization: review shared state, lock ordering, reentrancy, signal safety, concurrent frees, and time-of-check/time-of-use assumptions.
- For impact: identify protection mechanisms and reachability. A crash is not automatically an exploitable arbitrary-code-execution vulnerability.

Safer implementation evidence can include span-like bounded views, checked size calculations, explicit ownership, dynamic sanitizers in an authorized isolated build, and verified regression tests. Unsupported platform assumptions must remain caveats.
