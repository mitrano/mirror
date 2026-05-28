[< CV9.E2](../index.md)

# CV9.E2.S4 — Conversation Title Hardening

**Status:** Done
**Epic:** CV9.E2 — Stabilization & Robustness

---

## User-visible outcome

Conversation titles stop getting stuck as first-message fragments, skill-injection text, or blanks. Legacy conversations can be safely retitled through a bounded web operation with dry-run cost visibility before any database mutation.

---

## Scope

- Mark first-message titles as provisional when runtime logging creates them.
- Generate a better title at conversation close when the current title is blank, provisional, truncated, skill-like, or otherwise clearly low quality.
- Preserve manually edited titles and do not overwrite them automatically.
- Make the existing `batch-conversation-retitle` web operation runnable.
- Support dry-run candidate preview, token/cost estimation, and apply with backup.
- Preserve title provenance in conversation metadata.

---

## Non-goals

- No automatic retitle on page load.
- No unbounded batch apply.
- No transcript deletion or message edits.
- No arbitrary SQL or shell operation.
- No overwrite of titles marked as manual.

---

## Validation

See [test guide](test-guide.md).
