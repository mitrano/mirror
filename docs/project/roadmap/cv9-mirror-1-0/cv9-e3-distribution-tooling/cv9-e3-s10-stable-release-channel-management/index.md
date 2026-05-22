[< CV9.E3 Distribution & Tooling](../index.md)

# CV9.E3.S10 — Stable Release Channel Management

**Epic:** CV9.E3 Distribution & Tooling
**Status:** ✅ Done
**User-visible outcome:** Mirror Mind distinguishes integration updates from published releases, shows the local update channel, and exposes release notes through natural-language Mirror requests.

---

## What Changed

- Added `.mirror-update-channel` as a local, ignored clone marker.
- Valid update channels are `stable` and `main`; missing or invalid values default to `stable`.
- `runtime status`, `runtime version`, `runtime update --check`, `runtime update --dry-run`, `runtime update`, and `runtime update --repair-updater` can report or use the configured channel.
- `main` remains the integration/dogfooding channel.
- `stable` is the user-facing release channel and should advance only through release promotion.
- `python -m memory runtime release-notes [latest|vX.Y.Z]` reads narrative release notes from `docs/releases/`.
- Added the `mm-release-notes` skill so users can ask: `What's new in the latest Mirror Mind release?`

---

## Boundary

This story teaches the runtime how to follow channels and read release notes. It does not fully automate release promotion.

Release promotion remains a project/process action for now:

1. close the release arc;
2. bump version;
3. write `docs/releases/vX.Y.Z.md`;
4. pass CI and smoke validation;
5. tag `vX.Y.Z`;
6. fast-forward `stable` to the tagged release.

A future Maestro release doctor can automate these checks and perform promotion safely.

---

## Verification

```bash
PYTHONPATH=src uv run pytest tests/unit/memory/cli/test_runtime.py tests/unit/memory/cli/test_welcome.py
uv run --extra dev ruff check src/ tests/
uv run --extra dev ruff format --check src/ tests/
uv run --extra dev mypy src/memory/cli/runtime.py src/memory/cli/welcome.py
```

---

## See also

- [Runtime Self-Update Reference](../../../../../../REFERENCE.md#runtime-self-update)
- [Versioning](../../../../../process/versioning.md)
- [Release Notes](../../../../../process/release-notes.md)
