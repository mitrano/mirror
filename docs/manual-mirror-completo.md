# Manual Completo do Mirror Mind

Este documento é um guia prático para usar o Mirror Mind no dia a dia: conceitos, instalação, comandos UV, jornadas, memórias, personas, tarefas e modos de operação.

---

## Índice

<details>
<summary>O que é o Mirror Mind</summary>

- [Abrir seção](#1-o-que-é-o-mirror-mind)

</details>

<details>
<summary>Componentes principais</summary>

- [Abrir seção](#2-componentes-principais)
- [Identidade](#identidade)
- [Jornadas](#jornadas)
- [Journey path](#journey-path)

</details>

<details>
<summary>Instalação básica</summary>

- [Abrir seção](#3-instalação-básica)
- [Instalar dependências](#instalar-dependências)
- [Configurar ambiente](#configurar-ambiente)
- [Inicializar usuário](#inicializar-usuário)
- [Semear identidade no banco](#semear-identidade-no-banco)
- [Verificar instalação](#verificar-instalação)

</details>

<details>
<summary>Comandos UV essenciais</summary>

- [Abrir seção](#4-comandos-uv-essenciais)
- [Listar jornadas](#listar-jornadas)
- [Consultar uma jornada](#consultar-uma-jornada)
- [Criar jornada](#criar-jornada)
- [Atualizar journey path](#atualizar-journey-path)
- [Associar jornada a uma pasta](#associar-jornada-a-uma-pasta)
- [Carregar contexto em Builder Mode](#carregar-contexto-em-builder-mode)

</details>

<details>
<summary>Memórias</summary>

- [Abrir seção](#5-memórias)
- [Listar memórias](#listar-memórias)
- [Filtrar por jornada](#filtrar-por-jornada)
- [Pesquisar memórias](#pesquisar-memórias)
- [Pesquisar dentro de uma jornada](#pesquisar-dentro-de-uma-jornada)

</details>

<details>
<summary>Conversas</summary>

- [Abrir seção](#6-conversas)
- [Listar conversas recentes](#listar-conversas-recentes)
- [Filtrar por jornada](#filtrar-por-jornada-1)
- [Limitar quantidade](#limitar-quantidade)
- [Recuperar conversa específica](#recuperar-conversa-específica)

</details>

<details>
<summary>Attachments</summary>

- [Abrir seção](#7-attachments)
- [Listar attachments de uma jornada](#listar-attachments-de-uma-jornada)

</details>

<details>
<summary>Diário</summary>

- [Abrir seção](#8-diário)
- [Registrar entrada de diário](#registrar-entrada-de-diário)
- [Registrar diário associado a uma jornada](#registrar-diário-associado-a-uma-jornada)

</details>

<details>
<summary>Tarefas</summary>

- [Abrir seção](#9-tarefas)
- [Listar tarefas](#listar-tarefas)
- [Listar tarefas de uma jornada](#listar-tarefas-de-uma-jornada)
- [Criar tarefa](#criar-tarefa)
- [Ver detalhes completos de uma tarefa](#ver-detalhes-completos-de-uma-tarefa)
- [Marcar tarefa como em andamento](#marcar-tarefa-como-em-andamento)
- [Bloquear tarefa](#bloquear-tarefa)
- [Concluir tarefa](#concluir-tarefa)
- [Apagar tarefa](#apagar-tarefa)
- [Importar tarefas do journey path](#importar-tarefas-do-journey-path)

</details>

<details>
<summary>Identidade</summary>

- [Abrir seção](#10-identidade)
- [Listar identidades](#listar-identidades)
- [Listar por camada](#listar-por-camada)
- [Ler registro específico](#ler-registro-específico)
- [Editar identidade](#editar-identidade)
- [Como o Mirror aprende quem é o usuário](#como-o-mirror-aprende-quem-é-o-usuário)
- [Como fornecer melhor a própria identidade](#como-fornecer-melhor-a-própria-identidade)
- [Como checar o que o Mirror já sabe](#como-checar-o-que-o-mirror-já-sabe)

</details>

<details>
<summary>Personas</summary>

- [Abrir seção](#11-personas)
- [O que é uma persona](#o-que-é-uma-persona)
- [Quando uma persona é ativada](#quando-uma-persona-é-ativada)
- [Diferença entre persona e jornada](#diferença-entre-persona-e-jornada)
- [Quais personas padrão existem](#quais-personas-padrão-existem)
- [Como a persona aparece numa resposta](#como-a-persona-aparece-numa-resposta)
- [Ver personas existentes](#ver-personas-existentes)
- [Inspecionar persona](#inspecionar-persona)
- [Editar ou criar personas](#editar-ou-criar-personas)
- [Detectar persona para uma frase](#detectar-persona-para-uma-frase)
- [Saber qual persona foi usada numa conversa](#saber-qual-persona-foi-usada-numa-conversa)

</details>

<details>
<summary>Mirror Mode e Builder Mode</summary>

- [Abrir seção](#12-mirror-mode-e-builder-mode)
- [Mirror Mode](#mirror-mode)
- [Builder Mode](#builder-mode)

</details>

<details>
<summary>Comandos por runtime</summary>

- [Abrir seção](#13-comandos-por-runtime)

</details>

<details>
<summary>Backup</summary>

- [Abrir seção](#14-backup)
- [Criar backup](#criar-backup)

</details>

<details>
<summary>Consultar outros modelos</summary>

- [Abrir seção](#15-consultar-outros-modelos)

</details>

<details>
<summary>Consolidação e sombra</summary>

- [Abrir seção](#16-consolidação-e-sombra)
- [Consolidação de memórias](#consolidação-de-memórias)
- [Shadow](#shadow)

</details>

<details>
<summary>Estrutura técnica</summary>

- [Abrir seção](#17-estrutura-técnica)

</details>

<details>
<summary>Python API</summary>

- [Abrir seção](#18-python-api)

</details>

<details>
<summary>Extensões</summary>

- [Abrir seção](#19-extensões)

</details>

<details>
<summary>Patches locais</summary>

- [Abrir seção](#20-patches-locais)
- [Patch do comando `tasks show`](#patch-do-comando-tasks-show)
- [Como testar antes de aplicar](#como-testar-antes-de-aplicar)
- [Como aplicar o patch](#como-aplicar-o-patch)
- [Se o patch falhar](#se-o-patch-falhar)

</details>

<details>
<summary>Boas práticas</summary>

- [Abrir seção](#21-boas-práticas)
- [Para jornadas](#para-jornadas)
- [Para atualizações de journey path](#para-atualizações-de-journey-path)
- [Para arquivos de projeto](#para-arquivos-de-projeto)
- [Para tarefas](#para-tarefas)
- [Para segurança](#para-segurança)

</details>

<details>
<summary>Referências internas</summary>

- [Abrir seção](#22-referências-internas)

</details>

<details>
<summary>Resumo rápido</summary>

- [Abrir seção](#23-resumo-rápido)

</details>

---

## 1. O que é o Mirror Mind

[Voltar ao índice](#índice)

O Mirror Mind é um framework local-first de memória, identidade e continuidade para agentes de IA. Ele permite que conversas, decisões, aprendizados, projetos e padrões pessoais sejam preservados ao longo do tempo.

Em vez de cada chat começar do zero, o Mirror usa uma base local com:

- identidade do usuário;
- personas especializadas;
- jornadas/projetos;
- memórias extraídas de conversas;
- tarefas;
- histórico de conversas;
- documentos vivos chamados `journey_path`.

A base principal fica em SQLite, normalmente em:

```text
~/.mirror-minds/<usuario>/memory.db
```

---

## 2. Componentes principais

[Voltar ao índice](#índice)

### Identidade

A identidade define quem é o usuário e como o Mirror deve operar. Ela é organizada em camadas:

| Camada | Função |
|---|---|
| `self` | identidade profunda, visão de mundo, propósito |
| `ego` | comportamento operacional, tom e postura |
| `user` | dados e contexto do usuário |
| `persona` | lentes especializadas, como engineer, writer, therapist etc. |
| `shadow` | tensões, pontos cegos e padrões recorrentes |
| `journey` | identidade de uma jornada |
| `journey_path` | documento vivo de acompanhamento da jornada |

A identidade não é descoberta de uma vez. O Mirror forma uma imagem do usuário por camadas: algumas explícitas, algumas inferidas a partir das conversas, e outras consolidadas ao longo do tempo. A regra central é: o Mirror aprende melhor quando o usuário não fornece apenas fatos sobre sua vida, mas também mostra como interpreta, escolhe, sente, prioriza e dá sentido ao que vive.

A camada de identidade pode registrar, por exemplo:

- visão de mundo;
- valores e princípios;
- vontade, direção e ambições;
- modo de decidir;
- estilo de comunicação;
- forma de trabalhar;
- padrões emocionais;
- medos, tensões e contradições recorrentes;
- estética pessoal e maneira de estar no mundo;
- relações importantes;
- critérios para uma vida bem vivida;
- como o Mirror deve falar, confrontar, lembrar e apoiar o usuário.

### Jornadas

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

### Journey path

O `journey_path` é o documento vivo da jornada. Ele funciona como uma página de acompanhamento, manual ou roteiro prático.

Importante: o comando `journey update` substitui o conteúdo inteiro do `journey_path`. Para não apagar conteúdo antigo, primeiro consulte a jornada, copie o conteúdo atual, adicione a nova parte e atualize com o conteúdo completo.

---

## 3. Instalação básica

[Voltar ao índice](#índice)

### Instalar dependências

```bash
git clone https://github.com/viniciusteles/mirror.git
cd mirror
uv sync
```

### Configurar ambiente

```bash
cp .env.example .env
```

No `.env`, configure pelo menos:

```env
MIRROR_USER=seu-nome
OPENROUTER_API_KEY=sk-or-...
```

### Inicializar usuário

```bash
uv run python -m memory init seu-nome
```

### Semear identidade no banco

```bash
uv run python -m memory seed
```

### Verificar instalação

```bash
uv run python -m memory list personas --verbose
uv run python -m memory list journeys
uv run python -m memory detect-persona "quero ajuda para escrever um artigo"
```

---

## 4. Comandos UV essenciais

[Voltar ao índice](#índice)

Todos os comandos abaixo devem ser executados na pasta do repositório Mirror.

### Listar jornadas

```bash
uv run python -m memory journeys
```

Lista as jornadas existentes.

```bash
uv run python -m memory list journeys
```

Também lista jornadas pela interface geral de listagem.

### Consultar uma jornada

```bash
uv run python -m memory journey mirror-aprendizado
```

Mostra o estado completo da jornada: identidade, journey path, memórias recentes e conversas recentes.

```bash
uv run python -m memory journey status mirror-aprendizado
```

Forma equivalente de consultar status de uma jornada.

### Criar jornada

```bash
uv run python -m memory journey create psicologia \
  --name "Psicologia" \
  --description "Estudos e reflexões sobre psicologia." \
  --briefing "Usar esta jornada para temas ligados à psicologia." \
  --context "Jornada criada para organizar aprendizados, leituras e práticas."
```

Cria uma nova jornada.

### Atualizar journey path

```bash
uv run python -m memory journey update mirror-aprendizado "Novo conteúdo do journey path."
```

Substitui o conteúdo vivo da jornada.

Para textos maiores:

```bash
uv run python -m memory journey update mirror-aprendizado - <<'EOF'
## Área nova

Conteúdo novo aqui.
EOF
```

### Associar jornada a uma pasta

```bash
uv run python -m memory journey set-path mirror-aprendizado /caminho/da/pasta
```

Associa a jornada a um diretório local/projeto.

### Carregar contexto em Builder Mode

```bash
uv run python -m memory build load mirror-aprendizado
```

Carrega contexto da jornada para construção técnica ou edição de artefatos.

---

## 5. Memórias

[Voltar ao índice](#índice)

### Listar memórias

```bash
uv run python -m memory memories
```

### Filtrar por jornada

```bash
uv run python -m memory memories --journey mirror-aprendizado
```

### Pesquisar memórias

```bash
uv run python -m memory memories --search "comandos"
```

### Pesquisar dentro de uma jornada

```bash
uv run python -m memory memories --journey mirror-aprendizado --search "comandos"
```

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

## 6. Conversas

[Voltar ao índice](#índice)

### Listar conversas recentes

```bash
uv run python -m memory conversations
```

### Filtrar por jornada

```bash
uv run python -m memory conversations --journey mirror-aprendizado
```

### Limitar quantidade

```bash
uv run python -m memory conversations --journey mirror-aprendizado --limit 10
```

### Associar uma conversa existente a uma jornada

Use este helper quando uma conversa já existe no banco, mas não ficou associada
à jornada correta. Isso é útil, por exemplo, quando você começou uma sessão no
Pi antes de escolher a jornada, ou quando percebeu depois que uma conversa sobre
`plan-pmo-corp` ficou sem vínculo de jornada.

Primeiro descubra o ID da conversa com:

```text
/mm-conversations
```

ou pelo terminal:

```bash
uv run python -m memory conversations
```

Depois associe a conversa à jornada. O ID pode ser completo ou apenas um
prefixo, desde que esse prefixo resolva para uma conversa existente e única:

```bash
uv run python -m memory conversation-logger attach --conversation <conversation_id> --journey <journey_slug>
```

Exemplo:

```bash
uv run python -m memory conversation-logger attach --conversation 3fd487ca --journey plan-pmo-corp
```

Se a conversa a corrigir for a sessão Pi mais recente, use o helper curto:

```bash
uv run python -m memory conversation-logger attach-latest-pi --journey <journey_slug>
```

Exemplo:

```bash
uv run python -m memory conversation-logger attach-latest-pi --journey plan-pmo-corp
```

Diferença prática:

- `attach` associa uma conversa específica informada por ID ou prefixo;
- `attach-latest-pi` associa automaticamente a sessão Pi mais recente.

Ambos aceitam persona:

```bash
uv run python -m memory conversation-logger attach --conversation <conversation_id> --journey <journey_slug> --persona engineer
```

Para validar:

```bash
uv run python -m memory conversations --journey <journey_slug>
uv run python -m memory conversations --journey plan-pmo-corp
```

### Recuperar conversa específica

```bash
uv run python -m memory recall <conversation_id>
```

Com limite de mensagens:

```bash
uv run python -m memory recall <conversation_id> --limit 20
```

---

## 7. Attachments

[Voltar ao índice](#índice)

Attachments são documentos ou conteúdos associados a uma jornada e guardados no banco SQLite do Mirror.

### Listar attachments de uma jornada

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

Lista todos os attachments associados à jornada `mirror-aprendizado`.

---

## 8. Diário

[Voltar ao índice](#índice)

### Registrar entrada de diário

```bash
uv run python -m memory journal "Hoje aprendi um conceito importante."
```

### Registrar diário associado a uma jornada

```bash
uv run python -m memory journal --journey mirror-aprendizado "Hoje aprendi como consultar jornadas usando UV."
```

---

## 9. Tarefas

[Voltar ao índice](#índice)

Tarefas são ações práticas associadas ao uso do Mirror. Elas servem para transformar uma jornada em acompanhamento operacional: o contexto da jornada diz **o que é importante**, as memórias registram **o que foi aprendido ou decidido**, e as tarefas mostram **o que precisa ser feito agora ou depois**.

Uma tarefa pode existir sem jornada, mas fica mais útil quando vinculada a uma jornada específica. Assim, cada frente de trabalho ou aprendizado mantém sua própria lista de próximos passos. Por exemplo, na jornada `mirror-aprendizado`, uma tarefa pode ser "Documentar comandos UV"; em uma jornada de projeto, pode ser "Revisar briefing" ou "Criar plano da próxima entrega".

As tarefas ajudam a:

- manter próximos passos visíveis;
- separar ideias e aprendizados de ações executáveis;
- acompanhar o estado de cada ação;
- organizar pendências por jornada;
- importar checkboxes do `journey_path` para a lista de tarefas;
- evitar que decisões importantes fiquem perdidas no histórico da conversa.

Estados comuns de uma tarefa:

- **pendente** — ainda precisa ser feita;
- **em andamento** — já começou;
- **bloqueada** — depende de algo antes de avançar;
- **concluída** — já foi finalizada.

Na prática, use tarefas quando houver uma ação clara. Use memórias para aprendizados, decisões e padrões que devem sobreviver ao tempo. Use o `journey_path` para contexto vivo, roteiro e notas estruturadas da jornada.

### Listar tarefas

```bash
uv run python -m memory tasks list
```

### Listar tarefas de uma jornada

```bash
uv run python -m memory tasks list --journey mirror-aprendizado
```

### Criar tarefa

```bash
uv run python -m memory tasks add "Documentar comandos UV" --journey mirror-aprendizado
```

### Ver detalhes completos de uma tarefa

Depois de listar as tarefas de uma jornada e obter o ID da tarefa, use:

```bash
uv run python -m memory tasks show <task_id>
```

Também é possível usar apenas o começo do ID, desde que esse prefixo identifique uma única tarefa:

```bash
uv run python -m memory tasks show <prefixo-do-id>
```

Esse comando mostra uma visão amigável e completa da tarefa, incluindo:

- objetivo/título da tarefa;
- ID completo;
- jornada associada;
- status atual;
- origem da tarefa;
- etapa/ciclo da jornada, quando houver;
- prazo;
- horário agendado;
- dica de horário;
- data de criação;
- data da última atualização;
- data de conclusão, quando houver;
- contexto detalhado;
- metadados internos.

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

Use `tasks show` quando quiser ver “tudo, tudo, tudo” de uma tarefa em formato legível, sem precisar consultar diretamente o SQLite ou usar Python manualmente.

### Marcar tarefa como em andamento

```bash
uv run python -m memory tasks doing <task_id>
```

### Bloquear tarefa

```bash
uv run python -m memory tasks block <task_id>
```

### Concluir tarefa

```bash
uv run python -m memory tasks done <task_id>
```

### Apagar tarefa

```bash
uv run python -m memory tasks delete <task_id>
```

### Importar tarefas do journey path

```bash
uv run python -m memory tasks import mirror-aprendizado
```

O import lê checkboxes no `journey_path`, por exemplo:

```markdown
- [ ] Criar documento inicial
- [x] Revisar comandos principais
```

---

## 10. Identidade

[Voltar ao índice](#índice)

### Listar identidades

```bash
uv run python -m memory identity list
```

### Listar por camada

```bash
uv run python -m memory identity list --layer persona
```

### Ler registro específico

```bash
uv run python -m memory identity get journey mirror-aprendizado
```

### Editar identidade

```bash
uv run python -m memory identity edit user identity
```

### Como o Mirror aprende quem é o usuário

O Mirror não aprende a identidade do usuário como um formulário preenchido uma vez. Ele a constrói por acúmulo, correção e consolidação.

Os principais canais são:

1. **Identidade** — guarda verdades relativamente estáveis sobre o usuário: visão de mundo, valores, princípios, tom, postura, estilo de decisão, modo de trabalhar, presença pessoal e critérios de vida.
2. **Conversas** — funcionam como material bruto. Nelas aparecem decisões, conflitos, desejos, projetos, pessoas importantes, linguagem natural, prioridades e padrões de interpretação.
3. **Memórias** — preservam sínteses reutilizáveis extraídas ou registradas: aprendizados, decisões, ideias, compromissos, tensões, padrões e reflexões.
4. **Diário** — registra material íntimo e contextual que não aparece em tarefas: sentimentos, ambivalências, desejos, vergonha, fé, vontade, dúvidas e contradições.
5. **Jornadas** — mostram onde a vida ou o trabalho do usuário está se movendo. Elas guardam continuidade por frente, projeto ou tema importante.
6. **Shadow** — registra tensões, pontos cegos e padrões recorrentes menos explícitos. Não é uma camada de defeitos; é uma camada de material psíquico e comportamental que precisa ser visto com cuidado.

A conversa é o material bruto. A memória é a síntese. A identidade é o que deve orientar comportamento futuro. A jornada é o espaço de continuidade. O shadow é o lugar das tensões recorrentes.

### Como fornecer melhor a própria identidade

Para que o Mirror aprenda a operar de forma parecida com a presença real do usuário, use quatro formas de alimentação.

#### 1. Declarações diretas

Use frases explícitas quando quiser que algo seja lembrado ou transformado em identidade:

```text
Memorize isto sobre mim:
- Eu valorizo...
- Eu não suporto...
- Eu quero construir...
- Eu tenho medo de...
- Eu tendo a reagir assim quando...
- Eu quero que você me lembre disso quando eu esquecer...
```

#### 2. Retratos longos

Textos longos são úteis para formar contexto profundo. Bons temas:

```text
Quem sou eu hoje.
Como eu penso.
O que eu quero da vida.
O que eu acredito.
Como eu trabalho.
Como eu amo.
Como eu lido com conflito.
Como eu tomo decisões.
Como eu quero envelhecer.
O que eu quero preservar em mim.
O que eu quero transformar.
Como quero que o Mirror fale comigo.
O que quero que o Mirror confronte em mim.
```

#### 3. Situações concretas

A identidade real aparece em situação, especialmente quando há custo, conflito ou escolha. Em vez de registrar apenas um valor abstrato, descreva episódios concretos:

```text
Quando aconteceu X, eu senti Y, pensei Z e decidi W.
```

Isso ajuda o Mirror a entender não só o valor declarado, mas como ele se encarna no mundo material.

#### 4. Correção ativa

Quando o Mirror errar a imagem do usuário, corrija explicitamente:

```text
Não, isso não parece comigo. Eu não penso assim. O mais correto seria...
```

Ou:

```text
Você acertou uma parte, mas faltou isto...
```

Essa correção é uma das formas mais fortes de aprendizado, porque ajusta a representação diretamente.

### Como checar o que o Mirror já sabe

Use estes comandos para auditar identidade, memórias, conversas e jornadas:

```bash
uv run python -m memory identity list
uv run python -m memory identity get user identity
uv run python -m memory memories
uv run python -m memory memories --search "Ricardo"
uv run python -m memory conversations
uv run python -m memory journeys
```

No Pi, os atalhos equivalentes são:

```text
/mm-identity
/mm-memories
/mm-conversations
/mm-journeys
/mm-journey mirror-aprendizado
```

Uma boa prática é construir um dossiê vivo do usuário com seções como:

1. Quem sou eu.
2. O que eu quero.
3. O que eu acredito.
4. Meus valores e princípios.
5. Meu jeito de pensar.
6. Meu jeito de trabalhar.
7. Meu jeito de me relacionar.
8. Meus padrões emocionais.
9. Minhas tensões recorrentes.
10. O que quero que o Mirror preserve em mim.
11. O que quero que o Mirror confronte em mim.
12. Como o Mirror deve soar quando fala comigo.

A frase guia é: o Mirror aprende melhor quando o usuário não dá apenas informações sobre sua vida, mas também mostra como dá sentido à própria vida.

---

## 11. Personas

[Voltar ao índice](#índice)

### O que é uma persona

Uma persona é uma lente especializada da identidade do Mirror. Ela não é outro assistente separado: é o mesmo Mirror operando com um foco específico, como engenharia, escrita, estratégia, saúde, finanças ou reflexão emocional.

### Quando uma persona é ativada

A persona é ativada quando o tema da conversa combina com as palavras-chave e o descritor de roteamento daquela persona. Por exemplo, pedidos sobre código tendem a ativar `engineer`; pedidos sobre texto tendem a ativar `writer`; pedidos sobre emoções tendem a ativar `therapist`.

### Diferença entre persona e jornada

- **persona** define a lente de resposta: como o Mirror pensa aquele assunto;
- **jornada** define o espaço de continuidade: onde contexto, memórias, tarefas e documentos daquele tema/projeto ficam organizados.

### Quais personas padrão existem

As personas padrão disponíveis nesta instalação são:

- `coach` — hábitos, metas, consistência, execução;
- `designer` — design, UX/UI, marca, interface;
- `doctor` — saúde, sintomas, bem-estar, medicina;
- `engineer` — código, arquitetura, bugs, testes;
- `financial` — dinheiro, orçamento, investimentos, finanças;
- `prompt-engineer` — prompts, comportamento de LLM, instruções, arquivos de persona/skill;
- `researcher` — pesquisa, evidências, síntese, investigação;
- `strategist` — estratégia, posicionamento, negócios, trade-offs;
- `teacher` — ensino, didática, explicação, aprendizagem;
- `therapist` — emoções, padrões, tensões, saúde mental;
- `thinker` — pensamento, conceitos, modelos, clareza;
- `writer` — escrita, edição, voz, publicação.

### Como a persona aparece numa resposta

Quando uma persona está ativa numa resposta, ela pode aparecer com assinatura no formato:

```text
◇ engineer

[resposta]
```

Se nenhuma persona especializada for ativada, o ego responde sozinho e não há assinatura.

### Ver personas existentes

```bash
uv run python -m memory list personas --verbose
```

Lista as personas existentes no banco do Mirror com mais detalhes, incluindo `routing_keywords`.

```bash
uv run python -m memory list personas
```

Mostra uma lista mais simples das personas disponíveis.

### Inspecionar persona

```bash
uv run python -m memory inspect persona writer
```

Inspeciona uma persona específica. Troque `writer` por outra persona, como `engineer`, `therapist` ou `strategist`.

### Editar ou criar personas

Para editar uma persona existente:

```bash
uv run python -m memory identity edit persona writer
```

Para criar ou substituir uma persona via stdin:

```bash
cat persona.md | uv run python -m memory identity set persona minha-persona
```

Depois de alterar ou criar uma persona, gere novamente os descritores se quiser que o roteamento automático reflita melhor o novo conteúdo:

```bash
uv run python -m memory descriptor generate --layer persona --key minha-persona
```

### Detectar persona para uma frase

```bash
uv run python -m memory detect-persona "preciso organizar uma estratégia de negócio"
```

Testa qual persona o Mirror ativaria para uma frase.

### Saber qual persona foi usada numa conversa

Durante a resposta, a persona aparece com a assinatura `◇ nome-da-persona` quando uma persona especializada está ativa. Se não houver assinatura, o ego respondeu sozinho.

Para listar conversas filtrando por persona:

```bash
uv run python -m memory conversations --persona engineer
```

Para recuperar uma conversa e verificar as mensagens:

```bash
uv run python -m memory recall <conversation_id>
```

A lista real vem do banco SQLite do seu Mirror, então ela pode variar conforme sua identidade foi seeded/editada.

---

## 12. Mirror Mode e Builder Mode

[Voltar ao índice](#índice)

### Mirror Mode

Mirror Mode é usado para reflexão, decisões, sentido, escrita, estratégia, emoções e continuidade pessoal.

Em Pi/Gemini:

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

### Builder Mode

Builder Mode é usado para construção: código, documentos, arquitetura, YAML, bugs, tarefas técnicas e artefatos.

Em Pi/Gemini:

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

Pelo UV:

```bash
uv run python -m memory build load mirror-aprendizado
```

---

## 13. Comandos por runtime

[Voltar ao índice](#índice)

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

## 14. Backup

[Voltar ao índice](#índice)

### Criar backup

```bash
uv run python -m memory backup
```

O backup é salvo no diretório configurado, normalmente:

```text
~/.mirror-minds/<usuario>/backups/
```

---

## 15. Consultar outros modelos

[Voltar ao índice](#índice)

O Mirror pode consultar outros LLMs via OpenRouter.

```bash
uv run python -m memory consult openai "Qual seria uma boa estrutura para minha jornada de psicologia?"
```

Com jornada:

```bash
uv run python -m memory consult openai "Revise este plano" --journey mirror-aprendizado
```

Ver créditos:

```bash
uv run python -m memory consult credits
```

---

## 16. Consolidação e sombra

[Voltar ao índice](#índice)

### Consolidação de memórias

```bash
uv run python -m memory consolidate scan
uv run python -m memory consolidate list
uv run python -m memory consolidate apply <id>
uv run python -m memory consolidate reject <id>
```

A consolidação identifica padrões recorrentes e propõe fusões ou atualizações.

### Shadow

```bash
uv run python -m memory shadow scan
uv run python -m memory shadow list
uv run python -m memory shadow show <id>
uv run python -m memory shadow apply <id>
uv run python -m memory shadow reject <id>
```

A camada shadow ajuda a registrar tensões, pontos cegos e padrões menos explícitos.

---

## 17. Estrutura técnica

[Voltar ao índice](#índice)

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
| `intelligence/` | extração, busca, roteamento com LLM |
| `hooks/` | integrações com runtimes |
| `skills/` | lógica compartilhada por comandos/skills |

A direção de dependência é:

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

## 18. Python API

[Voltar ao índice](#índice)

Para scripts e extensões, use `MemoryClient`:

```python
from memory import MemoryClient

with MemoryClient() as mem:
    status = mem.get_journey_status("mirror-aprendizado")
    print(status)
```

Exemplos úteis:

```python
from memory import MemoryClient

with MemoryClient() as mem:
    mem.add_journal(
        "Aprendi a consultar jornadas pelo UV.",
        journey="mirror-aprendizado",
    )
```

```python
from memory import MemoryClient

with MemoryClient() as mem:
    results = mem.search("comandos UV", journey="mirror-aprendizado")
    for result in results:
        print(result.memory.title, result.score)
```

---

## 19. Extensões

[Voltar ao índice](#índice)

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

---

## 20. Patches locais

[Voltar ao índice](#índice)

Patches locais guardam mudanças feitas no Mirror que ainda não estão commitadas ou que podem ser perdidas ao atualizar o repositório. Eles funcionam como um arquivo de reaplicação: se uma atualização do repositório remover uma melhoria local, o patch permite aplicar novamente a mudança.

Nesta instalação, existe uma área para patches em:

```text
exports/patches/
```

### Fluxo genérico para aplicar qualquer patch

Use este fluxo para qualquer arquivo `.patch` dentro de `exports/patches/`.
Antes de aplicar, trabalhe em uma árvore limpa ou salve suas mudanças locais com
commit/stash, para conseguir desfazer com segurança se houver conflito.

#### 1. Listar patches disponíveis

```bash
find exports/patches -maxdepth 1 -type f -name '*.patch' | sort
```

Se existir um arquivo `.README.md` com o mesmo tema do patch, leia antes de
aplicar. Exemplo:

```bash
less exports/patches/tasks-show-command.README.md
```

#### 2. Escolher o patch

```bash
PATCH="exports/patches/NOME-DO-PATCH.patch"
```

Exemplos reais:

```bash
PATCH="exports/patches/tasks-show-command.patch"
PATCH="exports/patches/0001-Document-helpers-for-attaching-conversations-to-jour.patch"
```

#### 3. Identificar o tipo de patch

Existem dois formatos comuns:

1. **Patch simples de diff**, geralmente gerado com `git diff` e aplicado com
   `git apply`.
2. **Patch de commit**, geralmente gerado com `git format-patch` e aplicado com
   `git am` para preservar mensagem, autor e metadados do commit.

Para inspecionar rapidamente:

```bash
head -20 "$PATCH"
```

Se o arquivo começar com linhas como `From <hash> ...`, `From:`, `Date:` e
`Subject:`, provavelmente é um patch de commit. Se começar direto com
`diff --git`, normalmente é um patch simples de diff.

#### 4. Testar compatibilidade antes de aplicar

```bash
git apply --check "$PATCH"
```

Se não houver saída, o patch é compatível com a árvore atual. Se houver erro,
não aplique automaticamente: leia o erro, confira quais arquivos mudaram e veja
a seção “Se o patch falhar”.

#### 5. Aplicar o patch

Para patch simples de diff:

```bash
git apply "$PATCH"
```

Para patch de commit, preferencial quando o patch veio de `git format-patch`:

```bash
git am "$PATCH"
```

Se você não quiser preservar o commit de um patch `format-patch`, também pode
aplicar apenas as alterações com:

```bash
git apply "$PATCH"
```

#### 6. Validar depois de aplicar

```bash
git status --short
git diff --stat
```

Depois rode as validações específicas do patch. Se o patch alterar código
Python, normalmente rode testes e lint relacionados, por exemplo:

```bash
uv run pytest <caminho-dos-testes> -q
uv run ruff check <arquivos-alterados>
```

Se o patch alterar apenas documentação Markdown, uma checagem simples costuma
ser suficiente:

```bash
git diff --check
```

#### 7. Aplicar todos os patches de uma pasta, quando fizer sentido

Só faça isso quando você souber que todos os patches são desejados e compatíveis
entre si. Primeiro teste todos:

```bash
for PATCH in exports/patches/*.patch; do
  echo "Checking $PATCH"
  git apply --check "$PATCH" || exit 1
done
```

Depois aplique um por vez, escolhendo `git apply` ou `git am` conforme o tipo de
cada patch. Evite aplicar tudo automaticamente se houver mistura de patches de
diff e patches de commit.

#### 8. Se o patch falhar

Se `git apply --check "$PATCH"` falhar, provavelmente o repositório mudou nos
mesmos arquivos. Nesse caso:

1. leia qualquer `.README.md` associado ao patch;
2. abra o arquivo `.patch` e entenda quais arquivos/trechos ele altera;
3. reaplique manualmente a intenção do patch nos arquivos atuais;
4. rode testes, lint ou checagens de documentação conforme o tipo da mudança;
5. gere um novo patch atualizado se quiser preservar a reaplicação futura.

Se `git am "$PATCH"` falhar no meio da aplicação, use uma das opções abaixo:

```bash
git am --abort      # cancela a aplicação do patch de commit
git am --continue   # continua depois de resolver conflitos manualmente
```

### Patch do comando `tasks show`

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

### Como testar antes de aplicar

Depois de atualizar o repositório do Mirror, teste se o patch ainda pode ser aplicado:

```bash
git apply --check exports/patches/tasks-show-command.patch
```

Se esse comando não mostrar erro, o patch está compatível.

### Como aplicar o patch

```bash
git apply exports/patches/tasks-show-command.patch
```

Depois de aplicar, valide o comando:

```bash
uv run python -m memory tasks show <task_id>
```

E rode os testes relacionados:

```bash
uv run pytest tests/unit/memory/cli/test_tasks_cmd.py -q
uv run ruff check src/memory/cli/tasks_cmd.py tests/unit/memory/cli/test_tasks_cmd.py
```

### Se o patch falhar

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

## 21. Boas práticas

[Voltar ao índice](#índice)

### Para jornadas

- Use slugs curtos e em minúsculas: `mirror-aprendizado`, `psicologia`, `pmo-ti-jca`.
- Use uma jornada por frente importante.
- Coloque comandos, decisões e próximos passos no `journey_path`.
- Use memórias para aprendizados e decisões que devem sobreviver ao tempo.

### Para atualizações de journey path

Antes de atualizar:

```bash
uv run python -m memory journey mirror-aprendizado
```

Depois atualize com o conteúdo completo:

```bash
uv run python -m memory journey update mirror-aprendizado - <<'EOF'
[conteúdo antigo]

[conteúdo novo]
EOF
```

### Para arquivos de projeto

Arquivos de projeto são os documentos e artefatos mantidos dentro do repositório ou pasta operacional de um projeto: `README.md`, `docs/next-steps.md`, `docs/decisions.md`, `docs/architecture.md`, guias de setup, planos técnicos, checklists de validação e equivalentes. Eles não são a memória estratégica do Mirror; são a documentação acionável que permite continuar a execução prática sem depender do histórico da conversa.

Atualize arquivos de projeto quando a informação orientar execução técnica futura: próximos passos técnicos, setup, arquitetura, decisões implementáveis, instruções de execução, pendências de código, validações, testes, comandos, integrações ou documentação necessária para continuidade prática. Antes de registrar algo, verifique se já existe um arquivo apropriado, como `README.md`, `docs/next-steps.md`, `docs/decisions.md`, `docs/architecture.md` ou equivalente. Não crie documentação genérica desnecessária quando o projeto já tiver estrutura própria.

A diferença prática é esta:

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

Quando uma informação for importante tanto para memória estratégica quanto para execução técnica, registre nos dois lugares: na jornada, em forma sintética e contextual; no arquivo do projeto, em forma operacional e acionável. Se houver um documento vivo da jornada, como um Markdown associado, atualize-o quando a informação fizer parte do manual ou processo de uso do Mirror, não apenas quando for uma nota temporária do projeto.

### Para tarefas

- Crie tarefas com jornada associada sempre que possível.
- Use `doing`, `block` e `done` para manter estado claro.
- Importe checkboxes do `journey_path` quando fizer sentido.

### Para segurança

- Faça backups regularmente.
- Não edite o banco SQLite diretamente sem necessidade.
- Prefira comandos UV ou `MemoryClient`.
- Lembre que `.env` contém chaves privadas.

---

## 22. Referências internas

[Voltar ao índice](#índice)

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

## 23. Resumo rápido

[Voltar ao índice](#índice)

Comandos mais usados:

```bash
uv run python -m memory journeys
uv run python -m memory journey <slug>
uv run python -m memory journey create <slug> --name "Nome" --description "Descrição"
uv run python -m memory journey update <slug> - <<'EOF'
Conteúdo
EOF
uv run python -m memory memories --journey <slug>
uv run python -m memory conversations --journey <slug>
uv run python -m memory conversation-logger attach --conversation <conversation_id> --journey <slug>
uv run python -m memory conversation-logger attach-latest-pi --journey <slug>
uv run python -m memory tasks list --journey <slug>
uv run python -m memory journal --journey <slug> "Texto"
uv run python -m memory backup
```

O Mirror funciona melhor quando cada tema importante vira uma jornada, cada aprendizado importante vira memória e cada plano prático fica claro no `journey_path`.
