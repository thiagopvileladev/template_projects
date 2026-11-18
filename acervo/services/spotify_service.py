"""
SpotifyService — camada de integração com a Spotify Web API.

Ver docs/api/documento_api.md (seção 2) e docs/arquitetura/documento_arquitetura.md.

- Autenticação: OAuth 2.0 Client Credentials. O token fica em cache até
  pouco antes de expirar ("OAuth Token Cache" do diagrama de componentes).
- Resiliência: timeout de 5 s, tratamento de falha de conexão, de resposta
  inválida, de limite de requisições (HTTP 429) e de token expirado (HTTP 401).
- Qualquer falha vira SpotifyIndisponivel, que a view transforma em uma
  mensagem amigável, permitindo o cadastro manual (fallback).
- As credenciais vêm de variáveis de ambiente e nunca são registradas em log.
"""

import logging
from dataclasses import dataclass

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_URL = 'https://api.spotify.com/v1'
CACHE_TOKEN = 'spotify:access_token'
MAX_RESULTADOS = 5


class SpotifyIndisponivel(Exception):
    """Falha ao consultar o Spotify. A mensagem já é adequada ao usuário."""

    MENSAGEM_PADRAO = (
        'A busca automática no Spotify está temporariamente indisponível. '
        'Você pode preencher os dados da faixa manualmente.'
    )

    def __init__(self, mensagem=None):
        super().__init__(mensagem or self.MENSAGEM_PADRAO)


@dataclass
class FaixaSpotify:
    """Dados de uma faixa do Spotify já convertidos para o domínio do TrackVault."""

    spotify_id: str
    titulo: str
    artista: str
    duracao_ms: int | None
    isrc: str | None
    popularidade: int | None
    album_spotify_id: str | None
    album_titulo: str
    album_ano: int | None
    capa_url: str

    @classmethod
    def do_json(cls, item):
        album = item.get('album') or {}
        artistas = item.get('artists') or album.get('artists') or []
        imagens = album.get('images') or []
        data = album.get('release_date') or ''
        return cls(
            spotify_id=item['id'],
            titulo=item['name'],
            artista=', '.join(a['name'] for a in artistas if a.get('name')) or 'Desconhecido',
            duracao_ms=item.get('duration_ms'),
            isrc=(item.get('external_ids') or {}).get('isrc'),
            popularidade=item.get('popularity'),
            album_spotify_id=album.get('id'),
            album_titulo=album.get('name') or item['name'],
            album_ano=int(data[:4]) if data[:4].isdigit() else None,
            # A primeira imagem é a de maior resolução.
            capa_url=imagens[0]['url'] if imagens else '',
        )

    @property
    def duracao_formatada(self):
        if not self.duracao_ms:
            return ''
        segundos = self.duracao_ms // 1000
        return f'{segundos // 60}:{segundos % 60:02d}'


def configurado():
    return bool(settings.SPOTIFY_CLIENT_ID and settings.SPOTIFY_CLIENT_SECRET)


def _obter_token(forcar_novo=False):
    if not configurado():
        raise SpotifyIndisponivel(
            'A integração com o Spotify não está configurada. '
            'Você pode preencher os dados da faixa manualmente.'
        )

    if not forcar_novo and (token := cache.get(CACHE_TOKEN)):
        return token

    try:
        resposta = requests.post(
            TOKEN_URL,
            data={'grant_type': 'client_credentials'},
            auth=(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET),
            timeout=settings.SPOTIFY_TIMEOUT,
        )
        resposta.raise_for_status()
        dados = resposta.json()
        token = dados['access_token']
        expira_em = int(dados.get('expires_in', 3600))
    except requests.RequestException as erro:
        logger.warning('Spotify: falha ao obter token (%s)', type(erro).__name__)
        raise SpotifyIndisponivel() from erro
    except (ValueError, KeyError, TypeError) as erro:
        logger.warning('Spotify: resposta de token inválida')
        raise SpotifyIndisponivel() from erro

    # Guarda com 60 s de folga para não usar um token prestes a expirar.
    cache.set(CACHE_TOKEN, token, max(expira_em - 60, 60))
    return token


def _get(caminho, params=None, tentativa=1):
    token = _obter_token(forcar_novo=tentativa > 1)
    try:
        resposta = requests.get(
            f'{API_URL}{caminho}',
            params=params,
            headers={'Authorization': f'Bearer {token}'},
            timeout=settings.SPOTIFY_TIMEOUT,
        )
    except requests.Timeout as erro:
        logger.warning('Spotify: timeout em %s', caminho)
        raise SpotifyIndisponivel() from erro
    except requests.RequestException as erro:
        logger.warning('Spotify: falha de conexão em %s (%s)', caminho, type(erro).__name__)
        raise SpotifyIndisponivel() from erro

    if resposta.status_code == 401 and tentativa == 1:
        # Token expirou antes do previsto: renova uma única vez.
        cache.delete(CACHE_TOKEN)
        return _get(caminho, params, tentativa=2)

    if resposta.status_code == 429:
        espera = resposta.headers.get('Retry-After', 'alguns')
        logger.warning('Spotify: limite de requisições atingido (Retry-After=%s)', espera)
        raise SpotifyIndisponivel(
            f'O limite de consultas ao Spotify foi atingido. Tente novamente em {espera} segundos '
            'ou preencha os dados manualmente.'
        )

    if resposta.status_code == 404:
        raise SpotifyIndisponivel('Faixa não encontrada no Spotify.')

    if not resposta.ok:
        logger.warning('Spotify: HTTP %s em %s', resposta.status_code, caminho)
        raise SpotifyIndisponivel()

    try:
        return resposta.json()
    except ValueError as erro:
        logger.warning('Spotify: JSON inválido em %s', caminho)
        raise SpotifyIndisponivel() from erro


def buscar_faixas(termo):
    """Pesquisa faixas pelo nome (GET /v1/search). Retorna lista de FaixaSpotify."""
    termo = (termo or '').strip()
    if not termo:
        return []
    dados = _get('/search', {'q': termo[:100], 'type': 'track', 'limit': MAX_RESULTADOS})
    try:
        itens = dados['tracks']['items']
        return [FaixaSpotify.do_json(item) for item in itens if item]
    except (KeyError, TypeError, ValueError) as erro:
        logger.warning('Spotify: formato inesperado na busca')
        raise SpotifyIndisponivel() from erro


def obter_faixa(spotify_id):
    """Busca uma faixa pelo ID (GET /v1/tracks/{id})."""
    if not spotify_id or not spotify_id.isalnum() or len(spotify_id) > 64:
        raise SpotifyIndisponivel('Identificador de faixa do Spotify inválido.')
    dados = _get(f'/tracks/{spotify_id}')
    try:
        return FaixaSpotify.do_json(dados)
    except (KeyError, TypeError, ValueError) as erro:
        logger.warning('Spotify: formato inesperado na faixa')
        raise SpotifyIndisponivel() from erro
