from flask import Blueprint, request

from app import app, Base, constants, filters
from flask import render_template
from sqlalchemy import desc
from app.navigation import setup_nav

from helper import get_rdata

mod = Blueprint('player', __name__, url_prefix='/player')


@mod.route('/')
def show_player():
    rd = setup_nav()
    return render_template('players/players.html',
        rd=rd)
