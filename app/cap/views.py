from flask import Blueprint

from app import app
from app import CapBase, Base
from app.cap.models import Contract, Player, Team
from app.gamesummary.models import RosterMaster
from flask import render_template
from sqlalchemy import desc
from app.navigation import setup_nav

from calls import get_r_seasons
from models import ContractHeader

import datetime

mod = Blueprint('cap', __name__, url_prefix='/cap')


@mod.route('')
def show_team_cap():
  rd = setup_nav()
  return render_template('cap/teamscap.html',
      rd=rd)

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
    caps = ContractHeader.query.filter(ContractHeader.ContractTeamID==teamId).order_by(desc(ContractHeader.EffectiveSeason))
    players = {}
    playerids = set()
    for cap in caps:
        if cap.PlayerID not in players:
            players[cap.PlayerID] = cap
            playerids.add(cap.PlayerID)

    rostermaster = {}
    rosterquery = RosterMaster.query.filter(Base.metadata.tables['rostermaster'].c["woi.id"].in_(playerids)).all()
    woiid = {}
    for p in rosterquery:
        player = {}
        player["woi.id"] = p.__dict__["woi.id"]
        if p.pos is not None:
            player["pos"] = p.pos
        else:
            player["pos"] = "F"
        player["full_name"] = p.last.title() + ", " + p.first.title()
        rostermaster[p.numfirstlast] = player
        woiid[player["woi.id"]] = player

    forwards = {}
    defensemen = {}
    goalies = {}
    gone = {}
    its = {}

    now = datetime.datetime.now()
    cy = now.year
    years = []
    while len(years) < 5:
        years.append(cy-1)
        cy += 1

    for player in players:
        if player in woiid and int(players[player].EffectiveSeason) + int(players[player].ContractLength) > years[0]:
            currplayer = {}
            currplayer["ID"] = player
            position = woiid[player]["pos"]
            if position == "D":
                defensemen[player] = currplayer
            elif position == "G":
                goalies[player] = currplayer
            else:
                forwards[player] = currplayer
    return render_template('cap/teamcap.html',
        teamId=teamId,
        rd=rd,
        woiid=woiid,
        forwards=forwards,
        years=years)
#
# @app.route('/team/<teamId>/<seasonId>/')
# def show_team_historical(teamId, seasonId):
#     selectedTeam = models.Teams.query.filter_by(TeamId=teamId).first()
#     return render_template('teamcap.html',
#                             team = selectedTeam)