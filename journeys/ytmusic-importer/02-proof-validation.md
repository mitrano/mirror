# Prova de Viabilidade — YouTube Music Importer

## Objetivo

Validar se `ytmusicapi` é suficiente para criar/usar uma playlist do YouTube Music e adicionar músicas a partir de uma lista textual.

## Ponto exato de retomada técnica

A implementação da PoC já foi concluída. O próximo trabalho não é codar a ferramenta final: é validar autenticação real para operações de playlist.

Começar por uma destas duas rotas, nesta ordem preferencial:

1. criar credenciais OAuth Desktop App no Google Cloud com YouTube Data API v3 habilitada;
2. gerar `journeys/ytmusic-importer/oauth.json` com `ytmusicapi oauth`;
3. rodar dry-run autenticado;
4. se OAuth for inviável, refazer `browser.json` copiando headers completos de uma requisição real de `music.youtube.com/youtubei/v1/browse`.

O comando OAuth que faltou executar depende de `client_id` e `client_secret`:

```bash
uv run --extra ytmusic ytmusicapi oauth \
  --file journeys/ytmusic-importer/oauth.json \
  --client-id "SEU_CLIENT_ID" \
  --client-secret "SEU_CLIENT_SECRET"
```

## Comando

Dry-run seguro:

```bash
uv run --extra ytmusic python -m memory ytmusic-importer \
  --songs journeys/ytmusic-importer/smoke-songs.txt \
  --playlist "Mirror Test" \
  --auth journeys/ytmusic-importer/oauth.json
```

Aplicação real, após revisar o dry-run:

```bash
uv run --extra ytmusic python -m memory ytmusic-importer \
  --songs journeys/ytmusic-importer/smoke-songs.txt \
  --playlist "Mirror Test" \
  --auth journeys/ytmusic-importer/oauth.json \
  --apply
```

## Arquivo de músicas

Uma música por linha. Formatos aceitos:

```text
Radiohead - Weird Fishes
Milton Nascimento - Cais
Aphex Twin - Xtal
```

Linhas em branco e linhas iniciadas com `#` são ignoradas.

## Pré-requisitos

- instalar `ytmusicapi` no ambiente local;
- gerar um arquivo de autenticação de headers/cookies conforme a documentação do `ytmusicapi`;
- usar uma playlist descartável para o primeiro teste real.

## Critérios de validação

O experimento passa se:

- a autenticação local funcionar;
- o dry-run retornar matches compreensíveis;
- a execução com `--apply` criar ou localizar a playlist;
- as músicas forem adicionadas no YouTube Music;
- duplicatas já presentes não forem reinseridas;
- o relatório final mostrar adicionadas, ambíguas e não encontradas.

## Resultado parcial do primeiro teste real

Data: 2026-07-22

Resultado confirmado:

- `ytmusicapi` instalou e carregou corretamente no ambiente local;
- busca pública no YouTube Music funcionou para as 10 músicas de teste;
- os matches retornados foram majoritariamente corretos e suficientes para validar a hipótese de matching inicial.

Resultado ainda não confirmado:

- autenticação de biblioteca/playlist;
- localização/criação de playlist;
- adição real das músicas.

Bloqueio encontrado:

- o dry-run autenticado falhou ao consultar playlists com `JSONDecodeError` dentro de `ytmusicapi`, indicando que a resposta recebida não veio como JSON esperado. A causa provável é autenticação `browser` inválida/incompleta ou instabilidade do fluxo browser, que a própria CLI do `ytmusicapi` marca como deprecated.

Próxima tentativa recomendada:

- criar credenciais OAuth Desktop App no Google Cloud com YouTube Data API v3 habilitada;
- gerar `journeys/ytmusic-importer/oauth.json` com `ytmusicapi oauth`;
- repetir primeiro o dry-run autenticado;
- só usar `--apply` depois de um dry-run autenticado bem-sucedido e aprovado por Ricardo.

## Limitações conscientes

- `ytmusicapi` é biblioteca não oficial.
- O primeiro match é escolhido automaticamente mesmo quando há múltiplos candidatos; ambiguidades são reportadas para revisão, mas ainda não há seleção interativa.
- O PoC não deve ser usado em playlists importantes antes de validar com playlist descartável.
