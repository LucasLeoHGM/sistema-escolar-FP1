from flask import Blueprint, request, jsonify, render_template
from database import SessionLocal
from models import Turma
from sqlalchemy.exc import OperationalError

turmas_bp = Blueprint("turmas", __name__, url_prefix="/turmas")


@turmas_bp.route("/", methods=["GET"])
def page_listar_turmas():
    try:
        db = SessionLocal()
    except OperationalError as e:
        return render_template("turmas.html", turmas=[], db_error=str(e))

    try:
        turmas = db.query(Turma).order_by(Turma.id).all()
        turmas_out = []
        for t in turmas:
            turmas_out.append({'id': t.id, 'nome': t.nome, 'sala': t.sala, 'professor_id': t.professor_id, 'professor_nome': t.professor.nome if t.professor else None})
        return render_template("turmas.html", turmas=turmas_out)
    finally:
        db.close()


@turmas_bp.route("/api", methods=["GET"])
def api_listar_turmas():
    db = SessionLocal()
    try:
        turmas = db.query(Turma).order_by(Turma.id).all()
        return jsonify([{'id': t.id, 'nome': t.nome, 'sala': t.sala, 'professor_id': t.professor_id} for t in turmas])
    finally:
        db.close()


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

    db = SessionLocal()
    try:
        t = Turma(nome=data.get('nome'), sala=data.get('sala'), professor_id=data.get('professor_id'))
        db.add(t)
        db.commit()
        db.refresh(t)
        return jsonify({"mensagem": "Criado", "id": t.id}), 201
    finally:
        db.close()


@turmas_bp.route("/api/<int:id>", methods=["PUT"])
def api_atualizar_turma(id):
    data = request.json
    err = _validar_turma_payload(data)
    if err:
        return jsonify({"erro": err}), 400

    db = SessionLocal()
    try:
        t = db.get(Turma, id)
        if not t:
            return jsonify({"erro": "Turma não encontrada"}), 404
        t.nome = data.get('nome')
        t.sala = data.get('sala')
        t.professor_id = data.get('professor_id')
        db.commit()
        return jsonify({"mensagem": "Atualizado"})
    finally:
        db.close()


@turmas_bp.route("/api/<int:id>", methods=["DELETE"])
def api_deletar_turma(id):
    db = SessionLocal()
    try:
        t = db.get(Turma, id)
        if not t:
            return jsonify({"erro": "Turma não encontrada"}), 404
        db.delete(t)
        db.commit()
        return jsonify({"mensagem": "Deletado"})
    finally:
        db.close()
