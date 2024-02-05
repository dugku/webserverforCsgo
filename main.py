from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///csgoMatches.db'
db = SQLAlchemy(app)

class Matches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Map = db.Column(db.String(35))
    TeamsPlayed = db.Column(db.String(40))
    roundsPlayed = db.relationship('Rounds', backref='match',  lazy=True)
    playerscoreboard = db.relationship('playerScoreMatch', backref='match' ,lazy=True)

class Rounds(db.Model):
    econTeamA = db.Column(db.Integer)
    econTeamB = db.Column(db.Integer)
    bombPlanted = db.Column(db.Boolean)
    playerPlanted = db.Column(db.String(25))
    typeOfBuyTeamA = db.Column(db.String(15))
    typeofBuyTeamB = db.Column(db.String(15))
    WhatMatch = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable = False)

class playerScoreMatch(db.Model):
    steamId = db.Column(db.Integer, unique = True)
    userName = db.Column(db.String(30))
    kills = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    hs  = db.Column(db.Integer)
    hsPercent = db.Column(db.Float)
    adr = db.Column(db.Float)
    kast = db.Column(db.Float)
    kdratio = db.Column(db.Float)
    firstkill = db.Column(db.Integer)
    firstdeath  = db.Column(db.Integer)
    round2k = db.Column(db.Integer)
    round3k = db.Column(db.Integer)
    round4k = db.Column(db.Integer)
    round5k = db.Column(db.Integer)
    totaldmg = db.Column(db.Integer)
    tradekills = db.Column(db.Integer)
    tradedeaths = db.Column(db.Integer)

class players(db.Model):
    pass

@app.route("/MatchData", methods=["POST"])
def get_match():

    Math_json = request.get_json()

    MapPlayed = Math_json["Map"]
   
    WhoPlayedWho = Math_json["WhoVsWho"]


    for i in Math_json["Rounds"]:

        if i["EconA"] == 0:
            continue

        EconA = i["EconA"]
        EconB = i["EconB"]
        TypeOfBuyA = i["TypeOfBuyA"]
        TypeOfBuyB = i["TypeOfBuyB"]

    return jsonify(Math_json)

if __name__ == "__main__":
    app.run(debug=True)