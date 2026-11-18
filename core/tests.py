from django.test import TestCase
from django.urls import reverse

from accounts.models import Usuario
from acervo.models import Album, Avaliacao, Faixa


class HomeTests(TestCase):
    def test_home_vazia(self):
        resposta = self.client.get(reverse('core:home'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'O acervo ainda está vazio.')
        self.assertContains(resposta, 'img/logo.svg')

    def test_home_com_indicadores_e_cards(self):
        usuario = Usuario.objects.create_user(username='c', email='c@ex.com', password='SenhaForte!2026')
        album = Album.objects.create(titulo='18 Months', artista='Calvin Harris', capa_url='https://i.scdn.co/image/x')
        faixa = Faixa.objects.create(album=album, titulo='Feel So Close', genero='eletronica')
        Avaliacao.objects.create(usuario=usuario, faixa=faixa, nota_pessoal=9, nota_pitchfork=7.5)

        resposta = self.client.get(reverse('core:home'))
        self.assertEqual(resposta.context['total_faixas'], 1)
        self.assertEqual(resposta.context['genero_top'], 'Eletrônica')
        self.assertContains(resposta, 'Feel So Close')
        self.assertContains(resposta, 'https://i.scdn.co/image/x')
        self.assertContains(resposta, 'P 7,5')

    def test_menu_muda_com_login(self):
        self.assertContains(self.client.get('/'), 'Criar conta')
        usuario = Usuario.objects.create_user(username='curador', email='c@ex.com', password='SenhaForte!2026')
        self.client.force_login(usuario)
        resposta = self.client.get('/')
        self.assertContains(resposta, 'Relatórios')
        self.assertContains(resposta, 'Sair')
