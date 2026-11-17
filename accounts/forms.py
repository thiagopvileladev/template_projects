from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Usuario


class CadastroForm(UserCreationForm):
    """Cadastro de curador. A senha passa pelos validadores do settings."""

    class Meta:
        model = Usuario
        fields = ('email', 'username')
        labels = {'username': 'Nome de usuário'}
        help_texts = {'username': 'Como você vai aparecer no TrackVault.'}

    def clean_email(self):
        # E-mail sempre minúsculo: evita contas duplicadas como A@x.com e a@x.com.
        email = self.cleaned_data['email'].strip().lower()
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe uma conta com este e-mail.')
        return email


class LoginForm(AuthenticationForm):
    """Login por e-mail (UC01)."""

    username = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'autofocus': True, 'autocomplete': 'email'}),
    )

    error_messages = {
        # Mensagem do fluxo alternativo 3a do UC01. Não diz qual dos dois está
        # errado, para não revelar se o e-mail existe.
        'invalid_login': 'E-mail ou senha incorretos.',
        'inactive': 'Esta conta está desativada.',
    }

    def clean_username(self):
        return self.cleaned_data['username'].strip().lower()
