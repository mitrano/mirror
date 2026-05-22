"""Tests for runtime status CLI."""

import sqlite3
from pathlib import Path

from memory.cli.runtime import (
    CoreMigrationHealth,
    ExtensionHealth,
    GitStatus,
    RuntimeStatusReport,
    cmd_runtime,
    inspect_core_migrations,
    inspect_extension_health,
    render_runtime_status,
)
from memory.db.migrations import MIGRATIONS
from memory.extensions.migrations import run_migrations


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
        "core_migrations": CoreMigrationHealth(True, len(MIGRATIONS), len(MIGRATIONS), ()),
        "extensions": ("maestro",),
        "extension_health": (ExtensionHealth("maestro", True),),
        "python_version": "3.12.0",
        "memory_env": "production",
    }
    base.update(overrides)
    return RuntimeStatusReport(**base)


def _write_command_extension(root: Path, extension_id: str = "hello") -> Path:
    ext_dir = root / "extensions" / extension_id
    (ext_dir / "migrations").mkdir(parents=True)
    (ext_dir / "extension.py").write_text("def register(api):\n    return None\n", encoding="utf-8")
    (ext_dir / "skill.yaml").write_text(
        f"""
id: {extension_id}
name: Hello
category: extension
kind: command-skill
summary: Hello extension
entrypoint:
  module: extension
runtimes:
  pi:
    command_name: ext-{extension_id}
""".strip()
        + "\n",
        encoding="utf-8",
    )
    return ext_dir


def test_render_runtime_status_ready():
    rendered = render_runtime_status(_report())

    assert "Mirror runtime status" in rendered
    assert "Version: 0.7.0" in rendered
    assert "Repository: /repo" in rendered
    assert "Git dirty: no" in rendered
    assert f"Core migrations: current ({len(MIGRATIONS)}/{len(MIGRATIONS)})" in rendered
    assert "Installed extensions: 1 (maestro)" in rendered
    assert "Extension health: ready (1 checked)" in rendered
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
        core_migrations=CoreMigrationHealth(False, None, len(MIGRATIONS), ()),
        extensions=(),
        extension_health=(),
    )

    rendered = render_runtime_status(report)

    assert "Mirror home: not configured" in rendered
    assert "Mirror home note: Mirror home is not configured" in rendered
    assert "Database exists: unknown" in rendered
    assert "Status: attention needed" in rendered


def test_render_runtime_status_attention_needed_when_core_migrations_missing():
    report = _report(
        core_migrations=CoreMigrationHealth(
            False, len(MIGRATIONS) - 1, len(MIGRATIONS), (MIGRATIONS[-1][0],)
        )
    )

    rendered = render_runtime_status(report)

    assert "Core migrations: attention needed" in rendered
    assert MIGRATIONS[-1][0] in rendered
    assert "Status: attention needed" in rendered


def test_render_runtime_status_attention_needed_when_extension_health_fails():
    report = _report(
        extension_health=(
            ExtensionHealth(
                "hello", False, "pending migrations", pending_migrations=("001_init.sql",)
            ),
        )
    )

    rendered = render_runtime_status(report)

    assert "Extension health: attention needed (1 checked, 1 issue(s))" in rendered
    assert "hello: pending migrations; pending 001_init.sql" in rendered
    assert "Status: attention needed" in rendered


def test_inspect_core_migrations_reports_current(tmp_path):
    db_path = tmp_path / "memory.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE _migrations (id TEXT PRIMARY KEY, applied_at TEXT NOT NULL)")
        conn.executemany(
            "INSERT INTO _migrations (id, applied_at) VALUES (?, 'now')",
            [(migration_id,) for migration_id, _ in MIGRATIONS],
        )

    health = inspect_core_migrations(db_path, True)

    assert health.ready is True
    assert health.applied_count == len(MIGRATIONS)
    assert health.missing == ()


def test_inspect_core_migrations_reports_missing_without_mutating(tmp_path):
    db_path = tmp_path / "memory.db"

    health = inspect_core_migrations(db_path, False)

    assert health.ready is False
    assert health.note == "database missing"
    assert not db_path.exists()


def test_inspect_core_migrations_reports_missing_ids(tmp_path):
    db_path = tmp_path / "memory.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE _migrations (id TEXT PRIMARY KEY, applied_at TEXT NOT NULL)")
        conn.executemany(
            "INSERT INTO _migrations (id, applied_at) VALUES (?, 'now')",
            [(migration_id,) for migration_id, _ in MIGRATIONS[:-1]],
        )

    health = inspect_core_migrations(db_path, True)

    assert health.ready is False
    assert health.missing == (MIGRATIONS[-1][0],)


def test_inspect_extension_health_reports_prompt_skill_ready(tmp_path):
    ext_dir = tmp_path / "extensions" / "prompt"
    ext_dir.mkdir(parents=True)
    (ext_dir / "SKILL.md").write_text("# Prompt\n", encoding="utf-8")
    (ext_dir / "skill.yaml").write_text(
        """
id: prompt
name: Prompt
category: extension
kind: prompt-skill
summary: Prompt extension
runtimes:
  pi:
    command_name: ext-prompt
    skill_file: SKILL.md
""".strip()
        + "\n",
        encoding="utf-8",
    )
    db_path = tmp_path / "memory.db"
    db_path.touch()

    health = inspect_extension_health(tmp_path, db_path, True)

    assert health == (ExtensionHealth("prompt", True),)


def test_inspect_extension_health_reports_invalid_manifest(tmp_path):
    ext_dir = tmp_path / "extensions" / "broken"
    ext_dir.mkdir(parents=True)
    (ext_dir / "skill.yaml").write_text("id: broken\n", encoding="utf-8")
    db_path = tmp_path / "memory.db"
    db_path.touch()

    health = inspect_extension_health(tmp_path, db_path, True)

    assert len(health) == 1
    assert health[0].extension_id == "broken"
    assert health[0].ready is False
    assert "missing required field" in (health[0].note or "")


def test_inspect_extension_health_reports_pending_command_migration(tmp_path):
    ext_dir = _write_command_extension(tmp_path)
    (ext_dir / "migrations" / "001_init.sql").write_text(
        "CREATE TABLE ext_hello_pings (id INTEGER PRIMARY KEY);\n", encoding="utf-8"
    )
    db_path = tmp_path / "memory.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "CREATE TABLE _ext_migrations (extension_id TEXT, filename TEXT, checksum TEXT, applied_at TEXT, PRIMARY KEY (extension_id, filename))"
        )

    health = inspect_extension_health(tmp_path, db_path, True)

    assert health == (
        ExtensionHealth("hello", False, "pending migrations", pending_migrations=("001_init.sql",)),
    )


def test_inspect_extension_health_reports_checksum_drift(tmp_path):
    ext_dir = _write_command_extension(tmp_path)
    migration = ext_dir / "migrations" / "001_init.sql"
    migration.write_text(
        "CREATE TABLE ext_hello_pings (id INTEGER PRIMARY KEY);\n", encoding="utf-8"
    )
    db_path = tmp_path / "memory.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "CREATE TABLE _ext_migrations (extension_id TEXT, filename TEXT, checksum TEXT, applied_at TEXT, PRIMARY KEY (extension_id, filename))"
        )
        run_migrations(conn, extension_id="hello", migrations_dir=ext_dir / "migrations")
    migration.write_text(
        "CREATE TABLE ext_hello_pings (id INTEGER PRIMARY KEY, title TEXT);\n",
        encoding="utf-8",
    )

    health = inspect_extension_health(tmp_path, db_path, True)

    assert health == (
        ExtensionHealth(
            "hello", False, "migration checksum drift", drifted_migrations=("001_init.sql",)
        ),
    )


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
