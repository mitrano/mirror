[< Story](index.md)

# Plan - CV9.E3.S7 Safe Runtime Update Execution

## Design Direction

This is the first command in the self-update track that mutates the working tree, the database, or the network state. Everything before it was read-only or local-only.

The principle: every mutation must be preceded by an explicit gate, every mutation must be reversible through a documented manual route, and every stage must be visible to the user. No silent success, no silent failure, no silent partial state.

## Command Shape

```bash
uv run python -m memory runtime update
```

Optional flags considered for this story:

```bash
--mirror-home PATH    Override the resolved mirror home (consistent with other runtime commands).
--no-fetch            Skip git fetch and only act on already-known local refs. Useful in offline environments.
--skip-migrations     Apply the git update but do not open the database to apply migrations. Manual follow-up required.
```

`--dry-run` and `--check` belong to the existing read-only path and remain there.

## Stages

The command runs as an ordered pipeline. Each stage either passes, fails, or is skipped. The first failure stops the pipeline. Stages already executed do not roll back automatically. Recovery is documented manual work.

1. **Status gate**
   - Run `build_runtime_status`.
   - If status is not `ready`, stop with recovery instructions pointing at `runtime diagnose`.

2. **Fetch upstream**
   - Default behavior. Skipped when `--no-fetch` is passed.
   - Runs `git fetch <remote> <branch>` against the resolved upstream.
   - Mutating step in the sense that local remote-tracking refs change. The working tree is not touched.

3. **Plan**
   - Run `inspect_git_update_plan` against the freshly fetched state.
   - Acceptable plans: `none` (up to date) and `pull`.
   - Block plans: `ahead`, `diverged`, `blocked` of any other kind.
   - When the plan is `none`, the pipeline exits successfully with no further mutation.

4. **Backup database**
   - Run the existing backup creation (`memory.cli.backup.backup`).
   - Record the backup path. The path is shown on success and on failure of any later stage.

5. **Verify backup**
   - Run `verify_backup_archive` against the just-written archive.
   - If verification fails, stop and report the backup path so the user can inspect it.

6. **Apply code update**
   - Run a conservative `git merge --ff-only <upstream>` against the local branch.
   - If git refuses, stop. Working tree is unchanged because of `--ff-only`. No rollback needed.
   - Record previous commit and new commit.

7. **Apply migrations**
   - Open the database via `MemoryClient(env="production")` once, which triggers `run_migrations` on connection open.
   - Skipped when `--skip-migrations` is passed. In that case the user is told they must apply migrations manually.
   - This is the step where database state changes. The earlier backup is the recovery point.

8. **Post-update status**
   - Rebuild `RuntimeStatusReport`.
   - If status is `ready`, the update is reported as successful.
   - If status is not `ready`, the update reports partial success and prints diagnose hints. Code is on the new commit, database may be migrated, backup is available.

9. **Result**
   - Print a summary: previous commit, new commit, backup path, status after update.

## Recovery Messages

Every failure must end with a recovery block. Examples:

Status gate fails:

```text
Recovery:
- Run: python -m memory runtime diagnose
- Resolve the reported drift, then retry runtime update.
```

Fetch fails:

```text
Recovery:
- Check network connectivity and remote access.
- Retry runtime update, or use --no-fetch to plan from local refs only.
```

Plan blocks:

```text
Recovery:
- Resolve manually: <plan-specific instruction>.
- Re-run runtime update once resolved.
```

Backup fails:

```text
Recovery:
- Mirror home must be writable.
- Backup directory: <mirror_home>/backups
```

Git merge fails:

```text
Recovery:
- Working tree is unchanged because fast-forward refused to merge.
- Resolve manually.
```

Migrations fail:

```text
Recovery:
- Backup: <path>
- Previous commit: <sha>
- Restore database from the backup and run: git reset --hard <previous>
- Then re-run runtime update once the underlying issue is resolved.
```

## Models

Add to `memory.cli.runtime`:

```python
@dataclass(frozen=True)
class RuntimeUpdateStage:
    name: str
    state: str   # "pass" | "fail" | "skip"
    detail: str | None = None

@dataclass(frozen=True)
class RuntimeUpdateResult:
    stages: tuple[RuntimeUpdateStage, ...]
    previous_commit: str | None
    new_commit: str | None
    backup_path: Path | None
    status_after: RuntimeStatusReport | None
    success: bool
    recovery: tuple[str, ...] = ()
```

Orchestrator:

```python
def run_runtime_update(
    *,
    mirror_home_arg: str | Path | None = None,
    fetch: bool = True,
    migrate: bool = True,
) -> RuntimeUpdateResult: ...
```

Renderer:

```python
def render_runtime_update_result(result: RuntimeUpdateResult) -> str: ...
```

## Live Output vs. Structured Result

Tests need a structured result. Humans need live feedback. The orchestrator returns the result, but it can also call an optional `on_stage(stage)` callback so the CLI prints as stages complete.

For this story, the simpler form is acceptable: orchestrator builds the result, the CLI prints `render_runtime_update_result` at the end. Live progress can be a small follow-up if needed.

## Reused Pieces

Already in `memory.cli.runtime`:

- `build_runtime_status`
- `inspect_git_update_plan`
- `verify_backup_archive`
- `render_runtime_status`

Already in `memory.cli.backup`:

- `backup`

Already in `memory.client`:

- `MemoryClient` (opens DB, runs migrations on open)

New helpers needed:

- a small `git_fetch(remote, branch, cwd)` wrapper that uses the existing `_run_git`;
- a small `git_fast_forward(upstream, cwd)` wrapper.

## Boundary

This story stops here:

- it does not reinstall extensions;
- it does not sync uv dependencies (user is told if pyproject changed);
- it does not edit `.mirror-clone-role`;
- it does not log update history to the database (separate concern, future story).

## Tests

Use monkeypatching for `_run_git`, `create_backup`, `MemoryClient` open, and `build_runtime_status`. Real network and real database are out of scope for unit tests.

Test coverage targets:

- status gate blocks update when status is not ready;
- fetch failure stops pipeline and emits recovery;
- plan `none` exits successfully without further stages;
- plan `ahead`/`diverged` blocks with recovery;
- backup failure stops pipeline;
- backup verification failure stops pipeline;
- fast-forward failure stops pipeline with working tree intact;
- migrations failure stops pipeline with backup path in recovery;
- happy path runs all stages, post-status is ready, success is True;
- `--no-fetch` skips fetch stage;
- `--skip-migrations` skips migrations stage and adds a manual-follow-up note.

CLI dispatch tests:

- `runtime update` exits 0 on success;
- `runtime update` exits 1 on any failure;
- existing `update --dry-run` and `update --check` remain unchanged.

## Manual Smoke

The first real smoke is itself the demonstration of the boundary the team built:

- Run `runtime update --dry-run` in production. Expect `up to date` or a clean plan.
- Run `runtime update` in production. Expect either `no update required` or a clean fast-forward with backup printed.

## Documentation

Update:

- `REFERENCE.md` runtime section.
- `docs/project/decisions.md` if the conservative update policy (fast-forward only, manual recovery) becomes a stable design decision.
- `docs/process/runtime-repair-policy.md` to mention that runtime update execution is the controlled path for production clones to receive new code.
- `docs/process/worklog.md` after implementation.

## Risks

The largest risk is partial state when migrations fail after code has fast-forwarded. The recovery message must always carry both the previous commit and the backup path so the user can reverse both sides if needed.

A secondary risk is uv dependency drift, which is not solved in this story. If `pyproject.toml` changed, the post-update status will still report `ready`, but the user may need `uv sync` to install new dependencies. The renderer should print a hint when `pyproject.toml` was part of the fast-forwarded changes. This hint can be added in a small follow-up if it grows the story too much.
