from flask import Blueprint, request, jsonify, render_template
from config import get_connection, dict_cursor

turmas_bp = Blueprint("turmas", __name__, url_prefix="/turmas")


@turmas_bp.route("/", methods=["GET"])
def page_listar_turmas():
    conn = get_connection()
    try:
        cur = dict_cursor(conn)
        cur.execute("""
            SELECT t.id, t.nome, t.sala, t.professor_id, p.nome AS professor_nome
            FROM turmas t
            LEFT JOIN professores p ON p.id = t.professor_id
            ORDER BY t.id;
        """)
        turmas = cur.fetchall()
        return render_template("turmas.html", turmas=turmas)
    finally:
        conn.close()


@turmas_bp.route("/api", methods=["GET"])
def api_listar_turmas():
    conn = get_connection()
    try:
        cur = dict_cursor(conn)
        cur.execute("SELECT * FROM turmas ORDER BY id;")
        dados = cur.fetchall()
        return jsonify(dados)
    finally:
        conn.close()


def _validar_turma_payload(data):
    if not data or not isinstance(data, dict):
        return "Payload inválido"
    nome = data.get("nome")
    sala = data.get("sala")
    if not nome or not str(nome).strip():
        return "Campo 'nome' é obrigatório"
    if not sala or not str(sala).strip():
        return "Campo 'sala' é obrigatório"
    # professor_id é opcional; se fornecido, deve ser inteiro
    prof = data.get("professor_id")
    if prof is not None:
        try:
            int(prof)
        except (TypeError, ValueError):
            return "Campo 'professor_id' deve ser um inteiro"
    return None


@turmas_bp.route("/api", methods=["POST"])
def api_criar_turma():
    data = request.json
    err = _validar_turma_payload(data)
    if err:
        return jsonify({"erro": err}), 400

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO turmas (nome, sala, professor_id) VALUES (%s, %s, %s) RETURNING id;",
            (data.get("nome"), data.get("sala"), data.get("professor_id"))
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"mensagem": "Criado", "id": new_id}), 201
    finally:
        conn.close()


@turmas_bp.route("/api/<int:id>", methods=["PUT"])
def api_atualizar_turma(id):
    data = request.json
    err = _validar_turma_payload(data)
    if err:
        return jsonify({"erro": err}), 400

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE turmas SET nome=%s, sala=%s, professor_id=%s WHERE id=%s",
            (data.get("nome"), data.get("sala"), data.get("professor_id"), id)
        )
        conn.commit()
        return jsonify({"mensagem": "Atualizado"})
    finally:
        conn.close()


@turmas_bp.route("/api/<int:id>", methods=["DELETE"])
def api_deletar_turma(id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM turmas WHERE id=%s", (id,))
        conn.commit()
        return jsonify({"mensagem": "Deletado"})
    finally:
        conn.close()
