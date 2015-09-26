from flask import Blueprint

from app import app
from flask import render_template
from sqlalchemy import desc
from app.navigation import setup_nav

mod = Blueprint('game', __name__, url_prefix='/game')

@mod.route('/<gameId>/')
def show_game_summary(gameId):
    return render_template('game/gamesummary.html',
                           gameId = gameId)