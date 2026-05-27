# Prompt Gerador — Simulado de Artes P1

Use este prompt para gerar um simulado de Artes do 7º ano a partir da revisão da P1, seguindo o padrão identificado na prova real.

> Importante: este arquivo é uma **instância específica da P1**. Ele contém conteúdos da revisão da P1 e não deve ser usado diretamente para P2/P3 sem substituir integralmente o bloco de conteúdo pela revisão atual. Para novas provas, use o template reutilizável em `docs/provas/artes/PROMPT-TEMPLATE-SIMULADO.md`.

Arquivos de referência desta análise:

- Questões extraídas: `docs/provas/artes/p1/QUESTOES-EXTRAIDAS.md`
- Análise prova × revisão: `docs/provas/artes/p1/ANALISE-PROVA-REVISAO.md`
- Revisão: `docs/provas/artes/p1/revisoes/P1 - ARTES.txt`

---

## Prompt

Você é um professor especialista em Artes e História da Arte do 7º ano. Sua tarefa é gerar um simulado discursivo de Artes a partir da transcrição de uma revisão de prova.

O simulado deve imitar o padrão de uma prova real de Artes do 7º ano, identificada a partir de uma prova anterior da escola.

## Contexto do aluno

- Aluno de 12 anos.
- 7º ano do Ensino Fundamental.
- Disciplina: Artes / História da Arte.
- Tipo de prova: discursiva, com interpretação de imagens, vocabulário artístico e produção criativa.
- A linguagem deve ser simples, escolar e adequada ao 7º ano.

## Padrão da prova real de Artes

A prova real de Artes segue esta lógica:

> obra/imagem + conceito estudado + pergunta curta de identificação, interpretação, vocabulário ou criação visual.

A prova usa principalmente:

1. Obras de arte como ponto de partida.
2. Perguntas curtas e diretas.
3. Identificação de artistas, movimentos e técnicas.
4. Interpretação simbólica de obras.
5. Características visuais de movimentos artísticos.
6. Completar lacunas com banco de palavras.
7. Questão de excelência baseada em análise visual.
8. Questão prática/criativa de composição artística.

## Conteúdos da revisão que devem orientar o simulado

Use apenas os conteúdos presentes na revisão fornecida e nos padrões identificados na prova real. Priorize:

- arte de vanguarda;
- liberdade artística e ruptura com a tradição;
- Expressionismo;
- Expressionismo alemão;
- características visuais expressionistas;
- cores fortes;
- formas distorcidas;
- expressão intensa de sentimentos;
- medo, angústia, solidão e tristeza;
- Edvard Munch;
- O Grito;
- Gustav Klimt;
- mosaicos;
- padrões decorativos;
- pequenos fragmentos de vidro, mármore ou materiais semelhantes;
- arte bizantina;
- função educativa e decorativa dos mosaicos;
- Cristo e imperadores;
- Hans Baldung;
- As Três Idades da Vida e a Morte;
- vaidade;
- espelho;
- ampulheta;
- passagem do tempo;
- efemeridade da vida;
- Pieter Bruegel;
- representação da morte;
- técnica de profundidade;
- sobreposição;
- tamanho das figuras;
- nitidez;
- linhas diagonais;
- composição artística sobre passagem do tempo.

## Estrutura obrigatória do simulado

Crie exatamente:

1. 8 questões no total, seguindo a prova real.
2. A Questão de Excelência deve corresponder à Questão 07.
3. Não criar uma Questão 07 separada além da Questão de Excelência.
4. A Questão 08 deve ser uma questão prática/criativa de composição artística.
5. Gabarito comentado ao final.

Estrutura sugerida:

- Questão 01: características do Expressionismo ou arte de vanguarda.
- Questão 02: dado histórico/conceitual sobre Expressionismo ou vanguarda.
- Questão 03: interpretação simbólica de obra ligada à vida, morte, vaidade ou passagem do tempo.
- Questão 04: justificar por que um artista ou obra se aproxima de um movimento artístico.
- Questão 05: identificação de técnica artística, preferencialmente mosaico.
- Questão 06: completar lacunas com banco de palavras.
- Questão de Excelência / Questão 07: análise visual de profundidade ou outro conceito visual aplicado a uma obra.
- Questão 08: criação de composição artística com restrições claras.

## Regras para as questões

- Não usar múltipla escolha, salvo se a revisão original usar e for necessário adaptar.
- Não fazer questões longas demais.
- Não usar linguagem acadêmica ou de Ensino Médio.
- Não inventar artistas ou movimentos fora da revisão.
- Quando não for possível inserir imagem real, descrever a imagem ou obra de forma clara.
- Misturar memória, interpretação e aplicação visual.
- Incluir ao menos uma questão com banco de palavras.
- Incluir uma questão prática/criativa.
- A questão criativa deve ter critérios como uso de cor, ocupação do espaço, capricho e relação com o conceito.
- A questão de excelência deve exigir aplicação de conceito visual, não apenas definição.

## Padrão de gabarito comentado

Depois da prova, criar a seção:

```text
# GABARITO COMENTADO
```

Para cada questão, usar:

```text
## Questão XX

Resposta esperada:
[resposta modelo]

Comentário:
[critério simples de correção]
```

Para a questão criativa, o gabarito deve indicar critérios de avaliação, não uma única resposta correta.

Exemplo para questão criativa:

```text
Resposta esperada:
A composição deve representar a passagem do tempo sem usar símbolos proibidos, como relógio, ampulheta, morte ou criança.

Comentário:
Avaliar se o aluno representou visualmente a ideia de passagem do tempo, usou cores, ocupou o espaço, teve capricho e respeitou as restrições do enunciado.
```

## Formato de saída

Use exatamente esta estrutura:

```text
# SIMULADO — ARTES — P1

Nome: ___________________________________________
Turma: ___________________
Data: ____ / ____ / _______

## Questão 01
[enunciado]

Resposta:
__________________________________________________
__________________________________________________

## Questão 02
[enunciado]

Resposta:
__________________________________________________
__________________________________________________

...

## Questão de Excelência / Questão 07
[enunciado]

Resposta:
__________________________________________________
__________________________________________________
__________________________________________________

## Questão 08
[enunciado de produção artística]

Espaço para desenho/composição artística.

# GABARITO COMENTADO

## Questão 01

Resposta esperada:
...

Comentário:
...
```

## Critérios de qualidade antes de finalizar

Antes de entregar, verifique se:

1. O simulado parece uma prova real de Artes do 7º ano.
2. Há 8 questões no total.
3. A Questão de Excelência é a Questão 07.
4. A Questão 08 é prática/criativa.
5. Há banco de palavras em pelo menos uma questão.
6. Há interpretação de obra/imagem.
7. Há identificação de técnica ou movimento artístico.
8. Há gabarito comentado.
9. O conteúdo vem da revisão.
10. A linguagem está adequada para aluno de 12 anos.

Agora, gere o simulado completo com gabarito comentado usando a revisão abaixo.

## Transcrição da revisão

[COLE AQUI O TEXTO DA REVISÃO]
```
