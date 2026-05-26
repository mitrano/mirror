[< Story](index.md)

# Test Guide — CV13.E4.S3 Manual conversation title edit

## Automated checks

```bash
uv run pytest tests/unit/memory/web/test_server.py tests/unit/memory/surfaces/test_workspace.py
uv run ruff check src/memory/services src/memory/web src/memory/surfaces tests/unit/memory/web/test_server.py tests/unit/memory/surfaces/test_workspace.py
uv run ruff format --check src/memory/services src/memory/web src/memory/surfaces tests/unit/memory/web/test_server.py tests/unit/memory/surfaces/test_workspace.py
node --check src/memory/web/static/app.js
git diff --check
```

## Manual browser validation

1. Open Workspace and select a journey with conversations.
2. Open a conversation transcript from its card.
3. Edit the title manually and save.
4. Confirm the transcript title updates.
5. Reload the transcript and confirm the title persists.
6. Return to Workspace and confirm the conversation card title updates.
7. Confirm no generated-title/LLM action appears.
8. Confirm message content remains read-only.
