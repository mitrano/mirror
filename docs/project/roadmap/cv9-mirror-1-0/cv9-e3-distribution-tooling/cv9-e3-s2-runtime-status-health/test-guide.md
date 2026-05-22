[< Story](index.md)

# Test Guide — Runtime Status Health Checks

## Automated Verification

Focused story tests:

```bash
uv run pytest tests/unit/memory/cli/test_runtime.py tests/unit/memory/extensions/test_migrations.py
```

Expected result:

```text
33 passed
```

Full verification before closeout:

```bash
uv sync --extra dev
uv run pytest tests/unit/ tests/integration/ -m "not live"
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run mypy src/memory/cli/runtime.py src/memory/extensions/migrations.py
git diff --check
```

Observed result:

- `1073 passed` for unit and integration tests;
- ruff check passed;
- ruff format check passed;
- story-scoped mypy passed for changed runtime and extension migration modules;
- `git diff --check` passed.

Known limitation: `uv run mypy src/memory` currently fails on pre-existing typing debt across unrelated modules. This story did not introduce those failures; the changed modules pass scoped mypy.

## Manual Validation Route

Healthy local runtime, allowing for a dirty tree during implementation:

```bash
uv run python -m memory runtime status; true
```

Expected observations:

- output includes `Core migrations: current (10/10)` when every known core migration is applied;
- output includes `Extension health: ready (N checked)` when installed extensions are valid and migration ledgers match files on disk;
- output still includes version, repository, git, mirror home, database, Python, and environment;
- during an implementation session the aggregate status may be `attention needed` solely because `Git dirty: yes`.

Example healthy diagnostic dimensions observed locally:

```text
Core migrations: current (10/10)
Extension health: ready (3 checked)
```

## Mutation Safety Check

The runtime status implementation must not bootstrap or migrate the inspected database. Core and extension health open SQLite in read-only mode and never call the normal connection factory.

Regression command for missing database behavior:

```bash
uv run pytest tests/unit/memory/cli/test_runtime.py -k missing_without_mutating
```

Expected result:

- test passes;
- the inspected missing database path is not created.
