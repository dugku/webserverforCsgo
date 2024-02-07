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
    id = db.Column(db.Integer, primary_key=True)
    econTeamA = db.Column(db.Integer)
    scoreA = db.Column(db.Integer)
    scoreB = db.Column(db.Integer)
    econTeamB = db.Column(db.Integer)
    bombPlanted = db.Column(db.Boolean)
    playerPlanted = db.Column(db.String(25))
    typeOfBuyTeamA = db.Column(db.String(15))
    typeofBuyTeamB = db.Column(db.String(15))
    WhatMatch = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable = False)

class playerScoreMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steamId = db.Column(db.Integer, unique = True)
    impact = db.Column(db.Float)
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

@app.route("/MatchData", methods=["POST"])
def get_match():

    Math_json = request.get_json()

    new_match = Matches(
        Map=Math_json["Map"], 
        TeamsPlayed=Math_json["WhovsWho"]
    )

    new_round = Rounds(
        econTeamA = Math_json.Rounds.EconA,
        econTeamB = Math_json.Rounds["EconB"],
        bombPlanted = Math_json.Rounds["BombPlanted"],
        #playerPlanted = Math_json["PLayer"]
        typeOfBuyTeamA = Math_json.Rounds["TypeofBuyA"],
        typeofBuyTeamB = Math_json.Rounds["TypeofBuyB"],
        scoreA = Math_json.Rounds["ScoreA"],
        scoreB = Math_json.Rounds["ScoreB"],
    )

    new_round.match = new_round
    print(new_match)
    print(new_round)


    return jsonify(Math_json)

if __name__ == "__main__":
    app.run(debug=True)