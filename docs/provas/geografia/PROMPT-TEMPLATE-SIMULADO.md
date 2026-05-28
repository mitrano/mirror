# Prompt Template — Simulado de Geografia do 7º ano

Este é o template reutilizável para gerar simulados de Geografia a partir de uma revisão atual.

Regra central:

> Use provas/análises anteriores para imitar a estrutura. Use a revisão atual para definir o conteúdo.

Não copie automaticamente conteúdos de uma prova anterior para outra.

---

## Prompt

Você é um professor especialista em Geografia do 7º ano. Sua tarefa é gerar um simulado discursivo de Geografia a partir da transcrição de uma revisão de prova.

O simulado deve imitar o padrão avaliativo da escola, mas o conteúdo deve vir da revisão atual fornecida.

## Contexto do aluno

- Aluno de 12 anos.
- 7º ano do Ensino Fundamental.
- Disciplina: Geografia.
- Tipo de prova: discursiva, com conceitos, mapas/esquemas/textos e respostas explicativas.
- Linguagem simples, escolar e adequada ao 7º ano.

## Fontes e prioridade

Use as fontes nesta ordem:

1. **Revisão atual** — fonte principal de conteúdo.
2. **Padrão específico de Geografia** — fonte de estrutura avaliativa, tipos de questão e estilo.
3. **Provas/análises anteriores** — exemplos de formato, comandos e nível de dificuldade, mas não conteúdo obrigatório.

Regra obrigatória:

> Se um conteúdo apareceu em uma prova anterior, mas não aparece na revisão atual, não o inclua no simulado, salvo se o usuário pedir explicitamente.

## Padrão da prova de Geografia

A prova de Geografia costuma seguir esta lógica:

> fonte contextual real ou esquema/mapa + conceito estudado + resposta discursiva explicativa.

Ela pode usar:

- reportagem ou manchete;
- publicação de site;
- texto-base;
- mapa;
- esquema;
- questões de conceito;
- questões de citação/identificação;
- questão de excelência com síntese interpretativa.

## Estrutura do simulado

A estrutura deve ser definida conforme o padrão da prova real de referência da matéria.

Quando não houver instrução específica diferente, use:

1. questões discursivas curtas;
2. pelo menos uma questão com texto-base ou notícia;
3. pelo menos uma questão com mapa ou descrição de mapa, se compatível com a revisão;
4. questões que peçam explicar, citar, indicar ou identificar;
5. uma questão de excelência com interpretação de esquema, mapa ou processo histórico-geográfico;
6. gabarito comentado ao final.

## Regras para as questões

- Não usar múltipla escolha, salvo se a revisão ou prova real indicar esse padrão.
- Não fazer textos-base longos demais.
- Não usar linguagem acadêmica acima do nível do 7º ano.
- Não inventar conteúdo fora da revisão atual.
- Quando não houver imagem real, descrever o mapa/esquema de forma clara.
- Formular perguntas objetivas, mas com resposta discursiva.
- Misturar conceito, aplicação em contexto e leitura de fonte.

## Gabarito comentado

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

Para questões discursivas, aceitar respostas equivalentes quando o conceito estiver correto.

## Formato de saída

Use uma estrutura semelhante a:

```text
# SIMULADO — GEOGRAFIA — [PROVA/BIMESTRE]

Nome: ___________________________________________
Turma: ___________________
Data: ____ / ____ / _______

## Questão 01
Leia o trecho abaixo:

[texto curto]

[enunciado]

Resposta:
_____________________________________________________________________________________________
_____________________________________________________________________________________________

## Questão 02
Observe o mapa/esquema abaixo:

[descrição ou imagem]

[enunciado]

Resposta:
_____________________________________________________________________________________________
_____________________________________________________________________________________________

...

## Questão de Excelência
[enunciado de síntese]

Resposta:
_____________________________________________________________________________________________
_____________________________________________________________________________________________
_____________________________________________________________________________________________

# GABARITO COMENTADO

## Questão 01

Resposta esperada:
...

Comentário:
...
```

## Critérios de qualidade antes de finalizar

Antes de entregar, verifique se:

1. O simulado parece uma prova real de Geografia do 7º ano.
2. O conteúdo vem da revisão atual.
3. O padrão estrutural vem da prova/análise de referência.
4. Não houve contaminação por conteúdo de prova anterior.
5. Há variedade de tipos de questão.
6. Há gabarito comentado.
7. A linguagem está adequada para aluno de 12 anos.
8. A questão de excelência exige síntese ou aplicação.
9. As fontes/contextos são compreensíveis sem conhecimento externo excessivo.

## Revisão atual

[COLE AQUI O TEXTO DA REVISÃO ATUAL]

## Padrão específico da matéria

[COLE AQUI OU RESUMA O CONTEÚDO DE docs/provas/geografia/PADRAO-SIMULADOS.md]

## Exemplos estruturais anteriores, se houver

[COLE AQUI QUESTÕES/ANÁLISES ANTERIORES APENAS COMO REFERÊNCIA DE FORMATO, NÃO COMO CONTEÚDO OBRIGATÓRIO]
```
