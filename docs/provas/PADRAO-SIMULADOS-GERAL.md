# Padrão Geral — Geração de Simulados a partir de Provas Reais

Este arquivo registra diretrizes gerais para análise de provas reais, geração de simulados, criação de documentos e upload/compartilhamento. Ele vale para qualquer matéria, salvo quando houver um padrão específico da disciplina que complemente ou restrinja estas regras.

A formatação visual obrigatória dos simulados está registrada em:

```text
docs/provas/PADRAO-FORMATACAO-SIMULADOS.md
```

Esse padrão global de formatação deve ser aplicado a todos os simulados futuros, independentemente da matéria.

Padrões específicos por matéria devem ficar na pasta da matéria. Exemplo:

```text
docs/provas/ciencias/PADRAO-SIMULADOS.md
```

---

## 1. Estrutura de diretórios

A estrutura correta é:

```text
docs/provas/<materia>/<bimestre>/
```

Exemplos:

```text
docs/provas/ciencias/p1/
docs/provas/ciencias/p2/
docs/provas/historia/p1/
```

Arquivos de padrão geral ficam em:

```text
docs/provas/
```

Arquivos de padrão específico da matéria ficam em:

```text
docs/provas/<materia>/
```

Templates reutilizáveis de prompt da matéria ficam em:

```text
docs/provas/<materia>/PROMPT-TEMPLATE-SIMULADO.md
```

Materiais específicos de uma prova/bimestre ficam em:

```text
docs/provas/<materia>/<bimestre>/
```

---

## 2. Ordem geral do processo com prova real

Ao receber imagens de uma prova real:

1. Localizar ou criar a pasta correta em `docs/provas/<materia>/<bimestre>/`.
2. Extrair/transcrever as questões das imagens.
3. Salvar a transcrição das questões em um arquivo Markdown no diretório da prova:

```text
docs/provas/<materia>/<bimestre>/QUESTOES-EXTRAIDAS.md
```

4. Apresentar a transcrição para validação.
5. Apresentar entendimento inicial da estrutura da prova e das questões, incluindo quantidade total de questões, tipos de questão e tratamento da Questão de Excelência.
6. Aguardar validação/correção de Ricardo.
7. Só depois comparar prova real com a revisão/conteúdo estudado.
8. Identificar como a escola transforma conteúdo em pergunta.
9. Salvar a análise comparativa em um arquivo Markdown no diretório da prova:

```text
docs/provas/<materia>/<bimestre>/ANALISE-PROVA-REVISAO.md
```

10. Criar um prompt gerador de simulado em Markdown no diretório da prova:

```text
docs/provas/<materia>/<bimestre>/PROMPT-GERADOR-SIMULADO.md
```

11. Atualizar ou criar padrão específico da matéria, quando necessário.
12. Usar o padrão validado para gerar simulados futuros.

Regra importante: não comparar com a revisão antes de apresentar e validar as questões extraídas e a estrutura da prova.

---

## 3. Arquivos obrigatórios ao analisar prova real

Sempre que uma prova real for analisada a partir de imagens, gerar três arquivos no diretório da prova:

### 3.1. Questões extraídas

```text
docs/provas/<materia>/<bimestre>/QUESTOES-EXTRAIDAS.md
```

Deve conter:

- origem das imagens;
- observações de leitura ou partes cortadas/ilegíveis;
- todas as questões transcritas;
- observações validadas por Ricardo, como numeração especial ou ausência de questão.

### 3.2. Análise prova × revisão

```text
docs/provas/<materia>/<bimestre>/ANALISE-PROVA-REVISAO.md
```

Deve conter:

- arquivos de referência;
- visão geral dos temas da revisão;
- comparação questão por questão;
- como a revisão foi transformada em questão;
- habilidade cobrada em cada questão;
- matriz prova × revisão;
- padrão específico identificado;
- implicações para geração de simulados.

### 3.3. Prompt gerador de simulado

```text
docs/provas/<materia>/<bimestre>/PROMPT-GERADOR-SIMULADO.md
```

Deve conter uma instância de prompt para outra IA gerar um simulado igual ou melhor ao padrão validado para aquela prova/bimestre. O prompt deve separar claramente **estrutura avaliativa** de **conteúdo da revisão atual** e deve orientar o uso do controle de cobertura intrabimestre. O prompt deve incluir:

- contexto do aluno;
- matéria, série e tipo de prova;
- padrão identificado na prova real;
- conteúdos da revisão atual que devem orientar o simulado;
- estrutura obrigatória do simulado;
- tipos de questão esperados;
- regras de linguagem e nível escolar;
- formato do gabarito comentado;
- critérios de qualidade antes da entrega;
- regra para consultar `COBERTURA-SIMULADOS.md` antes de gerar o Simulado 02 ou superior;
- regra para priorizar temas, detalhes, exemplos e habilidades ainda não explorados nos simulados anteriores do mesmo bimestre;
- espaço explícito para colar a transcrição da revisão.

Regra contra contaminação: o prompt específico de uma prova/bimestre pode conter conteúdo daquela revisão, mas não deve ser usado diretamente em outra prova sem substituir integralmente o bloco de conteúdo pela revisão atual.

Regra contra rigidez temática: listas de temas, conteúdos ou eixos no prompt gerador são inventário de conteúdo disponível, não checklist obrigatório para todas as versões de simulado. Para o Simulado 02 ou superior, a cobertura intrabimestre tem prioridade sobre qualquer distribuição temática fixa. Não repetir mecanicamente todos os eixos centrais em todas as versões.

Quando a matéria passar a ter padrão próprio, criar também um template reutilizável em:

```text
docs/provas/<materia>/PROMPT-TEMPLATE-SIMULADO.md
```

O template da matéria deve conter apenas estrutura, regras e placeholders — não uma lista fixa de conteúdo de uma prova anterior.

Esses arquivos são parte do processo, não artefatos opcionais.

---

## 4. Ordem geral do processo para gerar simulado

Ao receber uma revisão/conteúdo para gerar simulado:

1. Ler a revisão.
2. Identificar temas centrais.
3. Criar ou consultar o controle de cobertura intrabimestre em:

```text
docs/provas/<materia>/<bimestre>/COBERTURA-SIMULADOS.md
```

4. Identificar temas, subtemas, detalhes, exemplos, contextos e habilidades já trabalhados nos simulados anteriores do mesmo bimestre/revisão.
5. Identificar temas e detalhes ainda não trabalhados ou pouco enfatizados dentro desse mesmo bimestre/revisão.
6. Identificar possíveis erros conceituais comuns.
7. Consultar o padrão geral, o padrão de formatação e o padrão específico da matéria.
8. Quando existir, usar o template da matéria como base, preenchendo com a revisão atual.
9. Definir explicitamente os focos novos do próximo simulado antes de gerar.
10. Para Simulado 02 ou superior, tratar listas de temas do prompt como inventário disponível, não como obrigação de cobrir todos os eixos novamente.
11. Gerar simulado no padrão validado, usando a cobertura para escolher a distribuição temática da versão.
12. Gerar gabarito comentado.
13. Gerar `.docx` bem formatado.
14. Atualizar `COBERTURA-SIMULADOS.md` com os temas/detalhes efetivamente usados no simulado gerado.
15. Gerar script curto de upload em `.local/upload-scripts/`.
16. O script deve fazer upload para Google Drive e compartilhar com o e-mail padrão.

---

## 5. Regras gerais para simulados

Salvo orientação contrária, cada simulado deve:

1. Parecer uma prova escolar real.
2. Preservar a quantidade e a estrutura de questões da prova real analisada para aquela matéria, incluindo a Questão de Excelência. Não assumir a quantidade de questões de outra matéria.
3. Usar linguagem adequada à série do aluno.
4. Usar situações contextualizadas quando isso combinar com o padrão da matéria.
5. Evitar perguntas genéricas demais.
6. Evitar linguagem técnica acima do nível escolar.
7. Não inventar conteúdo fora da revisão ou do material informado.
8. Ter gabarito.
9. Ter gabarito comentado quando a prova for discursiva ou quando Ricardo pedir padrão de estudo.
10. Trabalhar temas não abordados ou pouco enfatizados quando for um novo simulado sobre a mesma revisão.

---

## 6. Controle de cobertura intrabimestre

Para múltiplas versões de simulados dentro da mesma matéria e do mesmo bimestre/prova, deve existir um controle de cobertura em:

```text
docs/provas/<materia>/<bimestre>/COBERTURA-SIMULADOS.md
```

Esse arquivo serve para impedir que o Simulado 02, 03, 04 etc. repitam os mesmos focos do Simulado 01 sem necessidade.

### 6.1. Escopo

O controle de cobertura compara apenas simulados da **mesma matéria + mesmo bimestre + mesma revisão**.

Exemplos:

```text
docs/provas/filosofia/p2/COBERTURA-SIMULADOS.md
docs/provas/geografia/p2/COBERTURA-SIMULADOS.md
docs/provas/ingles/p2/COBERTURA-SIMULADOS.md
```

Não usar esse arquivo para comparar P1 com P2. A comparação é entre versões do mesmo bimestre:

```text
Simulado P2 01
Simulado P2 02
Simulado P2 03
```

### 6.2. O que registrar

O arquivo deve conter:

1. inventário hierárquico dos temas e detalhes da revisão atual;
2. marcadores visuais de cobertura tanto nos temas principais quanto nos subtemas/detalhes;
3. tabela por simulado gerado;
4. para cada questão:
   - tema;
   - subtema/detalhe;
   - exemplo ou contexto usado;
   - tipo de questão;
   - habilidade cobrada;
5. lista de temas/detalhes ainda não usados ou pouco explorados.

Usar esta legenda de cobertura:

```text
○ não explorado
◐ explorado parcialmente
● bem explorado
```

Regras:

- o símbolo deve aparecer no tema principal e em cada subtema/detalhe;
- o símbolo do tema principal representa a cobertura geral daquele eixo;
- o símbolo do subtema/detalhe representa o uso específico daquele item;
- quando um item for usado, registrar ao lado onde apareceu, por exemplo `S01-Q03`;
- se um tema estiver `●`, evitar repeti-lo sem novo ângulo, salvo quando for conceito central obrigatório.

Modelo reutilizável:

```text
docs/provas/TEMPLATE-COBERTURA-SIMULADOS.md
```

Modelo mínimo:

```markdown
# Cobertura de Simulados — <Matéria> <Bimestre>

## Inventário da revisão com cobertura

Legenda:

- ○ não explorado
- ◐ explorado parcialmente
- ● bem explorado

### ○ 1. Tema central 1

- ○ detalhe/subtema 1
- ○ detalhe/subtema 2

### ○ 2. Tema central 2

- ○ detalhe/subtema 1
- ○ detalhe/subtema 2

## Simulado 01

| Questão | Tema | Detalhe | Contexto/exemplo | Habilidade |
|---|---|---|---|---|
| Q01 | ... | ... | ... | ... |

## Temas e detalhes ainda pouco explorados

- ...
```

### 6.3. Regra para novos simulados

Antes de gerar o Simulado 02 ou superior:

1. ler os simulados anteriores do mesmo bimestre;
2. consultar ou atualizar `COBERTURA-SIMULADOS.md`;
3. identificar os temas, detalhes, exemplos e habilidades já usados;
4. definir os focos novos do próximo simulado;
5. só então gerar o novo simulado.

A regra não é “nunca repetir tema”. Alguns conceitos centrais precisam aparecer em mais de um simulado. A regra correta é:

> Se repetir um tema central, mudar o detalhe, o exemplo, o contexto ou a habilidade cobrada.

Para o Simulado 02 ou superior, a cobertura intrabimestre deve prevalecer sobre listas fixas de temas do prompt gerador. Essas listas representam o universo de conteúdo da revisão, não uma exigência de que toda versão cubra todos os eixos centrais novamente.

Assim:

- Simulado 01 pode fazer uma cobertura mais ampla dos eixos da revisão;
- Simulado 02 ou superior deve priorizar lacunas, detalhes pouco explorados, novos exemplos e novas habilidades;
- não transformar “temas da revisão” em checklist rígido repetido em todas as versões;
- manter obrigatórios apenas a quantidade/estrutura da prova real, o padrão da matéria, a revisão como limite de conteúdo, a questão de excelência quando existir, gabarito e formatação.

### 6.4. Checklist antes de finalizar novo simulado

Antes de entregar um novo simulado do mesmo bimestre, verificar:

1. a quantidade e estrutura seguem a prova real da matéria?
2. os tipos de questão seguem o padrão específico da matéria?
3. quais temas já apareceram nos simulados anteriores?
4. quais detalhes já apareceram?
5. quais exemplos/contextos já foram usados?
6. o novo simulado traz focos novos ou pouco explorados?
7. conceitos repetidos aparecem com novo ângulo?
8. `COBERTURA-SIMULADOS.md` foi atualizado após a geração?

---

## 7. Gabarito comentado

Quando houver gabarito comentado, usar para cada questão:

```text
Resposta esperada:
[resposta modelo]

Comentário:
[critério simples de correção]
```

O comentário deve explicar o que torna a resposta correta, parcialmente correta ou inadequada.

Para questões discursivas, não tratar a resposta modelo como frase única obrigatória. Aceitar variações quando o conceito estiver correto.

---

## 8. Padrão geral do arquivo `.docx`

Sempre que Ricardo pedir para gerar um simulado, gerar também o arquivo `.docx` respectivo.

O padrão visual obrigatório para **todos os simulados de todas as matérias** é o padrão validado no `simulado-p2-artes-04.docx`.

### 7.1. Fonte e tamanhos obrigatórios

Usar **Arial** como fonte base do documento.

Aplicar os tamanhos abaixo:

| Elemento | Tamanho | Estilo |
|---|---:|---|
| Título principal da prova | 16 pt | Negrito |
| Subtítulo / identificação da prova | 11 pt | Negrito |
| Cabeçalho de nome, turma e data | 11 pt | Negrito |
| Título de questão | 13 pt | Negrito |
| Enunciado das questões | 11 pt | Normal |
| Banco de palavras / instruções auxiliares | 10 pt | Negrito |
| Campo “Resposta:” | 10 pt | Negrito |
| Linhas de resposta | 10 pt | Normal |
| Título do gabarito comentado | 16 pt | Negrito |
| Título das questões no gabarito | 12 pt | Negrito |
| Rótulos “Resposta esperada:” e “Comentário:” | 10 pt | Negrito |
| Texto da resposta esperada | 11 pt | Normal |
| Texto do comentário | 10 pt | Normal |

Regra prática: corpo do simulado em **11 pt normal**, títulos de questão em **13 pt negrito**, títulos principais em **16 pt negrito** e elementos auxiliares/rótulos em **10 pt**. Não gerar o documento inteiro em negrito.

### 7.2. Estrutura e diagramação

O documento deve ter:

1. Cabeçalho claro.
2. Nome, turma e data.
3. Boa diagramação.
4. Margens adequadas.
5. Espaçamento entre questões.
6. Campo “Resposta:” quando houver resposta discursiva.
7. Linhas adequadas para resposta, usando 93 underscores por linha:

```text
_____________________________________________________________________________________________
```

8. Tabelas reais quando houver Coluna A / Coluna B.
9. Gabarito em nova página.
10. Nome de arquivo claro e consistente.

Evitar `.docx` gerado de forma pobre, sem espaçamento ou com colunas quebradas.

### 7.3. Regras obrigatórias de negrito

Não gerar o documento inteiro em negrito.

Usar negrito apenas em:

1. Título principal da prova.
2. Subtítulo / identificação da prova.
3. Cabeçalho de nome, turma e data.
4. Título de questão, como `Questão 01`.
5. Títulos de seções estruturais, como `TEXT I`, quando existirem.
6. Letras isoladas de subitens somente quando estiverem sozinhas por necessidade estrutural.
7. Banco de palavras / caixas de apoio.
8. Rótulos `Resposta:`, `Resposta esperada:` e `Comentário:`.
9. Título do gabarito comentado.
10. Títulos das questões dentro do gabarito.

Não usar negrito em:

1. Texto corrido dos enunciados.
2. Textos de leitura.
3. Alternativas comuns.
4. Frases que o aluno deve completar.
5. Linhas de resposta com underscores.
6. Texto da resposta esperada.
7. Texto do comentário do gabarito.

### 7.4. Regras obrigatórias para subitens

Quando uma questão tiver subitens com letra e pergunta curta, a letra e o texto devem ficar na **mesma linha**.

Formato correto:

```text
a. Where did Emma meet her friends?
```

Formato incorreto:

```text
a.
Where did Emma meet her friends?
```

Aplicar esta regra para todos os subitens `a.`, `b.`, `c.`, etc., em qualquer matéria.

Só separar a letra em linha própria quando o subitem for composto por bloco longo, tabela, imagem, múltiplas linhas ou quando a separação melhorar claramente a legibilidade.

### 7.5. Regras obrigatórias de espaçamento

O padrão de espaçamento do `.docx` deve seguir o `simulado-p2-artes-04.docx`:

| Elemento | Antes | Depois | Linha |
|---|---:|---:|---:|
| Título principal | 0 | 40 | 269 |
| Subtítulo | 0 | 160 | 269 |
| Cabeçalho de nome/turma/data | 0 | 200 | 269 |
| Título de questão | 200 | 80 | 269 |
| Primeira linha de enunciado após título | 0 | 80 | 269 |
| Continuação de enunciado | 0 | 120 | 269 |
| Campo `Resposta:` | 0 | 40 | 269 |
| Linha de resposta | 0 | 20 | 269 |
| Título do gabarito | 0 | 200 | 269 |
| Rótulos do gabarito | 0 | 0 | 269 |

Não aplicar espaçamento único genérico em todos os parágrafos. O espaçamento deve variar conforme o tipo de elemento.

### 7.6. Checklist obrigatório antes de entregar o `.docx`

Antes de entregar qualquer simulado em `.docx`, verificar:

1. O documento não está inteiro em negrito.
2. O corpo dos enunciados está em Arial 11 pt normal.
3. Os títulos de questão estão em Arial 13 pt negrito.
4. O título principal está em Arial 16 pt negrito.
5. Os rótulos de resposta estão em Arial 10 pt negrito.
6. As linhas de resposta estão em Arial 10 pt normal.
7. Subitens curtos estão na mesma linha da pergunta: `a. Pergunta...`.
8. Não há cabeçalho duplicado de nome/turma/data.
9. O espaçamento segue o padrão por tipo de elemento, não um espaçamento único para tudo.
10. O gabarito começa em nova página.

---

## 9. Scripts de upload

Sempre que gerar um `.docx` de simulado, gerar também script curto de upload.

Os scripts devem ficar em:

```text
.local/upload-scripts/
```

Eles são temporários/local-only e não precisam ser versionados.

Regra definida por Ricardo:

- scripts de upload não precisam ficar versionados;
- podem ser removidos um dia depois de criados;
- quando forem criados, devem ficar em pasta específica;
- não misturar scripts temporários com as provas nem com scripts permanentes do projeto.

A pasta `.local/upload-scripts/` deve permanecer no `.gitignore`.

---

## 10. Upload e compartilhamento

O upload para Google Drive deve usar OAuth.

Não pedir, não armazenar e não usar usuário/senha Google.

Sempre que fizer upload de simulado, compartilhar automaticamente com:

```text
nicolas.25438231@aluno.pensi.com.br
```

Permissão:

```text
writer
```

O script curto deve usar parâmetros equivalentes a:

```bash
--share-with nicolas.25438231@aluno.pensi.com.br --role writer
```

---

## 11. Segurança

Não versionar arquivos sensíveis, como:

```text
google-oauth-credentials.json
.google-drive-token.json
```

Também remover ou ignorar arquivos `:Zone.Identifier`, que são metadados do Windows.

---

## 12. Persistência e verificação

Sempre que um padrão importante for definido, ele deve ser persistido em arquivo Markdown e, quando relevante, referenciado na jornada correspondente.

Para verificar a jornada:

```bash
uv run python -m memory journey <slug-da-jornada>
```

Para verificar padrões gerais:

```bash
ls docs/provas/PADRAO-SIMULADOS-GERAL.md
```

Para verificar padrões específicos:

```bash
find docs/provas -maxdepth 3 -name 'PADRAO-SIMULADOS*.md' -print
```

---

## 13. Histórico estrutural

Houve uma correção estrutural na jornada `analise-provas-7ano`.

Estrutura antiga, incorreta:

```text
docs/provas/p1/ciencias/
```

Estrutura correta:

```text
docs/provas/ciencias/p1/
```

Motivo: a organização correta é primeiro por matéria e depois por bimestre/prova.

Se algum caminho antigo aparecer no futuro, tratá-lo como legado e corrigir.
---

## 14. Regra para novas matérias

Quando uma nova matéria for trabalhada pela primeira vez, seguir obrigatoriamente este processo:

1. Usar este padrão geral apenas para o que vale para todas as matérias.
2. Analisar a estrutura da prova real da nova matéria.
3. Comparar a prova real com a revisão/conteúdo da nova matéria.
4. Identificar o padrão específico daquela disciplina: tipos de questão, comandos, formato, linguagem, habilidades cobradas e forma de transformar revisão em prova.
5. Criar um padrão específico da matéria em:

```text
docs/provas/<materia>/PADRAO-SIMULADOS.md
```

6. Criar um template reutilizável da matéria em:

```text
docs/provas/<materia>/PROMPT-TEMPLATE-SIMULADO.md
```

7. Manter no padrão geral somente o que se aplica a todas as matérias.
8. Manter no padrão específico apenas o que pertence àquela disciplina.
9. Não copiar automaticamente o padrão específico de uma matéria para outra.
10. Para cada bimestre/prova, criar o prompt específico em:

```text
docs/provas/<materia>/<bimestre>/PROMPT-GERADOR-SIMULADO.md
```

Regra central: **o geral organiza o processo; o específico define como aquela matéria pergunta; o conteúdo vem da revisão atual.**

