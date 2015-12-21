from flask import Blueprint, request

from flask import render_template
from sqlalchemy import desc

from app.navigation import setup_nav
from app.gamesummary.models import TeamRun
from app import app, Base, constants, filters, helpers
from app.gamesummary.calls import get_r_standings, get_r_seasons, compiled_teams, row2dict

from forms import SeasonSelectForm, ComparisonForm, ComparisonGraphForm

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
    cpg = ComparisonGraphForm()
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
        gs["CF%"] = helpers.percent(gs["CF"], gs["CA"])
        gs["C+/-"] = gs["CF"] - gs["CA"]
        gs["SF"] = int(float(td["SF"]))
        gs["SA"] = int(float(td["SA"]))
        gs["SF%"] = helpers.percent(gs["SF"], gs["SA"])
        gs["S+/-"] = gs["SF"] - gs["SA"]
        gs["GF"] = int(td["GF"])
        gs["GA"] = int(td["GA"])
        gs["GF%"] = helpers.percent(gs["GF"], gs["GA"])
        gs["G+/-"] = int(gs["GF"] - gs["GA"])
        gs["CF%"] = helpers.percent(td["CF"], td["CA"])
        cf60 = helpers.c_60(td["CF"], gs["TOI"])
        ca60 = helpers.c_60(td["CA"], gs["TOI"])
        gs["CP60"] = round(cf60 + ca60, 2)
        gs["MSF"] = float(td["FF"]) - float(td["SF"])
        gs["FAC_WIN"] = float(td["FAC_WIN"])
        gs["FAC_LOSE"] = float(td["FAC_LOSE"])
        gs["ZSO"] = float(td["ZSO"])
        gs["ZSD"] = float(td["ZSD"])
        gs["ZSO%"] = helpers.percent(gs["ZSO"], gs["ZSD"])
        gs["HSCF"] = int(td["sSCF"])
        gs["HSCA"] = int(td["sSCA"])
        gs["HSCF%"] = helpers.percent(gs["HSCF"], gs["HSCA"])
        gs["HSC+/-"] = gs["HSCF"] - gs["HSCA"]
        gs["HSCF60"] = helpers.c_60(gs["HSCF"], gs["TOI"])
        gs["HSCA60"] = helpers.c_60(gs["HSCA"], gs["TOI"])
        gs["HSCP60"] = gs["HSCF60"] + gs["HSCA60"]
        gs["SCF"] = int(td["SCF"])
        gs["SCA"] = int(td["SCA"])
        gs["SCF%"] = helpers.percent(gs["SCF"], gs["SCA"])
        gs["SC+/-"] = gs["SCF"] - gs["SCA"]
        gs["SCF60"] = helpers.c_60(gs["SCF"], gs["TOI"])
        gs["SCA60"] = helpers.c_60(gs["SCA"], gs["TOI"])
        gs["SCP60"] = gs["SCF60"] + gs["SCA60"]
        gs["CF60"] = helpers.c_60(gs["CF"], gs["TOI"])
        gs["CA60"] = helpers.c_60(gs["CA"], gs["TOI"])
        gs["FF"] = int(float(td["FF"]))
        gs["FA"] = int(float(td["FA"]))
        gs["F+/-"] = gs["FF"] - gs["FA"]
        gs["FF%"] = helpers.percent(gs["FF"], gs["FA"])
        gs["FF60"] = helpers.c_60(gs["FF"], gs["TOI"])
        gs["FA60"] = helpers.c_60(gs["FA"], gs["TOI"])
        gs["FP60"] = gs["FF60"] + gs["FA60"]
        gs["MSF"] = gs["FF"] - gs["SF"]
        gs["MSA"] = gs["FA"] - gs["SA"]
        gs["BSF"] = gs["CF"] - gs["MSF"] - gs["SF"]
        gs["BSA"] = gs["CA"] - gs["MSA"] - gs["SA"]
        gs["SF60"] = helpers.c_60(gs["SF"], gs["TOI"])
        gs["SA60"] = helpers.c_60(gs["SA"], gs["TOI"])
        gs["GF60"] = helpers.c_60(gs["GF"], gs["TOI"])
        gs["GA60"] = helpers.c_60(gs["GA"], gs["TOI"])
        gs["FO_W"] = float(td["FAC_WIN"])
        gs["FO_L"] = float(td["FAC_LOSE"])
        gs["ZSO"] = float(td["ZSO"])
        gs["ZSN"] = float(td["ZSN"])
        gs["ZSD"] = float(td["ZSD"])
        gs["HIT"] = float(td["HIT"])
        gs["HIT-"] = float(td["HIT_TAKEN"])
        gs["PN-"] = float(td["PENL_DRAWN"])
        gs["PN"] = float(td["PENL_TAKEN"])
        gs["PenD"] = gs["PN-"] - gs["PN"]
        gs["OSh%"] = helpers.percent(gs["GF"], gs["SF"])
        gs["OFenSh%"] = helpers.percent(gs["GF"], gs["FF"])
        gs["OCOn%"] = helpers.ratio(gs["SF"], gs["CF"])
        if form.splitgame.data == True:
            if form.tablecolumns.data == "0" or form.tablecolumns.data == "9":
                gs["OFOn%"] = helpers.percent(gs["SF"], gs["MSF"])
                gs["OSh%"] = helpers.ratio(gs["GF"], gs["SF"])
                gs["OSv%"] = 100.00 - helpers.ratio(gs["GA"], gs["SA"])
                gs["PDO"] = round(gs["OSv%"] + gs["OSh%"], 2)
                gs["FO%"] = helpers.percent(gs["FAC_WIN"], gs["FAC_LOSE"])
            summaries.append(gs)
        else:
            if gs["Team"] not in compiled and gs["Team"] != "PHX":
                compiled[gs["Team"]] = []
            elif gs["Team"] == "PHX":
                if "ARI" not in compiled:
                    compiled["ARI"] = []
                compiled["ARI"].append(gs)
            if gs["Team"] != "PHX":
                compiled[gs["Team"]].append(gs)

    for team in compiled:
        gs = {}
        td = compiled[team]
        gs["Gm"] = len(td)
        gs["Team"] = team
        gs["CF"] = sum([x["CF"] for x in td])
        gs["CA"] = sum([x["CA"] for x in td])
        gs["CF%"] = helpers.percent(gs["CF"], gs["CA"])
        gs["C+/-"] = gs["CF"] - gs["CA"]
        gs["TOI"] = sum(x["TOI"] for x in td)
        seasons = sorted(set([x["season"] for x in td]))
        if len(seasons) == 1:
            gs["season"] = seasons[0]
        else:
            gs["season"] = seasons[0] + "-" + seasons[-1]
        gs["GF"] = sum([x["GF"] for x in td])
        gs["GA"] = sum([x["GA"] for x in td])
        gs["G+/-"] = int(gs["GF"] - gs["GA"])
        gs["ZSO"] = sum([x["ZSO"] for x in td])
        gs["ZSD"] = sum([x["ZSD"] for x in td])
        gs["CF%"] = helpers.percent(gs["CF"], gs["CA"])
        gs["CP60"] =  round(sum([x["CP60"] for x in td]) / len(td), 2)
        gs["OFOn%"] = helpers.percent(sum([x["SF"] for x in td]),
            sum([x["MSF"] for x in td]))
        gs["OSh%"] = helpers.ratio(sum([x["GF"] for x in td]), sum([x["SF"] for x in td]))
        gs["OSv%"] = 100.00 - helpers.ratio(sum([x["GA"] for x in td]), sum([x["SA"] for x in td]))
        gs["PDO"] = round(gs["OSv%"] + gs["OSh%"], 2)
        gs["FO%"] = helpers.percent(sum([x["FAC_WIN"] for x in td]), sum([x["FAC_LOSE"] for x in td]))
        gs["HSCF"] = sum([x["HSCF"] for x in td])
        gs["HSCA"] = sum([x["HSCA"] for x in td])
        gs["HSCF%"] = helpers.percent(gs["HSCF"], gs["HSCA"])
        gs["HSC+/-"] = gs["HSCF"] - gs["HSCA"]
        gs["HSCF60"] = round(sum([x["HSCF60"] for x in td]) / len(td), 2)
        gs["HSCA60"] = round(sum([x["HSCA60"] for x in td]) / len(td), 2)
        gs["HSCP60"] = gs["HSCF60"] + gs["HSCA60"]
        gs["SCF"] = sum([x["SCF"] for x in td])
        gs["SCA"] = sum([x["SCA"] for x in td])
        gs["SCF%"] = helpers.percent(gs["SCF"], gs["SCA"])
        gs["SC+/-"] = gs["SCF"] - gs["SCA"]
        gs["SCF60"] = round(sum([x["SCF60"] for x in td]) / len(td), 2)
        gs["SCA60"] = round(sum([x["SCA60"] for x in td]) / len(td), 2)
        gs["SCP60"] = gs["SCF60"] + gs["SCA60"]
        gs["CF60"] = round(sum([x["CF60"] for x in td]) / len(td), 2)
        gs["CA60"] = round(sum([x["CA60"] for x in td]) / len(td), 2)
        gs["FF"] = sum([x["FF"] for x in td])
        gs["FA"] = sum([x["FA"] for x in td])
        gs["F+/-"] = gs["FF"] - gs["FA"]
        gs["FF60"] = round(sum([x["FF60"] for x in td]) / len(td), 2)
        gs["FA60"] = round(sum([x["FA60"] for x in td]) / len(td), 2)
        gs["FP60"] = gs["FF60"] + gs["FA60"]
        gs["FF%"] = helpers.percent(gs["FF"], gs["FA"])
        gs["MSF"] = sum([x["MSF"] for x in td])
        gs["MSA"] = sum([x["MSA"] for x in td])
        gs["BSF"] = sum([x["BSF"] for x in td])
        gs["BSA"] = sum([x["BSA"] for x in td])
        gs["SF"] = sum([x["SF"] for x in td])
        gs["SA"] = sum([x["SA"] for x in td])
        gs["SF%"] = helpers.percent(gs["SF"], gs["SA"])
        gs["S+/-"] = gs["SF"] - gs["SA"]
        gs["SF60"] = round(sum([x["SF60"] for x in td]) / len(td), 2)
        gs["SA60"] = round(sum([x["SA60"] for x in td]) / len(td), 2)
        gs["GF"] = sum([x["GF"] for x in td])
        gs["GA"] = sum([x["GA"] for x in td])
        gs["GF%"] = helpers.percent(gs["GF"], gs["GA"])
        gs["GF60"] = round(sum([x["GF60"] for x in td]) / len(td), 2)
        gs["GA60"] = round(sum([x["GA60"] for x in td]) / len(td), 2)
        gs["FO_W"] = sum([x["FO_W"] for x in td])
        gs["FO_L"] = sum([x["FO_L"] for x in td])
        gs["ZSO"] = sum([x["ZSO"] for x in td])
        gs["ZSN"] = sum([x["ZSN"] for x in td])
        gs["ZSD"] = sum([x["ZSD"] for x in td])
        gs["ZSO%"] = helpers.percent(gs["ZSO"], gs["ZSD"])
        gs["HIT"] = sum([x["HIT"] for x in td])
        gs["HIT-"] = sum([x["HIT-"] for x in td])
        gs["PN-"] = sum([x["PN-"] for x in td])
        gs["PN"] = sum([x["PN"] for x in td])
        gs["PenD"] = gs["PN-"] - gs["PN"]
        gs["OSh%"] = helpers.percent(gs["GF"], gs["SF"])
        gs["OFenSh%"] = helpers.percent(gs["GF"], gs["FF"])
        gs["OCOn%"] = helpers.ratio(gs["SF"], gs["CF"])
        summaries.append(gs)

        

    return render_template('teams/teamcomparison.html',
        rd=rd,
        form=form,
        summaries=summaries,
        cpg=cpg)
