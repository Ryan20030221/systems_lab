# Ruff, pytest, and CI notes

## What does `ruff check` do?

`ruff check` runs lint checks. It looks for code-quality problems such as unused imports, style issues, and suspicious patterns before the code is reviewed or merged.

## What does `ruff format` do?

`ruff format` rewrites Python code into a consistent style so the project stays clean and readable.

## What does `pytest` do?

`pytest` runs the project's automated tests. It checks that important behavior still works after code changes.

## What does CI do?

CI means continuous integration. In this project, GitHub Actions runs the same quality checks automatically when code is pushed or opened in a pull request.

## Which commands must future modules pass?

Future modules must pass:

```bash
python -m ruff check .
python -m pytest
```

When code formatting changes are needed, run:

```bash
python -m ruff format .
```
