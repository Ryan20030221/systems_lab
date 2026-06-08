# Python Quality Automation Stack

## Purpose

This document is the authoritative reference for automated quality checks in `systems_lab`.
It records what tools are configured, how to run them, which checks run locally vs in CI,
what was intentionally deferred, and the escalation ladder for future gates.

Module: 12.75 — Python Quality Automation Stack

---

## Professional Framing

Professional speed comes from automation. Once a project has enough code that forgetting
a quality check wastes real time, repeated manual commands should become automatic. This
module wraps the existing pytest + ruff + CI workflow with local hooks and adds coverage
and type-checking as documented commands. Nothing about existing behavior changes.

Additive-first rule: all existing tools still work without pre-commit installed.
`python -m ruff check .` and `python -m pytest` run exactly as before. Pre-commit is a
convenience layer, not a replacement for any of them.

---

## Tools

### pre-commit

**What it is:** A framework that installs Git hooks — scripts that run automatically before
each `git commit`. Reads `.pre-commit-config.yaml` at the project root.

**Install (one-time per clone):**
```bash
pip install pre-commit
pre-commit install
```

**Run manually (validate config or after initial setup):**
```bash
pre-commit run --all-files
```

**Configuration file:** `.pre-commit-config.yaml`

**Hooks active:**
- `ruff-check` (v0.15.16) — runs the ruff linter; blocks commit if lint errors exist
- `trailing-whitespace` (v6.0.0) — removes trailing spaces from lines
- `end-of-file-fixer` (v6.0.0) — ensures files end with a newline
- `check-yaml` (v6.0.0) — validates YAML syntax
- `check-toml` (v6.0.0) — validates TOML syntax

**What is intentionally not a pre-commit hook:**
- pytest — too slow (1.5s+) for a commit-time gate; runs in CI instead
- pyright — not enough annotations yet for a clean pass; manual command only
- ruff-format — formatter not configured for this project yet; deferred

---

### coverage (pytest-cov)

**What it is:** Tracks which lines of code in `gpu_lab/` are executed when the test suite
runs. Shows gaps — not proof of correctness.

**Command:**
```bash
python -m pytest --cov=gpu_lab --cov-report=term-missing
```

**Configuration:** `pyproject.toml` `[tool.coverage.run]` and `[tool.coverage.report]`

**Source scope:** `gpu_lab/` only. Scripts and tests are excluded from measurement.

**Baseline (established Module 12.75):** <!-- fill in after first run --> **Baseline (established Module 12.75):** 1 error, 0 warnings
- `gpu_lab/experiment_summary.py:99` — `Sequence[str]` passed where `list[str]` annotated in `_validate_required_columns`. Fix: widen parameter annotation to `Sequence[str]`. Deferred to a future annotation pass.

**Important:** A covered line is not a verified line. Coverage shows where tests are
absent. It does not show whether tests are correct.

**Not a gate yet:** No `fail_under` threshold is configured. Coverage is measured and
documented. A minimum threshold can be added after a reliable baseline is established.

---

### pyright (static type checker)

**What it is:** Analyzes Python code without running it. Checks that type annotations are
consistent — flags type mismatches, wrong argument types, and missing attributes.

**Command:**
```bash
pyright
```

**Configuration:** `pyproject.toml` `[tool.pyright]`

**Mode:** `basic` — only reports errors where type annotations are present.
Does not report errors for unannotated code.

**Python version:** `3.14` (matches the project interpreter)

**Baseline (established Module 12.75):** <!-- fill in after first run -->

**Not a gate yet:** Type errors are not a commit block or CI failure. The project does not
have comprehensive annotations yet. Pyright is run as a diagnostic and documentation tool.
A CI gate can be added when annotations are widespread across `gpu_lab/`.

---

## Local vs CI Responsibility

| Check | Pre-commit (local, commit-time) | Manual (local, on demand) | CI (GitHub Actions, always) |
|---|---|---|---|
| Ruff linting | ✅ gate | ✅ | ✅ gate |
| pytest full suite | ❌ (too slow) | ✅ | ✅ gate |
| Coverage | ❌ | ✅ | ❌ (not gated yet) |
| Type checking (pyright) | ❌ | ✅ | ❌ (not gated yet) |
| Trailing whitespace | ✅ gate | ✅ | via ruff |

**Rule:** CI always runs independently of whether pre-commit was used. A developer can
bypass pre-commit with `git commit --no-verify`, but CI still catches lint and test
failures before merge.

---

## Automation Noise Policy

Noisy gates get bypassed. New gates are added only when:
- The check already passes reliably on the existing codebase
- The check is fast enough not to interrupt normal commit flow (< 2 seconds)
- The check provides a real signal, not just formatting preference

Current commit-time gate (ruff-check): already passing, runs in ~100ms. Appropriate.
Future gate candidates: see Escalation Ladder below.

---

## Quality Gate Escalation Ladder
