[< CV16](../index.md)

# CV16.DS4 — In-Session Exploratory Story

**Status:** ✅ Done

**Placement:** CV16 first stateful Explorer behavior story

**User-visible outcome:** While Explorer Mode is active, Mirror can preserve one current Exploratory Story for the active journey, including its accumulated story, narrative summary, and last story card context for the next turn.

---

## Why This Exists

DS3 made Explorer Mode enterable and leaveable. The next gap is continuity. Without a small field state, Explorer Mode can only instruct the assistant to preserve uncertainty in the current answer. It cannot reliably carry the exploratory shape across turns.

DS4 adds the minimal state substrate for the live Explorer conversation. This is intentionally not durable product persistence yet. The goal is to give the active Explorer lens one story that can be updated, inspected, and loaded into context while the journey session is active.

---

## Scope

- Add a small Explorer story service for one current Exploratory Story per journey.
- Store the story in runtime state, not in a new database schema.
- Include fields for current journey, exploratory story, narrative field summary, and last story card.
- Expose contained CLI operations to inspect, update, and clear the story.
- Load the story into `explore load` output when it exists.
- Update the Pi skill contract so Mirror updates or inspects the story during Explorer Mode work.

---

## Non-goals

- No signal/radar model in this slice.
- No LLM-based signal classifier.
- No automatic story thickening surface grammar.
- No promotion handoff to Builder.
- No long-term persistence or web visibility.
- No multi-story model.
- No schema migration.

---

## Acceptance Behavior

Given Explorer Mode is active for a journey, when Mirror records exploratory material, the current story is stored under that journey and can be read on the next turn.

Given a story already exists, when `explore load <journey>` runs again, the output includes the current Exploratory Story context.

Given the story is cleared, subsequent Explorer context no longer includes the previous story, summary, or last card.

Given multiple journeys exist, each journey has an isolated current Explorer story.

---

## References

- [Plan](plan.md)
- [Test Guide](test-guide.md)
- [CV16 Explorer Mode](../index.md)
- [ES-003 Explorer Mode](../../../exploration/es-003-explorer-mode.md)
