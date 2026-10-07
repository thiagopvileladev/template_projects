## Estrutura do Diagrama UML de Casos de Uso

Abaixo está a representação em texto (sintaxe PlantUML) do Diagrama de Casos de Uso. Este código pode ser copiado e colado em ferramentas como [PlantText](https://www.planttext.com/) ou [draw.io](https://app.diagrams.net/) para exportação da imagem (PNG/SVG):

```plantuml
@startuml
left to right direction
actor "Visitante" as v
actor "Curador (Usuário)" as c
actor "API Web do Spotify" as s <<Secundário>>

rectangle "Sistema TrackVault" {
  usecase "UC01: Autenticar-se" as UC01
  usecase "UC02: Gerenciar Acervo (CRUD)" as UC02
  usecase "UC03: Consultar Metadados no Spotify" as UC03
  usecase "UC04: Buscar Músicas" as UC04
  usecase "UC05: Gerar Relatório da Coleção" as UC05
  usecase "UC06: Consultar API REST Própria" as UC06
}

v --> UC04
v --> UC06

c --> UC01
c --> UC02
c --> UC03
c --> UC04
c --> UC05
c --> UC06

UC03 ..> s : <<consumo>>
UC02 ..> UC03 : <<extend>>
@enduml