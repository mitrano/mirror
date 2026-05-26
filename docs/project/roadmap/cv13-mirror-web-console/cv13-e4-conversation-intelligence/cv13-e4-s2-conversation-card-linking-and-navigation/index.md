[< CV13.E4](../index.md)

# CV13.E4.S2 — Conversation card linking and navigation

**Status:** ✅ Done
**Epic:** CV13.E4 — Conversation Intelligence
**Release target:** v0.14.0

---

## User-visible outcome

Workspace conversation cards behave like real navigation controls: selecting a card opens the read-only conversation transcript, and the transcript can return to Workspace.

---

## Scope

- Make Workspace conversation cards clickable/keyboard-accessible.
- Route cards to `#conversation/<conversation-id>` using the read-only detail page from S1.
- Preserve the selected journey context when returning to Workspace.
- Keep visible metadata clear enough to understand which conversation is being opened.

---

## Non-goals

- No retitle.
- No LLM calls.
- No message editing.
- No transcript deletion.
- No batch operations.

---

## Validation

See [test guide](test-guide.md).
