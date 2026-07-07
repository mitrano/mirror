"""Journey draft orchestration for pre-opening project journeys."""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from memory.models import Identity
from memory.services.journey import JourneyService
from memory.utils import strip_accents

DRAFT_FILE = "00-termo-abertura-draft.md"
OPENING_FILE = "00-termo-abertura.md"
JOURNEY_PATH_FILE = "01-journey-path.md"


@dataclass(frozen=True)
class JourneyDraftWriteResult:
    slug: str
    draft_dir: Path
    draft_file: Path


@dataclass(frozen=True)
class JourneyDraftPromotionResult:
    slug: str
    name: str
    final_dir: Path
    opening_file: Path
    journey_path_file: Path
    identity: Identity


def slugify(value: str) -> str:
    normalized = strip_accents(value).lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    normalized = re.sub(r"-+", "-", normalized)
    return normalized[:80].strip("-")


def validate_slug(slug: str) -> str:
    clean = slug.strip().lower()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,78}[a-z0-9]", clean):
        raise ValueError(
            "slug must be kebab-case, 3-80 chars, using lowercase letters, numbers, and hyphens"
        )
    if clean.endswith("-draft"):
        raise ValueError("use the final journey slug; '-draft' is added only to the draft folder")
    return clean


class JourneyDraftService:
    def __init__(self, journeys: JourneyService) -> None:
        self.journeys = journeys

    def draft_path(self, slug: str, *, base_dir: str | Path = "journeys") -> Path:
        clean_slug = validate_slug(slug)
        return Path(base_dir).expanduser().resolve() / "_drafts" / f"{clean_slug}-draft"

    def draft_file(self, slug: str, *, base_dir: str | Path = "journeys") -> Path:
        return self.draft_path(slug, base_dir=base_dir) / DRAFT_FILE

    def write_draft(
        self,
        *,
        slug: str,
        name: str,
        content: str | None = None,
        base_dir: str | Path = "journeys",
        force: bool = False,
    ) -> JourneyDraftWriteResult:
        clean_slug = validate_slug(slug)
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("name is required")
        draft_dir = self.draft_path(clean_slug, base_dir=base_dir)
        draft_file = draft_dir / DRAFT_FILE
        if draft_file.exists() and not force:
            raise ValueError(f"draft already exists: {draft_file}")
        draft_dir.mkdir(parents=True, exist_ok=True)
        body = (
            content.strip()
            if content and content.strip()
            else self.render_template(clean_slug, clean_name)
        )
        draft_file.write_text(body.rstrip() + "\n", encoding="utf-8")
        return JourneyDraftWriteResult(clean_slug, draft_dir, draft_file)

    def promote_draft(
        self,
        *,
        slug: str,
        base_dir: str | Path = "journeys",
        force: bool = False,
    ) -> JourneyDraftPromotionResult:
        clean_slug = validate_slug(slug)
        draft_file = self.draft_file(clean_slug, base_dir=base_dir)
        if not draft_file.exists():
            raise ValueError(f"draft file not found: {draft_file}")
        content = draft_file.read_text(encoding="utf-8")
        fields = self.extract_fields(content)
        name = fields.get("name") or self._infer_name(content, clean_slug)
        status = (fields.get("status") or "active").lower()
        stage = fields.get("stage") or "Iniciação"
        description = fields.get("description") or self._extract_section(
            content, "Síntese da Pré-Jornada"
        )
        if len(description.strip()) < 20:
            description = f"Jornada criada a partir do termo de abertura aprovado para {name}."

        final_dir = Path(base_dir).expanduser().resolve() / clean_slug
        if final_dir.exists() and not force:
            raise ValueError(f"final journey folder already exists: {final_dir}")
        final_dir.mkdir(parents=True, exist_ok=True)
        opening_file = final_dir / OPENING_FILE
        journey_path_file = final_dir / JOURNEY_PATH_FILE
        shutil.copyfile(draft_file, opening_file)
        journey_path_file.write_text(
            self.render_journey_path(
                name=name, status=status, stage=stage, opening_file=opening_file
            ),
            encoding="utf-8",
        )
        identity_content = self.journeys.draft_journey(
            name=name,
            slug=clean_slug,
            status=status,
            stage=stage,
            description=description.strip(),
            current_focus=fields.get("next_movement")
            or "Conduzir o primeiro plano de ação definido no termo de abertura.",
        )["content"]
        identity = self.journeys.create_journey(
            slug=clean_slug,
            content=identity_content,
            sync_file=str(journey_path_file),
            icon="■",
            color="blue",
        )
        return JourneyDraftPromotionResult(
            clean_slug,
            name,
            final_dir,
            opening_file,
            journey_path_file,
            identity,
        )

    def render_template(self, slug: str, name: str) -> str:
        today = date.today().isoformat()
        return f"""# Termo de Abertura de Jornada — Draft

## 1. Controle do Draft

- Status do documento: draft
- Jornada criada: não
- Nome da jornada: {name}
- Slug provisório: {slug}
- Data da última revisão: {today}

> Este documento é um rascunho de pré-abertura. A jornada só deve ser criada após aprovação explícita de Ricardo.

## 2. Síntese da Pré-Jornada

A preencher pela entrevista conversacional.

## 3. Parâmetros Propostos para Criação da Jornada

- Nome da jornada: {name}
- Slug: {slug}
- Status inicial: active
- Stage inicial: Iniciação
- Tipo de projeto:
- Journey Path sugerido: journeys/{slug}/01-journey-path.md

## 4. Contexto e Origem do Projeto

## 5. Objetivo, Resultado Esperado e Critérios de Sucesso

## 6. Escopo, Fora de Escopo e Dependências

## 7. Stakeholders e Governança Inicial

## 8. Situação Atual

### Fatos confirmados

### Hipóteses

### Pendências

### Decisões tomadas

### Decisões em aberto

## 9. Riscos e Pontos de Atenção

## 10. Contrato Operacional do Mirror

Nesta jornada, o Mirror deve atuar como parceiro de governança, clareza e rastreabilidade, preservando a voz autoral de Ricardo e ajudando a transformar conversas, decisões e pendências em controle vivo do projeto.

O Mirror deve priorizar:

- clareza estratégica;
- separação entre fato, hipótese e pendência;
- comunicação profissional com respeito relacional;
- controle de escopo;
- registro de decisões;
- identificação de riscos;
- próximos passos concretos;
- melhoria contínua do método de gestão de Ricardo.

## 11. Primeiro Plano de Ação

- Próximo movimento:
- Primeiras pessoas a acionar:
- Primeiras informações a levantar:
- Primeiros documentos/evidências a reunir:

## 12. Lacunas Antes da Criação

## 13. Confirmação para Criação

A jornada só deve ser criada quando Ricardo disser explicitamente: “Ok, crie a jornada dessa maneira.”
"""

    def render_journey_path(self, *, name: str, status: str, stage: str, opening_file: Path) -> str:
        today = date.today().isoformat()
        return f"""# {name} — Journey Path

**Status:** {status}
**Stage:** {stage}
**Created:** {today}

## Current status

Jornada criada a partir do Termo de Abertura aprovado.

## Source document

{opening_file}

## Next movement

Conduzir o primeiro plano de ação definido no termo de abertura.
"""

    def extract_fields(self, content: str) -> dict[str, str]:
        labels = {
            "Nome da jornada": "name",
            "Slug": "slug",
            "Slug provisório": "slug",
            "Status inicial": "status",
            "Stage inicial": "stage",
            "Descrição": "description",
            "Descricao": "description",
            "Próximo movimento": "next_movement",
            "Proximo movimento": "next_movement",
        }
        fields: dict[str, str] = {}
        for line in content.splitlines():
            match = re.match(r"^[-*]\s*([^:]+):\s*(.+?)\s*$", line.strip())
            if not match:
                continue
            label, value = match.groups()
            key = labels.get(label.strip())
            if key and value.strip():
                fields[key] = value.strip()
        return fields

    def _extract_section(self, content: str, title: str) -> str:
        pattern = re.compile(rf"^##\s+\d*\.?\s*{re.escape(title)}\s*$", re.MULTILINE)
        match = pattern.search(content)
        if not match:
            return ""
        rest = content[match.end() :]
        next_heading = re.search(r"^##\s+", rest, re.MULTILINE)
        section = rest[: next_heading.start()] if next_heading else rest
        return section.strip()

    def _infer_name(self, content: str, slug: str) -> str:
        for line in content.splitlines():
            if line.startswith("# "):
                title = line[2:].replace("— Draft", "").strip()
                if title and title != "Termo de Abertura de Jornada":
                    return title
        return slug.replace("-", " ").title()
