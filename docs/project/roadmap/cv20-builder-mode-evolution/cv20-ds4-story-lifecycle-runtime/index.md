[< CV20](../index.md)

# CV20.DS4 — Story Lifecycle Runtime

**Status:** 🟡 Planned

---

## Outcome

Builder can guide one Ariad story through Pull, Prepare, Plan, Implement, Validation, Review, Coherence, and Done using deterministic lifecycle gates.

---

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| CV20.DS4.US1 | Pull and Prepare | User Story | Navigator can pull DS/US/TS work and see Prepare assess context, risks, rules, and granularity | 🟡 Planned |
| CV20.DS4.US2 | Plan checkpoint gate | User Story | Builder creates a plan surface and blocks implementation until Navigator approval | 🟡 Planned |
| CV20.DS4.US3 | Validation checkpoint | User Story | Builder runs automated checks and presents a concrete Navigator validation route | 🟡 Planned |
| CV20.DS4.US4 | Coherence and Done gate | User Story | Builder verifies traces, records history according to policy, closes the story, and recommends next Pull | 🟡 Planned |

---

## Done Condition

DS4 is done when a non-trivial story can move through the Ariad lifecycle without the Driver silently skipping checkpoints or declaring progress without required artifacts.
