from flask import Blueprint, request

from app import app, Base, constants, filters
from flask import render_template
from sqlalchemy import desc
from app.navigation import setup_nav

from models import TeamRun, GoalieRun, PlayerRun, RosterMaster, GamesTest, PlayByPlay
from calls import get_games
from forms import GameSummaryForm

import math

import urllib2
from rpy2.robjects import r
from rpy2.robjects import pandas2ri
import pandas as pd

mod = Blueprint('game', __name__, url_prefix='/game')


@mod.route('/')
def show_games():
    rd = setup_nav()
    games = get_games()
    return render_template('game/games.html',
        rd=rd,
        games=games,
        teamname=filters.teamname)


@mod.route('/<gameId>/', methods=['GET', 'POST'])
def show_game_summary(gameId):
    # Get form results or default
    form = GameSummaryForm(request.form)
    if request.method == "POST" and form.validate():
        tablecolumns = form.tablecolumns.data
        teamstrengths = form.teamstrengths.data
        scoresituations = form.scoresituations.data
        period = constants.periods_options[form.period.data]["value"]
    else:
        tablecolumns = "0"
        teamstrengths = constants.strength_situations_dict[constants.strength_situations["default"]]["value"]
        scoresituations = constants.score_situations_dict[constants.score_situations["default"]]["value"]
        period = [0]
        period.extend(constants.periods_options[constants.periods["default"]]["value"])
    # Setup nav
    rd = setup_nav()
    # Get game information from URL
    season = gameId[0:8]
    gcode = gameId[8:]
    
    # Prepare form results for queries
    scorediffcat = int(scoresituations)
    gamestate = int(teamstrengths)
    period = [int(x) for x in period]

    # For testing, probably want to do this a different way in production TODO
    response = urllib2.urlopen("http://war-on-ice.com/data/games/" + season + gcode + ".RData")
    html = response.read()
    fp = open("rdata/2015201620001.RData", "w")
    fp.write(html)
    fp.close()
    robj = r.load("rdata/2015201620001.RData")

    rdata = {}
    keys = {}
    for sets in robj:
        myRData = pandas2ri.ri2py(r[sets])
        rdata[sets] = []
        keys[sets] = set()
        # convert to DataFrame
        if not isinstance(myRData, pd.DataFrame):
            myRData = pd.DataFrame(myRData)
        for element in myRData:
            keys[sets].add(element)
            counter = 0
            for value in myRData[element]:
                if counter >= len(rdata[sets]):
                    rdata[sets].append({})
                rdata[sets][counter][element] = value
                counter += 1
    rteamrun = rdata["teamrun"]
    teamrun = []
    teams = set()
    for tr in sorted(rteamrun, key=lambda x: x["TOI"], reverse=True):
        if tr["period"] in period and tr["gamestate"] == gamestate:
            if tr["Team"] not in teams:
                tr["MSF"] = int(tr["FF"]) - int(tr["SF"])
                tr["BSF"] = tr["CF"] - tr["MSF"] - tr["SF"]
                tr["TOI"] = round(float(tr["TOI"]) / 60.0, 1)
                teamrun.append(tr)
                teams.add(tr["Team"])
    goalies = []
    rgoalies = rdata["goalierun"]
    teams = set()
    foundplayers = set()
    for tr in sorted(rgoalies, key=lambda x: x["TOI"], reverse=True):
        if tr["period"] in period and tr["gamestate"] == gamestate:
            if tr["Team"] not in teams:
                tr["gu"] = tr["goals.0"]
                tr["su"] = tr["shots.0"]
                tr["gl"] = tr["goals.1"]
                tr["sl"] = tr["shots.1"]
                tr["gm"] = tr["goals.2"]
                tr["sm"] = tr["shots.2"]
                tr["gh"] = tr["goals.3"] + tr["goals.4"]
                tr["sh"] = tr["shots.3"] + tr["shots.4"]
                tr["TOI"] = round(float(tr["TOI"]) / 60.0, 1)
                goalies.append(tr)
                teams.add(tr["Team"])
                foundplayers.add(tr["ID"])

    rplayerrun = rdata["playerrun"]
    away = []
    home = []
    players = set()
    for tr in sorted(rplayerrun, key=lambda x: x["TOI"], reverse=True):
        if tr["ID"] not in foundplayers:
            foundplayers.add(tr["ID"])
        if tr["period"] in period and tr["gamestate"] == gamestate and tr["ID"] not in players:
            players.add(tr["ID"])
            tr["G"] = int(tr["GOAL1"] + tr["GOAL2"] + tr["GOAL3"] + tr["GOAL4"])
            tr["TOI"] = round(float(tr["TOI"]) / 60.0, 1)
            if tr["home"] == 1:
                home.append(tr)
            else:
                away.append(tr)


    # Get GamesTest information
    gamedata = GamesTest.query.filter_by(season=season,
        gcode=int(gcode)).first()

    rostermaster = {}
    rosterquery = RosterMaster.query.filter(Base.metadata.tables['rostermaster'].c["woi.id"].in_(foundplayers)).all()
    woiid = {}
    for p in rosterquery:
        player = {}
        player["woi.id"] = p.__dict__["woi.id"]
        player["pos"] = p.pos
        player["full_name"] = p.last.title() + ", " + p.first.title()
        rostermaster[p.numfirstlast] = player
        woiid[player["woi.id"]] = player

    return render_template('game/gamesummary.html',
                           tablecolumns=int(tablecolumns),
                           gameId=gameId,
                           strength_situations=constants.strength_situations,
                           score_situations=constants.score_situations,
                           periods=constants.periods,
                           rd=rd,
                           gamestate=gamestate,
                           period=period,
                           gamedata = gamedata,
                           form = form,
                           teamrun=teamrun,
                           goalies=goalies,
                           woiid=woiid,
                           away=away,
                           home=home)
