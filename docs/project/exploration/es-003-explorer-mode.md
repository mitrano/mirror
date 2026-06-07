[< Project](../briefing.md)

# ES-003 Explorer Mode

**Status:** Promoted to roadmap  
**Source:** Builder conversation on 2026-06-06, Ariad exploration references, and evidence from the Passagem exploratory conversation  
**Current attractor:** Explorer Mode as a native Mirror lens for uncertainty before construction  
**Delivery handoff:** [CV16 Explorer Mode](../roadmap/cv16-explorer-mode/index.md)  
**Capability Value:** CV16 Explorer Mode

---

## Initial Signal

Mirror has two strong operating lenses today:

- Mirror Mode reflects identity, memory, tensions, and personal or strategic sensemaking.
- Builder Mode turns a chosen journey into project construction, code changes, documentation updates, verification, and commits.

A third territory is appearing between them. Some material is too alive to leave as a normal reflective conversation, but too unformed to become Builder work. If it moves into Builder too soon, uncertainty is collapsed into premature commitment. If it remains only in Mirror Mode, important signals and story shifts can dissolve into essays.

Explorer Mode exists for this earlier territory: active exploration before construction.

---

## Thickened Story

Explorer Mode is a native Mirror lens for working with uncertainty before something becomes delivery, implementation, roadmap work, or durable archive.

It is not Builder Mode, because its purpose is not to edit files, implement behavior, validate a story, or close a delivery boundary. It is also not generic Mirror Mode, because it does more than reflect. It holds an active exploratory field where signals, tensions, corrections, hypotheses, and emerging stories are preserved and visibly thickened.

The key product failure that motivated this exploration came from the Passagem conversation. The user introduced material that changed the exploratory story, but the Mirror continued answering mostly as a reflective essay. The Ariad card occasionally appeared, but the story thickening was not reliably visible. Explorer Mode must correct that failure by making thickening part of the live experience, not an optional afterthought.

The strongest current distinction is:

```text
Explorer preserves uncertainty.
Builder executes commitment.
```

This is the product boundary. Explorer may formulate a hypothesis of construction, name a candidate, or propose promotion. It does not begin construction until the user explicitly confirms the lens switch.

---

## Activation Model

Explorer Mode should begin explicitly.

Candidate command:

```text
/mm-explore <journey>
```

Candidate natural-language activations:

```text
entrar em modo explorador nesta jornada
abrir exploração nesta jornada
```

Exit should also be explicit:

```text
sair do modo explorador
voltar ao modo normal
```

Promotion to Builder should be explicit:

```text
promover essa exploração para construção
promover para builder
```

While Explorer Mode is active, Mirror should assume that material brought by the user belongs to the exploratory field unless the user asks for a clear operational action, such as reading a file, summarizing a conversation, configuring a journey, or inspecting code. This reduces per-turn intent guessing and makes the mode precise because the user has already named the lens.

The first version should be a skill and context behavior, not a hidden runtime hook. The success criterion is not automatic detection. The success criterion is obedience to explicit exploration.

---

## Minimum State

The first usable version should preserve a small state surface.

```text
current_journey
current_exploratory_story
current_signal
signal_radar
narrative_field_summary
last_story_card
```

This state does not need to begin with a complex database model. A coherent first version can hold the state in Mirror context, journey context, or a simple structured artifact while the behavior is still being shaped. Persistence should follow behavior, not precede it.

The product risk is building storage before knowing the conversational contract. The first slice should prove that the Mirror can stay inside the exploratory lens, visibly thicken stories, and preserve the difference between signal, story, radar, snapshot, and promotion.

---

## First Surfaces

The initial surface vocabulary should stay small.

```text
Explorer Mode Active
Possible Signal
Signal Radar
Exploratory Story Opened
Story Thickened
Narrative Field Snapshot
Promotion Proposal
```

The most important surface is **Story Thickened**.

Possible Signal is useful, but it was not the core failure. The core failure was that the user corrected, refined, or deepened the exploration, and Mirror did not consistently return the accumulated story in its changed form. Explorer Mode should make the thickened current story visible whenever new material changes the story's meaning, tension, direction, or boundary.

---

## Natural Commands

Candidate first-version commands:

```text
abrir exploração
guardar no radar
abrir exploratory story
adensar essa história
mostrar campo narrativo
promover para builder
sair do modo explorador
```

These commands can start as skill instructions and natural-language conventions before becoming formal CLI subcommands. The mode should prefer a narrow, reliable vocabulary over a broad automatic classifier.

---

## Relationship With Ariad

Ariad Exploration is design inspiration, not a runtime architecture requirement.

The concepts that should carry forward are useful because they describe the work before delivery:

- signal;
- signal radar;
- exploratory story;
- story thickening;
- narrative field snapshot;
- candidate;
- promotion boundary;
- archive.

The implementation should remain Mirror-native. Explorer Mode belongs to Mirror's mode system and identity runtime, not to Maestro as a required overlay. Ariad can continue informing the method, especially around preservation of uncertainty and promotion into Delivery, but the product promise should be understandable to the Mirror community without requiring Ariad vocabulary first.

---

## Candidate Capability Value

### CV16 Explorer Mode

**Capability Value:** Mirror gains a native exploratory lens that preserves uncertainty, visibly thickens signals into exploratory stories, and proposes explicit promotion to Builder only when the user confirms readiness.

### Community Promise

Mirror is not only a place to reflect or build. It can also hold the uncertain middle: the field where something is becoming clear but is not ready to become work.

Explorer Mode lets a user enter that field deliberately. While active, Mirror listens for signals, opens exploratory stories, shows when the story thickens, keeps nearby signals in a radar, renders narrative field snapshots, and offers promotion when a candidate is ready. It does not silently convert exploration into delivery.

### Done Condition Seed

CV16 is done when a user can explicitly enter Explorer Mode for a journey, explore across multiple turns with visible story thickening, keep signals in radar, request a narrative field snapshot, receive a promotion proposal, and explicitly promote the exploration into Builder without hidden mode switching or premature construction.

---

## Roadmap Handoff

This exploration has been promoted into [CV16 Explorer Mode](../roadmap/cv16-explorer-mode/index.md).

The promoted delivery arc is:

1. Explorer activation contract.
2. In-session exploratory field.
3. Story thickening surfaces.
4. Promotion handoff to Builder.
5. Persistence and visibility after the conversational behavior is proven.

The first delivery story should avoid full persistence, web UI, or autonomous detection. It should prove the core mode behavior inside the conversational runtime.

---

## Conscious Non-Goals for First Slice

- No hidden hook-based intent interception.
- No automatic conversion from Mirror Mode to Explorer Mode.
- No automatic promotion to Builder.
- No requirement to implement Maestro as runtime substrate.
- No complex database schema before behavior is validated.
- No broad automatic classifier for every possible signal.
- No web console surface in the first slice unless the CLI behavior is already coherent.

---

## Open Questions

### Answered

- `/mm-explore <journey>` should only set mode context. It should not start a new conversation session by itself.
- Explorer Mode should be of the same nature as Builder Mode: an explicit operating lens for a journey, not a specialization hidden inside Mirror Mode.
- The first implementation should support only one current exploratory story per journey session.
- End users should not be expected to operate Mirror through commands. Natural language remains the product interface. Formal commands are behavioral resources the Mirror may use when a contained operation is appropriate.

### Still Open

- Where should non-persistent first-version state live: runtime state, journey identity, local context file, or session-scoped database state?
- How should `last_story_card` be represented so the next turn can thicken instead of replacing the story?
- What is the smallest promotion brief that Builder can consume without pretending the exploration is already a full delivery plan?

---

## Carry Forward Notes

- Explicit activation is a product principle, not just an implementation shortcut.
- Story Thickened is the core user-visible experience.
- Explorer Mode should assume exploratory intent while active, except for clear operational requests.
- Persistence should come after the mode behavior is coherent.
- Promotion to Builder must require explicit Navigator confirmation.
- Ariad's Exploration method should inform language and boundaries, but Mirror should own the runtime mode.
- The first public explanation should avoid presenting Explorer Mode as a project management feature. It is a cognitive lens for uncertainty before commitment.
- DS4 revised the first behavior slice away from signal/radar modeling. Signals remain possible method vocabulary, but the product behavior now starts from the accumulated Exploratory Story because that is the observable value in practice.
