from flask import Blueprint, request

from app import app, Base, constants, filters
from flask import render_template
from sqlalchemy import desc
from app.navigation import setup_nav
from app.gamesummary.models import RosterMaster

from app.helpers import get_rdata

mod = Blueprint('player', __name__, url_prefix='/player')

import resources

CORE_DATA = "http://data.war-on-ice.net/woi-common.RData"
CAP_DATA = "http://war-on-ice.com/cap/current-contract-full.RData"


@mod.route('/')
def show_player():
    rd = setup_nav()
    rdata = get_rdata(CAP_DATA)
    keys = []
    for cap in rdata["team.two"]:
        print cap["Name"], cap["S20152016"]
        break
    return render_template('players/players.html',
        rd=rd)


@mod.route("/gar/")
def show_gar():
    rd = setup_nav()
    csv = resources.get_csv("http://war-on-ice.com/data/GAR-seasonal.csv")
    cd = resources.combine_data(csv)
    total = resources.combine_seasons(cd)
    return render_template("players/gar.html",
        rd=rd,
        cd=cd,
        total=total)

