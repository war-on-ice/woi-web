from datetime import date

import app

from models import GamesTest


def get_games(cs=None):
    cy = date.today()
    if cs is None:
        cs = GamesTest.query.filter(GamesTest.date<=cy).\
            order_by(GamesTest.date.desc()).\
            order_by(app.Base.metadata.tables['gamestest'].c["game.end"]).\
            order_by(app.Base.metadata.tables['gamestest'].c["game.start"]).\
            order_by(app.Base.metadata.tables['gamestest'].c["status"]).first()
        cs = cs.season
    games = GamesTest.query.filter(GamesTest.date<=cy).filter(GamesTest.season==cs).\
        order_by(GamesTest.date.desc()).\
        order_by(app.Base.metadata.tables['gamestest'].c["game.end"]).\
        order_by(app.Base.metadata.tables['gamestest'].c["game.start"]).\
        order_by(app.Base.metadata.tables['gamestest'].c["status"]).\
        limit(1000)
    return games