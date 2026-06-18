---
name: "mm:journey"
description: Shows detailed journey status, creates journeys, and updates the journey path
user-invocable: true
---

# Journey

Use `/mm:journey` or `/mm:journey reflexo` to inspect journey status.

Use `/mm:journey create` to create a journey interactively.

## 1. Create Journey

When receiving `/mm:journey create` without enough fields, ask for: slug, name, description, briefing, and context. Then run:

```bash
uv run python -m memory journey create <slug> \
  --name "<name>" \
  --description "<description>" \
  --briefing "<briefing>" \
  --context "<context>"
```

If fields are already provided, pass them through to:

```bash
uv run python -m memory journey create <args>
```

## 2. Load Status

```bash
uv run python -m memory journey [JOURNEY]
```

If `$ARGUMENTS` was passed, use it as the journey name. Otherwise the script loads all journeys.

The script prints identity, journey path, recent memories, and recent conversations for each journey.

## 3. Synthesize

Combine the script output into a clear view of current progress.

## 4. Suggest Updates

If the journey path appears outdated relative to recent conversations and memories, suggest an update. After user confirmation:

```bash
uv run python -m memory journey update JOURNEY "UPDATED_CONTENT"
```

For long content, use stdin:

```bash
echo "CONTENT" | uv run python -m memory journey update JOURNEY -
```
