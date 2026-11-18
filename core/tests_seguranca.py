"""
Testes de regressão dos achados do DAST (docs/seguranca/relatorio_seguranca.md).
Garantem que as correções continuem valendo em mudanças futuras.
"""

import re
from wsgiref.headers import Headers

from django.test import TestCase
from django.urls import reverse

from accounts.models import Usuario
from acervo.models import Album, Avaliacao, Faixa
from core.middleware import remover_cors_dos_estaticos

SENHA = 'SenhaForte!2026'

# <script> sem src, atributo style= e manipuladores on*= (onclick, onload...)
INLINE = re.compile(r'<script(?![^>]*\bsrc=)[^>]*>|\sstyle=|\son[a-z]+=', re.I)


class CabecalhosTests(TestCase):
    def test_csp_restritiva_nas_paginas(self):
        """DAST-02: CSP sem 'unsafe-inline' e só com recursos do próprio site."""
        csp = self.client.get(reverse('core:home'))['Content-Security-Policy']
        self.assertIn("script-src 'self'", csp)
        self.assertIn("frame-ancestors 'none'", csp)
        self.assertIn("object-src 'none'", csp)
        self.assertNotIn('unsafe-inline', csp)
        self.assertNotIn('googleapis', csp)

    def test_csp_da_documentacao_libera_so_estilos(self):
        csp = self.client.get('/api/v1/docs/')['Content-Security-Policy']
        self.assertIn("style-src 'self' 'unsafe-inline'", csp)
        self.assertIn("script-src 'self';", csp)  # scripts continuam restritos

    def test_csp_tambem_na_api_e_no_404(self):
        self.assertIn('Content-Security-Policy', self.client.get('/api/v1/faixas/'))
        self.assertIn('Content-Security-Policy', self.client.get('/nao-existe/'))

    def test_permissions_policy(self):
        self.assertIn('camera=()', self.client.get('/')['Permissions-Policy'])

    def test_cookie_csrf_httponly(self):
        """DAST-05."""
        resposta = self.client.get(reverse('accounts:login'))
        self.assertTrue(resposta.cookies['csrftoken']['httponly'])

    def test_estaticos_sem_cors_aberto(self):
        """DAST-03: remove o Access-Control-Allow-Origin: * do WhiteNoise."""
        headers = Headers([('Access-Control-Allow-Origin', '*'), ('Cache-Control', 'max-age=60')])
        remover_cors_dos_estaticos(headers, 'x.css', '/static/x.css')
        self.assertNotIn('Access-Control-Allow-Origin', headers)
        self.assertEqual(headers['Cache-Control'], 'max-age=60')


class SemConteudoInlineTests(TestCase):
    """DAST-02: com CSP restritiva, JS/CSS inline seria bloqueado no navegador."""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(username='c', email='c@ex.com', password=SENHA)
        album = Album.objects.create(titulo='A', artista='B', capa_url='https://i.scdn.co/image/x')
        self.faixa = Faixa.objects.create(album=album, titulo='F', genero='rock', bpm=100)
        Avaliacao.objects.create(usuario=self.usuario, faixa=self.faixa, nota_pessoal=8)

    def assert_sem_inline(self, url):
        html = self.client.get(url).content.decode()
        self.assertEqual(INLINE.findall(html), [], url)

    def test_paginas_publicas(self):
        for url in ('/', '/faixas/', '/faixas/?q=x', '/albuns/', '/colecoes/', '/contas/entrar/',
                    '/contas/cadastro/', self.faixa.get_absolute_url(), '/nao-existe/'):
            self.assert_sem_inline(url)

    def test_paginas_logadas(self):
        self.client.force_login(self.usuario)
        for url in (self.faixa.get_absolute_url(), '/relatorios/', '/faixas/nova/', '/faixas/importar/',
                    '/colecoes/nova/', reverse('acervo:faixa_avaliar', args=[self.faixa.pk])):
            self.assert_sem_inline(url)

    def test_sem_recursos_externos(self):
        """DAST-04 e DAST-06: sem Google Fonts e sem Swagger UI de CDN."""
        for url in ('/', '/api/v1/docs/'):
            html = self.client.get(url).content.decode()
            self.assertNotIn('fonts.googleapis.com', html)
            self.assertNotIn('cdn.jsdelivr.net', html)
            for src in re.findall(r'<script[^>]*\bsrc="([^"]+)"', html):
                self.assertTrue(src.startswith('/'), src)


class InjecaoSqlTests(TestCase):
    """DAST-01 (falso positivo): payloads de SQL injection são tratados como texto."""

    def test_payloads_na_busca(self):
        Album.objects.create(titulo='Abbey Road', artista='The Beatles')
        for payload in ("case randomblob(1000000000) when not null then 1 else 1 end ",
                        "ZAP' || pg_sleep(5) || '", "' OR '1'='1", "1; DROP TABLE acervo_faixa; --"):
            resposta = self.client.get('/faixas/', {'artista': payload, 'q': payload})
            self.assertEqual(resposta.status_code, 200, payload)
            self.assertContains(resposta, 'Nenhuma faixa corresponde aos filtros informados.')
        self.assertTrue(Album.objects.exists())  # nada foi apagado

    def test_paginacao_da_api_nao_avalia_expressoes(self):
        """
        Falso positivo da varredura final (ZAP 40018 em page/page_size): os
        parâmetros são convertidos para inteiro pelo DRF; expressões e aspas
        nunca são calculadas nem chegam ao SQL.
        """
        album = Album.objects.create(titulo='A', artista='B')
        for i in range(8):
            Faixa.objects.create(album=album, titulo=f'F{i}', genero='rock')
        # Se "7-2" fosse calculado viriam 5 itens; o DRF ignora e usa o padrão (20).
        self.assertEqual(len(self.client.get('/api/v1/faixas/', {'page_size': '7-2'}).json()['results']), 8)
        self.assertEqual(len(self.client.get('/api/v1/faixas/', {'page_size': '5'}).json()['results']), 5)
        # Qualquer página inexistente recebe a mesma resposta 404.
        for pagina in ('10', '12-2', "10' AND '1'='1' -- "):
            resposta = self.client.get('/api/v1/faixas/', {'page': pagina})
            self.assertEqual(resposta.status_code, 404, pagina)
