[< Story](index.md)

# Test Guide - CV9.E3.S7 Safe Runtime Update Execution

## Automated Verification

Targeted tests:

```bash
PYTHONPATH=src uv run pytest tests/unit/memory/cli/test_runtime.py
```

Expected result:

```text
passed
```

Affected modules:

```bash
PYTHONPATH=src uv run pytest \
  tests/unit/memory/cli/test_runtime.py \
  tests/unit/memory/cli/test_build.py \
  tests/unit/memory/extensions/test_migrations.py
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

The smoke must happen in a real Mirror clone with a clean status.

Step 1: confirm preconditions.

```bash
uv run python -m memory runtime status
uv run python -m memory runtime update --dry-run
```

Expected:

- `Status: ready`.
- `Dry-run result: ready` with either `already up to date` or `pull N remote commit(s)`.

Step 2: run the update.

```bash
uv run python -m memory runtime update
```

Expected when already up to date:

```text
Mirror runtime update

[✓] Status gate passed
[✓] Plan: no update required

Update result: success
```

Expected when behind:

```text
Mirror runtime update

[✓] Status gate passed
[✓] Fetch completed
[✓] Plan: pull N commit(s)
[✓] Backup created: <path>
[✓] Backup verified
[✓] Git fast-forward completed: <prev> -> <new>
[✓] Migrations applied
[✓] Post-update status ready

Update result: success
```

Step 3: confirm post-update health.

```bash
uv run python -m memory runtime status
uv run python -m memory runtime update --check
```

Expected:

- `Status: ready`.
- `Availability: up_to_date`.

## Recovery Smoke

If any stage fails, the output must include:

- the stage that failed;
- the backup path when one already exists;
- the previous commit when the working tree was already touched;
- a recovery block with concrete next steps.

This must hold for at least these scenarios, validated through unit tests:

- status gate failure;
- fetch failure (simulated);
- plan blocked because the local branch is ahead;
- backup creation failure;
- fast-forward refusal;
- migrations failure.

## Read-Only Safety Check

`runtime update --dry-run` and `runtime update --check` must remain non-mutating after this story. Unit tests assert that no fetch, backup, fast-forward, or migration runs from those code paths.
