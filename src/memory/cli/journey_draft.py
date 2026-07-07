"""CLI for journey draft pre-opening documents."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from memory import MemoryClient
from memory.cli.common import db_path_from_mirror_home
from memory.services.journey_draft import JourneyDraftService, slugify


def _client_and_service(mirror_home: str | None) -> tuple[MemoryClient, JourneyDraftService]:
    mem = MemoryClient(db_path=db_path_from_mirror_home(mirror_home))
    return mem, JourneyDraftService(mem.journeys)


def cmd_start(args: argparse.Namespace) -> int:
    mem, service = _client_and_service(args.mirror_home)
    try:
        slug = args.slug or slugify(args.name)
        content = sys.stdin.read() if args.content_file == "-" else None
        if args.content_file and args.content_file != "-":
            content = Path(args.content_file).read_text(encoding="utf-8")
        result = service.write_draft(
            slug=slug,
            name=args.name,
            content=content,
            base_dir=args.base_dir,
            force=args.force,
        )
    finally:
        mem.close()
    print("Journey draft created")
    print(f"slug={result.slug}")
    print(f"draft_dir={result.draft_dir}")
    print(f"draft_file={result.draft_file}")
    return 0


def cmd_path(args: argparse.Namespace) -> int:
    mem, service = _client_and_service(args.mirror_home)
    try:
        print(service.draft_file(args.slug, base_dir=args.base_dir))
    finally:
        mem.close()
    return 0


def cmd_promote(args: argparse.Namespace) -> int:
    mem, service = _client_and_service(args.mirror_home)
    try:
        result = service.promote_draft(slug=args.slug, base_dir=args.base_dir, force=args.force)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    finally:
        mem.close()
    print("Journey draft promoted")
    print(f"journey={result.slug}")
    print(f"name={result.name}")
    print(f"final_dir={result.final_dir}")
    print(f"opening_file={result.opening_file}")
    print(f"journey_path_file={result.journey_path_file}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m memory journey-draft")
    parser.add_argument("--mirror-home", default=None)
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start", help="Create or rewrite a journey draft document")
    start.add_argument("--name", required=True)
    start.add_argument("--slug", default=None)
    start.add_argument("--base-dir", default="journeys")
    start.add_argument(
        "--content-file", default=None, help="Markdown file to write, or '-' for stdin"
    )
    start.add_argument("--force", action="store_true")
    start.set_defaults(func=cmd_start)

    path = sub.add_parser("path", help="Print the draft document path for a slug")
    path.add_argument("slug")
    path.add_argument("--base-dir", default="journeys")
    path.set_defaults(func=cmd_path)

    promote = sub.add_parser("promote", help="Create a real journey from an approved draft")
    promote.add_argument("slug")
    promote.add_argument("--base-dir", default="journeys")
    promote.add_argument("--force", action="store_true")
    promote.set_defaults(func=cmd_promote)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
