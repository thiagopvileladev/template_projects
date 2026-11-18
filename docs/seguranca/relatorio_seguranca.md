# Relatório de Segurança — TrackVault

Síntese das análises de segurança exigidas na seção 7.5 da especificação: **SAST** (análise estática do código e das dependências, sem executar a aplicação) e **DAST** (análise dinâmica da aplicação em execução).

| Análise | Situação | Evidências |
|---|---|---|
| SAST | ✅ Concluída | [`sast/1-inicial/`](sast/1-inicial/), [`sast/2-final/`](sast/2-final/) |
| DAST | ⏳ Pendente: depende da aplicação publicada (ver seção 2) | `dast/` |

---

## 1. SAST — Análise estática

### 1.1 Antes: escopo e alvo

| Item | Valor |
|---|---|
| Alvo | Código-fonte do repositório TrackVault (Python/Django) e dependências de produção (`requirements.txt`) |
| Pertence ao grupo | Sim, repositório do próprio grupo |
| Commit-base analisado | `d475b42` (branch `main`, 17/11/2026), etapa 11 concluída |
| Incluído | Todos os arquivos `.py` do projeto (apps `accounts`, `acervo`, `api`, `core`, `config`), inclusive testes |
| Excluído | `.venv/` (bibliotecas de terceiros), `staticfiles/` (gerado), `static/vendor/` (Bootstrap minificado), `docs/` |
| Ambiente | Windows 11, Python 3.14.0, ambiente virtual do projeto |

### 1.2 Durante: ferramentas e execução

Data da execução: **17/11/2026**.

| Ferramenta | Versão | Tipo | Comando | Duração |
|---|---|---|---|---|
| [Bandit](https://bandit.readthedocs.io/) | 1.9.4 | SAST de código Python | `bandit -r . -x ./.venv,./staticfiles,./htmlcov -f json` | ~1,3 s |
| [Semgrep](https://semgrep.dev/) | 1.186.0 | SAST de código com regras de Python, Django e segredos | `semgrep scan --config p/python --config p/django --config p/secrets --metrics=off --exclude=.venv --exclude=staticfiles --exclude=htmlcov --exclude=static/vendor --exclude=docs` | ~6 s |
| [pip-audit](https://pypi.org/project/pip-audit/) | 2.10.1 | Análise de dependências (CVEs conhecidas, base PyPI/OSV) | `pip-audit -r requirements.txt -f json` | ~28 s |

O pip-audit complementa o SAST, sem substituí-lo, como orienta a especificação. Além das ferramentas, foi feita **revisão manual de código** focada em autenticação, controle de acesso e limites de uso, que ferramentas de padrão não detectam.

Relatórios brutos guardados em [`sast/1-inicial/`](sast/1-inicial/) (`bandit.json`, `bandit.txt`, `semgrep.json`, `pip-audit.json`).

### 1.3 Resultado da análise inicial

| Fonte | Achados | Alta | Média | Baixa |
|---|---|---|---|---|
| Bandit | 16 | 0 | 0 | 16 |
| Semgrep | 2 | 1 (ERROR) | 1 (WARNING) | 0 |
| pip-audit (25 pacotes) | 0 | — | — | — |
| Revisão manual de código | 2 | 0 | 2 | 0 |
| Revisão de configuração da infraestrutura (Supabase) | 1 | 1 | 0 | 0 |
| **Total** | **21** | **2** | **3** | **16** |

### 1.4 Depois: triagem, priorização e correções

Classificação: **severidade** (impacto se explorado) × **probabilidade** (facilidade de explorar no TrackVault) → **prioridade**.

#### Achados confirmados e corrigidos

| ID | Fonte | Achado | Severidade | Probabilidade | Prioridade | Correção |
|---|---|---|---|---|---|---|
| SAST-04 | Revisão de configuração (17/11/2026, ao criar o banco) | **Tabelas do Django expostas pela Data API do Supabase.** O Supabase publica automaticamente o schema `public` por uma API REST acessível com a chave `anon` (considerada pública). As 16 tabelas criadas pelas migrations estavam sem Row Level Security e com `SELECT` liberado para `anon` e `authenticated`, incluindo `accounts_usuario` (e-mails e hashes de senha), contornando todo o controle de acesso do Django. | **Alta** (dados pessoais e hashes de senha) | Média (exige a chave anon do projeto, que não é tratada como segredo pelo Supabase) | **1** | Migration versionada `core/migrations/0001_protege_tabelas_supabase.py`: ativa RLS em todas as tabelas, revoga os privilégios de `anon`/`authenticated` e altera os privilégios padrão para que tabelas futuras também nasçam protegidas. O Django conecta como `postgres` (dono das tabelas, com `BYPASSRLS`) e não é afetado. Em SQLite a migration não faz nada. |
| SAST-01 | Revisão manual | **Login do site sem limite de tentativas.** A tela `/contas/entrar/` aceitava tentativas ilimitadas de senha (força bruta / *credential stuffing*). A API já tinha limite, o site não. | Média | Alta (ataque automatizável) | **1** | Bloqueio por conta: após 5 senhas erradas para um e-mail, novas tentativas são recusadas por 15 min, mesmo com a senha certa. O contador é compartilhado entre o site e a API (`accounts/protecao.py`). Em produção o cache fica no banco, compartilhado entre os workers do gunicorn. |
| SAST-02 | Revisão manual + verificação em produção | **Limite da API ineficaz (identificação errada do cliente).** (a) Sem `NUM_PROXIES`, o DRF usa o `X-Forwarded-For` inteiro como identidade do cliente; trocando o valor a cada requisição, o atacante escapava do limite de 5 tentativas/min em `/auth/token/`. (b) A primeira correção (`NUM_PROXIES=1`) passou nos testes locais, mas **falhou em produção**: no Render, a requisição atravessa Cloudflare e proxies internos rotativos (`10.x.x.x`), e o limite passou a contar por proxy. Em produção, 7 tentativas seguidas não foram bloqueadas; a tabela de cache mostrou 3 "clientes" diferentes para um único cliente real. | Média | Alta | **2** | `NUM_PROXIES=0` (o `X-Forwarded-For` é ignorado) e o middleware `core/middleware.py` usa o cabeçalho `CF-Connecting-IP`, preenchido pelo Cloudflare, como IP do cliente (`CLIENT_IP_HEADER`, ativo só no Render). |
| SAST-03 | Semgrep `csv-writer-injection` | **CSV injection na exportação do relatório.** Já havia proteção para os campos de texto, mas ela não cobria todas as colunas nem fórmulas precedidas de espaço (`"  =1+1"`). | Baixa (exige o usuário abrir o CSV no Excel e aceitar avisos) | Baixa | **3** | Sanitização aplicada a **todas** as células, inclusive após espaços, e ampliada para `\|` e `%` (`_linha_csv_segura`, `acervo/views.py`). |

Cada correção tem teste automatizado:

| ID | Teste | Evidência |
|---|---|---|
| SAST-04 | Verificação direta no banco do Supabase antes e depois da migration | **Antes:** 16 tabelas, 0 com RLS, 16 com `SELECT` para `anon`. **Depois:** 16 com RLS, 0 privilégios para `anon`/`authenticated`; `SET ROLE anon; SELECT ... FROM accounts_usuario` → `InsufficientPrivilege`; o Django continua lendo e gravando normalmente. |
| SAST-01 | `accounts/tests.py::test_bloqueia_apos_5_tentativas_erradas`, `test_login_certo_zera_contagem`; `api/tests.py::test_bloqueio_por_conta_compartilhado_com_o_site` | 6ª tentativa com a senha certa é recusada |
| SAST-02 | `api/tests.py::test_x_forwarded_for_forjado_nao_burla_limite`, `test_render_proxies_rotativos_usam_ip_do_cloudflare`, `test_cabecalho_de_ip_invalido_e_ignorado` | **Sem a correção** os testes falham (`[400, 400, 400, 400, 400, 400]`, idêntico ao observado em produção); **com a correção** a 6ª tentativa retorna `429`. **Verificação em produção (17/11/2026):** uso normal → `[400×5, 429, 429]`; forjando `X-Forwarded-For` → `[400×5, 429, 429]`; forjando `CF-Connecting-IP` → `403` do próprio Cloudflare em todas as tentativas. |
| SAST-03 | `acervo/tests_relatorio.py::test_csv_neutraliza_formulas`, `test_csv_neutraliza_formula_apos_espacos` | Células perigosas exportadas como texto (`'=...`) |

#### Falsos positivos

| Fonte | Regra | Local | Por que é falso positivo | Tratamento |
|---|---|---|---|---|
| Bandit | B105 *hardcoded password* | `acervo/services/spotify_service.py:24` | `TOKEN_URL` é a URL pública do OAuth do Spotify; o nome da variável contém "token" | `# nosec B105` com justificativa |
| Bandit | B105 | `acervo/services/spotify_service.py:26` | `CACHE_TOKEN` é o nome da chave no cache | `# nosec B105` com justificativa |
| Bandit | B105 | `api/views.py:149` | Texto de exemplo na documentação Swagger (`"sua-senha"`) | `# nosec B105` com justificativa |
| Bandit | B105 | `config/settings.py:167` | `'5/min'` é a taxa de requisições do limite `token` | `# nosec B105` com justificativa |
| Bandit | B105/B106 | 12 ocorrências em `*/tests.py` e `acervo/tests_*.py` | Senhas e tokens **fictícios** criados no banco temporário dos testes, destruído ao final; não dão acesso a nenhum ambiente real | Mantidos e documentados (ver riscos aceitos) |
| Semgrep | `logger-credential-disclosure` | `acervo/services/spotify_service.py:111` | A mensagem contém a palavra "token", mas registra apenas o **tipo** da exceção (ex.: `Timeout`), nunca o token ou as credenciais | `# nosemgrep` com justificativa |
| Semgrep | `csv-writer-injection` (após a correção) | `acervo/views.py` | A regra não reconhece o sanitizador próprio `_linha_csv_segura`, coberto por testes | `# nosemgrep` com justificativa |

#### Riscos aceitos

| Risco | Justificativa |
|---|---|
| Senhas fictícias em arquivos de teste (alertas B105/B106 do Bandit) | Necessárias para testar autenticação; existem só no banco temporário dos testes. Credenciais reais (`SECRET_KEY`, banco, Spotify, admin, contas de demonstração) vêm exclusivamente de variáveis de ambiente. |
| `SECURE_HSTS_PRELOAD` desativado (aviso do `manage.py check --deploy`) | A lista de *preload* dos navegadores exige domínio próprio; não se aplica ao subdomínio `*.onrender.com`. O HSTS está ativo (30 dias, `includeSubDomains`). |
| Bloqueio por conta pode ser usado para travar o login de um usuário por 15 min (negação de serviço direcionada) | Trade-off consciente: impedir a força bruta é mais importante no contexto acadêmico; o bloqueio expira sozinho e não afeta outras contas. |
| Identificação do cliente depende do Cloudflare na frente do Render (`CF-Connecting-IP`) | Verificado em produção: o Cloudflare recusa requisições que tentam enviar esse cabeçalho. Se o Render deixar de usar o Cloudflare, o cabeçalho deixa de chegar e o middleware mantém o `REMOTE_ADDR` (o limite fica menos eficaz, mas nada quebra); o teste em produção deve ser repetido após mudanças de infraestrutura. |
| `SECURE_HSTS_PRELOAD` e `SECRET_KEY` | O aviso `security.W009` do primeiro deploy (chave gerada pelo Render com menos de 50 caracteres) foi corrigido trocando a `SECRET_KEY` por uma de 50 caracteres gerada com `get_random_secret_key()`. |

### 1.5 Verificação: nova análise após as correções

Relatórios em [`sast/2-final/`](sast/2-final/).

| Fonte | Inicial | Final | Observação |
|---|---|---|---|
| Semgrep | 2 | **0** | 1 corrigido (SAST-03) + 1 falso positivo anotado |
| Bandit — código da aplicação | 4 | **0** | Falsos positivos anotados com `# nosec` e justificativa |
| Bandit — arquivos de teste | 12 | 18 | Apenas senhas fictícias de teste (risco aceito); o número subiu porque foram criados testes novos para SAST-01 e SAST-02 |
| pip-audit | 0 | **0** | 25 pacotes, nenhuma CVE conhecida |
| Revisão manual | 2 | **0** | SAST-01 e SAST-02 corrigidos e cobertos por testes |
| Revisão de configuração (Supabase) | 1 | **0** | SAST-04 corrigido por migration e verificado no banco |
| Testes automatizados | 95 aprovados | **102 aprovados** | 7 testes novos de segurança |

### 1.6 Como reproduzir

```bash
pip install -r requirements-dev.txt
bandit -r . -x ./.venv,./staticfiles,./htmlcov
semgrep scan --config p/python --config p/django --config p/secrets --metrics=off \
  --exclude=.venv --exclude=staticfiles --exclude=htmlcov --exclude=static/vendor --exclude=docs
pip-audit -r requirements.txt
```

---

## 2. DAST — Análise dinâmica

⏳ **Pendente.** O DAST precisa da aplicação publicada (etapa 11). Planejamento:

| Item | Plano |
|---|---|
| Ferramenta | OWASP ZAP (Baseline Scan e Full Scan autenticado), via Docker ou ZAP Desktop |
| Alvo | **Somente** a URL do TrackVault no Render, do próprio grupo (regra ética da seção 7.5). Não testar Spotify, Supabase nem o domínio do Render. |
| Dados | Banco com os dados de demonstração (`popular_demo`); nenhum dado pessoal real |
| Procedimento | Varredura inicial → triagem (severidade, probabilidade, falsos positivos) → correções → nova varredura e comparação |
| Pontos de atenção previstos | Ausência de `Content-Security-Policy`; recursos de terceiros (Google Fonts, Swagger UI via CDN) |
