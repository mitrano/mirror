# Termo de Abertura — Gravador de Reuniões Windows

## Controle do Draft

- Nome proposto: Gravador de Reuniões Windows
- Slug: `gravador-reunioes-windows`
- Status inicial: active
- Projeto local: `/home/ricardoalvares/repos/gravador-reunioes-windows`

## Síntese da Pré-Jornada

Criar uma ferramenta pessoal, local no Windows, acionada por arquivo `.bat`, para gravar reuniões capturando o áudio do microfone e o áudio do sistema em uma única trilha, segmentar a gravação em arquivos MP3 de 1 minuto, transcrever cada segmento com Gemini assim que ele for fechado e manter arquivos TXT de acompanhamento durante a reunião.

## Parâmetros Propostos para Criação da Jornada

- Uso: pessoal, local, no computador Windows de Ricardo.
- Interface inicial: arquivo `.bat` abrindo uma janela de terminal.
- Captura: microfone + áudio do sistema misturados em uma única trilha.
- Segmentação: arquivos MP3 de 1 minuto.
- Transcrição: Gemini, minuto a minuto, em paralelo à gravação.
- Organização: uma pasta padrão para todas as reuniões, com subpasta por sessão.
- Encerramento: sugestão automática de nome final da pasta, editável por Ricardo.

## Contexto e Origem do Projeto

Ricardo quer uma ferramenta prática para registrar reuniões enquanto elas acontecem, sem depender de interface gráfica complexa. A ferramenta deve permitir acompanhar a transcrição durante a própria reunião, preservando os áudios segmentados e a transcrição consolidada para consulta posterior.

## Objetivo, Resultado Esperado e Critérios de Sucesso

Objetivo: construir um programa confiável para gravar, segmentar, transcrever e organizar reuniões locais no Windows.

Resultado esperado:

- Ricardo aciona `gravar_reuniao.bat`.
- O programa cria uma pasta de sessão em uma pasta padrão de reuniões.
- O áudio do sistema e o microfone são capturados juntos.
- A cada minuto é gerado um MP3.
- Cada MP3 é transcrito pelo Gemini assim que fica disponível.
- O programa mantém dois TXTs:
  - `transcricao_completa.txt`: concatena toda a reunião.
  - `transcricao_live.txt`: mostra apenas o trecho mais recente, sem concatenar tudo.
- Ao encerrar, o sistema sugere um nome curto para a pasta; Ricardo pode aceitar com Enter ou editar.

Critérios de sucesso:

- Capturar corretamente voz de Ricardo e áudio dos demais participantes.
- Gerar segmentos MP3 sem perda relevante entre blocos.
- Transcrever incrementalmente durante a reunião.
- Permitir que os TXTs fiquem abertos em editor enquanto o programa continua escrevendo.
- Organizar cada reunião em pasta final legível por data, horário e descrição curta.

## Escopo, Fora de Escopo e Dependências

Escopo inicial:

- `.bat` de acionamento.
- Script Python de orquestração.
- Captura/mixagem de áudio.
- Segmentação em MP3.
- Transcrição Gemini.
- Escrita dos TXTs.
- Sugestão e renomeação da pasta final.

Fora de escopo inicial:

- Interface gráfica completa.
- Produto distribuível para terceiros.
- Integração com calendário.
- Identificação perfeita de falantes.
- Edição de áudio avançada.

Dependências:

- Windows de Ricardo.
- FFmpeg instalado: confirmado FFmpeg 8.0 full build gyan.dev.
- Gemini API/configuração de credenciais.
- Estratégia técnica para capturar áudio do sistema, pois o build atual reportou `Unknown input format: 'wasapi'`.

## Stakeholders e Governança Inicial

- Usuário e decisor: Ricardo.
- Operação: uso pessoal local.
- Mirror: explorar, desenhar, implementar e documentar a solução sem misturar com a jornada `transcricao-audio-video`.

## Situação Atual: fatos, hipóteses, pendências, decisões tomadas e em aberto

Fatos:

- FFmpeg está instalado no Windows de Ricardo.
- `dshow` listou os microfones:
  - `Microfone (Logi USB Headset)`
  - `Microfone (Realtek(R) Audio)`
- O comando `ffmpeg -list_devices true -f wasapi -i dummy` falhou com `Unknown input format: 'wasapi'`.

Decisões tomadas:

- A ferramenta será pessoal e local.
- A interface será `.bat` com janela de terminal.
- Áudio do sistema e microfone devem formar uma única trilha.
- Segmentos serão MP3 de 1 minuto.
- A transcrição deve ocorrer minuto a minuto.
- Serão gerados dois arquivos TXT: completo e live.
- O nome final da pasta será sugerido pelo sistema e editável.

Hipóteses:

- O microfone padrão inicial pode ser `Microfone (Logi USB Headset)`.
- A captura do áudio do sistema pode exigir alternativa a WASAPI no FFmpeg, como Stereo Mix, VB-Cable/Voicemeeter, ou biblioteca Python com loopback.

Pendências:

- Confirmar a melhor estratégia para capturar áudio do sistema.
- Definir estrutura inicial do projeto.
- Definir como Gemini será chamado.
- Definir comportamento exato de escrita nos arquivos TXT abertos.

## Riscos e Pontos de Atenção

- Captura do áudio do sistema é o risco técnico principal.
- Alguns editores podem não atualizar automaticamente arquivos modificados externamente.
- Transcrição minuto a minuto depende de latência e estabilidade da API Gemini.
- É necessário evitar travar a gravação quando uma transcrição falhar; transcrição deve funcionar em fila, desacoplada da captura.

## Contrato Operacional do Mirror

- Esta jornada não deve ser misturada com `transcricao-audio-video`.
- O projeto local deve viver em `/home/ricardoalvares/repos/gravador-reunioes-windows`.
- A construção deve privilegiar simplicidade, confiabilidade e uso pessoal.
- Antes de implementar captura definitiva, validar experimentalmente o caminho técnico de áudio do sistema + microfone.

## Primeiro Plano de Ação

1. Criar estrutura inicial do projeto.
2. Criar documentação mínima do objetivo e decisões.
3. Fazer experimento isolado de captura de microfone.
4. Investigar captura de áudio do sistema sem WASAPI no FFmpeg.
5. Escolher entre Stereo Mix, dispositivo virtual ou captura Python.
6. Criar protótipo de segmentação MP3.
7. Integrar transcrição Gemini.
8. Implementar escrita de `transcricao_completa.txt` e `transcricao_live.txt`.
9. Implementar renomeação final sugerida/editável.

## Lacunas Antes da Criação

A lacuna principal é técnica, não conceitual: capturar o áudio do sistema no Windows de Ricardo.

## Confirmação para Criação

Ricardo confirmou a criação de nova jornada e nova pasta para este programa, separada da jornada anterior.
