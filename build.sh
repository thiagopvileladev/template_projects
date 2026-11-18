#!/usr/bin/env bash
# Script de build executado pelo Render a cada deploy.
# Interrompe no primeiro erro, para não publicar uma versão quebrada.
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Arquivos estáticos (CSS, JS, imagens) servidos pelo WhiteNoise.
python manage.py collectstatic --noinput

# Cria/atualiza as tabelas no PostgreSQL do Supabase.
python manage.py migrate --noinput

# Tabela do cache compartilhado (bloqueio de login e limites da API).
python manage.py createcachetable

# Verificação das configurações de segurança de produção.
python manage.py check --deploy --fail-level ERROR

# Superusuário (admin) a partir de variáveis de ambiente, se definidas.
# DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_USERNAME e DJANGO_SUPERUSER_PASSWORD.
if [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ]; then
    python manage.py createsuperuser --noinput || echo "Superusuário já existe."
fi

# Dados de demonstração para a avaliação (idempotente).
if [ "${POPULAR_DEMO:-false}" = "true" ]; then
    python manage.py popular_demo
fi

# Capas dos álbuns sem capa, via Spotify (não interrompe o deploy se falhar).
python manage.py buscar_capas
