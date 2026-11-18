"""
Configurações do projeto TrackVault.

Valores sensíveis ou que mudam entre ambientes (desenvolvimento x produção)
são lidos de variáveis de ambiente via python-decouple. Em desenvolvimento,
eles vêm do arquivo .env (que NÃO é versionado); em produção (Render), são
cadastrados no painel da hospedagem. Veja .env.example.
"""

import sys
from pathlib import Path

import dj_database_url
from decouple import Csv, config
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


# --- Segurança básica -------------------------------------------------------

SECRET_KEY = config('SECRET_KEY')

# Padrão False: se a variável não for definida, o sistema sobe em modo seguro.
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())

# O Render informa o domínio público do serviço (ex.: trackvault.onrender.com).
# Ele é liberado automaticamente; nenhum outro host é aceito.
RENDER_EXTERNAL_HOSTNAME = config('RENDER_EXTERNAL_HOSTNAME', default='')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')


# --- Aplicações ---------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Terceiros
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'drf_spectacular_sidecar',  # Swagger UI servido localmente (DAST-06)
    # Apps do projeto
    'core',
    'accounts',
    'acervo',
    'api',
]

# Usuário customizado com login por e-mail (UC01).
AUTH_USER_MODEL = 'accounts.Usuario'

LOGIN_URL = 'accounts:login'

# O cookie CSRF não é lido por JavaScript no TrackVault (achado DAST-05).
CSRF_COOKIE_HTTPONLY = True

LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'core:home'

MIDDLEWARE = [
    # Primeiro: define o IP real do cliente antes de qualquer outro uso.
    'core.middleware.IPRealDoClienteMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # CSP e Permissions-Policy (achado DAST-02).
    'core.middleware.CabecalhosSegurancaMiddleware',
    # WhiteNoise serve os arquivos estáticos em produção sem servidor extra.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# --- Banco de dados -----------------------------------------------------------
# DATABASE_URL define o banco. Sem ela, usa SQLite local (desenvolvimento).
# Em produção aponta para o PostgreSQL do Supabase, exigindo SSL.

# Espaços e quebras de linha sobrando (comuns ao colar no painel) são ignorados.
DATABASE_URL = config('DATABASE_URL', default='').strip()
if DATABASE_URL and not DATABASE_URL.startswith(('postgresql://', 'postgres://', 'sqlite://')):
    # Mensagem clara sem exibir a URL (ela contém a senha do banco).
    raise ImproperlyConfigured(
        'DATABASE_URL inválida: deve começar com "postgresql://". '
        'Confira o valor colado nas variáveis de ambiente.'
    )

DATABASES = {
    'default': dj_database_url.parse(
        DATABASE_URL or f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        ssl_require=config('DATABASE_SSL_REQUIRE', default=False, cast=bool),
    )
}


# --- Senhas -------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- Idioma e fuso horário ----------------------------------------------------

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# --- Arquivos estáticos -------------------------------------------------------

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

# Nos testes não há collectstatic, então o manifesto não existe.
if 'test' in sys.argv:
    STORAGES['staticfiles'] = {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Remove Access-Control-Allow-Origin: * dos estáticos (achado DAST-03).
# O WhiteNoise exige a própria função (não o caminho em texto).
from core.middleware import remover_cors_dos_estaticos  # noqa: E402

WHITENOISE_ADD_HEADERS_FUNCTION = remover_cors_dos_estaticos


# --- Cache ------------------------------------------------------------------------
# Usado pelo token do Spotify, pelos limites da API e pelo bloqueio de login.
# Em produção fica no banco, compartilhado entre os workers do gunicorn
# (em memória, cada worker teria a sua própria contagem de tentativas).

if DEBUG or 'test' in sys.argv:
    CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}
else:
    CACHES = {'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'trackvault_cache',
    }}


# --- API REST própria (docs/api/documento_api.md, seção 1) --------------------

REST_FRAMEWORK = {
    # Leitura pública; escrita exige token (Authorization: Bearer <token>).
    'DEFAULT_AUTHENTICATION_CLASSES': ['api.autenticacao.BearerTokenAuthentication'],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
    'DEFAULT_PAGINATION_CLASS': 'api.paginacao.Paginacao',
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_PARSER_CLASSES': ['rest_framework.parsers.JSONParser'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # Limites de uso (PDF 7.3): protege contra abuso e força bruta no token.
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/min',
        'user': '120/min',
        'token': '5/min',  # nosec B105 - taxa de requisições, não é senha
    },
    # Achado SAST-02: 0 = identifica o cliente pelo REMOTE_ADDR e ignora o
    # X-Forwarded-For (que o cliente pode forjar). Em produção o REMOTE_ADDR
    # já vem corrigido pelo IPRealDoClienteMiddleware (CF-Connecting-IP).
    'NUM_PROXIES': config('NUM_PROXIES', default=0, cast=int),
}

# Cabeçalho confiável com o IP real do cliente (formato request.META).
# Render (atrás do Cloudflare): HTTP_CF_CONNECTING_IP. Local: vazio.
CLIENT_IP_HEADER = config('CLIENT_IP_HEADER', default='')

SPECTACULAR_SETTINGS = {
    'TITLE': 'TrackVault API',
    'DESCRIPTION': (
        'API REST do TrackVault para consulta do acervo musical e registro de avaliações.\n\n'
        '**Leitura** (GET) é pública. **Escrita** exige token: obtenha em '
        '`POST /api/v1/auth/token/` e envie no cabeçalho `Authorization: Bearer <token>`.\n\n'
        '**Limites:** 60 req/min sem autenticação, 120 req/min autenticado e 5 req/min '
        'para geração de token. Acima disso a resposta é `429 Too Many Requests`.'
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # Swagger UI hospedado no próprio site, sem CDN externo (achado DAST-06).
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    # Não envia o esquema para o validador externo do swagger.io.
    'SWAGGER_UI_SETTINGS': {'validatorUrl': None, 'deepLinking': True, 'persistAuthorization': True},
    'COMPONENT_SPLIT_REQUEST': True,
}


# --- Spotify Web API (docs/api/documento_api.md, seção 2) ---------------------

SPOTIFY_CLIENT_ID = config('SPOTIFY_CLIENT_ID', default='')
SPOTIFY_CLIENT_SECRET = config('SPOTIFY_CLIENT_SECRET', default='')
SPOTIFY_TIMEOUT = 5  # segundos, conforme o plano de integração


# --- Segurança em produção (PDF, seção 7.2) -----------------------------------
# Só ativadas com DEBUG=False, para não atrapalhar o desenvolvimento local.

if not DEBUG:
    # O Render termina o HTTPS no proxy e repassa este cabeçalho.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30  # 30 dias
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = 'same-origin'
    X_FRAME_OPTIONS = 'DENY'


# --- Logs -------------------------------------------------------------------------
# Em produção, os logs vão para a saída padrão e aparecem no painel do Render.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simples': {'format': '{asctime} {levelname} {name}: {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'simples'},
    },
    'root': {'handlers': ['console'], 'level': 'WARNING'},
    'loggers': {
        'django': {'handlers': ['console'], 'level': config('DJANGO_LOG_LEVEL', default='INFO'), 'propagate': False},
    },
}
