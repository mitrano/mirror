"""Task management CLI command."""

import argparse
import json

from memory import MemoryClient
from memory.models import Task

STATUS_ICONS = {
    "todo": "○",
    "doing": "◐",
    "done": "●",
    "blocked": "✖",
}


def _resolve_task(mem: MemoryClient, task_id: str) -> Task | None:
    task = mem.store.get_task(task_id)
    if task:
        return task

    all_tasks = mem.store.get_all_tasks()
    matches = [t for t in all_tasks if t.id.startswith(task_id)]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        print(f"❌ Ambiguous ID '{task_id}'. Matches:")
        for match in matches:
            print(f"  - `{match.id}` {match.title}")
        return None

    print(f"❌ Task '{task_id}' not found.")
    return None


def _format_optional(label: str, value: str | None) -> str:
    return f"{label}: {value if value else '(not set)'}"


def _format_metadata(metadata: str | None) -> str:
    if not metadata:
        return "(not set)"
    try:
        parsed = json.loads(metadata)
    except json.JSONDecodeError:
        return metadata
    return json.dumps(parsed, indent=2, ensure_ascii=False)


def cmd_show(mem: MemoryClient, args: argparse.Namespace) -> None:
    task = _resolve_task(mem, args.task_id)
    if not task:
        return

    icon = STATUS_ICONS.get(task.status, "?")
    print("📋 Tarefa")
    print()
    print(f"Objetivo: {task.title}")
    print()
    print("Identificação:")
    print(f"- ID: `{task.id}`")
    print(f"- Jornada: `{task.journey}`" if task.journey else "- Jornada: (not set)")
    print(f"- Status: {icon} {task.status}")
    print(f"- Origem: {task.source}")
    print()
    print("Planejamento:")
    print(f"- {_format_optional('Etapa', task.stage)}")
    print(f"- {_format_optional('Prazo', task.due_date)}")
    print(f"- {_format_optional('Horário agendado', task.scheduled_at)}")
    print(f"- {_format_optional('Dica de horário', task.time_hint)}")
    print()
    print("Datas:")
    print(f"- Criada em: {task.created_at}")
    print(f"- Atualizada em: {task.updated_at}")
    print(f"- {_format_optional('Concluída em', task.completed_at)}")
    print()
    print("Contexto:")
    print(task.context or "(not set)")
    print()
    print("Metadados:")
    print(_format_metadata(task.metadata))


def cmd_list(mem: MemoryClient, args: argparse.Namespace) -> None:
    if args.all:
        tasks = mem.list_tasks(journey=args.journey)
    elif args.status:
        tasks = mem.list_tasks(journey=args.journey, status=args.status)
    else:
        tasks = mem.list_tasks(journey=args.journey, open_only=True)

    if not tasks:
        print("No tasks found.")
        return

    by_journey: dict[str, list] = {}
    for t in tasks:
        key = t.journey or "(no journey)"
        by_journey.setdefault(key, []).append(t)

    if args.all:
        label = "all"
    elif args.status:
        label = args.status
    else:
        label = "open"
    total_open = sum(1 for t in tasks if t.status in ("todo", "doing", "blocked"))
    open_note = f" ({total_open} open)" if not args.status else ""
    print(f"📋 Tasks {label}: {len(tasks)}{open_note}\n")

    for journey, journey_tasks in by_journey.items():
        print(f"🧭 {journey}")
        for t in journey_tasks:
            icon = STATUS_ICONS.get(t.status, "?")
            due = f" 📅 {t.due_date}" if t.due_date else ""
            stage = f" [{t.stage}]" if t.stage else ""
            print(f"  {icon} `{t.id}` {t.title}{due}{stage}")
        print()


def cmd_add(mem: MemoryClient, args: argparse.Namespace) -> None:
    task = mem.add_task(
        title=args.title,
        journey=args.journey,
        due_date=args.due,
        stage=args.stage,
        source="manual",
    )
    print(f"✅ Task created: `{task.id}` - {task.title}")
    if task.journey:
        print(f"   Journey: {task.journey}")
    if task.due_date:
        print(f"   Due: {task.due_date}")


def cmd_status_change(mem: MemoryClient, args: argparse.Namespace, new_status: str) -> None:
    task = mem.store.get_task(args.task_id)
    if not task:
        all_tasks = mem.store.get_all_tasks()
        matches = [t for t in all_tasks if t.id.startswith(args.task_id)]
        if len(matches) == 1:
            task = matches[0]
        elif len(matches) > 1:
            print(f"❌ Ambiguous ID '{args.task_id}'. Matches: {', '.join(t.id for t in matches)}")
            return
        else:
            print(f"❌ Task '{args.task_id}' not found.")
            return

    if new_status == "done":
        mem.complete_task(task.id)
    else:
        mem.update_task(task.id, status=new_status)

    icon = STATUS_ICONS.get(new_status, "?")
    print(f"{icon} Task `{task.id}` → {new_status}: {task.title}")


def cmd_import(mem: MemoryClient, args: argparse.Namespace) -> None:
    if args.journey:
        journeys = [args.journey]
    else:
        all_t = mem.store.get_identity_by_layer("journey")
        journeys = [t.key for t in all_t]

    total = 0
    for journey in journeys:
        created = mem.import_tasks_from_journey_path(journey)
        if created:
            print(f"🧭 {journey}: {len(created)} tasks imported")
            for t in created:
                print(f"  ○ `{t.id}` {t.title}")
            total += len(created)

    if total == 0:
        print("No new tasks found in journey paths.")
    else:
        print(f"\n📋 Total: {total} tasks imported")


def cmd_sync(mem: MemoryClient, args: argparse.Namespace) -> None:
    if args.journey:
        journeys = [args.journey]
    else:
        all_t = mem.store.get_identity_by_layer("journey")
        journeys = [t.key for t in all_t if mem.get_sync_file(t.key)]

    if not journeys:
        print("No journey has sync configured.")
        return

    for journey in journeys:
        sync_file = mem.get_sync_file(journey)
        if not sync_file:
            print(f"⚠️  {journey}: no sync file configured")
            continue
        try:
            result = mem.sync_tasks_from_file(journey)
            print(f"🔄 {journey} (← {sync_file})")
            print(
                f"   +{result['created']} new | "
                f"✓{result['completed']} completed | ={result['unchanged']} unchanged"
            )
        except FileNotFoundError as e:
            print(f"❌ {journey}: {e}")
        except Exception as e:
            print(f"❌ {journey}: {e}")


def cmd_sync_config(mem: MemoryClient, args: argparse.Namespace) -> None:
    from pathlib import Path

    path = Path(args.file_path).expanduser().resolve()
    if not path.exists():
        print(f"⚠️  File not found: {path}")
        print("   Configuring it anyway; the file can be created later.")
    mem.set_sync_file(args.journey, str(path))
    print(f"🔗 {args.journey} → {path}")


def cmd_delete(mem: MemoryClient, args: argparse.Namespace) -> None:
    task = mem.store.get_task(args.task_id)
    if not task:
        all_tasks = mem.store.get_all_tasks()
        matches = [t for t in all_tasks if t.id.startswith(args.task_id)]
        if len(matches) == 1:
            task = matches[0]
        else:
            print(f"❌ Task '{args.task_id}' not found.")
            return

    mem.store.delete_task(task.id)
    print(f"🗑 Task removed: `{task.id}` - {task.title}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Task management")
    parser.add_argument("--journey", help="Filter by journey (applies to list)")
    parser.add_argument("--status", help="Filter by status (applies to list)")
    parser.add_argument(
        "--all", action="store_true", help="Include completed tasks (applies to list)"
    )
    parser.add_argument(
        "--mirror-home",
        default=None,
        help="Explicit user home whose database should be used for this command",
    )
    subparsers = parser.add_subparsers(dest="command")

    p_list = subparsers.add_parser("list")
    p_list.add_argument("--journey", help="Filter by journey")
    p_list.add_argument("--status", help="Filter by status")
    p_list.add_argument("--all", action="store_true", help="Include completed tasks")

    p_add = subparsers.add_parser("add")
    p_add.add_argument("title", help="Task title")
    p_add.add_argument("--journey", help="Journey slug")
    p_add.add_argument("--due", help="Due date (YYYY-MM-DD)")
    p_add.add_argument("--stage", help="Stage/cycle")

    p_show = subparsers.add_parser("show")
    p_show.add_argument("task_id", help="Task ID or unique ID prefix")

    p_done = subparsers.add_parser("done")
    p_done.add_argument("task_id", help="Task ID")

    p_doing = subparsers.add_parser("doing")
    p_doing.add_argument("task_id", help="Task ID")

    p_block = subparsers.add_parser("block")
    p_block.add_argument("task_id", help="Task ID")

    p_import = subparsers.add_parser("import")
    p_import.add_argument("journey", nargs="?", help="Journey slug (optional)")

    p_delete = subparsers.add_parser("delete")
    p_delete.add_argument("task_id", help="Task ID")

    p_sync = subparsers.add_parser("sync")
    p_sync.add_argument("journey", nargs="?", help="Journey slug (optional)")

    p_sync_config = subparsers.add_parser("sync-config")
    p_sync_config.add_argument("journey", help="Journey slug")
    p_sync_config.add_argument("file_path", help="Reference file path")

    args = parser.parse_args(argv)
    from memory.cli.common import db_path_from_mirror_home

    mem = MemoryClient(db_path=db_path_from_mirror_home(args.mirror_home))

    if args.command == "add":
        cmd_add(mem, args)
    elif args.command == "show":
        cmd_show(mem, args)
    elif args.command == "done":
        cmd_status_change(mem, args, "done")
    elif args.command == "doing":
        cmd_status_change(mem, args, "doing")
    elif args.command == "block":
        cmd_status_change(mem, args, "blocked")
    elif args.command == "import":
        cmd_import(mem, args)
    elif args.command == "delete":
        cmd_delete(mem, args)
    elif args.command == "sync":
        cmd_sync(mem, args)
    elif args.command == "sync-config":
        cmd_sync_config(mem, args)
    else:
        cmd_list(mem, args)


if __name__ == "__main__":
    main()
