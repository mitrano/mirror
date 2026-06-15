"""Navigator flow-unit helpers for Ariad Builder delivery."""

from __future__ import annotations

from dataclasses import dataclass

from memory.builder.delivery_cursor import (
    BuilderDeliveryCursor,
    get_delivery_cursor,
    set_delivery_cursor,
)
from memory.builder.surface_protocol import wrap_ariad_surface
from memory.storage.store import Store

FLOW_UNIT_STORY_BY_STORY = "story_by_story"
FLOW_UNIT_DELIVERY_STORY = "delivery_story"
ALLOWED_FLOW_UNITS = (FLOW_UNIT_STORY_BY_STORY, FLOW_UNIT_DELIVERY_STORY)


@dataclass(frozen=True)
class NavigatorFlowUnitReport:
    journey: str
    method: str
    active_item: str | None
    active_item_title: str | None
    active_item_level: str | None
    flow_unit: str
    source: str
    cursor: BuilderDeliveryCursor


def effective_navigator_flow_unit(cursor: BuilderDeliveryCursor) -> tuple[str, str]:
    """Return the effective Navigator flow unit and its source."""
    if cursor.navigator_flow_unit in ALLOWED_FLOW_UNITS:
        return cursor.navigator_flow_unit, "cursor"
    return FLOW_UNIT_STORY_BY_STORY, "default"


def set_navigator_flow_unit(
    store: Store,
    *,
    journey: str,
    method: str,
    flow_unit: str,
) -> NavigatorFlowUnitReport:
    """Persist the Navigator-facing flow unit for active Builder delivery."""
    if flow_unit not in ALLOWED_FLOW_UNITS:
        allowed = ", ".join(ALLOWED_FLOW_UNITS)
        raise ValueError(f"navigator flow unit must be one of: {allowed}")
    existing = get_delivery_cursor(store, journey)
    if existing is None:
        raise ValueError("delivery cursor is required before choosing navigator flow unit")
    updated = set_delivery_cursor(
        store,
        journey=journey,
        method=method,
        active_item=existing.active_item,
        active_item_title=existing.active_item_title,
        active_item_level=existing.active_item_level,
        active_checkpoint=existing.active_checkpoint,
        pending_confirmation=existing.pending_confirmation,
        last_delivery_event="navigator_flow_unit_selected",
        cadence_profile=existing.cadence_profile,
        cadence_limits=existing.cadence_limits,
        granularity_decision=existing.granularity_decision,
        navigator_flow_unit=flow_unit,
    )
    return NavigatorFlowUnitReport(
        journey=journey,
        method=method,
        active_item=updated.active_item,
        active_item_title=updated.active_item_title,
        active_item_level=updated.active_item_level,
        flow_unit=flow_unit,
        source="cursor",
        cursor=updated,
    )


def inspect_navigator_flow_unit(
    store: Store,
    *,
    journey: str,
    method: str,
) -> NavigatorFlowUnitReport:
    """Inspect the effective Navigator flow unit for active Builder delivery."""
    cursor = get_delivery_cursor(store, journey)
    if cursor is None:
        raise ValueError("delivery cursor is required before inspecting navigator flow unit")
    flow_unit, source = effective_navigator_flow_unit(cursor)
    return NavigatorFlowUnitReport(
        journey=journey,
        method=method,
        active_item=cursor.active_item,
        active_item_title=cursor.active_item_title,
        active_item_level=cursor.active_item_level,
        flow_unit=flow_unit,
        source=source,
        cursor=cursor,
    )


def render_navigator_flow_unit_report(report: NavigatorFlowUnitReport) -> str:
    """Render a deterministic Ariad surface for the Navigator flow-unit decision."""
    body = "\n".join(
        [
            "■ Navigator Flow Unit",
            "",
            "journey",
            report.journey,
            "",
            "method",
            report.method,
            "",
            "active item",
            report.active_item or "none",
            "",
            "active item title",
            report.active_item_title or "none",
            "",
            "active item level",
            report.active_item_level or "none",
            "",
            "effective flow unit",
            report.flow_unit,
            "",
            "source",
            report.source,
            "",
            "available choices",
            "- story_by_story: child User/Technical Stories remain Navigator-facing lifecycle units",
            "- delivery_story: parent Delivery Story becomes the Navigator-facing lifecycle unit while child stories remain traceable Driver work packages",
            "",
            "default",
            "story_by_story preserves current Ariad Builder behavior when no choice is recorded.",
            "",
            "boundary",
            "No Plan, implementation, validation, push, or release work was executed.",
        ]
    )
    return wrap_ariad_surface("navigator_flow_unit", body + "\n")
