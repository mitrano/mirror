[< CV9.E6 Web Visibility](../index.md)

# CV9.E6.S4 — Object Detail and Evidence Affordance

**Status:** 🟡 Planned  
**User-visible outcome:** Supported objects open into a common detail view with relationships and honest evidence/provenance states.

## Scope

Create the shared object detail grammar used by Atlas and Workspace:

- title;
- description;
- kind and id;
- relationships;
- evidence affordance;
- metadata;
- honest missing-provenance state.

## Acceptance Criteria

- Identity and persona objects have supported detail views.
- The same detail grammar can be reused by future memory, journey, conversation,
  task, and decision details.
- Evidence is shown when available and explicitly absent when not available.
- The detail route uses surface DTOs rather than route-level composition.

## Notes

This story should avoid claiming full provenance coverage. The important thing
is to establish the affordance and the honesty contract.
