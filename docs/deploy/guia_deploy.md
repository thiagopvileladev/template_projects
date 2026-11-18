# Guia de Deploy — TrackVault (Render + Supabase)

## Arquitetura de implantação

```text
Navegador / cliente da API
        │  HTTPS (certificado gerenciado pelo Render)
        ▼
Render — Web Service "trackvault" (região Virgínia, EUA)
  gunicorn → Django (WhiteNoise serve os arquivos estáticos)
        │                                  │
        │ PostgreSQL + SSL                 │ HTTPS (Client Credentials)
        ▼                                  ▼
Supabase — PostgreSQL (us-east-1)     Spotify Web API
```

| Arquivo | Função |
|---|---|
| `render.yaml` | Blueprint: tipo de serviço, comandos e lista de variáveis de ambiente (sem valores secretos) |
| `build.sh` | Instala dependências, coleta estáticos, aplica migrations, roda `check --deploy`, cria admin e dados de demonstração |
| `requirements.txt` | Dependências de produção com versões fixas |

## Passo 1 — Banco de dados no Supabase

1. Crie uma conta em https://supabase.com e clique em **New project**.
2. Preencha:
   - **Name:** `trackvault`
   - **Database Password:** clique em **Generate a password** e **guarde a senha** (ela não aparece de novo).
   - **Region:** `East US (North Virginia)`.
3. Aguarde o projeto ficar pronto (1–2 minutos).
4. Clique em **Connect** (topo da página) e escolha **Session pooler**.
   - Use o *Session pooler*, e não a *Direct connection*: a conexão direta do Supabase usa IPv6, que o Render não suporta.
5. Copie a connection string. Ela tem este formato:
   ```
   postgresql://postgres.abcdefghijkl:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:5432/postgres
   ```
6. Troque `[YOUR-PASSWORD]` pela senha do passo 2. Se a senha tiver caracteres especiais (`@`, `#`, `/`, `:` etc.), codifique-os para URL (ex.: `@` → `%40`).

Essa string é o valor de `DATABASE_URL`. Ela é um segredo: não cole no código nem no GitHub.

**Proteção contra a Data API do Supabase:** o Supabase expõe o schema `public` por uma API REST própria. A migration `core/0001_protege_tabelas_supabase` (aplicada automaticamente pelo `build.sh`) ativa Row Level Security e revoga o acesso dos papéis públicos (`anon`, `authenticated`) a todas as tabelas. Ver achado SAST-04 em `docs/seguranca/relatorio_seguranca.md`. Como defesa adicional, a Data API pode ser desligada em **Project Settings → Data API**, já que o TrackVault não a utiliza.

## Passo 2 — Serviço web no Render

1. Crie uma conta em https://render.com usando **Sign in with GitHub** (a conta dona do repositório).
2. No painel: **New → Blueprint**.
3. Conecte o repositório do TrackVault. O Render lê o `render.yaml` e mostra o serviço `trackvault`.
4. Preencha as variáveis marcadas como secretas:

| Variável | Valor |
|---|---|
| `DATABASE_URL` | Connection string do Supabase (Passo 1) |
| `SPOTIFY_CLIENT_ID` / `SPOTIFY_CLIENT_SECRET` | Credenciais do app no Spotify Developer Dashboard |
| `DEMO_PASSWORD` | Senha das contas de teste (para informar ao professor) |
| `DJANGO_SUPERUSER_EMAIL` | E-mail do administrador |
| `DJANGO_SUPERUSER_USERNAME` | Nome de usuário do administrador |
| `DJANGO_SUPERUSER_PASSWORD` | Senha forte do administrador (não compartilhar) |

   `SECRET_KEY` é gerada automaticamente pelo Render. `DEBUG=False` já vem definido.

5. Clique em **Apply**. O primeiro deploy leva de 3 a 6 minutos. Acompanhe em **Logs**; o final esperado é algo como:
   ```
   Acervo de demonstração pronto: 7 álbuns, 11 faixas, 9 avaliações.
   ==> Your service is live 🎉
   ```
6. A URL pública aparece no topo do serviço: `https://trackvault-xxxx.onrender.com`. O HTTPS já vem ativo.

O domínio do Render é liberado automaticamente em `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` (variável `RENDER_EXTERNAL_HOSTNAME`), sem precisar configurar nada.

## Passo 3 — Verificação pós-deploy

| Verificação | Como | Esperado |
|---|---|---|
| Página inicial | Abrir a URL | Home com o acervo de demonstração |
| HTTPS forçado | Abrir `http://...` (sem s) | Redireciona para `https://` |
| Login | Entrar com `curador.demo@trackvault.app` e `DEMO_PASSWORD` | Login funciona |
| Spotify | **Nova faixa → Importar do Spotify** | Resultados com capas |
| API | Abrir `/api/v1/docs/` | Swagger carregado |
| Admin | Abrir `/admin/` com o superusuário | Painel do Django |
| Página de erro | Abrir `/nao-existe/` | Página 404 do TrackVault, sem detalhes técnicos |
| Cabeçalhos | https://securityheaders.com com a URL do site | HSTS, X-Frame-Options, X-Content-Type-Options presentes |

## Atualizações

O `autoDeploy` está ativo: cada `git push` na branch `main` gera um novo deploy automaticamente. Se um passo do `build.sh` falhar (ex.: migration com erro), o deploy é interrompido e a versão anterior continua no ar.

## Limitações do plano gratuito

| Serviço | Limitação | Como lidar |
|---|---|---|
| Render (free) | O serviço "dorme" após 15 min sem acesso; o primeiro acesso depois disso leva ~1 minuto | Abrir o site alguns minutos antes da apresentação e da avaliação |
| Render (free) | Sem acesso a terminal (shell) | Admin e dados de demonstração são criados pelo `build.sh` via variáveis de ambiente |
| Supabase (free) | Projeto é pausado após 7 dias sem atividade | Acessar o site pelo menos uma vez por semana até o fim da avaliação; se pausar, reativar no painel do Supabase |

## Rodar como produção localmente (opcional)

```bash
# No .env: DEBUG=False
python manage.py collectstatic --noinput
python manage.py check --deploy
```
