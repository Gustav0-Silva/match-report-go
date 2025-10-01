from flask import Flask, render_template, request, redirect, url_for
from models import db, Jogador, Partida, Estatistica
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

# -------------------- ROTAS ---------------------

@app.route("/")
def index():
    partidas = Partida.query.all()
    return render_template("index.html", partidas=partidas)

# ---- Plantel de Jogadores ----

jogadores = []

@app.route("/plantel")
def plantel():
    jogadores = Jogador.query.all()  # pega todos os jogadores
    return render_template('plantel.html', jogadores=jogadores)

@app.route("/add_jogador", methods=["GET", "POST"])
def add_jogador():
    if request.method == "POST":
        nome = request.form.get("nome")
        posicao = request.form.get("posicao")
        numero = request.form.get("numero")

        if nome and posicao and numero:
            novo = Jogador(nome=nome, posicao=posicao, numero=numero)
            db.session.add(novo)
            db.session.commit()
            return redirect(url_for("plantel"))
    return render_template("add_jogador.html")

@app.route('/delete_jogador/<int:index>', methods=['POST', 'GET'])
def delete_jogador(index):
    jogador = Jogador.query.get_or_404(index)  # pega o jogador pelo id
    db.session.delete(jogador)
    db.session.commit()
    return redirect(url_for('plantel'))  # volta para a página do plantel

# ---- Iniciar Partida ----
@app.route("/sumula", methods=["GET", "POST"])
def sumula():
    jogadores = Jogador.query.all()

    if request.method == "POST":
        time_adversario = request.form.get("time_adversario")
        data = datetime.now().strftime("%d/%m/%Y")

        partida = Partida(time_adversario=time_adversario, data=data)
        db.session.add(partida)
        db.session.commit()

        for jogador in jogadores:
            estat = Estatistica(
                jogador_id=jogador.id,
                partida_id=partida.id,
                gol_marcado=int(request.form.get(f"gol_marcado_{jogador.id}", 0)),
                gol_sofrido=int(request.form.get(f"gol_sofrido_{jogador.id}", 0)),
                gol_contra=int(request.form.get(f"gol_contra_{jogador.id}", 0)),
                assistencia=int(request.form.get(f"assistencia_{jogador.id}", 0)),
                falta_feita=int(request.form.get(f"falta_feita_{jogador.id}", 0)),
                falta_sofrida=int(request.form.get(f"falta_sofrida_{jogador.id}", 0)),
                cartao_amarelo=int(request.form.get(f"cartao_amarelo_{jogador.id}", 0)),
                cartao_vermelho=int(request.form.get(f"cartao_vermelho_{jogador.id}", 0)),
            )
            db.session.add(estat)

        db.session.commit()
        return redirect(url_for("historico"))

    return render_template("sumula.html", jogadores=jogadores)

# ---- Histórico ----
@app.route("/historico")
def historico():
    partidas = Partida.query.all()
    return render_template("historico.html", partidas=partidas)

# ---- Estatística e Histórico (em branco por enquanto) ----
@app.route("/estatistica")
def estatistica():
    return "<h2>Em construção...</h2>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
