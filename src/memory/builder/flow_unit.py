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
        child_work_items=existing.child_work_items,
        aggregate_checkpoint_status=existing.aggregate_checkpoint_status,
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


def render_flow_unit_scope_confirmation_report(report: NavigatorFlowUnitReport) -> str:
    """Render the next shared-agreement surface after selecting a flow unit."""
    if report.flow_unit == FLOW_UNIT_DELIVERY_STORY:
        surface_name = "delivery_story_scope_confirmation"
        title = "       🧭  DELIVERY STORY SCOPE CONFIRMATION"
        understanding = _delivery_story_scope_hypothesis(report)
        scope_label = "Work packages in scope"
        scope_items = report.cursor.child_work_items
        prompt = "Before I create the DS Plan, correct or add anything:"
        questions = ("1. Is this the right scope?",)
    else:
        surface_name = "next_story_confirmation"
        title = "       🧭  NEXT STORY CONFIRMATION"
        understanding = (
            "We will continue story by story. The next step is to confirm which child story "
            "becomes the next Navigator-facing lifecycle unit."
        )
        scope_label = "Recommended story"
        scope_items = _recommended_story_items(report)
        prompt = "Before I create the Story Plan, correct or add anything:"
        questions = ("1. Is this the right next story?",)
    body = "\n".join(
        [
            "Delivery",
            "",
            "╭────────────────────────────────────────────────────────╮",
            _card_text(title),
            "│                                                        │",
            _card_text("My understanding"),
            *_card_wrapped(understanding),
            "│                                                        │",
            _card_text("Active delivery"),
            *_card_wrapped(_active_delivery(report)),
            *_scope_item_lines(scope_label, scope_items),
            "│                                                        │",
            *_card_wrapped(prompt),
            *[_line for question in questions for _line in _card_wrapped(question)],
            "│                                                        │",
            *_card_wrapped("Choose the next move when ready."),
            "╰────────────────────────────────────────────────────────╯",
        ]
    )
    return wrap_ariad_surface(surface_name, body + "\n")


def render_navigator_flow_unit_report(report: NavigatorFlowUnitReport) -> str:
    """Render a deterministic Ariad surface for the selected Navigator flow unit."""
    body = "\n".join(
        [
            "Delivery",
            "",
            "╭────────────────────────────────────────────────────────╮",
            "│        🧭  FLOW UNIT SELECTED                         │",
            "│                                                        │",
            _card_text("What changed?"),
            *_card_wrapped(_flow_unit_change_summary(report.flow_unit)),
            "│                                                        │",
            _card_text("Active delivery"),
            *_card_wrapped(_active_delivery(report)),
            "│                                                        │",
            _card_text("Selected flow unit"),
            _card_text(report.flow_unit),
            *_card_wrapped(_flow_unit_description(report.flow_unit)),
            "│                                                        │",
            _card_text("Next movement"),
            *_card_wrapped(_flow_unit_next_movement(report.flow_unit)),
            "│                                                        │",
            *_card_wrapped("Choose the next move when ready."),
            "╰────────────────────────────────────────────────────────╯",
        ]
    )
    return wrap_ariad_surface("navigator_flow_unit", body + "\n")


def _delivery_story_scope_hypothesis(report: NavigatorFlowUnitReport) -> str:
    title = (report.active_item_title or "").strip()
    normalized = title.lower()
    if "checkout" in normalized and "address" in normalized:
        return (
            "This Delivery Story should let the customer enter checkout, provide or confirm "
            "a delivery address, and leave the order ready for the next checkout step."
        )
    if title:
        return f"This Delivery Story should deliver the scope implied by: {title}."
    return (
        "I will infer a complete Delivery Story plan from the roadmap and project context; "
        "correct or add any scope details before I proceed."
    )


def _scope_item_lines(label: str, items: tuple[str, ...]) -> list[str]:
    if not items:
        return []
    return [
        "│                                                        │",
        _card_text(label),
        *_card_prefixed(items, "-"),
    ]


def _recommended_story_items(report: NavigatorFlowUnitReport) -> tuple[str, ...]:
    if report.cursor.child_work_items:
        return report.cursor.child_work_items[:1]
    return ()


def _flow_unit_change_summary(flow_unit: str) -> str:
    if flow_unit == FLOW_UNIT_DELIVERY_STORY:
        return "Navigator-facing lifecycle will continue at Delivery Story level."
    return "Navigator-facing lifecycle will continue story by story."


def _active_delivery(report: NavigatorFlowUnitReport) -> str:
    if report.active_item is None:
        return "none"
    title = f" — {report.active_item_title}" if report.active_item_title else ""
    return f"🟦[{report.active_item}]{title}"


def _flow_unit_description(flow_unit: str) -> str:
    if flow_unit == FLOW_UNIT_DELIVERY_STORY:
        return "the Delivery Story becomes the lifecycle unit; child stories remain traceable work packages"
    return "child stories get their own Navigator checkpoints"


def _flow_unit_next_movement(flow_unit: str) -> str:
    if flow_unit == FLOW_UNIT_DELIVERY_STORY:
        return "Plan the Delivery Story as the Navigator-facing unit."
    return "Confirm the recommended child story, then Plan."


def _card_text(text: str) -> str:
    width = 54
    return f"│ {text[:width]:<{width}} │"


def _card_prefixed(items: tuple[str, ...], prefix: str) -> list[str]:
    lines: list[str] = []
    for item in items:
        wrapped = _wrap_plain_text(item, width=52)
        for index, line in enumerate(wrapped):
            marker = prefix if index == 0 else " "
            lines.append(_card_text(f"{marker} {line}"))
    return lines or [_card_text("none")]


def _card_wrapped(text: str) -> list[str]:
    return [_card_text(line) for line in _wrap_plain_text(text, width=54)]


def _wrap_plain_text(text: str, *, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        if len(word) > width:
            if current:
                lines.append(current)
                current = ""
            for start in range(0, len(word), width):
                lines.append(word[start : start + width])
            continue
        candidate = f"{current} {word}".strip()
        if len(candidate) > width and current:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines or ["none"]
