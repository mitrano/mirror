"""Allowlisted operation catalog for the local web console."""

from __future__ import annotations

import math
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from memory.cli.backup import backup as create_backup
from memory.cli.common import db_path_from_mirror_home
from memory.cli.conversation_logger import diagnose_journey_associations
from memory.cli.runtime import RuntimeStatusReport, build_runtime_status, verify_backup_archive
from memory.client import MemoryClient
from memory.web.agent_prototype import run_agent_prototype
from memory.web.command_executor import ControlledCommand, run_controlled_command

ParameterType = Literal["string", "integer", "boolean", "choice"]
RiskLevel = Literal["read_only", "writes_backup", "writes_database", "external_llm"]
DryRunMode = Literal["unsupported", "supported", "required"]
ExecutionState = Literal["catalog_only", "future", "runnable"]


@dataclass(frozen=True)
class OperationParameter:
    """Declarative metadata for a safe operation parameter."""

    name: str
    label: str
    kind: ParameterType
    description: str
    required: bool = False
    default: str | int | bool | None = None
    choices: tuple[str, ...] = ()
    minimum: int | None = None
    maximum: int | None = None

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "name": self.name,
            "label": self.label,
            "kind": self.kind,
            "description": self.description,
            "required": self.required,
        }
        if self.default is not None:
            payload["default"] = self.default
        if self.choices:
            payload["choices"] = list(self.choices)
        if self.minimum is not None:
            payload["minimum"] = self.minimum
        if self.maximum is not None:
            payload["maximum"] = self.maximum
        return payload


@dataclass(frozen=True)
class WebOperation:
    """Server-owned definition for one allowlisted web operation."""

    id: str
    title: str
    description: str
    category: str
    risk_level: RiskLevel
    dry_run: DryRunMode
    execution: ExecutionState = "catalog_only"
    parameters: tuple[OperationParameter, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "riskLevel": self.risk_level,
            "dryRun": self.dry_run,
            "execution": self.execution,
            "parameters": [parameter.to_dict() for parameter in self.parameters],
        }


OPERATION_CATALOG: tuple[WebOperation, ...] = (
    WebOperation(
        id="runtime-health",
        title="Runtime health diagnosis",
        description="Inspect runtime version, database path, migration state, extension health, and configuration warnings without changing local state.",
        category="runtime",
        risk_level="read_only",
        dry_run="unsupported",
        execution="runnable",
    ),
    WebOperation(
        id="runtime-diagnose",
        title="Runtime diagnosis",
        description="Run the read-only runtime diagnosis command for the active Mirror and capture command evidence without exposing shell access.",
        category="runtime",
        risk_level="read_only",
        dry_run="unsupported",
        execution="runnable",
    ),
    WebOperation(
        id="database-backup",
        title="Database backup",
        description="Create and optionally verify a local backup archive for the active Mirror database before risky maintenance.",
        category="safety",
        risk_level="writes_backup",
        dry_run="unsupported",
        execution="runnable",
        parameters=(
            OperationParameter(
                name="verify",
                label="Verify backup",
                kind="boolean",
                description="Verify the created archive after backup completes.",
                default=True,
            ),
        ),
    ),
    WebOperation(
        id="conversation-journey-repair",
        title="Conversation journey repair",
        description="Find conversations missing journey association and repair them only after an explicit preview.",
        category="conversations",
        risk_level="writes_database",
        dry_run="required",
        execution="runnable",
        parameters=(
            OperationParameter(
                name="dryRun",
                label="Dry run",
                kind="boolean",
                description="Preview repair candidates without changing conversations.",
                default=True,
            ),
            OperationParameter(
                name="limit",
                label="Maximum conversations",
                kind="integer",
                description="Maximum number of conversations to inspect or repair in one run.",
                default=50,
                minimum=1,
                maximum=500,
            ),
        ),
    ),
    WebOperation(
        id="run-console-demo",
        title="Run console demo",
        description="Simulate a slow read-only operation that emits progress events so the run console can be validated in real time.",
        category="diagnostics",
        risk_level="read_only",
        dry_run="unsupported",
        execution="runnable",
        parameters=(
            OperationParameter(
                name="steps",
                label="Steps",
                kind="integer",
                description="Number of progress steps to emit.",
                default=5,
                minimum=1,
                maximum=12,
            ),
        ),
    ),
    WebOperation(
        id="agent-run-prototype",
        title="Agent run prototype",
        description="Launch a bounded read-only agent-shaped run from an intent and return a proposal through the async evidence model.",
        category="agent",
        risk_level="read_only",
        dry_run="unsupported",
        execution="runnable",
        parameters=(
            OperationParameter(
                name="intent",
                label="Intent",
                kind="string",
                description="Natural-language intent for the bounded read-only prototype.",
                required=True,
            ),
        ),
    ),
    WebOperation(
        id="batch-conversation-retitle",
        title="Batch conversation retitle",
        description="Suggest improved titles for older conversations using an LLM, with limits, preview, and approval before database writes.",
        category="conversations",
        risk_level="external_llm",
        dry_run="required",
        execution="runnable",
        parameters=(
            OperationParameter(
                name="dryRun",
                label="Dry run",
                kind="boolean",
                description="Preview retitle candidates and estimated cost without LLM calls or database writes.",
                default=True,
            ),
            OperationParameter(
                name="limit",
                label="Maximum conversations",
                kind="integer",
                description="Maximum number of conversations to consider in one batch.",
                default=10,
                minimum=1,
                maximum=100,
            ),
            OperationParameter(
                name="journey",
                label="Journey filter",
                kind="string",
                description="Optional journey id or slug used to limit the batch.",
                required=False,
            ),
        ),
    ),
)


def operation_catalog() -> list[dict[str, object]]:
    """Return the serialized server-owned operation catalog."""

    return [operation.to_dict() for operation in OPERATION_CATALOG]


def validate_operation_request(
    operation_id: str, parameters: dict[str, object] | None = None
) -> dict[str, object]:
    """Validate one operation request and return parsed parameters."""

    operation = _operation_by_id(operation_id)
    if operation is None:
        raise ValueError(f"Unknown operation: {operation_id}")
    if operation.execution != "runnable":
        raise ValueError(f"Operation is not runnable yet: {operation_id}")
    return _validate_parameters(operation, parameters or {})


def run_operation(
    operation_id: str,
    *,
    mirror_home: Path | None = None,
    start: Path | None = None,
    parameters: dict[str, object] | None = None,
    emit_event: Callable[[str, str, dict[str, object] | None], None] | None = None,
) -> dict[str, object]:
    """Run one implemented allowlisted operation and return web-safe results."""

    parsed_parameters = validate_operation_request(operation_id, parameters)
    operation = _operation_by_id(operation_id)
    if operation is None:
        raise ValueError(f"Unknown operation: {operation_id}")
    if operation.id == "runtime-health":
        return _run_runtime_health(mirror_home=mirror_home, start=start)
    if operation.id == "runtime-diagnose":
        return _run_runtime_diagnose(mirror_home=mirror_home, start=start)
    if operation.id == "database-backup":
        return _run_database_backup(mirror_home=mirror_home, parameters=parsed_parameters)
    if operation.id == "conversation-journey-repair":
        return _run_conversation_journey_repair(
            mirror_home=mirror_home, parameters=parsed_parameters
        )
    if operation.id == "batch-conversation-retitle":
        return _run_batch_conversation_retitle(
            mirror_home=mirror_home,
            parameters=parsed_parameters,
            emit_event=emit_event,
        )
    if operation.id == "run-console-demo":
        return _run_console_demo(parameters=parsed_parameters, emit_event=emit_event)
    if operation.id == "agent-run-prototype":
        return _run_agent_run_prototype(mirror_home=mirror_home, parameters=parsed_parameters)
    raise ValueError(f"Operation is not implemented yet: {operation_id}")


def _operation_by_id(operation_id: str) -> WebOperation | None:
    return next(
        (operation for operation in OPERATION_CATALOG if operation.id == operation_id), None
    )


def _validate_parameters(
    operation: WebOperation, parameters: dict[str, object]
) -> dict[str, object]:
    allowed = {parameter.name: parameter for parameter in operation.parameters}
    extra = set(parameters) - set(allowed)
    if extra:
        raise ValueError(f"Unsupported parameters for {operation.id}: {', '.join(sorted(extra))}")

    parsed: dict[str, object] = {}
    for name, parameter in allowed.items():
        value = parameters.get(name, parameter.default)
        if value is None:
            if parameter.required:
                raise ValueError(f"Parameter is required for {operation.id}: {name}")
            continue
        if parameter.kind == "boolean" and not isinstance(value, bool):
            raise ValueError(f"Parameter must be a boolean for {operation.id}: {name}")
        if parameter.kind == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
            raise ValueError(f"Parameter must be an integer for {operation.id}: {name}")
        if parameter.kind == "string" and not isinstance(value, str):
            raise ValueError(f"Parameter must be a string for {operation.id}: {name}")
        if parameter.kind == "choice" and value not in parameter.choices:
            raise ValueError(
                f"Parameter must be one of the allowed choices for {operation.id}: {name}"
            )
        if isinstance(value, int):
            if parameter.minimum is not None and value < parameter.minimum:
                raise ValueError(f"Parameter is below minimum for {operation.id}: {name}")
            if parameter.maximum is not None and value > parameter.maximum:
                raise ValueError(f"Parameter is above maximum for {operation.id}: {name}")
        parsed[name] = value
    return parsed


def _run_runtime_health(*, mirror_home: Path | None, start: Path | None) -> dict[str, object]:
    report = build_runtime_status(start=start, mirror_home_arg=mirror_home)
    return {
        "operationId": "runtime-health",
        "status": "completed",
        "outcome": report.status,
        "summary": _runtime_health_summary(report),
        "result": _runtime_status_payload(report),
    }


def _run_runtime_diagnose(*, mirror_home: Path | None, start: Path | None) -> dict[str, object]:
    argv = [sys.executable, "-m", "memory", "runtime", "diagnose"]
    if mirror_home is not None:
        argv.extend(["--mirror-home", str(mirror_home)])
    command = ControlledCommand(
        id="runtime-diagnose",
        argv=tuple(argv),
        cwd=start or Path.cwd(),
        timeout_seconds=30,
    )
    result = run_controlled_command(command)
    outcome = "ready" if result.succeeded else "attention needed"
    summary = [
        f"Command exit: {result.return_code if result.return_code is not None else 'timeout'}",
        "Runtime diagnosis command completed."
        if not result.timed_out
        else "Runtime diagnosis timed out.",
    ]
    return {
        "operationId": "runtime-diagnose",
        "status": "completed",
        "outcome": outcome,
        "summary": summary,
        "result": {"command": result.to_dict()},
    }


def _run_database_backup(
    *, mirror_home: Path | None, parameters: dict[str, object]
) -> dict[str, object]:
    if mirror_home is None:
        raise ValueError("Mirror home is required for database backup")
    backup_path = create_backup(silent=True, mirror_home=mirror_home)
    if backup_path is None:
        raise ValueError(f"Database not found for Mirror home: {mirror_home}")

    verify = parameters.get("verify", True)
    verification = verify_backup_archive(backup_path) if verify else None
    result: dict[str, object] = {
        "backupPath": str(backup_path),
        "recoveryRoute": [
            "Stop active runtime sessions that could write to the database.",
            "Move current memory.db, memory.db-wal, and memory.db-shm aside.",
            "Extract memory.db and sidecars from this backup into the Mirror home.",
            "Run runtime status against the Mirror home.",
            "Do not retry risky operations until status is ready.",
        ],
    }
    summary = [f"Backup created: {backup_path}"]
    if verification is not None:
        result["verification"] = {
            "valid": verification.valid,
            "entries": list(verification.entries),
            "note": verification.note,
        }
        summary.append(f"Verification result: {'valid' if verification.valid else 'invalid'}")
    else:
        result["verification"] = None
        summary.append("Verification skipped")

    return {
        "operationId": "database-backup",
        "status": "completed",
        "outcome": "backup_created",
        "summary": summary,
        "result": result,
    }


def _run_conversation_journey_repair(
    *, mirror_home: Path | None, parameters: dict[str, object]
) -> dict[str, object]:
    if mirror_home is None:
        raise ValueError("Mirror home is required for conversation journey repair")

    dry_run = bool(parameters.get("dryRun", True))
    limit = parameters.get("limit")
    findings = diagnose_journey_associations(
        mirror_home=mirror_home,
        apply=False,
        limit=int(limit) if limit is not None else None,
    )
    candidates = [_repair_candidate_payload(finding) for finding in findings]
    result: dict[str, object] = {
        "candidateCount": len(candidates),
        "appliedCount": 0,
        "candidates": candidates,
        "backupPath": None,
    }

    if dry_run or not candidates:
        outcome = "dry_run" if dry_run else "no_candidates"
        return {
            "operationId": "conversation-journey-repair",
            "status": "completed",
            "outcome": outcome,
            "summary": [f"Repair candidates: {len(candidates)}", "No conversations changed."],
            "result": result,
        }

    backup_path = create_backup(silent=True, mirror_home=mirror_home)
    if backup_path is None:
        raise ValueError("Database backup failed; refusing to repair conversations")

    with MemoryClient(db_path=db_path_from_mirror_home(mirror_home)) as mem:
        for candidate in candidates:
            mem.store.update_conversation(
                str(candidate["conversationId"]), journey=str(candidate["journey"])
            )

    result["appliedCount"] = len(candidates)
    result["backupPath"] = str(backup_path)
    return {
        "operationId": "conversation-journey-repair",
        "status": "completed",
        "outcome": "repaired",
        "summary": [
            f"Repair candidates: {len(candidates)}",
            f"Repaired conversations: {len(candidates)}",
            f"Backup created: {backup_path}",
        ],
        "result": result,
    }


def _run_batch_conversation_retitle(
    *,
    mirror_home: Path | None,
    parameters: dict[str, object],
    emit_event: Callable[[str, str, dict[str, object] | None], None] | None,
) -> dict[str, object]:
    if mirror_home is None:
        raise ValueError("Mirror home is required for batch conversation retitle")

    dry_run = bool(parameters.get("dryRun", True))
    limit = int(parameters.get("limit", 10))
    journey = str(parameters["journey"]).strip() if parameters.get("journey") else None
    candidates, total_candidates = _conversation_retitle_candidates(
        mirror_home=mirror_home,
        limit=limit,
        journey=journey,
    )
    estimate = _retitle_cost_estimate(candidates)
    result: dict[str, object] = {
        "candidateCount": len(candidates),
        "totalCandidateCount": total_candidates,
        "remainingAfterBatch": max(total_candidates - len(candidates), 0),
        "appliedCount": 0,
        "candidates": candidates,
        "estimate": estimate,
        "backupPath": None,
    }

    if dry_run or not candidates:
        outcome = "dry_run" if dry_run else "no_candidates"
        return {
            "operationId": "batch-conversation-retitle",
            "status": "completed",
            "outcome": outcome,
            "summary": [
                f"Retitle candidates in this batch: {len(candidates)}",
                f"Total candidates remaining before this run: {total_candidates}",
                f"Estimated remaining after this batch: {max(total_candidates - len(candidates), 0)}",
                f"Estimated input tokens: {estimate['estimatedInputTokens']}",
                f"Estimated cost: ${estimate['estimatedCostUsd']:.4f}",
                "No conversations changed.",
            ],
            "result": result,
        }

    if emit_event is not None:
        emit_event(
            "progress",
            f"Preparing to retitle {len(candidates)} conversation(s).",
            {"candidateCount": len(candidates), "estimatedCostUsd": estimate["estimatedCostUsd"]},
        )

    backup_path = create_backup(silent=True, mirror_home=mirror_home)
    if backup_path is None:
        raise ValueError("Database backup failed; refusing to retitle conversations")

    if emit_event is not None:
        emit_event("progress", f"Backup created: {backup_path}", {"backupPath": str(backup_path)})

    applied = 0
    with MemoryClient(db_path=db_path_from_mirror_home(mirror_home)) as mem:
        for index, candidate in enumerate(candidates, start=1):
            before = mem.store.get_conversation(str(candidate["conversationId"]))
            if before is None:
                continue
            updated = mem.conversations.maybe_generate_title(
                before.id,
                source="batch_retitle",
            )
            if updated is not None and updated.title != before.title:
                candidate["newTitle"] = updated.title
                applied += 1
                if emit_event is not None:
                    emit_event(
                        "progress",
                        f"Generated title {index}/{len(candidates)}: {updated.title}",
                        {
                            "conversationId": before.id,
                            "index": index,
                            "total": len(candidates),
                            "oldTitle": before.title,
                            "newTitle": updated.title,
                        },
                    )
            elif emit_event is not None:
                emit_event(
                    "progress",
                    f"No replacement title generated for {before.id[:8]}.",
                    {
                        "conversationId": before.id,
                        "index": index,
                        "total": len(candidates),
                        "oldTitle": before.title,
                    },
                )

    result["appliedCount"] = applied
    result["backupPath"] = str(backup_path)
    return {
        "operationId": "batch-conversation-retitle",
        "status": "completed",
        "outcome": "retitled",
        "summary": [
            f"Retitle candidates in this batch: {len(candidates)}",
            f"Total candidates remaining before this run: {total_candidates}",
            f"Estimated remaining after this batch: {max(total_candidates - applied, 0)}",
            f"Retitled conversations: {applied}",
            f"Backup created: {backup_path}",
        ],
        "result": result,
    }


def _conversation_retitle_candidates(
    *, mirror_home: Path, limit: int, journey: str | None
) -> tuple[list[dict[str, object]], int]:
    candidates: list[dict[str, object]] = []
    total_candidates = 0
    with MemoryClient(db_path=db_path_from_mirror_home(mirror_home)) as mem:
        conditions = ["1=1"]
        params: list[object] = []
        if journey:
            conditions.append("c.journey = ?")
            params.append(journey)
        rows = mem.store.conn.execute(
            f"""
            SELECT c.id, c.title, c.started_at, c.journey,
                   COUNT(m.id) AS message_count,
                   SUM(CASE WHEN m.role = 'user' THEN 1 ELSE 0 END) AS user_count,
                   SUM(CASE WHEN m.role = 'assistant' THEN 1 ELSE 0 END) AS assistant_count,
                   SUM(length(m.content)) AS content_chars
            FROM conversations c
            JOIN messages m ON m.conversation_id = c.id
            WHERE {" AND ".join(conditions)}
            GROUP BY c.id
            HAVING user_count > 0 AND assistant_count > 0
            ORDER BY c.started_at DESC
            """,
            params,
        ).fetchall()
        for row in rows:
            conversation = mem.store.get_conversation(row["id"])
            if conversation is None or not mem.conversations.title_needs_improvement(conversation):
                continue
            total_candidates += 1
            if len(candidates) < limit:
                reasons = _retitle_candidate_reasons(conversation.title)
                estimated_input_tokens = _estimate_retitle_input_tokens(
                    int(row["content_chars"] or 0)
                )
                candidates.append(
                    {
                        "conversationId": conversation.id,
                        "title": conversation.title,
                        "journey": conversation.journey,
                        "startedAt": conversation.started_at,
                        "messageCount": int(row["message_count"]),
                        "estimatedInputTokens": estimated_input_tokens,
                        "reasons": reasons,
                    }
                )
    return candidates, total_candidates


def _retitle_candidate_reasons(title: str | None) -> list[str]:
    clean = (title or "").strip()
    reasons: list[str] = []
    if not clean:
        reasons.append("blank_title")
    if "..." in clean:
        reasons.append("truncated_title")
    if len(clean) >= 55:
        reasons.append("long_title")
    if clean.lower().startswith("<skill"):
        reasons.append("skill_payload_title")
    return reasons or ["provisional_title"]


def _estimate_retitle_input_tokens(content_chars: int) -> int:
    prompt_overhead_chars = 400
    return max(1, math.ceil((content_chars + prompt_overhead_chars) / 4))


def _retitle_cost_estimate(candidates: list[dict[str, object]]) -> dict[str, object]:
    input_tokens = sum(int(candidate["estimatedInputTokens"]) for candidate in candidates)
    output_tokens = len(candidates) * 20
    input_cost = input_tokens * 0.0000001
    output_cost = output_tokens * 0.0000004
    return {
        "model": "google/gemini-2.5-flash-lite",
        "estimatedInputTokens": input_tokens,
        "estimatedOutputTokens": output_tokens,
        "estimatedCostUsd": round(input_cost + output_cost, 6),
        "pricing": {
            "inputPerTokenUsd": 0.0000001,
            "outputPerTokenUsd": 0.0000004,
        },
    }


def _run_console_demo(
    *,
    parameters: dict[str, object],
    emit_event: Callable[[str, str, dict[str, object] | None], None] | None,
) -> dict[str, object]:
    steps = int(parameters.get("steps", 5))
    for step in range(1, steps + 1):
        if emit_event is not None:
            emit_event(
                "progress",
                f"Demo progress {step}/{steps}.",
                {"step": step, "steps": steps},
            )
        time.sleep(1)
    return {
        "operationId": "run-console-demo",
        "status": "completed",
        "outcome": "demo_completed",
        "summary": [f"Emitted {steps} progress events.", "Demo operation completed."],
        "result": {"steps": steps, "note": "Read-only run console validation demo."},
    }


def _run_agent_run_prototype(
    *, mirror_home: Path | None, parameters: dict[str, object]
) -> dict[str, object]:
    result = run_agent_prototype(intent=str(parameters.get("intent", "")), mirror_home=mirror_home)
    return {
        "operationId": "agent-run-prototype",
        "status": "completed",
        "outcome": "proposal_ready",
        "summary": [
            "Agent prototype completed without writes.",
            "Proposal evidence is ready for review.",
        ],
        "result": {"agent": result.to_dict()},
    }


def _repair_candidate_payload(finding: dict[str, str | int]) -> dict[str, object]:
    return {
        "conversationId": str(finding["conversation_id"]),
        "journey": str(finding["journey"]),
        "reason": str(finding["reason"]),
        "title": str(finding["title"]),
        "startedAt": str(finding["started_at"]),
        "messageCount": int(finding["message_count"]),
    }


def _runtime_health_summary(report: RuntimeStatusReport) -> list[str]:
    summary = [f"Runtime status: {report.status}", f"Version: {report.version}"]
    if report.git.branch:
        summary.append(f"Git branch: {report.git.branch}")
    if report.mirror_home:
        summary.append(f"Mirror home: {report.mirror_home}")
    if report.mirror_home_error:
        summary.append(f"Mirror home note: {report.mirror_home_error}")
    if report.db_exists is False:
        summary.append("Database: missing")
    elif report.db_exists is True:
        summary.append("Database: present")
    return summary


def _runtime_status_payload(report: RuntimeStatusReport) -> dict[str, object]:
    return {
        "status": report.status,
        "version": report.version,
        "repository": _path_or_none(report.git.repository),
        "git": {
            "branch": report.git.branch,
            "commit": report.git.commit,
            "dirty": report.git.dirty,
            "error": report.git.error,
        },
        "mirrorHome": _path_or_none(report.mirror_home),
        "mirrorHomeError": report.mirror_home_error,
        "database": {
            "path": _path_or_none(report.db_path),
            "exists": report.db_exists,
        },
        "coreMigrations": {
            "ready": report.core_migrations.ready,
            "appliedCount": report.core_migrations.applied_count,
            "knownCount": report.core_migrations.known_count,
            "missing": list(report.core_migrations.missing),
            "unknown": list(report.core_migrations.unknown),
            "note": report.core_migrations.note,
        },
        "extensions": list(report.extensions),
        "extensionHealth": [
            {
                "extensionId": health.extension_id,
                "ready": health.ready,
                "note": health.note,
                "pendingMigrations": list(health.pending_migrations),
                "driftedMigrations": list(health.drifted_migrations),
                "unknownMigrations": list(health.unknown_migrations),
            }
            for health in report.extension_health
        ],
        "cloneRole": {
            "value": report.clone_role.value,
            "source": _path_or_none(report.clone_role.source),
            "note": report.clone_role.note,
        },
        "pythonVersion": report.python_version,
        "memoryEnv": report.memory_env,
        "updateChannel": {
            "value": report.update_channel.value,
            "source": _path_or_none(report.update_channel.source),
            "note": report.update_channel.note,
        },
    }


def _path_or_none(path: Path | None) -> str | None:
    return str(path) if path is not None else None
