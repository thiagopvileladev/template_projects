"""
CRUD do acervo (UC02 — Gerenciar Acervo).

Regras de acesso:
- Consultar álbuns e faixas é público (visitantes também navegam pelo acervo).
- Incluir, alterar e excluir exige login (UC02, pré-condição UC01).
- Avaliações e coleções pertencem a um usuário: só o dono altera ou exclui.
  Coleções privadas só aparecem para o dono.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import AlbumForm, AvaliacaoForm, ColecaoForm, FaixaForm
from .models import Album, Avaliacao, Colecao, Faixa

ITENS_POR_PAGINA = 20


# --- Álbuns -------------------------------------------------------------------

class AlbumListView(ListView):
    model = Album
    paginate_by = ITENS_POR_PAGINA

    def get_queryset(self):
        return Album.objects.annotate(total_faixas=Count('faixas'))


class AlbumDetailView(DetailView):
    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faixas'] = self.object.faixas.annotate(media=Avg('avaliacoes__nota_pessoal'))
        return context


class AlbumCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'acervo/form.html'
    success_message = 'Álbum "%(titulo)s" cadastrado com sucesso.'
    extra_context = {'titulo_pagina': 'Novo álbum', 'cancelar_url': reverse_lazy('acervo:album_lista')}

    def get_success_url(self):
        return reverse('acervo:album_detalhe', args=[self.object.pk])


class AlbumUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'acervo/form.html'
    success_message = 'Álbum "%(titulo)s" atualizado.'
    extra_context = {'titulo_pagina': 'Editar álbum'}

    def get_success_url(self):
        return reverse('acervo:album_detalhe', args=[self.object.pk])


class AlbumDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Album
    template_name = 'acervo/confirmar_exclusao.html'
    success_url = reverse_lazy('acervo:album_lista')
    success_message = 'Álbum excluído, junto com suas faixas.'
    extra_context = {'aviso': 'Todas as faixas e avaliações deste álbum também serão excluídas.'}


# --- Faixas -------------------------------------------------------------------

class FaixaListView(ListView):
    model = Faixa
    paginate_by = ITENS_POR_PAGINA

    def get_queryset(self):
        return Faixa.objects.select_related('album').annotate(
            media=Avg('avaliacoes__nota_pessoal')
        )


class FaixaDetailView(DetailView):
    model = Faixa

    def get_queryset(self):
        return Faixa.objects.select_related('album')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        avaliacoes = self.object.avaliacoes.select_related('usuario')
        context['avaliacoes'] = avaliacoes
        context['media'] = avaliacoes.aggregate(m=Avg('nota_pessoal'))['m']
        if self.request.user.is_authenticated:
            context['minha_avaliacao'] = avaliacoes.filter(usuario=self.request.user).first()
        return context


class FaixaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Faixa
    form_class = FaixaForm
    template_name = 'acervo/form.html'
    success_message = 'Faixa "%(titulo)s" cadastrada com sucesso.'
    extra_context = {'titulo_pagina': 'Nova faixa', 'cancelar_url': reverse_lazy('acervo:faixa_lista')}

    def get_initial(self):
        # Permite chegar já com o álbum escolhido: /faixas/nova/?album=3
        initial = super().get_initial()
        album_id = self.request.GET.get('album')
        if album_id and album_id.isdigit():
            initial['album'] = album_id
        return initial

    def get_success_url(self):
        return reverse('acervo:faixa_detalhe', args=[self.object.pk])


class FaixaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Faixa
    form_class = FaixaForm
    template_name = 'acervo/form.html'
    success_message = 'Faixa "%(titulo)s" atualizada.'
    extra_context = {'titulo_pagina': 'Editar faixa'}

    def get_success_url(self):
        return reverse('acervo:faixa_detalhe', args=[self.object.pk])


class FaixaDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Faixa
    template_name = 'acervo/confirmar_exclusao.html'
    success_url = reverse_lazy('acervo:faixa_lista')
    success_message = 'Faixa excluída.'
    extra_context = {'aviso': 'As avaliações desta faixa também serão excluídas.'}


# --- Avaliações (uma por usuário e faixa) -------------------------------------

@login_required
def avaliar_faixa(request, pk):
    faixa = get_object_or_404(Faixa, pk=pk)
    avaliacao = Avaliacao.objects.filter(faixa=faixa, usuario=request.user).first()

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST, instance=avaliacao)
        if form.is_valid():
            nova = form.save(commit=False)
            nova.faixa = faixa
            nova.usuario = request.user
            nova.save()
            messages.success(request, 'Avaliação salva.')
            return redirect('acervo:faixa_detalhe', pk=faixa.pk)
    else:
        form = AvaliacaoForm(instance=avaliacao)

    titulo = 'Editar avaliação' if avaliacao else 'Avaliar faixa'
    return render(request, 'acervo/form.html', {
        'form': form,
        'titulo_pagina': f'{titulo}: {faixa.titulo}',
        'cancelar_url': reverse('acervo:faixa_detalhe', args=[faixa.pk]),
    })


@login_required
@require_POST
def excluir_avaliacao(request, pk):
    # Filtrar pelo usuário garante que ninguém apaga avaliação de outra pessoa:
    # se não for o dono, a avaliação "não existe" (404).
    avaliacao = get_object_or_404(Avaliacao, pk=pk, usuario=request.user)
    faixa_pk = avaliacao.faixa_id
    avaliacao.delete()
    messages.success(request, 'Avaliação excluída.')
    return redirect('acervo:faixa_detalhe', pk=faixa_pk)


# --- Coleções -----------------------------------------------------------------

class ColecaoListView(ListView):
    model = Colecao
    paginate_by = ITENS_POR_PAGINA

    def get_queryset(self):
        # Públicas de todos + todas do próprio usuário.
        visiveis = Q(is_publica=True)
        if self.request.user.is_authenticated:
            visiveis |= Q(usuario=self.request.user)
        return (Colecao.objects.filter(visiveis)
                .select_related('usuario')
                .annotate(total_faixas=Count('faixas')))


class ColecaoDetailView(DetailView):
    model = Colecao

    def get_queryset(self):
        visiveis = Q(is_publica=True)
        if self.request.user.is_authenticated:
            visiveis |= Q(usuario=self.request.user)
        return Colecao.objects.filter(visiveis)


class DonoColecaoMixin(LoginRequiredMixin):
    """Restringe a edição/exclusão às coleções do próprio usuário (404 se não for)."""

    def get_queryset(self):
        return Colecao.objects.filter(usuario=self.request.user)


class ColecaoFormMixin:
    model = Colecao
    form_class = ColecaoForm
    template_name = 'acervo/form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('acervo:colecao_detalhe', args=[self.object.pk])


class ColecaoCreateView(LoginRequiredMixin, SuccessMessageMixin, ColecaoFormMixin, CreateView):
    success_message = 'Coleção "%(nome)s" criada.'
    extra_context = {'titulo_pagina': 'Nova coleção', 'cancelar_url': reverse_lazy('acervo:colecao_lista')}

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class ColecaoUpdateView(DonoColecaoMixin, SuccessMessageMixin, ColecaoFormMixin, UpdateView):
    success_message = 'Coleção "%(nome)s" atualizada.'
    extra_context = {'titulo_pagina': 'Editar coleção'}


class ColecaoDeleteView(DonoColecaoMixin, SuccessMessageMixin, DeleteView):
    template_name = 'acervo/confirmar_exclusao.html'
    success_url = reverse_lazy('acervo:colecao_lista')
    success_message = 'Coleção excluída. As faixas continuam no acervo.'
