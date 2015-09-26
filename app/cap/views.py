from flask import Blueprint

__author__ = 'akm'

from app import app
from app.cap.models import Contract, Player, Team
from flask import render_template
from sqlalchemy import desc
from app.navigation import setup_nav

mod = Blueprint('cap', __name__, url_prefix='/cap')

@mod.route('/player/<playerId>/')
def show_player_contract(playerId):
    rd = setup_nav()
    selectedPlayer =  Player.query.filter_by(PlayerId=playerId).first()
    selectedPlayerContracts = Contract.query.filter_by(PlayerID=playerId).order_by(desc(Contract.EffectiveSeason)).all()

    return render_template('cap/playercap.html',
                           player = selectedPlayer,
                           contractDetails = selectedPlayerContracts,
                           title = selectedPlayer.FullName, rd=rd)

@mod.route('/team/<teamId>/')
def show_team_current(teamId):
    rd = setup_nav()
    selectedTeam = Team.query.filter_by(TeamId=teamId).first()

    return render_template('cap/teamcap.html',
                            team = selectedTeam, rd=rd)
#
# @app.route('/team/<teamId>/<seasonId>/')
# def show_team_historical(teamId, seasonId):
#     selectedTeam = models.Teams.query.filter_by(TeamId=teamId).first()
#     return render_template('teamcap.html',
#                             team = selectedTeam)