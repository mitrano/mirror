# Padrão Geral — Geração de Simulados a partir de Provas Reais

Este arquivo registra diretrizes gerais para análise de provas reais, geração de simulados, criação de documentos e upload/compartilhamento. Ele vale para qualquer matéria, salvo quando houver um padrão específico da disciplina que complemente ou restrinja estas regras.

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
5. Apresentar entendimento inicial da estrutura da prova e das questões.
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

Deve conter uma instância de prompt para outra IA gerar um simulado igual ou melhor ao padrão validado para aquela prova/bimestre. O prompt deve separar claramente **estrutura avaliativa** de **conteúdo da revisão atual**. O prompt deve incluir:

- contexto do aluno;
- matéria, série e tipo de prova;
- padrão identificado na prova real;
- conteúdos da revisão atual que devem orientar o simulado;
- estrutura obrigatória do simulado;
- tipos de questão esperados;
- regras de linguagem e nível escolar;
- formato do gabarito comentado;
- critérios de qualidade antes da entrega;
- espaço explícito para colar a transcrição da revisão.

Regra contra contaminação: o prompt específico de uma prova/bimestre pode conter conteúdo daquela revisão, mas não deve ser usado diretamente em outra prova sem substituir integralmente o bloco de conteúdo pela revisão atual.

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
3. Identificar temas pouco trabalhados em simulados anteriores.
4. Identificar possíveis erros conceituais comuns.
5. Consultar o padrão geral e o padrão específico da matéria.
6. Quando existir, usar o template da matéria como base, preenchendo com a revisão atual.
7. Gerar simulado no padrão validado.
8. Gerar gabarito comentado.
9. Gerar `.docx` bem formatado.
10. Gerar script curto de upload em `.local/upload-scripts/`.
11. O script deve fazer upload para Google Drive e compartilhar com o e-mail padrão.

---

## 5. Regras gerais para simulados

Salvo orientação contrária, cada simulado deve:

1. Parecer uma prova escolar real.
2. Usar linguagem adequada à série do aluno.
3. Usar situações contextualizadas quando isso combinar com o padrão da matéria.
4. Evitar perguntas genéricas demais.
5. Evitar linguagem técnica acima do nível escolar.
6. Não inventar conteúdo fora da revisão ou do material informado.
7. Ter gabarito.
8. Ter gabarito comentado quando a prova for discursiva ou quando Ricardo pedir padrão de estudo.
9. Trabalhar temas não abordados ou pouco enfatizados quando for um novo simulado sobre a mesma revisão.

---

## 6. Gabarito comentado

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

## 7. Padrão geral do arquivo `.docx`

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

## 8. Scripts de upload

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

## 9. Upload e compartilhamento

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

## 10. Segurança

Não versionar arquivos sensíveis, como:

```text
google-oauth-credentials.json
.google-drive-token.json
```

Também remover ou ignorar arquivos `:Zone.Identifier`, que são metadados do Windows.

---

## 11. Persistência e verificação

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

## 12. Histórico estrutural

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

## 13. Regra para novas matérias

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

