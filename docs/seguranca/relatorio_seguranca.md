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
| Revisão manual | 2 | 0 | 2 | 0 |
| **Total** | **20** | **1** | **3** | **16** |

### 1.4 Depois: triagem, priorização e correções

Classificação: **severidade** (impacto se explorado) × **probabilidade** (facilidade de explorar no TrackVault) → **prioridade**.

#### Achados confirmados e corrigidos

| ID | Fonte | Achado | Severidade | Probabilidade | Prioridade | Correção |
|---|---|---|---|---|---|---|
| SAST-01 | Revisão manual | **Login do site sem limite de tentativas.** A tela `/contas/entrar/` aceitava tentativas ilimitadas de senha (força bruta / *credential stuffing*). A API já tinha limite, o site não. | Média | Alta (ataque automatizável) | **1** | Bloqueio por conta: após 5 senhas erradas para um e-mail, novas tentativas são recusadas por 15 min, mesmo com a senha certa. O contador é compartilhado entre o site e a API (`accounts/protecao.py`). Em produção o cache fica no banco, compartilhado entre os workers do gunicorn. |
| SAST-02 | Revisão manual | **Limite da API contornável com `X-Forwarded-For` forjado.** Sem `NUM_PROXIES`, o DRF usa o cabeçalho `X-Forwarded-For` inteiro como identidade do cliente; trocando o valor a cada requisição, o atacante escapava do limite de 5 tentativas/min em `/auth/token/`. | Média | Alta | **2** | `NUM_PROXIES` configurável (0 local, 1 no Render): o DRF passa a usar apenas o IP anotado pelo proxy do Render. |
| SAST-03 | Semgrep `csv-writer-injection` | **CSV injection na exportação do relatório.** Já havia proteção para os campos de texto, mas ela não cobria todas as colunas nem fórmulas precedidas de espaço (`"  =1+1"`). | Baixa (exige o usuário abrir o CSV no Excel e aceitar avisos) | Baixa | **3** | Sanitização aplicada a **todas** as células, inclusive após espaços, e ampliada para `\|` e `%` (`_linha_csv_segura`, `acervo/views.py`). |

Cada correção tem teste automatizado:

| ID | Teste | Evidência |
|---|---|---|
| SAST-01 | `accounts/tests.py::test_bloqueia_apos_5_tentativas_erradas`, `test_login_certo_zera_contagem`; `api/tests.py::test_bloqueio_por_conta_compartilhado_com_o_site` | 6ª tentativa com a senha certa é recusada |
| SAST-02 | `api/tests.py::test_x_forwarded_for_forjado_nao_burla_limite` | **Sem a correção** o teste falha (`400 != 429`: o atacante continua tentando); **com a correção** retorna `429 Too Many Requests` |
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
| `NUM_PROXIES=1` assume uma camada de proxy no Render | Se houver mais camadas, o efeito é **mais restritivo** (clientes compartilham o limite), nunca permite contornar. A validar nos logs após o deploy. |

### 1.5 Verificação: nova análise após as correções

Relatórios em [`sast/2-final/`](sast/2-final/).

| Fonte | Inicial | Final | Observação |
|---|---|---|---|
| Semgrep | 2 | **0** | 1 corrigido (SAST-03) + 1 falso positivo anotado |
| Bandit — código da aplicação | 4 | **0** | Falsos positivos anotados com `# nosec` e justificativa |
| Bandit — arquivos de teste | 12 | 18 | Apenas senhas fictícias de teste (risco aceito); o número subiu porque foram criados testes novos para SAST-01 e SAST-02 |
| pip-audit | 0 | **0** | 25 pacotes, nenhuma CVE conhecida |
| Revisão manual | 2 | **0** | SAST-01 e SAST-02 corrigidos e cobertos por testes |
| Testes automatizados | 95 aprovados | **100 aprovados** | 5 testes novos de segurança |

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
