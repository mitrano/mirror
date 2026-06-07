"""Tests for Explorer Story user-facing surfaces."""

from memory.services.explorer_story import ExplorerStory
from memory.surfaces.explorer_story import (
    render_exploratory_story_opened,
    render_missing_exploratory_story,
    render_narrative_field_snapshot,
    render_story_thickened,
)


def _story() -> ExplorerStory:
    return ExplorerStory(
        journey="explorer-mode",
        current_exploratory_story="Explorer centers on one accumulated story.",
        narrative_field_summary="Signals were removed from the first behavior slice.",
        last_story_card="The story became the observable unit.",
    )


def test_opened_surface_renders_story():
    rendered = render_exploratory_story_opened(_story())

    assert "△  EXPLORATORY STORY OPENED" in rendered
    assert "explorer-mode" in rendered
    assert "Explorer centers on one accumulated story." in rendered


def test_thickened_surface_renders_change_and_story():
    rendered = render_story_thickened(_story(), changed="External behavior became required.")

    assert "△  STORY THICKENED" in rendered
    assert "External behavior became required." in rendered
    assert "Explorer centers on one accumulated story." in rendered
    assert "Signals were removed" in rendered


def test_snapshot_surface_renders_current_field():
    rendered = render_narrative_field_snapshot(_story())

    assert "△  NARRATIVE FIELD SNAPSHOT" in rendered
    assert "Explorer centers on one accumulated story." in rendered
    assert "The story became the observable unit." in rendered


def test_missing_story_surface_is_clear():
    rendered = render_missing_exploratory_story(journey="explorer-mode")

    assert "△  NO EXPLORATORY STORY" in rendered
    assert "No current Exploratory Story" in rendered
