from flask import Blueprint, request, jsonify, render_template
import psycopg2
from config import get_connection, dict_cursor

turmas_bp = Blueprint("turmas", __name__, url_prefix="/turmas")

@turmas_bp.route("/", methods=["GET"])
def page_listar_turmas():
    try:
        conn = get_connection()
        cur = dict_cursor(conn)
        cur.execute("""
            SELECT t.id, t.nome, t.sala, t.professor_id, p.nome AS professor_nome
            FROM turmas t
            LEFT JOIN professores p ON p.id = t.professor_id
            ORDER BY t.id;
        """)
        turmas = cur.fetchall()
        return render_template("turmas.html", turmas=turmas)

    except Exception as e:
        return f"Erro ao carregar turmas: {e}", 500


@turmas_bp.route("/api", methods=["GET"])
def api_listar_turmas():
    try:
        conn = get_connection()
        cur = dict_cursor(conn)
        cur.execute("SELECT * FROM turmas ORDER BY id;")
        return jsonify(cur.fetchall())
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@turmas_bp.route("/api", methods=["POST"])
def api_criar_turma():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO turmas (nome, sala, professor_id) VALUES (%s, %s, %s) RETURNING id;",
            (data.get("nome"), data.get("sala"), data.get("professor_id"))
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"mensagem": "Criado", "id": new_id}), 201

    except psycopg2.Error as e:
        conn.rollback()

        if "foreign key" in str(e).lower():
            return jsonify({"erro": "Professor inválido. Informe um professor existente."}), 400

        return jsonify({"erro": "Erro ao criar turma."}), 500


@turmas_bp.route("/api/<int:id>", methods=["PUT"])
def api_atualizar_turma(id):
    data = request.json
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "UPDATE turmas SET nome=%s, sala=%s, professor_id=%s WHERE id=%s",
            (data.get("nome"), data.get("sala"), data.get("professor_id"), id)
        )

        if cur.rowcount == 0:
            return jsonify({"erro": "Turma não encontrada."}), 404

        conn.commit()
        return jsonify({"mensagem": "Atualizado"})

    except psycopg2.Error as e:
        conn.rollback()

        if "foreign key" in str(e).lower():
            return jsonify({"erro": "Professor inválido."}), 400

        return jsonify({"erro": "Erro ao atualizar turma."}), 500


@turmas_bp.route("/api/<int:id>", methods=["DELETE"])
def api_deletar_turma(id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM turmas WHERE id=%s", (id,))

        if cur.rowcount == 0:
            return jsonify({"erro": "Turma não encontrada."}), 404

        conn.commit()
        return jsonify({"mensagem": "Deletado"})

    except Exception as e:
        conn.rollback()
        return jsonify({"erro": str(e)}), 500
