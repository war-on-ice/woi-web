from flask import Blueprint, request

from flask import render_template
from sqlalchemy import desc

from app.navigation import setup_nav
from app.gamesummary.models import TeamRun
from app import app, Base, constants, filters, helpers
from app.gamesummary.calls import get_r_standings, get_r_seasons, compiled_teams, row2dict

from forms import SeasonSelectForm, ComparisonForm

import datetime
import urllib2

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


@mod.route('/comparisons/', methods=["GET", "POST"])
def show_team_comparisons():
    rd = setup_nav()

    teamgames = get_r_seasons()
    tablecolumns = [0, ]
    form = ComparisonForm(request.form)
    form.startingSeason.choices = [(x, str(x)[0:4] + "-" + str(x)[4:]) for x in sorted(teamgames.keys(), reverse=True)]
    form.endingSeason.choices = [(x, str(x)[0:4] + "-" + str(x)[4:]) for x in sorted(teamgames.keys(), reverse=True)]
    try:
        oldStart = form.startingSeason.data
        oldEnd = form.endingSeason.data
        form.startingSeason.data = int(form.startingSeason.data)
        form.endingSeason.data = int(form.endingSeason.data)
    except:
        pass
    allseasons = [(x, str(x)[0:4] + "-" + str(x)[4:]) for x in sorted(teamgames.keys(), reverse=True)]
    if request.method == "POST" and form.validate():
        startingSeason = form.startingSeason.data
        endingSeason = form.endingSeason.data
        form.startingSeason.data = oldStart
        form.endingSeason.data = oldEnd
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

    teamrun = TeamRun.query.filter(TeamRun.season.in_(seasons), TeamRun.gamestate.in_(teamstrengths),
        TeamRun.scorediffcat.in_(scoresituations), TeamRun.home.in_(homeaway),
        TeamRun.period.in_(periods)).all()
    summaries=[]
    compiled = {}
    for game in teamrun:
        td = row2dict(game)
        gs = {}
        gs["Gm"] = 1
        gs["Date"] = td["Date"]
        gs["Team"] = td["Team"]
        gs["season"] = str(td["season"]).split(".")[0]
        gs["TOI"] = round(float(td["TOI"]) / 60.0, 2)
        gs["CF"] = float(td["CF"])
        gs["CA"] = float(td["CA"])
        gs["SF"] = float(td["SF"])
        gs["SA"] = float(td["SA"])
        gs["GF"] = float(td["GF"])
        gs["GA"] = float(td["GA"])
        if form.tablecolumns.data == "0" or form.tablecolumns.data == "9":
            gs["CF%"] = helpers.percent(td["CF"], td["CA"])
            cf60 = helpers.c_60(td["CF"], gs["TOI"])
            ca60 = helpers.c_60(td["CA"], gs["TOI"])
            gs["CP60"] = round(cf60 + ca60, 2)
            gs["MSF"] = float(td["FF"]) - float(td["SF"])
            # FO%
            gs["FAC_WIN"] = float(td["FAC_WIN"])
            gs["FAC_LOSE"] = float(td["FAC_LOSE"])
            # ZSO
            gs["ZSO"] = float(td["ZSO"])
            gs["ZSD"] = float(td["ZSD"])
        if form.tablecolumns.data == "1" or form.tablecolumns.data == "9":
            gs["HSCF"] = float(td["sSCF"])
            gs["HSCA"] = float(td["sSCA"])
            gs["HSCF60"] = helpers.c_60(gs["HSCF"], gs["TOI"])
            gs["HSCA60"] = helpers.c_60(gs["HSCA"], gs["TOI"])
        if form.tablecolumns.data == "2" or form.tablecolumns.data == "9":
            gs["SCF"] = float(td["SCF"])
            gs["SCA"] = float(td["SCA"])
            gs["SCF60"] = helpers.c_60(gs["SCF"], gs["TOI"])
            gs["SCA60"] = helpers.c_60(gs["SCA"], gs["TOI"])
        if form.tablecolumns.data == "3" or form.tablecolumns.data == "9":
            gs["CF60"] = helpers.c_60(gs["CF"], gs["TOI"])
            gs["CA60"] = helpers.c_60(gs["CA"], gs["TOI"])
            gs["FF"] = float(td["FF"])
            gs["FA"] = float(td["FA"])
            gs["FF60"] = helpers.c_60(gs["FF"], gs["TOI"])
            gs["FA60"] = helpers.c_60(gs["FA"], gs["TOI"])
            gs["MSF"] = gs["FF"] - gs["SF"]
            gs["MSA"] = gs["FA"] - gs["SA"]
            gs["BSF"] = gs["CF"] - gs["MSF"] - gs["SF"]
            gs["BSA"] = gs["CA"] - gs["MSA"] - gs["SA"]
        if form.tablecolumns.data == "5" or form.tablecolumns.data == "9":
            gs["SF60"] = helpers.c_60(gs["SF"], gs["TOI"])
            gs["SA60"] = helpers.c_60(gs["SA"], gs["TOI"])
            gs["GF60"] = helpers.c_60(gs["GF"], gs["TOI"])
            gs["GA60"] = helpers.c_60(gs["GA"], gs["TOI"])
            gs["FF"] = float(td["FF"])
            gs["FA"] = float(td["FA"])
            gs["MSF"] = gs["FF"] - gs["SF"]
            gs["MSA"] = gs["FA"] - gs["SA"]
        if form.tablecolumns.data == "7" or form.tablecolumns.data == "9":
            gs["FAC_WIN"] = float(td["FAC_WIN"])
            gs["FAC_LOSE"] = float(td["FAC_LOSE"])
            gs["ZSO"] = float(td["ZSO"])
            gs["ZSN"] = float(td["ZSN"])
            gs["ZSD"] = float(td["ZSD"])
            gs["HIT"] = float(td["HIT"])
            gs["HIT_TAKEN"] = float(td["HIT_TAKEN"])
            gs["PENL_DRAWN"] = float(td["PENL_DRAWN"])
            gs["PENL_TAKEN"] = float(td["PENL_TAKEN"])
        if form.splitgame.data == True:
            if form.tablecolumns.data == "0" or form.tablecolumns.data == "9":
                gs["OFOn%"] = helpers.percent(gs["SF"], gs["MSF"])
                gs["OSh%"] = helpers.ratio(gs["GF"], gs["SF"])
                gs["OSv%"] = 100.00 - helpers.ratio(gs["GA"], gs["SA"])
                gs["FO%"] = helpers.percent(gs["FAC_WIN"], gs_["FAC_LOSE"])
            summaries.append(gs)
        else:
            if gs["Team"] not in compiled:
                compiled[gs["Team"]] = []
            compiled[gs["Team"]].append(gs)

    for team in compiled:
        comp = {}
        td = compiled[team]
        comp["Gm"] = len(td)
        comp["Team"] = team
        comp["CF"] = sum([x["CF"] for x in td])
        comp["CA"] = sum([x["CA"] for x in td])
        comp["TOI"] = sum(x["TOI"] for x in td)
        seasons = sorted(set([x["season"] for x in td]))
        if len(seasons) == 1:
            comp["season"] = seasons[0]
        else:
            comp["season"] = seasons[0] + "-" + seasons[-1]
        if form.tablecolumns.data == "0" or form.tablecolumns.data == "9":
            comp["GF"] = sum([x["GF"] for x in td])
            comp["GA"] = sum([x["GA"] for x in td])
            comp["ZSO"] = sum([x["ZSO"] for x in td])
            comp["ZSD"] = sum([x["ZSD"] for x in td])
            comp["CF%"] = helpers.percent(comp["CF"], comp["CA"])
            comp["CP60"] =  round(sum([x["CP60"] for x in td]) / len(td), 2)
            comp["OFOn%"] = helpers.percent(sum([x["SF"] for x in td]),
                sum([x["MSF"] for x in td]))
            try:
                comp["OSh%"] = round(sum([x["GF"] for x in td]) / sum([x["SF"] for x in td]) * 100, 2)
            except:
                comp["OSh%"] = 0
            comp["OSv%"] = 100.00 - helpers.ratio(sum([x["GA"] for x in td]), sum([x["SA"] for x in td]))
            comp["FO%"] = helpers.percent(sum([x["FAC_WIN"] for x in td]), sum([x["FAC_WIN"] for x in td]))
        if form.tablecolumns.data == "1" or form.tablecolumns.data == "9":
            comp["HSCF"] = sum([x["HSCF"] for x in td])
            comp["HSCA"] = sum([x["HSCA"] for x in td])
            comp["HSCF60"] = round(sum([x["HSCF60"] for x in td]) / len(td), 2)
            comp["HSCA60"] = round(sum([x["HSCA60"] for x in td]) / len(td), 2)
        if form.tablecolumns.data == "2" or form.tablecolumns.data == "9":
            comp["SCF"] = sum([x["SCF"] for x in td])
            comp["SCA"] = sum([x["SCA"] for x in td])
            comp["SCF60"] = round(sum([x["SCF60"] for x in td]) / len(td), 2)
            comp["SCA60"] = round(sum([x["SCA60"] for x in td]) / len(td), 2)
        if form.tablecolumns.data == "3" or form.tablecolumns.data == "9":
            comp["CF60"] = round(sum([x["CF60"] for x in td]) / len(td), 2)
            comp["CA60"] = round(sum([x["CA60"] for x in td]) / len(td), 2)
            comp["FF"] = sum([x["FF"] for x in td])
            comp["FA"] = sum([x["FA"] for x in td])
            comp["FF60"] = round(sum([x["FF60"] for x in td]) / len(td), 2)
            comp["FA60"] = round(sum([x["FA60"] for x in td]) / len(td), 2)
            comp["MSF"] = sum([x["MSF"] for x in td])
            comp["MSA"] = sum([x["MSA"] for x in td])
            comp["BSF"] = sum([x["BSF"] for x in td])
            comp["BSA"] = sum([x["BSA"] for x in td])
        if form.tablecolumns.data == "5" or form.tablecolumns.data == "9":
            comp["SF"] = sum([x["SF"] for x in td])
            comp["SA"] = sum([x["SA"] for x in td])
            comp["SF60"] = round(sum([x["SF60"] for x in td]) / len(td), 2)
            comp["SA60"] = round(sum([x["SA60"] for x in td]) / len(td), 2)
            comp["GF"] = sum([x["GF"] for x in td])
            comp["GA"] = sum([x["GA"] for x in td])
            comp["GF60"] = round(sum([x["GF60"] for x in td]) / len(td), 2)
            comp["GA60"] = round(sum([x["GA60"] for x in td]) / len(td), 2)
            comp["FF"] = sum([x["FF"] for x in td])
            comp["FA"] = sum([x["FA"] for x in td])
            comp["MSF"] = sum([x["MSF"] for x in td])
            comp["MSA"] = sum([x["MSA"] for x in td])
        if form.tablecolumns.data == "7" or form.tablecolumns.data == "9":
            comp["FAC_WIN"] = sum([x["FAC_WIN"] for x in td])
            comp["FAC_LOSE"] = sum([x["FAC_LOSE"] for x in td])
            comp["ZSO"] = sum([x["ZSO"] for x in td])
            comp["ZSN"] = sum([x["ZSN"] for x in td])
            comp["ZSD"] = sum([x["ZSD"] for x in td])
            comp["HIT"] = sum([x["HIT"] for x in td])
            comp["HIT_TAKEN"] = sum([x["HIT_TAKEN"] for x in td])
            comp["PENL_DRAWN"] = sum([x["PENL_DRAWN"] for x in td])
            comp["PENL_TAKEN"] = sum([x["PENL_TAKEN"] for x in td])
        summaries.append(comp)

        

    return render_template('teams/teamcomparison.html',
        rd=rd,
        form=form,
        summaries=summaries,)
