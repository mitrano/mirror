[< CV13.E4](../index.md)

# CV13.E4.S1 — Conversation detail page

**Status:** ✅ Done
**Epic:** CV13.E4 — Conversation Intelligence
**Release target:** v0.14.0

---

## User-visible outcome

A stored conversation can be opened as a read-only transcript page showing its title, context, timestamps, summary, and ordered messages.

---

## Scope

- Add a read-only conversation detail API.
- Render a web transcript page for one stored conversation.
- Show roles, message timestamps, message content, title, interface, journey, persona, started/ended state, and summary when present.
- Support direct hash navigation to a known conversation id.
- Keep Workspace card linking as a later story.

---

## Non-goals

- No conversation retitle.
- No LLM calls.
- No batch operations.
- No message editing.
- No deletion.
- No raw database view.

---

## Validation

See [test guide](test-guide.md).
