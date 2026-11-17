from django.urls import path

from . import views

app_name = 'acervo'

urlpatterns = [
    # Álbuns
    path('albuns/', views.AlbumListView.as_view(), name='album_lista'),
    path('albuns/novo/', views.AlbumCreateView.as_view(), name='album_novo'),
    path('albuns/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detalhe'),
    path('albuns/<int:pk>/editar/', views.AlbumUpdateView.as_view(), name='album_editar'),
    path('albuns/<int:pk>/excluir/', views.AlbumDeleteView.as_view(), name='album_excluir'),
    # Faixas
    path('faixas/', views.FaixaListView.as_view(), name='faixa_lista'),
    path('faixas/nova/', views.FaixaCreateView.as_view(), name='faixa_nova'),
    path('faixas/<int:pk>/', views.FaixaDetailView.as_view(), name='faixa_detalhe'),
    path('faixas/<int:pk>/editar/', views.FaixaUpdateView.as_view(), name='faixa_editar'),
    path('faixas/<int:pk>/excluir/', views.FaixaDeleteView.as_view(), name='faixa_excluir'),
    # Avaliações
    path('faixas/<int:pk>/avaliar/', views.avaliar_faixa, name='faixa_avaliar'),
    path('avaliacoes/<int:pk>/excluir/', views.excluir_avaliacao, name='avaliacao_excluir'),
    # Coleções
    path('colecoes/', views.ColecaoListView.as_view(), name='colecao_lista'),
    path('colecoes/nova/', views.ColecaoCreateView.as_view(), name='colecao_nova'),
    path('colecoes/<int:pk>/', views.ColecaoDetailView.as_view(), name='colecao_detalhe'),
    path('colecoes/<int:pk>/editar/', views.ColecaoUpdateView.as_view(), name='colecao_editar'),
    path('colecoes/<int:pk>/excluir/', views.ColecaoDeleteView.as_view(), name='colecao_excluir'),
]
