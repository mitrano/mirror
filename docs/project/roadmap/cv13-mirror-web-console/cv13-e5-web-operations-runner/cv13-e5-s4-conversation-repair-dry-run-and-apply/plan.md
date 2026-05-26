[< Story](index.md)

# Plan — CV13.E5.S4 Conversation repair dry-run and apply

## Implementation plan

1. Add a `dryRun` boolean parameter to the `conversation-journey-repair` catalog entry and mark the operation runnable.
2. Extend operation parameter validation to support the new boolean alongside the existing `limit` integer.
3. Run dry-run by calling `diagnose_journey_associations(apply=False)` against the selected Mirror home.
4. Run apply by calling `diagnose_journey_associations(apply=True)` against the selected Mirror home.
5. Return structured results with candidates and applied count.
6. Include backup evidence when apply mode creates a backup. If existing repair logic does not expose the backup path, refactor it minimally to return or support callback evidence without changing CLI behavior.
7. Add tests for dry-run no mutation, apply mutation with backup, limit validation, unsafe parameter rejection, and endpoint behavior.
8. Preserve the rule that only high-confidence inferred journey associations are repaired.

## Design boundaries

- The operation repairs only conversations where the existing inference logic identifies a clear journey.
- Dry-run is the default and should never write.
- Apply must create a backup first and fail if backup fails.
- The request cannot provide a target journey, SQL clause, conversation ids, or arbitrary reassignment map.
- The response can expose conversation ids and titles because this is a local operator surface for the user's own Mirror.
- This story is API-only unless implementation reveals a small visible surface is necessary.

## Result shape

Dry-run response:

- `operationId: conversation-journey-repair`,
- `status: completed`,
- `outcome: dry_run`,
- `result.candidateCount`,
- `result.appliedCount: 0`,
- `result.candidates`.

Apply response:

- `operationId: conversation-journey-repair`,
- `status: completed`,
- `outcome: repaired`,
- `result.candidateCount`,
- `result.appliedCount`,
- `result.backupPath`,
- `result.candidates`.

## Risks and mitigations

- Risk: wrong journey association. Mitigation: reuse existing high-confidence inference only and keep dry-run default.
- Risk: hidden write operation surprises the user. Mitigation: require explicit `dryRun: false` to apply and include backup evidence.
- Risk: repair becomes a generic reassignment tool. Mitigation: no target journey or conversation id parameters in this story.

## Verification approach

- Unit tests build a temporary Mirror database with journeys, a journeyless conversation, and messages matching a journey alias.
- Tests verify dry-run does not mutate and apply does mutate.
- Endpoint tests verify unsafe parameters and future operations remain rejected.
- Manual validation is not required unless a visible surface is introduced.
