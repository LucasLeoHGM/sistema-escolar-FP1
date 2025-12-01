from flask import Blueprint, request, jsonify, render_template
from config import get_connection, dict_cursor

professores_bp = Blueprint("professores", __name__, url_prefix="/professores")


@professores_bp.route("/", methods=["GET"])
def page_listar_professores():
    conn = get_connection()
    try:
        cur = dict_cursor(conn)
        cur.execute("""
            SELECT p.id, p.nome, p.disciplina
            FROM professores p
            ORDER BY p.id;
        """)
        professores = cur.fetchall()
        return render_template("professores.html", professores=professores)
    finally:
        conn.close()


@professores_bp.route("/api", methods=["GET"])
def api_listar_professores():
    conn = get_connection()
    try:
        cur = dict_cursor(conn)
        cur.execute("SELECT * FROM professores ORDER BY id;")
        dados = cur.fetchall()
        return jsonify(dados)
    finally:
        conn.close()


def _validar_professor_payload(data):
    if not data or not isinstance(data, dict):
        return "Payload inválido"
    nome = data.get("nome")
    disciplina = data.get("disciplina")
    if not nome or not str(nome).strip():
        return "Campo 'nome' é obrigatório"
    if not disciplina or not str(disciplina).strip():
        return "Campo 'disciplina' é obrigatório"
    return None


@professores_bp.route("/api", methods=["POST"])
def api_criar_professor():
    data = request.json
    err = _validar_professor_payload(data)
    if err:
        return jsonify({"erro": err}), 400

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO professores (nome, disciplina) VALUES (%s, %s) RETURNING id;",
            (data.get("nome"), data.get("disciplina"))
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"mensagem": "Criado", "id": new_id}), 201
    finally:
        conn.close()


@professores_bp.route("/api/<int:id>", methods=["PUT"])
def api_atualizar_professor(id):
    data = request.json
    err = _validar_professor_payload(data)
    if err:
        return jsonify({"erro": err}), 400

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE professores SET nome=%s, disciplina=%s WHERE id=%s",
            (data.get("nome"), data.get("disciplina"), id)
        )
        conn.commit()
        return jsonify({"mensagem": "Atualizado"})
    finally:
        conn.close()


@professores_bp.route("/api/<int:id>", methods=["DELETE"])
def api_deletar_professor(id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM professores WHERE id=%s", (id,))
        conn.commit()
        return jsonify({"mensagem": "Deletado"})
    finally:
        conn.close()
