# Debugging Stack

State: active (locked in at Module 13)

## Purpose

Turn failures into reproducible fixes instead of random edits. This stack owns
the standard procedure for investigating any failure in the project so a fix is
based on an identified root cause, not on guessing.

## Trigger

Activate on any:
- bug investigation
- failing test
- CI failure
- runtime exception / traceback
- unexpected output

## Required components

1. Traceback reading — read bottom-up: exception type and message first, then
   the deepest frame inside project code, then the call path.
2. Minimal reproduction — reduce the failure to the smallest input plus single
   command that triggers it reliably every time.
3. Isolated failing case — narrow to the exact value, row, file, or condition
   responsible by removing variables one at a time.
4. Regression test when practical — after fixing the root cause, add a test
   that fails on the old code and passes on the fix, in the existing owner test
   file. If a test is not practical, document why.

## Procedure reference

See notes/debugging_playbook.md for the ordered step-by-step procedure.

## Equivalent checks

- Python: reproduce with a small input; fix; ruff/pytest; regression test in
  tests/test_<owner>.py when practical.
- C++: reproduce; fix; rebuild with warnings; run test executable; sanitizers
  when taught (native debugging is Module 48).
- Docker: reproduce inside the container; rebuild; run the relevant check.
- API: reproduce the request; fix; endpoint/schema/error test.
- Cloud/remote: reproduce; fix; setup/auth/cost-aware verification.
- Docs-only: the bug note records reproduction, root cause, and fix (or a
  written reason no test is practical).

## Skip rule

A required component may be skipped only with a written professional reason
(e.g. a failure that genuinely cannot be reproduced, documented as such). Do
not start refactoring before the failure is reproduced.

## Future reuse rule

Every bug fix or confusing-failure investigation audits this stack.

## Not responsible for

- Advanced/interactive debuggers (pdb, gdb, IDE debuggers) — deferred.
- Logging — see Module 14 (Logging Foundations).
- Native C++ debugging with debug symbols and gdb — see Module 48.
