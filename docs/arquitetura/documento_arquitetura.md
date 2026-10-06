# Documento de Arquitetura de Software — TrackVault

## 1. Visão Geral da Arquitetura
O **TrackVault** adota uma arquitetura em camadas estruturada no padrão **MTV (Model-Template-View)** nativo do framework **Django**, combinada com o padrão **Repository/Service** para isolar a regra de negócio da integração externa com a API Web do Spotify.

---

## 2. Tecnologias Empregadas
* **Linguagem Backend:** Python
* **Framework Web:** Django
* **Framework de APIs:** Django REST Framework
* **Banco de Dados Relacional:**PostgreSQL (Produção)
* **Integração Externa:** Requests / Spotipy (com autenticação OAuth 2.0 Client Credentials)
* **Frontend Web:** HTML5, CSS3, JavaScript, React

---

## 3. Descrição das Camadas de Software

1. **Camada de Apresentação (Templates e DRF Serializers):**
   * **Interface Web:** Processa os dados retornados pelas views e renderiza páginas HTML responsivas para o usuário final.
   * **Interface API REST:** Utiliza *Serializers* do Django REST Framework para converter objetos `Model` em JSON e validar cargas úteis recebidas via requisições HTTP.

2. **Camada de Aplicação e Controle (Views / Controllers):**
   * Recebe e valida as requisições HTTP, gerencia sessões de autenticação, invoca os serviços de negócio e define a resposta HTTP apropriada (status 200, 201, 400, 404, 500).

3. **Camada de Serviços e Integração (Services Layer):**
   * Módulo desacoplado (`spotify_service.py`) encarregado de efetuar chamadas HTTP para a API Web do Spotify, gerenciar o token de acesso da aplicação, aplicar tratamento de *timeout* e capturar exceções de conexão.

4. **Camada de Domínio e Persistência (Models / ORM):**
   * Mapeia as entidades de negócio (Álbum, Faixa, Avaliação, Lista) para tabelas relacionais via Django ORM, aplicando validações de integridade no servidor.

---

## 4. Fluxo de Dados: Importação do Spotify

```text
[Usuário / Frontend] 
       │ 
       │ 1. Solicita importação de música ("Feel So Close")
       ▼
[Django View / Control] 
       │ 
       │ 2. Delega busca ao SpotifyService
       ▼
[SpotifyService] ───(HTTP GET + OAuth Token)───► [API Web Spotify]
       │                                               │
       │ 3. Retorna JSON com metadados                 │
       ◄───────────────────────────────────────────────┘
       │ 
       │ 4. Converte JSON para dicionário Python
       ▼
[Django View] ───(Preenche Form/Model)───► [Django ORM] ───► [Banco de Dados Relacional]
```


## 5. Estrutura do Diagrama UML de Componentes

```text
@startuml
package "Navegador Web / Cliente API" {
  [Interface do Usuário / Client HTTP]
}

package "Aplicação Django (TrackVault)" {
  [Router / URLconf] --> [Views / Controllers]
  [Views / Controllers] --> [Serializers / Templates]
  [Views / Controllers] --> [SpotifyService]
  [Views / Controllers] --> [Django ORM Models]
  [SpotifyService] ..> [OAuth Token Cache]
}

database "Banco de Dados Relacional" {
  [PostgreSQL / SQLite]
}

cloud "Serviços Externos" {
  [Spotify Web API]
}

[Interface do Usuário / Client HTTP] --> [Router / URLconf] : Requisições HTTP/JSON
[Django ORM Models] --> [PostgreSQL / SQLite] : SQL Queries
[SpotifyService] --> [Spotify Web API] : REST / HTTPS GET
@startuml
```