[< Story](index.md)

# Test Guide — CV13.E3.S5 Configuration coherence and validation

## Automated checks

```bash
uv run pytest tests/unit/memory/surfaces/test_workspace.py tests/unit/memory/web/test_configuration.py tests/unit/memory/web/test_server.py
uv run ruff check src/memory/services src/memory/surfaces src/memory/web tests/unit/memory/surfaces/test_workspace.py tests/unit/memory/web/test_configuration.py tests/unit/memory/web/test_server.py
uv run ruff format --check src/memory/services src/memory/surfaces src/memory/web tests/unit/memory/surfaces/test_workspace.py tests/unit/memory/web/test_configuration.py tests/unit/memory/web/test_server.py
node --check src/memory/web/static/app.js
git diff --check
```

## Manual browser validation

1. Open Configuration and confirm it only contains Mirror/runtime sections.
2. Confirm Environment masks secrets and has no edit controls.
3. Open Workspace, select a journey, and open Settings.
4. Confirm journey settings are shown there, not duplicated in Configuration.
5. Edit project path, sync file, icon, and color.
6. Save, reload, and confirm persistence.
7. Confirm there is no raw `.env`, JSON, YAML, database, or journey content editor.
