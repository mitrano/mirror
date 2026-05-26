[< CV13.E5](../index.md)

# CV13.E5.S4 — Conversation repair dry-run and apply

**Status:** ✅ Done
**Epic:** CV13.E5 — Web Operations Runner
**Release target:** v0.15.0

---

## User-visible outcome

The web operations API can preview and explicitly apply a bounded repair for conversations missing journey association, so Workspace can reflect recent work without requiring terminal repair commands.

---

## Scope

- Mark `conversation-journey-repair` as runnable.
- Require a `dryRun` parameter, defaulting to `true`.
- In dry-run mode, return candidates without mutating conversations.
- In apply mode, create a backup first and then apply the high-confidence associations found by the existing repair logic.
- Support the existing `limit` parameter.
- Return structured evidence: candidate count, applied count, candidates, backup path when applied, and clear summary text.
- Reject unsafe parameters and future operations.

---

## Non-goals

- No arbitrary journey reassignment UI.
- No manual candidate editing.
- No low-confidence or fuzzy repair.
- No repair without a backup.
- No streaming or job history.
- No visible Operations UI yet.

---

## Validation

See [test guide](test-guide.md).
