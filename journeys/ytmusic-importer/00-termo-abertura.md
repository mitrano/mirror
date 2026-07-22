# Termo de Abertura — YouTube Music Importer

## Controle do Draft

- Nome proposto: YouTube Music Importer
- Slug proposto: `ytmusic-importer`
- Estado: aprovado para criação inicial por Ricardo durante conversa exploratória.

## Síntese da Pré-Jornada

Construir uma forma simples de Ricardo passar uma lista de músicas e o Mirror, ou uma ferramenta auxiliar associada, inserir essas músicas em uma playlist do YouTube Music: usando uma playlist existente ou criando uma nova quando ela não existir.

## Parâmetros Propostos para Criação da Jornada

- Jornada: `ytmusic-importer`
- Natureza: automação pessoal / integração musical
- Modo inicial recomendado: Explorer, antes de Builder
- Primeira hipótese técnica: testar `ytmusicapi`, biblioteca não oficial para YouTube Music.

## Contexto e Origem do Projeto

Ricardo quer transformar listas textuais de músicas em playlists reais no YouTube Music sem trabalho manual de busca e inserção faixa a faixa.

## Objetivo, Resultado Esperado e Critérios de Sucesso

Objetivo: permitir importar uma lista de músicas para uma playlist do YouTube Music.

Resultado esperado mínimo:

- ler uma lista de músicas em texto;
- identificar artista e título quando possível;
- buscar correspondências no YouTube Music;
- criar playlist se ela não existir;
- adicionar músicas à playlist existente ou recém-criada;
- tratar ambiguidades e falhas de busca de forma revisável.

Critérios iniciais de sucesso:

- autenticação local funcionando;
- criação de playlist de teste;
- adição confiável de um lote pequeno de músicas;
- relatório claro de músicas adicionadas, ambíguas, não encontradas e duplicadas.

## Escopo, Fora de Escopo e Dependências

Escopo inicial:

- importação local a partir de arquivo texto ou lista colada;
- integração com conta pessoal do YouTube Music;
- fluxo revisável antes de mutações definitivas.

Fora de escopo inicial:

- interface web completa;
- sincronização contínua entre serviços;
- suporte multiusuário;
- publicação como produto SaaS.

Dependências prováveis:

- `ytmusicapi` ou YouTube Data API;
- autenticação local segura;
- testes com playlist real de baixo risco.

## Stakeholders e Governança Inicial

- Dono: Ricardo
- Operador técnico: Mirror/Builder quando promovido
- Usuário final inicial: Ricardo

## Situação Atual: fatos, hipóteses, pendências, decisões tomadas e em aberto

Fatos:

- O YouTube Music não oferece uma API pública simples equivalente à do Spotify para playlists musicais.
- Existem alternativas técnicas: `ytmusicapi`, YouTube Data API e automação de navegador.

Hipóteses:

- `ytmusicapi` deve ser o caminho mais rápido para um MVP local.
- A maior dificuldade será autenticação e qualidade dos matches.

Pendências:

- validar autenticação;
- testar busca e inserção em playlist;
- decidir formato de entrada;
- definir tratamento de ambiguidades.

## Riscos e Pontos de Atenção

- `ytmusicapi` é não oficial e pode quebrar.
- Cookies/headers de autenticação exigem cuidado.
- Matches errados podem inserir versões incorretas.
- Automação deve evitar duplicatas e permitir revisão.

## Contrato Operacional do Mirror

A jornada começa em Explorer Mode. O Mirror deve preservar incertezas, comparar caminhos técnicos e propor pequenos experimentos antes de executar implementação. Só deve passar para Builder quando Ricardo confirmar promoção explícita.

## Primeiro Plano de Ação

1. Explorar arquitetura possível.
2. Definir MVP local.
3. Propor experimento com 10 músicas e uma playlist de teste.
4. Se aprovado, promover para Builder.

## Lacunas Antes da Criação

- Nome final da CLI/ferramenta.
- Formato exato da lista de músicas.
- Estratégia de autenticação preferida.
- Se o importador ficará dentro do Mirror ou como ferramenta separada.

## Confirmação para Criação

Ricardo confirmou seguir com a criação da jornada usando o slug `ytmusic-importer`.
