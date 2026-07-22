# Termo de Abertura — YouTube Music Importer — Journey Path

**Status:** active
**Stage:** Iniciação
**Created:** 2026-07-22

## Current status

Prova de viabilidade implementada no Mirror como comando local `python -m memory ytmusic-importer`. O comando lê arquivo de músicas, busca no YouTube Music via `ytmusicapi`, opera em dry-run por padrão, cria/usa playlist apenas com `--apply`, evita duplicatas já presentes e emite relatório de matches, ambiguidades e não encontrados.

## Ponto exato de retomada

Ao montar esta jornada em uma nova sessão, não começar pela ferramenta final. Começar pela validação real de autenticação e playlist.

Estado confirmado:

- o PoC local já existe e está testado;
- a busca pública do `ytmusicapi` funcionou para as 10 músicas de `smoke-songs.txt`;
- os matches foram bons o suficiente para manter `ytmusicapi` como hipótese principal;
- a suíte automatizada passou após a implementação.

Estado ainda não confirmado:

- autenticação real para operações de biblioteca/playlist;
- localização ou criação real da playlist no YouTube Music;
- adição real das músicas na playlist.

Bloqueio atual:

- o arquivo `browser.json` foi gerado, mas o dry-run autenticado falhou ao consultar playlists com `JSONDecodeError` dentro do `ytmusicapi`;
- a tentativa de OAuth avançou até o ponto em que a CLI pediu `Google Youtube Data API client ID`, portanto o próximo caminho OAuth exige criar credenciais no Google Cloud.

Próximo comando lógico, depois de criar credenciais OAuth Desktop App no Google Cloud:

```bash
uv run --extra ytmusic ytmusicapi oauth \
  --file journeys/ytmusic-importer/oauth.json \
  --client-id "SEU_CLIENT_ID" \
  --client-secret "SEU_CLIENT_SECRET"
```

Depois disso, rodar o dry-run autenticado:

```bash
uv run --extra ytmusic python -m memory ytmusic-importer \
  --songs journeys/ytmusic-importer/smoke-songs.txt \
  --playlist "Mirror Test" \
  --auth journeys/ytmusic-importer/oauth.json
```

Só executar `--apply` depois de Ricardo revisar e aprovar o dry-run.

## Source document

/home/ricardoalvares/repos/mirror/journeys/ytmusic-importer/00-termo-abertura.md

## Next movement

Validar em conta real com uma playlist descartável e 10 músicas variadas. Antes do teste vivo, preparar o arquivo de autenticação do `ytmusicapi` e executar um dry-run. Só usar `--apply` depois de revisar o relatório.
