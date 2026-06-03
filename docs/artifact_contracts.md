# Generated Artifact Contracts

## Purpose

This document defines the project-wide contract for generated artifacts.

A **generated artifact** is any file or folder created by a command, script, experiment, benchmark, or reporting workflow. Examples include raw GPU logs, experiment summary CSVs, charts, Markdown reports, config snapshots, and run folders.

The goal is to make future generated outputs consistent, reproducible, easy to review, and safe for future modules to consume.

## Source Files vs. Generated Files

**Source files** are hand-written project files that belong in Git. Examples include reusable Python modules, scripts, tests, documentation, project configuration files, and `.gitignore`.

**Generated files** are outputs created by running the project. They usually should not be committed unless a module explicitly says they are intentional evidence artifacts.

Examples:

- Source file: `gpu_lab/reporting.py`
- Source file: `scripts/generate_experiment_report.py`
- Source file: `docs/reporting_stack.md`
- Generated file: `results/charts/experiment_efficiency.png`
- Generated file: `results/experiment_reports/markdown_report.md`
- Generated file: `results/experiment_summary.csv`

## Project-Wide Generated Artifact Rules

Generated artifacts must have a clear purpose, predictable path, documented content contract, cleanup policy, and future consumer.

A generated artifact should answer these questions:

- What created this artifact?
- What input data was used?
- What does the artifact contain?
- What schema, columns, sections, or units are required?
- Where should the artifact be saved?
- Should Git track it or ignore it?
- How can it be regenerated?
- Who or what will consume it later?

Generated artifacts should not be random scratch files. If a future module depends on the output, the output needs a contract.

## Git Tracking Policy

Git should track source files, reusable documentation, tests, scripts, project configuration, and small intentional fixtures.

Git should usually ignore generated outputs under `results/`.

The `.gitignore` file itself should be tracked by Git. The files and folders listed inside `.gitignore` are ignored.

Generated artifacts may only be committed when a module explicitly says they are stable evidence examples, fixtures, or documentation assets.

Before opening a PR, generated files should be checked with:

```bash
git status
git diff --stat
```

## Naming and Path Conventions

Generated experiment outputs should usually live under `results/`.

Preferred paths:

- Raw generated logs: `results/logs/`
- Experiment summary CSVs: `results/experiment_summary.csv` or `results/summaries/`
- Charts: `results/charts/`
- Markdown reports: `results/experiment_reports/`
- Run folders: `results/runs/`
- Generated config snapshots: `results/config_snapshots/`

Names should describe the artifact purpose. Avoid vague names like `output.csv`, `test.png`, or `final_report.md`.

When a run needs isolation, use a timestamped or named run folder.

## Artifact Contracts

Each generated artifact type needs a purpose, path, content contract, Git policy, cleanup rule, and future consumer.

### Raw GPU Logs

**Purpose:** Store raw measurements captured from GPU/system monitoring tools.

**Expected path:** `results/logs/` for generated run logs.

**Content contract:**

- Preserve original measurements as closely as possible.
- Include enough columns to identify time, power, temperature, utilization, clocks, or workload when available.
- Do not silently change units.
- Keep raw logs separate from cleaned summary outputs.

**Git policy:** Ignored by default because raw logs can be large, machine-specific, and repeatedly generated.

**Cleanup policy:** Safe to delete if the experiment can be rerun or if the important evidence has already been summarized.

**Future consumer:** Parsers, summary tools, diagnosis modules, and experiment reports.

### Experiment Summary CSVs

**Purpose:** Store cleaned or summarized experiment results.

**Expected path:** `results/experiment_summary.csv` or `results/summaries/`.

**Content contract:**

- Have a header row.
- Use descriptive column names.
- Use consistent units for numeric columns.
- Represent comparable experiment records in each row.
- Document required columns in the workflow that consumes them.

**Git policy:** Ignored by default unless a small CSV is intentionally committed as a test fixture or documentation example.

**Cleanup policy:** Safe to delete if it can be regenerated from raw logs or rerun experiments.

**Future consumer:** Reporting tools, chart generators, bottleneck diagnosis, controller dry-runs, and future recommendation reports.

### Charts

**Purpose:** Visualize experiment results clearly.

**Expected path:** `results/charts/`.

**Content contract:**

- Be generated from a known source CSV or data file.
- Include axis labels.
- Include units when relevant.
- Use a chart title that describes the claim or comparison.
- Avoid implying stronger evidence than the data supports.

**Git policy:** Ignored by default unless intentionally committed as documentation evidence.

**Cleanup policy:** Safe to delete if the source data and command are available.

**Future consumer:** Markdown reports, PR explanations, experiment reviews, and future recommendation evidence.

### Markdown Reports

**Purpose:** Summarize experiment evidence in a readable form.

**Expected path:** `results/experiment_reports/`.

**Content contract:**

- Identify the source data.
- Reference generated chart paths when charts are included.
- State the report title or experiment purpose.
- Include limitations.
- Avoid making claims not supported by the data.

**Git policy:** Ignored by default unless intentionally promoted into tracked documentation.

**Cleanup policy:** Safe to delete if it can be regenerated.

**Future consumer:** PR reviews, experiment history, future diagnosis modules, and product evidence.

### Config Files and Config Snapshots

**Purpose:** Separate reusable configuration from generated records of the settings used during a run.

**Expected paths:**

- Source config files: project config folders such as `config/`
- Generated config snapshots: `results/config_snapshots/` or inside a run folder

**Content contract:**

- Source config files define reusable defaults.
- Generated config snapshots record the exact settings used for one run.
- Config snapshots should not replace the source config.

**Git policy:**

- Source config files are usually tracked.
- Generated config snapshots are usually ignored.

**Cleanup policy:** Generated config snapshots can be deleted if the run does not need to be preserved.

**Future consumer:** Reproducibility checks, experiment reports, and debugging.

### Run Folders

**Purpose:** Group all artifacts from one experiment or workflow run.

**Expected path:** `results/runs/`.

**Content contract:**

- Group related logs, summaries, charts, reports, and config snapshots.
- Use a folder name that identifies the run.
- Use timestamped names when multiple runs are created.
- Do not contain source code copies unless explicitly required.

**Git policy:** Ignored by default.

**Cleanup policy:** Safe to delete if the run is no longer needed or can be regenerated.

**Future consumer:** Experiment review, debugging, reproducibility, and future automated analysis.

## Cleanup and Reproducibility Policy

Generated artifacts under `results/` can usually be deleted.

An artifact is reproducible when the project keeps enough information to recreate it, including:

- Source data or input path
- Command or workflow used
- Relevant configuration
- Expected output path
- Known limitations

If an artifact cannot be regenerated, it should be treated as temporary evidence and either documented intentionally or archived outside the normal source tree.

## PR Review Checklist

Before opening a PR, check that:

- [ ] No accidental files from `results/` are staged.
- [ ] No generated chart, report, log, or run folder is committed by accident.
- [ ] `.gitignore` is tracked if changed.
- [ ] Source documentation changes are intentional.
- [ ] Every new generated artifact type has a documented purpose.
- [ ] Paths and naming conventions are clear.
- [ ] Schema/content expectations are described.
- [ ] Cleanup and reproducibility rules are described.
- [ ] Future consumer is identified.
- [ ] No Python implementation was created for this non-code module.
- [ ] No workflow script was created for this non-code module.

## Future Reuse Trigger

Any future module that creates a CSV, JSON file, chart, Markdown report, raw log, config snapshot, benchmark output, or run folder must audit this document before creating the artifact.

This document becomes hardline for generated product outputs.

## Not Responsible For

This document does not define:

- Database storage policy
- Live dashboards
- Production data retention policy
- Cloud object storage layout
- New Python implementation
- Workflow scripts
- New chart or report generation logic
