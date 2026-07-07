# Journey Drafts

Journey Drafts are a pre-opening workflow for creating better Mirror journeys.
They let a future journey mature as a reviewable Markdown document before Mirror
creates the real journey in the database.

The purpose is simple: a journey should not be born from a loose conversation.
It should be born from a reviewed opening term.

---

## What a journey draft is

A journey draft is a temporary pre-journey folder with a filled opening document:

```text
journeys/_drafts/<slug>-draft/00-termo-abertura-draft.md
```

It is not a real journey yet. It does not appear as an active journey in the
Mirror database. It is a place to interview, clarify, revise, and decide whether
the future journey is ready to exist.

When approved, the draft is promoted into a real journey:

```text
journeys/<slug>/00-termo-abertura.md
journeys/<slug>/01-journey-path.md
```

Promotion also creates the journey identity in Mirror and sets the generated
`01-journey-path.md` as the journey sync file.

---

## When to use it

Use a journey draft when the future journey needs a clear opening frame before it
becomes active. This is especially useful for professional project journeys, such
as:

- software construction projects;
- software maintenance or evolution;
- POCs;
- fleet devices or operational technology;
- system integrations;
- supplier or service follow-up;
- projects that need governance, stakeholders, risks, decisions, and next steps.

Do not use a draft when the journey is already obvious and lightweight enough to
create directly.

---

## Conversational workflow

The intended flow is conversational, not bureaucratic:

1. Ricardo asks Mirror to open a possible journey draft.
2. Mirror interviews Ricardo in short rounds.
3. Mirror synthesizes what is clear, what is uncertain, and what is missing.
4. Mirror generates the filled Markdown draft.
5. Ricardo reviews and asks for adjustments.
6. Mirror updates the draft.
7. Ricardo explicitly approves creation.
8. Mirror promotes the draft into a real journey.

Mirror should ask at most three questions per round and should synthesize before
asking for more information.

A good starting prompt is:

```text
Quero abrir um draft de jornada para um projeto de POC de câmeras na frota.
```

Mirror should then conduct the interview and only materialize the Markdown when
there is enough substance to review.

---

## Draft document structure

The draft file should be organized as a **Termo de Abertura de Jornada — Draft**.
It normally includes:

1. Controle do Draft
2. Síntese da Pré-Jornada
3. Parâmetros Propostos para Criação da Jornada
4. Contexto e Origem do Projeto
5. Objetivo, Resultado Esperado e Critérios de Sucesso
6. Escopo, Fora de Escopo e Dependências
7. Stakeholders e Governança Inicial
8. Situação Atual
   - Fatos confirmados
   - Hipóteses
   - Pendências
   - Decisões tomadas
   - Decisões em aberto
9. Riscos e Pontos de Atenção
10. Contrato Operacional do Mirror
11. Primeiro Plano de Ação
12. Lacunas Antes da Criação
13. Confirmação para Criação

The draft should not include a command manual. It should describe how Mirror must
conduct the future journey, not teach Ricardo a list of commands.

---

## CLI reference

Create a draft from the built-in template:

```bash
uv run python -m memory journey-draft start \
  --name "Camera POC" \
  --slug camera-poc
```

Create or overwrite a draft using a filled Markdown document from stdin:

```bash
uv run python -m memory journey-draft start \
  --name "Camera POC" \
  --slug camera-poc \
  --content-file - \
  --force
```

Show where a draft file lives:

```bash
uv run python -m memory journey-draft path camera-poc
```

Promote an approved draft into a real journey:

```bash
uv run python -m memory journey-draft promote camera-poc
```

Promotion must only happen after explicit approval, for example:

```text
Ok, crie a jornada dessa maneira.
```

---

## What promotion does

When a draft is promoted, Mirror:

1. reads `journeys/_drafts/<slug>-draft/00-termo-abertura-draft.md`;
2. creates `journeys/<slug>/`;
3. copies the approved term to `journeys/<slug>/00-termo-abertura.md`;
4. creates `journeys/<slug>/01-journey-path.md`;
5. creates the journey identity in the database;
6. sets the generated journey path file as the journey sync file.

The draft folder is not deleted automatically. It remains as pre-opening evidence
unless Ricardo chooses to archive or remove it later.

---

## Safety rules

- A draft is not a real journey.
- Mirror must not promote a draft without explicit approval.
- The final slug must not include `-draft`; the suffix belongs only to the draft
  folder.
- The opening term is the source of truth for creating the journey.
- If important information is missing, record it under `Lacunas Antes da Criação`
  instead of pretending the project is clearer than it is.

---

## Related document

For Ricardo's personal fork/update setup, see
[Personal Fork Runtime](personal-fork-runtime.md).
