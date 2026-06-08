"""Soul Mode context loader."""

from __future__ import annotations

import argparse
import sys

from memory.client import MemoryClient
from memory.services.operating_mode import activate_mode, resolve_operating_session_id
from memory.services.soul import (
    clear_fruit_in_maturation,
    clear_harvested_fruit,
    get_fruit_in_maturation,
    get_harvested_fruit,
    harvest_fruit,
    resolve_soul_session_id,
    set_fruit_in_maturation,
)
from memory.services.soul_journal import compose_soul_harvest_journal
from memory.services.soul_prompt import compose_soul_self_voice_prompt
from memory.skills.mirror import _persist_global_sticky_defaults
from memory.surfaces.mode_transition import render_soul_mode_transition
from memory.surfaces.soul import (
    SoulListeningOption,
    render_active_rite,
    render_fruit_in_maturation,
    render_harvested_fruit,
    render_possible_listenings,
)


def cmd_load(slug: str | None = None, *, session_id: str | None = None) -> None:
    mem = MemoryClient()
    if slug:
        journey_content = mem.get_identity("journey", slug)
        if not journey_content:
            print(f"Error: journey '{slug}' not found.", file=sys.stderr)
            sys.exit(1)
        _persist_global_sticky_defaults(mem, persona=None, journey=slug)

    resolved_session_id = resolve_operating_session_id(mem.store, session_id)
    activate_mode(
        mem.store,
        mode="Soul Mode",
        journey=slug,
        session_id=resolved_session_id,
    )
    print(render_soul_mode_transition(journey=slug))


def cmd_listen(
    *,
    self_description: str | None = None,
    shadow_description: str | None = None,
    wisdom_description: str | None = None,
    beauty_description: str | None = None,
) -> None:
    options = _listening_options(
        self_description=self_description,
        shadow_description=shadow_description,
        wisdom_description=wisdom_description,
        beauty_description=beauty_description,
    )
    try:
        print(render_possible_listenings(options))
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


def cmd_rite(
    voice: str,
    *,
    utterance: str | None = None,
    listening_for: str | None = None,
    question: str | None = None,
) -> None:
    try:
        print(
            render_active_rite(
                voice,
                utterance=utterance,
                listening_for=listening_for,
                question=question,
            )
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


def cmd_fruit(
    action: str,
    fruit: str | None = None,
    *,
    session_id: str | None = None,
) -> None:
    mem = MemoryClient()
    resolved_session_id = _resolve_cli_soul_session_id(mem, session_id)
    try:
        if action == "set":
            if fruit is None:
                raise ValueError("fruit must not be empty")
            state = set_fruit_in_maturation(mem.store, fruit, session_id=resolved_session_id)
            print(render_fruit_in_maturation(state.fruit or ""))
        elif action == "show":
            state = get_fruit_in_maturation(mem.store, session_id=resolved_session_id)
            if not state.fruit:
                print("Error: No fruit in maturation.", file=sys.stderr)
                sys.exit(1)
            print(render_fruit_in_maturation(state.fruit))
        elif action == "clear":
            clear_fruit_in_maturation(mem.store, session_id=resolved_session_id)
            print("Fruit in maturation cleared.")
        else:
            raise ValueError(f"unknown fruit action: {action}")
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


def cmd_harvest(
    action: str,
    fruit: str | None = None,
    *,
    session_id: str | None = None,
    journey: str | None = None,
) -> None:
    mem = MemoryClient()
    resolved_session_id = _resolve_cli_soul_session_id(mem, session_id)
    try:
        if action == "set":
            state = harvest_fruit(mem.store, fruit=fruit, session_id=resolved_session_id)
            print(render_harvested_fruit(state.fruit or ""))
        elif action == "show":
            state = get_harvested_fruit(mem.store, session_id=resolved_session_id)
            if not state.fruit:
                print("Error: No harvested fruit.", file=sys.stderr)
                sys.exit(1)
            print(render_harvested_fruit(state.fruit))
        elif action == "save":
            state = get_harvested_fruit(mem.store, session_id=resolved_session_id)
            if not state.fruit:
                print("Error: No harvested fruit.", file=sys.stderr)
                sys.exit(1)
            conversation_id = _conversation_id_for_session(mem, resolved_session_id)
            journal = compose_soul_harvest_journal(
                fruit=state.fruit,
                conversation_id=conversation_id,
                messages=mem.store.get_messages(conversation_id) if conversation_id else [],
            )
            memory = mem.add_journal(
                content=journal.content,
                title=journal.title,
                layer="self",
                tags=["soul-mode", "harvested-fruit"],
                conversation_id=conversation_id,
                journey=journey,
                metadata=journal.metadata,
            )
            clear_harvested_fruit(mem.store, session_id=resolved_session_id)
            print(f"Harvest saved to journal. {memory.id}")
        elif action == "decline":
            clear_harvested_fruit(mem.store, session_id=resolved_session_id)
            print("Harvest discarded without journal save.")
        else:
            raise ValueError(f"unknown harvest action: {action}")
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


def cmd_prompt(voice: str) -> None:
    if voice != "self":
        print(f"Error: unsupported Soul Mode prompt voice: {voice}", file=sys.stderr)
        sys.exit(1)
    mem = MemoryClient()
    print(compose_soul_self_voice_prompt(mem))


def _resolve_cli_soul_session_id(mem: MemoryClient, session_id: str | None) -> str:
    return resolve_operating_session_id(mem.store, session_id) or resolve_soul_session_id(
        session_id
    )


def _conversation_id_for_session(mem: MemoryClient, session_id: str) -> str | None:
    session = mem.store.get_runtime_session(session_id)
    return session.conversation_id if session else None


def _listening_options(
    *,
    self_description: str | None,
    shadow_description: str | None,
    wisdom_description: str | None,
    beauty_description: str | None,
) -> list[SoulListeningOption]:
    raw_options = [
        ("self", self_description),
        ("shadow", shadow_description),
        ("wisdom", wisdom_description),
        ("beauty", beauty_description),
    ]
    return [
        SoulListeningOption(voice=voice, description=description.strip())
        for voice, description in raw_options
        if isinstance(description, str) and description.strip()
    ]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Soul Mode context loader")
    sub = parser.add_subparsers(dest="command", required=True)

    p_load = sub.add_parser("load", help="Activate Soul Mode")
    p_load.add_argument("slug", nargs="?", help="Optional journey ID")
    p_load.add_argument(
        "--session-id",
        default=None,
        help="Runtime session id for session-scoped operating mode state",
    )

    p_listen = sub.add_parser("listen", help="Render situated possible listenings")
    p_listen.add_argument("--matter", default=None, help="Living matter context for callers")
    p_listen.add_argument("--self", dest="self_description", default=None)
    p_listen.add_argument("--shadow", dest="shadow_description", default=None)
    p_listen.add_argument("--wisdom", dest="wisdom_description", default=None)
    p_listen.add_argument("--beauty", dest="beauty_description", default=None)

    p_rite = sub.add_parser("rite", help="Render an active Soul Mode rite")
    p_rite.add_argument("voice", choices=["self", "shadow"], help="Rite voice to activate")
    p_rite.add_argument("--says", dest="utterance", default=None, help="What the voice says")
    p_rite.add_argument("--listening-for", default=None, help="Situated listening focus")
    p_rite.add_argument("--question", default=None, help="Legacy alias for --says")

    p_fruit = sub.add_parser("fruit", help="Manage provisional Soul Mode fruit")
    fruit_sub = p_fruit.add_subparsers(dest="fruit_action", required=True)
    p_fruit_set = fruit_sub.add_parser("set", help="Set and render fruit in maturation")
    p_fruit_set.add_argument("fruit")
    p_fruit_set.add_argument("--session-id", default=None)
    p_fruit_show = fruit_sub.add_parser("show", help="Render current fruit in maturation")
    p_fruit_show.add_argument("--session-id", default=None)
    p_fruit_clear = fruit_sub.add_parser("clear", help="Clear current fruit in maturation")
    p_fruit_clear.add_argument("--session-id", default=None)

    p_harvest = sub.add_parser("harvest", help="Manage harvested Soul Mode fruit")
    harvest_sub = p_harvest.add_subparsers(dest="harvest_action", required=True)
    p_harvest_set = harvest_sub.add_parser("set", help="Set and render harvested fruit")
    p_harvest_set.add_argument("fruit", nargs="?")
    p_harvest_set.add_argument("--session-id", default=None)
    p_harvest_show = harvest_sub.add_parser("show", help="Render current harvested fruit")
    p_harvest_show.add_argument("--session-id", default=None)
    p_harvest_save = harvest_sub.add_parser("save", help="Save harvested fruit to journal")
    p_harvest_save.add_argument("--session-id", default=None)
    p_harvest_save.add_argument("--journey", default=None)
    p_harvest_decline = harvest_sub.add_parser("decline", help="Discard harvested fruit")
    p_harvest_decline.add_argument("--session-id", default=None)

    p_prompt = sub.add_parser("prompt", help="Render composed Soul Mode voice prompts")
    prompt_sub = p_prompt.add_subparsers(dest="prompt_voice", required=True)
    prompt_sub.add_parser("self", help="Render Self Voice prompt with user Self identity")

    args = parser.parse_args(argv)

    if args.command == "load":
        cmd_load(args.slug, session_id=args.session_id)
    elif args.command == "listen":
        cmd_listen(
            self_description=args.self_description,
            shadow_description=args.shadow_description,
            wisdom_description=args.wisdom_description,
            beauty_description=args.beauty_description,
        )
    elif args.command == "rite":
        cmd_rite(
            args.voice,
            utterance=args.utterance,
            listening_for=args.listening_for,
            question=args.question,
        )
    elif args.command == "fruit":
        cmd_fruit(
            args.fruit_action,
            getattr(args, "fruit", None),
            session_id=getattr(args, "session_id", None),
        )
    elif args.command == "harvest":
        cmd_harvest(
            args.harvest_action,
            getattr(args, "fruit", None),
            session_id=getattr(args, "session_id", None),
            journey=getattr(args, "journey", None),
        )
    elif args.command == "prompt":
        cmd_prompt(args.prompt_voice)
