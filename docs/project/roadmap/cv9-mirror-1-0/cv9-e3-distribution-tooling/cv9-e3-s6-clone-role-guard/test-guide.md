[< Story](index.md)

# Test Guide - CV9.E3.S6 Clone Role Guard

## Automated Verification

Targeted tests:

```bash
PYTHONPATH=src uv run pytest tests/unit/memory/cli/test_runtime.py tests/unit/memory/cli/test_build.py
```

Expected result:

```text
passed
```

Static checks:

```bash
uv run --extra dev ruff check src/ tests/
uv run --extra dev ruff format --check src/ tests/
```

Expected result:

```text
All checks passed!
```

## Manual Smoke

In the dev clone:

```bash
cat .mirror-clone-role
uv run python -m memory runtime status
uv run python -m memory build load mirror-mind
```

Expected:

- file shows `dev`;
- status reports `Clone role: dev`;
- `build load` proceeds normally.

In the production clone:

```bash
cat .mirror-clone-role
uv run python -m memory runtime status
uv run python -m memory build load mirror-mind
```

Expected:

- file shows `production`;
- status reports `Clone role: production`;
- `build load` exits non-zero with a clear message and an override hint.

Override path, in the production clone:

```bash
uv run python -m memory build load mirror-mind --allow-production
```

Expected:

- the override proceeds, with a visible note that production was overridden.

## Read-Only Safety Check

Inspecting clone role must not create, modify, or remove `.mirror-clone-role`. Tests should assert the file content is unchanged after `runtime status` and `inspect_clone_role` calls.
