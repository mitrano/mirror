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
