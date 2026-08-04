# Termo de Abertura — md2pdf

## Controle da Jornada

- **Nome:** md2pdf
- **Slug:** `md2pdf`
- **Status:** ativa
- **Origem do programa:** `C:\Users\ricardo.alvares\Downloads\mdpdf-cli-v1.0.0.zip`
- **Caminho acessível no WSL:** `/mnt/c/Users/ricardo.alvares/Downloads/mdpdf-cli-v1.0.0.zip`
- **Projeto proposto:** `/home/ricardoalvares/repos/md2pdf`

## Síntese da Jornada

A jornada reunirá o código do programa `mdpdf-cli` hoje armazenado em um ZIP no Windows. O primeiro movimento será importar o conteúdo para uma área de projeto versionável dentro da jornada, instalar as dependências em ambiente isolado e preparar uma conversão real de Markdown para PDF.

## Parâmetros da Jornada

- **Nome:** md2pdf
- **Slug:** `md2pdf`
- **Modo principal:** Builder
- **Estágio inicial:** preparação do projeto e validação local
- **Project path:** `/home/ricardoalvares/repos/md2pdf`

## Contexto e Origem do Projeto

O artefato de origem é `mdpdf-cli-v1.0.0.zip`, localizado na pasta Downloads do Windows. O ZIP contém um pacote Python 3.10+ com CLI `mdpdf`, código em `src/mdpdf_cli`, testes automatizados, README, instaladores e um Markdown de exemplo. O programa usa Markdown, Pygments e WeasyPrint para produzir PDFs.

## Objetivo, Resultado Esperado e Critérios de Sucesso

### Objetivo

Manter e evoluir o conversor Markdown para PDF dentro de uma jornada dedicada.

### Resultado esperado inicial

O código estará descompactado dentro da jornada, com ambiente de desenvolvimento reproduzível e um comando pronto para converter o arquivo de exemplo.

### Critérios de sucesso iniciais

1. O conteúdo do ZIP está preservado no projeto da jornada.
2. As dependências Python estão instaladas em ambiente isolado.
3. A suíte de testes existente executa com sucesso, ou qualquer impedimento é documentado com evidência.
4. O Markdown de exemplo é convertido em PDF.
5. O arquivo PDF produzido e o comando de repetição do teste são claramente identificados.

## Escopo, Fora de Escopo e Dependências

### Escopo inicial

- importar o programa do ZIP;
- inspecionar sua estrutura e instruções;
- preparar ambiente local;
- executar testes automatizados;
- realizar uma conversão de exemplo;
- documentar o procedimento de desenvolvimento e teste.

### Fora de escopo inicial

- publicar pacote em repositório externo;
- distribuir instalador novo;
- alterar comportamento do conversor antes da validação da versão importada;
- fazer push ou release sem autorização explícita.

### Dependências

- Python 3.10 ou superior;
- `uv` e acesso às dependências Python;
- bibliotecas nativas exigidas pelo WeasyPrint/Pango no ambiente local.

## Stakeholders e Governança Inicial

- **Navigator e proprietário:** Ricardo Alvares
- **Builder:** Mirror Mind
- Decisões de mudança funcional, publicação e release permanecem com Ricardo.
- O código importado será tratado como baseline v1.0.0 antes de alterações.

## Situação Atual

### Fatos

- O ZIP existe e está acessível pelo WSL.
- O arquivo contém `mdpdf-cli` versão 1.0.0, testes e exemplo.
- A CLI declara suporte a conversão unitária e em lote.

### Hipóteses

- O ambiente Linux atual poderá executar o WeasyPrint sem instalação adicional de bibliotecas do sistema.
- O exemplo incluído será suficiente para o primeiro teste de conversão.

### Pendências

- importar o ZIP;
- instalar o pacote e dependências;
- executar testes e conversão.

### Decisões tomadas

- usar o slug `md2pdf`;
- preservar o conteúdo original como baseline;
- começar por um teste de conversão do exemplo incluído.

### Decisões em aberto

- estratégia futura de versionamento e repositório independente;
- mudanças desejadas após a validação inicial.

## Riscos e Pontos de Atenção

- WeasyPrint pode depender de bibliotecas nativas ausentes.
- Nomes e caminhos entre Windows e WSL podem exigir tratamento específico.
- Artefatos gerados, ambientes virtuais e caches não devem ser confundidos com código-fonte versionável.
- A baseline importada deve permanecer distinguível das mudanças posteriores.

## Contrato Operacional do Mirror

- Trabalhar em Builder Mode para operações no projeto.
- Inspecionar antes de modificar e preservar a baseline importada.
- Usar TDD para mudanças comportamentais futuras.
- Manter README e documentação operacional coerentes com o código.
- Não publicar, fazer push ou release sem autorização explícita.
- Relatar comandos executados, resultados e bloqueios sem inventar evidências.

## Primeiro Plano de Ação

1. Criar a jornada e configurar seu `project_path`.
2. Extrair o ZIP para o diretório de projeto sem incluir uma pasta-raiz redundante.
3. Inspecionar arquivos e criar regras locais de ignore quando necessário.
4. Sincronizar/instalar dependências em ambiente isolado.
5. Executar a suíte de testes existente.
6. Converter `exemplos/relatorio-exemplo.md` e confirmar o PDF gerado.
7. Registrar o comando reproduzível e o resultado observado.

## Confirmação de Criação

Ricardo aprovou este termo e autorizou a criação da jornada `md2pdf`, a importação local do ZIP indicado e a preparação do primeiro teste de conversão. A confirmação não autoriza publicação, push ou release.
