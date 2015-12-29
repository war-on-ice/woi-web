from __future__ import division
from flask import Blueprint, request

from flask import render_template
from sqlalchemy import desc

from app.navigation import setup_nav
from app.gamesummary.models import TeamRun
from app import app, Base, constants, filters, helpers
from app.gamesummary.calls import get_r_standings, get_r_seasons, compiled_teams

from forms import SeasonSelectForm, ComparisonForm, ComparisonGraphForm, HistoryForm, GameGraphForm

import datetime
import urllib2
import numpy as np
import math

mod = Blueprint('team', __name__, url_prefix='/team')


@mod.route("/byteam/")
def show_by_team():
    rd = setup_nav()
    return render_template("teams/team.html",
        rd=rd)


@mod.route('/', methods=["GET", "POST"])
def show_team_standings():
    rd = setup_nav()
    # Determine season(s) to get information from
    teamgames = get_r_seasons()
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
    seasongames = get_r_standings(teamgames, seasons=seasons)

    return render_template('teams/teams.html',
        rd=rd,
        seasongames=seasongames,
        form=form,
        allseasons=allseasons,
        seasons=seasons)


@mod.route("/history/", methods=["GET", "POST"])
def show_team_history():
    rd = setup_nav()
    form = HistoryForm(request.form, prefix="form")
    cpg = ComparisonGraphForm()
    ggf = GameGraphForm(request.form, prefix="game-form")
    cpg.xaxis.data = "season"
    now = datetime.datetime.now().date()
    if request.method == "POST" and form.validate():
        pass
    else:
        form.endingDate.data = now
        form.startingDate.data = datetime.datetime.strptime("2002-10-01", "%Y-%m-%d").date()

    startingDate = form.startingDate.data
    endingDate = form.endingDate.data
    team = form.filterTeams.data
    columns = form.tablecolumns.data
    regularplayoffs = form.regularplayoffs.data

    # Filter teamrun based on form data
    teamstrengths = int(form.teamstrengths.data)
    if teamstrengths == 7:
        teamstrengths = [constants.strength_situations_dict[x]["value"] for x in constants.strength_situations_dict]
    else:
        teamstrengths = [teamstrengths, ]
    scoresituations = int(form.scoresituations.data)
    if scoresituations == 7:
        scoresituations = [constants.score_situations_dict[x]["value"] for x in constants.score_situations_dict]
    homeaway = form.homeAway.data
    if homeaway == "all":
        homeaway = [0, 1]
    else:
        homeaway = [int(homeaway), ]
    periods = constants.periods_options["All"]["value"]
    if 0 in periods:
        periods = [0, ]

    if 7 in scoresituations:
        scoresituations = [7, ]
    if 7 in teamstrengths:
        teamstrengths = [7, ]

    teamrun = TeamRun.query.filter(TeamRun.Date >= startingDate, TeamRun.Date <= endingDate,
        TeamRun.gamestate.in_(teamstrengths),
        TeamRun.scorediffcat.in_(scoresituations), TeamRun.home.in_(homeaway),
        TeamRun.Team == team,
        TeamRun.period.in_(periods)).all()

    games, seasons = helpers.calculate(teamrun, True)

    return render_template("teams/teamhistory.html",
        rd=rd,
        cpg=cpg,
        ggf=ggf,
        form=form,
        games=games,
        seasons=seasons)


@mod.route('/comparisons/', methods=["GET", "POST"])
def show_team_comparisons():
    rd = setup_nav()
    cpg = ComparisonGraphForm()
    teamgames = get_r_seasons()
    tablecolumns = [0, ]
    form = ComparisonForm(request.form)
    form.startingSeason.choices = [(x, str(x)[0:4] + "-" + str(x)[4:]) for x in sorted(teamgames.keys(), reverse=True)]
    form.endingSeason.choices = [(x, str(x)[0:4] + "-" + str(x)[4:]) for x in sorted(teamgames.keys(), reverse=True)]
    filterteams = form.filterTeams.data
    if filterteams is None:
        filterteams = []
    allteams = form.filterTeams.choices

    try:
        oldStart = form.startingSeason.data
        oldEnd = form.endingSeason.data
        form.startingSeason.data = int(form.startingSeason.data)
        form.endingSeason.data = int(form.endingSeason.data)
    except:
        pass
    allseasons = [(x, str(x)[0:4] + "-" + str(x)[4:]) for x in sorted(teamgames.keys(), reverse=True)]
    usedates = False

    if request.method == "POST" and form.validate():
        startingSeason = form.startingSeason.data
        endingSeason = form.endingSeason.data
        form.startingSeason.data = oldStart
        form.endingSeason.data = oldEnd
        startingDate = form.startingDate.data
        endingDate = form.endingDate.data
        usedates = form.bydate.data
        if not usedates:
            if endingSeason > startingSeason:
                begin = startingSeason
                end = endingSeason
            else:
                begin = endingSeason
                end = startingSeason
            currSeason = begin
            seasons = [begin, ]
            # TODO: Error check this?
            while begin != end:
                bsplit = str(begin)[0:4]
                begin = int(bsplit) * 10000 + 10001 + int(bsplit) + 1
                seasons.append(begin)
        else:
            if endingDate < startingDate:
                temp = endingDate
                endingDate = startingDate
                startingDate = temp
    else:
        smax = max(teamgames.keys())
        seasons = [smax, ]
    # Filter teamrun based on form data
    teamstrengths = int(form.teamstrengths.data)
    if teamstrengths == 7:
        teamstrengths = [constants.strength_situations_dict[x]["value"] for x in constants.strength_situations_dict]
    else:
        teamstrengths = [teamstrengths, ]
    scoresituations = int(form.scoresituations.data)
    if scoresituations == 7:
        scoresituations = [constants.score_situations_dict[x]["value"] for x in constants.score_situations_dict]
    homeaway = form.homeAway.data
    if homeaway == "all":
        homeaway = [0, 1]
    else:
        homeaway = [int(homeaway), ]
    periods = constants.periods_options[form.period.data]["value"]
    if 0 in periods:
        periods = [0, ]
    if 7 in scoresituations:
        scoresituations = [7, ]
    if 7 in teamstrengths:
        teamstrengths = [7, ]

    if not usedates:
        if len(filterteams) == 0:
            teamrun = TeamRun.query.filter(TeamRun.season.in_(seasons), TeamRun.gamestate.in_(teamstrengths),
                TeamRun.scorediffcat.in_(scoresituations), TeamRun.home.in_(homeaway),
                TeamRun.period.in_(periods)).all()
        else:
            teamrun = TeamRun.query.filter(TeamRun.season.in_(seasons), TeamRun.gamestate.in_(teamstrengths),
                TeamRun.scorediffcat.in_(scoresituations), TeamRun.home.in_(homeaway),
                TeamRun.Team.in_(filterteams),
                TeamRun.period.in_(periods)).all()
    else:
        if len(filterteams) == 0:
            teamrun = TeamRun.query.filter(TeamRun.Date >= startingDate, TeamRun.Date <= endingDate,
                TeamRun.gamestate.in_(teamstrengths),
                TeamRun.scorediffcat.in_(scoresituations), TeamRun.home.in_(homeaway),
                TeamRun.period.in_(periods)).all()
        else:
            teamrun = TeamRun.query.filter(TeamRun.Date >= startingDate, TeamRun.Date <= endingDate,
                TeamRun.gamestate.in_(teamstrengths),
                TeamRun.scorediffcat.in_(scoresituations), TeamRun.home.in_(homeaway),
                TeamRun.Team.in_(filterteams),
                TeamRun.period.in_(periods)).all()

    games, seasons = helpers.calculate(teamrun, form.divideSeason.data)
    if form.splitgame.data == True:
        summaries = games
    else:
        summaries = seasons

    return render_template('teams/teamcomparison.html',
        rd=rd,
        form=form,
        summaries=summaries,
        cpg=cpg,
        filterteams=filterteams,
        allteams=allteams)
