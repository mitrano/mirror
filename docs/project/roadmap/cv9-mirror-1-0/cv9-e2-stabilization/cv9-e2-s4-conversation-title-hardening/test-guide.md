[< Story](index.md)

# Test Guide — CV9.E2.S4 Conversation Title Hardening

## Automated validation

```bash
uv run pytest tests/unit/memory/services/test_conversation.py tests/unit/memory/web/test_operations.py tests/unit/memory/web/test_server.py
```

Expected result: all selected tests pass.

## Manual validation route

Use a non-production or backed-up Mirror home.

1. Start the web server against the target Mirror.
2. Open Operations and run `batch-conversation-retitle` with `dryRun=true`.
3. Confirm the result shows candidate count, estimated tokens, estimated cost, and candidate reasons without changing database titles.
4. Create/confirm a backup.
5. Run a small apply batch.
6. Confirm changed conversations have concise titles and metadata provenance.
7. Confirm manually edited titles are not selected or overwritten.

## Production safety notes

- Do not run apply without reviewing dry-run output.
- Apply creates a backup before title generation/writes.
- Large legacy sets should be processed in bounded batches.
