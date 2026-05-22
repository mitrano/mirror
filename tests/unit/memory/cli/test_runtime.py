"""Tests for runtime status CLI."""

from pathlib import Path

from memory.cli.runtime import GitStatus, RuntimeStatusReport, cmd_runtime, render_runtime_status


def _report(**overrides) -> RuntimeStatusReport:
    base = {
        "version": "0.7.0",
        "git": GitStatus(
            repository=Path("/repo"),
            branch="main",
            commit="abc1234",
            dirty=False,
        ),
        "mirror_home": Path("/home/.mirror-minds/alisson"),
        "mirror_home_error": None,
        "db_path": Path("/home/.mirror-minds/alisson/memory.db"),
        "db_exists": True,
        "extensions": ("maestro",),
        "python_version": "3.12.0",
        "memory_env": "production",
    }
    base.update(overrides)
    return RuntimeStatusReport(**base)


def test_render_runtime_status_ready():
    rendered = render_runtime_status(_report())

    assert "Mirror runtime status" in rendered
    assert "Version: 0.7.0" in rendered
    assert "Repository: /repo" in rendered
    assert "Git dirty: no" in rendered
    assert "Installed extensions: 1 (maestro)" in rendered
    assert "Status: ready" in rendered


def test_render_runtime_status_attention_needed_when_git_dirty():
    report = _report(git=GitStatus(Path("/repo"), "main", "abc1234", True))

    rendered = render_runtime_status(report)

    assert "Git dirty: yes" in rendered
    assert "Status: attention needed" in rendered


def test_render_runtime_status_attention_needed_when_mirror_home_missing():
    report = _report(
        mirror_home=None,
        mirror_home_error="Mirror home is not configured. Set MIRROR_HOME or MIRROR_USER.",
        db_path=None,
        db_exists=None,
        extensions=(),
    )

    rendered = render_runtime_status(report)

    assert "Mirror home: not configured" in rendered
    assert "Mirror home note: Mirror home is not configured" in rendered
    assert "Database exists: unknown" in rendered
    assert "Status: attention needed" in rendered


def test_cmd_runtime_status_dispatches(monkeypatch, capsys):
    monkeypatch.setattr(
        "memory.cli.runtime.build_runtime_status", lambda mirror_home_arg=None: _report()
    )

    rc = cmd_runtime(["status"])

    out = capsys.readouterr().out
    assert rc == 0
    assert "Mirror runtime status" in out
    assert "Status: ready" in out


def test_cmd_runtime_status_returns_nonzero_when_attention_needed(monkeypatch, capsys):
    monkeypatch.setattr(
        "memory.cli.runtime.build_runtime_status",
        lambda mirror_home_arg=None: _report(git=GitStatus(Path("/repo"), "main", "abc1234", True)),
    )

    rc = cmd_runtime(["status"])

    out = capsys.readouterr().out
    assert rc == 1
    assert "Status: attention needed" in out
