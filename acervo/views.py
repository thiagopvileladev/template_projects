"""
CRUD do acervo (UC02 — Gerenciar Acervo).

Regras de acesso:
- Consultar álbuns e faixas é público (visitantes também navegam pelo acervo).
- Incluir, alterar e excluir exige login (UC02, pré-condição UC01).
- Avaliações e coleções pertencem a um usuário: só o dono altera ou exclui.
  Coleções privadas só aparecem para o dono.
"""

import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .busca import BuscaFaixaForm, filtrar_faixas
from .forms import AlbumForm, AvaliacaoForm, ColecaoForm, FaixaForm
from .models import Album, Avaliacao, Colecao, Faixa
from .relatorios import RelatorioForm, gerar_relatorio
from .services import spotify_service

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
    """Lista de faixas com busca por múltiplos critérios (UC04)."""

    model = Faixa
    paginate_by = ITENS_POR_PAGINA

    def get_queryset(self):
        self.form = BuscaFaixaForm(self.request.GET or None, usuario=self.request.user)
        if self.form.is_bound and not self.form.is_valid():
            # Filtro inválido (ex.: nota 50): mostra o erro e nenhum resultado.
            return Faixa.objects.none()
        filtros = self.form.cleaned_data if self.form.is_bound else {}
        return filtrar_faixas(filtros)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        # Mantém os filtros ao trocar de página.
        params = self.request.GET.copy()
        params.pop('page', None)
        context['query_string'] = params.urlencode()
        return context


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
        initial = super().get_initial()
        # Permite chegar já com o álbum escolhido: /faixas/nova/?album=3
        album_id = self.request.GET.get('album')
        if album_id and album_id.isdigit():
            initial['album'] = album_id
        # Dados vindos da importação do Spotify (UC03, passo 4).
        if self.request.method == 'GET':
            self.importado = self.request.session.pop(SESSAO_IMPORTACAO, None)
            if self.importado:
                initial.update(self.importado)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['importado_spotify'] = getattr(self, 'importado', None)
        context['spotify_url'] = reverse('acervo:importar_spotify')
        return context

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


# --- Importação do Spotify (UC03) ---------------------------------------------

SESSAO_IMPORTACAO = 'importacao_spotify'


@login_required
def importar_spotify(request):
    """
    GET  ?q=termo  -> pesquisa no Spotify e lista os resultados.
    POST spotify_id -> importa a faixa escolhida: cria/reaproveita o álbum e
                       abre o formulário de nova faixa já preenchido.
    Em qualquer falha do Spotify, mostra a mensagem e oferece o cadastro manual.
    """
    if request.method == 'POST':
        try:
            dados = spotify_service.obter_faixa(request.POST.get('spotify_id', ''))
        except spotify_service.SpotifyIndisponivel as erro:
            messages.warning(request, str(erro))
            return redirect('acervo:importar_spotify')

        existente = Faixa.objects.filter(spotify_id=dados.spotify_id).first()
        if existente:
            messages.info(request, 'Esta faixa já está no acervo.')
            return redirect(existente)

        album = _album_da_importacao(dados)
        request.session[SESSAO_IMPORTACAO] = {
            'album': album.pk,
            'titulo': dados.titulo,
            'duracao_ms': dados.duracao_ms,
            # ISRC é único: não sugere um que já pertence a outra faixa.
            'isrc': dados.isrc if dados.isrc and not Faixa.objects.filter(isrc=dados.isrc).exists() else '',
            'popularidade': dados.popularidade,
            'spotify_id': dados.spotify_id,
        }
        return redirect('acervo:faixa_nova')

    termo = request.GET.get('q', '').strip()[:100]
    resultados, erro = [], None
    if termo:
        try:
            resultados = spotify_service.buscar_faixas(termo)
        except spotify_service.SpotifyIndisponivel as e:
            erro = str(e)

    return render(request, 'acervo/importar_spotify.html', {
        'termo': termo,
        'resultados': resultados,
        'erro': erro,
        'configurado': spotify_service.configurado(),
    })


def _album_da_importacao(dados):
    """Reaproveita o álbum (pelo ID do Spotify ou título+artista) ou cria um novo."""
    if dados.album_spotify_id:
        album = Album.objects.filter(spotify_id=dados.album_spotify_id).first()
        if album:
            return album
    album = Album.objects.filter(
        titulo__iexact=dados.album_titulo, artista__iexact=dados.artista
    ).first()
    if album:
        # Completa dados que faltavam no álbum cadastrado manualmente.
        if not album.capa_url and dados.capa_url:
            album.capa_url = dados.capa_url
        if not album.spotify_id and dados.album_spotify_id:
            album.spotify_id = dados.album_spotify_id
        album.save()
        return album
    return Album.objects.create(
        titulo=dados.album_titulo[:200],
        artista=dados.artista[:200],
        ano_lancamento=dados.album_ano,
        capa_url=dados.capa_url,
        spotify_id=dados.album_spotify_id,
    )


# --- Relatórios (UC05) ----------------------------------------------------------

def _relatorio_do_request(request):
    form = RelatorioForm(request.GET or None)
    if form.is_bound and not form.is_valid():
        return form, None
    filtros = form.cleaned_data if form.is_bound else {}
    return form, gerar_relatorio(filtros, request.user)


@login_required
def relatorio(request):
    form, dados = _relatorio_do_request(request)
    return render(request, 'acervo/relatorio.html', {
        'form': form,
        'r': dados,
        'gerado_em': timezone.localtime(),
        'query_string': request.GET.urlencode(),
    })


@login_required
def relatorio_csv(request):
    """Exporta a tabela consolidada em CSV (abre no Excel/Planilhas)."""
    form, dados = _relatorio_do_request(request)
    if dados is None:
        messages.error(request, 'Corrija os filtros antes de exportar.')
        return redirect('acervo:relatorio')

    resposta = HttpResponse(content_type='text/csv; charset=utf-8')
    resposta['Content-Disposition'] = 'attachment; filename="trackvault-relatorio.csv"'
    resposta.write('﻿')  # BOM: o Excel reconhece os acentos
    escritor = csv.writer(resposta, delimiter=';')
    escritor.writerow(['Título', 'Artista', 'Álbum', 'Ano', 'Gênero', 'BPM',
                       'Popularidade', 'Média das notas', 'Avaliações'])
    for f in dados['faixas']:
        # Toda linha passa por _linha_csv_segura, que neutraliza fórmulas (achado SAST-03).
        escritor.writerow(_linha_csv_segura([  # nosemgrep: python.django.security.injection.csv-writer-injection.csv-writer-injection
            f.titulo, f.album.artista, f.album.titulo,
            f.album.ano_lancamento or '', f.get_genero_display(), f.bpm or '',
            f.popularidade if f.popularidade is not None else '',
            f'{f.media:.1f}'.replace('.', ',') if f.media is not None else '',
            f.total_avaliacoes,
        ]))
    return resposta


INICIO_FORMULA = ('=', '+', '-', '@', '\t', '\r', '|', '%')


def _linha_csv_segura(celulas):
    """
    Evita "CSV injection" (OWASP): no Excel/Planilhas, uma célula que começa
    com = + - @ (mesmo após espaços) é executada como fórmula. Essas células
    recebem um apóstrofo na frente e passam a ser texto.
    """
    seguras = []
    for celula in celulas:
        texto = str(celula)
        if texto[:1] in INICIO_FORMULA or texto.lstrip()[:1] in INICIO_FORMULA:
            texto = f"'{texto}"
        seguras.append(texto)
    return seguras


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
