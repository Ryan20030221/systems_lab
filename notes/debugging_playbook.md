# Debugging Playbook

Purpose: the do-this-in-order procedure to run the moment a failure appears.
Operational companion to docs/debugging_stack.md.

Use when: any traceback, failing test, CI failure, or unexpected output.

## Steps

1. Read the traceback bottom-up.
   Record the exception type and message, the deepest frame inside project
   code, and the call path that reached it. Read the message first.

2. Reproduce minimally.
   Find the smallest input plus single command that triggers the failure every
   time. Shrink large inputs (e.g. a 2-row CSV instead of a full log).

3. Form one hypothesis.
   State one specific guess about the cause before changing anything.

4. Isolate the failing input or condition.
   Remove variables one at a time (bisect the data or the steps) until only the
   offending value/row/file/condition remains.

5. Classify the failure.
   Decide: invalid data, setup failure, or programmer bug. Reuse the Module 5
   validation boundary to place the fix at the right layer.

6. Fix the root cause, not the symptom.
   Do not catch-and-ignore. Fix the actual cause at the correct owner.

7. Add a regression test when practical.
   Write a test that fails on the old code and passes on the fix, in the
   existing owner test file (e.g. tests/test_experiment_summary.py). If no test
   is practical, write down why.

8. Confirm green.
   Re-run the suite (python -m pytest) and confirm nothing else regressed.

## Assumptions

- The existing pytest suite is where regression tests belong.
- The project's validation boundaries (Module 5) are available to the reader.

## Limitations

- Covers print/assert/pytest-level investigation only; interactive debuggers
  are out of scope at this stage.
- Does not prescribe fixes for specific bugs; it prescribes the procedure.

## Future reuse trigger

Opened on every real debugging session; audited by every bug fix.

## Not responsible for

Advanced debuggers; logging (Module 14); native C++ debugging (Module 48).
