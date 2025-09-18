from flask import Flask, render_template, request, redirect, url_for
from models import db, Jogador, Partida, Estatistica

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# -------------------- ROTAS ---------------------

@app.route("/")
def index():
    return render_template("index.html")

# ---- Plantel de Jogadores ----
@app.route("/jogadores")
def jogadores():
    lista = Jogador.query.all()
    return render_template("jogadores.html", jogadores=lista)

@app.route("/jogadores/add", methods=["GET", "POST"])
def add_jogador():
    if request.method == "POST":
        nome = request.form["nome"]
        nascimento = request.form["nascimento"]
        posicao = request.form["posicao"]
        novo = Jogador(nome=nome, nascimento=nascimento, posicao=posicao)
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for("jogadores"))
    return render_template("jogador_form.html")

@app.route("/jogadores/delete/<int:id>")
def delete_jogador(id):
    j = Jogador.query.get(id)
    db.session.delete(j)
    db.session.commit()
    return redirect(url_for("jogadores"))

# ---- Iniciar Partida ----
@app.route("/sumula", methods=["GET", "POST"])
def sumula():
    jogadores = Jogador.query.all()
    if request.method == "POST":
        id_jogador = request.form["jogador_id"]
        evento = request.form["evento"]
        tempo = request.form["tempo"]

        estat = Estatistica(jogador_id=id_jogador, evento=evento, tempo=tempo)
        db.session.add(estat)
        db.session.commit()
        return redirect(url_for("sumula"))

    estatisticas = Estatistica.query.all()
    return render_template("sumula.html", jogadores=jogadores, estatisticas=estatisticas)

# ---- Estatística e Histórico (em branco por enquanto) ----
@app.route("/estatistica")
def estatistica():
    return "<h2>Em construção...</h2>"

@app.route("/historico")
def historico():
    return "<h2>Em construção...</h2>"

if __name__ == "__main__":
    app.run(debug=True)
