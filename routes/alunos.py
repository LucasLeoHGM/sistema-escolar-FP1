from flask import Blueprint, request, jsonify, render_template
from config import get_connection, dict_cursor

alunos_bp = Blueprint("alunos", __name__, url_prefix="/alunos")


# Página HTML
@alunos_bp.route("/", methods=["GET"])
def page_listar_alunos():
    conn = get_connection()
    try:
        cur = dict_cursor(conn)
        cur.execute("""
            SELECT a.id, a.nome, a.idade, a.turma_id, t.nome AS turma_nome
            FROM alunos a
            LEFT JOIN turmas t ON t.id = a.turma_id
            ORDER BY a.id;
        """)
        alunos = cur.fetchall()
        return render_template("alunos.html", alunos=alunos)
    finally:
        conn.close()


# API JSON: listar
@alunos_bp.route("/api", methods=["GET"])
def api_listar_alunos():
    conn = get_connection()
    try:
        cur = dict_cursor(conn)
        cur.execute("SELECT * FROM alunos ORDER BY id;")
        dados = cur.fetchall()
        return jsonify(dados)
    finally:
        conn.close()


# Helper: validação mínima de entrada
def _validar_aluno_payload(data):
    if not data or not isinstance(data, dict):
        return "Payload inválido"
    nome = data.get("nome")
    idade = data.get("idade")
    if not nome or not str(nome).strip():
        return "Campo 'nome' é obrigatório"
    if idade is None:
        return "Campo 'idade' é obrigatório"
    try:
        idade_int = int(idade)
        if idade_int < 0:
            return "Campo 'idade' deve ser >= 0"
    except (TypeError, ValueError):
        return "Campo 'idade' deve ser um número inteiro"
    return None


# API JSON: criar
@alunos_bp.route("/api", methods=["POST"])
def api_criar_aluno():
    data = request.json
    err = _validar_aluno_payload(data)
    if err:
        return jsonify({"erro": err}), 400

    conn = get_connection()
    try:
        cur = conn.cursor()
        turma_id = data.get("turma_id")
        cur.execute(
            "INSERT INTO alunos (nome, idade, turma_id) VALUES (%s, %s, %s) RETURNING id;",
            (data.get("nome"), int(data.get("idade")), turma_id)
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"mensagem": "Criado", "id": new_id}), 201
    finally:
        conn.close()


# API JSON: atualizar
@alunos_bp.route("/api/<int:id>", methods=["PUT"])
def api_atualizar_aluno(id):
    data = request.json
    err = _validar_aluno_payload(data)
    if err:
        return jsonify({"erro": err}), 400

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE alunos SET nome=%s, idade=%s, turma_id=%s WHERE id=%s",
            (data.get("nome"), int(data.get("idade")), data.get("turma_id"), id)
        )
        conn.commit()
        return jsonify({"mensagem": "Atualizado"})
    finally:
        conn.close()


# API JSON: deletar
@alunos_bp.route("/api/<int:id>", methods=["DELETE"])
def api_deletar_aluno(id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM alunos WHERE id=%s", (id,))
        conn.commit()
        return jsonify({"mensagem": "Deletado"})
    finally:
        conn.close()
