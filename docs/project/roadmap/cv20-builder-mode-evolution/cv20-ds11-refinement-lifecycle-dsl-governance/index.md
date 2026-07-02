[< CV20](../index.md)

# CV20.DS11 — Refinement Lifecycle DSL Governance

**Status:** 🟡 Planned

---

## Outcome

Ariad governs Refinement Work through the same method-definition architecture that governs Delivery Work.

Refinement Stories, Change Requests, CR-cycle gates, RS-level review/coherence/close, transition prompts, deterministic surfaces, and Navigator stop conditions are declared as method data instead of being encoded only in Workbench runtime code or renderer conventions.

---

## Why This Exists

CV20.DS6 made Refinement Work usable: Builder can hold Refinement Stories, capture Change Requests, move CRs through their cycle, and render Navigator-facing surfaces.

Dogfooding then revealed a governance gap: Delivery Work is substantially DSL-governed, while Refinement Work still depends on imperative runtime conventions for lifecycle phases, transition prompts, surface grammar, and visual/event behavior.

This story closes that gap so Refinement Work is not a special-case subsystem. It becomes part of the effective Ariad method.

---

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| CV20.DS11.TS1 | Model Refinement Lifecycle In Method DSL | Technical Story | Method definitions can declare Refinement Story flow and Change Request cycle phases, gates, and stop conditions | 🟡 Planned |
| CV20.DS11.TS2 | Declare Refinement Surfaces And Routes | Technical Story | Refinement Work surfaces, events, and routes are represented as method data, including semantic flow-event headers | 🟡 Planned |
| CV20.DS11.US1 | Render Refinement Prompts From Effective Method | User Story | Builder selection/planning/validation prompts for CRs come from the effective method definition rather than hard-coded renderer text | 🟡 Planned |
| CV20.DS11.TS3 | Respect Refinement Overrides And Inspection | Technical Story | Method inspection and future overrides can show and adjust Refinement lifecycle preferences alongside Delivery preferences | 🟡 Planned |
| CV20.DS11.US2 | Prove Refinement DSL Governance Through Dogfooding | User Story | Existing RS/CR workflows continue to work while tests prove lifecycle gates, prompts, and surfaces are driven by method data | 🟡 Planned |

---

## Boundary

- This is not a redesign of the Refinement Work conceptual model.
- This does not add autonomous CR advancement.
- This does not remove deterministic runtime safeguards; DSL data declares the method, runtime code still enforces it.
- This should preserve the RS/CR storage model and human-readable display codes unless implementation pressure proves otherwise.

---

## Done Condition

DS11 is done when Refinement lifecycle phases, CR-cycle gates, RS-level transitions, transition prompts, surface definitions, and Navigator stop conditions are inspectable as Ariad method data and the Builder runtime uses the effective method definition to render and enforce Refinement Work behavior.
