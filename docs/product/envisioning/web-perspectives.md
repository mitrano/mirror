[< Envisioning](index.md)

> **Status: Exploratory product design.** This document captures the first
> product exploration for the Mirror Mind 1.0 web visibility surface. It is not
> yet a roadmap or implementation spec. It should be iterated until the team can
> derive concrete epics and stories.

# Mirror Web Perspectives

Mirror Mind 1.0 needs a web surface that makes the user's Mirror visible. The
surface should not feel like a database admin panel. It should help the user
stand in front of their Mirror with a chosen way of looking.

The current product direction is to model the web experience through
**perspectives**. A perspective is not a permanent user type. It is a viewing
mode over the same underlying Mirror data.

```text
same Mirror data
  identity
  personas
  journeys
  memories
  conversations
  tasks
  decisions

seen through different perspectives
  Atlas
  Workspace
```

The Mirror does not change when the perspective changes. The user's stance in
front of the Mirror changes.

## Product premise

Mirror Mind has at least two natural usage patterns:

- Some users approach Mirror as identity-first: identity, self-knowledge,
  personas, memory, recurring patterns, and long-term becoming are the primary
  value.
- Other users approach Mirror as work-first: journeys, projects, operational
  context, decisions, tasks, and continuity are the primary value.

The product should not split these into two separate products or force a user to
choose a fixed identity. The same person may need a reflective view in one
moment and an operational view in another.

The web surface should therefore ask a situational question:

```text
How do you want to look at your Mirror?
```

For Mirror Mind 1.0, the initial perspectives are:

```text
Atlas
  Explore identity, personas, memories, patterns, and conversations as a map of
  meaning.

Workspace
  Follow journeys, decisions, tasks, conversations, and useful context as a
  surface for action.
```

## Perspective behavior

If a user has not chosen a default perspective yet, the web app asks which
perspective they want to use. The choice can be saved as the default, but the
user can always switch perspectives later.

```text
Welcome to your Mirror

Choose how you want to look today.

┌─────────────────────────────┐   ┌─────────────────────────────┐
│ Atlas                       │   │ Workspace                   │
│                             │   │                             │
│ Explore identity, personas, │   │ Follow journeys, decisions, │
│ memories, and patterns.     │   │ tasks, and conversations.   │
│                             │   │                             │
│ [Enter Atlas]               │   │ [Enter Workspace]           │
└─────────────────────────────┘   └─────────────────────────────┘

[ ] Use this as my default perspective
```

Once inside the app, the active perspective remains visible and switchable.

```text
┌──────────────────────────────────────────────────────────────┐
│ Mirror Mind                         Perspective: Atlas ▾     │
├───────────────┬──────────────────────────────────────────────┤
│ Home          │                                              │
│ Identity      │                                              │
│ Personas      │              perspective content             │
│ Memories      │                                              │
│ Conversations │                                              │
│ Journeys      │                                              │
└───────────────┴──────────────────────────────────────────────┘
```

## Atlas perspective

Atlas treats Mirror as a map of meaning. It is for understanding what the Mirror
knows, how identity is structured, which personas are active, which memories
matter, and which patterns keep returning.

Primary question:

```text
What does my Mirror know about me, and where did that understanding come from?
```

Initial navigation:

```text
Home
Identity
Personas
Memories
Patterns
Conversations
Journeys
```

Atlas home wireframe:

```text
┌──────────────────────────────────────────────────────────────┐
│ Atlas                                      Search your Mirror │
├──────────────────────────────────────────────────────────────┤
│ How your Mirror sees you today                               │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Identity summary                                         │ │
│ │ Key layers, active voice, important context              │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌──────────────────────┐ ┌──────────────────────┐           │
│ │ Active personas      │ │ Recent memories      │           │
│ │ product-designer     │ │ 5 added this week    │           │
│ │ engineer             │ │ 2 shadow candidates  │           │
│ └──────────────────────┘ └──────────────────────┘           │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Patterns and evidence                                   │ │
│ │ Recurring themes with links to memories and conversations│ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

Example object interpretation:

```text
Memory in Atlas
  What this reveals about me
  Related identity layer
  Related personas
  Evidence conversations
  Confidence and provenance
```

## Workspace perspective

Workspace treats Mirror as a surface for action. It is for understanding current
journeys, decisions, tasks, project context, and the conversation trail that led
to the current state.

Primary question:

```text
Where are we, what has been decided, and what should move next?
```

Initial navigation:

```text
Home
Journeys
Tasks
Decisions
Conversations
Memories
Context
```

Workspace home wireframe:

```text
┌──────────────────────────────────────────────────────────────┐
│ Workspace                                  Search your Mirror │
├──────────────────────────────────────────────────────────────┤
│ Active journeys                                             │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Mirror Mind 1.0                                          │ │
│ │ Stage: web visibility discovery                          │ │
│ │ Next: document perspectives and derive roadmap           │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌──────────────────────┐ ┌──────────────────────┐           │
│ │ Recent decisions     │ │ Open tasks           │           │
│ │ 3 this week          │ │ 7 active             │           │
│ └──────────────────────┘ └──────────────────────┘           │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Recent conversations by journey                          │ │
│ │ Conversation trails that shaped the current work          │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

Example object interpretation:

```text
Memory in Workspace
  Why this matters to the current journey
  Related decisions
  Related tasks
  Related conversations
  Last used or referenced
```

## Shared object model

Perspectives should not duplicate data. They should change the presentation and
priority of the same objects.

```text
Persona
  Atlas: an internal lens of identity
  Workspace: a specialized operating mode

Memory
  Atlas: evidence of a pattern or identity claim
  Workspace: reusable context for action

Conversation
  Atlas: evidence and autobiographical material
  Workspace: decision trail and operational history

Journey
  Atlas: a transformation path
  Workspace: a project or active field of work
```

This keeps the product coherent: identity remains the foundation, but identity
is not forced as the only front door.

## Evidence principle

Every interpretive claim should be traceable. When the interface says that a
memory, pattern, persona, or journey means something, the user should be able to
inspect the evidence behind it.

Initial evidence affordances:

```text
View evidence
  conversations
  source memories
  related journey events
  created or updated timestamps
  confidence or status when available
```

Evidence is not a separate 1.0 perspective yet. It is a detail pattern used by
both Atlas and Workspace.

## 1.0 scope hypothesis

The 1.0 web visibility slice should stay small enough to ship, while still
making the perspective model visible.

Possible 1.0 scope:

- First-run perspective choice when no default exists.
- Persistent default perspective setting.
- Perspective switcher in the web shell.
- Atlas home with identity, personas, memories, conversations, and journeys in
  read-only form.
- Workspace home with journeys, conversations, decisions or tasks when present,
  and relevant memories in read-only form.
- Object detail pages reuse existing data services where possible.
- Evidence links appear where source data is available, without requiring a full
  graph interface.

Out of scope for the first slice:

- Visual graph navigation.
- Editing identity or memory content.
- Automated perspective inference.
- Full evidence graph.
- Multi-user web authentication beyond the current local-first boundary.

## Open questions

- Should the default perspective be stored in the database, in the user home, or
  in browser-local state?
- Should perspective affect URLs, for example `/atlas/memories` and
  `/workspace/memories`, or should it be a query or session state over shared
  routes?
- Which objects already have enough provenance to support useful evidence links
  in 1.0?
- Are decisions first-class data today, or should Workspace derive decisions
  from journey docs and conversation metadata until a stronger model exists?
- Should Atlas and Workspace have different sidebars, or one shared sidebar with
  perspective-specific ordering and labels?
- What is the smallest manual validation scenario that proves users understand
  what is inside their Mirror?
