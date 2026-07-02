"""Ariad artifact materialization surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from memory.builder.surface_protocol import wrap_ariad_surface


@dataclass(frozen=True)
class MaterializedArtifact:
    kind: str
    path: Path
    status: str


def render_artifacts_materialized_surface(
    *,
    context: str,
    artifacts: tuple[MaterializedArtifact, ...],
    project_path: Path | None = None,
    boundary: str = "Files were materialized only.",
) -> str:
    lines = [
        "Artifacts",
        "",
        "╭────────────────────────────────────────────────────────╮",
        "│        ✎  ARTIFACTS MATERIALIZED                      │",
        "│                                                        │",
        *_card_wrapped(context),
        "│                                                        │",
    ]
    if artifacts:
        for index, artifact in enumerate(artifacts):
            if index > 0:
                lines.append("│                                                        │")
            lines.extend(
                _card_wrapped(f"{_status_icon(artifact.status)} {artifact.status} {artifact.kind}")
            )
            lines.extend(_card_wrapped(_display_path(artifact.path, project_path)))
    else:
        lines.append(_card_text("none"))
    lines.extend(
        [
            "│                                                        │",
            *_card_wrapped(boundary),
            "╰────────────────────────────────────────────────────────╯",
        ]
    )
    return wrap_ariad_surface("artifacts_materialized", "\n".join(lines) + "\n")


def materialized_artifact(kind: str, path: Path, *, existed_before: bool) -> MaterializedArtifact:
    return MaterializedArtifact(
        kind=kind,
        path=path,
        status="updated" if existed_before else "created",
    )


def existing_artifact(kind: str, path: Path) -> MaterializedArtifact:
    return MaterializedArtifact(kind=kind, path=path, status="existing")


def _status_icon(status: str) -> str:
    return {"created": "✓", "updated": "✎", "existing": "↻"}.get(status, "•")


def _display_path(path: Path, project_path: Path | None) -> str:
    resolved = path.expanduser()
    if project_path is not None:
        try:
            return str(resolved.resolve().relative_to(project_path.expanduser().resolve()))
        except (OSError, ValueError):
            pass
    return str(path)


def _card_text(text: str) -> str:
    width = 54
    return f"│ {text[:width]:<{width}} │"


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
