from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///csgoMatches.db'
db = SQLAlchemy(app)

class Matches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Map = db.Column(db.String(35))
    TeamsPlayed = db.Column(db.String(40))
    roundsPlayed = db.relationship('Rounds', back_populates='match',  lazy=True)
    playerscoreboard = db.relationship('playerScoreMatch',back_populates='match' ,lazy=True)

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
    sidewon = db.Column(db.String(25))
    teamAname = db.Column(db.String(30))
    teamBname = db.Column(db.String(30))
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    match = db.relationship('Matches', back_populates='roundsPlayed')

class WeaponKill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_score_id = db.Column(db.Integer, db.ForeignKey('player_score_match.id'))
    weapon_id = db.Column(db.Integer)
    kill_count = db.Column(db.Integer)

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
    weapon_kills = db.relationship('WeaponKill', backref='player_score', lazy=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    match = db.relationship("Matches", back_populates='playerscoreboard')

class playerOverallStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steamid = db.Column(db.Integer, unique=True)
    userName = db.Column(db.String(30))
    kills = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    hs = db.Column(db.Integer)
    hsPercent = db.Column(db.Float)
    adr = db.Column(db.Float)
    kast = db.Column(db.Float)
    kdRatio = db.Column(db.Float)
    FkDiff = db.Column(db.Integer)
    round2k = db.Column(db.Integer)
    round3k = db.Column(db.Integer)
    round4k = db.Column(db.Integer)
    round5k = db.Column(db.Integer)
    totalDmg = db.Column(db.Integer)
    tradeKills = db.Column(db.Integer)
    tradeDeaths = db.Column(db.Integer)
    ctKills = db.Column(db.Integer)
    tKills = db.Column(db.Integer)
    effectiveFlashes = db.Column(db.Integer)
    avgFlashDuration = db.Column(db.Integer)
    totalutilDmg = db.Column(db.Integer)
    avgKillsrnd = db.Column(db.Float)
    avgDeathrnd = db.Column(db.Float)
    avgAssistsrnd  = db.Column(db.Float)
    roundsSurvive = db.Column(db.Integer)
    roundTraded = db.Column(db.Integer)

@app.route("/MatchData", methods=["POST"])
def get_match():

    Math_json = request.get_json()

    new_match = Matches(
        Map=Math_json["Match"]['Map'], 
        TeamsPlayed=Math_json["Match"]['WhoVsWho']
    )


    rounds = Math_json["Match"]["Rounds"]

    for i in rounds:

        if i["ScoreA"] == 0 and i["ScoreB"] == 0:
            continue    
        new_round = Rounds(
        econTeamA = i["EconA"],
        econTeamB = i["EconB"],
        bombPlanted = i["BombPlanted"],
        typeOfBuyTeamA = i["TypeofBuyA"],
        typeofBuyTeamB = i["TypeofBuyB"],
        sidewon = i["SideWon"],
        teamAname = i["TeamNameA"],
        teamBname = i["TeamNameB"],
        scoreA = i["ScoreA"],
        scoreB = i["ScoreB"],

        )   
        new_round.match = new_match
        db.session.add(new_round)

    player = Math_json["Match"]["Players"]

    for i in player:
       new_player = playerScoreMatch (
            steamId = i,
            impact = player[i]["ImpactPerRnd"],
            userName = player[i]["UserName"],
            kills = player[i]["Kills"],
            deaths = player[i]["Deaths"],
            assists = player[i]["Assists"],
            hs  = player[i]["HS"],
            hsPercent = player[i]["HeadPercent"],
            adr = player[i]["ADR"],
            kast = player[i]["KAST"],
            kdratio = player[i]["KDRatio"],
            firstkill = player[i]["Firstkill"],
            firstdeath = player[i]["FirstDeath"],
            round2k = player[i]["Round2k"],
            round3k = player[i]["Round3k"],
            round4k = player[i]["Round4k"],
            round5k = player[i]["Round5k"],
            totaldmg = player[i]["Totaldmg"],
            tradekill = player[i]["TradeKills"],
            tradedeaths = player[i]["TradeDeath"],
        )
       new_player.match = new_match
       db.session.add(new_player)
    
    return jsonify(Math_json)

if __name__ == "__main__":
    app.run(debug=True)