"""
IP real do cliente atrás dos proxies do Render (achado SAST-02, revisado).

Em produção a requisição passa por Cloudflare -> proxies internos do Render ->
gunicorn. O REMOTE_ADDR que chega ao Django é o IP interno de um desses
proxies (10.x.x.x), que muda entre requisições. Usá-lo como identidade do
cliente divide a contagem dos limites da API entre vários "clientes" e anula
a proteção contra força bruta.

O Cloudflare envia o IP do cliente no cabeçalho CF-Connecting-IP e sobrescreve
qualquer valor enviado pelo próprio cliente nesse cabeçalho. Quando
CLIENT_IP_HEADER está configurado, este middleware coloca esse IP em
REMOTE_ADDR, que é o valor usado pelos limites do DRF (com NUM_PROXIES=0).

Localmente CLIENT_IP_HEADER fica vazio e nada muda: o cabeçalho não é
confiável fora do Render, porque qualquer cliente poderia enviá-lo.
"""

import ipaddress
import logging

from django.conf import settings

logger = logging.getLogger(__name__)

CABECALHOS_DIAGNOSTICO = (
    'REMOTE_ADDR', 'HTTP_X_FORWARDED_FOR', 'HTTP_CF_CONNECTING_IP',
    'HTTP_TRUE_CLIENT_IP', 'HTTP_X_REAL_IP',
)


class IPRealDoClienteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, 'DIAGNOSTICO_IP', False) and request.path.startswith('/api/v1/auth/'):
            # Temporário: confirma em produção quais cabeçalhos chegam ao Django.
            logger.warning('DIAGNOSTICO_IP %s', {c: request.META.get(c) for c in CABECALHOS_DIAGNOSTICO})

        cabecalho = settings.CLIENT_IP_HEADER
        if cabecalho:
            valor = request.META.get(cabecalho, '').strip()
            try:
                request.META['REMOTE_ADDR'] = str(ipaddress.ip_address(valor))
            except ValueError:
                pass  # ausente ou inválido: mantém o REMOTE_ADDR original
        return self.get_response(request)
