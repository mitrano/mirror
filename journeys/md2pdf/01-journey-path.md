# md2pdf — Journey Path

**Status:** active
**Stage:** Orientação e Ofício implementados
**Created:** 2026-08-04

## Current status

O projeto v1.1.0 suporta formato Ofício/Legal e orientação Retrato/Paisagem. A implementação foi validada com 9 testes automatizados e uma conversão real de `exemplos/relatorio-exemplo.md` usando `--formato Oficio --orientacao paisagem`.

Esta jornada é a mantenedora do conversor oficial Markdown → PDF usado pelo MirrorMind nas jornadas locais.

## Source document

/home/ricardoalvares/repos/mirror/journeys/md2pdf/00-termo-abertura.md

## Next movement

Usar a versão 1.1.0 validada para conversões locais e decidir as próximas melhorias do conversor.

## Regra operacional — propagação de capacidades para o MirrorMind

Sempre que houver alteração no programa `mdpdf` que modifique, amplie ou remova capacidades disponíveis para conversão Markdown → PDF — por exemplo novos formatos de página, novas orientações, estilos, opções CLI, regras de saída, comportamento de sobrescrita ou modo de uso — o Mirror deve parar após a implementação e propor a Ricardo a atualização da regra geral do MirrorMind para todas as jornadas.

A proposta deve incluir:

1. o que mudou no `mdpdf`;
2. quais novas opções ou comportamentos passam a estar disponíveis;
3. se a mudança deve ou não ser exposta para todas as jornadas;
4. a redação sugerida para a regra geral em `ego/behavior`;
5. confirmação explícita de Ricardo antes de alterar a regra geral.

O Mirror não deve atualizar automaticamente a regra geral apenas porque o código mudou. Ele deve propor a atualização e aguardar aprovação, salvo quando Ricardo autorizar explicitamente a atualização direta.
