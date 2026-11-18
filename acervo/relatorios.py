"""
Relatório consolidado da coleção (UC05 — Gerar Relatório da Coleção / F05).

Indicadores previstos no UC05 e no protótipo da Tela 3:
média geral das notas, total de álbuns e faixas, faixas por gênero, média de
popularidade, artista mais avaliado e média de BPM por gênero.
"""

from django import forms
from django.db.models import Avg, Count, Q

from .models import Avaliacao, Faixa

LIMITE_TABELA = 500


class RelatorioForm(forms.Form):
    escopo = forms.ChoiceField(
        choices=[('acervo', 'Todo o acervo'), ('minhas', 'Somente faixas que avaliei')],
        required=False, initial='acervo',
    )
    genero = forms.ChoiceField(label='Gênero', required=False,
                               choices=[('', 'Todos')] + list(Faixa.Genero.choices))
    ano_de = forms.IntegerField(label='Lançamento de', required=False, min_value=1900, max_value=2100)
    ano_ate = forms.IntegerField(label='Lançamento até', required=False, min_value=1900, max_value=2100)
    nota_min = forms.FloatField(label='Nota mínima', required=False, min_value=0, max_value=10,
                                widget=forms.NumberInput(attrs={'step': '0.5'}))
    nota_max = forms.FloatField(label='Nota máxima', required=False, min_value=0, max_value=10,
                                widget=forms.NumberInput(attrs={'step': '0.5'}))

    def clean(self):
        dados = super().clean()
        for inicio, fim, rotulo in (('ano_de', 'ano_ate', 'ano'), ('nota_min', 'nota_max', 'nota')):
            a, b = dados.get(inicio), dados.get(fim)
            if a is not None and b is not None and a > b:
                raise forms.ValidationError(f'Intervalo de {rotulo} inválido: o início é maior que o fim.')
        return dados


def gerar_relatorio(filtros, usuario):
    """Calcula os indicadores a partir dos filtros validados (cleaned_data)."""
    so_minhas = filtros.get('escopo') == 'minhas'
    filtro_avaliacao = Q(avaliacoes__usuario=usuario) if so_minhas else Q()

    faixas = Faixa.objects.select_related('album').annotate(
        media=Avg('avaliacoes__nota_pessoal', filter=filtro_avaliacao),
        total_avaliacoes=Count('avaliacoes', filter=filtro_avaliacao),
    )
    if so_minhas:
        faixas = faixas.filter(id__in=Avaliacao.objects.filter(usuario=usuario).values('faixa_id'))
    if genero := filtros.get('genero'):
        faixas = faixas.filter(genero=genero)
    if (ano_de := filtros.get('ano_de')) is not None:
        faixas = faixas.filter(album__ano_lancamento__gte=ano_de)
    if (ano_ate := filtros.get('ano_ate')) is not None:
        faixas = faixas.filter(album__ano_lancamento__lte=ano_ate)
    if (nota_min := filtros.get('nota_min')) is not None:
        faixas = faixas.filter(media__gte=nota_min)
    if (nota_max := filtros.get('nota_max')) is not None:
        faixas = faixas.filter(media__lte=nota_max)

    ids = list(faixas.values_list('id', flat=True))
    base = Faixa.objects.filter(id__in=ids)
    avaliacoes = Avaliacao.objects.filter(faixa_id__in=ids)
    if so_minhas:
        avaliacoes = avaliacoes.filter(usuario=usuario)

    totais = base.aggregate(
        total_faixas=Count('id'),
        total_albuns=Count('album', distinct=True),
        media_bpm=Avg('bpm'),
        media_popularidade=Avg('popularidade'),
    )
    notas = avaliacoes.aggregate(media_geral=Avg('nota_pessoal'),
                                 media_pitchfork=Avg('nota_pitchfork'),
                                 total=Count('id'))

    artista_top = (avaliacoes.values('faixa__album__artista')
                   .annotate(qtd=Count('id'), media=Avg('nota_pessoal'))
                   .order_by('-qtd', '-media').first())

    rotulos = dict(Faixa.Genero.choices)
    por_genero = list(
        base.values('genero')
        .annotate(qtd=Count('id'), media_bpm=Avg('bpm'))
        .order_by('-qtd', 'genero')
    )
    medias_genero = dict(avaliacoes.values_list('faixa__genero').annotate(m=Avg('nota_pessoal')))
    maior = max((g['qtd'] for g in por_genero), default=0)
    for g in por_genero:
        g['rotulo'] = rotulos.get(g['genero'], g['genero'])
        g['media_nota'] = medias_genero.get(g['genero'])
        g['percentual'] = round(100 * g['qtd'] / totais['total_faixas']) if totais['total_faixas'] else 0
        # Largura da barra em passos de 5% (classes CSS tv-w-N, sem style inline).
        g['largura'] = 5 * round(20 * g['qtd'] / maior) if maior else 0

    return {
        **totais,
        'media_geral': notas['media_geral'],
        'media_pitchfork': notas['media_pitchfork'],
        'total_avaliacoes': notas['total'],
        'artista_top': artista_top,
        'genero_top': por_genero[0] if por_genero else None,
        'por_genero': por_genero,
        'top_faixas': list(faixas.filter(media__isnull=False).order_by('-media', 'titulo')[:10]),
        'faixas': list(faixas.order_by('album__artista', 'titulo')[:LIMITE_TABELA]),
        'tabela_cortada': totais['total_faixas'] > LIMITE_TABELA,
    }
