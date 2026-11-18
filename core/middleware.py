"""
IP real do cliente atrás dos proxies do Render (achado SAST-02, revisado).

Em produção a requisição passa por Cloudflare -> proxies internos do Render ->
gunicorn. O REMOTE_ADDR que chega ao Django é o IP interno de um desses
proxies (10.x.x.x), que muda entre requisições. Usá-lo como identidade do
cliente divide a contagem dos limites da API entre vários "clientes" e anula
a proteção contra força bruta.

O Cloudflare envia o IP do cliente no cabeçalho CF-Connecting-IP. Uma
requisição que tenta enviar esse cabeçalho por conta própria é recusada pelo
Cloudflare (HTTP 403), então ele não pode ser forjado. Quando CLIENT_IP_HEADER
está configurado, este middleware coloca esse IP em REMOTE_ADDR, que é o valor
usado pelos limites do DRF (com NUM_PROXIES=0).

Localmente CLIENT_IP_HEADER fica vazio e nada muda: o cabeçalho não é
confiável fora do Render, porque qualquer cliente poderia enviá-lo.
"""

import ipaddress

from django.conf import settings


class IPRealDoClienteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cabecalho = settings.CLIENT_IP_HEADER
        if cabecalho:
            valor = request.META.get(cabecalho, '').strip()
            try:
                request.META['REMOTE_ADDR'] = str(ipaddress.ip_address(valor))
            except ValueError:
                pass  # ausente ou inválido: mantém o REMOTE_ADDR original
        return self.get_response(request)
