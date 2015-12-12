# from sqlalchemy import Table
from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint, Table, Float, SmallInteger
from app import db#, metadata

from app import Base

#class PlayerSeason(db.Model):
#    __table__ = Base.metadata.tables['playerseason']