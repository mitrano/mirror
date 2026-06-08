"""Prompt composition for Soul Mode voices."""

from __future__ import annotations

from importlib.resources import files

from memory.client import MemoryClient

SELF_IDENTITY_PLACEHOLDER = "{user_self_identity}"
SELF_IDENTITY_UNAVAILABLE = (
    "No user Self identity layer is available yet. Use only the base Self Voice grammar."
)


def load_soul_self_voice_template() -> str:
    """Load the packaged Self Voice prompt template."""
    return _load_prompt("soul_self_voice.md")


def load_soul_wisdom_voice_template() -> str:
    """Load the packaged Wisdom Voice prompt template."""
    return _load_prompt("soul_wisdom_voice.md")


def load_soul_beauty_voice_template() -> str:
    """Load the packaged Beauty Voice prompt template."""
    return _load_prompt("soul_beauty_voice.md")


def compose_soul_self_voice_prompt(mem: MemoryClient) -> str:
    """Compose Self Voice prompt with the user's current Self identity layer."""
    template = load_soul_self_voice_template()
    identity = mem.get_identity("self", "soul")
    injected_identity = (
        identity.strip()
        if isinstance(identity, str) and identity.strip()
        else SELF_IDENTITY_UNAVAILABLE
    )
    return template.replace(SELF_IDENTITY_PLACEHOLDER, injected_identity)


def compose_soul_wisdom_voice_prompt() -> str:
    """Compose Wisdom Voice prompt."""
    return load_soul_wisdom_voice_template()


def compose_soul_beauty_voice_prompt() -> str:
    """Compose Beauty Voice prompt."""
    return load_soul_beauty_voice_template()


def _load_prompt(filename: str) -> str:
    return files("memory.prompts").joinpath(filename).read_text(encoding="utf-8")
