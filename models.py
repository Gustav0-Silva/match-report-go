from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Jogador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    nascimento = db.Column(db.String(20))
    posicao = db.Column(db.String(50))

class Partida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adversario = db.Column(db.String(100))
    data = db.Column(db.String(20))

class Estatistica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jogador_id = db.Column(db.Integer, db.ForeignKey('jogador.id'))
    evento = db.Column(db.String(50))  # gol, assistência, falta etc.
    tempo = db.Column(db.String(10))   # 1T ou 2T
