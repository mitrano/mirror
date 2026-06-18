"""Builder Home surface rendering for Ariad-adopted journeys."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from memory.builder.lifecycle_ribbon import render_lifecycle_ribbon
from memory.builder.pull_candidates import PullCandidatesReport
from memory.builder.surface_protocol import wrap_ariad_surface


@dataclass(frozen=True)
class RefinementFieldSnapshot:
    """Read-only Builder Home snapshot of nascent Refinement state."""

    active_refinement_story: str | None
    storage_state: str
    seed_change_requests: int
    seed_change_request_source: str | None
    next_move: str


def inspect_refinement_field(project_path: Path | None) -> RefinementFieldSnapshot:
    """Inspect current refinement field without requiring durable Workbench storage."""
    if project_path is None:
        return RefinementFieldSnapshot(
            active_refinement_story=None,
            storage_state="not implemented yet",
            seed_change_requests=0,
            seed_change_request_source=None,
            next_move="implement Workbench Storage Model before durable RS/CR work",
        )
    root = project_path.expanduser().resolve()
    ds6_plan = (
        root
        / "docs/project/roadmap/cv20-builder-mode-evolution/"
        / "cv20-ds6-refinement-workbench-flow/plan.md"
    )
    seed_count = 0
    seed_source: str | None = None
    if ds6_plan.is_file():
        try:
            content = ds6_plan.read_text(encoding="utf-8")
        except OSError:
            content = ""
        seed_count = len(re.findall(r"^###\s+CR:", content, flags=re.MULTILINE))
        if seed_count:
            seed_source = str(ds6_plan.resolve().relative_to(root))
    return RefinementFieldSnapshot(
        active_refinement_story=None,
        storage_state="not implemented yet",
        seed_change_requests=seed_count,
        seed_change_request_source=seed_source,
        next_move="implement Workbench Storage Model before durable RS/CR work",
    )


def render_builder_home_surface(
    *,
    journey: str,
    method: str,
    candidates_report: PullCandidatesReport,
    refinement: RefinementFieldSnapshot,
) -> str:
    """Render no-active-item Builder Home orientation for Ariad journeys."""
    recommended = candidates_report.recommended
    lines = [
        "Builder Home",
        render_lifecycle_ribbon("pull"),
        "",
        "╭────────────────────────────────────────────────────────╮",
        "│        ■  BUILDER HOME                                 │",
        "│                                                        │",
        _card_text("journey"),
        _card_text(journey),
        "│                                                        │",
        _card_text("method"),
        _card_text(method),
        "│                                                        │",
        _card_text("Delivery field"),
        *_card_wrapped(
            f"recommended pull: {_format_recommended(recommended)}"
            if recommended
            else "recommended pull: none"
        ),
        "│                                                        │",
        _card_text("Refinement field"),
        _card_text(f"active RS: {refinement.active_refinement_story or 'none'}"),
        _card_text(f"workbench storage: {refinement.storage_state}"),
        _card_text(f"seed CRs: {refinement.seed_change_requests}"),
    ]
    if refinement.seed_change_request_source:
        lines.extend(_card_wrapped(f"seed source: {refinement.seed_change_request_source}"))
    lines.extend(
        [
            _card_text(f"next refinement move: {refinement.next_move}"),
            "│                                                        │",
            _card_text("available moves"),
            *_card_prefixed(
                tuple(
                    move
                    for move in (
                        "pull recommended Delivery item",
                        "inspect roadmap further",
                        "review seed Change Requests",
                        "implement Workbench Storage Model before durable RS/CR work",
                    )
                ),
                "-",
            ),
            "│                                                        │",
            _card_text("boundary"),
            *_card_wrapped(
                "Builder Home orients only; no item was pulled and no lifecycle work was executed."
            ),
            "╰────────────────────────────────────────────────────────╯",
        ]
    )
    return wrap_ariad_surface("builder_home", "\n".join(lines) + "\n")


def _format_recommended(candidate: object | None) -> str:
    if candidate is None:
        return "none"
    code = getattr(candidate, "code", "")
    title = getattr(candidate, "title", "")
    level = getattr(candidate, "level", "")
    return f"{code} — {title} [{level}]"


def _card_text(text: str) -> str:
    width = 54
    return f"│ {text[:width]:<{width}} │"


def _card_prefixed(items: tuple[str, ...], prefix: str) -> list[str]:
    if not items:
        return [_card_text("none")]
    lines: list[str] = []
    for item in items:
        wrapped = _wrap_plain_text(item, width=52)
        for index, line in enumerate(wrapped):
            marker = prefix if index == 0 else " "
            lines.append(_card_text(f"{marker} {line}"))
    return lines


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
