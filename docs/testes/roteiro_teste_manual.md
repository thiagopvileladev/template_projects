# Roteiro de Teste Manual — TrackVault

Complementa os testes automatizados ([`relatorio_testes.md`](relatorio_testes.md)) com o que só pode ser verificado usando a aplicação: navegação, aparência, responsividade, impressão e a integração real com o Spotify.

## Preparação

1. Ambiente: local (`python manage.py runserver`) ou produção (URL pública).
2. Popular dados de demonstração: `python manage.py popular_demo`.
3. Contas de teste: `curador.demo@trackvault.app` e `critica.demo@trackvault.app` (senha definida em `DEMO_PASSWORD`).
4. Navegadores: um desktop (Chrome ou Firefox) e um celular, ou o modo dispositivo do DevTools (largura 375 px).

## Registro da execução

| Campo | Valor |
|---|---|
| Data | |
| Executado por | |
| Ambiente / URL | |
| Commit testado | |
| Navegador(es) | |

**Resultado:** marque ✅ (passou), ❌ (falhou, descreva em Observações) ou ⚠️ (passou com ressalva).

## Casos de teste

### UC01 — Autenticar-se

| ID | Passos | Resultado esperado | Resultado | Observações |
|---|---|---|---|---|
| CT01 | Clicar em **Criar conta**, preencher e-mail, nome e senha forte, enviar | Conta criada, usuário logado, mensagem "Conta criada com sucesso" | | |
| CT02 | Repetir o CT01 com o mesmo e-mail em letras maiúsculas | Erro "Já existe uma conta com este e-mail." | | |
| CT03 | Criar conta com senha `123` | Erros de senha curta, comum e só numérica | | |
| CT04 | Sair e entrar com e-mail e senha corretos | Login e redirecionamento para a página inicial | | |
| CT05 | Entrar com senha errada | Mensagem "E-mail ou senha incorretos." | | |
| CT06 | Deslogado, acessar `/faixas/nova/` digitando a URL | Redireciona para o login; após entrar, volta para `/faixas/nova/` | | |

### UC02 — Gerenciar acervo

| ID | Passos | Resultado esperado | Resultado | Observações |
|---|---|---|---|---|
| CT07 | **Álbuns → + Novo álbum** com título, artista e ano 2010 | Álbum criado, página de detalhe com mensagem de sucesso | | |
| CT08 | Criar álbum com ano 2999 | Erro "O ano de lançamento não pode estar no futuro." no campo | | |
| CT09 | No álbum, **+ Adicionar faixa**; preencher gênero e BPM 120 | Faixa criada já vinculada ao álbum | | |
| CT10 | Criar faixa com BPM 999 e ISRC `abc` | Erros nos dois campos; nada é salvo | | |
| CT11 | Editar a faixa e alterar o título | Título atualizado e mensagem de sucesso | | |
| CT12 | Na faixa, **Avaliar** com nota 9,5 e resenha | Avaliação aparece com a nota em verde | | |
| CT13 | Avaliar de novo a mesma faixa | O formulário abre com a avaliação existente; salvar atualiza em vez de duplicar | | |
| CT14 | Criar coleção privada com 2 faixas | Coleção criada; marcada como "privada" | | |
| CT15 | Logar com a outra conta de teste e abrir a URL da coleção privada | Página "não encontrada" (404) | | |
| CT16 | Excluir um álbum com faixas | Página de confirmação avisa da exclusão das faixas; após confirmar, álbum e faixas somem | | |

### UC03 — Importar do Spotify (requer credenciais configuradas)

| ID | Passos | Resultado esperado | Resultado | Observações |
|---|---|---|---|---|
| CT17 | **Nova faixa → Importar do Spotify**, pesquisar "Feel So Close" | Até 5 resultados com capa, artista, álbum e duração | | |
| CT18 | Clicar em **Importar** em um resultado | Formulário de nova faixa abre preenchido (título, álbum, duração, ISRC) com aviso para completar gênero e BPM | | |
| CT19 | Escolher gênero, informar BPM e salvar | Faixa salva; capa do álbum aparece no detalhe e na página inicial | | |
| CT20 | Importar de novo a mesma faixa | Mensagem "Esta faixa já está no acervo." e redirecionamento para ela | | |
| CT21 | Remover `SPOTIFY_CLIENT_ID` do `.env`, reiniciar e pesquisar | Mensagem de integração não configurada e link "Cadastrar manualmente" | | |
| CT22 | Desconectar a internet e pesquisar | Mensagem "temporariamente indisponível"; a página não trava (no máximo ~5 s) | | |

### UC04 — Buscar músicas

| ID | Passos | Resultado esperado | Resultado | Observações |
|---|---|---|---|---|
| CT23 | Deslogado, digitar "daft" na busca do topo | Faixas do Daft Punk listadas | | |
| CT24 | Em **Faixas**, filtrar gênero Eletrônica e nota mínima 9 | Apenas faixas eletrônicas com média ≥ 9 | | |
| CT25 | Filtrar BPM mínimo 200 e máximo 100 | Erro "O BPM mínimo não pode ser maior que o máximo." | | |
| CT26 | Buscar "xyz123" | Mensagem "Nenhuma faixa corresponde aos filtros informados." | | |
| CT27 | Ordenar por "Maior nota" | Faixas em ordem decrescente de média | | |

### UC05 — Relatório

| ID | Passos | Resultado esperado | Resultado | Observações |
|---|---|---|---|---|
| CT28 | Logado, abrir **Relatórios** | Indicadores, gráfico por gênero, ranking e tabela | | |
| CT29 | Conferir um indicador à mão (ex.: total de faixas) | Valor igual ao contado na lista de faixas | | |
| CT30 | Escopo "Somente faixas que avaliei" | Apenas faixas avaliadas pela conta logada | | |
| CT31 | **Imprimir / Salvar PDF** e salvar como PDF | PDF em fundo branco, sem menus, com data e autor | | |
| CT32 | **Exportar CSV** e abrir no Excel/Planilhas | Colunas separadas e acentos corretos | | |

### UC06 — API REST

| ID | Passos | Resultado esperado | Resultado | Observações |
|---|---|---|---|---|
| CT33 | Abrir `/api/v1/docs/` | Swagger lista todos os endpoints | | |
| CT34 | No Swagger, `POST /auth/token/` com a conta de teste; **Authorize** com o token; `POST /avaliacoes/` | 200 no token e 201 na avaliação | | |
| CT35 | Executar a coleção Postman inteira no Collection Runner | Todas as asserções aprovadas | | |

### Interface, identidade visual e responsividade

| ID | Passos | Resultado esperado | Resultado | Observações |
|---|---|---|---|---|
| CT36 | Percorrer todas as telas no desktop | Paleta escura, verde nos botões, logotipo e fontes Montserrat/Inter em todas | | |
| CT37 | Repetir em 375 px de largura | Menu vira hambúrguer; nada sai da tela na horizontal; tabelas rolam dentro do cartão | | |
| CT38 | Navegar só com o teclado (Tab) | Foco visível; "Pular para o conteúdo" aparece no primeiro Tab | | |

## Resumo da execução

| Total | ✅ | ⚠️ | ❌ |
|---|---|---|---|
| 38 | | | |

**Problemas encontrados e correções:**

-
