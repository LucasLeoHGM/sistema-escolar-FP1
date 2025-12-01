from flask import Blueprint, request, jsonify, render_template
from config import get_connection, dict_cursor

alunos_bp = Blueprint("alunos", __name__, url_prefix="/alunos")

# Página HTML
@alunos_bp.route("/", methods=["GET"])
def page_listar_alunos():
    conn = get_connection()
    cur = dict_cursor(conn)
    cur.execute("""
        SELECT a.id, a.nome, a.idade, a.turma_id, t.nome AS turma_nome
        FROM alunos a
        LEFT JOIN turmas t ON t.id = a.turma_id
        ORDER BY a.id;
    """)
    alunos = cur.fetchall()
    conn.close()
    return render_template("alunos.html", alunos=alunos)

# API JSON: listar
@alunos_bp.route("/api", methods=["GET"])
def api_listar_alunos():
    conn = get_connection()
    cur = dict_cursor(conn)
    cur.execute("SELECT * FROM alunos ORDER BY id;")
    dados = cur.fetchall()
    conn.close()
    return jsonify(dados)

# API JSON: criar
@alunos_bp.route("/api", methods=["POST"])
def api_criar_aluno():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO alunos (nome, idade, turma_id) VALUES (%s, %s, %s) RETURNING id;",
        (data.get("nome"), data.get("idade"), data.get("turma_id"))
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Criado", "id": new_id}), 201

# API JSON: atualizar
@alunos_bp.route("/api/<int:id>", methods=["PUT"])
def api_atualizar_aluno(id):
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE alunos SET nome=%s, idade=%s, turma_id=%s WHERE id=%s",
        (data.get("nome"), data.get("idade"), data.get("turma_id"), id)
    )
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Atualizado"})

# API JSON: deletar
@alunos_bp.route("/api/<int:id>", methods=["DELETE"])
def api_deletar_aluno(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM alunos WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Deletado"})
