# Personal Fork Runtime

Ricardo's Mirror runtime is configured to receive updates from his personal fork
so custom functionality can persist across updates.

This matters for Journey Drafts because the feature is personal to Ricardo's fork
and has not been contributed to the official upstream repository.

---

## Repository roles

The production runtime uses these remotes:

```text
origin   -> https://github.com/mitrano/mirror.git
upstream -> https://github.com/mirror-mind-ai/mirror
```

Meaning:

- `origin` is Ricardo's fork and is the source used by `/mm-update`;
- `upstream` is the official Mirror repository;
- local customizations should be committed to the fork;
- official changes can be merged into the fork when Ricardo wants to receive
  upstream improvements.

The runtime update channel remains:

```text
stable
```

So normal updates read from:

```text
origin/stable
```

---

## Why not update directly from upstream?

If the production runtime updated directly from the official repository, custom
features that exist only in Ricardo's fork could disappear or conflict during
updates.

Using the fork as the runtime source gives Ricardo a durable path:

```text
official Mirror upstream
        ↓
Ricardo's fork
        ↓
Ricardo's production runtime
```

---

## Normal update behavior

When Ricardo runs `/mm-update`, Mirror executes the runtime updater against the
configured remote and channel. In this setup, that means:

```text
origin/stable from mitrano/mirror
```

A healthy update check should say the runtime is up to date with `origin/stable`:

```bash
uv run python -m memory runtime update --check
```

Expected shape:

```text
Update channel: stable
Upstream: origin/stable
Availability: up_to_date
```

---

## Bringing official Mirror changes into the fork

When Ricardo wants official upstream improvements, the safe pattern is:

1. update the development clone from `upstream/main`;
2. reapply or preserve personal changes;
3. run tests;
4. push to `origin/main` and `origin/stable` in Ricardo's fork;
5. update production through the normal runtime updater.

Conceptual command sequence from the development clone:

```bash
cd /home/ricardoalvares/repos/mirror-dev
git fetch upstream
git reset --hard upstream/main
# reapply personal commits or merge/cherry-pick them
git push origin main
git push origin HEAD:stable
```

Then, from production:

```bash
cd /home/ricardoalvares/repos/mirror
uv run python -m memory runtime update --check
uv run python -m memory runtime update
```

Do not edit the production runtime directly for feature development. Use the dev
clone and promote tested changes through the fork.

---

## Current custom feature

The current fork-specific feature is Journey Drafts:

```bash
uv run python -m memory journey-draft --help
```

See [Journey Drafts](index.md) for usage.
