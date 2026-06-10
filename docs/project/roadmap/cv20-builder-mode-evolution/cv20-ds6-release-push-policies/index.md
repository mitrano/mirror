[< CV20](../index.md)

# CV20.DS6 — Release And Push Policies

**Status:** 🟡 Planned

---

## Outcome

Builder distinguishes commit, push, and release as separate gestures governed by the effective Ariad policy.

Release can be planned before story work or emerge after completed stories create a coherent public boundary. Push can remain conservative by default or become automatic after release publication when configured.

---

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| CV20.DS6.US1 | Release intent surface | User Story | Builder can surface planned or emergent release intent after Done or parent collapse | 🟡 Planned |
| CV20.DS6.TS1 | Commit and push policy resolver | Technical Story | Runtime resolves commit and push policies from method, project, journey, and overrides | 🟡 Planned |
| CV20.DS6.US2 | Push checkpoint or autopush | User Story | Builder asks before push by default and supports configured auto-push after release publication | 🟡 Planned |

---

## Done Condition

DS6 is done when Builder can record local history, push remote history, and prepare release work without conflating those actions.
