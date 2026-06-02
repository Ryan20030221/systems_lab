# Reporting Stack

## Purpose

The Reporting Stack turns experiment summary data into reproducible human-readable evidence artifacts.

It owns static chart and Markdown report generation for GPU experiment results.

## Owned Files

- `gpu_lab/reporting.py`
  - reusable reporting and chart-generation functions
- `scripts/generate_experiment_report.py`
  - command-line workflow script
- `tests/test_reporting.py`
  - regression tests for report/chart behavior
- `docs/reporting_stack.md`
  - stack contract and future reuse rules

## Generated Artifacts

Generated reports and charts must be written under `results/`.

Generated files must not be committed to Git.

Expected generated examples:

- `results/manual_reporting/fps_per_watt.png`
- `results/manual_reporting/fps_per_watt_report.md`
- `results/manual_reporting/experiment_summary.csv`

## Required Report Evidence

Each Markdown report must include:

- source CSV path
- generated chart path
- report title
- limitations

## Chart Requirements

Charts must include:

- x-axis label
- y-axis label
- units when applicable
- title
- saved PNG output path

## CLI Contract

The workflow script must expose:

- `--input`
- `--chart-output`
- `--report-output`
- `--x-column`
- `--y-column`
- `--x-label`
- `--y-label`
- `--title`
- `--limitation`

`--limitation` may be repeated.

## Ownership Rule

Reusable chart/report logic belongs in `gpu_lab/reporting.py`.

The script may only orchestrate workflow steps.

Future modules should reuse `gpu_lab.reporting`, not import from script internals.

## Limitations

This stack does not yet provide:

- dashboards
- live plotting
- statistical confidence intervals
- automatic recommendations
- database-backed reports
- raw log parsing inside the report workflow

## Future Reuse Trigger

Any future module that makes a claim about GPU performance, efficiency, bottlenecks, scheduling, placement, prediction, or controller behavior must consider whether to generate a Reporting Stack artifact.