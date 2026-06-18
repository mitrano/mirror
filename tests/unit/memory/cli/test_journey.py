"""Tests for journey CLI behavior."""

import pytest

from memory import MemoryClient
from memory.config import default_db_path_for_home

JOURNEY_CONTENT = """# Mirror POC
**Status:** active

## Description

Scoped journey description.
"""


def test_journey_status_reads_from_explicit_mirror_home(tmp_path, capsys):
    mirror_home = tmp_path / ".mirror" / "pati"
    db_path = default_db_path_for_home(mirror_home)
    mem = MemoryClient(env="test", db_path=db_path)
    mem.set_identity("journey", "mirror-poc", JOURNEY_CONTENT)
    mem.set_journey_path("mirror-poc", "# Journey path")
    mem.add_message(
        mem.start_conversation("cli", journey="mirror-poc", title="Scoped conversation").id,
        "user",
        "hello",
    )

    from memory.cli.journey import main

    main(["status", "mirror-poc", "--mirror-home", str(mirror_home)])

    captured = capsys.readouterr()
    assert "=== journey: mirror-poc ===" in captured.out
    assert "Scoped journey description." in captured.out
    assert "Scoped conversation" in captured.out


def test_journey_set_path_uses_journey_service(tmp_path, capsys):
    mirror_home = tmp_path / ".mirror" / "pati"
    db_path = default_db_path_for_home(mirror_home)
    mem = MemoryClient(env="test", db_path=db_path)
    mem.set_identity("journey", "mirror-poc", JOURNEY_CONTENT)
    project_path = tmp_path / "project"

    from memory.cli.journey import main

    main(["set-path", "mirror-poc", str(project_path), "--mirror-home", str(mirror_home)])

    captured = capsys.readouterr()
    assert "project_path set" in captured.err
    assert captured.out.strip() == str(project_path.resolve())
    assert mem.journeys.get_project_path("mirror-poc") == str(project_path.resolve())


def test_journey_create_with_fields_writes_journey_identity(tmp_path, capsys):
    mirror_home = tmp_path / ".mirror" / "pati"
    db_path = default_db_path_for_home(mirror_home)
    mem = MemoryClient(env="test", db_path=db_path)

    from memory.cli.journey import main

    main(
        [
            "create",
            "learning-ai",
            "--name",
            "Learning AI",
            "--description",
            "Track AI learning.",
            "--briefing",
            "Use for AI study conversations.",
            "--context",
            "Current focus: agents.",
            "--mirror-home",
            str(mirror_home),
        ]
    )

    captured = capsys.readouterr()
    assert "journey/learning-ai created" in captured.out
    entry = mem.store.get_identity("journey", "learning-ai")
    assert entry is not None
    assert "# Learning AI" in entry.content
    assert "**Status:** active" in entry.content
    assert "Track AI learning." in entry.content
    assert "Use for AI study conversations." in entry.content
    assert "Current focus: agents." in entry.content


def test_journey_create_prompts_for_missing_fields(mocker, tmp_path, capsys):
    mirror_home = tmp_path / ".mirror" / "pati"
    db_path = default_db_path_for_home(mirror_home)
    mem = MemoryClient(env="test", db_path=db_path)
    mocker.patch(
        "builtins.input",
        side_effect=[
            "health",
            "Health",
            "Track health and training.",
            "Use for health choices.",
            "Started in May.",
        ],
    )

    from memory.cli.journey import main

    main(["create", "--mirror-home", str(mirror_home)])

    captured = capsys.readouterr()
    assert "journey/health created" in captured.out
    entry = mem.store.get_identity("journey", "health")
    assert entry is not None
    assert "# Health" in entry.content
    assert "Track health and training." in entry.content


def test_journey_create_refuses_to_overwrite_existing_journey(tmp_path, capsys):
    mirror_home = tmp_path / ".mirror" / "pati"
    db_path = default_db_path_for_home(mirror_home)
    mem = MemoryClient(env="test", db_path=db_path)
    mem.set_identity("journey", "mirror-poc", JOURNEY_CONTENT)

    from memory.cli.journey import main

    with pytest.raises(SystemExit):
        main(
            [
                "create",
                "mirror-poc",
                "--name",
                "Mirror POC",
                "--description",
                "New description.",
                "--mirror-home",
                str(mirror_home),
            ]
        )

    captured = capsys.readouterr()
    assert "already exists" in captured.err
    assert mem.store.get_identity("journey", "mirror-poc").content == JOURNEY_CONTENT


def test_journey_update_explicit_mirror_home_overrides_environment_selection(
    mocker, tmp_path, capsys
):
    env_home = tmp_path / ".mirror" / "testuser"
    env_db_path = default_db_path_for_home(env_home)
    env_mem = MemoryClient(env="test", db_path=env_db_path)
    env_mem.set_identity("journey", "mirror-poc", JOURNEY_CONTENT)

    explicit_home = tmp_path / ".mirror" / "pati"
    explicit_db_path = default_db_path_for_home(explicit_home)
    explicit_mem = MemoryClient(env="test", db_path=explicit_db_path)
    explicit_mem.set_identity("journey", "mirror-poc", JOURNEY_CONTENT)

    mocker.patch.dict("os.environ", {"MIRROR_HOME": str(env_home)}, clear=False)

    from memory.cli.journey import main

    main(["update", "mirror-poc", "# Explicit path", "--mirror-home", str(explicit_home)])

    captured = capsys.readouterr()
    assert "updated" in captured.err
    assert explicit_mem.get_journey_path("mirror-poc") == "# Explicit path"
    assert env_mem.get_journey_path("mirror-poc") is None
