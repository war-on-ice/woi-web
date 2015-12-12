import urllib2
from rpy2.robjects import r
from rpy2.robjects import pandas2ri
import pandas as pd


def get_rdata(url):
    # For testing, probably want to do this a different way in production TODO
    response = urllib2.urlopen(url)
    html = response.read()
    fp = open("rdata" + url.replace("http://data.war-on-ice.net", "").replace("http://war-on-ice.com", ""), "w")
    fp.write(html)
    fp.close()
    robj = r.load("rdata" + url.replace("http://data.war-on-ice.net", "").replace("http://war-on-ice.com", ""))
    rdata = {}
    keys = {}
    for sets in robj:
        myRData = pandas2ri.ri2py(r[sets])
        rdata[sets] = []
        keys[sets] = set()
        # convert to DataFrame
        if not isinstance(myRData, pd.DataFrame):
            myRData = pd.DataFrame(myRData)
        for element in myRData:
            keys[sets].add(element)
            counter = 0
            for value in myRData[element]:
                if counter >= len(rdata[sets]):
                    rdata[sets].append({})
                rdata[sets][counter][element] = value
                counter += 1
    return rdata
