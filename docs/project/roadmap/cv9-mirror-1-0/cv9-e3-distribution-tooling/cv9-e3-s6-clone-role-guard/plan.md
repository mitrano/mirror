[< Story](index.md)

# Plan - CV9.E3.S6 Clone Role Guard

## Design Direction

Each clone declares its role through a local file. The Mirror runtime reads this file once and uses it to:

- decide whether Builder Mode is allowed in this clone;
- show the role in runtime status so it stays visible;
- make the boundary explicit in docs and future hooks.

The marker is per-clone identity, not part of the project. So it is local to the working tree and ignored by git. Each developer marks their own clones.

## Marker File

Path:

```text
.mirror-clone-role
```

Allowed contents:

```text
production
dev
```

Behavior:

- File missing: role is `production`.
- File present with a known value, after `strip().lower()`: role is that value.
- File present with an unknown value: role is `production`, with a note describing the unknown value.
- File unreadable due to permissions or IO error: role is `production`, with a note.

`production` is the safe default. The dangerous mode is the one that must be explicitly declared.

## API Shape

Add to `memory.cli.runtime`:

```python
@dataclass(frozen=True)
class CloneRole:
    value: str
    source: Path | None
    note: str | None = None

def inspect_clone_role(start: Path | None = None) -> CloneRole: ...
```

`value` is `"production"` or `"dev"`. `source` is the resolved file path when it exists.

`inspect_clone_role` walks from `start` up to the repository root resolved by git. If no git root is available, it returns `CloneRole("production", None, note="no repository")`.

## Runtime Status Integration

`RuntimeStatusReport` gains a `clone_role: CloneRole` field. The status renderer prints a dedicated line:

```text
Clone role: production
```

When the role is `production`, status keeps existing behavior. When the role is `dev`, status also keeps existing behavior. The role does not change whether status is ready or attention-needed. It is informational at this layer.

`runtime version`, which is concise by design, may also include the role.

## Builder Mode Guard

`memory build load <slug>` gains:

```bash
uv run python -m memory build load <slug> [--allow-production]
```

Logic:

- inspect clone role for `cwd`;
- if role is `dev`, proceed as today;
- if role is `production` and `--allow-production` is not set, exit non-zero with a message that:
  - names the current clone path;
  - reports the resolved role;
  - explains that development belongs in a `dev` clone;
  - shows how to override with `--allow-production` when the user has a clear reason.

The override flag exists because real life has emergencies. The boundary should resist accidents but not block intentional choices.

## Tests

Targeted tests for `inspect_clone_role`:

- file missing returns `production`;
- file with `production` returns `production`;
- file with `dev` returns `dev`;
- file with mixed case or surrounding whitespace normalizes to the role;
- unknown value returns `production` with note;
- unreadable file returns `production` with note;
- non-git directory returns `production` with note.

Targeted tests for `runtime status`:

- status output includes `Clone role: production` by default;
- status output reflects `dev` when the file is present.

Targeted tests for `memory build load`:

- production clone exits non-zero without `--allow-production`;
- production clone with `--allow-production` proceeds;
- dev clone proceeds normally.

## Documentation

Update:

- `REFERENCE.md` runtime section to document the marker and the guard.
- `docs/process/runtime-repair-policy.md` to mention that development in production clones is explicitly out of bounds.
- `docs/project/decisions.md` with a new decision: "Mirror Mind clones declare a role".
- `docs/process/worklog.md` after implementation.

## Boundary

This story does not implement session-start hooks, welcome card changes, or self-update execution. It implements the marker, the inspector, the status surface, and the Builder Mode guard. Everything else is a future story.
