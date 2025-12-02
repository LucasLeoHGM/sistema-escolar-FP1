from flask import Blueprint, render_template
from config import get_connection
import psycopg2

relatorios_bp = Blueprint("relatorios", __name__)

@relatorios_bp.route("/relatorios/alunos-por-turma")
def alunos_por_turma():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, nome, sala 
            FROM turmas
            ORDER BY id;
        """)
        turmas = cur.fetchall()

        dados = []

        for turma in turmas:
            turma_id = turma[0]

            cur.execute("""
                SELECT id, nome, idade
                FROM alunos
                WHERE turma_id = %s;
            """, (turma_id,))

            alunos = cur.fetchall()

            dados.append({
                "id": turma_id,
                "nome_turma": turma[1],
                "sala": turma[2],
                "alunos": [{"id": a[0], "nome": a[1], "idade": a[2]} for a in alunos]
            })

        return render_template("relatorio_alunos_por_turma.html", dados=dados)

    except Exception as e:
        return f"Erro ao gerar relatório: {e}", 500
