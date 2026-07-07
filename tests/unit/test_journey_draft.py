from memory import MemoryClient
from memory.services.journey_draft import JourneyDraftService


def test_write_draft_creates_review_document(tmp_path):
    mem = MemoryClient(db_path=tmp_path / "memory.db")
    service = JourneyDraftService(mem.journeys)

    result = service.write_draft(
        slug="camera-poc",
        name="Camera POC",
        base_dir=tmp_path / "journeys",
    )

    assert (
        result.draft_file
        == tmp_path / "journeys" / "_drafts" / "camera-poc-draft" / "00-termo-abertura-draft.md"
    )
    content = result.draft_file.read_text(encoding="utf-8")
    assert "# Termo de Abertura de Jornada — Draft" in content
    assert "- Slug: camera-poc" in content
    assert "Contrato Operacional do Mirror" in content
    assert "A jornada só deve ser criada" in content


def test_promote_draft_creates_journey_and_first_documents(tmp_path):
    mem = MemoryClient(db_path=tmp_path / "memory.db")
    service = JourneyDraftService(mem.journeys)
    draft = """# Termo de Abertura de Jornada — Draft

## 1. Controle do Draft

- Nome da jornada: Camera POC
- Slug: camera-poc
- Status inicial: active
- Stage inicial: Iniciação

## 2. Síntese da Pré-Jornada

Jornada para acompanhar uma POC de câmeras na frota, com governança, rastreabilidade, controle de pendências e validação operacional.

## 11. Primeiro Plano de Ação

- Próximo movimento: Levantar responsáveis e critérios de validação.
"""
    service.write_draft(
        slug="camera-poc",
        name="Camera POC",
        content=draft,
        base_dir=tmp_path / "journeys",
    )

    result = service.promote_draft(slug="camera-poc", base_dir=tmp_path / "journeys")

    assert result.opening_file.exists()
    assert result.journey_path_file.exists()
    status = mem.get_journey_status("camera-poc")
    assert "camera-poc" in status
    assert "Camera POC" in status["camera-poc"]["identity"]
    assert "POC de câmeras" in status["camera-poc"]["identity"]
    assert status["camera-poc"]["journey_path"]
