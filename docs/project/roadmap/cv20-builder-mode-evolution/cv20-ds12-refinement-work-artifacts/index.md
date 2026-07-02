[< CV20](../index.md)

# CV20.DS12 — Refinement Work Artifacts

**Status:** 🟡 Planned

---

## Outcome

Builder records Ariad Refinement Work as durable project artifacts, not only as database state and conversation surfaces.

Refinement Stories and Change Requests keep their operational state in the Workbench database, but their meaningful phase outputs — scope confirmation, implementation plan, implementation evidence, validation evidence, done notes, RS review, RS coherence, and closure summary — are materialized into inspectable files in the project workspace.

---

## Why This Exists

Dogfooding the Refinement CR cycle showed that the runtime captures state and evidence in SQLite, while Delivery Work already has a stronger artifact trail through story package files such as `plan.md`, `test-guide.md`, `review.md`, and `coherence.md`.

For small CRs, database state is enough to operate. For long-lived Refinement Stories, cross-session review, coherence checks, and future roadmap migration need durable artifacts that can be read, diffed, committed, reviewed, and referenced outside the database.

---

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| CV20.DS12.TS1 | Define Refinement Artifact Layout | Technical Story | The project has a canonical path and file structure for RS/CR artifacts | 🟡 Planned |
| CV20.DS12.TS2 | Materialize CR Phase Artifacts | Technical Story | CR scope, plan, implementation evidence, validation evidence, and done notes can be written to durable files | 🟡 Planned |
| CV20.DS12.TS3 | Materialize RS Review And Coherence Artifacts | Technical Story | RS review, coherence, and close outputs are written as durable project artifacts | 🟡 Planned |
| CV20.DS12.US1 | Show Artifact References In Refinement Surfaces | User Story | Navigator-facing Refinement surfaces show relevant artifact paths when artifacts are produced | 🟡 Planned |
| CV20.DS12.TS4 | Preserve Database As Operational Cursor | Technical Story | Runtime state remains in SQLite while project artifacts provide reviewable history; the two stay coherent | 🟡 Planned |

---

## Boundary

- This does not replace the Workbench database; SQLite remains the operational state store.
- This does not require every tiny CR to become a roadmap Delivery Story.
- This should not create noisy files for empty or purely transient events.
- Artifact generation must be deterministic, diff-friendly, and safe to commit.
- Artifact paths and required outputs should eventually be governed by the Ariad method DSL once Refinement DSL governance lands.

---

## Done Condition

DS12 is done when Refinement Stories and Change Requests can produce durable, project-local artifacts for their meaningful phase outputs, those artifacts are referenced by runtime surfaces, and RS-level review/coherence can rely on files plus database state instead of conversation history alone.
