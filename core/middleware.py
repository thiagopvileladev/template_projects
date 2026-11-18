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


# --- Cabeçalhos de segurança (achado DAST-02) -------------------------------------

# Política padrão: só recursos do próprio site. Sem JavaScript ou CSS inline.
# Imagens: capas de álbuns vêm do CDN do Spotify (e podem ser URLs informadas
# pelo curador), por isso qualquer origem HTTPS.
CSP_PADRAO = '; '.join([
    "default-src 'self'",
    "script-src 'self'",
    "style-src 'self'",
    "img-src 'self' data: https:",
    "font-src 'self'",
    "connect-src 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
    "base-uri 'self'",
    "object-src 'none'",
])

# Swagger UI (/api/v1/docs/): o template do drf-spectacular e o próprio
# Swagger UI usam CSS inline. Scripts continuam restritos ao próprio site.
CSP_DOCUMENTACAO = CSP_PADRAO.replace("style-src 'self'", "style-src 'self' 'unsafe-inline'")

PERMISSIONS_POLICY = 'camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()'


class CabecalhosSegurancaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resposta = self.get_response(request)
        if 'Content-Security-Policy' not in resposta:
            documentacao = request.path.startswith('/api/v1/docs/')
            resposta['Content-Security-Policy'] = CSP_DOCUMENTACAO if documentacao else CSP_PADRAO
        resposta.setdefault('Permissions-Policy', PERMISSIONS_POLICY)
        return resposta


def remover_cors_dos_estaticos(headers, path, url):
    """
    WHITENOISE_ADD_HEADERS_FUNCTION (achado DAST-03): o WhiteNoise adiciona
    Access-Control-Allow-Origin: * a todos os arquivos estáticos. O TrackVault
    não serve estáticos para outros sites, então o cabeçalho é removido.
    """
    del headers['Access-Control-Allow-Origin']
