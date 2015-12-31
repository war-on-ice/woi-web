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
        if row["team"] not in results:
            results[row["team"]] = {}
        if row["season"] not in results[row["team"]]:
            results[row["team"]][row["season"]] = []
        results[row["team"]][row["season"]].append(row)
    for seasons in results["NSH"]:
        print results["NSH"][seasons]
    return results
