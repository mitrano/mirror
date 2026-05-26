---
name: "mm-conversations"
description: Lists recent conversations from the memory database
user-invocable: true
---

# Conversations

When receiving `/mm-conversations [--limit N] [--journey SLUG] [--persona NAME]`:

```bash
uv run python -m memory conversations [args]
```

Present the output to the user without modification.

Use this command to discover conversation IDs before recalling or repairing
conversation metadata. If the user needs to associate an existing conversation
with a journey, the underlying helpers are:

```bash
uv run python -m memory conversation-logger attach --conversation <conversation_id> --journey <journey_slug> [--persona <name>]
uv run python -m memory conversation-logger attach-latest-pi --journey <journey_slug> [--persona <name>]
```

`<conversation_id>` may be a full ID or an unambiguous prefix. Validate with:

```bash
uv run python -m memory conversations --journey <journey_slug>
```
