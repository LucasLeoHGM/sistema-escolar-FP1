from flask import Blueprint, render_template
from database import SessionLocal
from models import Turma
from sqlalchemy.exc import OperationalError

relatorios_bp = Blueprint("relatorios", __name__)


@relatorios_bp.route("/relatorios/alunos-por-turma")
def alunos_por_turma():
    try:
        db = SessionLocal()
    except OperationalError as e:
        return render_template("relatorio_alunos_por_turma.html", dados=[], db_error=str(e))

    try:
        turmas = db.query(Turma).order_by(Turma.id).all()
        dados = []
        for t in turmas:
            alunos = [{'id': a.id, 'nome': a.nome, 'idade': a.idade} for a in t.alunos]
            dados.append({
                'id': t.id,
                'nome_turma': t.nome,
                'sala': t.sala,
                'alunos': alunos
            })
        return render_template("relatorio_alunos_por_turma.html", dados=dados)
    finally:
        db.close()
