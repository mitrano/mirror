[< CV9.DS7](../index.md)

# CV9.DS7.US2 — Apply Metadata Lifecycle Decisions Safely

**Type:** User Story  
**Status:** Active; blocked by operation surface  
**Parent:** [CV9.DS7 Conversation Metadata Lifecycle](../index.md)

---

## Intent

Apply accepted conversation metadata lifecycle decisions during conversation
metadata updates without creating durable weak metadata and without overriding
manual/user-edited title locks.

---

## Observable Behavior Seed

Conversation metadata updates follow lifecycle decisions for title, summary,
tags, readiness, provenance, confidence, and update source while preserving
manual locks.

---

## Pull State

Pulled after CV9.DS7.US1 and CV9.DS7.TS1 closed. D-001 triggered during the plan gate, so [CV9.DS7.TS2](../cv9-ds7-ts2-extract-metadata-lifecycle-policy-boundary/index.md) extracted the policy boundary. The bounded apply service was then implemented and reclassified as [CV9.DS7.TS3](../cv9-ds7-ts3-bounded-metadata-lifecycle-apply-service/index.md), because its validation is internal/automated. US2 remains open until [CV9.DS7.US3](../cv9-ds7-us3-metadata-lifecycle-operation-report/index.md) provides a Navigator-facing operation surface.

## Plan and Validation

- [Plan](plan.md)
- [Test Guide](test-guide.md)
