# Manual do Usuário do Mirror Mind

Este manual apresenta o Mirror Mind de forma progressiva: primeiro os conceitos, depois a instalação, os primeiros passos, o uso diário, os comandos, os recursos avançados, a manutenção e as boas práticas.

---

## Índice

- [1. Para quem é este manual](#1-para-quem-é-este-manual)
- [2. O que você vai aprender](#2-o-que-você-vai-aprender)
- [3. Pré-requisitos](#3-pré-requisitos)
- [4. Como usar este manual](#4-como-usar-este-manual)
- [5. O que é o Mirror Mind](#5-o-que-é-o-mirror-mind)
- [6. Conceitos fundamentais](#6-conceitos-fundamentais)
  - [6.1 Identidade](#61-identidade)
  - [6.2 Memória](#62-memória)
  - [6.3 Jornada](#63-jornada)
  - [6.4 Documento vivo ou journey path](#64-documento-vivo-ou-journey-path)
  - [6.5 Tarefa](#65-tarefa)
  - [6.6 Persona](#66-persona)
  - [6.7 Histórico de conversas](#67-histórico-de-conversas)
  - [6.8 Attachments](#68-attachments)
- [7. Diferenças entre os principais elementos](#7-diferenças-entre-os-principais-elementos)
- [8. Instalação básica](#8-instalação-básica)
  - [8.1 Instalar dependências](#81-instalar-dependências)
  - [8.2 Configurar ambiente](#82-configurar-ambiente)
  - [8.3 Inicializar usuário](#83-inicializar-usuário)
  - [8.4 Semear identidade no banco](#84-semear-identidade-no-banco)
  - [8.5 Verificar instalação](#85-verificar-instalação)
- [9. Primeiros passos](#9-primeiros-passos)
  - [9.1 Listar jornadas](#91-listar-jornadas)
  - [9.2 Consultar uma jornada](#92-consultar-uma-jornada)
  - [9.3 Criar uma jornada](#93-criar-uma-jornada)
  - [9.4 Registrar uma memória simples no diário](#94-registrar-uma-memória-simples-no-diário)
- [10. Uso diário do Mirror](#10-uso-diário-do-mirror)
  - [10.1 Escolher uma jornada](#101-escolher-uma-jornada)
  - [10.2 Trabalhar em modo reflexão](#102-trabalhar-em-modo-reflexão)
  - [10.3 Trabalhar em modo construção](#103-trabalhar-em-modo-construção)
  - [10.4 Consultar conversas anteriores](#104-consultar-conversas-anteriores)
- [11. Comandos mais usados](#11-comandos-mais-usados)
- [12. Jornadas](#12-jornadas)
  - [12.1 Listar jornadas](#121-listar-jornadas)
  - [12.2 Ver o estado de uma jornada](#122-ver-o-estado-de-uma-jornada)
  - [12.3 Criar jornada](#123-criar-jornada)
  - [12.4 Atualizar o documento vivo da jornada](#124-atualizar-o-documento-vivo-da-jornada)
  - [12.5 Associar uma jornada a uma pasta](#125-associar-uma-jornada-a-uma-pasta)
- [13. Memórias](#13-memórias)
  - [13.1 Listar memórias](#131-listar-memórias)
  - [13.2 Filtrar memórias por jornada](#132-filtrar-memórias-por-jornada)
  - [13.3 Pesquisar memórias](#133-pesquisar-memórias)
  - [13.4 Tipos comuns de memória](#134-tipos-comuns-de-memória)
- [14. Conversas](#14-conversas)
  - [14.1 Listar conversas recentes](#141-listar-conversas-recentes)
  - [14.2 Filtrar conversas por jornada](#142-filtrar-conversas-por-jornada)
  - [14.3 Associar uma conversa existente a uma jornada](#143-associar-uma-conversa-existente-a-uma-jornada)
  - [14.4 Recuperar uma conversa](#144-recuperar-uma-conversa)
- [15. Tarefas](#15-tarefas)
  - [15.1 Quando usar tarefas](#151-quando-usar-tarefas)
  - [15.2 Listar tarefas](#152-listar-tarefas)
  - [15.3 Criar tarefa](#153-criar-tarefa)
  - [15.4 Ver detalhes de uma tarefa](#154-ver-detalhes-de-uma-tarefa)
  - [15.5 Atualizar estado de uma tarefa](#155-atualizar-estado-de-uma-tarefa)
  - [15.6 Importar tarefas do documento vivo](#156-importar-tarefas-do-documento-vivo)
- [16. Diário](#16-diário)
- [17. Identidade](#17-identidade)
  - [17.1 Listar identidades](#171-listar-identidades)
  - [17.2 Ler uma identidade específica](#172-ler-uma-identidade-específica)
  - [17.3 Editar identidade](#173-editar-identidade)
- [18. Personas](#18-personas)
  - [18.1 O que é uma persona](#181-o-que-é-uma-persona)
  - [18.2 Quando uma persona é ativada](#182-quando-uma-persona-é-ativada)
  - [18.3 Ver personas existentes](#183-ver-personas-existentes)
  - [18.4 Inspecionar, editar e testar personas](#184-inspecionar-editar-e-testar-personas)
- [19. Attachments](#19-attachments)
- [20. Modos de operação e comandos por runtime](#20-modos-de-operação-e-comandos-por-runtime)
  - [20.1 Mirror Mode](#201-mirror-mode)
  - [20.2 Builder Mode](#202-builder-mode)
  - [20.3 Tabela de comandos por runtime](#203-tabela-de-comandos-por-runtime)
- [21. Recursos avançados](#21-recursos-avançados)
  - [21.1 Consultar outros modelos](#211-consultar-outros-modelos)
  - [21.2 Consolidação de memórias](#212-consolidação-de-memórias)
  - [21.3 Shadow](#213-shadow)
  - [21.4 Extensões](#214-extensões)
  - [21.5 Python API](#215-python-api)
- [22. Estrutura técnica do projeto](#22-estrutura-técnica-do-projeto)
- [23. Manutenção e segurança](#23-manutenção-e-segurança)
  - [23.1 Backup](#231-backup)
  - [23.2 Patches locais](#232-patches-locais)
- [24. Boas práticas](#24-boas-práticas)
  - [24.1 Boas práticas para jornadas](#241-boas-práticas-para-jornadas)
  - [24.2 Boas práticas para documentos vivos](#242-boas-práticas-para-documentos-vivos)
  - [24.3 Boas práticas para arquivos de projeto](#243-boas-práticas-para-arquivos-de-projeto)
  - [24.4 Boas práticas para tarefas](#244-boas-práticas-para-tarefas)
  - [24.5 Boas práticas de segurança](#245-boas-práticas-de-segurança)
- [25. Problemas comuns e como resolver](#25-problemas-comuns-e-como-resolver)
- [26. Referências internas](#26-referências-internas)
- [27. Resumo operacional](#27-resumo-operacional)

---

## 1. Para quem é este manual

Este manual é para usuários que querem usar o Mirror Mind como sistema local de memória, identidade e continuidade para agentes de IA.

Ele serve tanto para quem está começando quanto para quem já usa o Mirror e precisa consultar comandos, conceitos e boas práticas.

> **Observação:** este documento prioriza o uso prático. Ele explica os conceitos necessários antes de apresentar comandos e recursos avançados.

---

## 2. O que você vai aprender

Ao final deste manual, você deve conseguir:

- entender o que é o Mirror Mind;
- diferenciar identidade, memória, jornada, tarefa, persona, conversa e documento vivo;
- instalar e inicializar o Mirror;
- criar e consultar jornadas;
- registrar memórias e entradas de diário;
- listar e recuperar conversas anteriores;
- criar e acompanhar tarefas;
- usar `Mirror Mode` e `Builder Mode`;
- consultar attachments e documentos associados;
- usar recursos avançados, como extensões, consolidação, shadow, API Python e consulta a outros modelos;
- manter o ambiente seguro com backups e boas práticas.

---

## 3. Pré-requisitos

Para usar este manual, é recomendável ter:

- acesso ao repositório do Mirror;
- Python e `uv` instalados;
- terminal disponível;
- noções básicas de linha de comando;
- arquivo `.env` configurável;
- chave `OPENROUTER_API_KEY`, caso você queira usar consultas a outros modelos.

> **Atenção:** comandos que acessam LLMs externos podem gerar custo. Use com consciência, especialmente comandos de consulta, avaliação, geração de descritores, embeddings e busca semântica.

---

## 4. Como usar este manual

Leia as seções iniciais em ordem se você estiver começando. Elas explicam a lógica do sistema antes dos comandos.

Depois, use o índice como referência rápida. Cada seção de comando segue o mesmo padrão:

1. explicação do que o comando faz;
2. comando em bloco `bash`;
3. resultado esperado;
4. observações ou alertas quando necessário.

> **Boa prática:** antes de executar comandos que alteram dados, como atualização de jornada, edição de identidade ou remoção de tarefa, consulte primeiro o estado atual.

---

## 5. O que é o Mirror Mind

O Mirror Mind é um framework local-first de memória, identidade e continuidade para agentes de IA.

Na prática, ele permite que conversas, decisões, aprendizados, projetos e padrões pessoais sejam preservados ao longo do tempo. Em vez de cada chat começar do zero, o Mirror mantém uma base local com contexto reutilizável.

A base principal fica em SQLite, normalmente em:

```text
~/.mirror-minds/<usuario>/memory.db
```

O Mirror organiza informações em elementos como:

- identidade do usuário;
- personas especializadas;
- jornadas ou projetos;
- memórias extraídas de conversas;
- tarefas;
- histórico de conversas;
- documentos vivos chamados `journey_path`;
- attachments associados a jornadas.

---

## 6. Conceitos fundamentais

Antes de usar os comandos, é importante entender os principais blocos do Mirror.

### 6.1 Identidade

A identidade define quem é o usuário e como o Mirror deve operar. Ela funciona como uma camada de contexto permanente.

A identidade é organizada em camadas:

| Camada | Função |
|---|---|
| `self` | identidade profunda, visão de mundo e propósito |
| `ego` | comportamento operacional, tom e postura |
| `user` | dados e contexto do usuário |
| `persona` | lentes especializadas, como `engineer`, `writer` ou `therapist` |
| `shadow` | tensões, pontos cegos e padrões recorrentes |
| `journey` | identidade de uma jornada |
| `journey_path` | documento vivo de acompanhamento da jornada |

### 6.2 Memória

Memória é uma informação preservada no banco do Mirror para ser reutilizada no futuro.

Ela pode registrar decisões, aprendizados, padrões, ideias, compromissos, reflexões e tensões.

> **Observação:** memória não é o mesmo que histórico completo da conversa. A memória é uma síntese útil; a conversa é o registro do diálogo.

### 6.3 Jornada

Uma jornada é um espaço de continuidade para um tema, projeto ou frente importante.

Ela pode guardar:

- descrição;
- briefing;
- contexto;
- memórias relacionadas;
- conversas associadas;
- tarefas;
- notas;
- comandos úteis;
- progresso atual.

Exemplos de jornadas:

```text
mirror-aprendizado
psicologia
pmo-ti-jca
proj-anota
```

### 6.4 Documento vivo ou journey path

O `journey_path` é o documento vivo da jornada. Ele funciona como uma página de acompanhamento, manual, roteiro prático ou registro estruturado.

> **Atenção:** o comando `journey update` substitui o conteúdo inteiro do `journey_path`. Para não apagar conteúdo antigo, consulte a jornada, copie o conteúdo atual, adicione a nova parte e atualize com o conteúdo completo.

### 6.5 Tarefa

Tarefa é uma ação prática associada ao uso do Mirror ou a uma jornada específica.

Use tarefas quando houver algo claro a fazer, por exemplo:

- revisar um briefing;
- criar um documento;
- executar uma validação;
- acompanhar uma pendência;
- marcar algo como bloqueado ou concluído.

### 6.6 Persona

Uma persona é uma lente especializada da identidade do Mirror.

Ela não é outro assistente separado. É o mesmo Mirror operando com um foco específico, como engenharia, escrita, estratégia, saúde, finanças ou reflexão emocional.

Exemplos de personas:

- `engineer`;
- `writer`;
- `therapist`;
- `strategist`;
- `teacher`.

### 6.7 Histórico de conversas

O histórico de conversas é o registro de diálogos anteriores. Ele permite recuperar sessões passadas e consultar o que foi discutido.

A conversa preserva o fluxo; a memória preserva os pontos importantes extraídos ou registrados.

### 6.8 Attachments

Attachments são documentos ou conteúdos associados a uma jornada e guardados no banco SQLite do Mirror.

Eles funcionam como uma base de conhecimento vinculada à jornada.

---

## 7. Diferenças entre os principais elementos

Esta tabela resume as diferenças mais importantes.

| Elemento | Serve para | Exemplo |
|---|---|---|
| `memória` | preservar aprendizados, decisões e padrões | “Ricardo decidiu usar `mirror-aprendizado` como manual vivo.” |
| `jornada` | organizar continuidade de um tema ou projeto | `mirror-aprendizado` |
| `tarefa` | acompanhar uma ação executável | “Documentar comandos UV” |
| `identidade` | definir contexto permanente e modo de operação | camada `ego` ou `user` |
| `persona` | aplicar uma lente especializada | `engineer` para código |
| `journey_path` | manter um documento vivo da jornada | roteiro, manual ou plano |
| `conversa` | registrar o diálogo completo ou parcial | sessão anterior recuperada por `recall` |
| `attachment` | associar documentos à jornada | `manual-mirror-completo` |

> **Boa prática:** use jornadas para contexto estratégico, tarefas para ação, memórias para decisões e aprendizados, e documentos vivos para organização estruturada.

---

## 8. Instalação básica

Todos os comandos desta seção devem ser executados no terminal.

### 8.1 Instalar dependências

Este comando clona o repositório, entra na pasta do projeto e instala as dependências com `uv`.

```bash
git clone https://github.com/viniciusteles/mirror.git
cd mirror
uv sync
```

Resultado esperado: o ambiente Python do projeto será preparado.

### 8.2 Configurar ambiente

Copie o arquivo de exemplo de variáveis de ambiente.

```bash
cp .env.example .env
```

Depois, configure no `.env` pelo menos:

```env
MIRROR_USER=seu-nome
OPENROUTER_API_KEY=sk-or-...
```

Resultado esperado: o Mirror saberá qual usuário carregar e terá chave para recursos que dependem do OpenRouter.

### 8.3 Inicializar usuário

Este comando cria a estrutura inicial do usuário no Mirror.

```bash
uv run python -m memory init seu-nome
```

Resultado esperado: a pasta local do usuário será criada em `~/.mirror-minds/<usuario>/`.

### 8.4 Semear identidade no banco

Este comando carrega os arquivos de identidade iniciais para o banco SQLite.

```bash
uv run python -m memory seed
```

Resultado esperado: identidades, personas e jornadas iniciais serão inseridas no banco, quando ainda não existirem.

### 8.5 Verificar instalação

Use estes comandos para confirmar que personas, jornadas e roteamento estão funcionando.

```bash
uv run python -m memory list personas --verbose
uv run python -m memory list journeys
uv run python -m memory detect-persona "quero ajuda para escrever um artigo"
```

Resultado esperado: o terminal deve listar personas, jornadas e a persona detectada para a frase informada.

---

## 9. Primeiros passos

Esta seção mostra um fluxo mínimo para começar a usar o Mirror.

### 9.1 Listar jornadas

Use este comando para ver quais jornadas existem.

```bash
uv run python -m memory journeys
```

Resultado esperado: uma lista de jornadas com status, estágio e descrição.

### 9.2 Consultar uma jornada

Use este comando para ver o estado completo de uma jornada.

```bash
uv run python -m memory journey mirror-aprendizado
```

Resultado esperado: o terminal mostrará identidade da jornada, documento vivo, memórias recentes e conversas recentes.

### 9.3 Criar uma jornada

Use este comando quando quiser criar um novo espaço de continuidade.

```bash
uv run python -m memory journey create psicologia \
  --name "Psicologia" \
  --description "Estudos e reflexões sobre psicologia." \
  --briefing "Usar esta jornada para temas ligados à psicologia." \
  --context "Jornada criada para organizar aprendizados, leituras e práticas."
```

Resultado esperado: a jornada `psicologia` será criada no banco.

### 9.4 Registrar uma memória simples no diário

Use o diário para registrar uma observação ou aprendizado.

```bash
uv run python -m memory journal --journey mirror-aprendizado "Hoje aprendi como consultar jornadas usando UV."
```

Resultado esperado: uma entrada de diário será registrada e associada à jornada `mirror-aprendizado`.

---

## 10. Uso diário do Mirror

O uso diário do Mirror normalmente segue este ciclo:

1. escolher uma jornada;
2. carregar contexto;
3. trabalhar em reflexão ou construção;
4. registrar decisões, aprendizados ou tarefas;
5. consultar histórico quando necessário.

### 10.1 Escolher uma jornada

Use jornadas para separar temas importantes. Por exemplo:

- `mirror-aprendizado` para aprender o próprio Mirror;
- `pmo-ti-jca` para um projeto específico;
- `psicologia` para estudos e reflexões.

### 10.2 Trabalhar em modo reflexão

Use `Mirror Mode` para decisões, sentimentos, estratégia, escrita, mentoria, saúde, sentido e reflexão pessoal.

Em Pi ou Gemini CLI:

```text
/mm-mirror
```

Em Codex:

```text
$mm-mirror
```

Em Claude Code:

```text
/mm:mirror
```

### 10.3 Trabalhar em modo construção

Use `Builder Mode` para código, documentos, arquitetura, YAML, bugs, tarefas técnicas e criação de artefatos.

Em Pi ou Gemini CLI:

```text
/mm-build mirror-aprendizado
```

Em Codex:

```text
$mm-build mirror-aprendizado
```

Em Claude Code:

```text
/mm:build mirror-aprendizado
```

Pelo terminal:

```bash
uv run python -m memory build load mirror-aprendizado
```

Resultado esperado: o contexto da jornada será carregado para trabalho ativo.

### 10.4 Consultar conversas anteriores

Quando precisar recuperar algo discutido antes, liste as conversas e depois use `recall`.

```bash
uv run python -m memory conversations --journey mirror-aprendizado
```

Depois de obter o `conversation_id`, use:

```bash
uv run python -m memory recall <conversation_id>
```

---

## 11. Comandos mais usados

Esta é uma lista rápida dos comandos de uso mais frequente.

```bash
uv run python -m memory journeys
uv run python -m memory journey <slug>
uv run python -m memory journey create <slug> --name "Nome" --description "Descrição"
uv run python -m memory memories --journey <slug>
uv run python -m memory conversations --journey <slug>
uv run python -m memory conversation-logger attach --conversation <conversation_id> --journey <slug>
uv run python -m memory conversation-logger attach-latest-pi --journey <slug>
uv run python -m memory recall <conversation_id>
uv run python -m memory tasks list --journey <slug>
uv run python -m memory journal --journey <slug> "Texto"
uv run python -m memory backup
```

Para atualizar um documento vivo:

```bash
uv run python -m memory journey update <slug> - <<'EOF'
Conteúdo completo do documento vivo
EOF
```

> **Atenção:** `journey update` substitui o conteúdo inteiro do documento vivo.

---

## 12. Jornadas

Jornadas são a principal forma de organizar continuidade no Mirror.

### 12.1 Listar jornadas

Use este comando para listar jornadas existentes.

```bash
uv run python -m memory journeys
```

Forma alternativa:

```bash
uv run python -m memory list journeys
```

Resultado esperado: ambas as formas listam jornadas disponíveis.

### 12.2 Ver o estado de uma jornada

Use este comando para consultar uma jornada específica.

```bash
uv run python -m memory journey mirror-aprendizado
```

Forma equivalente:

```bash
uv run python -m memory journey status mirror-aprendizado
```

Resultado esperado: o terminal mostra o estado completo da jornada.

### 12.3 Criar jornada

Use este comando para criar uma jornada com nome, descrição, briefing e contexto.

```bash
uv run python -m memory journey create psicologia \
  --name "Psicologia" \
  --description "Estudos e reflexões sobre psicologia." \
  --briefing "Usar esta jornada para temas ligados à psicologia." \
  --context "Jornada criada para organizar aprendizados, leituras e práticas."
```

### 12.4 Atualizar o documento vivo da jornada

Use este comando para substituir o `journey_path` de uma jornada.

```bash
uv run python -m memory journey update mirror-aprendizado "Novo conteúdo do journey path."
```

Para textos maiores, use `stdin`:

```bash
uv run python -m memory journey update mirror-aprendizado - <<'EOF'
## Área nova

Conteúdo novo aqui.
EOF
```

> **Atenção:** o comando acima substitui o conteúdo inteiro do `journey_path`. Se quiser preservar o conteúdo antigo, consulte primeiro a jornada, copie o conteúdo atual, edite e envie o documento completo.

### 12.5 Associar uma jornada a uma pasta

Use este comando para vincular uma jornada a um diretório local ou projeto.

```bash
uv run python -m memory journey set-path mirror-aprendizado /caminho/da/pasta
```

Resultado esperado: a jornada passa a ter uma pasta associada.

---

## 13. Memórias

Memórias guardam aprendizados e decisões que precisam sobreviver ao tempo.

### 13.1 Listar memórias

Use este comando para listar memórias registradas.

```bash
uv run python -m memory memories
```

### 13.2 Filtrar memórias por jornada

Use este comando para listar apenas memórias de uma jornada.

```bash
uv run python -m memory memories --journey mirror-aprendizado
```

### 13.3 Pesquisar memórias

Use este comando para buscar memórias por texto.

```bash
uv run python -m memory memories --search "comandos"
```

Para pesquisar dentro de uma jornada específica:

```bash
uv run python -m memory memories --journey mirror-aprendizado --search "comandos"
```

Resultado esperado: o terminal lista memórias relacionadas ao termo pesquisado.

### 13.4 Tipos comuns de memória

As memórias podem ter tipos como:

- `decision`;
- `insight`;
- `idea`;
- `journal`;
- `tension`;
- `learning`;
- `pattern`;
- `commitment`;
- `reflection`.

---

## 14. Conversas

Conversas são registros de sessões anteriores. Elas ajudam a recuperar contexto detalhado.

### 14.1 Listar conversas recentes

Use este comando para listar conversas recentes.

```bash
uv run python -m memory conversations
```

### 14.2 Filtrar conversas por jornada

Use este comando para listar conversas associadas a uma jornada.

```bash
uv run python -m memory conversations --journey mirror-aprendizado
```

Para limitar a quantidade:

```bash
uv run python -m memory conversations --journey mirror-aprendizado --limit 10
```

### 14.3 Associar uma conversa existente a uma jornada

Use este recurso quando a conversa já existe no Mirror, mas não ficou associada
à jornada correta. Isso costuma acontecer quando você começou uma sessão antes
de carregar a jornada, ou quando percebeu depois que uma conversa de trabalho
deveria aparecer em uma jornada como `plan-pmo-corp`.

Para descobrir o ID da conversa, use o comando do runtime:

```text
/mm-conversations
```

Ou liste pelo terminal:

```bash
uv run python -m memory conversations
```

O ID pode ser completo ou apenas o prefixo, desde que esse prefixo identifique
uma única conversa existente. Com o ID em mãos, associe a conversa à jornada:

```bash
uv run python -m memory conversation-logger attach --conversation <conversation_id> --journey <journey_slug>
```

Exemplo:

```bash
uv run python -m memory conversation-logger attach --conversation 3fd487ca --journey plan-pmo-corp
```

Se você quer associar a sessão Pi mais recente, use:

```bash
uv run python -m memory conversation-logger attach-latest-pi --journey <journey_slug>
```

Exemplo:

```bash
uv run python -m memory conversation-logger attach-latest-pi --journey plan-pmo-corp
```

A diferença é simples: `attach` exige que você informe qual conversa quer
associar; `attach-latest-pi` escolhe automaticamente a sessão Pi mais recente.
Use `attach` para correções precisas ou conversas antigas. Use
`attach-latest-pi` logo após notar que a sessão Pi atual/recente ficou sem
jornada.

Ambos aceitam persona:

```bash
uv run python -m memory conversation-logger attach --conversation <conversation_id> --journey <journey_slug> --persona engineer
```

Para validar que funcionou, liste as conversas da jornada:

```bash
uv run python -m memory conversations --journey <journey_slug>
uv run python -m memory conversations --journey plan-pmo-corp
```

### 14.4 Recuperar uma conversa

Use este comando para carregar mensagens de uma conversa anterior.

```bash
uv run python -m memory recall <conversation_id>
```

Com limite de mensagens:

```bash
uv run python -m memory recall <conversation_id> --limit 20
```

Resultado esperado: o terminal mostra mensagens da conversa recuperada.

---

## 15. Tarefas

Tarefas transformam intenção em acompanhamento operacional.

### 15.1 Quando usar tarefas

Use tarefas quando houver uma ação clara. Use memórias para aprendizados, decisões e padrões. Use o `journey_path` para contexto vivo, roteiro e notas estruturadas.

Estados comuns de uma tarefa:

- `todo` ou pendente;
- `doing` ou em andamento;
- `blocked` ou bloqueada;
- `done` ou concluída.

### 15.2 Listar tarefas

Use este comando para listar todas as tarefas.

```bash
uv run python -m memory tasks list
```

Para listar tarefas de uma jornada:

```bash
uv run python -m memory tasks list --journey mirror-aprendizado
```

### 15.3 Criar tarefa

Use este comando para criar uma tarefa associada a uma jornada.

```bash
uv run python -m memory tasks add "Documentar comandos UV" --journey mirror-aprendizado
```

Resultado esperado: uma nova tarefa será criada para a jornada `mirror-aprendizado`.

### 15.4 Ver detalhes de uma tarefa

Depois de listar tarefas e obter o ID, use este comando para ver todos os detalhes.

```bash
uv run python -m memory tasks show <task_id>
```

Também é possível usar apenas o começo do ID, desde que esse prefixo identifique uma única tarefa.

```bash
uv run python -m memory tasks show <prefixo-do-id>
```

Resultado esperado: o comando mostra objetivo, ID, jornada, status, origem, etapa, prazo, horário, datas, contexto e metadados.

Exemplo de saída:

```text
📋 Tarefa

Objetivo: Melhorar cooldown do Gemini

Identificação:
- ID: `abc123...`
- Jornada: `proj-anota`
- Status: ○ todo
- Origem: conversation

Planejamento:
- Etapa: Fallback de transcrição
- Prazo: 2026-05-23
- Horário agendado: 2026-05-23T09:00
- Dica de horário: manhã

Datas:
- Criada em: 2026-05-22T...
- Atualizada em: 2026-05-22T...
- Concluída em: (not set)

Contexto:
Objetivo: evitar tentativas repetidas contra Gemini após quota.

Metadados:
(not set)
```

### 15.5 Atualizar estado de uma tarefa

Marcar como em andamento:

```bash
uv run python -m memory tasks doing <task_id>
```

Bloquear tarefa:

```bash
uv run python -m memory tasks block <task_id>
```

Concluir tarefa:

```bash
uv run python -m memory tasks done <task_id>
```

Apagar tarefa:

```bash
uv run python -m memory tasks delete <task_id>
```

### 15.6 Importar tarefas do documento vivo

Use este comando para importar checkboxes do `journey_path`.

```bash
uv run python -m memory tasks import mirror-aprendizado
```

Exemplo de checkboxes reconhecidos:

```markdown
- [ ] Criar documento inicial
- [x] Revisar comandos principais
```

---

## 16. Diário

O diário registra entradas livres, com ou sem jornada associada.

Para registrar uma entrada geral:

```bash
uv run python -m memory journal "Hoje aprendi um conceito importante."
```

Para registrar uma entrada associada a uma jornada:

```bash
uv run python -m memory journal --journey mirror-aprendizado "Hoje aprendi como consultar jornadas usando UV."
```

Resultado esperado: uma memória do tipo diário será criada.

---

## 17. Identidade

A identidade define o contexto permanente do Mirror.

### 17.1 Listar identidades

Use este comando para listar identidades no banco.

```bash
uv run python -m memory identity list
```

Para listar apenas uma camada:

```bash
uv run python -m memory identity list --layer persona
```

### 17.2 Ler uma identidade específica

Use este comando para ler uma entrada específica.

```bash
uv run python -m memory identity get journey mirror-aprendizado
```

Resultado esperado: o conteúdo da identidade da jornada será exibido.

### 17.3 Editar identidade

Use este comando para editar uma identidade no editor configurado.

```bash
uv run python -m memory identity edit user identity
```

> **Atenção:** editar identidade altera o comportamento futuro do Mirror. Faça isso com cuidado.

---

## 18. Personas

### 18.1 O que é uma persona

Uma persona é uma lente especializada. Ela orienta como o Mirror responde a determinado tipo de assunto.

A lista padrão desta instalação inclui:

- `coach` — hábitos, metas, consistência, execução;
- `designer` — design, UX/UI, marca, interface;
- `doctor` — saúde, sintomas, bem-estar, medicina;
- `engineer` — código, arquitetura, bugs, testes;
- `financial` — dinheiro, orçamento, investimentos, finanças;
- `prompt-engineer` — prompts, comportamento de LLM, instruções, arquivos de persona ou skill;
- `researcher` — pesquisa, evidências, síntese, investigação;
- `strategist` — estratégia, posicionamento, negócios, trade-offs;
- `teacher` — ensino, didática, explicação, aprendizagem;
- `therapist` — emoções, padrões, tensões, saúde mental;
- `thinker` — pensamento, conceitos, modelos, clareza;
- `writer` — escrita, edição, voz, publicação.

### 18.2 Quando uma persona é ativada

A persona é ativada quando o tema da conversa combina com palavras-chave e descritores de roteamento.

Exemplo: pedidos sobre código tendem a ativar `engineer`; pedidos sobre texto tendem a ativar `writer`; pedidos sobre emoções tendem a ativar `therapist`.

Quando uma persona aparece na resposta, o formato é:

```text
◇ engineer

[resposta]
```

Se nenhuma persona especializada for ativada, o `ego` responde sozinho e não há assinatura.

### 18.3 Ver personas existentes

Use este comando para listar personas com detalhes.

```bash
uv run python -m memory list personas --verbose
```

Forma simples:

```bash
uv run python -m memory list personas
```

### 18.4 Inspecionar, editar e testar personas

Inspecionar uma persona:

```bash
uv run python -m memory inspect persona writer
```

Editar uma persona existente:

```bash
uv run python -m memory identity edit persona writer
```

Criar ou substituir uma persona via `stdin`:

```bash
cat persona.md | uv run python -m memory identity set persona minha-persona
```

Gerar descritor de roteamento depois de alterar ou criar uma persona:

```bash
uv run python -m memory descriptor generate --layer persona --key minha-persona
```

Testar qual persona seria ativada por uma frase:

```bash
uv run python -m memory detect-persona "preciso organizar uma estratégia de negócio"
```

Listar conversas filtrando por persona:

```bash
uv run python -m memory conversations --persona engineer
```

---

## 19. Attachments

Attachments são documentos associados a uma jornada e guardados no banco SQLite.

Use este script para listar attachments de uma jornada.

```python
from memory import MemoryClient

with MemoryClient() as mem:
    attachments = mem.get_attachments("mirror-aprendizado")

    if not attachments:
        print("Nenhum attachment encontrado.")
    else:
        for att in attachments:
            print(f"- {att.name}")
            print(f"  ID: {att.id}")
            print(f"  Descrição: {att.description}")
            print(f"  Tipo: {att.content_type}")
            print()
```

Para executar diretamente pelo terminal:

```bash
uv run python - <<'PY'
from memory import MemoryClient

with MemoryClient() as mem:
    attachments = mem.get_attachments("mirror-aprendizado")

    if not attachments:
        print("Nenhum attachment encontrado.")
    else:
        for att in attachments:
            print(f"- {att.name}")
            print(f"  ID: {att.id}")
            print(f"  Descrição: {att.description}")
            print(f"  Tipo: {att.content_type}")
            print()
PY
```

Resultado esperado: o script lista todos os attachments associados à jornada `mirror-aprendizado`.

---

## 20. Modos de operação e comandos por runtime

O Mirror pode ser usado em diferentes runtimes. Os dois modos principais são `Mirror Mode` e `Builder Mode`.

### 20.1 Mirror Mode

Use `Mirror Mode` para reflexão, decisões, sentido, escrita, estratégia, emoções e continuidade pessoal.

Pi e Gemini CLI:

```text
/mm-mirror
```

Codex:

```text
$mm-mirror
```

Claude Code:

```text
/mm:mirror
```

### 20.2 Builder Mode

Use `Builder Mode` para construção: código, documentos, arquitetura, YAML, bugs, tarefas técnicas e artefatos.

Pi e Gemini CLI:

```text
/mm-build mirror-aprendizado
```

Codex:

```text
$mm-build mirror-aprendizado
```

Claude Code:

```text
/mm:build mirror-aprendizado
```

Pelo terminal:

```bash
uv run python -m memory build load mirror-aprendizado
```

### 20.3 Tabela de comandos por runtime

| Função | Pi/Gemini | Codex | Claude Code |
|---|---|---|---|
| Mirror Mode | `/mm-mirror` | `$mm-mirror` | `/mm:mirror` |
| Builder Mode | `/mm-build` | `$mm-build` | `/mm:build` |
| Jornadas | `/mm-journeys` | `$mm-journeys` | `/mm:journeys` |
| Jornada específica | `/mm-journey <slug>` | `$mm-journey <slug>` | `/mm:journey <slug>` |
| Memórias | `/mm-memories` | `$mm-memories` | `/mm:memories` |
| Conversas | `/mm-conversations` | `$mm-conversations` | `/mm:conversations` |
| Recall | `/mm-recall` | `$mm-recall` | `/mm:recall` |
| Tarefas | `/mm-tasks` | `$mm-tasks` | `/mm:tasks` |
| Diário | `/mm-journal` | `$mm-journal` | `/mm:journal` |
| Backup | `/mm-backup` | `$mm-backup` | `/mm:backup` |
| Ajuda | `/mm-help` | `$mm-help` | `/mm:help` |

---

## 21. Recursos avançados

### 21.1 Consultar outros modelos

O Mirror pode consultar outros LLMs via OpenRouter.

Use este comando para perguntar a um modelo da família `openai`.

```bash
uv run python -m memory consult openai "Qual seria uma boa estrutura para minha jornada de psicologia?"
```

Com jornada associada:

```bash
uv run python -m memory consult openai "Revise este plano" --journey mirror-aprendizado
```

Para ver créditos:

```bash
uv run python -m memory consult credits
```

> **Atenção:** consultas a LLMs externos podem gerar custo.

### 21.2 Consolidação de memórias

A consolidação identifica padrões recorrentes e propõe fusões ou atualizações.

Escanear consolidações:

```bash
uv run python -m memory consolidate scan
```

Listar propostas:

```bash
uv run python -m memory consolidate list
```

Aplicar uma proposta:

```bash
uv run python -m memory consolidate apply <id>
```

Rejeitar uma proposta:

```bash
uv run python -m memory consolidate reject <id>
```

### 21.3 Shadow

A camada `shadow` ajuda a registrar tensões, pontos cegos e padrões menos explícitos.

Escanear candidatos:

```bash
uv run python -m memory shadow scan
```

Listar candidatos:

```bash
uv run python -m memory shadow list
```

Ver detalhes:

```bash
uv run python -m memory shadow show <id>
```

Aplicar candidato:

```bash
uv run python -m memory shadow apply <id>
```

Rejeitar candidato:

```bash
uv run python -m memory shadow reject <id>
```

### 21.4 Extensões

Extensões adicionam capacidades ao Mirror sem modificar o core.

Tipos principais:

- `prompt-skill`: instruções em Markdown para orquestrar comandos existentes;
- `command-skill`: extensão com código, estado próprio e subcomandos.

Comandos básicos:

```bash
uv run python -m memory extensions list
uv run python -m memory extensions validate
uv run python -m memory extensions install <id> --extensions-root <diretorio>
uv run python -m memory ext list
uv run python -m memory ext <id> --help
```

### 21.5 Python API

Para scripts e extensões, use `MemoryClient`.

```python
from memory import MemoryClient

with MemoryClient() as mem:
    status = mem.get_journey_status("mirror-aprendizado")
    print(status)
```

Registrar uma entrada de diário por Python:

```python
from memory import MemoryClient

with MemoryClient() as mem:
    mem.add_journal(
        "Aprendi a consultar jornadas pelo UV.",
        journey="mirror-aprendizado",
    )
```

Pesquisar memórias por Python:

```python
from memory import MemoryClient

with MemoryClient() as mem:
    results = mem.search("comandos UV", journey="mirror-aprendizado")
    for result in results:
        print(result.memory.title, result.score)
```

---

## 22. Estrutura técnica do projeto

O código principal fica em:

```text
src/memory/
```

Subpastas importantes:

| Pasta | Função |
|---|---|
| `cli/` | comandos de terminal |
| `services/` | lógica de domínio |
| `storage/` | acesso ao SQLite |
| `intelligence/` | extração, busca e roteamento com LLM |
| `hooks/` | integrações com runtimes |
| `skills/` | lógica compartilhada por comandos e skills |

Direção de dependência:

```text
cli / hooks
  ↓
services
  ↓
storage
  ↓
db SQLite
```

---

## 23. Manutenção e segurança

### 23.1 Backup

Use este comando para criar um backup do banco de memória.

```bash
uv run python -m memory backup
```

Resultado esperado: o backup será salvo no diretório configurado, normalmente em:

```text
~/.mirror-minds/<usuario>/backups/
```

### 23.2 Patches locais

Patches locais guardam mudanças feitas no Mirror que ainda não estão commitadas ou que podem ser perdidas ao atualizar o repositório.

Nesta instalação, existe uma área para patches em:

```text
exports/patches/
```

#### Patch do comando tasks show

Foi criado um patch para preservar o comando:

```bash
uv run python -m memory tasks show <task_id>
```

Arquivos do patch:

```text
exports/patches/tasks-show-command.patch
exports/patches/tasks-show-command.README.md
```

Esse patch adiciona uma visualização amigável e completa dos detalhes de uma tarefa.

#### Testar antes de aplicar

Use este comando para verificar se o patch ainda pode ser aplicado.

```bash
git apply --check exports/patches/tasks-show-command.patch
```

Resultado esperado: se não houver erro, o patch está compatível.

#### Aplicar o patch

Use este comando para aplicar o patch.

```bash
git apply exports/patches/tasks-show-command.patch
```

Depois de aplicar, valide o comando:

```bash
uv run python -m memory tasks show <task_id>
```

Rode os testes relacionados:

```bash
uv run pytest tests/unit/memory/cli/test_tasks_cmd.py -q
uv run ruff check src/memory/cli/tasks_cmd.py tests/unit/memory/cli/test_tasks_cmd.py
```

#### Se o patch falhar

Se `git apply --check` falhar, provavelmente o repositório mudou nos mesmos arquivos. Nesse caso:

1. leia `exports/patches/tasks-show-command.README.md`;
2. abra `exports/patches/tasks-show-command.patch`;
3. reaplique manualmente a ideia do patch nos arquivos atuais;
4. rode os testes;
5. gere um novo patch atualizado.

Para gerar novamente o patch depois de ajustar:

```bash
git diff -- src/memory/cli/tasks_cmd.py src/memory/__main__.py tests/unit/memory/cli/test_tasks_cmd.py REFERENCE.md .pi/skills/mm-tasks/SKILL.md .claude/skills/mm:tasks/SKILL.md docs/manual-mirror-completo.md > exports/patches/tasks-show-command.patch
```

---

## 24. Boas práticas

### 24.1 Boas práticas para jornadas

- Use slugs curtos e em minúsculas, como `mirror-aprendizado`, `psicologia` ou `pmo-ti-jca`.
- Use uma jornada por frente importante.
- Coloque comandos, decisões e próximos passos no `journey_path` quando isso fizer sentido.
- Use memórias para aprendizados e decisões que devem sobreviver ao tempo.

### 24.2 Boas práticas para documentos vivos

Antes de atualizar um `journey_path`, consulte a jornada.

```bash
uv run python -m memory journey mirror-aprendizado
```

Depois, atualize com o conteúdo completo.

```bash
uv run python -m memory journey update mirror-aprendizado - <<'EOF'
[conteúdo antigo]

[conteúdo novo]
EOF
```

> **Atenção:** não envie apenas o trecho novo se a intenção for preservar o documento inteiro.

### 24.3 Boas práticas para arquivos de projeto

Arquivos de projeto são documentos e artefatos mantidos dentro do repositório ou pasta operacional de um projeto. Exemplos:

- `README.md`;
- `docs/next-steps.md`;
- `docs/decisions.md`;
- `docs/architecture.md`;
- guias de setup;
- planos técnicos;
- checklists de validação.

Eles não são a memória estratégica do Mirror. Eles são a documentação acionável que permite continuar a execução prática sem depender do histórico da conversa.

Atualize arquivos de projeto quando a informação orientar execução técnica futura, como:

- próximos passos técnicos;
- setup;
- arquitetura;
- decisões implementáveis;
- instruções de execução;
- pendências de código;
- validações;
- testes;
- comandos;
- integrações;
- documentação necessária para continuidade prática.

A diferença prática é:

- a jornada guarda intenção, decisões, direção estratégica, contexto de retomada, critérios de sucesso, mudanças importantes de rumo e acordos operacionais;
- os arquivos do projeto guardam detalhes técnicos acionáveis: como executar, validar, implementar, configurar, integrar e continuar o trabalho.

Exemplos de informações que vão na jornada:

- por que a frente existe e qual resultado importa;
- decisões estratégicas e mudanças relevantes de direção;
- critérios de sucesso e acordos operacionais;
- contexto sintético para retomada em sessões futuras;
- aprendizados ou padrões que devem permanecer na memória da jornada.

Exemplos de informações que vão em arquivos do projeto:

- comandos de instalação, teste, build, deploy ou validação;
- detalhes de arquitetura, integrações, APIs e configuração;
- próximos passos técnicos e pendências de código;
- decisões implementáveis que afetam arquivos, módulos ou runtime;
- documentação necessária para outro agente ou pessoa continuar a execução.

> **Boa prática:** quando uma informação for importante tanto para memória estratégica quanto para execução técnica, registre nos dois lugares: na jornada, de forma sintética e contextual; no arquivo do projeto, de forma operacional e acionável.

Antes de criar documentação nova, verifique se já existe um arquivo apropriado. Não crie documentação genérica desnecessária se o projeto já tiver estrutura própria.

### 24.4 Boas práticas para tarefas

- Crie tarefas com jornada associada sempre que possível.
- Use `doing`, `block` e `done` para manter estado claro.
- Importe checkboxes do `journey_path` quando fizer sentido.
- Use tarefas apenas para ações claras; não transforme toda ideia em tarefa.

### 24.5 Boas práticas de segurança

- Faça backups regularmente.
- Não edite o banco SQLite diretamente sem necessidade.
- Prefira comandos UV ou `MemoryClient`.
- Lembre que `.env` contém chaves privadas.
- Revise comandos destrutivos antes de executar.

---

## 25. Problemas comuns e como resolver

### O comando não encontra o módulo memory

Possível causa: você não está executando dentro do ambiente do projeto ou não está usando `uv run`.

Use:

```bash
uv run python -m memory journeys
```

### A jornada não aparece

Verifique se as identidades foram semeadas.

```bash
uv run python -m memory seed
uv run python -m memory journeys
```

### O documento vivo foi sobrescrito

O comando `journey update` substitui o conteúdo inteiro. Se você enviou apenas um trecho, o conteúdo anterior pode ter sido perdido.

> **Boa prática:** antes de atualizar, rode `uv run python -m memory journey <slug>` e copie o conteúdo atual.

### Não sei qual jornada usar

Liste as jornadas e leia as descrições.

```bash
uv run python -m memory journeys
```

Se nenhuma jornada corresponder ao tema, crie uma nova.

### Não sei qual persona foi usada

Durante a resposta, a persona aparece com assinatura como `◇ engineer`. Se não houver assinatura, o `ego` respondeu sozinho.

Você também pode listar conversas por persona:

```bash
uv run python -m memory conversations --persona engineer
```

### Um comando parece ambíguo

Mantenha o comando original, mas valide com `--help` quando disponível.

```bash
uv run python -m memory --help
uv run python -m memory tasks --help
uv run python -m memory identity --help
```

> **Observação:** alguns comandos podem variar conforme a versão local do Mirror.

### O patch local não aplica

Teste primeiro:

```bash
git apply --check exports/patches/tasks-show-command.patch
```

Se falhar, siga o procedimento da seção [Patches locais](#232-patches-locais).

---

## 26. Referências internas

Documentos úteis no repositório:

```text
README.md
REFERENCE.md
docs/getting-started.md
docs/architecture.md
docs/api.md
docs/product/extensions/index.md
docs/process/development-guide.md
```

---

## 27. Resumo operacional

O Mirror funciona melhor quando cada tipo de informação tem um lugar claro.

Use:

- `jornadas` para organizar temas e projetos importantes;
- `memórias` para aprendizados, decisões e padrões duradouros;
- `tarefas` para ações executáveis;
- `journey_path` para roteiro vivo e contexto estruturado;
- `conversas` para recuperar diálogos anteriores;
- `personas` para aplicar lentes especializadas;
- `attachments` para associar documentos a jornadas;
- `backup` para proteger a base local.

Comandos essenciais:

```bash
uv run python -m memory journeys
uv run python -m memory journey <slug>
uv run python -m memory memories --journey <slug>
uv run python -m memory conversations --journey <slug>
uv run python -m memory conversation-logger attach --conversation <conversation_id> --journey <slug>
uv run python -m memory conversation-logger attach-latest-pi --journey <slug>
uv run python -m memory recall <conversation_id>
uv run python -m memory tasks list --journey <slug>
uv run python -m memory journal --journey <slug> "Texto"
uv run python -m memory backup
```

> **Boa prática final:** comece simples. Crie uma jornada para cada frente importante, registre aprendizados como memórias, transforme ações em tarefas e mantenha os documentos vivos apenas quando eles realmente ajudarem na continuidade.
