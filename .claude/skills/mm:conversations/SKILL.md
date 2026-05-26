---
name: "mm:conversations"
description: Lists recent conversations from the memory database
user-invocable: true
---

# Conversations

When receiving `/mm:conversations`, run:

```bash
uv run python -m memory conversations [--limit N] [--journey ID] [--persona ID]
```

If `$ARGUMENTS` contains a filter such as a journey slug, use it as `--journey`.

Present the result to the user. Mention that `/mm:recall <id>` loads a conversation.

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
