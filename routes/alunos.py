from flask import Blueprint, request, jsonify, render_template
from database import SessionLocal
from models import Aluno, Turma
from sqlalchemy.exc import OperationalError, IntegrityError
from sqlalchemy.orm import joinedload

alunos_bp = Blueprint("alunos", __name__, url_prefix="/alunos")


# Página HTML
@alunos_bp.route("/", methods=["GET"])
def page_listar_alunos():
    try:
        db = SessionLocal()
    except OperationalError as e:
        return render_template("alunos.html", alunos=[], db_error=str(e))

    try:
        alunos = db.query(Aluno).options(joinedload(Aluno.turma)).order_by(Aluno.id).all()
        # Convert to simple dicts for template compatibility
        alunos_out = []
        for a in alunos:
            alunos_out.append({
                'id': a.id,
                'nome': a.nome,
                'idade': a.idade,
                'turma_id': a.turma_id,
                'turma_nome': a.turma.nome if a.turma else None
            })
        return render_template("alunos.html", alunos=alunos_out)
    finally:
        db.close()


# API JSON: listar
@alunos_bp.route("/api", methods=["GET"])
def api_listar_alunos():
    try:
        db = SessionLocal()
    except OperationalError:
        return jsonify([])

    try:
        alunos = db.query(Aluno).order_by(Aluno.id).all()
        return jsonify([{'id': a.id, 'nome': a.nome, 'idade': a.idade, 'turma_id': a.turma_id} for a in alunos])
    finally:
        db.close()


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

    try:
        db = SessionLocal()
    except OperationalError:
        return jsonify({"erro": "Banco de dados indisponível"}), 503

    try:
        turma_id = data.get('turma_id')
        if turma_id is not None:
            # validar existência da turma referenciada
            t = db.get(Turma, turma_id)
            if not t:
                return jsonify({"erro": "Turma não encontrada"}), 400

        aluno = Aluno(nome=data.get('nome'), idade=int(data.get('idade')), turma_id=turma_id)
        db.add(aluno)
        try:
            db.commit()
        except IntegrityError as ie:
            db.rollback()
            return jsonify({"erro": "Erro de integridade no banco: %s" % str(ie)}), 400
        db.refresh(aluno)
        return jsonify({"mensagem": "Criado", "id": aluno.id}), 201
    finally:
        db.close()


# API JSON: atualizar
@alunos_bp.route("/api/<int:id>", methods=["PUT"])
def api_atualizar_aluno(id):
    data = request.json
    err = _validar_aluno_payload(data)
    if err:
        return jsonify({"erro": err}), 400

    try:
        db = SessionLocal()
    except OperationalError:
        return jsonify({"erro": "Banco de dados indisponível"}), 503

    try:
        aluno = db.get(Aluno, id)
        if not aluno:
            return jsonify({"erro": "Aluno não encontrado"}), 404

        turma_id = data.get('turma_id')
        if turma_id is not None:
            t = db.get(Turma, turma_id)
            if not t:
                return jsonify({"erro": "Turma não encontrada"}), 400

        aluno.nome = data.get('nome')
        aluno.idade = int(data.get('idade'))
        aluno.turma_id = turma_id
        try:
            db.commit()
        except IntegrityError as ie:
            db.rollback()
            return jsonify({"erro": "Erro de integridade no banco: %s" % str(ie)}), 400
        return jsonify({"mensagem": "Atualizado"})
    finally:
        db.close()


# API JSON: deletar
@alunos_bp.route("/api/<int:id>", methods=["DELETE"])
def api_deletar_aluno(id):
    try:
        db = SessionLocal()
    except OperationalError:
        return jsonify({"erro": "Banco de dados indisponível"}), 503

    try:
        aluno = db.get(Aluno, id)
        if not aluno:
            return jsonify({"erro": "Aluno não encontrado"}), 404
        db.delete(aluno)
        db.commit()
        return jsonify({"mensagem": "Deletado"})
    finally:
        db.close()
