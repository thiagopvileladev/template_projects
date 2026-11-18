"""
Proteção das tabelas contra a Data API do Supabase (achado SAST-04).

O Supabase expõe automaticamente o schema "public" por uma API REST
(PostgREST), acessível com a chave "anon", que é pública. Sem esta migration,
as tabelas do Django (inclusive a de usuários, com e-mails e hashes de senha)
poderiam ser lidas por essa API, sem passar pelo Django.

O que é feito (somente em PostgreSQL com os papéis do Supabase):
1. Ativa Row Level Security (RLS) em todas as tabelas do schema public.
   Sem políticas, os papéis anon/authenticated não leem nenhuma linha.
2. Revoga os privilégios de anon e authenticated nas tabelas, sequências e
   funções existentes.
3. Altera os privilégios padrão: tabelas criadas no futuro (novas migrations,
   tabela de cache) também nascem sem acesso para esses papéis.

O Django conecta com o papel "postgres", dono das tabelas e com BYPASSRLS,
então continua funcionando normalmente. Em SQLite (desenvolvimento) e em
PostgreSQL sem os papéis do Supabase, a migration não faz nada.
"""

from django.db import migrations

PAPEIS_PUBLICOS = ('anon', 'authenticated')


def proteger(apps, schema_editor):
    conexao = schema_editor.connection
    if conexao.vendor != 'postgresql':
        return
    with conexao.cursor() as cursor:
        cursor.execute('SELECT rolname FROM pg_roles WHERE rolname = ANY(%s)', [list(PAPEIS_PUBLICOS)])
        papeis = [linha[0] for linha in cursor.fetchall()]
        if not papeis:
            return  # não é Supabase

        cursor.execute(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
        )
        for (tabela,) in cursor.fetchall():
            cursor.execute(f'ALTER TABLE public."{tabela}" ENABLE ROW LEVEL SECURITY')

        lista = ', '.join(papeis)
        for objeto in ('TABLES', 'SEQUENCES', 'FUNCTIONS'):
            cursor.execute(f'REVOKE ALL ON ALL {objeto} IN SCHEMA public FROM {lista}')
            cursor.execute(
                f'ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON {objeto} FROM {lista}'
            )


class Migration(migrations.Migration):
    # Roda depois que todas as tabelas do projeto existem.
    dependencies = [
        ('accounts', '0001_initial'),
        ('acervo', '0001_initial'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('authtoken', '0004_alter_tokenproxy_options'),
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(proteger, migrations.RunPython.noop),
    ]
