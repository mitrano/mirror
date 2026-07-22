# Termo de Abertura — YouTube Music Importer — Journey Path

**Status:** active
**Stage:** Iniciação
**Created:** 2026-07-22

## Current status

Prova de viabilidade implementada no Mirror como comando local `python -m memory ytmusic-importer`. O comando lê arquivo de músicas, busca no YouTube Music via `ytmusicapi`, opera em dry-run por padrão, cria/usa playlist apenas com `--apply`, evita duplicatas já presentes e emite relatório de matches, ambiguidades e não encontrados.

## Source document

/home/ricardoalvares/repos/mirror/journeys/ytmusic-importer/00-termo-abertura.md

## Next movement

Validar em conta real com uma playlist descartável e 10 músicas variadas. Antes do teste vivo, preparar o arquivo de autenticação do `ytmusicapi` e executar um dry-run. Só usar `--apply` depois de revisar o relatório.
