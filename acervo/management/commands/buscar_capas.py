"""
Completa as capas dos álbuns usando a Spotify Web API.

Uso:
    python manage.py buscar_capas            # grava capa e ID do Spotify
    python manage.py buscar_capas --simular  # só mostra o que encontraria

Procura apenas os álbuns sem capa, usando o mesmo SpotifyService do cadastro
(timeout, token em cache e tratamento de falhas). Só aceita um resultado
quando título e artista correspondem, para não gravar capa errada.

Nunca interrompe o deploy: se o Spotify estiver fora do ar ou sem
credenciais, avisa e termina normalmente; o site continua mostrando o
ícone padrão no lugar da capa.
"""

from django.core.management.base import BaseCommand

from acervo.models import Album
from acervo.services import spotify_service


class Command(BaseCommand):
    help = 'Busca no Spotify as capas dos álbuns que ainda não têm capa.'

    def add_arguments(self, parser):
        parser.add_argument('--simular', action='store_true', help='Não grava nada, só mostra os resultados.')

    def handle(self, *args, simular=False, **options):
        if not spotify_service.configurado():
            self.stdout.write(self.style.WARNING('Spotify não configurado: capas não foram buscadas.'))
            return

        encontradas, sem_resultado = 0, []
        for album in Album.objects.filter(capa_url=''):
            try:
                resultado = spotify_service.buscar_album(album.titulo, album.artista)
            except spotify_service.SpotifyIndisponivel as erro:
                self.stdout.write(self.style.WARNING(f'Spotify indisponível ({erro}). Busca interrompida.'))
                break

            if resultado is None:
                sem_resultado.append(str(album))
                continue

            encontradas += 1
            self.stdout.write(f'  {album} -> "{resultado.titulo}"')
            if simular:
                continue
            album.capa_url = resultado.capa_url
            # O ID do Spotify é único: só grava se nenhum outro álbum já o usa.
            if not album.spotify_id and not Album.objects.filter(spotify_id=resultado.spotify_id).exists():
                album.spotify_id = resultado.spotify_id
            album.save(update_fields=['capa_url', 'spotify_id'])

        acao = 'encontradas (simulação, nada gravado)' if simular else 'atualizadas'
        self.stdout.write(self.style.SUCCESS(f'Capas {acao}: {encontradas}.'))
        if sem_resultado:
            self.stdout.write('Sem correspondência confiável: ' + '; '.join(sem_resultado))
