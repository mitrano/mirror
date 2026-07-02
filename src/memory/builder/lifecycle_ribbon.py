"""Ariad lifecycle ribbon rendering."""

from __future__ import annotations

DELIVERY_LIFECYCLE_STAGES = (
    "pull",
    "prepare",
    "expand",
    "plan",
    "implement",
    "validate",
    "debt_review",
    "done",
)

DELIVERY_STAGE_LABELS = {
    "pull": "Pull",
    "prepare": "Prepare",
    "expand": "Expand",
    "plan": "Plan",
    "implement": "Implement",
    "validate": "Validate",
    "debt_review": "Debt Review",
    "done": "Done",
}

REFINEMENT_STORY_STAGES = (
    "pull",
    "select_cr",
    "cr_cycle",
    "review",
    "coherence",
    "close",
)

REFINEMENT_STORY_STAGE_LABELS = {
    "pull": "Pull",
    "select_cr": "Select CR",
    "cr_cycle": "CR Cycle",
    "review": "Review",
    "coherence": "Coherence",
    "close": "Close",
}

CHANGE_REQUEST_STAGES = (
    "confirm",
    "plan",
    "implement",
    "validate",
    "done_note",
)

CHANGE_REQUEST_STAGE_LABELS = {
    "confirm": "Confirm",
    "plan": "Plan",
    "implement": "Implement",
    "validate": "Validate",
    "done_note": "Done Note",
}


def render_lifecycle_ribbon(current: str = "pull") -> str:
    """Render a compact progress breadcrumb for the Ariad Delivery lifecycle."""
    return _render_progress_ribbon(
        current=current,
        stages=DELIVERY_LIFECYCLE_STAGES,
        labels=DELIVERY_STAGE_LABELS,
        label="Delivery Flow",
        separator="→",
        unknown_kind="Ariad lifecycle stage",
    )


def render_refinement_lifecycle_ribbon(current: str = "pull") -> str:
    """Render the Ariad Refinement Story flow, not the Delivery lifecycle."""
    return _render_progress_ribbon(
        current=current,
        stages=REFINEMENT_STORY_STAGES,
        labels=REFINEMENT_STORY_STAGE_LABELS,
        label="RS Flow",
        separator="→",
        unknown_kind="Ariad Refinement Story stage",
    )


def render_change_request_lifecycle_ribbon(current: str = "confirm") -> str:
    """Render the Ariad Change Request cycle inside Refinement Work."""
    return _render_progress_ribbon(
        current=current,
        stages=CHANGE_REQUEST_STAGES,
        labels=CHANGE_REQUEST_STAGE_LABELS,
        label="CR Cycle",
        separator="→",
        unknown_kind="Ariad Change Request stage",
    )


def _render_progress_ribbon(
    *,
    current: str,
    stages: tuple[str, ...],
    labels: dict[str, str],
    label: str,
    separator: str,
    unknown_kind: str,
) -> str:
    if current not in stages:
        raise ValueError(f"unknown {unknown_kind}: {current}")
    current_index = stages.index(current)
    parts: list[str] = []
    for index, stage in enumerate(stages):
        if index < current_index:
            marker = "✓"
        elif index == current_index:
            marker = "◉"
        else:
            marker = "○"
        parts.append(f"{marker} {labels[stage]}")
    return f"{label}: " + f" {separator} ".join(parts)
