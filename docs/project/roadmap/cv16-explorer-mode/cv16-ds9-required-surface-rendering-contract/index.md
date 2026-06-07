[< CV16](../index.md)

# CV16.DS9 — Required Surface Rendering and Operational Boundary Contract

**Status:** 🟡 Planned

**Placement:** CV16 release hardening story

**User-visible outcome:** Required Explorer surfaces such as `△ STORY THICKENED` and `△ BUILDER HANDOFF PROPOSED` cannot disappear into assistant interpretation, and clear operational requests such as editing files, applying procedures, or creating code are routed out of Explorer before mutation.

---

## Why This Exists

During external validation, `explore story thicken` correctly returned the `△ STORY THICKENED` surface, but the assistant summarized the concept instead of showing the card. The failure was not state or CLI behavior. It was the presentation contract between contained command output and the final assistant response.

Explorer surfaces are product output, not internal evidence. Explorer is also not the right lens for mutating project files. When the user asks for a clear operational action, Mirror must not force that request into story thickening or exploration.

---

## Scope

- Mark required Mirror surfaces in CLI output with an explicit contract marker.
- Update runtime skill instructions to require verbatim first-block rendering.
- Preserve the narrative/substantive versus local/refinement boundary before `story thicken` is called.
- Add an operational boundary rule for clear file, code, doc, command, and mutation requests while Explorer Mode is active.
- Require a visible mode-boundary response before mutating files or creating code from Explorer Mode.
- Add tests or smoke validation proving Explorer surfaces are distinguishable from ordinary command output.
- Investigate whether Pi can enforce or preserve required surface blocks automatically.

---

## Non-goals

- No broad runtime rendering framework.
- No changes to Explorer story semantics.
- No Builder handoff behavior changes beyond surface preservation.

---

## Acceptance Behavior

Given an Explorer command returns a required surface, the assistant renders that surface before commentary.

Given a required surface is present in CLI output, it is machine-identifiable by a stable marker.

Given external validation runs in Pi, `△ STORY THICKENED` appears immediately after a substantive story change.

Given the user makes a local refinement, such as icon, microcopy, visual label, or wording polish, Explorer does not call `story thicken` unless the user explicitly asks to preserve it in the Exploratory Story.

Given the user asks Explorer Mode to edit files, apply a procedure to a document, create code, run implementation commands, or otherwise mutate project state, Mirror does not treat the request as exploratory thickening. It names the request as operational work and asks to switch to Builder Mode, or uses an explicit operational override if the future contract defines one.

---

## References

- [CV16 Explorer Mode](../index.md)
