[< Story](index.md)

# Test Guide — CV13.E4.S2 Conversation card linking and navigation

## Automated checks

```bash
uv run pytest tests/unit/memory/surfaces/test_workspace.py tests/unit/memory/web/test_server.py
uv run ruff check src/memory/web src/memory/surfaces tests/unit/memory/surfaces/test_workspace.py tests/unit/memory/web/test_server.py
uv run ruff format --check src/memory/web src/memory/surfaces tests/unit/memory/surfaces/test_workspace.py tests/unit/memory/web/test_server.py
node --check src/memory/web/static/app.js
git diff --check
```

## Manual browser validation

1. Open Workspace and select a journey with conversations.
2. Confirm conversation cards look clickable/focusable.
3. Click a conversation card.
4. Confirm the transcript page opens and the URL becomes `#conversation/<id>`.
5. Return with “Back to Workspace” and confirm the Workspace view returns.
6. Focus a conversation card with the keyboard and press Enter/Space.
7. Confirm it opens the same transcript page.
8. Confirm no retitle/edit/delete/LLM actions appear.
