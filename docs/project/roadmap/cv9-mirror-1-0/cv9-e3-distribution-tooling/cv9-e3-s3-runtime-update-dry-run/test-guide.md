[< Story](index.md)

# Test Guide — Runtime Update Dry Run

## Automated Verification

Focused tests:

```bash
uv run pytest tests/unit/memory/cli/test_runtime.py
```

Full verification before closeout:

```bash
uv sync --extra dev
uv run pytest tests/unit/ tests/integration/ -m "not live"
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run mypy src/memory/cli/runtime.py
git diff --check
```

## Manual Validation Route

Run from the development repository:

```bash
cd /Users/alissonvale/Code/mirror-dev
uv run python -m memory runtime update --dry-run --mirror-home /Users/alissonvale/.mirror-minds/alisson-vale; true
```

Expected observations:

- command does not mutate git state or the database;
- output starts with `Mirror runtime update dry-run`;
- blocked state exits non-zero and names the blocking reason;
- during implementation, the local dirty tree blocks planning with `git tree is dirty`.

Observed manual result during this story:

```text
Mirror runtime update dry-run

Current status: attention needed
Repository: /Users/alissonvale/Code/mirror-dev
Git branch: main
Blocked:
  - git tree is dirty

Dry-run result: blocked
```

Ready and updateable branches are covered by unit tests through mocked git inspection, because producing those states manually would require changing repository history or remote refs during validation.
