from flask import Blueprint, request, jsonify, render_template
from config import get_connection, dict_cursor

turmas_bp = Blueprint("turmas", __name__, url_prefix="/turmas")

@turmas_bp.route("/", methods=["GET"])
def page_listar_turmas():
    conn = get_connection()
    cur = dict_cursor(conn)
    cur.execute("""
        SELECT t.id, t.nome, t.sala, t.professor_id, p.nome AS professor_nome
        FROM turmas t
        LEFT JOIN professores p ON p.id = t.professor_id
        ORDER BY t.id;
    """)
    turmas = cur.fetchall()
    conn.close()
    return render_template("turmas.html", turmas=turmas)

@turmas_bp.route("/api", methods=["GET"])
def api_listar_turmas():
    conn = get_connection()
    cur = dict_cursor(conn)
    cur.execute("SELECT * FROM turmas ORDER BY id;")
    dados = cur.fetchall()
    conn.close()
    return jsonify(dados)

@turmas_bp.route("/api", methods=["POST"])
def api_criar_turma():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO turmas (nome, sala, professor_id) VALUES (%s, %s, %s) RETURNING id;",
        (data.get("nome"), data.get("sala"), data.get("professor_id"))
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Criado", "id": new_id}), 201

@turmas_bp.route("/api/<int:id>", methods=["PUT"])
def api_atualizar_turma(id):
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE turmas SET nome=%s, sala=%s, professor_id=%s WHERE id=%s",
        (data.get("nome"), data.get("sala"), data.get("professor_id"), id)
    )
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Atualizado"})

@turmas_bp.route("/api/<int:id>", methods=["DELETE"])
def api_deletar_turma(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM turmas WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Deletado"})
