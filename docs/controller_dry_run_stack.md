# Controller Decision Dry-Run Stack

## Purpose

This stack converts bottleneck diagnosis results into safe controller decisions.

The controller decision layer is dry-run only. It may produce recommendations, but it must not perform real actuation.

## Scope

This stack may:

- read validated experiment summaries through the existing loader
- use bottleneck diagnosis results
- produce dry-run recommendations
- produce no-action decisions
- include confidence, evidence, limitations, safety notes, and rollback notes

This stack must not:

- change GPU settings
- change power limits
- change clocks
- change fan settings
- change scheduler behavior
- move workloads
- perform hardware actuation

## Dependency Chain

The required flow is:

```text
experiment_summary.csv
    ↓
load_experiment_summaries()
    ↓
diagnose_experiments()
    ↓
make_controller_decision()
    ↓
dry-run report
