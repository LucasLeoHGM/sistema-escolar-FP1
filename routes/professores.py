from flask import Blueprint, request, jsonify, render_template
from config import get_connection, dict_cursor

professores_bp = Blueprint("professores", __name__, url_prefix="/professores")

@professores_bp.route("/", methods=["GET"])
def page_listar_professores():
    conn = get_connection()
    cur = dict_cursor(conn)
    cur.execute("""
        SELECT p.id, p.nome, p.disciplina
        FROM professores p
        ORDER BY p.id;
    """)
    professores = cur.fetchall()
    conn.close()
    return render_template("professores.html", professores=professores)

@professores_bp.route("/api", methods=["GET"])
def api_listar_professores():
    conn = get_connection()
    cur = dict_cursor(conn)
    cur.execute("SELECT * FROM professores ORDER BY id;")
    dados = cur.fetchall()
    conn.close()
    return jsonify(dados)

@professores_bp.route("/api", methods=["POST"])
def api_criar_professor():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO professores (nome, disciplina) VALUES (%s, %s) RETURNING id;",
        (data.get("nome"), data.get("disciplina"))
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Criado", "id": new_id}), 201

@professores_bp.route("/api/<int:id>", methods=["PUT"])
def api_atualizar_professor(id):
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE professores SET nome=%s, disciplina=%s WHERE id=%s",
        (data.get("nome"), data.get("disciplina"), id)
    )
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Atualizado"})

@professores_bp.route("/api/<int:id>", methods=["DELETE"])
def api_deletar_professor(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM professores WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Deletado"})
