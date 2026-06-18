# Validation — CV20.DS6.US1

## Status

Blocked

## Automated Checks

- uv run pytest tests/unit/memory/builder/test_pull_candidates.py tests/unit/memory/cli/test_build.py -q
- uv run ruff check src/memory/builder src/memory/cli/build.py tests/unit/memory/builder tests/unit/memory/cli/test_build.py
- uv run ruff format --check src/memory/builder src/memory/cli/build.py tests/unit/memory/builder tests/unit/memory/cli/test_build.py
- uv run mypy src/memory/builder src/memory/cli/build.py
- git diff --check

Checks status: passed

## E2E

Decision: required

Evidence: Manual Navigator validation route prepared; awaiting Navigator acceptance. Navigator feedback found two issues: the next refinement move truncated `Model` to `Mode`, and field labels needed icons. Both were corrected. Driver smoke verified `uv run python -m memory build load sandbox-pet-store` renders `🟪 Delivery field`, `🧰 Refinement field`, and wraps `next refinement move: implement Workbench Storage Model before durable RS/CR work` without truncation.

## Navigator Validation

Route: Run: uv run python -m memory build load <ariad journey with no active item>. Expected: BUILDER_HOME, ROADMAP_SNAPSHOT, and PULL_CANDIDATES surfaces render in order; Builder Home shows Delivery field, Refinement field, workbench storage not implemented yet, seed CR count when present, and no lifecycle work is executed.

Navigator accepted: no

Expected observation: Builder activation orients around Builder Home work fields with Delivery and Refinement visible.

Pass condition: Navigator can see current Delivery field and nascent Refinement field from activation without confusing orientation with execution.

Fail condition: Activation remains Delivery-only, hides Refinement, shows irrelevant roadmap focus, or implies Workbench/RS/CR behavior already exists.

## Missing Evidence

- Navigator validation has not been accepted
