# TrackVault API v1 — Guia de uso

Documentação interativa (OpenAPI), gerada a partir do código:

| Formato | Caminho |
|---|---|
| Swagger UI (testar no navegador) | `/api/v1/docs/` |
| Esquema OpenAPI 3 (YAML) | `/api/v1/schema/` |

- **URL-base:** `https://<domínio-da-aplicação>/api/v1/` (local: `http://127.0.0.1:8000/api/v1/`)
- **Versão:** 1.0.0
- **Formato:** JSON (requisições com `Content-Type: application/json`)

## Autenticação

Leitura (`GET`) é pública. Criar, alterar ou excluir avaliações exige token.

```http
POST /api/v1/auth/token/
Content-Type: application/json

{"email": "curador@exemplo.com", "password": "sua-senha"}
```

```json
{"token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"}
```

Envie o token em todas as requisições de escrita:

```
Authorization: Bearer 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## Endpoints

| Método | Rota | Auth | Descrição |
|---|---|---|---|
| POST | `/auth/token/` | — | Obter token |
| GET | `/faixas/` | — | Listar faixas (filtros abaixo) |
| GET | `/faixas/{id}/` | — | Detalhar faixa |
| GET | `/albuns/` | — | Listar álbuns (`?artista=`) |
| GET | `/albuns/{id}/` | — | Detalhar álbum com faixas |
| GET | `/colecoes/` | — | Listar coleções públicas |
| GET | `/colecoes/{id}/` | — | Detalhar coleção pública |
| GET | `/avaliacoes/` | — | Listar avaliações (`?faixa=`, `?minhas=true`) |
| GET | `/avaliacoes/{id}/` | — | Detalhar avaliação |
| POST | `/avaliacoes/` | Token | Registrar avaliação |
| PUT/PATCH | `/avaliacoes/{id}/` | Token (autor) | Alterar a própria avaliação |
| DELETE | `/avaliacoes/{id}/` | Token (autor) | Excluir a própria avaliação |

### Filtros de `GET /faixas/`

| Parâmetro | Tipo | Exemplo |
|---|---|---|
| `q` | texto (título, artista ou álbum) | `?q=calvin` |
| `artista` | texto | `?artista=daft punk` |
| `genero` | código | `?genero=eletronica` |
| `nota_min` | 0 a 10 | `?nota_min=8` |
| `bpm_min`, `bpm_max` | 0 a 300 | `?bpm_min=120&bpm_max=130` |
| `colecao` | ID de coleção pública | `?colecao=3` |
| `ordem` | `titulo`, `artista`, `nota`, `bpm`, `recentes` | `?ordem=nota` |
| `page`, `page_size` | paginação (padrão 20, máx. 100) | `?page=2&page_size=50` |

Códigos de gênero: `rock`, `pop`, `hip_hop`, `eletronica`, `jazz`, `blues`, `classica`, `mpb`, `samba`, `sertanejo`, `funk`, `rnb`, `reggae`, `metal`, `indie`, `outro`.

## Exemplos

**Listar faixas eletrônicas**

```bash
curl "http://127.0.0.1:8000/api/v1/faixas/?genero=eletronica"
```

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "titulo": "Feel So Close",
      "artista": "Calvin Harris",
      "album": {"id": 1, "titulo": "18 Months", "capa_url": "https://i.scdn.co/image/..."},
      "genero": "Eletrônica",
      "genero_codigo": "eletronica",
      "bpm": 128,
      "duracao_ms": 206413,
      "isrc": "GBARL1100849",
      "popularidade": 74,
      "spotify_id": "1gihuPhrLraKYrJMAEONyc",
      "media_notas": 9.5
    }
  ]
}
```

**Registrar avaliação**

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/avaliacoes/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"faixa_id": 1, "nota_pessoal": 9.5, "resenha": "Excelente progressão de acordes."}'
```

```json
{
  "id": 1,
  "faixa_id": 1,
  "usuario": "curador",
  "nota_pessoal": 9.5,
  "nota_pitchfork": null,
  "resenha": "Excelente progressão de acordes.",
  "criado_em": "2026-11-17T20:15:00-03:00"
}
```

## Códigos de status e erros

| Código | Quando |
|---|---|
| `200 OK` | Consulta ou alteração bem-sucedida |
| `201 Created` | Avaliação registrada |
| `204 No Content` | Avaliação excluída |
| `400 Bad Request` | Dados ou filtros inválidos, JSON malformado, avaliação duplicada |
| `401 Unauthorized` | Token ausente ou inválido em rota de escrita |
| `403 Forbidden` | Tentativa de alterar avaliação de outro usuário |
| `404 Not Found` | Recurso inexistente |
| `405 Method Not Allowed` | Método não suportado (ex.: `POST /faixas/`) |
| `429 Too Many Requests` | Limite de requisições excedido |

Erros de validação indicam o campo:

```json
{"nota_pessoal": ["Certifique-se que este valor seja menor ou igual a 10.0."]}
```

Demais erros usam `detail`:

```json
{"detail": "As credenciais de autenticação não foram fornecidas."}
```

## Limites de uso

| Situação | Limite |
|---|---|
| Sem autenticação | 60 requisições/minuto por IP |
| Com token | 120 requisições/minuto por usuário |
| `POST /auth/token/` | 5 requisições/minuto por IP (proteção contra força bruta) |

Dados pessoais (e-mails) não são expostos pela API; avaliações e coleções mostram apenas o nome de usuário.
