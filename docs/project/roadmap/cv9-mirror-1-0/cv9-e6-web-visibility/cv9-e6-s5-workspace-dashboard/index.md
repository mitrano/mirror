[< CV9.E6 Web Visibility](../index.md)

# CV9.E6.S5 — Workspace Dashboard Slice

**Status:** 🟡 Planned  
**User-visible outcome:** Workspace shows a first useful read-only operational dashboard over available Mirror data.

## Scope

Implement the first Workspace read model after the Atlas surface pattern exists:

- active journeys section;
- recent conversations section;
- available tasks or operational context when service support is clean;
- relevant memories if they can be surfaced without ad hoc query logic;
- clear partial/empty states.

## Acceptance Criteria

- Workspace feels analytical and state-oriented, not like the Atlas psyche map.
- The dashboard uses the same shell, object model, detail grammar, and design
  tokens as Atlas.
- Workspace does not become a generic project-management clone.
- All sections are backed by surface DTOs.
- Unsupported areas are shown as honest empty or partial states.

## Notes

Decisions may remain derived or placeholder in 1.0 unless a stronger decision
model already exists by the time this story starts.
