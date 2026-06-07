[< Story](index.md)

# Test Guide — CV16.DS5 Story Thickening Surfaces

## Automated Verification

```bash
uv run pytest \
  tests/unit/memory/surfaces/test_explorer_story.py \
  tests/unit/memory/services/test_explorer_story.py \
  tests/unit/memory/cli/test_explore.py
```

Expected: all tests pass.

Lint:

```bash
uv run ruff check \
  src/memory/surfaces/explorer_story.py \
  src/memory/services/explorer_story.py \
  src/memory/cli/explore.py \
  tests/unit/memory/surfaces/test_explorer_story.py \
  tests/unit/memory/services/test_explorer_story.py \
  tests/unit/memory/cli/test_explore.py
```

Expected: all checks pass.

## Manual Smoke

Open a story:

```bash
uv run python -m memory explore story open explorer-mode \
  --story "Explorer Mode is becoming visibly stateful." \
  --summary "The story now has a surface, not only stored state." \
  --last-card "Opened around visible Explorer behavior."
```

Expected: output includes `△ EXPLORATORY STORY OPENED`.

Thicken the story:

```bash
uv run python -m memory explore story thicken explorer-mode \
  --story "Explorer Mode is becoming visibly stateful through story surfaces." \
  --summary "The design shifted from storage to visible thickening." \
  --last-card "Story thickened around observable behavior." \
  --changed "The useful unit is the visible story, not a signal taxonomy."
```

Expected: output includes `△ STORY THICKENED`, the changed text, and the updated story.

Render a snapshot:

```bash
uv run python -m memory explore story snapshot explorer-mode
```

Expected: output includes `△ NARRATIVE FIELD SNAPSHOT` and reflects the latest story.

## External Behavior Validation

Run this in Pi, not only through direct CLI commands. The goal is to validate the product behavior as the user experiences it: natural language in, visible Explorer surfaces out.

Start a fresh Pi session in this repository and activate Explorer Mode:

```text
/mm-explore explorer-mode
```

Expected:

- the assistant renders the `△ EXPLORER MODE ACTIVE` transition surface;
- the footer/status line shows `Active Journey explorer-mode on △ Explorer Mode`;
- the response does not begin Builder work.

Open an Exploratory Story through natural language:

```text
Vamos explorar a hipótese de que Explorer Mode deve girar em torno de uma única história acumulada, não de signals.
```

Expected:

- the assistant renders `△ EXPLORATORY STORY OPENED` or equivalent story-opening surface;
- the surface contains the story in accumulated form, not only a reflective paragraph;
- `uv run python -m memory explore story show explorer-mode` shows the stored story.

Thicken the story with corrective material:

```text
A correção é que eu quero validar comportamento externo, não só comandos internos. A story precisa aparecer na conversa.
```

Expected:

- the assistant renders `△ STORY THICKENED`;
- the surface names what changed;
- `uv run python -m memory explore story show explorer-mode` reflects the thickened story.

Ask for the current field:

```text
me mostra o campo narrativo atual
```

Expected:

- the assistant renders `△ NARRATIVE FIELD SNAPSHOT`;
- the snapshot reflects the latest story state.

Cleanup after validation:

```bash
uv run python -m memory explore story clear explorer-mode
uv run python -m memory explore deactivate
```

If the Pi session was only for validation and should not remain in history:

```text
/mm-discard
```

## Pass Condition

Explorer Mode has observable story-opening, story-thickening, and snapshot surfaces in an external Pi conversation, not only through internal CLI smoke tests. It preserves the no autonomous detection, no signal/radar modeling, no durable persistence, and no silent Builder promotion boundaries.
