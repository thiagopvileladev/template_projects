# Identidade Visual e Protótipos de Interface — TrackVault

## 1. Identidade de Marca e Proposta Visual

* **Nome do Projeto:** TrackVault
* **Slogan / Assinatura:** *Curadoria, Acervo e Análises Críticas Musicais em um só Lugar.*
* **Proposta Visual:** Estética moderna *Dark Mode* inspirada em plataformas de streaming e players de áudio, utilizando alto contraste para facilitar o uso prolongado e destacar as capas dos álbuns e relatórios gráficos.

---

## 2. Paleta de Cores e Tipografia

### 2.1. Tabela de Cores (Códigos HEX)

| Aplicação | Nome da Cor | Código HEX | Amostra / Função |
| :--- | :--- | :--- | :--- |
| **Fundo Principal** | Dark Slate | `#121212` | Fundo geral da aplicação em modo escuro. |
| **Superfície / Cards** | Surface Charcoal | `#1E1E1E` | Fundo de painéis, formulários e cartões de música. |
| **Destaque / Ação** | Spotify Green | `#1DB954` | Botões primários, links ativos e badges de sucesso. |
| **Sotaque / Pitchfork**| Pitchfork Red | `#E50914` | Destaques de notas críticas e alertas do sistema. |
| **Texto Principal** | Pure White | `#FFFFFF` | Títulos e textos de alta relevância. |
| **Texto Secundário** | Muted Gray | `#A7A7A7` | Rótulos, metadados e descrições secundárias. |

### 2.2. Tipografia
* **Fonte Primária (Interface):** `Inter` ou `Roboto` (Sans-serif moderna, legível em telas e dispositivos móveis).
* **Fonte Secundária (Destaques/Notas):** `Montserrat` (para títulos de álbuns e indicadores de relatórios).

---

## 3. Estrutura das Telas Essenciais (Wireframes e Layouts)

### Tela 1: Dashboard / Catálogo Principal (`/`)
* **Header / Navbar:** Logo TrackVault à esquerda; barra de pesquisa rápida ao centro; avatar/botão de login do curador à direita.
* **Seção Hero:** Painel estatístico com resumo da coleção (Total de Músicas, Média de Notas, Gênero Predominante).
* **Grid de Álbuns:** Exibição em *Cards* responsivos mostrando a capa do álbum (carregada do Spotify), título da faixa, artista, nota do curador e nota Pitchfork.
* **Rodapé:** Links para documentação da API REST e status da integração com o Spotify.

### Tela 2: Formulário de Cadastro e Importação (`/faixas/nova/`)
* **Campo de Busca Externa:** Input com o campo *"Pesquisar faixa no Spotify pelo nome"*.
* **Botão de Ação:** *"Importar do Spotify"*, que dispara a chamada AJAX/Fetch para auto-preencher os campos abaixo.
* **Formulário Interno (Django Form):**
  * Título da Música (text)
  * Artista / Banda (text)
  * Gênero Musical (select/dropdown)
  * Andamento BPM (number)
  * Nota Pessoal / Curadoria (range de 0.0 a 10.0)
  * Resenha / Análise Crítica (textarea)
* **Ações:** Botões *"Salvar Faixa"* e *"Cancelar"*.

### Tela 3: Painel de Relatórios Consolidados (`/relatorios/`)
* **Filtros do Relatório:** Seleção por período de lançamento, intervalo de notas ou gênero musical.
* **Cards de Indicadores (KPIs):**
  * Média Geral da Coleção
  * Artista Mais Avaliado
  * Média de BPM por Gênero
* **Tabela Consolidada:** Lista detalhada para impressão ou exportação em PDF.