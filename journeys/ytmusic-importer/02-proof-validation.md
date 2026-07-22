# Prova de Viabilidade — YouTube Music Importer

## Objetivo

Validar se `ytmusicapi` é suficiente para criar/usar uma playlist do YouTube Music e adicionar músicas a partir de uma lista textual.

## Comando

Dry-run seguro:

```bash
uv run python -m memory ytmusic-importer \
  --songs /caminho/para/songs.txt \
  --playlist "Mirror Test" \
  --auth /caminho/para/browser.json
```

Aplicação real, após revisar o dry-run:

```bash
uv run python -m memory ytmusic-importer \
  --songs /caminho/para/songs.txt \
  --playlist "Mirror Test" \
  --auth /caminho/para/browser.json \
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

## Limitações conscientes

- `ytmusicapi` é biblioteca não oficial.
- O primeiro match é escolhido automaticamente mesmo quando há múltiplos candidatos; ambiguidades são reportadas para revisão, mas ainda não há seleção interativa.
- O PoC não deve ser usado em playlists importantes antes de validar com playlist descartável.
