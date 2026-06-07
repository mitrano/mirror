"""Plain-text Explorer Story surfaces."""

from __future__ import annotations

from memory.services.explorer_story import ExplorerStory

WIDTH = 56


def render_exploratory_story_opened(story: ExplorerStory) -> str:
    return _box(
        "△  EXPLORATORY STORY OPENED",
        _story_rows(story, include_last_card=True),
    )


def render_story_thickened(story: ExplorerStory, *, changed: str | None = None) -> str:
    rows: list[tuple[str, str]] = []
    if changed and changed.strip():
        rows.append(("what changed", changed.strip()))
    rows.extend(_story_rows(story, include_last_card=True))
    return _box("△  STORY THICKENED", rows)


def render_narrative_field_snapshot(story: ExplorerStory) -> str:
    return _box(
        "△  NARRATIVE FIELD SNAPSHOT",
        _story_rows(story, include_last_card=True),
    )


def render_missing_exploratory_story(*, journey: str) -> str:
    return _box(
        "△  NO EXPLORATORY STORY",
        [
            ("journey", journey),
            ("state", "No current Exploratory Story is stored for this journey."),
        ],
    )


def _story_rows(story: ExplorerStory, *, include_last_card: bool) -> list[tuple[str, str]]:
    rows = [("journey", story.journey)]
    if story.current_exploratory_story:
        rows.append(("current story", story.current_exploratory_story))
    if story.narrative_field_summary:
        rows.append(("narrative summary", story.narrative_field_summary))
    if include_last_card and story.last_story_card:
        rows.append(("last card", story.last_story_card))
    if len(rows) == 1:
        rows.append(("current story", "No story text recorded yet."))
    return rows


def _box(title: str, rows: list[tuple[str, str]]) -> str:
    lines = ["Mirror", "╭" + "─" * WIDTH + "╮", _line(f"        {title}")]
    for label, value in rows:
        lines.append(_line(""))
        lines.append(_line(f"  {label}"))
        for wrapped in _wrap(value):
            lines.append(_line(f"  {wrapped}"))
    lines.append("╰" + "─" * WIDTH + "╯")
    return "\n".join(lines)


def _line(text: str) -> str:
    content = text[:WIDTH]
    return "│" + content.ljust(WIDTH) + "│"


def _wrap(text: str) -> list[str]:
    max_width = WIDTH - 2
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        if len(current) + 1 + len(word) <= max_width:
            current += " " + word
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines
