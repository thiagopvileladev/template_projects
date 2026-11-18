"""
TrackVault API v1 (UC06 — Consultar API REST Própria).

Contrato: docs/api/documento_api.md. Documentação interativa em /api/v1/docs/.
"""

from django.db.models import Avg, Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from acervo.busca import BuscaFaixaForm, filtrar_faixas
from acervo.models import Album, Avaliacao, Colecao, Faixa

from .permissoes import DonoOuSomenteLeitura
from .serializers import (
    AlbumDetalheSerializer,
    AlbumSerializer,
    AvaliacaoSerializer,
    ColecaoSerializer,
    FaixaSerializer,
    TokenRespostaSerializer,
    TokenSerializer,
)

FILTROS_FAIXA = [
    OpenApiParameter('q', str, description='Texto no título, artista ou álbum.'),
    OpenApiParameter('artista', str, description='Parte do nome do artista.'),
    OpenApiParameter('genero', str, description='Código do gênero.',
                     enum=[codigo for codigo, _ in Faixa.Genero.choices]),
    OpenApiParameter('nota_min', float, description='Média mínima das avaliações (0 a 10).'),
    OpenApiParameter('bpm_min', int, description='BPM mínimo.'),
    OpenApiParameter('bpm_max', int, description='BPM máximo.'),
    OpenApiParameter('colecao', int, description='ID de uma coleção pública.'),
    OpenApiParameter('ordem', str, description='Ordenação.',
                     enum=['titulo', 'artista', 'nota', 'bpm', 'recentes']),
    OpenApiParameter('page_size', int, description='Itens por página (padrão 20, máximo 100).'),
]


@extend_schema_view(
    list=extend_schema(summary='Listar faixas do acervo', parameters=FILTROS_FAIXA,
                       responses={200: FaixaSerializer(many=True), 400: OpenApiTypes.OBJECT}),
    retrieve=extend_schema(summary='Detalhar uma faixa'),
)
class FaixaViewSet(viewsets.ReadOnlyModelViewSet):
    """Consulta pública do acervo, com os mesmos filtros da busca do site."""

    serializer_class = FaixaSerializer

    def get_queryset(self):
        if self.action != 'list':
            return Faixa.objects.select_related('album').annotate(media=Avg('avaliacoes__nota_pessoal'))
        # Pela API só coleções públicas podem ser usadas como filtro.
        form = BuscaFaixaForm(self.request.query_params)
        if not form.is_valid():
            raise serializers.ValidationError(
                {campo: [str(e) for e in erros] for campo, erros in form.errors.items()}
            )
        return filtrar_faixas(form.cleaned_data)


@extend_schema_view(
    list=extend_schema(summary='Listar álbuns',
                       parameters=[OpenApiParameter('artista', str, description='Parte do nome do artista.')]),
    retrieve=extend_schema(summary='Detalhar um álbum com suas faixas'),
)
class AlbumViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        qs = Album.objects.annotate(total_faixas=Count('faixas'))
        if self.action == 'retrieve':
            return qs.prefetch_related('faixas__album')
        if artista := self.request.query_params.get('artista', '').strip()[:100]:
            qs = qs.filter(artista__icontains=artista)
        return qs

    def get_serializer_class(self):
        return AlbumDetalheSerializer if self.action == 'retrieve' else AlbumSerializer


EXEMPLO_AVALIACAO = OpenApiExample(
    'Nova avaliação',
    value={'faixa_id': 1, 'nota_pessoal': 9.5, 'nota_pitchfork': 8.2,
           'resenha': 'Excelente progressão de acordes no sintetizador principal.'},
    request_only=True,
)


@extend_schema_view(
    list=extend_schema(summary='Listar avaliações', parameters=[
        OpenApiParameter('faixa', int, description='Somente avaliações desta faixa.'),
        OpenApiParameter('minhas', bool, description='true = somente as do usuário autenticado.'),
    ]),
    retrieve=extend_schema(summary='Detalhar uma avaliação'),
    create=extend_schema(summary='Registrar avaliação (requer token)', examples=[EXEMPLO_AVALIACAO],
                         responses={201: AvaliacaoSerializer, 400: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT}),
    update=extend_schema(summary='Substituir a própria avaliação (requer token)'),
    partial_update=extend_schema(summary='Alterar parte da própria avaliação (requer token)'),
    destroy=extend_schema(summary='Excluir a própria avaliação (requer token)'),
)
class AvaliacaoViewSet(viewsets.ModelViewSet):
    serializer_class = AvaliacaoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, DonoOuSomenteLeitura]

    def get_queryset(self):
        qs = Avaliacao.objects.select_related('usuario', 'faixa')
        params = self.request.query_params
        if (faixa := params.get('faixa', '')).isdigit():
            qs = qs.filter(faixa_id=faixa)
        if params.get('minhas') == 'true' and self.request.user.is_authenticated:
            qs = qs.filter(usuario=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


@extend_schema_view(
    list=extend_schema(summary='Listar coleções públicas'),
    retrieve=extend_schema(summary='Detalhar uma coleção pública'),
)
class ColecaoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ColecaoSerializer

    def get_queryset(self):
        return (Colecao.objects.filter(is_publica=True)
                .select_related('usuario').prefetch_related('faixas__album'))


class TokenView(APIView):
    """Troca e-mail e senha por um token de acesso."""

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'token'

    @extend_schema(
        summary='Obter token de acesso',
        request=TokenSerializer,
        responses={200: TokenRespostaSerializer, 400: OpenApiTypes.OBJECT, 429: OpenApiTypes.OBJECT},
        examples=[OpenApiExample('Login', value={'email': 'curador@exemplo.com', 'password': 'sua-senha'},  # nosec B105 - exemplo da documentação
                                 request_only=True)],
        tags=['auth'],
    )
    def post(self, request):
        serializer = TokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        token, _ = Token.objects.get_or_create(user=serializer.validated_data['usuario'])
        return Response({'token': token.key}, status=status.HTTP_200_OK)
