[< Story](index.md)

# Plan — CV16.DS5 Story Thickening Surfaces

## Boundary

This story turns DS4's in-session Exploratory Story into visible Explorer behavior. It should render deterministic surfaces and update/read the existing story state, but it should not introduce autonomous interpretation, LLM rewriting, durable persistence, or Builder handoff.

The Mirror can decide in the conversation when to call the contained operations. The Python core only provides reliable operations and surfaces.

## Surface Model

Add a plain-text surface module, likely:

```text
src/memory/surfaces/explorer_story.py
```

Candidate renderers:

```python
render_exploratory_story_opened(story: ExplorerStory) -> str
render_story_thickened(story: ExplorerStory, *, changed: str | None = None) -> str
render_narrative_field_snapshot(story: ExplorerStory) -> str
```

Keep these surfaces compact and visibly distinct from raw context. They should use the same box language as mode transitions where helpful, but do not over-abstract the existing renderer unless necessary.

## CLI Operations

Extend `python -m memory explore story` with surface-oriented operations:

```bash
uv run python -m memory explore story open <journey> \
  --story "..." \
  --summary "..." \
  --last-card "..."

uv run python -m memory explore story thicken <journey> \
  --story "..." \
  --summary "..." \
  --last-card "..." \
  --changed "..."

uv run python -m memory explore story snapshot <journey>
```

Semantics:

- `open` updates the story and renders `△ EXPLORATORY STORY OPENED`.
- `thicken` updates the story and renders `△ STORY THICKENED`.
- `snapshot` reads the stored story and renders `△ NARRATIVE FIELD SNAPSHOT`.
- `snapshot` should handle missing stories gracefully.

Retain DS4's lower-level commands:

```bash
story update
story show
story clear
```

Those are still useful for testing and direct inspection.

## Skill Contract

Update `.pi/skills/mm-explore/SKILL.md` so the assistant uses the new operations:

- when a story begins, call `story open` and render the surface;
- when new material changes the accumulated story, call `story thicken` and render the surface;
- when the user asks for the current field/story, call `story snapshot`;
- never switch to Builder without explicit confirmation.

## Tests

Add `tests/unit/memory/surfaces/test_explorer_story.py`:

- opened surface includes title, journey, and current story;
- thickened surface includes title, changed text, current story, and summary when present;
- snapshot surface includes current story, summary, and last card;

Extend `tests/unit/memory/cli/test_explore.py`:

- `cmd_story_open` stores story and renders opened surface;
- `cmd_story_thicken` updates story and renders thickened surface;
- `cmd_story_snapshot` renders stored story;
- missing story snapshot returns a clear message.

## Validation Route

Automated:

```bash
uv run pytest \
  tests/unit/memory/surfaces/test_explorer_story.py \
  tests/unit/memory/services/test_explorer_story.py \
  tests/unit/memory/cli/test_explore.py
```

Lint:

```bash
uv run ruff check \
  src/memory/surfaces/explorer_story.py \
  src/memory/services/explorer_story.py \
  src/memory/cli/explore.py \
  tests/unit/memory/surfaces/test_explorer_story.py \
  tests/unit/memory/services/test_explorer_story.py \
  tests/unit/memory/cli/test_explore.py
```

Manual smoke:

```bash
uv run python -m memory explore story open explorer-mode \
  --story "Explorer Mode is becoming visibly stateful." \
  --summary "The story now has a surface, not only stored state." \
  --last-card "Opened around visible Explorer behavior."

uv run python -m memory explore story thicken explorer-mode \
  --story "Explorer Mode is becoming visibly stateful through story surfaces." \
  --summary "The design shifted from storage to visible thickening." \
  --last-card "Story thickened around observable behavior." \
  --changed "The useful unit is the visible story, not a signal taxonomy."

uv run python -m memory explore story snapshot explorer-mode
```

Expected:

- each operation renders a distinct `△` Explorer surface;
- `thicken` updates the stored story;
- `snapshot` reflects the latest story;

## Risks

### Surfaces become decorative

The surface should not be a banner over unchanged content. `Story Thickened` should be used when the story shape changes. The operation cannot judge that autonomously; the skill contract must place responsibility on the assistant during Explorer Mode.

### Experiment proposal belongs elsewhere

DS6 owns attractors and experiment proposals. DS5 should stop at making the Exploratory Story visible.

### Too many commands

These commands are not the product interface. They are contained resources for the assistant and validation. Natural language remains the interface.
