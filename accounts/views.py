from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import CadastroForm, LoginForm


class EntrarView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Conta criada com sucesso. Bem-vindo ao TrackVault!')
            return redirect('core:home')
    else:
        form = CadastroForm()

    return render(request, 'accounts/cadastro.html', {'form': form})
