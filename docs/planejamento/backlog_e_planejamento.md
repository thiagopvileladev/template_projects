# Backlog de Tarefas, Cronograma e Gestão de Riscos — TrackVault

## 1. Backlog de Tarefas da Fase 2 (Implementação e Publicação)

| ID | Módulo / Requisito | Descrição da Tarefa | Responsável | Prioridade |
| :--- | :--- | :--- | :--- | :---: |
| **TK01** | Ambiente & Setup | Configurar projeto Django 5.x, PostgreSQL/SQLite e arquivo `.env`. | Thiago | Alta |
| **TK02** | Banco de Dados | Criar *Models* (Álbum, Faixa, Avaliação, Coleção) e aplicar *Migrations*. | Colaborador | Alta |
| **TK03** | Autenticação | Implementar controle de acesso, views de Login, Logout e Cadastro. | Thiago | Alta |
| **TK04** | CRUD Acervo | Desenvolver Views e Forms com validação no servidor para Músicas/Álbuns. | Colaborador | Alta |
| **TK05** | Módulo de Busca | Implementar busca parametrizada por título, artista e gênero musical. | Thiago | Alta |
| **TK06** | Consumo Spotify | Implementar `SpotifyService` com `requests`, OAuth Client Credentials e timeout. | Thiago | Alta |
| **TK07** | API REST Própria | Desenvolver Serializers e Endpoints DRF para `/api/v1/faixas/` e `/avaliacoes/`. | Colaborador | Alta |
| **TK08** | Relatórios | Criar painel de relatórios consolidados com opção de exportação/impressão PDF. | Colaborador | Média |
| **TK09** | Frontend / UI | Aplicar Bootstrap 5 e paleta Dark Mode (`#121212`, `#1DB954`) nos templates HTML. | Thiago | Média |
| **TK10** | Publicação & HTTPS | Configurar deploy em servidor de hospedagem com HTTPS e `DEBUG=False`. | Thiago | Alta |
| **TK11** | Segurança (SAST/DAST) | Executar Bandit/Semgrep (SAST) e OWASP ZAP (DAST), gerando relatório de correções. | Colaborador | Alta |

---

## 2. Cronograma de Execução e Marcos (Milestones)

* **Marco 1 — Estrutura e Modelos:** Modelos de banco criados e sistema de autenticação operacional.
* **Marco 2 — Funcionalidades Core:** CRUD completo, Busca e Integração funcional com a API do Spotify.
* **Marco 3 — API REST & Relatórios:** Endpoints JSON do DRF e painel de estatísticas finalizados.
* **Marco 4 — Deploy & Segurança:** Aplicação publicada em HTTPS com análises SAST e DAST executadas.

---

## 3. Matriz de Riscos do Projeto

| Risco Identificado | Severidade | Estratégia de Mitigação / Contingência |
| :--- | :---: | :--- |
| **Indisponibilidade ou Rate Limit da API do Spotify** | Alta | Aplicação de *timeout=5s*, tratamento de exceções e liberação de formulário manual (*fallback*). |
| **Exposição involuntária de segredos no GitHub** | Alta | Uso estrito de `python-decouple` / `.env` e cadastro do `.env` no `.gitignore` desde a primeira submissão. |
| **Atrasos na configuração do ambiente de hospedagem** | Média | Escolha prévia de plataformas com suporte nativo a Django e banco de dados relacional. |