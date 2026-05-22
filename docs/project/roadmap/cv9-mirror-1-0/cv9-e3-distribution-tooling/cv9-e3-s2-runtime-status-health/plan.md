[< Story](index.md)

# Plan — Runtime Status Health Checks

## Design Intent

`memory runtime status` is the current-state gate for future self-update work. This story deepens that gate without turning it into an updater. The command should inspect and report; it should not repair, migrate, reinstall, or mutate the user's runtime.

The design rule is conservative diagnosis. If the command cannot safely inspect a health dimension, it reports attention needed with the reason. Silence is reserved for confirmed health, not for unknown state.

## Current Code Shape

Runtime status lives in `src/memory/cli/runtime.py`.

Current report fields:

- package version;
- git repository, branch, commit, dirty state;
- mirror home resolution;
- database path and existence;
- installed extension directory names;
- Python version;
- `MEMORY_ENV`;
- aggregate status: `ready` or `attention needed`.

Core migrations are defined in `src/memory/db/migrations.py` as `MIGRATIONS`. Applied core migrations are recorded in the `_migrations` table. Extension migration bookkeeping is stored in `_ext_migrations`, and validation helpers already exist in `src/memory/extensions/migrations.py` and `src/memory/cli/extensions.py`.

## Proposed Shape

Add small immutable report types in `memory.cli.runtime`:

- `CoreMigrationHealth`: database readable, applied count, known count, missing ids, note.
- `ExtensionHealth`: extension id, status, note, pending migration files.
- possibly `ExtensionSummary`: count healthy, count needing attention, detailed rows.

Keep this inside the runtime CLI for now. If the health logic grows beyond status or is reused by update dry-run, extract it later into a service in the self-update story. Premature extraction would make this slice larger without proven reuse.

## Core Migration Health

Algorithm:

1. If there is no `db_path`, report unknown because mirror home is not resolved.
2. If the database file does not exist, report missing database.
3. Open the SQLite file read-only using a URI connection such as `file:<path>?mode=ro`.
4. Check whether `_migrations` exists.
5. Read applied migration ids.
6. Compare with `[id for id, _ in MIGRATIONS]`.
7. Report ready only when every known migration id is present.

The command must not call `get_connection()`, because that would bootstrap schema and run migrations. Runtime status is diagnostic; it must not change the database while asking whether it is safe to update.

## Extension Health

Use the installed extensions root under the resolved mirror home. For each child directory with `skill.yaml`:

1. Load and validate the manifest with `load_extension_manifest()`.
2. If manifest validation fails, report attention needed.
3. For prompt-skill extensions, report ready after manifest validation.
4. For command-skill extensions, inspect `migrations/*.sql` without applying anything.
5. Compare migration files against `_ext_migrations` rows for that extension.
6. Report attention needed when a migration file exists on disk but has no applied row.
7. Report attention needed when an applied migration row exists but the current file checksum does not match the recorded checksum.
8. Preserve the extension migration runner's compatibility rule: a recorded legacy raw checksum should be accepted when the current raw file still matches.

Because checksum helpers are private in `memory.extensions.migrations`, this story has two options:

- expose a small public inspection helper from `memory.extensions.migrations`, or
- keep a runtime-local inspection helper that calls only public behavior where possible.

The preferred route is to add a public helper in `memory.extensions.migrations`, for example `inspect_migration_files(conn, extension_id, migrations_dir)`, returning missing and drifted files without running SQL. That keeps checksum semantics in one place and avoids duplicating the normalised checksum contract.

## Rendering

Extend the existing human output minimally:

```text
Core migrations: current (10/10)
Extension health: ready (3 checked)
```

When attention is needed:

```text
Core migrations: attention needed (9/10 applied; missing 010_create_consolidations)
Extension health: attention needed (2 checked, 1 issue)
  - maestro: pending migration 002_add_status.sql
```

The exact wording can change during implementation, but the output should remain one screen for healthy status and concrete enough for repair when unhealthy.

## Status Rule

`RuntimeStatusReport.status` becomes `attention needed` when:

- existing current checks fail;
- core migration health is not ready;
- any extension health item is not ready.

Exit codes remain unchanged: `0` for ready, `1` for attention needed.

## Tests

Add unit tests in `tests/unit/memory/cli/test_runtime.py` and, if a public migration inspection helper is added, in `tests/unit/memory/extensions/test_migrations.py`.

Test cases:

- render includes healthy core migration and extension health lines;
- report status is attention needed when core migrations are missing;
- core health opens the database read-only and does not create a missing database;
- extension health reports invalid manifests;
- extension health reports pending command-skill migrations;
- extension health reports checksum drift;
- extension health accepts prompt-skill extensions without migrations;
- CLI return code remains zero for ready and non-zero for attention needed.

## Documentation

Update:

- `REFERENCE.md`, runtime status paragraph;
- CV9.E3 index story table;
- story `test-guide.md` after implementation with actual commands.

Update `docs/process/worklog.md` only after the story is complete.

## Risks

The main risk is accidental mutation. Opening the database through existing connection factories would run schema and migrations as a side effect. This story must use read-only SQLite inspection for status.

The second risk is checksum duplication. Extension migration drift should use the same checksum semantics as the extension migration runner, otherwise status and migration execution could disagree. Prefer exposing a public inspection helper rather than reimplementing checksum logic in the runtime CLI.
