from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    """
    Token do DRF aceito no formato definido no contrato da API:
    Authorization: Bearer <token>
    (o padrão do DRF seria "Token <token>").
    """

    keyword = 'Bearer'


class BearerTokenScheme(OpenApiAuthenticationExtension):
    """Faz o Swagger mostrar o botão "Authorize" com o esquema Bearer."""

    target_class = 'api.autenticacao.BearerTokenAuthentication'
    name = 'BearerToken'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'description': 'Token obtido em POST /api/v1/auth/token/.',
        }
