[< Story](index.md)

# Test Guide — CV13.E4.S1 Conversation detail page

## Automated checks

```bash
uv run pytest tests/unit/memory/web/test_server.py tests/unit/memory/surfaces/test_workspace.py
uv run ruff check src/memory/web src/memory/surfaces tests/unit/memory/web/test_server.py tests/unit/memory/surfaces/test_workspace.py
uv run ruff format --check src/memory/web src/memory/surfaces tests/unit/memory/web/test_server.py tests/unit/memory/surfaces/test_workspace.py
node --check src/memory/web/static/app.js
git diff --check
```

## Manual browser validation

1. Open the web app with a Mirror that has stored conversations.
2. Copy a conversation id from the Workspace conversation card ID chip.
3. Open a direct conversation URL/hash: `#conversation/<conversation-id>`.
4. Confirm the page shows title, interface, started/ended state, journey/persona when present, summary when present, and ordered messages.
5. Confirm message roles and timestamps are visible.
6. Confirm the page is read-only: no retitle button, no edit form, no delete action, no LLM action.
7. Confirm the back button returns to Workspace.
