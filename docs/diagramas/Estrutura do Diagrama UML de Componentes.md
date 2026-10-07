## Estrutura do Diagrama UML de Componentes

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