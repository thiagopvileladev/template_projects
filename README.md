<p align="center">
  <img src="static/img/logo.svg" alt="Logotipo do TrackVault" width="96" height="96">
</p>

<h1 align="center">TrackVault</h1>

<p align="center"><em>Curadoria, Acervo e Análises Críticas Musicais em um só Lugar.</em></p>

<p align="center">
  <img src="https://img.shields.io/badge/status-fase%202%20conclu%C3%ADda-1DB954" alt="Status: Fase 2 concluída">
  <img src="https://img.shields.io/badge/vers%C3%A3o-1.0.0-1E1E1E" alt="Versão 1.0.0">
  <img src="https://img.shields.io/badge/testes-119%20aprovados-1DB954" alt="119 testes aprovados">
  <img src="https://img.shields.io/badge/cobertura-94%25-1DB954" alt="Cobertura 94%">
</p>

<p align="center">
  <a href="https://trackvault-3hpa.onrender.com"><strong>Aplicação publicada</strong></a> ·
  <a href="https://trackvault-3hpa.onrender.com/api/v1/docs/"><strong>Documentação da API</strong></a> ·
  <a href="docs/seguranca/relatorio_seguranca.md"><strong>Relatório de segurança</strong></a>
</p>

---

| | |
|---|---|
| **Instituição** | CEUB — Análise e Desenvolvimento de Sistemas |
| **Disciplina** | Desenvolvimento Web — Turma A, 4º semestre |
| **Professor** | Felippe Pires |
| **Situação** | Fase 2 concluída: aplicação implementada, publicada com HTTPS e avaliada com SAST e DAST |

## 1. Sobre o projeto

O **TrackVault** é uma aplicação web em Python/Django para catalogar, avaliar e analisar acervos musicais. O curador cadastra álbuns e faixas (manualmente ou importando metadados do **Spotify**), registra a própria nota e a nota da crítica (Pitchfork), organiza coleções temáticas e acompanha indicadores em relatórios. Os dados do acervo também ficam disponíveis por uma **API REST própria**.

### Problema

Colecionadores, DJs e curadores não têm um lugar único para reunir a coleção, as notas da crítica, as próprias resenhas e listas temáticas. Os serviços de streaming oferecem o áudio, mas não a gestão de metadados críticos nem relatórios sobre o acervo de cada pessoa.

### Público-alvo

- **Usuários primários:** colecionadores de música, DJs, estudantes e profissionais de produção e crítica musical, curadores de playlists.
- **Usuários secundários:** desenvolvedores e sistemas que consultam o acervo pela API REST.

### Funcionalidades

| Funcionalidade | Onde |
|---|---|
| Cadastro, login por e-mail e proteção contra força bruta | `/contas/cadastro/`, `/contas/entrar/` |
| CRUD de álbuns, faixas, avaliações e coleções, com validação no servidor | `/albuns/`, `/faixas/`, `/colecoes/` |
| Importação de metadados do Spotify (título, álbum, artista, ano, capa, duração, ISRC), com cadastro manual quando o Spotify está indisponível | `/faixas/importar/` |
| Busca com filtros combinados (texto, artista, gênero, nota mínima, faixa de BPM, coleção) e ordenação | `/faixas/` e barra de busca do topo |
| Relatório com indicadores, gráfico por gênero, ranking e tabela consolidada, com impressão/PDF e exportação CSV | `/relatorios/` (requer login) |
| API REST própria com autenticação por token, paginação, filtros e limites de uso | `/api/v1/` |
| Identidade visual própria (paleta escura, logotipo, tipografia Montserrat/Inter), responsiva | todas as telas |

## 2. Acesso para avaliação

| Item | Endereço |
|---|---|
| Aplicação | https://trackvault-3hpa.onrender.com |
| Documentação da API (Swagger) | https://trackvault-3hpa.onrender.com/api/v1/docs/ |
| Esquema OpenAPI 3 | https://trackvault-3hpa.onrender.com/api/v1/schema/ |
| Guia da API (exemplos, códigos de erro, limites) | [`docs/api/guia_api_v1.md`](docs/api/guia_api_v1.md) |
| Coleção de requisições (Postman) | [`docs/testes/TrackVault_API.postman_collection.json`](docs/testes/TrackVault_API.postman_collection.json) |

**Contas de teste** (acervo fictício de demonstração):

| E-mail | Perfil |
|---|---|
| `curador.demo@trackvault.app` | Curador com avaliações e coleções (uma pública e uma privada) |
| `critica.demo@trackvault.app` | Segundo curador, para testar permissões entre usuários |

A senha das contas de teste é informada ao professor no quadro de submissão e não fica no repositório.

> A hospedagem usa o plano gratuito do Render: após 15 minutos sem acesso o serviço "dorme", e o primeiro acesso seguinte pode levar cerca de 1 minuto.

## 3. Integrantes

| Nome | Matrícula | Principais contribuições na Fase 2 |
|---|---|---|
| Thiago Paranaiba Vilela | 22501672 | Configuração do projeto, autenticação, busca, integração com o Spotify, identidade visual, deploy (Render + Supabase) |
| Marcio Tavares | 22611487 | Modelos e migrations, CRUD do acervo, API REST, relatórios, análises de segurança SAST e DAST |

Testes automatizados e roteiro de teste manual foram feitos pelos dois integrantes. A divisão completa está no [backlog](docs/planejamento/backlog_e_planejamento.md) e no histórico de commits.

## 4. Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem e framework | Python 3.13+, Django 5.2 (padrão MTV) |
| API REST | Django REST Framework, drf-spectacular (OpenAPI 3 + Swagger UI servido localmente) |
| Banco de dados | PostgreSQL 17 (Supabase) em produção; SQLite em desenvolvimento |
| Integração externa | Spotify Web API (OAuth 2.0 Client Credentials) via `requests` |
| Frontend | Templates Django, Bootstrap 5.3, CSS e JavaScript próprios, fontes hospedadas localmente |
| Servidor e hospedagem | gunicorn + WhiteNoise no Render (HTTPS), atrás do Cloudflare |
| Configuração | python-decouple (`.env`), dj-database-url |
| Qualidade e segurança | `django.test`, coverage.py, Bandit, Semgrep, pip-audit, OWASP ZAP |

Arquitetura em camadas descrita em [`docs/arquitetura/documento_arquitetura.md`](docs/arquitetura/documento_arquitetura.md). As diferenças entre o que foi planejado na Fase 1 e o que foi implementado estão justificadas em [`docs/fase2/mudancas_fase1.md`](docs/fase2/mudancas_fase1.md).

## 5. Como executar localmente

**Pré-requisitos:** Python 3.13 ou superior e Git.

```bash
# 1. Clonar o repositório
git clone https://github.com/thiagopvileladev/template_projects.git
cd template_projects

# 2. Ambiente virtual e dependências
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/macOS
pip install -r requirements-dev.txt

# 3. Variáveis de ambiente
copy .env.example .env          # Windows
# cp .env.example .env          # Linux/macOS
```

Abra o `.env` e preencha ao menos a `SECRET_KEY`. Para gerar uma:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

```bash
# 4. Banco de dados (SQLite local) e dados de demonstração
python manage.py migrate
python manage.py popular_demo   # contas de teste e acervo fictício
python manage.py buscar_capas   # opcional: capas via Spotify (exige as chaves no .env)

# 5. Executar
python manage.py runserver
```

Acesse http://127.0.0.1:8000. Sem `DEMO_PASSWORD` no `.env`, o `popular_demo` gera uma senha aleatória e a exibe no terminal. Para criar um administrador: `python manage.py createsuperuser`.

### Testes

```bash
python manage.py test           # 119 testes
coverage run manage.py test && coverage report
```

Detalhes em [`docs/testes/relatorio_testes.md`](docs/testes/relatorio_testes.md).

## 6. Variáveis de ambiente

Nenhum valor secreto fica no repositório. Em desenvolvimento os valores vêm do `.env` (ignorado pelo Git; modelo em [`.env.example`](.env.example)); em produção, do painel do Render (lista em [`render.yaml`](render.yaml)).

| Variável | Obrigatória | Descrição |
|---|---|---|
| `SECRET_KEY` | Sim | Chave secreta do Django (50+ caracteres aleatórios) |
| `DEBUG` | Não | `True` só em desenvolvimento; padrão `False` |
| `ALLOWED_HOSTS` | Não | Domínios aceitos, separados por vírgula; padrão `localhost,127.0.0.1` |
| `CSRF_TRUSTED_ORIGINS` | Não | Origens confiáveis para CSRF (com `https://`) |
| `DATABASE_URL` | Produção | Connection string do PostgreSQL (Session pooler do Supabase); vazia = SQLite local |
| `DATABASE_SSL_REQUIRE` | Produção | `True` para exigir SSL na conexão com o banco |
| `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET` | Não | Credenciais do app no Spotify Developer Dashboard; sem elas, a importação fica desativada e o cadastro manual continua funcionando |
| `NUM_PROXIES`, `CLIENT_IP_HEADER` | Produção | Identificação do IP real do cliente atrás do proxy (Render: `0` e `HTTP_CF_CONNECTING_IP`) |
| `DEMO_PASSWORD` | Não | Senha das contas de teste criadas pelo `popular_demo` |
| `POPULAR_DEMO` | Não | `true` para criar os dados de demonstração no deploy |
| `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_PASSWORD` | Não | Administrador criado automaticamente no deploy |

O domínio do Render (`RENDER_EXTERNAL_HOSTNAME`) é informado pela própria plataforma e liberado automaticamente.

## 7. Publicação

A aplicação é publicada no **Render** a partir do Blueprint [`render.yaml`](render.yaml), com banco **PostgreSQL no Supabase**. Cada push na branch `main` gera um deploy automático; o [`build.sh`](build.sh) instala as dependências, coleta os arquivos estáticos, aplica as migrations, verifica as configurações de produção (`check --deploy`) e prepara os dados de demonstração.

Em produção: `DEBUG=False`, HTTPS obrigatório com HSTS, cookies seguros, `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` restritos ao domínio publicado, Content-Security-Policy restritiva e segredos apenas em variáveis de ambiente. Passo a passo em [`docs/deploy/guia_deploy.md`](docs/deploy/guia_deploy.md).

## 8. Segurança

| Análise | Ferramentas | Resultado |
|---|---|---|
| SAST | Bandit 1.9.4, Semgrep 1.186.0, pip-audit 2.10.1 e revisão manual | 4 achados confirmados corrigidos (força bruta no login, limite da API contornável, CSV injection, tabelas expostas pela Data API do Supabase); 0 CVEs nas dependências |
| DAST | OWASP ZAP 2.17.0 contra a aplicação publicada | 5 achados confirmados corrigidos (CSP, SRI, CORS nos estáticos, Swagger de CDN, cookie CSRF); 3 falsos positivos comprovados; 0 achados em aberto |

Escopo, configuração, relatórios brutos, triagem, falsos positivos, riscos aceitos e comparação antes/depois em [`docs/seguranca/relatorio_seguranca.md`](docs/seguranca/relatorio_seguranca.md).

## 9. Documentação

| Fase | Documento | Local |
|---|---|---|
| 1 | Documento de Visão | [`docs/visao/documento_de_visao.md`](docs/visao/documento_de_visao.md) |
| 1 | Casos de uso (UML + especificações) | [`docs/casos-de-uso/especificacao_casos_de_uso.md`](docs/casos-de-uso/especificacao_casos_de_uso.md) |
| 1 | Arquitetura | [`docs/arquitetura/documento_arquitetura.md`](docs/arquitetura/documento_arquitetura.md) |
| 1 | Modelo de dados | [`docs/banco-de-dados/modelo_de_dados.md`](docs/banco-de-dados/modelo_de_dados.md) |
| 1 | Contrato da API e plano de integração | [`docs/api/documento_api.md`](docs/api/documento_api.md) |
| 1 | Identidade visual e protótipos | [`docs/prototipos/identidade_e_prototipos.md`](docs/prototipos/identidade_e_prototipos.md) |
| 1 | Backlog e planejamento | [`docs/planejamento/backlog_e_planejamento.md`](docs/planejamento/backlog_e_planejamento.md) |
| 1 | Imagens dos diagramas | [`docs/diagramas/`](docs/diagramas/) |
| 2 | Mudanças em relação à Fase 1 (com DER implementado) | [`docs/fase2/mudancas_fase1.md`](docs/fase2/mudancas_fase1.md) |
| 2 | Guia da API v1 | [`docs/api/guia_api_v1.md`](docs/api/guia_api_v1.md) |
| 2 | Relatório de testes, roteiro manual e coleção Postman | [`docs/testes/`](docs/testes/) |
| 2 | Relatório de segurança (SAST e DAST) e evidências | [`docs/seguranca/`](docs/seguranca/) |
| 2 | Guia de deploy | [`docs/deploy/guia_deploy.md`](docs/deploy/guia_deploy.md) |

## 10. Estrutura do repositório

```text
├── accounts/              # Usuário com login por e-mail, cadastro e proteção contra força bruta
├── acervo/                # Álbuns, faixas, avaliações, coleções, busca, relatórios
│   ├── services/          # SpotifyService (integração externa)
│   └── management/        # Comandos popular_demo e buscar_capas
├── api/                   # API REST v1 (DRF): serializers, views, autenticação, permissões
├── core/                  # Página inicial, middlewares de segurança, migration de proteção do Supabase
├── config/                # settings.py, urls.py, wsgi.py
├── templates/             # Layout base, páginas de erro e componentes de formulário
├── static/                # CSS, JS, logotipo, fontes e Bootstrap (servidos pelo WhiteNoise)
├── docs/                  # Documentação das Fases 1 e 2
├── build.sh, render.yaml  # Deploy no Render
├── requirements.txt       # Dependências de produção (versões fixas)
└── requirements-dev.txt   # Dependências de testes e análise de segurança
```

## 11. Licença e créditos

Projeto acadêmico desenvolvido para a disciplina de Desenvolvimento Web do CEUB. O código é de autoria dos integrantes e seu uso fica restrito a fins educacionais.

Componentes de terceiros, usados conforme suas licenças:

| Componente | Licença |
|---|---|
| Django, Django REST Framework, drf-spectacular | BSD-3-Clause |
| Bootstrap 5.3.3 | MIT |
| Swagger UI (via drf-spectacular-sidecar) | Apache-2.0 |
| Fontes Inter e Montserrat | SIL Open Font License 1.1 ([`static/fonts/LICENSE.txt`](static/fonts/LICENSE.txt)) |
| WhiteNoise, gunicorn, requests | MIT / Apache-2.0 |

Metadados e capas de álbuns obtidos pela [Spotify Web API](https://developer.spotify.com/documentation/web-api), conforme os termos de uso para desenvolvedores do Spotify.
