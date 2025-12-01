from flask import Blueprint, request, jsonify, render_template
from database import SessionLocal
from models import Professor
from sqlalchemy.exc import OperationalError

professores_bp = Blueprint("professores", __name__, url_prefix="/professores")


@professores_bp.route("/", methods=["GET"])
def page_listar_professores():
    try:
        db = SessionLocal()
    except OperationalError as e:
        return render_template("professores.html", professores=[], db_error=str(e))

    try:
        profs = db.query(Professor).order_by(Professor.id).all()
        profs_out = [{'id': p.id, 'nome': p.nome, 'disciplina': p.disciplina} for p in profs]
        return render_template("professores.html", professores=profs_out)
    finally:
        db.close()


@professores_bp.route("/api", methods=["GET"])
def api_listar_professores():
    db = SessionLocal()
    try:
        profs = db.query(Professor).order_by(Professor.id).all()
        return jsonify([{'id': p.id, 'nome': p.nome, 'disciplina': p.disciplina} for p in profs])
    finally:
        db.close()


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

    db = SessionLocal()
    try:
        p = Professor(nome=data.get('nome'), disciplina=data.get('disciplina'))
        db.add(p)
        db.commit()
        db.refresh(p)
        return jsonify({"mensagem": "Criado", "id": p.id}), 201
    finally:
        db.close()


@professores_bp.route("/api/<int:id>", methods=["PUT"])
def api_atualizar_professor(id):
    data = request.json
    err = _validar_professor_payload(data)
    if err:
        return jsonify({"erro": err}), 400

    db = SessionLocal()
    try:
        p = db.get(Professor, id)
        if not p:
            return jsonify({"erro": "Professor não encontrado"}), 404
        p.nome = data.get('nome')
        p.disciplina = data.get('disciplina')
        db.commit()
        return jsonify({"mensagem": "Atualizado"})
    finally:
        db.close()


@professores_bp.route("/api/<int:id>", methods=["DELETE"])
def api_deletar_professor(id):
    db = SessionLocal()
    try:
        p = db.get(Professor, id)
        if not p:
            return jsonify({"erro": "Professor não encontrado"}), 404
        db.delete(p)
        db.commit()
        return jsonify({"mensagem": "Deletado"})
    finally:
        db.close()
