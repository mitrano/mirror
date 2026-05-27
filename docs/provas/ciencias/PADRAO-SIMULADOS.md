# Padrão Operacional — Simulados de Ciências do 7º ano

Este arquivo complementa o padrão geral de simulados registrado em:

```text
docs/provas/PADRAO-SIMULADOS-GERAL.md
```

Ele registra o padrão específico definido na jornada `analise-provas-7ano` para análise de provas reais e geração de simulados escolares de **Ciências, 7º ano, prova discursiva**.

O objetivo é garantir que simulados gerados hoje, em um mês ou em seis meses mantenham o mesmo padrão pedagógico, documental e operacional validado por Ricardo.

Este padrão foi inicialmente derivado da análise da P1 de Ciências, mas não pertence apenas à P1. Ele é o padrão geral de Ciências/provas discursivas e deve ser reutilizado, refinado e customizado quando novas provas reais ou revisões forem analisadas, como P2, P3 etc.

Este padrão não deve ser assumido automaticamente para outras matérias nem para provas objetivas sem nova análise.

---

## 1. Jornada associada

- Jornada: `analise-provas-7ano`
- Finalidade: analisar provas discursivas de Ciências do filho de Ricardo, extrair o padrão avaliativo da escola e gerar simulados no mesmo estilo, com gabarito e documentos prontos para Google Docs.
- Aluno: 12 anos, 7º ano.
- Prioridade: fidelidade ao padrão da escola, linguagem adequada ao 7º ano e utilidade prática para estudo.

---

## 2. Ordem obrigatória do processo

Ao receber imagens de uma prova real:

1. Extrair/transcrever as questões das imagens.
2. Apresentar as questões extraídas para validação de Ricardo.
3. Apresentar o entendimento inicial da estrutura da prova e das questões.
4. Aguardar validação/correção.
5. Só depois comparar a prova com a revisão estudada pelo aluno.
6. Identificar como a escola transforma conteúdo da revisão em perguntas.
7. Usar esse padrão para gerar simulados futuros.

Ao receber uma revisão para gerar simulado:

1. Ler a revisão.
2. Identificar temas centrais, temas pouco trabalhados e possíveis erros conceituais.
3. Gerar o simulado no padrão definido abaixo.
4. Gerar gabarito comentado.
5. Gerar arquivo `.docx` bem formatado.
6. Gerar script curto de upload em `.local/upload-scripts/`.
7. O script deve fazer upload para Google Drive e compartilhar com o e-mail padrão.

---

## 3. Padrão pedagógico da prova real identificada

A prova real analisada não cobra apenas definição direta. Ela usa a seguinte lógica:

> situação cotidiana curta + conceito científico aplicado + comando simples + resposta escolar explicativa.

A prova costuma evitar perguntas como:

> “Defina alavanca.”

E prefere perguntas como:

> “Um trabalhador usa um martelo apoiado na madeira para retirar um prego. Qual é o tipo de máquina simples empregado?”

Portanto, os simulados devem:

1. Começar preferencialmente com uma situação cotidiana.
2. Inserir o conceito científico dentro da situação.
3. Pedir que o aluno reconheça, explique, relacione, complete ou justifique.
4. Cobrar compreensão aplicada, não apenas memorização.
5. Usar linguagem simples, adequada ao 7º ano.
6. Evitar linguagem técnica excessiva.
7. Não usar questões de múltipla escolha, salvo pedido explícito.

---

## 4. Estrutura obrigatória dos simulados

Cada simulado deve conter:

1. Cabeçalho com:
   - título da prova;
   - série/ano;
   - identificação da P1/P2 quando aplicável;
   - linha para nome, turma e data.
2. 9 questões principais.
3. 1 questão de excelência ao final.
4. Espaço adequado para resposta nas questões discursivas.
5. Gabarito separado após quebra de página.
6. Gabarito comentado, não apenas respostas secas.

---

## 5. Tipos de questão que devem ser misturados

O simulado deve alternar formatos, como na prova real:

- questão discursiva explicativa;
- completar frases;
- relacionar Coluna A e Coluna B;
- identificação de conceito em situação prática;
- explicação de causa e consequência;
- correção de erro conceitual comum;
- classificação de situações;
- questão de excelência com comparação e justificativa.

A prova não deve ser composta apenas por questões abertas longas.

---

## 6. Qualidade esperada das questões

As questões devem:

1. Parecer questões escolares reais.
2. Ter enunciados claros e não excessivamente longos.
3. Usar exemplos cotidianos próximos de um aluno de 12 anos.
4. Cobrar os conceitos da revisão sem inventar conteúdo externo.
5. Trabalhar também temas que foram pouco abordados nos simulados anteriores.
6. Incluir erros conceituais comuns para o aluno corrigir quando isso for pedagogicamente útil.

Exemplos de erros conceituais úteis:

- “O gelo passa frio para a mão.”
- “A água saiu de dentro da lata porque apareceram gotinhas fora.”
- “Micro-ondas esquenta por ar quente encostando no alimento.”
- “Calor e temperatura são a mesma coisa.”
- “Todos os casos envolvem o mesmo tipo de propagação de calor.”

---

## 7. Padrão da questão de excelência

A questão de excelência deve ser mais integradora que as demais.

Ela deve:

1. Apresentar uma situação-problema mais completa.
2. Exigir comparação entre alternativas ou situações.
3. Pedir justificativa explícita.
4. Integrar dois ou mais conceitos da revisão.
5. Permitir resposta mais longa.

Exemplo de boa questão de excelência:

> Comparar uma caneca de metal, uma garrafa plástica comum e uma garrafa térmica para conservar chocolate quente, usando condução, convecção, irradiação e sistema quase isolado.

---

## 8. Padrão do gabarito

O gabarito deve ser comentado.

Para cada questão, incluir:

1. `Resposta esperada:` — resposta modelo em linguagem adequada ao 7º ano.
2. `Comentário:` — critério simples de correção, explicando o que torna a resposta correta ou parcialmente correta.

O gabarito deve aceitar variações de resposta discursiva quando o conceito estiver correto.

Não tratar respostas discursivas como se houvesse apenas uma frase obrigatória.

---

## 9. Padrão do arquivo `.docx`

Sempre que um simulado for gerado, também gerar arquivo `.docx` respectivo.

O `.docx` deve ter:

1. Boa diagramação.
2. Margens adequadas.
3. Espaçamento real entre questões.
4. Títulos destacados.
5. Campo “Resposta:” antes das linhas de resposta.
6. Linhas suficientes para respostas discursivas.
7. Tabelas reais para questões de Coluna A / Coluna B.
8. Gabarito em nova página.
9. Nome de arquivo claro.

Padrão de nome sugerido:

```text
simulado-p2-ciencias-03-melhorado.docx
```

---

## 10. Padrão dos scripts de upload

Sempre que gerar um `.docx` de simulado, gerar também script curto de upload.

Os scripts devem ficar em:

```text
.local/upload-scripts/
```

Eles não devem ficar misturados em `docs/provas/` nem em `scripts/`.

Eles são temporários/local-only e não precisam ser versionados.

Regra operacional definida por Ricardo:

- scripts de upload não precisam ficar versionados;
- podem ser removidos um dia depois de criados;
- quando forem criados, devem ficar em pasta específica.

A pasta `.local/upload-scripts/` deve permanecer no `.gitignore`.

---

## 11. Padrão de upload e compartilhamento

O upload é feito via Google Drive API com OAuth.

Sempre que fizer upload de simulado, compartilhar automaticamente com:

```text
nicolas.25438231@aluno.pensi.com.br
```

Permissão:

```text
writer
```

O script curto deve usar o script Python local de upload com parâmetros equivalentes a:

```bash
--share-with nicolas.25438231@aluno.pensi.com.br --role writer
```

Não pedir nem armazenar usuário/senha Google.
Usar OAuth.

Arquivos sensíveis, como credenciais OAuth e token local, não devem ser versionados.

---

## 12. Estrutura de diretórios

Estrutura correta definida por Ricardo:

```text
docs/provas/<materia>/<bimestre>/
```

Para padrões gerais da matéria, usar a pasta da matéria:

```text
docs/provas/ciencias/PADRAO-SIMULADOS.md
```

Para materiais específicos de Ciências/P1, o caminho correto é:

```text
docs/provas/ciencias/p1/
```

Histórico de migração: inicialmente, nesta sessão, os arquivos foram criados em:

```text
docs/provas/p1/ciencias/
```

Essa estrutura estava invertida. Ricardo corrigiu o padrão para que a matéria venha antes do bimestre. Em 2026-05-25, os arquivos foram movidos de `docs/provas/p1/ciencias/` para `docs/provas/ciencias/p1/`, e as referências textuais conhecidas foram atualizadas.

Se no futuro aparecer algum caminho antigo com `docs/provas/p1/ciencias/`, ele deve ser tratado como legado e corrigido para `docs/provas/ciencias/p1/`.

---

## 13. Como verificar persistência

Para verificar a jornada no banco do Mirror:

```bash
uv run python -m memory journey analise-provas-7ano
```

Para verificar este padrão operacional:

```bash
ls docs/provas/ciencias/PADRAO-SIMULADOS.md
```

ou abrir este arquivo diretamente.

Para verificar scripts locais temporários:

```bash
ls .local/upload-scripts/
```

---

## 14. Estado validado por Ricardo

Validações feitas por Ricardo nesta sessão:

1. Os simulados `01`, `02` e `03` melhorados ficaram bons.
2. O upload dos três simulados melhorados funcionou.
3. O compartilhamento com `nicolas.25438231@aluno.pensi.com.br` funcionou.
4. O fluxo OAuth/upload/compartilhamento está validado de ponta a ponta.
5. Este padrão deve ser reutilizado para próximos simulados.

---

## 15. Regra final

Quando Ricardo pedir “gere um simulado”, assumir automaticamente:

1. gerar simulado no padrão pedagógico validado;
2. gerar gabarito comentado;
3. gerar `.docx` bem formatado;
4. gerar script curto em `.local/upload-scripts/`;
5. script deve fazer upload para Google Drive;
6. script deve compartilhar com `nicolas.25438231@aluno.pensi.com.br` como `writer`.
