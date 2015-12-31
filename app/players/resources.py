import csv, urllib2


def get_csv(url):
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    results = []
    headers = []
    for row in cr:
        if len(headers) == 0:
            headers = row
        else:
            rowdict = {}
            for kint in xrange(len(row)):
                rowdict[headers[kint]] = row[kint]
            results.append(rowdict)
    return results


def combine_data(csv):
    results = {}
    for row in csv:
        if row["woi.id"] not in results:
            results[row["woi.id"]] = {}
        if row["season"] not in results[row["woi.id"]]:
            results[row["woi.id"]][row["season"]] = []
        results[row["woi.id"]][row["season"]].append(row)
    return results


def combine_seasons(csv):
    results = []
    keys = []
    od = ["", "session", "Name", "woi.id", "season", "ID", "team"]
    for player in csv:
        presults = {}
        for season in csv[player]:
            for ps in csv[player][season]:
                if ps["session"] != "Playoffs":
                    if len(presults) == 0:
                        keys = ps.keys()
                        for key in keys:
                            if key not in od:
                                presults[key] = []
                            else:
                                presults[key] = ps[key]
                    for key in presults:
                        if key not in od:
                            presults[key].append(float(ps[key]))
        for key in presults:
            if key not in od:
                presults[key] = reduce(lambda x, y: x + y, presults[key]) / len(presults[key])
        results.append(presults)
    # Find Missing Names
    roster = get_csv("http://war-on-ice.com/data/roster.unique.csv")
    found = {}
    for player in roster:
        found[player["woi.id"]] = {}
        found[player["woi.id"]]["Name"] = player["first"] + " " + player["last"]
        found[player["woi.id"]]["Position"] = player["pos"]
    for player in results:
        if player["Name"] == "NA" and player["woi.id"] in found:
            player["Name"] = found[player["woi.id"]]["Name"]
        if player["woi.id"] in found:
            player["Position"] = found[player["woi.id"]]["Position"]
    print results[0].keys()
    return results
