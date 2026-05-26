[< Story](index.md)

# Test Guide — CV13.E5.S4 Conversation repair dry-run and apply

## Automated checks

```bash
uv run pytest tests/unit/memory/web/test_operations.py tests/unit/memory/web/test_server.py
uv run ruff check src/memory/cli/runtime.py src/memory/web tests/unit/memory/web/test_operations.py tests/unit/memory/web/test_server.py
uv run ruff format --check src/memory/cli/runtime.py src/memory/web tests/unit/memory/web/test_operations.py tests/unit/memory/web/test_server.py
node --check src/memory/web/static/app.js
git diff --check
```

## Manual validation

Manual validation is optional for this API-only story unless a visible web surface is introduced.

If manual validation is desired:

1. Start the local web server against a disposable Mirror home with journeyless conversations and known journey aliases.
2. Confirm `conversation-journey-repair` is marked runnable:

   ```bash
   curl http://127.0.0.1:8765/api/operations/catalog | python -m json.tool
   ```

3. Run dry-run:

   ```bash
   curl -X POST http://127.0.0.1:8765/api/operations/run \
     -H 'Content-Type: application/json' \
     -d '{"operationId":"conversation-journey-repair","parameters":{"dryRun":true,"limit":50}}' | python -m json.tool
   ```

4. Confirm candidates are returned and no conversation journey is updated.
5. Run apply only after reviewing candidates:

   ```bash
   curl -X POST http://127.0.0.1:8765/api/operations/run \
     -H 'Content-Type: application/json' \
     -d '{"operationId":"conversation-journey-repair","parameters":{"dryRun":false,"limit":50}}' | python -m json.tool
   ```

6. Confirm candidates were applied, a backup path is returned, and the affected conversations now have journey associations.
7. Confirm unsupported parameters are rejected.

## Expected result

The web API can preview and apply only high-confidence journey association repairs, with dry-run by default and backup before mutation.
