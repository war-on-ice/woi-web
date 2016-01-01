from app.gamesummary.calls import row2dict


def percent(cf, ca):
    try:
        return round(float(cf) / (float(cf) + float(ca)) * 100.00, 2)
    except:
        return 0


def ratio(one, two):
    try:
        return round(float(one) / float(two) * 100.00, 2)
    except:
        return 0


def c_60(c, toi, games=1):
    try:
        return round(float(c) * (60 * games) / float(toi), 2)
    except:
        return 0


def calculate(teamrun, splitseasons=False):
    games = []
    allseasons = []
    compiled = {}
    for game in teamrun:
        td = row2dict(game)
        gs = {}
        gs["Gm"] = 1
        gs["Date"] = td["Date"]
        gs["Team"] = td["Team"]
        gs["season"] = str(td["season"]).split(".")[0]
        gs["TOI"] = float(td["TOI"]) # round(float(td["TOI"]) / 60.0, 2)
        gs["CF"] = float(td["CF"])
        gs["CA"] = float(td["CA"])
        gs["CF%"] = percent(gs["CF"], gs["CA"])
        gs["C+/-"] = gs["CF"] - gs["CA"]
        gs["SF"] = int(float(td["SF"]))
        gs["SA"] = int(float(td["SA"]))
        gs["SF%"] = percent(gs["SF"], gs["SA"])
        gs["S+/-"] = gs["SF"] - gs["SA"]
        gs["GF"] = int(td["GF"])
        gs["GA"] = int(td["GA"])
        gs["GF%"] = percent(gs["GF"], gs["GA"])
        gs["G+/-"] = int(gs["GF"] - gs["GA"])
        gs["CF%"] = percent(td["CF"], td["CA"])
        cf60 = c_60(td["CF"], gs["TOI"])
        ca60 = c_60(td["CA"], gs["TOI"])
        gs["CP60"] = round(cf60 + ca60, 2)
        gs["MSF"] = float(td["FF"]) - float(td["SF"])
        gs["FAC_WIN"] = float(td["FAC_WIN"])
        gs["FAC_LOSE"] = float(td["FAC_LOSE"])
        gs["ZSO"] = float(td["ZSO"])
        gs["ZSD"] = float(td["ZSD"])
        gs["ZSO%"] = percent(gs["ZSO"], gs["ZSD"])
        gs["HSCF"] = int(td["sSCF"])
        gs["HSCA"] = int(td["sSCA"])
        gs["HSCF%"] = percent(gs["HSCF"], gs["HSCA"])
        gs["HSC+/-"] = gs["HSCF"] - gs["HSCA"]
        gs["HSCF60"] = c_60(gs["HSCF"], gs["TOI"])
        gs["HSCA60"] = c_60(gs["HSCA"], gs["TOI"])
        gs["HSCP60"] = gs["HSCF60"] + gs["HSCA60"]
        gs["SCF"] = int(td["SCF"])
        gs["SCA"] = int(td["SCA"])
        gs["SCF%"] = percent(gs["SCF"], gs["SCA"])
        gs["SC+/-"] = gs["SCF"] - gs["SCA"]
        gs["SCF60"] = c_60(gs["SCF"], gs["TOI"])
        gs["SCA60"] = c_60(gs["SCA"], gs["TOI"])
        gs["SCP60"] = gs["SCF60"] + gs["SCA60"]
        gs["CF60"] = c_60(gs["CF"], gs["TOI"])
        gs["CA60"] = c_60(gs["CA"], gs["TOI"])
        gs["FF"] = int(float(td["FF"]))
        gs["FA"] = int(float(td["FA"]))
        gs["F+/-"] = gs["FF"] - gs["FA"]
        gs["FF%"] = percent(gs["FF"], gs["FA"])
        gs["FF60"] = c_60(gs["FF"], gs["TOI"])
        gs["FA60"] = c_60(gs["FA"], gs["TOI"])
        gs["FP60"] = gs["FF60"] + gs["FA60"]
        gs["MSF"] = gs["FF"] - gs["SF"]
        gs["MSA"] = gs["FA"] - gs["SA"]
        gs["BSF"] = gs["CF"] - gs["MSF"] - gs["SF"]
        gs["BSA"] = gs["CA"] - gs["MSA"] - gs["SA"]
        gs["SF60"] = c_60(gs["SF"], gs["TOI"])
        gs["SA60"] = c_60(gs["SA"], gs["TOI"])
        gs["GF60"] = c_60(gs["GF"], gs["TOI"])
        gs["GA60"] = c_60(gs["GA"], gs["TOI"])
        gs["FO_W"] = float(td["FAC_WIN"])
        gs["FO_L"] = float(td["FAC_LOSE"])
        gs["ZSO"] = float(td["ZSO"])
        gs["ZSN"] = float(td["ZSN"])
        gs["ZSD"] = float(td["ZSD"])
        gs["HIT"] = float(td["HIT"])
        gs["HIT-"] = float(td["HIT_TAKEN"])
        gs["PN-"] = float(td["PENL_DRAWN"])
        gs["PN"] = float(td["PENL_TAKEN"])
        gs["PenD"] = gs["PN-"] - gs["PN"]
        gs["OSh%"] = percent(gs["GF"], gs["SF"])
        gs["OFenSh%"] = percent(gs["GF"], gs["FF"])
        gs["FenSv%"] = 100 - percent(gs["GA"], gs["FA"])
        gs["OCOn%"] = ratio(gs["SF"], gs["CF"])
        gs["OFOn%"] = percent(gs["SF"], gs["MSF"])
        gs["OSh%"] = ratio(gs["GF"], gs["SF"])
        gs["OSv%"] = 100.00 - ratio(gs["GA"], gs["SA"])
        gs["PDO"] = round(gs["OSv%"] + gs["OSh%"], 2)
        gs["FO%"] = percent(gs["FAC_WIN"], gs["FAC_LOSE"])
        games.append(gs)
        if gs["Team"] not in compiled and gs["Team"] != "PHX":
            compiled[gs["Team"]] = []
        elif gs["Team"] == "PHX":
            if "ARI" not in compiled:
                compiled["ARI"] = []
            compiled["ARI"].append(gs)
        if gs["Team"] != "PHX":
            compiled[gs["Team"]].append(gs)

    if splitseasons is True:
        seasondates = set()
        for team in compiled:
            seasondates.update([x["season"] for x in compiled[team]])
        byseason = {}
        for tname in compiled:
            teamlist = compiled[tname]
            for team in teamlist:
                if team["season"] not in byseason:
                    byseason[team["season"]] = {}
                if tname not in byseason[team["season"]]:
                    byseason[team["season"]][tname] = []
                byseason[team["season"]][tname].append(team)
        for season in byseason:
            allseasons.extend(get_team_data(byseason[season]))
    else:
        allseasons.extend(get_team_data(compiled))
    return games, allseasons


def get_team_data(compiled):
    tc = []
    for team in compiled:
        gs = {}
        td = compiled[team]
        gs["Gm"] = len(td)
        gs["Team"] = team
        gs["CF"] = sum([x["CF"] for x in td])
        gs["CA"] = sum([x["CA"] for x in td])
        gs["CF%"] = percent(gs["CF"], gs["CA"])
        gs["C+/-"] = gs["CF"] - gs["CA"]
        gs["TOI"] = sum(x["TOI"] for x in td)
        seasons = sorted(set([x["season"] for x in td]))
        if len(seasons) == 1:
            gs["season"] = seasons[0]
        else:
            gs["season"] = seasons[0] + "-" + seasons[-1]
        gs["GF"] = sum([x["GF"] for x in td])
        gs["GA"] = sum([x["GA"] for x in td])
        gs["G+/-"] = int(gs["GF"] - gs["GA"])
        gs["ZSO"] = sum([x["ZSO"] for x in td])
        gs["ZSD"] = sum([x["ZSD"] for x in td])
        gs["CF%"] = percent(gs["CF"], gs["CA"])
        gs["CP60"] =  round(sum([x["CP60"] for x in td]) / len(td), 2)
        gs["OFOn%"] = percent(sum([x["SF"] for x in td]),
            sum([x["MSF"] for x in td]))
        gs["OSh%"] = ratio(sum([x["GF"] for x in td]), sum([x["SF"] for x in td]))
        gs["OSv%"] = 100.00 - ratio(sum([x["GA"] for x in td]), sum([x["SA"] for x in td]))
        gs["PDO"] = round(gs["OSv%"] + gs["OSh%"], 2)
        gs["FO%"] = percent(sum([x["FAC_WIN"] for x in td]), sum([x["FAC_LOSE"] for x in td]))
        gs["HSCF"] = sum([x["HSCF"] for x in td])
        gs["HSCA"] = sum([x["HSCA"] for x in td])
        gs["HSCF%"] = percent(gs["HSCF"], gs["HSCA"])
        gs["HSC+/-"] = gs["HSCF"] - gs["HSCA"]
        gs["HSCF60"] = round(sum([x["HSCF60"] for x in td]) / len(td), 2)
        gs["HSCA60"] = round(sum([x["HSCA60"] for x in td]) / len(td), 2)
        gs["HSCP60"] = gs["HSCF60"] + gs["HSCA60"]
        gs["SCF"] = sum([x["SCF"] for x in td])
        gs["SCA"] = sum([x["SCA"] for x in td])
        gs["SCF%"] = percent(gs["SCF"], gs["SCA"])
        gs["SC+/-"] = gs["SCF"] - gs["SCA"]
        gs["SCF60"] = round(sum([x["SCF60"] for x in td]) / len(td), 2)
        gs["SCA60"] = round(sum([x["SCA60"] for x in td]) / len(td), 2)
        gs["SCP60"] = gs["SCF60"] + gs["SCA60"]
        gs["CF60"] = round(sum([x["CF60"] for x in td]) / len(td), 2)
        gs["CA60"] = round(sum([x["CA60"] for x in td]) / len(td), 2)
        gs["FF"] = sum([x["FF"] for x in td])
        gs["FA"] = sum([x["FA"] for x in td])
        gs["F+/-"] = gs["FF"] - gs["FA"]
        gs["FF60"] = round(sum([x["FF60"] for x in td]) / len(td), 2)
        gs["FA60"] = round(sum([x["FA60"] for x in td]) / len(td), 2)
        gs["FP60"] = gs["FF60"] + gs["FA60"]
        gs["FF%"] = percent(gs["FF"], gs["FA"])
        gs["MSF"] = sum([x["MSF"] for x in td])
        gs["MSA"] = sum([x["MSA"] for x in td])
        gs["BSF"] = sum([x["BSF"] for x in td])
        gs["BSA"] = sum([x["BSA"] for x in td])
        gs["SF"] = sum([x["SF"] for x in td])
        gs["SA"] = sum([x["SA"] for x in td])
        gs["SF%"] = percent(gs["SF"], gs["SA"])
        gs["S+/-"] = gs["SF"] - gs["SA"]
        gs["SF60"] = round(sum([x["SF60"] for x in td]) / len(td), 2)
        gs["SA60"] = round(sum([x["SA60"] for x in td]) / len(td), 2)
        gs["GF"] = sum([x["GF"] for x in td])
        gs["GA"] = sum([x["GA"] for x in td])
        gs["GF%"] = percent(gs["GF"], gs["GA"])
        gs["GF60"] = round(sum([x["GF60"] for x in td]) / len(td), 2)
        gs["GA60"] = round(sum([x["GA60"] for x in td]) / len(td), 2)
        gs["FO_W"] = sum([x["FO_W"] for x in td])
        gs["FO_L"] = sum([x["FO_L"] for x in td])
        gs["ZSO"] = sum([x["ZSO"] for x in td])
        gs["ZSN"] = sum([x["ZSN"] for x in td])
        gs["ZSD"] = sum([x["ZSD"] for x in td])
        gs["ZSO%"] = percent(gs["ZSO"], gs["ZSD"])
        gs["HIT"] = sum([x["HIT"] for x in td])
        gs["HIT-"] = sum([x["HIT-"] for x in td])
        gs["PN-"] = sum([x["PN-"] for x in td])
        gs["PN"] = sum([x["PN"] for x in td])
        gs["PenD"] = gs["PN-"] - gs["PN"]
        gs["OSh%"] = percent(gs["GF"], gs["SF"])
        gs["OFenSh%"] = percent(gs["GF"], gs["FF"])
        gs["FenSv%"] = 100 - percent(gs["GA"], gs["FA"])
        gs["OCOn%"] = ratio(gs["SF"], gs["CF"])
        tc.append(gs)
    return tc
