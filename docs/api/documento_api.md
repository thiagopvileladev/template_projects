# Contrato de API e Plano de Integração — TrackVault

## 1. Nossa API REST (TrackVault API)

A API própria foi projetada para permitir que sistemas de terceiros consultem o acervo musical catalogado e as avaliações registradas.

* **URL Base:** `/api/v1/`
* **Formato de Dados:** JSON
* **Autenticação:** Baseada em Token (para rotas de escrita). Rotas de leitura do acervo público são abertas.

### 1.1. Endpoint: Listar Acervo

* **Rota:** `GET /api/v1/faixas/`
* **Descrição:** Retorna a lista de músicas catalogadas, suportando paginação.
* **Parâmetros de Query (Opcionais):**

  * `genero` (string)
  * `artista` (string)

#### Respostas HTTP

* `200 OK`: Sucesso.

#### Exemplo de Resposta (200 OK)

```json
{
  "count": 1,
  "next": null,
  "results": [
    {
      "id": 1,
      "titulo": "Feel So Close",
      "artista": "Calvin Harris",
      "genero": "Electronic",
      "bpm": 128
    }
  ]
}
```

### 1.2. Endpoint: Registrar Avaliação

* **Rota:** `POST /api/v1/avaliacoes/`
* **Descrição:** Permite que um curador envie uma nova resenha/nota para uma faixa específica.
* **Autenticação:** Obrigatória (Header `Authorization: Bearer <token>`).

#### Respostas HTTP

* `201 Created`: Avaliação registrada com sucesso.
* `400 Bad Request`: Erro de validação nos dados enviados.
* `401 Unauthorized`: Token ausente ou inválido.

#### Exemplo de Requisição

```json
{
  "faixa_id": 1,
  "nota_pessoal": 9.5,
  "resenha": "Excelente progressão de acordes no sintetizador principal."
}
```

## 2. Plano de Integração Externa (Spotify Web API)

Para cumprir o requisito de integração com um serviço externo em um fluxo funcional, o **TrackVault** consumirá a API pública do Spotify durante a etapa de cadastro de faixas.

### 2.1. Detalhes do Consumo

* **API Escolhida:** Spotify Web API
* **Documentação Oficial:** https://developer.spotify.com/documentation/web-api
* **Finalidade no Sistema:** Quando o curador for adicionar uma música, o sistema fará uma busca no Spotify pelo título para auto-preencher metadados como a capa do álbum, andamento (BPM) e o código ISRC. O gênero será preenchido manualmente pelo curador no formulário local.
* **Endpoint Consumido:** `GET https://api.spotify.com/v1/search`
* **Dados Utilizados:**

  * `tracks.items[0].album.images[0].url`
  * `tracks.items[0].external_ids.isrc`

### 2.2. Autenticação e Segurança

A autenticação será feita via fluxo **Client Credentials (OAuth 2.0)**.

As chaves `SPOTIFY_CLIENT_ID` e `SPOTIFY_CLIENT_SECRET` serão mantidas exclusivamente no arquivo `.env` do ambiente de produção e injetadas no Django via variáveis de ambiente, nunca sendo versionadas no repositório GitHub.

### 2.3. Tratamento de Falhas e Indisponibilidade

O consumo será feito no backend utilizando a biblioteca `requests` do Python. Para garantir resiliência, implementaremos:

1. **Timeout Configurado:** A requisição `requests.get()` terá um parâmetro de `timeout=5` segundos para evitar que o servidor Django trave aguardando resposta.

2. **Tratamento de Exceções:** Em caso de `requests.exceptions.Timeout` ou `requests.exceptions.ConnectionError` (indisponibilidade da API do Spotify), o sistema fará a captura do erro e retornará uma mensagem amigável na interface web:

   > "A busca automática no Spotify está temporariamente indisponível. Você pode preencher os dados da faixa manualmente."

3. **Fallback:** O sistema permite o cadastro manual (digitação completa do formulário) caso a API externa falhe, garantindo que o curador não fique impedido de trabalhar.
