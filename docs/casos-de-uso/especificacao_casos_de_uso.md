# Especificações de Casos de Uso — TrackVault

## 1. Atores do Sistema

| Ator | Tipo | Descrição |
| :--- | :--- | :--- |
| **Visitante** | Primário | Usuário não autenticado que pode realizar buscas públicas e consultar a API REST. |
| **Curador (Usuário)** | Primário | Usuário autenticado responsável por gerenciar coleções, cadastrar faixas e gerar relatórios. |
| **API Web do Spotify** | Secundário | Serviço externo consultado para obter metadados (capas, popularidade, BPM e gênero). |

---

## 2. Catálogo de Casos de Uso

| ID | Nome | Atores Primários | Prioridade |
| :--- | :--- | :--- | :--- |
| **UC01** | Autenticar-se | Curador | Alta |
| **UC02** | Gerenciar Acervo (Álbuns e Faixas) | Curador | Alta |
| **UC03** | Consultar e Importar Metadados Extermos | Curador | Alta |
| **UC04** | Buscar Músicas no Acervo | Visitante, Curador | Alta |
| **UC05** | Gerar Relatório da Coleção | Curador | Média |
| **UC06** | Consultar API REST Própria | Visitante, Curador | Alta |

---

## 3. Especificações Detalhadas dos Casos de Uso

### UC01 — Autenticar-se
* **Descrição breve:** Permitir que o curador acesse as funcionalidades restritas do sistema.
* **Pré-condições:** O curador possui conta previamente cadastrada e ativa.
* **Pós-condições de sucesso:** Sessão autenticada criada e redirecionamento para o dashboard principal.
* **Fluxo Principal:**
  1. O curador informa e-mail e senha na tela de login.
  2. O sistema valida as credenciais no banco de dados.
  3. O sistema cria a sessão e exibe a tela inicial do usuário.
* **Fluxo Alternativo (3a - Credenciais Inválidas):**
  * O sistema exibe mensagem de erro ("E-mail ou senha incorretos") e permanece na tela de login.

---

### UC02 — Gerenciar Acervo (Álbuns e Faixas)
* **Descrição breve:** Permitir a inclusão, consulta, alteração e exclusão (CRUD) de álbuns, faixas, notas de crítica e listas temáticas.
* **Pré-condições:** Curador autenticado no sistema (UC01).
* **Pós-condições de sucesso:** Dados gravados, atualizados ou removidos no banco de dados com mensagem de confirmação.
* **Fluxo Principal:**
  1. O curador seleciona a opção de adicionar ou editar um álbum/faixa.
  2. O curador preenche os campos (título, artista, gênero, nota da crítica/Pitchfork e observações).
  3. O sistema valida os campos obrigatórios no servidor.
  4. O sistema persiste as informações no banco de dados e exibe a lista atualizada.
* **Fluxo Alternativo (2a - Auto-preenchimento via Spotify):**
  * O curador clica em "Buscar no Spotify", disparando a execução do **UC03** antes de salvar.
* **Fluxo de Exceção (E1 - Dados Incompletos):**
  * O sistema destaca os campos inválidos e impede o salvamento até a correção.

---

### UC03 — Consultar e Importar Metadados Externos
* **Descrição breve:** Buscar dados de faixas/álbuns na API do Spotify para preencher automaticamente os campos no cadastro.
* **Pré-condições:** Curador autenticado e conexão com a internet disponível.
* **Pós-condições de sucesso:** Dados retornados do Spotify (capa, popularidade, BPM, gênero) preenchidos nos campos da tela de cadastro.
* **Fluxo Principal:**
  1. O curador digita o nome do álbum ou música e clica em "Importar do Spotify".
  2. O backend Django realiza uma requisição HTTP à API Web do Spotify usando credenciais de cliente.
  3. O Spotify retorna os dados em formato JSON.
  4. O sistema preenche os campos do formulário para validação do curador.
* **Fluxo de Exceção (E1 - Indisponibilidade da API do Spotify):**
  * Caso ocorra *timeout* ou falha de conexão, o sistema exibe aviso ("Serviço do Spotify indisponível no momento") e permite o preenchimento manual dos dados.

---

### UC04 — Buscar Músicas no Acervo
* **Descrição breve:** Pesquisar no acervo local por múltiplos critérios.
* **Pré-condições:** Nenhuma (disponível para Visitantes e Curadores).
* **Pós-condições de sucesso:** O sistema apresenta a lista filtrada de faixas/álbuns correspondentes.
* **Fluxo Principal:**
  1. O usuário informa um ou mais filtros (título, artista, gênero ou nota).
  2. O sistema realiza a consulta no banco de dados.
  3. O sistema exibe os resultados organizados em formato de tabela/cards.
* **Fluxo Alternativo (3a - Nenhum resultado encontrado):**
  * O sistema exibe mensagem informando que nenhum registro corresponde aos filtros informados.

---

### UC05 — Gerar Relatório da Coleção
* **Descrição breve:** Gerar painel com indicadores consolidados do acervo, com opção de exportação/impressão.
* **Pré-condições:** Curador autenticado no sistema (UC01).
* **Pós-condições de sucesso:** Relatório exibido em tela com opção de impressão/download em PDF.
* **Fluxo Principal:**
  1. O curador acessa o menu "Relatórios".
  2. O sistema calcula indicadores consolidados (média de notas, total de álbuns, faixas por gênero e média de popularidade).
  3. O sistema exibe os dados consolidados e gráficos explicativos.
  4. O curador clica em "Exportar / Imprimir PDF".
  5. O sistema gera a versão otimizada para impressão.

---

### UC06 — Consultar API REST Própria
* **Descrição breve:** Expor dados do acervo via endpoints JSON para consumo por terceiros.
* **Pré-condições:** Requisição HTTP enviada para uma rota válida da API.
* **Pós-condições de sucesso:** Resposta HTTP 200 OK acompanhada do payload JSON correspondente.
* **Fluxo Principal:**
  1. O cliente envia uma requisição `GET` para `/api/v1/tracks/`.
  2. O backend Django REST Framework processa os parâmetros de consulta.
  3. O sistema retorna o documento JSON com o acervo filtrado e paginado.

---

## 4. Estrutura do Diagrama UML de Casos de Uso

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