## Visão geral do projeto

Este projeto é um **mini sistema de gestão escolar** feito com **Flask** e **PostgreSQL**.
Ele permite cadastrar e listar **professores**, **turmas** e **alunos**, além de gerar um
**relatório de alunos por turma**.

Estrutura principal:

- `app.py`: ponto de entrada da aplicação Flask e registro dos blueprints.
- `config.py`: configuração e funções de conexão com o banco de dados PostgreSQL.
- `routes/`: módulos de rotas (alunos, professores, turmas, relatórios).
- `templates/`: páginas HTML que consomem as APIs (via JavaScript) e exibem os dados.

---

## `app.py` – aplicação Flask e registro de blueprints

Arquivo responsável por criar o objeto `app` do Flask e registrar todos os módulos de rotas.

Exemplo importante:

```12:23:app.py
app = Flask(__name__)

app.register_blueprint(alunos_bp)
app.register_blueprint(professores_bp)
app.register_blueprint(turmas_bp)
app.register_blueprint(relatorios_bp)


@app.route("/")
def home():
    """Rota da página inicial."""
    return render_template("base.html")
```

**O que acontece aqui:**

- `Flask(__name__)`: cria a aplicação.
- `register_blueprint(...)`: conecta cada módulo de rotas (`alunos`, `professores`, `turmas`, `relatorios`) na aplicação principal.
- A rota `/` mostra o menu inicial (`base.html`) com links para as telas.

---

## `config.py` – conexão com o banco de dados

Centraliza os detalhes da conexão com o PostgreSQL e oferece funções utilitárias.

Trecho relevante:

```4:22:config.py
DB_CONFIG = {
    "host": "...",
    "database": "test1_v02p",
    "user": "test1_v02p_user",
    "password": "...",
    "port": "5432",
}


def get_connection():
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"],
    )


def dict_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
```

**Funções principais:**

- **`get_connection()`**: abre uma nova conexão com o banco.
- **`dict_cursor(conn)`**: devolve um cursor que retorna linhas como dicionários
  (em vez de tuplas), o que facilita o uso nas APIs/JSON.

---

## Rotas de Alunos – `routes/alunos.py`

Este módulo implementa:

- Página HTML `/alunos/` (interface para o usuário).
- API REST sob `/alunos/api` com operações:
  - `GET /alunos/api` – listar
  - `POST /alunos/api` – criar
  - `PUT /alunos/api/<id>` – atualizar
  - `DELETE /alunos/api/<id>` – deletar

### Blueprint e página HTML

```4:23:routes/alunos.py
alunos_bp = Blueprint("alunos", __name__, url_prefix="/alunos")


@alunos_bp.route("/", methods=["GET"])
def page_listar_alunos():
    conn = get_connection()
    cur = dict_cursor(conn)
    cur.execute(
        """
        SELECT a.id, a.nome, a.idade, a.turma_id, t.nome AS turma_nome
        FROM alunos a
        LEFT JOIN turmas t ON t.id = a.turma_id
        ORDER BY a.id;
    """
    )
    alunos = cur.fetchall()
    conn.close()
    return render_template("alunos.html", alunos=alunos)
```

**Como funciona:**

- O **blueprint** `alunos_bp` agrupa todas as rotas de alunos com prefixo `/alunos`.
- A função `page_listar_alunos`:
  - abre conexão (`get_connection`);
  - executa um `SELECT` com `JOIN` nas turmas;
  - passa a lista de alunos para o template `alunos.html`.

### API – exemplo de criação de aluno

```32:44:routes/alunos.py
@alunos_bp.route("/api", methods=["POST"])
def api_criar_aluno():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO alunos (nome, idade, turma_id) VALUES (%s, %s, %s) RETURNING id;",
        (data.get("nome"), data.get("idade"), data.get("turma_id")),
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Criado", "id": new_id}), 201
```

**Passo a passo:**

- `request.json`: lê o corpo da requisição como dicionário Python.
- `INSERT ... RETURNING id`: insere o aluno e devolve o ID gerado.
- `conn.commit()`: grava as alterações.
- `jsonify(...)`: responde com JSON (incluindo o novo `id`).

---

## Rotas de Professores – `routes/professores.py`

Mesma ideia de alunos, mas para a tabela `professores`.

Exemplo de listagem (página HTML):

```6:17:routes/professores.py
@professores_bp.route("/", methods=["GET"])
def page_listar_professores():
    conn = get_connection()
    cur = dict_cursor(conn)
    cur.execute(
        """
        SELECT p.id, p.nome, p.disciplina
        FROM professores p
        ORDER BY p.id;
    """
    )
    professores = cur.fetchall()
    conn.close()
    return render_template("professores.html", professores=professores)
```

Exemplo de criação via API:

```28:40:routes/professores.py
@professores_bp.route("/api", methods=["POST"])
def api_criar_professor():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO professores (nome, disciplina) VALUES (%s, %s) RETURNING id;",
        (data.get("nome"), data.get("disciplina")),
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Criado", "id": new_id}), 201
```

---

## Rotas de Turmas – `routes/turmas.py`

Gerencia a entidade **turma**, com relacionamento opcional com professor.

Exemplo da página HTML:

```6:18:routes/turmas.py
@turmas_bp.route("/", methods=["GET"])
def page_listar_turmas():
    conn = get_connection()
    cur = dict_cursor(conn)
    cur.execute(
        """
        SELECT t.id, t.nome, t.sala, t.professor_id, p.nome AS professor_nome
        FROM turmas t
        LEFT JOIN professores p ON p.id = t.professor_id
        ORDER BY t.id;
    """
    )
    turmas = cur.fetchall()
    conn.close()
    return render_template("turmas.html", turmas=turmas)
```

Exemplo de atualização:

```43:54:routes/turmas.py
@turmas_bp.route("/api/<int:id>", methods=["PUT"])
def api_atualizar_turma(id):
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE turmas SET nome=%s, sala=%s, professor_id=%s WHERE id=%s",
        (data.get("nome"), data.get("sala"), data.get("professor_id"), id),
    )
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Atualizado"})
```

---

## Relatório – `routes/relatorios.py` e `templates/relatorio_alunos_por_turma.html`

Gera uma visão de **todas as turmas e seus respectivos alunos**.

### Lado Python (montando os dados)

```6:40:routes/relatorios.py
@relatorios_bp.route("/relatorios/alunos-por-turma")
def alunos_por_turma():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, nome, sala 
        FROM turmas
        ORDER BY id;
    """
    )
    turmas = cur.fetchall()

    dados = []

    for turma in turmas:
        turma_id = turma[0]

        cur.execute(
            """
            SELECT id, nome, idade
            FROM alunos
            WHERE turma_id = %s;
        """,
            (turma_id,),
        )

        alunos = cur.fetchall()

        dados.append(
            {
                "id": turma_id,
                "nome_turma": turma[1],
                "sala": turma[2],
                "alunos": [
                    {"id": a[0], "nome": a[1], "idade": a[2]} for a in alunos
                ],
            }
        )

    return render_template("relatorio_alunos_por_turma.html", dados=dados)
```

**Resumo:**

- Busca todas as turmas.
- Para cada turma, busca os alunos com aquele `turma_id`.
- Monta uma lista de dicionários (`dados`) usada no template.

### Lado template (Jinja2)

```19:43:templates/relatorio_alunos_por_turma.html
{% for turma in dados %}
    <div class="turma">
        <h2>Turma: {{ turma.nome_turma }} (Sala: {{ turma.sala }})</h2>

        {% if turma.alunos %}
        <table>
            <tr>
                <th>ID</th>
                <th>Nome</th>
                <th>Idade</th>
            </tr>

            {% for aluno in turma.alunos %}
            <tr>
                <td>{{ aluno.id }}</td>
                <td>{{ aluno.nome }}</td>
                <td>{{ aluno.idade }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p><b>Nenhum aluno nesta turma.</b></p>
        {% endif %}
    </div>
{% endfor %}
```

**O que acontece:**

- Laço externo `{% for turma in dados %}`: percorre cada turma.
- Laço interno `{% for aluno in turma.alunos %}`: monta as linhas da tabela.
- Se `turma.alunos` estiver vazio, mostra a mensagem "Nenhum aluno nesta turma".

---

## Templates com JavaScript – `alunos.html`, `professores.html`, `turmas.html`

Esses templates seguem o mesmo padrão:

- Um **formulário** HTML com inputs.
- Uma **tabela** para exibir os dados.
- Um **script JavaScript** que chama a API REST (backend Flask) via `fetch`.

### Exemplo – criação de aluno (frontend)

```47:57:templates/alunos.html
document.getElementById("formAluno").addEventListener("submit", async (e)=>{
    e.preventDefault();
    const payload = {
        nome: document.getElementById("nome").value,
        idade: parseInt(document.getElementById("idade").value),
        turma_id: parseInt(document.getElementById("turma_id").value)
    };
    await fetch(API, { method: "POST", headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) });
    e.target.reset();
    listar();
});
```

Conecta diretamente com a rota **`POST /alunos/api`** descrita em `routes/alunos.py`.

### Exemplo – edição de professor (frontend)

```59:68:templates/professores.html
async function editar(id, nome, disciplina){
    const novoNome = prompt("Nome:", nome) || nome;
    const novaDisciplina = prompt("Disciplina:", disciplina) || disciplina;
    await fetch(`${API}/${id}`, {
        method: "PUT",
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ nome: novoNome, disciplina: novaDisciplina })
    });
    listar();
}
```

Usa `PUT /professores/api/<id>` para atualizar o registro no backend.

---

## Página inicial – `templates/base.html`

Serve apenas como **menu de navegação**:

```8:14:templates/base.html
<h1>Sistema de Gestão Escolar</h1>
<ul>
    <li><a href="/professores/">Professores</a></li>
    <li><a href="/turmas/">Turmas</a></li>
    <li><a href="/alunos/">Alunos</a></li>
    <li><a href="/relatorios/alunos-por-turma">Relatório: Alunos por Turma</a></li>
</ul>
```

Ao clicar em cada link, o navegador chama a rota correspondente, que por sua vez
carrega a página HTML e, em muitos casos, dispara o JavaScript que consome as APIs.

---

## Resumo conceitual

- **Back-end (Flask + psycopg2)**:
  - expõe rotas HTTP (páginas e APIs JSON);
  - acessa o PostgreSQL usando SQL simples (`SELECT`, `INSERT`, `UPDATE`, `DELETE`);
  - organiza o código em **blueprints** por domínio (alunos, professores, turmas, relatórios).

- **Front-end (HTML + JavaScript)**:
  - renderiza formulários e tabelas;
  - chama as rotas de API usando `fetch` (AJAX);
  - atualiza a tabela em tempo real após operações de CRUD.




