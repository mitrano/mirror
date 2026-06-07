"""Explorer Mode context loader.

First slice: activate Explorer Mode for a journey and return the normal Mirror
context plus exploratory operating instructions. Explorer state and story
thickening persistence are later CV16 stories.
"""

from __future__ import annotations

import argparse
import sys

from memory.client import MemoryClient
from memory.services.explorer_story import (
    clear_explorer_story,
    get_explorer_story,
    render_explorer_story_context,
    update_explorer_story,
)
from memory.services.operating_mode import activate_mode, deactivate_mode
from memory.skills.mirror import _persist_global_sticky_defaults
from memory.surfaces.mode_transition import render_explorer_mode_transition

EXPLORER_GUIDANCE = """=== Explorer Mode guidance ===
Explorer Mode is experimental. The full Explorer experience is being built and will be available soon.

Explorer preserves uncertainty. Builder executes commitment.

While Explorer Mode is active:
- Treat new substantive material as part of the current Exploratory Story unless the user asks for a clear operational action.
- Preserve tensions, hypotheses, corrections, and emerging story shape.
- Update the in-session story when new material changes the accumulated story.
- Render Story Thickened when new material changes the accumulated story.
- Do not promote to Builder or Delivery without explicit user confirmation.
"""

EXPLORER_DEACTIVATED_SURFACE = """Mirror
╭────────────────────────────────────────────────────────╮
│        △  EXPLORER MODE DEACTIVATED                    │
│                                                        │
│  current lens                                          │
│  ◌ Mirror Mode                                         │
│                                                        │
│  context                                               │
│  Journey context remains available when it is sticky.  │
│                                                        │
│  boundary                                              │
│  Explorer lens ended. Uncertainty was not promoted.    │
╰────────────────────────────────────────────────────────╯
"""


def cmd_load(slug: str) -> None:
    mem = MemoryClient()
    journey_content = mem.get_identity("journey", slug)
    if not journey_content:
        print(f"Error: journey '{slug}' not found.", file=sys.stderr)
        sys.exit(1)

    activate_mode(mem.store, mode="Explorer Mode", journey=slug)
    _persist_global_sticky_defaults(mem, persona=None, journey=slug)

    print(f"\033[38;5;183m△ Explorer Mode active — journey: {slug}\033[0m", file=sys.stderr)
    print(render_explorer_mode_transition(journey=slug))
    print(mem.load_mirror_context(journey=slug))
    story = get_explorer_story(mem.store, slug)
    if story:
        print("\n" + render_explorer_story_context(story))
    print("\n" + EXPLORER_GUIDANCE)


def cmd_deactivate() -> None:
    mem = MemoryClient()
    deactivate_mode(mem.store)
    print(EXPLORER_DEACTIVATED_SURFACE)


def cmd_story_show(slug: str) -> None:
    mem = MemoryClient()
    story = get_explorer_story(mem.store, slug)
    if not story:
        print(f"No Exploratory Story for journey: {slug}")
        return
    print(render_explorer_story_context(story))


def cmd_story_update(
    slug: str,
    *,
    story: str | None,
    summary: str | None,
    last_card: str | None,
) -> None:
    mem = MemoryClient()
    updated = update_explorer_story(
        mem.store,
        slug,
        current_exploratory_story=story,
        narrative_field_summary=summary,
        last_story_card=last_card,
    )
    print(render_explorer_story_context(updated))


def cmd_story_clear(slug: str) -> None:
    mem = MemoryClient()
    clear_explorer_story(mem.store, slug)
    print(f"Exploratory Story cleared for journey: {slug}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Explorer Mode context loader")
    sub = parser.add_subparsers(dest="command", required=True)

    p_load = sub.add_parser("load", help="Activate Explorer Mode for a journey")
    p_load.add_argument("slug", help="Journey ID")

    sub.add_parser("deactivate", help="Deactivate Explorer Mode and return to Mirror Mode")

    p_story = sub.add_parser("story", help="Manage the current Exploratory Story")
    story_sub = p_story.add_subparsers(dest="story_command", required=True)

    p_story_show = story_sub.add_parser("show", help="Show the current Exploratory Story")
    p_story_show.add_argument("slug", help="Journey ID")

    p_story_update = story_sub.add_parser("update", help="Create or update the Exploratory Story")
    p_story_update.add_argument("slug", help="Journey ID")
    p_story_update.add_argument("--story", default=None, help="Current exploratory story")
    p_story_update.add_argument("--summary", default=None, help="Narrative field summary")
    p_story_update.add_argument("--last-card", default=None, help="Last story card context")

    p_story_clear = story_sub.add_parser("clear", help="Clear the current Exploratory Story")
    p_story_clear.add_argument("slug", help="Journey ID")

    args = parser.parse_args(argv)
    if args.command == "load":
        cmd_load(args.slug)
    elif args.command == "deactivate":
        cmd_deactivate()
    elif args.command == "story":
        if args.story_command == "show":
            cmd_story_show(args.slug)
        elif args.story_command == "update":
            cmd_story_update(
                args.slug,
                story=args.story,
                summary=args.summary,
                last_card=args.last_card,
            )
        elif args.story_command == "clear":
            cmd_story_clear(args.slug)


if __name__ == "__main__":
    main()
