from datetime import date

from helper import get_rdata

import datetime

CORE_DATA = "http://data.war-on-ice.net/woi-common.RData"

def get_r_seasons():
    rdata = get_rdata(CORE_DATA)
    teamgames = {}
    keys = set()
    print rdata.keys()
    for roster in rdata["seasons"]:
        print roster
        for key in roster:
            keys.add(key)
    print keys
    return teamgames