# Technical Debt Ledger

This ledger records structural cost the project is consciously carrying.

Do not record every imperfection. Record debt that may affect future delivery,
safety, maintainability, validation, operation, or product coherence.

## States

```text
Carried   known and accepted for now
Paying    currently being reduced by active work
Paid      resolved or reduced enough to close
Dropped   no longer relevant or replaced by another item
```

## Debt Items

| ID | Title | Kind | Severity | Status | Source | Revisit Trigger |
|----|-------|------|----------|--------|--------|-----------------|
| D-001 | Metadata lifecycle policy and evidence filtering live inside ConversationService | design | medium | Carried | CV9.DS7.US1 / CV9.DS7.TS1 | If debt grows further during DS7, especially before or during US2 apply behavior |

## D-001 — Metadata lifecycle policy and evidence filtering live inside ConversationService

**Kind:** design  
**Severity:** medium  
**Status:** Carried  
**Source:** CV9.DS7.US1 / CV9.DS7.TS1  

### Carrying reason

US1 needed an observable non-mutating dry-run, and TS1 added enough policy to
avoid brittle title decisions. Keeping the policy helpers in `ConversationService`
is acceptable while the behavior remains dry-run-only.

### Revisit trigger

If debt grows further during DS7, refactor. In particular, revisit before or
during CV9.DS7.US2 if apply/mutation behavior makes metadata lifecycle policy,
evidence filtering, or write boundaries harder to reason about.

### Closure condition

Policy and evidence filtering are either small enough to remain local, or they
are extracted into a clearer metadata lifecycle policy/service boundary before
mutation behavior is added.

### Notes

Current evidence terms are useful for candidate signaling but noisy. This is not
blocking while decisions remain non-mutating and candidate-based.
