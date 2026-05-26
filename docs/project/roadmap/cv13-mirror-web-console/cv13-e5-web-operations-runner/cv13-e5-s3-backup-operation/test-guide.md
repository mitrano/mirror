[< Story](index.md)

# Test Guide — CV13.E5.S3 Backup operation

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

1. Start the local web server against a disposable Mirror home with an existing `memory.db`.
2. Confirm `database-backup` is marked runnable:

   ```bash
   curl http://127.0.0.1:8765/api/operations/catalog | python -m json.tool
   ```

3. Run the backup operation:

   ```bash
   curl -X POST http://127.0.0.1:8765/api/operations/run \
     -H 'Content-Type: application/json' \
     -d '{"operationId":"database-backup","parameters":{"verify":true}}' | python -m json.tool
   ```

4. Confirm the response includes the backup path, verification result, archive entries, and manual recovery route.
5. Confirm the backup archive exists under the selected Mirror backup location.
6. Confirm unsupported fields are rejected:

   ```bash
   curl -X POST http://127.0.0.1:8765/api/operations/run \
     -H 'Content-Type: application/json' \
     -d '{"operationId":"database-backup","parameters":{"path":"/tmp/unsafe"}}' | python -m json.tool
   ```

## Expected result

The web API can create and verify a local backup for the selected Mirror database, without exposing restore, arbitrary destination paths, shell commands, or streaming.
