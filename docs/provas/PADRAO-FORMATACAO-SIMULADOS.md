# Padrão Global de Formatação — Simulados

Este arquivo define o padrão visual e estrutural que deve ser usado em **todos os simulados gerados**, independentemente da matéria.

Referência visual adotada: `docs/provas/artes/p2/simulados/simulado-p2-artes-04.md`.

---

## 1. Cabeçalho

Todo simulado deve iniciar com título em H1:

```text
# SIMULADO — <MATÉRIA> — <PROVA/BIMESTRE> — <NÚMERO>
```

Exemplo:

```text
# SIMULADO — GEOGRAFIA — P2 — 01
```

Logo abaixo, usar a linha de identificação em uma única linha:

```text
Nome: ___________________________________________  Turma: ___________________  Data: ____ / ____ / _______
```

Depois, inserir separador:

```text
---
```

---

## 2. Títulos de questões

Cada questão deve usar H2:

```text
## Questão 01
```

Para questão de excelência, usar:

```text
## Questão de Excelência / Questão 07
```

quando ela corresponder a uma questão numerada específica, ou:

```text
## Questão de Excelência
```

quando a prova não indicar numeração equivalente.

---

## 3. Espaçamento entre blocos

Usar linha em branco entre:

- título da questão e enunciado;
- parágrafos do enunciado;
- enunciado e `Resposta:`;
- `Resposta:` e as linhas de resposta;
- linhas de resposta;
- fim da questão e separador `---`.

Cada questão deve terminar com:

```text
---
```

Exceto a última questão antes do gabarito, que também pode terminar com `---` para separar do gabarito.

---

## 4. Enunciados

Os enunciados devem seguir o padrão:

1. contexto curto, quando houver;
2. pergunta principal em negrito, quando for útil destacar o comando;
3. linguagem clara e adequada ao 7º ano;
4. comandos objetivos: explique, cite, identifique, indique, compare, complete, circule, associe.

Exemplo:

```text
Uma pessoa colocou uma pasta plástica roxa na frente da mão e ainda conseguiu enxergar parcialmente através dela.

**Explique o que essa comparação mostra sobre pigmentos transparentes e pigmentos opacos.**
```

---

## 5. Respostas discursivas

Para questões discursivas, usar:

```text
Resposta:

_____________________________________________________________________________________________

_____________________________________________________________________________________________

_____________________________________________________________________________________________
```

A linha de resposta deve ter exatamente 93 underscores:

```text
_____________________________________________________________________________________________
```

Manter uma linha em branco entre as linhas de resposta, como no simulado de referência.

Quantidade recomendada:

- resposta curta: 2 linhas;
- resposta média: 3 linhas;
- resposta de excelência: 4 linhas;
- questão muito simples: 1 linha, se suficiente.

---

## 6. Questões com itens

Quando houver itens, usar letras minúsculas seguidas de ponto:

```text
a. Texto do item __________________________.

b. Texto do item __________________________.
```

Para questões com subrespostas discursivas, usar:

```text
### a. Título ou item

Resposta:

_____________________________________________________________________________________________
```

---

## 7. Banco de palavras e lacunas

Para questões de completar, usar:

```text
**Complete as lacunas com as palavras da caixa:**

**Banco de palavras:** palavra — palavra — palavra — palavra

 a. Frase com lacuna __________________________.
```

As lacunas internas de frases podem usar underscores curtos:

```text
__________________________
```

---

## 8. Listas e instruções

Quando houver instruções, usar lista com hífen:

```text
Instruções:

- primeira instrução;
- segunda instrução;
- terceira instrução.
```

---

## 9. Gabarito comentado

O gabarito deve começar com H1:

```text
# GABARITO COMENTADO
```

Cada questão do gabarito deve usar H2:

```text
## Questão 01
```

Para cada questão, usar exatamente esta estrutura:

```text
Resposta esperada:
[resposta modelo]

Comentário:
[critério simples de correção]
```

Não usar listas excessivamente complexas no gabarito, salvo quando a questão pedir itens.

---

## 10. Tabelas, associações em colunas, esquemas e blocos visuais

Quando uma questão usar tabela no Markdown, o arquivo `.docx` **não pode** mostrar a tabela como texto cru com barras verticais (`|`).

No Word, a tabela deve ser convertida para **tabela real**, com:

- bordas visíveis;
- cabeçalho em negrito;
- fonte Calibri 11 pt no conteúdo;
- espaçamento interno suficiente para leitura;
- largura ajustada à página;
- linhas de resposta dentro das células preservadas quando houver lacunas.

Exemplo incorreto no `.docx`:

```text
| Situação | Fator climático |
|---|---|
| Área próxima ao oceano | ____________________ |
```

Exemplo correto no `.docx`: uma tabela real com duas colunas, uma para `Situação` e outra para `Fator climático`.

Se a ferramenta usada para gerar o `.docx` não conseguir criar tabela real, reescrever a questão em formato de lista antes de gerar o Word.

### 10.1. Questões de associação em duas colunas

Quando uma questão pedir associação entre letras/opções e descrições, o `.docx` deve colocar os blocos **lado a lado em duas colunas**, e não um abaixo do outro.

Formato obrigatório no Word:

- tabela real sem aparência pesada;
- duas colunas;
- coluna esquerda: opções com letras, por exemplo `A. Equatorial`;
- coluna direita: lacunas para preencher, por exemplo `(   ) Temperaturas mais amenas...`;
- cabeçalhos opcionais, como `Tipos climáticos` e `Características`;
- bordas podem ser invisíveis ou finas, desde que a organização em duas colunas fique clara;
- fonte 11 pt;
- largura ajustada à página.

Exemplo visual desejado:

```text
Tipos climáticos                         Características
A. Equatorial                            (   ) Quente e úmido...
B. Tropical típico                       (   ) Estação seca e chuvosa...
C. Tropical de altitude                  (   ) Temperaturas mais amenas...
D. Subtropical                           (   ) Estações do ano mais definidas...
```

Evitar no `.docx`:

```text
A. Equatorial
B. Tropical típico
C. Tropical de altitude
D. Subtropical

(   ) ...
(   ) ...
(   ) ...
```

Esse formato vertical só é aceitável no Markdown de trabalho; no Word deve virar duas colunas.

### 10.2. Esquemas e blocos visuais

Quando uma questão trouxer esquema, diagrama textual, fluxo, código visual ou bloco explicativo destacado no Markdown, o `.docx` deve envolver esse bloco em uma **moldura/quadro** para diferenciar do restante do enunciado.

Exemplos de blocos que devem virar moldura no Word:

```text
CERRADO
clima tropical típico
+ estação seca e chuvosa
+ vegetação adaptada
```

ou:

```text
ELEMENTOS NATURAIS
clima + relevo + solo + vegetação + hidrografia
          ↓
DOMÍNIOS MORFOCLIMÁTICOS
```

No Word, usar uma tabela de uma célula ou caixa equivalente, com:

- borda visível, mas fina;
- espessura de borda recomendada em OOXML: `w:sz="5"`;
- largura menor que a largura útil da página, deixando recuo lateral maior;
- largura recomendada em OOXML: aproximadamente `w:w="7600"` e tabela centralizada;
- espaçamento interno;
- fonte 10 ou 11 pt;
- espaço antes/depois para não colar no enunciado.

---

## 11. Tom visual geral

O simulado deve parecer uma prova escolar limpa, legível e bem espaçada.

Evitar:

- blocos de texto longos demais;
- tabelas em texto cru no `.docx`;
- excesso de Markdown complexo;
- enunciados colados nas linhas de resposta;
- linhas de resposta com tamanho diferente do padrão global;
- falta de separador entre questões.

---

## 12. Propriedades obrigatórias do documento Word `.docx`

Além do Markdown, todo arquivo `.docx` de simulado deve seguir as propriedades visuais extraídas do documento de referência:

```text
docs/provas/artes/p2/simulados/simulado-p2-artes-04.docx
```

### 12.1. Página

Usar:

- tamanho da página: **Carta / Letter**;
- largura: **8,5 pol.**;
- altura: **11 pol.**;
- orientação: **retrato**.

Em OOXML, isso corresponde a:

```text
<w:pgSz w:w="12240" w:h="15840"/>
```

### 12.2. Margens

Usar margens compactas, como no simulado de Artes 04:

- superior: **0,55 pol.** / aproximadamente **1,40 cm**;
- inferior: **0,55 pol.** / aproximadamente **1,40 cm**;
- esquerda: **0,65 pol.** / aproximadamente **1,65 cm**;
- direita: **0,65 pol.** / aproximadamente **1,65 cm**;
- cabeçalho: **0,50 pol.**;
- rodapé: **0,50 pol.**.

Em OOXML:

```text
<w:pgMar w:top="792" w:right="936" w:bottom="792" w:left="936" w:header="720" w:footer="720" w:gutter="0"/>
```

### 12.3. Fonte

Usar a fonte padrão do Word/Google Docs equivalente ao tema **minorHAnsi**, visualmente equivalente a **Calibri**.

Quando a ferramenta de geração exigir uma fonte explícita, usar:

```text
Calibri
```

### 12.4. Tamanhos de fonte

Usar os seguintes tamanhos:

| Elemento | Tamanho |
|---|---:|
| Título principal do documento Word | **16 pt** |
| Subtítulo do documento Word | **11 pt** |
| Linha de nome/turma/data | **11 pt** |
| Título da questão | **13 pt** |
| Enunciado/contexto | **11 pt** |
| Pergunta em destaque | **11 pt** |
| Lista de instruções | **11 pt** |
| Rótulo `Resposta:` | **10 pt** |
| Linhas de resposta | **10 pt** |
| Gabarito comentado | seguir 11 pt no corpo e 13 pt nos títulos |

Em OOXML, lembrar que `w:sz` usa meio-ponto. Exemplos:

```text
16 pt = w:sz 32
13 pt = w:sz 26
11 pt = w:sz 22
10 pt = w:sz 20
```

### 12.5. Alinhamento

Usar:

- título principal: **centralizado**;
- subtítulo: **centralizado**;
- linha de nome/turma/data: alinhamento à esquerda;
- questões, enunciados e respostas: alinhamento à esquerda.

### 12.6. Espaçamento entre linhas

Usar espaçamento próximo de **1,12** entre linhas, conforme o documento de referência.

Em OOXML:

```text
<w:spacing w:line="269" w:lineRule="auto"/>
```

Se a ferramenta não permitir 1,12 exatamente, usar **simples** ou **1,1**, evitando espaçamento duplo.

### 12.7. Espaçamento antes/depois de parágrafos

Usar o seguinte padrão aproximado:

| Elemento | Antes | Depois |
|---|---:|---:|
| Título principal | 0 pt | 2 pt |
| Subtítulo | 0 pt | 8 pt |
| Nome/turma/data | 0 pt | 10 pt |
| Título da questão | 10 pt | 4 pt |
| Parágrafo de contexto/enunciado | 0 pt | 4 pt |
| Pergunta em destaque | 0 pt | 6 pt |
| `Resposta:` | 0 pt | 2 pt |
| Cada linha de resposta | 0 pt | 1 pt |
| Itens de lista | 0 pt | 1 pt |

Em OOXML, referências do simulado de Artes 04:

```text
before="200" ≈ 10 pt
after="200"  ≈ 10 pt
after="160"  ≈ 8 pt
after="120"  ≈ 6 pt
after="80"   ≈ 4 pt
after="40"   ≈ 2 pt
after="20"   ≈ 1 pt
```

### 12.8. Negrito

Usar negrito para:

- título principal;
- títulos das questões;
- pergunta principal quando destacada no enunciado;
- rótulo `Resposta:`;
- títulos do gabarito.

Não usar negrito excessivo no corpo do texto.

### 12.9. Título interno do `.docx`

No Word, preferir o cabeçalho visual do modelo de Artes 04:

```text
Prova de <Matéria> — 7º ano
<Px> — <tema/resumo da revisão> — Simulado <NN>
Nome: ___________________________________________  Turma: __________  Data: ____ / ____ / _______
```

Exemplo:

```text
Prova de Geografia — 7º ano
P2 — Climas, hidrografia e domínios morfoclimáticos — Simulado 01
Nome: ___________________________________________  Turma: __________  Data: ____ / ____ / _______
```

Esse cabeçalho Word pode ser mais limpo que o título H1 do Markdown, desde que o conteúdo e a identificação do simulado permaneçam claros.

### 12.10. Linhas de resposta no `.docx`

As linhas de resposta devem manter exatamente 93 underscores:

```text
_____________________________________________________________________________________________
```

Usar fonte 10 pt para as linhas, para caberem bem na largura da página com as margens do padrão.

### 12.11. Gabarito no `.docx`

Quando o `.docx` incluir gabarito, ele deve começar em nova seção visual clara, preferencialmente em nova página quando possível.

Usar:

```text
Gabarito comentado
Questão 01
Resposta esperada:
...
Comentário:
...
```

Se o objetivo for entregar apenas a prova ao aluno, o gabarito pode ficar apenas no `.md` ou em um `.docx` separado, desde que Ricardo peça assim. Na ausência de orientação contrária, manter o gabarito comentado no final.

---

## 13. Obrigatoriedade

Este padrão deve ser aplicado a todos os simulados futuros e deve orientar também revisões de simulados já gerados quando Ricardo solicitar reformatar algum arquivo.
