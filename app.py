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
    app.run(debug=True)
