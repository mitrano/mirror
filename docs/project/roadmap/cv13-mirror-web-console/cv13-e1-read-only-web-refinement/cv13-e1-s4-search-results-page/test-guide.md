[< Story](index.md)

# Test Guide — CV13.E1.S4 Search results page

## Automated validation

Run:

```bash
uv run pytest tests/unit/memory/surfaces/test_search.py tests/unit/memory/web/test_server.py
uv run ruff check src/memory/surfaces src/memory/web tests/unit/memory/surfaces/test_search.py tests/unit/memory/web/test_server.py
uv run ruff format --check src/memory/surfaces src/memory/web tests/unit/memory/surfaces/test_search.py tests/unit/memory/web/test_server.py
node --check src/memory/web/static/app.js
git diff --check
```

Expected result: all commands pass.

## Manual browser validation

Start the web app:

```bash
uv run python -m memory web
```

Use the search input in the header.

Expected observations:

- submitting a query opens a search results page;
- matching memory cards appear when retained memories match the query;
- an honest empty state appears when nothing matches;
- browser Back returns to the previous perspective/page.
