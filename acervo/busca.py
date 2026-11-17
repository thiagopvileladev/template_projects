"""
Busca no acervo (UC04 — Buscar Músicas no Acervo / F03 — Busca Avançada).

Os filtros ficam em um formulário Django para que os parâmetros recebidos
da URL sejam validados no servidor antes de chegar ao banco. A mesma função
de filtragem é usada pela tela de busca e pela API REST.
"""

from django import forms
from django.db.models import Avg, Q

from .models import Colecao, Faixa

ORDENACOES = {
    'titulo': ('titulo',),
    'artista': ('album__artista', 'titulo'),
    'nota': ('-media', 'titulo'),
    'bpm': ('bpm', 'titulo'),
    'recentes': ('-id',),
}


class BuscaFaixaForm(forms.Form):
    q = forms.CharField(label='Busca', required=False, max_length=100,
                        widget=forms.TextInput(attrs={'placeholder': 'Título, artista ou álbum'}))
    artista = forms.CharField(required=False, max_length=100)
    genero = forms.ChoiceField(label='Gênero', required=False,
                               choices=[('', 'Todos')] + list(Faixa.Genero.choices))
    nota_min = forms.FloatField(label='Nota mínima', required=False, min_value=0, max_value=10,
                                widget=forms.NumberInput(attrs={'step': '0.5'}))
    bpm_min = forms.IntegerField(label='BPM mín.', required=False, min_value=0, max_value=300)
    bpm_max = forms.IntegerField(label='BPM máx.', required=False, min_value=0, max_value=300)
    colecao = forms.ModelChoiceField(label='Coleção', required=False,
                                     queryset=Colecao.objects.none(), empty_label='Todas')
    ordem = forms.ChoiceField(required=False, choices=[
        ('titulo', 'Título'), ('artista', 'Artista'), ('nota', 'Maior nota'),
        ('bpm', 'BPM'), ('recentes', 'Mais recentes'),
    ])

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Só aparecem coleções que o usuário pode ver (públicas + as dele).
        visiveis = Q(is_publica=True)
        if usuario is not None and usuario.is_authenticated:
            visiveis |= Q(usuario=usuario)
        self.fields['colecao'].queryset = Colecao.objects.filter(visiveis)

    def clean(self):
        dados = super().clean()
        bpm_min, bpm_max = dados.get('bpm_min'), dados.get('bpm_max')
        if bpm_min is not None and bpm_max is not None and bpm_min > bpm_max:
            raise forms.ValidationError('O BPM mínimo não pode ser maior que o máximo.')
        return dados

    @property
    def tem_filtro(self):
        return self.is_bound and any(
            v not in (None, '') for k, v in self.cleaned_data.items() if k != 'ordem'
        )


def filtrar_faixas(filtros, queryset=None):
    """Aplica os filtros já validados (cleaned_data) e devolve o queryset."""
    qs = queryset if queryset is not None else Faixa.objects.all()
    qs = qs.select_related('album').annotate(media=Avg('avaliacoes__nota_pessoal'))

    if termo := filtros.get('q'):
        qs = qs.filter(
            Q(titulo__icontains=termo)
            | Q(album__artista__icontains=termo)
            | Q(album__titulo__icontains=termo)
        )
    if artista := filtros.get('artista'):
        qs = qs.filter(album__artista__icontains=artista)
    if genero := filtros.get('genero'):
        qs = qs.filter(genero=genero)
    if (nota_min := filtros.get('nota_min')) is not None:
        qs = qs.filter(media__gte=nota_min)
    if (bpm_min := filtros.get('bpm_min')) is not None:
        qs = qs.filter(bpm__gte=bpm_min)
    if (bpm_max := filtros.get('bpm_max')) is not None:
        qs = qs.filter(bpm__lte=bpm_max)
    if colecao := filtros.get('colecao'):
        qs = qs.filter(colecoes=colecao)

    return qs.order_by(*ORDENACOES.get(filtros.get('ordem') or 'titulo'))
