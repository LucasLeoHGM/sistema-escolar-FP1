import os
from flask import Flask, render_template
from routes.alunos import alunos_bp
from routes.professores import professores_bp
from routes.turmas import turmas_bp
from routes.relatorios import relatorios_bp

app = Flask(__name__)

app.register_blueprint(alunos_bp)
app.register_blueprint(professores_bp)
app.register_blueprint(turmas_bp)
app.register_blueprint(relatorios_bp)

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
