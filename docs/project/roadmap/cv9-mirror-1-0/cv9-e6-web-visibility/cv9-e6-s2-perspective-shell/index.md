[< CV9.E6 Web Visibility](../index.md)

# CV9.E6.S2 — Perspective Shell and Preference

**Status:** 🟢 Planned — Plan checkpoint ready
**User-visible outcome:** The local web app lets the user choose Atlas or Workspace, remembers the default, and keeps a stable shell across perspectives.

## Scope

Add the shared web shell for Mirror visibility:

- first-run perspective choice when no default exists;
- perspective switcher;
- stable header with Mirror identity and global search affordance;
- user-home default perspective preference;
- honest fallback when the preference cannot be read or written.

## Acceptance Criteria

- A new local web session asks for a perspective when no default exists.
- The default perspective is stored in the user home, not only in browser-local
  state.
- The active perspective remains visible and switchable.
- Atlas and Workspace share the same shell.
- The docs browser remains accessible or intentionally repositioned.

## Plan and Validation

- [Plan](plan.md)
- [Test Guide](test-guide.md)

## Notes

This story should not implement the full Atlas or Workspace content. It creates
the frame they will inhabit.
