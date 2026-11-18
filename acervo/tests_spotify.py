"""
Testes da integração com o Spotify (UC03).

O Spotify é simulado com unittest.mock: os testes não fazem chamadas reais,
então rodam sem internet e sem credenciais, e conseguem reproduzir falhas
(timeout, queda de conexão, JSON inválido, limite de requisições).
"""

from unittest import mock

import requests
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import Usuario

from .models import Album, Faixa
from .services import spotify_service
from .services.spotify_service import SpotifyIndisponivel

FAIXA_JSON = {
    'id': '1gihuPhrLraKYrJMAEONyc',
    'name': 'Feel So Close',
    'duration_ms': 206413,
    'popularity': 74,
    'external_ids': {'isrc': 'GBARL1100849'},
    'artists': [{'name': 'Calvin Harris'}],
    'album': {
        'id': '7w19PFbxAjwZ7UVNp9z0uT',
        'name': '18 Months',
        'release_date': '2012-10-26',
        'images': [{'url': 'https://i.scdn.co/image/capa-grande'}, {'url': 'https://i.scdn.co/image/capa-pequena'}],
    },
}


def resposta_fake(status=200, json_data=None, headers=None, json_invalido=False):
    resposta = mock.Mock(status_code=status, ok=200 <= status < 300, headers=headers or {})
    if json_invalido:
        resposta.json.side_effect = ValueError('JSON inválido')
    else:
        resposta.json.return_value = json_data
    resposta.raise_for_status.side_effect = (
        None if resposta.ok else requests.HTTPError(f'{status}')
    )
    return resposta


TOKEN_OK = resposta_fake(json_data={'access_token': 'token-123', 'expires_in': 3600})


@override_settings(SPOTIFY_CLIENT_ID='id-teste', SPOTIFY_CLIENT_SECRET='segredo-teste')
class SpotifyServiceTests(TestCase):
    def setUp(self):
        cache.clear()

    @mock.patch('acervo.services.spotify_service.requests.get')
    @mock.patch('acervo.services.spotify_service.requests.post', return_value=TOKEN_OK)
    def test_busca_converte_dados(self, post, get):
        get.return_value = resposta_fake(json_data={'tracks': {'items': [FAIXA_JSON]}})
        [faixa] = spotify_service.buscar_faixas('feel so close')

        self.assertEqual(faixa.titulo, 'Feel So Close')
        self.assertEqual(faixa.artista, 'Calvin Harris')
        self.assertEqual(faixa.isrc, 'GBARL1100849')
        self.assertEqual(faixa.album_ano, 2012)
        self.assertEqual(faixa.capa_url, 'https://i.scdn.co/image/capa-grande')
        self.assertEqual(faixa.duracao_formatada, '3:26')
        # Timeout de 5 s e token no cabeçalho, como no plano de integração.
        _, kwargs = get.call_args
        self.assertEqual(kwargs['timeout'], 5)
        self.assertEqual(kwargs['headers'], {'Authorization': 'Bearer token-123'})

    @mock.patch('acervo.services.spotify_service.requests.get')
    @mock.patch('acervo.services.spotify_service.requests.post', return_value=TOKEN_OK)
    def test_token_fica_em_cache(self, post, get):
        get.return_value = resposta_fake(json_data={'tracks': {'items': []}})
        spotify_service.buscar_faixas('a')
        spotify_service.buscar_faixas('b')
        self.assertEqual(post.call_count, 1)

    @mock.patch('acervo.services.spotify_service.requests.get')
    @mock.patch('acervo.services.spotify_service.requests.post', return_value=TOKEN_OK)
    def test_renova_token_expirado_uma_vez(self, post, get):
        get.side_effect = [
            resposta_fake(status=401),
            resposta_fake(json_data={'tracks': {'items': [FAIXA_JSON]}}),
        ]
        self.assertEqual(len(spotify_service.buscar_faixas('x')), 1)
        self.assertEqual(post.call_count, 2)

    @mock.patch('acervo.services.spotify_service.requests.get', side_effect=requests.Timeout)
    @mock.patch('acervo.services.spotify_service.requests.post', return_value=TOKEN_OK)
    def test_timeout(self, post, get):
        with self.assertRaisesMessage(SpotifyIndisponivel, 'temporariamente indisponível'):
            spotify_service.buscar_faixas('x')

    @mock.patch('acervo.services.spotify_service.requests.get', side_effect=requests.ConnectionError)
    @mock.patch('acervo.services.spotify_service.requests.post', return_value=TOKEN_OK)
    def test_falha_de_conexao(self, post, get):
        with self.assertRaises(SpotifyIndisponivel):
            spotify_service.buscar_faixas('x')

    @mock.patch('acervo.services.spotify_service.requests.post', side_effect=requests.ConnectionError)
    def test_falha_ao_obter_token(self, post):
        with self.assertRaises(SpotifyIndisponivel):
            spotify_service.buscar_faixas('x')

    @mock.patch('acervo.services.spotify_service.requests.get')
    @mock.patch('acervo.services.spotify_service.requests.post', return_value=TOKEN_OK)
    def test_limite_de_requisicoes(self, post, get):
        get.return_value = resposta_fake(status=429, headers={'Retry-After': '30'})
        with self.assertRaisesMessage(SpotifyIndisponivel, 'Tente novamente em 30 segundos'):
            spotify_service.buscar_faixas('x')

    @mock.patch('acervo.services.spotify_service.requests.get')
    @mock.patch('acervo.services.spotify_service.requests.post', return_value=TOKEN_OK)
    def test_json_invalido(self, post, get):
        get.return_value = resposta_fake(json_invalido=True)
        with self.assertRaises(SpotifyIndisponivel):
            spotify_service.buscar_faixas('x')

    @mock.patch('acervo.services.spotify_service.requests.get')
    @mock.patch('acervo.services.spotify_service.requests.post', return_value=TOKEN_OK)
    def test_formato_inesperado(self, post, get):
        get.return_value = resposta_fake(json_data={'erro': 'outra coisa'})
        with self.assertRaises(SpotifyIndisponivel):
            spotify_service.buscar_faixas('x')

    @mock.patch('acervo.services.spotify_service.requests.get')
    @mock.patch('acervo.services.spotify_service.requests.post', return_value=TOKEN_OK)
    def test_campos_opcionais_ausentes(self, post, get):
        # Se o Spotify deixar de enviar algum campo, a importação continua.
        minimo = {'id': 'abc123', 'name': 'Faixa', 'album': {'name': 'Álbum'}}
        get.return_value = resposta_fake(json_data=minimo)
        faixa = spotify_service.obter_faixa('abc123')
        self.assertIsNone(faixa.isrc)
        self.assertIsNone(faixa.popularidade)
        self.assertEqual(faixa.capa_url, '')

    def test_id_invalido_nao_chama_o_spotify(self):
        with self.assertRaisesMessage(SpotifyIndisponivel, 'inválido'):
            spotify_service.obter_faixa('../../me')

    @override_settings(SPOTIFY_CLIENT_ID='', SPOTIFY_CLIENT_SECRET='')
    def test_sem_credenciais(self):
        with self.assertRaisesMessage(SpotifyIndisponivel, 'não está configurada'):
            spotify_service.buscar_faixas('x')


@override_settings(SPOTIFY_CLIENT_ID='id-teste', SPOTIFY_CLIENT_SECRET='segredo-teste')
class ImportacaoViewTests(TestCase):
    def setUp(self):
        cache.clear()
        self.usuario = Usuario.objects.create_user(username='c', email='c@ex.com', password='SenhaForte!2026')
        self.client.force_login(self.usuario)
        self.url = reverse('acervo:importar_spotify')

    def test_exige_login(self):
        self.client.logout()
        self.assertEqual(self.client.get(self.url).status_code, 302)

    @mock.patch('acervo.services.spotify_service.buscar_faixas')
    def test_pesquisa_mostra_resultados(self, buscar):
        buscar.return_value = [spotify_service.FaixaSpotify.do_json(FAIXA_JSON)]
        resposta = self.client.get(self.url, {'q': 'feel so close'})
        self.assertContains(resposta, 'Feel So Close')
        self.assertContains(resposta, '18 Months')

    @mock.patch('acervo.services.spotify_service.buscar_faixas', side_effect=SpotifyIndisponivel())
    def test_spotify_fora_do_ar_mostra_fallback(self, buscar):
        resposta = self.client.get(self.url, {'q': 'x'})
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'temporariamente indisponível')
        self.assertContains(resposta, 'Cadastrar manualmente')

    @mock.patch('acervo.services.spotify_service.obter_faixa')
    def test_importar_preenche_formulario_e_salva(self, obter):
        obter.return_value = spotify_service.FaixaSpotify.do_json(FAIXA_JSON)

        resposta = self.client.post(self.url, {'spotify_id': FAIXA_JSON['id']})
        self.assertRedirects(resposta, reverse('acervo:faixa_nova'), fetch_redirect_response=False)
        album = Album.objects.get(spotify_id='7w19PFbxAjwZ7UVNp9z0uT')
        self.assertEqual(album.capa_url, 'https://i.scdn.co/image/capa-grande')

        # O formulário abre preenchido para o curador conferir (UC03, passo 4).
        form = self.client.get(reverse('acervo:faixa_nova')).context['form']
        self.assertEqual(form.initial['titulo'], 'Feel So Close')
        self.assertEqual(form.initial['isrc'], 'GBARL1100849')
        self.assertEqual(form.initial['album'], album.pk)

        # O curador completa gênero e BPM e salva.
        self.client.post(reverse('acervo:faixa_nova'), {
            'album': album.pk, 'titulo': 'Feel So Close', 'genero': 'eletronica', 'bpm': 128,
            'duracao_ms': 206413, 'isrc': 'GBARL1100849', 'popularidade': 74,
            'spotify_id': FAIXA_JSON['id'],
        })
        faixa = Faixa.objects.get()
        self.assertEqual(faixa.spotify_id, FAIXA_JSON['id'])
        self.assertEqual(faixa.bpm, 128)

    @mock.patch('acervo.services.spotify_service.obter_faixa')
    def test_reaproveita_album_cadastrado_manualmente(self, obter):
        manual = Album.objects.create(titulo='18 months', artista='calvin harris')
        obter.return_value = spotify_service.FaixaSpotify.do_json(FAIXA_JSON)
        self.client.post(self.url, {'spotify_id': FAIXA_JSON['id']})
        self.assertEqual(Album.objects.count(), 1)
        manual.refresh_from_db()
        self.assertEqual(manual.spotify_id, '7w19PFbxAjwZ7UVNp9z0uT')

    @mock.patch('acervo.services.spotify_service.obter_faixa')
    def test_faixa_ja_importada(self, obter):
        album = Album.objects.create(titulo='18 Months', artista='Calvin Harris')
        existente = Faixa.objects.create(album=album, titulo='Feel So Close', spotify_id=FAIXA_JSON['id'])
        obter.return_value = spotify_service.FaixaSpotify.do_json(FAIXA_JSON)
        resposta = self.client.post(self.url, {'spotify_id': FAIXA_JSON['id']})
        self.assertRedirects(resposta, existente.get_absolute_url())

    @mock.patch('acervo.services.spotify_service.obter_faixa', side_effect=SpotifyIndisponivel())
    def test_importacao_com_falha_volta_com_mensagem(self, obter):
        resposta = self.client.post(self.url, {'spotify_id': 'abc'}, follow=True)
        self.assertContains(resposta, 'temporariamente indisponível')
        self.assertFalse(Album.objects.exists())
