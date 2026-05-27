# systems_lab

[![Tests](https://github.com/Ryan20030221/systems_lab/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/Ryan20030221/systems_lab/actions/workflows/tests.yml)

## Setup

Create a local Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Check that Python and pip are using the local environment:

```bash
python --version
python -m pip --version
```

## Tooling and checks

This project uses `pytest` for automated tests and `ruff` for code quality checks.

Run tests:

```bash
python -m pytest
```

Run lint checks:

```bash
python -m ruff check .
```

Format code:

```bash
python -m ruff format .
```

Before a module is considered complete, tests and lint checks should pass locally. After Module 7.5, GitHub Actions also runs these checks automatically on pushes and pull requests.

## Experiment Workflow

Module 10 introduces a basic experiment-design workflow.

Before running a GPU experiment, copy or reference `docs/experiment_template.md` and define the baseline, independent variable, dependent variables, control variables, warmup plan, repeated trials, and success criteria.

After running an experiment, summarize the result in `results/experiment_summary.csv`.

The summary CSV is not raw telemetry. It is a compact record of the main result from each experiment condition or trial.
