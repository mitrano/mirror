"""Soul Mode journal entry composition."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from memory.models import Message


@dataclass(frozen=True)
class SoulJournalEntry:
    title: str
    content: str
    metadata: str


def compose_soul_harvest_journal(
    *,
    fruit: str,
    conversation_id: str | None = None,
    messages: list[Message] | None = None,
) -> SoulJournalEntry:
    """Compose a structured Markdown journal entry from a harvested fruit.

    The harvested fruit remains the ritual synthesis, but the persisted journal
    entry preserves more source material and links back to the conversation when
    available.
    """
    normalized_fruit = fruit.strip()
    if not normalized_fruit:
        raise ValueError("harvested fruit must not be empty")

    title = _title_from_fruit(normalized_fruit)
    content = _markdown_content(
        fruit=normalized_fruit,
        conversation_id=conversation_id,
        messages=messages or [],
    )
    metadata = {
        "format": "markdown",
        "origin": {
            "mode": "soul",
            "conversation_id": conversation_id,
            "conversation_uri": f"mirror://conversation/{conversation_id}"
            if conversation_id
            else None,
        },
        "harvested_fruit": normalized_fruit,
    }
    return SoulJournalEntry(
        title=title,
        content=content,
        metadata=json.dumps(metadata, ensure_ascii=False),
    )


def _title_from_fruit(fruit: str) -> str:
    first_sentence = re.split(r"(?<=[.!?])\s+", fruit, maxsplit=1)[0].strip()
    first_sentence = first_sentence.rstrip(".!?").strip()
    if len(first_sentence) <= 80:
        return first_sentence
    return first_sentence[:77].rstrip() + "..."


def _markdown_content(
    *,
    fruit: str,
    conversation_id: str | None,
    messages: list[Message],
) -> str:
    sections = [
        "Esta entrada nasceu de uma colheita em Soul Mode.",
        "## Fruto\n\n" + _blockquote(fruit),
    ]

    if conversation_id:
        sections.append(f"## Origem\n\n[Conversa originária](mirror://conversation/{conversation_id})")

    transcript = _format_transcript(messages)
    if transcript:
        sections.append("## Material vivo da conversa\n\n" + transcript)

    return "\n\n".join(sections) + "\n"


def _format_transcript(messages: list[Message], *, limit: int = 16) -> str:
    if not messages:
        return ""
    selected = messages[:limit]
    lines: list[str] = []
    for message in selected:
        role = "User" if message.role == "user" else "Mirror" if message.role == "assistant" else message.role.title()
        content = message.content.strip()
        if not content:
            continue
        lines.append(f"### {role}\n\n{content}")
    omitted = len(messages) - len(selected)
    if omitted > 0:
        lines.append(f"_Mais {omitted} mensagens ficaram preservadas na conversa originária._")
    return "\n\n".join(lines)


def _blockquote(text: str) -> str:
    return "\n".join(f"> {line}" if line else ">" for line in text.splitlines())
