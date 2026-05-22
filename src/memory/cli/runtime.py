"""Runtime status inspection for Mirror Mind."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path

from memory.config import (
    MEMORY_ENV,
    default_db_path_for_home,
    default_extensions_dir_for_home,
    resolve_mirror_home,
)


@dataclass(frozen=True)
class GitStatus:
    repository: Path | None
    branch: str | None
    commit: str | None
    dirty: bool | None
    error: str | None = None


@dataclass(frozen=True)
class RuntimeStatusReport:
    version: str
    git: GitStatus
    mirror_home: Path | None
    mirror_home_error: str | None
    db_path: Path | None
    db_exists: bool | None
    extensions: tuple[str, ...]
    python_version: str
    memory_env: str

    @property
    def status(self) -> str:
        if self.mirror_home_error:
            return "attention needed"
        if self.git.error:
            return "attention needed"
        if self.git.dirty:
            return "attention needed"
        if self.db_exists is False:
            return "attention needed"
        return "ready"


def package_version() -> str:
    try:
        return metadata.version("mirror")
    except metadata.PackageNotFoundError:
        return _version_from_pyproject(Path.cwd()) or "unknown"


def _version_from_pyproject(start: Path) -> str | None:
    for parent in (start.resolve(), *start.resolve().parents):
        pyproject = parent / "pyproject.toml"
        if not pyproject.exists():
            continue
        for line in pyproject.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("version ="):
                return line.partition("=")[2].strip().strip('"')
    return None


def _run_git(args: list[str], *, cwd: Path) -> tuple[int, str, str]:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=2,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, "", str(exc)
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def inspect_git(start: Path) -> GitStatus:
    code, stdout, stderr = _run_git(["rev-parse", "--show-toplevel"], cwd=start)
    if code != 0 or not stdout:
        return GitStatus(
            repository=None,
            branch=None,
            commit=None,
            dirty=None,
            error=stderr or "not a git repository",
        )

    repository = Path(stdout).resolve()
    branch_code, branch, branch_err = _run_git(["branch", "--show-current"], cwd=repository)
    commit_code, commit, commit_err = _run_git(["rev-parse", "--short", "HEAD"], cwd=repository)
    dirty_code, dirty_out, dirty_err = _run_git(["status", "--porcelain"], cwd=repository)

    errors = [
        err
        for code, err in (
            (branch_code, branch_err),
            (commit_code, commit_err),
            (dirty_code, dirty_err),
        )
        if code != 0 and err
    ]

    return GitStatus(
        repository=repository,
        branch=branch if branch_code == 0 and branch else None,
        commit=commit if commit_code == 0 and commit else None,
        dirty=bool(dirty_out) if dirty_code == 0 else None,
        error="; ".join(errors) if errors else None,
    )


def list_installed_extensions(mirror_home: Path | None) -> tuple[str, ...]:
    if mirror_home is None:
        return ()
    extensions_dir = default_extensions_dir_for_home(mirror_home)
    if not extensions_dir.exists() or not extensions_dir.is_dir():
        return ()
    return tuple(
        sorted(
            child.name
            for child in extensions_dir.iterdir()
            if child.is_dir() and (child / "skill.yaml").exists()
        )
    )


def build_runtime_status(
    *,
    start: Path | None = None,
    mirror_home_arg: str | Path | None = None,
) -> RuntimeStatusReport:
    start_path = (start or Path.cwd()).expanduser().resolve()
    git = inspect_git(start_path)

    mirror_home: Path | None = None
    mirror_home_error: str | None = None
    try:
        mirror_home = resolve_mirror_home(mirror_home=mirror_home_arg)
    except ValueError as exc:
        mirror_home_error = str(exc)

    db_path = default_db_path_for_home(mirror_home) if mirror_home else None
    db_exists = db_path.exists() if db_path else None

    return RuntimeStatusReport(
        version=package_version(),
        git=git,
        mirror_home=mirror_home,
        mirror_home_error=mirror_home_error,
        db_path=db_path,
        db_exists=db_exists,
        extensions=list_installed_extensions(mirror_home),
        python_version=sys.version.split()[0],
        memory_env=MEMORY_ENV,
    )


def _yes_no(value: bool | None) -> str:
    if value is None:
        return "unknown"
    return "yes" if value else "no"


def render_runtime_status(report: RuntimeStatusReport) -> str:
    lines: list[str] = []
    lines.append("Mirror runtime status")
    lines.append("")
    lines.append(f"Version: {report.version}")
    lines.append(f"Repository: {report.git.repository if report.git.repository else 'unknown'}")
    lines.append(f"Git branch: {report.git.branch or 'unknown'}")
    lines.append(f"Git commit: {report.git.commit or 'unknown'}")
    lines.append(f"Git dirty: {_yes_no(report.git.dirty)}")
    if report.git.error:
        lines.append(f"Git status note: {report.git.error}")
    lines.append(f"Mirror home: {report.mirror_home if report.mirror_home else 'not configured'}")
    if report.mirror_home_error:
        lines.append(f"Mirror home note: {report.mirror_home_error}")
    lines.append(f"Database: {report.db_path if report.db_path else 'unknown'}")
    lines.append(f"Database exists: {_yes_no(report.db_exists)}")
    if report.extensions:
        lines.append(
            f"Installed extensions: {len(report.extensions)} ({', '.join(report.extensions)})"
        )
    else:
        lines.append("Installed extensions: 0")
    lines.append(f"Python: {report.python_version}")
    lines.append(f"MEMORY_ENV: {report.memory_env}")
    lines.append("")
    lines.append(f"Status: {report.status}")
    return "\n".join(lines) + "\n"


def cmd_runtime(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Inspect Mirror runtime state")
    subparsers = parser.add_subparsers(dest="command", required=True)
    status_parser = subparsers.add_parser("status", help="Inspect runtime status")
    status_parser.add_argument("--mirror-home", dest="mirror_home")
    args = parser.parse_args(argv)

    if args.command == "status":
        report = build_runtime_status(mirror_home_arg=args.mirror_home)
        sys.stdout.write(render_runtime_status(report))
        return 0 if report.status == "ready" else 1

    parser.print_help()
    return 1


def main(argv: list[str] | None = None) -> None:
    raise SystemExit(cmd_runtime(sys.argv[1:] if argv is None else argv))
