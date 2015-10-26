from flask import Blueprint

from datetime import date

from app import constants
from app import app, Base
from flask import render_template
from sqlalchemy import desc
from app.navigation import setup_nav
from app import constants

from models import TeamRun, GoalieRun, PlayerRun, RosterMaster

import math

mod = Blueprint('game', __name__, url_prefix='/game')


@mod.route('/')
def show_games():
    rd = setup_nav()
    cy = date.today().year
    print(cy)
    #games = TeamRun.objects.filter()
    return render_tempalte('game/games.html')

@mod.route('/<gameId>/')
def show_game_summary(gameId):
    rd = setup_nav()
    season = gameId[0:8]
    gcode = gameId[8:]
    scorediffcat = constants.score_situations_dict["All"]["value"]
    gamestate = constants.strength_situations_dict["Even strength 5v5"]["value"]
    teamruns = TeamRun.query.filter_by(season=season,
        gcode=int(gcode),
        scorediffcat=scorediffcat,
        gamestate=gamestate).order_by(TeamRun.TOI).all()
    teamruns = teamruns[-2:]
    teamsummaries = []
    for td in teamruns:
        team = {}
        team["team"] = td.Team
        team["gf"] = int(td.GF)
        team["sf"] = int(td.SF)
        team["msf"] = int(td.FF) - int(td.SF)
        team["cf"] = int(td.CF)
        team["bsf"] = team["cf"] - team["msf"] - team["sf"]
        team["scf"] = int(td.SCF)
        team["hscf"] = int(td.sSCF)
        team["zso"] = int(td.ZSO)
        team["hit"] = int(td.HIT)
        team["pn"] = int(td.PENL_TAKEN)
        team["fo_w"] = int(td.FAC_WIN)
        team["toi"] = round(float(td.TOI) / 60.0, 1)
        teamsummaries.append(team)

    goalieruns = GoalieRun.query.filter_by(season=season,
        gcode=int(gcode),
        scorediffcat=scorediffcat,
        gamestate=gamestate).order_by(GoalieRun.TOI).all()
    goalies = []
    foundgoalies = set()
    for td in reversed(goalieruns):
        if td.ID not in foundgoalies:
            foundgoalies.add(td.ID)
            goalie = {}
            goalie["name"] = td.ID
            goalie["team"] = td.Team
            goalie["gu"] = td.__dict__["goals.0"]
            goalie["su"] = td.__dict__["shots.0"]
            goalie["gl"] = td.__dict__["goals.1"]
            goalie["sl"] = td.__dict__["shots.1"]
            goalie["gm"] = td.__dict__["goals.2"]
            goalie["sm"] = td.__dict__["shots.2"]
            goalie["gh"] = td.__dict__["goals.3"] + td.__dict__["goals.4"]
            goalie["sh"] = td.__dict__["shots.3"] + td.__dict__["shots.4"]
            goalie["toi"] = round(float(td.TOI) / 60.0, 1)
            goalies.append(goalie)

    playerruns = PlayerRun.query.filter_by(season=season,
        gcode=int(gcode),
        scorediffcat=scorediffcat,
        gamestate=gamestate).order_by(PlayerRun.TOI).all()
    foundplayers = set()
    away = []
    home = []
    for td in reversed(playerruns):
        if td.ID not in foundplayers:
            foundplayers.add(td.ID)
            player = {}
            player["name"] = td.ID
            player["g"] = int(td.GOAL1 + td.GOAL2 + td.GOAL3 + td.GOAL4)
            player["a1"] = int(td.ASSIST)
            player["a2"] = int(td.ASSIST_2)
            player["p"] = player["g"] + player["a1"] + player["a2"]
            player["ihsc"] = int(td.isSC)
            player["isc"] = int(td.iSC)
            player["icf"] = int(td.SHOT + td.SHOT1 + td.SHOT2 + td.SHOT3 + td.SHOT4)
            player["cplusminus"] = int(td.CF - td.CA)
            player["fplusminus"] = int(td.FF - td.FA)
            player["gplusminus"] = int(td.GF - td.GA)
            player["cf"] = int(td.CF)
            player["ff"] = int(td.FF)
            player["zso"] = int(td.ZSO)
            player["zsd"] = int(td.ZSD)
            player["ab"] = int(td.BLOCKED_SHOT + td.BLOCKED_SHOT1 + td.BLOCKED_SHOT2 + td.BLOCKED_SHOT3 + td.BLOCKED_SHOT4)
            player["fo_w"] = int(td.FAC_WIN)
            player["fo_l"] = int(td.FAC_LOSE)
            player["hit"] = int(td.HIT)
            player["hitminus"] = int(td.HIT_TAKEN)
            player["pn"] = int(td.PENL_TAKEN)
            player["pnminus"] = int(td.PENL_DRAWN)
            player["toi"] = round(float(td.TOI) / 60.0, 1)
            if td.home == 1:
                home.append(player)
            else:
                away.append(player)

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

    for a in away:
        print woiid[str(a["name"])]

    return render_template('game/gamesummary.html',
                           gameId = gameId,
                           strength_situations = constants.strength_situations,
                           score_situations = constants.score_situations,
                           periods = constants.periods,
                           rd = rd,
                           teamruns = teamsummaries,
                           goalies = goalies,
                           away = away,
                           home = home,
                           woiid = woiid,
                           rostermaster = rostermaster)
