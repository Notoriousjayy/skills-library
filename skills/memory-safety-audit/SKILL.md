---
name: memory-safety-audit
description: Audit memory-unsafe source for buffer boundaries, integer conversions, object lifetimes, and race conditions. Use for C/C++ code or unsafe language and FFI boundary reviews.
license: Apache-2.0
---

# memory-safety-audit

## Steps
1. Establish the language standard, compiler, target architecture, allocation model, sanitizer coverage, and build assumptions; do not assume they are known.
2. Inventory user-controlled lengths, allocation sizes, pointer arithmetic, conversions, string handling, unsafe APIs, ownership transfers, concurrency, and cleanup paths.
3. Trace size/index arithmetic through types and integer promotions; verify upper/lower bounds before arithmetic and memory accesses.
4. Examine allocation, object lifecycle, early returns, exceptions, and parallel operations for memory misuse and TOCTOU behavior.
5. Classify findings only when data and control-flow evidence supports them; compiler flags do not eliminate source defects automatically.
6. Propose safe abstractions, checked arithmetic, RAII/ownership strategies, and regression checks. Run sanitizers or build binaries only with authorization.

See [memory safety checklist](references/memory-checklist.md). Synthetic examples are not exploit recipes.
