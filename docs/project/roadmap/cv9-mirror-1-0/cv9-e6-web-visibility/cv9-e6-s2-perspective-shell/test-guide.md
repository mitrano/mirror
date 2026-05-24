[< Story](index.md)

# Test Guide — CV9.E6.S2 Perspective Shell and Preference

## Automated validation

Run focused web and surface tests:

```bash
uv run pytest tests/unit/memory/web tests/unit/memory/surfaces tests/unit/memory/test_public_api.py
```

Run lint and format checks for changed web code:

```bash
uv run --extra dev ruff check src/memory/web tests/unit/memory/web
uv run --extra dev ruff format --check src/memory/web tests/unit/memory/web
```

If static assets are changed, run the browser smoke route below.

## Expected automated result

- Preference persistence tests pass.
- Server API tests pass for shell state and perspective updates.
- Existing docs browser tests still pass.
- Surface tests still pass.
- Ruff reports no lint or formatting issues for changed Python files.

## Manual validation route

Start the local web server with an isolated or personal Mirror home:

```bash
uv run python -m memory web --port 8765
```

Open:

```text
http://127.0.0.1:8765
```

First-run validation when no default exists:

- remove or move `<mirror-home>/web/preferences.json` before starting;
- page shows a perspective choice instead of silently defaulting only in browser
  state;
- choose Atlas;
- refresh page;
- Atlas remains the default because the user-home preference was written.

Switcher validation:

- active perspective is visible;
- switch to Workspace;
- Workspace content renders from `/api/surface/workspace`;
- switch back to Atlas;
- Atlas content renders from `/api/surface/atlas`;
- Docs remains accessible and existing docs navigation still works.

Preference file validation:

```bash
cat <mirror-home>/web/preferences.json
```

Expected:

```json
{"default_perspective": "atlas"}
```

or `workspace` depending on the selected default.

Fallback validation:

- corrupt the preferences file with invalid JSON;
- reload the page;
- the server returns a warning state instead of crashing;
- the UI lets the user choose a perspective again.

## Known exclusions

- Full Atlas map design.
- Full Workspace dashboard design.
- Functional global search.
- Object detail and evidence routing.
- Remote/multi-user support.
