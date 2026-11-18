"""
Proteção contra força bruta no login (achado SAST-01, docs/seguranca).

Conta as tentativas falhas por e-mail no cache. Depois de MAX_TENTATIVAS
erros, novas tentativas para aquele e-mail são recusadas por BLOQUEIO_SEGUNDOS,
mesmo com a senha correta. O e-mail é guardado como hash no cache.

A contagem é por e-mail (e não por IP) porque o endereço do cliente chega por
proxy no Render e pode ser forjado; o bloqueio por conta impede testar senhas
em uma mesma conta, que é o ataque relevante aqui.
"""

import hashlib

from django.core.cache import cache

MAX_TENTATIVAS = 5
BLOQUEIO_SEGUNDOS = 15 * 60


def _chave(email):
    digest = hashlib.sha256((email or '').strip().lower().encode()).hexdigest()
    return f'login-falhas:{digest}'


def bloqueado(email):
    return cache.get(_chave(email), 0) >= MAX_TENTATIVAS


def registrar_falha(email):
    chave = _chave(email)
    # add() só cria se não existir; o prazo conta a partir da primeira falha.
    if not cache.add(chave, 1, BLOQUEIO_SEGUNDOS):
        try:
            cache.incr(chave)
        except ValueError:  # expirou entre o add e o incr
            cache.add(chave, 1, BLOQUEIO_SEGUNDOS)


def limpar(email):
    cache.delete(_chave(email))
