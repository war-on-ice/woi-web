from flask import Blueprint, request

from app import app, Base, constants, filters
from flask import render_template
from sqlalchemy import desc
from app.navigation import setup_nav
from app.gamesummary.calls import get_r_standings, get_r_seasons

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
