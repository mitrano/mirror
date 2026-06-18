---
name: "mm-journey"
description: Shows detailed journey status and optionally updates the journey path
user-invocable: true
---

# Journey

When receiving `/mm-journey [slug]`:

```bash
uv run python -m memory journey [slug]
```

When receiving `/mm-journey create` without enough fields, run an interactive agent workflow:

1. Ask for: slug, name, description, briefing, and context.
2. Keep the slug lowercase with hyphens, e.g. `my-journey`.
3. Create the journey with:

```bash
uv run python -m memory journey create <slug> \
  --name "<name>" \
  --description "<description>" \
  --briefing "<briefing>" \
  --context "<context>"
```

When receiving `/mm-journey create <slug> ...` with fields already provided, pass them through to:

```bash
uv run python -m memory journey create <args>
```

When receiving `/mm-journey update <slug> <content>`:

```bash
uv run python -m memory journey update <slug> "<content>"
# or pipe via stdin:
echo "<content>" | uv run python -m memory journey update <slug> -
```

Present the output to the user.
