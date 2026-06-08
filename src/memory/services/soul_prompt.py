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
    return files("memory.prompts").joinpath("soul_self_voice.md").read_text(encoding="utf-8")


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
