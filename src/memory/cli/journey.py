"""Journey CLI: inspect, create, and update journey status."""

import argparse
import re
import sys

from memory import MemoryClient
from memory.cli.common import db_path_from_mirror_home

_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def _prompt(label: str, current: str | None = None) -> str:
    if current:
        return current
    return input(f"{label}: ").strip()


def _format_journey_identity(
    *,
    name: str,
    status: str,
    description: str,
    briefing: str,
    context: str,
) -> str:
    parts = [f"# {name}", f"**Status:** {status}"]
    if description:
        parts.append(f"\n## Description\n\n{description}")
    if briefing:
        parts.append(f"\n## Briefing\n\n{briefing}")
    if context:
        parts.append(f"\n## Context\n\n{context}")
    return "\n".join(parts).rstrip() + "\n"


def cmd_create(args: list[str], *, mirror_home: str | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="memory journey create",
        description="Interactively create a journey identity entry",
    )
    parser.add_argument("slug", nargs="?", help="Journey slug, e.g. personal-growth")
    parser.add_argument("--name", default=None, help="Human-readable journey name")
    parser.add_argument("--status", default="active", help="Journey status (default: active)")
    parser.add_argument("--description", default=None, help="Short description")
    parser.add_argument("--briefing", default=None, help="When the mirror should use this journey")
    parser.add_argument("--context", default=None, help="Living context for the journey")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing journey")
    parsed = parser.parse_args(args)

    slug = _prompt("Journey slug", parsed.slug)
    if not _SLUG_RE.match(slug):
        print(
            "Error: slug must use lowercase letters, numbers, and hyphens.",
            file=sys.stderr,
        )
        sys.exit(1)

    mem = MemoryClient(db_path=db_path_from_mirror_home(mirror_home))
    existing = mem.store.get_identity("journey", slug)
    if existing and not parsed.force:
        print(
            f"Error: journey '{slug}' already exists. Use --force to overwrite.",
            file=sys.stderr,
        )
        sys.exit(1)

    name = _prompt("Name", parsed.name) or slug.replace("-", " ").title()
    description = _prompt("Description", parsed.description)
    briefing = _prompt("Briefing", parsed.briefing)
    context = _prompt("Context", parsed.context)

    if not description:
        print("Error: description is required.", file=sys.stderr)
        sys.exit(1)

    content = _format_journey_identity(
        name=name,
        status=parsed.status,
        description=description,
        briefing=briefing,
        context=context,
    )
    mem.set_identity("journey", slug, content)
    action = "updated" if existing else "created"
    print(f"✓ journey/{slug} {action}")


def cmd_status(journey: str | None, *, mirror_home: str | None = None) -> None:
    mem = MemoryClient(db_path=db_path_from_mirror_home(mirror_home))
    status = mem.get_journey_status(journey)

    for name, data in status.items():
        print(f"=== journey: {name} ===")

        if data.get("identity"):
            print("\n--- identity ---")
            print(data["identity"])

        if data.get("journey_path"):
            print("\n--- journey path ---")
            print(data["journey_path"])

        memories = data.get("recent_memories", [])
        if memories:
            print(f"\n--- recent memories ({len(memories)}) ---")
            for m in memories:
                print(f"  [{m.created_at[:10]}] {m.title}")
        else:
            print("\n--- recent memories ---")
            print("  No recent memories.")

        conversations = data.get("recent_conversations", [])
        if conversations:
            print(f"\n--- recent conversations ({len(conversations)}) ---")
            for c in conversations:
                title = c.title or "(untitled)"
                print(f"  [{c.started_at[:10]}] {title}")
        else:
            print("\n--- recent conversations ---")
            print("  No recent conversations.")

        print()


def cmd_set_path(journey: str, path: str, *, mirror_home: str | None = None) -> None:
    mem = MemoryClient(db_path=db_path_from_mirror_home(mirror_home))
    try:
        project_path = mem.journeys.set_project_path(journey, path)
    except ValueError:
        print(f"Error: journey '{journey}' not found.", file=sys.stderr)
        sys.exit(1)
    print(f"project_path set for '{journey}': {project_path}", file=sys.stderr)
    print(project_path)


def cmd_update(journey: str, content: str, *, mirror_home: str | None = None) -> None:
    if content == "-":
        content = sys.stdin.read()
    mem = MemoryClient(db_path=db_path_from_mirror_home(mirror_home))
    mem.set_journey_path(journey, content)
    print(f"Journey path '{journey}' updated.", file=sys.stderr)


def _parse_args(argv: list[str]) -> tuple[str | None, list[str]]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--mirror-home", default=None)
    parsed, remaining = parser.parse_known_args(argv)
    return parsed.mirror_home, remaining


def main(argv: list[str] | None = None) -> None:
    args = sys.argv[1:] if argv is None else argv
    mirror_home, remaining = _parse_args(args)

    if remaining and remaining[0] == "create":
        cmd_create(remaining[1:], mirror_home=mirror_home)
    elif remaining and remaining[0] == "update":
        if len(remaining) < 3:
            print("Usage: python -m memory journey update <slug> <content|-stdin>", file=sys.stderr)
            sys.exit(1)
        cmd_update(remaining[1], remaining[2], mirror_home=mirror_home)
    elif remaining and remaining[0] == "set-path":
        if len(remaining) < 3:
            print("Usage: python -m memory journey set-path <slug> <path>", file=sys.stderr)
            sys.exit(1)
        cmd_set_path(remaining[1], remaining[2], mirror_home=mirror_home)
    else:
        # Optional: journey status [slug]
        slug = (
            remaining[1]
            if len(remaining) >= 2 and remaining[0] == "status"
            else (remaining[0] if remaining else None)
        )
        cmd_status(slug, mirror_home=mirror_home)


if __name__ == "__main__":
    main()
