[< Story](index.md)

# Test Guide — CV16.DS4 In-Session Exploratory Story

## Automated Verification

```bash
uv run pytest \
  tests/unit/memory/services/test_explorer_story.py \
  tests/unit/memory/cli/test_explore.py
```

Expected: all tests pass.

Lint:

```bash
uv run ruff check \
  src/memory/services/explorer_story.py \
  src/memory/cli/explore.py \
  tests/unit/memory/services/test_explorer_story.py \
  tests/unit/memory/cli/test_explore.py
```

Expected: all checks pass.

## Manual Smoke

Create or update the active story:

```bash
uv run python -m memory explore story update explorer-mode \
  --story "Explorer Mode is becoming a story field, not only a mode flag." \
  --summary "The current design is testing minimal runtime state before persistence." \
  --last-card "Story opened around in-session continuity."
```

Inspect the story:

```bash
uv run python -m memory explore story show explorer-mode
```

Expected: output includes the story, summary, and last card.

Load Explorer Mode with the stored story:

```bash
uv run python -m memory explore load explorer-mode >/tmp/mirror-explore-story-load.txt
rg "Exploratory Story|story field|in-session continuity" /tmp/mirror-explore-story-load.txt
```

Expected: load output includes the story context.

Clear the story:

```bash
uv run python -m memory explore story clear explorer-mode
uv run python -m memory explore story show explorer-mode
```

Expected: the story is gone or shown as empty.

## Pass Condition

Explorer Mode can preserve and expose one current Exploratory Story for the active journey without introducing durable Explorer persistence, hidden detection, signal/radar modeling, or Builder promotion behavior.
