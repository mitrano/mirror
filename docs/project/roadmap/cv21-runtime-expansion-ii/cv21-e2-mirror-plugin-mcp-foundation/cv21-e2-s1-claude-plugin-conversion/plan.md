[< Story](index.md)

# Plan — CV21.E2.S1 Claude plugin conversion

## Design

This story repackages the existing standalone Claude integration as a canonical
Claude **plugin**. It changes packaging and path resolution only — no `memory`
core behavior, no skill content, no hook logic beyond making paths
plugin-relative.

### Target plugin layout

A self-contained plugin directory, distributable as a unit (later imported by
`agy`/`grok` and snapshotted by Codex):

```text
<plugin-root>/
  .claude-plugin/
    plugin.json          # manifest (no $schema; version synced to pyproject)
  skills/
    mm-mirror/SKILL.md
    mm-build/SKILL.md
    ...                  # full canonical mm-* set
  hooks/
    hooks.json           # hook events → ${CLAUDE_PLUGIN_ROOT}/hooks/*.sh
    session-start.sh
    log-user-prompt.sh
    mirror-inject.sh
    log-session-end.sh
```

### Manifest (`plugin.json`)

Claude-format manifest, validated against `claude` 2.1.114. E1 found the
validator rejects unknown keys, so the manifest stays minimal:

```json
{
  "name": "mirror-mind",
  "version": "0.29.0",
  "description": "Mirror Mind — local-first memory and identity for agentic runtimes.",
  "author": { "name": "Mirror Mind" }
}
```

Version must match `pyproject.toml`. How the sync is enforced (manual now,
generated later) is a decision below.

### Hooks

The four standalone hooks move into the plugin and become plugin-relative.
Today they `cd "$CLAUDE_PROJECT_DIR"` and call `python3 -m memory`, which assumes
the agent's cwd is the Mirror repo. As a plugin, the hook scripts live under
`${CLAUDE_PLUGIN_ROOT}` while the user's project is elsewhere, so:

- `hooks/hooks.json` references `${CLAUDE_PLUGIN_ROOT}/hooks/<name>.sh`;
- the scripts keep their current semantics (SessionStart logging, UserPromptSubmit
  inject + log, Stop end+backup, async where used);
- **path resolution to the `memory` package** must not depend on the user's cwd
  (see Risks — this is the load-bearing portability question).

### Skill bundling and the single-source-of-truth question

Today three skill surfaces exist: `.pi/skills/mm-*` (canonical source, 25),
`.claude/skills/mm:*` (hand-maintained copies, 21, drifted), and the shared
`.agents/skills/` symlink surface. A plugin must ship **real files** (symlinks do
not survive `import`/`install`), so the plugin needs its own materialized
`skills/`. Committing a fourth hand-maintained copy violates DRY and guarantees
future drift (the missing `discard`/`explore`/`soul`/`update` skills are proof
the copy model already failed once).

Recommendation: treat the plugin `skills/` as a **build artifact generated from
the canonical `.pi/skills/` source**, not a hand-maintained copy. The generator
also rewrites the skill `name`/invocation token to the plugin convention. This
keeps one source of truth and makes drift impossible by construction.

## Implementation steps

1. Add tests first (TDD): a manifest/structure test asserting the plugin has a
   valid `.claude-plugin/plugin.json`, the full `mm-*` skill set, and the four
   hooks, with the manifest version equal to `pyproject.toml`.
2. Decide and implement the skill-bundling strategy (generate from `.pi/skills/`
   — recommended — vs commit copies).
3. Create the plugin directory, manifest, and `hooks/hooks.json`.
4. Move/copy the four hook scripts to the plugin and make paths plugin-relative;
   resolve the `memory` package independent of the user's cwd.
5. Reconcile the skill drift so the plugin carries all 25 canonical skills.
6. Run `claude plugin validate <plugin-root>`; fix manifest until it passes.
7. Write the isolated smoke test (see test-guide) and confirm production DB
   checksum is unchanged.

## Design decisions to confirm at the plan checkpoint

These are structural choices I do not want to make unilaterally:

1. **Plugin location in the repo.** Options: a dedicated `packaging/`-style
   directory (clean separation, clearly a distributable artifact — recommended),
   versus reusing the `.claude/` location. Recommendation: a dedicated directory
   so the canonical package is obviously self-contained and not confused with the
   standalone integration.
2. **Skill bundling: generate vs commit.** Recommendation: generate the plugin
   `skills/` from canonical `.pi/skills/` to avoid a fourth drifting copy.
3. **Skill parity reconciliation scope.** The plugin should carry the full
   canonical set. Confirm we bring `discard`/`explore`/`soul`/`update` into the
   canonical package now rather than shipping a known gap.
4. **Standalone `.claude/` retention.** Keep it untouched this epic (CV21
   non-goal: no forced migration). Confirm.

## Risks

- **Hook path portability (load-bearing).** The current hooks assume the Mirror
  repo is the cwd and `python3 -m memory` resolves there. Installed as a plugin
  over an arbitrary user project, that assumption breaks. The conversion must
  resolve the `memory` package deterministically (installed entry point, or an
  explicit interpreter/path) without depending on the user's project cwd. If this
  is not solved, the plugin validates but does nothing at runtime.
- **Validator strictness.** E1 already hit the `$schema` rejection on 2.1.114.
  Keep the manifest minimal and validate empirically, not from docs.
- **Drift reintroduction.** Hand-copying skills recreates exactly the gap this
  story exists to close. Generation is the structural defense.
- **Scope creep into S2/S3.** No MCP, no statusLine here. Hold the boundary.

## Verification

Automated and isolated-smoke verification is specified in
[test-guide.md](test-guide.md). At minimum:

```bash
uv run pytest tests/unit/  # plugin manifest/structure tests
claude plugin validate <plugin-root>
bash scripts/smoke_claude_plugin.sh   # isolated; production DB checksum unchanged
```
