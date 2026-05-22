[< Story](index.md)

# Plan — Runtime Update Dry Run

## Design Intent

This story adds the planning surface for Mirror self-update, not the update itself. The command should answer: "if I were allowed to update, what would I do, and is it safe to proceed?"

The dry-run must be read-only. It should not fetch, pull, create backups, run migrations, edit files, or write history. It should inspect the local repository and configured Mirror home, then produce a plan that can be reviewed before a future real update command exists.

## Command Shape

Add a subcommand under the existing runtime CLI:

```bash
uv run python -m memory runtime update --dry-run [--mirror-home PATH]
```

`--dry-run` is required for this story. If `runtime update` is called without it, the command should fail with a clear message such as: `runtime update currently supports --dry-run only`.

This keeps the public surface honest. We introduce the verb now, but only the safe mode is implemented.

## Safety Gate

The dry-run starts by building the same `RuntimeStatusReport` used by `runtime status`.

If `report.status != "ready"`, the dry-run is blocked and returns non-zero. The output should include the status details or at least the blocking reasons:

- dirty git tree;
- repository unavailable;
- mirror home not configured;
- database missing;
- core migration health not ready;
- extension health not ready.

Because `runtime status` already centralizes these checks, the dry-run should reuse its data instead of recomputing those dimensions independently.

## Git Update Inspection

When status is ready, inspect the local branch's upstream relationship without mutating refs.

Suggested git commands:

```bash
git rev-parse --abbrev-ref --symbolic-full-name @{u}
git rev-list --left-right --count HEAD...@{u}
```

Interpretation:

- no upstream: blocked, no update target configured;
- ahead=0, behind=0: planned, no code update needed;
- ahead=0, behind>0: planned, future real update would pull/rebase/fast-forward remote commits;
- ahead>0, behind=0: blocked, local commits exist and automatic update should not proceed;
- ahead>0, behind>0: blocked, branch diverged and needs manual reconciliation.

No `git fetch` in this story. Fetching mutates remote tracking refs, so it belongs to a later explicit update planning or execution decision. This dry-run inspects what the local repo already knows.

## Dry-Run Report Shape

Add dataclasses in `memory.cli.runtime`, likely:

- `GitUpdatePlan`: upstream, ahead, behind, ready, action, note.
- `RuntimeUpdateDryRun`: status report, git plan, backup steps, validation steps, ready.

Human output:

```text
Mirror runtime update dry-run

Current status: ready
Repository: /path/to/repo
Git branch: main
Upstream: origin/main
Update plan: pull 3 remote commit(s)
Backup: required before real update (/path/to/mirror-home/backups)
Validation after update:
  - uv run pytest tests/unit/ tests/integration/ -m "not live"
  - uv run ruff check src/ tests/
  - uv run ruff format --check src/ tests/

Dry-run result: ready
```

Blocked example:

```text
Mirror runtime update dry-run

Current status: attention needed
Blocked:
  - git tree is dirty

Dry-run result: blocked
```

The exact wording can shift during implementation, but it should be concise, deterministic, and actionable.

## Exit Codes

- `0`: dry-run produced a safe plan.
- `1`: dry-run is blocked or cannot inspect required state.

A no-op plan where local branch equals upstream returns `0`, because the state is safe and the plan is simply "no code update needed".

## Tests

Extend `tests/unit/memory/cli/test_runtime.py`.

Test cases:

- `runtime update` without `--dry-run` returns non-zero with clear message.
- dirty status blocks dry-run.
- missing upstream blocks dry-run.
- equal branch reports no update needed.
- behind-only branch reports update available and returns zero.
- ahead-only branch blocks automatic update planning.
- diverged branch blocks automatic update planning.
- output includes backup and validation steps when plan is ready.
- existing `runtime status` tests still pass.

Mock `_run_git` and `build_runtime_status` for most unit tests. Avoid tests that need network or a real remote.

## Documentation

Update:

- `REFERENCE.md` command table and runtime paragraph;
- CV9.E3 story table;
- story `test-guide.md` after implementation with actual commands and observed results;
- `docs/process/worklog.md` after completion.

Update `mirror-self-update` journey after completion, because this story materially advances the umbrella path.

## Risks and Boundaries

The main risk is accidental mutation. Do not use `git fetch`, `git pull`, backup commands, migration commands, or extension install commands.

The second risk is giving false confidence when local remote tracking refs are stale. The dry-run should state that it is based on the local upstream state and does not contact the remote. A later story can add explicit fetch policy if needed.
