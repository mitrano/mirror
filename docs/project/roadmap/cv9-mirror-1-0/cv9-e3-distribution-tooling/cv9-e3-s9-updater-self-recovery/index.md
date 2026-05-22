[< CV9.E3 Distribution & Tooling](../index.md)

# CV9.E3.S9 — Updater Self-Recovery

**Epic:** CV9.E3 Distribution & Tooling
**Status:** ✅ Done
**User-visible outcome:** If the normal updater cannot complete its status gate because the updater itself is stale or crashes, Mirror Mind has a safe code-only recovery lane that a non-expert user can run.

---

## What Changed

- `runtime update` catches status-gate crashes before mutation and automatically enters updater self-repair.
- `runtime update --repair-updater` exposes the same lane explicitly.
- The repair lane uses a minimal preflight instead of full runtime health:
  - repository must be available;
  - git tree must be clean;
  - upstream must be configured;
  - fetch is attempted unless `--no-fetch` is passed;
  - only fast-forward code updates are allowed;
  - database backup is created and verified when a Mirror home and database are available;
  - migrations are skipped.
- Successful repair prints a next step instructing the user to rerun `runtime update` with the repaired updater.

---

## Why

A production self-update attempt exposed a bootstrap problem: if a stale updater
crashes during full runtime health inspection, the user cannot use the updater to
install the fix. Manual recovery is acceptable for framework development, but not
for end users.

Updater self-recovery keeps the risk bounded: it updates code only, never runs
migrations, refuses dirty or diverged trees, and preserves a backup when local
data is discoverable.

---

## Verification

```bash
PYTHONPATH=src uv run pytest tests/unit/memory/cli/test_welcome.py tests/unit/memory/cli/test_runtime.py tests/unit/memory/cli/test_build.py tests/unit/memory/extensions/test_migrations.py
uv run --extra dev ruff check src/ tests/
uv run --extra dev ruff format --check src/ tests/
uv run --extra dev mypy src/memory/cli/runtime.py
```

---

## See also

- [Runtime Self-Update Reference](../../../../../../REFERENCE.md#runtime-self-update)
- [Runtime Repair Policy](../../../../../process/runtime-repair-policy.md)
