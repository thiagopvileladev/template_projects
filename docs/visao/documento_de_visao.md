# Documento de Visão: TrackVault

## 1. Contexto e Problema
Entusiastas de música, DJs, estudantes de produção e curadores musicais enfrentam dificuldades para centralizar suas coleções, anotações de críticas (como notas da Pitchfork ou resenhas autorais) e organizar listas temáticas (como seleções para o Halloween ou melhores faixas de uma década) em um único local. As plataformas tradicionais de streaming disponibilizam acervos de áudio, mas não oferecem ferramentas nativas para a gestão personalizada de metadados críticos, análises acadêmicas e relatórios analíticos consolidados sobre o acervo do próprio usuário

## 2. Justificativa
O **TrackVault** resolve essa fragmentação ao unir um sistema de gerenciamento de coleções musicais a um mecanismo de enriquecimento automático de dados através da API Web do Spotify A aplicação oferece ao usuário um ambiente centralizado para catalogação, avaliação e geração de relatórios visuais sobre o acervo, garantindo a integridade dos dados por meio de validações no servidor

## 3. Objetivos
### 3.1 Objetivo Geral
Desenvolver e disponibilizar uma aplicação web responsiva em Python e Django para catalogação, avaliação e análise estatística de acervos musicais, integrada à API do Spotify e com exposição de dados via API REST própria

### 3.2 Objetivos Específicos
* Implementar o cadastro completo (CRUD) de álbuns, faixas, avaliações críticas e coleções temáticas com validações no servidor
* Integrar a API Web do Spotify para consulta e importação automática de metadados (capas de álbuns, popularidade, *danceability*, *bpm* e gênero)
* Desenvolver uma API REST própria estruturada em formato JSON para consulta externa do acervo
* Disponibilizar relatórios gráficos e indicadores consolidados da coleção, com opção de visualização e exportação/impressão

## 4. Público-Alvo
* **Usuários Primários:** Colecionadores de música, DJs, estudantes e profissionais de produção/crítica musical e curadores de playlists.
* **Usuários Secundários:** Desenvolvedores e sistemas de terceiros que consomem a API REST exposta pelo sistema para consulta de acervos

## 5. Stakeholders
* **Equipe de Desenvolvimento:** Alunos integrantes do grupo, responsáveis pela concepção, modelagem, arquitetura, implementação e testes da aplicação
* **Corpo Docente:** Professor da disciplina de Desenvolvimento Web, responsável pela orientação e avaliação das entregas das Fases 1 e 2

## 6. Escopo
O escopo da solução abrange o desenvolvimento completo do **TrackVault**, contemplando:
* Módulo de autenticação e controle de acesso de usuários
* Módulo de gerenciamento (CRUD) de álbuns, faixas, avaliações pessoais/críticas e listas temáticas
* Módulo de busca avançada com múltiplos critérios de filtragem
* Módulo de integração e consulta à API externa do Spotify
* Módulo de geração de relatórios e indicadores estatísticos
* Módulo de API REST própria para disponibilização de dados em JSON

## 7. Itens Fora do Escopo
* Player de reprodução contínua e completa de áudio por streaming (devido a restrições de direitos autorais de APIs de terceiros).
* Módulo de comércio eletrônico (venda de arquivos digitais, ingressos, assinaturas ou licenças).
* Aplicativo móvel nativo para iOS ou Android (a interface web será responsiva)
* Processamento de pagamentos ou cobranças financeiras.

## 8. Funcionalidades
* **F01 - Autenticação e Perfil:** Cadastro, login e gestão de contas de usuário com controle de acesso
* **F02 - Gerenciamento de Álbuns e Faixas (CRUD):** Inclusão, edição, visualização e remoção de registros com validações no servidor
* **F03 - Busca Avançada:** Pesquisa parametrizada por título, artista, gênero, notas de crítica ou coleções específicas
* **F04 - Integração com Spotify:** Pesquisa em tempo real na API externa para auto-preenchimento de dados de músicas e capas de álbuns
* **F05 - Relatórios e Indicadores:** Exibição gráfica e exportável de dados consolidados da coleção (ex: distribuição por gênero, média de popularidade e notas)
* **F06 - API REST Própria:** Rotas públicas e autenticadas em JSON para consumo de dados por terceiros

## 9. Restrições
* **Tecnológicas:** O backend deve ser desenvolvido exclusivamente em Python com a versão mais recente do framework Django e banco de dados relacional
* **De Configuração e Segurança:** Credenciais, tokens e chaves de API não devem ser armazenados no código ou repositório, devendo ser injetados via variáveis de ambiente
  
* **De Interface:** A interface web precisa ser responsiva e utilizável em telas móveis e desktop
* **De Implantação:** Na Fase 2, o sistema deve ser publicado com HTTPS e subdomínio acessível

## 10. Premissas
* A API Web do Spotify permanecerá ativa, gratuita e acessível durante a execução do projeto
* Os usuários terão acesso à internet para realizar o consumo da API externa em tempo real
* Todos os integrantes do grupo utilizarão a ferramenta Git/GitHub com commits frequentes e rastreáveis

## 11. Riscos Iniciais e Mitigações
* **Risco 01: Limite de requisições (*Rate Limit*) ou indisponibilidade pontual da API do Spotify.**
  * *Mitigação:* Armazenar em cache local no banco de dados os metadados já consultados e implementar rotinas de tratamento de falha com mensagens amigáveis
* **Risco 02: Complexidade na modelagem de relacionamentos N:N (músicas em múltiplas coleções).**
  * *Mitigação:* Definir o Diagrama Entidade-Relacionamento (DER) detalhadamente na Fase 1.
* **Risco 03: Incompatibilidade entre os documentos da Fase 1 e o código final da Fase 2.**
  * *Mitigação:* Manter a rastreabilidade contínua da arquitetura durante a implementação e registrar eventuais mudanças de escopo justificadas

## 12. Critérios de Sucesso
* Cumprimento de 100% dos requisitos funcionais e técnicos descritos na especificação oficial do trabalho
* Rastreabilidade e correspondência direta entre a documentação entregue na Fase 1 e o código funcional apresentado na Fase 2
* Aplicação implantada e operando via HTTPS, acompanhada dos relatórios de análise estática e dinâmica de segurança (SAST/DAST)