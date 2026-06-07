"""In-session Explorer Mode story state.

The Explorer Story is intentionally stored in runtime state for the first
behavior slice. It is a live conversational field, not durable Explorer archive.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from memory.storage.store import Store

EXPLORER_STORY_SESSION_PREFIX = "__explorer_story__:"
_UNSET = object()


@dataclass(frozen=True)
class ExplorerStory:
    journey: str
    current_exploratory_story: str | None = None
    narrative_field_summary: str | None = None
    last_story_card: str | None = None


def _session_id(journey: str) -> str:
    normalized = journey.strip()
    if not normalized:
        raise ValueError("journey must not be empty")
    return f"{EXPLORER_STORY_SESSION_PREFIX}{normalized}"


def _clean(value: str | None | object) -> str | None | object:
    if value is _UNSET:
        return _UNSET
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def get_explorer_story(store: Store, journey: str) -> ExplorerStory | None:
    """Return the current in-session Explorer Story for a journey."""
    normalized_journey = journey.strip()
    if not normalized_journey:
        raise ValueError("journey must not be empty")
    session = store.get_runtime_session(_session_id(normalized_journey))
    if not session or not session.active or not session.metadata:
        return None
    try:
        data = json.loads(session.metadata)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None

    return ExplorerStory(
        journey=normalized_journey,
        current_exploratory_story=_string_or_none(data.get("current_exploratory_story")),
        narrative_field_summary=_string_or_none(data.get("narrative_field_summary")),
        last_story_card=_string_or_none(data.get("last_story_card")),
    )


def update_explorer_story(
    store: Store,
    journey: str,
    *,
    current_exploratory_story: str | None | object = _UNSET,
    narrative_field_summary: str | None | object = _UNSET,
    last_story_card: str | None | object = _UNSET,
) -> ExplorerStory:
    """Create or update the in-session Explorer Story for a journey.

    Omitted fields preserve existing values. Explicit empty strings or None clear
    the corresponding scalar.
    """
    normalized_journey = journey.strip()
    if not normalized_journey:
        raise ValueError("journey must not be empty")
    existing = get_explorer_story(store, normalized_journey)

    story_value = _clean(current_exploratory_story)
    summary_value = _clean(narrative_field_summary)
    last_card_value = _clean(last_story_card)

    updated = ExplorerStory(
        journey=normalized_journey,
        current_exploratory_story=(
            existing.current_exploratory_story
            if story_value is _UNSET and existing
            else (None if story_value is _UNSET else story_value)
        ),
        narrative_field_summary=(
            existing.narrative_field_summary
            if summary_value is _UNSET and existing
            else (None if summary_value is _UNSET else summary_value)
        ),
        last_story_card=(
            existing.last_story_card
            if last_card_value is _UNSET and existing
            else (None if last_card_value is _UNSET else last_card_value)
        ),
    )

    store.upsert_runtime_session(
        _session_id(normalized_journey),
        interface="explorer_story",
        journey=normalized_journey,
        active=True,
        metadata=json.dumps(
            {
                "current_exploratory_story": updated.current_exploratory_story,
                "narrative_field_summary": updated.narrative_field_summary,
                "last_story_card": updated.last_story_card,
            },
            ensure_ascii=False,
        ),
    )
    return updated


def clear_explorer_story(store: Store, journey: str) -> None:
    """Clear the current in-session Explorer Story for a journey."""
    normalized_journey = journey.strip()
    if not normalized_journey:
        raise ValueError("journey must not be empty")
    store.upsert_runtime_session(
        _session_id(normalized_journey),
        interface="explorer_story",
        journey=normalized_journey,
        active=False,
        metadata=None,
    )


def render_explorer_story_context(story: ExplorerStory) -> str:
    """Render Explorer Story context for prompt injection or CLI inspection."""
    lines = ["=== △ Exploratory Story ===", f"journey: {story.journey}"]
    if story.current_exploratory_story:
        lines.extend(["", "current exploratory story:", story.current_exploratory_story])
    if story.narrative_field_summary:
        lines.extend(["", "narrative field summary:", story.narrative_field_summary])
    if story.last_story_card:
        lines.extend(["", "last story card:", story.last_story_card])
    return "\n".join(lines)


def _string_or_none(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    return cleaned or None
