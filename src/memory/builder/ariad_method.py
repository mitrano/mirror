"""Built-in Ariad method definition for Builder Mode."""

from __future__ import annotations

from memory.builder.method_definition import (
    CheckpointDefinition,
    DslResolution,
    LifecycleEvent,
    MethodDefinition,
    SurfaceDefinition,
    Taxonomy,
    TaxonomyLevel,
    TemplateDefinition,
)

_STATE_VOCABULARY = (
    "Planned",
    "Active",
    "Blocked",
    "Validated",
    "Done",
    "Deferred",
    "Dropped",
)

_ARIAD_TEMPLATES = (
    TemplateDefinition(
        id="ariad_adoption",
        path="docs/project/roadmap/ariad-adoption.md",
        description="Records Ariad adoption readiness for this project.",
        content="""# Ariad Adoption

This project is prepared for Ariad-governed Builder Mode.

## Method

- adopted method: ariad
- adoption prepares documentation templates only
- delivery cursor sync is handled by a later Builder story

## Boundaries

Template preparation does not execute story lifecycle work, change story status,
commit, push, or release.
""",
    ),
    TemplateDefinition(
        id="technical_debt_ledger",
        path="docs/project/roadmap/technical-debt-ledger.md",
        description="Versioned debt ledger used by Ariad Review and Refactor.",
        content="""# Technical Debt Ledger

Ariad Review records technical debt here when debt should be paid now or deferred.

| ID | Source Story | Location | Kind | Description | Impact | Recommendation | Navigator Decision | Status |
|----|--------------|----------|------|-------------|--------|----------------|--------------------|--------|

## Deferred Debt Requirements

When debt is deferred, record the defer reason and revisit trigger.
""",
    ),
    TemplateDefinition(
        id="delivery_story_index",
        path="docs/project/roadmap/templates/delivery-story-index.md",
        description="Template for an Ariad Delivery Story index.",
        content="""[< Parent](../index.md)

# <CODE> — <Delivery Story Title>

**Status:** 🟡 Planned

---

## Outcome

<Coherent delivery outcome this story creates.>

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|

## Done Condition

<Condition that closes this delivery story.>
""",
    ),
    TemplateDefinition(
        id="user_story_index",
        path="docs/project/roadmap/templates/user-story-index.md",
        description="Template for an Ariad User Story index.",
        content="""[< Parent](../index.md)

# <CODE> — <User Story Title>

**Status:** 🟡 Planned
**Type:** User Story

---

## Outcome

<Navigator-visible behavior or capability.>

## Acceptance Behavior

```text
Given <context>
When <action>
Then <observable result>
```

## Scope

- <in scope>

## Out Of Scope

- <out of scope>

## Validation

<Navigator-facing validation route.>
""",
    ),
    TemplateDefinition(
        id="technical_story_index",
        path="docs/project/roadmap/templates/technical-story-index.md",
        description="Template for an Ariad Technical Story index.",
        content="""[< Parent](../index.md)

# <CODE> — <Technical Story Title>

**Status:** 🟡 Planned
**Type:** Technical Story

---

## Outcome

<Internal capability or substrate.>

## Acceptance Behavior

```text
Given <technical context>
When <operation runs>
Then <internal behavior or invariant holds>
```

## Scope

- <in scope>

## Out Of Scope

- <out of scope>

## Validation

<Automated or internal validation route.>
""",
    ),
    TemplateDefinition(
        id="plan",
        path="docs/project/roadmap/templates/plan.md",
        description="Template for the Ariad Plan checkpoint artifact.",
        content="""[< Story](index.md)

# Plan — <CODE> <Title>

## Pull

<Pulled item and why this level now.>

## Prepare

<Context summary, story shape, risks, and applicable rules.>

## Scope

- <in scope>

## Non-Goals

- <out of scope>

## Implementation Approach

<How implementation will proceed.>

## Test Strategy

<Automated and manual tests.>

## Validation Route

<How the Navigator validates observable behavior, when applicable.>

## Checkpoint

Implementation must not start until the Navigator approves this plan.
""",
    ),
    TemplateDefinition(
        id="test_guide",
        path="docs/project/roadmap/templates/test-guide.md",
        description="Template for Ariad validation evidence and Navigator validation.",
        content="""[< Story](index.md)

# Test Guide — <CODE> <Title>

## Automated Validation

```bash
<commands>
```

## Navigator Validation

<Manual validation route, expected observation, pass condition, and fail condition.>

## Validation Evidence

<Recorded evidence after validation runs.>
""",
    ),
    TemplateDefinition(
        id="review",
        path="docs/project/roadmap/templates/review.md",
        description="Template for Ariad Review debt scan.",
        content="""[< Story](index.md)

# Review — <CODE> <Title>

## Changed Surface

<Files, modules, docs, and behaviors changed.>

## Debt Scan

<Design, test, documentation, duplication, complexity, naming, coupling, or migration debt.>

## Recommendation

<No action, defer, or pay now.>

## Navigator Decision

<Decision and rationale.>
""",
    ),
    TemplateDefinition(
        id="coherence",
        path="docs/project/roadmap/templates/coherence.md",
        description="Template for Ariad Coherence integration check.",
        content="""[< Story](index.md)

# Coherence — <CODE> <Title>

## Process

<Lifecycle and checkpoint alignment.>

## Project

<Roadmap, docs, and runtime state alignment.>

## Product

<Behavior and product boundary alignment.>

## Result

<Coherent or incoherent, with next action.>
""",
    ),
)

ARIAD_METHOD = MethodDefinition(
    id="ariad",
    label="Ariad",
    resolution=DslResolution(
        layers=(
            "method_default",
            "project_config",
            "journey_config",
            "navigator_override",
        ),
        conflict_policy="explicit_override",
        audit=True,
    ),
    taxonomy=Taxonomy(
        state_vocabulary=_STATE_VOCABULARY,
        levels=(
            TaxonomyLevel(
                id="cv",
                label="Capability Value",
                contains=("delivery_story",),
                allowed_states=(
                    "Planned",
                    "Active",
                    "Blocked",
                    "Done",
                    "Deferred",
                    "Dropped",
                ),
                state_semantics={
                    "Done": "the project reached the value boundary named by this CV",
                },
            ),
            TaxonomyLevel(
                id="delivery_story",
                label="Delivery Story",
                contains=("user_story", "technical_story"),
                allowed_states=_STATE_VOCABULARY,
                state_semantics={
                    "Validated": (
                        "child stories passed their relevant validation, but delivery story "
                        "closure may still be pending"
                    ),
                    "Done": (
                        "child stories produced a coherent delivery outcome and the project "
                        "history reflects that outcome"
                    ),
                },
            ),
            TaxonomyLevel(
                id="user_story",
                label="User Story",
                contains=("task",),
                allowed_states=_STATE_VOCABULARY,
                state_semantics={
                    "Validated": (
                        "observable behavior or capability passed automated evidence and "
                        "Navigator-facing validation"
                    ),
                    "Done": (
                        "validated behavior is coherent, reviewed, recorded, and absorbed "
                        "into its parent delivery arc"
                    ),
                },
            ),
            TaxonomyLevel(
                id="technical_story",
                label="Technical Story",
                contains=("task",),
                allowed_states=_STATE_VOCABULARY,
                state_semantics={
                    "Validated": (
                        "internal capability passed automated or internal evidence sufficient "
                        "for the delivery story"
                    ),
                    "Done": (
                        "technical substrate is coherent, reviewed, recorded, and ready for "
                        "its parent delivery arc"
                    ),
                },
            ),
            TaxonomyLevel(
                id="task",
                label="Task",
                allowed_states=("Planned", "Active", "Blocked", "Done"),
                state_semantics={
                    "Done": "concrete local work is complete inside its parent story",
                },
            ),
        ),
    ),
    lifecycle=(
        LifecycleEvent(id="pull", meaning="escolhe o foco"),
        LifecycleEvent(id="prepare", meaning="lê o terreno"),
        LifecycleEvent(id="plan", meaning="firma o contrato"),
        LifecycleEvent(id="implement", meaning="muda o sistema"),
        LifecycleEvent(id="validation", meaning="prova comportamento"),
        LifecycleEvent(id="review", meaning="encara a dívida"),
        LifecycleEvent(id="coherence", meaning="integra os rastros"),
        LifecycleEvent(id="done", meaning="registra e fecha"),
    ),
    checkpoints=(
        CheckpointDefinition(
            id="after_plan",
            occurs_after="plan",
            blocks=("implement",),
            required_artifacts=("plan",),
            required_confirmations=("navigator_approval",),
        ),
        CheckpointDefinition(
            id="navigator_validation",
            occurs_after="validation",
            blocks=("done",),
            required_artifacts=("validation_route", "validation_evidence"),
            required_confirmations=("navigator_validation",),
        ),
        CheckpointDefinition(
            id="review_decision",
            occurs_after="review",
            blocks=("coherence",),
            required_artifacts=("review_report",),
            required_confirmations=("navigator_debt_decision",),
        ),
    ),
    policies={
        "history": {
            "commit": {
                "mode": "propose_and_wait",
                "granularity": "coherent_story",
                "message_style": "descriptive_why",
            },
            "worklog": {"mode": "meaningful_milestones"},
            "decision_records": {"mode": "when_architectural_or_process_decision_changes"},
        },
        "push": {
            "mode": "ask_before_push",
            "allowed_after": ["story_done", "release_publish", "manual_request"],
            "requires": [
                "clean_worktree",
                "commits_present",
                "remote_configured",
                "navigator_confirmation",
            ],
        },
        "release": {"modes": ["planned_release", "emergent_release"]},
    },
    templates=_ARIAD_TEMPLATES,
    surfaces=(
        SurfaceDefinition(id="adoption_report", event="adoption"),
        SurfaceDefinition(id="builder_resume", event="on_builder_load"),
        SurfaceDefinition(id="pull_report", event="pull"),
        SurfaceDefinition(id="prepare_report", event="prepare"),
        SurfaceDefinition(
            id="plan_checkpoint",
            event="plan",
            stops_for="navigator_approval",
        ),
        SurfaceDefinition(
            id="validation_checkpoint",
            event="validation",
            stops_for="navigator_validation",
        ),
        SurfaceDefinition(
            id="review_checkpoint",
            event="review",
            stops_for="navigator_debt_decision",
        ),
        SurfaceDefinition(id="coherence_report", event="coherence"),
        SurfaceDefinition(id="done_report", event="done"),
    ),
    open_questions={
        "maintenance_and_operational_updates": {
            "status": "open",
            "note": "Do not overdesign upfront. Model when real cases appear.",
        },
        "final_surface_content": {
            "status": "open",
            "note": "Use Ariad visual grammar during implementation.",
        },
        "final_dsl_file_format": {
            "status": "open",
            "note": "YAML is the exploration notation, not yet a committed parser format.",
        },
    },
)


def get_ariad_method() -> MethodDefinition:
    """Return the built-in Ariad Builder method definition."""
    return ARIAD_METHOD
