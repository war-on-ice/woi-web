from app.constants import section_danger


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
