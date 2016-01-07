from app.constants import section_danger
from app.helpers import percent


def add2team(existing, newdata):
    existing["links"].append(newdata)
    return existing


def findPPGoal(eventcount, teampp, teamgoal):
    for pp in eventcount[teampp]:
        start = pp["seconds"]
        end = pp["seconds"] + pp["length"]
        for goal in eventcount[teamgoal]:
            if goal["seconds"] > start and goal["seconds"] < end:
                pp["length"] = goal["seconds"] - start
    return eventcount


def calc_sc(scs, play):
    if section_danger[play["new.loc.section"]] >= 2:
        scs.append({"seconds": play["seconds"], "value": len(scs)})
    return scs


def get_coplayers(rdata, coplayers={}):
    for play in rdata["coplayer"]:
        ckey = play["p1"] + "|" + play["p2"]
        if ckey not in coplayers:
            coplayers[ckey] = play
        else:
            for key in play:
                if key not in ["p1", "p2"]:
                    coplayers[ckey][key] += play[key]
    return coplayers


def get_hvh(coplayers, playerteams, woiid):
    coplayerlist = []
    coplayerdict = {}
    coplayerlinks = []
    hometeam = None
    awayteam = None
    for co in coplayers:
        matchup = coplayers[co]
        # Define each "Node" (player), and assign a value to them
        for p in ["p1", "p2"]:
            team = 0
            if matchup[p] not in coplayerdict:
                if hometeam is None and matchup[p] in playerteams:
                    hometeam = playerteams[matchup[p]]
                elif awayteam is None and matchup[p] in playerteams and hometeam != playerteams[matchup[p]]:
                    awayteam = playerteams[matchup[p]]
                if matchup[p] in playerteams and playerteams[matchup[p]] == hometeam:
                    team = 1
                if matchup[p] in playerteams:
                    coplayerlist.append({"name": matchup[p], "team": playerteams[matchup[p]], "rname": str(woiid[matchup[p]]["full_name"]), "group": team})
                    coplayerdict[matchup[p]] = len(coplayerlist) - 1
        if matchup["p1"] in playerteams and matchup["p2"] in playerteams:
            # Then create a link between these two with the corresponding values
            link = {}
            link["source"] = coplayerdict[matchup["p1"]]
            link["target"] = coplayerdict[matchup["p2"]]
            link["sourcename"] = matchup["p1"]
            link["targetname"] = matchup["p2"]
            link["TOI"] = matchup["el2"]
            link["evf"] = matchup["evf"]
            link["eva"] = matchup["eva"]
            link["cf%"] = percent(matchup["evf"], matchup["eva"])
            coplayerlinks.append(link)

    # Set up the 4 arrays for the co occurrency
    hvh = {"nodes": coplayerlist, "links": coplayerlinks}
    return hvh, hometeam, awayteam
