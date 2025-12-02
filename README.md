## Sistema de Gestão Escolar – Flask + PostgreSQL

Aplicação web simples para gerenciar **alunos**, **professores** e **turmas**, além de gerar um **relatório de alunos por turma**.

Foi desenvolvida com **Flask** (Python) no back-end, **PostgreSQL** como banco de dados e **HTML + JavaScript (fetch)** no front-end.

---

## Desafio Escolhido
**Desafio 1 – Sistema de Gestão Escolar Comunitária**

---

## Nome dos Alunos
- Júlia Oliveira Veríssimo  
- Kelly Priscilla de Siqueira Melo  
- Luis Lucena Wanderley De Siqueira  
- Lucas Henrique Gomes Medeiros  
- Mariana Xavier Bezerra  
- Micaella Maria Barbosa Cabral
- Victor Jose Paes e Silva

---

**Líder:** Lucas Henrique Gomes Medeiros

## Tecnologias utilizadas

- **Python 3**
- **Flask**
- **psycopg2** (driver PostgreSQL para Python)
- **PostgreSQL**
- HTML, CSS e JavaScript puro (sem frameworks frontend)

---

## Estrutura do projeto

- `app.py`  
  Arquivo principal. Cria a aplicação Flask, registra os *blueprints* (módulos de rotas) e define a rota inicial `/` que renderiza o menu (`templates/base.html`).

- `config.py`  
  Centraliza a configuração de conexão com o banco PostgreSQL (`DB_CONFIG`) e expõe as funções:
  - `get_connection()` – abre uma nova conexão com o banco;
  - `dict_cursor(conn)` – cria um cursor que retorna linhas como dicionários.

- `routes/`  
  Módulos de rotas da aplicação:
  - `alunos.py` – rotas e API para alunos;
  - `professores.py` – rotas e API para professores;
  - `turmas.py` – rotas e API para turmas;
  - `relatorios.py` – relatório de alunos por turma.

- `templates/`  
  Templates HTML que rendem as páginas:
  - `base.html` – menu inicial;
  - `alunos.html` – tela de alunos (usa JS para consumir `/alunos/api`);
  - `professores.html` – tela de professores (consome `/professores/api`);
  - `turmas.html` – tela de turmas (consome `/turmas/api`);
  - `relatorio_alunos_por_turma.html` – relatório de alunos por turma.

- `DOCUMENTACAO.md`  
  Documento explicando com mais detalhes o código, incluindo trechos exemplificados de cada parte importante.

---

## Pré-requisitos

- Python 3 instalado
- PostgreSQL instalado e acessível
- Um banco de dados configurado com as tabelas esperadas (`alunos`, `professores`, `turmas`)
- Biblioteca `psycopg2` instalada

Instalação das dependências Python (exemplo usando `pip`):

```bash
pip install flask psycopg2 psycopg2-binary
```

> Obs.: `psycopg2-binary` é prático para desenvolvimento local; em produção, prefira `psycopg2`.

---

## Configuração do banco de dados

No arquivo `config.py` existe um dicionário `DB_CONFIG` com os parâmetros de conexão:

- `host`
- `database`
- `user`
- `password`
- `port`

Ajuste esses valores para o seu ambiente PostgreSQL.

Exemplo de script SQL mínimo (apenas ilustração – adapte conforme sua necessidade):

```sql
CREATE TABLE professores (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    disciplina TEXT NOT NULL
);

CREATE TABLE turmas (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    sala TEXT,
    professor_id INTEGER REFERENCES professores(id)
);

CREATE TABLE alunos (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    idade INTEGER,
    turma_id INTEGER REFERENCES turmas(id)
);
```

---

## Como executar o projeto

1. **Clonar ou copiar o projeto** para uma pasta local.
2. Garantir que as dependências Python estão instaladas.
3. Ajustar os dados de `DB_CONFIG` em `config.py` para o seu banco PostgreSQL.
4. No diretório do projeto, executar:

```bash
python app.py
```

5. A aplicação, em modo de desenvolvimento, normalmente ficará acessível em:

```text
http://127.0.0.1:5000/
```

Abra esse endereço no navegador.

---

## Telas principais

### Menu inicial (`/`)

- `base.html` mostra links para:
  - `/professores/`
  - `/turmas/`
  - `/alunos/`
  - `/relatorios/alunos-por-turma`

### Professores (`/professores/`)

- Página com formulário para **cadastrar professores** (nome + disciplina).
- Tabela listando todos os professores.
- Botões para **editar** e **excluir**.
- A página consome as rotas:
  - `GET /professores/api`
  - `POST /professores/api`
  - `PUT /professores/api/<id>`
  - `DELETE /professores/api/<id>`

### Turmas (`/turmas/`)

- Formulário para cadastrar **turmas**, com:
  - nome da turma;
  - sala;
  - ID do professor (opcional).
- Tabela com listagem das turmas.
- Ações de editar/excluir, usando as rotas:
  - `GET /turmas/api`
  - `POST /turmas/api`
  - `PUT /turmas/api/<id>`
  - `DELETE /turmas/api/<id>`

### Alunos (`/alunos/`)

- Formulário para cadastrar **alunos**, com:
  - nome;
  - idade;
  - ID da turma.
- Tabela com a listagem dos alunos.
- Ações de editar/excluir, consumindo:
  - `GET /alunos/api`
  - `POST /alunos/api`
  - `PUT /alunos/api/<id>`
  - `DELETE /alunos/api/<id>`

### Relatório de alunos por turma (`/relatorios/alunos-por-turma`)

- Mostra cada turma e, abaixo, uma tabela com os alunos daquela turma (id, nome, idade).
- Se uma turma não tiver alunos, mostra a mensagem **"Nenhum aluno nesta turma."**.

---

## Fluxo geral da aplicação

1. O usuário acessa a URL inicial (`/`) e escolhe um módulo (alunos, professores, turmas ou relatório).
2. Nas páginas de **alunos**, **professores** e **turmas**:
   - o JavaScript carrega a lista inicial chamando as rotas API (`GET .../api`);
   - o formulário, ao ser enviado, faz um `fetch` para `POST .../api`;
   - botões de editar/deletar fazem `PUT` e `DELETE` via `fetch`.
3. O back-end Flask recebe essas requisições, faz consultas/alterações no PostgreSQL via `psycopg2` e responde em JSON.
4. No relatório, o back-end monta uma estrutura de dados agrupada (turmas + alunos) e passa para o template Jinja2, que renderiza o HTML final.

---

## Onde aprender mais sobre o código

Para uma explicação detalhada de cada função, rota e template, consulte o arquivo:

- `DOCUMENTACAO.md`

Ele apresenta os trechos mais importantes do código e explica passo a passo o que cada parte faz.


