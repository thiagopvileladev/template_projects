"""Testes do relatório consolidado (UC05)."""

from django.test import TestCase
from django.urls import reverse

from accounts.models import Usuario

from .models import Album, Avaliacao, Faixa

SENHA = 'SenhaForte!2026'


class RelatorioTests(TestCase):
    def setUp(self):
        self.eu = Usuario.objects.create_user(username='eu', email='eu@ex.com', password=SENHA)
        self.outro = Usuario.objects.create_user(username='outro', email='o@ex.com', password=SENHA)

        calvin = Album.objects.create(titulo='18 Months', artista='Calvin Harris', ano_lancamento=2012)
        daft = Album.objects.create(titulo='RAM', artista='Daft Punk', ano_lancamento=2013)
        beatles = Album.objects.create(titulo='Abbey Road', artista='The Beatles', ano_lancamento=1969)

        self.feel = Faixa.objects.create(album=calvin, titulo='Feel So Close', genero='eletronica', bpm=128, popularidade=80)
        self.sweet = Faixa.objects.create(album=calvin, titulo='Sweet Nothing', genero='eletronica', bpm=128, popularidade=70)
        self.lucky = Faixa.objects.create(album=daft, titulo='Get Lucky', genero='eletronica', bpm=116)
        self.come = Faixa.objects.create(album=beatles, titulo='Come Together', genero='rock', bpm=82)

        Avaliacao.objects.create(usuario=self.eu, faixa=self.feel, nota_pessoal=9, nota_pitchfork=7)
        Avaliacao.objects.create(usuario=self.eu, faixa=self.sweet, nota_pessoal=7)
        Avaliacao.objects.create(usuario=self.outro, faixa=self.feel, nota_pessoal=5)
        Avaliacao.objects.create(usuario=self.outro, faixa=self.come, nota_pessoal=10)

        self.client.force_login(self.eu)

    def gerar(self, **filtros):
        resposta = self.client.get(reverse('acervo:relatorio'), filtros)
        self.assertEqual(resposta.status_code, 200)
        return resposta, resposta.context['r']

    def test_exige_login(self):
        self.client.logout()
        self.assertEqual(self.client.get(reverse('acervo:relatorio')).status_code, 302)
        self.assertEqual(self.client.get(reverse('acervo:relatorio_csv')).status_code, 302)

    def test_indicadores_do_acervo(self):
        _, r = self.gerar()
        self.assertEqual(r['total_faixas'], 4)
        self.assertEqual(r['total_albuns'], 3)
        self.assertEqual(r['total_avaliacoes'], 4)
        self.assertAlmostEqual(r['media_geral'], (9 + 7 + 5 + 10) / 4)
        self.assertAlmostEqual(r['media_bpm'], (128 + 128 + 116 + 82) / 4)
        self.assertAlmostEqual(r['media_popularidade'], 75)
        self.assertEqual(r['artista_top']['faixa__album__artista'], 'Calvin Harris')
        self.assertEqual(r['genero_top']['genero'], 'eletronica')
        self.assertEqual(r['genero_top']['percentual'], 75)

    def test_por_genero(self):
        _, r = self.gerar()
        rock = next(g for g in r['por_genero'] if g['genero'] == 'rock')
        self.assertEqual(rock['qtd'], 1)
        self.assertEqual(rock['media_nota'], 10)
        self.assertEqual(rock['largura'], 33)  # 1 de 3 (maior grupo)

    def test_escopo_minhas_avaliacoes(self):
        _, r = self.gerar(escopo='minhas')
        self.assertEqual(r['total_faixas'], 2)
        self.assertEqual(r['total_avaliacoes'], 2)
        self.assertAlmostEqual(r['media_geral'], 8)
        # A média de cada faixa considera só as minhas notas.
        feel = next(f for f in r['faixas'] if f.pk == self.feel.pk)
        self.assertEqual(feel.media, 9)

    def test_filtro_genero_e_periodo(self):
        _, r = self.gerar(genero='eletronica', ano_de=2013)
        self.assertEqual([f.titulo for f in r['faixas']], ['Get Lucky'])

    def test_filtro_intervalo_de_notas(self):
        _, r = self.gerar(nota_min=8, nota_max=10)
        self.assertEqual({f.titulo for f in r['faixas']}, {'Come Together'})

    def test_intervalo_invalido(self):
        resposta, r = self.gerar(ano_de=2020, ano_ate=2000)
        self.assertIsNone(r)
        self.assertContains(resposta, 'Intervalo de ano inválido')

    def test_sem_resultados(self):
        resposta, r = self.gerar(genero='jazz')
        self.assertEqual(r['total_faixas'], 0)
        self.assertContains(resposta, 'Nenhuma faixa corresponde aos filtros informados.')

    def test_ranking(self):
        _, r = self.gerar()
        self.assertEqual(r['top_faixas'][0], self.come)

    def test_pagina_tem_impressao_e_exportacao(self):
        resposta, _ = self.gerar()
        self.assertContains(resposta, 'Imprimir / Salvar PDF')
        self.assertContains(resposta, reverse('acervo:relatorio_csv'))

    def test_exportar_csv_respeita_filtros(self):
        resposta = self.client.get(reverse('acervo:relatorio_csv'), {'genero': 'rock'})
        self.assertEqual(resposta.status_code, 200)
        self.assertIn('attachment', resposta['Content-Disposition'])
        linhas = resposta.content.decode('utf-8-sig').strip().splitlines()
        self.assertEqual(len(linhas), 2)  # cabeçalho + 1 faixa
        self.assertIn('Come Together;The Beatles;Abbey Road;1969;Rock;82', linhas[1])

    def test_csv_neutraliza_formulas(self):
        album = Album.objects.create(titulo='=HYPERLINK("http://mal.com")', artista='X')
        Faixa.objects.create(album=album, titulo='@SUM(1+1)', genero='pop')
        conteudo = self.client.get(reverse('acervo:relatorio_csv'), {'genero': 'pop'}).content.decode('utf-8-sig')
        self.assertIn("'@SUM(1+1)", conteudo)
        self.assertIn("'=HYPERLINK", conteudo)

    def test_csv_neutraliza_formula_apos_espacos(self):
        album = Album.objects.create(titulo='Normal', artista='  =1+1')
        Faixa.objects.create(album=album, titulo='Faixa', genero='funk')
        conteudo = self.client.get(reverse('acervo:relatorio_csv'), {'genero': 'funk'}).content.decode('utf-8-sig')
        self.assertIn("'  =1+1", conteudo)
