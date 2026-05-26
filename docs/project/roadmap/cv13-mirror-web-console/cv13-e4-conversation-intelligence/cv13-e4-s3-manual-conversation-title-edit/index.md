[< CV13.E4](../index.md)

# CV13.E4.S3 — Manual conversation title edit

**Status:** ✅ Done
**Epic:** CV13.E4 — Conversation Intelligence
**Release target:** v0.14.0

---

## User-visible outcome

A selected conversation title can be edited manually from its transcript page without invoking an LLM or modifying message content.

---

## Scope

- Add a safe service-backed conversation title update.
- Add a guarded web endpoint for one conversation title.
- Add a simple title edit form to the conversation detail page.
- Refresh the transcript title after save.
- Keep message content read-only.

---

## Non-goals

- No generated titles.
- No LLM calls.
- No batch retitle.
- No message editing.
- No conversation deletion.

---

## Validation

See [test guide](test-guide.md).
