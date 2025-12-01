import os
from flask import Flask, render_template, request, jsonify
from sqlalchemy.exc import OperationalError
from routes.alunos import alunos_bp
from routes.professores import professores_bp
from routes.turmas import turmas_bp
from routes.relatorios import relatorios_bp

app = Flask(__name__)

app.register_blueprint(alunos_bp)
app.register_blueprint(professores_bp)
app.register_blueprint(turmas_bp)
app.register_blueprint(relatorios_bp)


@app.errorhandler(OperationalError)
def handle_db_error(err):
    # For API endpoints, return JSON 503; for pages, render a message
    if request.path.startswith('/api') or request.path.startswith('/alunos/api') or request.path.startswith('/professores/api') or request.path.startswith('/turmas/api'):
        return jsonify({"erro": "Banco de dados indisponível"}), 503
    return render_template('base.html', db_error=str(err)), 503


@app.context_processor
def inject_flags():
    # expose a flag to templates so the UI can show/hide dev-only controls
    seed_flag = os.getenv('ALLOW_SEED', '').lower() in ('1', 'true', 'yes') or os.getenv('FLASK_DEBUG', '').lower() in ('1', 'true', 'yes')
    return dict(seed_allowed=seed_flag)

@app.route("/")
def home():
    return render_template("base.html")

if __name__ == "__main__":
    # Ensure SQLAlchemy models/tables are created at startup
    from database import init_db
    try:
        init_db()
    except Exception as e:
        # Print the error to help debugging during development
        print("init_db() failed:", e)

    # Respect environment variable for debug mode (safer than hardcoding)
    debug_flag = os.getenv("FLASK_DEBUG", os.getenv("DEBUG", "False")).lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", debug=debug_flag)
