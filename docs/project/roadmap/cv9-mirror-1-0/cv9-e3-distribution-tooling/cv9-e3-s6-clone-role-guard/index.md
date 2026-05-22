[< CV9.E3 Distribution & Tooling](../index.md)

# CV9.E3.S6 - Clone Role Guard

**Status:** ✅ Done  
**Epic:** CV9.E3 Distribution & Tooling

---

## User-Visible Outcome

Mirror Mind distinguishes its own clones by an explicit role. A user can have a `production` clone for daily use and a `dev` clone for development, and Mirror tools refuse to confuse one with the other.

When Builder Mode tries to start in a `production` clone, it stops and explains the boundary instead of operating silently.

Runtime status reports the current clone role so the role is visible in every read-only inspection.

---

## Problem

Mirror Mind code currently has no notion of which clone is doing what. The same checkout can act as a daily-use Mirror, a development workspace, and a self-update target, with no signal to the user.

During the runtime self-update work this caused a real boundary violation: development happened in `~/mirror`, the personal production clone, while the dev clone `~/Code/mirror-dev` sat unused and behind. Nothing in `mm-build`, `runtime status`, or the session surfaces warned that production code was being modified.

The principle the user expects is:

- `production` is the daily-use, stable Mirror Mind. It receives code through `git pull` today and through `runtime update` in the future.
- `dev` is the development workspace. Working tree dirtiness, in-flight stories, and ad hoc experimentation are expected there.

Today nothing enforces or even surfaces this distinction.

---

## Scope

In scope:

- Define an explicit clone role marker.
- Default role is `production`.
- A new role inspector in `memory.cli.runtime`.
- `runtime status` reports the clone role.
- `memory build load` refuses to start Builder Mode in a `production` clone unless the user passes an explicit override.
- Documentation of the new boundary in `docs/project/decisions.md` and the runtime repair policy.
- Tests for: default role, missing file, malformed file, `production` blocking, `dev` allowing, override flag.

Out of scope:

- Migrating existing extensions or runtimes to use the role marker.
- Pi/Claude/Gemini session-start hooks to display the role at session opening.
- Automatic creation of marker files.
- Self-update flow changes.

---

## Done Condition

- Every Mirror Mind clone gets its role from a `.mirror-clone-role` file at the repo root.
- The marker file is git-ignored. It is identity of the clone, not of the project.
- Default role is `production` when the file is missing, unreadable, or contains an unknown value.
- `runtime status` displays the role on a dedicated line.
- `memory build load <slug>` exits with an explicit error in `production` clones unless the user passes `--allow-production`.
- The decisions log records the production/dev boundary as a stable design decision.
- `REFERENCE.md`, runtime repair policy, and worklog are updated.
