[< CV21](../index.md)

# CV21.E2 — Mirror Plugin & MCP Foundation (Claude)

**Status:** 🟢 In Progress
**User-visible outcome:** Mirror Mind ships as a canonical Claude-format plugin (skills + lifecycle hooks) plus a Mirror MCP server, validated on Claude as the reference runtime. Claude users install Mirror as a versioned plugin instead of committing `.claude/` scaffolding into their repos.

---

## What This Is

E2 builds the keystone artifact of CV21: the **canonical package** every other
runtime consumes by import/install. [E1](../cv21-e1-unified-plugin-mcp-spike/index.md)
proved — in an isolated scratch dir — that the package is real and chose the
strategy ([decision](../../../decisions.md#cv21-converges-on-a-canonical-plugin-plus-mcp-server-bridged-by-import)):
converge on a Claude-format plugin plus a Mirror MCP server, propagated per
runtime, with a thin-adapter + shared-MCP fallback.

E2 turns that decision into a production artifact and proves it on the
most-used runtime. Concretely:

1. Author the canonical Mirror plugin (`.claude-plugin/plugin.json` bundling the
   `mm-*` skills + the four lifecycle hooks).
2. Author the Mirror **MCP server** (`python -m memory mcp`) carrying the command
   surface and on-demand context (not automatic per-turn injection — E1 finding).
3. Wire the plugin `statusLine` to Mirror's existing status-line surface.
4. Prove the package on Claude with an **isolated smoke test** that mutates no
   production mirror, repo, or runtime config.

Claude is the reference runtime: the native home of the plugin format, so the
canonical package is built and validated where it is best understood. The
standalone `.claude/` path keeps working — the plugin is the recommended path,
not a forced migration (CV21 non-goal).

---

## Scope

- A canonical Claude-format plugin directory with a validating
  `.claude-plugin/plugin.json` manifest (version synced to `pyproject.toml`).
- The full canonical `mm-*` skill set bundled into the plugin, reconciling the
  current `.claude/skills/` drift (`discard`, `explore`, `soul`, `update` are
  missing today).
- The four lifecycle hooks (`SessionStart`, `UserPromptSubmit` inject + log,
  `Stop` end+backup) carried by the plugin and portable to plugin-relative paths.
- The Mirror MCP server exposing the command surface + on-demand identity context.
- `statusLine` wired to `python -m memory welcome --status-line`.
- An isolated smoke test proving plugin load + skill discovery + hook firing +
  MCP reachability against a temporary database, with the production DB checksum
  unchanged.

---

## Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| [CV21.E2.S1](cv21-e2-s1-claude-plugin-conversion/index.md) | Claude plugin conversion | Implementation | The standalone `.claude/` skills + hooks become a canonical Claude plugin that passes `claude plugin validate`; isolated load smoke test | 🟡 Planned · plan + test-guide written |
| CV21.E2.S2 | Mirror MCP server | Implementation | `python -m memory mcp` serves the command surface + on-demand identity context; validates as an `mcpServers` entry; isolated smoke test | 🟡 Planned |
| CV21.E2.S3 | Plugin status line | Implementation | The plugin `statusLine` renders Mirror's compact status line on Claude | 🟡 Planned · may fold into S1 if trivial |
| CV21.E2.S4 | Reference-runtime smoke test | Integration | End-to-end isolated smoke test proving the full package (plugin + hooks + MCP) loads and runs equivalently to standalone `.claude/` | 🟡 Planned |

---

## Non-goals

- No per-runtime implementation (Codex E4–E5, Antigravity E7, Grok E10 consume
  this package; they are out of scope here).
- No forced migration of Claude users off standalone `.claude/`; both paths work.
- No automatic per-turn Mirror Mode injection *through MCP* — E1 proved MCP is
  pull-based; automatic injection stays in the runtime hooks.
- No marketplace publishing or public distribution channel (later epic / CV).
- No change to the Python `memory` core behavior beyond adding the `mcp`
  command surface.

---

## Done Condition

CV21.E2 is done when:

- a canonical Claude-format plugin bundling the full `mm-*` skill set + lifecycle
  hooks passes `claude plugin validate`;
- the Mirror MCP server (`python -m memory mcp`) serves the command surface +
  on-demand context and validates as a portable `mcpServers` entry;
- the plugin `statusLine` renders Mirror's status line on Claude;
- an isolated smoke test proves the package loads and runs equivalently to the
  standalone `.claude/` integration, with the production DB checksum unchanged;
- the runtime interface contract and decisions log note the plugin as the
  recommended Claude packaging, with standalone `.claude/` retained.

---

## References

- [CV21 — Runtime Expansion II](../index.md)
- [CV21.E1 Unified Plugin & MCP Spike](../cv21-e1-unified-plugin-mcp-spike/index.md)
- [Convergence decision](../../../decisions.md#cv21-converges-on-a-canonical-plugin-plus-mcp-server-bridged-by-import)
- [Runtime Interface Contract](../../../../product/specs/runtime-interface/index.md)
- Claude Code plugins: <https://docs.claude.com/en/docs/claude-code/plugins>
