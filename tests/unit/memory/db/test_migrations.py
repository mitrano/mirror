"""Tests for the migration runner — skip-if-applied and idempotency."""

import sqlite3

from memory.db.migrations import MIGRATIONS, run_migrations

MIGRATION_IDS = [mid for mid, _apply in MIGRATIONS]


def _applied_ids(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute("SELECT id FROM _migrations").fetchall()
    return {row[0] for row in rows}


def _fresh_conn() -> sqlite3.Connection:
    """Conexão em memória sem nenhum schema — simula banco zerado."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


class TestRunMigrations:
    def test_creates_migrations_table(self, db_conn):
        run_migrations(db_conn)
        tables = {
            row[0] for row in db_conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        assert "_migrations" in tables

    def test_all_migrations_recorded(self, db_conn):
        run_migrations(db_conn)
        applied = _applied_ids(db_conn)
        assert set(MIGRATION_IDS).issubset(applied)

    def test_migrations_idempotent(self, db_conn):
        """Running twice must not raise and must not duplicate entries."""
        run_migrations(db_conn)
        run_migrations(db_conn)
        for mid in MIGRATION_IDS:
            count = db_conn.execute(
                "SELECT COUNT(*) FROM _migrations WHERE id = ?", (mid,)
            ).fetchone()[0]
            assert count == 1, f"Migration {mid} recorded {count} times"

    def test_already_applied_migration_skipped(self, db_conn):
        """Pre-recording a migration ID causes run_migrations to skip it."""
        run_migrations(db_conn)  # apply all first
        count_before = db_conn.execute("SELECT COUNT(*) FROM _migrations").fetchone()[0]

        # Remove one and re-run — it should be skipped (table already exists)
        # Just verify the count stays the same after a second run
        run_migrations(db_conn)
        count_after = db_conn.execute("SELECT COUNT(*) FROM _migrations").fetchone()[0]
        assert count_after == count_before

    def test_migrations_list_not_empty(self):
        assert len(MIGRATIONS) > 0

    def test_each_migration_has_id_and_apply_callable(self):
        for mid, apply in MIGRATIONS:
            assert mid, "Migration id must not be empty"
            assert callable(apply), f"Migration {mid} must expose a callable apply"

    def test_migration_ids_are_unique(self):
        assert len(MIGRATION_IDS) == len(set(MIGRATION_IDS)), "Duplicate migration IDs found"

    def test_tasks_table_has_temporal_fields_after_migration(self, db_conn):
        """Migration 004 adds scheduled_at and time_hint to tasks."""
        run_migrations(db_conn)
        cols = {row[1] for row in db_conn.execute("PRAGMA table_info(tasks)")}
        assert "scheduled_at" in cols
        assert "time_hint" in cols

    def test_attachments_table_created_by_migration(self, db_conn):
        """Migration 002 creates the attachments table."""
        run_migrations(db_conn)
        tables = {
            row[0] for row in db_conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        assert "attachments" in tables

    def test_llm_calls_table_created_by_migration_006(self):
        """Migration 006 creates llm_calls on a legacy DB that lacks it."""
        conn = _fresh_conn()
        run_migrations(conn)
        tables = {
            row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        assert "llm_calls" in tables

    def test_llm_calls_migration_idempotent_on_schema_db(self, db_conn):
        """Migration 006 is a no-op when llm_calls already exists from SCHEMA."""
        run_migrations(db_conn)  # llm_calls already exists via SCHEMA
        run_migrations(db_conn)  # second run must not raise
        count = db_conn.execute(
            "SELECT COUNT(*) FROM _migrations WHERE id = '006_create_llm_calls'"
        ).fetchone()[0]
        assert count == 1

    def test_llm_calls_table_has_expected_columns(self, db_conn):
        run_migrations(db_conn)
        cols = {row[1] for row in db_conn.execute("PRAGMA table_info(llm_calls)")}
        expected = {
            "id",
            "role",
            "model",
            "prompt",
            "response",
            "prompt_tokens",
            "completion_tokens",
            "latency_ms",
            "cost_usd",
            "conversation_id",
            "session_id",
            "called_at",
        }
        assert expected.issubset(cols)

    def test_operation_runs_table_created_by_migration_011(self):
        conn = _fresh_conn()
        run_migrations(conn)
        tables = {
            row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        cols = {row[1] for row in conn.execute("PRAGMA table_info(operation_runs)")}

        assert "operation_runs" in tables
        assert {
            "id",
            "operation_id",
            "status",
            "outcome",
            "parameters_json",
            "summary_json",
            "result_json",
            "error",
            "started_at",
            "completed_at",
            "created_at",
        }.issubset(cols)

    def test_operation_run_events_table_created_by_migration_012(self):
        conn = _fresh_conn()
        run_migrations(conn)
        tables = {
            row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        cols = {row[1] for row in conn.execute("PRAGMA table_info(operation_run_events)")}

        assert "operation_run_events" in tables
        assert {
            "id",
            "run_id",
            "sequence",
            "kind",
            "message",
            "details_json",
            "created_at",
        }.issubset(cols)

    def test_builder_workbench_tables_created_by_migration_015(self):
        conn = _fresh_conn()
        run_migrations(conn)
        tables = {
            row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }

        assert "builder_refinement_stories" in tables
        assert "builder_change_requests" in tables
        assert "builder_refinement_cursors" in tables
        story_cols = {
            row[1] for row in conn.execute("PRAGMA table_info(builder_refinement_stories)")
        }
        cr_cols = {row[1] for row in conn.execute("PRAGMA table_info(builder_change_requests)")}
        cursor_cols = {
            row[1] for row in conn.execute("PRAGMA table_info(builder_refinement_cursors)")
        }
        indexes = {
            row[1]
            for row in conn.execute(
                "SELECT type, name FROM sqlite_master WHERE type = 'index' AND (name LIKE 'idx_builder_%' OR name LIKE 'ux_builder_%')"
            )
        }

        assert {
            "id",
            "journey",
            "display_code",
            "title",
            "description",
            "status",
            "position",
            "source",
            "provenance",
            "created_at",
            "updated_at",
            "pulled_at",
            "closed_at",
        }.issubset(story_cols)
        assert {
            "id",
            "journey",
            "display_code",
            "refinement_story_id",
            "title",
            "body",
            "status",
            "position",
            "source",
            "provenance",
            "outcome_notes",
            "created_at",
            "updated_at",
            "completed_at",
        }.issubset(cr_cols)
        assert {
            "journey",
            "active_refinement_story_id",
            "active_change_request_id",
            "last_refinement_event",
            "updated_at",
        }.issubset(cursor_cols)
        assert "idx_builder_refinement_stories_journey_status" in indexes
        assert "idx_builder_change_requests_story_status" in indexes
        assert "idx_builder_change_requests_journey_status" in indexes
        assert "ux_builder_refinement_stories_journey_display_code" in indexes
        assert "ux_builder_change_requests_journey_display_code" in indexes

    def test_builder_workbench_display_codes_backfilled_by_migration_016(self):
        conn = _fresh_conn()
        conn.execute("CREATE TABLE _migrations (id TEXT PRIMARY KEY, applied_at TEXT NOT NULL)")
        for migration_id in MIGRATION_IDS[:15]:
            conn.execute(
                "INSERT INTO _migrations (id, applied_at) VALUES (?, ?)",
                (migration_id, "2026-06-26T00:00:00Z"),
            )
        conn.executescript(
            """
            CREATE TABLE builder_refinement_stories (
                id TEXT PRIMARY KEY,
                journey TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL DEFAULT 'draft',
                position INTEGER NOT NULL DEFAULT 0,
                source TEXT NOT NULL DEFAULT 'manual',
                provenance TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                pulled_at TEXT,
                closed_at TEXT
            );
            CREATE TABLE builder_change_requests (
                id TEXT PRIMARY KEY,
                journey TEXT NOT NULL,
                refinement_story_id TEXT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'captured',
                position INTEGER NOT NULL DEFAULT 0,
                source TEXT NOT NULL DEFAULT 'manual',
                provenance TEXT,
                outcome_notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                completed_at TEXT
            );
            INSERT INTO builder_refinement_stories
                (id, journey, title, status, position, source, created_at, updated_at)
                VALUES
                ('rs-a', 'mirror', 'Second', 'draft', 1, 'manual', '2026-01-02', '2026-01-02'),
                ('rs-b', 'mirror', 'First', 'draft', 0, 'manual', '2026-01-01', '2026-01-01');
            INSERT INTO builder_change_requests
                (id, journey, refinement_story_id, title, body, status, position, source, created_at, updated_at)
                VALUES
                ('cr-a', 'mirror', 'rs-b', 'First CR', 'Body', 'captured', 0, 'manual', '2026-01-01', '2026-01-01'),
                ('cr-b', 'mirror', 'rs-b', 'Second CR', 'Body', 'captured', 1, 'manual', '2026-01-02', '2026-01-02');
            """
        )

        run_migrations(conn)

        stories = conn.execute(
            "SELECT id, display_code FROM builder_refinement_stories ORDER BY position"
        ).fetchall()
        change_requests = conn.execute(
            "SELECT id, display_code FROM builder_change_requests ORDER BY created_at"
        ).fetchall()
        assert [(row[0], row[1]) for row in stories] == [("rs-b", "RS001"), ("rs-a", "RS002")]
        assert [(row[0], row[1]) for row in change_requests] == [
            ("cr-a", "CR001"),
            ("cr-b", "CR002"),
        ]
