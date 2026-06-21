[< Story](index.md)

# Test Guide — CV21.E2.S1 Claude plugin conversion

## Automated validation

Run the project verification suite plus the new plugin structure tests:

```bash
uv sync --extra dev
uv run pytest tests/unit/ tests/integration/ -m "not live"
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run mypy src/memory
git diff --check
```

Expected result: all commands pass, including the new test asserting the plugin
manifest is valid, the manifest version equals `pyproject.toml`, the full
canonical `mm-*` skill set is present, and the four lifecycle hooks exist.

## Plugin manifest validation

Validate the canonical plugin with the Claude CLI:

```bash
claude plugin validate <plugin-root>
```

Expected result: validation passes with no errors. (E1 finding: the `$schema`
key must be absent — `claude` 2.1.114 rejects unknown manifest keys.)

Confirm the skill set has no drift against the canonical source:

```bash
diff \
  <(ls .pi/skills | sed 's/^mm-//' | sort) \
  <(ls <plugin-root>/skills | sed 's/^mm-//' | sort)
```

Expected result: no differences — the plugin carries all 25 canonical skills.

## Isolated smoke test

The smoke test must not touch the production database. It follows the standard
isolation pattern (temporary `DB_PATH`, production checksum recorded before and
after) from the runtime interface contract and `scripts/smoke_codex.sh`.

```bash
bash scripts/smoke_claude_plugin.sh
```

The script must:

1. Record the production DB checksum.
2. Point `DB_PATH` at an isolated temporary database (`MEMORY_ENV=production`).
3. Load the plugin in an isolated Claude invocation (temporary `HOME`/config so
   `~/.claude` installed-plugins state is not mutated) and assert:
   - the plugin loads without error;
   - a representative `mm-*` skill is discoverable;
   - the `SessionStart` hook fires and writes to the isolated DB.
4. Inspect the isolated DB and assert the expected rows exist.
5. Re-check the production DB checksum and assert it is unchanged.

Expected result: the script exits `0`, prints the isolated-DB assertions as
passed, and reports the production checksum unchanged.

## Backward-compatibility check

Confirm the standalone `.claude/` integration is untouched and still works:

```bash
git status --short .claude/
```

Expected result: no modifications to `.claude/` introduced by this story.

## Manual validation route (Navigator)

In a throwaway project directory (not the Mirror repo), with the plugin
installed into an isolated Claude config:

- start a Claude session and confirm the Mirror status/skills are available;
- invoke a Mirror skill (e.g. `mm-help`) and confirm it runs;
- confirm a new conversation is logged into the **isolated** database, not the
  production Mirror database.

Known limitation / conscious exclusion: this story proves plugin load, skill
discovery, and hook firing only. The MCP server (S2) and `statusLine` (S3) are
validated in their own stories.
