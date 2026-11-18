from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerSplitView
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register('faixas', views.FaixaViewSet, basename='faixa')
router.register('albuns', views.AlbumViewSet, basename='album')
router.register('avaliacoes', views.AvaliacaoViewSet, basename='avaliacao')
router.register('colecoes', views.ColecaoViewSet, basename='colecao')

urlpatterns = [
    path('auth/token/', views.TokenView.as_view(), name='token'),
    # Documentação (PDF 7.3): esquema OpenAPI e Swagger UI.
    # SplitView: o script de inicialização é um arquivo separado (sem JS inline,
    # compatível com a Content-Security-Policy). O Redoc foi removido: carregava
    # Google Fonts e script inline, e o Swagger já cobre a documentação (DAST-06).
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerSplitView.as_view(url_name='api:schema'), name='docs'),
    path('', include(router.urls)),
]
