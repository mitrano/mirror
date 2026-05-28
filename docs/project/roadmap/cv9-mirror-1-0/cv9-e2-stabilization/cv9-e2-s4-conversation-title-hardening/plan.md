[< Story](index.md)

# Plan — CV9.E2.S4 Conversation Title Hardening

## Problem

Runtime logging currently seeds a conversation title from the first user message and then leaves it unchanged. In real sessions, that first message may be a skill payload, command wrapper, long setup text, or a partial user request. The web app already supports one-off title suggestions, but legacy correction and automatic prevention are not wired into the core lifecycle.

## Design

1. **Title provenance metadata**
   - Runtime first-message titles become `title_status=provisional` and `title_source=first_user`.
   - Manual edits become `title_status=manual` and `title_source=manual`.
   - Automatic generation becomes `title_status=generated` and `title_source=llm_auto`.
   - Batch legacy generation becomes `title_status=generated` and `title_source=batch_retitle`.

2. **Core lifecycle hardening**
   - `ConversationService.end_conversation()` attempts title improvement before extraction returns.
   - It only runs when a conversation has enough content to title: at least one user and one assistant message.
   - It only updates titles that are blank, provisional, truncated with ellipsis, skill-like, or unusually long.
   - LLM failure is fail-quiet and does not block session close or extraction.
   - Manual titles are never overwritten.

3. **Batch web operation**
   - `batch-conversation-retitle` becomes runnable and accepts `dryRun`, `limit`, and optional `journey`.
   - Dry-run does not call the LLM. It returns candidates, reasons, estimated tokens, estimated cost, and current titles.
   - Apply creates a backup before LLM calls/database writes.
   - Apply processes only bounded candidates and records previous title/provenance in metadata.

## Trade-offs

- The cost estimate uses a conservative character-to-token approximation instead of tokenizer-specific accounting. This keeps dry-run offline and fast.
- The candidate heuristic is intentionally simple and explainable rather than ML-based.
- Apply remains bounded by the operation parameter maximum; large legacy repair can run in batches.

## Verification

- Unit tests for title lifecycle and metadata preservation.
- Web operation tests for catalog state, dry-run, apply, backup creation, and no manual overwrite.
- Existing web/server single-conversation title tests must continue to pass.
