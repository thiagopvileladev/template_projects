from django.core.cache import cache
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.models import Usuario
from acervo.models import Album, Avaliacao, Colecao, Faixa

SENHA = 'SenhaForte!2026'
BASE = '/api/v1'


class BaseAPITest(APITestCase):
    def setUp(self):
        cache.clear()  # zera os contadores de limite de requisições
        self.curador = Usuario.objects.create_user(username='curador', email='c@ex.com', password=SENHA)
        self.outro = Usuario.objects.create_user(username='outro', email='o@ex.com', password=SENHA)
        self.album = Album.objects.create(titulo='18 Months', artista='Calvin Harris', ano_lancamento=2012)
        self.faixa = Faixa.objects.create(album=self.album, titulo='Feel So Close', genero='eletronica', bpm=128)
        rock_album = Album.objects.create(titulo='Rock Album', artista='Banda')
        self.rock = Faixa.objects.create(album=rock_album, titulo='Rock Song', genero='rock', bpm=150)

    def autenticar(self, usuario=None):
        token = Token.objects.create(user=usuario or self.curador)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.key}')


class FaixasAPITests(BaseAPITest):
    def test_listar_publico_com_paginacao(self):
        resposta = self.client.get(f'{BASE}/faixas/')
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta['Content-Type'], 'application/json')
        dados = resposta.json()
        self.assertEqual(dados['count'], 2)
        self.assertIn('next', dados)
        # Campos do contrato da Fase 1.
        faixa = next(f for f in dados['results'] if f['id'] == self.faixa.pk)
        for campo in ('id', 'titulo', 'artista', 'genero', 'bpm'):
            self.assertIn(campo, faixa)
        self.assertEqual(faixa['artista'], 'Calvin Harris')

    def test_filtros_do_contrato(self):
        dados = self.client.get(f'{BASE}/faixas/', {'genero': 'rock'}).json()
        self.assertEqual([f['titulo'] for f in dados['results']], ['Rock Song'])
        dados = self.client.get(f'{BASE}/faixas/', {'artista': 'calvin'}).json()
        self.assertEqual([f['titulo'] for f in dados['results']], ['Feel So Close'])

    def test_filtro_invalido_retorna_400(self):
        resposta = self.client.get(f'{BASE}/faixas/', {'nota_min': 50})
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nota_min', resposta.json())

    def test_page_size(self):
        dados = self.client.get(f'{BASE}/faixas/', {'page_size': 1}).json()
        self.assertEqual(len(dados['results']), 1)
        self.assertIsNotNone(dados['next'])

    def test_detalhe_e_404(self):
        self.assertEqual(self.client.get(f'{BASE}/faixas/{self.faixa.pk}/').json()['album']['titulo'], '18 Months')
        self.assertEqual(self.client.get(f'{BASE}/faixas/9999/').status_code, status.HTTP_404_NOT_FOUND)

    def test_acervo_e_somente_leitura(self):
        self.autenticar()
        resposta = self.client.post(f'{BASE}/faixas/', {'titulo': 'x'}, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_filtro_por_colecao_privada_nao_permitido(self):
        privada = Colecao.objects.create(usuario=self.curador, nome='Secreta')
        privada.faixas.add(self.faixa)
        resposta = self.client.get(f'{BASE}/faixas/', {'colecao': privada.pk})
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)


class AlbunsColecoesAPITests(BaseAPITest):
    def test_album_com_faixas(self):
        dados = self.client.get(f'{BASE}/albuns/{self.album.pk}/').json()
        self.assertEqual(dados['total_faixas'], 1)
        self.assertEqual(dados['faixas'][0]['titulo'], 'Feel So Close')

    def test_colecoes_so_publicas_e_sem_email(self):
        Colecao.objects.create(usuario=self.curador, nome='Pública', is_publica=True)
        Colecao.objects.create(usuario=self.curador, nome='Privada')
        resposta = self.client.get(f'{BASE}/colecoes/')
        nomes = [c['nome'] for c in resposta.json()['results']]
        self.assertEqual(nomes, ['Pública'])
        self.assertNotIn('c@ex.com', resposta.content.decode())


class TokenAPITests(BaseAPITest):
    def test_obter_token(self):
        resposta = self.client.post(f'{BASE}/auth/token/', {'email': 'C@EX.com', 'password': SENHA}, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.json()['token'], Token.objects.get(user=self.curador).key)

    def test_credenciais_invalidas(self):
        resposta = self.client.post(f'{BASE}/auth/token/', {'email': 'c@ex.com', 'password': 'errada'}, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('E-mail ou senha incorretos.', str(resposta.json()))

    def test_limite_de_tentativas(self):
        for _ in range(5):
            self.client.post(f'{BASE}/auth/token/', {'email': 'c@ex.com', 'password': 'errada'}, format='json')
        resposta = self.client.post(f'{BASE}/auth/token/', {'email': 'c@ex.com', 'password': SENHA}, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class AvaliacoesAPITests(BaseAPITest):
    URL = f'{BASE}/avaliacoes/'

    def test_criar_sem_token_retorna_401(self):
        resposta = self.client.post(self.URL, {'faixa_id': self.faixa.pk, 'nota_pessoal': 9}, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_invalido_retorna_401(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer token-falso')
        resposta = self.client.post(self.URL, {'faixa_id': self.faixa.pk, 'nota_pessoal': 9}, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_criar_avaliacao_201(self):
        self.autenticar()
        resposta = self.client.post(self.URL, {
            'faixa_id': self.faixa.pk, 'nota_pessoal': 9.5,
            'resenha': 'Excelente progressão de acordes no sintetizador principal.',
        }, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resposta.json()['usuario'], 'curador')
        self.assertEqual(Avaliacao.objects.get().usuario, self.curador)

    def test_validacoes_400(self):
        self.autenticar()
        resposta = self.client.post(self.URL, {'faixa_id': 9999, 'nota_pessoal': 11}, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        erros = resposta.json()
        self.assertIn('faixa_id', erros)
        self.assertIn('nota_pessoal', erros)

    def test_avaliacao_duplicada_400(self):
        Avaliacao.objects.create(usuario=self.curador, faixa=self.faixa, nota_pessoal=7)
        self.autenticar()
        resposta = self.client.post(self.URL, {'faixa_id': self.faixa.pk, 'nota_pessoal': 9}, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Você já avaliou esta faixa', str(resposta.json()))

    def test_nao_altera_avaliacao_de_outro_403(self):
        alheia = Avaliacao.objects.create(usuario=self.outro, faixa=self.faixa, nota_pessoal=7)
        self.autenticar()
        resposta = self.client.patch(f'{self.URL}{alheia.pk}/', {'nota_pessoal': 1}, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.delete(f'{self.URL}{alheia.pk}/').status_code, status.HTTP_403_FORBIDDEN)

    def test_alterar_e_excluir_a_propria(self):
        minha = Avaliacao.objects.create(usuario=self.curador, faixa=self.faixa, nota_pessoal=7)
        self.autenticar()
        resposta = self.client.patch(f'{self.URL}{minha.pk}/', {'nota_pessoal': 8.5}, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.json()['nota_pessoal'], 8.5)
        self.assertEqual(self.client.delete(f'{self.URL}{minha.pk}/').status_code, status.HTTP_204_NO_CONTENT)

    def test_listar_por_faixa(self):
        Avaliacao.objects.create(usuario=self.curador, faixa=self.faixa, nota_pessoal=7)
        Avaliacao.objects.create(usuario=self.curador, faixa=self.rock, nota_pessoal=5)
        dados = self.client.get(self.URL, {'faixa': self.rock.pk}).json()
        self.assertEqual(dados['count'], 1)

    def test_json_malformado_400(self):
        self.autenticar()
        resposta = self.client.post(self.URL, '{isso não é json', content_type='application/json')
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)


class DocumentacaoAPITests(BaseAPITest):
    def test_swagger_redoc_e_schema(self):
        self.assertEqual(self.client.get(f'{BASE}/docs/').status_code, 200)
        self.assertEqual(self.client.get(f'{BASE}/redoc/').status_code, 200)
        schema = self.client.get(f'{BASE}/schema/')
        self.assertEqual(schema.status_code, 200)
        self.assertIn(b'/api/v1/avaliacoes/', schema.content)
