# Modelo de Banco de Dados — TrackVault

## 1. Visão Geral
O modelo de dados do **TrackVault** foi estruturado em um banco de dados relacional (compatível com SQLite para desenvolvimento e PostgreSQL para produção), aplicando regras de normalização e restrições de integridade referencial para garantir a consistência das informações do acervo musical.

---

## 2. Diagrama Entidade-Relacionamento (DER Conceitual / Lógico)

Representação em código Mermaid (renderizável no GitHub) das entidades e cardinalidades:

```mermaid
erDiagram
    USUARIO ||--o{ AVALIACAO : escreve
    ALBUM ||--|{ FAIXA : contem
    FAIXA ||--o{ AVALIACAO : recebe
    FAIXA }|--|{ COLECAO : pertence

    USUARIO {
        int id PK
        string username
        string email
        string password_hash
        boolean is_staff
        datetime date_joined
    }

    ALBUM {
        int id PK
        string titulo
        string artista
        int ano_lancamento
        string capa_url
        string spotify_id UK
    }

    FAIXA {
        int id PK
        int album_id FK
        string titulo
        int duracao_ms
        int bpm
        string genero
        string isrc UK
    }

    AVALIACAO {
        int id PK
        int usuario_id FK
        int faixa_id FK
        float nota_pitchfork
        float nota_pessoal
        text resenha
        datetime criado_em
    }

    COLECAO {
        int id PK
        int usuario_id FK
        string nome
        string descricao
        boolean is_publica
    }