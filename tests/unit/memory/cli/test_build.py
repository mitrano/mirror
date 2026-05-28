"""Tests for Builder Mode CLI context loader."""

from pathlib import Path

import pytest

from memory import MemoryClient
from memory.cli import build
from memory.cli.runtime import CloneRole
from memory.config import default_db_path_for_home

JOURNEY_CONTENT = """# Mirror POC
**Status:** active

## Description

Scoped journey description.
"""


def test_build_load_reads_project_path_from_journey_service(mocker, tmp_path, capsys):
    mirror_home = tmp_path / ".mirror" / "pati"
    db_path = default_db_path_for_home(mirror_home)
    mem = MemoryClient(env="test", db_path=db_path)
    mem.set_identity("journey", "mirror-poc", JOURNEY_CONTENT)
    project_path = tmp_path / "project"
    mem.journeys.set_project_path("mirror-poc", str(project_path))

    mocker.patch("memory.cli.build.MemoryClient", return_value=mem)
    mocker.patch("memory.cli.build.switch_conversation")
    mocker.patch("memory.cli.build._persist_global_sticky_defaults")
    inspect = mocker.patch(
        "memory.cli.build.inspect_clone_role",
        return_value=CloneRole("dev", Path("/repo/.mirror-clone-role")),
    )
    mocker.patch.object(mem, "load_mirror_context", return_value="context")
    mocker.patch.object(mem, "search", return_value=[])

    build.cmd_load("mirror-poc")

    captured = capsys.readouterr()
    assert f"project_path={project_path.resolve()}" in captured.out
    inspect.assert_called_once_with(project_path.resolve())


def test_build_load_refuses_when_journey_project_path_is_production_clone(mocker, tmp_path, capsys):
    mirror_home = tmp_path / ".mirror" / "pati"
    db_path = default_db_path_for_home(mirror_home)
    mem = MemoryClient(env="test", db_path=db_path)
    mem.set_identity("journey", "mirror-poc", JOURNEY_CONTENT)
    project_path = tmp_path / "production-project"
    mem.journeys.set_project_path("mirror-poc", str(project_path))

    mocker.patch("memory.cli.build.MemoryClient", return_value=mem)
    inspect = mocker.patch(
        "memory.cli.build.inspect_clone_role",
        return_value=CloneRole("production", Path("/repo/.mirror-clone-role")),
    )

    with pytest.raises(SystemExit) as exc:
        build.cmd_load("mirror-poc")

    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert "Builder Mode refused" in err
    assert "Project path:" in err
    assert "--ignore-production-role" in err
    inspect.assert_called_once_with(project_path.resolve())


def test_build_load_allows_production_clone_when_override_passed(mocker, tmp_path, capsys):
    mirror_home = tmp_path / ".mirror" / "pati"
    db_path = default_db_path_for_home(mirror_home)
    mem = MemoryClient(env="test", db_path=db_path)
    mem.set_identity("journey", "mirror-poc", JOURNEY_CONTENT)

    mocker.patch("memory.cli.build.MemoryClient", return_value=mem)
    mocker.patch("memory.cli.build.switch_conversation")
    mocker.patch("memory.cli.build._persist_global_sticky_defaults")
    mocker.patch(
        "memory.cli.build.inspect_clone_role",
        return_value=CloneRole("production", Path("/repo/.mirror-clone-role")),
    )
    mocker.patch.object(mem, "load_mirror_context", return_value="context")
    mocker.patch.object(mem, "search", return_value=[])

    build.cmd_load("mirror-poc", ignore_production_role=True)

    err = capsys.readouterr().err
    assert "Production clone override" in err
