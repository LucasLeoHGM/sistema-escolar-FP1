from flask import Blueprint, request, jsonify, render_template
import psycopg2
from config import get_connection, dict_cursor

alunos_bp = Blueprint("alunos", __name__, url_prefix="/alunos")

@alunos_bp.route("/", methods=["GET"])
def page_listar_alunos():
    try:
        conn = get_connection()
        cur = dict_cursor(conn)
        cur.execute("""
            SELECT a.id, a.nome, a.idade, a.turma_id, t.nome AS turma_nome
            FROM alunos a
            LEFT JOIN turmas t ON t.id = a.turma_id
            ORDER BY a.id;
        """)
        alunos = cur.fetchall()
        return render_template("alunos.html", alunos=alunos)

    except Exception as e:
        return f"Erro ao carregar alunos: {e}", 500


@alunos_bp.route("/api", methods=["GET"])
def api_listar_alunos():
    try:
        conn = get_connection()
        cur = dict_cursor(conn)
        cur.execute("SELECT * FROM alunos ORDER BY id;")
        return jsonify(cur.fetchall())
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@alunos_bp.route("/api", methods=["POST"])
def api_criar_aluno():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO alunos (nome, idade, turma_id) VALUES (%s, %s, %s) RETURNING id;",
            (data.get("nome"), data.get("idade"), data.get("turma_id"))
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"mensagem": "Criado", "id": new_id}), 201

    except psycopg2.Error as e:
        conn.rollback()

        if "foreign key" in str(e).lower():
            return jsonify({"erro": "Turma inválida. Informe um ID de turma existente."}), 400

        return jsonify({"erro": "Erro ao criar aluno."}), 500


@alunos_bp.route("/api/<int:id>", methods=["PUT"])
def api_atualizar_aluno(id):
    data = request.json
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "UPDATE alunos SET nome=%s, idade=%s, turma_id=%s WHERE id=%s",
            (data.get("nome"), data.get("idade"), data.get("turma_id"), id)
        )

        if cur.rowcount == 0:
            return jsonify({"erro": "Aluno não encontrado."}), 404

        conn.commit()
        return jsonify({"mensagem": "Atualizado"})

    except psycopg2.Error as e:
        conn.rollback()

        if "foreign key" in str(e).lower():
            return jsonify({"erro": "Turma inválida."}), 400

        return jsonify({"erro": "Erro ao atualizar aluno."}), 500


@alunos_bp.route("/api/<int:id>", methods=["DELETE"])
def api_deletar_aluno(id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM alunos WHERE id=%s", (id,))

        if cur.rowcount == 0:
            return jsonify({"erro": "Aluno não encontrado."}), 404

        conn.commit()
        return jsonify({"mensagem": "Deletado"})

    except Exception as e:
        conn.rollback()
        return jsonify({"erro": str(e)}), 500
