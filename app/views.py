from app.navigation import setup_nav
from flask import Blueprint, render_template


from gamesummary import calls, models

import constants
import ast

mod = Blueprint('app', __name__)


@mod.route("/")
def index():
    rd = setup_nav()
    teamDict = constants.teamDict
    teamDict["Atlanta Thrashers"] = "ATL"

    search = []
    for team in teamDict:
        line = [team, teamDict[team]]
        search.append(line)

    players = models.RosterMaster.query.all()
    count = 0
    for player in players:
        count += 1
        line = [player.FullName, player.__dict__["PlayerId"]]
        search.append(line)

    games = calls.get_r_games()
    #games = calls.get_games()
    return render_template("index.html", rd=rd,
        games=games,
        search=search)


@mod.route("/r/<string:pagename>/")
def iframe_woi(pagename):
    rd = setup_nav()
    print pagename
    return render_template("woi-frame.html", page=pagename, rd=rd,
        url="http://biscuit.war-on-ice.com/" + pagename)


@mod.route("/glossary/")
def glossary():
    rd = setup_nav()
    tf = open("html/glossary_text.txt")
    tf = tf.read().decode('utf-8')
    text = ast.literal_eval(tf)
    return render_template("misc/glossary.html", rd = rd,
        text=text)


@mod.route("/about/")
def about():
    rd = setup_nav()
    return render_template("misc/about.html", rd = rd)