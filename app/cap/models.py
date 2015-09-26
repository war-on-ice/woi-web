# from sqlalchemy import Table
from sqlalchemy import Column, Integer, PrimaryKeyConstraint, Table, Float, SmallInteger
from app import db#, metadata

from app import Base

class Player(db.Model):
    __table__ = Base.metadata.tables["Player"]
    # __tablename__ = "roster"
    # woiid = db.Column(db.String(15), primary_key= True)
    # pos = db.Column(db.String(3))
    # firstlast = db.Column(db.String(200))
    # dob = db.Column(db.DateTime)

    def __repr__(self):
        return self.woiid

class ContractHeaders(db.Model):
    __table__ = Base.metadata.tables["ContractHeader"]
   # __table__ = metadata.tables["ContractHeader"]

    def __repr__(self):
        return self.ContractID


class Contract(db.Model):
    __tablename__ = "Contracts"
    DetailID = Column(Integer, primary_key= True)
    # ContractID = Column(Integer)
    # PlayerID = Column(db.String(14))
    # ContractTeamID = Column(db.String(5))
    # HeaderType = Column(db.String(5))
    # SigningDate = Column(db.Date)
    # EffectiveSeason = Column(Integer)
    # ContractLength = Column(Integer)
    # Season = Column(Integer)
    # BaseSalary = Column(db.Float)
    # SigningBonus = Column(db.Float)
    # MaxPerfBonus = Column(db.Float)
    # PerfBonusMet = Column(db.Float)
    # MinorSalary = Column(db.Float)
    # JuniorSalary = Column(db.Float)
    # MinimumSalary = Column(db.Float)
    # PerfBonusElg = Column(db.SmallInteger)
    # Clause = Column(db.SmallInteger)
    # NDC = Column(db.SmallInteger)
    # NTC = Column(db.SmallInteger)
    # Slid = Column(db.SmallInteger)
    # BoughtOut = Column(db.SmallInteger)
    # Retired = Column(db.SmallInteger)
    # Source = Column(db.String(100))
    # Unconfirmed = Column(db.Integer)
    # ActiveContract = Column(db.Integer)
    # AAV = Column(db.Float)
    __table_args__ = (PrimaryKeyConstraint(DetailID), {"autoload":True, "autoload_with": db.engine},)

    def __repr__(self):
        return self.ContractID

class Team(db.Model):
    __table__ = Base.metadata.tables["Team"]
    # __table__ = metadata.tables["Teams"]

    def __repr__(self):
        return self.TeamId