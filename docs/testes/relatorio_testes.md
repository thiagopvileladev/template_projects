# Relatório de Testes — TrackVault

A estratégia de testes tem três frentes, como pede a especificação (seção 7.1):

| Frente | Ferramenta | Onde |
|---|---|---|
| Testes automatizados (funções principais e API) | `django.test` + `rest_framework.test`, cobertura com `coverage.py` | `*/tests.py`, `acervo/tests_*.py` |
| Coleção de requisições da API | Postman (formato v2.1, com asserções por requisição) | [`TrackVault_API.postman_collection.json`](TrackVault_API.postman_collection.json) |
| Roteiro de teste manual | Casos de teste ligados aos casos de uso | [`roteiro_teste_manual.md`](roteiro_teste_manual.md) |

## 1. Testes automatizados

### Como executar

```bash
pip install -r requirements-dev.txt
coverage run manage.py test
coverage report        # resumo no terminal
coverage html          # relatório navegável em htmlcov/index.html
```

Os testes usam um banco temporário criado e destruído a cada execução e **não acessam a internet**: a API do Spotify é simulada com `unittest.mock`, o que permite reproduzir falhas (timeout, queda de conexão, limite de requisições) de forma controlada.

### Resultado

Execução de 18/11/2026 (versão final) — Python 3.14.0, Django 5.2.19.

| Indicador | Valor |
|---|---|
| Testes executados | **119** |
| Aprovados | **119** |
| Falhas / erros | 0 |
| Cobertura de código (linhas + ramificações) | **94%** |

### Cobertura por caso de uso

| Caso de uso / requisito | Arquivo de teste | Testes | O que é verificado |
|---|---|---|---|
| UC01 — Autenticar-se | `accounts/tests.py` | 8 | Cadastro, e-mail duplicado (sem diferenciar maiúsculas), senha fraca, login por e-mail, mensagem genérica em credencial inválida, logout somente via POST, bloqueio após 5 tentativas erradas (SAST-01) |
| UC02 — Gerenciar acervo | `acervo/tests.py` | 20 | CRUD de álbuns, faixas, avaliações e coleções; validações (ano futuro, BPM, ISRC, nota 0–10); exclusão em cascata; login obrigatório; usuário não altera dados de outro (404); coleção privada invisível |
| UC03 — Importar do Spotify | `acervo/tests_spotify.py` | 25 | Conversão do JSON, timeout de 5 s, cache do token, renovação após 401, falha de conexão, HTTP 429, JSON inválido, campos ausentes, credenciais ausentes, fluxo completo de importação, fallback manual e comando `buscar_capas` (correspondência de título e artista, simulação, Spotify fora do ar) |
| UC04 — Buscar músicas | `acervo/tests.py` (`BuscaTests`) | 11 | Busca livre, filtros combinados, nota mínima, faixa de BPM, coleção, ordenação, nenhum resultado, filtros inválidos validados no servidor, paginação preservando filtros |
| UC05 — Relatório | `acervo/tests_relatorio.py` | 13 | Cada indicador conferido com valores calculados à mão, escopo "minhas avaliações", filtros, intervalo inválido, exportação CSV e proteção contra CSV injection (SAST-03) |
| UC06 — API REST | `api/tests.py` | 26 | Códigos 200, 201, 204, 400, 401, 403, 404, 405 e 429; paginação; filtros; Bearer token; e-mails não expostos; Swagger/OpenAPI no ar; limites resistentes a `X-Forwarded-For` forjado e a proxies rotativos (SAST-02) |
| Página inicial e dados de demonstração | `core/tests.py` | 5 | Indicadores e cards da home, menu conforme login, comando `popular_demo` idempotente |
| Segurança (regressão do DAST) | `core/tests_seguranca.py` | 11 | CSP restritiva, `Permissions-Policy`, cookie CSRF HttpOnly, estáticos sem CORS aberto, nenhuma página com JS/CSS inline, nenhum recurso de CDN externo, payloads de SQL injection na busca e na paginação da API |

### Cobertura por módulo (principais)

| Módulo | Cobertura |
|---|---|
| `accounts/forms.py`, `api/serializers.py`, `core/views.py`, `acervo/management/commands/buscar_capas.py` | 100% |
| `acervo/busca.py`, `acervo/relatorios.py`, `core/middleware.py` | 97% |
| `acervo/views.py`, `api/views.py` | 95% |
| `accounts/protecao.py` | 90% |
| `acervo/services/spotify_service.py` | 86% |
| **Total** | **94%** |

As linhas não cobertas são, em sua maioria, as configurações de produção de `config/settings.py` (ativadas apenas com `DEBUG=False`, verificadas no deploy) e ramos defensivos raros do serviço do Spotify (por exemplo, HTTP 404 e erros genéricos 5xx).

## 2. Coleção de requisições da API

Arquivo: [`TrackVault_API.postman_collection.json`](TrackVault_API.postman_collection.json) — 18 requisições em 5 pastas (autenticação, faixas, álbuns/coleções, avaliações e documentação). Cada requisição contém asserções automáticas do código HTTP e do formato do JSON.

1. Importe o arquivo no Postman (também funciona no Insomnia e no Thunder Client).
2. Ajuste as variáveis `base_url`, `email` e `senha` (use uma conta de teste).
3. Execute com o **Collection Runner**. O token é salvo automaticamente após a primeira requisição.

Para gerar um acervo e contas de teste: `python manage.py popular_demo` (ver README).

## 3. Roteiro de teste manual

Ver [`roteiro_teste_manual.md`](roteiro_teste_manual.md). Cobre os fluxos pela interface, a responsividade e a impressão do relatório, que não são verificáveis pelos testes automatizados.
