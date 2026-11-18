"""
Popula o banco com dados de demonstração (PDF, seção 7.2: "contas de teste ou
dados fictícios").

Uso:
    python manage.py popular_demo

A senha das contas de teste vem da variável de ambiente DEMO_PASSWORD. Se ela
não existir, uma senha aleatória é gerada e exibida uma única vez — nenhuma
senha fica gravada no código ou no repositório.

O comando é idempotente: rodar de novo não duplica nada.
"""

import os
import secrets

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import Usuario
from acervo.models import Album, Avaliacao, Colecao, Faixa

CONTAS = [
    ('curador.demo@trackvault.app', 'curador_demo'),
    ('critica.demo@trackvault.app', 'critica_demo'),
]

# (álbum, artista, ano, [(faixa, gênero, bpm, duração_ms)])
ACERVO = [
    ('18 Months', 'Calvin Harris', 2012, [
        ('Feel So Close', 'eletronica', 128, 206000),
        ('Sweet Nothing', 'eletronica', 128, 212000),
    ]),
    ('Random Access Memories', 'Daft Punk', 2013, [
        ('Get Lucky', 'eletronica', 116, 369000),
        ('Instant Crush', 'eletronica', 110, 337000),
    ]),
    ('Abbey Road', 'The Beatles', 1969, [
        ('Come Together', 'rock', 82, 259000),
        ('Here Comes the Sun', 'rock', 129, 185000),
    ]),
    ('Kind of Blue', 'Miles Davis', 1959, [
        ('So What', 'jazz', 136, 562000),
    ]),
    ('Elis & Tom', 'Elis Regina e Tom Jobim', 1974, [
        ('Águas de Março', 'mpb', 112, 213000),
    ]),
    ('To Pimp a Butterfly', 'Kendrick Lamar', 2015, [
        ('Alright', 'hip_hop', 110, 219000),
    ]),
    ('Currents', 'Tame Impala', 2015, [
        ('The Less I Know the Better', 'indie', 117, 216000),
        ('Let It Happen', 'indie', 125, 467000),
    ]),
]

# (faixa, conta, nota pessoal, nota Pitchfork, resenha)
AVALIACOES = [
    ('Feel So Close', 0, 9.0, 6.8, 'Sintetizadores limpos e um refrão que gruda.'),
    ('Get Lucky', 0, 9.5, 8.8, 'Groove impecável; a guitarra de Nile Rodgers carrega a faixa.'),
    ('Get Lucky', 1, 8.0, 8.8, 'Ótima, mas tocou demais no rádio.'),
    ('Come Together', 0, 10.0, 10.0, 'Linha de baixo histórica.'),
    ('So What', 1, 10.0, None, 'Aula de modalismo.'),
    ('Águas de Março', 0, 9.8, None, 'Diálogo perfeito entre as duas vozes.'),
    ('Alright', 1, 9.2, 9.3, 'Hino com produção densa e letra urgente.'),
    ('The Less I Know the Better', 0, 8.5, 9.1, 'Baixo hipnótico.'),
    ('Instant Crush', 1, 7.0, 8.8, None),
]


class Command(BaseCommand):
    help = 'Cria contas de teste e um acervo fictício para demonstração.'

    @transaction.atomic
    def handle(self, *args, **options):
        senha = os.environ.get('DEMO_PASSWORD')
        senha_gerada = not senha
        if senha_gerada:
            senha = secrets.token_urlsafe(12)

        contas = []
        for email, username in CONTAS:
            usuario, criado = Usuario.objects.get_or_create(email=email, defaults={'username': username})
            if criado or not senha_gerada:
                usuario.set_password(senha)
                usuario.save()
            contas.append(usuario)

        faixas = {}
        for titulo_album, artista, ano, lista in ACERVO:
            album, _ = Album.objects.get_or_create(
                titulo=titulo_album, artista=artista, defaults={'ano_lancamento': ano})
            for titulo, genero, bpm, duracao in lista:
                faixa, _ = Faixa.objects.get_or_create(
                    album=album, titulo=titulo,
                    defaults={'genero': genero, 'bpm': bpm, 'duracao_ms': duracao})
                faixas[titulo] = faixa

        for titulo, conta, nota, pitchfork, resenha in AVALIACOES:
            Avaliacao.objects.get_or_create(
                usuario=contas[conta], faixa=faixas[titulo],
                defaults={'nota_pessoal': nota, 'nota_pitchfork': pitchfork, 'resenha': resenha or ''})

        colecao, _ = Colecao.objects.get_or_create(
            usuario=contas[0], nome='Clássicos para domingo',
            defaults={'descricao': 'Faixas atemporais para ouvir sem pressa.', 'is_publica': True})
        colecao.faixas.add(faixas['Come Together'], faixas['So What'], faixas['Águas de Março'])

        privada, _ = Colecao.objects.get_or_create(
            usuario=contas[0], nome='Set de sexta (rascunho)',
            defaults={'descricao': 'Coleção privada de exemplo.', 'is_publica': False})
        privada.faixas.add(faixas['Feel So Close'], faixas['Get Lucky'], faixas['Let It Happen'])

        self.stdout.write(self.style.SUCCESS(
            f'Acervo de demonstração pronto: {Album.objects.count()} álbuns, '
            f'{Faixa.objects.count()} faixas, {Avaliacao.objects.count()} avaliações.'))
        self.stdout.write('Contas de teste: ' + ', '.join(email for email, _ in CONTAS))
        if senha_gerada:
            self.stdout.write(self.style.WARNING(
                f'Senha gerada (anote, não será exibida de novo): {senha}\n'
                'Para definir a sua, use a variável de ambiente DEMO_PASSWORD.'))
        else:
            self.stdout.write('Senha: a definida em DEMO_PASSWORD.')
