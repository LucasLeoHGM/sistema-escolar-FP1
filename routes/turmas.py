from flask import Blueprint, request, jsonify, render_template
from database import session_scope
from models import Turma
from sqlalchemy.exc import OperationalError, IntegrityError

turmas_bp = Blueprint("turmas", __name__, url_prefix="/turmas")


@turmas_bp.route("/", methods=["GET"])
def page_listar_turmas():
    try:
        with session_scope() as db:
            turmas = db.query(Turma).order_by(Turma.id).all()
            turmas_out = []
            for t in turmas:
                turmas_out.append({'id': t.id, 'nome': t.nome, 'sala': t.sala, 'professor_id': t.professor_id, 'professor_nome': t.professor.nome if t.professor else None})
            return render_template("turmas.html", turmas=turmas_out)
    except OperationalError as e:
        return render_template("turmas.html", turmas=[], db_error=str(e))


@turmas_bp.route("/api", methods=["GET"])
def api_listar_turmas():
    try:
        with session_scope() as db:
            turmas = db.query(Turma).order_by(Turma.id).all()
            return jsonify([{'id': t.id, 'nome': t.nome, 'sala': t.sala, 'professor_id': t.professor_id} for t in turmas])
    except OperationalError:
        return jsonify([]), 503


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

    try:
        with session_scope() as db:
            t = Turma(nome=data.get('nome'), sala=data.get('sala'), professor_id=data.get('professor_id'))
            db.add(t)
            db.flush()
            db.refresh(t)
            return jsonify({"mensagem": "Criado", "id": t.id}), 201
    except OperationalError:
        return jsonify({"erro": "Banco de dados indisponível"}), 503
    except IntegrityError as ie:
        return jsonify({"erro": str(ie)}), 400


@turmas_bp.route("/api/<int:id>", methods=["PUT"])
def api_atualizar_turma(id):
    data = request.json
    err = _validar_turma_payload(data)
    if err:
        return jsonify({"erro": err}), 400

    try:
        with session_scope() as db:
            t = db.get(Turma, id)
            if not t:
                return jsonify({"erro": "Turma não encontrada"}), 404
            t.nome = data.get('nome')
            t.sala = data.get('sala')
            t.professor_id = data.get('professor_id')
            db.flush()
            return jsonify({"mensagem": "Atualizado"})
    except OperationalError:
        return jsonify({"erro": "Banco de dados indisponível"}), 503
    except IntegrityError as ie:
        return jsonify({"erro": str(ie)}), 400


@turmas_bp.route("/api/<int:id>", methods=["DELETE"])
def api_deletar_turma(id):
    try:
        with session_scope() as db:
            t = db.get(Turma, id)
            if not t:
                return jsonify({"erro": "Turma não encontrada"}), 404
            db.delete(t)
            return jsonify({"mensagem": "Deletado"})
    except OperationalError:
        return jsonify({"erro": "Banco de dados indisponível"}), 503
