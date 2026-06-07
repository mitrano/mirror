"""Tests for in-session Explorer Story state."""

from memory import MemoryClient
from memory.config import default_db_path_for_home
from memory.services.explorer_story import (
    clear_explorer_story,
    get_explorer_story,
    render_explorer_story_context,
    update_explorer_story,
)


def _client(tmp_path):
    mirror_home = tmp_path / ".mirror" / "alisson-vale"
    return MemoryClient(db_path=default_db_path_for_home(mirror_home))


def test_update_creates_explorer_story_for_journey(tmp_path):
    mem = _client(tmp_path)

    story = update_explorer_story(
        mem.store,
        "explorer-mode",
        current_exploratory_story="Explorer is becoming observable.",
        narrative_field_summary="Runtime story state before persistence.",
        last_story_card="Story opened.",
    )

    assert story.journey == "explorer-mode"
    assert story.current_exploratory_story == "Explorer is becoming observable."
    assert story.narrative_field_summary == "Runtime story state before persistence."
    assert story.last_story_card == "Story opened."

    loaded = get_explorer_story(mem.store, "explorer-mode")
    assert loaded == story


def test_update_preserves_omitted_fields(tmp_path):
    mem = _client(tmp_path)
    update_explorer_story(
        mem.store,
        "explorer-mode",
        current_exploratory_story="Initial story.",
        narrative_field_summary="Initial summary.",
        last_story_card="Initial card.",
    )

    updated = update_explorer_story(
        mem.store,
        "explorer-mode",
        current_exploratory_story="Thickened story.",
    )

    assert updated.current_exploratory_story == "Thickened story."
    assert updated.narrative_field_summary == "Initial summary."
    assert updated.last_story_card == "Initial card."


def test_update_can_clear_explicit_scalar(tmp_path):
    mem = _client(tmp_path)
    update_explorer_story(
        mem.store,
        "explorer-mode",
        current_exploratory_story="Initial story.",
        narrative_field_summary="Initial summary.",
    )

    updated = update_explorer_story(
        mem.store,
        "explorer-mode",
        narrative_field_summary="",
    )

    assert updated.current_exploratory_story == "Initial story."
    assert updated.narrative_field_summary is None


def test_explorer_stories_are_isolated_by_journey(tmp_path):
    mem = _client(tmp_path)
    update_explorer_story(
        mem.store,
        "explorer-mode",
        current_exploratory_story="Explorer story.",
    )
    update_explorer_story(
        mem.store,
        "mirror-mind",
        current_exploratory_story="Mirror story.",
    )

    explorer = get_explorer_story(mem.store, "explorer-mode")
    mirror = get_explorer_story(mem.store, "mirror-mind")

    assert explorer is not None
    assert mirror is not None
    assert explorer.current_exploratory_story == "Explorer story."
    assert mirror.current_exploratory_story == "Mirror story."


def test_clear_explorer_story(tmp_path):
    mem = _client(tmp_path)
    update_explorer_story(
        mem.store,
        "explorer-mode",
        current_exploratory_story="Explorer story.",
    )

    clear_explorer_story(mem.store, "explorer-mode")

    assert get_explorer_story(mem.store, "explorer-mode") is None


def test_invalid_metadata_returns_none(tmp_path):
    mem = _client(tmp_path)
    mem.store.upsert_runtime_session(
        "__explorer_story__:explorer-mode",
        interface="explorer_story",
        journey="explorer-mode",
        active=True,
        metadata="{invalid-json",
    )

    assert get_explorer_story(mem.store, "explorer-mode") is None


def test_render_explorer_story_context(tmp_path):
    mem = _client(tmp_path)
    story = update_explorer_story(
        mem.store,
        "explorer-mode",
        current_exploratory_story="Explorer is becoming observable.",
        narrative_field_summary="Runtime story state before persistence.",
        last_story_card="Story opened.",
    )

    rendered = render_explorer_story_context(story)

    assert "=== △ Exploratory Story ===" in rendered
    assert "journey: explorer-mode" in rendered
    assert "Explorer is becoming observable." in rendered
    assert "Runtime story state before persistence." in rendered
    assert "Story opened." in rendered
