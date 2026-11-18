from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
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
    # Documentação (PDF 7.3): esquema OpenAPI, Swagger UI e Redoc.
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='docs'),
    path('redoc/', SpectacularRedocView.as_view(url_name='api:schema'), name='redoc'),
    path('', include(router.urls)),
]
