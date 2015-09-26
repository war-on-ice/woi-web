from flask import Blueprint

from app import constants
from app import app
from flask import render_template
from sqlalchemy import desc
from app.navigation import setup_nav

mod = Blueprint('game', __name__, url_prefix='/game')

@mod.route('/<gameId>/')
def show_game_summary(gameId):
    return render_template('game/gamesummary.html',
                           gameId = gameId)

@mod.route('/test/<gameId>/')
def show_game_summary_test(gameId):
    rd = setup_nav()
    return render_template('game/gamesummary2.html',
                           gameId = gameId,
                           strength_situations = constants.strength_situations,
                           score_situations = constants.score_situations,
                           periods = constants.periods,
                           rd = rd)