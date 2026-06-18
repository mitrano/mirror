"""Tests for task management CLI behavior."""

from memory import MemoryClient
from memory.config import default_db_path_for_home


def test_tasks_list_reads_from_explicit_mirror_home(tmp_path, capsys):
    mirror_home = tmp_path / ".mirror" / "pati"
    db_path = default_db_path_for_home(mirror_home)
    mem = MemoryClient(env="test", db_path=db_path)
    mem.add_task(title="Scoped task", journey="mirror-poc")

    from memory.cli.tasks_cmd import main

    main(["--mirror-home", str(mirror_home), "list"])

    captured = capsys.readouterr()
    assert "Scoped task" in captured.out
    assert "mirror-poc" in captured.out


def test_tasks_add_explicit_mirror_home_overrides_environment_selection(mocker, tmp_path, capsys):
    env_home = tmp_path / ".mirror" / "testuser"
    explicit_home = tmp_path / ".mirror" / "pati"
    mocker.patch.dict("os.environ", {"MIRROR_HOME": str(env_home)}, clear=False)

    from memory.cli.tasks_cmd import main

    main(["--mirror-home", str(explicit_home), "add", "Explicit task", "--journey", "mirror-poc"])

    captured = capsys.readouterr()
    assert "Task created" in captured.out

    env_mem = MemoryClient(env="test", db_path=default_db_path_for_home(env_home))
    explicit_mem = MemoryClient(env="test", db_path=default_db_path_for_home(explicit_home))
    assert env_mem.list_tasks() == []
    explicit_tasks = explicit_mem.list_tasks()
    assert len(explicit_tasks) == 1
    assert explicit_tasks[0].title == "Explicit task"


def test_tasks_show_prints_full_friendly_task_details(tmp_path, capsys):
    mirror_home = tmp_path / ".mirror" / "pati"
    db_path = default_db_path_for_home(mirror_home)
    mem = MemoryClient(env="test", db_path=db_path)
    task = mem.add_task(
        title="Melhorar cooldown do Gemini",
        journey="proj-anota",
        due_date="2026-05-23",
        stage="Fallback de transcrição",
        context="Objetivo: evitar tentativas repetidas contra Gemini após quota.",
        source="conversation",
    )
    mem.update_task(task.id, scheduled_at="2026-05-23T09:00", time_hint="manhã")

    from memory.cli.tasks_cmd import main

    main(["--mirror-home", str(mirror_home), "show", task.id[:8]])

    captured = capsys.readouterr()
    assert "📋 Tarefa" in captured.out
    assert "Melhorar cooldown do Gemini" in captured.out
    assert f"ID: `{task.id}`" in captured.out
    assert "Jornada: `proj-anota`" in captured.out
    assert "Status: ○ todo" in captured.out
    assert "Etapa: Fallback de transcrição" in captured.out
    assert "Prazo: 2026-05-23" in captured.out
    assert "Horário agendado: 2026-05-23T09:00" in captured.out
    assert "Dica de horário: manhã" in captured.out
    assert "Origem: conversation" in captured.out
    assert "Objetivo: evitar tentativas repetidas" in captured.out


def test_tasks_show_reports_ambiguous_prefix(tmp_path, capsys):
    mirror_home = tmp_path / ".mirror" / "pati"
    db_path = default_db_path_for_home(mirror_home)
    mem = MemoryClient(env="test", db_path=db_path)
    task_a = mem.add_task(title="Alpha", journey="proj-anota")
    task_b = mem.add_task(title="Beta", journey="proj-anota")
    mem.store.update_task(task_a.id, id="same-prefix-a")
    mem.store.update_task(task_b.id, id="same-prefix-b")

    from memory.cli.tasks_cmd import main

    main(["--mirror-home", str(mirror_home), "show", "same"])

    captured = capsys.readouterr()
    assert "Ambiguous ID" in captured.out
    assert "same-prefix-a" in captured.out
    assert "same-prefix-b" in captured.out
