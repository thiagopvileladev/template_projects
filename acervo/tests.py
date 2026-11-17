from django.test import TestCase
from django.urls import reverse

from accounts.models import Usuario

from .models import Album, Avaliacao, Colecao, Faixa

SENHA = 'SenhaForte!2026'


class BaseAcervoTest(TestCase):
    def setUp(self):
        self.curador = Usuario.objects.create_user(username='curador', email='c@ex.com', password=SENHA)
        self.outro = Usuario.objects.create_user(username='outro', email='o@ex.com', password=SENHA)
        self.album = Album.objects.create(titulo='18 Months', artista='Calvin Harris', ano_lancamento=2012)
        self.faixa = Faixa.objects.create(album=self.album, titulo='Feel So Close', genero='eletronica', bpm=128)

    def entrar(self, usuario=None):
        self.client.force_login(usuario or self.curador)


class AlbumCrudTests(BaseAcervoTest):
    def test_lista_e_detalhe_sao_publicos(self):
        self.assertContains(self.client.get(reverse('acervo:album_lista')), '18 Months')
        self.assertContains(self.client.get(self.album.get_absolute_url()), 'Feel So Close')

    def test_criar_exige_login(self):
        resposta = self.client.get(reverse('acervo:album_novo'))
        self.assertRedirects(resposta, f"{reverse('accounts:login')}?next={reverse('acervo:album_novo')}")

    def test_criar_editar_excluir(self):
        self.entrar()
        resposta = self.client.post(reverse('acervo:album_novo'), {
            'titulo': 'Motion', 'artista': 'Calvin Harris', 'ano_lancamento': 2014,
        })
        novo = Album.objects.get(titulo='Motion')
        self.assertRedirects(resposta, novo.get_absolute_url())

        self.client.post(reverse('acervo:album_editar', args=[novo.pk]), {
            'titulo': 'Motion (Deluxe)', 'artista': 'Calvin Harris', 'ano_lancamento': 2014,
        })
        novo.refresh_from_db()
        self.assertEqual(novo.titulo, 'Motion (Deluxe)')

        self.client.post(reverse('acervo:album_excluir', args=[novo.pk]))
        self.assertFalse(Album.objects.filter(pk=novo.pk).exists())

    def test_validacao_ano_futuro(self):
        self.entrar()
        resposta = self.client.post(reverse('acervo:album_novo'), {
            'titulo': 'X', 'artista': 'Y', 'ano_lancamento': 2999,
        })
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'não pode estar no futuro')

    def test_excluir_album_exclui_faixas(self):
        self.entrar()
        self.client.post(reverse('acervo:album_excluir', args=[self.album.pk]))
        self.assertFalse(Faixa.objects.exists())


class FaixaCrudTests(BaseAcervoTest):
    def dados(self, **extra):
        return {'album': self.album.pk, 'titulo': 'Sweet Nothing', 'genero': 'eletronica', **extra}

    def test_criar_faixa_normaliza_isrc(self):
        self.entrar()
        self.client.post(reverse('acervo:faixa_nova'), self.dados(isrc='gbarl1200619'))
        self.assertEqual(Faixa.objects.get(titulo='Sweet Nothing').isrc, 'GBARL1200619')

    def test_isrc_vazio_em_varias_faixas(self):
        # ISRC é único, mas vazio vira NULL e não conflita.
        self.entrar()
        self.client.post(reverse('acervo:faixa_nova'), self.dados(titulo='A'))
        self.client.post(reverse('acervo:faixa_nova'), self.dados(titulo='B'))
        self.assertEqual(Faixa.objects.filter(isrc__isnull=True).count(), 3)

    def test_validacoes(self):
        self.entrar()
        resposta = self.client.post(reverse('acervo:faixa_nova'), self.dados(bpm=999, isrc='abc'))
        self.assertEqual(resposta.status_code, 200)
        form = resposta.context['form']
        self.assertIn('bpm', form.errors)
        self.assertIn('isrc', form.errors)

    def test_titulo_obrigatorio(self):
        self.entrar()
        resposta = self.client.post(reverse('acervo:faixa_nova'), self.dados(titulo=''))
        self.assertIn('titulo', resposta.context['form'].errors)

    def test_editar_e_excluir(self):
        self.entrar()
        self.client.post(reverse('acervo:faixa_editar', args=[self.faixa.pk]), self.dados(titulo='Novo título'))
        self.faixa.refresh_from_db()
        self.assertEqual(self.faixa.titulo, 'Novo título')
        self.client.post(reverse('acervo:faixa_excluir', args=[self.faixa.pk]))
        self.assertFalse(Faixa.objects.exists())

    def test_excluir_exige_login(self):
        self.client.post(reverse('acervo:faixa_excluir', args=[self.faixa.pk]))
        self.assertTrue(Faixa.objects.exists())


class AvaliacaoTests(BaseAcervoTest):
    def avaliar(self, **dados):
        return self.client.post(reverse('acervo:faixa_avaliar', args=[self.faixa.pk]), dados)

    def test_avaliar_e_reavaliar_mantem_uma_avaliacao(self):
        self.entrar()
        self.avaliar(nota_pessoal=9.5, resenha='Ótima')
        self.avaliar(nota_pessoal=8.0, resenha='Mudei de ideia')
        avaliacao = Avaliacao.objects.get()
        self.assertEqual(avaliacao.nota_pessoal, 8.0)
        self.assertEqual(avaliacao.usuario, self.curador)

    def test_detalhe_mostra_avaliacoes_e_media(self):
        Avaliacao.objects.create(usuario=self.curador, faixa=self.faixa, nota_pessoal=9, nota_pitchfork=8.2, resenha='Linda')
        Avaliacao.objects.create(usuario=self.outro, faixa=self.faixa, nota_pessoal=7)
        self.entrar()
        resposta = self.client.get(self.faixa.get_absolute_url())
        self.assertContains(resposta, 'Linda')
        self.assertContains(resposta, 'P 8,2')
        self.assertEqual(resposta.context['media'], 8.0)
        self.assertContains(resposta, 'Editar minha avaliação')

    def test_nota_fora_do_intervalo(self):
        self.entrar()
        resposta = self.avaliar(nota_pessoal=11)
        self.assertIn('nota_pessoal', resposta.context['form'].errors)
        self.assertFalse(Avaliacao.objects.exists())

    def test_nao_exclui_avaliacao_de_outro_usuario(self):
        avaliacao = Avaliacao.objects.create(usuario=self.outro, faixa=self.faixa, nota_pessoal=7)
        self.entrar()
        resposta = self.client.post(reverse('acervo:avaliacao_excluir', args=[avaliacao.pk]))
        self.assertEqual(resposta.status_code, 404)
        self.assertTrue(Avaliacao.objects.exists())

    def test_excluir_avaliacao_exige_post(self):
        avaliacao = Avaliacao.objects.create(usuario=self.curador, faixa=self.faixa, nota_pessoal=7)
        self.entrar()
        resposta = self.client.get(reverse('acervo:avaliacao_excluir', args=[avaliacao.pk]))
        self.assertEqual(resposta.status_code, 405)


class ColecaoTests(BaseAcervoTest):
    def test_criar_colecao_com_faixas(self):
        self.entrar()
        self.client.post(reverse('acervo:colecao_nova'), {
            'nome': 'Halloween', 'descricao': 'Sombrias', 'is_publica': 'on', 'faixas': [self.faixa.pk],
        })
        colecao = Colecao.objects.get()
        self.assertEqual(colecao.usuario, self.curador)
        self.assertEqual(list(colecao.faixas.all()), [self.faixa])

    def test_nome_repetido_para_o_mesmo_usuario(self):
        Colecao.objects.create(usuario=self.curador, nome='Halloween')
        self.entrar()
        resposta = self.client.post(reverse('acervo:colecao_nova'), {'nome': 'halloween'})
        self.assertContains(resposta, 'Você já tem uma coleção com este nome.')

    def test_colecao_privada_invisivel_para_outros(self):
        privada = Colecao.objects.create(usuario=self.outro, nome='Segredo', is_publica=False)
        self.entrar()
        self.assertEqual(self.client.get(privada.get_absolute_url()).status_code, 404)
        self.assertNotContains(self.client.get(reverse('acervo:colecao_lista')), 'Segredo')

    def test_nao_edita_colecao_de_outro_usuario(self):
        publica = Colecao.objects.create(usuario=self.outro, nome='Pública', is_publica=True)
        self.entrar()
        resposta = self.client.post(reverse('acervo:colecao_editar', args=[publica.pk]), {'nome': 'Hackeada'})
        self.assertEqual(resposta.status_code, 404)
        publica.refresh_from_db()
        self.assertEqual(publica.nome, 'Pública')
