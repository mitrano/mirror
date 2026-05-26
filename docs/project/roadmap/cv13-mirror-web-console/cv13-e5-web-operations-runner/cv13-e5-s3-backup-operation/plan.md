[< Story](index.md)

# Plan — CV13.E5.S3 Backup operation

## Implementation plan

1. Change `database-backup` from `execution: future` to `execution: runnable`.
2. Extend the operation dispatcher to accept operation-specific parameters through a validated `parameters` object.
3. Keep `runtime-health` parameterless and reject parameters for it.
4. Implement `database-backup` by calling `memory.cli.backup.backup()` directly with the selected `mirror_home`.
5. Verify the created archive when `verify` is true by reusing `verify_backup_archive()` from runtime inspection.
6. Return structured evidence: operation id, completed status, backup path, entries, verification validity, note, and manual recovery route text.
7. Return a request failure when the selected Mirror database does not exist.
8. Add tests that create a temporary Mirror database, run the backup operation, verify the archive, and prove arbitrary paths or command-like fields remain rejected.

## Design boundaries

- The operation may write only to the selected Mirror home's backup directory or the already configured backup directory respected by existing backup behavior.
- The request must not accept `backupPath`, `destination`, `path`, shell command, raw SQL, or executable fields.
- The response may expose local filesystem paths because this is a local-first operator surface, but it must not expose secrets or environment values.
- Verification is structural archive verification, not restore.
- Missing database is a failed operation request, not an implicit database creation.

## Result shape

A successful response should include:

- `operationId: database-backup`,
- `status: completed`,
- `outcome: backup_created`,
- `summary`,
- `result.backupPath`,
- `result.verification.valid`,
- `result.verification.entries`,
- `result.recoveryRoute`.

## Risks and mitigations

- Risk: backup operation becomes arbitrary file write. Mitigation: no destination parameter and reuse selected Mirror-home backup defaults.
- Risk: users confuse backup creation with restore/recovery. Mitigation: response includes manual recovery route and no restore endpoint.
- Risk: operation parameters become too permissive. Mitigation: validate allowed parameters per operation and reject extra request fields.

## Verification approach

- Unit tests cover successful backup creation and archive verification.
- Endpoint tests cover runnable backup, missing database rejection, and unsafe field rejection.
- Existing runtime-health tests remain green.
- Manual validation is not required unless a user-facing surface is introduced.
