[< CV13.E5](../index.md)

# CV13.E5.S3 — Backup operation

**Status:** ✅ Done
**Epic:** CV13.E5 — Web Operations Runner
**Release target:** v0.15.0

---

## User-visible outcome

The web operations API can create a local backup archive for the selected Mirror database and return verifiable evidence about the created archive.

---

## Scope

- Mark the `database-backup` catalog entry as runnable.
- Implement `database-backup` through the existing backup service path, not shell commands.
- Require an existing active Mirror database before creating a backup.
- Support the existing `verify` parameter.
- Return backup path, archive entries, verification result, and recovery note text suitable for future UI display.
- Reject unsupported parameters and future operations.

---

## Non-goals

- No restore operation.
- No backup download endpoint.
- No deleting backups.
- No streaming or job history.
- No runtime update execution.
- No generic filesystem picker or arbitrary backup path input.
- No operation UI surface yet.

---

## Validation

See [test guide](test-guide.md).
