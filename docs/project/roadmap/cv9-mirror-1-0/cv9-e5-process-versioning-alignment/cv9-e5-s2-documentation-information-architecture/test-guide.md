[< CV9.E5.S2](index.md)

# Test Guide — Documentation Information Architecture

This story changes documentation structure and navigation. Verification focuses
on link sanity, discoverability, roadmap consistency, and repository cleanliness.
No runtime smoke test is required unless implementation changes CLI behavior.

---

## Automated Checks

Run from the repository root:

```bash
uv run --extra dev ruff check src/ tests/
uv run --extra dev ruff format --check src/ tests/
git diff --check
```

If implementation changes code or moves files referenced by code, also run:

```bash
PYTHONPATH=src uv run pytest tests/unit/ tests/integration/ -m "not live"
```

Expected result: all commands pass.

---

## Documentation Presence Checks

```bash
test -f docs/index.md
test -f docs/product/index.md
test -f docs/project/briefing.md
test -f docs/project/roadmap/index.md
test -f docs/process/development-guide.md
test -f docs/process/runtime-repair-policy.md
test -f docs/releases/index.md
test -f REFERENCE.md
```

Expected result: no output and exit code 0.

---

## Discoverability Checks

Confirm the docs home points to the major user paths and reference surfaces:

```bash
rg "new user|operator|contributor|developer|Runtime|Reference" docs/index.md
rg "runtime update|runtime status|runtime diagnose|Runtime Repair Policy" docs/index.md REFERENCE.md
rg "Process|Project|Product" docs/index.md docs/process/triad.md
rg "Architecture|Python API|REFERENCE" docs/index.md
rg "Release" docs/index.md docs/releases/index.md
```

Expected result: each command returns at least one relevant match.

---

## Roadmap Consistency Checks

```bash
rg "CV9.E3.*Done|Distribution & Tooling.*Done" docs/project/roadmap/cv9-mirror-1-0/index.md docs/project/roadmap/cv9-mirror-1-0/cv9-e3-distribution-tooling/index.md
rg "CV9.E5.S2.*Documentation Information Architecture" docs/project/roadmap/cv9-mirror-1-0/cv9-e5-process-versioning-alignment/index.md
rg "Documentation Information Architecture" docs/project/roadmap/cv9-mirror-1-0/cv9-e5-process-versioning-alignment/cv9-e5-s2-documentation-information-architecture/index.md
```

Expected result: roadmap status and story references agree.

---

## Link Sanity Checks

Use `rg` to inspect newly edited links:

```bash
rg "\]\([^)]*\)" docs/index.md docs/process docs/product docs/project/roadmap/cv9-mirror-1-0/cv9-e5-process-versioning-alignment
```

Then manually verify changed relative links resolve. At minimum, open:

1. `docs/index.md`
2. `docs/process/runtime-repair-policy.md`
3. `docs/project/roadmap/cv9-mirror-1-0/index.md`
4. `docs/project/roadmap/cv9-mirror-1-0/cv9-e3-distribution-tooling/index.md`
5. `docs/project/roadmap/cv9-mirror-1-0/cv9-e5-process-versioning-alignment/index.md`
6. `docs/project/roadmap/cv9-mirror-1-0/cv9-e5-process-versioning-alignment/cv9-e5-s2-documentation-information-architecture/index.md`

Expected result: no broken links introduced by this story.

---

## Manual Coherence Review

Read the docs as four reader types:

- **New user:** can find Getting Started and first-run path.
- **Operator:** can find runtime status, update, backup, diagnose, and repair policy.
- **Contributor:** can find roadmap, decisions, development guide, and worklog.
- **Developer:** can find architecture, API, runtime interface, and command reference.

Confirm:

- The docs home explains the purpose of major sections.
- Process / Project / Product remains the conceptual backbone.
- Reference material is discoverable without diluting the triad.
- Runtime self-update docs are visible but not over-promoted as product vision.
- Any deliberate no-move decisions are documented.
