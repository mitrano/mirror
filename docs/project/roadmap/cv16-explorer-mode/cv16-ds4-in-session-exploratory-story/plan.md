[< Story](index.md)

# Plan — CV16.DS4 In-Session Exploratory Story

## Boundary

This story adds the minimal story substrate for Explorer Mode. It should be observable through contained CLI operations and through `explore load`, but it should not yet try to generate the final Explorer card grammar. DS5 owns the user-facing Story Thickened and Narrative Field Snapshot surfaces.

The story is in-session and journey-scoped. It is allowed to live in runtime state because DS7 owns durable persistence and visibility after conversational behavior is proven. Signals and radar are intentionally left out of this slice because their practical value is not yet clear; the observable value is the Exploratory Story itself.

## State Model

Create a small dataclass, likely in `src/memory/services/explorer_story.py`:

```python
@dataclass(frozen=True)
class ExplorerStory:
    journey: str
    current_exploratory_story: str | None = None
    narrative_field_summary: str | None = None
    last_story_card: str | None = None
```

Store one story per journey in `runtime_sessions` using a dedicated synthetic session id:

```text
__explorer_story__:<journey>
```

Use JSON metadata for the story payload. Keep `active=True` while the story exists. This avoids a schema migration and keeps DS4 aligned with the first-slice principle that persistence follows behavior.

## Service Operations

Add service functions:

```python
get_explorer_story(store, journey) -> ExplorerStory | None
update_explorer_story(store, journey, *, current_exploratory_story=None, narrative_field_summary=None, last_story_card=None) -> ExplorerStory
clear_explorer_story(store, journey) -> None
render_explorer_story_context(story) -> str
```

Update semantics:

- omitted arguments leave existing values unchanged;
- provided strings replace scalar fields after trimming;
- empty strings clear scalar fields only if explicitly supported by CLI flags;
- story reads tolerate invalid JSON by returning `None` rather than crashing.

## CLI Operations

Extend `src/memory/cli/explore.py` with contained operations:

```bash
uv run python -m memory explore story show <journey>
uv run python -m memory explore story update <journey> \
  --story "..." \
  --summary "..." \
  --last-card "..."
uv run python -m memory explore story clear <journey>
```

The command names are intentionally plain because they are not the final natural-language product interface. They are the contained resource the Mirror skill can call after interpreting the user's natural language.

`explore load <journey>` should include the rendered story context after normal identity context when a story exists.

## Pi Skill Contract

Update `.pi/skills/mm-explore/SKILL.md`:

- when new material changes the Exploratory Story, call `explore story update` with the updated story shape;
- when the user asks what is currently being explored, call `explore story show`;
- continue to avoid Builder promotion without explicit confirmation.

## Tests

Add `tests/unit/memory/services/test_explorer_story.py` for service behavior:

- creates a story for a journey;
- updates scalar fields without erasing omitted fields;
- isolates stories by journey;
- clears a story;
- invalid metadata returns no story.

Extend `tests/unit/memory/cli/test_explore.py` for CLI behavior:

- update command stores story data;
- show command renders stored story;
- clear command removes stored story;
- `cmd_load()` includes story context when present.

## Validation Route

Automated:

```bash
uv run pytest \
  tests/unit/memory/services/test_explorer_story.py \
  tests/unit/memory/cli/test_explore.py
```

Lint:

```bash
uv run ruff check \
  src/memory/services/explorer_story.py \
  src/memory/cli/explore.py \
  tests/unit/memory/services/test_explorer_story.py \
  tests/unit/memory/cli/test_explore.py
```

Manual smoke:

```bash
uv run python -m memory explore story update explorer-mode \
  --story "Explorer Mode is becoming a story field, not only a mode flag." \
  --summary "The current design is testing minimal runtime state before persistence." \
  --last-card "Story opened around in-session continuity."

uv run python -m memory explore story show explorer-mode
uv run python -m memory explore load explorer-mode >/tmp/mirror-explore-story-load.txt
uv run python -m memory explore story clear explorer-mode
uv run python -m memory explore story show explorer-mode
```

Expected:

- show renders the stored story;
- load includes the story context;
- clear removes it;
- a second journey does not see the first journey's story.

## Risks

### Runtime state becomes accidental persistence

The story will survive until cleared because it is in SQLite runtime state. That is acceptable for DS4, but docs and naming should avoid presenting it as durable Explorer archive. DS7 owns real persistence and visibility.

### CLI shape becomes product shape

The `story update/show/clear` commands are operational resources. The product surface remains natural language through the skill.

### Too much behavior before surfaces

DS4 should not render polished Story Thickened cards. It should create the story state that DS5 can use to render them coherently.
