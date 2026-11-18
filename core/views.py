from django.db.models import Avg, Count
from django.shortcuts import render

from acervo.models import Avaliacao, Faixa


def home(request):
    """Dashboard / catálogo principal (protótipo, Tela 1)."""
    genero_top = (Faixa.objects.values('genero').annotate(qtd=Count('id'))
                  .order_by('-qtd').first())
    destaques = (Faixa.objects.select_related('album')
                 .annotate(media=Avg('avaliacoes__nota_pessoal'),
                           pitchfork=Avg('avaliacoes__nota_pitchfork'))
                 .order_by('-id')[:12])
    return render(request, 'core/home.html', {
        'total_faixas': Faixa.objects.count(),
        'media_notas': Avaliacao.objects.aggregate(m=Avg('nota_pessoal'))['m'],
        'genero_top': Faixa.Genero(genero_top['genero']).label if genero_top else None,
        'destaques': destaques,
    })
