from flask import Blueprint, request, jsonify, render_template
import psycopg2
from config import get_connection, dict_cursor

professores_bp = Blueprint("professores", __name__, url_prefix="/professores")

@professores_bp.route("/", methods=["GET"])
def page_listar_professores():
    try:
        conn = get_connection()
        cur = dict_cursor(conn)
        cur.execute("""
            SELECT p.id, p.nome, p.disciplina
            FROM professores p
            ORDER BY p.id;
        """)
        professores = cur.fetchall()
        return render_template("professores.html", professores=professores)

    except Exception as e:
        return f"Erro ao carregar professores: {e}", 500


@professores_bp.route("/api", methods=["GET"])
def api_listar_professores():
    try:
        conn = get_connection()
        cur = dict_cursor(conn)
        cur.execute("SELECT * FROM professores ORDER BY id;")
        return jsonify(cur.fetchall())
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@professores_bp.route("/api", methods=["POST"])
def api_criar_professor():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO professores (nome, disciplina) VALUES (%s, %s) RETURNING id;",
            (data.get("nome"), data.get("disciplina"))
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"mensagem": "Criado", "id": new_id}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"erro": str(e)}), 500


@professores_bp.route("/api/<int:id>", methods=["PUT"])
def api_atualizar_professor(id):
    data = request.json
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "UPDATE professores SET nome=%s, disciplina=%s WHERE id=%s",
            (data.get("nome"), data.get("disciplina"), id)
        )

        if cur.rowcount == 0:
            return jsonify({"erro": "Professor não encontrado."}), 404

        conn.commit()
        return jsonify({"mensagem": "Atualizado"})

    except Exception as e:
        conn.rollback()
        return jsonify({"erro": str(e)}), 500


@professores_bp.route("/api/<int:id>", methods=["DELETE"])
def api_deletar_professor(id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM professores WHERE id=%s", (id,))

        if cur.rowcount == 0:
            return jsonify({"erro": "Professor não encontrado."}), 404

        conn.commit()
        return jsonify({"mensagem": "Deletado"})

    except Exception as e:
        conn.rollback()
        return jsonify({"erro": str(e)}), 500
