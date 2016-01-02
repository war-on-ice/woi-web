from flask import Blueprint, request

from app import app, Base, constants, filters
from flask import render_template
from sqlalchemy import desc, or_
from app.navigation import setup_nav

from models import TeamRun, GoalieRun, PlayerRun, RosterMaster, GamesTest, PlayByPlay
from calls import get_r_games, get_r_seasons
from forms import GameSummaryForm, SeriesSummaryForm

import math

from helper import get_rdata
from helpers import add2team
from app.helpers import percent

mod = Blueprint('game', __name__, url_prefix='/game')


@mod.route('/')
def show_games():
    rd = setup_nav()
    games = get_r_games()
    return render_template('game/games.html',
        rd=rd,
        games=games,
        teamname=filters.teamname)

@mod.route('/series/', methods=["GET", "POST"])
def show_series():
    rd = setup_nav()
    form = SeriesSummaryForm(request.form)
    teamgames = get_r_seasons()
    form.season.choices = [(x, str(x)[0:4] + "-" + str(x)[4:]) for x in sorted(teamgames.keys(), reverse=True)]

    if request.method == "POST":
        period = constants.periods_options[form.period.data]["value"]
    else:
        period = [0]
        period.extend(constants.periods_options[constants.periods["default"]]["value"])

    tablecolumns = form.tablecolumns.data

    # Find games where these teams faced each other
    games = GamesTest.query.filter(GamesTest.season==form.season.data, or_(GamesTest.hometeam==form.team1.data, GamesTest.hometeam==form.team2.data),
        or_(GamesTest.awayteam==form.team1.data, GamesTest.awayteam==form.team2.data))
    gcodes = set()
    for game in games:
        gcodes.add(game.gcode)

    gamedata = []
    teams = []
    goalies = []

    skip = ["period", "home", "Opponent", "gamestate", "gcode", "Team", "TOI", "Gm", "ID"]

    gamefound = set()
    foundplayers = set()
    goaliefound = set()
    playerfound = set()
    away = []
    home = []
    allplayers = []
    playerteams = {}
    players = set()
    coplayers = {}
    for gcode in gcodes:
        rdata = get_rdata("http://data.war-on-ice.net/games/" + str(form.season.data) + str(gcode) + ".RData")
        rteamrun = rdata["teamrun"]
        for play in rdata["coplayer"]:
            ckey = play["p1"] + "|" + play["p2"]
            if ckey not in coplayers:
                coplayers[ckey] = play
            else:
                for key in play:
                    if key not in ["p1", "p2"]:
                        coplayers[ckey][key] += play[key]
        for tr in sorted(rteamrun, key=lambda x: x["TOI"], reverse=True):
            gid = str(tr["gcode"]) + str(tr["season"]) + str(tr["Team"])
            if tr["period"] in period and int(tr["gamestate"]) == int(form.teamstrengths.data) and gid not in gamefound:
                gamefound.add(gid)
                ar = None
                for team in teams:
                    if team["Team"] == tr["Team"]:
                        ar = team
                        break
                if ar is None:
                    tr["MSF"] = int(tr["FF"]) - int(tr["SF"])
                    tr["BSF"] = tr["CF"] - tr["MSF"] - tr["SF"]
                    teams.append(tr)
                else:
                    for key in tr:
                        if key not in skip:
                            ar[key] += tr[key]
                    ar["MSF"] += int(tr["FF"]) - int(tr["SF"])
                    ar["BSF"] += tr["CF"] - (int(tr["FF"]) - int(tr["SF"])) - tr["SF"]
                    ar["TOI"] += float(tr["TOI"])
        rgoalies = rdata["goalierun"]
        for tr in sorted(rgoalies, key=lambda x: x["TOI"], reverse=True):
            gid = str(tr["gcode"]) + str(tr["season"]) + str(tr["Team"]) + str(tr["ID"])
            if tr["period"] in period and tr["gamestate"] == int(form.teamstrengths.data) and gid not in goaliefound:
                goaliefound.add(gid)
                ar = None
                for goalie in goalies:
                    if goalie["ID"] == tr["ID"] and goalie["Team"] == tr["Team"]:
                        ar = goalie
                        break
                if ar is None:
                    tr["gu"] = tr["goals.0"]
                    tr["su"] = tr["shots.0"]
                    tr["gl"] = tr["goals.1"]
                    tr["sl"] = tr["shots.1"]
                    tr["gm"] = tr["goals.2"]
                    tr["sm"] = tr["shots.2"]
                    tr["gh"] = tr["goals.3"] + tr["goals.4"]
                    tr["sh"] = tr["shots.3"] + tr["shots.4"]
                    tr["TOI"] = float(tr["TOI"]) # round(float(tr["TOI"]) / 60.0, 1)
                    tr["Gm"] = 1
                    goalies.append(tr)
                    foundplayers.add(tr["ID"])
                else:
                    ar["gu"] += tr["goals.0"]
                    ar["su"] += tr["shots.0"]
                    ar["gl"] += tr["goals.1"]
                    ar["sl"] += tr["shots.1"]
                    ar["gm"] += tr["goals.2"]
                    ar["sm"] += tr["shots.2"]
                    ar["gh"] += tr["goals.3"] + tr["goals.4"]
                    ar["sh"] += tr["shots.3"] + tr["shots.4"]
                    ar["TOI"] += float(tr["TOI"])  #round(float(tr["TOI"]) / 60.0, 1)
                    ar["Gm"] += 1
        rplayerrun = rdata["playerrun"]
        for tr in sorted(rplayerrun, key=lambda x: x["TOI"], reverse=True):
            if tr["ID"] not in foundplayers:
                foundplayers.add(tr["ID"])
            gid = str(tr["gcode"]) + str(tr["season"]) + str(tr["Team"]) + str(tr["ID"])
            if tr["period"] in period and tr["gamestate"] == int(form.teamstrengths.data) and gid not in playerfound:
                playerfound.add(gid)
                players.add(tr["ID"])
                ar = None
                pteam = None
                for p in allplayers:
                    if p["ID"] == tr["ID"]:
                        ar = p
                        break
                if ar is None:
                    tr["G"] = int(tr["GOAL1"] + tr["GOAL2"] + tr["GOAL3"] + tr["GOAL4"])
                    tr["TOI"] = float(tr["TOI"]) # round(float(tr["TOI"]) / 60.0, 1)
                    tr["Gm"] = 1
                    allplayers.append(tr)
                    playerteams[tr["ID"]] = tr["Team"]
                else:
                    for key in tr:
                        if key not in skip:
                            ar[key] += tr[key]
                    ar["G"] += int(tr["GOAL1"] + tr["GOAL2"] + tr["GOAL3"] + tr["GOAL4"])
                    ar["TOI"] += float(tr["TOI"]) # round(float(tr["TOI"]) / 60.0, 1)
                    ar["Gm"] += 1

    ht = None
    at = None
    for player in allplayers:
        if ht is None:
            home.append(player)
            ht = player["Team"]
        elif ht == player["Team"]:
            home.append(player)
        elif at == None:
            away.append(player)
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

    coplayerlist = []
    coplayerdict = {}
    coplayerlinks = []
    hometeam = None
    awayteam = None
    for co in coplayers:
        matchup = coplayers[co]
        # Define each "Node" (player), and assign a value to them
        for p in ["p1", "p2"]:
            team = 0
            if matchup[p] not in coplayerdict:
                if hometeam is None:
                    hometeam = playerteams[matchup[p]]
                elif awayteam is None and hometeam != playerteams[matchup[p]]:
                    awayteam = playerteams[matchup[p]]
                if playerteams[matchup[p]] == hometeam:
                    team = 1
                coplayerlist.append({"name": matchup[p], "team": playerteams[matchup[p]], "rname": str(woiid[matchup[p]]["full_name"]), "group": team})
                coplayerdict[matchup[p]] = len(coplayerlist) - 1
        # Then create a link between these two with the corresponding values
        link = {}
        link["source"] = coplayerdict[matchup["p1"]]
        link["target"] = coplayerdict[matchup["p2"]]
        link["sourcename"] = matchup["p1"]
        link["targetname"] = matchup["p2"]
        link["TOI"] = matchup["el2"]
        link["evf"] = matchup["evf"]
        link["eva"] = matchup["eva"]
        link["cf%"] = percent(matchup["evf"], matchup["eva"])
        coplayerlinks.append(link)

    # Set up the 4 arrays for the co occurrency
    hvh = {"nodes": coplayerlist, "links": coplayerlinks}

    return render_template("game/series.html",
        rd=rd,
        hvh=hvh,
        form=form,
        home=home,
        away=away,
        woiid=woiid,
        teamrun=teams,
        goalies=goalies,
        gamedata=gamedata,
        coplayers=coplayers,
        tablecolumns=int(tablecolumns))


@mod.route('/<gameId>/tables', methods=['GET'])
def show_game_summary_tables(gameId):
    rd = setup_nav()

    if request.method == "GET":
        tablecolumns = request.args.get("tablecolumns")
        teamstrengths = request.args.get("teamstrengths")
        scoresituations = request.args.get("scoresituation")
        period = constants.periods_options[request.args.get("period")]["value"]
    else:
        tablecolumns = "0"
        teamstrengths = constants.strength_situations_dict[constants.strength_situations["default"]]["value"]
        scoresituations = constants.score_situations_dict[constants.score_situations["default"]]["value"]
        period = [0]
        period.extend(constants.periods_options[constants.periods["default"]]["value"])

    # Get game information from URL
    season = gameId[0:8]
    gcode = gameId[8:]
    
    # Prepare form results for queries
    scorediffcat = int(scoresituations)
    gamestate = int(teamstrengths)
    period = [int(x) for x in period]

    rdata = get_rdata("http://data.war-on-ice.net/games/" + season + gcode + ".RData")

    
    rteamrun = rdata["teamrun"]
    teamrun = []
    teams = set()
    for tr in sorted(rteamrun, key=lambda x: x["TOI"], reverse=True):
        if tr["period"] in period and tr["gamestate"] == gamestate:
            if tr["Team"] not in teams:
                tr["MSF"] = int(tr["FF"]) - int(tr["SF"])
                tr["BSF"] = tr["CF"] - tr["MSF"] - tr["SF"]
                tr["TOI"] = float(tr["TOI"]) # round(float(tr["TOI"]) / 60.0, 1)
                teamrun.append(tr)
                teams.add(tr["Team"])
    goalies = []
    rgoalies = rdata["goalierun"]
    teams = set()
    foundplayers = set()
    for tr in sorted(rgoalies, key=lambda x: x["TOI"], reverse=True):
        if tr["period"] in period and tr["gamestate"] == gamestate:
            if tr["ID"] not in foundplayers:
                tr["gu"] = tr["goals.0"]
                tr["su"] = tr["shots.0"]
                tr["gl"] = tr["goals.1"]
                tr["sl"] = tr["shots.1"]
                tr["gm"] = tr["goals.2"]
                tr["sm"] = tr["shots.2"]
                tr["gh"] = tr["goals.3"] + tr["goals.4"]
                tr["sh"] = tr["shots.3"] + tr["shots.4"]
                tr["TOI"] = float(tr["TOI"]) # round(float(tr["TOI"]) / 60.0, 1)
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
            tr["TOI"] = float(tr["TOI"]) #round(float(tr["TOI"]) / 60.0, 1)
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

    return render_template('game/gamesummarytables.html',
        tablecolumns=int(tablecolumns),
        home=home,
        away=away,
        gamedata=gamedata,
        goalies=goalies,
        woiid=woiid,
        teamrun=teamrun)

@mod.route('/<gameId>/header')
def show_game_summary_header(gameId):
    rd = setup_nav()
    season = gameId[0:8]
    gcode = gameId[8:]
    # Get GamesTest information
    gamedata = GamesTest.query.filter_by(season=season,
        gcode=int(gcode)).first()
    return render_template('game/gamesummaryheader.html',
        gamedata=gamedata)


@mod.route('/<gameId>/', methods=['GET', 'POST'])
def show_game_summary(gameId):

    # Get game information from URL
    season = gameId[0:8]
    gcode = gameId[8:]

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
    
    # Prepare form results for queries
    scorediffcat = int(scoresituations)
    gamestate = int(teamstrengths)
    period = [int(x) for x in period]

    # Setup nav
    rd = setup_nav()

    # Get GamesTest information
    gamedata = GamesTest.query.filter_by(season=season,
        gcode=int(gcode)).first()

    if gamedata.status == 3:
        live = False
    else:
        live = True

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
                           live=live)
