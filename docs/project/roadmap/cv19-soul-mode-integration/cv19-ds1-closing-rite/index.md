[< CV19](../index.md)

# CV19.DS1 — Closing Rite

**Status:** 🟡 Planned

**Placement:** First story in `v0.26.0 — Soul Mode Integration`

**User-visible outcome:** A user can close Soul Mode and see a ritual closing surface that gathers what was harvested, what still echoes, what remains open, and what may want integration.

---

## Why This Exists

Soul Mode can now open, listen, voice, mature, and harvest. But it does not yet have a clean ritual closing.

Without a Closing Rite, the user can leave with insight but no threshold. The rite needs a final surface that honors what appeared without immediately turning it into identity mutation, advice, or tasks.

Closing is not integration yet. It is the threshold before integration.

---

## Scope

- Add a Closing Rite surface for Soul Mode.
- Allow callers to pass situated closing material:
  - what was harvested;
  - what still echoes;
  - what remains open;
  - what may want integration.
- Add CLI rendering support for the closing rite.
- Update the Pi Soul Mode skill so natural-language requests like “let's close”, “encerrar”, or “fechar o rito” render the Closing Rite.
- Ensure closing does not save a journal entry, mutate identity, or apply integration.

---

## Non-goals

- No integration review classification yet.
- No psyche enrichment proposal yet.
- No identity mutation.
- No automatic journal save.
- No web UI.
- No new voice behavior.

---

## Acceptance Behavior

Given the user asks to close Soul Mode, Mirror renders a Closing Rite surface.

Given the Closing Rite renders, it includes what was harvested when available and can also include what still echoes, what remains open, and what may want integration.

Given the Closing Rite renders, no identity entry, journal entry, journey state, or project file is mutated automatically.

Given the user asks whether something should remain in identity, Mirror can name that this belongs to a future Integration Review or proposal step, not to Closing Rite itself.

---

## References

- [CV19 — Soul Mode Integration](../index.md)
- [CV18 — Soul Mode More Voices](../../cv18-soul-mode-more-voices/index.md)
