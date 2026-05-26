[< CV13](../index.md)

# CV13.E4 — Conversation Intelligence

**Status:** 🟢 In Progress
**Release target:** v0.14.0

---

## User-visible outcome

Stored conversations become readable and navigable in the web app, then gain safe title-improvement operations that only run when explicitly requested.

---

## Stories

| Code | Story | User-visible outcome | Status |
|------|-------|----------------------|--------|
| [CV13.E4.S1](cv13-e4-s1-conversation-detail-page/index.md) | Conversation detail page | A stored conversation can be opened as a read-only transcript page | ✅ Done |
| CV13.E4.S2 | Conversation card linking and navigation | Workspace conversation cards link to their detail pages with clear back navigation | 🟢 In Progress |
| CV13.E4.S3 | Manual conversation title edit | A selected conversation title can be safely edited without LLM calls | 🟡 Planned |
| CV13.E4.S4 | Single conversation retitle | A selected conversation can request an LLM title suggestion and save it only after approval | 🟡 Planned |
| CV13.E4.S5 | Legacy retitle planning / dry-run | Legacy conversation retitle can be previewed safely before any batch execution | 🟡 Planned |

---

## Guardrails

- No LLM calls on page load.
- No batch mutation in this epic until preview/dry-run boundaries exist.
- No message editing.
- No transcript deletion.
- No raw database editor.
