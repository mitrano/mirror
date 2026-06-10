[< CV20](../index.md)

# CV20.DS3 — Builder Resume Surface

**Status:** 🟡 Planned

---

## Outcome

Builder load resumes an Ariad-governed journey from method DSL, roadmap files, and persisted runtime state.

The Navigator sees a concise briefing, roadmap position, active delivery item, active checkpoint, pending confirmation, and allowed next actions.

---

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| CV20.DS3.US1 | Resume Ariad journey | User Story | Builder load renders current journey, roadmap, checkpoint, and next actions | 🟡 Planned |
| CV20.DS3.TS1 | Delivery cursor persistence | Technical Story | Runtime stores and loads active item, checkpoint, pending transition, and evidence index | 🟡 Planned |
| CV20.DS3.TS2 | Roadmap position resolver | Technical Story | Builder resolves active roadmap position according to Ariad taxonomy | 🟡 Planned |

---

## Done Condition

DS3 is done when Builder can reopen an adopted journey and place the Navigator exactly where delivery previously stopped.
