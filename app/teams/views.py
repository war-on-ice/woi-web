from flask import Blueprint, request

from app import app, Base, constants, filters
from flask import render_template
from sqlalchemy import desc
from app.navigation import setup_nav

from helper import get_rdata
from forms import SeasonSelectForm

import datetime
import urllib2

mod = Blueprint('team', __name__, url_prefix='/team')


@mod.route("byteam/")
def show_by_team():
    rd = setup_nav()
    return render_template("teams/team.html",
        rd=rd)


@mod.route('/', methods=["GET", "POST"])
def show_team_standings():
    rd = setup_nav()
    rdata = get_rdata("http://data.war-on-ice.net/nhlscrapr-core.RData")
    teamgames = {}
    for game in rdata["games"]:
        if game["season"] not in teamgames:
            teamgames[game["season"]] = []
        teamgames[game["season"]].append(game)
    seasongames = {}
    # Determine season(s) to get information from
    form = SeasonSelectForm(request.form)
    form.seasons.choices = [(x, str(x)[0:4] + "-" + str(x)[4:]) for x in sorted(teamgames.keys(), reverse=True)]
    try:
        form.seasons.data = [int(x) for x in form.seasons.data]
    except:
        pass
    allseasons = [(x, str(x)[0:4] + "-" + str(x)[4:]) for x in sorted(teamgames.keys(), reverse=True)]
    if request.method == "POST" and form.validate():
        seasons = [int(x) for x in form.seasons.data]
    else:
        smax = max(teamgames.keys())
        seasons = [smax, ]
    for season in seasons:
        for team in teamgames[season]:
            hometeam = team["hometeam"]
            awayteam = team["awayteam"]
            if hometeam != "" and awayteam != "":
                if hometeam not in seasongames:
                    seasongames[hometeam] = {}
                if awayteam not in seasongames:
                    seasongames[awayteam] = {}
                if team["status"] != 1 and team["status"] != 4:
                    if "Gm" not in seasongames[hometeam]:
                        seasongames[hometeam] = prepare_team()
                    if "Gm" not in seasongames[awayteam]:
                        seasongames[awayteam] = prepare_team()
                    seasongames[hometeam]["Gm"] += 1
                    seasongames[awayteam]["Gm"] += 1
                    seasongames[hometeam]["GF"] += team["homescore"]
                    seasongames[hometeam]["GA"] += team["awayscore"]
                    seasongames[awayteam]["GF"] += team["awayscore"]
                    seasongames[awayteam]["GA"] += team["homescore"]
                    seasongames[hometeam]["CF"] += team["homecorsi"]
                    seasongames[hometeam]["CA"] += team["awaycorsi"]
                    seasongames[awayteam]["CF"] += team["awaycorsi"]
                    seasongames[hometeam]["CA"] += team["homecorsi"]
                    # Determine winner, if game is still not going on
                    if team["status"] != 2:
                        if team["homescore"] > team["awayscore"]:
                            winner = hometeam
                            loser = awayteam
                        elif team["awayscore"] > team["homescore"]:
                            winner = awayteam
                            loser = hometeam
                        if team["periods"] == 3:
                            seasongames[winner]["RW"] += 1
                            seasongames[loser]["RL"] += 1
                            seasongames[winner]["PNow"] += 2
                            seasongames[winner]["P3"] += 3
                            seasongames[winner]["PTie"] += 2
                            seasongames[winner]["PNL"] += 2
                        elif team["periods"] == 4:
                            seasongames[winner]["OW"] += 1
                            seasongames[loser]["OL"] += 1
                            seasongames[winner]["PNow"] += 2
                            seasongames[loser]["PNow"] += 1
                            seasongames[winner]["P3"] += 2
                            seasongames[loser]["P3"] += 1
                            seasongames[winner]["PTie"] += 2
                            seasongames[loser]["PTie"] += 1
                            seasongames[winner]["PNL"] += 2
                        elif team["periods"] == 5:
                            seasongames[winner]["SW"] += 1
                            seasongames[loser]["SL"] += 1
                            seasongames[winner]["PNow"] += 2
                            seasongames[loser]["PNow"] += 1
                            seasongames[winner]["P3"] += 2
                            seasongames[loser]["P3"] += 1
                            seasongames[winner]["PTie"] += 1
                            seasongames[loser]["PTie"] += 1
                            seasongames[winner]["PNL"] += 2
    return render_template('teams/teams.html',
        rd=rd,
        seasongames=seasongames,
        form=form,
        allseasons=allseasons,
        seasons=seasons)


def prepare_team():
    keys = ["Gm", "RW", "OW", "SW", "RL", "OL", "SL", "GF", "GA", "CF", "CA", "PNow", "P3", "PTie", "PNL"]
    dic = {}
    for key in keys:
        dic[key] = 0
    return dic
