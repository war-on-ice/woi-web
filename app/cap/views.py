from flask import Blueprint

__author__ = 'akm'

from app import app
from app.cap.models import Contracts, Players
from flask import render_template
from sqlalchemy import desc
from app.navigation import setup_nav

mod = Blueprint('cap', __name__, url_prefix='/cap')

# @app.route('/')
# def show_index():
#     return render_template('index.html',
#                            title='Test Page')

@mod.route('/player/<playerId>/')
def show_player_contract(playerId):
    rd = setup_nav()
    selectedPlayer =  Players.query.filter_by(woiid=playerId).first()
    selectedPlayerContracts = Contracts.query.filter_by(PlayerID=playerId).order_by(desc(Contracts.EffectiveSeason)).all()

    return render_template('cap/playercap.html',
                           player = selectedPlayer,
                           contractDetails = selectedPlayerContracts,
                           title = selectedPlayer.firstlast, rd=rd)

# @app.route('/team/<teamId>/')
# def show_team_current(teamId):
#     selectedTeam = models.Teams.query.filter_by(TeamId=teamId).first()
#
#     return render_template('teamcap.html',
#                             team = selectedTeam)
#
# @app.route('/team/<teamId>/<seasonId>/')
# def show_team_historical(teamId, seasonId):
#     selectedTeam = models.Teams.query.filter_by(TeamId=teamId).first()
#     return render_template('teamcap.html',
#                             team = selectedTeam)