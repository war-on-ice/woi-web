


def get_db_game_summary():
    # Get GamesTest information
    gamedata = GamesTest.query.filter_by(season=season,
        gcode=int(gcode)).first()
    # See if teamruns exists. If it doesn't, the game hasn't started or it's live
    teamruns = TeamRun.query.filter_by(season=season,
        gcode=int(gcode),
        scorediffcat=scorediffcat,
        gamestate=gamestate)\
        .filter(Base.metadata.tables["teamrun"].c.period.in_(period))\
        .order_by(TeamRun.TOI).all()
    # Determine if we need to get live data
    live = False
    if len(teamruns) == 0:
        live = True
        playbyplay = PlayByPlay.query.filter_by(season=season,
            gcode=int(gcode)).all()
        print len(playbyplay)
        print playbyplay
    finalteams = []
    teams = set()
    examine = len(teamruns)
    while len(finalteams) < 2:
        if examine == 0:
            break
        examine -= 1
        tr = teamruns[examine]
        if tr.Team not in teams:
            finalteams.append(tr)
            teams.add(tr.Team)

    teamruns = finalteams
    teamsummaries = []
    for td in teamruns:
        team = {}
        team["team"] = td.Team
        team["gf"] = int(td.GF)
        team["sf"] = int(td.SF)
        team["msf"] = int(td.FF) - int(td.SF)
        team["cf"] = int(td.CF)
        team["bsf"] = team["cf"] - team["msf"] - team["sf"]
        team["scf"] = int(td.SCF)
        team["hscf"] = int(td.sSCF)
        team["zso"] = int(td.ZSO)
        team["hit"] = int(td.HIT)
        team["pn"] = int(td.PENL_TAKEN)
        team["fo_w"] = int(td.FAC_WIN)
        team["toi"] = float(td.TOI) # round(float(td.TOI) / 60.0, 1)
        teamsummaries.append(team)

    goalieruns = GoalieRun.query.filter_by(season=season,
        gcode=int(gcode),
        scorediffcat=scorediffcat,
        gamestate=gamestate)\
        .filter(Base.metadata.tables["goalierun"].c.period.in_(period))\
        .order_by(GoalieRun.TOI).all()
    goalies = []
    foundgoalies = set()
    for td in reversed(goalieruns):
        if td.ID not in foundgoalies:
            foundgoalies.add(td.ID)
            goalie = {}
            goalie["name"] = td.ID
            goalie["team"] = td.Team
            goalie["gu"] = td.__dict__["goals.0"]
            goalie["su"] = td.__dict__["shots.0"]
            goalie["gl"] = td.__dict__["goals.1"]
            goalie["sl"] = td.__dict__["shots.1"]
            goalie["gm"] = td.__dict__["goals.2"]
            goalie["sm"] = td.__dict__["shots.2"]
            goalie["gh"] = td.__dict__["goals.3"] + td.__dict__["goals.4"]
            goalie["sh"] = td.__dict__["shots.3"] + td.__dict__["shots.4"]
            goalie["toi"] = float(td.TOI)  # round(float(td.TOI) / 60.0, 1)
            goalies.append(goalie)

    playerruns = PlayerRun.query.filter_by(season=season,
        gcode=int(gcode),
        scorediffcat=scorediffcat,
        gamestate=gamestate)\
        .order_by(PlayerRun.TOI).all()
    foundplayers = set()
    away = []
    home = []
    for td in reversed(playerruns):
        if td.ID not in foundplayers:
            foundplayers.add(td.ID)
            player = {}
            player["name"] = td.ID
            player["g"] = int(td.GOAL1 + td.GOAL2 + td.GOAL3 + td.GOAL4)
            player["a1"] = int(td.ASSIST)
            player["a2"] = int(td.ASSIST_2)
            player["p"] = player["g"] + player["a1"] + player["a2"]
            player["ihsc"] = int(td.isSC)
            player["isc"] = int(td.iSC)
            player["icf"] = int(td.SHOT + td.SHOT1 + td.SHOT2 + td.SHOT3 + td.SHOT4)
            player["cplusminus"] = int(td.CF - td.CA)
            player["fplusminus"] = int(td.FF - td.FA)
            player["gplusminus"] = int(td.GF - td.GA)
            player["cf"] = int(td.CF)
            player["ff"] = int(td.FF)
            player["zso"] = int(td.ZSO)
            player["zsd"] = int(td.ZSD)
            player["ab"] = int(td.BLOCKED_SHOT + td.BLOCKED_SHOT1 + td.BLOCKED_SHOT2 + td.BLOCKED_SHOT3 + td.BLOCKED_SHOT4)
            player["fo_w"] = int(td.FAC_WIN)
            player["fo_l"] = int(td.FAC_LOSE)
            player["hit"] = int(td.HIT)
            player["hitminus"] = int(td.HIT_TAKEN)
            player["pn"] = int(td.PENL_TAKEN)
            player["pnminus"] = int(td.PENL_DRAWN)
            player["toi"] = float(td.TOI) # round(float(td.TOI) / 60.0, 1)
            if td.home == 1:
                home.append(player)
            else:
                away.append(player)

    rostermaster = {}
    rosterquery = RosterMaster.query.filter(CapBase.metadata.tables['Player'].c["PlayerId"].in_(foundplayers)).all()
    woiid = {}
    for p in rosterquery:
        player = {}
        player["woi.id"] = p.__dict__["PlayerId"]
        player["pos"] = p.Position
        player["full_name"] = p.FullName
        woiid[player["woi.id"]] = player


def add2team(existing, newdata):
    existing["links"].append(newdata)
    return existing
