# Tasks Detalhadas — YouTube Music Importer

## Ponto de retomada

A PoC já foi implementada. A retomada deve começar pela validação real da autenticação e das operações de playlist no YouTube Music, não pela construção da ferramenta final.

## Tasks aprovadas

### 1. Criar credenciais OAuth Desktop App para YouTube Data API v3

**Objetivo:** obter `client_id` e `client_secret` para autenticação OAuth do `ytmusicapi`.

**Detalhes:**

- criar ou selecionar projeto no Google Cloud;
- habilitar YouTube Data API v3;
- criar credencial OAuth do tipo Desktop App;
- guardar `client_id` e `client_secret` localmente, sem commitar.

**Critério de conclusão:** credenciais disponíveis para gerar `oauth.json`.

### 2. Gerar `journeys/ytmusic-importer/oauth.json`

**Objetivo:** substituir ou complementar o fluxo `browser.json`, que falhou no teste autenticado.

**Comando-base:**

```bash
uv run --extra ytmusic ytmusicapi oauth \
  --file journeys/ytmusic-importer/oauth.json \
  --client-id "SEU_CLIENT_ID" \
  --client-secret "SEU_CLIENT_SECRET"
```

**Critério de conclusão:** arquivo `oauth.json` criado localmente e ignorado pelo Git.

### 3. Rodar dry-run autenticado com playlist `Mirror Test`

**Objetivo:** validar se o `ytmusicapi` autenticado consegue consultar biblioteca/playlist.

**Comando-base:**

```bash
uv run --extra ytmusic python -m memory ytmusic-importer \
  --songs journeys/ytmusic-importer/smoke-songs.txt \
  --playlist "Mirror Test" \
  --auth journeys/ytmusic-importer/oauth.json
```

**Critério de conclusão:** dry-run roda sem erro de autenticação e produz relatório de matches/playlist.

### 4. Revisar qualidade dos matches do dry-run

**Objetivo:** verificar se os matches automáticos são bons o bastante para permitir aplicação real.

**Critério de conclusão:** Ricardo aprova o relatório ou identifica músicas que exigem correção/seleção manual.

### 5. Executar `--apply` em playlist descartável após aprovação

**Objetivo:** validar mutação real de playlist com baixo risco.

**Comando-base:**

```bash
uv run --extra ytmusic python -m memory ytmusic-importer \
  --songs journeys/ytmusic-importer/smoke-songs.txt \
  --playlist "Mirror Test" \
  --auth journeys/ytmusic-importer/oauth.json \
  --apply
```

**Critério de conclusão:** playlist é criada/localizada e músicas são adicionadas corretamente.

### 6. Registrar resultado final da viabilidade end-to-end

**Objetivo:** atualizar a jornada com evidência objetiva sobre a viabilidade real.

**Arquivos esperados:**

- `journeys/ytmusic-importer/01-journey-path.md`;
- `journeys/ytmusic-importer/02-proof-validation.md`.

**Critério de conclusão:** documentação registra se `ytmusicapi` foi aprovado, rejeitado ou mantido com ressalvas.

### 7. Decidir formato da ferramenta final

**Objetivo:** escolher se a ferramenta final será CLI simples, CLI interativa, extensão Mirror ou utilitário separado.

**Critério de conclusão:** decisão registrada na jornada antes de nova implementação.

### 8. Implementar seleção/revisão interativa de ambiguidades

**Objetivo:** evoluir o PoC para permitir revisão humana dos matches ambíguos antes de aplicar mudanças.

**Critério de conclusão:** usuário consegue aceitar, rejeitar ou escolher candidatos antes de `--apply`.
