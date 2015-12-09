# from sqlalchemy import Table
from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint, Table, Float, SmallInteger
from app import db#, metadata

from app import Base

class TeamRun(db.Model):
    __table__ = Base.metadata.tables['teamrun']
    __mapper_args__ = {
        'primary_key': [Base.metadata.tables['teamrun'].c.gcode,
        Base.metadata.tables['teamrun'].c.TOI,
        Base.metadata.tables['teamrun'].c.season,
        Base.metadata.tables['teamrun'].c.Team,
        Base.metadata.tables['teamrun'].c.scorediffcat,
        Base.metadata.tables['teamrun'].c.season]
    }


class PlayByPlay(db.Model):
    __table__ = Base.metadata.tables['playbyplay']
    __mapper_args__ = {
        'primary_key': [Base.metadata.tables['playbyplay'].c.gcode,
        Base.metadata.tables['playbyplay'].c.season,
        Base.metadata.tables['playbyplay'].c.seconds,
        Base.metadata.tables['playbyplay'].c.period]
    }


class GoalieRun(db.Model):
    __table__ = Base.metadata.tables['goalierun']
    __mapper_args__ = {
        'primary_key': [Base.metadata.tables['goalierun'].c.gcode,
        Base.metadata.tables['goalierun'].c.TOI,
        Base.metadata.tables['goalierun'].c.season,
        Base.metadata.tables['goalierun'].c.ID]
    }


class RosterMaster(db.Model):
    __table__ = Base.metadata.tables['rostermaster']
    __mapper_args__ = {
        'primary_key': [Base.metadata.tables['rostermaster'].c["woi.id"]]
    }


class GameRoster(db.Model):
    __table__ = Base.metadata.tables['gameroster']
    __mapper_args__ = {
        'primary_key': [Base.metadata.tables['gameroster'].c.gcode,
        Base.metadata.tables['gameroster'].c.season,
        Base.metadata.tables['gameroster'].c.numfirstlast,]
    }


class GamesTest(db.Model):
    __table__ = Base.metadata.tables['gamestest']
    __mapper_args__ = {
        'primary_key': [Base.metadata.tables['gamestest'].c.gcode,
        Base.metadata.tables['gamestest'].c.season]
    }


class PlayerRun(db.Model):
    __table__ = Base.metadata.tables['playerrun']
    __mapper_args__ = {
        'primary_key': [Base.metadata.tables['playerrun'].c.gcode,
        Base.metadata.tables['playerrun'].c.TOI,
        Base.metadata.tables['playerrun'].c.season,
        Base.metadata.tables['playerrun'].c.ID,]
    }
