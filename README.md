# TrackVault

> *Curadoria, Acervo e Análises Críticas Musicais em um só Lugar.*

[![Status](https://img.shields.io/badge/status-fase__1__concluida-green)]()
[![Versão](https://img.shields.io/badge/versão-0.1.0-blue)]()
[![Licença](https://img.shields.io/badge/licença-acadêmica-lightgrey)]()

**Instituição:** CEUB  
**Curso:** Análise e Desenvolvimento de Sistemas  
**Disciplina:** Desenvolvimento Web  
**Turma / Semestre:** Turma A | 4° semestre  
**Professor(a):** Felippe Pires Ferreira  
**Status do projeto:** Entrega da Fase 1 — Documentação e Arquitetura

---

## 1. Visão Geral do Projeto

O **TrackVault** é uma aplicação web desenvolvida em Python/Django para curadores, DJs, críticos e entusiastas da música catalogarem e organizarem acervos musicais. O sistema permite consolidar notas de veículos especializados (como a Pitchfork), avaliações autorais e coleções temáticas em uma interface centralizada e moderna em *Dark Mode*.

Para enriquecer a experiência do usuário sem digitação exaustiva, a plataforma integra-se à **Spotify Web API** para consultar e auto-preencher metadados técnicos de faixas e álbuns, como capas em alta resolução, duração, artista, data de lançamento, códigos ISRC e entre outros.

---

## 2. Guia de Navegação pela Documentação (Fase 1)

Toda a documentação técnica, modelagens e diagramas da Fase 1 foram organizados na pasta [`docs/`](./docs/), divididos nas seguintes subpastas:

| Artefato / Entrega | Localização | Descrição |
| :--- | :--- | :--- |
| **Documento de Visão** | [`docs/visao/documento_de_visao.md`](./docs/visao/documento_de_visao.md) | Problema, objetivos, escopo, stakeholders, restrições e riscos. |
| **Casos de Uso** | [`docs/casos-de-uso/especificacao_casos_de_uso.md`](./docs/casos-de-uso/especificacao_casos_de_uso.md) | Diagrama UML (PlantUML) e especificações textuais dos fluxos. |
| **Arquitetura de Software** | [`docs/arquitetura/documento_arquitetura.md`](./docs/arquitetura/documento_arquitetura.md) | Padrão MTV, camadas, componentes e diagrama de fluxo. |
| **Modelo de Dados** | [`docs/banco-de-dados/modelo_de_dados.md`](./docs/banco-de-dados/modelo_de_dados.md) | Diagrama Entidade-Relacionamento (Mermaid) e tabelas. |
| **Contrato de API & Integrações** | [`docs/api/documento_api.md`](./docs/api/documento_api.md) | Endpoints JSON da API REST própria e plano de integração do Spotify. |
| **Identidade Visual & Protótipos** | [`docs/prototipos/identidade_e_prototipos.md`](./docs/prototipos/identidade_e_prototipos.md) | Paleta de cores (*Dark Slate/Spotify Green*), tipografia e wireframes. |
| **Planejamento & Backlog** | [`docs/planejamento/backlog_e_planejamento.md`](./docs/planejamento/backlog_e_planejamento.md) | Tarefas da Fase 2, cronograma de marcos e matriz de riscos. |
| **Imagens dos Diagramas** | [`docs/diagramas/`](./docs/diagramas/) | Arquivos exportados dos diagramas para visualização rápida. |

---

## 3. Estrutura do Repositório

```text
trackvault/
├── README.md                   # Apresentação e guia de navegação principal
├── docs/                       # Artefatos da Fase 1
│   ├── api/                    # Contrato da API REST e plano do Spotify
│   ├── arquitetura/            # Documento de Arquitetura do Sistema
│   ├── banco-de-dados/         # MER/DER e Modelo Lógico
│   ├── casos-de-uso/           # Especificação dos Casos de Uso
│   ├── diagramas/              # Imagens exportadas dos diagramas
│   ├── planejamento/           # Backlog e Cronograma
│   ├── prototipos/             # Identidade visual e wireframes
│   └── visao/                  # Documento de Visão do Projeto
```
## 4. Participantes

| Nome | Matrícula |
|---|---|
| Thiago Paranaiba Vilela | 22501672 |
| Marcio Tavares | 22611487 |
