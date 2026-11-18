from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from .models import Usuario

SENHA = 'SenhaForte!2026'


class CadastroTests(TestCase):
    def test_cadastro_cria_usuario_e_faz_login(self):
        resposta = self.client.post(reverse('accounts:cadastro'), {
            'email': 'Curador@Exemplo.com',
            'username': 'curador',
            'password1': SENHA,
            'password2': SENHA,
        })
        self.assertRedirects(resposta, reverse('core:home'))
        usuario = Usuario.objects.get()
        self.assertEqual(usuario.email, 'curador@exemplo.com')  # salvo em minúsculas
        self.assertEqual(int(self.client.session['_auth_user_id']), usuario.pk)

    def test_cadastro_rejeita_email_repetido(self):
        Usuario.objects.create_user(username='a', email='a@exemplo.com', password=SENHA)
        resposta = self.client.post(reverse('accounts:cadastro'), {
            'email': 'A@exemplo.com',
            'username': 'outro',
            'password1': SENHA,
            'password2': SENHA,
        })
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Já existe uma conta com este e-mail.')
        self.assertEqual(Usuario.objects.count(), 1)

    def test_cadastro_rejeita_senha_fraca(self):
        resposta = self.client.post(reverse('accounts:cadastro'), {
            'email': 'b@exemplo.com',
            'username': 'b',
            'password1': '123',
            'password2': '123',
        })
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(Usuario.objects.exists())


class LoginTests(TestCase):
    def setUp(self):
        cache.clear()
        Usuario.objects.create_user(username='curador', email='curador@exemplo.com', password=SENHA)

    def test_login_por_email(self):
        resposta = self.client.post(reverse('accounts:login'), {
            'username': 'CURADOR@exemplo.com',
            'password': SENHA,
        })
        self.assertRedirects(resposta, reverse('core:home'))

    def test_login_com_senha_errada_mostra_mensagem_do_uc01(self):
        resposta = self.client.post(reverse('accounts:login'), {
            'username': 'curador@exemplo.com',
            'password': 'errada',
        })
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'E-mail ou senha incorretos.')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_bloqueia_apos_5_tentativas_erradas(self):
        """SAST-01: força bruta no login."""
        url = reverse('accounts:login')
        for _ in range(5):
            self.client.post(url, {'username': 'curador@exemplo.com', 'password': 'errada'})
        # Mesmo com a senha certa, a conta fica bloqueada temporariamente.
        resposta = self.client.post(url, {'username': 'CURADOR@exemplo.com', 'password': SENHA})
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Muitas tentativas de login')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_certo_zera_contagem(self):
        url = reverse('accounts:login')
        for _ in range(4):
            self.client.post(url, {'username': 'curador@exemplo.com', 'password': 'errada'})
        self.client.post(url, {'username': 'curador@exemplo.com', 'password': SENHA})
        self.client.logout()
        for _ in range(4):
            self.client.post(url, {'username': 'curador@exemplo.com', 'password': 'errada'})
        resposta = self.client.post(url, {'username': 'curador@exemplo.com', 'password': SENHA})
        self.assertRedirects(resposta, reverse('core:home'))

    def test_logout_exige_post(self):
        self.client.login(username='curador@exemplo.com', password=SENHA)
        self.assertEqual(self.client.get(reverse('accounts:logout')).status_code, 405)
        resposta = self.client.post(reverse('accounts:logout'))
        self.assertRedirects(resposta, reverse('core:home'))
        self.assertNotIn('_auth_user_id', self.client.session)
