# Config Validation Acceleration Stack

## Purpose
Provide a professional, typed config implementation (`gpu_lab/config_professional.py`)
built on Pydantic as the going-forward replacement for the hand-written
`gpu_lab/config.py`. It validates config from a declared schema instead of hand-written
`if` checks.

## Status
- Active. `gpu_lab/config_professional.py` is the preferred config implementation for new modules.
- `gpu_lab/config.py` is frozen/legacy. New modules do not import it.

## IMPORTANT — NOT a drop-in replacement for config.py
A deliberate decision (Option C) left the two implementations un-reconciled. They share
function names but NOT behavior:

| Function | config.py (legacy) | config_professional.py (preferred) |
|---|---|---|
| `validate_config` | returns the cleaned/coerced dict | returns `None`, raises `ValidationError` |
| `load_config` | returns the cleaned dict | returns the raw dict (validated as a side effect) |
| `resolve_config` | `(defaults, *, min_utilization=None)` | `(default_config, override_config)` dict merge |
| extra keys | silently dropped | forbidden (`extra="forbid"`) |
| `min_utilization` | required | defaults to 50.0 |

New modules must use `config_professional`'s signatures, never `config.py`'s.

## Professional framing
Hand-written validation (one `if` block per field) is fine for a key or two but gets
repetitive and inconsistent as config grows. A schema library lets you declare the valid
shape once and get checking plus clear errors for free.

## Beginner concept
`config.py` checked each value by hand. `config_professional.py` describes the valid shape
as a Pydantic model and lets the library do the checking.

## The model
```python
class LabConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    min_utilization: float = Field(default=50.0, ge=0.0, le=100.0)
    default_results_dir: str = Field(default="results")
    default_logs_dir: str = Field(default="logs")
```

## Public API
- `load_config(path: str | Path) -> dict` — load JSON, validate, return the raw dict.
- `validate_config(config: dict) -> None` — validate; raises `pydantic.ValidationError`.
- `resolve_config(default_config: dict, override_config: dict) -> dict` — merge (override wins), validate, return.

## Workflow
`scripts/validate_config_professional.py` loads `config/defaults.json`, optionally applies
`--min-utilization` via `resolve_config`, and reports the result (exit 0 valid, exit 1
invalid). The override path doubles as the "override works" check.

## Common mistakes
- Using `config.py`'s old return/signature behavior with `config_professional`.
- Adding pydantic-settings / TOML / YAML / env-vars before a real use case exists.
- Forgetting `extra="forbid"` requires the model to list every key in the file.
- Catching `ValueError` instead of `pydantic.ValidationError`.

## Error cases
- Missing file → `FileNotFoundError`.
- Malformed JSON → `json.JSONDecodeError`.
- Wrong type / out-of-range / unknown key → `pydantic.ValidationError`.

## Tests / checks
- `tests/test_config_professional.py` — behavior tests.
- `tests/test_validate_config_professional.py` — script I/O tests.
- ruff + pytest + pre-commit pass.
- These prove correct behavior in isolation; they do NOT prove equivalence to `config.py`
  (equivalence was intentionally not pursued).

## Future reuse trigger
Future config-heavy modules use `gpu_lab/config_professional.py` and the signatures above.
Revisit if env-var/deployment overrides become real (add pydantic-settings) or nested
config appears (add nested models).

## Assumptions & limitations
- Assumes `config/defaults.json` contains only keys the model knows about (`extra="forbid"`).
- Flat config, three fields; no env/secret/nested support yet.
- `config.py` remains in the tree as legacy; no migration performed.

## Production Equivalent / Library Escalation
- This module: Pydantic v2 `BaseModel` for a flat local config.
- Env-var/.env/secret precedence across environments → pydantic-settings (`BaseSettings`).
- TOML/YAML config → `tomllib` (3.11+) or PyYAML paired with the model.
- Nested/large config → nested Pydantic models (overlaps with the later FastAPI/Pydantic stack).

