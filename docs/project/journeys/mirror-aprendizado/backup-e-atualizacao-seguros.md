# Plano Seguro de Backup e Atualização do Mirror

Data: 2026-06-18
Jornada: `mirror-aprendizado`

## Objetivo

Atualizar a instalação local do Mirror a partir da versão mais recente disponível no GitHub, sem perder alterações locais, commits não enviados ao remoto, banco de dados, memórias, documentos pessoais ou arquivos de jornada.

Este plano assume a situação atual observada no repositório:

```text
Branch local: main
Remote: origin -> https://github.com/mirror-mind-ai/mirror
Estado atual observado: main ahead 28, behind 319
HEAD observado na revisão do plano: cdf0f5a Refine safe Mirror backup plan
Commits locais recentes relevantes:
- cdf0f5a Refine safe Mirror backup plan
- e14ae94 Document Ricardo's authorial voice for versioned review
- 82c079e Document safe Mirror update plan
- 98153cd Preserve local Mirror learning and CLI updates
```

A proteção deve sempre considerar o **HEAD atual no momento da execução**, não apenas um commit antigo citado neste documento. Se novos commits locais forem criados antes da atualização, a branch de proteção deve ser criada apontando para o estado mais recente.

Como Ricardo não tem permissão para fazer push no repositório oficial do Mirror, a proteção das alterações locais deve ser feita por referências locais, arquivos de backup e, idealmente, um fork/repositório privado próprio.

## Princípios de segurança

1. Não executar `git reset --hard origin/main` antes de proteger os commits locais.
2. Não confiar apenas no reflog como mecanismo de recuperação.
3. Separar claramente:
   - código oficial atualizado do Mirror;
   - alterações locais de Ricardo;
   - banco SQLite e dados pessoais;
   - exports, attachments e documentos de jornadas.
4. Registrar cada etapa antes de fazer mudanças destrutivas.
5. Só aplicar atualização depois de confirmar que há pelo menos dois caminhos de recuperação.

## Garantia real sobre as alterações locais

Este plano garante que tudo o que Ricardo alterou nesta versão local do Mirror continue **disponível para recuperação e reutilização** depois da atualização.

Essa garantia vem de três proteções principais:

```text
1. Branch local preservando o estado atual: minhas-alteracoes-mirror
2. Bundle Git externo com os commits locais
3. Backup completo da pasta do repositório
```

A garantia não significa que as alterações locais ficarão **ativas automaticamente** na `main` depois da atualização. Se a `main` for atualizada com:

```bash
git reset --hard origin/main
```

ela passará a refletir a versão oficial do GitHub. As alterações de Ricardo continuarão disponíveis na branch e nos backups, mas precisarão ser reaplicadas quando fizer sentido.

Formas de acesso depois da atualização:

```bash
# Voltar integralmente para a versão local preservada
git switch minhas-alteracoes-mirror

# Recuperar um arquivo específico da versão local preservada
git checkout minhas-alteracoes-mirror -- caminho/do/arquivo

# Trazer commits específicos para a versão atualizada
git cherry-pick 98153cd
git cherry-pick 82c079e
git cherry-pick e14ae94

# Tentar rebasear as alterações locais sobre a versão nova
git rebase origin/main
```

Portanto, o compromisso do plano é: **nada do que foi alterado localmente deve ser perdido**. A incorporação dessas alterações na versão nova é uma etapa posterior, deliberada e sujeita a validação/conflitos.

## Riscos principais

### 1. Perder commits locais

A branch local está à frente do remoto. Se a `main` for forçada para `origin/main`, os commits locais deixam de estar na ponta da branch.

Mitigação:

```bash
git branch minhas-alteracoes-mirror
```

### 2. Perder alterações pessoais não versionadas

Arquivos ignorados pelo Git ou fora do controle de versão podem não entrar no commit.

Mitigação:

```bash
git status --short --ignored
```

E backup externo da pasta inteira.

### 3. Perder banco de memória

O banco SQLite local contém conversas, memórias, identidade, jornadas e attachments. Ele não deve depender de Git.

Mitigação:

```bash
uv run python -m memory backup
```

Ou backup manual do banco, se necessário.

### 4. Conflitos ao reaplicar mudanças locais

Como o remoto está muitos commits à frente, trazer alterações locais por `rebase`, `merge` ou `cherry-pick` pode gerar conflitos.

Mitigação:

- atualizar primeiro a `main` limpa;
- testar a versão oficial;
- reaplicar mudanças locais seletivamente em uma branch separada.

## Plano completo

## Fase 0 — Não atualizar ainda

Antes de qualquer atualização, confirmar o estado atual:

```bash
cd /home/ricardoalvares/repos/mirror
git status --short --branch
git log --oneline --decorate -n 20
git remote -v
```

Resultado esperado:

- branch `main` existe;
- remoto `origin` aponta para o GitHub oficial;
- commit `98153cd` aparece no histórico local;
- não há alterações não commitadas relevantes, ou elas foram explicitamente tratadas.

## Fase 1 — Criar branch local de proteção

Criar uma referência local permanente para as alterações de Ricardo, apontando para o **HEAD atual**:

```bash
git branch minhas-alteracoes-mirror
```

Se houver dúvida sobre qual commit será protegido, conferir antes:

```bash
git log --oneline --decorate -n 5
```

Validar que o HEAD atual e os commits recentes estão protegidos:

```bash
git branch --contains HEAD
git branch --contains e14ae94
git branch --contains 82c079e
git branch --contains 98153cd
```

Resultado esperado:

```text
main
minhas-alteracoes-mirror
```

Se a branch já existir, usar um nome datado:

```bash
git branch backup-mirror-antes-update-2026-06-18
```

## Fase 2 — Criar bundle Git externo

Criar um arquivo `.bundle` com os commits locais protegidos. Preferencialmente salvar fora da pasta do repositório, para que o backup não dependa do próprio diretório que será atualizado:

```bash
mkdir -p /home/ricardoalvares/backups/mirror/git
git bundle create /home/ricardoalvares/backups/mirror/git/mirror-minhas-alteracoes-2026-06-18.bundle minhas-alteracoes-mirror
```

Validar o bundle:

```bash
git bundle verify /home/ricardoalvares/backups/mirror/git/mirror-minhas-alteracoes-2026-06-18.bundle
```

Esse arquivo permite recuperar a branch mesmo se o repositório local for danificado.

Para restaurar futuramente em outro clone:

```bash
git clone /home/ricardoalvares/backups/mirror/git/mirror-minhas-alteracoes-2026-06-18.bundle mirror-recuperado
```

Ou buscar a branch dentro de um repositório existente:

```bash
git fetch /home/ricardoalvares/backups/mirror/git/mirror-minhas-alteracoes-2026-06-18.bundle minhas-alteracoes-mirror:minhas-alteracoes-mirror
```

## Fase 3 — Backup do banco de memória

Executar o backup oficial, se disponível:

```bash
uv run python -m memory backup
```

Depois verificar onde o backup foi salvo conforme a saída do comando.

Se o comando não estiver disponível ou falhar, fazer backup manual dos arquivos de banco conhecidos. Primeiro localizar arquivos SQLite:

```bash
find . -type f \( -name '*.db' -o -name '*.sqlite' -o -name '*.sqlite3' \) -print
```

Depois copiar para uma pasta datada:

```bash
mkdir -p /home/ricardoalvares/backups/mirror/db/2026-06-18
cp caminho/do/banco.db /home/ricardoalvares/backups/mirror/db/2026-06-18/
```

Não assumir o caminho do banco sem verificar, porque ele pode variar conforme configuração local.

## Fase 4 — Backup da pasta inteira do repositório

Criar um backup externo da pasta atual antes da atualização:

```bash
mkdir -p /home/ricardoalvares/backups/mirror/full
cd /home/ricardoalvares/repos
tar --exclude='mirror/.venv' \
    -czf /home/ricardoalvares/backups/mirror/full/mirror-backup-completo-2026-06-18.tar.gz mirror
```

Não excluir arquivos internos de `.git/objects/pack/`. Eles podem conter objetos essenciais do repositório Git. Para um backup completo confiável, preservar a pasta `.git` inteira, excluindo no máximo ambientes recriáveis como `.venv`.

Alternativa mais simples, porém maior:

```bash
mkdir -p /home/ricardoalvares/backups/mirror/full
cd /home/ricardoalvares/repos
tar -czf /home/ricardoalvares/backups/mirror/full/mirror-backup-completo-2026-06-18.tar.gz mirror
```

Validar que o arquivo foi criado:

```bash
ls -lh /home/ricardoalvares/backups/mirror/full/mirror-backup-completo-2026-06-18.tar.gz
```

## Fase 5 — Registrar estado antes da atualização

Salvar diagnósticos em arquivos para auditoria:

```bash
mkdir -p /home/ricardoalvares/backups/mirror/update-audit/2026-06-18
git status --short --branch > /home/ricardoalvares/backups/mirror/update-audit/2026-06-18/git-status.txt
git log --oneline --decorate --graph -n 80 > /home/ricardoalvares/backups/mirror/update-audit/2026-06-18/git-log.txt
git branch -vv > /home/ricardoalvares/backups/mirror/update-audit/2026-06-18/git-branches.txt
git remote -v > /home/ricardoalvares/backups/mirror/update-audit/2026-06-18/git-remotes.txt
```

Opcionalmente registrar diferenças entre a versão local e o remoto:

```bash
git fetch origin
git log --oneline origin/main..main > /home/ricardoalvares/backups/mirror/update-audit/2026-06-18/commits-locais-nao-remotos.txt
git log --oneline main..origin/main > /home/ricardoalvares/backups/mirror/update-audit/2026-06-18/commits-remotos-nao-locais.txt
```

## Fase 6 — Atualizar a `main` local para a versão oficial

Somente depois das fases anteriores.

Buscar o remoto:

```bash
git fetch origin
```

Garantir que a branch local de proteção existe e aponta para o estado atual desejado:

```bash
git branch --contains HEAD
git branch --contains e14ae94
git branch --contains 82c079e
git branch --contains 98153cd
```

Atualizar a `main` para refletir exatamente o GitHub oficial:

```bash
git switch main
git reset --hard origin/main
```

Atenção: este é o passo destrutivo. Só deve ser executado depois dos backups.

## Fase 7 — Atualizar dependências

Após atualizar o código:

```bash
uv sync
```

Se houver instruções novas no `README.md`, `REFERENCE.md` ou documentação de release, segui-las antes de continuar.

## Fase 8 — Validar instalação atualizada

Rodar verificações básicas:

```bash
uv run python -m memory --help
uv run python -m memory journeys
uv run python -m memory conversations
```

Rodar testes, se viável:

```bash
uv run pytest
```

Se a suíte completa for pesada, começar por testes principais:

```bash
uv run pytest tests/unit/memory
```

## Fase 9 — Verificar banco e dados pessoais

Confirmar que o Mirror ainda acessa:

- jornadas;
- memórias;
- identidade;
- conversas;
- attachments relevantes.

Comandos úteis:

```bash
uv run python -m memory journeys
uv run python -m memory memories
uv run python -m memory conversations
```

Se algum comando tiver mudado na versão nova, consultar:

```bash
uv run python -m memory --help
```

## Fase 10 — Reaplicar alterações locais, se necessário

Não misturar imediatamente as alterações locais na `main` atualizada.

Criar uma branch de integração:

```bash
git switch -c integrar-minhas-alteracoes-apos-update
```

Opção A — rebase da branch local sobre a versão nova:

```bash
git switch minhas-alteracoes-mirror
git rebase origin/main
```

Se houver muitos conflitos, abortar:

```bash
git rebase --abort
```

Opção B — cherry-pick seletivo dos commits desejados:

```bash
git switch integrar-minhas-alteracoes-apos-update
git cherry-pick 98153cd
git cherry-pick 82c079e
git cherry-pick e14ae94
```

Usar apenas os commits que ainda fizerem sentido na versão nova. Se algum commit misturar documentação pessoal e mudanças de código, preferir recuperar arquivos específicos em vez de aplicar o commit inteiro.

Opção C — extrair arquivos específicos da branch antiga:

```bash
git checkout minhas-alteracoes-mirror -- caminho/do/arquivo
```

Essa opção é útil para recuperar documentos pessoais sem trazer mudanças antigas de código.

## Fase 11 — Validar novamente depois da integração

Depois de reaplicar qualquer alteração local:

```bash
git status --short
uv run python -m memory --help
uv run pytest
```

Se houve alteração em comandos, skills ou documentação operacional, testar manualmente os fluxos afetados.

## Fase 12 — Estratégia futura recomendada

Como Ricardo não tem push no repositório oficial, o ideal é adotar uma destas estratégias:

### Opção 1 — Fork pessoal

Criar um fork no GitHub pessoal e adicionar como remote:

```bash
git remote add ricardo git@github.com:SEU_USUARIO/mirror.git
```

Então enviar branches pessoais:

```bash
git push ricardo minhas-alteracoes-mirror
```

Vantagem: backup remoto real dos commits próprios.

### Opção 2 — Repositório privado de backup

Criar um repositório privado só para guardar customizações pessoais do Mirror.

### Opção 3 — Bundles versionados fora do repositório

Manter periodicamente arquivos `.bundle` em local externo:

```bash
git bundle create ~/backups/mirror-$(date +%Y%m%d).bundle --all
```

Vantagem: simples e independente de permissões no GitHub.

## Checklist antes de atualizar

Antes de executar o `reset --hard`, confirmar:

```text
[x] HEAD atual foi conferido com git log --oneline --decorate -n 5.
[x] Commits locais recentes relevantes existem: cdf0f5a, e14ae94, 82c079e e 98153cd.
[x] Branch minhas-alteracoes-mirror foi criada apontando para o HEAD atual disponível no momento da primeira proteção.
[x] git branch --contains HEAD mostra a branch de backup.
[x] git branch --contains cdf0f5a, e14ae94, 82c079e e 98153cd mostra a branch de backup.
[ ] Bundle Git foi criado fora do repositório e verificado.
[x] Banco SQLite foi salvo por backup oficial.
[x] Backup completo da pasta foi criado fora do repositório.
[x] Estado Git foi registrado em /home/ricardoalvares/backups/mirror/update-audit/.
[ ] Ricardo autorizou explicitamente iniciar a atualização.
```

## Checklist depois de atualizar

```text
[ ] main aponta para origin/main.
[ ] uv sync foi executado.
[ ] uv run python -m memory --help funciona.
[ ] Jornadas aparecem corretamente.
[ ] Conversas/memórias aparecem corretamente.
[ ] Testes principais passam ou falhas foram analisadas.
[ ] Alterações locais necessárias foram reaplicadas seletivamente.
[ ] Novo estado funcional foi commitado em branch própria, se houver mudanças.
```

## Registro de execução do backup

Execução iniciada após autorização de Ricardo para avançar com o processo de backup, sem executar a atualização da `main`.

Itens concluídos:

```text
[x] Revisão do plano commitada em cdf0f5a Refine safe Mirror backup plan.
[x] Branch local de proteção criada: minhas-alteracoes-mirror.
[x] Banco de memória salvo pelo comando oficial uv run python -m memory backup.
    Arquivo gerado: /home/ricardoalvares/.mirror-minds/ricardo/backups/memory_20260619_182822.zip
[x] Auditoria Git pré-update salva em: /home/ricardoalvares/backups/mirror/update-audit/2026-06-18/
[x] Backup completo da pasta salvo em: /home/ricardoalvares/backups/mirror/full/mirror-backup-completo-2026-06-18.tar.gz
    Tamanho observado: 36M
[ ] Bundle Git externo criado e verificado.
[ ] Branch minhas-alteracoes-mirror atualizada após o commit deste registro de execução.
[ ] Atualização da main para origin/main executada.
```

Observação: o backup oficial do banco gerou arquivo com timestamp `20260619_182822`, conforme relógio do ambiente no momento da execução.

## Comando proibido até os backups estarem prontos

Não executar antes da autorização explícita:

```bash
git reset --hard origin/main
```

## Estado desta documentação

Este arquivo deixou de ser apenas um plano e passou a registrar a execução parcial do backup. Até este ponto, foram executadas etapas de proteção e backup. Nenhuma etapa de atualização da `main` para `origin/main` foi executada.
