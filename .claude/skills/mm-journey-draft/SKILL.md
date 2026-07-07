---
name: "mm-journey-draft"
description: Creates and promotes reviewable journey opening drafts
user-invocable: true
---

# Journey Draft

Use this skill when Ricardo wants to start a possible future journey without
creating the real journey yet.

## Conversational Flow

1. Interview Ricardo conversationally, not as a form.
2. Ask at most three questions per round.
3. Synthesize what is clear, what is uncertain, and what remains missing.
4. When enough material exists, generate a Markdown opening term.
5. Materialize the draft with:

```bash
uv run python -m memory journey-draft start \
  --name "<journey name>" \
  --slug <slug> \
  --content-file -
```

Write the full Markdown document to stdin.

The draft path is:

```text
journeys/_drafts/<slug>-draft/00-termo-abertura-draft.md
```

Do not create the real journey until Ricardo explicitly approves the filled
opening term, e.g. "Ok, crie a jornada dessa maneira." After approval, promote:

```bash
uv run python -m memory journey-draft promote <slug>
```

Promotion creates:

```text
journeys/<slug>/00-termo-abertura.md
journeys/<slug>/01-journey-path.md
```

and creates the journey identity with the Journey Path file as its sync file.

## Draft Document Shape

The draft should include:

- Controle do Draft
- Síntese da Pré-Jornada
- Parâmetros Propostos para Criação da Jornada
- Contexto e Origem do Projeto
- Objetivo, Resultado Esperado e Critérios de Sucesso
- Escopo, Fora de Escopo e Dependências
- Stakeholders e Governança Inicial
- Situação Atual: fatos, hipóteses, pendências, decisões tomadas e em aberto
- Riscos e Pontos de Atenção
- Contrato Operacional do Mirror
- Primeiro Plano de Ação
- Lacunas Antes da Criação
- Confirmação para Criação

Do not add a command manual section. The document describes how Mirror should
conduct the journey, not how Ricardo must use commands.
